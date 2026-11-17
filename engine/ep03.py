"""EP003: You Wake Up in Pompeii. Would You Get Out in Time?   (Roman Italy, AD 79; point-of-view pillar)

Same contract as ep01.py / ep02.py. Motion helpers (app, E, lerp, step, arrow) come from ep02.
A small "hour" chip in the top-left corner runs through the whole episode: it is the clock of the story.
"""
from thsq import *
import math
import thsq as T
import life
from ep02 import E, app, lerp, step, L, card, arrow, chip, F
G = 900
ROWS = ["GET THROUGH THE MORNING", "READ THE SKY", "GET OUT IN TIME"]; HID = "START AGAIN"
SK = {"day": ((140, 196, 226), (236, 240, 230)), "dawn": ((122, 150, 200), (250, 214, 176)), "noon": ((120, 190, 232), (226, 240, 240)),
      "ash": ((30, 28, 36), (74, 64, 62)), "dusk": ((60, 52, 84), (214, 130, 96)), "glow": ((24, 20, 28), (120, 60, 44)), "pale": ((176, 176, 176), (226, 222, 214))}
PAVE = (192, 186, 180); PAVE2 = (164, 158, 154)
HOUSES = [(30, 300, 300, OCHRE, 0), (345, 340, 350, RWALL, 1), (700, 280, 300, (232, 200, 170), 0), (995, 350, 340, RWALL, 0), (1360, 300, 310, OCHRE, 1), (1675, 330, 345, RWALL, 0)]
COATS = ["blue", "brown", "green", "rose", "teal", "slate", "red"]
def Q(c, shown=4, done=0, hidden=None): c.questlog(ROWS, shown, done, hidden); return c
def sky(c, hz, kind="day", clouds=True):
    c.im.paste(life._grad(hz, *SK[kind]), (0, 0))
    if clouds and kind in ("day", "dawn", "noon"):
        for i, (cx, cy, k) in enumerate(((260, 110, 1.0), (900, 70, .7))):
            xx = (cx+T.TT*(7+3*i)) % (W+400)-200
            for dx, dy, r in ((-70, 10, 44), (0, -14, 60), (70, 12, 46), (0, 22, 50)): c.da.ellipse([(xx+dx*k-r*k*1.5)*S, (cy+dy*k-r*k)*S, (xx+dx*k+r*k*1.5)*S, (cy+dy*k+r*k)*S], fill=(255, 255, 255, 200))
def dim(c, a=120, col=(20, 18, 26)): c.da.rectangle([0, 0, W*S, H*S], fill=(*col, int(a)))
def hud(c, t, night=False):
    w = c.tw(t, 46)+110; c.rect(36, 36, 36+w, 116, PAPER, INK, 6, 16)
    if night: c.ell(58, 54, 102, 98, NAVY, INK, 4); c.ell(72, 50, 110, 88, PAPER, None)
    else:
        c.ell(60, 56, 100, 96, MARI, INK, 4)
        for a in range(0, 360, 45): c.line([(80+26*math.cos(math.radians(a+T.TT*20)), 76+26*math.sin(math.radians(a+T.TT*20))), (80+34*math.cos(math.radians(a+T.TT*20)), 76+34*math.sin(math.radians(a+T.TT*20)))], 4, MARI, False)
    c.text(124, 74, t, 46, INK, "lm")
def town(kind="day", hz=600, base=790, peak=True, green=True, plume=None, layer=0.0, shake=0.0, mountain=True, mcx=1280):
    """The street set: sky, the mountain, a row of house fronts, paving. layer = depth of pumice in px; shake jitters the houses."""
    c = C(PAVE); sky(c, hz, kind)
    if mountain:
        tip = c.vesuvius(mcx, hz+60, 1150, 470, VINE if green else (132, 124, 118), green, peak)
        if plume: c.plume(tip[0], tip[1]+30, plume[0], plume[1], T.TT, plume[2] if len(plume) > 2 else ASHC, plume[3] if len(plume) > 3 else 1.0)
    c.rect(0, hz+60, W, H, PAVE, None)
    for i, (x, w, h, col, shop) in enumerate(HOUSES):
        dx = shake*8*math.sin(T.TT*38+i*2.1); dy = shake*5*math.sin(T.TT*31+i)
        c.rhouse(x+dx, base+dy, w, h, col, TERRA if i % 2 == 0 else (150, 100, 80), shop=bool(shop))
    c.rect(0, base, W, base+34, (214, 208, 200), INK, 5); c.rect(0, base+34, W, H, PAVE2, None)
    for i in range(9): c.line([(i*240-40, base+40), (i*250-120, H)], 4, (140, 134, 130), False)
    for j in (1, 2): c.line([(0, base+34+j*90), (W, base+34+j*90)], 4, (140, 134, 130), False)
    if layer > 0:
        yy = base+34-layer; pts = [(0, yy)]+[(x, yy+10*math.sin(x*.013)) for x in range(0, W+1, 120)]+[(W, H), (0, H)]; c.poly(pts, PUM, INK, 5)
    return c
def roomset(wall=(236, 214, 182), fl=(176, 136, 100), hz=800):
    c = C(wall); c.rect(0, hz, W, H, fl, None); c.line([(0, hz), (W, hz)], 6, INK, False)
    for i in range(1, 8): c.line([(i*260-60, hz+6), (i*280-180, H)], 3, (156, 118, 86))
    return c
def folk(c, xs, y=980, h=280, exs=("worry", "wow", "n", "sad"), poses=("stand", "shrug", "stand", "chin"), pil=False, flip=None):
    out = []
    for i, x in enumerate(xs):
        f = c.person(x, y+(i % 3)*28, h-(i % 2)*20, poses[i % len(poses)], exs[i % len(exs)], COATS[i % 7], flip=(i % 2 == 1) if flip is None else flip)
        if pil: c.pillow(f)
        out.append(f)
    return out
def sidp(c, x, y, h, pose="stand", ex="n", pil=False, **k):
    f = c.fig(x, y, h, pose, ex, "modern", **k)
    if pil: c.pillow(f)
    return f

# ================= cold open =================
def wake(k=0):
    c = roomset((214, 196, 186)); c.rect(1320, 150, 1700, 470, SK["dawn"][1], INK, 9); c.ell(1450, 330, 1570, 450, MARI, None); c.line([(1510, 150), (1510, 470)], 7); c.rect(1300, 470, 1720, 494, WOOD, INK, 5)
    c.rect(300, 720, 1100, 760, WOOD, INK, 6, 4); c.line([(330, 760), (330, 900)], 14, WOOD); c.line([(1070, 760), (1070, 900)], 14, WOOD); c.rect(320, 664, 1080, 724, (232, 220, 206), INK, 6, 14); c.rect(330, 626, 520, 676, WHITE, INK, 5, 18)
    q = app("sit", .5, .3); sidp(c, 700, 664, 300, "stand" if q < 1 else "up", "sleep" if q < .6 else "bored", sit=True)
    hud(c, "FIRST LIGHT"); return c
def clockbar(k):
    c = C(); x0, x1 = 200, 1720; c.rect(x0, 470, x1, 600, WHITE, INK, 7, 12); q = app("cb0", 1.0, .1); xm = x0+(x1-x0)*7/25
    c.rect(x0, 470, x0+(xm-x0)*q, 600, MARI, INK, 7, 12); c.text(x0, 660, "DAWN", 54); c.text(xm, 660, "ABOUT 1 PM", 54, RED)
    c.text((x0+xm)/2, 380, "NORMAL LIFE", 70); c.text((x0+xm)/2, 300, "ABOUT 7 HOURS", 90, RED)
    if k >= 1:
        q2 = app("cb1", 1.1, .1); c.rect(xm, 470, xm+(x1-xm)*q2, 600, NAVY, INK, 7, 12); c.text((xm+x1)/2, 535, "ONE NIGHT", 80, PAPER); c.text(x1, 660, "NEXT MORNING", 54)
        L(c, "ONE DECISION", 880, size=110, bg=MARI)
    return c
def crowdsplit(k):
    c = C()
    for i in range(96):
        col, row = i % 16, i//16; x = 210+col*100; y = 300+row*110; out = i >= 86
        c.line([(x, y+18), (x, y+52)], 22, INK, False); c.line([(x, y+18), (x, y+52)], 14, (150, 146, 142) if (out and k) else TEAL, False); c.ell(x-20, y-24, x+20, y+14, PAPER, INK, 5)
    L(c, "MOST PEOPLE GOT OUT ALIVE", 130, size=84)
    if k: L(c, "MORE THAN A THOUSAND DID NOT", 990, 1180, 72, bg=MARI); c.text(380, 990, "(ICONS NOT TO SCALE)", 44, (120, 110, 98))
    return c
def whenleft(k=0):
    c = C(); c.ell(760, 240, 1160, 640, WHITE, INK, 12); a = T.TT*1.2
    c.line([(960, 440), (960+150*math.cos(a), 440+150*math.sin(a))], 12, RED, False); c.line([(960, 440), (960+90*math.cos(a/12), 440+90*math.sin(a/12))], 16, INK, False); c.ell(942, 422, 978, 458, INK, None)
    L(c, "THE DIFFERENCE: MOSTLY WHEN THEY LEFT", 860, size=72, bg=MARI); return c
def intro(k):
    c = C(); s = c.fig(W/2, 900-(1-T.ease(T.LT/0.3))*900, 520, "drop" if T.LT < .5 else "self", "wow" if T.LT < .5 else "smile", "modern")
    c.marker(s["head"][0]+20, s["head"][1]-110, 46)
    if T.LT > .6: L(c, "YOU", 160, 1400, 120)
    return c
def bakery(k=0, loaves=0):
    c = roomset(); c.rect(1240, 130, 1660, 430, (60, 60, 96) if k == 2 else SK["dawn"][1], INK, 9); c.rect(1220, 430, 1680, 452, WOOD, INK, 5)
    if k == 2:
        for i in range(8): x = 1260+(i*83) % 380; y = 150+(i*57) % 260; c.ell(x, y, x+7, y+7, PAPER, None)
    c.oven(430, 900, 1.25, T.TT+.1); c.rect(1100, 720, 1700, 750, WOOD, INK, 6, 4); c.line([(1140, 750), (1140, 900)], 14, WOOD); c.line([(1660, 750), (1660, 900)], 14, WOOD)
    for i in range(loaves): c.rloaf(1180+i*120, 690, .9)
    s = sidp(c, 900, 940, 340, "hold", "det" if k != 1 else "smile", flip=True); hx, hy = s["hand"]; c.line([(hx+60, hy+20), (hx-260, hy-10)], 10, WOOD); c.ell(hx-330, hy-34, hx-240, hy+14, WOOD, INK, 5)
    if k == 1: L(c, "AGE 19. BAKERY HAND, POMPEII.", 90, 1180, 60)
    return c
def qbake(shown, done=0): return Q(bakery(0), shown, done)
def hiddenq(k, done=3):
    c = C(); c.questlog(ROWS, 4, done, None, x=545, y=200)
    if k: c.marker(470, 800, 36)
    return c

# ================= the morning =================
def dawn(k):
    c = town("dawn"); hud(c, "FIRST LIGHT")
    if k == 1:
        c.calpage(560, 440, 1.0, "AUGUST", "24?"); c.calpage(1360, 440, 1.0, "OCTOBER", "24?"); c.rect(860, 370, 1060, 510, PAPER, INK, 6, 16); c.text(960, 436, "OR", 110, RED); L(c, "SCHOLARS STILL ARGUE", 130, 1100, 72, bg=MARI)
    if k == 2:
        c.rect(0, 900, W, H, SEA, None); c.line([(0, 900), (W, 900)], 6, INK, False)
        for i in range(8): x = (i*263+T.TT*30) % W; c.line([(x, 960+(i % 3)*40), (x+60, 960+(i % 3)*40)], 5, WHITE, False)
        c.galley(lerp(-300, 760, T.ease(T.LP)), 1030, 460, bob=T.TT*2); L(c, "A PORT TOWN", 150, 1100, 90)
    if k == 3: L(c, "10,000 TO 15,000 PEOPLE", 150, 1100, 80, bg=MARI); folk(c, [300, 520, 760, 1000, 1240, 1480, 1700], 990, 240, ("smile", "n", "joy", "bored"), ("walk", "stand", "wave", "stand"))
    return c
def trade(k):
    c = C((204, 226, 232)); c.poly([(1180, 0), (1500, 0), (1560, 260), (1700, 520), (1760, 760), (1640, 800), (1500, 560), (1380, 380), (1240, 260)], SAND, INK, 7)
    c.poly([(0, 420), (260, 380), (420, 520), (360, 860), (0, 900)], SAND, INK, 7); c.poly([(360, 0), (980, 0), (900, 160), (620, 260), (420, 200)], SAND, INK, 7)
    c.ell(1596, 566, 1636, 606, RED, INK, 6); L(c, "POMPEII", 520, 1700, 60); c.text(190, 640, "SPAIN", 80); c.text(680, 110, "GAUL", 80)
    for i in range(3): c.amphora(1300+i*90, 960, .8)
    if k >= 1:
        q = app("tr1", 1.1, .1); x, y = lerp(1560, 440, q), lerp(640, 680, q)-110*math.sin(q*math.pi); arrow(c, 1540, 660, lerp(1540, 470, q), lerp(660, 690, q), TEAL, 12, 34); c.amphora(x, y, .7); L(c, "WINE JARS", 820, 960, 66)
    if k >= 2:
        q = app("tr2", 1.1, .1); arrow(c, 1540, 540, lerp(1540, 800, q), lerp(540, 230, q), RED, 12, 34); c.amphora(lerp(1540, 800, q), lerp(540, 230, q)-80*math.sin(q*math.pi), .7, (150, 110, 90)); L(c, "FISH SAUCE", 330, 1240, 66, bg=MARI)
    c.text(960, 1030, "SKETCH MAP, NOT TO SCALE", 40, (110, 120, 124)); return c
def breadline(k=0):
    c = town("dawn"); hud(c, "BEFORE SUNRISE")
    for i, x in enumerate((760, 960, 1150, 1340, 1530)):
        xx = lerp(x+700, x, app(("bl", i), .7, i*.15)); f = c.person(xx, 980+(i % 2)*30, 270, "stand" if i % 2 else "point", ("bored", "n", "smile", "bored", "n")[i], COATS[i], flip=True)
    c.bubble(1150, 470, "BREAD?", 80, (-120, 80)); sidp(c, 520, 985, 300, "hold", "worry"); c.rloaf(640, 870, .9)
    return c
def bakecount(k):
    c = C(); n = int(35*app("bc", 1.3, .1)+.5)
    for i in range(n): c.rloaf(260+(i % 7)*150, 330+(i//7)*118, .82)
    c.text(1560, 430, str(n), 300, RED); c.text(1560, 640, "BAKERIES", 90); c.text(1560, 730, "(ABOUT)", 54, (120, 110, 98))
    if k: c.mill(1560, 1040, .7); L(c, "MANY GRIND THEIR OWN FLOUR", 990, 760, 66, bg=MARI)
    return c
def millscene(k):
    c = roomset(hz=760); a = T.TT*1.6; front = math.sin(a) > 0; dx = 560*math.cos(a); mx = 1180
    if k >= 2: c.oven(250, 860, .8, T.TT+.1)
    if not front: c.donkey(mx+dx, 880, 1.15, flip=True, step=T.TT*9)
    c.mill(mx, 980, 1.9)
    if front: c.donkey(mx+dx, 1050, 1.5, flip=False, step=T.TT*9)
    if k == 0: L(c, "THE MILL: A BLOCK OF LAVA ROCK", 110, size=68)
    if k == 1: L(c, "THE ENGINE: ONE DONKEY", 110, size=72, bg=MARI)
    if k >= 2: L(c, "WORST JOB IN POMPEII", 110, 1180, 70)
    if k == 3: s = sidp(c, 560, 1000, 340, "carry", "strain"); c.rect(s["hand0"][0]-80, s["hand0"][1]-70, s["hand"][0]+80, s["hand"][1]-10, (226, 206, 170), INK, 6, 8); L(c, "SECOND WORST", 250, 560, 70, bg=MARI)
    return c
def loaves(k):
    if k == 0:
        c = bakery(0, 0); n = int(5*app("lv", 1.0, .15)+.5)
        for i in range(n): c.rloaf(1180+i*120, 690, .9)
        hud(c, "SUNRISE"); return c
    c = C((236, 214, 182)); c.rloaf(760, 540, 6.2); q = app("stamp", .25, .5); z = 2-q
    if T.LT > .5 or q >= 1: c.rect(1080-190*z, 400-80*z, 1080+190*z, 400+80*z, (190, 130, 70), INK, 7*z, 10); c.text(1080, 396, "BAKER'S MARK", 54*z, (110, 66, 34))
    L(c, "STAMPED WITH THE BAKERY'S MARK", 990, size=66, bg=MARI); return c
def street(k):
    c = town("day"); hud(c, "MORNING")
    pts = [(x, 960+16*math.sin(x*.02+T.TT*4)) for x in range(-40, W+80, 60)]; c.line(pts, 56, (120, 100, 70), False); c.line(pts, 40, (156, 132, 90), False)
    for i in range(6): x = (i*340+T.TT*120) % (W+100)-50; c.ell(x, 950, x+26, 966, (120, 100, 70), None)
    if k <= 1:
        s = sidp(c, 560, 900, 330, "chin", "pain" if k else "worry")
        if k: L(c, "THE STREET IS DISGUSTING", 150, 1180, 70, bg=MARI)
        for i in range(3): x = 760+i*90; c.line([(x, 720-20*math.sin(T.TT*3+i)), (x+20, 660), (x-6, 600+20*math.sin(T.TT*3+i))], 8, (140, 150, 90), False)
    if k == 2:
        f = c.person(520, 800, 250, "pour", "bored", "rose"); hx, hy = f["hand"]; q = (T.TT*.9) % 1
        for i in range(7): t = min(1, q*1.6+i*.06); c.ell(hx+40+t*300-14, hy+20+t*t*150-14, hx+40+t*300+14, hy+20+t*t*150+14, (156, 132, 90), INK, 3)
        L(c, "NO DRAIN. OUT THE FRONT DOOR.", 150, 1180, 66)
    return c
def stonesc(k):
    if k == 2:
        c = C(PAVE2); c.rect(0, 0, W, 250, (214, 208, 200), INK, 6); c.rect(0, 830, W, H, (214, 208, 200), INK, 6); c.text(240, 120, "SIDEWALK", 60, (120, 114, 110)); c.text(240, 950, "SIDEWALK", 60, (120, 114, 110))
        for y in (340, 540, 740): c.rect(860, y-70, 1060, y+70, (226, 220, 212), INK, 7, 30)
        x = lerp(-300, 1500, T.ease(T.LP*.95))
        for y in (440, 640): c.line([(0, y), (x, y)], 10, (120, 114, 110), False)
        c.rect(x-200, 400, x+40, 680, WOOD, INK, 7, 8)
        for y in (440, 640): c.rect(x-150, y-22, x-30, y+22, (90, 70, 54), INK, 5, 6)
        c.line([(x+40, 540), (x+200, 540)], 10, (90, 70, 54)); L(c, "WHEELS FIT THE GAPS", 955, 1150, 62, bg=MARI); c.text(1560, 120, "SEEN FROM ABOVE", 50, (120, 114, 110)); return c
    c = town("day"); hud(c, "MORNING"); xs = [760, 960, 1160]
    c.rect(0, 900, W, H, (140, 126, 100), None); c.line([(0, 900), (W, 900)], 5, INK, False)
    for i in range(8): x = (i*260+T.TT*90) % (W+100)-50; c.line([(x, 960+(i % 3)*36), (x+60, 960+(i % 3)*36)], 6, (176, 160, 120), False)
    for x in xs: c.rect(x-96, 838, x+96, 940, (226, 220, 212), INK, 8, 30)
    q = T.ease(T.GP) if k <= 1 else 1; s = q*4; i = min(3, int(s)); fr = s-i; P = [520]+xs+[1400]
    x = P[i]+(P[min(4, i+1)]-P[i])*fr; y = 850-abs(math.sin(fr*math.pi))*90 if q < 1 else 850
    sidp(c, x, y if 0 < i+fr < 3.999 or q < 1 else 850, 300, "run" if 0 < fr < 1 and q < 1 else "stand", "det" if q < 1 else "smile")
    if k == 0: L(c, "STEPPING STONES", 150, 1180, 84)
    if k == 1: L(c, "DRY FEET", 150, 1180, 96, bg=MARI)
    if k == 3: L(c, "CROSSWALK. AGE: 2,000 YEARS.", 150, 1150, 68, bg=MARI)
    return c
def wallset():
    c = C(RWALL); c.rect(0, 700, W, 880, TERRA, None); c.line([(0, 700), (W, 700)], 5, INK, False); c.rect(0, 880, W, H, PAVE2, None); c.line([(0, 880), (W, 880)], 6, INK, False); return c
def wall(k):
    c = wallset()
    if k <= 1:
        for i in range(9):
            x = 140+(i % 3)*600; y = 150+(i//3)*170; pts = [(x+j*38, y+18*math.sin(j*1.9+i)) for j in range(11)]; c.line(pts, 9, RED if i % 2 == 0 else (120, 60, 50))
        sidp(c, 1560, 1010, 330, "chin", "n", flip=True)
        if k: L(c, "A LOT OF IT: ELECTION ADS", 990, 760, 70, bg=MARI)
        hud(c, "MID-MORNING"); return c
    if k == 2: c.text(960, 300, "ALL THE WORSHIPPERS OF ISIS", 110, RED); c.text(960, 470, "CALL FOR HELVIUS SABINUS", 110, RED); sidp(c, 1560, 1010, 300, "point", "smile", flip=True)
    if k in (3, 4):
        c.text(960, 300, "ALL THE DEADBEATS", 130, RED); c.text(960, 470, "ASK FOR VATIA", 130, RED)
        if k == 4: f = c.person(520, 1010, 330, "shrug", "angry", "teal"); L(c, "VATIA (PROBABLY DID NOT PAY FOR THIS)", 990, 1250, 54, bg=MARI)
    if k >= 5:
        t = "I ADMIRE YOU, WALL, FOR NOT HAVING COLLAPSED\nAT HAVING TO CARRY THE TEDIOUS SCRIBBLINGS\nOF SO MANY WRITERS"; n = len(t) if k == 6 else int(len(t)*min(1, app("gr", 2.2, .1))+.5)
        c.text(960, 380, t[:n] if n else " ", 72, (90, 70, 60))
        if k == 6: sidp(c, 1560, 1010, 300, "shrug", "smile", flip=True); L(c, "SCRATCHED ON A WALL IN POMPEII", 990, 700, 58)
    return c
def flat(k):
    c = roomset((224, 206, 190)); c.rect(1340, 160, 1640, 400, SK["noon"][1], INK, 9); c.rect(1320, 400, 1660, 422, WOOD, INK, 5)
    c.rect(200, 720, 760, 756, WOOD, INK, 6, 4); c.rect(214, 668, 746, 724, (232, 220, 206), INK, 6, 12); c.line([(230, 756), (230, 900)], 12, WOOD); c.line([(730, 756), (730, 900)], 12, WOOD)
    sidp(c, 1080, 950, 330, "shrug", "worry" if k else "n")
    if k == 0: L(c, "NO KITCHEN", 150, size=100)
    if k == 1: c.rect(1380, 800, 1560, 900, (90, 84, 80), INK, 6, 8); c.fire(1470, 800, 1.3); L(c, "OR A FIRE HAZARD", 150, size=90, bg=MARI)
    hud(c, "MIDDAY"); return c
def bars(k=0):
    c = C(); n = int(158*app("bars", 1.6, .1)+.5)
    for i in range(n):
        x = 150+(i % 20)*56; y = 380+(i//20)*74; c.rect(x, y, x+40, y+34, OCHRE, INK, 4, 4); c.ell(x+10, y-8, x+30, y+6, (150, 96, 70), INK, 3)
    c.text(1560, 520, str(n), 300, RED); c.text(1560, 730, "SNACK BARS", 86); return c
def snack(k):
    c = C((232, 214, 190)); c.rect(0, 0, W, 240, TERRA, None); c.line([(0, 240), (W, 240)], 5, INK, False); c.rect(0, 860, W, H, PAVE2, None); c.line([(0, 860), (W, 860)], 6, INK, False)
    for i in range(4): c.amphora(1340+i*120, 600, 1.0)
    c.rect(1280, 600, 1800, 620, WOOD, INK, 5)
    f = c.person(1180, 850, 330, "pour" if k < 2 else "wave", "smile", "green", flip=True); c.barcounter(620, 900, 760, 230)
    for i in range(3): r = 16+8*math.sin(T.TT*4+i); c.da.ellipse([(800+i*240-r)*S, (560-i*10-r-(T.TT*40 % 60))*S, (800+i*240+r)*S, (560-i*10+r-(T.TT*40 % 60))*S], fill=(255, 255, 255, 150))
    s = sidp(c, 330, 950, 340, "hold", "smile" if k < 2 else "joy")
    if k < 2: c.coin(s["hand"][0]+40, s["hand"][1]-10, 26, "")
    else: c.rect(s["hand"][0]+10, s["hand"][1]-50, s["hand"][0]+90, s["hand"][1]+10, (196, 132, 96), INK, 5, 14)
    if k == 0: L(c, "A STONE COUNTER, JARS SUNK IN THE TOP", 130, size=60)
    if k == 1: L(c, "FOOD AND WINE, TO GO, FOR A FEW COINS", 130, size=60, bg=MARI)
    if k == 2: L(c, "FAST FOOD, AD 79", 130, size=96, bg=MARI)
    hud(c, "MIDDAY") if k == 0 else None; return c
def amph(k):
    c = C(SK["noon"][1]); c.rect(0, 760, W, H, SAND, None); c.arena(960, 560, 1500, 640)
    if k == 1: L(c, "20,000 SEATS", 130, size=110, bg=MARI)
    if k == 2:
        c.rect(0, 0, W, H, PAPER, None); c.line([(240, 860), (1680, 860)], 7); q = app("ab", .9, .15)
        c.rect(420, 860-500*q, 760, 860, TERRA, INK, 7, 6); c.text(590, 930, "SEATS", 64); c.text(590, 860-500*q-56, "20,000", 84)
        c.rect(1120, 860-250, 1460, 860, GREY, INK, 7, 6); c.rect(1120, 860-375, 1460, 860-250, (226, 218, 206), INK, 7, 6); c.text(1290, 930, "PEOPLE IN TOWN", 64); c.text(1290, 860-375-56, "10,000 TO 15,000", 76)
    return c
def brawl(k):
    if k <= 1:
        c = C((214, 204, 190))
        for r in range(4): c.line([(0, 250+r*150), (W, 250+r*150)], 6, (150, 140, 128), False)
        folk(c, [200, 420, 640], 860, 270, ("angry", "strain", "angry"), ("up", "point", "cheer"), flip=False); folk(c, [1280, 1500, 1720], 860, 270, ("angry", "det", "strain"), ("up", "point", "cheer"), flip=True)
        bl = [(960+150*math.cos(i*1.3+T.TT*5)*(.6+.3*math.sin(i+T.TT*7)), 760+110*math.sin(i*1.7+T.TT*4), 90+16*math.sin(i*2+T.TT*9)) for i in range(7)]; c.puff(bl, (226, 214, 196))
        for i in range(5): a = i*72+T.TT*200; c.text(960+230*math.cos(math.radians(a)), 760+170*math.sin(math.radians(a)), "!", 110, RED)
        L(c, "AD 59: A BLOODY BRAWL IN THE STANDS" if k == 0 else "POMPEII VS THE NEXT TOWN OVER", 120, size=64, bg=MARI if k else PAPER); return c
    c = C(SK["noon"][1]); c.rect(0, 760, W, H, SAND, None); c.arena(960, 520, 1300, 560); q = app("ban", .3, .3)
    c.rect(960-420*q, 480-110*q, 960+420*q, 480+110*q, PAPER, RED, 14, 12)
    if q > .9: c.text(960, 440, "CLOSED", 130, RED); c.text(960, 540, "BY ROME, FOR TEN YEARS", 56)
    if k == 3: sidp(c, 380, 1010, 320, "shrug", "bored"); L(c, "A STADIUM BAN", 960, 1240, 96, bg=MARI)
    return c
def quake(k):
    if k == 0:
        c = town("day", shake=1.0); hud(c, "MIDDAY"); sidp(c, 700+8*math.sin(T.TT*40), 990, 320, "shrug", "wow"); L(c, "THE GROUND SHAKES HERE. A LOT.", 150, 1180, 64); return c
    if k in (1, 2):
        c = town("day"); c.rect(0, 0, W, H, None, None); x, base, w, h = 995, 790, 350, 340
        c.line([(x+60, base-h+20), (x+110, base-h*.6), (x+80, base-h*.4), (x+140, base-20)], 9, INK); c.line([(x+250, base-h+40), (x+220, base-h*.5), (x+270, base-h*.3)], 8, INK)
        if k == 2:
            for xx in (x-30, x+w+30): c.line([(xx, base), (xx, base-h-60)], 10, WOOD)
            for j in range(3): c.line([(x-30, base-80-j*110), (x+w+30, base-80-j*110)], 8, WOOD)
            L(c, "SOME OF IT STILL ISN'T FIXED", 990, size=70, bg=MARI)
        L(c, "AD 62: A BAD EARTHQUAKE", 150, 1150, 72); return c
    c = C()
    for i in range(4):
        x = 330+i*420; q = app(("day", i), .3, i*.3)
        if q > 0:
            c.rect(x-150, 300, x+150, 640, WHITE, INK, 7, 14); c.text(x, 360, "DAY "+str(i+1), 60); pts = [(x-120+j*12, 500+(26+i*8)*math.sin(j*1.7+T.TT*10)*math.exp(-abs(j-10)/5)) for j in range(21)]; c.line(pts, 7, RED)
    if k == 3: L(c, "FOUR DAYS OF SMALL TREMORS", 800, size=76)
    if k == 4: folk(c, [520, 960, 1400], 1040, 230, ("bored", "n", "smile"), ("shrug", "shrug", "shrug")); L(c, "NORMAL HERE", 150, size=96, bg=MARI)
    return c
def mountain(k, done=0):
    c = C(SAND); sky(c, 700, "noon"); c.vesuvius(960, 760, 1700, 600); c.rect(0, 760, W, H, (150, 186, 120), None); c.line([(0, 760), (W, 760)], 6, INK, False)
    c.rhouse(240, 940, 260, 200, RWALL, TERRA, upper=False); c.rhouse(1460, 960, 230, 180, OCHRE, TERRA, upper=False)
    for i in range(14): x = 560+(i % 7)*120; y = 860+(i//7)*90; c.line([(x, y), (x, y-60)], 6, (120, 90, 60)); c.ell(x-22, y-84, x+22, y-44, (104, 150, 90), INK, 4)
    if k == 0: L(c, "JUST A MOUNTAIN", 130, size=96)
    if k == 1: L(c, "FARMS. GOOD SOIL.", 130, size=90, bg=MARI)
    if k == 2: c.text(900, 330, "?", 240*(.8+.2*app("qm", .3)), PAPER); L(c, "NOBODY HERE KNOWS WHAT IT IS", 130, size=72, bg=MARI)
    if done: Q(c, 4, done)
    hud(c, "LATE MORNING") if not done else None; return c

# ================= the afternoon =================
def erupt(k):
    g = T.ease(T.GP*1.05) if k <= 1 else 1; c = town("noon" if g < .5 else "day", peak=g < .08, plume=(520, 760, ASHC, max(.03, g)), shake=1.0 if g < .5 else 0)
    hud(c, "ABOUT 1 PM")
    if k == 1: L(c, "ASH AND ROCK, STRAIGHT UP", 150, 760, 70, bg=MARI); folk(c, [300, 520, 760], 1000, 250, ("wow", "wow", "worry"), ("stand", "point", "shrug"))
    return c
def baymap(c=None, dots=("POMPEII",), cloud=0.0, labels=True):
    c = c or C(SEA); P = {"CUMAE": (300, 250), "MISENUM": (370, 470), "PUTEOLI": (560, 300), "NAPLES": (830, 270), "HERCULANEUM": (1010, 410), "POMPEII": (1290, 560), "STABIAE": (1240, 720)}
    c.rect(0, 0, W, H, SEA, None); c.poly([(0, 0), (W, 0), (W, H), (760, H), (640, 960), (900, 900), (1160, 800), (1200, 700), (1180, 600), (1040, 440), (900, 330), (700, 330), (540, 350), (430, 400), (400, 500), (330, 480), (300, 330), (200, 150), (0, 120)], SAND, INK, 7)
    c.vesuvius(1170, 400, 330, 170, VINE if cloud <= 0 else (132, 124, 118), False, cloud <= 0)
    for i in range(10): x = (i*211) % 700+60; y = 520+(i*137) % 480; c.line([(x, y), (x+50, y)], 5, WHITE, False)
    for n in dots:
        x, y = P[n]; q = app(("dot", n), .25); c.ell(x-18*q, y-18*q, x+18*q, y+18*q, RED, INK, 6)
        if labels: c.text(x+(30 if n not in ("MISENUM", "CUMAE") else 0), y+(4 if n not in ("MISENUM", "CUMAE") else 52), n, 46, INK, "lm" if n not in ("MISENUM", "CUMAE") else "mm")
    c.text(300, 1030, "SKETCH MAP, NOT TO SCALE", 40, (60, 100, 124)); return c, P
def pliny(k):
    if k == 0:
        c, P = baymap(dots=("POMPEII", "MISENUM"), cloud=1); c.plume(1160, 290, 230, 300, T.TT, ASHC, 1.0); a, b = P["MISENUM"], (1130, 200); q = app("look", .9, .2)
        for i in range(int(12*q)): t0 = i/12; c.line([(lerp(a[0], b[0], t0), lerp(a[1], b[1], t0)), (lerp(a[0], b[0], t0+.04), lerp(a[1], b[1], t0+.04))], 8, RED, False)
        L(c, "ACROSS THE BAY", 880, 420, 70); return c
    c = roomset((226, 214, 196)); c.rect(1100, 150, 1700, 520, SK["ash"][1], INK, 9); c.plume(1400, 520, 300, 420, T.TT, ASHC, 1.0); c.rect(1080, 520, 1720, 544, WOOD, INK, 5); c.rect(1080, 130, 1100, 540, (226, 214, 196), None); c.rect(1700, 130, 1740, 540, (226, 214, 196), None)
    c.rect(520, 700, 1000, 730, WOOD, INK, 6, 4); c.line([(560, 730), (560, 900)], 14, WOOD); c.line([(960, 730), (960, 900)], 14, WOOD); c.rect(700, 660, 900, 700, (226, 200, 150), INK, 5, 4)
    f = c.person(620, 940, 340, "write", "det", "teal"); L(c, "PLINY THE YOUNGER" if k == 1 else "HIS LETTERS: OUR EYEWITNESS", 990, 760, 70, bg=MARI if k == 2 else PAPER); return c
def pine(k):
    c = C(); c.line([(240, 900), (1680, 900)], 7); c.rect(520, 520, 560, 900, (120, 90, 60), INK, 6); c.puff([(540+dx, 470+abs(dx)*.12, 86-abs(dx)*.1) for dx in range(-260, 261, 65)], (104, 150, 90)); c.text(540, 970, "AN UMBRELLA PINE", 60)
    if k >= 1: c.plume(1340, 900, 420, 620, T.TT, ASHC, app("pg", 1.0, .1)); c.text(1340, 970, "THE CLOUD", 60); L(c, "\"MORE LIKE AN UMBRELLA PINE THAN ANY OTHER TREE\"", 130, size=56, bg=MARI)
    return c
def height(k=0):
    c = C(SK["day"][1]); c.rect(0, 960, W, H, VINE, None); c.line([(0, 960), (W, 960)], 6, INK, False); c.vesuvius(760, 960, 300, 60, (132, 124, 118), False, False); q = app("hg", 1.4, .1)
    c.plume(760, 910, 760, 700, T.TT, ASHC, max(.05, q)); c.line([(1500, 960), (1500, 150)], 8)
    for i, km in enumerate((10, 20, 30)):
        y = 960-270*(i+1)
        if q*30 >= km-2: c.line([(1470, y), (1530, y)], 8); c.text(1560, y-4, str(km)+" KM", 70, INK, "lm")
    L(c, "UP TO 30 KM HIGH (MODERN ESTIMATES)", 1030, 620, 54, bg=MARI); return c
def rate(k=0):
    c = C(DARK); v = int(1500000*max(0.0, T.LT if T.LT < 8 else 1)); c.text(960, 380, format(v, ","), 230, MARI); c.text(960, 590, "TONS OF ROCK", 100, PAPER)
    c.stones(40, T.TT, 1080, 1.4); L(c, "1.5 MILLION TONS A SECOND (ONE ESTIMATE)", 900, size=58, bg=MARI); return c
def wind(k=0):
    c, P = baymap(dots=("POMPEII",), cloud=1); q = T.ease(T.LP*1.1); x0, y0 = 1160, 300; x1, y1 = 1460, 760
    bl = [(lerp(x0, x1, t0*q)+60*math.sin(i*2.1), lerp(y0, y1, t0*q)+40*math.cos(i*1.7), 70+50*t0*q+10*math.sin(T.TT*3+i)) for i, t0 in enumerate([j/9 for j in range(10)])]; c.puff(bl, ASHC)
    for j in range(3): arrow(c, 760+j*40, 150+j*110, 760+j*40+150, 150+j*110+130, PAPER, 12, 34)
    c.text(700, 120, "WIND", 80, PAPER); x, y = P["POMPEII"]; c.ell(x-18, y-18, x+18, y+18, RED, INK, 6); L(c, "STRAIGHT OVER YOU", 950, 1250, 80, bg=MARI); return c
def dark(k, done=0):
    q = T.ease(T.LP*1.3) if k == 0 else 1; c = town("day" if q < .5 else "ash", peak=False, green=q < .5, plume=(520, 900, (120, 114, 110), 1.0), layer=0 if k < 2 else 26)
    sidp(c, 620, 990, 320, "stand" if k == 0 else "up", "wow" if k < 2 else "worry"); folk(c, [1150, 1400, 1650], 1000, 250, ("wow", "worry", "wow"), ("point", "shrug", "stand"), flip=True)
    dim(c, 150*q)
    if k >= 1: c.stones(46, T.TT, 1080, 1.3)
    hud(c, "EARLY AFTERNOON", True)
    if k == 0: L(c, "THE SUN GOES OUT", 150, 1180, 84)
    if k == 1: L(c, "THEN IT RAINS STONES", 150, 1180, 80, bg=MARI)
    if done: Q(c, 4, done)
    return c
def pumice(k):
    c = C(DARK); c.rect(0, 880, W, H, (70, 66, 72), None)
    if k == 0:
        bx, by = 1100, 500; c.puff([(bx+dx, by+dy, r) for dx, dy, r in ((-150, 20, 150), (0, -40, 190), (160, 30, 150), (10, 90, 160))], PUM)
        for i in range(12): x = bx-220+(i*97) % 440; y = by-150+(i*61) % 300; r = 14+(i*7) % 16; c.ell(x-r, y-r, x+r, y+r, (150, 146, 140), None)
        sidp(c, 420, 1000, 330, "point", "wow"); L(c, "PUMICE: LIGHT ROCK, FULL OF HOLES", 130, size=64); return c
    layer = 0 if k == 1 else 150*app("pile", 1.2, .1); c.stones(50, T.TT, 900-layer, 1.5)
    if layer: c.poly([(0, 900-layer)]+[(x, 900-layer+12*math.sin(x*.012)) for x in range(0, W+1, 120)]+[(W, H), (0, H)], PUM, INK, 5)
    s = sidp(c, 960, 900-layer*.5, 380, "up", "pain" if int(T.TT*3) % 2 else "worry")
    if k == 1: L(c, "IT MOSTLY DOESN'T KILL YOU", 130, size=72)
    if k == 2: L(c, "IT PILES UP", 130, size=110, bg=MARI)
    return c
def noplan(k):
    c = town("ash", peak=False, green=False, plume=(520, 900, (120, 114, 110), 1.0), layer=30); fs = folk(c, [330, 620, 910, 1200, 1490], 1000, 270, ("wow", "worry", "sad", "wow", "worry"), ("shrug", "chin", "shrug", "point", "shrug")); dim(c, 150); c.stones(40, T.TT, 1080, 1.3)
    for i, f in enumerate(fs):
        q = app(("np", i), .25, i*.18)
        if q > 0: c.bubble(f["head"][0]+40, f["head"][1]-130, "?", 90*q+2, (-30, 30))
    hud(c, "AFTERNOON", True)
    if k: L(c, "NOBODY KNEW THIS COULD HAPPEN", 1010, size=66, bg=MARI)
    return c
def choice(k):
    c = C(DARK); c.stones(30, T.TT, 1080, 1.2)
    def panel(x, on=True): c.rect(x, 230, x+800, 880, (58, 54, 64) if on else (44, 42, 50), PAPER, 7, 18)
    panel(120); c.rhouse(300, 800, 440, 400, RWALL, TERRA, upper=False); c.rect(480, 470, 600, 580, MARI, INK, 6); c.fig(540, 610, 110, "stand", "worry", "modern"); c.rect(470, 580, 610, 600, WOOD, INK, 4)
    c.text(520, 950, "A: STAY INDOORS", 76, PAPER)
    if k >= 2:
        panel(1000); f = sidp(c, 1400, 830, 330, "walk" if step() else "stand", "worry", pil=True); c.stones(14, T.TT, 800, 1.3, x0=1040, x1=1760, seed=3); c.text(1400, 950, "B: WALK OUT", 76, PAPER)
    if k == 0: L(c, "TWO OPTIONS", 120, size=96)
    if k == 1: L(c, "WAIT FOR IT TO STOP", 120, 520, 66)
    if k == 2: L(c, "IN THE DARK, STONES ON YOUR HEAD", 120, 1380, 52)
    if k == 3: c.rect(112, 222, 928, 888, None, MARI, 14, 22); L(c, "FEELS LIKE THE SMART CHOICE", 120, 520, 60, bg=MARI)
    if k == 4: c.redx(520, 540, 230, 40); L(c, "FOR THEM, THE SHELTER WAS THE TRAP", 120, size=66, bg=MARI)
    return c
def pillows(k):
    c = C(SK["ash"][1]); sky(c, 760, "ash"); c.rect(0, 760, W, H, (120, 110, 104), None); c.line([(0, 760), (W, 760)], 6, INK, False)
    fs = folk(c, [360, 660, 960, 1260, 1560], 990, 300, ("worry", "det", "worry", "strain", "det"), ("up", "stand", "up", "stand", "up"), pil=True); dim(c, 90); c.stones(40, T.TT, 1080, 1.3)
    if k == 0: L(c, "DOWN THE COAST: PILLOWS ON THEIR HEADS", 120, size=60)
    if k == 1: L(c, "TIED ON WITH STRIPS OF CLOTH", 120, size=68)
    if k == 2: L(c, "NOT A JOKE. PLINY WROTE IT DOWN.", 120, size=68, bg=MARI)
    return c
def fleet(k):
    c = C(SEA); sky(c, 560, "dusk" if k < 3 else "ash"); c.plume(1700, 560, 380, 900, T.TT, (96, 90, 92), 1.0); c.rect(0, 560, W, H, (70, 110, 140) if k < 3 else (52, 80, 104), None); c.line([(0, 560), (W, 560)], 6, INK, False)
    for i in range(12): x = (i*263+T.TT*30) % W; y = 620+(i*97) % 420; c.line([(x, y), (x+60, y)], 5, (150, 190, 210), False)
    adv = T.GP*260 if k <= 2 else 260
    for i, (x, y, w) in enumerate(((250, 900, 620), (900, 760, 420), (1300, 680, 300))): c.galley(x+adv*(1-.2*i), y, w, bob=T.TT*2+i)
    if k >= 2:
        f = c.person(330+adv, 838, 240, "point" if k >= 4 else "stand", "det", "red");
        if k == 2: L(c, "PLINY THE ELDER, FLEET COMMANDER", 990, size=60, bg=MARI)
    if k >= 3: c.stones(44, T.TT, 1080, 1.3); dim(c, 60)
    if k == 0: L(c, "THE ROMAN FLEET PUTS TO SEA", 120, 760, 66)
    if k == 1: L(c, "TO RESCUE PEOPLE FROM THE SHORE", 120, 760, 60)
    if k == 3: L(c, "ASH ON THE DECKS: HOTTER, THICKER", 120, 760, 60)
    if k == 5: c.bubble(900, 470, "FORTUNE FAVOURS THE BRAVE.", 64, (-330, 130))
    return c
def beach(k):
    if k == 0:
        c, P = baymap(dots=("MISENUM", "POMPEII", "STABIAE"), cloud=1); a, b = P["MISENUM"], P["STABIAE"]; q = app("sail", 1.2, .1); pts = [(lerp(a[0], b[0], t0), lerp(a[1], b[1], t0)+90*math.sin(t0*math.pi)) for t0 in [j/20*q for j in range(21)]]
        c.line(pts, 9, PAPER, False); x, y = pts[-1]; c.poly([(x-26, y-14), (x+30, y), (x-26, y+14)], WOOD, INK, 4); return c
    c = C(SK["ash"][1]); sky(c, 620, "glow"); c.rect(0, 620, W, 760, (52, 80, 104), None); c.rect(0, 740, W, H, (150, 140, 124), None); c.line([(0, 740), (W, 740)], 6, INK, False); c.galley(1400, 760, 520, bob=0)
    dim(c, 80); c.stones(30, T.TT, 1080, 1.2)
    L(c, "STABIAE. HE DIES ON THIS BEACH THE NEXT MORNING.", 130, size=54, bg=MARI); return c
def night(k):
    g = T.GP; c = town("ash", peak=False, green=False, plume=(520, 900, (110, 100, 100), 1.0), layer=40+150*g); dim(c, 170); c.stones(60, T.TT, 1080, 1.4)
    hrs = ["3 PM", "5 PM", "7 PM", "9 PM", "11 PM", "1 AM"]; hud(c, hrs[min(5, int(g*6))], True)
    if k: L(c, "HOUR AFTER HOUR", 1000, size=84, bg=MARI)
    return c
def depth(k):
    c = C((58, 54, 64)); q = app("dp", 1.6, .1) if k == 0 else 1; top = 880-560*q*.93
    c.rhouse(360, 880, 560, 620, RWALL, TERRA); c.poly([(0, top)]+[(x, top+14*math.sin(x*.011)) for x in range(0, W+1, 120)]+[(W, H), (0, H)], PUM, INK, 6)
    c.line([(1240, 880), (1240, 280)], 8, PAPER)
    for m in range(4): y = 880-m*200; c.line([(1210, y), (1270, y)], 8, PAPER); c.text(1300, y-4, str(m)+" M", 60, PAPER, "lm")
    c.fig(1560, 880, 272, "stand", "worry", "modern"); c.text(1560, 950, "YOU", 56, INK)
    c.text(700, 170, "HOURS: "+str(int(18*q)), 90, PAPER)
    if k: L(c, "NEARLY 3 METRES OF PUMICE", 1000, 620, 66, bg=MARI)
    return c
def roof(k):
    c = C((58, 54, 64)); c.rect(0, 880, W, H, PUM, None); c.line([(0, 880), (W, 880)], 6, INK, False); x, w, h = 520, 880, 440; q = app("fall", .6, .5) if k == 1 else 0
    c.rect(x, 880-h, x+w, 880, RWALL, INK, 7); c.rect(x+3, 880-h*.34, x+w-3, 877, TERRA, None); c.rect(x+w*.42, 880-h*.5, x+w*.58, 880, (92, 66, 46), INK, 5)
    sag = 30+170*q; pts = [(x-20, 880-h), (x+w*.5, 880-h+sag), (x+w+20, 880-h)]; c.line(pts, 26, INK, False); c.line(pts, 16, TILE, False)
    c.poly([(x-10, 880-h-10), (x+w*.25, 880-h-150+sag*.5), (x+w*.5, 880-h-120+sag), (x+w*.75, 880-h-150+sag*.5), (x+w+10, 880-h-10), (x+w*.5, 880-h+sag-12)], PUM, INK, 6)
    c.stones(40, T.TT, 300, 1.4)
    if q > .5:
        for i in range(8): a = i*45; c.line([(x+w*.5+120*math.cos(math.radians(a)), 700+90*math.sin(math.radians(a))), (x+w*.5+190*math.cos(math.radians(a)), 700+140*math.sin(math.radians(a)))], 10, RED)
    L(c, "NOW PUT THAT ON A ROOF" if k == 0 else "ROOFS START TO GIVE WAY", 110, size=76, bg=MARI if k else PAPER); return c
def third(k):
    c = C(); c.text(960, 170, "OF THE BODIES FOUND IN POMPEII", 70)
    for i in range(100):
        col, row = i % 20, i//20; x = 190+col*81; y = 330+row*112; hot = i < 38
        c.line([(x, y+18), (x, y+52)], 20, INK, False); c.line([(x, y+18), (x, y+52)], 12, RED if hot else GREY, False); c.ell(x-18, y-22, x+18, y+12, PAPER, INK, 5)
    L(c, "38% WERE IN THE PUMICE LAYER", 910, size=66, bg=MARI)
    if k: L(c, "MOST OF THEM INDOORS", 1020, size=60)
    return c
def black(k=0):
    c = C((14, 13, 18)); c.stones(30, T.TT, 1080, 1.2, (70, 68, 72)); c.text(960, 440, "\"BLACKER AND DENSER", 110, (200, 196, 190)); c.text(960, 580, "THAN ANY NIGHT\"", 110, (200, 196, 190)); c.text(960, 740, "PLINY THE YOUNGER", 56, MARI)
    hud(c, "NIGHT", True); return c
def window(k):
    c = C((40, 38, 46)); x, w, h = 420, 700, 760; c.rect(x, 940-h, x+w, 940, RWALL, INK, 7); c.rect(x+3, 940-h*.3, x+w-3, 937, TERRA, None); c.rect(x+w*.4, 940-h*.42, x+w*.6, 940, (92, 66, 46), INK, 5)
    c.rect(x+w*.36, 240, x+w*.64, 400, (60, 48, 42), INK, 6); c.poly([(x-20, 180), (x+w+20, 180), (x+w, 140), (x, 140)], TILE, INK, 6)
    top = 560; c.poly([(0, top)]+[(xx, top+14*math.sin(xx*.011)) for xx in range(0, W+1, 120)]+[(W, H), (0, H)], PUM, INK, 6)
    q = app("climb", 1.2, .2) if k == 1 else 0; sx = lerp(x+w*.5, 1420, q); sy = lerp(400, 560, q)-110*math.sin(q*math.pi)
    sidp(c, sx, sy, 250, "stand" if q in (0, 1) else "run", "worry" if q < 1 else "det", pil=True); dim(c, 90); c.stones(40, T.TT, 560, 1.3)
    L(c, "DOOR BURIED?" if k == 0 else "OUT THROUGH AN UPSTAIRS WINDOW", 1010, size=70, bg=MARI if k else PAPER); return c
def walkout(k, done=0):
    c = C((40, 38, 46)); sky(c, 620, "glow"); c.vesuvius(360, 640, 700, 300, (60, 54, 58), False, False); c.plume(340, 420, 300, 900, T.TT, (84, 76, 80), 1.0); c.rect(0, 620, W, H, PUM, None); c.line([(0, 620), (W, 620)], 6, INK, False)
    off = (T.TT*60) % 240
    for i in range(10): x = i*240-off; c.poly([(x, 640), (x+60, 624), (x+130, 646)], (196, 192, 184), None)
    xs = [520, 760, 1000, 1240, 1480]; fs = []
    for i, x in enumerate(xs):
        if i == 2: f = sidp(c, x, 960, 320, "walk" if (int(T.TT*5)+i) % 2 else "stand", "det", pil=True)
        else: f = c.person(x, 960, 300-(i % 2)*20, "walk" if (int(T.TT*5)+i) % 2 else "stand", ("worry", "det", "n", "worry", "sad")[i], COATS[i]); c.pillow(f)
        fs.append(f)
    for a, b in zip(fs, fs[1:]): c.line([a["hand"], b["hand0"]], 6, (120, 100, 80))
    dim(c, 110); c.stones(46, T.TT, 1080, 1.3)
    if k == 0: L(c, "AND YOU WALK", 120, 1200, 96)
    if k == 1: L(c, "AWAY FROM THE MOUNTAIN", 120, 1200, 76, bg=MARI)
    if k == 2 and not done: L(c, "KEEP WALKING", 120, 1200, 110, bg=MARI)
    hud(c, "NIGHT", True)
    if done: Q(c, 4, done)
    return c
def calls(k):
    c = C((22, 20, 28)); c.rect(0, 820, W, H, (48, 46, 54), None); fs = folk(c, [240, 520, 800, 1080, 1360, 1640], 1010, 280, ("wow", "sad", "worry", "wow", "sad", "worry"), ("up", "shrug", "point", "up", "shrug", "stand"), pil=True); dim(c, 150); c.stones(30, T.TT, 1080, 1.2)
    labs = ["CALLING FOR THEIR PARENTS", "THEIR CHILDREN", "THEIR WIVES"]
    for i in range(min(k+1, 3) if k < 3 else 0): L(c, labs[i], 150+i*130, 420+i*520, 60)
    if k == 3: L(c, "SOME PRAYED FOR DEATH", 300, size=96, bg=MARI); c.text(960, 440, "PLINY THE YOUNGER, ON THE FAR SIDE OF THE BAY", 46, (200, 196, 190))
    return c

# ================= the second morning =================
def column(k):
    c = C((30, 28, 36)); sky(c, 900, "glow" if k == 0 else "dawn"); c.vesuvius(960, 940, 1300, 420, (70, 62, 66), False, False); c.rect(0, 940, W, H, PUM, None); c.line([(0, 940), (W, 940)], 6, INK, False)
    if k == 0:
        c.plume(920, 640, 560, 1500, T.TT, (96, 88, 92), 1.0)
        for j in (-1, 1): arrow(c, 920+j*170, 520, 920+j*170, 300-20*math.sin(T.TT*4), MARI, 14, 40)
        L(c, "ALL NIGHT, IT HOLDS ITSELF UP", 1010, size=70); hud(c, "NIGHT", True); return c
    q = app("coll", 1.3, .15); c.plume(920, 640, 560*(1-.6*q), 1500, T.TT, (96, 88, 92), 1.0)
    for j in (-1, 1): c.puff([(920+j*(120+i*110*q), 660+i*52*q, 80+i*10) for i in range(int(1+5*q))], (120, 110, 108))
    L(c, "AROUND DAWN, IT COLLAPSES", 1010, size=76, bg=MARI); hud(c, "DAWN, DAY 2"); return c
def surge(k):
    c = C(SK["dawn"][1]); sky(c, 700, "dawn"); c.poly([(0, 300), (500, 240), (W, 760), (W, H), (0, H)], (112, 104, 100), INK, 7); c.rect(1500, 700, 1900, 760, None, None, 0)
    adv = T.GP*900 if k <= 2 else 900; bl = []
    for i in range(16): t0 = i/15; x = -200+adv*(.25+.75*t0)+60*math.sin(i*1.9+T.TT*5); y = 250+(x+200)*.27+40*math.cos(i*2.3+T.TT*4); bl.append((x, y-90, 150+40*math.sin(i+T.TT*6)))
    c.puff(bl, (150, 140, 134)); c.rhouse(1560, 930, 260, 200, RWALL, TERRA, upper=False)
    if k == 0: L(c, "NOT LAVA", 950, 620, 110)
    if k == 1: L(c, "GAS AND ASH, AROUND 300°C", 950, 720, 72, bg=MARI)
    if k == 2: L(c, "SOMETHING LIKE 200 MILES AN HOUR", 950, 760, 64, bg=MARI)
    hud(c, "DAWN, DAY 2"); return c
def map2(k):
    c, P = baymap(dots=("HERCULANEUM", "POMPEII") if k else ("HERCULANEUM",), cloud=1); a = (1140, 330); b = P["HERCULANEUM"]; q = app("s1", .8, .2)
    c.puff([(lerp(a[0], b[0], t0*q), lerp(a[1], b[1], t0*q), 34+30*t0) for t0 in (0, .25, .5, .75, 1)], (150, 140, 134)); c.ell(b[0]-18, b[1]-18, b[0]+18, b[1]+18, RED, INK, 6); c.text(b[0]-40, b[1]+56, "HERCULANEUM", 50); L(c, "HERCULANEUM IS HIT FIRST", 900, 1300, 64, bg=MARI); return c
def vaults(k):
    c = C(SK["dawn"][1]); sky(c, 420, "ash"); c.rect(0, 420, W, 820, (176, 160, 140), INK, 7); c.rect(0, 820, W, 940, SAND, None); c.rect(0, 940, W, H, (60, 96, 124), None); c.line([(0, 820), (W, 820)], 6, INK, False)
    for i in range(6):
        x = 170+i*290; c.d.pieslice([(x-110)*S, 520*S, (x+110)*S, 1100*S], 180, 360, fill=(44, 38, 40), outline=INK, width=7*S); c.rect(x-108, 806, x+108, 822, (44, 38, 40), None)
        if k <= 1:
            for j in range(4): c.ell(x-70+j*44, 730+(j % 2)*26, x-38+j*44, 762+(j % 2)*26, PAPER, INK, 4)
    if k == 0: L(c, "STONE VAULTS BY THE BEACH", 130, size=72)
    if k == 1: L(c, "ABOUT 300 PEOPLE SHELTERING", 130, size=72, bg=MARI)
    if k == 2:
        c.rect(0, 0, W, 420, SK["day"][1], None); c.line([(0, 420), (W, 420)], 7, INK, False); f = c.fig(960, 1000, 330, "hold", "wow", "sci"); c.line([f["hand"], (f["hand"][0]+90, f["hand"][1]+60)], 10, WOOD); L(c, "FOUND IN 1980", 130, size=110, bg=MARI)
    return c
def surge7(k):
    g = T.ease(T.GP) if k <= 1 else 1; c = town("pale", peak=False, green=False, layer=200, base=790)
    bl = [(lerp(2300, 200, g)+i*190+50*math.sin(i*2+T.TT*5), 430+120*math.sin(i*1.3)+30*math.cos(T.TT*4+i), 230+40*math.sin(i+T.TT*6)) for i in range(12)]; c.puff(bl, (150, 140, 134))
    if k == 2: c.rect(0, 0, W, H, (150, 140, 134), None); c.text(960, 480, "ANYONE STILL INSIDE THE WALLS", 96, PAPER); c.text(960, 620, "HAS NO CHANCE", 130, PAPER)
    if k == 1: L(c, "A SURGE REACHES POMPEII", 1000, size=76, bg=MARI)
    hud(c, "JUST AFTER 7 AM, DAY 2"); return c
def cause(k):
    c = C((150, 140, 134)); c.text(960, 150, "HOW DID THEY DIE?", 90, PAPER)
    c.rect(140, 300, 920, 800, PAPER, INK, 7, 18); c.text(530, 400, "ONE RECENT STUDY", 60); c.text(530, 560, "SUFFOCATED\nIN THE ASH", 100, RED)
    if k: c.rect(1000, 300, 1780, 800, PAPER, INK, 7, 18); c.text(1390, 400, "OTHERS", 60); c.text(1390, 560, "THE HEAT\nCAME FIRST", 100, RED); L(c, "STILL ARGUED", 930, size=80, bg=MARI)
    return c
def snow(k):
    c = C((226, 222, 214)); sky(c, 620, "pale", False); c.ell(1380, 120, 1500, 240, (246, 240, 226), None); c.vesuvius(560, 660, 1000, 300, (190, 186, 180), False, False)
    c.poly([(0, 620)]+[(x, 640+40*math.sin(x*.006)+20*math.sin(x*.017)) for x in range(0, W+1, 80)]+[(W, H), (0, H)], (236, 232, 224), INK, 6)
    for x, y in ((1180, 700), (1420, 730)): c.poly([(x-90, y), (x+90, y), (x+70, y-30), (x-70, y-30)], TILE, INK, 5)
    for i in range(30): xx = (i*197+T.TT*12) % W; yy = (i*89+T.TT*40) % 600; c.ell(xx, yy, xx+7, yy+7, (250, 248, 244), None)
    if k == 0: L(c, "THEN IT'S QUIET", 150, size=96)
    if k == 1: L(c, "\"BURIED DEEP IN ASH, LIKE SNOW\"", 150, size=76, bg=MARI); c.text(960, 300, "PLINY THE YOUNGER", 50, (110, 104, 100))
    return c
def strata(c, top=330):
    c.rect(0, 0, W, top, SK["day"][1], None); c.rect(0, top, W, top+50, VINE, INK, 6); c.rect(0, top+50, W, H, (176, 168, 160), None)
    for i, col in enumerate(((190, 184, 176), PUM, (160, 152, 146))): c.rect(0, top+50+i*110, W, top+160+i*110, col, None); c.line([(0, top+160+i*110), (W, top+160+i*110)], 4, (130, 124, 120), False)
def gone(k):
    c = C(); strata(c)
    for i, (x, w, h, col, shop) in enumerate(HOUSES): c.rhouse(x, 1040, w, h*.8, (214, 204, 190), (176, 140, 126), shop=bool(shop), roof=i % 2 == 0)
    c.da.rectangle([0, 380*S, W*S, H*S], fill=(176, 168, 160, 120))
    if k == 0: L(c, "NOT RUINED. GONE.", 150, size=100)
    if k == 1: L(c, "UNDER METRES OF ROCK", 150, size=90, bg=MARI)
    if k == 2:
        yr = int(lerp(79, 1748, app("yrs", 1.6, .1))); c.text(960, 170, str(yr), 230, RED); q = app("dig", .5, 1.6); c.line([(1500, 120), (1560, 330+60*q)], 14, WOOD); c.poly([(1530, 330+60*q), (1590, 330+60*q), (1560, 420+60*q)], (150, 150, 160), INK, 5)
    return c
def casts(k):
    c = C(); strata(c, 250)
    if k >= 2: q = app("pour", 1.2, .2) if k == 2 else 1
    c.castfig(960, 700, 2.2, plaster=k >= 3)
    if k == 2:
        c.da.ellipse([(960-330*q)*S, (700-60)*S, (960+330*q)*S, (700+70)*S], fill=(240, 236, 226, 230)); c.castfig(960, 700, 2.2, plaster=False); c.line([(960, 250), (960, 640)], 16, (240, 236, 226), False); c.rect(900, 150, 1020, 250, (200, 196, 190), INK, 6, 8)
    f = c.fig(420, 250, 190, "point", "wow" if k < 3 else "sad", "sci")
    L(c, ["HOLLOWS IN THE HARDENED ASH", "SPACES WHERE BODIES USED TO BE", "FILL ONE WITH PLASTER", "A PERSON, IN THEIR LAST MOMENT"][k], 990, size=66, bg=MARI if k in (1, 3) else PAPER); return c
def count1150(k):
    c = C(); v = int(lerp(0, 1150, app("c1150", 1.4, .1))); c.text(700, 380, format(v, ","), 300, RED); c.text(700, 620, "BODIES FOUND SO FAR (ABOUT)", 64)
    if k:
        c.rect(1240, 240, 1780, 760, (226, 214, 190), INK, 8, 30); c.poly([(1560, 244), (1776, 244), (1776, 500), (1640, 460)], (150, 146, 140), INK, 6); c.text(1670, 350, "NOT\nYET\nDUG", 54, PAPER)
        for i in range(4): c.line([(1260, 340+i*100), (1620-(i % 2)*60, 340+i*100)], 5, (170, 150, 120)); c.line([(1320+i*90, 260), (1320+i*90, 740)], 5, (170, 150, 120))
        c.text(1510, 820, "THE TOWN, FROM ABOVE (SKETCH)", 40, (120, 110, 98))
    return c
def didyou(k=0):
    c = C(PUM); sky(c, 640, "pale", False); c.vesuvius(420, 660, 800, 240, (176, 170, 166), False, False); c.rect(0, 640, W, H, (226, 222, 214), None); c.line([(0, 640), (W, 640)], 6, INK, False)
    sidp(c, 620, 960, 340, "chin", "worry", pil=True); c.questlog(ROWS, 4, 2, None)
    L(c, "DID YOU MAKE IT?", 1010, 520, 80, bg=MARI); return c
def depends(k):
    c = C()
    for i in range(min(k+1, 2)):
        y = 380+i*330; good = i == 0; c.rect(160, y-120, 1760, y+120, WHITE, INK, 7, 18); c.text(220, y-50, "LEFT IN THE AFTERNOON" if good else "WAITED FOR IT TO STOP", 70, INK, "lm")
        q = app(("dep", i), 1.0, .2); x = lerp(260, 1300, q)
        if good: c.fig(x, y+100, 150, "walk" if step() and q < 1 else "stand", "det", "modern"); (c.tick(1560, y, 60) if q >= 1 else None)
        else:
            c.rhouse(1130, y+104, 200, 150, RWALL, TERRA, upper=False); (c.redx(1560, y, 60, 22) if q >= 1 else None)
    L(c, "IT DEPENDS", 130, size=96); return c

# ================= the hidden quest =================
def myth(k):
    c = C((236, 226, 210)); c.rect(520, 260, 1400, 800, CREAM, INK, 8, 10); c.ell(480, 240, 560, 820, (226, 206, 160), INK, 7); c.ell(1360, 240, 1440, 820, (226, 206, 160), INK, 7)
    c.text(960, 400, "THE STORY OF POMPEII", 60); c.text(960, 560, "EVERYBODY DIED.", 100); c.text(960, 700, "THE END", 60, (120, 110, 98))
    if k >= 1: None
    if k == 2: c.strike(600, 560, 1320, 26); L(c, "THEY DIDN'T", 950, size=120, bg=MARI)
    return c
def pop(k):
    c = C(); c.text(960, 150, "POMPEII AND HERCULANEUM: 15,000 TO 20,000 PEOPLE", 60)
    for i in range(100):
        col, row = i % 20, i//20; x = 190+col*81; y = 320+row*112; dead = i >= 89 and k
        c.line([(x, y+18), (x, y+52)], 20, INK, False); c.line([(x, y+18), (x, y+52)], 12, (150, 146, 142) if dead else TEAL, False); c.ell(x-18, y-22, x+18, y+12, PAPER, INK, 5)
    if k: L(c, "THOUGHT TO HAVE DIED: ABOUT 2,000", 950, size=66, bg=MARI); c.text(960, 1040, "(EACH FIGURE: ABOUT 175 PEOPLE)", 40, (120, 110, 98))
    return c
def where(k=0):
    c = C(PUM); sky(c, 640, "pale", False); c.rect(0, 640, W, H, (214, 206, 190), None); c.line([(0, 640), (W, 640)], 6, INK, False); c.poly([(700, 1080), (900, 640), (1020, 640), (1220, 1080)], (190, 180, 164), INK, 5)
    off = T.GP*120
    for i, x in enumerate((500, 760, 1000, 1240, 1460)): c.person(x+off*.3, 940-(i % 2)*30, 250, "walk" if (int(T.TT*5)+i) % 2 else "stand", ("worry", "n", "sad", "det", "worry")[i], COATS[i])
    c.text(960, 330, "?", 330, RED); L(c, "WHERE DID EVERYONE ELSE GO?", 990, size=72, bg=MARI); return c
def tuck(k):
    if k <= 1:
        c = roomset((226, 222, 214), (150, 140, 128)); c.rect(980, 660, 1700, 700, WOOD, INK, 6, 4); c.line([(1040, 700), (1040, 900)], 14, WOOD); c.line([(1640, 700), (1640, 900)], 14, WOOD)
        f = c.fig(760, 940, 350, "hold", "det", "sci"); c.glasses(f); c.rect(1100, 380, 1560, 660, CREAM, INK, 6, 6)
        for i in range(6): c.line([(1140, 430+i*38), (1500-(i % 3)*50, 430+i*38)], 5, (120, 100, 80))
        c.text(1330, 330, "FAMILY NAMES", 54); L(c, "STEVEN TUCK, HISTORIAN" if k == 0 else "NAMES DISTINCTIVE TO THE TWO TOWNS", 110, size=66 if k == 0 else 58, bg=MARI if k else PAPER); return c
    c = C(); c.text(480, 190, "NAMES FROM POMPEII", 60); c.text(1440, 190, "OTHER TOWNS, AFTER AD 79", 60)
    for i in range(5):
        y = 320+i*130; c.rect(240, y-44, 720, y+44, CREAM, INK, 6, 10); c.line([(280, y), (640-(i % 2)*80, y)], 7, (120, 100, 80)); c.rect(1200, y-44, 1680, y+44, WHITE, INK, 6, 10); c.line([(1240, y), (1560-(i % 3)*60, y)], 7, (150, 146, 142))
        q = app(("match", i), .35, .25+i*.3)
        if q > 0 and i != 3: j = (i+2) % 5; arrow(c, 720, y, lerp(720, 1200, q), lerp(y, 320+j*130, q), TEAL, 9, 26)
    L(c, "HE LOOKED FOR THEM ELSEWHERE", 1000, size=66, bg=MARI); return c
def found(k):
    names = ["NAPLES", "CUMAE", "PUTEOLI"]; hold = T.LT/max(T.LP, 1e-6) if T.LP < 1 else 0
    c, P = baymap(dots=(), cloud=1); x, y = P["POMPEII"]; c.ell(x-16, y-16, x+16, y+16, (110, 104, 100), INK, 5); c.text(x+30, y+4, "POMPEII", 44, (90, 84, 80), "lm")
    for i, n in enumerate(names):
        q = app(("fd", n), .3, (.28+i*.2)*hold) if k == 0 else 1
        if q > 0: a, b = P[n]; c.ell(a-24*q, b-24*q, a+24*q, b+24*q, TEAL, INK, 6); c.text(a, b-56, n, 60*q+1)
    q = app("fd_ost", .3, .86*hold) if k == 0 else 1
    if q > 0: arrow(c, 520, 90, 400, 30, TEAL, 14, 40); c.text(840, 84, "OSTIA, UP THE COAST", 54*q+1)
    if k == 1: c.ell(210, 150, 950, 420, None, MARI, 12); L(c, "MOSTLY THE SAME STRETCH OF COAST", 880, 1300, 56, bg=MARI)
    if k == 2: L(c, "AND HE SAYS HIS COUNT IS FAR TOO LOW", 880, 1280, 54, bg=MARI)
    return c
def emperor(k):
    c = C(SK["day"][1]); sky(c, 640, "day"); c.rect(0, 640, W, H, PAVE, None); c.line([(0, 640), (W, 640)], 6, INK, False)
    q = app("build", 1.2, .1) if k == 1 else (0 if k == 0 else 1)
    for i, x in enumerate((900, 1240, 1560)):
        h = 300*max(.15, q if k else .15); c.rhouse(x, 900, 280, h, RWALL if i % 2 else OCHRE, TERRA, upper=h > 200, roof=q >= 1, door=h > 160)
        if k and q < 1:
            for xx in (x-20, x+300): c.line([(xx, 900), (xx, 560)], 9, WOOD)
            c.line([(x-20, 900-h-20), (x+300, 900-h-20)], 8, WOOD)
    f = c.person(420, 960, 380, "point", "det", (126, 70, 130)); u = f["u"]; hx, hy = f["head"]
    for j in range(7): a = math.radians(200+j*23); c.ell(hx+.62*u*math.cos(a)-12, hy+.5*u+.62*u*math.sin(a)-12, hx+.62*u*math.cos(a)+12, hy+.5*u+.62*u*math.sin(a)+12, (104, 150, 90), INK, 3)
    L(c, "THE EMPEROR PAYS FOR NEW BUILDING" if k == 0 else "WITH THE MONEY OF VICTIMS WHO LEFT NO HEIRS", 120, size=62 if k == 0 else 52, bg=MARI if k else PAPER); return c
def fourth(k):
    c = C(); c.questlog(ROWS, 4, 4 if k else 3, HID, x=545, y=200)
    if k: c.marker(470, 800, 36)
    return c
def names(k):
    c = C((226, 222, 214)); c.rect(0, 860, W, H, (150, 140, 128), None); c.line([(0, 860), (W, 860)], 6, INK, False)
    c.poly([(560, 880), (560, 380), (760, 250), (1160, 250), (1360, 380), (1360, 880)], (214, 208, 200), INK, 8); c.text(960, 420, "A FAMILY NAME", 64); c.text(960, 520, "FROM POMPEII", 64)
    for i in range(3): c.line([(660, 620+i*60), (1260-(i % 2)*120, 620+i*60)], 7, (150, 146, 142))
    if k: L(c, "CARVED IN THE WRONG TOWN", 130, size=80, bg=MARI); sidp(c, 1620, 1000, 300, "point", "smile", flip=True)
    else: L(c, "WE CAN'T NAME MOST OF THEM", 130, size=76)
    return c
def oven80(k):
    c = C((58, 50, 48)); c.d.pieslice([200*S, 120*S, 1720*S, 1700*S], 180, 360, fill=(150, 116, 96), outline=INK, width=10*S); c.rect(200, 900, 1720, 1000, (120, 84, 70), INK, 8)
    n = int(80*app("o80", 1.5, .1)+.5) if k == 0 else 80
    for i in range(n):
        row = i//16; col = i % 16; x = 330+col*84+(row % 2)*40; y = 440+row*92; c.rloaf(x, y, .66, True)
    c.text(960, 290, "ABOUT "+str(n)+" LOAVES" if k <= 1 else " ", 90, INK)
    if k == 1: L(c, "BURNT BLACK, WHERE THE BAKER LEFT THEM", 1010, size=58, bg=MARI)
    if k == 2: L(c, "SOMEBODY PUT THEM IN", 290, size=84)
    if k == 3: L(c, "NOBODY TOOK THEM OUT", 290, size=84, bg=MARI); c.line([(1500, 1060), (1760, 420)], 14, WOOD); c.ell(1700, 330, 1830, 440, WOOD, INK, 6)
    return c
def maybe(k):
    c = C(); c.rect(120, 220, 920, 860, (226, 222, 214), INK, 7, 18); c.text(520, 520, "?", 420, (150, 146, 142)); c.text(520, 940, "MAYBE THAT BAKER DIED", 60)
    if k:
        c.rect(1000, 220, 1800, 860, SK["day"][1], INK, 7, 18); c.plume(1640, 620, 260, 300, T.TT, ASHC, 1.0); c.rect(1004, 700, 1796, 856, PAVE, None); c.line([(1000, 700), (1800, 700)], 5, INK, False)
        x = lerp(1560, 1180, T.ease(T.LP)); f = c.person(x, 840, 280, "run" if step() else "walk", "det", "brown", flip=True); c.pillow(f); c.rloaf(1650, 800, .7); c.text(1400, 940, "OR LEFT THE BREAD", 60, TEAL)
    return c
def leave(k):
    c = town("noon", peak=False, plume=(420, 620, ASHC, 1.0)); x = lerp(700, 1500, T.ease(T.GP)); sidp(c, x, 990, 330, ("run" if step() else "walk") if T.GP < .97 else "wave", "det" if T.GP < .97 else "smile")
    c.rect(300, 880, 620, 910, WOOD, INK, 6, 4)
    for i in range(3): c.rloaf(360+i*100, 850, .8)
    if k: L(c, "LEAVE THE BREAD", 150, 1100, 120, bg=MARI)
    return c
def finale(k=0):
    c = C(SEA); sky(c, 600, "day"); c.rect(0, 600, W, 700, SEA, None); c.rect(0, 690, W, H, PAVE, None); c.line([(0, 690), (W, 690)], 6, INK, False); c.rhouse(60, 900, 330, 300, OCHRE, TERRA, shop=True); c.rhouse(420, 900, 300, 330, RWALL, TERRA)
    for i in range(3): c.rloaf(130+i*90, 760, .7)
    sidp(c, 840, 1000, 330, "cheer", "joy"); Q(c, 4, 4, HID); L(c, "QUEST COMPLETE", 100, 480, 100, bg=MARI); return c

U = [
 ("You wake up in Pompeii. It's the year seventy-nine.", [F(card, "POMPEII. AD 79."), F(wake, 0)]),
 ("You have about seven hours of normal life left.", [F(clockbar, 0)]),
 ("After that, you have one night to make one decision.", [F(clockbar, 1)]),
 ("Most people in this town got out alive. More than a thousand did not.", [F(crowdsplit, 0), F(crowdsplit, 1)]),
 ("As far as anyone can tell, the difference was mostly when they left.", [F(whenleft)]),
 ("So let's put you there, and see what you'd do.", [F(intro, 0)], "chime"),
 ("You're nineteen. You work the ovens at a bakery near the forum.", [F(bakery, 0), F(bakery, 1)]),
 ("You are made up. The town, the timeline and the bodies are not.", [F(card, "YOU ARE MADE UP.", "THE TOWN, THE TIMELINE AND THE BODIES ARE NOT.", 140)]),
 ("Here's your quest log. One: get through the morning.", [F(qbake, 0), F(qbake, 1)], "tick"),
 ("Two: read the sky.", [F(qbake, 2)], "tick"),
 ("Three: get out in time.", [F(qbake, 3)], "tick"),
 ("There's a fourth quest hidden at the end. It's the part of this story almost nobody tells.", [F(qbake, 4), F(hiddenq, 1, 0)], "tick"),
 ("First light, on a day in late summer or autumn. Scholars still argue about which.", [F(dawn, 0), F(dawn, 1)]),
 ("Pompeii is a port town of somewhere between ten and fifteen thousand people.", [F(dawn, 2), F(dawn, 3)]),
 ("It's a working town. Its wine jars turn up as far away as Spain. Its fish sauce reaches Gaul.", [F(trade, 0), F(trade, 1), F(trade, 2)]),
 ("Your day starts before everyone else's, because everyone else wants bread.", [F(bakery, 2), F(breadline)]),
 ("There are about thirty-five bakeries in town. Many grind their own flour.", [F(bakecount, 0), F(bakecount, 1)]),
 ("The mill is a block of lava rock, and a donkey walks it round in circles.", [F(millscene, 0), F(millscene, 1)]),
 ("The donkey has the worst job in Pompeii. You have the second worst.", [F(millscene, 2), F(millscene, 3)]),
 ("By sunrise the first loaves are out, each one stamped with the bakery's mark.", [F(loaves, 0), F(loaves, 1)]),
 ("Now, the street. The street is disgusting.", [F(street, 0), F(street, 1)]),
 ("Most houses have no drain, so the dirty water goes out the front door.", [F(street, 2)]),
 ("That's why the roads have stepping stones. Big raised blocks, so you can cross with dry feet.", [F(stonesc, 0), F(stonesc, 1)]),
 ("The gaps between them are just wide enough for cart wheels.", [F(stonesc, 2)]),
 ("It's a two-thousand-year-old crosswalk.", [F(stonesc, 3)]),
 ("The walls are covered in writing. A lot of it is election ads.", [F(wall, 0), F(wall, 1)]),
 ("One says all the worshippers of Isis are voting for Helvius Sabinus.", [F(wall, 2)]),
 ("Another says all the deadbeats are asking for Vatia. Vatia probably didn't pay for that one.", [F(wall, 3), F(wall, 4)]),
 ("And somebody has scratched a complaint. I admire you, wall, for not having collapsed under so much tedious scribbling.", [F(wall, 5), F(wall, 6)]),
 ("Lunch. You don't cook. A flat like yours has no kitchen, or one that's a fire hazard.", [F(flat, 0), F(flat, 1)]),
 ("So the town has a hundred and fifty-eight snack bars.", [F(bars)]),
 ("A stone counter, with big jars sunk into it. Food and wine, to go, for a few coins.", [F(snack, 0), F(snack, 1)]),
 ("Fast food is not a modern idea.", [F(snack, 2)]),
 ("Down the road is the amphitheatre. It holds twenty thousand people. That's more than live here.", [F(amph, 0), F(amph, 1), F(amph, 2)]),
 ("Twenty years ago a bloody brawl broke out in the stands, against fans from the next town. Rome shut the arena for ten years.", [F(brawl, 0), F(brawl, 1), F(brawl, 2)]),
 ("So yes. This town got a stadium ban.", [F(brawl, 3)]),
 ("One more thing. The ground shakes here. A lot.", [F(quake, 0)]),
 ("Seventeen years ago an earthquake badly damaged the town. Some of it still isn't fixed.", [F(quake, 1), F(quake, 2)]),
 ("For the last four days there have been small tremors. Nobody panics. Tremors are normal here.", [F(quake, 3), F(quake, 4)]),
 ("And the mountain behind the town is just a mountain. Farms. Good soil.", [F(mountain, 0), F(mountain, 1)]),
 ("It last erupted so long ago that nobody here knows what it is.", [F(mountain, 2)]),
 ("Quest one, complete. That was the last normal morning.", [F(mountain, 3, 1)], "chime"),
 ("About one in the afternoon.", [F(card, "ABOUT 1 PM")]),
 ("A column of ash and rock punches straight up out of the mountain.", [F(erupt, 0), F(erupt, 1)]),
 ("Across the bay, a young man named Plinny is watching. His letters are our eyewitness account.", [F(pliny, 0), F(pliny, 1), F(pliny, 2)]),
 ("He says the cloud looks like an umbrella pine. A tall trunk, then branches spreading flat.", [F(pine, 0), F(pine, 1)]),
 ("Modern estimates put that trunk at up to thirty kilometres high.", [F(height)]),
 ("By one estimate, it throws out a million and a half tons of rock every second.", [F(rate)]),
 ("And the wind is carrying it straight over you.", [F(wind)]),
 ("The sun goes out. Then it starts to rain stones.", [F(dark, 0), F(dark, 1)]),
 ("Pumice. Light rock, full of holes. It mostly doesn't kill you. It piles up.", [F(pumice, 0), F(pumice, 1), F(pumice, 2)]),
 ("Quest two. Read the sky. And here's the problem.", [F(dark, 2, 1)]),
 ("Nobody in town has a plan for this, because nobody knew it could happen.", [F(noplan, 0), F(noplan, 1)]),
 ("So you have two options. Shelter indoors, and wait for it to stop.", [F(choice, 0), F(choice, 1)]),
 ("Or walk out, in the dark, with stones falling on your head.", [F(choice, 2)]),
 ("Indoors feels like the smart choice.", [F(choice, 3)]),
 ("Down the coast, people are tying pillows to their heads with strips of cloth. That's not a joke. Plinny wrote it down.", [F(pillows, 0), F(pillows, 1), F(pillows, 2)]),
 ("Out at sea, the commander of the Roman fleet has launched his warships to rescue people from the shore. He is Plinny's uncle.", [F(fleet, 0), F(fleet, 1), F(fleet, 2)]),
 ("Ash falls on the decks, hotter and thicker the closer they get.", [F(fleet, 3)]),
 ("He could turn back. He says: fortune favours the brave.", [F(fleet, 4), F(fleet, 5)]),
 ("He lands down the coast. By tomorrow he will be dead on that beach.", [F(beach, 0), F(beach, 1)]),
 ("Back in Pompeii, hour after hour, the stones keep coming.", [F(night, 0), F(night, 1)]),
 ("The pumice falls for about eighteen hours. By the end it's nearly three metres deep.", [F(depth, 0), F(depth, 1)]),
 ("Now think about that on a roof.", [F(roof, 0)]),
 ("As it piles up, roofs start to give way.", [F(roof, 1)]),
 ("Of the bodies found in Pompeii, more than a third were in this layer. Most of them indoors.", [F(third, 0), F(third, 1)]),
 ("For them, the shelter was the trap.", [F(choice, 4)]),
 ("Outside, Plinny says it's blacker than any night.", [F(black)]),
 ("If your door is buried, you go out through an upstairs window.", [F(window, 0), F(window, 1)]),
 ("And you walk. Away from the mountain, with a pillow on your head, holding on to the person in front.", [F(walkout, 0), F(walkout, 1)]),
 ("On the far side of the bay, Plinny is running too. He hears people calling for their parents, their children, their wives.", [F(calls, 0), F(calls, 1), F(calls, 2)]),
 ("He says some were so afraid of dying that they prayed for death.", [F(calls, 3)]),
 ("Keep walking.", [F(walkout, 2)]),
 ("Quest three. Get out in time. Here is what in time means.", [F(walkout, 2, 2)]),
 ("All night, that column of ash has been holding itself up.", [F(column, 0)]),
 ("Around dawn, it collapses.", [F(column, 1)]),
 ("What comes down the mountain isn't lava. It's a cloud of gas and ash, at around three hundred degrees, moving at something like two hundred miles an hour.", [F(surge, 0), F(surge, 1), F(surge, 2)]),
 ("The first surges hit Her-cue-lay-nee-um, the next town along the bay.", [F(map2, 0)]),
 ("About three hundred people are sheltering in the stone vaults by its beach.", [F(vaults, 0), F(vaults, 1)]),
 ("They are found in nineteen eighty.", [F(vaults, 2)]),
 ("Shortly after seven in the morning, a surge reaches Pompeii.", [F(surge7, 0), F(surge7, 1)]),
 ("Anyone still inside the walls has no chance.", [F(surge7, 2)]),
 ("One recent study says most of them suffocated in the ash. Others think the heat killed them first.", [F(cause, 0), F(cause, 1)]),
 ("Then it's quiet. Plinny says that when daylight came back, everything was buried deep in ash, like snow.", [F(snow, 0), F(snow, 1)]),
 ("The town isn't ruined. It's gone. Under metres of rock.", [F(gone, 0), F(gone, 1)]),
 ("It stays hidden until seventeen forty-eight.", [F(gone, 2)]),
 ("When people dig, they find hollows in the hardened ash. Spaces where bodies used to be.", [F(casts, 0), F(casts, 1)]),
 ("Fill one with plaster, and you get the shape of a person in their last moment.", [F(casts, 2), F(casts, 3)]),
 ("About eleven hundred and fifty bodies have been found so far. And part of the town has never been dug.", [F(count1150, 0), F(count1150, 1)]),
 ("So. Quest three. Did you make it?", [F(didyou)]),
 ("That depends on whether you left in the afternoon, or waited for it to stop.", [F(depends, 0), F(depends, 1)]),
 ("Now the hidden one.", [F(hiddenq, 0), F(hiddenq, 1)], "chime"),
 ("For a long time, the story of Pompeii ended right there. Everybody died.", [F(myth, 0), F(myth, 1)]),
 ("They didn't.", [F(myth, 2)]),
 ("Pompeii and Her-cue-lay-nee-um together held fifteen to twenty thousand people. The eruption is thought to have killed about two thousand of them.", [F(pop, 0), F(pop, 1)]),
 ("So where did everyone else go?", [F(where)]),
 ("A historian named Steven Tuck went looking. He took family names that were distinctive to the two towns, and searched for them in other places, after the eruption.", [F(tuck, 0), F(tuck, 1), F(tuck, 2)]),
 ("He found them. In Naples. In Koo-my. In Poo-tee-oh-lee. In Oss-tee-ah.", [F(found, 0)]),
 ("Mostly along the same stretch of coast.", [F(found, 1)]),
 ("And he says his count is far too low.", [F(found, 2)]),
 ("The emperor paid for new building in those towns. He used the money of victims who died with no heirs.", [F(emperor, 0), F(emperor, 1), F(emperor, 2)]),
 ("That's the fourth quest. Start again.", [F(fourth, 0), F(fourth, 1)], "tick"),
 ("We can't name most of the people who did it. We only know they did, because their names turn up in the wrong town.", [F(names, 0), F(names, 1)]),
 ("As for the bakery. In one oven in Pompeii, about eighty loaves were found, burnt black, right where the baker left them.", [F(oven80, 0), F(oven80, 1)]),
 ("Somebody put them in. Nobody took them out.", [F(oven80, 2), F(oven80, 3)]),
 ("Maybe that baker died. Or maybe that baker looked at the sky, did the sums, and left the bread.", [F(maybe, 0), F(maybe, 1)]),
 ("If the ground shakes and the sky goes dark at noon: leave the bread.", [F(leave, 0), F(leave, 1)]),
 ("Quest complete.", [F(finale)], "chime"),
]

CAPTION_FIX = [("Plinny", "Pliny"), ("Her-cue-lay-nee-um", "Herculaneum"), ("Oss-tee-ah", "Ostia"), ("Koo-my", "Cumae"), ("Poo-tee-oh-lee", "Puteoli"),
               ("the year seventy-nine", "the year 79"), ("nineteen eighty", "1980"), ("seventeen forty-eight", "1748"),
               ("ten and fifteen thousand", "10,000 and 15,000"), ("fifteen to twenty thousand", "15,000 to 20,000"), ("twenty thousand", "20,000"), ("about two thousand", "about 2,000"),
               ("two-thousand-year-old", "2,000-year-old"), ("a hundred and fifty-eight", "158"), ("thirty-five", "35"), ("eleven hundred and fifty", "1,150"),
               ("a million and a half", "1.5 million"), ("thirty kilometres", "30 kilometres"), ("three hundred degrees", "300 degrees"), ("two hundred miles", "200 miles"),
               ("About three hundred people", "About 300 people"), ("about eighteen hours", "about 18 hours"), ("three metres", "3 metres"), ("about eighty loaves", "about 80 loaves"),
               ("about seven hours", "about 7 hours"), ("ten years", "10 years"), ("Seventeen years", "17 years"), ("Twenty years", "20 years"), ("seven in the morning", "7 in the morning")]
