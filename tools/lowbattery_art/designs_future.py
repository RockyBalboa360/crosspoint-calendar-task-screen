"""Pictures 1-4: the classic battery icon and three futuristic circuit-board scenes."""
import math

from artlib import BLACK, WHITE, W, H, Canvas, tone
from registry import design


def circuit_path(rng, x, y, dirx, length, bends=3):
    """A trace that leaves (x, y) horizontally in direction dirx and bends by 45 degrees a few times."""
    pts = [(x, y)]
    heading = 0.0
    for _ in range(bends):
        run = rng.uniform(length * 0.12, length * 0.3)
        x += dirx * run * math.cos(heading)
        y += run * math.sin(heading)
        pts.append((x, y))
        heading = rng.choice([-math.pi / 4, 0.0, math.pi / 4]) if heading == 0.0 else 0.0
        diag = rng.uniform(14, 40)
        x += dirx * diag * math.cos(heading)
        y += diag * math.sin(heading)
        pts.append((x, y))
    x += dirx * rng.uniform(length * 0.1, length * 0.25)
    pts.append((x, y))
    return pts


def node(c, x, y, r=7, color=WHITE, hole=BLACK):
    c.circle(x, y, r, color)
    c.circle(x, y, r * 0.45, hole)


@design("Classic battery", "Klassischer Akku", "classic")
def classic(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.05))
    c.ellipse(60, 500, 440, 560, tone(0.35))
    x0, y0, x1, y1 = 40, 210, 400, 430
    c.rrect(x0, y0, x1, y1, 48, BLACK)
    c.rrect(x0 + 28, y0 + 28, x1 - 28, y1 - 28, 26, WHITE)
    c.rrect(x1 - 4, y0 + 62, x1 + 46, y1 - 62, 20, BLACK)
    c.rrect(x0 + 44, y0 + 44, x0 + 96, y1 - 44, 14, BLACK)        # the last sliver of charge
    # lightning bolt with rounded corners
    bolt = [(250, 250), (200, 332), (240, 332), (214, 392), (292, 308), (250, 308), (276, 250)]
    c.poly(bolt, BLACK)
    for (x, y) in bolt:
        c.circle(x, y, 7, BLACK)
    c.line(bolt, 14, BLACK)
    for (x, y) in [(60, 130), (410, 150), (90, 520), (400, 540)]:
        c.line([(x - 16, y), (x + 16, y)], 5)
        c.line([(x, y - 16), (x, y + 16)], 5)


@design("Circuit HUD", "Schaltkreis-Anzeige", "future")
def circuit_hud(c: Canvas):
    rng = c.rng
    c.rect(0, 0, W, 640, BLACK)
    # traces left and right, mirrored
    for side in (-1, 1):
        for i in range(9):
            y = 120 + i * 52 + rng.uniform(-10, 10)
            x0 = 240 + side * 100
            path = circuit_path(rng, x0, y, side, 190, bends=rng.choice([2, 3]))
            c.line(path, 3, WHITE)
            node(c, path[-1][0], path[-1][1], 6)
    # battery outline (double line) with a nub
    c.rrect(150, 110, 330, 540, 30, WHITE)
    c.rrect(158, 118, 322, 532, 24, BLACK)
    c.rrect(166, 126, 314, 524, 20, WHITE)
    c.rrect(172, 132, 308, 518, 16, BLACK)
    c.rrect(205, 82, 275, 118, 8, WHITE)
    c.rrect(214, 90, 266, 118, 4, BLACK)
    # six segments, only the lowest is lit
    for k in range(6):
        top = 142 + k * 62
        if k == 5:
            c.rrect(184, top, 296, top + 50, 8, WHITE)
        else:
            c.rrect(184, top, 296, top + 50, 8, WHITE)
            c.rrect(188, top + 4, 292, top + 46, 5, BLACK)
            for gx in range(194, 290, 10):
                c.circle(gx, top + 25, 1.6, WHITE)
    c.text((364, 100), "+", 40, WHITE)
    c.text((364, 508), "-", 52, WHITE)
    c.rect(330, 130, 360, 134, WHITE) if False else None


@design("Holo battery", "Hologramm-Akku", "future")
def holo(c: Canvas):
    rng = c.rng
    c.rect(0, 0, W, 640, BLACK)
    cx, cy = 240, 470

    def iso(u, v):
        return (cx + (u - v) * 0.7071, cy + (u + v) * 0.7071 * 0.5)

    # glow on the board (white dots on black)
    c.ellipse(-20, 330, 500, 620, tone(0.8))
    c.ellipse(40, 380, 440, 580, tone(0.65))
    # traces on the board plane
    for corner in range(4):
        base = corner * math.pi / 2
        for k in range(5):
            off = (k - 2) * 26
            pts = []
            r = 120
            u, v = (r * math.cos(base) + off * -math.sin(base), r * math.sin(base) + off * math.cos(base))
            pts.append(iso(u, v))
            heading = base
            for step in range(rng.choice([2, 3])):
                run = rng.uniform(40, 110)
                u += run * math.cos(heading)
                v += run * math.sin(heading)
                pts.append(iso(u, v))
                heading = base + rng.choice([-math.pi / 4, 0, math.pi / 4])
                run = rng.uniform(20, 60)
                u += run * math.cos(heading)
                v += run * math.sin(heading)
                pts.append(iso(u, v))
                heading = base
            c.line(pts, 3, WHITE)
            x, y = pts[-1]
            c.ellipse(x - 7, y - 3.5, x + 7, y + 3.5, WHITE)
            c.ellipse(x - 3, y - 1.5, x + 3, y + 1.5, BLACK)
    # pad rings
    for rx, ry, w in [(112, 56, 5), (90, 45, 3), (68, 34, 3)]:
        c.ellipse(cx - rx, cy - ry, cx + rx, cy + ry, WHITE)
        c.ellipse(cx - rx + w, cy - ry + w / 2, cx + rx - w, cy + ry - w / 2, BLACK)
    # cylinder battery
    x0, x1, top, bottom = 175, 305, 120, 450
    c.rect(x0, top, x1, bottom, WHITE)
    c.ellipse(x0, bottom - 26, x1, bottom + 26, WHITE)
    c.ellipse(x0, top - 26, x1, top + 26, WHITE)
    c.rect(x0 + 6, top, x1 - 6, bottom, BLACK)
    c.ellipse(x0 + 6, bottom - 22, x1 - 6, bottom + 22, BLACK)
    c.ellipse(x0 + 6, top - 20, x1 - 6, top + 20, BLACK)
    c.ellipse(x0 + 28, top - 14, x1 - 28, top + 14, WHITE)
    c.ellipse(x0 + 38, top - 10, x1 - 38, top + 10, BLACK)
    c.rrect(222, top - 40, 258, top - 14, 6, WHITE)
    # segments: only the lowest band is filled
    for k in range(5):
        y = 180 + k * 54
        c.arc([x0 + 10, y - 22, x1 - 10, y + 22], 0, 180, w=3, fill=WHITE)
    c.rect(x0 + 10, 395, x1 - 10, bottom, WHITE)
    c.ellipse(x0 + 10, bottom - 22, x1 - 10, bottom + 22, WHITE)
    c.ellipse(x0 + 10, 373, x1 - 10, 417, WHITE)
    c.ellipse(x0 + 16, 379, x1 - 16, 411, BLACK) if False else None
    # lightning bolt in front, with a dark edge
    bolt = [(262, 260), (228, 350), (256, 350), (232, 440), (298, 330), (268, 330), (288, 260)]
    c.line(bolt + [bolt[0]], 12, BLACK)
    c.poly(bolt, WHITE)
    c.line(bolt + [bolt[0]], 3, BLACK)


@design("Cyber cylinder", "Cyber-Zelle", "future")
def cyber_cell(c: Canvas):
    rng = c.rng
    c.rect(0, 0, W, 640, tone(0.04))
    for _ in range(70):
        x, y = rng.uniform(10, 470), rng.uniform(10, 330)
        s = rng.choice([3, 4, 5])
        c.rect(x, y, x + s, y + s, BLACK)
    # floor grid in perspective
    horizon = 380
    c.rect(0, horizon, W, 640, tone(0.1))
    c.line([(0, horizon), (W, horizon)], 4)
    for k in range(1, 9):
        y = horizon + (k ** 1.7) * 6
        if y < 640:
            c.line([(0, y), (W, y)], 2)
    for k in range(-8, 9):
        c.line([(240 + k * 14, horizon), (240 + k * 80, 640)], 2)
    # reflection of the cylinder: dithered bands that fade out
    x0, x1 = 165, 315
    for i, level in enumerate([0.42, 0.32, 0.22, 0.14, 0.08]):
        y = 420 + i * 36
        c.rect(x0, y, x1, y + 36, tone(level))
    # circuit traces on the floor, left and right of the base
    for side in (-1, 1):
        for i in range(6):
            y = 418 + i * 14
            x = 240 + side * 98
            n1 = rng.uniform(26, 56)
            n2 = rng.uniform(16, 30)
            n3 = rng.uniform(30, 70)
            pts = [(x, y), (x + side * n1, y), (x + side * (n1 + n2), y + rng.choice([-1, 1]) * n2), (x + side * (n1 + n2 + n3), y + 0)]
            pts[-1] = (pts[-1][0], pts[-2][1])
            c.line(pts, 3)
            c.circle(pts[-1][0], pts[-1][1], 5)
            c.circle(pts[-1][0], pts[-1][1], 2, WHITE)
    # cylinder
    top, bottom = 90, 408
    body = [(x0, top), (x1, top), (x1, bottom), (x0, bottom)]
    c.rect(x0 - 4, top, x1 + 4, bottom, BLACK)
    c.ellipse(x0 - 4, bottom - 24, x1 + 4, bottom + 24, BLACK)
    c.ellipse(x0 - 4, top - 24, x1 + 4, top + 24, BLACK)
    c.rect(x0, top, x1, bottom, WHITE)
    c.ellipse(x0, bottom - 21, x1, bottom + 21, WHITE)
    c.ellipse(x0, top - 21, x1, top + 21, WHITE)
    # circuit skin (orthogonal lines clipped to the body)
    lines = []
    for i in range(14):
        x = x0 + 8 + i * 10.5
        y0 = top + rng.uniform(0, 60)
        lines.append([(x, y0), (x, y0 + rng.uniform(60, 200))])
    for i in range(16):
        y = top + 20 + i * 19
        xs = x0 + rng.uniform(0, 40)
        lines.append([(xs, y), (xs + rng.uniform(40, 120), y)])
    c.lines_in([(x0, top), (x1, top), (x1, bottom), (x0, bottom)], lines, 2.2)
    c.hatch([(x1 - 40, top), (x1, top), (x1, bottom), (x1 - 40, bottom)], gap=5, angle=60, w=1.5)
    c.rect(x0, 330, x1, bottom, tone(0.55))
    c.ellipse(x0, bottom - 21, x1, bottom + 21, tone(0.55))
    c.line([(x0 - 4, top), (x0 - 4, bottom)], 5)
    c.line([(x1 + 4, top), (x1 + 4, bottom)], 5)
    c.arc([x0 - 4, bottom - 24, x1 + 4, bottom + 24], 0, 180, w=5)
    # top cap
    c.ellipse(x0 - 4, top - 24, x1 + 4, top + 24, BLACK)
    c.ellipse(x0 + 14, top - 15, x1 - 14, top + 15, WHITE)
    c.ellipse(x0 + 44, top - 9, x1 - 44, top + 9, BLACK)
    c.rrect(222, top - 38, 258, top - 12, 5, BLACK)
    c.bolt(300, 300, 76, fill=BLACK)
