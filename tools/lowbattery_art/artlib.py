"""Tiny drawing toolkit for the low-battery artwork (1-bit, 480x640).

Two layers are drawn at 2x and reduced to 1x at the end:
  A  "ink": 0 = black, 255 = white (shapes are anti-aliased, then thresholded)
  T  "tone": 255 = none, lower values = gray, rendered with an ordered dither
Painting order works like paint: white clears both layers, a tone shape clears the ink below it and
sets the tone, black only touches the ink layer.
All coordinates are given in final (1x) pixels.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 480, 640
S = 2  # supersampling factor

FONT_BOLD = Path(__file__).resolve().parents[2] / "lib/EpdFont/builtinFonts/source/NotoSans/NotoSans-Bold.ttf"

BAYER8 = [
    [0, 32, 8, 40, 2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44, 4, 36, 14, 46, 6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [3, 35, 11, 43, 1, 33, 9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47, 7, 39, 13, 45, 5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21],
]

BLACK = "black"
WHITE = "white"


def tone(level):
    """level 0..1 = share of black dots (0 = nothing, 1 = solid black)."""
    return ("tone", level)


class Canvas:
    def __init__(self, seed=1):
        self.A = Image.new("L", (W * S, H * S), 255)
        self.T = Image.new("L", (W * S, H * S), 255)
        self.dA = ImageDraw.Draw(self.A)
        self.dT = ImageDraw.Draw(self.T)
        self.rng = random.Random(seed)

    # ---- low level -------------------------------------------------------------------------
    def _s(self, v):
        if isinstance(v, (list, tuple)):
            return [self._s(x) for x in v]
        return v * S

    def _paint(self, op, *args, **kw):
        """op is the name of an ImageDraw method; kw may contain fill=BLACK|WHITE|tone()."""
        fill = kw.pop("fill", BLACK)
        if fill == BLACK:
            getattr(self.dA, op)(*args, fill=0, **kw)
        elif fill == WHITE:
            getattr(self.dA, op)(*args, fill=255, **kw)
            getattr(self.dT, op)(*args, fill=255, **kw)
        else:
            level = fill[1]
            getattr(self.dA, op)(*args, fill=255, **kw)
            getattr(self.dT, op)(*args, fill=int(round(255 * (1 - level))), **kw)

    # ---- shapes ------------------------------------------------------------------------------
    def poly(self, pts, fill=BLACK):
        self._paint("polygon", [tuple(p) for p in self._s(pts)], fill=fill)

    def rect(self, x0, y0, x1, y1, fill=BLACK):
        self._paint("rectangle", self._s([x0, y0, x1, y1]), fill=fill)

    def rrect(self, x0, y0, x1, y1, r, fill=BLACK):
        self._paint("rounded_rectangle", self._s([x0, y0, x1, y1]), radius=r * S, fill=fill)

    def ellipse(self, x0, y0, x1, y1, fill=BLACK):
        self._paint("ellipse", self._s([x0, y0, x1, y1]), fill=fill)

    def circle(self, cx, cy, r, fill=BLACK):
        self.ellipse(cx - r, cy - r, cx + r, cy + r, fill)

    def line(self, pts, w=3, fill=BLACK, joint="curve"):
        self._paint("line", [tuple(p) for p in self._s(pts)], width=max(1, int(round(w * S))), joint=joint, fill=fill)

    def arc(self, box, a0, a1, w=3, fill=BLACK):
        self._paint("arc", self._s(box), start=a0, end=a1, width=int(round(w * S)), fill=fill)

    def outline_poly(self, pts, w=3, fill=BLACK):
        self.line(list(pts) + [pts[0]], w, fill)

    def ring(self, cx, cy, r, w=3, fill=BLACK):
        self.dA.ellipse(self._s([cx - r, cy - r, cx + r, cy + r]), outline=0 if fill == BLACK else 255, width=int(w * S))
        if fill == WHITE:
            self.dT.ellipse(self._s([cx - r, cy - r, cx + r, cy + r]), outline=255, width=int(w * S))

    def rframe(self, x0, y0, x1, y1, r, w=4):
        """Rounded-rectangle outline (does not touch the inside)."""
        self.dA.rounded_rectangle(self._s([x0, y0, x1, y1]), radius=r * S, outline=0, width=int(w * S))

    def text(self, xy, s, size=40, fill=BLACK, anchor="la"):
        font = ImageFont.truetype(str(FONT_BOLD), int(size * S))
        x, y = self._s(xy)
        self._paint("text", (x, y), s, font=font, anchor=anchor, fill=fill)

    def text_width(self, s, size):
        font = ImageFont.truetype(str(FONT_BOLD), int(size * S))
        return font.getlength(s) / S

    # ---- helpers for drawing --------------------------------------------------------------
    def wobble(self, pts, amp=1.4, step=7):
        """Hand-drawn look: resample a polyline and jitter every point a little."""
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for i in range(n):
                t = i / n
                out.append((x0 + (x1 - x0) * t + self.rng.uniform(-amp, amp),
                            y0 + (y1 - y0) * t + self.rng.uniform(-amp, amp)))
        out.append(pts[-1])
        return out

    def sketch_line(self, pts, w=3, amp=1.3):
        self.line(self.wobble(pts, amp), w)

    def sketch_poly(self, pts, w=3, fill=None, amp=1.3):
        if fill is not None:
            self.poly(pts, fill)
        self.line(self.wobble(list(pts) + [pts[0]], amp), w)

    def sketch_ellipse(self, box, w=3, fill=None, amp=1.2):
        x0, y0, x1, y1 = box
        cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
        pts = [(cx + rx * math.cos(a / 24 * 2 * math.pi), cy + ry * math.sin(a / 24 * 2 * math.pi)) for a in range(25)]
        if fill is not None:
            self.poly(pts[:-1], fill)
        self.line(self.wobble(pts, amp, 9), w)

    def hatch(self, pts, gap=6, angle=45, w=1.5, cross=False):
        """Fill a polygon with parallel lines (clipped to the polygon)."""
        mask = Image.new("L", (W * S, H * S), 0)
        ImageDraw.Draw(mask).polygon([tuple(p) for p in self._s(pts)], fill=255)
        lines = Image.new("L", (W * S, H * S), 0)
        dl = ImageDraw.Draw(lines)
        for ang in ([angle, angle + 90] if cross else [angle]):
            a = math.radians(ang)
            dx, dy = math.cos(a), math.sin(a)
            nx, ny = -dy, dx
            diag = math.hypot(W, H)
            k = -diag
            while k < diag:
                cx, cy = W / 2 + nx * k, H / 2 + ny * k
                dl.line([(cx - dx * diag) * S, (cy - dy * diag) * S, (cx + dx * diag) * S, (cy + dy * diag) * S],
                        fill=255, width=max(1, int(w * S)))
                k += gap
        inked = Image.composite(lines, Image.new("L", lines.size, 0), mask)
        self.A.paste(0, mask=inked)

    def lines_in(self, pts, polylines, w=2.0, color=0):
        """Draw polylines clipped to a polygon (ink on the ink layer)."""
        mask = Image.new("L", (W * S, H * S), 0)
        ImageDraw.Draw(mask).polygon([tuple(p) for p in self._s(pts)], fill=255)
        layer = Image.new("L", (W * S, H * S), 0)
        dl = ImageDraw.Draw(layer)
        for pl in polylines:
            dl.line([tuple(p) for p in self._s(pl)], fill=255, width=max(1, int(w * S)), joint="curve")
        inked = Image.composite(layer, Image.new("L", layer.size, 0), mask)
        self.A.paste(color, mask=inked)

    def dots(self, pts, gap=6, r=1.3):
        """Halftone dots clipped to a polygon."""
        mask = Image.new("L", (W * S, H * S), 0)
        ImageDraw.Draw(mask).polygon([tuple(p) for p in self._s(pts)], fill=255)
        layer = Image.new("L", (W * S, H * S), 0)
        dl = ImageDraw.Draw(layer)
        row = 0
        y = 0
        while y < H:
            x = (gap / 2) * (row % 2)
            while x < W:
                dl.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=255)
                x += gap
            y += gap * 0.87
            row += 1
        inked = Image.composite(layer, Image.new("L", layer.size, 0), mask)
        self.A.paste(0, mask=inked)

    def stars(self, count, box, rmax=2.2, avoid=None):
        x0, y0, x1, y1 = box
        for _ in range(count):
            x, y = self.rng.uniform(x0, x1), self.rng.uniform(y0, y1)
            r = self.rng.choice([0.9, 1.2, 1.6, rmax])
            self.circle(x, y, r)
            if r >= rmax - 0.01:
                self.line([(x - 5, y), (x + 5, y)], 1.2)
                self.line([(x, y - 5), (x, y + 5)], 1.2)

    def bolt(self, cx, cy, h, w=None, fill=BLACK):
        w = w or h * 0.55
        pts = [(cx + w * 0.10, cy - h / 2), (cx - w * 0.50, cy + h * 0.06), (cx - w * 0.05, cy + h * 0.06),
               (cx - w * 0.15, cy + h / 2), (cx + w * 0.50, cy - h * 0.10), (cx + w * 0.05, cy - h * 0.10)]
        self.poly(pts, fill)

    def battery(self, x, y, w, h, level, line=6, nub=None, round_r=None, fill_tone=None):
        """Classic battery icon with a fill level 0..1 (inside area is white)."""
        nub = nub or h * 0.4
        r = round_r if round_r is not None else min(h * 0.18, 18)
        self.rrect(x, y, x + w, y + h, r, BLACK)
        self.rrect(x + line, y + line, x + w - line, y + h - line, max(1, r - line * 0.6), WHITE)
        self.rrect(x + w - 2, y + (h - nub) / 2, x + w + line * 1.6, y + (h + nub) / 2, 3, BLACK)
        if level > 0:
            inner = w - 2 * (line + 5)
            fw = max(6, inner * level)
            self.rect(x + line + 5, y + line + 5, x + line + 5 + fw, y + h - line - 5, fill_tone or BLACK)

    def battery_v(self, x, y, w, h, level, line=6, fill_tone=None, nub_w=None, nub_h=22):
        """Upright battery (nub on top), x,y = top-left of the body, level 0..1 fills from the bottom."""
        nub_w = nub_w or w * 0.4
        r = min(w * 0.16, 22)
        self.rrect(x, y, x + w, y + h, r, BLACK)
        self.rrect(x + line, y + line, x + w - line, y + h - line, max(1, r - line * 0.6), WHITE)
        self.rrect(x + (w - nub_w) / 2, y - nub_h, x + (w + nub_w) / 2, y + 4, 5, BLACK)
        if level > 0:
            fh = max(8, (h - 2 * (line + 5)) * level)
            self.rect(x + line + 5, y + h - line - 5 - fh, x + w - line - 5, y + h - line - 5, fill_tone or BLACK)

    def face(self, cx, cy, s, mood="sad", dx=None, brows=True):
        """Cartoon face centred at cx, cy. s ~ half the eye distance. mood: sad | sleep | dead | happy | scream |
        tired | worried | angry | cool."""
        dx = dx or s * 0.62
        er = s * 0.36
        lw = max(2.5, s * 0.12)
        for sgn in (-1, 1):
            ex = cx + sgn * dx
            if mood == "sleep":
                self.arc([ex - er, cy - er * 0.7, ex + er, cy + er * 0.9], 20, 160, w=lw)
            elif mood == "dead":
                self.line([(ex - er * .8, cy - er * .8), (ex + er * .8, cy + er * .8)], lw * 1.2)
                self.line([(ex - er * .8, cy + er * .8), (ex + er * .8, cy - er * .8)], lw * 1.2)
            elif mood == "cool":
                self.rrect(ex - er * 1.25, cy - er * 0.7, ex + er * 1.25, cy + er * 0.7, 6, BLACK)
            else:
                self.circle(ex, cy, er, WHITE)
                self.ring(ex, cy, er, lw)
                look = {"sad": (0, 0.35), "tired": (0, 0.45), "worried": (-sgn * 0.25, 0.2), "angry": (sgn * -0.1, 0.1)}.get(mood, (0.1, 0.1))
                self.circle(ex + look[0] * er, cy + look[1] * er, er * 0.5)
                self.circle(ex + look[0] * er - er * 0.14, cy + look[1] * er - er * 0.16, er * 0.15, WHITE)
                if mood == "tired":
                    self.poly([(ex - er - 2, cy - er - 2), (ex + er + 2, cy - er - 2), (ex + er + 2, cy - er * 0.05), (ex - er - 2, cy - er * 0.05)], WHITE)
                    self.line([(ex - er - 3, cy - er * 0.05), (ex + er + 3, cy - er * 0.05)], lw)
                    self.arc([ex - er, cy + er * 0.2, ex + er, cy + er * 1.9], 20, 160, w=lw * 0.7)
            if brows and mood in ("sad", "worried"):
                self.line([(ex - sgn * er * 1.3, cy - er * 1.2), (ex + sgn * er * 1.1, cy - er * 1.9)] if sgn < 0 else
                          [(ex - sgn * er * 1.3, cy - er * 1.2), (ex + sgn * er * 1.1, cy - er * 1.9)], lw)
            if brows and mood == "angry":
                self.line([(ex - sgn * er * 1.4, cy - er * 1.9), (ex + sgn * er * 0.8, cy - er * 1.1)], lw * 1.3)
        my = cy + s * 1.0
        if mood in ("sad", "tired", "worried"):
            self.arc([cx - s * 0.5, my - s * 0.05, cx + s * 0.5, my + s * 0.75], 205, 335, w=lw)
        elif mood in ("happy", "cool"):
            self.arc([cx - s * 0.65, my - s * 0.55, cx + s * 0.65, my + s * 0.45], 15, 165, w=lw)
        elif mood == "scream":
            self.ellipse(cx - s * 0.45, my - s * 0.25, cx + s * 0.45, my + s * 0.75)
        elif mood == "angry":
            self.line(self.wobble([(cx - s * 0.5, my + s * 0.3), (cx + s * 0.5, my + s * 0.3)], 2.5, 7), lw)
        elif mood == "sleep":
            self.line([(cx - s * 0.25, my + s * 0.15), (cx + s * 0.25, my + s * 0.15)], lw)
        elif mood == "dead":
            self.line([(cx - s * 0.45, my + s * 0.25), (cx - s * 0.15, my + s * 0.1), (cx + s * 0.15, my + s * 0.4),
                       (cx + s * 0.45, my + s * 0.25)], lw)

    def label(self, xy, s, size=30, anchor="ma", pad=8):
        """Text on a white plate with a thin outline, so it stays legible over tone."""
        w = self.text_width(s, size)
        x, y = xy
        if anchor == "ma":
            x0 = x - w / 2
        elif anchor == "ra":
            x0 = x - w
        else:
            x0 = x
        self.rrect(x0 - pad - 2, y - pad + 2, x0 + w + pad + 2, y + size * 1.25 + pad - 2, 10, BLACK)
        self.rrect(x0 - pad, y - pad + 4, x0 + w + pad, y + size * 1.25 + pad - 4, 8, WHITE)
        self.text((x0, y), s, size)

    def pixel_text(self, x, y, s, k=6):
        """Chunky 8-bit lettering: tiny bitmap font scaled up with nearest-neighbour blocks."""
        font = ImageFont.load_default()
        tmp = Image.new("L", (int(font.getlength(s)) + 2, 14), 0)
        ImageDraw.Draw(tmp).text((1, 0), s, font=font, fill=255)
        big = tmp.resize((tmp.width * k * S, tmp.height * k * S), Image.NEAREST)
        self.A.paste(0, (int(x * S), int(y * S)), big)
        return tmp.width * k

    def sprite(self, x, y, rows, k=8, fill=BLACK):
        """ASCII pixel art: '#' = ink, '.' = clear."""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    self.rect(x + i * k, y + j * k, x + (i + 1) * k, y + (j + 1) * k, fill)

    def bez(self, p0, p1, p2, n=14):
        return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                 (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]

    def speech(self, x0, y0, x1, y1, tail, w=4, r=18, think=False):
        """Rounded speech bubble; the pointer starts on the bottom edge and ends at tail."""
        cx = min(max(tail[0], x0 + 30), x1 - 30)
        self.rrect(x0 - w, y0 - w, x1 + w, y1 + w, r + w, BLACK)
        self.poly([(cx - 20 - w, y1 - 6), (tail[0], tail[1]), (cx + 8 + w, y1 - 6)], BLACK)
        self.rrect(x0, y0, x1, y1, r, WHITE)
        self.poly([(cx - 17, y1 - 8), (tail[0] + (cx - tail[0]) * 0.0 + 0.8, tail[1] - 4 - w * 0.4), (cx + 6, y1 - 8)], WHITE)

    def plug(self, x, y, size, angle=0, face=None):
        """Two-pin plug with its body; (x, y) = centre of the body. angle in degrees (0 = pins point right)."""
        a = math.radians(angle)
        ca, sa = math.cos(a), math.sin(a)

        def tr(px, py):
            return (x + px * ca - py * sa, y + px * sa + py * ca)

        body = [tr(-size * 0.6, -size * 0.45), tr(size * 0.25, -size * 0.45), tr(size * 0.25, size * 0.45),
                tr(-size * 0.6, size * 0.45)]
        self.poly(body, BLACK)
        inner = [tr(-size * 0.5, -size * 0.35), tr(size * 0.15, -size * 0.35), tr(size * 0.15, size * 0.35),
                 tr(-size * 0.5, size * 0.35)]
        self.poly(inner, WHITE)
        for sy in (-0.22, 0.22):
            self.line([tr(size * 0.25, size * sy), tr(size * 0.75, size * sy)], size * 0.13)
        return tr

    def cord(self, pts, w=5):
        """Smooth-ish cable through the given points (Catmull-Rom)."""
        out = []
        P = [pts[0]] + list(pts) + [pts[-1]]
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            for t in [k / 12 for k in range(12)]:
                t2, t3 = t * t, t * t * t
                out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                        + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
        out.append(pts[-1])
        self.line(out, w)
        return out

    def gear(self, cx, cy, r, teeth=10, hole=0.35, depth=0.22, rot=0, fill=BLACK, hole_fill=WHITE, spokes=0):
        pts = []
        n = teeth * 4
        for i in range(n):
            ang = rot + i / n * 2 * math.pi
            phase = i % 4
            rr = r if phase in (1, 2) else r * (1 - depth)
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        self.poly(pts, fill)
        if hole_fill is not None:
            self.circle(cx, cy, r * hole, hole_fill)
        if spokes:
            for k in range(spokes):
                ang = rot + k / spokes * 2 * math.pi
                self.line([(cx, cy), (cx + (r * (1 - depth) - 3) * math.cos(ang), cy + (r * (1 - depth) - 3) * math.sin(ang))],
                          r * 0.12, WHITE if fill == BLACK else BLACK)
            self.circle(cx, cy, r * 0.2, fill)
            self.circle(cx, cy, r * 0.08, WHITE if fill == BLACK else BLACK)

    def cloud(self, cx, cy, s, fill=WHITE, outline=3):
        """Puffy cloud; drawn as outline + white interior."""
        blobs = [(-0.9, 0.1, 0.55), (-0.35, -0.25, 0.7), (0.3, -0.2, 0.62), (0.85, 0.1, 0.5), (0.0, 0.15, 0.7)]
        for dx, dy, rr in blobs:
            self.circle(cx + dx * s, cy + dy * s, rr * s + outline, BLACK)
        for dx, dy, rr in blobs:
            self.circle(cx + dx * s, cy + dy * s, rr * s, fill)
        self.rect(cx - 1.2 * s, cy + 0.15 * s, cx + 1.3 * s, cy + 0.6 * s + outline, WHITE)

    def sweat(self, x, y, s=10):
        self.poly([(x, y - s * 1.3), (x - s * 0.7, y + s * 0.2), (x, y + s * 0.8), (x + s * 0.7, y + s * 0.2)], BLACK)
        self.circle(x - s * 0.15, y + s * 0.15, s * 0.22, WHITE)

    # ---- output ---------------------------------------------------------------------------------
    def render(self):
        ink = self.A.resize((W, H), Image.LANCZOS).point(lambda v: 0 if v < 140 else 255)
        tone_img = self.T.resize((W, H), Image.BOX)
        out = Image.new("1", (W, H), 1)
        ip, tp, op = ink.load(), tone_img.load(), out.load()
        for y in range(H):
            row = BAYER8[y % 8]
            for x in range(W):
                if ip[x, y] == 0:
                    op[x, y] = 0
                else:
                    darkness = (255 - tp[x, y]) / 255.0
                    if darkness > 0.02 and darkness * 64 > row[x % 8] + 0.5:
                        op[x, y] = 0
        return out
