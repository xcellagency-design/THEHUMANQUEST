"""EP004: You Survived the Black Death. Now Ask for a Raise.   (England, 1349-1381; money pillar)

Same contract as ep01.py / ep02.py / ep03.py. Motion helpers (app, E, lerp, step, arrow) come from ep02.
A year chip in the top-left corner carries the date through the episode, the way EP003's clock did.
Every moving thing is driven by T.LT / T.LP / T.GP / T.TT and rests in its final state on the contact sheet.
"""
from thsq import *
import math
import thsq as T
import life
from ep02 import E, app, lerp, step, L, card, arrow, chip, F
ROWS = ["LIVE THROUGH THE PLAGUE", "GET A RAISE", "KEEP IT"]; HID = "OUTLAST THEM"
SK = {"day": ((140, 196, 226), (236, 240, 230)), "dawn": ((122, 150, 200), (250, 214, 176)), "grey": ((120, 126, 140), (198, 200, 196)),
      "dusk": ((60, 52, 84), (226, 140, 100)), "gold": ((240, 190, 110), (252, 232, 170)), "night": ((16, 22, 48), (58, 70, 112))}
PATH = (206, 186, 140); PATH2 = (176, 156, 112); ROOM = (214, 204, 190); FLOORC = (170, 130, 96); SEA = (98, 152, 182); INKP = (110, 40, 30); FAINT = (96, 88, 78)
COATS = ["brown", "green", "blue", "rose", "slate"]; HOODS = {"brown": (150, 100, 70), "green": (96, 130, 90), "blue": (86, 130, 160), "rose": (190, 120, 110), "slate": (84, 90, 110), "teal": (30, 120, 116), "red": (170, 60, 50)}
COTS = [(40, 300, 170), (390, 280, 160), (1130, 300, 175), (1480, 270, 160), (1780, 300, 170)]

# ---------- small helpers ----------
def Q(c, shown=4, done=0, hidden=None): c.questlog(ROWS, shown, done, hidden); return c
def dimc(c, a=120, col=(20, 18, 26)): c.da.rectangle([0, 0, W*S, H*S], fill=(*col, int(max(0, min(255, a)))))
def hud(c, t):
    w = c.tw(t, 46)+112; c.rect(36, 36, 36+w, 116, PAPER, INK, 6, 16); c.penny(80, 76, 24); c.text(124, 74, t, 46, INK, "lm")
def sky(c, hz, kind="day", clouds=True, sun=True):
    c.im.paste(life._grad(hz, *SK[kind]), (0, 0))
    if kind == "night":
        for i in range(50): x = (i*197) % W; y = (i*89) % max(60, hz-80)+10; r = 3+2*math.sin(T.TT*2+i); c.da.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=(255, 248, 236, 230))
        return
    if sun and kind in ("day", "gold", "dawn"): c.da.ellipse([1615*S, 165*S, 1885*S, 435*S], fill=(255, 226, 130, 70)); c.ell(1685, 235, 1815, 365, MARI, INK, 6)
    if clouds:
        for i, (cx, cy, k) in enumerate(((260, 110, 1.0), (900, 70, .7), (1320, 180, .8))):
            xx = (cx+T.TT*(7+3*i)) % (W+400)-200
            for dx, dy, r in ((-70, 10, 44), (0, -14, 60), (70, 12, 46), (0, 22, 50)): c.da.ellipse([(xx+dx*k-r*k*1.5)*S, (cy+dy*k-r*k)*S, (xx+dx*k+r*k*1.5)*S, (cy+dy*k+r*k)*S], fill=(255, 255, 255, 200 if kind in ("day", "dawn") else 120))
def hills(c, hz, col=(168, 200, 140)):
    c.poly([(0, hz), (0, hz-60), (300, hz-110), (700, hz-50), (1100, hz-100), (1500, hz-40), (W, hz-80), (W, hz)], col, INK, 5)
def farvill(c, x, y, k=1.0):
    """A village far away: three small roofs and a church tower. (x, y) = ground."""
    for dx, w in ((0, 70), (90, 60), (250, 70)):
        c.rect(x+dx*k, y-34*k, x+(dx+w)*k, y, DAUB, INK, 4); c.poly([(x+(dx-8)*k, y-34*k), (x+(dx+w/2)*k, y-70*k), (x+(dx+w+8)*k, y-34*k)], THATCH, INK, 4)
    c.rect(x+170*k, y-96*k, x+204*k, y, FLINT, INK, 4); c.poly([(x+166*k, y-96*k), (x+187*k, y-130*k), (x+208*k, y-96*k)], (160, 108, 88), INK, 4)
def vill(kind="day", dead=(), hz=540, smoke=True):
    """The village set: hills, church, a row of cottages, the yard in front. dead = indexes of cottages gone dark."""
    grey = kind == "grey"; c = C(GRASS); sky(c, hz, kind); hills(c, hz, (150, 164, 140) if grey else (168, 200, 140))
    c.rect(0, hz, W, H, (150, 170, 130) if grey else GRASS, None); c.line([(0, hz), (W, hz)], 5, INK, False); c.church(790, hz+120, .66); c.tree(690, hz+130, .8); c.tree(1110, hz+70, .5)
    for i, (x, w, h) in enumerate(COTS):
        top = c.cottage(x, 800, w, h, dead=i in dead)
        if smoke and i not in dead: c.smoke(top[0]+w*.22, top[1]-6, 3)
    c.rect(0, 800, W, H, PATH, None); c.line([(0, 800), (W, 800)], 5, INK, False)
    for i in range(10): c.line([(i*210+40, 860+(i % 3)*64), (i*210+100, 860+(i % 3)*64)], 4, PATH2, False)
    return c
def field(kind="day", hz=500, far=True, cols=None):
    """The open field: ridge-and-furrow strips running to the horizon."""
    c = C(GRASS); sky(c, hz, kind); hills(c, hz+10)
    if far: farvill(c, 250, hz+12); farvill(c, 1380, hz+12, .8); c.tree(700, hz+16, .5); c.tree(1180, hz+16, .44)
    c.strips(hz+16, H, 9, cols=cols or ((176, 200, 120), (212, 194, 112), (166, 128, 94))); c.line([(0, hz+16), (W, hz+16)], 5, INK, False)
    return c
def meadow(kind="day", hz=560, road=False, sun=True):
    c = C(GRASS); sky(c, hz, kind, sun=sun); hills(c, hz); c.rect(0, hz, W, H, GRASS if kind != "grey" else (150, 170, 130), None); c.line([(0, hz), (W, hz)], 5, INK, False)
    if road:
        c.rect(0, 830, W, 1010, PATH, None); c.line([(0, 830), (W, 830)], 5, INK, False); c.line([(0, 1010), (W, 1010)], 5, INK, False)
        for i in range(9): c.line([(i*230+30, 920), (i*230+110, 920)], 5, PATH2, False)
    return c
def hall(kind="day", win=True):
    """Inside the manor hall: timber posts, a tall window, a boarded floor."""
    c = C(ROOM)
    for i in range(6): c.line([(i*370+60, 0), (i*370+60, 780)], 24, TIMBER, False)
    c.line([(0, 80), (W, 80)], 28, TIMBER, False)
    if win:
        c.ell(1300, 250, 1540, 490, SK[kind][1], INK, 9); c.rect(1300, 370, 1540, 650, SK[kind][1], INK, 9); c.rect(1306, 362, 1534, 390, SK[kind][1], None); c.line([(1420, 256), (1420, 650)], 7); c.line([(1300, 510), (1540, 510)], 7)
    c.rect(0, 780, W, H, FLOORC, None); c.line([(0, 780), (W, 780)], 6, INK, False)
    for i in range(1, 8): c.line([(i*260-60, 786), (i*280-180, H)], 3, (140, 104, 76))
    return c
def table(c, x0=980, x1=1700, y=780):
    c.line([(x0+50, y), (x0+50, y+150)], 16, TIMBER, False); c.line([(x1-50, y), (x1-50, y+150)], 16, TIMBER, False); c.rect(x0, y-34, x1, y, WOOD, INK, 6, 4)
def parch(title=None, size=70):
    c = C((226, 214, 190)); c.roll(260, 90, 1660, 990, 40)
    if title: c.text(960, 200, title, size, INKP)
    return c
def cotin(kind="night"):
    """Inside a cottage: daub wall, beams, a small window, a hearth, an earth floor."""
    c = C((196, 180, 156)); c.line([(0, 110), (W, 110)], 26, TIMBER, False)
    for x in (380, 1540): c.line([(x, 110), (x, 800)], 22, TIMBER, False)
    c.rect(1600, 230, 1800, 410, SK[kind][1], INK, 9); c.line([(1700, 230), (1700, 410)], 7); c.rect(0, 800, W, H, (150, 118, 92), None); c.line([(0, 800), (W, 800)], 6, INK, False)
    c.rect(120, 760, 330, 800, (120, 116, 112), INK, 6, 8); c.fire(225, 760, 1.2)
    return c
def pallet(c, x0=560, x1=1260, y=800):
    c.rect(x0, y-40, x1, y, WOOD, INK, 6, 4); c.rect(x0+10, y-92, x1-10, y-36, THATCH, INK, 6, 16); c.rect(x0+14, y-128, x0+190, y-84, WOOL, INK, 5, 18)
def emap(dots=(), sea=(196, 220, 230)):
    """Sketch map of Britain. dots = [(place, label, dx, dy)]. Returns (canvas, places)."""
    c = C(sea); P = c.britain(560, 60, 1.08)
    for i in range(12): x = (i*211) % 480+30; y = 150+(i*137) % 820; c.line([(x, y), (x+50, y)], 5, WHITE, False)
    for i in range(8): x = 1400+(i*173) % 440; y = 110+(i*197) % 860; c.line([(x, y), (x+50, y)], 5, WHITE, False)
    for n, lab, dx, dy in dots:
        x, y = P[n]; q = app(("dot", n), .25); c.ell(x-16*q, y-16*q, x+16*q, y+16*q, RED, INK, 6)
        if lab: c.label(x+dx, y+dy, lab, 44)
    c.text(280, 1040, "SKETCH MAP, NOT TO SCALE", 38, (90, 120, 136)); return c, P
def sidp(c, x, y, h, pose="stand", ex="n", **k): return c.fig(x, y, h, pose, ex, "modern", **k)
def peasant(c, x, y, h=280, pose="stand", ex="n", coat="brown", hd=True, flip=False, **k):
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k)
    if hd and not k.get("rot"): c.hood(f, HOODS[coat], flip)
    return f
def bailiff(c, x, y, h=330, pose="stand", ex="n", flip=False, **k): f = c.person(x, y, h, pose, ex, "teal", flip=flip, **k); c.coif(f); return f
def lordp(c, x, y, h=340, pose="stand", ex="n", flip=False, coat="red", **k):
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); u = f["u"]; hx, hy = f["head"]; c.hood(f, NAVY, flip)
    c.line([(hx-.34*u, hy+1.2*u), (hx, hy+1.5*u), (hx+.34*u, hy+1.2*u)], max(4, u*.07), MARI); return f
def king(c, x, y, h=360, pose="stand", ex="n", flip=False, **k): f = c.person(x, y, h, pose, ex, "red", flip=flip, **k); c.crown(f); return f
def monk(c, x, y, h=320, pose="stand", ex="n", flip=False, coat="brown", **k): f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); c.tonsure(f); return f
def justice(c, x, y, h=330, pose="stand", ex="n", flip=False, **k): f = c.person(x, y, h, pose, ex, "slate", flip=flip, **k); c.coif(f); return f
def scholar(c, x, y, h=320, pose="stand", ex="n", coat="slate", flip=False, **k): f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); c.glasses(f); return f
def reaperf(c, x, y, h=330, pose="hold", ex="n", flip=False, tool=True, **k):
    f = c.person(x, y, h, pose, ex, "green", flip=flip, **k); c.strawhat(f)
    if tool: c.sickle(f["hand"][0]+(-10 if flip else 10), f["hand"][1]+34, h/300, flip)
    return f
def icon(c, x, y, col=TEAL, k=1.0):
    c.line([(x, y+18*k), (x, y+52*k)], 22*k, INK, False); c.line([(x, y+18*k), (x, y+52*k)], 14*k, col, False); c.ell(x-20*k, y-24*k, x+20*k, y+14*k, PAPER, INK, 5*k)
def mhouse(c, x, y, k=1.0, col=FLINT, roof=(166, 98, 78)):
    c.poly([(x-120*k, y-110*k), (x-90*k, y-170*k), (x+90*k, y-170*k), (x+120*k, y-110*k)], roof, INK, 5); c.rect(x-110*k, y-110*k, x+110*k, y, col, INK, 5); c.rect(x-18*k, y-66*k, x+18*k, y, (84, 60, 46), INK, 4, 8)
    for dx in (-66, 66): c.rect(x+(dx-14)*k, y-84*k, x+(dx+14)*k, y-40*k, GLASSD, INK, 4)
def bigcrown(c, x, y, k=1.0, col=MARI):
    c.poly([(x-200*k, y+90*k), (x-230*k, y-110*k), (x-110*k, y-10*k), (x, y-150*k), (x+110*k, y-10*k), (x+230*k, y-110*k), (x+200*k, y+90*k)], col, INK, 9)
    for dx, dy in ((-230, -110), (0, -150), (230, -110)): c.ell(x+dx*k-26*k, y+dy*k-30*k, x+dx*k+26*k, y+dy*k+22*k, RED, INK, 6)
    c.rect(x-200*k, y+50*k, x+200*k, y+100*k, col, INK, 8, 6)
def squig(c, x, y, n=9, seed=0, col=(110, 90, 70), w=5): c.line([(x+j*26, y+7*math.sin(j*1.9+seed)) for j in range(n)], w, col)
def typed(t, key, d=1.0, t0=.1):
    n = int(len(t)*app(key, d, t0)+.999); return t[:n] if n else " "
def fallp(c, n=30, r=22, y1=H, seed=0, x0=0, x1=W):
    """Pennies falling down the screen between x0 and x1 (loops)."""
    for i in range(n):
        j = i+seed*17; sp = 380+(j*53) % 240; x = x0+(j*211+(j*j*7) % 97) % (x1-x0); y = (((j*173) % 1000)/1000*y1+T.TT*sp) % y1; c.penny(x, y, r)
# ================= cold open =================
VX = [520, 760, 1000, 1240, 1480, 1720]
def cold(k):
    q = app("half", .5, .5) if k else 0; on = q > .5; c = vill("day", dead=(1, 3) if on else ())
    for i, x in enumerate(VX):
        if on and i in (1, 3, 4): c.grave(x, 990+(i % 2)*24, min(1, (q-.5)*2+.05))
        else: peasant(c, x, 990+(i % 2)*24, 250, "stand", "sad" if k else ("smile", "n", "joy", "n", "smile", "n")[i], COATS[i % 5], flip=i % 2 == 1)
    sidp(c, 250, 1010, 320, "drop" if k else "stand", "sad" if k else "n")
    if k: dimc(c, 70*q); L(c, "ABOUT HALF YOUR VILLAGE IS DEAD", 150, 1100, 70)
    hud(c, "1349"); return c
def boss(k):
    c = field("day"); c.wheat(0, W, 760, 150, T.TT, 26); c.wheat(10, W, 850, 170, T.TT+1, 28, seed=3)
    bailiff(c, 1340, 1020, 350, "shrug" if k == 0 else "hold", "worry", flip=True); sidp(c, 520, 1020, 350, "stand" if k == 0 else "chin", "n" if k == 0 else "smug")
    if k == 0: L(c, "A HARVEST. NOBODY TO BRING IT IN.", 130, size=66)
    if k == 1: c.bubble(1340, 400, "PLEASE?", 90, (0, 60)); L(c, "YOUR BOSS NEEDS YOU", 130, 520, 70, bg=MARI)
    return c
def ask(k):
    c = C((232, 226, 200)); c.rect(0, 900, W, H, PATH, None); c.line([(0, 900), (W, 900)], 6, INK, False)
    if k == 0:
        s = sidp(c, 640, 1000, 440, "hold", "smug"); c.bubble(1240, 330, "MORE.", 150, (-260, 110)); c.penny(s["hand"][0]+50, s["hand"][1]-40-abs(math.sin(T.TT*5))*50, 34); return c
    sidp(c, 260, 1000, 340, "hold", "smug")
    for i in range(6): peasant(c, lerp(2200+i*120, 560+i*220, app(("ask", i), .6, i*.14)), 990+(i % 2)*34, 290, "hold", ("smug", "smile", "det", "smug", "n", "smile")[i], COATS[i % 5])
    L(c, "SO DO PLENTY OF OTHERS", 170, size=88, bg=MARI); return c
def kingroll(c, lines, key, x0=1020, x1=1700, d=.8):
    """A roll unrolling beside the king; lines = [(text, size, colour)] appear as it opens."""
    q = app(key, d, .2); y1 = 250+100*len(lines)*q+90*q; c.roll(x0, 190, x1, max(262, y1))
    for i, (t, sz, col) in enumerate(lines):
        if q > (i+1)/(len(lines)+.4): c.text((x0+x1)/2, 320+i*110, t, sz, col)
def court(c):
    c.rect(0, 800, W, 1000, (170, 60, 50), None); c.line([(0, 800), (W, 800)], 5, INK, False); c.line([(0, 1000), (W, 1000)], 5, INK, False); c.pennon(150, 780, 560, None, RED, 200, T.TT*2)
def kingban(k=0):
    c = hall(win=False); court(c); king(c, 600, 1010, 430, "point", "angry")
    kingroll(c, [("BY ORDER OF THE KING", 54, INKP), ("PAY: AS IN 1346", 84, INK), ("AND NO MORE", 84, RED)], "ban"); L(c, "JUNE 1349", 150, 600, 76); return c
def question(k):
    c = C(); c.pennies(250, 420, 8, 44, 4, 104); sidp(c, 960, 1010, 380, "shrug", "worry"); king(c, 1560, 1010, 380, "stand", "angry", flip=True)
    c.text(960, 380, "?", 250*(.8+.2*app("qm", .3)), RED)
    if k: L(c, "DO YOU ACTUALLY GET YOUR RAISE?", 130, size=74, bg=MARI)
    return c
def intro(k=0):
    c = C(); s = c.fig(W/2, 900-(1-T.ease(T.LT/0.3))*900, 520, "drop" if T.LT < .5 else "self", "wow" if T.LT < .5 else "smile", "modern"); c.marker(s["head"][0]+20, s["head"][1]-110, 46)
    if T.LT > .6: L(c, "YOU", 160, 1400, 120)
    return c
def team(c, x, moving=True, k=1.1):
    """Sid behind the plough and a pair of oxen; x = the ploughshare, k = size."""
    r = k/1.1; st = T.TT*8 if moving else 0; c.line([(-20, 978), (x-40*r, 978)], 20, (140, 100, 72), False)
    c.ox(x+650*r, 900, 1.1*k, step=st+1.5); c.ox(x+450*r, 968, 1.2*k, step=st); hd, bm = c.plough(x, 972, k); c.line([bm, (x+350*r, 972-120*r)], 7, TIMBER)
    return sidp(c, x-300*r, 1012, 340*r, ("walk" if step() else "hold") if moving else "hold", "det")
def ploughing(k):
    c = field("day"); mv = k == 0 and T.GP < .96; x = lerp(360, 760, T.ease(T.GP)) if k == 0 else (760 if k == 1 else 330); team(c, x, mv, 1.1 if k < 2 else .82)
    if k == 1: L(c, "AGE 22. PLOUGHMAN. SOUTHERN ENGLAND.", 130, size=62)
    hud(c, "1349") if k < 2 else None; return c
def qfield(shown, done=0): return Q(ploughing(2), shown, done)
def hiddenq(k, done=0):
    c = C(); c.questlog(ROWS, 4, done, None, x=545, y=200)
    if k: c.marker(470, 800, 36)
    return c

# ================= before the plague =================
def worth(k=0):
    c = vill("day"); hud(c, "BEFORE THE PLAGUE"); s = sidp(c, 760, 1010, 400, "shrug", "bored"); q = app("tag", .3, .4)
    if q > 0: c.line([(s["head"][0]+70, s["head"][1]+250), (1150, 600)], 5); c.pricetag(1270, 600, 1.7*q, "NOT MUCH")
    return c
def crowd(k):
    if k == 2:
        c = C(); c.rect(360, 560, 1560, 760, (176, 200, 120), INK, 7, 8)
        for i in range(5): c.line([(360+i*240+120, 566), (360+i*240+120, 754)], 4, (140, 168, 96), False)
        for i in range(14): x = 420+i*82; icon(c, x, 470+10*math.sin(T.TT*5+i*1.3), (TEAL, MARI, EARTH)[i % 3], 1.5)
        for d in (-1, 1): arrow(c, 960+d*760, 660, 960+d*(640+20*math.sin(T.TT*4)), 660, RED, 16, 44)
        L(c, "NOT ENOUGH LAND", 220, size=110, bg=MARI); return c
    c = field("day"); m = int(72*app("cr", 1.3, .1)+.5)
    for i in range(m): col, row = i % 18, i//18; icon(c, 110+col*100+(row % 2)*46, 660+row*112, (TEAL, MARI, EARTH, PINK)[(i*7) % 4], 1.25)
    if k == 0: L(c, "\"HORRENDOUSLY OVERPOPULATED\"", 150, size=80); L(c, "ONE HISTORIAN, ON BRITAIN IN THE EARLY 1300s", 300, size=44, bg=MARI)
    if k == 1: L(c, "PLENTY OF HANDS", 170, size=110)
    return c
def hired(k=0):
    c = hall(win=False); table(c, 1040, 1740); bailiff(c, 1400, 1010, 350, "write", "n", flip=True); sidp(c, 620, 1010, 350, "stand", "n"); q = app("yr", 1.2, .2)
    for i in range(12): on = i < int(12*q+.5); c.rect(320+i*108, 190, 320+i*108+94, 290, MARI if on else WHITE, INK, 5, 8); c.text(367+i*108, 236, str(i+1), 50, INK if on else (190, 184, 172))
    L(c, "HIRED BY THE YEAR", 400, 960, 84); return c
def paykind(k):
    c = C((232, 226, 200)); c.rect(0, 880, W, H, PATH, None); c.line([(0, 880), (W, 880)], 6, INK, False)
    for i in range(4):
        q = app(("sk", i), .3, .12*i)
        if q > 0: c.sack(300+i*240, 880-(1-q)*600, 1.7)
    L(c, "MOST OF YOUR PAY: GRAIN", 170, 660, 76)
    if k == 1: c.pennies(1420, 660, 9, 34, 3, 84); L(c, "COIN: ABOUT A FIFTH", 500, 1500, 60, bg=MARI)
    return c
def coins(k):
    c = C(); q = app(("cn", min(k, 1)), 1.0, .1); n = int(60*q+.5) if k == 0 else 60+int(60*q+.5)
    c.pennies(170, 340, n, 22, 20, 53); c.text(1560, 400, str(n//12), 300, RED); c.text(1560, 610, "SHILLINGS", 90); c.text(1560, 700, "= "+str(n)+" PENNIES", 54, FAINT)
    c.text(690, 230, "THE COIN PART OF YOUR PAY. IT VARIED.", 54, FAINT)
    if k == 2: L(c, "A YEAR", 860, 1560, 120, bg=MARI)
    return c
def money(k):
    c = C(); c.pennies(250, 280, 12, 30, 12, 74); c.text(1206, 276, "=", 110); c.rect(1310, 216, 1710, 340, MARI, INK, 7, 16); c.text(1510, 274, "1 SHILLING", 72); c.text(657, 372, "12 PENNIES", 54, FAINT)
    if k >= 1:
        q = app("sh", .9, .1); m = int(20*q+.5)
        for i in range(m): x = 250+(i % 10)*98; y = 520+(i//10)*104; c.rect(x-42, y-42, x+42, y+42, MARI, INK, 5, 10); c.text(x, y-3, "1s", 46)
        if q >= 1: c.text(1236, 568, "=", 110); c.rect(1310, 510, 1710, 634, TEAL, INK, 7, 16); c.text(1510, 568, "1 POUND", 72, PAPER); c.text(691, 716, "20 SHILLINGS", 54, FAINT)
    if k == 2: c.strike(1330, 568, 1690, 12); L(c, "YOU WON'T BE NEEDING THAT WORD", 900, 760, 56, bg=MARI)
    sidp(c, 1510, 1056, 300, ("up", "chin", "shrug")[k], ("n", "n", "bored")[k]); return c
def villein(k):
    c = vill("day"); hud(c, "BEFORE THE PLAGUE")
    for i, x in enumerate((420, 700, 980, 1260, 1540)):
        f = peasant(c, x, 1000+(i % 2)*24, 290, "stand", ("n", "sad", "n", "sad", "smile")[i], COATS[i])
        if i in (1, 3):
            q = app(("vt", i), .25, .3+i*.12)
            if q > 0: chip(c, x, f["head"][1]-56, "VILLEIN", NAVY, 44*q+1)
    if k == 1: L(c, "NOT FREE", 170, size=110, bg=MARI)
    return c
def week(k):
    c = field("day")
    for i in range(7):
        x = 130+i*212; lord = i < 2 or (i == 2 and k == 1); on = lord and (app(("wk", i), .3, .2+i*.3) > .5 if i < 2 else app("wk3", .3, .2) > .5)
        c.rect(x, 110, x+196, 300, TEAL if on else WHITE, INK, 7, 14); c.text(x+98, 166, "DAY "+str(i+1), 56, PAPER if on else INK)
        if on: c.text(x+98, 244, "LORD'S" if i < 2 else "MAYBE", 52, PAPER)
    x = lerp(240, 980, T.ease(T.GP)); c.line([(-20, 984), (x-30, 984)], 20, (140, 100, 72), False); c.ox(x+470, 976, 1.2, step=T.TT*8); hd, bm = c.plough(x, 980, 1.1); c.line([bm, (x+370, 860)], 7, TIMBER)
    peasant(c, x-300, 1016, 330, "walk" if step() else "hold", "strain", "green"); L(c, "2 OR 3 DAYS A WEEK ON THE LORD'S OWN FIELDS", 430, size=56); return c
def rules(k):
    c = meadow("day", road=True)
    if k == 0:
        c.manor(1280, 780, 560, 250); x = lerp(260, 820, app("lv", 1.0, .1)); st = x >= 815
        peasant(c, x, 1000, 330, "stand" if st else ("walk" if step() else "stand"), "worry" if st else "n", "green"); bailiff(c, 1180, 1000, 340, "point", "angry", flip=True)
        if st: c.redx(1000, 640, 70, 20)
        L(c, "USUALLY HE CAN'T LEGALLY LEAVE", 150, 800, 66); return c
    lordp(c, 380, 1000, 350, "hold", "smug"); f = peasant(c, 760, 1000, 320, "hold", "sad", "green", flip=True); c.penny(lerp(f["hand"][0], 520, app("pay", .6, .5)), f["hand"][1]-10-60*math.sin(app("pay", .6, .5)*math.pi), 30)
    if k == 1:
        x = lerp(1100, 1560, T.ease(T.LP)); peasant(c, x, 990, 300, "walk" if step() else "stand", "joy", "rose", hd=False); peasant(c, x+150, 990, 310, "walk" if step() else "stand", "smile", "blue")
        L(c, "DAUGHTER MARRIES OFF THE MANOR: A FINE", 150, size=60)
    if k == 2: c.grave(1380, 960, 1.6); L(c, "HE DIES: HIS HEIR PAYS TO INHERIT", 150, size=64, bg=MARI)
    return c

# ================= the plague arrives =================
def boaticon(c, x, y, k=1.0):
    c.poly([(x-44*k, y-12*k), (x+44*k, y-12*k), (x+30*k, y+14*k), (x-30*k, y+14*k)], WOOD, INK, 5); c.line([(x, y-12*k), (x, y-70*k)], 6, TIMBER); c.poly([(x-26*k, y-66*k), (x+26*k, y-66*k), (x+22*k, y-22*k), (x-22*k, y-22*k)], PAPER, INK, 4)
def harbour(kind="day"):
    c = C(SEA); sky(c, 520, kind); hills(c, 520); c.rect(0, 520, W, H, SEA, None); c.line([(0, 520), (W, 520)], 5, INK, False)
    for i in range(12): x = (i*263+T.TT*24) % (W+100)-50; y = 600+(i*97) % 440; c.line([(x, y), (x+60, y)], 5, WHITE, False)
    c.cottage(1340, 760, 290, 210); c.cottage(1650, 760, 270, 200); c.rect(1180, 760, W, H, (196, 176, 144), INK, 6)
    for i in range(4): c.rect(1180+i*200, 760, 1210+i*200, 1000, TIMBER, INK, 5)
    return c
def ship(k):
    if k == 0:
        c, P = emap(dots=(("DORSET", "DORSET", 200, 70),)); x1, y1 = P["DORSET"]; q = T.ease(T.LP*1.1); x = lerp(760, x1, q); y = lerp(1100, y1+34, q)
        for i in range(int(10*q)): c.ell(lerp(760, x1, i/10)-5, lerp(1100, y1+34, i/10)-5, lerp(760, x1, i/10)+5, lerp(1100, y1+34, i/10)+5, INK, None)
        boaticon(c, x, y, 1.1); L(c, "A SHIP FROM GASCONY", 560, 1580, 48); L(c, "ONE CHRONICLE'S ACCOUNT", 670, 1580, 40, bg=MARI); hud(c, "JUNE 1348"); return c
    c = harbour(); q = T.ease(T.LP*1.15); c.cog(lerp(-200, 860, q), 800, 560, bob=T.TT*2, furl=max(0, (q-.6)/.4)); hud(c, "JUNE 1348"); L(c, "A PORT IN DORSET", 150, 1000, 76); return c
def sailor(k):
    if k == 1:
        c, P = emap(dots=(("DORSET", "DORSET", -40, 120), ("BRISTOL", "BRISTOL?", -190, -30), ("SOUTHAMPTON", "SOUTHAMPTON?", 250, 110))); L(c, "OTHER CHRONICLES: OTHER PORTS", 150, 1420, 50, bg=MARI); hud(c, "1348"); return c
    c = harbour(); c.cog(860, 800, 560, bob=T.TT*2, furl=1); c.line([(1040, 760), (1200, 760)], 12, TIMBER); x = lerp(1040, 1280, T.ease(T.LP))
    for i in range(7): a = T.TT*2+i*.9; r = 12+6*math.sin(T.TT*3+i); c.da.ellipse([(x+100*math.cos(a)-r)*S, (600+130*math.sin(a*1.3)-r)*S, (x+100*math.cos(a)+r)*S, (600+130*math.sin(a*1.3)+r)*S], fill=(90, 110, 70, 150))
    f = c.person(x, 772, 230, "walk" if step() else "stand", "pain", "blue"); c.hat(f, "cap", (70, 80, 110)); peasant(c, 1600, 800, 210, "wave", "smile", "rose", flip=True)
    hud(c, "JUNE 1348"); L(c, "A SAILOR BRINGS THE SICKNESS ASHORE", 150, 1000, 60); return c
SPR = [(320, 800, 0), (400, 760, .1), (330, 700, .13), (250, 760, .16), (470, 740, .2), (535, 705, .28), (590, 740, .31), (160, 800, .34), (450, 640, .36), (560, 640, .4), (380, 600, .44), (250, 650, .5), (620, 600, .5),
       (480, 540, .54), (590, 540, .57), (190, 580, .6), (90, 850, .6), (420, 460, .65), (300, 460, .68), (510, 430, .72), (460, 330, .8), (320, 340, .82), (440, 230, .9), (290, 230, .92), (410, 110, .97), (300, 90, .99)]
def blot(c, g):
    for x, y, t in SPR:
        if t <= g: r = 78*min(1, (g-t)/.08+.15); cx, cy = 560+x*1.08, 60+y*1.08; c.da.ellipse([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], fill=(70, 44, 80, 150))
def spread(k):
    g = lerp(0, .3, T.ease(T.LP)) if k == 0 else (lerp(.3, .86, T.ease(T.LP)) if k == 1 else lerp(.86, 1.01, T.ease(T.LP*1.4)))
    c, P = emap(dots=(("LONDON", "LONDON: BY NOVEMBER", 290, -30),) if k == 0 else ()); blot(c, g)
    if k == 1: c.label(P["NORTH"][0]+330, P["NORTH"][1], "THE NORTH: NEXT SUMMER", 46, bg=MARI)
    if k == 2: c.rect(1290, 270, 1840, 800, PAPER, INK, 7, 22); c.text(1560, 430, str(int(500*T.ease(T.LP*1.3))), 260, RED); c.text(1560, 620, "DAYS", 110); c.text(1560, 720, "(ABOUT)", 54, FAINT); L(c, "TO CROSS THE COUNTRY", 900, 1565, 50)
    hud(c, "1348" if k == 0 else "1349"); return c
def desk(c, x=1100, y=800):
    c.poly([(x-200, y-170), (x+200, y-230), (x+200, y-200), (x-200, y-140)], WOOD, INK, 6); c.line([(x-150, y-150), (x-150, y)], 16, TIMBER, False); c.line([(x+150, y-200), (x+150, y)], 16, TIMBER, False)
    c.poly([(x-150, y-196), (x+150, y-240), (x+150, y-214), (x-150, y-170)], PARCH, INK, 4)
def knighton(k):
    if k == 0:
        c = hall("day"); desk(c, 1040, 800); monk(c, 700, 1000, 360, "write", "det"); c.jug(1500, 780, .7, (60, 56, 60)); L(c, "KNIGHTON, A CHRONICLER", 150, 760, 70); return c
    c = cotin("night"); pallet(c); c.person(1000, 664, 300, "stand", "pain", "brown", rot=-90); n = min(3, int(T.LP*3.6)+1)
    for i in range(3): c.rect(500+i*240, 180, 500+i*240+200, 330, RED if i < n else WHITE, INK, 7, 14); c.text(600+i*240, 252, "DAY "+str(i+1), 60, PAPER if i < n else INK)
    L(c, "FEW LASTED MORE THAN 2 OR 3 DAYS IN BED", 450, 840, 56, bg=MARI); return c
def toll(k):
    c = C(); x0, x1, y = 260, 1660, 560; c.rect(x0, y-60, x1, y+60, WHITE, INK, 7, 12); xa = x0+(x1-x0)*.4; xb = x0+(x1-x0)*.6
    for p in (0, 20, 40, 60, 80, 100): x = x0+(x1-x0)*p/100; c.line([(x, y+60), (x, y+92)], 6); c.text(x, y+136, str(p)+"%", 52)
    if k == 0: c.text(960, 290, "?", 300*(.8+.2*app("q", .3)), RED); L(c, "NOBODY KNOWS THE TOLL", 870, size=84)
    if k >= 1: q = app("band", .7, .1); c.rect(xa, y-60, xa+(xb-xa)*q, y+60, RED, INK, 7); L(c, "40 TO 60 PERCENT: THE RANGE YOU'LL HEAR MOST", 300, size=58)
    if k == 2:
        qa = app("lo", .3, .2); qb = app("hi", .3, 1.5)
        if qa > 0: arrow(c, xa-24, y, xa-24-250*qa, y, NAVY, 16, 40); c.label(x0+(x1-x0)*.2, 860, "SOME HISTORIANS: LESS", 52)
        if qb > 0: arrow(c, xb+24, y, xb+24+110*qb, y, NAVY, 16, 40); c.label(x0+(x1-x0)*.76, 860, "ONE: MORE", 52, bg=MARI)
    c.text(960, 1020, "SHARE OF PEOPLE IN ENGLAND WHO DIED, 1348-49 (ESTIMATES)", 50, FAINT); return c
def sick(k):
    c = cotin("night" if k == 0 else "dawn"); pallet(c)
    if k == 0: c.fig(1000, 664, 300, "stand", "pain", "modern", rot=-90); dimc(c, 90); L(c, "THEN YOU GET IT", 200, 800, 96); hud(c, "1349"); return c
    if k == 1: sidp(c, 860, 712, 300, "stand", "bored", sit=True); L(c, "SOMETHING THE STORY USUALLY SKIPS", 200, 840, 60)
    if k == 2: sidp(c, 860, 712, 300, "up", "smile", sit=True); L(c, "SOME PEOPLE RECOVERED", 200, 840, 88, bg=MARI)
    hud(c, "1349"); return c
NAMED = {0: ("HENRY BROUN", "1 WEEK"), 5: ("JOHN DERWORTH", "9 WEEKS"), 14: ("AGNES MOLD", "9 WEEKS")}
def sicklist(k):
    if k == 0: c, P = emap(dots=(("WARBOYS", "WARBOYS, HUNTINGDONSHIRE", 420, -10),)); hud(c, "1349"); return c
    if k == 1:
        c = hall("day"); desk(c, 1040, 800); monk(c, 700, 1000, 360, "write", "n", coat="banker"); monk(c, 1640, 1000, 330, "chin", "worry", flip=True, coat="banker"); c.roll(1180, 560, 1300, 600, 12); c.roll(1210, 520, 1330, 560, 12); L(c, "THE MONKS OF RAMSEY ABBEY KEEP A LIST", 150, size=60); return c
    c = parch("TOO SICK TO WORK. WARBOYS, 1349." if k == 2 else None, 60); n = 22 if k >= 3 else int(22*app("sl", 2.2, .1)+.5)
    for i in range(n):
        x = 340+(i//11)*680; y = 286+(i % 11)*58
        if i in NAMED: c.text(x, y, NAMED[i][0], 42, INK, "lm"); c.text(x+400, y, NAMED[i][1], 42, RED, "lm")
        else: squig(c, x, y, 8+(i*7) % 4, i); squig(c, x+400, y, 3+(i*5) % 3, i+3, (150, 70, 60))
    if k == 3: L(c, "22 NAMES, AND HOW LONG EACH WAS GONE", 196, size=52, bg=MARI)
    if k == 4: L(c, "A LIST OF SURVIVORS", 196, size=70, bg=MARI)
    return c
def backwork(k=0):
    c = field("day"); c.wheat(1100, W, 760, 160, T.TT, 26); c.wheat(1060, W, 900, 180, T.TT+1, 28, seed=2); q = T.ease(T.LP*1.1)
    for i in range(3): peasant(c, lerp(300+i*190, 760+i*190, q), 1000+(i % 2)*26, 300, ("walk" if step() else "stand") if q < .98 else "stand", "smile", COATS[i])
    peasant(c, 160, 1010, 300, "stand", "pain", "slate"); L(c, "3 OUT OF 4: BACK AT WORK INSIDE A MONTH", 150, size=62); return c
def sickleave(k):
    c = C(); x0, x1 = 240, 1680; q = app("yl", .9, .1); c.rect(x0, 380, x1, 520, WHITE, INK, 7, 12); c.rect(x0, 380, x0+(x1-x0)*q, 520, MARI, INK, 7, 12); c.text(960, 290, "ALLOWED OFF SICK: UP TO A YEAR AND A DAY", 70)
    if k == 0: peasant(c, 1300, 1040, 320, "stand", "pain", "brown")
    if k == 1:
        w = (x1-x0)*7/366; c.rect(x0, 380, x0+w, 520, RED, INK, 6); arrow(c, x0+w/2+150, 700, x0+w/2+14, 540, RED, 12, 34); L(c, "HENRY BROUN TOOK ONE WEEK", 760, 760, 70, bg=MARI); peasant(c, lerp(1300, 1560, T.ease(T.LP)), 1040, 320, "walk" if step() else "stand", "det", "brown")
    return c
def graves(k=0):
    c = meadow("grey", 520); c.church(1280, 760, 1.0)
    for i in range(14): c.grave(170+(i % 7)*150+(i//7)*60, 840+(i//7)*150, 1.0)
    dimc(c, 50); L(c, "IT DOESN'T COUNT THE ONES WHO NEVER CAME BACK", 150, size=56); return c
def lucky(k=0):
    c = vill("day", dead=(1, 3)); sidp(c, 520, 1010, 350, "cheer", "smile"); Q(c, 4, 1); return c

# ================= after the plague: the raise =================
def around(k=0):
    c = vill("day", dead=(1, 3, 4)); c.grave(760, 960, 1.1); c.grave(1500, 990, 1.1); c.grave(1180, 940, 1.0); sidp(c, 400, 1010, 350, "chin", "sad"); hud(c, "1349"); return c
def strays(k):
    c = field("day"); c.wheat(0, W, 700, 130, T.TT, 26, seed=1); c.ox((T.TT*34+900) % (W+500)-250, 770, 1.0, step=T.TT*6)
    for i in range(4): c.sheep((300+i*470+T.TT*52) % (W+300)-150, 940+(i % 2)*60, 1.25, step=T.TT*7+i)
    c.wheat(0, W, 1070, 150, T.TT+1, 30, seed=5)
    if k == 0: L(c, "KNIGHTON: SHEEP AND CATTLE IN THE CROPS", 150, size=60)
    if k == 1: L(c, "NOBODY TO DRIVE THEM OFF", 150, size=80, bg=MARI)
    return c
def horsep(k):
    c = vill("day", dead=(1, 3, 4)); c.horse(640, 1030, 1.2, step=0); c.line([(880, 640), (1130, 590)], 5); c.pricetag(1260, 580, 1.8, "40s")
    if k == 1:
        c.strike(1110, 580, 1420, 12); q = app("np", .3, .5)
        if q > 0: c.pricetag(1340, 800, 1.9*q, "6s 8d", MARI)
    L(c, "A HORSE WORTH 40 SHILLINGS" if k == 0 else "SELLS FOR 6 SHILLINGS AND 8 PENCE", 150, 1100, 60, bg=PAPER if k == 0 else MARI); return c
def rot(k):
    c = field("grey"); d = T.ease(T.GP)
    for j, y in enumerate((640, 760, 890, 1030)): c.wheat(-10, W, y, 110+j*24, T.TT*(1-d), 24+j*3, droop=d, seed=j)
    L(c, "CROPS PERISH IN THE FIELDS" if k == 0 else "NOBODY TO GATHER THEM", 150, size=76, bg=PAPER if k == 0 else MARI); return c
def lack(k):
    c = meadow("day"); c.manor(1000, 800, 800, 320); c.rect(0, 800, W, H, PATH, None); c.line([(0, 800), (W, 800)], 5, INK, False); c.scythe(330, 960, 1.0, 74); c.pitchfork(1320, 1040, .9, -80)
    f = lordp(c, 640, 1010, 380, "shrug", "worry")
    for i in range(3): c.text(f["head"][0]-170+i*170, f["head"][1]-90-24*abs(math.sin(T.TT*3+i)), "?", 110, RED)
    L(c, "SUCH A LACK OF SERVANTS" if k == 0 else "NO ONE KNOWS WHAT TO DO", 150, 1250, 66, bg=PAPER if k == 0 else MARI); return c
def youknow(k=0):
    c = field("day"); c.wheat(0, W, 760, 150, T.TT, 26); sidp(c, 960, 1070, 520, "chin", "smug"); L(c, "YOU KNOW EXACTLY WHAT TO DO", 130, size=76, bg=MARI); return c
def q2(k=0):
    c = field("day"); c.wheat(0, W, 760, 150, T.TT, 26); sidp(c, 520, 1020, 360, "point", "det"); Q(c, 4, 1); return c
def reaper(k):
    c = field("day"); c.wheat(0, W, 700, 150, T.TT, 26); c.wheat(10, W, 800, 160, T.TT+1, 28, seed=2); reaperf(c, 420, 1020, 350, "hold", "smug"); lordp(c, 1500, 1020, 350, "hold", "worry", flip=True)
    c.rect(640, 240, 1280, 560, PAPER, INK, 8, 22); n = int(8*app("r8", 1.2, .3)+.5)
    for i in range(n): c.penny(712+i*72, 470, 30)
    c.text(960, 340, str(n)+"d", 150, RED)
    if k == 0: L(c, "AUTUMN: NO REAPER FOR LESS THAN 8 PENCE", 110, size=58)
    if k == 1: c.loaf(1130, 372, 1.0); c.jug(1218, 392, .58); L(c, "PLUS HIS FOOD", 110, size=90, bg=MARI)
    return c
def eight(k=0):
    c = C(MARI)
    for i in range(8): c.penny(330+i*180, 720+24*math.sin(T.TT*4+i*.8), 70)
    c.text(960, 380, "8d", 420, INK); L(c, "REMEMBER THAT NUMBER", 930, size=70); return c
def rate(k):
    c = C(); c.text(960, 110, "AVERAGE DAY RATE IN ONE SAMPLE OF MANOR ACCOUNTS", 58, FAINT); c.line([(300, 880), (1620, 880)], 7); q = app("b1", .6, .1)
    c.rect(520, 880-200*q, 800, 880, TEAL, INK, 7, 6); c.text(660, 950, "1349", 76)
    if q >= 1: c.text(660, 620, "ABOUT 1.5d", 80)
    if k >= 1:
        q2 = app("b2", .8, .1); c.rect(1120, 880-400*q2, 1400, 880, RED, INK, 7, 6); c.text(1260, 950, "1350", 76)
        if q2 >= 1: c.text(1260, 410, "3d", 120, RED)
    if k == 2: arrow(c, 850, 700, 1090, 540, INK, 14, 40); L(c, "IN A SINGLE YEAR", 280, 620, 84, bg=MARI)
    return c
def suffolk(k):
    if k <= 1:
        c = field("day"); hud(c, "1349")
        for i in range(5): c.sheaf(150+i*165, 820+(i % 2)*130, 1.05)
        c.wheat(990, W, 760, 160, T.TT, 26); c.wheat(960, W, 900, 180, T.TT+1, 28, seed=3); c.wheat(1000, W, 1050, 190, T.TT, 30, seed=4); c.pricetag(470, 600, 2.5, "3d AN ACRE")
        if k == 1:
            q = app("p5", .3, .2)
            if q > 0: c.pricetag(1420, 600, 2.5*q, "5d AN ACRE", MARI)
        L(c, "FORNHAM ALL SAINTS, SUFFOLK", 150, 1000, 60); return c
    c = C((232, 226, 200)); c.rect(0, 900, W, H, PATH, None); c.line([(0, 900), (W, 900)], 6, INK, False); f = reaperf(c, 620, 1010, 420, "hold", "joy", tool=False); hx, hy = f["hand"]; r = 24 if k == 2 else 40
    for i in range(5): t = (T.TT*.9+i*.2) % 1; c.penny(hx+50+30*math.sin(i*2.1), hy-30-520*(1-t), r)
    c.pennies(hx+10, hy+6, 3, r*.8, 3, r*1.5); L(c, "MORE TIPS" if k == 2 else "AND BIGGER ONES", 220, 1380, 110 if k == 2 else 92, bg=PAPER if k == 2 else MARI); return c
def moving(k):
    c = meadow("day", road=True); mhouse(c, 330, 800, 2.4); mhouse(c, 1590, 800, 2.4, (214, 204, 186), (120, 130, 150))
    for i in range(5): peasant(c, (i*440+T.TT*150) % (W+300)-150, 960+(i % 2)*44, 280, "walk" if int(T.TT*5+i) % 2 == 0 else "stand", ("det", "smile", "n")[i % 3], COATS[i])
    if k == 0: L(c, "PEOPLE START MOVING", 150, size=90)
    else: L(c, "IF THIS LORD WON'T PAY, ANOTHER MIGHT", 150, size=62, bg=MARI)
    return c
def rent(k):
    c = vill("day", dead=(3,)); lordp(c, 600, 1010, 360, "up" if k == 0 else "hold", "worry" if k == 0 else "smile"); peasant(c, 1240, 1010, 330, ("walk" if step() else "stand") if k == 0 else "stand", "det" if k == 0 else "smile", "green", flip=k == 1)
    c.pricetag(930, 560, 1.8, "RENT")
    if k == 0: c.bubble(470, 330, "WAIT!", 96, (60, 70))
    if k == 1: c.strike(780, 560, 1090, 12); L(c, "KNIGHTON: LORDS LET TENANTS OFF THEIR RENT", 150, size=58, bg=MARI)
    return c
def tohall(k):
    c = hall(); bailiff(c, 1680, 910, 340, "write" if k == 0 else "shrug", "n" if k == 0 else "wow", flip=True); table(c, 1120, 1840); c.roll(1180, 664, 1360, 742, 14); c.pennies(1440, 720, 4, 20, 4, 44)
    x = lerp(-200, 620, app("in", 1.1, .1)) if k == 0 else 620; s = sidp(c, x, 1010, 360, ("walk" if step() else "stand") if x < 615 else ("stand" if k == 0 else "hold"), "det" if k == 0 else "smug")
    if k == 1:
        c.bubble(700, 330, "               ", 96, (-40, 80))
        for i in range(5): c.penny(540+i*80, 330, 32*app(("bp", i), .2, .2+i*.15))
    L(c, "THE BAILIFF" if k == 0 else "YOU NAME A NUMBER", 160, 700, 70, bg=PAPER if k == 0 else MARI); return c
def acct(k):
    """The Kent account roll. k: 0 map, 1 rises, 2 the reason, 3 food, 4 slips back, 5 food slips."""
    if k == 0: c, P = emap(dots=(("MEOPHAM", "MEOPHAM, KENT", 260, 40),)); L(c, "A MANOR'S ACCOUNTS", 150, 1500, 56, bg=MARI); hud(c, "1349"); return c
    c = parch("MEOPHAM, KENT: THE MANOR ACCOUNTS", 56); rows = ["PLOUGHMEN", "CARTER", None]; up = k == 1; dn = k >= 4
    if k == 2:
        c.text(960, 470, typed("\"THE HEAVY MORTALITY", "hm", .8), 96, INKP); c.text(960, 610, typed("OF THAT YEAR\"", "hm2", .6, .9), 96, INKP); L(c, "THE ROLL'S OWN REASON", 840, size=60, bg=MARI); return c
    for i, r in enumerate(rows):
        y = 330+i*110
        if r: c.text(380, y, r, 70, INK, "lm")
        else: squig(c, 380, y, 11, i)
        squig(c, 800, y, 5, i+7, (150, 70, 60))
        if i < 2:
            q = app(("ar", i, k), .3, .3+i*.4)
            if q > 0 and up: arrow(c, 1100, y+32, 1100, y+32-64*q, TEAL, 18, 36)
            if q > 0 and dn: arrow(c, 1100, y-32, 1100, y-32+64*q, RED, 18, 36)
    if k == 1: L(c, "CASH PAY UP ABOUT 10%. MOST FOR THESE TWO.", 860, size=56, bg=MARI)
    if k == 3:
        for i in range(13):
            q = app(("fs", i), .25, .1+(i-10)*.3) if i >= 10 else 1
            if q > 0: c.sack(420+i*90, 900-(1-q)*200, .62, (214, 190, 140) if i < 10 else MARI)
        c.text(960, 690, "FOOD ALLOWANCE: UP NEARLY A THIRD", 64, RED)
    if k >= 4:
        c.text(1380, 350, "BY 1353:", 66); c.text(1380, 440, "SLIPPING BACK", 66, RED)
        if k == 5:
            for i in range(13):
                gone = i >= 11
                if not gone or app("fg", .5, .3) < .5: c.sack(420+i*90, 900, .62, (214, 190, 140) if i < 10 else MARI)
            L(c, "SO HAS MOST OF THE EXTRA FOOD", 690, 960, 56, bg=MARI)
    return c
def easy(k):
    c = hall(win=False); c.sack(790, 1040, 1.0); c.sack(920, 1050, 1.0)
    s = sidp(c, 500, 1010, 360, "cheer" if k == 0 else "stand", "joy" if k == 0 else "worry")
    if k == 0: Q(c, 4, 2); return c
    dimc(c, 120); bigcrown(c, 1320, lerp(-300, 400, app("cr", .45, .15)), 1.5); L(c, "TOO EASY", 800, 1320, 120, bg=MARI); return c
# ================= the law =================
def ordin(k):
    if k == 0:
        c, P = emap(dots=()); blot(c, .62+.06*T.LP); x, y = P["LONDON"]; c.rect(1400, 560, 1800, 880, PAPER, INK, 7, 20); bigcrown(c, 1600, 690, .5); c.text(1600, 810, "THE KING ACTS", 54); arrow(c, 1010, 500, 1010, 380+20*math.sin(T.TT*4), INK, 14, 40)
        c.label(330, 430, "THE PLAGUE IS STILL\nHEADING NORTH", 46); hud(c, "JUNE 1349"); return c
    c = hall(win=False); court(c); king(c, 560, 1010, 430, "hold", "det")
    kingroll(c, [("THE ORDINANCE", 80, INKP), ("OF LABOURERS", 80, INKP)] if k == 1 else [("THE ORDINANCE", 80, INKP), ("OF LABOURERS", 80, INKP), ("JUNE 1349", 70, RED)], "ord"); hud(c, "JUNE 1349"); return c
def ord1(k):
    c = parch("THE ORDINANCE OF LABOURERS, 1349", 60); rows = ["FIT TO WORK", "UNDER 60", "NO LAND OR TRADE TO LIVE ON"]
    for i, r in enumerate(rows):
        if i <= k:
            y = 310+i*120; q = app(("or", i), .3, .1); c.rect(400, y-38, 476, y+38, WHITE, INK, 6, 8); c.text(520, y-4, r, 70, INK, "lm")
            if q > .5: c.tick(438, y, 26)
    if k == 3: z = .7+.3*app("mw", .25, .1); c.rect(960-590*z, 760-80*z, 960+590*z, 760+80*z, RED, INK, 8, 18); c.text(960, 756, "YOU MUST WORK FOR WHOEVER ASKS", 72*z, PAPER)
    return c
def back46(k):
    c = C(); y = 620; c.line([(260, y), (1660, y)], 9); X = [360, 760, 1160, 1560]; c.line([(1160, y), (1560, y)], 22, RED, False); c.text(1360, y-70, "PLAGUE", 60, RED)
    for x, yr in zip(X, (1346, 1347, 1348, 1349)): c.ell(x-20, y-20, x+20, y+20, WHITE, INK, 7); c.text(x, y+86, str(yr), 76)
    sidp(c, 1560, y-34, 230, "shrug", "worry"); q = app("bk", 1.0, .3); pts = [(lerp(1500, 380, t/20*q), y-330-150*math.sin(t/20*q*math.pi)) for t in range(21)]; c.line(pts, 14, TEAL, False)
    if q > .97: arrow(c, 400, y-300, 366, y-80, TEAL, 14, 40); c.pennies(280, y+190, 3, 34, 3, 80); c.text(600, y+190, "THE USUAL PAY IN 1346", 56, INK, "lm")
    L(c, "YOUR PAY: WHATEVER WAS USUAL IN 1346" if k == 0 else "BEFORE THE PLAGUE", 130, size=64, bg=PAPER if k == 0 else MARI); return c
def cell(c): c.rect(0, 0, W, H, (150, 146, 142), None); [c.line([(0, 150+r*190), (W, 150+r*190)], 5, (120, 116, 112), False) for r in range(5)]; [c.line([(140+i*260+(r % 2)*130, 150+r*190), (140+i*260+(r % 2)*130, 340+r*190)], 5, (120, 116, 112), False) for r in range(4) for i in range(8)]
def prison(k):
    c = C(); cell(c); c.rect(560, 150, 1360, 1000, (64, 58, 60), None); sidp(c, 960, 990, 480, "hold" if k == 0 else "drop", "sad"); c.gaol(960, 1000, 760, 800, 6)
    L(c, "REFUSE TO WORK: PRISON" if k == 0 else "LEAVE BEFORE YOUR TERM IS UP: PRISON", 130, size=60, bg=PAPER if k == 0 else MARI); return c
def alms(k):
    c = meadow("day", road=True); c.cottage(1380, 830, 320, 180); f = c.person(1150, 1020, 300, "hold", "sad", "slate", flip=True, sit=True); g = peasant(c, 640, 1000, 330, "hold", "smile", "rose")
    c.penny(lerp(g["hand"][0]+40, 900, .5+.5*math.sin(T.TT*3)), g["hand"][1]-20, 30)
    if k == 1: c.redx(880, 700, 150, 30); L(c, "ALMS TO A BEGGAR WHO COULD WORK: AN OFFENCE", 150, size=56, bg=MARI)
    return c
def ignore(k):
    c = meadow("day", road=True); c.citywall(830, 0, W, 420); c.roll(1370, 440, 1710, 650, 20); c.text(1540, 520, "BY ORDER", 50, INKP); c.text(1540, 584, "OF THE KING", 42, INKP)
    for i in range(4): peasant(c, (i*520+T.TT*170) % (W+300)-150, 1000+(i % 2)*30, 260, "walk" if int(T.TT*5+i) % 2 == 0 else "stand", ("smug", "smile", "bored", "smug")[i], COATS[i])
    if k == 0: L(c, "IT DOESN'T TAKE", 170, 700, 96)
    if k == 1: L(c, "KNIGHTON: \"SO ARROGANT AND HOSTILE\"", 170, 760, 60, bg=MARI)
    if k == 2: L(c, "THEY PAID NO HEED TO THE KING'S COMMAND", 170, 780, 56, bg=MARI)
    return c
def parl(k=0):
    c = hall(win=False); c.pennon(180, 780, 600, None, RED, 200, T.TT*2); c.pennon(1740, 780, 600, None, NAVY, -200, T.TT*2+1)
    for i in range(5): lordp(c, 420+i*270, 900, 300, ("chin", "point", "stand", "point", "chin")[i], ("det", "angry", "n", "angry", "det")[i], flip=i > 2, coat=("red", "blue", "banker", "green", "red")[i])
    c.rect(260, 880, 1660, 930, WOOD, INK, 7, 6); q = app("pl", .9, .2); c.rect(960-560*q, 838, 960+560*q, 890, PARCH, INK, 5)
    for i in range(int(9*q)): squig(c, 960-520*q+i*118*q, 866, 3, i, (150, 70, 60), 4)
    c.rect(260, 930, 1660, 1080, (130, 94, 66), INK, 7); L(c, "PARLIAMENT COMES BACK WITH A PRICE LIST", 180, size=58, bg=MARI); return c
def statute(k):
    if k == 0: c = parch(); c.text(960, 430, typed("THE STATUTE", "st", .5), 150, INKP); c.text(960, 620, typed("OF LABOURERS", "st2", .5, .5), 150, INKP); c.text(960, 800, "1351", 110, RED); return c
    c = C((232, 226, 200)); c.rect(0, 900, W, H, PATH, None); c.line([(0, 900), (W, 900)], 6, INK, False)
    for i in range(4): peasant(c, 300+i*230, 1000+(i % 2)*26, 300, "hold", ("smug", "smile", "det", "smug")[i], COATS[i])
    z = .8+.2*app(("x", k), .25, .1); c.text(1500, 480, "x2" if k == 1 else "x3", 330*z, RED); L(c, "\"DOUBLE OR TREBLE\" THE OLD WAGE, IT COMPLAINS", 150, size=56, bg=MARI if k == 2 else PAPER); return c
PR = [("HAYMAKING", "A DAY", 1, "1d"), ("MOWING", "AN ACRE, OR A DAY", 5, "5d"), ("THRESHING WHEAT", "A QUARTER", 2.5, "2.5d"), ("MASTER CARPENTER", "A DAY", 3, "3d"), ("MASTER MASON", "A DAY", 4, "4d")]
def prices(k):
    c = parch("STATUTE OF LABOURERS, 1351: THE MOST YOU MAY BE PAID", 50)
    for i in range(k+1):
        y = 310+i*130; q = app(("pr", i), .5, .1); nm, det, n, pr = PR[i]; c.text(320, y-18, nm, 66, INK, "lm"); c.text(322, y+38, det, 40, FAINT, "lm"); m = int(n)
        if q > .3:
            for j in range(m): c.penny(960+j*66, y, 29)
            if n % 1: c.halfpenny(960+m*66+6, y, 29)
        if q > .7: c.text(1480, y-4, pr, 104, RED)
    return c
def reap(k):
    c = C(); c.line([(960, 110), (960, 990)], 6, (200, 190, 170), False); reaperf(c, 210, 1030, 300, "hold", "smug" if k == 0 else "angry"); c.text(480, 150, "KNIGHTON'S REAPER", 60); c.pennies(520, 300, 8, 36, 4, 88); c.loaf(640, 560, 1.3); c.jug(790, 560, .7); c.text(690, 640, "8d AND HIS FOOD", 60, RED)
    if k >= 1:
        justice(c, 1750, 1020, 340, "stand", "det", flip=True); c.text(1440, 150, "THE LAW", 60); n = 2 if k == 1 else 2+(1 if app("p3", .2, .5) > 0 else 0); c.pennies(1180, 340, n, 44, 3, 110); c.text(1330, 520, ("2d A DAY" if n == 2 else "3d A DAY"), 96, RED)
        if k == 2: c.label(1300, 700, "3d FROM THE SECOND\nWEEK OF AUGUST", 46, bg=MARI)
    return c
def extras(k):
    c = C((232, 226, 200)); c.rect(0, 760, W, H, WOOD, None); c.line([(0, 760), (W, 760)], 7, INK, False); c.ham(480, 640, 1.9); c.jug(960, 740, 1.5); c.pennies(1380, 620, 3, 46, 3, 110)
    for i, (x, t) in enumerate(((480, "MEAT"), (960, "DRINK"), (1490, "COURTESY"))):
        c.text(x, 880, t, 70, PAPER)
        if i <= k: c.redx(x, 610, 130, 28)
    if k == 2: L(c, "\"WITHOUT MEAT OR DRINK, OR OTHER COURTESY\"", 150, size=60, bg=MARI)
    else: L(c, "NO EXTRAS", 150, size=100)
    return c
def foryou(k):
    c = C(); sidp(c, 420, 1010, 440, "self", "worry"); c.marker(440, 330, 40)
    c.rect(900, 250, 1700, 470, WHITE, INK, 8, 20); c.text(1240, 356, "BY THE YEAR", 96, INK)
    if k >= 1: c.tick(1580, 360, 44)
    if k >= 1: c.rect(900, 560, 1700, 780, WHITE, INK, 8, 20); c.text(1240, 666, "BY THE DAY", 96, FAINT)
    if k == 2: c.redx(1580, 670, 76, 24)
    L(c, "FARM SERVANTS: HOW YOU MAY BE HIRED", 130, 1200, 54, bg=MARI); return c
def town(kind="day"):
    c = C((206, 196, 176)); sky(c, 500, kind)
    for i, (x, w, h) in enumerate(((20, 330, 250), (380, 300, 220), (1250, 310, 240), (1590, 320, 260))): c.cottage(x, 760, w, h)
    c.rect(0, 760, W, H, (200, 190, 170), None); c.line([(0, 760), (W, 760)], 5, INK, False)
    for i in range(14): c.ell((i*163) % W, 800+(i*71) % 250, (i*163) % W+60, 826+(i*71) % 250, (184, 174, 154), None)
    for j in range(3): c.rect(870+j*24, 760-(j+1)*26, 1110-j*24, 760-j*26, FLINT, INK, 5)
    c.rect(978, 460, 1002, 684, FLINT, INK, 5); c.rect(930, 520, 1050, 544, FLINT, INK, 5); return c
def market(k):
    c = town()
    if k <= 1:
        x = lerp(-150, 560, T.ease(T.GP)); s = sidp(c, x, 1020, 360, "up", "det"); c.pitchfork(s["hand"][0], s["hand"][1]+170, .9)
        for i in range(3): peasant(c, 1300+i*190, 1000+(i % 2)*30, 280, "stand", ("n", "bored", "smile")[i], COATS[i+1], flip=True)
        if k == 1: L(c, "TOOLS IN YOUR HAND, INTO TOWN", 150, size=66, bg=MARI)
        return c
    if k == 2:
        s = sidp(c, 700, 1020, 350, "up", "smile"); c.pitchfork(s["hand"][0], s["hand"][1]+170, .9); lordp(c, 1180, 1020, 350, "point", "n", flip=True)
        for i in range(4): peasant(c, 180+i*130 if i < 2 else 1480+(i-2)*170, 1000+(i % 2)*30, 270, "stand", "n", COATS[i], flip=i >= 2)
        L(c, "HIRED IN THE OPEN", 150, size=96); return c
    dimc(c, 90); lordp(c, 760, 1010, 340, "hold", "smug"); peasant(c, 1140, 1010, 330, "hold", "smug", "green", flip=True); c.pennies(900, 700, 3, 28, 3, 64); c.redx(960, 760, 230, 34); L(c, "NO PRIVATE DEALS", 150, size=100, bg=MARI); return c
def oath(k):
    c = town(); s = sidp(c, 640, 1020, 380, "up", "bored"); j = justice(c, 1240, 1020, 380, "hold", "det", flip=True); hx, hy = j["hand"]; c.rect(hx-110, hy-50, hx+20, hy+40, (120, 60, 50), INK, 6, 6); c.rect(hx-100, hy-42, hx+10, hy+32, PARCH, INK, 3, 4)
    if k == 1: L(c, "TWICE A YEAR: AN OATH TO KEEP ALL OF IT", 150, size=60, bg=MARI)
    return c
def stockb(k):
    c = town(); c.stocks(1280, 1030, 1.0, 1-app("sb", .8, .3)); f = peasant(c, 620, 1030, 340, "up" if int(T.TT*4) % 2 == 0 else "hold", "det", "brown", hd=False); c.rect(f["hand"][0]-10, f["hand"][1]-60, f["hand"][0]+60, f["hand"][1]-20, (90, 84, 80), INK, 5)
    L(c, "STOCKS", 150, size=110) if k == 0 else L(c, "TO BE BUILT IN EVERY TOWN", 150, size=76, bg=MARI); return c
def pen(k):
    if k == 0:
        c = town(); sidp(c, 520, 965, 300, "shrug", "sad"); c.stocks(520, 1040, 1.3)
        for dx in (-117, 117): c.ell(520+dx-36, 871-24, 520+dx+36, 871+24, INK, None)
        n = min(3, int(T.LP*3.4)+1)
        for i in range(3): c.rect(790+i*140, 240, 790+i*140+120, 370, RED if i < n else WHITE, INK, 6, 10); c.text(850+i*140, 300, str(i+1), 76, PAPER if i < n else INK)
        L(c, "REFUSE THE OATH: 3 DAYS OR MORE IN THE STOCKS", 130, size=54); return c
    c = C(); cell(c); c.rect(160, 200, 800, 1000, (64, 58, 60), None); sidp(c, 480, 990, 430, "drop", "sad" if k == 1 else "pain"); c.gaol(480, 1000, 600, 760, 6)
    n = int((40 if k == 1 else 90)*app(("tl", k), 1.2, .2)+.5); c.rect(1040, 260, 1720, 760, PAPER, INK, 8, 22); c.text(1380, 430, str(n), 330, RED); c.text(1380, 660, "DAYS", 120)
    L(c, "BREAK THE OATH: 40 DAYS IN PRISON" if k == 1 else "DO IT AGAIN: THREE MONTHS", 130, 1300, 54, bg=PAPER if k == 1 else MARI); return c
def bench(c, n=3, ex=("det", "n", "angry")):
    for i in range(n): justice(c, 660+i*300, 900, 320, ("chin", "write", "stand")[i % 3], ex[i % 3], flip=i == 2)
    c.rect(420, 740, 1500, 800, WOOD, INK, 7, 6); c.rect(440, 800, 1480, 1080, (130, 94, 66), INK, 7)
def justices(k):
    c = hall(); bench(c); c.roll(880, 664, 1040, 740, 14)
    L(c, "NEW JUDGES" if k == 0 else "JUSTICES OF LABOURERS", 170, 760, 90 if k == 0 else 76, bg=PAPER if k == 0 else MARI); return c
def fines(k):
    c = C(); c.text(520, 200, "THE TOWN'S TAX BILL", 64); c.rect(300, 280, 740, 900, TEAL, INK, 8, 10); q = app("fn", .9, .3) if k else 0
    for i in range(3): yy = 300+i*120; x = lerp(1300, 520, q) if k else 1300; c.rect(x-200, yy, x+200, yy+104, MARI, INK, 7, 10); c.text(x, yy+50, "FINE", 60)
    if not k: c.text(1300, 200, "FINES FROM THE NEW COURTS", 60); arrow(c, 1060, 480, 800, 480, INK, 16, 44)
    if k and q > .95: c.text(520, 790, "STILL OWED", 64, PAPER); c.label(1300, 470, "THE TOWN OWES LESS", 70); L(c, "THE CLEVER PART", 880, 1300, 84, bg=MARI)
    return c
def turnin(k):
    c = town(); f = peasant(c, 960, 1030, 340, "hold", "worry", "green"); c.pennies(f["hand"][0]+10, f["hand"][1]-30, 3, 24, 3, 52)
    for i in range(4): x = (300, 520, 1400, 1640)[i]; peasant(c, x, 1010+(i % 2)*30, 300, "point", ("angry", "det", "angry", "smug")[i], COATS[(i+1) % 5], flip=i >= 2)
    L(c, "EVERY TOWN HAS A REASON TO TURN OFFENDERS IN", 150, size=56, bg=MARI if k else PAPER); return c
def colch(k):
    if k == 0: c, P = emap(dots=(("COLCHESTER", "COLCHESTER", 240, -30),)); hud(c, "1352"); L(c, "THE JUSTICES SIT", 150, 1500, 60, bg=MARI); return c
    if k == 1:
        c = hall(); bench(c, 3, ("smug", "smile", "smug")); [c.pennies(960-(m-1)*25, 716-r*40, m, 22, m, 50) for r, m in enumerate((17, 15))]; hud(c, "1352"); L(c, "MORE THAN 84 POUNDS IN FINES", 180, 760, 70, bg=MARI); return c
    c = C(NAVY); fallp(c, 14, 26, x0=40, x1=500); fallp(c, 14, 26, seed=3, x0=1420, x1=1880); v = int(20251*T.ease(T.LP*1.4)); c.text(960, 400, format(v, ","), 280, MARI); c.text(960, 620, "PENNIES", 120, PAPER); L(c, "OVER TWENTY THOUSAND", 860, size=70, bg=MARI); return c
def press(k):
    """The law as a lid on a stack of wages. k 0 the stack pushes; 1 it is held down; 2 years later the stack lifts and cracks it."""
    c = C((232, 226, 200)); c.rect(0, 900, W, H, PATH, None); c.line([(0, 900), (W, 900)], 6, INK, False); j = 7*math.sin(T.TT*9) if k == 0 else 0
    n = 8 if k == 0 else (int(lerp(8, 5, app("dn", .7, .2))+.5) if k == 1 else int(lerp(5, 12, app("up", .9, .2))+.5)); top = 900-n*44
    for i in range(n): yy = 900-i*44+(j if i == n-1 else 0); c.rect(700, yy-40, 1220, yy, SILVER, INK, 6, 14); c.line([(760, yy-20), (1160, yy-20)], 4, (150, 156, 166), False)
    c.text(960, 964, "WAGES", 64); y = top-70+j
    if k < 2: c.rect(480, y-50, 1440, y+50, PARCH, INK, 7, 6); c.text(960, y-4, "STATUTE OF LABOURERS", 64, INKP)
    else:
        g = 30*app("up", .9, .2); c.poly([(480, y-50), (950-g, y-50), (930-g, y), (954-g, y+50), (480, y+50)], PARCH, INK, 7); c.poly([(970+g, y-50), (1440, y-50), (1440, y+50), (974+g, y+50), (950+g, y)], PARCH, INK, 7)
        c.text(716-g/2, y-4, "STATUTE OF", 62, INKP); c.text(1206+g/2, y-4, "LABOURERS", 62, INKP)
    justice(c, 250, 1010, 340, "point" if k < 2 else "shrug", "det" if k < 2 else "wow"); reaperf(c, 1680, 1010, 330, "stand" if k < 2 else "cheer", ("det", "sad", "joy")[k], flip=True, tool=False)
    L(c, ("DOES IT WORK?", "FOR A FEW YEARS, IT DOES", "FOR DAY WAGES, THE LAW IS BEATEN")[k], 170, 1100, (100, 76, 62)[k], bg=(PAPER, MARI, MARI)[k]); hud(c, ("EARLY 1350s", "EARLY 1350s", "AFTER 1361")[k]); return c
def rollclose(c=None):
    c = C((226, 214, 190)); c.rect(0, 110, W, 830, PARCH, None); c.line([(0, 110), (W, 110)], 7, INK, False); c.line([(0, 830), (W, 830)], 7, INK, False)
    for i in (0, 1): squig(c, 140, 200+i*540, 52, i, (150, 130, 96), 6)
    return c
def carter(k):
    """Close on the account roll: the carter's wage, written, struck out, written again."""
    c = rollclose(); c.text(200, 470, "CARTER", 170, INK, "lm")
    if k == 4: c.da.ellipse([900*S, 240*S, 1600*S, 700*S], fill=(255, 214, 90, int(70+30*math.sin(T.TT*3))))
    c.text(1250, 470, typed("11s", "c11", .5, .3) if k == 0 else "11s", 210, INK)
    if k >= 1: c.strike(1050, 470, 1460, 26)
    if k >= 2: c.text(1560, 300, typed("9s 6d", "c96", .6, .2), 130, RED)
    if k == 3: L(c, "MEOPHAM, KENT: THE ACCOUNT ROLL", 960, size=54)
    if k == 5: L(c, "SOMEBODY THOUGHT HE WAS WORTH IT", 960, size=60, bg=MARI)
    return c
def maybe(k):
    c = hall()
    if k == 0: f = peasant(c, 960, 1010, 400, "hold", "sad", "blue", hd=False); c.pennies(f["hand"][0]+10, f["hand"][1]-20, 2, 30, 2, 66); L(c, "MAYBE HIS PAY WAS CUT", 170, size=84); return c
    if k == 1:
        table(c, 700, 1300); bailiff(c, 1480, 1010, 360, "hold", "smug", flip=True); f = peasant(c, 520, 1010, 360, "hold", "smug", "blue", hd=False); c.roll(880, 660, 1120, 742, 14)
        x = lerp(1300, 760, (T.TT*.5) % 1); c.penny(x, 900, 26); L(c, "MAYBE ONLY THE PAPERWORK WAS", 170, size=70, bg=MARI); return c
    c = C(); scholar(c, 520, 1010, 420, "chin", "det"); c.roll(1040, 260, 1640, 760, 30); c.text(1340, 420, "11s", 130, INK); c.strike(1210, 420, 1470, 18); c.text(1340, 600, "9s 6d", 110, RED)
    L(c, "THE HISTORIAN WHO STUDIED IT:", 130, 1340, 46); L(c, "MAYBE A WAY ROUND THE LAW", 890, 1340, 56, bg=MARI) if k == 3 else None; return c
def ways(k):
    c = C((232, 226, 200)); c.pricetag(760, 520, 3.0, "WAGE"); c.pennies(1240, 480, 6, 40, 3, 96)
    if k == 1:
        c.strike(470, 520, 1080, 16); q = app("rw", .3, .5)
        if q > 0: c.pricetag(860, 860, 3.0*q, "REWARD", MARI)
    L(c, "WAYS ROUND IT" if k == 0 else "STOP CALLING IT A WAGE", 150, size=84, bg=PAPER if k == 0 else MARI); return c
def abbot(k):
    if k == 3: c = C(); scholar(c, 520, 1010, 420, "shrug", "smile", "rose"); c.bubble(1060, 330, "\"NO DOUBT\"", 130, (-300, 70)); L(c, "ONE HISTORIAN, ON WHY", 880, 1260, 60, bg=MARI); return c
    c = meadow("day"); c.church(1040, 800, 1.5); c.rect(0, 800, W, H, PATH, None); c.line([(0, 800), (W, 800)], 5, INK, False)
    a = monk(c, 620, 1010, 380, "hold", "smile", coat="banker", staff=False); w = peasant(c, 1100, 1010, 340, "hold", "joy", "green", flip=True)
    if k == 0: c.penny(lerp(a["hand"][0]+30, w["hand"][0]-30, (T.TT*.7) % 1), a["hand"][1]-20-60*math.sin(((T.TT*.7) % 1)*math.pi), 30); L(c, "SEASONAL BONUSES", 250, 540, 84, bg=MARI)
    if k >= 1: c.sack(860, 1010, 1.5, t="WHEAT")
    if k == 2: L(c, "THE GRAIN ALLOWANCE: PAID IN WHEAT", 250, 620, 54, bg=MARI)
    hud(c, "BURY ST EDMUNDS ABBEY"); return c
def eat(k=0):
    c = hall(); table(c, 760, 1500); c.loaf(1000, 746, 1.6); c.jug(1200, 746, .8); c.rect(470, 900, 660, 1020, WOOD, INK, 6, 6); s = sidp(c, 560, 900, 420, "hold", "joy" if int(T.TT*3) % 2 == 0 else "smile", sit=True); c.loaf(s["hand"][0]+30, s["hand"][1]+10, 1.2)
    L(c, "A RAISE YOU CAN EAT", 170, size=100, bg=MARI); return c
def courts(k):
    c = C(); n0 = 7 if k == 2 else (int(7*app("zc", 1.6, .2)+.5) if k == 1 else 0)
    for i in range(8):
        x = 330+(i % 4)*420; y = 470+(i//4)*330; z = i < n0; mhouse(c, x, y, 1.25, (226, 222, 214) if z else FLINT, (190, 184, 176) if z else (166, 98, 78))
        if z: c.text(x, y+56, "0 CASES", 54, FAINT)
        elif k and i == 7: c.text(x, y+56, "SOME", 54, RED)
    L(c, "ONE STUDY CHECKED 8 MANORS" if k == 0 else "7 OF THE 8 NEVER RECORDED A SINGLE CASE", 130, size=64 if k == 0 else 56, bg=PAPER if k == 0 else MARI); return c
def back61(k):
    c = vill("grey", dead=(0, 3)); q = app("fd", .5, .6) if k == 2 else 0
    for i in range(5):
        x = 420+i*270
        if k == 2 and i == 2 and q > .5: c.grave(x, 1000, 1.3)
        else: peasant(c, x, 1010, 300, "stand", "worry" if k else "n", COATS[i], flip=i > 2)
    dimc(c, 30+30*min(k, 1)); L(c, ("1361", "THE PLAGUE COMES BACK", "ABOUT 1 IN 5 (ONE ESTIMATE)")[k], 180, 1100, (150, 70, 70)[k], bg=(PAPER, PAPER, MARI)[k]); hud(c, "1361"); return c
def half(k):
    c = C(); c.text(960, 110, "DAY RATE FOR A THATCHER AND HIS MATE", 58, FAINT); c.line([(420, 880), (1500, 880)], 7); a, b = 3.5, 5.7; q = app("hf", .9, .2); v = lerp(a, b, q)
    c.rect(600, 880-a*100, 860, 880, TEAL, INK, 7, 6); c.rect(1060, 880-v*100, 1320, 880, RED, INK, 7, 6); c.text(730, 880-a*100-56, "3.5d", 80); c.text(1190, 880-v*100-56, str(round(v, 1))+"d", 80, RED)
    c.text(730, 950, "EARLY 1340s", 60); c.text(1190, 950, "EARLY 1370s", 60); c.text(960, 1030, "ONE EXAMPLE FROM THE STUDY", 44, FAINT)
    if k == 1: L(c, "UP BY MORE THAN HALF", 320, 580, 70, bg=MARI)
    return c
def dinner(k):
    c = hall(win=False)
    for i in range(3): peasant(c, 560+i*400, 930, 300, "hold", ("n", "smile", "n")[i] if k < 2 else ("bored", "sad", "bored")[i], COATS[i], hd=False)
    table(c, 360, 1560, 800); c.bowl(620, 730, 1.0); c.ham(1000, 720, 1.1); c.fishp(1360, 730, 1.0)
    if k == 0: L(c, "PARLIAMENT EVEN TRIES TO CONTROL DINNER", 180, 1040, 58)
    if k in (1, 2): L(c, "SERVANTS: MEAT OR FISH ONLY ONCE A DAY", 180, 1040, 58, bg=MARI)
    if k == 2:
        for x in (1000, 1360): arrow(c, 1180, 850, x, 790, RED, 12, 30)
        c.label(1180, 900, "ONCE A DAY", 64, bg=MARI)
    if k == 3: z = 2-app("rp", .25, .2); c.rect(1040-470*z, 270-100*z, 1040+470*z, 270+100*z, PAPER, RED, 14, 16); c.text(1040, 262, "REPEALED THE NEXT YEAR", 76*z, RED)
    hud(c, "1364" if k == 3 else "1363"); return c
def langland(k):
    if k == 0: c = hall("dusk"); desk(c, 1040, 800); f = peasant(c, 700, 1000, 360, "write", "angry", "green"); L(c, "WILLIAM LANGLAND, POET", 150, 760, 70); return c
    c = hall(); table(c, 700, 1560, 800); old = k == 1
    if old: c.bowl(980, 740, 1.2); c.cabbage(980, 700, 1.0); c.jug(1300, 766, .9, (150, 140, 120))
    else: c.ham(960, 700, 1.5); c.fishp(1330, 716, 1.3)
    sidp(c, 440, 1010, 380, "point" if old else "cheer", "bored" if old else "joy")
    if old: c.redx(1130, 640, 150, 28)
    L(c, "DAY-OLD VEGETABLES AND CHEAP ALE? NO." if old else "FRESH MEAT AND FISH", 170, 1130, 56 if old else 90, bg=PAPER if old else MARI); return c
def kept(k):
    c = hall(win=False)
    if k == 0: s = sidp(c, 520, 1010, 360, "cheer", "joy"); c.ham(s["hand"][0]+10, s["hand"][1]-70, .8); Q(c, 4, 3); return c
    table(c, 1080, 1760); c.ham(1260, 730, 1.0); c.pennies(1500, 716, 6, 20, 3, 44); sidp(c, 700, 1030, 460, "chin", "worry"); dimc(c, 80); c.text(1200, 430, "?", 420*(.8+.2*app("qm", .3)), MARI); L(c, "DIDN'T YOU?", 170, 700, 100); return c
# ================= the hidden quest: who really got paid =================
def halfgone(k):
    c = C(); q = app("hg", .6, .3) if k >= 1 else 0; q2 = app("mv", .8, .2) if k == 2 else 0
    for i in range(10):
        gone = k >= 1 and i % 2 == 1 and q > .5; x = 240+i*160
        if gone: c.ell(x-30, 300-36, x+30, 300+21, None, (200, 192, 180), 5); c.line([(x, 330), (x, 380)], 8, (200, 192, 180), False)
        else: icon(c, x, 300, TEAL, 2.0)
        px = lerp(x, x-160+56 if i % 2 == 1 else x-56, q2) if k == 2 else x; c.penny(px, 660, 52)
    c.text(960, 150, "PEOPLE", 60, FAINT); c.text(960, 540, "COINS", 60, FAINT)
    if k == 1: L(c, "PERHAPS HALF THE PEOPLE ARE GONE", 900, size=70)
    if k == 2: L(c, "THE COINS AREN'T", 900, size=100, bg=MARI)
    return c
def infl(k):
    if k == 2:
        c = C(); x0, x1 = 240, 1680; c.line([(x0, 620), (x1, 620)], 9); q = app("ph", 1.0, .2); xm = x0+(x1-x0)*.72
        c.rect(x0, 500, x0+(xm-x0)*q, 600, RED, INK, 7, 8); c.text(x0, 700, "1349", 76); c.text(xm, 700, "MID 1370s", 76, RED); c.text(x1, 700, "1380", 60, FAINT); L(c, "PRICES STAY HIGH", 330, size=110, bg=MARI); return c
    c = C((232, 226, 200)); c.rect(0, 800, W, H, WOOD, None); c.line([(0, 800), (W, 800)], 7, INK, False); c.loaf(420, 790, 2.4); c.jug(960, 790, 1.5); c.fishp(1480, 730, 1.6); up = 60*app("ris", 1.0, .2) if k == 1 else 0
    for x in (420, 960, 1480):
        c.pricetag(x+30, 470-up, 1.3, "PRICE", MARI if k else CREAM)
        if k: arrow(c, x-170, 560, x-170, 400-up*.5, RED, 18, 44)
    L(c, "MORE MONEY PER HEAD" if k == 0 else "EVERYTHING COSTS MORE", 150, size=84, bg=PAPER if k == 0 else MARI); return c
def realw(k):
    c = C(); c.text(300, 400, "BEFORE", 70); c.text(300, 728, "AFTER", 70); c.pennies(520, 400, 3, 40, 3, 96); c.pennies(520, 680, 6, 40, 3, 96)
    for y in (400, 728): arrow(c, 900, y, 1060, y, INK, 14, 40)
    for i in range(3): c.loaf(1220+i*170, 440, 1.5)
    q = app("ls", .5, .5) if k == 2 else 0
    for i in range(3):
        if not (k == 2 and i == 2 and q > .5): c.loaf(1220+i*170, 768, 1.5)
    if k == 2 and q > .5: c.redx(1560, 728, 60, 18)
    L(c, ("A BIGGER WAGE", "OFTEN BUYS NO MORE", "SOMETIMES LESS")[k], 150, size=86, bg=(PAPER, MARI, MARI)[k]); c.text(960, 1000, "AN ILLUSTRATION, NOT REAL PRICES", 44, FAINT); return c
def kinds(k):
    if k == 3:
        c = parch("THE ORDINANCE OF LABOURERS, 1349", 56); c.text(960, 470, typed("\"THE LACK ESPECIALLY", "lk", .7), 100, INKP); c.text(960, 620, typed("OF PLOUGHMEN\"", "lk2", .5, .8), 100, INKP); L(c, "THE KING'S ORDER NAMES YOUR JOB", 850, size=58, bg=MARI); return c
    c = field("day", far=False); a = reaperf(c, 400, 1020, 360, "hold", "smile" if k < 2 else "joy"); chip(c, 400, a["head"][1]-80, "DAY LABOURER", TEAL, 46)
    s = sidp(c, 1480, 1020, 360, "stand" if k < 2 else "self", "n" if k < 2 else "worry"); chip(c, 1480, s["head"][1]-80, "YOU: PLOUGHMAN", RED, 46)
    if k == 1:
        q = app("dl", .8, .2); c.rect(720, 600, 1040, 990, PAPER, INK, 7, 16); c.line([(750, 910), (1010, 910)], 6); c.rect(770, 910-110, 860, 910, TEAL, INK, 6, 6); c.rect(900, 910-lerp(110, 220, q), 990, 910, RED, INK, 6, 6)
        c.text(815, 948, "1349", 44); c.text(945, 948, "1350", 44); L(c, "NEARLY DOUBLED IN A YEAR", 170, 760, 60, bg=MARI)
    if k == 2:
        for i in range(3): c.sack(1050+i*110, 1040, .9)
        L(c, "HIRED BY THE YEAR. PAID MOSTLY IN GRAIN.", 170, 1100, 50, bg=MARI)
    if k == 0: L(c, "IT MATTERS WHAT KIND OF WORKER YOU ARE", 170, size=60)
    return c
def three(k):
    c = hall(win=False)
    for i in range(3): scholar(c, 620+i*340, 910, 330, ("write", "chin", "stand")[i], ("det", "n", "smile")[i], ("slate", "rose", "teal")[i], flip=i == 2)
    table(c, 420, 1500, 790)
    for i in range(5): c.roll(520+i*190, 704, 640+i*190, 752, 12)
    L(c, "THREE ECONOMIC HISTORIANS" if k == 0 else "CLARIDGE, DELABASTITA AND GIBBS (2023)", 180, size=70 if k == 0 else 54, bg=PAPER if k == 0 else MARI); return c
FAM = [(1349, 25), (1355, 24), (1362, 26), (1370, 24), (1380, 25), (1392, 31), (1405, 36), (1422, 41), (1436, 53)]
def famchart(k):
    """Yearly farm servants' pay. A sketch through the averages the study gives. k: 0-1 flat to 1380, 2 climbing, 3 doubled, 4-6 the close."""
    c = C(); box = c.chartbox(260, 250, 1660, 900, None); pts = [((x-1345)/95, y/62) for x, y in FAM]; xf = (1380-1349)/(1436-1349)
    g = lerp(0, xf, T.ease(T.GP*1.15)) if k <= 1 else (lerp(xf, 1, T.ease(T.GP*1.1)) if k in (2, 3) else 1.0)
    bx0, by0, bx1, by1 = box; X = lambda yr: bx0+(bx1-bx0)*(yr-1345)/95
    if k >= 4: c.da.rectangle([X(1349)*S, by0*S, X(1380)*S, by1*S], fill=(224, 79, 58, 46)); c.text((X(1349)+X(1380))/2, by1-56, "30 YEARS", 60, RED)
    for yr in (1349, 1380, 1430): c.line([(X(yr), by1), (X(yr), by1+22)], 6); c.text(X(yr), by1+62, str(yr)+("s" if yr == 1430 else ""), 54)
    tip = c.plot(box, pts, g, RED, 13)
    c.text(960, 170, "A PLOUGHMAN'S YEARLY PAY (AVERAGES, GRAIN INCLUDED)", 54, FAINT); c.text(960, 1036, "SKETCH. THE LABELLED FIGURES ARE FROM THE STUDY.", 46, FAINT)
    if k <= 1 and g > xf*.5: c.label(X(1364), 540, "ABOUT 25 SHILLINGS", 46)
    if k == 1: L(c, "BARELY MOVES FOR 30 YEARS", 330, 760, 66, bg=MARI)
    if k == 2: c.label(X(1392), 430, "1380s: IT STARTS CLIMBING", 46, bg=MARI)
    if k == 3: c.label(X(1410), 330, "1430s: ROUGHLY DOUBLED", 52, bg=MARI)
    if k == 5: c.rect(X(1364)-150, 330, X(1364)+150, 420, PARCH, INK, 6, 6); c.text(X(1364), 371, "THE LAW", 60, INKP); L(c, "THE LAW: PART OF THE REASON", 770, 1270, 50)
    if k == 6: L(c, "IT COULDN'T MANAGE FORTY", 770, 1270, 62, bg=MARI)
    return c
def golden(k):
    c = C(GRASS); sky(c, 600, "gold", sun=False); c.da.ellipse([560*S, 300*S, 1360*S, 1100*S], fill=(255, 236, 150, 90)); c.ell(760, 400, 1160, 800, MARI, INK, 8); c.rect(0, 600, W, H, (206, 196, 120), None); c.line([(0, 600), (W, 600)], 6, INK, False)
    c.wheat(0, W, 760, 150, T.TT, 26); c.wheat(10, W, 880, 170, T.TT+1, 28, seed=2); reaperf(c, 520, 1030, 360, "cheer", "joy", tool=False)
    if k == 0: L(c, "THE GOLDEN AGE OF THE ENGLISH LABOURER", 150, 900, 56)
    if k >= 1: x = lerp(1960, 1380, T.ease(T.GP*1.1)); sidp(c, x, 1030, 350, ("walk" if step() else "stand") if x > 1390 else "shrug", "bored", flip=x > 1390, staff=True)
    if k == 2: L(c, "FOR YOU: A GENERATION LATE", 150, size=70, bg=MARI)
    return c
WHY = [("OTHER OPTIONS", "CHEAP LAND. DAY WORK."), ("GRAIN PRICES", "FALL AND STEADY"), ("EMPLOYERS", "STOP HOLDING THE LINE")]
def why(k):
    c = C(); L(c, "WHY THEN? THE THREE POINT TO THREE THINGS", 110, size=54)
    for i in range(3):
        x = 360+i*600; on = i < k; c.rect(x-260, 250, x+260, 930, WHITE if not on else CREAM, INK, 8, 22); c.ell(x-56, 280, x+56, 392, MARI if on else (236, 230, 220), INK, 7); c.text(x, 332, str(i+1), 80)
        if not on: c.text(x, 600, "?", 220, (214, 206, 192)); continue
        z = app(("wy", i), .3, .1); c.text(x, 780, WHY[i][0], 60*z+1); c.text(x, 858, WHY[i][1], 44*z+1, RED)
        if i == 0: c.line([(x, 720), (x, 470)], 12, TIMBER, False); c.poly([(x+6, 460), (x+200, 460), (x+236, 502), (x+200, 544), (x+6, 544)], PARCH, INK, 5); c.text(x+110, 498, "LAND", 56); c.poly([(x-6, 570), (x-204, 570), (x-240, 612), (x-204, 654), (x-6, 654)], PARCH, INK, 5); c.text(x-116, 608, "DAY WORK", 46)
        if i == 1: c.sack(x-60, 700, 1.3); arrow(c, x+120, 470, x+120, 470+200*z, RED, 18, 44)
        if i == 2: c.poly([(x-190, 500), (x-14, 500), (x-34, 560), (x-10, 620), (x-190, 620)], PARCH, INK, 6); c.poly([(x+14, 500), (x+190, 500), (x+190, 620), (x+18, 620), (x-6, 560)], PARCH, INK, 6); c.text(x-104, 556, "THE", 52, INKP); c.text(x+104, 556, "LAW", 52, INKP)
    return c
def burst(c, x, y, r=90, col=RED):
    pts = []
    for i in range(16): a = i*math.pi/8+T.TT*1.5; rr = r*(1.0 if i % 2 == 0 else .5)*(1+.12*math.sin(T.TT*12+i)); pts.append((x+rr*math.cos(a), y+rr*math.sin(a)))
    c.poly(pts, col, INK, 6); c.ell(x-r*.3, y-r*.3, x+r*.3, y+r*.3, MARI, None)
def explode(k):
    if k == 0:
        c, P = emap(dots=()); q = app("ex", .3, .2)
        if q > 0: burst(c, P["ESSEX"][0]+30, P["ESSEX"][1]-10, 80*q); burst(c, P["KENT"][0]+30, P["KENT"][1]+30, 80*q)
        L(c, "THE COUNTRY EXPLODES", 150, 1480, 56, bg=MARI); hud(c, "1381"); return c
    c = C((196, 220, 230)); P = c.britain(-1340, -2252, 4.0); lon = P["LONDON"]; q = T.ease(T.LP)
    for n, lx, ly, dy in (("ESSEX", 330, -50, -16), ("KENT", 330, 60, 16)):
        x, y = P[n]; burst(c, x+40, y, 90); arrow(c, x-30, y-dy, lerp(x-30, lon[0]+34, q), lerp(y-dy, lon[1]+dy, q), INK, 14, 36); c.label(x+lx, y+ly, n, 64)
    c.ell(lon[0]-22, lon[1]-22, lon[0]+22, lon[1]+22, RED, INK, 7); c.label(lon[0]-250, lon[1]-10, "LONDON", 64, bg=MARI)
    c.text(280, 1040, "SKETCH MAP, NOT TO SCALE", 38, (90, 120, 136)); L(c, "ESSEX AND KENT RISE", 150, 1300, 70); hud(c, "1381"); return c
def poll(k):
    c = hall(win=False); justice(c, 1700, 930, 340, "write", "det", flip=True); table(c, 980, 1800, 800); a = lordp(c, 620, 1010, 360, "hold", "bored"); b = peasant(c, 320, 1010, 320, "hold", "sad", "brown")
    if k >= 1: c.pennies(1040, 700, int(12*app("pa", .8, .2)+.5), 20, 6, 46); chip(c, 1155, 630, "RICH: 12d", RED, 40)
    if k >= 2: c.pennies(1340, 700, int(12*app("pb", .8, .2)+.5), 20, 6, 46); chip(c, 1455, 630, "POOR: 12d", NAVY, 40)
    L(c, ("A POLL TAX", "12 PENCE FROM EVERYONE OVER 15", "RICH OR POOR")[k], 180, 1040, (100, 60, 100)[k], bg=(PAPER, PAPER, MARI)[k]); hud(c, "1380"); return c
def mob(c, xs, y=1010, h=300, flip=False, exs=("angry", "det", "strain", "angry"), tools=True):
    for i, x in enumerate(xs):
        f = peasant(c, x, y+(i % 3)*26, h-(i % 2)*20, ("up", "cheer", "point", "up")[i % 4], exs[i % len(exs)], COATS[i % 5], flip=flip)
        if tools and i % 2 == 0: c.pitchfork(f["hand"][0], f["hand"][1]+150, .8, 8 if not flip else -8)
def tolondon(k=0):
    c = meadow("day", road=True); c.citywall(830, 1100, W, 330, gate=1560); x0 = lerp(-900, 0, T.ease(T.LP)); mob(c, [x0+160+i*150 for i in range(6)]); c.pennon(x0+560, 1000, 520, None, RED, 240, T.TT*3)
    L(c, "THE REBELS REACH LONDON", 210, 700, 72, bg=MARI); hud(c, "JUNE 1381"); return c
def mileend(k):
    c = meadow("day"); c.citywall(700, 1150, W, 220); c.rect(0, 700, W, H, GRASS, None); c.line([(0, 700), (W, 700)], 5, INK, False); mob(c, [140, 300, 460, 620, 780], tools=k < 2)
    king(c, 1320, 1010, 350, "stand" if k < 3 else "chin", "worry", flip=True); lordp(c, 1530, 1000, 330, "stand", "angry", flip=True); lordp(c, 1720, 1010, 330, "stand", "worry", flip=True, coat="blue")
    if k >= 2: c.pennon(380, 1000, 640*app("b1", .35, .1)+10, "END SERFDOM", RED, 420, T.TT*3, 56)
    if k >= 4: c.pennon(700, 1000, 520*app("b2", .35, .1)+10, "END THE\nWAGE LIMITS", NAVY, 400, T.TT*3+1, 46)
    if k == 0: L(c, "MILE END", 170, 1000, 110)
    if k == 1: L(c, "THE KING: RICHARD II", 170, 1280, 64, bg=MARI)
    if k == 4: L(c, "(ONE ACCOUNT OF THEIR DEMANDS)", 170, 1240, 46, bg=MARI)
    hud(c, "JUNE 1381"); return c
def agrees(k):
    c = meadow("day"); c.citywall(700, 1150, W, 220); c.rect(0, 700, W, H, GRASS, None); c.line([(0, 700), (W, 700)], 5, INK, False); mob(c, [140, 300, 460, 620, 780], tools=False, exs=("joy", "smile", "wow", "joy") if k else ("det", "worry", "n", "det"))
    king(c, 1320, 1010, 350, "hold", "n", flip=True)
    if k == 0: c.bubble(1280, 380, "AGREED.", 110, (20, 90))
    if k == 1:
        for i in range(5): q = (T.TT*.5+i*.2) % 1; c.charter(lerp(1130, 200, q), 600-200*math.sin(q*math.pi)+i*14, .5)
        L(c, "CHARTERS GO OUT", 150, size=96, bg=MARI)
    hud(c, "JUNE 1381"); return c
def smith(k=0):
    c = meadow("dusk"); c.citywall(700, 0, W, 240); c.rect(0, 700, W, H, (150, 160, 120), None); c.line([(0, 700), (W, 700)], 5, INK, False)
    f = c.person(1160, 1010, 360, "point", "angry", "banker", flip=True); c.hat(f, "bowler", (120, 40, 40)); hx, hy = f["hand"]; c.line([(hx, hy), (hx-90, hy+10)], 12, INK, False); c.line([(hx, hy), (hx-90, hy+10)], 6, SILVER, False)
    q = app("fall", .5, .7); peasant(c, 760, 1010, 350, "drop", "pain", "green", rot=-60*q) if q > .02 else peasant(c, 760, 1010, 350, "up", "wow", "green")
    if .0 < q < 1: burst(c, 960, 640, 110)
    L(c, "THE MAYOR OF LONDON STABS WAT TYLER", 210, size=62, bg=MARI); hud(c, "THE NEXT DAY"); return c
def revoked(k):
    if k <= 1:
        c = C((232, 226, 200)); z = 2-app("rv", .25, .5) if k == 0 else 1; c.charter(960, 500, 2.3, "CHARTER", 4, RED, None)
        if k == 1 or T.LT > .5: c.rect(960-360*z, 520-90*z, 960+360*z, 520+90*z, PARCH, RED, 16, 14); c.text(960, 514, "REVOKED", 150*z, RED)
        hud(c, "JULY 1381"); return c
    c = meadow("dusk", 520); dimc(c, 90)
    for i in range(24): c.grave(130+(i % 8)*230+(i//8)*50, 700+(i//8)*150, .8)
    v = int(1500*T.ease(T.LP*1.4)) if k == 2 else 1500; c.text(960, 300, format(v, ","), 260, PAPER); L(c, "AT LEAST. EXECUTED OR KILLED IN BATTLE." if k == 3 else "BY NOVEMBER", 520, size=56, bg=MARI); hud(c, "NOVEMBER 1381"); return c
def lose(k):
    c = meadow("dusk" if k == 0 else "dawn", 600, sun=False, **({} if k < 2 else {}))
    if k == 2: c.ell(860, 400, 1060, 600, MARI, INK, 7); hills(c, 600); c.rect(0, 600, W, H, GRASS, None); c.line([(0, 600), (W, 600)], 5, INK, False); c.wheat(700, 1220, 780, 90, T.TT, 30)
    c.line([(500, 980), (1380, 900)], 12, TIMBER); c.poly([(1100, 926), (1380, 900), (1420, 990), (1150, 1020)], RED, INK, 6); c.pitchfork(700, 1040, 1.0, 84)
    if k < 2: dimc(c, 90-50*k)
    L(c, ("SO THE REBELS LOSE", "AND THEN, OVER THE NEXT LIFETIME", "SOME OF WHAT THEY WANTED HAPPENS ANYWAY")[k], 170, size=(96, 62, 60)[k], bg=(PAPER, PAPER, MARI)[k]); return c
def nopoll(k=0):
    c = hall(win=False); justice(c, 620, 930, 350, "shrug", "worry"); table(c, 340, 920, 800); c.roll(1140, 320, 1660, 660, 30); c.text(1400, 490, "POLL TAX", 104, INKP); c.redx(1400, 490, 190, 16)
    L(c, "PARLIAMENT DOESN'T TRY ANOTHER POLL TAX", 170, size=58, bg=MARI); return c
def caps(k):
    c = C(); c.line([(300, 880), (1620, 880)], 7); c.rect(520, 880-190, 800, 880, TEAL, INK, 7, 6); c.text(660, 950, "THE OLD MAXIMUM", 54); q = app("nc", .9, .2)
    c.rect(1120, 880-lerp(190, 470, q), 1400, 880, RED, INK, 7, 6); c.text(1260, 950, "THE NEW MAXIMUM, 1388", 54)
    c.line([(440, 880-190), (1480, 880-190)], 5, (150, 140, 128), False)
    if k == 1: L(c, "WELL ABOVE THE OLD ONES", 230, size=84, bg=MARI)
    else: L(c, "PARLIAMENT GIVES GROUND ON PAY", 230, size=64)
    c.text(960, 1030, "BAR HEIGHTS ARE A SKETCH", 46, FAINT); hud(c, "1388"); return c
def wither(k):
    c = meadow("day"); c.manor(60, 780, 520, 240); c.cottage(1420, 780, 320, 180); c.rect(0, 780, W, H, PATH, None); c.line([(0, 780), (W, 780)], 5, INK, False)
    a = lordp(c, 520, 1010, 350, "hold", "bored" if k else "smug"); b = peasant(c, 1340, 1010, 330, "stand" if k < 2 else "wave", "sad" if k == 0 else "smile", "green", flip=True)
    g = 0 if k == 0 else (T.ease(T.GP*1.2) if k == 1 else 1.0); n = 10
    for i in range(n):
        if i/n < 1-g: x = lerp(a["hand"][0]+30, b["hand"][0]-10, i/(n-1)); y = a["hand"][1]+40*math.sin(i/(n-1)*math.pi); c.ell(x-30, y-18, x+30, y+18, None, (90, 96, 110), 9)
        else: x = lerp(a["hand"][0]+30, b["hand"][0]-10, i/(n-1)); c.ell(x-30, 1000, x+30, 1030, None, (170, 166, 160), 7)
    L(c, ("SERFDOM? THE CHARTERS WERE REVOKED.", "IT WITHERS AWAY", "OVER THE NEXT CENTURY")[k], 150, size=(58, 100, 90)[k], bg=(PAPER, MARI, MARI)[k]); hud(c, ("1381", "1400s", "1400s")[k]); return c
def econ(k):
    c = meadow("day", road=True); mhouse(c, 250, 800, 2.3); mhouse(c, 1670, 800, 2.3, (214, 204, 186), (120, 130, 150))
    lordp(c, 560, 1030, 330, "point", "angry" if k >= 2 else "det"); lordp(c, 1400, 1030, 330, "point", "smile", flip=True, coat="blue")
    x = 960 if k < 2 else lerp(960, 1170, T.ease(T.LP)); peasant(c, x, 1010, 330, ("walk" if step() else "stand") if 965 < x < 1165 else "chin", "smug", "green")
    if k >= 1: c.bubble(580, 440, "TERMS", 70, (0, 70)); c.bubble(1390, 410, "BETTER\nTERMS", 80, (0, 60), f=MARI)
    if k in (0, 3): L(c, "HISTORIANS: MOSTLY ECONOMICS, NOT THE REVOLT" if k == 0 else "A LORD WHO NEEDS TENANTS HAS TO COMPETE", 150, size=54, bg=PAPER if k == 0 else MARI)
    return c
def fourth(k):
    c = C(); c.questlog(ROWS, 4, 3 if k == 0 else 4, HID if k else None, x=545, y=200)
    if k: c.marker(470, 800, 36)
    return c
def books(k):
    c = C((214, 196, 170))
    for j in (0, 1):
        y = 420+j*400; c.rect(120, y, 1800, y+36, WOOD, INK, 7)
        for i in range(17):
            x = 170+i*96; h = 230+(i*53+j*31) % 90; col = ((140, 70, 60), (70, 100, 120), (90, 120, 90), (150, 120, 70))[(i+j) % 4]
            if (j == 0 and 6 <= i <= 9) or (j == 1 and i >= 10): continue
            c.rect(x, y-h, x+78, y, col, INK, 5, 4); c.line([(x+14, y-h+40), (x+64, y-h+40)], 4, MARI, False)
    x = 170+6*96; c.rect(x+10, 60, x+364, 420, (110, 40, 30), INK, 8, 8); c.rect(x+34, 84, x+340, 396, None, MARI, 4, 6); c.text(x+187, 160, "STATUTE", 64, MARI); c.text(x+187, 236, "OF", 50, MARI); c.text(x+187, 312, "LABOURERS", 54, MARI)
    for i in range(3): c.line([(x+364, 60), (x+364+110-i*26, 60+70+i*46)], 3, (244, 240, 232), False)
    v = 1351+int((1863-1351)*T.ease(T.GP*1.15)) if k < 2 else 1863; c.rect(1130, 480, 1790, 800, PAPER, INK, 8, 22); c.text(1460, 630, str(v), 220, RED if v == 1863 else INK)
    if k == 2: L(c, "ON THE BOOKS UNTIL 1863", 960, 600, 70, bg=MARI)
    return c
def finale(k=0):
    c = C(GRASS); sky(c, 500, "gold", sun=False); c.da.ellipse([180*S, 150*S, 760*S, 730*S], fill=(255, 236, 150, 90)); c.ell(380, 330, 560, 510, MARI, INK, 7); hills(c, 510, (176, 190, 120)); c.rect(0, 510, W, H, (176, 190, 120), None); farvill(c, 1380, 512, .8)
    c.strips(516, H, 9, cols=((196, 196, 110), (220, 190, 104), (170, 130, 94))); c.line([(0, 516), (W, 516)], 5, INK, False); team(c, 330, False, .82); Q(c, 4, 4, HID); L(c, "QUEST COMPLETE", 100, 480, 100, bg=MARI); return c
U = [
 ("It's thirteen forty-nine. About half your village is dead.", [F(card, "ENGLAND. 1349."), F(cold, 0), F(cold, 1)]),
 ("And for the first time in your life, your boss needs you more than you need him.", [F(boss, 0), F(boss, 1)]),
 ("So you ask for more money. So do plenty of others.", [F(ask, 0), F(ask, 1)]),
 ("Within the year, the king bans the raise.", [F(kingban)]),
 ("So here's the question. Do you actually get your raise?", [F(question, 0), F(question, 1)], "chime"),
 ("You're twenty-two. You're a ploughman on a manor in the south of England.", [F(intro), F(ploughing, 0), F(ploughing, 1)]),
 ("You are made up. The wages, the laws and the fines are not.", [F(card, "YOU ARE MADE UP.", "THE WAGES, THE LAWS AND THE FINES ARE NOT.", 140)]),
 ("Here's your quest log. One: live through the plague.", [F(qfield, 0), F(qfield, 1)], "tick"),
 ("Two: get a raise.", [F(qfield, 2)], "tick"),
 ("Three: keep it.", [F(qfield, 3)], "tick"),
 ("There's a fourth quest hidden at the end. It's about who really got paid.", [F(qfield, 4), F(hiddenq, 1, 0)], "tick"),
 ("First, what you're worth before the plague. Not much.", [F(card, "BEFORE THE PLAGUE"), F(worth)]),
 ("One historian calls Britain in the early thirteen hundreds horrendously overpopulated. Plenty of hands. Not enough land.", [F(crowd, 0), F(crowd, 1), F(crowd, 2)]),
 ("You're hired by the year. Most of your pay isn't money. It's grain.", [F(hired), F(paykind, 0), F(paykind, 1)]),
 ("The coin part might be five shillings. It might be ten. A year.", [F(coins, 0), F(coins, 1), F(coins, 2)]),
 ("Twelve pennies make a shilling. Twenty shillings make a pound. You won't be needing the word pound.", [F(money, 0), F(money, 1), F(money, 2)]),
 ("Some of your neighbours aren't free. They're villens.", [F(villein, 0), F(villein, 1)]),
 ("A villen can owe the lord two or three days' work a week, on the lord's own fields.", [F(week, 0), F(week, 1)]),
 ("Usually he can't legally leave. If his daughter marries off the manor, he pays a fine. When he dies, his heir pays to inherit.", [F(rules, 0), F(rules, 1), F(rules, 2)]),
 ("Then, in June of thirteen forty-eight, by one chronicle's account, a ship from Gascony docks in Dorset.", [F(card, "JUNE 1348"), F(ship, 0), F(ship, 1)]),
 ("A sailor on board brings the sickness with him. Other chronicles name other ports.", [F(sailor, 0), F(sailor, 1)]),
 ("By November it's in London. By the next summer it's in the north.", [F(spread, 0), F(spread, 1)]),
 ("It takes about five hundred days to cross the country.", [F(spread, 2)]),
 ("A chronicler named Nighton writes that few people lasted more than two or three days in bed.", [F(knighton, 0), F(knighton, 1)]),
 ("Nobody knows the toll. Forty to sixty percent is the range you'll hear most. Some historians say less. One says more.", [F(toll, 0), F(toll, 1), F(toll, 2)]),
 ("Then you get it.", [F(sick, 0)]),
 ("Here's something the story usually skips. Some people recovered.", [F(sick, 1), F(sick, 2)]),
 ("On a manor in Huntingdon-sheer, the monks kept a list of tenants too sick to work in the spring and summer of thirteen forty-nine. Twenty-two names, and how long each was gone.", [F(sicklist, 0), F(sicklist, 1), F(sicklist, 2), F(sicklist, 3)]),
 ("Three out of four were back at work inside a month.", [F(backwork)]),
 ("The rules allowed up to a year and a day off sick. Henry Brown took one week.", [F(sickleave, 0), F(sickleave, 1)]),
 ("It's a list of survivors. It doesn't count the ones who never came back.", [F(sicklist, 4), F(graves)]),
 ("You're on the lucky list. Quest one, complete.", [F(lucky)], "chime"),
 ("Now look around.", [F(around)]),
 ("Nighton again. Sheep and cattle wander through the crops, and there's nobody to drive them off.", [F(strays, 0), F(strays, 1)]),
 ("A horse that was worth forty shillings sells for six shillings and eight pence.", [F(horsep, 0), F(horsep, 1)]),
 ("Crops perish in the fields, for want of anyone to gather them.", [F(rot, 0), F(rot, 1)]),
 ("He says there's such a lack of servants that no one knows what he ought to do.", [F(lack, 0), F(lack, 1)]),
 ("You know exactly what to do.", [F(youknow)]),
 ("Quest two. Get a raise.", [F(q2)], "tick"),
 ("That autumn, Nighton says, nobody can get a reaper for less than eight pence. Plus his food.", [F(reaper, 0), F(reaper, 1)]),
 ("Remember that number. Eight pence.", [F(eight)]),
 ("In one sample of manor accounts, the average day rate goes from about a penny and a half to three pence. In a single year.", [F(rate, 0), F(rate, 1), F(rate, 2)]),
 ("On a manor in Suffolk, part of the harvest still costs three pence an acre to reap. The rest costs five. And the reaper gets more tips, and bigger ones.", [F(suffolk, 0), F(suffolk, 1), F(suffolk, 2), F(suffolk, 3)]),
 ("And people start moving. If this lord won't pay, another one might.", [F(moving, 0), F(moving, 1)]),
 ("Nighton says lords let tenants off their rent, just to stop them leaving.", [F(rent, 0), F(rent, 1)]),
 ("So you go to the bailiff, and you name a number.", [F(tohall, 0), F(tohall, 1)]),
 ("The accounts of a manor in Kent show what happens next. Cash pay goes up, most of all for the ploughmen and the carter.", [F(acct, 0), F(acct, 1)]),
 ("The account roll gives the reason. The heavy mortality of that year.", [F(acct, 2)]),
 ("The food allowance goes up too, by nearly a third.", [F(acct, 3)]),
 ("Quest two, complete. That was easy.", [F(easy, 0)], "chime"),
 ("It was too easy.", [F(easy, 1)]),
 ("Because the king has already moved. June, thirteen forty-nine. The plague is still heading north, and he issues the Ordinance of Labourers.", [F(card, "JUNE 1349"), F(ordin, 0), F(ordin, 1), F(ordin, 2)]),
 ("If you're fit, under sixty, and have no land or trade to live on, you must work for whoever asks.", [F(ord1, 0), F(ord1, 1), F(ord1, 2), F(ord1, 3)]),
 ("Your pay is whatever was usual in thirteen forty-six. Before the plague.", [F(back46, 0), F(back46, 1)]),
 ("Refuse, or leave before your term is up, and you go to prison.", [F(prison, 0), F(prison, 1)]),
 ("Even giving alms to a beggar who could work becomes an offence.", [F(alms, 0), F(alms, 1)]),
 ("It doesn't take. Nighton says the labourers were so arrogant and hostile that they paid no heed to the king's command.", [F(ignore, 0), F(ignore, 1), F(ignore, 2)]),
 ("So in thirteen fifty-one, Parliament comes back with a price list.", [F(card, "1351"), F(parl)]),
 ("The Statute of Labourers. It complains that servants won't work unless they get double or triple the old wage.", [F(statute, 0), F(statute, 1), F(statute, 2)]),
 ("Then it names the prices. Haymaking: a penny a day.", [F(prices, 0)]),
 ("Mowing: five pence an acre, or five pence a day.", [F(prices, 1)]),
 ("Threshing a quarter of wheat: two pence hay-penny.", [F(prices, 2)]),
 ("A master carpenter: three pence a day. A master mason: four.", [F(prices, 3), F(prices, 4)]),
 ("And reaping. Nighton's reaper wanted eight pence and his food. The law says two pence a day. Three, from the second week of August.", [F(reap, 0), F(reap, 1), F(reap, 2)]),
 ("No extras. The statute says: without meat or drink, or other courtesy.", [F(extras, 0), F(extras, 1), F(extras, 2)]),
 ("It has rules for you in particular. Farm servants are hired by the year, or the usual term. Not by the day.", [F(foryou, 0), F(foryou, 1), F(foryou, 2)]),
 ("Looking for work? You carry your tools into town in your hand, and you're hired in the open. No private deals.", [F(market, 0), F(market, 1), F(market, 2), F(market, 3)]),
 ("Twice a year, you swear an oath to keep all of it.", [F(oath, 0), F(oath, 1)]),
 ("And it orders stocks to be built in every town.", [F(stockb, 0), F(stockb, 1)]),
 ("Refuse the oath, and it's three days or more in the stocks. Break it, and it's forty days in prison. Do it again: three months.", [F(pen, 0), F(pen, 1), F(pen, 2)]),
 ("There are new judges for this. Justices of Labourers.", [F(justices, 0), F(justices, 1)]),
 ("And here's the clever part. The fines are set against the local tax bill.", [F(fines, 0), F(fines, 1)]),
 ("So every town has a reason to turn offenders in.", [F(turnin, 0), F(turnin, 1)]),
 ("In thirteen fifty-two, the justices at Coal-chester raise more than eighty-four pounds in fines. That's over twenty thousand pennies.", [F(colch, 0), F(colch, 1), F(colch, 2)]),
 ("Does it work? For a few years, it does.", [F(press, 0), F(press, 1)]),
 ("On that manor in Kent, by thirteen fifty-three, the ploughmen's cash pay has slipped back. So has most of the extra food.", [F(acct, 4), F(acct, 5)]),
 ("And in the account roll, the carter's wage is written as eleven shillings. Then it's crossed out, and changed to nine and six pence.", [F(carter, 0), F(carter, 1), F(carter, 2), F(carter, 3)]),
 ("Maybe his pay was cut. Maybe only the paperwork was. The historian who studied it thinks it may be a way round the law.", [F(maybe, 0), F(maybe, 1), F(maybe, 2), F(maybe, 3)]),
 ("Because there are ways round it. You stop calling it a wage.", [F(ways, 0), F(ways, 1)]),
 ("On one abbey's estates, the abbot pays seasonal bonuses, and hands out the grain allowance in wheat. One historian has no doubt why.", [F(abbot, 0), F(abbot, 1), F(abbot, 2), F(abbot, 3)]),
 ("A raise you can eat.", [F(eat)]),
 ("And the manor courts barely bother. One study checked eight manors. Seven never recorded a single case.", [F(courts, 0), F(courts, 1), F(courts, 2)]),
 ("Then, in thirteen sixty-one, the plague comes back. By one estimate, it kills about one in five.", [F(back61, 0), F(back61, 1), F(back61, 2)]),
 ("After that, for day wages, the law is beaten. By the early thirteen seventies, wage rates are up by more than half.", [F(press, 2), F(half, 0), F(half, 1)]),
 ("Parliament even tries to control dinner. A law of thirteen sixty-three says servants are to be served meat or fish only once a day. It's repealed the next year.", [F(dinner, 0), F(dinner, 1), F(dinner, 2), F(dinner, 3)]),
 ("The poet William Langland grumbles that labourers now turn down day-old vegetables and cheap ale. They want fresh meat and fish.", [F(langland, 0), F(langland, 1), F(langland, 2)]),
 ("Quest three, complete. You kept your raise.", [F(kept, 0)], "chime"),
 ("Didn't you?", [F(kept, 1)]),
 ("Now the hidden one. Who really got paid?", [F(hiddenq, 0, 3), F(hiddenq, 1, 3)], "chime"),
 ("Start with prices. Perhaps half the people are gone. The coins aren't.", [F(halfgone, 0), F(halfgone, 1), F(halfgone, 2)]),
 ("More money per head means everything costs more. And prices stay high until the mid thirteen seventies.", [F(infl, 0), F(infl, 1), F(infl, 2)]),
 ("For a quarter of a century, a bigger wage often buys no more than the old one did. Sometimes less.", [F(realw, 0), F(realw, 1), F(realw, 2)]),
 ("And it matters what kind of worker you are.", [F(kinds, 0)]),
 ("The day labourer nearly doubled his rate in a year.", [F(kinds, 1)]),
 ("But you're a ploughman. Hired by the year, paid mostly in grain. The king's order mentions the shortage of ploughmen by name.", [F(kinds, 2), F(kinds, 3)]),
 ("Three economic historians have gone through the accounts for workers like you.", [F(three, 0), F(three, 1)]),
 ("Their finding: on average, your pay barely moves for thirty years.", [F(famchart, 0), F(famchart, 1)]),
 ("It starts climbing in the thirteen eighties. By the fourteen thirties, it has roughly doubled.", [F(famchart, 2), F(famchart, 3)]),
 ("So the golden age of the English labourer does come, these three say. For you, it arrives a generation late.", [F(golden, 0), F(golden, 1), F(golden, 2)]),
 ("Why then? They point to three things. Land is cheap now, and day work pays, so you have other options.", [F(why, 0), F(why, 1)]),
 ("Grain prices fall and steady, so being paid in grain matters less.", [F(why, 2)]),
 ("And employers stop holding the line.", [F(why, 3)]),
 ("Just as that begins, the country explodes.", [F(explode, 0)]),
 ("Thirteen eighty. A poll tax. Twelve pence from everyone over fifteen, rich or poor.", [F(poll, 0), F(poll, 1), F(poll, 2)]),
 ("The next summer, Essex and Kent rise, and the rebels reach London.", [F(explode, 1), F(tolondon)]),
 ("At Mile End they face the king, Richard the Second, and demand an end to serfdom. One account of their demands adds an end to the wage limits.", [F(mileend, 0), F(mileend, 1), F(mileend, 2), F(mileend, 3), F(mileend, 4)]),
 ("He agrees. Charters go out. The next day, the mayor of London stabs their leader, Wat Tyler.", [F(agrees, 0), F(agrees, 1), F(smith)]),
 ("By July the charters are revoked. By November, at least fifteen hundred people have been executed or killed in battle.", [F(revoked, 0), F(revoked, 1), F(revoked, 2), F(revoked, 3)]),
 ("So the rebels lose. And then, over the next lifetime, some of what they wanted happens anyway.", [F(lose, 0), F(lose, 1), F(lose, 2)]),
 ("Parliament doesn't try another poll tax.", [F(nopoll)]),
 ("In thirteen eighty-eight, it gives ground on pay. New maximum wages, well above the old ones.", [F(caps, 0), F(caps, 1)]),
 ("And serfdom? The charters were revoked. It just withers away, over the next century.", [F(wither, 0), F(wither, 1), F(wither, 2)]),
 ("Historians put that down mostly to economics, not to the revolt. A lord who needs tenants has to offer better terms than the lord next door.", [F(econ, 0), F(econ, 1), F(econ, 2), F(econ, 3)]),
 ("That's the fourth quest. Outlast them.", [F(fourth, 0), F(fourth, 1)], "tick"),
 ("Your pay stayed down for thirty years, and the law was part of the reason. It couldn't manage forty.", [F(famchart, 4), F(famchart, 5), F(famchart, 6)]),
 ("The Statute of Labourers stayed on the books until eighteen sixty-three.", [F(books, 0), F(books, 2)]),
 ("And in an account roll from a manor in Kent, there's a carter's wage with a line through it.", [F(carter, 3), F(carter, 4)]),
 ("Eleven shillings. Somebody thought he was worth it.", [F(carter, 4), F(carter, 5)]),
 ("Quest complete.", [F(finale)], "chime"),
]

CAPTION_FIX = [("Nighton", "Knighton"), ("villens", "villeins"), ("villen", "villein"), ("Huntingdon-sheer", "Huntingdonshire"), ("Henry Brown", "Henry Broun"), ("Coal-chester", "Colchester"), ("hay-penny", "ha'penny"),
               ("thirteen forty-nine", "1349"), ("thirteen forty-eight", "1348"), ("thirteen forty-six", "1346"), ("thirteen fifty-one", "1351"), ("thirteen fifty-two", "1352"), ("thirteen fifty-three", "1353"),
               ("thirteen sixty-one", "1361"), ("thirteen sixty-three", "1363"), ("thirteen seventies", "1370s"), ("thirteen eighties", "1380s"), ("thirteen eighty-eight", "1388"), ("Thirteen eighty.", "1380."),
               ("fourteen thirties", "1430s"), ("eighteen sixty-three", "1863"), ("thirteen hundreds", "1300s"), ("fifteen hundred people", "1,500 people"), ("twenty thousand", "20,000"),
               ("eighty-four pounds", "84 pounds"), ("five hundred days", "500 days"), ("Forty to sixty percent", "40 to 60 percent"), ("forty shillings", "40 shillings"), ("forty days", "40 days"),
               ("Twenty-two names", "22 names"), ("thirty years", "30 years"), ("under sixty", "under 60"), ("over fifteen", "over 15"), ("Twelve pence", "12 pence"), ("twenty-two.", "22.")]
