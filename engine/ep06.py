"""EP006: What Did Vikings Do All Winter?   (a farm in central Norway, about AD 950; daily-life pillar)

Same contract as ep01.py to ep05.py. Motion helpers (app, E, lerp, step, arrow) come from ep02; the sky, the little people and the counters from ep05.
The first frame is the scene itself, close and moving: no text card before it (the lesson of the EP001 and EP003 retention curves).
A bar in the top-left corner carries the 180 days of the Icelandic calendar's winter through the episode; it shows a number only where the script gives one.
Scenes set in the present (the Danish experiment, the DNA study, the digs) wear a place-and-year tag instead of the bar.
Fires, smoke, snow, breath, the sun's low arc, skaters, spindles and every counter move with T.TT / T.LT / T.LP / T.GP and rest in their final state on the contact sheet.
The maps are sketches (modern coastlines, roughly drawn) and say so on screen. Faces, clothes and the farm are invented and drawn plainly.
"""
from thsq import *
import math
import thsq as T
import life
from ep02 import E, app, lerp, step, card, arrow, chip, F
from ep05 import sky as sky5, book, icon, icons, count, dimc, beard
ROWS = ["FILL THE HOUSE", "STAY WARM, DON'T CHOKE", "GET THROUGH 180 DAYS"]; HID = "THE LOOM"
EV = (238, 226, 204); SEAM = (196, 220, 230); SNOWG = (236, 242, 248); WALLC = (104, 74, 52); WALLD = (78, 54, 40); FLOORC = (132, 102, 76); BENCH = (150, 110, 78)
BARC = (120, 170, 210); MEAT = (196, 110, 90); DRESS = {"rose": (176, 96, 96), "blue": (70, 110, 150), "green": (84, 130, 96), "brown": (128, 92, 64), "slate": (74, 80, 108), "teal": (24, 122, 118), "red": (160, 60, 50)}
GROUND = {"snow": SNOWG, "autumn": (198, 180, 112), "spring": (156, 194, 124), "night": (146, 160, 194), "dusk": (216, 208, 222), "wet": (150, 166, 120)}

# ---------- small helpers ----------
def L(c, t, y=210, x=W/2, size=64, **k): c.label(x, y, t, size, **k); return c
def Q(c, shown=4, done=0, hidden=None): c.questlog(ROWS, shown, done, hidden); return c
def tag(c, t, x=36, y=36, col=PAPER):
    w = c.tw(t, 44)+56; c.rect(x, y, x+w, y+76, col, INK, 6, 16); c.text(x+28, y+35, t, 44, INK, "lm"); return x+w
def flake(c, x, y, r=22, col=(70, 120, 170), w=5):
    for a in range(0, 180, 60): dx, dy = r*math.cos(math.radians(a)), r*math.sin(math.radians(a)); c.line([(x-dx, y-dy), (x+dx, y+dy)], w, col, False)
def hud(c, frac=None, t=None, where=None):
    """Top left: the winter bar. frac = how much of the 180 days is gone (0..1); t = words beside it, used only where the script gives a number."""
    x = 36
    if where: x = tag(c, where)+16
    if frac is not None:
        w = 84+270+(c.tw(t, 40)+34 if t else 0)+22; c.rect(x, 36, x+w, 112, PAPER, INK, 6, 16); flake(c, x+44, 74, 22); c.rect(x+84, 56, x+354, 92, WHITE, INK, 5, 8)
        if frac > 0: c.rect(x+84, 56, x+84+max(14, 270*min(1, frac)), 92, BARC, INK, 5, 8)
        c.line([(x+219, 50), (x+219, 98)], 4, INK, False)
        if t: c.text(x+372, 73, t, 40, INK, "lm")
    return c
def mapnote(c, t="SKETCH MAP, NOT TO SCALE"):
    w = c.tw(t, 44)+44; c.rect(20, 1004, 20+w, 1070, SEAM, None, 0, 10); c.text(42, 1038, t, 44, (70, 100, 116), "lm")
def nmap(lonc=4.0, latc=60.0, sy=38.0, note=True):
    c = C(SEAM); P = c.northmap(lonc, latc, sy)
    if note: mapnote(c)
    return c, P
def place(c, P, name, t=None, dx=0, dy=-70, size=44, r=13, col=RED, ring=False, **k):
    lo, la = NORTHPLACES[name]; x, y = P(lo, la); q = app(("dot", name), .25); c.ell(x-r*q, y-r*q, x+r*q, y+r*q, col, INK, 5)
    if ring:
        for i in range(3): rr = 24+30*((T.TT*.8+i/3) % 1); c.ell(x-rr, y-rr, x+rr, y+rr, None, col, 4)
    if t: c.label(x+dx, y+dy, t, size, **k)
    return x, y
def sunlow(c, x, y, r=56, col=MARI):
    c.da.ellipse([(x-r*2.3)*S, (y-r*2.3)*S, (x+r*2.3)*S, (y+r*2.3)*S], fill=(255, 226, 130, 70)); c.ell(x-r, y-r, x+r, y+r, col, INK, 6)
def snowf(c, n=70, seed=0, big=5): c.snowfall(n, T.TT, seed, big)
def rainf(c, n=70, col=(200, 214, 226, 170)):
    for i in range(n):
        x = (i*211+int(T.TT*900)) % (W+300)-150; y = (i*137+int(T.TT*1500)) % (H+200)-100; c.da.line([x*S, y*S, (x-26)*S, (y+70)*S], fill=col, width=3*S)
def sidp(c, x, y, h, pose="stand", ex="n", **k): return c.fig(x, y, h, pose, ex, "modern", **k)
def cape(c, x, y, h, col=(84, 96, 132), flip=False):
    """A cloak hanging behind a figure that is about to be drawn at (x, y, h)."""
    u = h*1.25/3.5; c.poly([(x-.62*u, y-2.42*u), (x+.62*u, y-2.42*u), (x+.86*u, y-.5*u), (x-.86*u, y-.5*u)], col, INK, max(4, u*.07))
def sidc(c, x, y, h, pose="stand", ex="n", col=(84, 96, 132), **k):
    """Sid in a cloak, for outdoors."""
    if not k.get("rot"): cape(c, x, y, h, col)
    return sidp(c, x, y, h, pose, ex, **k)
def man(c, x, y, h=320, pose="stand", ex="n", coat="brown", flip=False, bd=False, cloak=None, **k):
    if cloak and not k.get("rot"): cape(c, x, y, h, cloak)
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k)
    if bd and not k.get("rot"): beard(c, f, flip, (120, 84, 50) if bd is True else bd)
    return f
def woman(c, x, y, h=310, pose="stand", ex="n", coat="rose", flip=False, **k):
    """A woman as drawn here: a long dress and a head-cloth. Clothes are generic, not copied from a find."""
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); u = f["u"]; hx, hy = f["head"]; d = -1 if flip else 1; col = DRESS.get(coat, (150, 110, 90))
    if not k.get("sit") and not k.get("rot"): c.poly([(x-.44*u, y-1.34*u), (x+.44*u, y-1.34*u), (x+.74*u, y-.05*u), (x-.74*u, y-.05*u)], col, INK, max(4, u*.07))
    if not k.get("rot"):
        c.d.pieslice([(hx-.66*u)*S, (hy-.2*u)*S, (hx+.66*u)*S, (hy+.8*u)*S], 180, 360, fill=WOOLC, outline=INK, width=int(max(4, u*.07)*S))
        c.poly([(hx-d*.62*u, hy+.3*u), (hx-d*.92*u, hy+.86*u), (hx-d*.5*u, hy+.62*u)], WOOLC, INK, max(3, u*.06))
    return f
def kid(c, x, y, h=190, pose="stand", ex="n", coat="green", flip=False, **k): return c.person(x, y, h, pose, ex, coat, flip=flip, **k)
def sci(c, x, y, h=330, pose="stand", ex="n", flip=False, **k): return c.fig(x, y, h, pose, ex, "sci", flip, **k)
def blanket(c, x0, y0, x1, y1, col=(150, 120, 96)):
    """A wool blanket lying over someone: a soft outline that rises and falls with their breathing, folds, a fringe along the hem."""
    br = 6*math.sin(T.TT*1.6+x0*.01); n = 9; w = x1-x0; dk = tuple(int(v*.8) for v in col)
    top = [(x0+w*i/n, y0-br-(y1-y0)*.07*math.sin(i/n*math.pi)*(1+.5*math.sin(i*1.9))) for i in range(n+1)]
    hem = [(x1-w*i/n, y1+(y1-y0)*.03*math.sin(i*2.1)) for i in range(n+1)]
    c.poly(top+hem, col, INK, 6)
    for i in range(1, n, 2): xx = x0+w*i/n; c.line([(xx, y0-br+(y1-y0)*.16), (xx+w*.03, (y0+y1)/2), (xx-w*.01, y1-(y1-y0)*.16)], 4, dk, False)
    for i in range(int(w/26)): xx = x0+10+i*26; c.line([(xx, y1-2), (xx, y1+12)], 3, dk, False)
def breath(c, x, y, k=1.0, flip=False):
    """A puff of breath in cold air."""
    d = -1 if flip else 1
    for i in range(3):
        q = ((i/3+T.TT*.5) % 1); r = (12+q*30)*k; xx = x+d*q*90*k; yy = y-q*26*k; c.da.ellipse([(xx-r)*S, (yy-r)*S, (xx+r)*S, (yy+r)*S], fill=(255, 255, 255, int(170*(1-q))))

# ---------- sets ----------
def land(sk="cold", ground="snow", hz=640, sun=None, mts=True, seed=1, moon=None):
    """Open country: sky, mountains on the horizon, the ground."""
    G = GROUND[ground]; c = C(G); sky5(c, hz, sk, clouds=sk != "night", sun=bool(moon), sx=moon or 1560)
    if sun: sunlow(c, *sun)
    if mts: c.peaks(hz, h=250, seed=seed, col=(128, 140, 170) if sk != "night" else (44, 52, 84))
    c.rect(0, hz, W, H, G, None); c.line([(0, hz), (W, hz)], 6, INK, False)
    for i in range(11):
        x = (i*197) % W; y = hz+70+(i*83) % (H-hz-120)
        if ground in ("snow", "night", "dusk"): c.line([(x, y), (x+70, y-8), (x+140, y)], 4, SNOWD if ground != "night" else (120, 134, 170), False)
        else: c.line([(x, y), (x+8, y-26)], 5, (150, 140, 80) if ground == "autumn" else (110, 150, 90), False); c.line([(x+14, y), (x+26, y-22)], 5, (150, 140, 80) if ground == "autumn" else (110, 150, 90), False)
    return c
def farm(sk="cold", ground="snow", lit=False, sun=None, x=760, y=850, w=860, smoke=True, byre=True, hz=640, seed=1, moon=None, rp=True, mts=True):
    """The farm from outside: the longhouse, a byre, a fence, pines. rp=False leaves out the pines on the right (behind the quest log)."""
    c = land(sk, ground, hz, sun, seed=seed, moon=moon, mts=mts); sn = ground in ("snow", "night", "dusk")
    for px, k in ((96, 1.5), (236, 1.1), (1800, 1.6), (1650, 1.0)):
        if rp or px < 1000: c.pine(px, hz+50+k*46, k, sn)
    if byre: c.longhouse(x+w/2+320, y-36, 380, 200, snow=sn, smoke=False, door=.5)
    c.longhouse(x, y, w, 310, snow=sn, smoke=smoke, lit=lit)
    for fx in range(40, 300, 84): c.line([(fx, y+60), (fx, y-10)], 9, TIMBER, False)
    c.line([(20, y+10), (300, y+10)], 7, TIMBER, False); c.line([(20, y+40), (300, y+40)], 7, TIMBER, False)
    return c
def haze(c, a=1.0, y0=40, y1=520, n=9):
    """Wood smoke hanging under the roof."""
    for i in range(n):
        x = (i*263+T.TT*(18+i*3)) % (W+600)-300; y = y0+(i*97) % max(1, (y1-y0)); r = 150+(i*37) % 110
        c.da.ellipse([(x-r*1.9)*S, (y-r*.55)*S, (x+r*1.9)*S, (y+r*.55)*S], fill=(226, 222, 214, int(min(255, 46*a))))
def longfire(c, x0=620, x1=1300, y=960, k=1.0):
    """The long fireplace: a stone-edged strip down the middle of the floor."""
    n = int((x1-x0)/56)
    if k > 0: c.da.ellipse([(x0-260)*S, (y-360*k)*S, (x1+260)*S, (y+120)*S], fill=(255, 170, 60, int(34+10*math.sin(T.TT*8))))
    c.rect(x0-20, y-14, x1+20, y+24, (58, 50, 48), INK, 5, 12)
    if k > 0:
        m = max(2, n//2)
        for i in range(m): xx = x0+44+(x1-x0-88)*i/max(1, m-1); life._fire(c, xx, y+2, k*(.72+.22*math.sin(T.TT*10+i*2.1)+.1*(i % 3)))
    else:
        for i in range(n): xx = x0+30+(x1-x0-60)*i/max(1, n-1); c.ell(xx-10, y-8, xx+10, y+8, (226, 110, 50) if (i+int(T.TT*2)) % 3 else (150, 70, 40), None)
    for i in range(n+1): xx = x0+(x1-x0)*i/n; c.ell(xx-24, y+2, xx+24, y+36, (150, 146, 140), INK, 4)
def hall(fire=1.0, hole="night", smoke=1.0, x0=620, x1=1300, dim=0, posts=(300, 1620), fy=960):
    """Inside the longhouse, looking at one long wall: the plank bench along it, the roof posts, the long fire on the floor, the smoke hole in the roof."""
    c = C(WALLC)
    for xx in range(0, W, 64): c.line([(xx, 150), (xx, 640)], 3, WALLD, False)
    c.rect(0, 0, W, 150, (70, 50, 40), None)
    for xx in range(-200, W+200, 190): c.line([(xx, 150), (xx+120, 0)], 12, (50, 36, 30), False)
    c.rect(860, -10, 1060, 54, {"night": (20, 28, 60), "day": (196, 218, 236), "dusk": (124, 112, 152)}[hole], INK, 6); c.line([(0, 150), (W, 150)], 8, (50, 36, 30), False)
    c.rect(-10, 640, W+10, 700, BENCH, INK, 6); c.rect(-10, 700, W+10, 800, (120, 86, 60), INK, 6)
    for xx in range(120, W, 240): c.line([(xx, 706), (xx, 794)], 4, WALLD, False)
    c.rect(0, 800, W, H, FLOORC, None); c.line([(0, 800), (W, 800)], 6, INK, False)
    for i in range(9): x = (i*233) % W; y = 850+(i*71) % 200; c.line([(x, y), (x+40, y)], 4, (112, 86, 64), False)
    for px in posts: c.rect(px-26, 0, px+26, 846, (86, 60, 44), INK, 6)
    if fy: longfire(c, x0, x1, fy, fire)
    if smoke:
        if fy:
            for i in range(7):
                q = ((i/7+T.TT*.1) % 1); xx = lerp((x0+x1)/2, 960, q)+34*math.sin(T.TT+i*2); yy = lerp(fy-120, 30, q); r = 36+q*76
                c.da.ellipse([(xx-r)*S, (yy-r)*S, (xx+r)*S, (yy+r)*S], fill=(232, 228, 220, int(90*(1-q*.5)*min(1, smoke))))
        haze(c, smoke)
    if dim: dimc(c, dim)
    return c
def onbench(c, x, h=300, pose="stand", ex="n", coat="brown", flip=False, w=False, **k):
    """Someone sitting on the wall bench, legs hanging down its front (the bench top is at the hips)."""
    return (woman if w else man)(c, x, 792, h, pose, ex, coat, flip=flip, **k)
def asleep(c, x, h=280, coat="brown", flip=False, col=(150, 120, 96)):
    """Someone asleep on the wall bench under a blanket; head to the left unless flip."""
    u = h*1.25/3.5; c.person(x, 590, h, "stand", "sleep", coat, rot=90 if flip else -90); d = 1 if flip else -1
    a, b = sorted((x-d*.2*u, x+d*2.75*u)); blanket(c, a, 528, b, 646, col)
def ice(sk="cold", sun=None, hz=600, seed=3, pines=True):
    """A frozen lake under the mountains."""
    c = land(sk, "snow", hz, sun, seed=seed)
    if pines:
        for px, k in ((120, 1.3), (300, .9), (1700, 1.4), (1860, 1.0)): c.pine(px, hz+40+k*30, k, True)
    c.poly([(-10, H+10), (-10, 760), (260, 716), (700, 700), (1300, 704), (1700, 724), (W+10, 770), (W+10, H+10)], ICEC, INK, 6)
    for i in range(12): x = (i*173+40) % W; y = 800+(i*59) % 230; c.line([(x, y), (x+90, y-10)], 4, ICED, False)
    return c
def ev(t=None, col=EV):
    """A plain page for evidence from the present day, with its place-and-year tag."""
    c = C(col)
    if t: tag(c, t)
    return c
def table(c, x0=560, x1=1360, y=1010, h=170, col=WOOD):
    c.line([(x0+50, y-h), (x0+50, y)], 18, TIMBER, False); c.line([(x1-50, y-h), (x1-50, y)], 18, TIMBER, False); c.rect(x0, y-h-34, x1, y-h, col, INK, 6, 4)
def hang(c, x, y, kind="ham", k=1.0, sw=0.0):
    """Something hanging from a hook at (x, y)."""
    c.line([(x, y), (x+sw*.3, y+40*k)], 5, INK, False)
    if kind == "ham": joint(c, x+sw*.3, y+36*k, k)
    elif kind == "cod": c.cod(x, y+30*k, k*.9, True, sw)
    else:
        pts = [(x+sw*(.3+i*.15), y+40*k+i*44*k) for i in range(5)]; c.line(pts, 5, INK, False)
        for (xx, yy) in pts[:-1]: c.ell(xx-20*k, yy+2*k, xx+20*k, yy+42*k, (150, 70, 60), INK, max(3, 5*k))
def stores(c, y=200, t=0.0, n=7):
    """A beam hung with the winter's food."""
    c.line([(0, y), (W, y)], 22, (60, 44, 34), False)
    for i in range(n): x = 180+i*(W-360)/(n-1); hang(c, x, y, ("ham", "saus", "cod", "ham", "cod", "saus", "ham")[i % 7], 1.0, 10*math.sin(T.TT*1.2+i))

# ================= cold open =================
def wake(k):
    if k == 0:
        # close on the bench: the wall planks, the sleeper, the ember light, the smoke crossing the frame
        c = C(WALLD)
        for xx in range(0, W, 150): c.line([(xx, 0), (xx, 820)], 5, (60, 42, 32), False)
        c.rect(-10, 820, W+10, 900, BENCH, INK, 8); c.rect(-10, 900, W+10, H+10, (110, 78, 54), INK, 8)
        g = .5+.5*math.sin(T.TT*3.1); c.da.ellipse([900*S, 500*S, 2500*S, 1500*S], fill=(255, 150, 50, int(40+26*g)))
        op = T.LT > .9; f = sidp(c, 1620, 690, 640, "stand", ("wow" if T.LT < 1.5 else "worry") if op else "sleep", rot=-90)
        blanket(c, 1230, 500, 1800, 850, (156, 124, 98)); br = 6*math.sin(T.TT*1.6+12.3)
        c.line([(1130, 650), (1300, 610-br), (1470, 640-br)], 18, INK, False); c.ell(1470-28, 640-br-28, 1470+28, 640-br+28, PAPER, INK, 12)
        if op and T.LT > 1.5:
            for i in range(3): q = ((i/3+T.TT*.9) % 1); r = 16+q*30; c.da.ellipse([(900-q*150-r)*S, (600-q*60-r)*S, (900-q*150+r)*S, (600-q*60+r)*S], fill=(240, 236, 228, int(190*(1-q))))
        dimc(c, 70 if not op else 40, (20, 14, 10)); haze(c, 1.5, 60, 520, 10); return c
    c = hall(fire=.34, hole="night", smoke=1.6, dim=60); asleep(c, 600, 290, "slate"); asleep(c, 1780, 290, "green", col=(128, 110, 120))
    s = sidbench(c, 1000, "chin", "pain" if int(T.TT*2.2) % 2 == 0 else "worry"); blanket(c, 880, 664, 1120, 800, (156, 124, 98))
    for i in range(3): q = ((i/3+T.TT*.9) % 1); r = 14+q*26; c.da.ellipse([(s["head"][0]+70+q*110-r)*S, (s["head"][1]+70-q*40-r)*S, (s["head"][0]+70+q*110+r)*S, (s["head"][1]+70-q*40+r)*S], fill=(240, 236, 228, int(200*(1-q))))
    haze(c, 1.0, 60, 480); return c
def where(k):
    if k == 0:
        c = farm("night", "night", lit=True, moon=1500); snowf(c, 60); tag(c, "CENTRAL NORWAY, ABOUT AD 950"); L(c, "LATE DECEMBER", 250, 420, 76); return c
    if k == 1:
        c, P = nmap(8, 62, 62); x, y = place(c, P, "FARM", "YOU ARE ABOUT HERE", 330, -30, 54, ring=True); tag(c, "CENTRAL NORWAY, ABOUT AD 950"); return c
    c = C(NIGHT_); cx, cy, r = 560, 590, 330; c.ell(cx-r, cy-r, cx+r, cy+r, (24, 30, 62), INK, 8); a = 67.5*app("lit", .8)
    if a > 1: c.d.pieslice([(cx-r+8)*S, (cy-r+8)*S, (cx+r-8)*S, (cy+r-8)*S], 270-a/2, 270+a/2, fill=(250, 214, 110))
    for i in range(24): an = math.radians(i*15); c.line([(cx+(r-34)*math.cos(an), cy+(r-34)*math.sin(an)), (cx+(r-8)*math.cos(an), cy+(r-8)*math.sin(an))], 5, PAPER, False)
    c.ell(cx-16, cy-16, cx+16, cy+16, PAPER, INK, 5); c.text(cx, cy+r+56, "ONE DAY: 24 HOURS", 50, PAPER)
    c.text(1330, 430, "4½", 360, (250, 214, 110)); c.text(1330, 690, "HOURS OF", 110, PAPER); c.text(1330, 810, "DAYLIGHT", 110, PAPER); return c
NIGHT_ = (20, 26, 54)
def days(k):
    c = C(EV); n = count(0, 180, 1.3, .1, "c180"); c.text(960, 470, str(n), 380, NAVY); c.text(960, 720, "DAYS OF WINTER", 110)
    c.rect(360, 820, 1560, 880, WHITE, INK, 7, 12); c.rect(360, 820, 360+max(16, 1200*n/180), 880, BARC, INK, 7, 12); flake(c, 300, 850, 34, w=7)
    L(c, "BY THE OLD ICELANDIC CALENDAR", 190, 960, 60, bg=MARI); return c
def store(k):
    c = hall(fire=0, hole="day", smoke=0, fy=0, posts=(1700,)); stores(c, 190)
    c.barrel(260, 800, 1.0); c.barrel(420, 800, 1.0); c.sack(620, 800, 1.1); c.vat(1340, 800, .62); c.sack(1560, 800, 1.0)
    s = sidp(c, 960, 1040, 360, "chin", "worry"); hud(c, .37)
    if k: L(c, "IT HAS TO LAST", 480, 1420, 84, bg=MARI)
    return c
def summer(k):
    if k == 0:
        c = C((78, 138, 172)); sky5(c, 520, "day", sx=320); c.peaks(520, h=170, seed=4, col=(126, 160, 150), snow=False); c.swell(520, T.TT*.5, (54, 104, 142), 5, 420)
        x = lerp(1500, 900, T.GP); c.longship(x, 800, 760, flip=True, bob=T.TT*1.5, wind=T.TT); crew(c, x, 800, 760, True)
        c.swell(812, T.TT, (78, 138, 172), 11, 300, ph=3); c.crests(850, 1040, T.TT, 14); L(c, "SUMMER. YOU'VE HEARD THIS PART.", 170, 960, 62); return c
    c = land("grey", "snow", 600, seed=4); c.poly([(-10, 600), (W+10, 600), (W+10, 700), (-10, 720)], (112, 146, 166), INK, 6)
    c.longship(900, 900, 860, sail=0); c.poly([(440, 906), (560, 882), (1240, 882), (1350, 906), (1366, 938), (424, 938)], SNOWC, INK, 6)
    for xx in (600, 900, 1200): c.line([(xx, 938), (xx-30, 990)], 14, TIMBER, False)
    snowf(c, 80); hud(c, .37); L(c, "THIS IS THE OTHER HALF OF THE YEAR", 200, 1060, 60, bg=MARI); return c
def youare(k):
    if k == 0:
        c = C(); s = c.fig(760, 930-(1-T.ease(T.LT/0.3))*900, 520, "drop" if T.LT < .5 else "self", "wow" if T.LT < .5 else "smile", "modern"); c.marker(s["head"][0]+20, s["head"][1]-110, 46)
        if T.LT > .6: L(c, "YOU", 200, 1360, 130); L(c, "16 WINTERS OLD", 400, 1360, 76, bg=MARI)
        return c
    c = land("cold", "snow", 600, (1700, 520), seed=4); c.poly([(-10, 600), (W+10, 600), (W+10, 690), (-10, 706)], (112, 146, 166), INK, 6)
    c.longship(1430, 880, 700, sail=0); c.poly([(1090, 886), (1190, 866), (1670, 866), (1760, 886), (1776, 912), (1080, 912)], SNOWC, INK, 6)
    s = sidc(c, 300, 1030, 380, "point", "smile"); breath(c, s["head"][0]+70, s["head"][1]+90)
    q = app("th", .35, .3)
    if q > 0:
        for (dx, dy, r) in ((120, -30, 14), (200, -76, 22)): c.ell(s["head"][0]+dx-r, s["head"][1]+dy-r, s["head"][0]+dx+r, s["head"][1]+dy+r, WHITE, INK, 5)
        c.rect(560, 130, 1120, 500, WHITE, INK, 7, 60); c.longship(840, 370, 360*q, bob=T.TT*2, wind=T.TT); c.text(840, 446, "NEXT SUMMER?", 54)
    hud(c, .37); return c
def madeup(k):
    if k == 0:
        c = C(EV); sidp(c, 520, 960, 420, "self", "smile"); c.longhouse(1340, 880, 640, 240, smoke=False)
        for (x, t) in ((520, "YOU: MADE UP"), (1340, "THE FARM: MADE UP")): c.label(x, 250, t, 62, bg=MARI)
        return c
    if k == 1:
        c = C(EV); L(c, "THE EVIDENCE IS REAL", 170, 960, 84)
        for i, (x, t) in enumerate(((330, "A BONE SKATE"), (760, "A WOOL SOCK"), (1190, "COD BONES"), (1600, "A SAGA"))):
            q = app(("ev", i), .3, i*.35)
            if q <= 0: continue
            c.rect(x-195, 330, x+195, 920, PAPER, INK, 7, 22); c.text(x, 850, t, 52)
            if i == 0: c.boneskate(x+10, 620, .8*q)
            if i == 1: c.sock(x-50, 720, .9*q)
            if i == 2: fishbone(c, x-70, 540, 1.2*q); fishbone(c, x+70, 660, 1.0*q)
            if i == 3: book(c, x, 590, 1.9*q)
        return c
    if k == 2:
        c, P = nmap(-6, 61, 46)
        for i, (n, t, dx, dy) in enumerate((("FARM", "NORWAY", 150, -10), ("ICELAND", "ICELAND", 0, -90), ("DENMARK", "DENMARK", 190, 20), ("YORK", "YORK", -130, 30), ("ORKNEY", "ORKNEY", -170, -30), ("HAITHABU", "HAITHABU", 220, 60))):
            if T.LP*7 > i or not life._new(("mm", i)): place(c, P, n, t, dx, dy, 40)
        L(c, "FROM ALL OVER THE NORSE WORLD", 130, 620, 54, bg=MARI); return c
    c = C(EV); scribe(c); L(c, "SOME OF IT WAS WRITTEN DOWN CENTURIES LATER", 220, 960, 56); return c
def qfarm(shown, done=0, hidden=None):
    c = farm("cold", "snow", lit=True, sun=(420, 560), x=520, w=760, byre=False, rp=False); snowf(c, 40); return Q(c, shown, done, hidden)
def hiddenq(k, done=0):
    c = C(); c.questlog(ROWS, 4, done, None, x=545, y=200); return c
def noage(k=0):
    c = C(EV); c.text(960, 430, "THE  ? ? ?  AGE", 200, NAVY); c.line([(680, 560), (1010, 560)], 10, RED, False); sidp(c, 960, 1020, 300, "shrug", "n"); return c
def qcard(n, t): return card("QUEST "+n, t)
def qdone(n, hidden=None, sk="cold", ground="snow", snow=True):
    c = farm(sk, ground, lit=True, sun=(420, 560), x=520, w=760, byre=False, rp=False)
    if snow: snowf(c, 50)
    return Q(c, 4, n, hidden)

# ================= quest one: fill the house =================
def byre(hay=1.0, cows=3, dimv=0, sp=400, x0=500):
    """The cattle end: stalls, cows, the hay they are eating."""
    c = hall(fire=0, hole="day", smoke=0, fy=0, posts=())
    for i in range(cows+1): x = x0-200+i*sp; c.rect(x-14, 560, x+14, 1010, (86, 60, 44), INK, 6)
    for i in range(cows): c.ox(x0+i*sp, 1010, 1.25 if sp >= 400 else 1.05, c=((176, 124, 88), (214, 196, 170), (120, 92, 76))[i % 3], step=T.TT*1.5+i)
    if hay > .03: c.haycock(1640, 1030, 1.5*hay)
    if dimv: dimc(c, dimv)
    return c
def october(k=0):
    c = farm("day", "autumn", sun=(1560, 250), x=640, w=760); c.haycock(1500, 1010, 1.1); c.haycock(1720, 990, .9); c.haycock(1280, 1040, 1.0)
    sidp(c, 300, 1040, 330, "walk" if step() else "stand", "n"); hud(c, 0, None, "OCTOBER"); return c
def seasons(k):
    c = C(EV); cx, cy, r = 960, 600, 360; c.d.pieslice([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], 90, 270, fill=(236, 206, 110)); c.d.pieslice([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], 270, 450, fill=(166, 200, 228))
    c.ell(cx-r, cy-r, cx+r, cy+r, None, INK, 9); c.line([(cx, cy-r), (cx, cy+r)], 9, INK, False); sunlow(c, cx-170, cy, 60); flake(c, cx+170, cy, 76, w=12)
    a = T.TT*.5; c.line([(cx, cy), (cx+(r-40)*math.cos(a), cy+(r-40)*math.sin(a))], 12, RED, False); c.ell(cx-18, cy-18, cx+18, cy+18, RED, INK, 5)
    L(c, "THE ICELANDIC CALENDAR: TWO SEASONS", 130, 960, 60, bg=MARI)
    if k: c.text(300, 600, "SUMMER", 110, (170, 120, 30)); c.text(1630, 600, "WINTER", 110, (60, 100, 150))
    return c
def begins(k):
    c = C(EV)
    if k == 0:
        c.calpage(520, 540, 1.6, "OCTOBER", "SAT", c=NAVY); c.text(520, 880, "WINTER BEGINS", 80, NAVY); c.text(1300, 430, "DAY 1", 170, NAVY); c.rect(1000, 560, 1600, 620, WHITE, INK, 7, 12); c.rect(1000, 560, 1016, 620, BARC, INK, 7, 6); c.text(1300, 700, "OF 180", 90)
        return c
    s = sidp(c, 420, 1000, 430, "self", "smile"); n = int(16*app("fl", 1.0, .1)+.5)
    for i in range(n): flake(c, 900+(i % 8)*110, 420+(i//8)*150, 40, w=8)
    if k == 1: L(c, "YOUR AGE: 16 WINTERS", 200, 1280, 70); return c
    c.text(1100, 800, "YEARS", 130, GREY); c.strike(940, 800, 1260); c.text(1580, 800, "WINTERS", 130, NAVY); L(c, "YOUR AGE: 16 WINTERS", 200, 1280, 70); return c
def hayq(k):
    c = hall(fire=0, hole="day", smoke=0, fy=0, posts=(1760,))
    for i in range(4): c.haycock(640+i*330, 1010-(i % 2)*30, 1.5)
    s = sidp(c, 280, 1040, 360, "point", "det" if k == 0 else "worry")
    if k:
        for i in range(4):
            if T.LP*5 > i: c.text(640+i*330, 720-(i % 2)*30, str(i+1), 120, PAPER)
        L(c, "HOW MUCH HAY DID YOU CUT?", 300, 1100, 70, bg=MARI)
    hud(c, 0, None, "AUTUMN"); return c
def cattle(k):
    if k < 2:
        c = byre(1.0 if k == 0 else lerp(1.0, .45, T.LP)); tag(c, "ICELAND: THE BEST EVIDENCE")
        L(c, "CATTLE SPEND THE WINTER INDOORS" if k == 0 else "EATING THE HAY", 300, 900, 64 if k == 0 else 84, bg=PAPER if k == 0 else MARI); return c
    c = land("cold", "snow", 620, (1500, 540), seed=5)
    for i, (x, y) in enumerate(((420, 900), (760, 980), (1120, 900), (1460, 1000))):
        xx = x+T.GP*30*(1 if i % 2 else -1); d = -1 if i % 2 else 1
        for j in range(4): tx = xx+d*(150+j*26); c.line([(tx, y+6), (tx+d*8, y-34-(j % 2)*12)], 6, (120, 150, 90), False)
        c.sheep(xx, y, 1.7, flip=i % 2 == 1, step=T.TT*2+i)
    snowf(c, 40); tag(c, "ICELAND: THE BEST EVIDENCE"); L(c, "SHEEP ARE TOUGHER. THEY CAN GRAZE OUTSIDE.", 300, 960, 58); return c
ANIM = [("ox", 300), ("ox", 560), ("sheep", 820), ("sheep", 1040), ("pig", 1270), ("ox", 1560)]
def herd(c, y=900, marks=None, k=1.0):
    for i, (a, x) in enumerate(ANIM):
        if a == "ox": c.ox(x, y, .9*k, c=((176, 124, 88), (214, 196, 170))[i % 2], step=T.TT+i)
        elif a == "sheep": c.sheep(x, y, 1.3*k, step=T.TT+i)
        else: c.pig(x, y, 1.1*k)
        m = marks[i] if marks else None
        if m == "?": c.text(x, y-300, "?", 130, NAVY)
        elif m == "v" and app(("mk", i), .25, i*.22) > .5: c.tick(x, y-290, 44)
        elif m == "x" and app(("mk", i), .25, i*.22) > .5: c.redx(x, y-100, 70, 18)
def sumf(k):
    if k == 0:
        c = C(EV); a = 5*math.sin(T.TT*1.3); c.line([(960, 330), (960, 800)], 22, TIMBER, False); c.poly([(860, 800), (960, 740), (1060, 800)], TIMBER, INK, 6)
        dy = 420*math.sin(math.radians(a)); xs = ((520, 330+dy), (1400, 330-dy)); c.line([xs[0], xs[1]], 20, INK, False); c.line([xs[0], xs[1]], 12, TIMBER, False)
        for i, (x, y) in enumerate(xs):
            c.line([(x, y), (x-170, y+230)], 5, INK, False); c.line([(x, y), (x+170, y+230)], 5, INK, False); c.rect(x-220, y+230, x+220, y+256, WOOD, INK, 6, 8)
            if i == 0: c.haycock(x-90, y+230, 1.0); c.haycock(x+90, y+230, .8)
            else: c.ox(x-90, y+230, .72); c.sheep(x+130, y+230, .9)
        c.text(520, 190, "HAY", 110, (150, 120, 40)); c.text(1400, 190, "ANIMALS", 110, NAVY); L(c, "EVERY AUTUMN, THE FARM DOES A SUM", 920, 960, 60, bg=MARI); return c
    if k == 1:
        c = ev("ICELAND: AN EXCAVATED FARM"); c.rect(0, 860, W, H, (176, 150, 112), None); c.line([(0, 860), (W, 860)], 6, INK, False); c.poly([(900, 860), (940, 1000), (1700, 1000), (1740, 860)], (140, 112, 84), INK, 6)
        for i in range(6): c.ell(1000+i*112, 950+(i % 2)*10, 1050+i*112+(i % 3)*14, 992, (150, 146, 140), INK, 4)
        f = c.person(420, 1010, 400, "point", "n", "green", hat="cap"); say(c, f, 1120, 330, "THEY HAD TO DECIDE\nHOW MANY TO SLAUGHTER\nAND STORE.", 62); c.label(1300, 720, "AN ARCHAEOLOGIST WHO DUG THERE", 44, bg=MARI); return c
    c = C(EV); herd(c, 900, ["?"]*6 if k == 2 else ["v", "x", "v", "x", "x", "v"]); c.line([(120, 906), (1800, 906)], 6, INK, False)
    L(c, "HOW MANY TO KEEP?" if k == 2 else "KEEP. SLAUGHTER AND STORE.", 200, 960, 76, bg=PAPER if k == 2 else MARI); return c
def toomany(k):
    if k == 0:
        c = byre(0, 4, sp=350, x0=400); c.rect(1200, 180, 1800, 250, WHITE, INK, 7, 12); c.rect(1200, 180, 1200+max(14, 600*lerp(.8, .03, T.LP)), 250, HAYC, INK, 7, 12); c.text(1120, 214, "HAY", 70, PAPER)
        L(c, "KEEP TOO MANY...", 400, 700, 76); hud(c, lerp(.3, .8, T.LP)); return c
    c = farm("grey", "snow", x=1300, w=700, byre=False); c.ox(330, 1010, 1.3, c=(214, 196, 170)); f = sidc(c, 800, 1040, 340, "shrug", "worry"); snowf(c, 50)
    hud(c, .82); L(c, "THE HAY RUNS OUT BEFORE THE GRASS COMES BACK", 250, 960, 54, bg=MARI); return c
def wetsum(n=1):
    c = land("storm", "wet", 600, seed=2)
    for i, (x, y, k) in enumerate((((360, 880, 1.2), (900, 960, 1.5), (1480, 900, 1.3)) if n == 1 else ((620, 930, 1.3), (1380, 900, 1.0)))):
        c.poly([(x-110*k, y), (x-96*k, y-50*k), (x-40*k, y-84*k), (x+50*k, y-80*k), (x+100*k, y-44*k), (x+112*k, y)], (176, 160, 90), INK, 6)
        for j in range(5): c.line([(x-70*k+j*36*k, y-60*k), (x-80*k+j*36*k, y-14*k)], 4, (130, 120, 70), False)
        c.ell(x-210*k, y+6, x-20*k, y+44, (120, 150, 176), INK, 4)
        if n == 2: c.ell(x+60*k, y+40, x+300*k, y+90, (120, 150, 176), INK, 4)
    rainf(c, 90); return c
def wet(k):
    if k == 0: c = wetsum(); tag(c, "SUMMER"); L(c, "A COLD, WET SUMMER", 250, 960, 84); return c
    if k == 1:
        c = hall(fire=0, hole="day", smoke=0, fy=0, posts=(1760,)); c.haycock(1100, 1010, .8); sidp(c, 600, 1040, 380, "shrug", "worry"); L(c, "NOT ENOUGH HAY", 300, 960, 84, bg=MARI); hud(c, 0, None, "AUTUMN"); return c
    c = C(EV); herd(c, 900, ["x", "x", "v", "x", "x", "v"]); c.line([(120, 906), (1800, 906)], 6, INK, False); L(c, "LITTLE CHOICE BUT TO CULL HARD", 200, 960, 70, bg=MARI); return c
def better(k):
    c = hall(fire=1.0, hole="night", smoke=.7, x0=120, x1=520, fy=1000, posts=(300,)); table(c, 760, 1700, 1010, 190)
    for i, x in enumerate((880, 1080, 1290, 1500)): (c.ham(x, 772, .9) if i % 2 == 0 else c.bowl(x, 730, .8))
    c.jug(1630, 786, .7); man(c, 660, 1030, 340, "hold", "joy", "brown", bd=True); woman(c, 1800, 1030, 320, "hold", "smile", "blue", flip=True); s = sidp(c, 1190, 1040, 300, "cheer", "joy")
    L(c, ("A STRANGE RESULT", "ONE SCHOLAR OF ICELAND THINKS...", "...PEOPLE MAY HAVE EATEN BETTER THAN USUAL")[k], 330, 960, (76, 60, 54)[k], bg=PAPER if k < 2 else MARI)
    hud(c, .2); return c
def second(k):
    if k == 0: c = wetsum(2); tag(c, "THE NEXT SUMMER"); L(c, "THE DANGER: A SECOND BAD SUMMER", 250, 960, 66, bg=MARI); return c
    c = land("grey", "wet", 620, seed=2); c.ox(1100, 1000, 1.5, flip=True, c=(214, 196, 170)); c.sheep(1560, 1010, 1.5, flip=True)
    f = man(c, 560, 1030, 380, "hold", "worry", "brown", bd=True); c.line([f["hand"], (900, 800)], 6, (120, 84, 58), False); rainf(c, 50); L(c, "NOW YOU'RE TRYING TO KEEP WHAT'S LEFT", 250, 960, 60); return c
def keep(k):
    c = C(EV)
    for i, (x, t) in enumerate(((360, "DRY IT"), (960, "SMOKE IT"), (1560, "SALT IT"))):
        c.rect(x-250, 250, x+250, 930, PAPER, INK, 7, 22)
        if k < i: c.text(x, 590, "?", 200, GREY); continue
        q = app(("kp", i), .3); c.text(x, 330, t, 84*q, NAVY)
        if i == 0:
            c.line([(x-190, 420), (x+190, 420)], 14, TIMBER, False)
            for j in range(3): hang(c, x-130+j*130, 420, "ham", .8, 14*math.sin(T.TT*2+j))
            for j in range(3): yy = 700+j*60; xx = x-220+((T.TT*160+j*130) % 300); c.line([(xx, yy), (xx+50, yy-8), (xx+100, yy)], 5, (170, 170, 170), False)
        if i == 1:
            c.line([(x-190, 420), (x+190, 420)], 14, TIMBER, False); hang(c, x-90, 420, "saus", .8, 0); hang(c, x+90, 420, "ham", .8, 0); life._fire(c, x, 900, .9+.1*math.sin(T.TT*11)); c.smoke(x, 800, 4)
        if i == 2:
            c.barrel(x, 870, 1.4, lid=False); joint(c, x, 440, .9)
            for j in range(9): yy = 470+((T.TT*240+j*70) % 190); c.rect(x-110+j*26-4, yy-4, x-110+j*26+4, yy+4, WHITE, INK, 2)
            c.text(x, 896, "WHERE THERE'S SALT", 46, INK)
    return c
def saus(k):
    if k == 0:
        c = hall(fire=.8, hole="day", smoke=.6, x0=100, x1=460, fy=1000, posts=(300,)); table(c, 700, 1560, 1010, 190); woman(c, 1700, 1030, 330, "hold", "det", "green", flip=True); s = sidp(c, 560, 1040, 330, "hold", "n")
        n = int(9*T.ease(T.LP*1.2))+1; c.line([(770, 770), (770+n*82, 770)], 6, INK, False)
        for i in range(n): x = 780+i*82; c.ell(x-36, 748+(i % 2)*8, x+36, 792+(i % 2)*8, (150, 70, 60), INK, 5)
        c.bowl(1500, 734, .8, (150, 60, 50)); L(c, "SAUSAGES: THE OFFAL AND THE BLOOD", 320, 1000, 60); hud(c, .03); return c
    c = C(EV)
    if k == 1:
        c.vat(960, 900, 1.3, (244, 214, 110))
        for j in range(12): yy = 330+((T.TT*260+j*60) % 240); c.rect(800+j*28-5, yy-5, 800+j*28+5, yy+5, WHITE, INK, 2)
        L(c, "BUTTER, SALTED HARD", 190, 960, 84); return c
    c.text(600, 480, "FAT", 420, (226, 170, 60)); s = sidp(c, 1360, 980, 420, "hold", "joy"); c.rect(s["hand"][0]-10, s["hand"][1]-60, s["hand"][0]+90, s["hand"][1]+10, (244, 214, 110), INK, 6, 10); L(c, "IN A LONG WINTER, IT'S WHAT YOU NEED", 860, 640, 54, bg=MARI); return c
def vats(k):
    c = hall(fire=0, hole="day", smoke=0, fy=0, posts=(1780,)); c.vat(640, 1040, 1.5); c.vat(1320, 1040, 1.5); w = woman(c, 980, 1040, 330, "up" if k else "hold", "n", "blue"); tag(c, "ICELAND: NO SALT")
    if k:
        hx, hy = w["hand"]; y = lerp(hy+60, 640, T.ease(T.LP*1.3)); c.line([(hx, hy), (1300, y)], 6, INK, False); c.rect(1220, y, 1380, y+120, (214, 190, 140), INK, 6, 18); c.line([(1220, y+60), (1380, y+60)], 5, (120, 84, 58), False); c.line([(1300, y), (1300, y+120)], 5, (120, 84, 58), False)
    L(c, "BIG VATS OF CURDLED MILK", 330, 760, 66, bg=MARI if k else PAPER); return c
def shore(sk="cold", hz=560, seed=6, calm=False):
    """A northern coast: sea to steep mountains, a shelf of rock in front."""
    c = C((84, 116, 138)); sky5(c, hz, sk, sun=False); c.peaks(hz, h=380, seed=seed, col=(120, 130, 156)); c.swell(hz, T.TT*.5, (84, 116, 138), 5, 420); c.crests(hz+30, 800, T.TT*.5, 9, (200, 220, 226), 2)
    c.poly([(-10, H+10), (-10, 860), (300, 820), (900, 836), (1500, 816), (W+10, 850), (W+10, H+10)], (150, 150, 158), INK, 6)
    for i in range(7): x = 100+i*270; c.line([(x, 900+(i % 2)*50), (x+90, 890+(i % 2)*50)], 4, (120, 120, 130), False)
    return c
def lofo(k):
    if k == 0:
        c, P = nmap(13, 65, 120); a = place(c, P, "FARM", "YOU", -110, 0, 46); b = P(*NORTHPLACES["LOFOTEN"]); q = T.ease(T.LP*1.2)
        arrow(c, a[0]+10, a[1]-30, lerp(a[0]+10, b[0]-10, q), lerp(a[1]-30, b[1]+50, q), RED, 12, 40)
        if q > .9: c.label(b[0]+280, b[1]-10, "NORTH NORWAY", 54, bg=MARI)
        L(c, "FAR UP THE COAST", 950, 520, 70); return c
    if k == 1:
        c = shore(); c.fishrack(620, 900, 760, 430, 9, T.TT); c.fishrack(1500, 880, 520, 330, 6, T.TT+1); snowf(c, 30); L(c, "COD, HUNG ON WOODEN RACKS", 180, 960, 66); return c
    c = shore(); c.line([(-20, 230), (W+20, 230)], 30, INK, False); c.line([(-20, 230), (W+20, 230)], 20, TIMBER, False)
    for i in range(6): c.cod(200+i*300, 250, 3.0, T.LP > .5, 26*math.sin(T.TT*1.7+i))
    for j in range(5): yy = 380+j*120; xx = (T.TT*420+j*400) % (W+400)-200; c.line([(xx, yy), (xx+150, yy)], 6, PAPER, False)
    L(c, "AND THE COLD AIR DRIES IT", 930, 960, 70, bg=MARI); return c
def stock(k):
    if k == 0:
        c = shore(); s = sidc(c, 700, 1040, 420, "hold", "wow"); hx, hy = s["hand"]; stockfish(c, hx-70, hy+24, hx+360, hy-70, 34)
        for i in range(3): r = 30+40*((T.TT*1.6+i/3) % 1); c.d.arc([(hx+400-r)*S, (hy-80-r)*S, (hx+400+r)*S, (hy-80+r)*S], 300, 60, fill=INK, width=6*S)
        L(c, "STOCKFISH", 220, 1250, 110, bg=MARI); return c
    c = C(EV); stockfish(c, 220, 720, 800, 560, 54); n = count(1, 10, 1.2, .1, "c10")
    c.text(1340, 300, "AS MUCH AS", 80, NAVY); c.text(1340, 520, str(n), 340, NAVY); c.text(1340, 760, "YEARS LATER", 100); L(c, "SOME MEDIEVAL ACCOUNTS: STILL EDIBLE", 930, 960, 62, bg=MARI); return c
def helix(c, x0, x1, y, amp=70, ph=0.0):
    pa = [(x, y+amp*math.sin((x-x0)/70+ph)) for x in range(int(x0), int(x1)+1, 14)]; pb = [(x, y-amp*math.sin((x-x0)/70+ph)) for x in range(int(x0), int(x1)+1, 14)]
    for i in range(0, len(pa), 3): c.line([pa[i], pb[i]], 5, (150, 150, 160), False)
    c.line(pa, 10, TEAL, False); c.line(pb, 10, RED, False)
def dna(k):
    if k < 2:
        c = ev("2017"); table(c, 420, 1500, 1010, 210, (226, 226, 232))
        for i in range(5): fishbone(c, 580+i*190, 730-(i % 2)*10, .7)
        sci(c, 1700, 1020, 380, "chin" if k == 0 else "point", "det", flip=True)
        if k == 0: L(c, "FIVE COD BONES", 300, 960, 84); return c
        helix(c, 480, 1440, 420, 70, T.TT*2); L(c, "SCIENTISTS READ THE DNA", 200, 960, 70, bg=MARI); return c
    c, P = nmap(8, 61.5, 58); tag(c, "2017"); a = place(c, P, "HAITHABU", "A VIKING AGE PORT\n(NOW IN GERMANY)", 330, 60, 42, ring=k == 2)
    if k == 2: return c
    b = place(c, P, "LOFOTEN", "ARCTIC COD,\nOFF LOFOTEN", 290, -10, 42); codroute(c, P, T.ease(T.LP*1.25))
    L(c, "MORE THAN 1,000 MILES", 560, 460, 70, bg=MARI); return c
def further(k=0):
    c, P = nmap(8, 61.5, 58); codroute(c, P); place(c, P, "HAITHABU"); place(c, P, "LOFOTEN")
    x, y = place(c, P, "FARM"); r = 34+4*math.sin(T.TT*3); c.ell(x-r, y-r, x+r, y+r, None, NAVY, 7); c.label(x+350, y, "EVERYWHERE YOU'VE BEEN", 46); c.label(520, 520, "THE FISH", 60, bg=MARI); return c

# ================= quest two: stay warm without choking =================
def house(k):
    if k == 0:
        c = farm("cold", "snow", sun=(1500, 540), x=900, w=1300, byre=False); q = app("dim", .6); xm = 900
        c.line([(lerp(xm, 270, q), 1000), (lerp(xm, 1530, q), 1000)], 10, NAVY, False)
        if q > .9:
            for xx in (270, 1530): c.line([(xx, 970), (xx, 1030)], 10, NAVY, False)
        snowf(c, 40); hud(c, .1); L(c, "LONG, AND BUILT OF WOOD", 250, 960, 70); return c
    c = hall(fire=1.0, hole="dusk", smoke=.6, x0=260, x1=1660); sidbench(c, 960, "hold", "smile"); hud(c, .1); L(c, "A LONG FIRE DOWN THE MIDDLE", 330, 960, 70, bg=MARI); return c
def nochim(k):
    if k == 0:
        c = C(EV); c.longhouse(960, 800, 1100, 380, smoke=False, door=.2); c.rect(1260, 250, 1340, 440, BRICK, INK, 6); c.rect(1245, 236, 1355, 262, BRICK, INK, 6); c.rect(700, 690, 800, 770, SKY, INK, 6); c.line([(750, 690), (750, 770)], 4, INK, False)
        if T.LT > .3: c.redx(1300, 340, 80, 20)
        if T.LT > .9: c.redx(750, 730, 70, 20)
        L(c, "NO CHIMNEY. NO WINDOWS.", 150, 960, 80); return c
    c = hall(fire=1.0, hole="dusk", smoke=1.0 if k == 1 else 2.6, x0=560, x1=1360); hud(c, .1)
    if k == 1: a = 12*math.sin(T.TT*3); arrow(c, 960, 520+a, 960, 130+a, PAPER, 12, 40); L(c, "OUT THROUGH A HOLE IN THE ROOF", 600, 1380, 56); return c
    s = sidp(c, 420, 1040, 360, "wave", "pain"); haze(c, 1.6, 300, 900, 8); L(c, "EVENTUALLY.", 380, 1300, 110, bg=MARI); return c
def beds(k):
    if k == 0:
        c = hall(fire=.9, hole="day", smoke=.5); onbench(c, 500, 290, "hold", "n", "brown", bd=True); w = onbench(c, 840, 280, "hold", "smile", "green", w=True); kid(c, 1120, 724, 170, "wave", "joy", "rose"); onbench(c, 1420, 290, "chin", "n", "slate")
        hud(c, .1); L(c, "PLANK BEDS ALONG THE WALLS: SIT BY DAY", 300, 960, 58); return c
    c = hall(fire=.3, hole="night", smoke=.5)
    for i, (x, col) in enumerate(((560, "brown"), (1080, "green"), (1640, "slate"))): asleep(c, x, 280, col, col=((150, 120, 96), (128, 110, 120), (120, 130, 110))[i])
    for i in range(3): c.text(360+i*530+20*math.sin(T.TT*2+i), 440-30*((T.TT*.6+i*.3) % 1), "z", 80, PAPER)
    dimc(c, 80); hud(c, .1); L(c, "SLEEP BY NIGHT", 300, 960, 76, bg=MARI); return c
def stall(k):
    c = hall(fire=.9, hole="day", smoke=.8 if k == 0 else 1.5, x0=160, x1=640, posts=(820,))
    for x in (1120, 1460, 1800): c.rect(x-14, 560, x+14, 1010, (86, 60, 44), INK, 6)
    c.ox(1300, 1010, 1.1, flip=True, step=T.TT); c.ox(1640, 1010, 1.1, flip=True, c=(214, 196, 170), step=T.TT+2); hud(c, .1)
    if k == 0: L(c, "NO SEPARATE STABLE? THE ANIMALS GET ONE END", 300, 960, 54); return c
    s = sidp(c, 740, 1050, 340, "chin", "pain"); breath(c, 1110, 860, 1.6, flip=True); L(c, "SAME ROOF. SAME AIR.", 300, 960, 84, bg=MARI); return c
def air(k=0):
    c = C(WALLC)
    for xx in range(0, W, 150): c.line([(xx, 0), (xx, H)], 5, WALLD, False)
    c.da.ellipse([-400*S, 500*S, 900*S, 1500*S], fill=(255, 150, 50, 50)); s = sidp(c, 900, 1500, 900, "chin", "pain" if int(T.TT*2.4) % 2 == 0 else "worry"); haze(c, 2.2, 40, 900, 12); L(c, "ABOUT THAT AIR.", 200, 1400, 90); return c
def dk(k):
    if k == 0:
        c = land("grey", "snow", 640, seed=7, mts=False); c.longhouse(520, 840, 760, 300, snow=True); c.longhouse(1440, 820, 620, 260, snow=True, door=.7)
        c.person(880, 1050, 230, "walk" if step() else "stand", "n", "red", hat="cap"); c.person(1140, 1056, 230, "wave", "smile", "blue", hat="cloche", flip=True); snowf(c, 40)
        tag(c, "DENMARK, WINTER 2011–12"); L(c, "TWO REBUILT VIKING AGE HOUSES", 250, 960, 64); return c
    if k == 1:
        c = ev("DENMARK, WINTER 2011–12"); n = count(1, 13, 1.2, .1, "c13")
        for i in range(13):
            x = 280+(i % 7)*230; y = 420+(i//7)*250; c.rect(x-90, y-90, x+90, y+90, WHITE if i >= n else BARC, INK, 7, 14); c.text(x, y, str(i+1), 90, INK if i >= n else PAPER)
        c.text(1500, 900, "WEEKS", 150, NAVY); L(c, "THEY LIVED IN THEM", 190, 960, 76); return c
    c = hall(fire=1.0, hole="day", smoke=1.2); f = c.person(1500, 1040, 340, "hold", "n", "red", hat="cap", flip=True); c.line([(1100, 150), (1100, 860)], 6, INK, False); c.bowl(1100, 880, 1.1, (70, 66, 70))
    tag(c, "DENMARK, WINTER 2011–12"); L(c, "COOKING AND HEATING WITH A WOOD FIRE", 300, 960, 58, bg=MARI); return c
def meas(k):
    if k == 0:
        c = hall(fire=1.0, hole="day", smoke=1.4); f = sci(c, 380, 1040, 360, "hold", "det"); hx, hy = f["hand"]; c.rect(hx-10, hy-90, hx+170, hy+30, (226, 226, 232), INK, 6, 10)
        a = math.radians(-120+50*math.sin(T.TT*3)); c.line([(hx+80, hy+10), (hx+80+60*math.cos(a), hy+10+60*math.sin(a))], 6, RED, False); tag(c, "DENMARK, WINTER 2011–12"); L(c, "SCIENTISTS MEASURED WHAT THEY BREATHED", 300, 1000, 56); return c
    c = ev("DENMARK, WINTER 2011–12"); y0 = 860; lim = 600
    for i, (x, t) in enumerate(((560, "CARBON\nMONOXIDE"), (1360, "FINE SMOKE\nPARTICLES"))):
        c.line([(x-260, y0), (x+260, y0)], 8, INK, False); c.text(x, y0+84, t, 56)
        for xx in range(int(x-250), int(x+250), 60): c.line([(xx, lim), (xx+34, lim)], 7, RED, False)
        c.text(x-250, lim-40, "WHO LIMIT", 44, RED, "lm")
        if k-1 >= i: q = app(("bar", i), .7, .1); c.rect(x-110, y0-(y0-lim+70)*q, x+110, y0, (120, 116, 112), INK, 7)
    c.rect(560, 1016, 1360, 1072, EV, None); c.text(960, 1044, "A SKETCH: THE HEIGHTS ARE NOT MEASUREMENTS", 44, (120, 110, 98))
    if k == 2: L(c, "BOTH HIGHER THAN THE WHO'S LIMITS", 250, 960, 62, bg=MARI)
    return c
def worst(k):
    c = hall(fire=1.0, hole="day", smoke=1.6); c.line([(1000, 150), (1000, 860)], 6, INK, False); c.bowl(1000, 880, 1.1, (70, 66, 70)); w = woman(c, 1470, 1040, 340, "hold", "n", "rose", flip=True); kd = kid(c, 1700, 1040, 180, "stand", "worry", "green", flip=True); hud(c, .1)
    if k == 0: L(c, "THE RESEARCHERS THINK...", 290, 760, 60); return c
    if k == 1: L(c, "WOMEN AND SMALL CHILDREN PROBABLY\nGOT THE WORST OF IT", 290, 800, 54, bg=MARI); return c
    c.marker(w["head"][0], w["head"][1]-110, 44); c.marker(kd["head"][0], kd["head"][1]-90, 34); L(c, "REMEMBER THAT", 290, 800, 90, bg=MARI); return c
def light(k):
    if k == 0:
        c = hall(fire=1.0, hole="night", smoke=.6, dim=120); longfire(c, 620, 1300, 960, 1.0); onbench(c, 520, 290, "hold", "n", "brown"); onbench(c, 1420, 280, "hold", "n", "blue", w=True, flip=True)
        tag(c, "VIKING YORK"); L(c, "THE FIRE GAVE MOST OF THE LIGHT", 300, 960, 62); return c
    c = C((40, 30, 26)); table(c, 420, 1500, 1000, 200, (120, 86, 60))
    for x in (720, 1200): c.da.ellipse([(x-260)*S, 330*S, (x+260)*S, 850*S], fill=(255, 200, 100, 46))
    c.rushlamp(720, 766, 1.5, T.TT); c.candle(1200, 766, 1.6, T.TT); c.text(720, 890, "RUSH LAMPS", 60, PAPER); c.text(1130, 890, "THE ODD CANDLE", 60, PAPER); tag(c, "VIKING YORK"); return c
def cloakf(k):
    if k == 0:
        c = farm("grey", "snow", x=1300, w=760, byre=False); x = lerp(300, 760, T.GP); s = sidc(c, x, 1040, 380, "walk" if step() else "stand", "det"); breath(c, s["head"][0]+80, s["head"][1]+90)
        snowf(c, 110, 2, 6); hud(c, .37); L(c, "OUTDOORS: A THICK CLOAK", 250, 760, 66); return c
    c = C(EV); q = app("ly", .5, .3); x = 640; cape(c, x-70*q, 1000, 620, (56, 66, 100)); cape(c, x, 1000, 620); s = sidp(c, x, 1000, 620, "self", "smile")
    if q > .5: c.line([(420, 600), (330, 440)], 5, INK, False); c.label(300, 390, "LAYER TWO", 50)
    c.text(1400, 430, "OFTEN", 110, NAVY); c.text(1400, 600, "TWO", 200, RED); c.text(1400, 770, "LAYERS", 110, NAVY); return c
def sockf(k):
    if k == 0:
        c = ev("YORK, ENGLAND"); c.rect(0, 860, W, H, (150, 124, 96), None); c.line([(0, 860), (W, 860)], 6, INK, False); c.poly([(900, 860), (940, 1000), (1700, 1000), (1740, 860)], (112, 90, 70), INK, 6)
        f = c.person(480, 1010, 400, "point", "wow", "blue", hat="cap"); hx, hy = f["hand"]; c.sock(hx+30, hy+110, .6); L(c, "ARCHAEOLOGISTS FOUND A WOOL SOCK", 230, 1100, 60); return c
    c = ev("YORK, ENGLAND"); c.rect(560, 880, 1000, 920, (120, 116, 112), INK, 6, 8); c.sock(690, 880, 1.7)
    c.text(1400, 520, "1", 420, RED); c.text(1400, 800, "SOCK", 130, NAVY)
    if k == 2: L(c, "THE ONLY ONE OF ITS KIND FOUND IN ENGLAND", 240, 1000, 56, bg=MARI)
    return c
def nochange(k=0):
    c = C(EV); s = sidp(c, 760, 1010, 440, "hold", "worry"); hx, hy = s["hand"]; c.sock(hx+10, hy+120, .7, RED); c.text(1260, 560, "?", 300, NAVY); L(c, "SOME THINGS DON'T CHANGE", 170, 960, 76); return c
NEEDS = ["FIRE, FOR NUMB KNEES", "FOOD AND CLOTHING", "WATER", "A CHANCE TO DRY OFF", "A FRIENDLY WORD"]
def poem(k):
    if k == 0:
        c = farm("night", "night", lit=True, x=1100, w=900, byre=False); x = lerp(120, 480, T.GP); m = man(c, x, 1050, 360, "walk" if step() else "stand", "worry", "slate", cloak=(70, 60, 80)); breath(c, m["head"][0]+70, m["head"][1]+80)
        snowf(c, 130, 3, 6); tag(c, "AN OLD NORSE POEM: HÁVAMÁL"); L(c, "WHAT A TRAVELLER NEEDS", 250, 1300, 62); return c
    c = hall(fire=1.1, hole="night", smoke=.6, x0=80, x1=520, posts=(), fy=1000); m = man(c, 720, 1050, 350, "hold", "smile" if k == 3 else "n", "slate")
    if k >= 2: c.bowl(560, 900, .7); c.jug(640, 960, .6)
    if k == 3: woman(c, 1010, 1050, 330, "wave", "smile", "green", flip=True)
    n = {1: 1, 2: 3, 3: 5}[k]; first = {1: 0, 2: 1, 3: 3}[k]; c.rect(1200, 190, 1890, 230+n*96+30, PAPER, INK, 7, 20)
    for i in range(n):
        if app(("nd", i), .25, (i-first)*.5 if i >= first else 0) > .5: c.tick(1256, 270+i*96, 22); c.text(1306, 266+i*96, NEEDS[i], 54, INK, "lm")
    tag(c, "AN OLD NORSE POEM: HÁVAMÁL"); return c
def damp(k):
    c = C(WALLC)
    for xx in range(0, W, 150): c.line([(xx, 0), (xx, 820)], 5, WALLD, False)
    c.rect(0, 820, W, H, FLOORC, None); c.line([(0, 820), (W, 820)], 6, INK, False); c.rect(820, -10, 1100, 900, (120, 86, 60), INK, 8)
    for i in range(4): y = ((T.TT*520+i*260) % 780); c.poly([(1180+i*14, y), (1168+i*14, y+34), (1192+i*14, y+34)], WATER, INK, 3)
    c.ell(1040, 880, 1400, 940, WATER, INK, 5)
    if k:
        for (x, y, r) in ((880, 760, 50), (1000, 820, 64), (920, 860, 40), (1060, 720, 34)): c.ell(x-r, y-r*.7, x+r, y+r*.7, (60, 50, 40), None)
        c.line([(960, 560), (940, 660), (980, 740), (950, 840)], 7, INK, False)
    L(c, "THE HOUSE'S OWN ENEMY: DAMP" if k == 0 else "DAMP ROTS WOOD", 300, 1420 if k == 0 else 1440, 60 if k == 0 else 84, bg=PAPER if k == 0 else MARI); return c
def hamq(k=0):
    c = hall(fire=.9, hole="day", smoke=1.0, x0=140, x1=620, posts=(300,)); c.line([(700, 200), (W, 200)], 22, (60, 44, 34), False); hang(c, 1400, 200, "ham", 1.5, 8*math.sin(T.TT*1.3)); s = sidp(c, 1000, 1050, 380, "self", "bored")
    for (x, y) in ((1500, 420), (s["head"][0], s["head"][1]-40)):
        for i in range(3): q = ((i/3+T.TT*.35) % 1); r = 16+q*30; c.da.ellipse([(x+30*math.sin(T.TT+i)-r)*S, (y-q*150-r)*S, (x+30*math.sin(T.TT+i)+r)*S, (y-q*150+r)*S], fill=(240, 236, 228, int(210*(1-q))))
    hud(c, .1); L(c, "YOU SMELL LIKE A SMOKED HAM", 330, 560, 54, bg=MARI); return c

# ================= quest three: get through a hundred and eighty days =================
def sol(k=0):
    q = T.GP; c = farm("dusk" if q < .1 or q > .9 else "cold", "snow", sun=(lerp(430, 1500, q), 600-150*math.sin(math.pi*q)), x=960, w=820, byre=False); snowf(c, 30)
    hud(c, .37); L(c, "BY THE SOLSTICE" if k == 0 else "FOUR AND A HALF HOURS OF DAYLIGHT", 250, 960, 70 if k == 0 else 58, bg=PAPER if k == 0 else MARI); return c
def month(k):
    c = C(EV); c.rect(360, 240, 1560, 560, PAPER, INK, 8, 24); c.rect(360, 240, 1560, 340, NAVY, INK, 8, 24); c.text(960, 288, "THE ICELANDERS' NAME FOR THIS MONTH", 50, PAPER); c.text(960, 450, "MÖRSUGUR", 170, NAVY)
    if k:
        lv = lerp(1.0, .15, T.LP); c.vat(520, 1030, 1.1, PLANKD); c.ell(520-170, 1030-240*lv-28, 520+170, 1030-240*lv+28, (244, 214, 110), INK, 6)
        c.text(1240, 720, "IT CAN BE READ AS", 60); c.text(1240, 860, "FAT-SUCKER", 150, RED)
    return c
def what(k=0):
    c = hall(fire=.8, hole="dusk", smoke=.7); s = sidbench(c, 960, "chin", "bored", 310); onbench(c, 480, 280, "hold", "bored", "brown", bd=True); kid(c, 1420, 724, 170, "stand", "bored", "green")
    for i in range(3): c.text(1120+i*70, 360-10*math.sin(T.TT*2+i), ".", 160, PAPER)
    hud(c, .37); L(c, "SO WHAT DO YOU DO ALL WINTER?", 300, 620, 60); return c
def leg(c, x, y, k=1.0, flip=False, skate=True):
    """A lower leg (Sid's: a plain ink line) and a leather shoe standing on (x, y), in close-up, on a bone skate."""
    d = -1 if flip else 1; c.line([(x-d*16*k, y-640*k), (x-d*6*k, y-90*k)], 34*k, INK, False)
    c.poly([(x-d*70*k, y-110*k), (x+d*60*k, y-110*k), (x+d*170*k, y-50*k), (x+d*170*k, y), (x-d*70*k, y)], (150, 104, 70), INK, max(4, 8*k))
    if skate:
        c.boneskate(x+d*40*k, y+52*k, 1.25*k, flip, laces=False)
        for hx in (-60, 110): c.line([(x+d*(hx+40)*k, y+18*k), (x+d*(hx+10)*k, y-112*k)], max(4, 8*k), (120, 84, 58), False); c.line([(x+d*(hx+40)*k, y+18*k), (x+d*(hx+90)*k, y-108*k)], max(4, 8*k), (120, 84, 58), False)
def bones(k=0):
    c = C(ICEC); c.rect(0, 0, W, 330, SNOWG, None); c.line([(0, 330), (W, 330)], 6, INK, False)
    for i in range(10): x = (i*211+50) % W; y = 520+(i*97) % 480; c.line([(x, y), (x+120, y-12)], 5, ICED, False)
    dx = 30*math.sin(T.TT*1.2); c.rect(700+dx, -300, 1160+dx, 250, MARI, INK, 12, 150)
    leg(c, 790+dx, 800, 1.0); leg(c, 1090+dx, 850, 1.0); c.label(1500, 520, "YOU STRAP BONES\nTO YOUR FEET", 60); return c
def skate(k):
    c = C(EV)
    if k == 0:
        c.boneskate(960, 660, 2.6); c.text(960, 250, "AN ICE SKATE", 110, NAVY)
        if T.LT > .5: c.line([(700, 500), (560, 400)], 5, INK, False); c.label(470, 370, "LEATHER LACES", 50)
        if T.LT > 1.0: c.line([(1000, 680), (1100, 820)], 5, INK, False); c.label(1180, 860, "FLAT, POLISHED UNDERSIDE", 50)
        return c
    c.ox(520, 860, 1.9, c=(214, 196, 170)); c.horse(1380, 860, 1.5, flip=True)
    for (x, y) in ((606, 780), (1300, 760)):
        r = 70+8*math.sin(T.TT*4); c.ell(x-r, y-r, x+r, y+r, None, RED, 9)
    c.line([(100, 866), (1820, 866)], 6, INK, False); L(c, "THE LOWER LEG BONE OF A COW OR A HORSE", 190, 960, 58); return c
def skater(c, x, y, h=340, ex="smile", flip=False, cloak=(84, 96, 132), who=None, pole=True, coat="brown"):
    """Someone standing on bone skates, pushing along with a pole between the feet. The feet stay on the ice."""
    d = -1 if flip else 1; u = h*1.25/3.5
    for sgn in (-1, 1): c.boneskate(x+sgn*.2*u+d*.1*u, y+.16*u, u/250, flip, laces=False)
    if cloak: cape(c, x, y, h, cloak)
    f = sidp(c, x, y, h, "hold", ex, flip=flip) if who is None else c.person(x, y, h, "hold", ex, coat, flip=flip)
    if pole:
        hx, hy = f["hand"]; sw = .5*u*math.sin(T.TT*5); c.line([(hx+d*.3*u, hy-.9*u), (hx-d*(.9*u)+sw, y+.2*u)], max(6, u*.09), INK, False); c.line([(hx+d*.3*u, hy-.9*u), (hx-d*(.9*u)+sw, y+.2*u)], max(3, u*.05), PLANK, False)
    return f
def glide(k):
    c = ice("cold", (1560, 520)); x = lerp(260, 1500, T.GP); c.line([(120, 1010), (x-60, 1010)], 4, PAPER, False); c.line([(120, 1030), (x-60, 1030)], 4, PAPER, False); skater(c, x, 980, 360)
    hud(c, .4); L(c, "YOU DON'T LIFT YOUR FEET" if k == 0 else "YOU PUSH ALONG WITH A POLE", 250, 960, 66, bg=PAPER if k == 0 else MARI); return c
def pigf(k):
    if k == 0:
        c = ice("cold", (1560, 520)); c.pig(1400, 720, 1.5, flip=True); s = sidc(c, 640, 760, 360, "hold", "det"); hx, hy = s["hand"]; c.boneskate(hx+150, hy+30, .9, laces=False)
        r = 20+6*math.sin(T.TT*8); c.ell(hx+110+40*math.sin(T.TT*4)-r, hy+30-r, hx+110+40*math.sin(T.TT*4)+r, hy+30+r, (250, 236, 180), INK, 4); hud(c, .4); L(c, "RUB PIG FAT UNDERNEATH", 240, 1340, 66); return c
    c = ice("cold", (1560, 520)); x = lerp(200, 1500, T.ease(T.LP))
    for i in range(5): yy = 760+i*46; c.line([(x-420-i*30, yy), (x-170, yy)], 6, PAPER, False)
    skater(c, x, 980, 360, "joy"); hud(c, .4); L(c, "AND THEY RUN FASTER", 250, 800, 76, bg=MARI); return c
def forty(k=0):
    c = ev("COPPERGATE, YORK"); n = count(0, 42, 1.3, .1, "c42")
    for i in range(n): c.boneskate(250+(i % 7)*178, 300+(i//7)*124, .42, laces=False)
    c.text(1640, 440, "MORE\nTHAN", 80, NAVY); c.text(1640, 680, "40", 260, RED)
    if k: c.text(1640, 880, "AT ONE DIG", 70, NAVY)
    return c
def fun(k):
    c = ice("cold", (1560, 520))
    if k == 0:
        x = lerp(300, 1200, T.GP); c.sack(x-120, 800, 1.1); f = skater(c, x, 980, 360, "n"); c.line([(120, 1020), (x-60, 1020)], 4, PAPER, False); hud(c, .4); L(c, "FOR GETTING ABOUT", 250, 960, 76); return c
    x = lerp(300, 800, T.GP); skater(c, x, 960, 250, "joy", who="k", coat="green", cloak=None); skater(c, x+420, 1000, 250, "joy", who="k", coat="rose", cloak=None); c.person(1560, 1000, 240, "cheer", "joy2", "blue", rot=80)
    hud(c, .4); L(c, "AND FOR FUN", 250, 700, 84, bg=MARI); c.label(1280, 400, "THE NATIONAL MUSEUM OF DENMARK SAYS BOTH", 44); return c
def skis(k=0):
    from ep05 import along
    c = land("cold", "snow", 560, (1560, 470), seed=8); c.poly([(-10, 520), (500, 640), (1100, 860), (1700, 1000), (W+10, 1030), (W+10, H+10), (-10, H+10)], SNOWC, INK, 6)
    for px, k_ in ((1500, 1.2), (1760, .9)): c.pine(px, 930+k_*40, k_, True)
    pts = [(200, 560), (500, 640), (1100, 860), (1500, 950)]; x, y = along(pts, T.GP); x2, y2 = along(pts, min(1, T.GP+.03)); sl = (y2-y)/max(1, x2-x)
    for off in (0, 26): c.ski(x-200+off, y-200*sl+4+off*.4, x+150+off, y+150*sl+4+off*.4, 14)
    s = sidc(c, x, y+2, 300, "hold", "joy")
    for i in range(6): r = 10+i*5; xx = x-150-i*46; yy = y-60-i*40*sl*3-30*math.sin(T.TT*6+i); c.da.ellipse([(xx-r)*S, (yy-r)*S, (xx+r)*S, (yy+r)*S], fill=(255, 255, 255, 220))
    hud(c, .4); L(c, "WHERE THE SNOW COMES EARLY, YOU SKI", 200, 1200, 58); return c
def patch(k):
    c = C((150, 150, 158)); sky5(c, 300, "day", sun=False); c.peaks(300, h=200, seed=9); c.rect(0, 300, W, H, (150, 150, 158), None); c.line([(0, 300), (W, 300)], 6, INK, False)
    for i in range(16): x = (i*197+30) % W; y = 360+(i*113) % 660; c.ell(x-30, y-14, x+30, y+14, (128, 128, 138), INK, 4)
    c.poly([(300, 520), (760, 430), (1300, 440), (1700, 560), (1640, 880), (1100, 980), (520, 940), (260, 760)], ICEC, INK, 7); c.line([(520, 600), (1000, 540), (1400, 600)], 5, WHITE, False)
    c.ski(520, 800, 900, 700, 22, (120, 90, 62))
    if k >= 1 and app("t1", .3) > .03: c.pricetag(760, 590, 1.2*app("t1", .3), "2014", MARI)
    if k == 2:
        q = app("sk2", .4, .2)
        if q > .03: c.ski(1020, 860, 1020+380*q, 860-90*q, 22, (120, 90, 62)); c.pricetag(1330, 660, 1.2*q, "2021", MARI)
        L(c, "ITS PARTNER, SEVEN YEARS LATER", 190, 1180, 58)
    tag(c, "NORWAY: A MELTING ICE PATCH"); return c
def skilen(k):
    c = C(EV)
    if k == 0:
        c.ski(260, 620, 1560, 620, 34, (120, 90, 62)); q = app("d", .6); c.line([(lerp(960, 260, q), 760), (lerp(960, 1680, q), 760)], 9, NAVY, False)
        if q > .9:
            for xx in (260, 1680): c.line([(xx, 730), (xx, 790)], 9, NAVY, False)
        c.text(960, 870, "A LITTLE OVER 6 FEET", 100, NAVY); return c
    c.line([(200, 620), (1720, 620)], 12, INK, False)
    for x, t, s_ in ((420, "THE 700s", "THE SKIS ARE MADE"), (1500, "ABOUT 950", "YOU")): c.line([(x, 570), (x, 670)], 12, INK, False); c.text(x, 480, t, 110, NAVY); c.text(x, 760, s_, 66)
    q = T.ease(T.LP*1.3); arrow(c, 460, 900, lerp(460, 1460, q), 900, RED, 12, 40); c.text(960, 980, "A COUPLE OF CENTURIES", 64, RED); c.ski(280, 330, 560, 310, 16, (120, 90, 62)); return c
def powder(k=0):
    c = land("day", "snow", 640, None, seed=9); tag(c, "NORWAY: A MELTING ICE PATCH"); f = c.person(420, 1020, 400, "point", "smile", "red", hat="cap"); c.ski(900, 1000, 1700, 960, 26, (120, 90, 62)); c.ski(960, 1040, 1760, 1000, 26, (120, 90, 62))
    if k: say(c, f, 1150, 330, "THEY WOULD BE CALLED\nPOWDER BOARDS TODAY,\nI THINK.", 70); c.label(1320, 720, "ONE OF THE ARCHAEOLOGISTS", 46, bg=MARI)
    return c
def sundown(k=0):
    q = T.ease(T.LP); c = farm("dusk", "dusk", lit=True, sun=(430, lerp(500, 640, q)), x=1060, w=820, byre=False, mts=False); dimc(c, 130*q, (10, 14, 40)); hud(c, .4); L(c, "MID-AFTERNOON. THE SUN GOES DOWN.", 250, 1060, 62); return c
def play(k):
    if k == 0:
        c = hall(fire=1.0, hole="night", smoke=.6, x0=140, x1=620, dim=40, posts=(300,)); table(c, 900, 1320, 1000, 150); c.rect(960, 800, 1260, 818, (190, 150, 104), INK, 5)
        for i, x in enumerate((1010, 1080, 1150, 1210)): c.gpiece(x, 800, .34, (BONEC, (70, 62, 60))[i % 2])
        sidp(c, 760, 1040, 340, "point", "smile"); man(c, 1470, 1040, 350, "chin", "det", "slate", flip=True, bd=True); hud(c, .4); L(c, "SO YOU PLAY", 300, 1110, 90); return c
    c = C((60, 44, 36)); c.da.ellipse([200*S, 0, 1700*S, 1200*S], fill=(255, 190, 90, 40))
    if k == 1: c.taflboard(1100, 560, 2.4); L(c, "HNEFATAFL", 300, 360, 90, bg=MARI); return c
    c.taflboard(620, 590, 1.7)
    for i in range(2): b = abs(math.sin(T.TT*3+i*1.1)); c.die(1300+i*240, 800-260*b*(1-T.LP), 2.2, (5, 2)[i] if T.LP > .6 else 1+int(T.TT*9+i*3) % 6)
    L(c, "AND DICE", 190, 1420, 90, bg=MARI); return c
def pieces(k=0):
    c = C(EV); L(c, "THE PIECES SURVIVE", 170, 960, 80)
    for i, (t, col) in enumerate((("STONE", (150, 146, 140)), ("BONE", BONEC), ("GLASS", GLASSG), ("ANTLER", ANTLER), ("AMBER", AMBER))):
        if i > (2 if k == 0 else 4): continue
        q = app(("pc", i), .25, (i if k == 0 else i-3)*.4 if (k == 0 or i >= 3) else 0)
        if q > 0: x = 320+i*320; c.gpiece(x, 700, 2.2*q, col); c.text(x, 800, t, 70)
    c.line([(140, 708), (1780, 708)], 6, INK, False); return c
def warn(k=0):
    c = C(EV); book(c, 620, 600, 3.2); c.die(1300, 540, 1.8, 6); c.die(1520, 700, 1.8, 3)
    if k: c.redx(1410, 620, 190, 26)
    L(c, "ONE SAGA WARNS AGAINST GAMBLING WITH DICE", 190, 960, 58, bg=MARI); return c
def feasters(c, y=1040, horns=True, n=5, ex="smile", lift=0.0, tbl=False):
    out = []
    for i in range(n):
        x = 300+i*290; w_ = i in (1, 4); f = (woman if w_ else man)(c, x, y, 320, "wave" if horns else "stand", ex, ("brown", "green", "slate", "red", "blue")[i], flip=i >= 3, **({} if w_ else {"bd": i % 2 == 0}))
        if horns: c.horn(f["hand"][0], f["hand"][1]-76-lift*abs(math.sin(T.TT*4+i)), .8, flip=i < 3); c.ell(f["hand"][0]-16, f["hand"][1]-16, f["hand"][0]+16, f["hand"][1]+16, PAPER, INK, 5)
        out.append(f)
    if tbl:
        c.rect(120, y-110, 1640, y-76, WOOD, INK, 6, 4); c.rect(140, y-76, 1620, y+10, (120, 86, 60), INK, 6)
        for i in range(4): c.bowl(440+i*290, y-166, .6)
    return out
def feast(k):
    c = hall(fire=1.1, hole="night", smoke=.6, x0=80, x1=440, dim=30, posts=(), fy=1000)
    for i, (x, col, w_) in enumerate(((620, "brown", False), (860, "green", True), (1560, "slate", False), (1790, "blue", True))): onbench(c, x, 280, "hold", "smile", col, w=w_, flip=i > 1)
    sidbench(c, 1080, "hold", "smile", 290)
    if k == 0:
        f = man(c, 1330, 1050, 380, "up", "det", "red", bd=True); hud(c, .45); L(c, "WHEN THERE'S A FEAST, YOU LISTEN", 300, 960, 62); return c
    f = man(c, 1330, 1050, 380, "hold", "smile", "red", bd=True); c.lyre(f["hand"][0]+46, f["hand"][1]+100, .72); c.ell(f["hand"][0]-16, f["hand"][1]-16, f["hand"][0]+16, f["hand"][1]+16, PAPER, INK, 5)
    for i in range(4): q = ((i/4+T.TT*.3) % 1); note(c, 1500+q*240+20*math.sin(T.TT*3+i), 560-q*220, 1.0)
    hud(c, .45); c.label(700, 330, "POEMS. MUSIC. STORIES.", 70, bg=MARI); return c
def written(k):
    if k == 0: c = C(EV); scribe(c); tag(c, "ICELAND, CENTURIES LATER"); L(c, "THE STORIES THAT GOT WRITTEN DOWN", 300, 960, 62); return c
    c = C(NIGHT_); book(c, 960, 800, 3.6)
    for i in range(3):
        x = 700+i*260; yy = 470-40*math.sin(T.TT*1.5+i); c.da.ellipse([(x-90)*S, (yy-110)*S, (x+90)*S, (yy+150)*S], fill=(220, 230, 255, 150)); c.ell(x-36, yy-40, x-12, yy-10, NIGHT_, None); c.ell(x+12, yy-40, x+36, yy-10, NIGHT_, None)
    tag(c, "ICELAND, CENTURIES LATER"); L(c, "THEY KEEP PUTTING THEIR HAUNTINGS AT YULE", 240, 1000, 56, bg=MARI); return c
def glam(k):
    if k == 0:
        c = land("night", "night", 620, seed=5, moon=1640); c.person(1200, 950, 330, "stand", "sleep", "banker", rot=-84); c.puff([(760+i*90, 950+(i % 2)*14, 60+(i % 3)*10) for i in range(7)], SNOWC, INK, 5)
        m = man(c, 420, 1040, 340, "hold", "wow", "brown", bd=True); hx, hy = m["hand"]; c.line([(hx, hy+40), (hx, hy-90)], 10, TIMBER, False); life._fire(c, hx, hy-90, .5+.06*math.sin(T.TT*12)); c.da.ellipse([(hx-200)*S, (hy-290)*S, (hx+200)*S, (hy+110)*S], fill=(255, 190, 90, 50))
        snowf(c, 70); tag(c, "GRETTIS SAGA"); L(c, "GLAM: FOUND DEAD IN THE SNOW AT YULE", 260, 800, 58); return c
    if k == 1:
        c = farm("night", "night", lit=True, x=1260, w=900, byre=False, moon=300); f = c.person(420, 1050, 420, "stand", "n", "banker"); dimc(c, 60, (10, 14, 40)); hx, hy = f["head"]; u = f["u"]
        for dx in (-.12, .34): c.ell(hx+(dx-.1)*u, hy+.38*u, hx+(dx+.1)*u, hy+.58*u, (190, 240, 255), None)
        snowf(c, 70); tag(c, "GRETTIS SAGA"); L(c, "AND HE COMES BACK", 250, 1160, 84, bg=MARI); return c
    q = T.LP; c = farm("cold", "snow", sun=(lerp(500, 1400, q), 560-230*math.sin(math.pi*q)), x=1260, w=900, byre=False); x = 420
    if q < .8:
        for i in range(10): a = i*36; c.line([(x+90*math.cos(math.radians(a)), 800+190*math.sin(math.radians(a))), (x+90*math.cos(math.radians(a+18)), 800+190*math.sin(math.radians(a+18)))], 6, (150, 160, 190), False)
    tag(c, "GRETTIS SAGA"); L(c, "THE HAUNTINGS EASE AS THE DAYS GROW LONGER", 250, 1000, 54); return c
def threew(k):
    c = C(NIGHT_); c.rect(0, 760, W, H, (146, 160, 194), None); c.line([(0, 760), (W, 760)], 6, INK, False)
    for i in range(3):
        if k == 0 and T.LP*3.4 < i: continue
        x = 360+i*600; c.pine(x-190, 880, 1.0, True); c.longhouse(x+60, 900, 360, 190, snow=True, smoke=False); c.label(x+40, 520, f"YEAR {i+1}", 80)
    if k:
        d = T.ease(T.LP); c.poly([(-10, H+10), (-10, lerp(1000, 800, d)), (400, lerp(980, 760, d)), (900, lerp(1000, 790, d)), (1500, lerp(980, 750, d)), (W+10, lerp(1000, 800, d)), (W+10, H+10)], SNOWC, INK, 6); dimc(c, 110*d, (6, 8, 24))
    snowf(c, 150, 4, 6); L(c, "IN THE MYTHS: A WINTER THAT LASTS THREE YEARS" if k == 0 else "THEN THE END OF THE WORLD", 200, 960, 56 if k == 0 else 84, bg=PAPER if k == 0 else MARI); return c
def darkf(k=0):
    c = hall(fire=0, hole="night", smoke=.5, x0=700, x1=1220); s = sidbench(c, 960, "self", "wow", 330); dimc(c, 118, (8, 8, 20)); hx, hy = s["head"]; u = s["u"]
    for dx in (-.12, .34): c.ell(hx+(dx-.11)*u, hy+.34*u, hx+(dx+.11)*u, hy+.6*u, PAPER, None); c.ell(hx+(dx-.05)*u, hy+.42*u, hx+(dx+.05)*u, hy+.54*u, INK, None)
    for i in range(5): xx = 760+i*100; c.ell(xx-9, 954, xx+9, 970, (226, 110, 50) if (i+int(T.TT*2)) % 3 else (150, 70, 40), None)
    snowf(c, 14, 5, 4); hud(c, .45); return c
def mid(k):
    c = C(EV); c.rect(260, 480, 1660, 620, WHITE, INK, 9, 16); q = app("half", .9, .1); c.rect(260, 480, 260+max(18, 700*q), 620, BARC, INK, 9, 16); c.line([(960, 430), (960, 670)], 10, INK, False)
    c.text(960, 370, "MIDWINTER", 100, NAVY); c.text(610, 760, f"{count(0, 90, .9, .1, 'c90')} DAYS DOWN", 90, NAVY)
    if k: c.text(1310, 760, "90 TO GO", 90, RED)
    L(c, "THE HALFWAY MARK, BY THE ICELANDIC CALENDAR", 190, 960, 54, bg=MARI); flake(c, 180, 550, 44, w=8); return c
def yule(k=0):
    c = farm("night", "night", lit=True, x=1100, w=1000, byre=False, moon=260); c.da.ellipse([620*S, 520*S, 1560*S, 1120*S], fill=(255, 190, 90, 60))
    for i, x0 in enumerate((200, 430)):
        x = x0+T.GP*150; m = man(c, x, 1040+i*10, 260, "up", "smile", ("brown", "blue")[i], cloak=(70, 60, 80)); hx, hy = m["hand"]; c.line([(hx, hy+50), (hx, hy-50)], 9, TIMBER, False); life._fire(c, hx, hy-50, .4+.05*math.sin(T.TT*12+i))
    snowf(c, 80); hud(c, .5); L(c, "YULE", 260, 1500, 170, bg=MARI); return c
def know(k):
    if k == 0:
        c = C(EV); c.rect(560, 300, 1360, 980, PAPER, INK, 8, 10); c.text(960, 380, "THE OLD YULE: WHAT WE KNOW", 50)
        for i in range(2): c.line([(640, 500+i*70), (1280-(i*260), 500+i*70)], 8, (150, 130, 96), False)
        if T.LT > .5: c.text(960, 800, "NOT MUCH", 130*(.8+.2*app("nm", .3, .5)), RED)
        return c
    if k == 1: c = C(EV); scribe(c, "blue", False); tag(c, "ICELAND"); L(c, "THE FULLEST ACCOUNT: SNORRI STURLUSON,\nMORE THAN 200 YEARS LATER", 280, 960, 56); return c
    c = C(EV); a = c.person(520, 1010, 400, "point", "angry", "green"); b = c.person(1400, 1010, 400, "point", "angry", "red", flip=True); c.glasses(a); say(c, a, 700, 330, "THE SOLSTICE.", 70); say(c, b, 1220, 330, "MID-JANUARY.", 70, flip=True)
    L(c, "SCHOLARS STILL ARGUE ABOUT THE DATE", 130, 960, 60, bg=MARI); return c
def nights3(k=0):
    c = farm("night", "night", lit=True, x=960, w=900, byre=False, smoke=False); n = min(3, int(T.LP*3.6)+1)
    for i in range(n): x = 520+i*440; c.da.ellipse([(x-120)*S, 190*S, (x+120)*S, 430*S], fill=(255, 250, 220, 40)); c.ell(x-60, 250, x+60, 370, (244, 240, 220), INK, 6); c.ell(x-28, 240, x+70, 344, (14, 20, 46), None)
    tag(c, "SNORRI'S ACCOUNT"); L(c, "FROM MIDWINTER NIGHT, FOR THREE NIGHTS", 930, 960, 58); return c
def king(c, x, y, h=400, pose="point", ex="det", flip=False, cross=False):
    f = man(c, x, y, h, pose, ex, "red", flip=flip, bd=(96, 70, 44)); c.crown(f)
    if cross: u = f["u"]; hx, hy = f["head"]; c.line([(hx, hy+1.5*u), (hx, hy+2.0*u)], max(4, u*.09), PAPER, False); c.line([(hx-.16*u, hy+1.66*u), (hx+.16*u, hy+1.66*u)], max(4, u*.09), PAPER, False)
    return f
def hakon(k):
    if k == 0:
        c = hall(fire=1.0, hole="day", smoke=.5, x0=140, x1=560, posts=(300,)); king(c, 900, 1040, 440, "point", "det", cross=True); tag(c, "SNORRI'S ACCOUNT"); L(c, "KING HÁKON THE GOOD", 300, 1300, 80); c.label(1400, 440, "A KING OF ABOUT YOUR TIME", 50, bg=MARI); return c
    c = C(EV); tag(c, "SNORRI'S ACCOUNT"); q = T.ease(T.LP*1.2)
    for x, t, col in ((480, "MIDWINTER NIGHT", NAVY), (1440, "CHRISTMAS", DGREEN)): c.rect(x-330, 520, x+330, 860, PAPER, INK, 8, 24); c.text(x, 790, t, 70, col)
    x = lerp(480, 1440, q); c.rect(x-170, 560, x+170, 720, MARI, INK, 8, 20); c.text(x, 636, "YULE", 110)
    arrow(c, 830, 440, 1090, 440, RED, 14, 44); L(c, "HE ORDERS YULE MOVED", 250, 960, 70); return c
def ale(k):
    if k == 0:
        c = hall(fire=1.0, hole="night", smoke=.5, x0=1660, x1=1880, posts=()); feasters(c); tag(c, "SNORRI'S ACCOUNT"); L(c, "EVERYONE HAD TO HAVE ALE FOR IT", 300, 900, 64); return c
    c = C(EV); tag(c, "SNORRI'S ACCOUNT")
    if k == 1:
        c.sack(420, 800, 2.0, t="GRAIN"); q = T.ease(T.LP*1.3); arrow(c, 620, 640, lerp(620, 860, q), 640, RED, 14, 44); c.barrel(1060, 820, 2.0); c.text(1060, 900, "ALE", 80, NAVY)
        c.text(1560, 430, "OR PAY\nA FINE", 110, RED); c.moneybag(1560, 900, 1.2); L(c, "BREWED FROM A MEASURE OF GRAIN", 200, 960, 62, bg=MARI); return c
    lv = lerp(1.0, .1, T.LP); c.barrel(620, 900, 2.6, lid=False); c.rect(620-104, 900-360*lv-24, 620+104, 900-24, (214, 160, 70), None); c.text(1300, 500, "KEEP THE FEAST", 100, NAVY); c.text(1300, 680, "FOR AS LONG AS\nTHE ALE LASTS", 80); return c
def litres(k):
    c = C(EV)
    if k == 0: c.sack(700, 860, 2.6, t="GRAIN"); c.text(1320, 480, "THE TRANSLATIONS:", 70, NAVY); c.text(1320, 640, "A MEASURE\nOF GRAIN", 110, RED); return c
    if k == 1:
        c.poly([(500, 900), (460, 420), (1060, 420), (1020, 900)], PLANK, INK, 8); c.rect(490, 470, 1030, 890, (226, 196, 120), None)
        for i in range(1, 8): c.line([(500+i*65, 430), (504+i*64, 890)], 4, PLANKD, False)
        c.line([(440, 560), (1080, 560)], 12, (84, 78, 74), False); c.line([(450, 800), (1070, 800)], 12, (84, 78, 74), False)
        c.text(1480, 480, "ABOUT\n16 LITRES", 110, NAVY); c.text(1480, 760, "ROUGHLY\n4 GALLONS", 70); L(c, "A MEASURE, BY ONE ESTIMATE", 190, 960, 60, bg=MARI); return c
    c.barrel(640, 880, 2.6); c.text(1320, 480, "SOME RETELLINGS:", 70, NAVY); c.text(1320, 640, "16 LITRES\nOF ALE", 110); return c
def popular(k=0):
    c = hall(fire=0, hole="night", smoke=.4, fy=0, posts=()); c.da.ellipse([200*S, 200*S, 1700*S, 1500*S], fill=(255, 190, 90, 50))
    for i, (x, w_, col) in enumerate(((440, False, "brown"), (960, True, "green"), (1480, False, "red"))):
        f = (woman if w_ else man)(c, x, 1170, 620, "wave", "joy", col, flip=i == 2, **({} if w_ else {"bd": True})); hx, hy = f["hand"]; c.horn(hx, hy-150-40*abs(math.sin(T.TT*4+i)), 1.6, flip=i < 2); c.ell(hx-30, hy-30, hx+30, hy+30, PAPER, INK, 8)
    L(c, "AS LAWS GO, A POPULAR ONE", 160, 960, 70, bg=MARI); return c
def liver(k):
    c = hall(fire=1.0, hole="night", smoke=.5, x0=60, x1=300, posts=()); table(c, 660, 1500, 1010, 190); tag(c, "SAME SAGA")
    kg = king(c, 1080, 1040, 400, "stand" if k < 2 else "shrug", "worry" if k < 2 else "pain", cross=True)
    for i, x in enumerate((480, 1700)): man(c, x, 1040, 360, "point" if k else "stand", "angry", ("brown", "slate")[i], flip=i == 1, bd=True)
    if k == 0: L(c, "THE CHRISTIAN PART WAS LESS POPULAR", 300, 1040, 60); return c
    c.ell(960, 760, 1200, 800, (190, 186, 180), INK, 6); c.ell(1010, 730, 1150, 786, (120, 40, 44), INK, 5)
    L(c, "AT A YULE FEAST, THE FARMERS..." if k == 1 else "...MAKE THE KING EAT HORSE LIVER", 300, 1040, 60, bg=PAPER if k == 1 else MARI); return c
def raiders(k):
    c = hall(fire=1.0, hole="night", smoke=.5, x0=1700, x1=1880, posts=())
    for i in range(5): c.roundshield(300+i*290, 330, 84, (RED, MARI, TEAL, RED, MARI)[i]); c.line([(300+i*290+120, 240), (300+i*290+120, 440)], 10, (150, 150, 156), False)
    fs = feasters(c, tbl=True); hud(c, .5)
    if k == 0: L(c, "NOW LOOK WHO'S AT THE TABLE", 150, 1100, 60); return c
    for f in (fs[0], fs[2], fs[3]): c.marker(f["head"][0], f["head"][1]-60, 30)
    L(c, "THE RAIDERS. HOME FOR THE WINTER.", 150, 1100, 60, bg=MARI); return c
def wheel(c, cx, cy, r, a, labels=True):
    cols = ((176, 210, 140), (236, 206, 110), (214, 160, 96), (166, 200, 228))
    for i in range(4): c.d.pieslice([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], 180+i*90, 270+i*90, fill=cols[i])
    c.ell(cx-r, cy-r, cx+r, cy+r, None, INK, 9); c.line([(cx-r, cy), (cx+r, cy)], 7, INK, False); c.line([(cx, cy-r), (cx, cy+r)], 7, INK, False)
    c.line([(cx, cy), (cx+r*.42*math.cos(a), cy+r*.42*math.sin(a))], 14, RED, False); c.ell(cx-20, cy-20, cx+20, cy+20, RED, INK, 5)
    if labels:
        for i, t in enumerate(("SPRING", "SUMMER", "AUTUMN", "WINTER")): an = math.radians(225+i*90); c.text(cx+r*.66*math.cos(an), cy+r*.66*math.sin(an), t, r*.16, INK)
def seasonal(k=0):
    c = C(EV); wheel(c, 620, 600, 360, math.radians(210)+T.GP*5.0); c.longship(1400, 560, 520, bob=T.TT*2, wind=T.TT); c.swell(570, T.TT, OCEAN, 8, 260, y1=640, x0=1080, x1=1720)
    L(c, "RAIDING CAN BE SEASONAL WORK", 130, 960, 66, bg=MARI)
    if k: book(c, 1400, 840, 1.6); c.text(1400, 990, "ONE SAGA SPELLS IT OUT", 56, NAVY)
    return c
SV = "ORKNEYINGA SAGA: SVEIN, TWO CENTURIES AFTER YOU"
def svein(k):
    if k == 0:
        c, P = nmap(-2, 59, 90); place(c, P, "ORKNEY", "ORKNEY", 190, -10, 60, ring=True, bg=MARI); tag(c, SV); return c
    if k == 1:
        c = land("day", "spring", 620, (1700, 280), seed=3); c.rect(0, 800, W, H, SOIL, None); c.line([(0, 800), (W, 800)], 6, INK, False)
        for i in range(8): c.line([(0, 850+i*34), (W, 850+i*34)], 4, (128, 94, 68), False)
        x = lerp(420, 900, T.GP); m = man(c, x, 1030, 380, "up", "n", "red", bd=True); hx, hy = m["hand"]
        for i in range(8): q = ((i/8+T.TT*.8) % 1); c.ell(hx+q*260-6, hy+q*q*420-6, hx+q*260+6, hy+q*q*420+6, WHEATC, INK, 2)
        tag(c, SV); L(c, "SPRING: HE SOWS HIS FIELDS", 260, 760, 64); return c
    c = C((78, 138, 172)); sky5(c, 520, "day", sx=320); c.swell(520, T.TT*.5, (54, 104, 142), 5, 420); x = lerp(700, 1200, T.GP); c.longship(x, 820, 700, bob=T.TT*1.5, wind=T.TT); crew(c, x, 820, 700); c.swell(832, T.TT, (78, 138, 172), 11, 300, ph=3); c.crests(870, 1040, T.TT, 14)
    tag(c, SV); L(c, "THEN PLUNDERING: HIS “SPRING-TRIP”", 220, 1000, 62, bg=MARI); return c
def svein2(k):
    if k == 0:
        c = land("gold", "autumn", 620, (1500, 380), seed=3); c.wheat(40, W-40, 900, 190, T.TT, 30, seed=1); c.wheat(20, W-20, 1040, 220, T.TT, 34, seed=2); m = man(c, 620, 1040, 400, "hold", "smile", "red", bd=True); c.scythe(m["hand"][0]+60, m["hand"][1], 1.3, 20+14*math.sin(T.TT*3))
        tag(c, SV); L(c, "HOME AFTER MIDSUMMER, FOR THE HARVEST", 250, 1080, 58); return c
    if k == 1:
        c = C((70, 92, 108)); sky5(c, 520, "grey", sun=False); c.swell(520, T.TT*.5, (70, 92, 108), 6, 420); x = lerp(1300, 800, T.GP); c.longship(x, 820, 700, flip=True, bob=T.TT*1.8, wind=T.TT); crew(c, x, 820, 700, True); c.swell(832, T.TT, (98, 122, 136), 12, 300, ph=3); c.crests(870, 1040, T.TT, 14, (200, 214, 220))
        tag(c, SV); L(c, "RAIDS AGAIN, UNTIL A MONTH INTO WINTER", 220, 1000, 58); return c
    c = hall(fire=0, hole="night", smoke=.3, fy=0, posts=(), dim=70); n = count(0, 80, 1.2, .1, "c80"); crowd(c, 200, 540, 80, 20, 80, 140, 84, shown=n)
    tag(c, SV); L(c, f"WINTER AT HOME: SOME {n} MEN,\nEATING AND DRINKING AT HIS EXPENSE", 290, 960, 56, bg=MARI); return c
def stay851(k):
    if k == 0:
        c = land("grey", "snow", 600, seed=6, mts=False); c.poly([(-10, 600), (W+10, 600), (W+10, 700), (-10, 716)], (112, 146, 166), INK, 6)
        for i, x in enumerate((420, 1000, 1560)): c.longship(x, 860+(i % 2)*40, 480, sail=0, flip=i % 2 == 1)
        for x in (700, 1290): c.poly([(x-110, 1050), (x, 890), (x+110, 1050)], (200, 186, 154), INK, 6); c.poly([(x-24, 1050), (x, 960), (x+24, 1050)], (90, 70, 56), INK, 5); life._fire(c, x+190, 1050, .6+.06*math.sin(T.TT*11+x))
        man(c, 1010, 1056, 230, "hold", "n", "slate", bd=True); man(c, 1620, 1056, 230, "hold", "n", "brown", flip=True)
        snowf(c, 70); tag(c, "THE ANGLO-SAXON CHRONICLE, 851"); L(c, "NOT EVERYONE COMES HOME", 250, 960, 76); return c
    c = C(EV); a = c.roll(300, 250, 1620, 900, 40); c.text(960, 370, "851", 130, RED)
    if k >= 2: c.text(960, 610, "“THE HEATHENS NOW FOR THE FIRST TIME\nREMAINED OVER WINTER\nIN THE ISLE OF THANET.”", 60, INKQ)
    c.text(960, 820, "THE ANGLO-SAXON CHRONICLE", 50, NAVY)
    if k == 3: L(c, "A CENTURY BEFORE YOU. WORTH WRITING DOWN.", 130, 960, 56, bg=MARI)
    return c
INKQ = (90, 44, 34)
def thaw(k=0):
    c = ice("day", (1700, 330)); c.poly([(700, 860), (900, 830), (1250, 850), (1340, 930), (1100, 1000), (760, 960)], (120, 170, 200), INK, 5)
    for pts in ([(300, 900), (520, 860), (700, 880)], [(1340, 930), (1560, 900), (1700, 960)], [(900, 1000), (960, 1050), (1100, 1060)]): c.line(pts, 6, (90, 130, 160), False)
    s = sidp(c, 420, 760, 330, "wave", "joy"); hud(c, 1.0, "DAY 180"); L(c, "THE ICE GOES SOFT. YOU MADE IT.", 220, 1020, 66, bg=MARI); return c

# ================= the hidden quest: the loom =================
def weaver(c, x, y, k=1.0, prog=.4, coat="rose", flip=False, ex="n"):
    """A woman working at the loom: the loom, then the weaver beside it with a hand on the cloth."""
    e = c.loom(x, y, k, prog, T.TT); w = woman(c, x+(-1 if flip else 1)*330*k, y+30*k, 420*k, "point", ex, coat, flip=not flip); return e, w
def spinner(c, x, y, h=330, coat="green", flip=False, ex="n"):
    """A woman spinning: wool held up in one hand, the spindle turning on its thread below it."""
    w = woman(c, x, y, h, "up", ex, coat, flip=flip); hx, hy = w["hand"]; u = w["u"]; c.puff([(hx-10, hy-30, .26*u), (hx+16, hy-50, .22*u), (hx+26, hy-14, .2*u)], WOOLC, INK, max(3, u*.05))
    dy = (.9+.5*((T.TT*.35) % 1))*u; c.spindle(hx+16, hy+dy, u/120, T.TT, (hx+16, hy-10)); return w
def walkpast(k=0):
    c = hall(fire=.9, hole="day", smoke=.6, x0=200, x1=760); c.loom(1500, 800, .7, .45, T.TT); woman(c, 1250, 800, 290, "point", "n", "rose"); x = lerp(200, 900, T.GP); sidp(c, x, 1060, 330, "walk" if step() else "stand", "bored")
    hud(c, 1.0, "DAY 180"); L(c, "YOU'VE WALKED PAST IT ALL WINTER", 300, 700, 58); return c
def loomr(k=0):
    c = C(WALLC)
    for xx in range(0, W, 150): c.line([(xx, 0), (xx, 900)], 5, WALLD, False)
    c.rect(0, 900, W, H, FLOORC, None); c.line([(0, 900), (W, 900)], 6, INK, False); c.da.ellipse([300*S, -100*S, 1500*S, 1100*S], fill=(255, 220, 140, int(46+14*math.sin(T.TT*3))))
    weaver(c, 1000, 960, 1.35, lerp(.3, .6, T.GP), "rose"); L(c, "THE LOOM", 220, 380, 130, bg=MARI); return c
def clothy(k):
    if k == 0:
        c = C(EV); wheel(c, 600, 600, 370, T.TT*.9); c.loom(1400, 900, .95, lerp(.2, .8, T.LP), T.TT); L(c, "CLOTH DOESN'T WAIT FOR A SEASON", 130, 960, 64, bg=MARI); return c
    c = hall(fire=.9, hole="day", smoke=.5, x0=120, x1=520); spinner(c, 760, 1040, 340, "green"); c.loom(1380, 1000, .9, lerp(.3, .6, T.GP), T.TT); woman(c, 1700, 1030, 360, "point", "n", "rose", flip=True); kid(c, 1010, 1040, 170, "up", "smile", "blue")
    L(c, "ALL YEAR ROUND. MOSTLY THE WOMEN.", 300, 960, 62); return c
def seashore(sk="day", ground="spring", hz=560, seed=6):
    """The shore below the farm: the fjord, the far mountains, the beach in front."""
    c = C((84, 136, 170)); sky5(c, hz, sk, sun=False); c.peaks(hz, h=300, seed=seed, col=(126, 150, 160)); c.swell(hz, T.TT*.5, (84, 136, 170), 5, 420); c.crests(hz+30, 760, T.TT*.5, 9, (220, 234, 238), 2)
    G = GROUND[ground]; c.poly([(-10, H+10), (-10, 830), (500, 800), (1200, 812), (W+10, 790), (W+10, H+10)], G if ground != "spring" else (206, 196, 150), INK, 6); return c
def forship(k):
    if k == 0:
        c = C(EV); x = 620; c.poly([(x-110, 360), (x+110, 360), (x+330, 500), (x+270, 600), (x+150, 540), (x+190, 900), (x-190, 900), (x-150, 540), (x-270, 600), (x-330, 500)], (176, 96, 96), INK, 8); c.d.pieslice([(x-60)*S, 310*S, (x+60)*S, 410*S], 0, 180, fill=EV, outline=INK, width=8*S)
        c.sock(1180, 880, 1.2); c.clothbolt(1560, 880, 1.2); L(c, "NOT ONLY FOR CLOTHES", 170, 960, 76); return c
    c = seashore(); q = T.ease(T.LP*1.2); c.longship(1060, 770, 1000, bob=T.TT*1.2, wind=T.TT, sail=max(.04, q)); c.swell(782, T.TT, (98, 150, 182), 9, 300, ph=2, y1=836); L(c, "FOR THE SHIP", 930, 360, 100, bg=MARI); return c
def sailbig(k):
    if k == 0:
        c = C((140, 196, 226)); sky5(c, H, "day", sun=False); x, yt, hw, yb = 960, 150, 700, 900; bl = 30*math.sin(T.TT*1.3); c.line([(x-hw-60, yt), (x+hw+60, yt)], 36, INK, False); c.line([(x-hw-60, yt), (x+hw+60, yt)], 22, PLANK, False)
        c.poly([(x-hw, yt), (x+hw, yt), (x+hw+bl*.5, (yt+yb)/2), (x+hw, yb), (x+bl, yb+30), (x-hw, yb), (x-hw+bl*.5, (yt+yb)/2)], WOOLC, INK, 10)
        for i in range(1, 8): xx = x-hw+2*hw*i/8; c.line([(xx, yt+12), (xx+bl*.6, yb-8)], 5, (196, 180, 146), False)
        c.rect(1500, 760, 1700, 1090, (110, 80, 56), INK, 8); sidp(c, 400, 1060, 190, "up", "wow"); c.label(960, 520, "ONE SAIL: PROBABLY MORE THAN\n1,000 SQUARE FEET OF CLOTH", 62); return c
    c = land("day", "spring", 600, (1640, 260), seed=6)
    for i, (x, y, k_) in enumerate(((420, 960, 2.2), (980, 1020, 2.6), (1520, 950, 2.0))): c.sheep(x, y, k_, flip=i == 2, step=T.TT+i)
    L(c, "AND MOST ARE WOOL", 250, 960, 84, bg=MARI); return c
def spin(k):
    if k == 0:
        c = C(WALLC)
        for xx in range(0, W, 150): c.line([(xx, 0), (xx, H)], 5, WALLD, False)
        c.da.ellipse([-300*S, 300*S, 1100*S, 1500*S], fill=(255, 170, 60, 44)); w = woman(c, 620, 1500, 900, "up", "n", "green"); hx, hy = w["hand"]; c.puff([(hx-20, hy-70, 90), (hx+50, hy-110, 76), (hx+70, hy-20, 70)], WOOLC, INK, 7)
        c.spindle(hx+40, hy+420+60*math.sin(T.TT*.9), 2.6, T.TT, (hx+40, hy-10)); L(c, "SPUN ON HAND SPINDLES", 220, 1380, 66); return c
    c = C(EV); q = T.ease(T.LP*1.2)
    for i in range(6):
        x0 = 540+i*140; off = (i-2.5)*110*(1-q); c.rect(x0+off, 280, x0+140+off, 900, WOOLC, INK, 6)
        for j in range(15): c.line([(x0+off+10, 300+j*40), (x0+off+130, 300+j*40)], 2, (200, 186, 154), False)
    L(c, "THE CLOTH IS WOVEN IN STRIPS", 170, 960, 70, bg=MARI); return c
def flock(c, n, x0=120, y0=330, per=35, gx=48, gy=46, k=1.0):
    for i in range(n):
        x = x0+(i % per)*gx*k; y = y0+(i//per)*gy*k; c.ell(x-17*k, y-12*k, x+17*k, y+12*k, WOOLC, INK, max(2, 3*k)); c.ell(x+13*k, y-9*k, x+25*k, y+5*k, (70, 64, 60), None)
def woolq(k):
    c = C(EV)
    if k == 0: c.text(960, 430, "HOW MUCH WOOL?", 190, NAVY); c.sheep(960, 900, 2.4, step=T.TT); return c
    if k == 1: n = count(0, 150, 1.0, .1, "c150"); flock(c, n, 110, 440, 25, 60, 70, 1.2); c.text(960, 250, "ONE ESTIMATE: THE WOOL OF 150 TO 200 SHEEP", 70, NAVY); c.text(960, 990, f"{n} DRAWN HERE", 50); return c
    n = count(150, 700, 1.2, .1, "c700"); flock(c, n, 140, 380, 35, 48, 31, 1.0); c.text(960, 250, "ANOTHER: A YEAR'S WOOL FROM ABOUT 700", 76, RED); return c
def workq(k):
    if k == 0: c = C(EV); c.text(960, 430, "HOW MUCH WORK?", 190, NAVY); c.loom(960, 1050, .75, .5, T.TT); return c
    c = hall(fire=.8, hole="day", smoke=.4, x0=60, x1=260, posts=())
    for i in range(4):
        x = 420+i*380
        if i % 2 == 0: c.loom(x, 1010, .62, lerp(.3, .7, T.GP), T.TT); woman(c, x+170, 1040, 300, "point", "n", ("rose", "blue")[i//2], flip=True)
        else: spinner(c, x+60, 1040, 300, ("green", "brown")[i//2])
    t = "FOUR WOMEN" if k == 1 else "FOUR WOMEN × 10 HOURS A DAY × A FULL YEAR"; L(c, t, 250, 960, 84 if k == 1 else 58, bg=MARI)
    if k == 2: c.label(960, 400, "ONE TEXTILE RESEARCHER'S ESTIMATE", 46)
    return c
def onesail(k=0):
    c = C(EV); x, yt = 960, 240; hw = 520; yb = 860; bl = 26*math.sin(T.TT*1.3); c.line([(x-hw-40, yt), (x+hw+40, yt)], 30, INK, False); c.line([(x-hw-40, yt), (x+hw+40, yt)], 18, PLANK, False)
    c.poly([(x-hw, yt), (x+hw, yt), (x+hw+bl*.5, (yt+yb)/2), (x+hw, yb), (x+bl, yb+24), (x-hw, yb), (x-hw+bl*.5, (yt+yb)/2)], WOOLC, INK, 9)
    for i in range(1, 6): xx = x-hw+2*hw*i/6; c.line([(xx, yt+10), (xx+bl*.6, yb-6)], 4, (196, 180, 146), False)
    c.text(960, 560, "FOR ONE\nLARGE SAIL", 150, NAVY); return c
def grease(k):
    if k == 0:
        c = hall(fire=.8, hole="day", smoke=.4, x0=60, x1=260, posts=())
        for xx in (520, 1500): c.line([(xx, 520), (xx, 1010)], 20, INK, False); c.line([(xx, 520), (xx, 1010)], 12, PLANK, False)
        c.line([(470, 560), (1550, 560)], 26, INK, False); c.line([(470, 560), (1550, 560)], 16, PLANK, False); q = T.LP; c.rect(580, 566, 1440, 950, WOOLC, INK, 8); c.rect(580, 566, 580+860*q, 950, (196, 168, 104), None)
        for i in range(1, 6): c.line([(580+i*143, 572), (580+i*143, 944)], 3, (170, 150, 110), False)
        c.rect(580, 566, 1440, 950, None, INK, 8)
        for i in range(5):
            xx = 640+i*150
            if xx < 580+860*q: yy = 956+((T.TT*130+i*40) % 70); c.ell(xx-7, yy-9, xx+7, yy+9, (196, 168, 104), INK, 3)
        s = sidp(c, min(1640, 700+900*q), 1056, 320, "up", "det", flip=True); c.jug(330, 1040, 1.0); L(c, "THEN IT'S SOAKED IN GREASE", 330, 1000, 66); return c
    c = seashore("storm", "wet"); c.longship(960, 790, 1000, bob=T.TT*2, wind=T.TT*2); c.swell(802, T.TT, (62, 84, 104), 14, 300, ph=2, y1=856)
    for i in range(14):
        q = ((i/14+T.TT*.9) % 1); x0 = 740+(i*37) % 440; y0 = 280+(i*53) % 300; c.ell(x0+q*60-7, y0+q*q*160-7, x0+q*60+7, y0+q*q*160+7, WATER, INK, 3)
    rainf(c, 60); L(c, "TO HOLD THE WIND AND SHED THE WATER", 940, 960, 58, bg=MARI); return c
def clothes(k):
    c = C(EV)
    if k < 2:
        n = count(0, 100, 1.1, .1, "c100"); crowd(c, 200, 440, 100, 25, 62, 130, 70, shown=n); c.text(960, 220, f"SEA CLOTHES FOR {n} MEN", 100, NAVY)
        if k == 1: c.longship(1750, 360, 240, bob=T.TT*2, wind=T.TT); c.label(960, 990, "AND THE SAIL OF A VERY BIG SHIP", 50, bg=MARI)
        return c
    n = count(0, 84, 1.3, .1, "c84"); c.text(600, 520, str(n), 460, RED); c.text(1340, 440, "YEARS", 170, NAVY); c.text(1340, 640, "OF ONE PERSON'S\nLABOUR", 80); L(c, "ONE CALCULATION", 930, 960, 64, bg=MARI); return c
def pct(k=0):
    c = C(EV); q = app("pct", .9, .1); c.rect(200, 460, 1720, 640, WOOLC, INK, 9, 12); c.rect(200, 460, 200+max(20, 1520*.034*q), 640, (136, 94, 62), INK, 9, 6)
    c.line([(226, 650), (300, 790)], 6, INK, False); c.text(560, 860, "BUILDING THE SHIP:\nABOUT 3%", 76, (110, 70, 44)); c.text(1000, 550, "EVERYTHING ELSE", 90, NAVY); c.longship(1500, 930, 300, sail=0); L(c, "THE WHOLE JOB, BY THAT CALCULATION", 280, 960, 64); return c
def benchf(k=0):
    c = C(EV); c.longship(960, 960, 1500, mast=False, oars=7); n = 7
    for i in range(n):
        x = 440+i*174; c.person(x, 945, 150, "hold", "det", ("red", "blue", "brown", "slate", "green")[i % 5])
        if k:
            q = app(("bw", i), .25, i*.2)
            if q > 0:
                for j in range(7): yy = lerp(700, 500, j/7); c.ell(x-5, yy-5, x+5, yy+5, RED, None)
                whead(c, x, 340, .9*q, ("rose", "green", "blue", "brown")[i % 4])
    L(c, "EVERY MAN ON A ROWING BENCH..." if k == 0 else "...NEEDS A WOMAN AT HOME, WORKING MOST OF A YEAR", 150, 960, 60 if k == 0 else 50, bg=PAPER if k == 0 else MARI); return c
def money(k):
    if k == 0:
        c = ev("ICELAND, LATER"); c.clothbolt(620, 800, 2.0); c.text(1020, 640, "=", 260, NAVY); c.text(1420, 640, "MONEY", 190, RED); L(c, "THE CLOTH ITSELF", 230, 960, 76); return c
    if k == 1:
        c = ev("ICELAND, LATER"); c.rect(0, 900, W, H, (206, 186, 150), None); c.line([(0, 900), (W, 900)], 6, INK, False); table(c, 1040, 1560, 1010, 190); f = c.person(1700, 1010, 360, "hold", "n", "banker", flip=True); c.text(1300, 940, "TAXES", 70, PAPER)
        x = lerp(380, 780, T.ease(T.LP*1.3)); w = woman(c, x, 1010, 350, "hold", "n", "blue"); c.clothbolt(w["hand"][0]+90, w["hand"][1]+60, .7, n=3); c.clothbolt(1300, 786, .7, n=2); L(c, "YOU COULD PAY YOUR TAXES IN IT", 240, 960, 66, bg=MARI); return c
    c = ev("ICELAND, LATER"); f = c.person(420, 1010, 420, "point", "smile", "teal"); hair(c, f); say(c, f, 1180, 330, "WOMEN WERE\nMAKING THE MONEY!", 90); c.label(1320, 700, "ONE ARCHAEOLOGIST", 50, bg=MARI); c.clothbolt(1500, 1000, 1.0); return c
def shipyou(k=0):
    c = seashore("day", "spring"); c.longship(1200, 900, 900, sail=0)
    for xx in (880, 1200, 1520): c.line([(xx-60, 946), (xx+60, 946)], 22, TIMBER, False)
    s = sidp(c, 300, 1040, 360, "point", "smile"); L(c, "THE SHIP YOU WANTED A PLACE ON", 180, 960, 64); return c
def above(k=0):
    c = seashore("day", "spring"); mx, my = c.longship(620, 780, 900, bob=T.TT*1.2, wind=T.TT); c.swell(792, T.TT, (98, 150, 182), 9, 300, ph=2, y1=840)
    if k == 0: c.label(620, 150, "AND ABOVE IT", 70); return c
    for i in range(4):
        q = app(("w4", i), .3, i*.3)
        if q > 0: woman(c, 1180+i*190, 1050, 270*q, "stand", "n", ("rose", "green", "blue", "brown")[i], flip=True)
    c.label(1440, 420, "BY THAT COUNT:\nA YEAR OUT OF\nFOUR WOMEN'S LIVES", 60, bg=MARI); return c
def backroom(k):
    if k == 2:
        c = seashore("day", "spring"); c.longship(960, 790, 1100, bob=T.TT*1.2, wind=T.TT); c.swell(802, T.TT, (98, 150, 182), 9, 300, ph=2, y1=850); L(c, "AND IT WAS MOSTLY WOMEN\nWHO MADE THE SAIL", 930, 960, 62, bg=MARI); return c
    c = hall(fire=1.0, hole="day", smoke=1.7, x0=140, x1=640, posts=(300,)); c.loom(1250, 1000, .9, .55, T.TT); w = woman(c, 1560, 1030, 360, "point", "n", "rose", flip=True); kd = kid(c, 900, 1040, 180, "stand", "worry", "green")
    if k == 0: L(c, "THINK BACK TO THAT SMOKY ROOM", 300, 960, 64); return c
    c.marker(w["head"][0], w["head"][1]-110, 44); c.marker(kd["head"][0], kd["head"][1]-90, 34); L(c, "THE BEST GUESS AT WHO BREATHED THE MOST:\nTHE WOMEN AND THE SMALL CHILDREN", 290, 960, 50, bg=MARI); return c
def summer1(k):
    if k == 0:
        c = C((214, 232, 196)); c.calpage(560, 540, 1.6, "APRIL", "THU", c=DGREEN); c.text(560, 880, "SUMMER BEGINS", 80, DGREEN); sunlow(c, 1360, 470, 110); c.text(1360, 760, "THE ICELANDIC\nCALENDAR", 70, NAVY); return c
    if k == 1:
        c = farm("day", "spring", sun=(1700, 250), x=1380, w=620, byre=False, y=760); c.rect(0, 860, W, H, SOIL, None); c.line([(0, 860), (W, 860)], 6, INK, False)
        for i in range(6): c.line([(0, 900+i*34), (W, 900+i*34)], 4, (128, 94, 68), False)
        x = lerp(300, 700, T.GP); s = sidp(c, x, 1056, 320, "up", "smile"); hx, hy = s["hand"]
        for i in range(8): q = ((i/8+T.TT*.8) % 1); c.ell(hx+q*240-6, hy+q*q*400-6, hx+q*240+6, hy+q*q*400+6, WHEATC, INK, 2)
        L(c, "FIRST THE SOWING", 250, 620, 76); return c
    c = seashore("day", "spring"); q = T.ease(T.LP); x = lerp(1250, 800, q); y = lerp(900, 810, q); c.longship(x, y, 700, flip=True, sail=0, bob=T.TT*2*q)
    if q > .5: c.swell(822, T.TT, (98, 150, 182), 9, 300, ph=2, y1=860, x0=0, x1=int(x+240))
    for i in range(3): man(c, x+450+i*150, 1046, 280, "pull", "det", ("brown", "slate", "red")[i], flip=True)
    L(c, "THEN THE SHIPS GO DOWN TO THE WATER", 170, 960, 60, bg=MARI); return c
def leave(k):
    c = seashore("gold", "spring"); x = lerp(1000, 460, T.GP); w = lerp(520, 300, T.GP); c.longship(x, 690, w, flip=True, bob=T.TT*1.5, wind=T.TT); c.swell(700, T.TT*.7, (110, 160, 172), 7, 300, ph=2, y1=790)
    woman(c, 1380, 1040, 340, "wave", "n", "rose", flip=True); woman(c, 1700, 1040, 330, "stand", "n", "blue", flip=True); kid(c, 1120, 1050, 180, "wave", "smile", "green", flip=True)
    if k == 0: L(c, "THEY'LL COME HOME WITH PLUNDER, AND STORIES", 200, 960, 56); return c
    L(c, "THE VIKING AGE", 300, 960, 150, bg=MARI); return c
def recap(k):
    c = C(EV)
    for i, (x, t) in enumerate(((330, "THEY SKATED"), (960, "THEY DRANK"), (1590, "SOME MADE THE\nSUMMER POSSIBLE"))):
        c.rect(x-280, 200, x+280, 940, PAPER if (i < 2 or k < 2) else (255, 240, 200), INK, 8, 24)
        if k < i: continue
        q = app(("rc", i), .3); c.text(x, 300, t, 56 if i == 2 else 70, NAVY if i < 2 else RED)
        if i == 0: c.rect(x-270, 760, x+270, 930, ICEC, None, 0, 20); skater(c, x+60*math.sin(T.TT*1.4), 800, 250*q)
        if i == 1: f = man(c, x, 850, 280*q, "wave", "joy", "red", bd=True); c.horn(f["hand"][0], f["hand"][1]-70-20*abs(math.sin(T.TT*4)), .8, flip=True); c.ell(f["hand"][0]-14, f["hand"][1]-14, f["hand"][0]+14, f["hand"][1]+14, PAPER, INK, 5)
        if i == 2: c.loom(x-70, 900, .62*q, lerp(.3, .7, T.LP), T.TT); woman(c, x+150, 900, 250*q, "point", "n", "rose", flip=True)
    return c
def spinage(k=0):
    c = C(EV); c.text(860, 430, "THE SPINNING AGE", 190, NAVY)
    if T.LT > .7 or not life._new(("sa",)): c.strike(250, 446, 1470, 16)
    s = sidp(c, 1560, 1030, 340, "up", "n"); hx, hy = s["hand"]; c.spindle(hx, hy+190+30*math.sin(T.TT*.9), 1.4, T.TT, (hx, hy)); return c
def finq(k=0):
    c = farm("day", "spring", lit=False, sun=(420, 300), x=520, w=760, byre=False, rp=False); return Q(c, 4, 4, HID)
def hidrow(k=0):
    c = C(); c.questlog(ROWS, 4, 3, None if (k == 0 and T.LT < .0) else (HID if k else None), x=545, y=200); return c

def sidbench(c, x, pose="stand", ex="n", h=300, **k):
    """Sid sitting on the wall bench."""
    return sidp(c, x, 792, h, pose, ex, **k)
def joint(c, x, y, k=1.0):
    """A leg of smoked meat hanging from (x, y)."""
    c.rect(x-9*k, y, x+9*k, y+60*k, BONEC, INK, max(3, 4*k), 6*k)
    c.poly([(x-18*k, y+46*k), (x+18*k, y+46*k), (x+56*k, y+120*k), (x+50*k, y+190*k), (x, y+218*k), (x-50*k, y+190*k), (x-56*k, y+120*k)], MEAT, INK, max(3, 6*k))
    c.line([(x-30*k, y+110*k), (x-36*k, y+170*k)], max(3, 7*k), (226, 150, 130), False)
def stockfish(c, x0, y0, x1, y1, w=40):
    """A dried, split, headless cod lying from its tail (x0, y0) to the cut end (x1, y1): stiff as a board."""
    Ln = math.hypot(x1-x0, y1-y0); ux, uy = (x1-x0)/Ln, (y1-y0)/Ln; nx, ny = -uy, ux; P = lambda q, v: (x0+ux*Ln*q+nx*v, y0+uy*Ln*q+ny*v)
    c.poly([P(-.1, w*.9), P(.02, 0), P(-.1, -w*.9), P(.1, -w*.3), P(.1, w*.3)], CODD, INK, 6)
    c.poly([P(.08, w*.3), P(.4, w*.8), P(.85, w), P(1, w*.8), P(1, -w*.8), P(.85, -w), P(.4, -w*.8), P(.08, -w*.3)], CODD, INK, 7); c.line([P(.25, 0), P(.97, 0)], 4, (170, 146, 96), False)
def fishbone(c, x, y, k=1.0):
    """A fish vertebra: a small ring with spines."""
    for a in (-78, -102, 78, 102): c.line([(x, y), (x+74*k*math.cos(math.radians(a)), y+74*k*math.sin(math.radians(a)))], max(3, 6*k), INK, False)
    c.ell(x-30*k, y-30*k, x+30*k, y+30*k, BONEC, INK, max(3, 6*k)); c.ell(x-10*k, y-10*k, x+10*k, y+10*k, (200, 190, 160), INK, max(2, 3*k))
def hair(c, f, col=(110, 70, 40)):
    u = f["u"]; hx, hy = f["head"]; lw = max(4, u*.07)
    for sgn in (-1, 1): c.rect(hx+sgn*.6*u-.13*u, hy+.2*u, hx+sgn*.6*u+.13*u, hy+1.05*u, col, INK, lw, .1*u)
    c.d.pieslice([(hx-.68*u)*S, (hy-.24*u)*S, (hx+.68*u)*S, (hy+.7*u)*S], 180, 360, fill=col, outline=INK, width=int(lw*S))
def say(c, f, bx, by, t, size=62, flip=False):
    """A speech bubble centred on (bx, by) whose tail ends beside the mouth of the fig f. Keep the bubble above the head."""
    u = f["u"]; mx, my = f["head"][0]+(-.5 if flip else .72)*u, f["head"][1]+.62*u; n = t.count("\n")+1; h = size*1.2*n+34*1.3; c.bubble(bx, by, t, size, (mx-bx, my-(by+h/2)))
def scribe(c, coat="banker", ton=True):
    """Someone writing a book at a desk by candlelight."""
    table(c, 700, 1440, 1000, 190); c.candle(1360, 776, 1.0, T.TT); f = c.person(880, 1010, 380, "write", "det", coat); book(c, 1190, 752, 1.5)
    if ton: c.tonsure(f)
    c.line([f["hand"], (f["hand"][0]+70+6*math.sin(T.TT*9), f["hand"][1]-90)], 6, INK, False); return f
def crowd(c, x0, y0, n, per=20, gx=80, gy=140, h=78, shown=None, coats=("red", "blue", "brown", "slate", "green")):
    """n small people in rows of per, from the top left; shown limits how many have arrived."""
    for i in range(n if shown is None else min(n, int(shown))): c.person(x0+(i % per)*gx, y0+(i//per)*gy, h, "stand", "n", coats[(i*7+i//per) % len(coats)])
def note(c, x, y, k=1.0, col=PAPER):
    """A written music note, floating."""
    c.ell(x-16*k, y-12*k, x+16*k, y+12*k, col, None); c.line([(x+14*k, y), (x+14*k, y-70*k), (x+44*k, y-54*k)], max(3, 6*k), col, False)
def crew(c, x, y, w, flip=False, n=5):
    """Men standing in a ship at (x, y, w), shields along the side."""
    for i in range(n): px = x+(-.29+.58*i/(n-1))*w; c.person(px, y-.012*w, w*.18, "stand", "det", ("red", "blue", "brown", "slate", "green")[i % 5], flip=flip); c.roundshield(px, y-.034*w, w*.04, (RED, MARI, TEAL)[i % 3])
def codroute(c, P, q=1.0, n=30):
    """The dotted line from the Lofoten cod grounds to Haithabu, bent out over the sea (a sketch: nobody knows the route)."""
    a = P(*NORTHPLACES["HAITHABU"]); b = P(*NORTHPLACES["LOFOTEN"])
    for i in range(int(n*q)+1): x = lerp(b[0], a[0], i/n)-300*math.sin(math.pi*i/n)**.8; y = lerp(b[1], a[1], i/n); c.ell(x-8, y-8, x+8, y+8, RED, None)
def whead(c, x, y, k=1.0, col="rose"):
    """A small woman, head and shoulders: head-cloth, face, dress."""
    c.rect(x-44*k, y+26*k, x+44*k, y+120*k, DRESS[col], INK, max(3, 6*k), 16*k); c.rect(x-40*k, y-40*k, x+40*k, y+30*k, PAPER, INK, max(3, 6*k), 12*k)
    c.d.pieslice([(x-50*k)*S, (y-62*k)*S, (x+50*k)*S, (y+16*k)*S], 180, 360, fill=WOOLC, outline=INK, width=int(max(3, 6*k)*S))
    for dx in (-14, 14): c.line([(x+dx*k, y-12*k), (x+dx*k, y+2*k)], max(2, 5*k), INK, False)
def Fq(n, t): g = lambda: qcard(n, t); g.scene = "qcard"+n; return g
# (narration, [frames], chime?)   Respellings are for the voice only; CAPTION_FIX restores the display forms.
U = [
 ("You wake up on a wooden bench, in the dark, breathing smoke.", [F(wake, 0), F(wake, 1)]),
 ("Late December, central Norway, around the year nine fifty. Four and a half hours of daylight.", [F(where, 0), F(where, 1), F(where, 2)]),
 ("Winter, by the old Icelandic calendar, is a hundred and eighty days long. What the farm killed and stored this autumn has to last.", [F(days, 0), F(store, 0), F(store, 1)]),
 ("You've heard what Vikings do in summer. This is the other half of the year.", [F(summer, 0), F(summer, 1)], "chime"),
 ("You're sixteen winters old. Next summer you want a place on a ship.", [F(youare, 0), F(youare, 1)]),
 ("You are made up. So is the farm. The evidence is real. It comes from all over the Norse world, and some of it was written down centuries later.", [F(madeup, 0), F(madeup, 1), F(madeup, 2), F(madeup, 3)]),
 ("Here's your quest log. One: fill the house before the snow.", [F(qfarm, 0), F(qfarm, 1)], "tick"),
 ("Two: stay warm without choking.", [F(qfarm, 2)], "tick"),
 ("Three: get through a hundred and eighty days.", [F(qfarm, 3)], "tick"),
 ("There's a fourth quest hidden at the end. It's the one nobody names an age after.", [F(qfarm, 4), F(hiddenq, 1, 0), F(noage)], "tick"),
 ("Quest one. Fill the house. Go back to October.", [Fq("ONE", "FILL THE HOUSE"), F(october)], "tick"),
 ("That Icelandic calendar has only two seasons. Summer and winter.", [F(seasons, 0), F(seasons, 1)]),
 ("Winter begins on a Saturday in October, and people count their ages in winters. Not years. Winters.", [F(begins, 0), F(begins, 1), F(begins, 2)]),
 ("Winter's first job is arithmetic. How much hay did you cut this summer?", [F(hayq, 0), F(hayq, 1)]),
 ("In Iceland, where the best evidence is, cattle spend the winter indoors, eating it. Sheep are tougher, and can graze outside.", [F(cattle, 0), F(cattle, 1), F(cattle, 2)]),
 ("So every autumn the farm does a sum. An archaeologist who dug one of those farms put it plainly: they had to decide how many to slaughter and store.", [F(sumf, 0), F(sumf, 1), F(sumf, 2), F(sumf, 3)]),
 ("Keep too many, and the hay runs out before the grass comes back.", [F(toomany, 0), F(toomany, 1)]),
 ("After a cold, wet summer there isn't enough hay, and farmers, small ones most of all, have little choice but to cull hard.", [F(wet, 0), F(wet, 1), F(wet, 2)]),
 ("Which makes for a strange result. One scholar of Iceland thinks that after a bad summer, people may have eaten better than usual.", [F(better, 0), F(better, 1), F(better, 2)]),
 ("The danger is a second bad summer, when farmers are trying to keep whatever animals they have left.", [F(second, 0), F(second, 1)]),
 ("Now keep the meat. Dry it. Smoke it. Salt it, where there's salt.", [F(keep, 0), F(keep, 1), F(keep, 2)]),
 ("After the slaughter come the sausages, from the offal and the blood. The butter is salted hard. In a long winter, fat is what you need.", [F(saus, 0), F(saus, 1), F(saus, 2)]),
 ("In Iceland, with no salt, they keep food in big vats of curdled milk.", [F(vats, 0), F(vats, 1)]),
 ("And far up the Norwegian coast there's a better trick, one that seems to be in use by your day. Hang cod on wooden racks, and let the cold air dry it.", [F(lofo, 0), F(lofo, 1), F(lofo, 2)]),
 ("It's called stockfish. Some medieval accounts suggest it could still be eaten as much as ten years later.", [F(stock, 0), F(stock, 1)]),
 ("In twenty seventeen, scientists read the DNA in five cod bones from a Viking Age port in what is now Germany. They matched the Arctic cod that swim off Lo-fo-ten, more than a thousand miles away.", [F(dna, 0), F(dna, 1), F(dna, 2), F(dna, 3)]),
 ("That fish had travelled further than you ever have.", [F(further)]),
 ("Quest one, complete. Let it snow.", [F(qdone, 1)], "chime"),
 ("Quest two. Stay warm without choking.", [Fq("TWO", "STAY WARM WITHOUT CHOKING")], "tick"),
 ("Your house is long, built of wood, with a long fire down the middle.", [F(house, 0), F(house, 1)]),
 ("There's no chimney, and there are no windows. The smoke leaves through a hole in the roof. Eventually.", [F(nochim, 0), F(nochim, 1), F(nochim, 2)]),
 ("Along the walls run plank beds. You sit on them by day, and sleep on them by night.", [F(beds, 0), F(beds, 1)]),
 ("If the farm has no separate stable, the animals are stalled at one end. Same roof. Same air.", [F(stall, 0), F(stall, 1)]),
 ("About that air.", [F(air)]),
 ("In the winter of twenty eleven to twelve, people in Denmark spent thirteen weeks living in two rebuilt Viking Age houses, cooking and heating with a wood fire.", [F(dk, 0), F(dk, 1), F(dk, 2)]),
 ("Scientists measured what they breathed. The carbon monoxide and the fine smoke particles both came out higher than the limits the World Health Organization sets today.", [F(meas, 0), F(meas, 1), F(meas, 2)]),
 ("The researchers think women and small children probably got the worst of it.", [F(worst, 0), F(worst, 1)]),
 ("Remember that. It comes back.", [F(worst, 2)]),
 ("In Viking York, the fire also gave most of the light. The rest was rush lamps, and the odd candle.", [F(light, 0), F(light, 1)]),
 ("For outdoors, there's a thick cloak, often two layers of it.", [F(cloakf, 0), F(cloakf, 1)]),
 ("And in that same town, archaeologists found a wool sock. One sock. It's the only one of its kind ever found in England.", [F(sockf, 0), F(sockf, 1), F(sockf, 2)]),
 ("Some things don't change.", [F(nochange)]),
 ("An Old Norse poem lists what a traveller needs when he comes in from the cold. Fire, for knees numb with cold. Food and clothing. Water, a chance to dry off, and a friendly word.", [F(poem, 0), F(poem, 1), F(poem, 2), F(poem, 3)]),
 ("The house has an enemy of its own. Damp. Damp rots wood.", [F(damp, 0), F(damp, 1)]),
 ("Quest two, complete. You're warm. You smell like a smoked ham.", [F(qdone, 2), F(hamq)], "chime"),
 ("Quest three. Get through a hundred and eighty days.", [Fq("THREE", "GET THROUGH 180 DAYS")], "tick"),
 ("By the solstice, the daylight is down to those four and a half hours.", [F(sol, 0), F(sol, 1)]),
 ("The Icelanders had a name for the month around the solstice. It can be read as fat-sucker.", [F(month, 0), F(month, 1)]),
 ("So what do you actually do all winter?", [F(what)]),
 ("You strap bones to your feet.", [F(bones)]),
 ("Ice skates. The lower leg bone of a cow or a horse, tied on with leather laces.", [F(skate, 0), F(skate, 1)]),
 ("You don't lift your feet. You stand on the bones and push yourself along with a pole.", [F(glide, 0), F(glide, 1)]),
 ("Rub pig fat underneath, and they run faster.", [F(pigf, 0), F(pigf, 1)]),
 ("At one dig in York, archaeologists found more than forty of them.", [F(forty, 0), F(forty, 1)]),
 ("They're for getting about, and they're for fun. The National Museum of Denmark says both.", [F(fun, 0), F(fun, 1)]),
 ("Where the snow comes early, you ski.", [F(skis)]),
 ("A pair of skis melted out of a Norwegian ice patch. One in twenty fourteen. Its partner, seven years later.", [F(patch, 0), F(patch, 1), F(patch, 2)]),
 ("They're a little over six feet long, and they were made in the seven hundreds, a couple of centuries before you.", [F(skilen, 0), F(skilen, 1)]),
 ("One of the archaeologists said they'd be called powder boards today.", [F(powder, 0), F(powder, 1)]),
 ("Then, in the middle of the afternoon, the sun goes down.", [F(sundown)]),
 ("So you play. There's a board game called nef-ah-tah-fell, and there are dice.", [F(play, 0), F(play, 1), F(play, 2)]),
 ("The pieces survive. Stone, bone, glass, antler, amber.", [F(pieces, 0), F(pieces, 1)]),
 ("And one saga carries a warning against gambling with dice.", [F(warn, 0), F(warn, 1)]),
 ("When there's a feast, you listen. Poems. Music. Stories.", [F(feast, 0), F(feast, 1)]),
 ("The stories that got written down, centuries later in Iceland, keep putting their hauntings at Yule.", [F(written, 0), F(written, 1)]),
 ("In one, a man called Glam is found dead in the snow at Yule, and comes back. The hauntings ease as the days grow longer.", [F(glam, 0), F(glam, 1), F(glam, 2)]),
 ("And in the myths, the end of the world begins with a winter that lasts three years.", [F(threew, 0), F(threew, 1)]),
 ("In the dark, that doesn't feel like a myth.", [F(darkf)]),
 ("Then midwinter. By the Icelandic calendar, the halfway mark. Ninety days down. Ninety to go.", [F(mid, 0), F(mid, 1)]),
 ("And somewhere in the dark middle of it, Yule.", [F(yule)]),
 ("Here's what we really know about the old Yule. Not much. The fullest account was written by an Icelander more than two hundred years later, and scholars still argue about the date.", [F(know, 0), F(know, 1), F(know, 2)]),
 ("He says it started on midwinter night and ran for three nights.", [F(nights3)]),
 ("He also says a king of about your time, Hawkon the Good, ordered Yule moved to the same time as Christmas.", [F(hakon, 0), F(hakon, 1)]),
 ("And that everyone had to have ale for it, brewed from a measure of grain, or pay a fine. And keep the feast for as long as the ale lasted.", [F(ale, 0), F(ale, 1), F(ale, 2)]),
 ("The translations say a measure of grain. By one estimate a measure was about sixteen litres, roughly four gallons. Some retellings make it sixteen litres of ale.", [F(litres, 0), F(litres, 1), F(litres, 2)]),
 ("As laws go, it's a popular one.", [F(popular)]),
 ("The Christian part was less popular. In the same saga, farmers make the king eat horse liver at a Yule feast.", [F(liver, 0), F(liver, 1), F(liver, 2)]),
 ("Now look who's at the table. The raiders. Home for the winter.", [F(raiders, 0), F(raiders, 1)]),
 ("Because raiding can be seasonal work. One saga spells it out.", [F(seasonal, 0), F(seasonal, 1)]),
 ("It's the saga of the Orkney earls, and the raider is called Svayn, two centuries after you. In spring he sows his fields. Then he goes plundering. He calls it his spring trip.", [F(svein, 0), F(svein, 1), F(svein, 2)]),
 ("He's home after midsummer for the harvest, raids again until a month into winter, and then stays home, with some eighty men eating and drinking at his expense.", [F(svein2, 0), F(svein2, 1), F(svein2, 2)]),
 ("Not everyone comes home. A century before you, in eight fifty-one, the Anglo-Saxon Chronicle records that the heathens, for the first time, stayed over winter. It was worth writing down.", [F(stay851, 0), F(stay851, 1), F(stay851, 2), F(stay851, 3)]),
 ("Quest three, complete. The ice goes soft. You made it.", [F(qdone, 3, None, "day", "spring", False), F(thaw)], "chime"),
 ("But there was a fourth quest. You've walked past it all winter.", [F(hiddenq, 1, 3), F(walkpast)]),
 ("It's the loom.", [F(loomr)], "tick"),
 ("Making cloth doesn't wait for a season. It goes on all year round, and it's mostly the women who do it.", [F(clothy, 0), F(clothy, 1)]),
 ("Not only for clothes. For the ship.", [F(forship, 0), F(forship, 1)]),
 ("A big warship's sail is probably more than a thousand square feet of cloth, and most are wool.", [F(sailbig, 0), F(sailbig, 1)]),
 ("The thread is spun on hand spindles, and the cloth is woven in strips.", [F(spin, 0), F(spin, 1)]),
 ("How much wool? The estimates run from the wool of a hundred and fifty sheep, to a year's wool from about seven hundred.", [F(woolq, 0), F(woolq, 1), F(woolq, 2)]),
 ("How much work? One textile researcher, working from experiments, puts it at four women, ten hours a day, for a full year.", [F(workq, 0), F(workq, 1), F(workq, 2)]),
 ("For one large sail.", [F(onesail)]),
 ("Then it's soaked in grease, to hold the wind and shed the water.", [F(grease, 0), F(grease, 1)]),
 ("And the crew needs sea clothes. One calculation, for a very big ship, its sail and a hundred men, comes to eighty-four years of one person's labour.", [F(clothes, 0), F(clothes, 1), F(clothes, 2)]),
 ("Building the ship itself was about three percent of the job.", [F(pct)]),
 ("By that sum, every man on a rowing bench needs a woman at home, working most of a year, to put him there.", [F(benchf, 0), F(benchf, 1)]),
 ("In Iceland, later, the cloth itself was money. You could pay your taxes in it. As one archaeologist put it: women were making the money.", [F(money, 0), F(money, 1), F(money, 2)]),
 ("So here is the ship you wanted a place on.", [F(shipyou)]),
 ("And above it, by that count, a year out of four women's lives.", [F(above, 0), F(above, 1)]),
 ("Think back to that smoky room. The researchers' best guess at who breathed the most of it: the women and the small children. And it was mostly women who made the sail.", [F(backroom, 0), F(backroom, 1), F(backroom, 2)]),
 ("By the Icelandic calendar, the first day of summer is a Thursday in April. First the sowing. Then the ships go down to the water.", [F(summer1, 0), F(summer1, 1), F(summer1, 2)]),
 ("They'll come home with plunder, and stories. One day the whole age will be named after them.", [F(leave, 0), F(leave, 1)]),
 ("So what did Vikings do all winter? They skated. They drank. And some of them made the summer possible.", [F(recap, 0), F(recap, 1), F(recap, 2)]),
 ("Nobody is going to call it the Spinning Age.", [F(spinage)]),
 ("Quest four, complete.", [F(finq)], "chime"),
]

CAPTION_FIX = [("Lo-fo-ten", "Lofoten"), ("Svayn", "Svein"), ("nef-ah-tah-fell", "hnefatafl"), ("Hawkon", "Hákon"), ("nine fifty", "950"), ("a hundred and eighty days", "180 days"), ("Four and a half hours", "4½ hours"), ("four and a half hours", "4½ hours"),
               ("sixteen winters", "16 winters"), ("twenty seventeen", "2017"), ("twenty eleven to twelve", "2011 to 2012"), ("thirteen weeks", "13 weeks"), ("more than forty", "more than 40"), ("twenty fourteen", "2014"), ("seven hundreds", "700s"),
               ("Ninety days down. Ninety to go.", "90 days down. 90 to go."), ("two hundred years", "200 years"), ("sixteen litres", "16 litres"), ("some eighty men", "some 80 men"), ("eight fifty-one", "851"),
               ("a hundred and fifty sheep", "150 sheep"), ("about seven hundred", "about 700"), ("ten hours a day", "10 hours a day"), ("a hundred men", "100 men"), ("eighty-four years", "84 years"), ("three percent", "3 percent"), ("a thousand square feet", "1,000 square feet"), ("a thousand miles", "1,000 miles"), ("ten years later", "10 years later")]
