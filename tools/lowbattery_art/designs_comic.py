"""Pictures 11-13: comic sketch style (wobbly pen lines, hatching, speech bubbles)."""
import math

from artlib import BLACK, WHITE, W, H, Canvas, tone
from registry import design


def rr_pts(x0, y0, x1, y1, r, n=6):
    pts = []
    for (cx, cy, a0) in [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def burst(c, cx, cy, r0, r1, n=18, w=3):
    for i in range(n):
        a = i / n * 2 * math.pi + 0.1
        rr = r1 * (0.8 + 0.2 * ((i * 7) % 3) / 2)
        c.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * rr, cy + math.sin(a) * rr)], w)


@design("Hungry monster", "Hungriges Monster", "comic")
def hungry(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.05))
    burst(c, 240, 330, 190, 300, 26, 3)
    c.ellipse(80, 540, 400, 610, tone(0.4))
    body = rr_pts(100, 170, 380, 540, 46)
    c.sketch_poly(body, w=6, fill=WHITE, amp=1.6)
    c.hatch(rr_pts(300, 180, 372, 532, 40), gap=7, angle=60, w=2.2)
    c.hatch(rr_pts(108, 470, 372, 532, 30), gap=7, angle=-30, w=2.2)
    c.sketch_poly(rr_pts(170, 120, 310, 178, 14), w=6, fill=WHITE)
    # mouth
    mouth = [(140, 330), (160, 300), (320, 300), (342, 330), (330, 440), (240, 470), (150, 440)]
    c.poly(mouth, BLACK)
    for i in range(7):  # teeth
        x = 160 + i * 26
        c.poly([(x, 304), (x + 26, 304), (x + 13, 336 + (i % 2) * 8)], WHITE)
    for i in range(6):
        x = 168 + i * 26
        c.poly([(x, 450 - i * 0 - abs(i - 2.5) * 5), (x + 26, 450 - abs(i - 2.5) * 5), (x + 13, 418)], WHITE)
    c.ellipse(190, 405, 290, 470, tone(0.5))      # tongue
    c.line([(240, 405), (240, 450)], 3)
    # eyes
    for ex, dxp in [(185, 6), (295, -8)]:
        c.sketch_ellipse((ex - 38, 215, ex + 38, 291), w=6, fill=WHITE)
        c.circle(ex + dxp, 255, 11)
    c.line([(140, 195), (225, 222)], 8)
    c.line([(340, 195), (255, 222)], 8)
    # drool and stars
    for x, y in [(160, 450), (330, 455)]:
        c.sweat(x, y + 22, 9)
    # arms with fork (plug) and knife
    c.sketch_line([(100, 400), (55, 380), (46, 300)], 10)
    c.sketch_line([(380, 400), (425, 380), (436, 300)], 10)
    c.circle(46, 298, 15)
    c.circle(436, 298, 15)
    c.plug(46, 230, 62, angle=-90)
    c.poly([(428, 285), (445, 285), (452, 190), (436, 170)], BLACK)
    c.poly([(432, 280), (441, 280), (446, 196), (437, 184)], WHITE)
    c.rrect(428, 280, 446, 310, 5)
    # legs
    c.sketch_line([(190, 540), (186, 590)], 10)
    c.sketch_line([(290, 540), (294, 590)], 10)
    c.ellipse(156, 580, 216, 612)
    c.ellipse(262, 580, 324, 612)
    c.speech(20, 30, 340, 100, (150, 160), w=4)
    c.text((180, 42), "FEED ME!", 48, anchor="ma")
    c.text((410, 70), "grrr", 28, anchor="ma")


@design("Intensive care", "Intensivstation", "comic")
def hospital(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.05))
    c.line([(0, 470), (W, 470)], 5)
    c.rect(0, 470, W, H, tone(0.3))
    # monitor
    c.sketch_poly(rr_pts(30, 40, 200, 150, 14), w=6, fill=WHITE)
    c.line([(44, 105), (80, 105), (92, 70), (108, 128), (120, 105), (186, 105)], 4)
    c.circle(186, 62, 5)
    c.sketch_line([(115, 150), (115, 175)], 6)
    c.sketch_poly([(75, 175), (155, 175), (140, 190), (90, 190)], w=4, fill=BLACK)
    # bed
    c.sketch_poly([(40, 250), (60, 250), (60, 520), (40, 520)], w=5, fill=BLACK)
    c.sketch_poly([(60, 420), (400, 420), (400, 450), (60, 450)], w=5, fill=WHITE)
    c.sketch_line([(100, 450), (100, 520)], 8)
    c.sketch_line([(360, 450), (360, 520)], 8)
    c.sketch_poly(rr_pts(60, 340, 140, 380, 18), w=5, fill=WHITE)   # pillow
    # battery lying in bed
    body = rr_pts(105, 300, 330, 410, 24)
    c.sketch_poly(body, w=6, fill=WHITE)
    c.rrect(330, 330, 352, 380, 6, BLACK)
    c.rect(114, 309, 138, 401, BLACK)
    c.face(228, 335, 22, "sad", dx=40)
    # bandage on head + thermometer
    c.poly([(116, 300), (150, 292), (162, 312), (128, 322)], WHITE)
    c.sketch_line([(116, 300), (150, 292), (162, 312), (128, 322), (116, 300)], 4)
    c.line([(133, 296), (146, 316)], 3)
    c.line([(228, 372), (290, 392)], 5)
    c.circle(292, 393, 6)
    # blanket
    blanket = [(160, 372), (340, 372), (420, 430), (400, 478), (150, 478), (130, 430)]
    c.sketch_poly(blanket, w=5, fill=WHITE)
    c.hatch(blanket, gap=10, angle=-35, w=2.5)
    c.hatch(blanket, gap=10, angle=-35, w=2.5, cross=True) if False else None
    # IV stand
    c.sketch_line([(430, 120), (430, 500)], 8)
    c.sketch_line([(380, 500), (480, 500)], 8)
    c.circle(390, 510, 9)
    c.circle(470, 510, 9)
    c.sketch_line([(430, 120), (380, 100)], 6)
    c.sketch_poly(rr_pts(340, 100, 420, 200, 16), w=5, fill=WHITE)
    c.bolt(380, 150, 64)
    c.line([(380, 200), (380, 220)], 4)
    c.cord([(380, 220), (370, 280), (300, 300), (250, 340)], 4)
    c.plug(262, 322, 36, angle=200)
    c.speech(210, 35, 330, 90, (260, 165), w=4)
    c.text((270, 44), "...", 40, anchor="ma")
    c.label((90, 585), "ICU", 40, anchor="ma")
    c.text((390, 560), "beep", 22)
    c.text((410, 590), "beep", 22)


@design("Then and now", "Früher und heute", "comic")
def then_now(c: Canvas):
    # panel 1
    c.rect(14, 14, 466, 314, WHITE)
    burst(c, 240, 170, 80, 300, 30, 3)
    c.battery_v(165, 80, 150, 190, 1.0, line=7, fill_tone=tone(0.32))
    c.face(240, 140, 26, "cool")
    c.hatch([(172, 100), (212, 100), (212, 262), (172, 262)], gap=7, angle=50, w=2) if False else None
    c.sketch_line([(165, 180), (120, 150), (95, 105)], 10)
    c.sketch_line([(315, 180), (360, 150), (385, 105)], 10)
    c.ellipse(80, 82, 120, 124, BLACK)
    c.ellipse(360, 82, 400, 124, BLACK)
    c.arc([95, 140, 135, 190], 200, 330, w=6) if False else None
    for sx, sy in [(60, 60), (420, 60), (70, 260), (410, 270)]:
        c.line([(sx - 14, sy), (sx + 14, sy)], 4)
        c.line([(sx, sy - 14), (sx, sy + 14)], 4)
    c.sketch_line([(205, 270), (205, 300)], 10)
    c.sketch_line([(275, 270), (275, 300)], 10)
    c.rect(14, 300, 466, 314, tone(0.5))
    c.label((126, 28), "THEN", 26, anchor="ma")
    c.sketch_poly(rr_pts(14, 14, 466, 314, 6), w=7)
    # panel 2
    c.rect(14, 330, 466, 626, tone(0.3))
    # rain cloud
    c.cloud(150, 420, 50, WHITE, 5)
    for x in (110, 140, 170, 200):
        c.line([(x, 462), (x - 8, 484)], 3)
    # wilted battery leaning
    pts = [(175, 590), (150, 470), (190, 400), (270, 392), (300, 455), (290, 590)]
    c.sketch_poly([(190, 590), (172, 480), (205, 430), (305, 445), (320, 590)], w=7, fill=WHITE)
    c.sketch_poly([(205, 430), (215, 405), (265, 410), (255, 440)], w=6, fill=BLACK)
    c.rect(196, 560, 316, 586, BLACK)
    c.face(255, 505, 22, "dead" if False else "sad")
    c.sketch_line([(195, 520), (150, 560), (140, 600)], 9)
    c.sketch_line([(320, 520), (352, 565), (350, 600)], 9)
    # wilted flower
    c.sketch_line([(400, 610), (402, 540), (385, 500)], 6)
    c.circle(380, 494, 12)
    c.sketch_line([(380, 494), (366, 510)], 4)
    c.sketch_line([(402, 580), (430, 560)], 5)
    c.label((380, 345), "sigh...", 26, anchor="ma")
    c.label((126, 345), "NOW", 26, anchor="ma") if False else None
    c.label((390, 640 - 60), "", 1) if False else None
    c.label((70, 340), "NOW", 26, anchor="ma")
    c.sketch_poly(rr_pts(14, 330, 466, 626, 6), w=7)
