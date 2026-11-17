from thsq import *
import math
import thsq as T
import life
G = 860  # default feet line

def crew(c, xs, y, h, pose="stand", ex="n", who="extra", **k):
    return [c.fig(x, y, h, pose, ex if isinstance(ex, str) else ex[i % len(ex)], who, **k) for i, x in enumerate(xs)]
def Q(c, shown=4, done=0, hidden=None): c.quest(shown, done, hidden); return c
def L(cv, t, y=120, x=W/2, size=72, **k): cv.label(x, y, t, size, **k); return cv

def myth(k):
    c = C((242, 216, 204)); c.rect(0, 700, W, H, (228, 176, 158), None); c.line([(0, 700), (W, 700)])
    c.sledge(180, G, 300); c.block(200, G-22, 260, 190, (236, 214, 200))
    hs = crew(c, [760, 950, 1140, 1330, 1520], G, 250, "pull", "sad", "chain")
    c.line([(520, G-110), hs[0]["hand"], hs[-1]["hand"]], 7, EARTH)
    for x in range(700, 1560, 60): c.ell(x, G+14, x+34, G+34, None, INK, 5)
    if k >= 1:
        b = c.fig(600, G, 270, "up", "angry", "boss"); hx, hy = b["hand"]; c.line([(hx, hy), (hx+90, hy-80), (hx+190, hy-20), (hx+250, hy-90)], 6)
    if k >= 2: L(c, "100,000 PRISONERS?", 130)
    if k >= 3: c.redx(W/2, H/2, 330, 44)
    return c
def herod(k):
    c = C().bg("sand"); c.pyramid(1280, 700, 900, 520, (226, 212, 186), 1, 9)
    g = c.fig(420, G, 300, "hold", "smile", "greek"); c.papyrus(g["hand"][0]+40, g["hand"][1]-20, .5)
    if k >= 1:
        c.rect(160, 900, 1760, 1040, PAPER, INK, 6, 18); c.line([(260, 985), (1660, 985)], 8)
        for x, t in ((260, "BUILT"), (1660, "HE ARRIVES")): c.ell(x-16, 969, x+16, 1001, RED, INK, 5); c.text(x, 935, t, 44)
        c.text(960, 940, "2,000 YEARS LATE", 60, RED)
    return c
def evid(k):
    c = C()
    it = [(430, "A DIARY"), (960, "A PAYROLL"), (1490, "SKELETONS")]
    for i in range(k):
        x = it[i][0]
        if i == 0: c.papyrus(x, 430, 2.1)
        if i == 1: c.loaf(x-110, 540, 2.2); c.jar(x+110, 570, 2.0)
        if i == 2: c.bone(x-170, 340, x+170, 540); c.bone(x-170, 540, x+170, 340)
        c.text(x, 740, it[i][1], 104)
    return c
def beer(k):
    c = C()
    if k == 0: c.jar(W/2, 760, 3.2); L(c, "PAID IN BEER", 170, size=110)
    if k == 1: c.text(W/2, 430, "COULDN'T SAY", 150); c.text(W/2, 660, "NO", 260, RED); c.strike(760, 660, 1160, 26)
    if k == 2:
        c.bg("sand"); hs = crew(c, [660, 960, 1260], G, 330, "wave", ["joy", "joy2", "joy"])
        for h in hs: c.jar(h["hand"][0], h["hand"][1]+20, .7)
        L(c, "CREW NAME: THE DRUNKARDS", 150, size=84)
    return c
def intro(k):
    c = C(); s = c.fig(W/2, 900-(1-T.ease(T.LT/0.3))*900*(k == 0), 520, "drop" if k == 0 else "self", "wow" if k == 0 else "worry", "sid")
    c.marker(s["head"][0]+20, s["head"][1]-110, 46)
    if k: L(c, "YOU", 160, 1400, 120)
    return c
def card(t, sub=None, size=150, col=INK):
    c = C(); c.card(t, size, sub, col); return c
def field(k=0):
    c = C().bg("field"); c.rect(0, 610, W, 700, WATER, None); c.line([(0, 610), (W, 610)], 5); c.line([(0, 700), (W, 700)], 6)
    for x in (1240, 1470, 1690): c.hut(x, 760, 180, 130)
    c.fig(520, G+40, 340, "wave" if k else "stand", "smile", "sid")
    if k == 1: L(c, "AGE 17. BARLEY FARMER.", 150)
    return c
def flood(k):
    c = C().bg("flood", 600); c.hut(240, 800, 330, 230); c.rect(0, 740, W, H, WATER, None)
    for i in range(10): x = (i*263) % W; y = 790+(i*97) % 240; c.line([(x, y), (x+50, y)], 5, WHITE)
    c.fig(400, 572, 250, "self" if k >= 3 else "chin", "wow" if k >= 3 else "bored", "sid", sit=True)
    if k >= 1:
        b = c.fig(1330, 800, 290, "point" if k >= 2 else "stand", "det", "boss", flip=True, staff=(k < 2)); crew(c, [1500, 1640], 800, 250, "stand", "n", flip=True); c.boat(1180, 830, 620)
    return c
def scholars(k):
    c = C(); c.fig(520, 760, 380, "point", "n", "sci"); c.fig(1400, 760, 380, "point", "n", "sci", flip=True)
    L(c, "HAWASS", 190, 520, 76); L(c, "LEHNER", 190, 1400, 76)
    if k == 0: c.text(960, 480, "?", 300, RED)
    if k in (1, 3): L(c, "CONSCRIPTS", 900, 520, 84, bg=MARI)
    if k >= 2: L(c, "OBLIGATORY LABOR", 900, 1400, 84, bg=MARI)
    if k == 3: L(c, "A TAX YOU PAY WITH YOUR BACK", 1010, 960, 60)
    return c
def barn(k):
    c = C(SKY); c.rect(0, 700, W, H, (150, 196, 120), None); c.line([(0, 700), (W, 700)])
    for x in (980, 1280, 1580): c.line([(x, 880), (x, 380)], 16, EARTH)
    c.line([(960, 380), (1600, 380)], 16, EARTH); c.line([(980, 380), (1280, 240), (1580, 380)], 16, EARTH)
    s = c.fig(520, G+20, 340, "carry", "bored", "modern"); c.line([(s["hand0"][0]-150, s["hand0"][1]-10), (s["hand"][0]+150, s["hand"][1]-10)], 22, EARTH)
    crew(c, [1130, 1430], G+20, 300, "cheer", "joy", "plain")
    if k: L(c, "NOT EVERYONE IS THRILLED", 130)
    return c
def menu(k):
    c = C(); c.rect(1000, 180, 1560, 900, WHITE, INK, 8, 20); c.text(1280, 280, "MENU", 110); c.line([(1060, 350), (1500, 350)], 5)
    c.text(1280, 480, "YES", 150, TEAL); c.text(1280, 700, "NO", 150)
    if k: c.strike(1140, 700, 1420, 22)
    c.fig(520, 900, 440, "chin" if not k else "shrug", "n" if not k else "worry", "sid")
    return c
def boat(k, done=0):
    c = C().bg("river", 560); c.rect(0, 520, W, 560, SAND, None); c.line([(0, 520), (W, 520)], 5); c.pyramid(1560, 520, 420, 250, STONE, .55, 5)
    x = 180+(k+T.LP)*260; s = c.fig(x+130, 800, 270, "wave" if k == 2 else "stand", ["worry", "n", "wow"][k % 3], "sid"); crew(c, [x+260, x+370, x+480], 800, 240, "stand", ["n", "smile", "bored"]); c.boat(x, 830, 600)
    c.line([(x+560, 700), (x+640, 900)], 9, EARTH)
    if done: Q(c, 4, done)
    return c
def city(k):
    c = C().bg("sand", 640)
    if k == 0:
        c.fig(560, G, 340, "walk", "n", "sid"); c.line([(1300, 860), (1300, 560)], 12, EARTH); c.rect(1180, 520, 1500, 620, PAPER, INK, 6, 8); c.text(1340, 566, "WORK CAMP ->", 54); return c
    c.pyramid(1560, 640, 520, 330, STONE, .6, 6); c.poly([(0, 1080), (0, 760), (260, 700), (520, 800), (640, 1080)], DSAND, INK, 6)
    c.fig(260, 712, 250, "drop", "wow", "sid")
    c.rect(760, 700, 1840, 1000, (226, 196, 150), INK, 6, 10)
    for x in (800, 940, 1080, 1220): c.silo(x, 900, 110, 150)
    for x in (1380, 1540, 1700): c.hut(x, 960, 130, 100); c.smoke(x+70, 830, 3 if k < 4 else 4)
    if k == 2: L(c, "THE LOST CITY OF THE PYRAMID BUILDERS", 110, size=64)
    if k == 3: L(c, "ROYAL GRAIN SILOS", 620, 1010, 60, bg=MARI)
    if k == 4: L(c, "BAKERIES BY THE DOZEN", 620, 1560, 60, bg=MARI)
    return c
def hall(k):
    c = C().bg("hall", 420)
    for i in range(7): c.line([(120+i*280, 0), (120+i*280, 420)], 10, (120, 84, 58))
    for r, y in enumerate((640, 860, 1040)):
        for i in range(5):
            x = 330+i*340; sid = (r == 1 and i == 2)
            c.rect(x-290, y+6, x+20, y+26, (226, 200, 150), INK, 4, 8)
            c.fig(x, y, 240, "stand", ("wow" if k else "bored") if sid else "sleep", "sid" if sid else "extra", rot=-90)
            if not sid and (i+r) % 2 == 0: c.text(x-250, y-110, "Z", 60, PAPER)
    if k: L(c, "40-50 PER HALL", 110)
    return c
def bars(k):
    c = C(); c.rect(260, 300, 1660, 440, EARTH, INK, 7, 10); c.text(960, 370, "100,000", 96, PAPER)
    if k >= 1: c.strike(240, 370, 1680, 26)
    if k >= 2: c.rect(260, 600, 540, 740, MARI, INK, 7, 10); c.text(900, 670, "ABOUT 20,000", 110)
    if k >= 3: c.rect(260, 600, 400, 740, TEAL, INK, 7, 10); c.text(720, 850, "ONLY HALF HAUL STONE", 80, TEAL)
    return c
def team(k):
    c = C().bg("sand"); c.block(1240, G, 520, 380)
    xs = [300, 520, 740, 960]
    if k == 0: crew(c, [300, 740, 960, 1130], G, 300, "stand", ["smile", "n", "smug", "n"]); c.fig(520, G, 320, "wave", "smile", "sid"); L(c, "YOUR TEAM", 130)
    else:
        p = c.fig(1130, G, 300, "up", "smile", "extra"); crew(c, [300, 740, 960], G, 300, "cheer" if k == 3 else "stand", ["joy", "smile", "joy2"])
        c.line([(1320, 560), (1420, 520), (1520, 590), (1640, 540)], 22, RED); c.line([(1340, 660), (1500, 640)], 22, RED)
        s = c.fig(520, G, 320, "cheer" if k == 3 else "stand", "joy" if k == 3 else "wow", "sid"); hx, hy = s["head"]; c.ell(hx+8, hy+60, hx+30, hy+82, RED, None)
        if k == 2: L(c, "FRIENDS OF KHUFU", 130, size=90, c=RED)
        if k == 3: L(c, "DRUNKARDS OF MENKAURE", 130, size=84, c=RED); c.jar(300+110, G-260, .6); c.jar(960+110, G-260, .6)
    return c
def softball(k):
    c = C(SKY); c.rect(0, 760, W, H, (150, 196, 120), None); c.line([(0, 760), (W, 760)])
    s = c.fig(460, 920, 380, "up", "wow" if k else "smile", "modern"); hx, hy = s["hand"]; c.ell(hx-50, hy-70, hx+50, hy+30, EARTH, INK, 6)
    if k:
        c.block(980, 560-(1-T.ease(T.LT/0.3))*760, 620, 440)
        for i in range(3): c.line([(1040+i*200, 60), (1040+i*200, 100)], 8)
        L(c, "2.5 TONS", 340, 1290, 110)
    else: c.ell(1100, 200, 1180, 280, WHITE, INK, 6); L(c, "COMPANY SOFTBALL", 110)
    return c
def pyr(k):
    c = C(); c.line([(200, 900), (1720, 900)], 7); p = [.05, .25, .6, 1, 1][k]+([.25, .6, 1, 1, 1][k]-[.05, .25, .6, 1, 1][k])*T.ease(T.LP*1.6)
    c.pyramid(820, 900, 1100, 640, STONE, p, 14)
    if p < 1: c.poly([(270, 900), (820, 260), (1370, 900)], None, (190, 176, 150), 4)
    if k >= 1: L(c, "2.3 MILLION BLOCKS", 130, size=96)
    if k >= 3: c.line([(1520, 900), (1520, 260)], 10, RED); c.line([(1490, 260), (1550, 260)], 10, RED); c.line([(1490, 900), (1550, 900)], 10, RED); c.text(1690, 560, "146 M", 110, RED)
    if k >= 4: L(c, "TALLEST THING ON EARTH FOR NEARLY 4,000 YEARS", 1000, size=58)
    return c
def clock(k):
    c = C(); c.ell(180, 290, 680, 790, WHITE, INK, 12); c.rect(400, 230, 460, 300, INK, None); a = [-60, 30, 150][k]+T.TT*240
    c.line([(430, 540), (430+190*math.cos(math.radians(a-90)), 540+190*math.sin(math.radians(a-90)))], 12, RED); c.ell(412, 522, 448, 558, INK, None)
    c.text(1240, 540, ["ABOUT 270\nBLOCKS A DAY", "1 BLOCK EVERY\n2-3 MINUTES", "ALL DAY.\nFOR 20 YEARS."][k], 120)
    return c
def seesaw(k=0):
    c = C(); c.line([(240, 700), (1680, 700)], 18, EARTH); c.poly([(900, 860), (960, 706), (1020, 860)], GREY, INK, 7); c.line([(200, 860), (1720, 860)], 7)
    c.block(330, 690, 300, 230); c.truck(1180, 690, 1.3); L(c, "ONE BLOCK = ABOUT ONE PICKUP TRUCK", 180, size=70)
    return c
def haul(k, lab=None, pour=False, ex="strain"):
    c = C().bg("sand"); dx = ((k % 2)+T.LP)*60
    if pour: c.ell(1420+dx, G-6, 1880, G+50, (196, 160, 110), None)
    c.sledge(120+dx, G, 320); c.block(140+dx, G-22, 280, 210)
    xs = [640+dx+i*170 for i in range(4)]; hs = crew(c, xs, G, 260, "pull", ["strain", "det", "strain", "pain"])
    s = c.fig(xs[-1]+175, G, 280, "pull", ex, "sid")
    c.line([(480+dx, G-60), hs[0]["hand"], s["hand"]], 8, EARTH)
    if pour:
        p = c.fig(1620+dx, G, 260, "pour", "n", "extra"); hx, hy = p["hand"]; c.jar(hx+10, hy+30, .6, False)
        for i in range(4): c.line([(hx+50+i*14, hy+20+i*40+(T.TT*3 % 1)*30), (hx+56+i*14, hy+44+i*40+(T.TT*3 % 1)*30)], 7, WATER)
    if lab: L(c, lab, 130, size=84)
    return c
def sand(k):
    c = C()
    def panel(x, wet):
        c.rect(x, 330, x+760, 800, WHITE, INK, 7, 16); c.rect(x+4, 660, x+756, 796, (196, 160, 110) if wet else SAND, None); c.line([(x, 660), (x+760, 660)], 6)
        c.sledge(x+200, 660, 240); c.block(x+215, 638, 210, 150)
        if not wet: c.poly([(x+470, 660), (x+540, 590), (x+640, 660)], SAND, INK, 6)
        c.text(x+380, 270, "WET" if wet else "DRY", 100, TEAL if wet else INK)
    panel(140, False)
    if k >= 1: panel(1020, True)
    if k >= 2: L(c, "HALF THE FORCE", 930, size=100, bg=MARI)
    return c
def lab(k):
    c = C(); c.rect(360, 520, 1560, 760, WHITE, INK, 8, 12); c.rect(366, 620, 1554, 754, (196, 160, 110), None); c.line([(360, 620), (1560, 620)], 5)
    c.sledge(700, 620, 200); c.block(715, 598, 170, 110); c.line([(960, 590), (1240, 590)], 7, EARTH); c.ell(1240, 540, 1340, 640, WHITE, INK, 7); c.line([(1290, 590), (1320, 560)], 7, RED)
    L(c, "UNIVERSITY OF AMSTERDAM, 2014", 160, size=70)
    if k: L(c, "DAMP SAND = TWICE AS STIFF", 900, size=84, bg=MARI)
    return c
def tombwall(k=0):
    c = C((236, 214, 160))
    for y in (120, 960): c.rect(0, y-40, W, y, EARTH, None); c.line([(0, y-40), (W, y-40)], 5); c.line([(0, y), (W, y)], 5)
    c.sledge(180, 800, 420); c.rect(260, 420, 520, 778, STONE, INK, 7, 30)
    hs = crew(c, [900, 1080, 1260, 1440, 1620], 800, 250, "pull", "n", "extra"); c.line([(640, 740), hs[0]["hand"], hs[-1]["hand"]], 8, EARTH)
    p = c.fig(690, 800, 230, "pour", "n", "extra"); hx, hy = p["hand"]; c.jar(hx+10, hy+30, .5, False); c.line([(hx+40, hy+30), (hx+60, hy+120)], 7, WATER)
    L(c, "OUR SKETCH OF A LATER TOMB PAINTING, ABOUT 1900 BC", 1020, size=44)
    return c
def mapt(k):
    c = C(); pts = [(900+70*math.sin(i/2.2), i*60) for i in range(19)]; c.line(pts, 120, WATER)
    c.pyramid(430, 520, 220, 150); c.ell(560, 440, 610, 490, RED, INK, 6); L(c, "GIZA", 600, 470, 80)
    c.block(1400, 620, 150, 100, WHITE); c.ell(1330, 520, 1380, 570, RED, INK, 6); L(c, "TURA", 700, 1470, 80)
    if k >= 1:
        for i in range(int(9*T.ease(T.LT/0.9)) if k == 1 else 9): x = 1320-i*82; y = 560-i*8; c.ell(x, y, x+22, y+22, INK, None)
    if k >= 2: L(c, "WHITE OUTER STONE", 150, size=84)
    return c
def merer(k):
    c = C().bg("river", 560); c.rect(0, 520, W, 560, SAND, None); c.line([(0, 520), (W, 520)], 5)
    for i in range(4): c.block(700+i*120, 770, 110, 80, WHITE)
    m = c.fig(540, 800, 290, "write", "det", "scribe"); c.papyrus(m["hand"][0]+50, m["hand"][1]+10, .45)
    crew(c, [1180, 1290, 1400], 800, 240, "hold", "strain"); c.boat(400, 830, 1120)
    for x in (1240, 1350, 1460): c.line([(x, 730), (x+70, 940)], 8, EARTH)
    if k >= 1: L(c, "MERER", 330, 540, 96, bg=MARI)
    if k >= 2: L(c, "BOAT CREW: ABOUT 40", 150, size=84)
    return c
def harbour(k):
    c = C().bg("sand", 620); c.rect(0, 560, W, 620, WATER, None); c.line([(0, 560), (W, 560)], 5)
    c.ell(980, 520, 1380, 900, GREY, INK, 7); c.ell(1300, 560, 1760, 920, (190, 178, 160), INK, 7)
    s = c.fig(640, G+20, 340, "hold", "wow", "sci"); c.papyrus(s["hand"][0]+60, s["hand"][1]-10, .6)
    L(c, "RED SEA COAST, 2013", 130)
    if k: L(c, "OLDEST INSCRIBED PAPYRUS EVER FOUND", 1000, size=64, bg=MARI)
    return c
def loop(i):
    c = C(); caps = ["LOAD STONE", "SAIL TO GIZA", "SLEEP", "SAIL BACK"]
    for j in range(4):
        x = 110+j*440; on = (j == i) or i >= 4
        c.rect(x, 330, x+380, 720, WHITE if on else (240, 232, 220), TEAL if on else INK, 12 if on else 6, 18)
        cx = x+190
        if j == 0: c.block(cx-90, 620, 180, 130)
        if j in (1, 3): c.boat(cx-120, 590, 240); c.block(cx-40, 540, 80, 60) if j == 1 else None; c.text(cx, 430, "->" if j == 1 else "<-", 90)
        if j == 2: c.fig(cx+100, 600, 200, "stand", "sleep", "scribe", rot=-90); c.text(cx-70, 440, "Z Z", 70)
        c.text(cx, 790, caps[j], 60, INK if on else (150, 140, 128))
    L(c, "MERER'S LOGBOOK" if i < 4 else "REPEAT.", 170, size=90)
    return c
def count(k):
    c = C(); c.text(W/2, 300, "2-3 ROUND TRIPS\nEVERY 10 DAYS", 120)
    if k:
        for i in range(20): c.block(360+(i % 10)*124, 760+(i//10)*110, 104, 90, WHITE)
        c.text(W/2, 580, "ABOUT 200 BLOCKS A MONTH", 90, TEAL)
    return c
def shrugm(k):
    c = C().bg("river", 600); c.pyramid(1380, 600, 1000, 540, WHITE, 1, 0)
    m = c.fig(480, 800, 300, ["chin", "shrug", "write"][k], ["bored", "bored", "det"][k], "scribe"); c.boat(300, 830, 520)
    if k == 2: c.papyrus(m["hand"][0]+50, m["hand"][1]+10, .45)
    if k >= 1: L(c, "\"HORIZON OF KHUFU\"", 130, 1380, 80)
    return c
def timesheet(k):
    c = C().bg("room", 760); c.rect(820, 640, 1500, 680, EARTH, INK, 6); c.line([(880, 680), (880, 900)], 12, EARTH); c.line([(1440, 680), (1440, 900)], 12, EARTH)
    c.rect(1000, 540, 1300, 640, WHITE, INK, 5)
    for i in range(4): c.line([(1020, 562+i*20), (1280, 562+i*20)], 3, (150, 150, 150))
    c.fig(640, 900, 380, "write", "bored", "modern"); L(c, "TIMESHEET", 300, 620, 80)
    if k: L(c, "4,500 YEARS OLD", 1000, size=84, bg=MARI)
    return c
def pay(k):
    c = C(); c.ell(710, 290, 1210, 790, MARI, INK, 12); c.text(960, 530, "$" if k == 0 else "?", 300)
    if k: c.redx(960, 540, 260, 36); L(c, "NO COINS FOR ALMOST 2,000 YEARS", 940, size=76)
    return c
def ration(k):
    c = C().bg("sand"); c.fig(1380, G, 320, "hold" if k < 1 else "stand", "det", "boss", flip=True, staff=(k >= 1))
    s = c.fig(620, G, 340, "hold", "n" if k == 0 else "wow" if k < 3 else "worry", "sid"); hx, hy = s["hand"]
    if k >= 1:
        for i in range(10): c.loaf(hx+10+(i % 2)*10, hy-i*42, 1.0)
        c.jar(960, G, 1.3)
    if k >= 2: L(c, "10 LOAVES + A MEASURE OF BEER", 110, size=76)
    if k >= 3: L(c, "PER DAY", 230, size=96, bg=MARI)
    return c
def staple(k=0):
    c = C(); c.jar(700, 800, 3.0); c.loaf(1250, 760, 3.0); L(c, "BEER = FOOD, NOT A PARTY", 160, size=90)
    return c
def pottery(k):
    c = C()
    for i in range(9): x = 300+(i % 5)*110+(i//5)*55; y = 720-(i//5)*110; c.poly([(x-50, y-110), (x+50, y-110), (x+24, y), (x-24, y)], (200, 150, 110), INK, 6)
    c.text(520, 840, "BREAD MOULDS: #1", 70)
    if k:
        for i in range(5): c.jar(1200+(i % 3)*130+(i//3)*65, 720-(i//3)*130, 1.0, False)
        c.text(1400, 840, "BEER JARS: #2", 70)
    return c
def herd(k):
    c = C().bg("sand")
    for i in range(3): c.animal(300+i*300+T.GP*110, G-(i % 2)*40, 1.4)
    for i in range(3): c.animal(1180+i*230+T.GP*110, G+60-(i % 2)*50, 1.0, WHITE, False)
    L(c, "21 CATTLE + 23 SHEEP, EVERY DAY", 130, size=80)
    if k: L(c, "(HAWASS'S ESTIMATE)", 250, size=56)
    return c
def feast(k, done=0):
    c = C().bg("night", 640); c.fire(960, 900, 1.6)
    crew(c, [300, 1500, 1720], 900, 280, "cheer", ["joy", "joy2", "joy"], sit=True)
    s = c.fig(640, 900, 300, "up", "joy" if k else "wow", "sid", sit=True); hx, hy = s["hand"]; c.bone(hx-10, hy+10, hx+90, hy-70, (200, 110, 80))
    if k == 0: L(c, "LEHNER: MOSTLY AT BIG FEASTS", 110, size=70)
    if done: Q(c, 4, done)
    return c
def skel(k):
    c = C(); x = 620
    c.poly(rr_pts(x, 230, 170, 150, 44), WHITE, INK, 7); c.ell(x-46, 205, x-16, 240, INK, None); c.ell(x+16, 205, x+46, 240, INK, None)
    for i in range(9): c.rect(x-22, 322+i*44, x+22, 356+i*44, WHITE, INK, 5, 8)
    for i in range(4): c.line([(x-130, 360+i*50), (x-22, 345+i*50)], 9); c.line([(x+22, 345+i*50), (x+130, 360+i*50)], 9)
    c.bone(x-160, 350, x-230, 620); c.bone(x+160, 350, x+230, 620, brk=(k >= 3)); c.bone(x-50, 740, x-70, 1000); c.bone(x+50, 740, x+70, 1000)
    if k == 0: c.text(1320, 520, "BONES\nKEEP\nRECEIPTS", 130)
    if k >= 1: c.ell(x-90, 440, x+90, 740, None, RED, 10); c.text(1320, 400, "WORN-DOWN SPINES", 84, RED if k == 1 else INK)
    if k >= 2: c.ell(x-130, 690, x+130, 800, None, RED, 10); c.text(1320, 560, "WORN-OUT JOINTS", 84, RED if k == 2 else INK)
    if k >= 3: c.text(1320, 720, "SNAPPED LIMBS", 84, RED)
    return c
def healed(k):
    c = C()
    if k < 2:
        c.bone(360, 540, 1560, 540); c.ell(900, 505, 1020, 575, WHITE, INK, 6)
        if k == 1:
            for y in (480, 600): c.line([(620, y), (1300, y)], 22, EARTH)
            for x in (720, 960, 1200): c.line([(x, 470), (x, 610)], 14, PAPER); c.line([(x-8, 470), (x-8, 610)], 4); c.line([(x+8, 470), (x+8, 610)], 4)
        L(c, "HEALED STRAIGHT" if k == 0 else "SET WITH A SPLINT", 220, size=100)
    else:
        c.bone(360, 540, 1200, 540); c.ell(1160, 500, 1250, 580, WHITE, INK, 6); L(c, "AMPUTATION. PATIENT SURVIVED.", 220, size=84)
    return c
def accident(k):
    c = C().bg("sand")
    if k == 0: c.poly([(820, 860), (880, 560), (1260, 640), (1200, 860)], STONE, INK, 7); c.fig(560, G, 320, "shrug", "wow", "sid"); c.text(700, 380, "!", 200, RED)
    else:
        c.block(760, G, 420, 300); c.fig(700, G+30, 300, "cheer", "pain", "sid", rot=-90)
        for i in range(8): a = i*45; c.line([(760+90*math.cos(math.radians(a)), 700+90*math.sin(math.radians(a))), (760+150*math.cos(math.radians(a)), 700+150*math.sin(math.radians(a)))], 10, RED)
    return c
def carryS(k):
    c = C().bg("sand"); x = 500+(k+T.LP)*320
    a = c.fig(x, G, 290, "carry", "det", "extra"); b = c.fig(x+330, G, 290, "carry", "worry", "extra")
    c.fig(x+320, G-360, 280, "stand", "pain", "sid", rot=-90)
    return c
def splint(k):
    c = C().bg("hall", 520); c.rect(380, 880, 1100, 910, (226, 200, 150), INK, 5, 8)
    c.fig(1040, 880, 320, "stand", "smile" if k else "worry", "sid", rot=-90)
    for y in (836, 912): c.line([(880, y), (1080, y)], 12, EARTH)
    for x in (920, 980, 1040): c.line([(x, 830), (x, 918)], 10, PAPER)
    c.fig(280, 900, 300, "hold", "det", "extra")
    if k: h = c.fig(1360, 900, 300, "hold", "smile", "extra", flip=True); c.loaf(h["hand"][0]-40, h["hand"][1]+10, 1.2)
    if k == 2: L(c, "WORKPLACE HEALTHCARE, 2560 BC", 130, size=80, bg=MARI)
    return c
def lifebar(k=0):
    c = C(); c.rect(260, 520, 1660, 600, WHITE, INK, 7, 10); c.text(260, 680, "0", 80); c.text(1660, 680, "70", 80)
    x = 260+1400*35/70; c.rect(260, 520, 260+(x-260)*max(.03, T.ease(T.LT/0.7)), 600, MARI, INK, 7, 10); c.poly([(x, 510), (x-36, 430), (x+36, 430)], RED, INK, 6); L(c, "MOST DIED IN THEIR THIRTIES", 300, size=84)
    return c
def home(k, done=0):
    if k == 1:
        c = C().bg("hall", 520); c.rect(560, 880, 1300, 910, (226, 200, 150), INK, 5, 8); c.fig(940, 880, 340, "self", "worry", "extra"); L(c, "A NEW CREW TAKES YOUR BUNK", 150, size=76)
    else:
        c = C().bg("river", 560); c.rect(0, 520, W, 560, BARLEY, None); c.line([(0, 520), (W, 520)], 5)
        for x in (160, 380): c.hut(x, 540, 160, 110)
        c.fig(900, 800, 300, "wave", "smile", "sid", flip=True); crew(c, [1060, 1190], 800, 240, "stand", "smile", flip=True); c.boat(720, 830, 600)
    if done: Q(c, 4, done)
    return c
def hidden(k):
    c = C(); c.quest(4, 3, "BE REMEMBERED" if k else None, x=545, y=200)
    if k: c.marker(480, 800, 36)
    return c
def king(k):
    c = C().bg("sand"); c.pyramid(1100, 700, 1300, 620, STONE, 1, 12)
    c.poly([(1020, 300), (1050, 230), (1080, 280), (1100, 220), (1120, 280), (1150, 230), (1180, 300)], MARI, INK, 6)
    L(c, "A MACHINE FOR ONE MAN'S AFTERLIFE", 110, size=68)
    if k: c.fig(300, G+60, 260, "shrug", "sad", "sid"); L(c, "YOURS ISN'T IN THE BUDGET", 1010, size=64)
    return c
def tombs(k, dusk=False):
    c = C().bg("dusk" if dusk else "sand", 640); c.pyramid(1380, 640, 1100, 560, (214, 200, 190) if dusk else STONE, 1, 0)
    c.poly([(0, 1080), (0, 760), (900, 640), (1100, 1080)], (120, 100, 96) if dusk else DSAND, None)
    for i, (x, y) in enumerate([(160, 900), (340, 860), (520, 930), (700, 880), (260, 1020), (600, 1040)]): c.tomb(x, y)
    if not dusk: L(c, ["1990", "THE BUILDERS' OWN TOMBS", "MANY ARE FROM LATER GENERATIONS"][k], 120, 520, [120, 72, 56][k])
    elif k: L(c, "BESIDE THE KING", 150, 520, 90)
    return c
def inside(k):
    c = C().bg("cave", 700); c.rect(300, 660, 1620, 700, EARTH, INK, 6)
    for i in range(3): c.jar(520+i*190, 660, 1.5)
    for i in range(3): c.loaf(1160+i*170, 660, 1.5)
    if k: L(c, "SAME PAY. FOREVER.", 200, size=110)
    return c
def recap(n):
    c = C(); caps = ["DRAFTED", "FED", "HURT", "PATCHED UP", "SENT HOME"]
    for i in range(n):
        x = 240+i*360
        if i == 0: c.fig(x-40, 560, 220, "point", "det", "boss")
        if i == 1: c.loaf(x, 520, 1.8)
        if i == 2: c.bone(x-90, 380, x+90, 540, brk=True)
        if i == 3: c.bone(x-90, 460, x+90, 460); c.line([(x-60, 420), (x+60, 420)], 16, EARTH); c.line([(x-60, 500), (x+60, 500)], 16, EARTH)
        if i == 4: c.boat(x-110, 500, 220)
        c.text(x, 700, caps[i], 74)
    c.text(W/2, 900, "NOT A SLAVE. NOT EXACTLY A VOLUNTEER.", 92, TEAL)
    return c
def cutaway(k):
    c = C(); c.line([(160, 940), (1760, 940)], 7); c.pyramid(960, 940, 1400, 780, STONE, 1, 0)
    c.rect(880, 600, 1040, 680, WHITE, INK, 6)
    for i in range(5): c.rect(880, 560-i*34, 1040, 584-i*34, RED if k else WHITE, INK, 5)
    c.line([(870, 410), (960, 360), (1050, 410)], 7)
    L(c, "KING'S BURIAL ROOM", 640, 1330, 54)
    if k: L(c, "SEALED CHAMBERS ABOVE IT", 480, 1380, 54, c=RED)
    return c
def paint(k):
    c = C(STONE)
    for y in (360, 720): c.line([(0, y), (W, y)], 6, (190, 176, 150))
    for x, y0 in ((500, 0), (1300, 0), (900, 360), (300, 720), (1500, 720)): c.line([(x, y0), (x, y0+360)], 6, (190, 176, 150))
    if k == 0: c.line([(360, 560), (620, 500), (900, 580)], 46, RED); c.line([(900, 580), (1200, 380)], 22, EARTH); c.line([(880, 600), (930, 560)], 50, INK)
    if k == 1: c.line([(360, 560), (620, 500), (900, 580), (1180, 500), (1500, 560)], 46, RED); c.line([(520, 700), (1320, 680)], 46, RED); L(c, "NOT A PRAYER. A TEAM NAME.", 200, size=84)
    if k == 2: c.text(W/2, 540, "FRIENDS OF KHUFU", 190, RED)
    return c
def finale(k):
    if k == 0:
        c = C().bg("sand"); c.pyramid(960, 700, 1300, 620, STONE, 1, 12); c.poly([(880, 300), (910, 230), (940, 280), (960, 220), (980, 280), (1010, 230), (1040, 300)], MARI, INK, 6); L(c, "THE KING: REMEMBERED", 1000, size=76); return c
    c = C().bg("sand"); c.block(1240, G, 520, 380); c.line([(1320, 560), (1420, 520), (1520, 590), (1640, 540)], 22, RED); c.line([(1340, 660), (1500, 640)], 22, RED)
    crew(c, [240, 440, 840, 1040], G, 300, "cheer", ["joy", "joy2", "joy", "smile"])
    s = c.fig(640, G, 330, "cheer", "joy", "sid"); hx, hy = s["head"]; c.ell(hx+8, hy+62, hx+30, hy+84, RED, None)
    if k == 2: L(c, "THEY SIGNED IT", 130, size=110, c=RED)
    if k == 3: Q(c, 4, 4, "BE REMEMBERED"); L(c, "QUEST COMPLETE", 130, 560, 110, bg=MARI)
    return c
def questfield(shown, done=0): return Q(field(0), shown, done)

def ringed():
    c = tombwall(); c.ell(560, 440, 840, 840, None, RED, 12); return c
def F(f, *a, **k):
    g = lambda: f(*a, **k); g.scene = f.__name__; return g
# (narration, [frames], chime?)  — respellings for the voice only
U = [
 ("You were told slaves built the pyramids.", [F(myth, 0)]),
 ("Whips. Chains. A hundred thousand prisoners in the sand.", [F(myth, 1), F(myth, 2), F(myth, 3)]),
 ("That picture comes from a Greek writer who showed up two thousand years late.", [F(herod, 0), F(herod, 1)]),
 ("The people who actually built it left a diary, a payroll, and their own skeletons.", [F(evid, 1), F(evid, 2), F(evid, 3)]),
 ("And their story is stranger. They were paid in beer.", [F(beer, 0)]),
 ("They couldn't say no. And one crew called itself the Drunkards.", [F(beer, 1), F(beer, 2)]),
 ("So let's make you one of them.", [F(intro, 0), F(intro, 1)], "chime"),
 ("It's about twenty-five sixty B C. You're seventeen.", [F(card, "2560 BC"), F(field, 0)]),
 ("You farm barley in a village on the Nile.", [F(field, 1)]),
 ("You are made up. Everything that happens to you is in the evidence.", [F(card, "YOU ARE MADE UP.", "THE FACTS AREN'T.", 140)]),
 ("Here's your quest log. One: get to Giza.", [F(questfield, 0), F(questfield, 1)], "tick"),
 ("Two: earn your bread.", [F(questfield, 2)], "tick"),
 ("Three: get home in one piece.", [F(questfield, 3)], "tick"),
 ("There's a fourth quest hidden at the end. Almost nobody sees it coming.", [F(questfield, 4)], "tick"),
 ("Every summer the Nile floods your fields. For weeks, there's nothing to farm.", [F(flood, 0), lambda: L(flood(0), "FLOOD SEASON: NOTHING TO FARM", 130)]),
 ("That's when the king's men arrive.", [F(flood, 1)]),
 ("They don't want your grain. They want you.", [F(flood, 2), F(flood, 3)]),
 ("Historians still argue about how much choice you had.", [F(scholars, 0)]),
 ("Zahi Hawahss, Egypt's best-known archaeologist, calls men like you conscripts.", [lambda: L(scholars(0), "EGYPT'S BEST-KNOWN ARCHAEOLOGIST", 900, 620, 50), F(scholars, 1)]),
 ("Mark Layner, who dug up your future home, calls it obligatory labor. A tax you pay with your back.", [F(scholars, 2), F(scholars, 3)]),
 ("He compares it to a barn-raising. Everyone is expected to show up. Not everyone is thrilled.", [F(barn, 0), F(barn, 1)]),
 ("So you're not a slave. Nobody owns you. But no isn't on the menu either.", [F(menu, 0), F(menu, 1)]),
 ("You climb into a boat with the other boys from your village, and you sail for Giza.", [F(boat, 0), F(boat, 1)]),
 ("Quest one, complete.", [F(boat, 2, 1)], "chime"),
 ("You expect a camp. You get a city.", [F(city, 0), F(city, 1)]),
 ("Archaeologists call it the Lost City of the Pyramid Builders. The crown built it for exactly one job.", [F(city, 2), F(city, 1)]),
 ("There are royal grain silos. There are bakeries by the dozen.", [F(city, 3), F(city, 4)]),
 ("You sleep in a long hall, shoulder to shoulder, with forty or fifty other men.", [F(hall, 0), F(hall, 1)]),
 ("About twenty thousand people may live here, counting the bakers, the brewers and the scribes.", [F(bars, 0), F(bars, 2)]),
 ("Not a hundred thousand. And only about half of them ever touch a stone.", [F(bars, 1), F(bars, 3)]),
 ("Then you get your team. Crews had names, and they painted them on the blocks.", [F(team, 0), F(team, 1)]),
 ("One was the Friends of Koofoo. A few kings later, another was the Drunkards of Men-cow-ray.", [F(team, 2), F(team, 3)]),
 ("Picture a company softball team. Except the season lasts for months, and the ball weighs two and a half tons.", [F(softball, 0), F(softball, 1)]),
 ("Here's the job. The Great Pyramid needs about two point three million blocks.", [F(pyr, 0), F(pyr, 1)]),
 ("If the work took around twenty-three years, that's roughly two hundred and seventy blocks a day.", [F(pyr, 2), F(clock, 0)]),
 ("One block every two or three minutes. All day. For two decades.", [F(clock, 1), F(clock, 2)]),
 ("A typical block weighs about as much as a pickup truck.", [F(seesaw)]),
 ("When it's finished it will stand one hundred and forty-six metres tall. Nothing humans build will beat it for nearly four thousand years.", [F(pyr, 3), F(pyr, 4)]),
 ("And you have rope, a wooden sledge, and your crew.", [F(haul, 0), F(haul, 1)]),
 ("Plus one trick. Somebody walks in front and pours water on the sand.", [F(haul, 2), F(haul, 3, None, True)]),
 ("It looks like a ritual. It's physics.", [F(haul, 4, "IT LOOKS LIKE A RITUAL", True), F(haul, 5, "IT'S PHYSICS", True)]),
 ("In twenty fourteen, physicists in Amsterdam tested it. Damp sand is about twice as stiff as dry sand.", [F(lab, 0), F(lab, 1)]),
 ("The sledge stops digging in, and the force you need drops by half.", [F(sand, 0), F(sand, 1), F(sand, 2)]),
 ("A later Egyptian tomb painting shows exactly that. A man at the front of a sledge, pouring water.", [F(tombwall), lambda: ringed()]),
 ("Half the effort. Still a truck.", [F(haul, 0, "HALF THE EFFORT", True), F(haul, 1, "STILL A TRUCK", True, "pain")]),
 ("The best stone doesn't come from here. The white outer blocks come from Toora, across the river.", [F(mapt, 0), F(mapt, 1), F(mapt, 2)]),
 ("We know because one of your coworkers kept a logbook.", [F(merer, 0)]),
 ("His name was Mehrer. He ran a boat crew of about forty men.", [F(merer, 1), F(merer, 2)]),
 ("In twenty thirteen his diary turned up at an ancient harbour on the Red Sea. It's the oldest inscribed papyrus ever found.", [F(harbour, 0), F(harbour, 1)]),
 ("And it is gloriously boring. Load stone. Sail to the pyramid. Sleep there. Sail back. Repeat.", [F(loop, -1), F(loop, 0), F(loop, 1), F(loop, 2), F(loop, 3), F(loop, 4)]),
 ("Two or three round trips every ten days. About two hundred blocks a month.", [F(count, 0), F(count, 1)]),
 ("He never once says the pyramid is amazing. He calls it by its name, Horizon of Koofoo, and goes back for more rocks.", [F(shrugm, 0), F(shrugm, 1), F(shrugm, 2)]),
 ("It's a timesheet. It just happens to be four and a half thousand years old.", [F(timesheet, 0), F(timesheet, 1)]),
 ("So what does all this pay? Not coins. Coins won't exist for almost two thousand years.", [F(pay, 0), F(pay, 1)]),
 ("You're paid in food. The standard ration for a laborer in this era was ten loaves of bread and a measure of beer. Per day.", [F(ration, 0), F(ration, 1), F(ration, 2), F(ration, 3)]),
 ("Beer here is a staple food, not a party.", [F(staple)]),
 ("Bread moulds are the most common pottery in the whole city. Beer jars come second.", [F(pottery, 0), F(pottery, 1)]),
 ("And there's meat. Hawahss estimates twenty-one cattle and twenty-three sheep arrived every single day.", [F(herd, 0), F(herd, 1)]),
 ("Layner thinks most of it was served at big feasts.", [F(feast, 0)]),
 ("Either way, you're eating beef. For a farm kid, that's a feast.", [F(feast, 1)]),
 ("Quest two, complete. You earned your bread. Literally.", [F(feast, 1, 2)], "chime"),
 ("Quest three is the hard one. Get home in one piece.", [F(haul, 2, None, False, "worry")]),
 ("Because the builders' bones were found too. And bones keep receipts.", [F(skel, 0)]),
 ("Worn-down spines. Worn-out joints. Arms and legs that had snapped.", [F(skel, 1), F(skel, 2), F(skel, 3)]),
 ("But here's the twist. Most of those breaks had healed straight.", [F(healed, 0)]),
 ("Somebody set them with a splint.", [F(healed, 1)]),
 ("A few skeletons even show amputations the patient survived.", [F(healed, 2)]),
 ("So when a block rolls onto your leg, and one day something will, you aren't left in the sand.", [F(accident, 0), F(accident, 1)]),
 ("Someone carries you out. Someone sets the bone. And you keep getting your bread.", [F(carryS, 0), F(splint, 0), F(splint, 1)]),
 ("Four and a half thousand years ago, you had workplace healthcare.", [F(splint, 2)]),
 ("It still wasn't a long life. Most of the people in that cemetery died in their thirties.", [F(card, "NOT A LONG LIFE"), F(lifebar)]),
 ("But if your months are up and your legs still work, you sail home. A new crew takes your bunk.", [F(home, 0), F(home, 1)]),
 ("Quest three, complete. Barely.", [F(home, 0, 3)], "chime"),
 ("Now the hidden one.", [F(hidden, 0), F(hidden, 1)], "chime"),
 ("The pyramid is a machine for one man's afterlife. Yours isn't in the budget.", [F(king, 0), F(king, 1)]),
 ("But in nineteen ninety, a cemetery turned up in the shadow of the pyramids. Small, modest tombs. The builders' own.", [F(tombs, 0), F(tombs, 1)]),
 ("Not every grave belongs to Koofoo's crews. Many come from later generations of builders.", [F(tombs, 2), lambda: L(tombs(2), "NOT ALL OF THEM KHUFU'S CREWS", 1000, 560, 56)]),
 ("Inside some of them: jars of beer and loaves of bread, packed for the next world.", [F(inside, 0), lambda: L(inside(0), "PACKED FOR THE NEXT WORLD", 200, size=84)]),
 ("Same pay. Forever.", [F(inside, 1)]),
 ("And think about where they are. Slaves don't get buried beside the king.", [F(tombs, 0, True), F(tombs, 1, True)]),
 ("So no, you weren't a slave. You weren't exactly a volunteer either.", [F(recap, 0)]),
 ("You were a farm kid who got drafted, got fed, got hurt, got patched up, and got sent home.", [F(recap, 1), F(recap, 2), F(recap, 3), F(recap, 4), F(recap, 5)]),
 ("And high inside the Great Pyramid, in sealed chambers above the king's burial room, there's red paint on the stone.", [F(cutaway, 0), F(cutaway, 1), F(paint, 0)]),
 ("It isn't a prayer for the king. It's a team name.", [F(paint, 1)]),
 ("Friends of Koofoo.", [F(paint, 2)]),
 ("The king wanted to be remembered forever. He was.", [F(finale, 0)]),
 ("But so was the crew. They signed it.", [F(finale, 1), F(finale, 2)]),
 ("Quest complete.", [F(finale, 3)], "chime"),
]

# Display spellings for captions: the narration text is respelled for the voice, captions show the real names.
CAPTION_FIX = [("Koofoo", "Khufu"), ("Hawahss", "Hawass"), ("Layner", "Lehner"), ("Mehrer", "Merer"), ("Toora", "Tura"), ("Men-cow-ray", "Menkaure"),
               ("twenty-five sixty B C", "2560 BC"), ("twenty fourteen", "2014"), ("twenty thirteen", "2013"), ("nineteen ninety", "1990"),
               ("two point three million", "2.3 million"), ("one hundred and forty-six", "146"), ("two hundred and seventy", "270"),
               ("twenty-three years", "23 years"), ("two and a half tons", "2.5 tons"), ("forty or fifty", "40 or 50"), ("twenty thousand", "20,000"), ("a hundred thousand", "100,000")]
