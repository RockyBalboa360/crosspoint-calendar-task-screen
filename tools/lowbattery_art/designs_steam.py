"""Pictures 14-16: steampunk (brass, gears, pipes, rivets)."""
import math

from artlib import BLACK, WHITE, W, H, Canvas, tone
from registry import design


def rivets(c, pts, r=4):
    for x, y in pts:
        c.circle(x, y, r, BLACK)
        c.circle(x - r * 0.25, y - r * 0.25, r * 0.4, WHITE)


def ring_rivets(c, cx, cy, rad, n, r=4):
    rivets(c, [(cx + rad * math.cos(i / n * 2 * math.pi), cy + rad * math.sin(i / n * 2 * math.pi)) for i in range(n)], r)


def frame(c, w=7):
    """Double rivetted border; call it LAST so that content sticking out is covered."""
    for x0, y0, x1, y1 in [(0, 0, W, 22), (0, H - 22, W, H), (0, 0, 22, H), (W - 22, 0, W, H)]:
        c.rect(x0, y0, x1, y1, WHITE)
    c.rframe(10, 10, W - 10, H - 10, 26, 9)
    c.rframe(26, 26, W - 26, H - 26, 16, 4)
    for (x, y) in [(40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)]:
        c.circle(x, y, 13, WHITE)
        c.circle(x, y, 13, BLACK)
        c.circle(x, y, 8, WHITE)
        c.circle(x, y, 3, BLACK)


def valve(c, cx, cy, r):
    c.circle(cx, cy, r, BLACK)
    c.circle(cx, cy, r - 6, WHITE)
    for k in range(4):
        a = k * math.pi / 4
        c.line([(cx - math.cos(a) * (r - 3), cy - math.sin(a) * (r - 3)), (cx + math.cos(a) * (r - 3), cy + math.sin(a) * (r - 3))], 5)
    c.circle(cx, cy, 8, BLACK)
    c.circle(cx, cy, 3, WHITE)


def pipe(c, pts, w=22):
    c.line(pts, w + 8, BLACK)
    c.line(pts, w, WHITE)
    c.line([(x - 2, y - 3) for x, y in pts], 4, tone(0.55))


def flange(c, x, y, horizontal, w=22):
    if horizontal:
        c.rrect(x - 7, y - w / 2 - 8, x + 7, y + w / 2 + 8, 3, BLACK)
    else:
        c.rrect(x - w / 2 - 8, y - 7, x + w / 2 + 8, y + 7, 3, BLACK)


@design("Pressure gauge", "Druckmesser", "steam")
def gauge(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.12))
    # big gear behind the gauge
    c.gear(380, 450, 105, teeth=14, hole=0.4, depth=0.18, spokes=6, rot=0.2)
    c.gear(100, 520, 60, teeth=9, hole=0.35, depth=0.2, spokes=4, rot=0.4)
    # pipes + boiler
    pipe(c, [(240, 380), (240, 470)], 26)
    c.rrect(130, 450, 350, 590, 26, BLACK)
    c.rrect(138, 458, 342, 582, 20, WHITE)
    c.hatch([(138, 530), (342, 530), (342, 582), (138, 582)], gap=7, angle=-30, w=2)
    for x in (185, 295):
        c.rect(x - 6, 458, x + 6, 582, BLACK)
    rivets(c, [(x, y) for x in (185, 295) for y in (475, 520, 565)] + [(160, 470), (320, 470), (160, 570), (320, 570)])
    pipe(c, [(350, 520), (410, 520), (410, 330)], 20)
    flange(c, 410, 425, False, 20)
    valve(c, 410, 300, 28)
    pipe(c, [(130, 520), (70, 520), (70, 380)], 20)
    flange(c, 70, 450, False, 20)
    c.circle(70, 345, 24, BLACK)
    c.circle(70, 345, 17, WHITE)
    c.line([(70, 345), (80, 332)], 3)
    # steam
    c.cloud(425, 235, 32, WHITE, 4)
    c.cloud(455, 175, 24, WHITE, 4)
    c.cloud(60, 285, 26, WHITE, 4)
    # the gauge
    cx, cy, R = 240, 230, 150
    c.circle(cx, cy, R + 12, BLACK)
    c.circle(cx, cy, R, WHITE)
    c.circle(cx, cy, R - 10, tone(0.4))
    c.circle(cx, cy, R - 22, WHITE)
    ring_rivets(c, cx, cy, R - 5, 12, 4)
    start, sweep = 150, 240
    # empty zone (hatched wedge)
    wedge = [(cx, cy)] + [(cx + (R - 28) * math.cos(math.radians(start + t)), cy + (R - 28) * math.sin(math.radians(start + t))) for t in range(0, 62, 4)]
    c.poly(wedge, WHITE)
    c.hatch(wedge, gap=6, angle=45, w=2.2)
    for i in range(0, 25):
        a = math.radians(start + i * sweep / 24)
        l = 18 if i % 4 == 0 else 9
        c.line([(cx + (R - 30) * math.cos(a), cy + (R - 30) * math.sin(a)), (cx + (R - 30 - l) * math.cos(a), cy + (R - 30 - l) * math.sin(a))], 3 if i % 4 == 0 else 2)
    c.text((cx - 100, cy + 55), "E", 36, anchor="ma")
    c.text((cx + 100, cy + 55), "F", 36, anchor="ma")
    c.text((cx, cy - 98), "PSI", 22, anchor="ma")
    na = math.radians(start + 6)
    c.poly([(cx + 8 * math.cos(na + 1.57), cy + 8 * math.sin(na + 1.57)), (cx + (R - 36) * math.cos(na), cy + (R - 36) * math.sin(na)),
            (cx + 8 * math.cos(na - 1.57), cy + 8 * math.sin(na - 1.57))], BLACK)
    c.circle(cx, cy, 14, BLACK)
    c.circle(cx, cy, 6, WHITE)
    c.arc([cx - R + 30, cy - R + 30, cx + R - 30, cy + R - 30], 200, 250, w=5, fill=WHITE) if False else None
    c.arc([cx - 100, cy - 100, cx + 100, cy + 100], 255, 300, w=5, fill=WHITE)
    c.label((240, 600), "LOW", 28) if False else None
    frame(c)


@design("Airship", "Luftschiff", "steam")
def airship(c: Canvas):
    for i in range(8):
        c.rect(0, i * 80, W, i * 80 + 80, tone(0.24 - i * 0.03))
    for (x, y, s) in [(80, 120, 38), (400, 90, 30), (110, 500, 44), (390, 540, 36)]:
        c.cloud(x, y, s, WHITE, 4)
    c.circle(410, 190, 0, BLACK)
    # envelope
    c.ellipse(40, 150, 420, 360, BLACK)
    c.ellipse(48, 158, 412, 352, WHITE)
    c.hatch([(48, 255), (412, 255), (385, 330), (300, 352), (180, 352), (80, 330)], gap=8, angle=-35, w=2.2)
    for x in range(100, 420, 50):
        c.arc([x - 40, 150, x + 40, 360], 100, 260, w=3) if False else c.line(c.bez((x, 158), (x + (x - 240) * 0.22, 255), (x, 352), 12), 3)
    c.line([(48, 255), (432, 255)], 3) if False else None
    rivets(c, [(x, 255) for x in range(70, 420, 38)], 3)
    c.battery(165, 203, 150, 62, 0.06, line=7)      # emblem on the envelope
    # tail fins and propeller
    c.poly([(395, 205), (440, 165), (440, 205), (418, 255)], BLACK)
    c.poly([(395, 305), (440, 345), (440, 305), (418, 255)], BLACK)
    c.circle(430, 255, 9, BLACK)
    for k in range(3):
        a = k * 2.094 + 0.3
        c.line([(430, 255), (430 + 32 * math.cos(a), 255 + 32 * math.sin(a))], 7)
    # struts + gondola
    for x in (150, 240, 330):
        c.line([(x, 345), (x, 395)], 5)
    c.rrect(110, 390, 370, 470, 20, BLACK)
    c.rrect(118, 398, 362, 462, 15, WHITE)
    for x in (150, 215, 280, 335):
        c.circle(x, 430, 17, BLACK)
        c.circle(x, 430, 11, WHITE)
        c.line([(x - 11, 430), (x + 11, 430)], 2)
    c.line([(110, 470), (370, 470)], 5)
    rivets(c, [(x, 475) for x in range(125, 370, 30)], 3)
    # chimney with steam
    c.rect(300, 365, 322, 392, BLACK)
    c.cloud(318, 335, 20, WHITE, 3)
    # rope ladder + gear
    c.line([(150, 470), (150, 560)], 4)
    c.line([(190, 470), (190, 560)], 4)
    for y in range(485, 560, 18):
        c.line([(150, y), (190, y)], 4)
    c.gear(88, 470, 38, teeth=9, hole=0.4, spokes=4)
    # fuel tank with gauge below the gondola
    c.rrect(250, 480, 360, 560, 22, BLACK)
    c.rrect(258, 488, 352, 552, 16, WHITE)
    c.hatch([(258, 530), (352, 530), (352, 552), (258, 552)], gap=6, angle=45, w=2)
    c.line([(280, 470), (280, 482)], 6)
    c.line([(330, 470), (330, 482)], 6)
    c.circle(305, 520, 24, BLACK)
    c.circle(305, 520, 18, WHITE)
    c.line([(305, 520), (290, 531)], 4)
    c.text((305, 482), "E", 16, anchor="ma") if False else None
    c.bolt(420, 440, 40)
    c.sweat(105, 60, 0) if False else None
    frame(c)


@design("Accumulator tower", "Akkuturm", "steam")
def tower(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.14))
    # gears behind
    c.gear(110, 330, 88, teeth=12, hole=0.4, spokes=5, rot=0.1)
    c.gear(375, 400, 100, teeth=14, hole=0.4, spokes=6, rot=0.3)
    c.gear(60, 520, 42, teeth=8, hole=0.35, spokes=4)
    # tower cylinder
    c.rrect(165, 165, 315, 540, 22, BLACK)
    c.rrect(173, 173, 307, 532, 16, WHITE)
    c.rect(173, 173, 307, 532, WHITE)
    for y in (200, 330, 470):
        c.rect(165, y, 315, y + 22, BLACK)
        rivets(c, [(x, y + 11) for x in range(183, 310, 24)], 3)
    # glass window with a tiny level
    c.rrect(205, 235, 275, 325, 12, BLACK)
    c.rrect(211, 241, 269, 319, 8, WHITE)
    c.rect(211, 300, 269, 319, tone(0.8))
    c.line([(222, 250), (222, 300)], 4, WHITE) if False else None
    c.line([(228, 246), (228, 290)], 3, tone(0.3))
    for y in (258, 276, 294):
        c.line([(262, y), (269, y)], 3)
    c.battery(205, 370, 70, 40, 0.06, line=5)
    c.text((240, 424), "ACCUM.", 20, anchor="ma")
    # dome + tesla coil
    c.poly(c.bez((165, 165), (240, 90), (315, 165), 14), BLACK)
    c.poly(c.bez((176, 165), (240, 105), (304, 165), 14), WHITE)
    c.rect(231, 85, 249, 120, BLACK)
    for i in range(4):
        y = 118 - i * 20
        c.rrect(226 - i * 3, y - 16, 254 + i * 3, y + 6, 8, BLACK)
        c.rrect(231 - i * 3, y - 11, 249 + i * 3, y + 1, 5, WHITE)
    c.circle(240, 42, 17, BLACK)
    c.circle(240, 42, 10, WHITE)
    # sparks
    for (x1, y1) in [(130, 70), (350, 64), (110, 150), (370, 150)]:
        pts = [(240, 42), ((240 + x1) / 2 + 8, (42 + y1) / 2 - 10), ((240 + x1) / 2 - 8, (42 + y1) / 2 + 12), (x1, y1)]
        c.line(pts, 3)
    # pipes + valves
    pipe(c, [(165, 410), (120, 410), (120, 560)], 20)
    pipe(c, [(315, 440), (370, 440), (370, 560)], 20)
    valve(c, 120, 470, 22)
    valve(c, 370, 490, 24)
    # base and plaque
    c.rrect(130, 540, 350, 585, 8, BLACK)
    c.rrect(138, 546, 342, 579, 5, WHITE)
    c.text((240, 548), "ACCUMULATOR", 24, anchor="ma")
    rivets(c, [(145, 563), (335, 563)], 3)
    c.cloud(60, 140, 28, WHITE, 4)
    c.cloud(420, 130, 30, WHITE, 4)
    frame(c)
