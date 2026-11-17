"""EP002: You Have $1,000 in 1929. What Happens Next?   (New York, 1929-1934; money pillar)

Same contract as ep01.py: scene functions draw one still each, U lists (narration, [frames], flag).
New in this episode: most scenes move inside the still (walks, counters, charts that draw themselves,
falling paper). Every moving thing is driven by T.LT / T.LP / T.GP / T.TT, and rests in its final
state when the still is rendered for the contact sheet.
"""
from thsq import *
import math
import thsq as T
import life
G = 880
ROWS = ["PICK A HOME FOR $1,000", "GET THROUGH OCTOBER", "STILL HAVE IT IN 1933"]; HID = "TRUST A BANK AGAIN"
SKYC = {"day": ((140, 196, 226), (232, 240, 236)), "dusk": ((52, 56, 108), (238, 156, 122)), "night": ((16, 22, 48), (58, 70, 112)),
        "grey": ((146, 156, 170), (212, 214, 212)), "dawn": ((120, 170, 210), (250, 226, 190))}
BLD = {"day": ((170, 178, 200), (250, 236, 180)), "dusk": ((92, 88, 128), (255, 214, 120)), "night": ((40, 46, 80), (255, 220, 130)),
       "grey": ((150, 154, 164), (226, 222, 200)), "dawn": ((166, 172, 196), (250, 236, 180))}
PAVE = {"day": ((214, 206, 196), (176, 168, 158)), "dusk": ((150, 132, 132), (112, 98, 104)), "night": ((92, 92, 112), (66, 66, 86)),
        "grey": ((196, 192, 186), (160, 156, 150)), "dawn": ((214, 206, 196), (176, 168, 158))}
FLOOR = (190, 150, 110); BOARD = (56, 70, 64); POSTC = (72, 120, 168)
TAGS = {"margin": ("MARGIN YOU", RED), "stock": ("STOCK YOU", TEAL), "bank": ("BANK YOU", NAVY), "matt": ("MATTRESS YOU", EARTH), "post": ("POST OFFICE YOU", POSTC)}
KINDS = ["margin", "stock", "bank", "matt"]

# ---------- timing helpers ----------
def E(d=0.4, t0=0.0): return T.ease((T.LT-t0)/d)
def app(key, d=0.3, t0=0.0):
    """0..1 while something new arrives in this still; 1 if it was already on screen in the previous still."""
    return T.ease((T.LT-t0)/d) if life._new(("A", key)) else 1.0
def lerp(a, b, q): return a+(b-a)*q
def usd(v): return "$"+format(int(round(v)), ",")
def step(): return int(T.TT*5) % 2 == 0
def L(cv, t, y=120, x=W/2, size=72, **k): cv.label(x, y, t, size, **k); return cv
def Q(c, shown=4, done=0, hidden=None): c.questlog(ROWS, shown, done, hidden); return c
def card(t, sub=None, size=150, col=INK):
    c = C(); c.card(t, size, sub, col); return c

# ---------- sets ----------
def sky(c, hz, kind="day"):
    c.im.paste(life._grad(hz, *SKYC[kind]), (0, 0))
    if kind == "night":
        for i in range(50):
            x = (i*197) % W; y = (i*89) % max(60, hz-160)+10; r = 3+2*math.sin(T.TT*2+i); c.da.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=(255, 248, 236, 230))
    else:
        for i, (cx, cy, k) in enumerate(((300, 120, 1.0), (980, 70, .7), (1500, 170, .85))):
            xx = (cx+T.TT*(7+3*i)) % (W+400)-200
            for dx, dy, r in ((-70, 10, 44), (0, -14, 60), (70, 12, 46), (0, 22, 50)):
                c.da.ellipse([(xx+dx*k-r*k*1.5)*S, (cy+dy*k-r*k)*S, (xx+dx*k+r*k*1.5)*S, (cy+dy*k+r*k)*S], fill=(255, 255, 255, 205 if kind in ("day", "dawn") else 110))
def street(kind="day", hz=640, seed=3, city=True, hmax=420):
    c = C(CONC); sky(c, hz, kind)
    if city: c.skyline(hz, seed, BLD[kind][0], BLD[kind][1], hmax=hmax)
    c.rect(0, hz, W, H, PAVE[kind][0], None); c.line([(0, hz), (W, hz)], 6, INK, False)
    c.rect(0, H-64, W, H, PAVE[kind][1], None); c.line([(0, H-64), (W, H-64)], 5, INK, False)
    for i in range(7): c.line([(140+i*290, hz+8), (60+i*320, H-70)], 3, PAVE[kind][1])
    return c
def office(hz=780, win=(1160, 110, 1780, 520), kind="day", seed=5, wall=WALL):
    c = C(wall)
    if win:
        x0, y0, x1, y1 = win; c.rect(x0, y0, x1, y1, SKYC[kind][1], None); c.skyline(y1, seed, BLD[kind][0], BLD[kind][1], x0=x0+6, x1=x1-6, hmin=80, hmax=y1-y0-130)
        c.rect(x0, y0, x1, y1, None, INK, 9); c.line([((x0+x1)/2, y0), ((x0+x1)/2, y1)], 7); c.line([(x0, (y0+y1)/2), (x1, (y0+y1)/2)], 7); c.rect(x0-20, y1, x1+20, y1+24, WOOD, INK, 5)
    c.rect(0, hz, W, H, FLOOR, None); c.line([(0, hz), (W, hz)], 6, INK, False)
    for i in range(1, 8): c.line([(i*260-60, hz+6), (i*280-180, H)], 3, (170, 132, 96))
    return c
DX = [300, 740, 1180, 1620]; DX5 = [240, 600, 960, 1320, 1680]; DCOL = [RED, TEAL, NAVY, EARTH, POSTC]; DNAME = ["MARGIN", "STOCK", "BANK", "MATTRESS", "POST OFFICE"]
def hall(names=0, dim=(), open=None, stag=False, xs=DX, w=250, skip=()):
    c = C((232, 220, 204)); c.rect(0, 800, W, H, FLOOR, None); c.line([(0, 800), (W, 800)], 6, INK, False)
    for i in range(1, 9): c.line([(W/2+(i-4.5)*260, 806), (W/2+(i-4.5)*520, H)], 3, (170, 132, 96))
    for i, x in enumerate(xs):
        if i in skip or (stag and app(("dr", i), 0.01, i*0.32) <= 0): continue
        c.door(x, 800, w, 430, i+1, DCOL[i], DNAME[i] if i < names else None, open[i] if open else 0, dim=i in dim)
    return c
def bankhall():
    c = C(MARBLE); c.rect(0, 820, W, H, (214, 206, 196), None); c.line([(0, 820), (W, 820)], 6, INK, False)
    for i in range(9):
        for j in range(2):
            if (i+j) % 2 == 0: c.poly([(i*240-120+j*60, 826+j*128), (i*240+120+j*60, 826+j*128), (i*240+180+j*60, 954+j*128), (i*240-60+j*60, 954+j*128)], (196, 188, 178), None)
    for x in (90, 1830): c.rect(x-50, 0, x+50, 820, WHITE, INK, 6); c.rect(x-70, 770, x+70, 820, WHITE, INK, 6)
    return c
def bedroom():
    c = C((222, 204, 196)); c.rect(1380, 130, 1740, 470, (30, 38, 78), INK, 9); c.ell(1600, 180, 1680, 260, CREAM, None)
    for i in range(9): x = 1400+(i*83) % 320; y = 150+(i*57) % 300; c.ell(x, y, x+6, y+6, PAPER, None)
    c.line([(1560, 130), (1560, 470)], 7); c.line([(1380, 300), (1740, 300)], 7); c.rect(1360, 470, 1760, 494, WOOD, INK, 5)
    c.rect(0, 840, W, H, (176, 136, 100), None); c.line([(0, 840), (W, 840)], 6, INK, False)
    for i in range(1, 8): c.line([(i*260-60, 846), (i*280-180, H)], 3, (156, 118, 86))
    return c
def floor_bg():
    c = C((132, 106, 86)); c.rect(0, 760, W, H, (176, 138, 100), None); c.line([(0, 760), (W, 760)], 6, INK, False)
    c.rect(120, 80, 1800, 430, BOARD, INK, 8, 8)
    for r in range(4):
        for i in range(12):
            x = 160+i*136; y = 118+r*74; c.rect(x, y, x+110, y+50, (74, 94, 84), None); c.line([(x+12, y+25), (x+56+((i*7+r*5) % 4)*12, y+25)], 5, (210, 230, 200))
    return c
def slips(c, n=16, ymax=760):
    for i in range(n):
        x = (i*137+T.TT*46*(1+i % 3)) % (W+80)-40; y = (i*89+T.TT*130*(1+(i % 4)*.3)) % ymax; a = T.TT*3+i
        dx, dy = 22*math.cos(a), 22*math.sin(a); c.poly([(x-dx, y-dy), (x+dy*.5, y-dx*.5), (x+dx, y+dy), (x-dy*.5, y+dx*.5)], PAPER, INK, 3)

# ---------- cast ----------
def chip(c, x, y, t, col, size=40):
    w = c.tw(t, size)+36; x = min(max(x, w/2+20), W-w/2-20); c.rect(x-w/2, y-size*.72, x+w/2, y+size*.72, col, INK, 5, 12); c.text(x, y-3, t, size, PAPER)
def you(c, x, y, h, kind, pose="stand", ex="n", tag=True, dy=0, **k):
    f = c.fig(x, y, h, pose, ex, "modern", **k)
    if tag and kind and not k.get("rot"): t, col = TAGS[kind]; chip(c, f["head"][0], f["head"][1]-h*.2-28+dy, t, col, max(38, h*.125))
    return f
def bandage(c, f):
    u = f["u"]; x, y = f["head"]; c.line([(x-.5*u, y+.2*u), (x-.1*u, y+.02*u)], u*.16, INK, False); c.line([(x-.5*u, y+.2*u), (x-.1*u, y+.02*u)], u*.1, WHITE, False)
    c.line([(x-.42*u, y+.02*u), (x-.2*u, y+.22*u)], u*.16, INK, False); c.line([(x-.42*u, y+.02*u), (x-.2*u, y+.22*u)], u*.1, WHITE, False)
def walker(c, key, x0, x1, y, h, d=1.0, t0=0.0, rest="stand", ex="n", kind=None, tag=False, flip=False):
    q = app(key, d, t0); x = lerp(x0, x1, q); mv = 0.02 < q < 0.98
    return you(c, x, y, h, kind, ("walk" if step() else "stand") if mv else rest, ex, tag, flip=(x1 < x0) if mv else flip)
def arrow(c, x0, y0, x1, y1, col=INK, w=12, head=34):
    a = math.atan2(y1-y0, x1-x0); c.line([(x0, y0), (x1, y1)], w, col, False)
    for s in (-1, 1): c.line([(x1, y1), (x1-head*math.cos(a+s*.5), y1-head*math.sin(a+s*.5))], w, col, False)
def minibank(c, x, y, k=1.0, closed=True):
    c.rect(x-60*k, y-70*k, x+60*k, y, MARBLE, INK, 5*k); c.poly([(x-72*k, y-70*k), (x, y-116*k), (x+72*k, y-70*k)], MARBLE, INK, 5*k)
    for dx in (-36, 0, 36): c.rect(x+(dx-8)*k, y-62*k, x+(dx+8)*k, y, WHITE, INK, 3*k)
    if closed: c.line([(x-58*k, y-84*k), (x+58*k, y+6*k)], 13*k, RED, False); c.line([(x+58*k, y-84*k), (x-58*k, y+6*k)], 13*k, RED, False)

# ================= cold open =================
def cold(k):
    c = street("day", 640, 3)
    s = c.fig(620, G+50, 400, "hold", "smile", "modern"); hx, hy = s["hand"]; c.cash(hx+70, hy+40, 8, 1.15)
    if k >= 1: L(c, "$1,000", 330, 1250, 150, bg=MARI)
    return c
def pay(k):
    c = C()
    if k == 0:
        n = int(8*app("m8", 1.3)+.5)
        for i in range(8):
            x = 300+(i % 4)*300; y = 300+(i//4)*340
            if i < n: c.calpage(x, y, .8, "MONTH", str(i+1))
            else: c.rect(x-104, y-128, x+104, y+128, None, (224, 214, 198), 5, 10)
        c.fig(1630, 900, 330, "write", "det", "modern"); L(c, "ABOUT 8 MONTHS' PAY", 990, 760, 84, bg=MARI)
    else:
        q = app("y4", 1.5)
        for i in range(4):
            x = 330+i*420; c.calpage(x, 300, .8, "YEAR", "'"+str(26+i))
            c.cash(x, 800, int((2+i*2)*min(1, q*4/(i+1))+.5), 1.25)
        L(c, "4 YEARS OF SAVING", 950, size=84, bg=MARI)
    return c
def fates(k):
    c = C(); caps = [("GONE IN TWO DAYS", RED), ("SHRINKS TO $110", INK), ("OR BUYS MORE", TEAL)]
    for i in range(min(k+1, 3)):
        x = 96+i*586; a = app(("fate", i), 1.0, 0.25); cx = x+270
        c.rect(x, 200, x+540, 820, WHITE, INK, 7, 18)
        if i == 0:
            n = int(8*(1-a)+.5); c.cash(cx, 720, n, 1.4)
            if n == 0:
                c.text(cx, 520, "$0", 220, RED)
                for j in range(8): b = j*45; c.line([(cx+150*math.cos(math.radians(b)), 520+150*math.sin(math.radians(b))), (cx+200*math.cos(math.radians(b)), 520+200*math.sin(math.radians(b)))], 9, RED)
        if i == 1:
            n = int(8-7*a+.5); c.cash(cx, 720, n, 1.4); c.text(cx, 360, usd(lerp(1000, 110, a)), 130)
        if i == 2:
            c.cash(cx-110, 720, 8, 1.15); arrow(c, cx+140, 720, cx+140, 720-330*max(.15, a), TEAL, 22, 60)
        c.text(cx, 900, caps[i][0], 64, caps[i][1])
    return c
def where(k):
    c = hall(0, dim=(0, 1, 2, 3)); c.fig(880, 1020, 340, "chin", "n", "modern"); c.cash(1090, 1020, 8, .95)
    if k: L(c, "IT DEPENDS WHERE YOU PUT IT", 110, size=78)
    return c
def four(k):
    c = C(); q = app("split4", 0.9); xs = [330, 750, 1170, 1590]
    for i, x in enumerate(xs):
        xx = lerp(960, x, q); s = c.fig(xx, 880, 330, "hold", ["smile", "n", "smug", "worry"][i] if q > .95 else "wow", "modern"); c.cash(s["hand"][0]+56, s["hand"][1]+34, 6, .8)
        if q > .95: c.ell(xx-52, 250, xx+52, 354, DCOL[i], INK, 7); c.text(xx, 298, str(i+1), 80, PAPER)
    if k: L(c, "WHICH YOU SURVIVES?", 990, size=84, bg=MARI)
    return c
def intro(k):
    c = C(); s = c.fig(W/2, 900-(1-T.ease(T.LT/0.3))*900*(k == 0), 520, "drop" if k == 0 else "self", "wow" if k == 0 else "smile", "modern")
    c.marker(s["head"][0]+20, s["head"][1]-110, 46)
    if k: L(c, "YOU", 160, 1400, 120)
    return c
def clerk(k=0):
    c = office(); c.desk(110, 960, 600, 180); c.typewriter(360, 780, 1.35)
    for i in range(5): c.rect(560, 772-i*10, 680, 780-i*10, WHITE, INK, 3)
    f = c.fig(840, 970, 340, "write", "det" if k != 1 else "smile", "modern", flip=True)
    if k == 1: c.marker(f["head"][0]-10, f["head"][1]-90, 34); L(c, "AGE 24. CLERK. NEW YORK CITY.", 80, 560, 62)
    return c
def qoffice(shown, done=0): return Q(clerk(0), shown, done)

# ================= the mood =================
DOW20 = [(1921.65, 63), (1922, 81), (1923, 99), (1924, 96), (1925, 121), (1926, 157), (1927, 157), (1928, 202), (1929, 300), (1929.67, 381)]
def norm(pts, x0, x1, ymax): return [((x-x0)/(x1-x0), y/ymax) for x, y in pts]
def climb(k):
    c = C(); box = c.chartbox(110, 190, 1320, 900, "THE DOW JONES INDUSTRIAL AVERAGE")
    for i in range(9): c.text(box[0]+(box[2]-box[0])*(i+.35)/8.02, 945, "'"+str(21+i), 44, (120, 110, 98))
    tip = c.plot(box, norm(DOW20, 1921.65, 1929.67, 420), app("climb", 2.2), RED, 13, True, (250, 226, 214))
    c.fig(1610, 930, 360, "point" if k else "chin", "wow" if k == 2 else "smile", "modern", flip=True)
    if k >= 1: L(c, "1921: 63", 690, 360, 70)
    if k >= 2: L(c, "SEPT 1929: 381", 250, 1020, 78, bg=MARI)
    if k >= 3: L(c, "EIGHT YEARS OF UP", 330, 520, 70)
    return c
def six(k):
    if k == 0:
        c = C(); c.line([(240, 880), (1180, 880)], 7); g = app("grow6", 0.9)
        c.rect(380, 880-63*1.5, 560, 880, GREY, INK, 7, 6); c.text(470, 940, "1921", 60); c.text(470, 880-63*1.5-50, "63", 70)
        hh = lerp(63, 381, g)*1.5; c.rect(800, 880-hh, 980, 880, RED, INK, 7, 6); c.text(890, 940, "1929", 60); c.text(890, 880-hh-50, str(int(lerp(63, 381, g))), 70)
        c.text(1500, 520, "×6", 380*(0.7+0.3*app("x6", 0.3, 0.8)), RED)
        return c
    c = office(); a = c.person(520, 950, 340, "wave", "joy", "teal", None, RED); c.fig(1010, 950, 330, "stand", "wow" if k == 1 else "bored", "modern", flip=True)
    c.bubble(520, 250, "I KNOW A GUY\nWHO GOT RICH!", 70, (-10, 70))
    if k == 2: c.person(200, 950, 320, "wave", "joy2", "rose", "cloche"); c.person(1500, 950, 330, "wave", "joy", "blue", "cap", flip=True); c.bubble(1560, 600, "ME TOO!", 60, (-20, 30)); c.bubble(230, 590, "SO DO I!", 56, (-20, 30))
    return c
def dots(k):
    c = C()
    for i in range(80):
        col, row = i % 16, i//16; x = 210+col*100; y = 300+row*118; hot = (i == 37)
        c.line([(x, y+20), (x, y+56)], 22, INK, False); c.line([(x, y+20), (x, y+56)], 14, RED if hot else GREY, False); c.ell(x-21, y-26, x+21, y+16, PAPER, INK, 5)
    x, y = 210+5*100, 300+2*118; p = 1+.08*math.sin(T.TT*6); c.ell(x-62*p, y-52*p, x+62*p, y+84*p, None, RED, 9)
    if k == 0: L(c, "ALMOST NOBODY IS THAT GUY", 130, size=84)
    if k >= 1: L(c, "ABOUT 1.5 MILLION BROKER ACCOUNTS", 130, size=74)
    if k >= 2: L(c, "IN A COUNTRY OF 120 MILLION: ROUGHLY 1 IN 80", 990, size=60, bg=MARI)
    return c
def loud(k=0, t="I GOT RICH!"):
    c = C((244, 232, 214)); c.rect(0, 860, W, H, FLOOR, None); c.line([(0, 860), (W, 860)], 6, INK, False)
    for i, x in enumerate((170, 360, 1560, 1760)): c.person(x, 930+(i % 2)*40, 280, "stand", ["bored", "n", "bored", "worry"][i], ["slate", "brown", "green", "blue"][i], [None, "cap", "cloche", None][i], flip=x > 900)
    g = c.person(820, 960, 420, "hold", "joy", "red", "bowler", TEAL); hx, hy = g["hand"]; c.megaphone(hx+30, hy-20, 1.5+.08*math.sin(T.TT*14))
    w = 1+0.05*math.sin(T.TT*9); c.bubble(1400, 300, t, 96*w, (-170, 110))
    if k: L(c, "THE LOUD ONES", 150, 420, 76, bg=MARI)
    return c

# ================= four doors =================
def doors0(k=0): return hall(0, stag=True)
def doorhi(i, k=0):
    c = hall(i+1, dim=[j for j in range(4) if j != i], open=[0.85*app(("dopen", i), .5, .3) if j == i else 0 for j in range(4)])
    return c
def broker(k):
    c = C((200, 212, 194)); c.rect(0, 800, W, H, FLOOR, None); c.line([(0, 800), (W, 800)], 6, INK, False)
    c.rect(1010, 90, 1810, 470, BOARD, INK, 8, 8); c.text(1410, 140, "TODAY'S PRICES", 52, PAPER)
    for r in range(4):
        y = 214+r*62; c.line([(1060, y), (1250+(r*37) % 90, y)], 7, (210, 230, 200)); up = 12*math.sin(T.TT*4+r)
        c.poly([(1600, y+14), (1630, y-22-up*.3), (1660, y+14)], (150, 220, 150), None); c.line([(1690, y), (1770, y)], 7, (210, 230, 200))
    c.tickerm(830, 800, 1.25, 230, T.TT*5)
    b = c.person(1420, 880, 350, "point", "smug", "broker", None, RED, flip=True); c.desk(1150, 950, 560, 170); c.cert(1330, 760, .42, "STOCK")
    s = c.fig(400, 940, 350, "hold", "smile", "modern"); c.cash(s["hand"][0]+56, s["hand"][1]+34, 8, .85)
    if k == 1: L(c, "DOOR 1: THE BROKER", 130, 480, 76)
    if k == 2: L(c, "BUYING ON MARGIN", 130, 480, 84, bg=MARI)
    return c
BX, BY, BW, BH = 220, 560, 144, 170
def bar(c, nyou=1, nloan=9, lq=1.0, yq=1.0, y=BY, x=BX, bw=BW, bh=BH):
    for i in range(nyou+nloan):
        xx = x+i*bw
        if i < nyou: yy = y-(1-yq)*520; c.rect(xx, yy-bh, xx+bw-8, yy, MARI, INK, 7, 8)
        else: x2 = xx+(1-lq)*1700; c.rect(x2, y-bh, x2+bw-8, y, NAVY, INK, 7, 8)
def brace(c, x0, x1, y, t, size=84, col=INK):
    c.line([(x0, y+26), (x0, y), (x1, y), (x1, y+26)], 7, col); c.text((x0+x1)/2, y-56, t, size, col)
def slice_(k):
    c = C(); a = app("yours", .5); b = app("loan", .8, .15) if k >= 1 else 0
    bar(c, 1, 9 if k >= 1 else 0, b, a)
    if a > .95: c.text(BX+BW/2-4, BY-BH/2, "YOU", 56)
    if k >= 1 and b > .95: c.text(BX+BW*5.5, BY-BH/2, "THE BROKER'S LOAN", 84, PAPER)
    c.fig(BX+BW/2+6, 990, 260, "up", "smile", "modern")
    if k >= 1: c.person(lerp(2100, BX+BW*5.5, b), 990, 270, "up", "smug", "broker", None, RED)
    if k == 0: L(c, "YOU PUT DOWN A SLICE", 160, 1180, 80)
    if k == 1: L(c, "THE BROKER LENDS THE REST", 160, 1080, 80)
    if k == 2: L(c, "AS LITTLE AS 10% DOWN", 190, size=96, bg=MARI)
    if k >= 3: brace(c, BX, BX+10*BW-8, BY-BH-36, (usd(lerp(1000, 10000, app("ten", 1.0, .15)))+" OF STOCK") if k < 5 else "$11,000 OF STOCK", 92); c.text(BX+BW*1.5+70, BY+74, "YOUR $1,000", 62, RED)
    if k >= 4:
        g = app("gain", .7); c.rect(BX+10*BW, BY-BH*g, BX+11*BW-8, BY, TEAL, INK, 7, 8)
        if g > .9: c.text(BX+10.5*BW-4, BY-BH/2, "+10%", 50, PAPER)
    if k == 4: L(c, "PRICES RISE 10%", 150, 1500, 70)
    if k == 5: L(c, "THE LOAN: STILL $9,000", 780, 1470, 62); L(c, "YOURS: $2,000", 920, 1470, 84, bg=MARI)
    return c
def radio(k):
    c = C((236, 222, 204)); c.rect(0, 830, W, H, FLOOR, None); c.line([(0, 830), (W, 830)], 6, INK, False)
    for i in range(3):
        r = 250+i*90+(T.TT*70) % 90; al = int(max(0, 150-(r-250)*.5)); c.da.arc([(960-r)*S, (500-r)*S, (960+r)*S, (500+r)*S], 200, 340, fill=(224, 79, 58, al), width=10*S)
    c.rect(800, 700, 1120, 830, WOOD, INK, 7, 6); c.radio(960, 700, 1.5)
    for i, x in enumerate((230, 470, 1450, 1690)): c.person(x, 930+(i % 2)*40, 310, "up" if i % 2 else "cheer", ["joy", "wow", "joy2", "joy"][i], ["green", "rose", "blue", "brown"][i], ["cap", "cloche", "fedora", None][i], flip=x > 960)
    L(c, "THE STOCK EVERYBODY WANTS: RADIO", 100, size=72)
    if k: L(c, "\"RADIO\" = R.C.A.", 1000, size=84, bg=MARI)
    return c
def pool(k):
    c = C(); box = c.chartbox(760, 260, 1800, 850); c.text(1280, 900, "RADIO, MARCH 1929 (SKETCH, NOT TO SCALE)", 44, (120, 110, 98))
    if k == 0:
        q = app("pump", 1.6); c.plot(box, [(0, .25), (.25, .3), (.25+.45*q, .3+.52*q)], 1, RED, 13)
    else:
        q = app("dump", 1.2); c.plot(box, [(0, .25), (.25, .3), (.7, .82), (.7+.26*q, .82-.5*q)], 1, RED, 13)
    fs = [c.person(x, 950, 330, "up" if k == 0 else "hold", "smug" if k else "det", "banker", "top", [RED, TEAL, MARI][i]) for i, x in enumerate((170, 370, 570))]
    if k >= 1:
        for f in fs: c.moneybag(f["hand"][0]+60, f["hand"][1]+100, .8)
    if k == 0: L(c, "A POOL OF INSIDERS PUSHES IT UP", 100, 620, 62)
    if k == 1: L(c, "THEN THEY SELL EVERYTHING", 100, 620, 68)
    if k == 2: L(c, "THEN THEY SELL EVERYTHING", 100, 620, 68); L(c, "LEGAL AT THE TIME", 1010, 1280, 84, bg=MARI)
    return c
def outright(k):
    c = C(); c.rect(BX, BY-BH, BX+BW-8, BY, MARI, INK, 7, 8); c.text(BX+BW/2-4, BY-BH/2, "YOU", 56)
    for i in range(1, 10): c.rect(BX+i*BW, BY-BH, BX+(i+1)*BW-8, BY, None, (222, 212, 196), 5, 8)
    s = c.fig(BX+BW/2+40, 990, 260, "hold", "smile", "modern"); c.cert(s["hand"][0]+130, s["hand"][1]+10, .8, "RADIO")
    L(c, "DOOR 2: SAME BROKER, NO LOAN", 190, size=80)
    if k: L(c, "$1,000 OF STOCK. BOUGHT AND PAID FOR.", 760, 1150, 60, bg=MARI)
    return c
def bankext(k):
    c = street("day", 620, 4); c.bankfront(820, 900, 700, 460, "CORNER BANK")
    walker(c, "tobank", 150, 560, 960, 330, 1.4, rest="hold", ex="smile")
    if k: L(c, "DOOR 3: THE BANK ON THE CORNER", 110, 620, 66)
    return c
def counter(c, tex="smile", gap=130):
    t = c.person(1300, 800, 330, "hold", tex, "banker", None, TEAL, flip=True)
    c.rect(880, 610, 1740, 840, WOOD, INK, 7, 6); c.rect(860, 586, 1760, 620, (120, 84, 58), INK, 6, 4)
    for x in range(900, 1741, 56):
        if abs(x-1300) > gap: c.line([(x, 586), (x, 330)], 9, BRASS, False)
    c.line([(880, 330), (1740, 330)], 14, BRASS, False); c.line([(1300-gap, 440), (1300-gap, 330)], 9, BRASS, False); c.line([(1300+gap, 440), (1300+gap, 330)], 9, BRASS, False)
    c.rect(1180, 250, 1420, 318, PAPER, INK, 5, 8); c.text(1300, 282, "TELLER", 50)
    return t
def teller(k):
    c = bankhall(); counter(c)
    s = walker(c, "toteller", 330, 660, 930, 350, 1.0, rest="hold", ex="smile");
    if app("toteller", 1.0) >= 1: c.cash(s["hand"][0]+56, s["hand"][1]+34, 8, .85)
    if k >= 1: L(c, "MARBLE COLUMNS. BRASS RAILS.", 130, 560, 66)
    if k >= 2: L(c, "AND IT PAYS YOU INTEREST", 1000, 620, 76, bg=MARI)
    return c
def mattress(k):
    c = bedroom(); c.bed(430, 930, 800, lift=.75*app("lift", .5, .2), cashn=4, k=1.3)
    c.fig(1500, 960, 340, "point", "smile" if k < 3 else "worry", "modern", flip=True)
    if k == 0: L(c, "DOOR 4: THE MATTRESS", 130, 560, 76)
    for i in range(min(k, 3)): L(c, ["NO INTEREST", "NO RISK", "NO RESPECT"][i], 130+i*124, 380, 76, bg=MARI if i == 2 else PAPER)
    return c
def laugh(k):
    c = office(win=(1240, 110, 1800, 480)); j = 6*math.sin(T.TT*16)
    c.person(330, 950+j, 330, "point", "joy", "teal", None, RED); c.person(590, 950-j, 310, "point", "joy2", "rose", "cloche")
    c.fig(1060, 950, 320, "shrug", "worry", "modern", flip=True); c.bubble(500, 240, "DOOR FOUR? HA!", 72, (-60, 90))
    if k: L(c, "\"AFRAID OF MONEY\"", 1000, 760, 76, bg=MARI)
    return c
def split(k, done=0):
    op = .85*app("open4", .5) if k >= 1 else 0; c = hall(0, open=[op]*4)
    for i in range(4):
        if k == 0: you(c, DX[i], 1020, 250, KINDS[i], "stand", ["smile", "n", "smug", "bored"][i], dy=-(i % 2)*0)
        elif k == 1:
            q = app(("walkin", i), 1.1, .45+i*.2)
            if q < 1: you(c, DX[i]+20, lerp(1020, 800, q), lerp(250, 190, q), KINDS[i], "walk" if step() else "stand", "n", tag=q < .5)
    if k == 2: L(c, "ONE OF YOU BEHIND EACH DOOR", 110, 520, 62)
    if done: Q(c, 4, done)
    return c

# ================= October =================
def peak(k):
    if k < 2:
        c = C(); c.calpage(330, 500, 1.3, "SEPT", "3", "1929"); box = c.chartbox(740, 250, 1800, 880)
        tip = c.plot(box, [(0, .2), (.2, .36), (.4, .32), (.6, .56), (.8, .7), (1, .9)], app("pk", 1.1), RED, 13)
        if k == 1: L(c, "THE DOW CLOSES AT 381", 150, 1270, 76, bg=MARI)
        return c
    c = C((236, 226, 210)); c.rect(0, 0, W, 90, WOOD, INK, 6); c.line([(960, 90), (960, 200)], 9, (90, 84, 80)); c.bell(960, 200, 2.3)
    for dx in (-230, 230): c.text(960+dx, 330, "...", 120, (150, 140, 128))
    c.fig(520, 980, 330, "shrug", "bored", "modern"); L(c, "NOBODY RINGS A BELL AT THE TOP", 1000, 1200, 62)
    return c
def slide(k):
    c = C(); c.calpage(300, 500, 1.2, "1929", "SEPT" if k == 0 else "OCT"); box = c.chartbox(700, 250, 1800, 880)
    pts = [(0, .9), (.14, .84), (.3, .72), (.46, .62), (.62, .7), (.78, .79)]
    if k == 0: c.plot(box, pts[:4], app("sl", 1.2), RED, 13); L(c, "DOWN ABOUT 10%", 760, 1050, 76, c=RED)
    else: c.plot(box, pts, lerp(.46/.78, 1, app("bn", 1.0)), RED, 13); L(c, "THEN A BOUNCE", 790, 1280, 76, c=TEAL)
    return c
def fisher(k):
    c = C((226, 214, 196)); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
    c.rect(960, 150, 1800, 660, BOARD, INK, 9, 6); c.rect(940, 660, 1820, 690, WOOD, INK, 5)
    c.line([(1020, 600), (1020, 210)], 6, PAPER); c.line([(1020, 600), (1750, 600)], 6, PAPER)
    c.line([(1030, 570), (1180, 480), (1330, 340), (1440, 300), (1640, 300)], 12, PAPER); c.text(1500, 240, "PLATEAU", 64, PAPER)
    if k == 3:
        q = app("crk", .9, .3); c.line([(1640, 300), (1640+70*q, 300+270*q)], 12, RED, False); c.text(1700, 420, "?", 110*q+1, RED)
    c.rect(300, 640, 520, 870, WOOD, INK, 7, 6); c.rect(280, 610, 540, 650, WOOD, INK, 6, 4)
    e = c.person(660, 950, 370, "point", "smug" if k < 3 else "worry", "brown", None, RED); c.glasses(e)
    if k == 0: L(c, "A FAMOUS YALE ECONOMIST, MID-OCTOBER", 80, 560, 54)
    if k in (1, 2): c.bubble(480, 250, "STOCK PRICES HAVE REACHED...", 50, (60, 90))
    if k == 2: L(c, "\"A PERMANENTLY HIGH PLATEAU\"", 1000, size=72, bg=MARI)
    if k == 3: L(c, "FAMOUS FOR A DIFFERENT REASON, SOON", 1000, size=62)
    return c
def crowd(c, xs, y=960, exs=("wow", "worry", "strain", "angry"), poses=("up", "cheer", "shrug", "wave"), h=300, hat=True):
    coats = ["slate", "brown", "green", "blue", "rose", "banker", "teal"]; hats = ["fedora", "bowler", "cap", None, "fedora"]
    return [c.person(x, y+(i % 3)*36, h-(i % 2)*20, poses[i % len(poses)], exs[i % len(exs)], coats[i % 7], hats[i % 5] if hat else None, flip=i % 2 == 1) for i, x in enumerate(xs)]
def floor(k):
    c = floor_bg(); c.tickerm(180, 1040, 1.2, 380, T.TT*6); crowd(c, [520, 720, 920, 1120, 1320, 1520, 1720]); slips(c)
    if k == 0: c.calpage(300, 300, .85, "OCT", "24", "THURSDAY")
    if k >= 1: L(c, "NEARLY 13 MILLION SHARES", 210, 1000, 86)
    if k >= 2: L(c, "A RECORD", 350, 1000, 90, bg=MARI)
    return c
def bankers(k):
    c = floor_bg(); crowd(c, [170, 360, 1620, 1790], 960, ("wow", "n", "wow", "worry"), ("stand", "stand", "shrug", "stand")); slips(c, 7)
    for i in range(3):
        x = lerp(2150+i*190, 780+i*210, app(("bk", i), 1.3)); mv = app(("bk", i), 1.3) < .98
        f = c.person(x, 1000, 360, ("walk" if step() else "stand") if mv else ("up" if i == 1 else "stand"), "det", "banker", "top", [RED, MARI, TEAL][i], flip=mv)
        if i == 1 and not mv: hx, hy = f["hand"]; c.line([(hx, hy), (hx, hy-150)], 10, WOOD); c.rect(hx-150, hy-300, hx+150, hy-140, PAPER, INK, 7, 10); c.text(hx, hy-224, "BUY", 110, TEAL)
    if k >= 1: L(c, "THE BIG BANKERS BUY. IN PUBLIC.", 250, size=76)
    if k >= 2: L(c, "TO SHOW EVERYONE IT'S FINE", 380, size=66, bg=MARI)
    return c
def weekend(k=0):
    c = C(); days = [("FRI", "25"), ("SAT", "26"), ("SUN", "27")]
    for i, (a, b) in enumerate(days):
        q = app(("wk", i), .3, i*.55)
        if q > 0: c.calpage(480+i*480, 400-(1-q)*60, 1.05, "OCT", b, a)
    c.line([(240, 800), (1680, 800)], 7); c.line([(260, 760+4*math.sin(T.TT*3)), (700, 756), (1100, 762+4*math.sin(T.TT*2)), (1660, 758)], 14, TEAL)
    L(c, "IT HOLDS FOR A WEEKEND", 940, size=80)
    return c
def monday(k):
    c = C(); c.calpage(310, 500, 1.3, "OCT", "28", "MONDAY"); box = c.chartbox(740, 250, 1800, 880)
    c.plot(box, [(0, .84), (.2, .82), (.4, .8), (.55, .78), (1, .22)], lerp(.55, 1, app("mon", 1.0, .2)), RED, 14)
    if k >= 1: c.text(1180, 640, "-13%", 250*(.7+.3*app("m13", .25)), RED)
    if k >= 2: L(c, "IN ONE DAY", 1000, 1270, 90, bg=MARI)
    return c
def myou(k):
    c = C(); bar(c, 1, 9); c.text(BX+BW*5.5, BY-BH/2, "THE BROKER'S LOAN", 84, PAPER)
    if k == 0: c.text(BX+BW/2-4, BY-BH/2, "YOU", 56); brace(c, BX, BX+10*BW-8, BY-BH-36, "$10,000 OF STOCK", 92)
    if k >= 1:
        q = app("bite", 1.0, .2); w = 1.3*BW*q; c.rect(BX, BY-BH, BX+w, BY, RED, INK, 7, 8)
        for i in range(int(w/36)): c.line([(BX+12+i*36, BY-12), (BX+40+i*36, BY-BH+12)], 6, (160, 40, 30))
        brace(c, BX, BX+1.3*BW, BY-BH-36, "-13% = -$1,300", 92, RED)
    you(c, BX+BW/2+16, 1000, 260, "margin", "self" if k < 2 else "shrug", "worry" if k < 2 else "wow")
    if k >= 2: L(c, "YOUR $1,000: GONE", 760, 1250, 84)
    if k >= 3: L(c, "PLUS $300 YOU NEVER HAD", 900, 1250, 76, bg=MARI)
    return c
def call(k):
    c = C((200, 212, 194)); c.rect(960, 0, W, H, WALL, None); c.rect(0, 830, W, H, FLOOR, None); c.line([(0, 830), (W, 830)], 6, INK, False); c.line([(960, 0), (960, H)], 12, INK, False)
    b = c.person(430, 960, 380, "hold", "angry", "broker", None, RED); c.phone(b["hand"][0]+60, b["hand"][1]+150, .9)
    c.rect(1180, 700, 1420, 724, WOOD, INK, 5); c.line([(1300, 724), (1300, 900)], 14, WOOD); c.phone(1300, 700, 1.0, T.TT+.01)
    you(c, 1620, 960, 350, "margin", "shrug", "wow", flip=True)
    if k == 0: L(c, "THE BROKER DOESN'T WAIT", 110, 480, 62)
    if k >= 1:
        q = app("tele", .3); c.rect(960-470*q, 230-140*q, 960+470*q, 230+140*q, CREAM, INK, 8, 14)
        if q > .9: c.text(960, 184, "MARGIN CALL", 120, RED); c.text(960, 300, "PAY TODAY, OR WE SELL YOUR SHARES", 50)
    if k >= 2: c.bubble(1330, 480, "TODAY?!", 70, (110, 30))
    return c
def sell(k):
    if k == 0:
        c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
        f = you(c, 760, 980, 420, "margin", "shrug", "sad"); u = f["u"]
        for sx in (-1, 1): c.poly([(760+sx*.5*u, 980-1.55*u), (760+sx*.95*u, 980-1.4*u), (760+sx*.6*u, 980-1.15*u)], PAPER, INK, 5)
        L(c, "YOU CAN'T PAY", 480, 1400, 100)
        return c
    if k == 1:
        c = C((200, 212, 194)); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
        c.cert(1180, 500, 2.3, "YOUR SHARES"); q = app("stamp", .25, .5); z = 2.2-1.2*q
        if T.LT > .5 or q >= 1: c.rect(1180-280*z, 520-90*z, 1180+280*z, 520+90*z, None, RED, 16*z, 12); c.text(1180, 516, "SOLD", 150*z, RED)
        c.person(430, 980, 400, "up", "det", "broker", None, RED)
        return c
    c = street("dusk", 760, 7, hmax=560); spots = [(260, 330), (620, 210), (930, 380), (1250, 230), (1560, 360), (1760, 160), (430, 520), (1100, 560)]
    for i, (x, y) in enumerate(spots):
        q = app(("sellb", i), .2, .12+i*.22)
        if q > 0: c.bubble(x, y-(1-q)*30, "SELL!", 64*q+2, (-30+(i % 3)*30, 50), RED)
    pts = [(0, 800), (300, 830), (620, 880), (980, 930), (1400, 990), (W, 1040)]; qq = app("fallline", 2.2)
    c.plot((0, 0, W, 1), [(x/W, 1-y) for x, y in pts], qq, RED, 14, True)
    if k == 3: L(c, "EVERY BROKER. SAME MOMENT. SAME FALLING MARKET.", 1010, size=56, bg=MARI)
    return c
def tuesday(k):
    c = C((236, 226, 210)); c.rect(0, 860, W, H, FLOOR, None); c.line([(0, 860), (W, 860)], 6, INK, False)
    c.calpage(330, 430, 1.25, "OCT", "29", "TUESDAY"); c.tickerm(900, 860, 1.5, 520, T.TT*7)
    for j in range(3):
        pts = [(1000+i*80, 930+j*46+18*math.sin(i*1.3+j+T.TT*4)) for i in range(11)]; c.line(pts, 19, INK, False); c.line(pts, 13, PAPER, False)
    if k >= 1: L(c, "16 MILLION SHARES", 180, 1330, 90)
    if k >= 2: L(c, "DOWN NEARLY 12% MORE", 330, 1330, 78, c=RED)
    return c
def out(k):
    c = hall(4, dim=(0,)); c.redx(DX[0], 580, 140, 34); c.fig(720, 1016, 290, "cheer", "pain", "modern", rot=-90); chip(c, 520, 936, "MARGIN YOU", RED, 40)
    L(c, "OUT IN TWO DAYS", 110, size=96, c=RED)
    if k: c.text(1250, 1000, "$0", 160, RED)
    return c
def fair(k):
    c = C(); bw = 118
    for r, (ny, lab) in enumerate(((1, "10% DOWN"), (4.5, "40-50% DOWN"))):
        y = 430+r*300
        for i in range(10):
            x = 560+i*bw; c.rect(x, y-140, x+bw-8, y, NAVY, INK, 6, 8)
        c.rect(560, y-140, 560+max(.2, ny*app(("fair", r), .8, .2+r*.7))*bw-8, y, MARI, INK, 6, 8); c.text(300, y-70, lab, 70)
    L(c, "TO BE FAIR: BY 1929 MANY BROKERS WANTED MORE", 130, size=58)
    if k: L(c, "THOSE CUSTOMERS LASTED A LITTLE LONGER", 960, size=62, bg=MARI)
    return c
def bruised(k):
    c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
    c.rect(1320, 680, 1640, 706, WOOD, INK, 5); c.line([(1480, 706), (1480, 900)], 14, WOOD); c.phone(1480, 680, 1.1)
    for i in range(3): c.text(1600+i*46, 470-i*46, "z", 60+i*14, (150, 140, 128))
    f = you(c, 700, 980, 400, "stock", "hold", "worry" if k == 0 else "n"); bandage(c, f); c.cert(f["hand"][0]+150, f["hand"][1]+10, .9, "RADIO")
    if k == 0: L(c, "BRUISED, BUT ALIVE", 1000, 1350, 76)
    if k == 1: L(c, "NO LOAN. NO CALL.", 1000, 1400, 80)
    if k == 2: L(c, "STILL OWNS EVERY SHARE", 1000, 1350, 76, bg=MARI)
    return c
def half(k):
    c = C(); box = c.chartbox(110, 220, 1150, 880, "SEPT TO MID-NOVEMBER 1929"); q = app("half", 1.6)
    c.plot(box, [(0, .95), (.15, .86), (.3, .9), (.5, .8), (.58, .56), (.63, .5), (.72, .6), (.86, .55), (1, .49)], q, RED, 13)
    f = you(c, 1640, 990, 300, "stock", "stand", "worry"); bandage(c, f); c.cash(1380, 990, int(lerp(8, 4, q)+.5), 1.2); c.text(1380, 560, usd(lerp(1000, 500, q)), 120)
    if k: L(c, "DOWN ALMOST HALF", 990, 630, 78, bg=MARI)
    return c
def clever(k):
    c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
    for i, (x, kind) in enumerate(((360, "bank"), (1560, "matt"))):
        f = you(c, x, 980, 380, kind, "hold", "smug", flip=i == 1); hx, hy = f["hand"]; c.newspaper(hx+(190 if i == 0 else -190), hy+40, .9, "STOCKS COLLAPSE")
    if k: L(c, "FEELING VERY CLEVER", 1010, size=76, bg=MARI)
    return c
def lineup(k, done=2):
    c = C(); xs = [150, 380, 610, 840]
    if k == 0:
        c.fig(xs[0]+110, 900, 210, "cheer", "pain", "modern", rot=-90); chip(c, xs[0], 730, "MARGIN YOU", RED, 30); c.redx(xs[0], 850, 90, 22)
        f = you(c, xs[1], 900, 230, "stock", "stand", "worry", dy=-50); bandage(c, f)
        you(c, xs[2], 900, 230, "bank", "stand", "smug"); you(c, xs[3], 900, 230, "matt", "stand", "smug", dy=-50); c.text(480, 1000, "THREE OF YOU LEFT", 70)
    else:
        f = you(c, xs[0], 900, 230, "stock", "stand", "sad"); bandage(c, f); you(c, xs[1], 900, 230, "bank", "stand", "worry", dy=-50)
        you(c, xs[2], 900, 230, "matt", "stand", "smile"); you(c, xs[3], 900, 230, "post", "stand", "joy", dy=-50); c.text(480, 1000, "1933", 90)
    return Q(c, 4, done)
def spot(i, ex="worry"):
    c = hall(4, dim=[j for j in range(4) if j != i]); f = you(c, 960, 1040, 400, KINDS[i], "self", ex)
    if i == 1: bandage(c, f)
    return c

# ================= the staircase =================
def badpart(k):
    c = C(); c.line([(160, 700), (1760, 700)], 10); q = T.ease(T.GP*1.3)
    c.ell(240, 676, 288, 724, RED, INK, 6); c.text(264, 790, "OCT 1929", 54); c.text(264, 850, "THE CRASH", 54, RED)
    for i, yr in enumerate(("1930", "1931", "1932")):
        x = 700+i*420
        if q*1400 > x-340: c.ell(x-20, 680, x+20, 720, INK, None); c.text(x, 790, yr, 64)
    f = you(c, lerp(330, 1560, q), 696, 300, "stock", ("walk" if step() else "stand") if q < .98 else "stand", "worry"); bandage(c, f)
    if k == 0: L(c, "THE CRASH ISN'T THE BAD PART", 110, 700, 76)
    if k == 1: L(c, "THE NEXT THREE YEARS ARE", 110, 700, 80, bg=MARI)
    return c
def cliff(k):
    c = C((226, 236, 240))
    if k == 0:
        c.poly([(0, 380), (760, 380), (760, 900), (W, 900), (W, H), (0, H)], DSAND, INK, 7); q = app("fall", .9, .2)
        x = lerp(700, 1080, q); y = lerp(380, 900, q*q); f = c.fig(x, y, 280, "cheer" if q < 1 else "stand", "wow" if q < 1 else "n", "modern", rot=0 if q >= 1 else q*50)
        L(c, "NOT A CLIFF", 180, 1350, 90);
        if q >= 1: c.redx(1350, 180, 150, 22)
        return c
    pts = [(0, 250)]
    for i in range(6): pts += [(260+i*270, 250+i*120), (260+i*270, 370+i*120)]
    c.poly(pts+[(W, 970), (W, H), (0, H)], DSAND, INK, 7); q = app("tumble", 2.0, .1); s = min(5.999, q*6); i = int(s); fr = s-i
    x = 130+i*270+fr*270; y = 250+i*120+(120 if fr > .55 else 0)-abs(math.sin(fr*math.pi))*40
    if q >= 1: c.fig(1750, 970, 260, "stand", "pain", "modern")
    else: c.fig(x, y-10, 260, "cheer", "wow", "modern", rot=s*150 % 360 or 1)
    L(c, "A STAIRCASE", 180, 1350, 96, bg=MARI)
    return c
RAL = [(0, .66), (.15, .98), (.3, .7), (.36, .82), (.42, .53), (.5, .65), (.62, .4), (.66, .52), (.8, .24), (.86, .3), (1, .14)]
def rallies(k):
    c = C(); box = c.chartbox(150, 170, 1770, 880); q = T.ease(T.GP*1.15) if k == 0 else 1
    c.text(960, 930, "THE DOW, NOVEMBER 1929 TO JULY 1932", 46, (120, 110, 98)); c.plot(box, RAL, q, RED, 13)
    for i, (t, v, dx, dy) in enumerate(((0, .66, 250, 130), (.42, .53, 60, 120), (.8, .24, -60, 110))):
        if q >= t+.03:
            x = box[0]+(box[2]-box[0])*t+dx; y = box[3]-(box[3]-box[1])*v+dy; L(c, "THE BOTTOM?", y, x, 54)
            if k >= 1: c.strike(x-175, y, x+175, 12)
    if k >= 1: L(c, "NONE OF THEM IS", 330, 1380, 84, bg=MARI)
    return c
def bottom(k):
    c = C(); c.calpage(310, 500, 1.3, "JULY", "8", "1932"); box = c.chartbox(740, 250, 1800, 880)
    tip = c.plot(box, [(0, .953), (.04, .5), (.16, .735), (.4, .4), (.5, .485), (.72, .18), (.8, .22), (1, .103)], app("btm", 1.5), RED, 13)
    c.text(880, 300, "381", 70)
    if k: L(c, "THE DOW CLOSES AT 41", 400, 1400, 72, bg=MARI)
    return c
def eightynine(k):
    c = C(); c.line([(240, 900), (1240, 900)], 7); q = app("89", 1.1, .2)
    c.rect(380, 900-381*1.6, 600, 900, GREY, INK, 7, 6); c.text(490, 960, "1929 PEAK", 56); c.text(490, 900-381*1.6-56, "381", 80)
    v = lerp(381, 41, q); c.rect(820, 900-v*1.6, 1040, 900, RED, INK, 7, 6); c.text(930, 960, "JULY 1932", 56); c.text(930, 900-v*1.6-56, str(int(v)), 80)
    c.text(1520, 520, "-"+str(int(lerp(0, 89, q)))+"%", 260, RED)
    return c
def stack110(k):
    c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False); q = app("s110", 1.4, .2)
    f = you(c, 520, 980, 380, "stock", "shrug", "sad"); bandage(c, f); c.cash(1180, 980, int(lerp(8, 1, q)+.5), 1.9); c.text(1300, 420, usd(lerp(1000, 110, q)), 230, RED if q > .9 else INK)
    if k: L(c, "ABOUT $110 LEFT", 1010, 1250, 76, bg=MARI)
    return c
def right(k):
    c = C(); rows = ["DIDN'T BORROW", "DIDN'T PANIC", "DID EVERYTHING RIGHT"]
    for i in range(min(k+1, 3)):
        y = 300+i*190; c.rect(170, y-56, 282, y+56, WHITE, INK, 8, 12); c.tick(226, y, 40); c.text(330, y-4, rows[i], 96, INK, "lm")
    if k >= 3:
        c.bill(1400, 480, 3.4); q = app("cut", .7, .2); x0 = 1400-272+544*.11; c.da.rectangle([x0*S, (480-140)*S, (x0+(1400+280-x0)*q)*S, (480+140)*S], fill=(255, 248, 236, 222))
        c.line([(x0, 480-160), (x0, 480+160)], 8, RED, False); L(c, "YOU KEPT 11 CENTS ON THE DOLLAR", 960, 960, 68, bg=MARI)
    return c

# ================= the bank =================
def bankyou(k):
    c = street("day", 620, 4); c.bankfront(900, 900, 700, 460, "CORNER BANK")
    you(c, 480, 970, 360, "bank", "stand" if k == 0 else "chin", "smug" if k == 0 else "worry")
    if k: c.bubble(560, 250, "STILL FEELING CLEVER?", 62, (-60, 80))
    return c
def box(k):
    if k < 2:
        c = C((176, 182, 196))
        for r in range(4):
            for i in range(7):
                x = 270+i*200; y = 170+r*190; me = (r == 1 and i == 3)
                c.rect(x, y, x+180, y+170, MARI if me else (206, 212, 224), INK, 6, 8); c.ell(x+78, y+110, x+102, y+134, BRASS, INK, 4)
                if me: c.text(x+90, y+56, "YOU", 60)
                else: c.line([(x+50, y+56), (x+130, y+56)], 5, (150, 156, 170))
        if k == 0: L(c, "A BOX WITH YOUR NAME ON IT?", 1000, size=76)
        if k == 1: c.redx(960, 445, 150, 34); L(c, "THAT'S NOT WHAT A BANK DOES", 1000, size=76, bg=MARI)
        return c
    c = C(); c.bankfront(770, 400, 380, 230, "BANK"); T0 = [(330, 880), (960, 880), (1590, 880)]
    c.house(330, 880, 1.25); c.factory(960, 880, 1.2); c.shopfront(1420, 880, 340, 250, "SHOP")
    for j, (tx, ty) in enumerate(T0):
        sx, sy = 960+(tx-960)*.3, 430; ex_, ey = tx, ty-(270 if j != 1 else 300); arrow(c, sx, sy, ex_, ey, TEAL, 12, 34)
        q = (T.TT*.6+j*.33) % 1; c.coin(lerp(sx, ex_, q), lerp(sy, ey, q), 30)
    L(c, "IT LENDS YOUR MONEY OUT", 1000, size=72, bg=MARI)
    return c
def morning(k):
    c = bankhall(); counter(c, "smile" if k == 0 else "wow")
    if k == 0: c.person(680, 930, 340, "hold", "smile", "rose", "cloche"); L(c, "FINE, ON A NORMAL MORNING", 130, 560, 66)
    else:
        for i, x in enumerate((200, 370, 540, 700, 860, 1010)):
            xx = lerp(x-900, x, app(("rush", i), .7, i*.08)); c.person(xx, 930+(i % 3)*40, 320-(i % 2)*20, "up" if i % 2 else "point", ["angry", "worry", "wow", "angry", "strain", "worry"][i], ["slate", "brown", "green", "blue", "rose", "teal"][i], ["fedora", "cap", "cloche", None, "bowler", "fedora"][i])
        L(c, "NOT IF EVERYONE ASKS ON THE SAME MORNING", 120, 800, 56, bg=MARI)
    return c
def shut(k):
    c = C(); n = [6, 16, 40][k]; n0 = [0, 6, 16][k]; q = app(("shut", k), 1.4, .15); m = int(lerp(n0, n, q)+.5)
    for i in range(m):
        col, row = i % 10, i//10; minibank(c, 220+col*164, 520+row*150, .82+.25*(1-min(1, (lerp(n0, n, q)-i)*1.2)) if i >= n0 else .82)
    big = [usd(lerp(0, 1350, q))[1:], "+"+usd(lerp(0, 2300, q))[1:], usd(lerp(3650, 9000, q))[1:]+"+"][k]
    c.text(560, 190, big, 220, RED); c.text(1300, 150, ["BANKS SHUT IN 1930", "MORE IN 1931", "BY 1933"][k], 86); c.text(1300, 260, "EACH ICON = ABOUT 225 BANKS", 46, (120, 110, 98))
    return c
def bous(k):
    c = street("grey", 600, 9, hmax=380); c.bankfront(520, 900, 880, 500, "BANK OF UNITED STATES", closed=k >= 3)
    if k >= 3: crowd(c, [330, 560, 800, 1120, 1360, 1590], 990, ("worry", "angry", "sad", "wow"), ("stand", "up", "shrug", "stand"), 270)
    L(c, ["ONE OF THEM IS IN YOUR CITY", "NEW YORK CITY, DECEMBER 1930", "DESPITE THE NAME: AN ORDINARY BANK", "$200 MILLION IN DEPOSITS", "THE BIGGEST U.S. BANK FAILURE SO FAR"][k], 80, size=[66, 62, 62, 76, 62][k], bg=MARI if k in (2, 4) else PAPER)
    return c
def rumor(k, calm=False):
    c = office(win=(1240, 110, 1800, 480))
    a = c.person(520, 950, 340, "hold", "worry" if not calm else "wow", "green", None, TEAL); 
    if not calm: you(c, 980, 950, 340, "bank", "stand", "wow", flip=True); c.bubble(520, 250, "PSST. ABOUT\nYOUR BANK...", 66, (-10, 70))
    else:
        f = you(c, 980, 950, 340, "bank", "hold", "bored", flip=True); c.loaf(f["hand"][0]-10, f["hand"][1]+10, 1.3); c.bubble(520, 250, "PSST. ABOUT\nYOUR BANK...", 66, (-10, 70))
        if k >= 1: c.bubble(1150, 330, "SO?", 90, (-80, 70))
        if k >= 2: L(c, "THE RUMOR STOPS WORKING", 1000, size=80, bg=MARI)
    return c
def lunch(k=0):
    c = street("day", 620, 6); c.ell(1480, 90, 1700, 310, WHITE, INK, 10); c.line([(1590, 200), (1590, 120)], 10, INK, False); c.line([(1590, 200), (1592, 140)], 14, RED, False); c.text(1590, 370, "12:00", 60)
    x = lerp(-100, 1250, T.ease(T.LP*.9)); you(c, x, 960, 350, "bank", "run" if step() else "walk", "worry")
    for i in range(3): c.line([(x-190-i*60, 760+i*50), (x-270-i*60, 760+i*50)], 9, (150, 144, 136), False)
    return c
QCOAT = ["slate", "brown", "green", "blue", "rose", "teal", "banker", "red", "slate", "green", "brown", "blue", "rose"]; QHAT = ["fedora", "cap", "cloche", None, "bowler", "fedora", "top", None, "cap", "cloche", "fedora", None, "bowler"]
def queue(kind="grey", leave=0.0, closed=False, plaque=False, sid="wow", name="YOUR BANK"):
    c = street(kind, 600, 9, hmax=380); c.bankfront(1200, 860, 600, 420, name, closed)
    if plaque: c.plaque(1150, 640, .42, "FDIC"); c.shield(1830, 520, .7)
    spots = [(1420-i*170, 900) for i in range(8)]+[(330+i*200, 1050) for i in range(5)]; n = len(spots)
    for i, (x, y) in enumerate(spots):
        q = max(0.0, min(1.0, leave*2.2-(n-1-i)/n*1.2)); back = i >= 8
        if q >= 1: continue
        xx = x+(-1 if not back else 1)*T.ease(q)*0+(q*1500 if back else -q*1700); mv = 0 < q < 1
        if back and i == n-1 and sid: you(c, xx, y, 300, "bank", ("walk" if step() else "stand") if mv else "stand", sid if not mv else "smile", flip=False)
        else: c.person(xx, y, 300 if back else 250, ("walk" if step() else "stand") if mv else ("stand" if i % 3 else "chin"), ("worry", "angry", "sad", "n")[i % 4] if not mv else "n", QCOAT[i], QHAT[i], flip=(not back) if mv else (not back and i % 2 == 0))
    return c
def line1(k):
    c = queue("grey"); L(c, "A LINE AROUND THE BLOCK", 90, 620, 76, bg=MARI if k else PAPER)
    return c
def trap(k):
    c = C()
    for i in range(min(k+1, 2)):
        x = 110+i*880; c.rect(x, 230, x+820, 860, WHITE, INK, 7, 18); cx = x+410
        if i == 0:
            c.ell(cx+150, 300, cx+310, 460, WHITE, INK, 8); a = T.TT*1.5; c.line([(cx+230, 380), (cx+230+60*math.cos(a), 380+60*math.sin(a))], 8, RED, False)
            c.fig(cx-110, 800, 300, "chin", "bored", "modern"); c.text(cx, 910, "WAIT CALMLY...", 64); c.text(cx, 990, "MAYBE LOSE EVERYTHING", 64, RED)
        else:
            minibank(c, cx+190, 520, 1.7, False); c.line([(cx+150, 400), (cx+190, 450), (cx+170, 480), (cx+215, 520)], 9, RED)
            c.fig(cx-150+20*math.sin(T.TT*8), 800, 300, "run", "worry", "modern"); c.text(cx, 910, "RUN...", 64); c.text(cx, 990, "AND HELP BREAK THE BANK", 64, RED)
    L(c, "THE TRAP", 120, size=100, bg=MARI)
    return c
def noins(k):
    if k < 2:
        c = C(); c.shield(960, 330, 1.5, GREY); c.text(W/2, 600, "FEDERAL DEPOSIT INSURANCE", 120)
        if k: c.strike(250, 600, 1670, 26); c.text(W/2, 800, "DOESN'T EXIST YET", 110, RED)
        return c
    c = street("grey", 600, 12, hmax=380); c.bankfront(110, 880, 560, 400, "BANK", True)
    c.rect(1380, 760, 1700, 790, WOOD, INK, 6); c.line([(1420, 790), (1420, 940)], 12, WOOD); c.line([(1660, 790), (1660, 940)], 12, WOOD)
    for i in range(3): c.coin(1500+i*50, 740, 22)
    c.rect(1400, 560, 1680, 650, PAPER, INK, 6, 8); c.text(1540, 602, "CLAIMS", 60)
    c.person(1790, 960, 300, "stand", "bored", "banker", None, TEAL, flip=True)
    for i, x in enumerate((1240, 1050, 860, 670)): c.person(x, 960+(i % 2)*30, 290, "stand", ("sad", "worry", "sad", "bored")[i], QCOAT[i+2], QHAT[i+2])
    you(c, 470, 990, 300, "bank", "stand", "sad")
    L(c, "A DIFFERENT LINE, FOR WHATEVER IS LEFT", 90, 1100, 58, bg=MARI)
    return c
def billion(k):
    c = C(); q = app("bil", 1.3, .15); c.text(W/2, 400, "$%.1f BILLION" % lerp(0, 1.3, q), 250, RED)
    for i in range(12):
        x = 200+i*140; y = 640+((T.TT*210+i*97) % 460); c.coin(x, y, 34)
    if k: L(c, "LOST BY DEPOSITORS", 640, size=84, bg=MARI)
    return c
def gamble(k):
    c = street("grey", 620, 4); c.bankfront(900, 900, 700, 460, "YOUR BANK", door=(40, 36, 34)); c.text(1250, 590, "?", 170, RED)
    you(c, 440, 980, 360, "bank", "chin", "worry")
    for j, x in enumerate((660, 760)):
        y = 1000-abs(math.sin(T.TT*4+j))*70; c.rect(x-40, y-80, x+40, y, WHITE, INK, 6, 12)
        for dx, dy in ((-18, -58), (18, -22), (0, -40)) if j == 0 else ((-18, -58), (18, -22), (-18, -22), (18, -58)): c.ell(x+dx-8, y+dy-8, x+dx+8, y+dy+8, INK, None)
    L(c, "A GAMBLE ON A BANK YOU CAN'T SEE INSIDE", 80, size=58, bg=MARI if k else PAPER)
    return c

# ================= the mattress =================
def coward(k):
    c = bedroom(); p = c.bed(430, 930, 800, 0, 0, 1.3); you(c, 760, 632, 300, "matt", "stand" if k == 0 else "shrug", "bored" if k == 0 else "worry", sit=True)
    if k: c.bubble(1480, 640, "COWARD!", 90, (260, 60))
    return c
def glow(k):
    c = bedroom(); p = 60+int(40*math.sin(T.TT*5)); c.da.ellipse([420*S, 560*S, 1300*S, 900*S], fill=(255, 214, 90, p))
    c.bed(380, 930, 880, .9, 6, 1.4)
    for i, (x, y) in enumerate(((520, 600), (760, 540), (1010, 600), (1180, 540), (640, 480))):
        r = 26+16*math.sin(T.TT*7+i*1.7); c.line([(x-r, y), (x+r, y)], 8, MARI, False); c.line([(x, y-r), (x, y+r)], 8, MARI, False)
    you(c, 1560, 970, 340, "matt", "chin", "wow", flip=True)
    if k: L(c, "SOMETHING STRANGE UNDER THE BED", 90, 620, 62)
    return c
def prices(k):
    c = C()
    if k < 2:
        q = app("pdrop", 1.0, .15); c.line([(520, 200), (520, 920)], 8, (200, 190, 176)); c.pricetag(560, lerp(300, 780, q), 2.2, "PRICES"); arrow(c, 1000, 300, 1000, 300+500*max(.2, q), RED, 30, 80)
        c.text(1440, 480, "FALLING", 150, RED)
        if k == 1: L(c, "NOT STOCK PRICES. ALL PRICES.", 990, size=80, bg=MARI)
        return c
    items = [(360, "RENT"), (960, "SHOES"), (1560, "BREAD")]; hold = T.LT/max(T.LP, 1e-6) if T.LP < 1 else 0
    for i, th in enumerate((.12, .42, .7)):   # each item lands as its word is spoken
        x, t = items[i]; q = app(("item", i), .5, th*hold)
        if q <= 0: continue
        c.rect(x-200, 760, x+200, 800, WOOD, INK, 6, 6)
        if i == 0: c.keyp(x-10, 680, 1.7)
        if i == 1: c.shoe(x, 760, 1.7)
        if i == 2: c.loaf(x, 760, 2.6)
        c.pricetag(x+10, 900, 1.3, t); arrow(c, x, 240, x, 240+260*max(.25, q), RED, 26, 64)
    L(c, "ALL PRICES ARE FALLING", 110, size=80)
    return c
def thirty(k):
    c = C(); q = app("p30", 1.0, .2) if k else 0; c.text(460, 240, "1930", 100); c.pricetag(470, 560, 3.2, "PRICE")
    z = lerp(1, .7, q); c.text(1400, 240, "1933", 100); c.pricetag(1410, 560, 3.2*z, "PRICE"); arrow(c, 860, 560, 1040, 560, INK, 16, 44)
    if k: L(c, "AVERAGE PRICES: DOWN NEARLY 30%", 950, size=76, bg=MARI)
    return c
def crate(c, x, y, s=92):
    c.rect(x, y-s, x+s, y, (214, 176, 120), INK, 5, 4); c.line([(x+8, y-s+8), (x+s-8, y-8)], 4, (160, 124, 80)); c.line([(x+s-8, y-s+8), (x+8, y-8)], 4, (160, 124, 80))
def shops(k):
    c = C(); c.line([(120, 900), (1800, 900)], 7); you(c, 250, 900, 280, "matt", "hold", "smile" if k else "n"); c.cash(430, 900, 8, .9)
    c.text(830, 190, "1930", 90)
    for i in range(10): crate(c, 640+(i % 4)*98, 900-(i//4)*98)
    if k:
        c.text(1440, 190, "1933", 90); q = app("crates", 1.2, .15); m = int(lerp(0, 14, q)+.5)
        for i in range(m): crate(c, 1250+(i % 4)*98, 900-(i//4)*98)
        L(c, "$1,000 NOW SHOPS LIKE $1,400", 1000, 1000, 72, bg=MARI)
    else: L(c, "SAME DOLLARS", 520, 1380, 76)
    return c
def ahead(k):
    c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
    c.rect(780, 720, 1140, 940, MARI, INK, 8, 8); c.text(960, 830, "1", 150)
    you(c, 960, 720, 330, "matt", "cheer" if k else "stand", "joy" if k else "smile")
    f = you(c, 380, 960, 290, "stock", "stand", "sad"); bandage(c, f); you(c, 1540, 960, 290, "bank", "stand", "worry", flip=True)
    if k == 0: L(c, "NO RISK. NO INTEREST.", 130, size=74)
    if k == 1: L(c, "AHEAD OF EVERYONE", 130, size=88, bg=MARI)
    return c
def jobs(k):
    c = street("grey", 620, 14); xs = [420, 780, 1140, 1500]
    for i, x in enumerate(xs):
        idle = (k >= 1 and i == 3)
        f = c.person(x, 960, 340, "stand" if not idle else "shrug", ("n", "smile", "n", "n")[i] if not idle else "sad", ["blue", "brown", "green", "rose"][i] if not idle else "grey", "cap")
        if idle: c.rect(x-150, 520, x+150, 620, PAPER, INK, 6, 8); c.text(x, 566, "NO JOB", 70, RED)
    if k == 0: L(c, "THERE IS A CATCH", 90, size=80)
    if k >= 1: L(c, "BY 1933: ONE WORKER IN FOUR HAS NO JOB", 90, 700, 62, bg=MARI)
    return c
def groceries(k):
    c = bedroom(); c.bed(430, 930, 800, .75, [4, 2, 1][k], 1.3)
    f = you(c, 1500, 970, 340, "matt", "hold", "worry", flip=True); c.bill(f["hand"][0]-80, f["hand"][1], .8)
    c.poly([(1640, 970), (1660, 760), (1840, 760), (1860, 970)], (196, 156, 110), INK, 6); c.loaf(1750, 770, 1.5)
    if k == 1: L(c, "NOT A STRATEGY", 130, 560, 80)
    if k == 2: L(c, "NOT A STRATEGY", 130, 560, 80); L(c, "GROCERIES", 270, 560, 96, bg=MARI)
    return c
def fifth(k):
    q = app("d5", .8, .3); c = hall(4, dim=(0, 1, 2, 3), xs=DX5, w=220, skip=(4,))
    c.door(lerp(2300, DX5[4], q), 800, 220, 430, 5, POSTC, "POST OFFICE" if q >= 1 else None)
    if k: L(c, "A FIFTH DOOR NOBODY MENTIONED", 110, 760, 66)
    return c
def post(k):
    c = street("day", 620, 8); c.bankfront(170, 900, 820, 460, "U.S. POST OFFICE", f=(232, 220, 200)); c.flag(1120, 900, 560, 1.5, T.TT*3)
    you(c, 1560, 1010, 280, "post", "wave" if k == 0 else "stand", "smile", flip=True)
    labs = ["2% INTEREST", "RUN BY THE GOVERNMENT", "UP TO $2,500"]
    for i in range(min(k, 3)): L(c, labs[i], 120+i*124, 1480, 62, bg=MARI if i == k-1 else PAPER)
    return c
def x5(k):
    c = C(); c.line([(700, 250), (700, 930)], 6, (200, 190, 176)); c.text(380, 200, "THE 1920s", 80); c.text(1300, 200, "1933", 90)
    c.person(380, 880, 330, "stand", "smile", "blue", "cap")
    for i in range(5):
        q = app(("ps", i), .3, .2+i*.22)
        if q > 0: c.person(860+i*200, 880+(1-q)*40, 330, "stand" if i % 2 else "wave", ("smile", "n", "joy", "smile", "n")[i], QCOAT[i+1], QHAT[i+1])
    if k: c.text(1300, 990, "×5 POSTAL SAVERS", 100, POSTC)
    return c
SCORE = [("margin", "$0", "OUT IN TWO DAYS", RED, "pain"), ("stock", "ABOUT $110", "", INK, "sad"), ("bank", "$1,000... OR $0", "DEPENDS ON A RUMOR", INK, "worry"),
         ("matt", "$1,000", "BUYS LIKE $1,400", TEAL, "smile"), ("post", "$1,000 + INTEREST", "", TEAL, "joy")]
def score(n, done=0):
    c = C(); c.text(W/2, 105, "SCOREBOARD, 1933", 100)
    for i in range(n):
        kind, main, sub, col, ex = SCORE[i]; y = 262+i*158; q = app(("sc", i), .35); dx = (1-q)*1900
        c.rect(120+dx, y-68, 1800+dx, y+68, WHITE, INK, 7, 14)
        if i == n-1: p = 4+3*math.sin(T.TT*5); c.rect(120+dx-p, y-68-p, 1800+dx+p, y+68+p, None, MARI, 10, 16)
        c.fig(205+dx, y+58, 88, "stand", ex, "modern"); chip(c, 500+dx, y, TAGS[kind][0], TAGS[kind][1], 42)
        c.text(790+dx, y-4, main, 84, col, "lm")
        if sub: c.text(1770+dx, y-2, sub, 46, (110, 100, 90), "rm")
    if done: Q(c, 4, done)
    return c

# ================= the hidden quest =================
def hiddenq(k, done=3):
    c = C(); c.questlog(ROWS, 4, done, None, x=545, y=200)
    if k: c.marker(470, 800, 36)
    return c
def holiday(k):
    if k == 0:
        c = C(); c.calpage(360, 500, 1.3, "MARCH", "1933")
        for i in range(3): minibank(c, 900+i*330, 640, 2.0, app(("mb", i), .2, .3+i*.3) > 0)
        L(c, "THE BANKING SYSTEM HAS COLLAPSED", 950, size=68)
        return c
    if k == 1:
        c = office(win=None, wall=(214, 222, 214)); c.flag(300, 900, 620, 1.7, T.TT*2)
        p = c.person(1000, 860, 380, "write", "det", "banker", None, NAVY); c.desk(640, 980, 820, 200); c.rect(1080, 700, 1280, 790, WHITE, INK, 5)
        for i in range(3): c.line([(1100, 722+i*20), (1250-i*30, 722+i*20)], 4, (150, 150, 150))
        L(c, "THE NEW PRESIDENT", 120, 1200, 76)
        return c
    c = street("grey", 600, 9, hmax=380)
    for i in range(3): c.bankfront(90+i*620, 900, 500, 380, ["FIRST BANK", "CITY BANK", "FARMERS BANK"][i], app(("cl", i), .2, .15+i*.3) > 0)
    L(c, "EVERY BANK IN THE COUNTRY: CLOSED", 90, size=68, bg=MARI)
    return c
def nobody(k):
    c = street("grey", 620, 14)
    for x in (220, 1700): c.line([(x, 640), (x, 200)], 12, (90, 84, 80), False)
    c.rect(220, 190, 1700, 340, PAPER, INK, 8, 6); c.text(960, 262, "BANK HOLIDAY", 130, RED)
    crowd(c, [330, 560, 790, 1020, 1250], 960, ("sad", "bored", "worry", "sad"), ("stand", "shrug", "stand", "chin"), 300)
    if k: c.umbrella(1620, 1000, 1.3); c.redx(1620, 760, 130, 26); L(c, "NOBODY IS ON HOLIDAY", 480, 760, 72, bg=MARI)
    return c
def law(k):
    c = C((214, 222, 214)); c.rect(0, 700, W, H, WOOD, None); c.line([(0, 700), (W, 700)], 6, INK, False)
    c.poly([(520, 1010), (600, 330), (1400, 330), (1480, 1010)], CREAM, INK, 8); c.text(1000, 420, "BANKING ACT OF 1933", 72)
    for i in range(5): c.line([(660-i*8, 520+i*64), (1340+i*8-(i % 2)*120, 520+i*64)], 5, (170, 160, 146))
    q = app("sig", 1.1, .3); pts = [(980+i*26, 900+26*math.sin(i*1.3)) for i in range(int(14*q)+2)]; c.line(pts, 9, NAVY)
    px, py = pts[-1]; c.line([(px, py), (px+90, py-170)], 14, INK, False); c.line([(px, py), (px+16, py-30)], 14, BRASS, False)
    c.calpage(240, 300, .8, "JUNE", "16", "1933")
    if k: L(c, "SOMETHING NEW", 190, 1560, 76, bg=MARI)
    return c
def fdic(k):
    c = C(); words = ["FEDERAL", "DEPOSIT", "INSURANCE", "CORPORATION"]
    if k == 0:
        for i, w in enumerate(words):
            q = app(("fw", i), .25, .1+i*.55)
            if q > 0: c.text(240, 210+i*210, w[0], 190*q+1, TEAL, "lm"); c.text(248+c.tw(w[0], 190*q+1), 226+i*210, w[1:], 130*q+1, INK, "lm")
        c.shield(1500, 540, 2.2)
        return c
    for i, ch in enumerate("FDIC"):
        q = app(("fl", i), .22, i*.18)
        if q > 0: c.text(420+i*360, 480, ch, 430*(.6+.4*q), TEAL)
    c.text(W/2, 860, "FEDERAL DEPOSIT INSURANCE CORPORATION", 70)
    return c
def back(k):
    c = street("day", 600, 9, hmax=380); c.bankfront(1160, 880, 600, 420, "YOUR BANK", True); c.calpage(250, 310, .85, "JAN", "1", "1934")
    f = you(c, 620, 990, 340, "bank", "hold" if k else "stand", "joy" if k else "n")
    if k >= 1:
        q = app("fly", 1.2, .2)
        for i in range(5):
            t = max(0.0, min(1.0, q*1.8-i*.2))
            if 0 < t < 1: c.bill(lerp(1460, f["hand"][0]+60, t), lerp(700, f["hand"][1], t)-180*math.sin(t*math.pi), .7)
        c.cash(f["hand"][0]+60, f["hand"][1]+34, int(8*q+.5), .85); L(c, "BANK FAILS? YOU GET IT BACK.", 90, 1180, 64)
    if k == 0: L(c, "FROM JANUARY 1, 1934", 90, 1180, 68)
    if k >= 2: L(c, "UP TO $2,500", 290, 1180, 90, bg=MARI)
    return c
def covered(k):
    c = C(); c.rect(260, 380, 1560, 560, None, INK, 9, 12); q = app("cov", .6, .1); c.rect(260, 380, 260+1300*.4*max(.08, q), 560, MARI, INK, 9, 12)
    c.text(910, 290, "INSURED UP TO $2,500", 84); c.text(260+260, 470, "YOUR $1,000", 62); c.shield(1730, 470, 1.25)
    you(c, 520, 1040, 270, "bank", "cheer" if k else "stand", "joy" if k else "smile")
    if k: L(c, "COVERED. ALL OF IT.", 880, 1250, 96, bg=MARI)
    return c
def line2(k):
    lv = [0, lerp(0, .55, T.LP), lerp(.55, 1.2, T.LP), 1.2][k]; c = queue("grey" if k < 3 else "day", lv, plaque=k >= 1, sid="wow" if k == 0 else "smile")
    if k == 0: L(c, "NOW THINK ABOUT THAT LINE", 90, 620, 70)
    if k == 1: L(c, "MONEY SAFE EITHER WAY: NO REASON TO RUN", 90, 660, 54)
    if k == 2: L(c, "NOBODY RUNS", 90, 620, 84)
    if k == 3: L(c, "THE BANK DOESN'T BREAK", 90, 620, 80, bg=MARI); you(c, 760, 1000, 320, "bank", "wave", "joy")
    return c
def fourth(k):
    if k < 2:
        c = C(); c.questlog(ROWS, 4, 4, HID, x=545, y=200)
        if k: c.marker(470, 800, 36)
        return c
    c = C(); c.cert(600, 440, 2.2, "THE RULES"); c.shield(1420, 430, 1.9); c.fig(1060, 1050, 230, "shrug", "smile", "modern")
    L(c, "YOU DIDN'T COMPLETE IT", 900, 520, 62)
    if k == 3: L(c, "THE RULES DID", 900, 1510, 88, bg=MARI)
    return c
def drawer(k):
    c = C(WALL); c.rect(0, 850, W, H, FLOOR, None); c.line([(0, 850), (W, 850)], 6, INK, False)
    c.rect(1000, 560, 1560, 940, WOOD, INK, 8, 8); q = app("shutd", .6, .5) if k == 1 else 0; o = 150*(1-q) if k <= 1 else 0
    for i in range(3):
        y = 600+i*112; dx = o if i == 0 else 0
        if i == 0 and dx > 4: c.rect(1030, y, 1530, y+90, (60, 44, 34), INK, 5); c.cert(1280, y+20-dx*.5, .8, "RADIO")
        w = dx*.16; c.rect(1030-w, y+dx*.45, 1530+w, y+90+dx*.45, (170, 126, 88), INK, 6, 4); c.ell(1262, y+32+dx*.45, 1298, y+58+dx*.45, BRASS, INK, 4)
    f = you(c, 560, 980, 380, "stock", "point" if k < 2 else "stand", "n" if k < 2 else "bored"); bandage(c, f)
    if k == 2:
        for a in range(0, 91, 30): c.line([(1560, 560), (1560-130*math.cos(math.radians(a)), 560+130*math.sin(math.radians(a)))], 3, (150, 150, 150))
        for r in (50, 90, 125): c.d.arc([(1560-r)*S, (560-r)*S, (1560+r)*S, (560+r)*S], 90, 180, fill=(150, 150, 150), width=3*S)
        L(c, "HELD ON. NEVER LOOKED.", 130, size=78)
    return c
LONG = [(1929.67, 381), (1929.87, 199), (1930.3, 294), (1930.96, 158), (1931.15, 194), (1932.0, 78), (1932.52, 41), (1933.5, 100), (1934.5, 96), (1935.9, 144), (1937.2, 194), (1938.25, 99), (1938.9, 155),
        (1939.7, 150), (1940.9, 131), (1942.3, 93), (1943.5, 140), (1944.9, 152), (1945.95, 193), (1946.4, 212), (1946.8, 165), (1947.9, 181), (1949.45, 162), (1950.4, 225), (1951.7, 270), (1952.95, 292),
        (1953.7, 256), (1954.5, 340), (1954.9, 382)]
def longc(k):
    c = C(); box = c.chartbox(130, 230, 1790, 880, "THE DOW, 1929 TO 1954"); pts = norm(LONG, 1929.67, 1954.9, 430)
    yy = box[3]-(box[3]-box[1])*381/430
    for i in range(30): c.line([(box[0]+i*54, yy), (box[0]+i*54+30, yy)], 6, TEAL, False)
    for i, yr in enumerate((1930, 1935, 1940, 1945, 1950)): x = box[0]+(box[2]-box[0])*(yr-1929.67)/25.23; c.line([(x, box[3]), (x, box[3]+16)], 5); c.text(x, 925, str(yr), 46, (120, 110, 98))
    q = T.ease(T.GP*1.1) if k < 2 else 1; c.plot(box, pts, q, RED, 11)
    c.text(520, yy-44, "1929 HIGH: 381", 54, TEAL)
    if k == 1: L(c, "NOVEMBER 23, 1954", 790, 1330, 76, bg=MARI)
    if k == 2: L(c, "PRICE ONLY. DIVIDENDS NOT COUNTED.", 1000, size=64)
    if k == 3: L(c, "STILL A LONG TIME TO BE RIGHT", 1000, size=72, bg=MARI)
    return c
def ages(k):
    c = C(); q = app("arr", .7, .1); arrow(c, 700, 560, 700+500*max(.1, q), 560, INK, 16, 46); c.text(950, 450, "25 YEARS", 120, RED)
    if k >= 1: c.fig(440, 900, 400, "stand", "smile", "modern"); L(c, "1929: AGE 24", 1000, 440, 70)
    if k >= 2: b = c.fig(1480, 900, 400, "stand", "bored", "modern", flip=True); c.glasses(b); L(c, "1954: AGE 49", 1000, 1480, 70, bg=MARI)
    return c

# ================= the ending =================
def smart(k):
    c = hall(5, dim=(0, 1, 2) if k >= 1 else (), xs=DX5, w=220)
    if k == 0: c.fig(960, 1030, 290, "chin", "n", "modern"); L(c, "THE SMART MOVE IN SEPTEMBER 1929?", 100, size=64)
    if k >= 1: L(c, "WITH HINDSIGHT: THE BORING ONES", 100, size=68)
    if k == 2:
        for i in range(6):
            x = (i*380+T.TT*30) % (W+500)-250; c.da.ellipse([(x-330)*S, (300+(i % 3)*150)*S, (x+330)*S, (520+(i % 3)*150)*S], fill=(236, 232, 226, 200))
        c.fig(960, 1030, 290, "shrug", "worry", "modern"); L(c, "NOBODY COULD HAVE PROVED IT THEN", 990, 1400, 58, bg=MARI)
    return c
def three(k):
    c = C(); caps = ["A PLATEAU", "A PLAN", "A TIP"]
    for i in range(min(k+1, 3)):
        x = 96+i*586; cx = x+270; c.rect(x, 200, x+540, 820, WHITE, INK, 7, 18)
        if i == 0:
            c.rect(cx-10, 260, cx+240, 440, BOARD, INK, 6, 4); c.line([(cx+10, 410), (cx+80, 320), (cx+220, 320)], 9, PAPER); e = c.person(cx-110, 800, 300, "point", "smug", "brown", None, RED); c.glasses(e)
        if i == 1:
            f = c.person(cx-60, 800, 300, "up", "det", "banker", "top", MARI); hx, hy = f["hand"]; c.line([(hx, hy), (hx, hy-70)], 8, WOOD); c.rect(hx-100, hy-190, hx+100, hy-70, PAPER, INK, 6, 8); c.text(hx, hy-134, "BUY", 80, TEAL)
        if i == 2:
            c.person(cx-90, 800, 300, "hold", "smug", "teal", None, RED); c.bubble(cx+60, 330, "PSST. RADIO.", 50, (-70, 60))
        c.text(cx, 900, caps[i], 80, RED)
    L(c, ["THE ECONOMIST HAD...", "THE BANKERS HAD...", "THE GUY AT THE OFFICE HAD..."][min(k, 2)], 110, size=66)
    return c
def youhad(k):
    c = hall(4, dim=()); s = c.fig(960, 1040, 330, "hold", "n", "modern"); c.cash(s["hand"][0]+56, s["hand"][1]+34, 8, .85)
    if k: L(c, "YOU HAD $1,000 AND FOUR DOORS", 100, size=72, bg=MARI)
    return c
def sign(k):
    if k < 2:
        c = street("day", 600, 11); c.rect(700, 300, 1700, 900, (206, 214, 222), INK, 8); c.rect(760, 420, 1140, 900, SKY, INK, 6); c.rect(1220, 420, 1420, 900, SKY, INK, 6); c.rect(1424, 420, 1624, 900, SKY, INK, 6)
        c.rect(760, 320, 1640, 400, NAVY, INK, 6, 6); c.text(1200, 358, "BANK", 64, PAPER); c.plaque(1160, 620, .28, "FDIC")
        walker(c, "tobank2", 120, 480, 980, 340, 1.4, ex="smile")
        if k == 1: p = 1+.06*math.sin(T.TT*6); c.ell(1160-90*p, 620-70*p, 1160+90*p, 620+70*p, None, RED, 10); L(c, "A SMALL SIGN BY THE DOOR", 110, 620, 68)
        return c
    c = C((206, 214, 222)); z = .8+.2*app("plq", .35); c.plaque(960, 500, 3.0*z, "FDIC")
    if k == 3:
        c.da.rectangle([0, 0, W*S, H*S], fill=(206, 214, 222, 150)); 
        for i in range(7): c.person(180+i*250, 1040+(i % 2)*20, 300, "stand", "n", "grey", QHAT[i])
        c.da.rectangle([0, 620*S, W*S, H*S], fill=(206, 214, 222, 150)); c.plaque(960, 400, 2.2, "FDIC"); L(c, "BECAUSE OF THE LINE AROUND THE BLOCK", 1000, size=62, bg=MARI)
    return c
def finale(k):
    c = street("day", 620, 4); c.bankfront(120, 900, 640, 440, "CORNER BANK"); c.plaque(60, 640, .34, "FDIC")
    c.fig(830, 1000, 340, "cheer", "joy", "modern"); Q(c, 4, 4, HID); L(c, "QUEST COMPLETE", 100, 480, 100, bg=MARI)
    return c

def F(f, *a, **k):
    g = lambda: f(*a, **k); g.scene = f.__name__; return g
# (narration, [frames], chime?)   Respellings are for the voice only; CAPTION_FIX restores the display forms.
U = [
 ("It's September, nineteen twenty-nine. You have one thousand dollars.", [F(card, "SEPTEMBER 1929"), F(cold, 0), F(cold, 1)]),
 ("That's about eight months' pay. It took you four years to save.", [F(pay, 0), F(pay, 1)]),
 ("It can vanish in two days. It can shrink to a hundred and ten dollars. Or it can quietly buy more than it does today.", [F(fates, 0), F(fates, 1), F(fates, 2)]),
 ("The difference is where you put it this week.", [F(where, 0), F(where, 1)]),
 ("So let's put it in four places at once, and see which you survives.", [F(four, 0), F(four, 1)], "chime"),
 ("You're twenty-four. You're a clerk in New York City.", [F(intro, 0), F(clerk, 1)]),
 ("You are made up. The numbers aren't.", [F(card, "YOU ARE MADE UP.", "THE NUMBERS AREN'T.", 140)]),
 ("Here's your quest log. One: pick a home for your thousand dollars.", [F(qoffice, 0), F(qoffice, 1)], "tick"),
 ("Two: get through October.", [F(qoffice, 2)], "tick"),
 ("Three: still have it in nineteen thirty-three.", [F(qoffice, 3)], "tick"),
 ("There's a fourth quest hidden at the end. It's the reason you've never had to think about any of this.", [F(qoffice, 4), F(hiddenq, 1, 0)], "tick"),
 ("First, the mood. The stock market has been climbing for eight years.", [F(card, "FIRST, THE MOOD"), F(climb, 0)]),
 ("In nineteen twenty-one, the Dow Jones average stood at sixty-three. This month it touches three hundred and eighty-one.", [F(climb, 1), F(climb, 2), F(climb, 3)]),
 ("Six times higher. Everyone you know has a story about a guy who got rich.", [F(six, 0), F(six, 1), F(six, 2)]),
 ("Almost nobody you know is that guy. Only about one and a half million Americans even have an account with a broker.", [F(dots, 0), F(dots, 1), F(dots, 2)]),
 ("But the ones who do are loud.", [F(loud, 0)]),
 ("So. Four doors.", [F(doors0)]),
 ("Door one. The broker. You buy stocks on margin.", [F(doorhi, 0), F(broker, 2)]),
 ("Margin means you put down a slice of the price, and the broker lends you the rest.", [F(slice_, 0), F(slice_, 1)]),
 ("That slice can be as little as ten percent.", [F(slice_, 2)]),
 ("So your thousand dollars buys ten thousand dollars of stock.", [F(slice_, 3)]),
 ("If prices rise ten percent, you've doubled your money. This is the part the loud guys talk about.", [F(slice_, 4), F(slice_, 5), F(loud, 1, "DOUBLED MY MONEY!")]),
 ("The stock everybody wants is Radio. That's R C A.", [F(radio, 0), F(radio, 1)]),
 ("In March, a pool of insiders spent a week pushing Radio's price up. Then they sold everything. That was legal.", [F(pool, 0), F(pool, 1), F(pool, 2)]),
 ("Door two. Same broker, no loan. A thousand dollars of stock, bought and paid for.", [F(doorhi, 1), F(outright, 0), F(outright, 1)]),
 ("Door three. The bank on the corner. Marble columns, brass rails, and it pays you interest.", [F(doorhi, 2), F(bankext, 1), F(teller, 1), F(teller, 2)]),
 ("Door four. The mattress. No interest, no risk, no respect.", [F(doorhi, 3), F(mattress, 0), F(mattress, 2), F(mattress, 3)]),
 ("Your coworkers think door four is for people who are afraid of money.", [F(laugh, 0), F(laugh, 1)]),
 ("So we'll make four of you, and send one through each door.", [F(split, 0), F(split, 1)]),
 ("Quest one, complete.", [F(split, 2, 1)], "chime"),
 ("September third. The Dow closes at three eighty-one. Nobody rings a bell at the top.", [F(peak, 0), F(peak, 1), F(peak, 2)]),
 ("Through September, prices slide about ten percent. Then they bounce.", [F(slide, 0), F(slide, 1)]),
 ("In mid-October, a famous Yale economist says stock prices have reached what looks like a permanently high plateau.", [F(fisher, 0), F(fisher, 1), F(fisher, 2)]),
 ("He is about to become famous for a different reason.", [F(fisher, 3)]),
 ("Thursday, October twenty-fourth. Nearly thirteen million shares change hands. A record.", [F(floor, 0), F(floor, 1), F(floor, 2)]),
 ("The big bankers step in and buy shares in public, to show everyone it's fine.", [F(bankers, 0), F(bankers, 1), F(bankers, 2)]),
 ("It holds for a weekend.", [F(weekend)]),
 ("Monday, October twenty-eighth. The Dow falls nearly thirteen percent. In one day.", [F(monday, 0), F(monday, 1), F(monday, 2)]),
 ("Now look at margin you. You owned ten thousand dollars of stock, with one thousand of your own.", [F(spot, 0), F(myou, 0)]),
 ("A thirteen percent drop is thirteen hundred dollars. Your thousand is gone. So is three hundred you never had.", [F(myou, 1), F(myou, 2), F(myou, 3)]),
 ("The broker doesn't wait for you to feel better. He sends a margin call. Pay up today, or he sells your shares.", [F(call, 0), F(call, 1), F(call, 2)]),
 ("You can't pay. He sells. So does every other broker in the city, at the same moment, into the same falling market.", [F(sell, 0), F(sell, 1), F(sell, 2), F(sell, 3)]),
 ("That's Tuesday, October twenty-ninth. Sixteen million shares. Down nearly twelve percent more.", [F(tuesday, 0), F(tuesday, 1), F(tuesday, 2)]),
 ("Margin you is finished. Out in two days.", [F(out, 0), F(out, 1)]),
 ("To be fair, by nineteen twenty-nine many brokers wanted a lot more than ten percent down. Those customers lasted a little longer.", [F(fair, 0), F(fair, 1)]),
 ("Stock you is bruised, but alive. No loan, no call. You still own every share.", [F(bruised, 0), F(bruised, 1), F(bruised, 2)]),
 ("By mid-November the market is down almost half. Your thousand is about five hundred.", [F(half, 0), F(half, 1)]),
 ("Bank you and mattress you read about it in the paper, and feel very clever.", [F(clever, 0), F(clever, 1)]),
 ("Quest two, complete. Three of you left.", [F(lineup, 0)], "chime"),
 ("Here's what nobody tells stock you. The crash isn't the bad part. The bad part is the next three years.", [F(spot, 1), F(badpart, 0), F(badpart, 1)]),
 ("The market doesn't fall off a cliff and stop. It falls down a staircase.", [F(cliff, 0), F(cliff, 1)]),
 ("Every rally looks like the bottom. None of them is.", [F(rallies, 0), F(rallies, 1)]),
 ("The real bottom comes on July eighth, nineteen thirty-two. The Dow closes at forty-one.", [F(bottom, 0), F(bottom, 1)]),
 ("That's eighty-nine percent below the peak.", [F(eightynine, 0)]),
 ("Your thousand dollars of stock is now worth about a hundred and ten.", [F(stack110, 0), F(stack110, 1)]),
 ("You didn't borrow. You didn't panic. You did everything right, and you kept eleven cents on the dollar.", [F(right, 0), F(right, 1), F(right, 2), F(right, 3)]),
 ("Now, bank you. Still feeling clever?", [F(bankyou, 0), F(bankyou, 1)]),
 ("A bank doesn't keep your money in a box with your name on it. It lends it out.", [F(box, 0), F(box, 1), F(box, 2)]),
 ("That works, as long as everyone doesn't ask for their money on the same morning.", [F(morning, 0), F(morning, 1)]),
 ("In nineteen thirty, thirteen hundred and fifty banks shut their doors.", [F(card, "1930"), F(shut, 0)]),
 ("One of them is in your city. It's called the Bank of United States. Despite the name, it's an ordinary bank.", [F(bous, 0), F(bous, 1), F(bous, 2)]),
 ("Two hundred million dollars in deposits. The biggest bank failure the country has ever seen.", [F(bous, 3), F(bous, 4)]),
 ("Then you hear a rumor about your own bank. You go down at lunch. There's already a line around the block.", [F(rumor, 0), F(lunch), F(line1, 0)]),
 ("This is the trap. If you wait calmly, you might lose everything. If you run, you help break the bank.", [F(line1, 1), F(trap, 0), F(trap, 1)]),
 ("And there's no insurance. If the bank dies, you join a different line, for whatever is left.", [F(noins, 0), F(noins, 1), F(noins, 2)]),
 ("Nineteen thirty-one. About twenty-three hundred more banks go under.", [F(card, "1931"), F(shut, 1)]),
 ("By nineteen thirty-three, the count passes nine thousand.", [F(shut, 2)]),
 ("Depositors lose about one point three billion dollars.", [F(billion, 0), F(billion, 1)]),
 ("So bank you is a gamble, on a bank you can't see inside.", [F(gamble, 0), F(gamble, 1)]),
 ("And mattress you? The coward?", [F(coward, 0), F(coward, 1)]),
 ("Something strange is happening to the cash under the bed.", [F(glow, 0), F(glow, 1)]),
 ("Prices are falling. Not stock prices. All prices. Rent. Shoes. Bread.", [F(prices, 0), F(prices, 1), F(prices, 2)]),
 ("Between nineteen thirty and nineteen thirty-three, average prices drop by nearly thirty percent.", [F(thirty, 0), F(thirty, 1)]),
 ("So a dollar buys more every month. Your thousand dollars now shops like fourteen hundred.", [F(shops, 0), F(shops, 1)]),
 ("You took no risk, earned no interest, and came out ahead of everyone.", [F(ahead, 0), F(ahead, 1)]),
 ("There is a catch. By nineteen thirty-three, one worker in four has no job.", [F(jobs, 0), F(jobs, 1)]),
 ("If you're one of them, the mattress isn't a strategy. It's groceries.", [F(groceries, 0), F(groceries, 1), F(groceries, 2)]),
 ("And there was a fifth door that nobody at your office mentioned. The post office.", [F(fifth, 0), F(fifth, 1), F(post, 0)]),
 ("The Post Office takes savings. Two percent interest, run by the government, up to twenty-five hundred dollars.", [F(post, 1), F(post, 2), F(post, 3)]),
 ("By nineteen thirty-three, five times as many people are using it as before.", [F(x5, 0), F(x5, 1)]),
 ("Quest three, complete. Scoreboard.", [F(lineup, 1, 3), F(score, 0)], "chime"),
 ("Margin you: zero, in two days.", [F(score, 1)]),
 ("Stock you: about a hundred and ten dollars.", [F(score, 2)]),
 ("Bank you: somewhere between a thousand and nothing, depending on a rumor.", [F(score, 3)]),
 ("Mattress you: a thousand dollars that buys like fourteen hundred.", [F(score, 4)]),
 ("Post office you: a thousand, plus interest.", [F(score, 5)]),
 ("Now the hidden one.", [F(hiddenq, 0), F(hiddenq, 1)], "chime"),
 ("March, nineteen thirty-three. The banking system has collapsed. The new president closes every bank in the country.", [F(holiday, 0), F(holiday, 1), F(holiday, 2)]),
 ("They call it a bank holiday. Nobody is on holiday.", [F(nobody, 0), F(nobody, 1)]),
 ("That June, he signs a law that creates something new. The Federal Deposit Insurance Corporation. The F D I C.", [F(law, 0), F(law, 1), F(fdic, 0), F(fdic, 1)]),
 ("From January first, nineteen thirty-four, if your bank fails, you get your money back. Up to twenty-five hundred dollars.", [F(back, 0), F(back, 1), F(back, 2)]),
 ("Your thousand is covered. All of it.", [F(covered, 0), F(covered, 1)]),
 ("Think about what that does to the line around the block.", [F(line2, 0)]),
 ("If your money is safe either way, there's no reason to run. And if nobody runs, the bank doesn't break.", [F(line2, 1), F(line2, 2), F(line2, 3)]),
 ("The rumor stops working.", [F(rumor, 2, True)]),
 ("That's the fourth quest. Trust a bank again. And you didn't complete it. The rules did.", [F(fourth, 0), F(fourth, 1), F(fourth, 2), F(fourth, 3)], "tick"),
 ("As for stock you. Say you held those shares and never looked.", [F(drawer, 0), F(drawer, 1), F(drawer, 2)]),
 ("The Dow gets back to its nineteen twenty-nine high on November twenty-third, nineteen fifty-four.", [F(longc, 0), F(longc, 1)]),
 ("Twenty-five years. You were twenty-four. Now you're forty-nine.", [F(ages, 0), F(ages, 1), F(ages, 2)]),
 ("That's counting price alone, not dividends. It's still a long time to be right.", [F(longc, 2), F(longc, 3)]),
 ("So what was the smart move in September, nineteen twenty-nine?", [F(smart, 0)]),
 ("With hindsight, the boring one. And nobody at the time could have proved it.", [F(smart, 1), F(smart, 2)]),
 ("The economist had a plateau. The bankers had a plan. The guy at the office had a tip.", [F(three, 0), F(three, 1), F(three, 2)]),
 ("You had a thousand dollars and four doors.", [F(youhad, 0), F(youhad, 1)]),
 ("Next time you walk into an American bank, look for a small sign by the door. F D I C.", [F(sign, 0), F(sign, 1), F(sign, 2)]),
 ("It's there because of the line around the block.", [F(sign, 3)]),
 ("Quest complete.", [F(finale, 0)], "chime"),
]

# Display spellings for captions (applied in order, so longer phrases come first).
CAPTION_FIX = [("R C A", "RCA"), ("F D I C", "FDIC"),
               ("October twenty-fourth", "October 24th"), ("October twenty-eighth", "October 28th"), ("October twenty-ninth", "October 29th"), ("July eighth", "July 8th"),
               ("November twenty-third", "November 23rd"), ("January first", "January 1st"), ("September third", "September 3rd"),
               ("nineteen twenty-nine", "1929"), ("nineteen twenty-one", "1921"), ("nineteen thirty-three", "1933"), ("nineteen thirty-four", "1934"), ("nineteen thirty-two", "1932"),
               ("nineteen thirty-one", "1931"), ("Nineteen thirty-one", "1931"), ("nineteen thirty", "1930"), ("nineteen fifty-four", "1954"),
               ("three hundred and eighty-one", "381"), ("three eighty-one", "381"), ("sixty-three", "63"), ("forty-one", "41"),
               ("Two hundred million dollars", "$200 million"), ("one point three billion dollars", "$1.3 billion"), ("twenty-five hundred dollars", "$2,500"),
               ("thirteen hundred and fifty", "1,350"), ("thirteen hundred dollars", "$1,300"), ("twenty-three hundred", "2,300"), ("nine thousand", "9,000"),
               ("ten thousand dollars", "$10,000"), ("one thousand dollars", "$1,000"), ("A thousand dollars", "$1,000"), ("a thousand dollars", "$1,000"), ("one thousand of your own", "$1,000 of your own"), ("thousand dollars", "$1,000"),
               ("a hundred and ten dollars", "$110"), ("a hundred and ten", "$110"), ("fourteen hundred", "$1,400"), ("three hundred you never had", "$300 you never had"),
               ("eighty-nine percent", "89%"), ("thirteen percent", "13%"), ("twelve percent", "12%"), ("thirty percent", "30%"), ("ten percent", "10%"), ("Two percent", "2%"),
               ("thirteen million", "13 million"), ("Sixteen million", "16 million"), ("one and a half million", "1.5 million"),
               ("Twenty-five years", "25 years"), ("twenty-four", "24"), ("forty-nine", "49"), ("eleven cents", "11 cents")]
