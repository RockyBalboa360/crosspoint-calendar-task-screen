"""Pictures 1-10: pop / cartoon scenes."""
import math

from artlib import BLACK, WHITE, W, H, Canvas, tone
from registry import design


def glow(c, cx, cy, r0, r1, rings=7):
    for i in range(rings):
        r = r1 - (r1 - r0) * i / (rings - 1)
        c.circle(cx, cy, r, tone(0.10 + 0.5 * i / rings))


@design("Sleepy battery", "Schlafender Akku", "pop")
def sleepy(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.16))
    c.stars(30, (10, 10, 470, 330))
    c.circle(395, 105, 54, BLACK)          # crescent moon
    c.circle(418, 90, 48, tone(0.16))
    c.circle(418, 90, 48, WHITE) if False else None
    # cloud bed
    c.cloud(240, 575, 150, WHITE, 5)
    c.cloud(95, 600, 70, WHITE, 5)
    c.cloud(395, 605, 75, WHITE, 5)
    # battery
    c.battery_v(140, 170, 200, 340, 0.06, line=9)
    c.face(240, 290, 44, "sleep")
    c.circle(190, 340, 13, tone(0.55))
    c.circle(290, 340, 13, tone(0.55))
    # nightcap (bent cone with pom-pom)
    left = c.bez((148, 186), (150, 90), (70, 104), 16)
    right = c.bez((70, 104), (300, 40), (335, 186), 16)
    cap = left + right[1:]
    c.poly(cap, BLACK)
    inner_l = c.bez((162, 182), (160, 100), (80, 112), 16)
    inner_r = c.bez((80, 112), (290, 56), (320, 182), 16)
    inner = inner_l + inner_r[1:]
    c.poly(inner, WHITE)
    c.hatch(inner, gap=11, angle=-40, w=3)
    c.circle(62, 112, 22, BLACK)
    c.circle(62, 112, 15, WHITE)
    c.rrect(134, 170, 346, 198, 12, BLACK)
    c.rrect(142, 176, 338, 192, 8, WHITE)
    # Zzz
    for (x, y, sz) in [(350, 236, 46), (388, 178, 62), (430, 100, 80)]:
        c.text((x, y), "Z", sz)
    # dream bubble with bolt
    c.circle(104, 262, 8, BLACK)
    c.circle(78, 238, 12, BLACK)
    c.ellipse(10, 120, 130, 222, BLACK)
    c.ellipse(15, 125, 125, 217, WHITE)
    c.bolt(70, 171, 62)


@design("Marathon runner", "Marathon-Akku", "pop")
def marathon(c: Canvas):
    c.rect(0, 0, W, 330, tone(0.07))
    for a in range(0, 360, 30):
        r = math.radians(a)
        c.line([(385 + math.cos(r) * 52, 85 + math.sin(r) * 52), (385 + math.cos(r) * 72, 85 + math.sin(r) * 72)], 5)
    c.circle(385, 85, 40, BLACK)
    c.circle(385, 85, 31, WHITE)
    c.rect(0, 520, W, H, tone(0.3))
    c.line([(0, 520), (W, 520)], 6)
    for x in range(-10, W, 70):
        c.line([(x, 585), (x + 34, 585)], 5)
    # finish gate
    c.line([(36, 520), (36, 150)], 9)
    c.line([(444, 520), (444, 150)], 9)
    c.rrect(22, 140, 458, 220, 10, BLACK)
    for i in range(15):
        for j in range(3):
            if (i + j) % 2 == 0:
                c.rect(30 + i * 28.5, 148 + j * 23, 30 + (i + 1) * 28.5, 148 + (j + 1) * 23, WHITE)
    # runner
    c.battery_v(165, 270, 150, 215, 0.07, line=8)
    c.face(240, 350, 28, "tired")
    c.ellipse(228, 395, 255, 436, BLACK)    # tongue
    c.line([(241, 398), (241, 428)], 3, WHITE)
    c.line([(165, 360), (112, 392), (88, 345)], 11)
    c.line([(315, 360), (362, 328), (398, 372)], 11)
    c.line([(205, 485), (172, 538), (122, 548)], 11)
    c.line([(278, 485), (340, 512), (372, 468)], 11)
    c.rrect(98, 538, 148, 560, 9, BLACK)
    c.rrect(358, 452, 394, 476, 9, BLACK)
    for (x, y, s) in [(140, 300, 13), (345, 292, 11), (120, 430, 9), (330, 400, 9)]:
        c.sweat(x, y, s)
    for y in (300, 360, 420, 480):
        c.line([(14, y), (60 + (y % 3) * 9, y)], 5)
    c.label((240, 590), "So close!", 32)


@design("Desert", "Wüste", "pop")
def desert(c: Canvas):
    c.rect(0, 0, W, 340, tone(0.07))
    c.circle(345, 130, 62, BLACK)
    c.circle(345, 130, 50, WHITE)
    for a in range(0, 360, 20):
        r = math.radians(a)
        c.line([(345 + math.cos(r) * 76, 130 + math.sin(r) * 76), (345 + math.cos(r) * 98, 130 + math.sin(r) * 98)], 5)
    c.poly([(0, 340), (80, 306), (150, 300), (230, 330), (290, 346), (360, 312), (420, 304), (480, 330), (480, 640), (0, 640)], tone(0.3))
    c.line([(0, 340), (80, 306), (150, 300), (230, 330), (290, 346), (360, 312), (420, 304), (480, 330)], 5)
    c.poly([(0, 440), (120, 396), (300, 446), (480, 400), (480, 640), (0, 640)], tone(0.52))
    c.line([(0, 440), (120, 396), (300, 446), (480, 400)], 5)
    # distant sign with wall socket (mirage)
    c.line([(96, 332), (96, 262)], 7)
    c.rrect(60, 190, 132, 268, 12, BLACK)
    c.rrect(67, 197, 125, 261, 8, WHITE)
    c.circle(86, 222, 7)
    c.circle(106, 222, 7)
    c.rrect(92, 236, 100, 252, 3, BLACK)
    for k in range(3):
        c.line(c.wobble([(48, 288 + k * 11), (150, 288 + k * 11)], 3, 8), 2.5)
    # cactus
    c.rrect(385, 240, 417, 410, 16, BLACK)
    c.rrect(345, 296, 367, 356, 11, BLACK)
    c.rrect(345, 336, 398, 358, 11, BLACK)
    c.rrect(412, 270, 436, 336, 11, BLACK)
    c.rrect(398, 322, 436, 346, 11, BLACK)
    # vultures
    for x, y, s in [(210, 96, 1.0), (262, 156, 0.75), (62, 100, 0.65)]:
        c.line([(x - 30 * s, y + 7 * s), (x - 12 * s, y - 9 * s), (x, y + 5 * s), (x + 12 * s, y - 9 * s), (x + 30 * s, y + 7 * s)], 5 * s + 1)
    # crawling battery with an outstretched arm
    c.rrect(165, 468, 375, 568, 22, BLACK)
    c.rrect(173, 476, 367, 560, 15, WHITE)
    c.rrect(375, 497, 402, 539, 6, BLACK)
    c.rect(181, 484, 208, 552, BLACK)
    c.face(288, 505, 24, "tired", dx=34)
    c.line([(165, 520), (118, 495), (80, 462)], 11)
    c.circle(80, 460, 11)
    c.line([(185, 568), (158, 600), (120, 598)], 11)
    c.sweat(250, 450, 11)
    c.sweat(330, 446, 9)
    c.label((300, 592), "need... power...", 26, anchor="ma")


@design("Graveyard", "Friedhof", "pop")
def graveyard(c: Canvas):
    c.rect(0, 0, W, 400, tone(0.32))
    c.stars(24, (10, 10, 470, 220))
    c.circle(345, 125, 72, WHITE)
    c.ring(345, 125, 72, 6)
    c.circle(322, 105, 11, tone(0.35))
    c.circle(368, 140, 14, tone(0.35))
    for bx, by, sc in [(75, 95, 1.0), (185, 58, 0.7), (130, 160, 0.55)]:
        c.poly([(bx - 30 * sc, by), (bx - 11 * sc, by - 10 * sc), (bx, by + 5 * sc), (bx + 11 * sc, by - 10 * sc), (bx + 30 * sc, by),
                (bx + 15 * sc, by + 15 * sc), (bx, by + 8 * sc), (bx - 15 * sc, by + 15 * sc)], BLACK)
    c.ellipse(-120, 420, 600, 760, BLACK)
    c.ellipse(-60, 450, 540, 760, tone(0.5))
    # dead tree
    c.line([(50, 470), (62, 380), (45, 320)], 12)
    c.line([(60, 380), (105, 340)], 8)
    c.line([(50, 335), (18, 300)], 7)
    # tombstone
    c.rrect(140, 215, 340, 540, 80, BLACK)
    c.rect(140, 300, 340, 540, BLACK)
    c.rrect(158, 233, 322, 540, 62, WHITE)
    c.rect(158, 300, 322, 540, WHITE)
    c.battery(188, 285, 106, 60, 0.04, line=7)
    c.text((240, 372), "R.I.P.", 50, anchor="ma")
    c.line([(176, 450), (304, 450)], 5)
    c.line([(196, 470), (284, 470)], 4)
    # flowers: plugs on stems
    for x, d in [(108, 1), (372, -1)]:
        c.cord([(x, 545), (x + 6 * d, 500), (x - 2 * d, 455)], 6)
        c.plug(x - 2 * d, 430, 38, angle=-90)
        c.line([(x + 3 * d, 505), (x + 28 * d, 490)], 5)
        c.ellipse(x + 20 * d - 12, 478, x + 20 * d + 12, 494, BLACK)
    # ghost
    c.poly([(395, 330), (395, 450), (410, 435), (425, 455), (440, 435), (455, 455), (465, 440), (465, 330)], BLACK)
    c.rrect(395, 290, 465, 380, 34, BLACK)
    c.poly([(400, 340), (400, 440), (412, 428), (425, 446), (440, 428), (453, 446), (460, 434), (460, 340)], WHITE)
    c.rrect(400, 295, 460, 380, 30, WHITE)
    c.circle(418, 330, 7)
    c.circle(442, 330, 7)
    c.ellipse(422, 345, 438, 368)
    c.label((430, 250), "Boo!", 26)
    for x in range(8, 472, 38):
        c.line([(x, 575), (x, 625)], 5)
        c.poly([(x - 6, 575), (x, 560), (x + 6, 575)])
    c.line([(0, 590), (480, 590)], 5)
    c.line([(0, 612), (480, 612)], 5)


@design("Rocket out of fuel", "Rakete ohne Treibstoff", "pop")
def rocket(c: Canvas):
    c.rect(0, 0, W, 640, BLACK)
    rng = c.rng
    for _ in range(90):
        x, y = rng.uniform(5, 475), rng.uniform(5, 635)
        c.circle(x, y, rng.choice([1.2, 1.6, 2.2]), WHITE)
    for sx, sy in [(60, 70), (420, 560), (400, 120)]:
        c.line([(sx - 9, sy), (sx + 9, sy)], 2, WHITE)
        c.line([(sx, sy - 9), (sx, sy + 9)], 2, WHITE)
    # ringed planet
    c.circle(380, 150, 62, WHITE)
    c.circle(380, 150, 56, tone(0.45))
    c.hatch_white = None
    c.ring(380, 150, 86, 0)
    c.arc([282, 120, 478, 188], 190, 350, w=6, fill=WHITE)
    c.arc([282, 120, 478, 188], 10, 170, w=6, fill=WHITE)
    c.circle(362, 128, 9, WHITE)
    c.circle(400, 172, 6, WHITE)
    # rocket (tilted slightly)
    def R(x, y):
        a = math.radians(-14)
        return (240 + (x - 240) * math.cos(a) - (y - 340) * math.sin(a), 340 + (x - 240) * math.sin(a) + (y - 340) * math.cos(a))
    body = [R(x, y) for x, y in [(185, 220), (295, 220), (300, 440), (180, 440)]]
    c.poly([R(240, 90)] + [R(x, y) for x, y in [(190, 190), (290, 190)]], WHITE)
    c.poly(body, WHITE)
    c.poly([R(240, 90), R(180, 215), R(300, 215)], WHITE)
    c.line([R(240, 90), R(180, 215), R(180, 440)], 6, BLACK) if False else None
    for pts in ([R(240, 84), R(172, 222), R(308, 222)],):
        c.outline_poly(pts, 6, WHITE)
    c.poly([R(240, 96), R(190, 218), R(290, 218)], tone(0.0) if False else WHITE)
    c.poly([R(240, 96), R(194, 214), R(286, 214)], BLACK) if False else None
    # nose cone shading + body outline
    c.poly([R(240, 112), R(206, 200), R(274, 200)], tone(0.55))
    c.line([R(180, 215), R(180, 440), R(300, 440), R(300, 215)], 6, BLACK) if False else None
    # fins
    c.poly([R(180, 340), R(120, 460), R(180, 440)], WHITE)
    c.poly([R(300, 340), R(360, 460), R(300, 440)], WHITE)
    c.line([R(180, 340), R(120, 460), R(180, 440)], 5, BLACK) if False else None
    # porthole with sad battery inside
    cx, cy = R(240, 290)
    c.circle(cx, cy, 52, BLACK)
    c.circle(cx, cy, 42, WHITE)
    c.battery(cx - 30, cy - 14, 54, 30, 0.06, line=4)
    # panel stripes
    c.line([R(180, 380), R(300, 380)], 5, BLACK)
    c.line([R(180, 400), R(300, 400)], 5, BLACK)
    # nozzle and sputtering spark
    nz = [R(205, 440), R(275, 440), R(262, 470), R(218, 470)]
    c.poly(nz, tone(0.6))
    sx, sy = R(240, 500)
    c.bolt(sx, sy + 14, 54, fill=WHITE)
    for k in range(5):
        c.circle(sx + rng.uniform(-35, 35), sy + 50 + k * 14, 3, WHITE)
    # fuel gauge
    gx, gy, gr = 112, 520, 68
    c.circle(gx, gy, gr + 6, WHITE)
    c.circle(gx, gy, gr, BLACK)
    c.circle(gx, gy, gr - 6, WHITE)
    for i in range(0, 9):
        a = math.radians(200 + i * 17.5)
        c.line([(gx + (gr - 10) * math.cos(a), gy + (gr - 10) * math.sin(a)), (gx + (gr - 20) * math.cos(a), gy + (gr - 20) * math.sin(a))], 3)
    c.poly([(gx, gy)] + [(gx + (gr - 10) * math.cos(math.radians(200 + t)), gy + (gr - 10) * math.sin(math.radians(200 + t))) for t in range(0, 32, 4)], tone(0.7))
    a = math.radians(203)
    c.line([(gx, gy), (gx + (gr - 14) * math.cos(a), gy + (gr - 14) * math.sin(a))], 5)
    c.circle(gx, gy, 8)
    c.text((gx - 52, gy + 10), "E", 26)
    c.text((gx + 38, gy + 10), "F", 26)
    c.text((300, 40), "no fuel!", 34, fill=WHITE)


@design("Arcade game over", "Arcade", "pop")
def arcade(c: Canvas):
    from PIL import Image, ImageDraw, ImageFont

    def px(x, y, text, k, white=True):
        font = ImageFont.load_default()
        tmp = Image.new("L", (int(font.getlength(text)) + 2, 14), 0)
        ImageDraw.Draw(tmp).text((1, 0), text, font=font, fill=255)
        big = tmp.resize((tmp.width * k * 2, tmp.height * k * 2), Image.NEAREST)
        c.A.paste(255 if white else 0, (int(x * 2), int(y * 2)), big)
        c.T.paste(255, (int(x * 2), int(y * 2)), big)
        return tmp.width * k

    def block(x, y, k, rows, white=True):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch == "#":
                    c.rect(x + i * k, y + j * k, x + (i + 1) * k, y + (j + 1) * k, WHITE if white else BLACK)

    c.rect(0, 0, W, 640, BLACK)
    c.rect(12, 12, W - 12, 628, WHITE)
    c.rect(22, 22, W - 22, 618, BLACK)
    px(44, 44, "PLAYER 1", 4)
    px(280, 44, "LIVES", 4)
    heart = ["..##..##..", ".########.", "##########", "##########", ".########.", "..######..", "...####...", "....##...."]
    outline = ["..##..##..", ".##.##.##.", "##..###..#", "#........#", ".#......#.", "..#....#..", "...#..#...", "....##...."]
    block(280, 84, 6, heart)
    block(350, 84, 6, outline)
    block(420, 84, 6, outline)
    # big pixel battery
    k = 12
    x0, y0 = 54, 190
    c.rect(x0, y0, x0 + 31 * k, y0 + 11 * k, WHITE)
    c.rect(x0 + 2 * k, y0 + 2 * k, x0 + 29 * k, y0 + 9 * k, BLACK)
    c.rect(x0 + 31 * k, y0 + 3 * k, x0 + 33 * k, y0 + 8 * k, WHITE)
    c.rect(x0 + 3 * k, y0 + 3 * k, x0 + 5 * k, y0 + 8 * k, WHITE)
    # warning sign
    c.poly([(240, 340), (170, 450), (310, 450)], WHITE)
    c.poly([(240, 364), (192, 438), (288, 438)], BLACK)
    c.rect(234, 382, 246, 418, WHITE)
    c.rect(234, 426, 246, 436, WHITE)
    for (sx, sy) in [(60, 330), (410, 345), (70, 450), (400, 440), (430, 250), (46, 262)]:
        block(sx, sy, 6, [".#.", "###", ".#."])
    px(62, 490, "INSERT CHARGER", 4)
    px(120, 548, "CONTINUE?", 4)
    c.rect(22, 596, W - 22, 618, WHITE)


@design("Last candle", "Letzte Kerze", "pop")
def candle(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.62))
    glow(c, 240, 190, 40, 210, rings=8)
    # flame halo rays
    for a in range(0, 360, 24):
        r = math.radians(a)
        c.line([(240 + math.cos(r) * 78, 190 + math.sin(r) * 78), (240 + math.cos(r) * 100, 190 + math.sin(r) * 100)], 4)
    # holder dish
    c.ellipse(70, 560, 410, 620, BLACK)
    c.ellipse(80, 556, 400, 606, WHITE)
    c.ellipse(130, 562, 350, 596, tone(0.35))
    c.rrect(380, 560, 450, 576, 7, BLACK) if False else None
    c.ring(420, 585, 28, 9)
    c.circle(420, 585, 28, BLACK) if False else None
    # melted candle body = battery shape with a melted top
    c.rrect(150, 330, 330, 585, 22, BLACK)
    c.rrect(158, 338, 322, 577, 16, WHITE)
    c.rect(158, 338, 322, 420, WHITE)
    drips = [(158, 338), (322, 338), (322, 420), (300, 440), (290, 400), (270, 470), (250, 405), (236, 430), (215, 395), (190, 455), (172, 410), (158, 430)]
    c.poly([(150, 330), (330, 330), (330, 345)] + [(322, 345)] + [(322, 420), (305, 432), (296, 400), (278, 468), (258, 410), (240, 436), (222, 398), (196, 458), (178, 412), (158, 430)], BLACK)
    c.poly([(158, 338), (322, 338), (322, 416), (303, 424), (295, 394), (278, 458), (260, 404), (240, 428), (222, 392), (196, 448), (178, 406), (158, 424)], WHITE)
    c.bolt(240, 500, 100)
    c.text((240, 330), "", 1)
    # nub / wick
    c.rrect(215, 300, 265, 335, 8, BLACK)
    c.line([(240, 300), (242, 272)], 6)
    # flame
    flame = c.bez((240, 150), (270, 205), (240, 275), 12) + c.bez((240, 275), (205, 205), (240, 150), 12)[1:]
    c.poly(flame, BLACK)
    inner = c.bez((240, 190), (256, 225), (240, 262), 10) + c.bez((240, 262), (222, 225), (240, 190), 10)[1:]
    c.poly(inner, WHITE)
    # moth
    mx, my = 360, 160
    c.ellipse(mx - 6, my - 14, mx + 6, my + 16, BLACK)
    c.poly([(mx - 4, my - 6), (mx - 46, my - 34), (mx - 52, my + 8), (mx - 6, my + 8)], BLACK)
    c.poly([(mx + 4, my - 6), (mx + 46, my - 34), (mx + 52, my + 8), (mx + 6, my + 8)], BLACK)
    c.circle(mx - 28, my - 8, 7, WHITE)
    c.circle(mx + 28, my - 8, 7, WHITE)
    c.line([(mx - 3, my - 14), (mx - 16, my - 36)], 3)
    c.line([(mx + 3, my - 14), (mx + 16, my - 36)], 3)
    c.label((240, 36), "last light...", 34)


@design("Plug in love", "Stecker verliebt", "pop")
def plug_love(c: Canvas):
    c.rect(0, 0, W, 480, tone(0.1))
    for y in range(30, 460, 46):
        for x in range(24 + (y // 46 % 2) * 22, W, 44):
            c.circle(x, y, 3.5)
    c.rect(0, 480, W, H, tone(0.5))
    c.line([(0, 480), (W, 480)], 7)
    # wall socket (right)
    c.rrect(335, 230, 470, 400, 22, BLACK)
    c.rrect(344, 239, 461, 391, 16, WHITE)
    c.circle(380, 300, 12)
    c.circle(380, 300, 5, WHITE)
    c.circle(425, 300, 12)
    c.circle(425, 300, 5, WHITE)
    c.face(403, 262, 14, "happy")
    c.ellipse(375, 350, 430, 375, tone(0.5))
    # plug (left), reaching with a stretched cord
    px, py = 195, 330
    c.plug(px, py, 88, angle=0)
    c.face(px - 14, py - 6, 14, "worried", brows=True)
    c.cord([(px - 52, py + 4), (120, 360), (60, 440), (170, 540), (330, 560), (450, 540)], 8)
    for k in range(4):
        c.line([(px - 70 - k * 6, py - 40 - k * 14), (px - 90 - k * 6, py - 46 - k * 14)], 4)
    # gap marker with a spark
    c.line([(250, 345), (335, 345)], 4)
    for i in range(2):
        x = 288 + i * 4
    c.bolt(292, 300, 64)
    for (x, y, s) in [(265, 250, 26), (330, 195, 22), (225, 215, 18)]:
        hp = [(x, y + s * 0.9), (x - s, y - s * 0.1), (x - s * 0.5, y - s * 0.7), (x, y - s * 0.3), (x + s * 0.5, y - s * 0.7), (x + s, y - s * 0.1)]
        c.poly(hp, BLACK)
    c.label((240, 570), "so close...", 32)
    # tiny battery on the floor, cheering
    c.battery(40, 510, 90, 50, 0.05, line=6)


@design("Hourglass", "Sanduhr", "pop")
def hourglass(c: Canvas):
    c.rect(0, 0, W, 640, tone(0.06))
    # frame
    c.rrect(95, 40, 385, 84, 14, BLACK)
    c.rrect(95, 556, 385, 600, 14, BLACK)
    for x in (115, 365):
        c.rect(x - 11, 84, x + 11, 556, BLACK)
    c.rect(115 - 3, 84, 115 + 3, 556, WHITE) if False else None
    # glass
    top = c.bez((135, 100), (135, 250), (232, 320), 14) + [(248, 320)] + c.bez((248, 320), (345, 250), (345, 100), 14)
    top_poly = [(135, 100), (345, 100)] + list(reversed(top))[:0] + top[::-1] if False else None
    glass = [(140, 90)] + c.bez((140, 90), (140, 240), (236, 305), 14)[1:] + [(236, 320), (244, 320), (244, 305)] + c.bez((244, 305), (340, 240), (340, 90), 14)[1:]
    glass_low = [(236, 320), (244, 320), (244, 335)] + c.bez((244, 335), (340, 400), (340, 550), 14)[1:] + [(140, 550)] + c.bez((140, 550), (140, 400), (236, 335), 14)[1:]
    c.poly(glass, WHITE)
    c.poly(glass_low, WHITE)
    c.line(glass + [glass[0]], 7)
    c.line(glass_low + [glass_low[0]], 7)
    # sand = bolts: a thin layer on top, heap at the bottom
    c.poly([(160, 112), (320, 112), (300, 150), (180, 150)] if False else [(165, 78), (315, 78), (300, 90), (180, 90)], BLACK) if False else None
    c.poly([(150, 536), (330, 536), (310, 520), (284, 480), (262, 440), (240, 424), (218, 440), (196, 480), (170, 520)], BLACK) if False else None
    heap = [(142, 548)] + c.bez((142, 548), (200, 540), (240, 430), 14)[1:] + c.bez((240, 430), (280, 540), (338, 548), 14)[1:]
    c.poly(heap, tone(0.75))
    c.line(heap, 5)
    c.poly([(176, 160), (304, 160), (280, 175), (200, 175)], tone(0.75))
    for k in range(6):
        c.circle(240, 330 + k * 22, 3.5 if k % 2 else 2.5)
    # small bolts floating in the lower bulb heap
    for (x, y, s) in [(215, 500, 34), (262, 492, 30), (240, 456, 32)]:
        c.bolt(x, y, s, fill=WHITE)
    c.bolt(240, 220, 48, fill=tone(0.45))
    # sparkles + tick marks
    for (x, y) in [(60, 140), (430, 200), (50, 400), (440, 450)]:
        c.line([(x - 14, y), (x + 14, y)], 4)
        c.line([(x, y - 14), (x, y + 14)], 4)
    for i in range(12):
        a = i / 12 * 2 * math.pi
        c.line([(240 + math.cos(a) * 218, 320 + math.sin(a) * 218), (240 + math.cos(a) * 232, 320 + math.sin(a) * 232)], 3) if False else None
    c.rrect(60, 606, 420, 628, 8, BLACK) if False else None


@design("Cat and cable", "Katze und Kabel", "pop")
def cat_cable(c: Canvas):
    c.rect(0, 0, W, 400, tone(0.1))
    c.rect(0, 400, W, H, tone(0.45))
    c.line([(0, 400), (W, 400)], 7)
    # window with moon
    c.rect(300, 50, 450, 230, BLACK)
    c.rect(310, 60, 440, 220, WHITE)
    c.line([(375, 60), (375, 220)], 6)
    c.line([(310, 140), (440, 140)], 6)
    c.circle(407, 100, 20, tone(0.3))
    # cat: sitting, seen from the front
    c.ellipse(55, 400, 255, 600, BLACK)                 # haunches
    c.poly(c.bez((95, 330), (40, 470), (60, 560), 12) + [(255, 560)] + c.bez((255, 560), (270, 470), (215, 330), 12), BLACK)  # body
    c.ellipse(88, 250, 232, 372, BLACK)                  # head
    c.poly([(94, 285), (92, 205), (140, 262)], BLACK)    # ears
    c.poly([(226, 285), (228, 205), (180, 262)], BLACK)
    c.poly([(104, 270), (102, 228), (128, 262)], tone(0.45))
    c.poly([(216, 270), (218, 228), (192, 262)], tone(0.45))
    for ex in (128, 192):
        c.ellipse(ex - 20, 285, ex + 20, 335, WHITE)
        c.ellipse(ex - 6, 289, ex + 6, 331, BLACK)
    c.poly([(150, 345), (170, 345), (160, 357)], WHITE)
    for sgn in (-1, 1):
        for dy in (-8, 2, 12):
            c.line([(160 + sgn * 62, 348 + dy * 0.5), (160 + sgn * 112, 342 + dy * 1.6)], 3)
    c.ellipse(78, 560, 140, 600, tone(0.0) if False else WHITE) if False else None
    c.ellipse(60, 565, 130, 605, BLACK)
    c.ellipse(180, 565, 250, 605, BLACK)
    # tail curls around in front
    c.line(c.bez((250, 560), (330, 640), (290, 590), 10) if False else [(250, 585), (300, 605), (330, 580), (322, 548)], 20)
    # chewed cable: tiny frayed end with a spark
    c.cord([(135, 618), (250, 630), (330, 615), (390, 585), (420, 545)], 8)
    for dx, dy in [(-14, -22), (2, -26), (16, -16), (-26, -8)]:
        c.line([(420, 545), (420 + dx, 545 + dy)], 4)
    c.bolt(448, 500, 56)
    # small battery waiting on the floor
    c.battery_v(380, 400, 78, 120, 0.05, line=7)
    c.face(419, 452, 14, "worried")
    c.speech(268, 118, 400, 188, (200, 245))
    c.text((334, 128), "?!", 46, anchor="ma")
