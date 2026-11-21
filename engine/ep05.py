"""EP005: You Joined Magellan's Voyage in 1519. Only 18 Finished It.   (at sea, Spain to the Spice Islands and home, 1519-1522; point-of-view pillar)

Same contract as ep01.py to ep04.py. Motion helpers (app, E, lerp, step, arrow) come from ep02.
A date chip and a row of five ship marks in the top-left corner carry the date and the size of the fleet through the episode.
The sea, the ships, the flags, the route on the map and every counter move with T.TT / T.LT / T.LP / T.GP and rest in their
final state on the contact sheet. The maps are sketches (modern coastlines, roughly drawn) and say so on screen.
"""
from thsq import *
import math
import thsq as T
import life
from ep02 import E, app, lerp, step, card, arrow, chip, F
ROWS = ["FIND THE WAY THROUGH", "CROSS THE OTHER SIDE", "FILL UP WITH CLOVES"]; HID = "GET HOME"
SK = {"day": ((132, 192, 226), (232, 240, 232)), "dawn": ((122, 150, 200), (250, 214, 176)), "grey": ((112, 122, 138), (196, 200, 198)), "storm": ((54, 60, 78), (128, 136, 146)),
      "dusk": ((60, 52, 92), (236, 150, 104)), "gold": ((238, 186, 110), (252, 232, 176)), "night": ((14, 20, 46), (50, 64, 106)), "cold": ((150, 170, 190), (226, 232, 236))}
SEAC = {"day": (OCEAND, OCEAN), "dawn": ((70, 110, 150), (98, 142, 176)), "grey": ((70, 92, 108), (98, 122, 136)), "storm": ((40, 58, 76), (62, 84, 104)), "dusk": ((58, 66, 110), (86, 96, 142)),
        "gold": ((80, 128, 150), (110, 160, 172)), "night": ((20, 32, 62), (34, 52, 88)), "cold": ((84, 116, 138), (112, 146, 166))}
SEAM = (196, 220, 230); FAINT = (96, 88, 78); DECKC = (198, 162, 118); DECKL = (160, 124, 88); HOLD = (78, 58, 46); INKP = (110, 40, 30)
CAPS = {"blue": (70, 90, 130), "brown": (120, 84, 60), "slate": (70, 74, 96), "rose": (170, 100, 96), "teal": (160, 56, 48), "green": (70, 110, 76), "red": (120, 44, 40)}
CREW = ["blue", "brown", "slate", "rose"]
# The route as a sketch: (longitude, latitude), longitude running on below -180 so the line can be drawn across the edge of the map.
ROUTE = [(-6.4, 36.8), (-18, 28), (-26, 12), (-31, -2), (-33, -12), (-43.2, -23), (-50, -31), (-56, -36.5), (-63, -43), (-67.2, -49.3), (-68, -52.3), (-71, -53.4), (-75.5, -52.5), (-79, -44), (-84, -30), (-100, -18), (-125, -10), (-155, -2),
         (-180, 6), (-205, 11), (-215.2, 13.5), (-234.4, 11), (-236.1, 10.3), (-240, 8), (-244, 5.5), (-238, 3.5), (-232.6, .7), (-234, -6), (-240, -10.5), (-255, -22), (-280, -34), (-310, -39), (-341.5, -37), (-349, -30), (-358, -15), (-372, 0),
         (-381, 10), (-383.6, 15), (-388, 30), (-378, 37), (-366.4, 36.8)]
ST = {"START": 0, "RIO": 5, "PLATE": 7, "JULIAN": 9, "VIRGINS": 10, "OUT": 12, "THIEVES": 20, "PHIL": 21, "CEBU": 22, "TIDORE": 26, "CAPE": 32, "VERDE": 37, "HOME": 40}

# ---------- small helpers ----------
def L(c, t, y=210, x=W/2, size=64, **k): c.label(x, y, t, size, **k); return c
def Q(c, shown=4, done=0, hidden=None): c.questlog(ROWS, shown, done, hidden); return c
def dimc(c, a=120, col=(10, 14, 30)): c.da.rectangle([0, 0, W*S, H*S], fill=(*col, int(max(0, min(255, a)))))
def hud(c, date=None, ships=None):
    """Date chip, top left; ships = how many of the five are still with you (the rest are crossed out)."""
    w = -16
    if date: w = c.tw(date, 44)+56; c.rect(36, 36, 36+w, 112, PAPER, INK, 6, 16); c.text(64, 71, date, 44, INK, "lm")
    if ships is not None:
        x0 = 36+w+16; c.rect(x0, 36, x0+5*62+22, 112, PAPER, INK, 6, 16)
        for i in range(5): c.naoicon(x0+42+i*62, 92, .74, lost=i >= ships)
    return c
def sky(c, hz, kind="day", clouds=True, sun=True, sx=1600):
    c.im.paste(life._grad(int(hz), *SK[kind]), (0, 0))
    if kind == "night":
        for i in range(56): x = (i*197) % W; y = (i*89) % max(60, int(hz)-70)+10; r = 3+2*math.sin(T.TT*2+i); c.da.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=(255, 248, 236, 230))
        if sun: c.da.ellipse([(sx-110)*S, 250*S, (sx+110)*S, 470*S], fill=(255, 250, 220, 36)); c.ell(sx-52, 308, sx+52, 412, (244, 240, 220), INK, 6); c.ell(sx-22, 300, sx+70, 392, SK[kind][0], None)
        return
    if sun and kind in ("day", "gold", "dawn", "dusk", "cold"):
        sy = hz-150 if kind in ("day", "cold") else hz-74; col = MARI if kind != "dusk" else (244, 130, 80)
        c.da.ellipse([(sx-130)*S, (sy-130)*S, (sx+130)*S, (sy+130)*S], fill=(255, 226, 130, 70)); c.ell(sx-60, sy-60, sx+60, sy+60, col, INK, 6)
    if clouds:
        dark = kind in ("storm", "grey")
        for i, (cx, cy, k) in enumerate(((260, 150, 1.0), (900, 330, .7), (1320, 120, .8))):
            xx = (cx+T.TT*(7+3*i)) % (W+400)-200
            for dx, dy, r in ((-70, 10, 44), (0, -14, 60), (70, 12, 46), (0, 22, 50)): c.da.ellipse([(xx+dx*k-r*k*1.5)*S, (cy+dy*k-r*k)*S, (xx+dx*k+r*k*1.5)*S, (cy+dy*k+r*k)*S], fill=(150, 156, 168, 200) if dark else (255, 255, 255, 200 if kind in ("day", "dawn", "cold") else 120))
def sea(kind="day", hz=540, clouds=True, sun=True, calm=False, sx=300):
    """Open water to the horizon. Put ships on it, then call wash() at their waterline to lay the nearer water over their keels."""
    c = C(SEAC[kind][0]); sky(c, hz, kind, clouds, sun, sx); c.swell(hz, T.TT*.5, SEAC[kind][0], 2 if calm else 5, 420)
    if not calm: c.crests(hz+24, hz+150, T.TT*.5, 9, (200, 220, 226), 1)
    return c
def wash(c, y, kind="day", calm=False, amp=None, n=14, y1=H):
    c.swell(y, T.TT, SEAC[kind][1], (3 if calm else 11) if amp is None else amp, 300, ph=y*.013, y1=y1)
    if not calm: c.crests(y+34, min(y1, H)-30, T.TT, n, FOAM if kind not in ("night", "storm") else (170, 190, 204), int(y) % 7)
    return c
def rain(c, n=70, col=(210, 222, 232, 150)):
    for i in range(n):
        x = (i*211+int(T.TT*900)) % (W+300)-150; y = (i*137+int(T.TT*1500)) % (H+200)-100; c.da.line([x*S, y*S, (x-26)*S, (y+70)*S], fill=col, width=3*S)
def snow(c, n=60):
    for i in range(n):
        x = (i*211+int(T.TT*40)+int(30*math.sin(T.TT+i))) % W; y = (i*137+int(T.TT*120)) % H; c.da.ellipse([(x-5)*S, (y-5)*S, (x+5)*S, (y+5)*S], fill=(255, 255, 255, 220))
def deck(kind="day", mast=1560, roll=True, hz=470, sx=170):
    """On the open deck: sky and a rolling horizon, the bulwark, the planks, one mast with its shrouds."""
    c = C(SEAC[kind][1]); r = 16*math.sin(T.TT*.9) if roll else 0; sky(c, hz+30, kind, sx=sx)
    c.poly([(0, hz-r), (W, hz+r), (W, 660), (0, 660)], SEAC[kind][1], None); c.line([(0, hz-r), (W, hz+r)], 5, INK, False)
    for i in range(7): x = (i*311+int(T.TT*30)) % W; y = hz+50+(i*53) % 120; c.line([(x, y), (x+30, y-6), (x+60, y)], 5, FOAM if kind not in ("night", "storm") else (150, 170, 190), False)
    if mast:
        for dx in (-330, -220, -110, 110, 220, 330): c.line([(mast, -20), (mast+dx, 640)], 5, (84, 70, 58), False)
        for yy in range(120, 640, 86):
            q = yy/660; c.line([(mast-330*q, yy), (mast-110*q, yy)], 4, (84, 70, 58), False); c.line([(mast+110*q, yy), (mast+330*q, yy)], 4, (84, 70, 58), False)
    c.rect(-10, 640, W+10, 830, HULL, INK, 6)
    for yy in (700, 762): c.line([(0, yy), (W, yy)], 4, HULLD, False)
    for x in range(110, W, 250): c.line([(x, 664), (x, 826)], 6, HULLD, False)
    c.rect(-10, 620, W+10, 656, HULLD, INK, 6, 6)
    c.rect(0, 826, W, H, DECKC, None); c.line([(0, 826), (W, 826)], 6, INK, False)
    for i in range(1, 9): c.line([(i*240-80, 832), (i*262-260, H)], 3, DECKL, False)
    if mast:
        c.rect(mast-36, -10, mast+36, 836, HULLD, INK, 7)
        for yy in (300, 620): c.rect(mast-42, yy, mast+42, yy+26, (70, 60, 54), INK, 5, 6)
    return c
def below(lamp=960):
    """Below deck: ribs, planks, a hanging lantern."""
    c = C(HOLD)
    for x in range(-60, W+200, 300): c.line([(x, -10), (x-60, 826)], 34, (56, 42, 34), False)
    for yy in (150, 330, 510, 690): c.line([(0, yy), (W, yy)], 4, (56, 42, 34), False)
    c.rect(0, 826, W, H, (112, 86, 64), None); c.line([(0, 826), (W, 826)], 6, INK, False)
    for i in range(1, 9): c.line([(i*240-80, 832), (i*262-260, H)], 3, (86, 64, 48), False)
    if lamp:
        sw = 26*math.sin(T.TT*1.1); lx = lamp+sw; c.line([(lamp, -10), (lx, 150)], 5, INK, False)
        c.da.ellipse([(lx-520)*S, (190-430)*S, (lx+520)*S, (190+520)*S], fill=(255, 206, 120, 34)); c.da.ellipse([(lx-260)*S, (190-240)*S, (lx+260)*S, (190+280)*S], fill=(255, 214, 130, 40))
        c.rect(lx-34, 150, lx+34, 236, (250, 216, 130), INK, 6, 8); c.rect(lx-42, 138, lx+42, 156, (60, 52, 48), INK, 5, 4)
    return c
def coast(c, y, x0=0, x1=W, h=150, col=ISLE, seed=0, rock=False):
    """A strip of land standing on the line y (headland, far shore, cliffs)."""
    n = max(4, int((x1-x0)/160)); pts = [(x0, y)]
    for i in range(n+1): q = i/n; pts.append((x0+(x1-x0)*q, y-h*(.55+.45*math.sin(q*7+seed)*math.sin(q*3.1+seed*2)) if not rock else y-h*(.6+.4*((i*7+seed) % 3)/2)))
    pts.append((x1, y)); c.poly(pts, col, INK, 6)
def beach(c, y=830, col=SAND, kind="day"):
    c.swell(y, T.TT*.7, col, 6, 560, ph=1.3)
    for i in range(12): x = (i*173) % W; yy = y+50+(i*59) % max(1, H-y-70); c.line([(x, yy), (x+34, yy)], 4, DSAND, False)
    return c
def quay(kind="day", ships=2, hz=520, sun=True):
    """Seville from the riverside: a far bank of houses and a tower, the river, a stone quay in front."""
    c = C(SEAC[kind][0]); sky(c, hz, kind, sun=sun, sx=1700); r = [(40, 150, 90, RWALL), (200, 120, 70, OCHRE), (330, 170, 110, RWALL), (520, 130, 80, PINK), (660, 200, 96, RWALL), (880, 140, 76, OCHRE), (1030, 180, 104, RWALL), (1230, 150, 84, PINK), (1500, 190, 92, RWALL), (1700, 160, 80, OCHRE)]
    for x, w, h, col in r:
        c.rect(x, hz-h, x+w, hz, col, INK, 5); c.poly([(x-8, hz-h), (x+w/2, hz-h-34), (x+w+8, hz-h)], TILE, INK, 5); c.rect(x+w*.4, hz-h*.5, x+w*.6, hz-h*.2, GLASSD, INK, 3)
    c.rect(1390, hz-250, 1470, hz, RWALL, INK, 6); c.rect(1380, hz-270, 1480, hz-244, RWALL, INK, 5); c.poly([(1396, hz-270), (1430, hz-330), (1464, hz-270)], TILE, INK, 5)
    c.swell(hz, T.TT*.4, SEAC[kind][0], 3, 500)
    if ships:
        for i in range(ships): c.nao(420+i*620, 700, 400, bob=T.TT*1.3+i, furl=1, wind=T.TT)
    c.swell(716, T.TT*.6, SEAC[kind][1], 5, 380); c.crests(740, 800, T.TT*.5, 6)
    c.rect(-10, 810, W+10, H+10, CONC, INK, 6)
    for yy in (880, 950, 1020): c.line([(0, yy), (W, yy)], 3, (180, 172, 160), False)
    for i in range(12): c.line([(i*170+((i % 2)*60), 814), (i*170+((i % 2)*60), 880)], 3, (180, 172, 160), False)
    for x in (300, 1650): c.rect(x-18, 760, x+18, 816, (70, 62, 58), INK, 5, 6)
    return c
def table(c, x0=980, x1=1500, y=1010, h=150):
    c.line([(x0+40, y-h), (x0+40, y)], 16, TIMBER, False); c.line([(x1-40, y-h), (x1-40, y)], 16, TIMBER, False); c.rect(x0, y-h-30, x1, y-h, WOOD, INK, 6, 4)
def wmap(lonc=0.0, latc=8.0, sx=5.1, sy=6.6, note=True, grid=True):
    c = C(SEAM); P = c.worldmap(lonc, latc, sx, sy, grid=grid)
    if note: mapnote(c)
    return c, P
def mapnote(c, t="SKETCH MAP, NOT TO SCALE"):
    w = c.tw(t, 34)+40; c.rect(20, 1016, 20+w, 1070, SEAM, None, 0, 10); c.text(40, 1044, t, 34, (70, 100, 116), "lm")
def rpt(i):
    i = max(0.0, min(len(ROUTE)-1.0, i)); a = int(i); b = min(a+1, len(ROUTE)-1); q = i-a; return (lerp(ROUTE[a][0], ROUTE[b][0], q), lerp(ROUTE[a][1], ROUTE[b][1], q))
def route(c, P, upto, start=0, col=RED, w=8, ship=True, k=1.0, dots=False):
    """Draw the voyage on a map from route index start to upto (fractions allowed). The mark at the tip is the fleet."""
    pts = [rpt(start)]+[ROUTE[j] for j in range(int(start)+1, int(upto)+1)]+([rpt(upto)] if upto != int(upto) else [])
    for off in (0, 360):
        px = [P(lo+off, la) for lo, la in pts]
        if len(px) > 1 and max(p[0] for p in px) > -40 and min(p[0] for p in px) < W+40:
            if dots:
                for a, b in zip(px, px[1:]):
                    n = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1])/26))
                    for j in range(n): x = lerp(a[0], b[0], j/n); y = lerp(a[1], b[1], j/n); c.ell(x-5*k, y-5*k, x+5*k, y+5*k, col, None)
            else: c.line(px, (w+5)*k, INK, False); c.line(px, w*k, col, False)
    if ship:
        lo, la = rpt(upto)
        for off in (0, 360):
            x, y = P(lo+off, la)
            if -60 < x < W+60: c.naoicon(x, y+6*k, .9*k)
def place(c, P, name, t=None, dx=0, dy=-70, size=44, off=0, r=13, col=RED, **k):
    lo, la = SEAPLACES[name]; x, y = P(lo+off, la); q = app(("dot", name), .25); c.ell(x-r*q, y-r*q, x+r*q, y+r*q, col, INK, 5)
    if t: c.label(x+dx, y+dy, t, size, **k)
    return x, y
def sidp(c, x, y, h, pose="stand", ex="n", **k): return c.fig(x, y, h, pose, ex, "modern", **k)
def sailor(c, x, y, h=300, pose="stand", ex="n", coat="blue", flip=False, cap=True, **k):
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k)
    if cap and not k.get("rot"): c.hat(f, "cap", CAPS.get(coat, EARTH))
    return f
def beard(c, f, flip=False, col=(72, 54, 42)):
    u = f["u"]; x, y = f["head"]; d = -1 if flip else 1
    c.poly([(x-d*.5*u, y+.56*u), (x-d*.42*u, y+.9*u), (x+d*.12*u, y+1.34*u), (x+d*.62*u, y+.9*u), (x+d*.66*u, y+.56*u), (x+d*.5*u, y+.86*u), (x-d*.3*u, y+.86*u)], col, INK, max(3, u*.06))
def captain(c, x, y, h=340, pose="stand", ex="det", flip=False, **k):
    """Magellan as drawn here: dark coat, dark flat hat, beard. No portrait from life is being copied."""
    f = c.person(x, y, h, pose, ex, "broker", flip=flip, **k)
    if not k.get("rot"): beard(c, f, flip); c.hat(f, "bowler", (44, 40, 50))
    return f
def elcano(c, x, y, h=330, pose="stand", ex="n", flip=False, **k):
    f = c.person(x, y, h, pose, ex, "teal", flip=flip, **k); c.hat(f, "cap", (160, 56, 48)); return f
def book(c, x, y, k=1.0):
    c.poly([(x-70*k, y-40*k), (x, y-28*k), (x+70*k, y-40*k), (x+70*k, y+30*k), (x, y+42*k), (x-70*k, y+30*k)], PARCH, INK, max(3, 5*k)); c.line([(x, y-28*k), (x, y+42*k)], max(2, 4*k), INK, False)
    for i in range(3):
        for sgn in (-1, 1): c.line([(x+sgn*14*k, y-12*k+i*16*k), (x+sgn*56*k, y-18*k+i*16*k)], max(2, 3*k), INKP, False)
def piga(c, x, y, h=320, pose="write", ex="det", flip=False, bk=True, **k):
    """Antonio Pigafetta: green coat, green cap, always with his book."""
    f = c.person(x, y, h, pose, ex, "green", flip=flip, **k); c.hat(f, "cap", CAPS["green"])
    if bk: book(c, f["hand"][0]+(-30 if flip else 30), f["hand"][1]+10, h/420)
    return f
def islander(c, x, y, h=300, pose="stand", ex="n", coat="rose", flip=False, spear=False, back=False, **k):
    f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); u = f["u"]; hx, hy = f["head"]; c.line([(hx-.58*u, hy+.14*u), (hx+.58*u, hy+.14*u)], max(4, u*.13), MARI, False)
    if spear: sx, sy = f["hand0" if back else "hand"]; c.line([(sx, sy-h*.8), (sx, y)], max(4, h*.02), TIMBER, False); c.poly([(sx-h*.03, sy-h*.8), (sx, sy-h*.95), (sx+h*.03, sy-h*.8)], (150, 150, 156), INK, 4)
    return f
def portu(c, x, y, h=320, pose="stand", ex="n", flip=False, **k):
    f = c.person(x, y, h, pose, ex, "red", flip=flip, **k); c.hat(f, "bowler", SILVER); return f
def kingf(c, x, y, h=360, pose="stand", ex="n", coat="red", flip=False, **k): f = c.person(x, y, h, pose, ex, coat, flip=flip, **k); c.crown(f); return f
def icon(c, x, y, col=TEAL, k=1.0):
    c.line([(x, y+18*k), (x, y+52*k)], 22*k, INK, False); c.line([(x, y+18*k), (x, y+52*k)], 14*k, col, False); c.ell(x-20*k, y-24*k, x+20*k, y+14*k, PAPER, INK, max(3, 5*k))
def icons(c, x, y, n, per=10, col=TEAL, k=1.0, gx=62, gy=104, cols=None, shown=None):
    """n little people in rows of per, from the top left (x, y). cols(i) may give each its own colour; shown limits how many have arrived."""
    for i in range(n if shown is None else min(n, int(shown))): icon(c, x+(i % per)*gx*k, y+(i//per)*gy*k, cols(i) if cols else col, k)
def count(a, b, d=1.0, t0=.1, key=None): return int(round(lerp(a, b, app(key or ("n", a, b), d, t0))))
def sack(c, x, y, k=1.0, t=None): c.sack(x, y, k, (206, 178, 128)); c.clove(x, y-64*k, .5*k, 20); (c.text(x, y+44*k, t, 40*k) if t else None)
def vict(c, x, y, w=560, **k): return c.nao(x, y, w, bob=k.pop("bob", T.TT*1.6), wind=T.TT, **k)
def fleet(c, y, xs, w=300, lost=(), kind="day", flip=True, furl=0.0, calm=False, torn=False):
    for i, x in enumerate(xs):
        if i in lost: c.nao(x, y-(i % 2)*16, w, flip=flip, ghost=True)
        else: c.nao(x, y-(i % 2)*16, w, flip=flip, bob=T.TT*1.5+i*1.3, wind=T.TT+i, furl=furl, torn=torn)
    wash(c, y+10, kind, calm)

# ================= cold open =================
def strip(c, s, k=1.0):
    """The piece of hide: a stiff grey-brown strap clamped in Sid's teeth and gripped in his fist, bending as he tugs."""
    u = s["u"]; hx, hy = s["hand"]; mx, my = s["head"][0]+.1*u, s["head"][1]+.8*u; tug = 9*k*math.sin(T.TT*7); col = (186, 160, 128)
    pts = [(mx-.05*u, my), (lerp(mx, hx, .4), lerp(my, hy, .4)+.2*u+tug*.4), (hx, hy+tug), (hx+.5*u, hy+.2*u+tug)]
    c.line(pts, .4*u, INK, False); c.line(pts, .31*u, col, False)
    for q in (.2, .5, .8):
        for a, b in ((pts[1], pts[2]), (pts[2], pts[3])): x = lerp(a[0], b[0], q); y = lerp(a[1], b[1], q); c.ell(x-.03*u, y-.03*u, x+.03*u, y+.03*u, (110, 86, 62), None)
    c.ell(hx-.2*u, hy+tug-.2*u, hx+.2*u, hy+tug+.2*u, PAPER, INK, max(4, u*.06))
    c.line([(mx-.2*u, my-.02*u), (mx-.1*u, my-.08*u), (mx, my-.02*u), (mx+.1*u, my-.08*u), (mx+.2*u, my-.02*u)], max(4, u*.07), INK, False)
def chew(k):
    if k == 0:
        c = deck("grey", mast=0, sx=1500); s = sidp(c, 760, 1560, 880, "hold", "det"); strip(c, s); return c
    c = deck("grey", mast=1500); c.line([(1000, 170), (1920, 170)], 20, HULLD, False); c.rect(1040, 176, 1920, 226, SAILC, INK, 6, 20)
    for i, x in enumerate((1090, 1250, 1410, 1680, 1830)): c.rect(x-64, 150, x+64, 244, (186, 160, 128), INK, 6, 10) if i != 1 else c.rect(x-64, 150, x+64, 244, None, PAPER, 5, 10)
    c.barrel(1130, 1010, 1.0); s = sidp(c, 560, 1020, 400, "hold", "det"); strip(c, s); hx, hy = s["hand"]
    q = app("arr", .5, .3)
    if q > 0: arrow(c, 1220, 262, lerp(1220, hx+70, q), lerp(262, hy-40, q), PAPER, 9, 30)
    L(c, "OX HIDE. IT WAS PART OF THE SHIP.", 330, 620, 58); return c
def ratp(k):
    c = below(1250); c.barrel(250, 1010, 1.25); c.barrel(430, 1030, 1.0); c.barrel(1720, 1020, 1.2)
    if k == 0:
        x = lerp(2000, 900, T.ease(T.LP*1.2)); c.rat(x, 1010, 2.3, flip=True, t=T.TT if T.LP < .8 else 0); q = app("tag", .3, .5)
        if q > 0: c.line([(x+60, 840), (x+190, 640)], 5, PAPER, False); c.pricetag(x+290, 590, 1.7*q, "½ DUCAT", GOLD)
        L(c, "ONE RAT", 240, 620, 80); return c
    s = sidp(c, 900, 1030, 420, "shrug", "worry")
    for i in range(3): c.text(1150+i*110, 560-20*math.sin(T.TT*3+i), "?", 130, PAPER)
    L(c, "AND YOU CAN'T FIND ONE", 240, 720, 70, bg=MARI); return c
FX = [300, 640, 980, 1320, 1660]
def five(k):
    c = sea("day"); dx = -60*T.GP; g = app("gone", .6, .5) if k >= 1 else 0
    for i, x in enumerate(FX):
        if k >= 1 and i != 2 and g > .5: c.nao(x+dx, 800-(i % 2)*16, 270, flip=True, ghost=True)
        else: c.nao(x+dx, 800-(i % 2)*16, 270, flip=True, bob=T.TT*1.5+i*1.3, wind=T.TT+i, torn=k >= 1 and i == 2 and g > .5)
    wash(c, 810)
    if k == 0: L(c, "FIVE SHIPS LEAVE SPAIN", 210, size=76)
    if k == 1: L(c, "ONE FINISHES", 210, size=84, bg=MARI)
    if k == 2:
        dimc(c, 150*app("dim", .3)); c.text(520, 500, str(count(0, 18, .7, .1, "c18")), 420, PAPER); c.text(1480, 440, "OF THE", 110, PAPER); c.text(1480, 570, "CREW", 150, PAPER)
    return c
def q18(k):
    c = C(); icons(c, 200, 300, 18, 9, TEAL, 1.9, 66, 124, shown=18*app("row", .8)); s = sidp(c, 1560, 1010, 420, "self", "worry"); c.text(1560, 330, "?", 230*(.8+.2*app("qm", .3)), RED)
    if k: L(c, "ARE YOU ONE OF THE 18?", 850, 730, 86, bg=MARI)
    return c

# ================= who you are =================
def intro(k=0):
    c = C(); s = c.fig(W/2, 900-(1-T.ease(T.LT/0.3))*900, 520, "drop" if T.LT < .5 else "self", "wow" if T.LT < .5 else "smile", "modern"); c.marker(s["head"][0]+20, s["head"][1]-110, 46)
    if T.LT > .6: L(c, "YOU", 160, 1400, 120)
    return c
def signon(k=0):
    c = quay("day", ships=1); table(c, 1040, 1560, 1030, 170); c.roll(1180, 770, 1420, 836, 14); f = c.person(1700, 1030, 330, "hold", "n", "slate", flip=True); c.coif(f)
    q = T.ease(T.LP*1.3); s = sidp(c, lerp(380, 880, q), 1030, 350, ("walk" if step() else "stand") if q < .97 else "write", "smile")
    if q > .97: c.line([(s["hand"][0], s["hand"][1]), (s["hand"][0]+30, s["hand"][1]-50)], 6, INK, False)
    hud(c, "SEVILLE, 1519"); L(c, "A SAILOR. YOU'VE JUST SIGNED ON.", 210, 760, 62); return c
def madeup(k=0):
    c = C(); c.card("YOU ARE MADE UP.", 150, "THE VOYAGE ISN'T."); return c
def pigaf(k):
    c = deck("day", mast=1620); c.barrel(1130, 1010, 1.15); p = piga(c, 900, 1020, 400, "write", "det"); c.line([(p["hand"][0]+40, p["hand"][1]-20), (p["hand"][0]+70+6*math.sin(T.TT*9), p["hand"][1]-90)], 6, INK, False)
    L(c, "ANTONIO PIGAFETTA", 210, 780, 76)
    if k: L(c, "HE SAILED WITH IT, AND WROTE IT DOWN", 330, 860, 54, bg=MARI)
    return c
def qsea(shown, done=0, hidden=None):
    c = sea("day", sx=300); vict(c, 470, 800, 560, flip=True); wash(c, 812); return Q(c, shown, done, hidden)
def hiddenq(k, done=0):
    c = C(); c.questlog(ROWS, 4, done, None, x=545, y=200); return c
def nocap(k=0):
    c = deck("day", mast=300, sx=1720); captain(c, 960, 1020, 420, "shrug", "n"); c.text(1330, 430, "?", 220, RED); L(c, "NOT EVEN THE CAPTAIN", 210, 1100, 70); return c

# ================= why go: cloves =================
def why(k):
    c = C((250, 238, 214)); a = 8*math.sin(T.TT*1.4)
    if k == 0: sidp(c, 620, 1000, 440, "shrug", "n"); c.text(1250, 520, "WHY GO\nAT ALL?", 190, NAVY); return c
    c.cloves(600, 620, 9, 1.25, 3); c.text(1330, 520, "CLOVES", 230, CLOVEC); return c
def molmap(k):
    c, P = wmap(); place(c, P, "SEVILLE", "SEVILLE", -150, -70); x, y = place(c, P, "TIDORE", "THE MOLUCCAS", -230, 110)
    for i in range(3): r = 30+26*((T.TT*.8+i/3) % 1); c.ell(x-r, y-r, x+r, y+r, None, RED, 4)
    if k: L(c, "THE SPICE ISLANDS", 880, 1560, 62, bg=MARI)
    return c
def price(k):
    c = C((250, 238, 214)); L(c, "BY ONE ACCOUNT", 120, 960, 54, bg=MARI); c.text(960, 250, "100 POUNDS OF CLOVES", 80)
    for side, x in ((0, 500), (1, 1420)):
        if k < side+1: continue
        c.rect(x-380, 330, x+380, 990, PAPER, INK, 7, 22); c.text(x, 400, ("OUT THERE", "IN SEVILLE")[side], 76, CLOVEC if side == 0 else NAVY); sack(c, x-220, 700, 1.25*app(("sk", side), .3))
        if side == 0: c.ducat(x+150, 620, 86, True); c.text(x+120, 800, "ABOUT HALF\nA DUCAT", 60)
        elif k >= 3:
            n = count(0, 42, 1.2, .1, "c42")
            for i in range(n): c.ducat(x-30+(i % 7)*56, 500+(i//7)*56, 25)
            c.text(x+138, 880, f"{n} DUCATS", 76, RED)
    if k == 0: sack(c, 960, 760, 2.0)
    return c
def road(k):
    if k == 1:
        c = quay("day"); m = captain(c, 800, 1030, 420, "point", "det"); L(c, "FERDINAND MAGELLAN", 210, 800, 76); return c
    c, P = wmap(); x0, y0 = place(c, P, "SEVILLE"); x1, y1 = place(c, P, "TIDORE", "THE SPICE ISLANDS", -40, 110, 44)
    if k == 0:
        for (x, y) in ((x0, y0), (x1, y1)):
            for i in range(3): r = 26+30*((T.TT*.8+i/3) % 1); c.ell(x-r, y-r, x+r, y+r, None, RED, 4)
        c.text(1270, 720, "?", 220*(.8+.2*app("rq", .3)), RED); L(c, "SPAIN WANTS ITS OWN ROAD THERE", 900, 660, 64); return c
    q = T.ease(T.LP*1.2); arrow(c, x0-20, y0+10, lerp(x0-20, 610, q), lerp(y0+10, 440, q), RED, 14, 44); L(c, "HIS PLAN: SAIL WEST", 900, 620, 70, bg=MARI); return c
def port(k):
    c = C((238, 226, 204)); c.rect(0, 900, W, H, (206, 186, 150), None); c.line([(0, 900), (W, 900)], 6, INK, False)
    if k == 0:
        m = captain(c, 800, 1010, 460, "self", "n"); chip(c, 1250, 420, "PORTUGUESE", NAVY, 70); c.line([(1010, 430), (900, 470)], 6, INK, False); return c
    kg = kingf(c, 1400, 1010, 440, "point", "angry", "green", flip=True); c.bubble(1080, 470, "NO.", 150, (190, 90)); q = T.ease(T.LP*1.1); captain(c, lerp(820, 380, q), 1010, 400, "walk" if step() and q < .97 else "stand", "sad", flip=True)
    L(c, "HIS OWN KING TURNED HIM DOWN", 170, 620, 60); return c
def recruit(k):
    c = quay("day", ships=1); table(c, 500, 1000, 1030, 170); c.roll(640, 770, 860, 836, 14); captain(c, 300, 1030, 360, "hold", "worry")
    for i, x in enumerate((1180, 1400, 1620)): sailor(c, x+T.GP*90, 1030+(i % 2)*16, 300, "walk" if step() else "stand", "worry", CREW[i], flip=False)
    c.label(1150, 250, "\n".join(("HIGH RISK", "LOW PAY", "A PORTUGUESE CAPTAIN")[:k+1]), 52)
    hud(c, "SEVILLE, 1519"); return c
def foreign(k):
    c = C(); n = 30; sp = 19; icons(c, 200, 380, n, 10, k=1.7, gx=66, gy=120, cols=lambda i: TEAL if i < sp else MARI)
    if k == 0: L(c, "SO FOREIGNERS ARE LET IN", 200, 960, 76); return c
    icon(c, 1400, 470, TEAL, 1.7); c.text(1470, 500, "SPANIARDS", 60, INK, "lm"); icon(c, 1400, 710, MARI, 1.7); c.text(1470, 740, "FROM\nELSEWHERE", 60, INK, "lm")
    L(c, "SPANIARDS: UNDER TWO THIRDS OF THE CREW", 200, 960, 60, bg=MARI); return c
def twoy(k=0):
    c = C((238, 226, 204)); q = app("p2", .3, .5); c.calpage(660, 580, 1.5, "YEAR", "1", c=TEAL)
    if q > 0: c.calpage(1260, 580, 1.5*q, "YEAR", "2", c=TEAL)
    L(c, "EXPECTED: TWO YEARS", 190, 960, 80); return c
def vic(k):
    c = sea("day", sun=False); v = vict(c, 760, 800, 740, flip=True); wash(c, 818, amp=9); c.label(1540, 520, "YOUR SHIP:\nTHE VICTORIA", 64)
    if k == 1: c.label(1540, 740, "45 MEN ON\nTHE CREW LIST", 54, bg=MARI)
    if k == 2:
        q = app("dim", .5); x0, x1 = 400, 1130; xm = (x0+x1)/2
        c.line([(lerp(xm, x0, q), 880), (lerp(xm, x1, q), 880)], 9, PAPER, False)
        if q > .9: c.line([(x0, 850), (x0, 910)], 9, PAPER, False); c.line([(x1, 850), (x1, 910)], 9, PAPER, False)
        c.label(xm, 940, "HULL: 60-ODD FEET", 54)
    return c
def depart(k):
    if k == 0:
        c = sea("day", sx=300); coast(c, 548, 1250, W+40, 150, (190, 196, 150), 2); c.rect(1560, 440, 1620, 548, RWALL, INK, 5); c.poly([(1550, 440), (1590, 396), (1630, 440)], TILE, INK, 5)
        for i, x in enumerate((1500, 1210, 930, 650, 370)): c.nao(x-T.GP*150, 790-(i % 2)*18, 290, flip=True, bob=T.TT*1.5+i*1.3, wind=T.TT+i)
        wash(c, 802); hud(c, "20 SEPT 1519", 5); L(c, "5 SHIPS. ABOUT 240 MEN.", 210, 1060, 70); return c
    c, P = wmap(-34, 20, 13, 16); place(c, P, "SANLUCAR", "SANLÚCAR", 170, -60); route(c, P, lerp(0, 2.2, T.ease(T.LP)), k=1.4); hud(c, "20 SEPT 1519", 5); L(c, "INTO THE ATLANTIC", 880, 560, 70, bg=MARI); return c
def heads(k):
    c = C((238, 226, 204)); L(c, "THE HEADCOUNTS DON'T AGREE", 150, 960, 70)
    for i, (x, who, n) in enumerate(((560, "PIGAFETTA", "237"), (1360, "SOME HISTORIES", "270"))):
        c.rect(x-330, 300, x+330, 940, PAPER, INK, 7, 22); c.text(x, 390, who, 70, CAPS["green"] if i == 0 else NAVY)
        if k > i: c.text(x, 640, n, 300*(.8+.2*app(("hn", i), .3)), RED); c.text(x, 850, "MEN", 70)
        else: c.text(x, 640, "?", 300, GREY)
    return c

# ================= quest one: the way through =================
def qcard(n, t): return card("QUEST "+n, t)
def shipsleft(n, t, sub=None):
    c = C((238, 226, 204))
    for i in range(5):
        x = 360+i*300; gone = i >= n; new = i == n and app(("sl", n), .4, .3) < 1
        c.naoicon(x, 640, 3.6, lost=gone and not new)
    L(c, t, 250, 960, 90, bg=MARI)
    if sub: L(c, sub, 870, 960, 60)
    return c
def along(pts, q):
    q = max(0.0, min(1.0, q)); ds = [math.hypot(b[0]-a[0], b[1]-a[1]) for a, b in zip(pts, pts[1:])]; t = q*sum(ds)
    for (a, b), d in zip(zip(pts, pts[1:]), ds):
        if t <= d: return (lerp(a[0], b[0], t/d), lerp(a[1], b[1], t/d))
        t -= d
    return pts[-1]
SPATH = [(1800, 345), (1560, 400), (1400, 520), (1220, 560), (1060, 500), (900, 560), (760, 700), (560, 740), (380, 660), (120, 700)]
def straitmap(prog=0.0, west="?"):
    """The strait as a diagram: land above and below, the channel winding between, east on the right. A sketch and labelled as one."""
    c = C(SEAM)
    north = [(-10, -10), (W+10, -10), (W+10, 250), (1700, 230), (1540, 310), (1380, 430), (1220, 470), (1060, 400), (900, 450), (740, 600), (560, 640), (380, 560), (160, 600), (-10, 560)]
    south = [(-10, H+10), (W+10, H+10), (W+10, 470), (1780, 430), (1600, 500), (1440, 620), (1240, 660), (1060, 610), (930, 670), (800, 810), (560, 850), (380, 770), (180, 810), (-10, 800)]
    c.poly(north, (214, 220, 178), INK, 7); c.poly(south, (198, 208, 170), INK, 7)
    for i in range(int(60*prog)+1): x, y = along(SPATH, i/60*1.0); c.ell(x-6, y-6, x+6, y+6, RED, None)
    x, y = along(SPATH, prog); c.naoicon(x, y+8, 1.5, flip=True)
    c.text(1740, 300, "ATLANTIC", 60, (50, 84, 104)); c.text(60, 640, west, 120 if west == "?" else 60, (50, 84, 104), "lm"); mapnote(c, "SKETCH, NOT TO SCALE")
    return c
def channel(kind="cold", ships=4, lost=(), fires=False, sail=True, w=230):
    """Inside the strait, looking west: cliffs on both sides (the southern shore is on the left), the fleet in the channel."""
    c = sea(kind, hz=524, sun=False); rk = ROCKC if kind != "night" else (44, 46, 62); rk2 = (150, 146, 150) if kind != "night" else (58, 60, 78)
    c.poly([(-10, 240), (170, 220), (330, 320), (520, 410), (700, 496), (770, 528), (-10, 528)], rk, INK, 7); c.poly([(W+10, 190), (1720, 220), (1560, 330), (1390, 420), (1230, 496), (1150, 528), (W+10, 528)], rk, INK, 7)
    for x0, y0, x1, y1 in ((60, 300, 150, 520), (300, 360, 360, 520), (1800, 280, 1730, 520), (1540, 380, 1500, 520)): c.line([(x0, y0), (x1, y1)], 4, rk2, False)
    if kind in ("cold", "grey"):
        for pts in ([(100, 232), (170, 220), (250, 270), (180, 262)], [(1720, 220), (1830, 204), (1770, 250), (1650, 268)]): c.poly(pts, WHITE, INK, 4)
    if fires:
        for i, (x, y) in enumerate(((70, 262), (250, 292), (400, 372), (560, 446), (690, 506), (150, 420), (360, 480))):
            fl = 1+.1*math.sin(T.TT*11+i*2); c.da.ellipse([(x-46)*S, (y-80)*S, (x+46)*S, (y+14)*S], fill=(255, 190, 80, 90)); life._fire(c, x, y, (.42+.1*(i % 3))*fl)
    xs = [1420, 1080, 760, 440][:ships]
    for i, x in enumerate(xs):
        if i in lost: c.nao(x, 780-(i % 2)*30, w, flip=True, ghost=True)
        else: c.nao(x-(T.GP*70 if sail else 0), 780-(i % 2)*30, w, flip=True, bob=T.TT*1.5+i*1.3, wind=T.TT+i, furl=0 if sail else 1)
    wash(c, 790, kind)
    c.poly([(-10, H+10), (-10, 900), (140, 930), (300, 1010), (380, H+10)], rk, INK, 7); c.poly([(W+10, H+10), (W+10, 880), (1790, 920), (1640, 1010), (1570, H+10)], rk, INK, 7)
    return c
def rio(k):
    if k == 0:
        c, P = wmap(-34, 6, 12, 14.5); place(c, P, "SANLUCAR"); route(c, P, lerp(2.2, 5, T.ease(T.LP)), k=1.3); hud(c, "DEC 1519", 5); L(c, "ACROSS THE ATLANTIC", 900, 1400, 62); return c
    c = sea("day", sx=300); coast(c, 548, -40, 900, 210, (120, 170, 110), 1); c.poly([(1180, 548), (1230, 380), (1300, 300), (1380, 330), (1430, 548)], (120, 170, 110), INK, 6); coast(c, 548, 1400, W+40, 120, (130, 178, 116), 4)
    fleet(c, 760, (360, 680, 1000, 1320, 1640), 270, furl=1, calm=True); beach(c, 900); c.palm(160, 1000, 1.1, T.TT); c.palm(1790, 1010, 1.2, T.TT+1, flip=True)
    hud(c, "DEC 1519", 5); L(c, "THE BAY THAT WILL BE RIO DE JANEIRO", 210, 1140, 56); return c
def plate(k):
    if k == 0:
        c, P = wmap(-46, -26, 20, 24); route(c, P, lerp(5, 7, T.ease(T.LP)), 4.2, k=1.5); hud(c, None, 5); L(c, "THEN SOUTH", 210, 1380, 80); return c
    c = sea("day", sx=300, clouds=False); muddy = k == 2; coast(c, 548, -40, 560 if not muddy else 700, 90, (150, 188, 122), 2); coast(c, 548, 1360 if not muddy else 1220, W+40, 90, (150, 188, 122), 6)
    for i, x in enumerate((1400, 1180, 960, 740, 520)): c.nao(x, 740-(i % 2)*16, 190, flip=True, bob=T.TT*1.5+i, wind=T.TT+i)
    wash(c, 748, n=10)
    if muddy: c.da.rectangle([0, 548*S, W*S, H*S], fill=(150, 110, 60, int(120*app("mud", .5)))); c.redx(960, 500, 54, 18)
    hud(c, None, 5); L(c, "ONE HUGE RIVER MOUTH. THE GAP?" if k == 1 else "IT'S A RIVER.", 240, 960, 66 if k == 1 else 90, bg=MARI if k == 1 else PAPER); return c
def julian(k):
    c = sea("cold"); coast(c, 548, -40, W+40, 110, (176, 170, 156), 5, rock=True); fleet(c, 760, (360, 680, 1000, 1320, 1640), 270, furl=1, kind="cold", calm=True); beach(c, 900, (200, 196, 186)); snow(c)
    hud(c, "31 MAR 1520", 5); L(c, "PORT ST JULIAN", 210, 1180, 76)
    if k: L(c, "THE FLEET STOPS FOR THE WINTER", 330, 1180, 56, bg=MARI)
    return c
def mutiny(k):
    c = sea("night"); coast(c, 548, -40, W+40, 110, (40, 44, 60), 5, rock=True); fleet(c, 760, (360, 680, 1000, 1320, 1640), 270, furl=1, kind="night", calm=True)
    for i, (x0, x1) in enumerate(((520, 840), (1480, 1160))):
        x = lerp(x0, x1, T.ease(T.GP)); c.rowboat(x, 900+i*50, .9, flip=x1 < x0, bob=T.TT*4, n=3); c.da.ellipse([(x-90)*S, (790+i*50)*S, (x+90)*S, (950+i*50)*S], fill=(255, 210, 120, 50)); c.rect(x-10, 836+i*50, x+10, 866+i*50, (250, 216, 130), INK, 4, 4)
    hud(c, "1520", 5); L(c, "MIDNIGHT", 210, 1180, 80)
    if k: c.label(1180, 330, "THE SPANISH CAPTAINS MUTINY", 60, PAPER, RED)
    return c
def sword(c, f, flip=False):
    hx, hy = f["hand"]; d = -1 if flip else 1; u = f["u"]; c.line([(hx, hy), (hx+d*1.5*u, hy-1.1*u)], max(5, u*.09), INK, False); c.line([(hx, hy), (hx+d*1.5*u, hy-1.1*u)], max(3, u*.05), SILVER, False); c.line([(hx-d*.14*u, hy-.2*u), (hx+d*.2*u, hy+.08*u)], max(5, u*.1), INK, False)
def turns(k):
    c = deck("night", mast=1740, sx=260)
    for i, (x, fl) in enumerate(((280, False), (1180, True), (1480, True))): f = sailor(c, x, 1030, 350, "hold", "angry", ("slate", "brown", "rose")[i], flip=fl); sword(c, f, fl)
    sidp(c, 800, 1030, 380, "shrug" if k else "stand", "worry" if k else "wow"); hud(c, "1520", 5)
    L(c, "YOUR SHIP TURNS" if k == 0 else "NOBODY ASKS YOU", 210, 1080, 76, bg=PAPER if k == 0 else MARI); return c
def wins(k):
    if k == 0:
        c = deck("dawn", mast=1620, sx=260); m = captain(c, 860, 1030, 430, "hold", "det"); sword(c, m); L(c, "MAGELLAN WINS", 210, 1040, 84); hud(c, "1520", 5); return c
    c = C((238, 226, 204))
    if k == 1:
        book(c, 600, 600, 3.0); book(c, 1320, 600, 3.0); c.text(960, 590, "≠", 230, RED); L(c, "THE ACCOUNTS DIFFER ON THE DETAILS", 220, 960, 64, bg=MARI); return c
    L(c, "ONE COMMON VERSION", 150, 960, 64, bg=MARI)
    for i, (x, a, b) in enumerate(((560, "YOUR CAPTAIN", "KILLED IN\nTHE FIGHTING"), (1360, "ANOTHER CAPTAIN", "EXECUTED"))):
        if k-2 < i: continue
        c.rect(x-330, 280, x+330, 960, PAPER, INK, 7, 22); c.text(x, 350, a, 62); icon(c, x, 540, (150, 144, 136), 3.6); c.redx(x, 560, 110, 20); c.text(x, 830, b, 64, RED)
    return c
def maroon(k):
    c = sea("cold"); d = 400*T.GP if k else 0; sc = 1-.25*T.GP if k else 1
    for i, x in enumerate((980, 720, 460, 200)): c.nao(x-d*.5, 640-(i % 2)*10, 170*sc, flip=True, bob=T.TT*1.5+i, wind=T.TT+i)
    wash(c, 648, "cold", n=8); beach(c, 860, (200, 196, 186)); f = c.person(1240, 1010, 300, "wave" if k == 0 else "stand", "worry", "red", flip=True); c.hat(f, "bowler", (60, 50, 60)); g = c.person(1480, 1020, 290, "stand", "sad", "brown", flip=True); c.tonsure(g)
    L(c, "LEFT ON THE SHORE: A NOBLEMAN AND A PRIEST", 210, 1060, 52); return c
def pardon(k):
    c = deck("day", mast=0); captain(c, 260, 1030, 400, "point", "det")
    for i, x in enumerate((700, 940, 1420, 1660)): sailor(c, x, 1030, 330, "stand", "worry", CREW[i], flip=True)
    e = elcano(c, 1180, 1030, 350, "stand", "worry" if k == 0 else "n", flip=True)
    if k == 0: L(c, "THE OTHER MUTINEERS ARE PARDONED", 210, 1020, 64); return c
    c.marker(e["head"][0], e["head"][1]-90, 34); L(c, "JUAN SEBASTIÁN ELCANO", 180, 1100, 76)
    if k == 2: L(c, "REMEMBER THAT NAME", 300, 1100, 60, bg=MARI)
    return c
def stay(k=0):
    c = C((226, 232, 236)); n = min(5, int(T.LP*6.5)+1)
    for i, m in enumerate(("APR", "MAY", "JUN", "JUL", "AUG")[:n]): c.calpage(330+i*315, 600, 1.1, "1520", m, c=SLATE)
    snow(c, 30); L(c, "ABOUT FIVE MONTHS AT PORT ST JULIAN", 240, 960, 64); return c
def giant(k):
    c = sea("cold", hz=600, sx=300); coast(c, 608, -40, W+40, 100, (176, 170, 156), 3, rock=True); wash(c, 640, "cold", n=5); beach(c, 780, (200, 196, 186))
    g = c.person(900, 1040, 620, "stand", "n", "brown"); hip = 1040-1.3*g["u"]
    for i, x in enumerate((500, 1260)): sailor(c, x, 1040, 222, "stand", "wow", CREW[i], flip=i == 1)
    piga(c, 1640, 1040, 222, "write", "det", flip=True)
    if k >= 1:
        for x in range(380, 1420, 44): c.line([(x, hip), (x+22, hip)], 6, RED, False)
        c.label(1500, 520, "THE SAILORS REACH\nHIS WAIST", 46)
    L(c, "PIGAFETTA DESCRIBES A VERY TALL MAN" if k < 2 else "HIS MEASUREMENT, NOT OURS", 150, 1100, 60, bg=PAPER if k < 2 else MARI); return c
def wreck(k):
    if k == 0:
        c = sea("storm", sun=False); coast(c, 560, 1300, W+40, 260, (70, 70, 84), 3, rock=True); c.nao(820+20*math.sin(T.TT*2), 800, 480, flip=True, bob=T.TT*5, tilt=14+6*math.sin(T.TT*2.4), torn=True, wind=T.TT*3)
        wash(c, 800, "storm", amp=26); c.poly([(1260, H+10), (1380, 860), (1520, 800), (1700, 850), (W+10, 780), (W+10, H+10)], (70, 70, 84), INK, 7); rain(c); hud(c, "1520", 5); L(c, "THE SANTIAGO, SCOUTING SOUTH", 210, 1120, 64); return c
    if k == 1:
        c = sea("grey", sun=False); c.poly([(1180, 720), (1300, 560), (1500, 600), (1700, 540), (1840, 720)], (70, 70, 84), INK, 6); c.nao(1420, 700, 520, tilt=-30, torn=True, furl=.4, flag=None); wash(c, 716, "grey"); beach(c, 860, (190, 186, 176))
        for i, x in enumerate((240, 450, 660, 870)): sailor(c, x, 1030, 310, ("stand", "shrug", "stand", "stand")[i], ("worry", "n", "sad", "worry")[i], CREW[i])
        hud(c, "1520", 4); L(c, "WRECKED. THE CREW SURVIVES.", 210, 1060, 66); return c
    return shipsleft(4, "FOUR SHIPS")
def again(k=0):
    c = sea("cold", sx=300); coast(c, 548, 1100, W+40, 120, (176, 170, 156), 5, rock=True); fleet(c, 780, [x-T.GP*120 for x in (520, 880, 1240, 1600)], 290, kind="cold"); hud(c, "LATE AUG 1520", 4); L(c, "YOU SAIL AGAIN", 210, 1100, 76); return c
def cape(k):
    if k == 0:
        c, P = wmap(-62, -47, 42, 50); route(c, P, lerp(9, 10, T.ease(T.LP)), 8.4, k=1.6); x, y = P(-68.4, -52.3); c.label(x+470, y-60, "YOU ROUND A CAPE", 60); hud(c, "21 OCT 1520", 4); return c
    c = straitmap(lerp(0, .09, T.ease(T.LP))); hud(c, "21 OCT 1520", 4); L(c, "AND THE COAST OPENS", 900, 1300, 70, bg=MARI); return c
def notriver(k=0):
    c = channel("cold", 4); hud(c, "OCT 1520", 4); L(c, "THIS ONE ISN'T A RIVER", 210, 1100, 76, bg=MARI); return c
def strait(k):
    if k == 2:
        c = channel("storm", 4); rain(c); hud(c, "OCT–NOV 1520", 4); L(c, "ROCK, STORMS AND CURRENTS", 210, 1120, 70); return c
    q = T.ease(T.LP); c = straitmap(lerp(.09, .5, q) if k == 0 else lerp(.5, .82, q)); hud(c, "OCT 1520" if k == 0 else "OCT–NOV 1520", 4)
    if k == 0: c.rect(1180, 760, 1800, 990, PAPER, INK, 7, 22); c.text(1340, 870, str(count(1, 38, 1.4, .1, "c38")), 170, RED); c.text(1600, 880, "DAYS", 110)
    else: c.rect(1100, 760, 1820, 990, PAPER, INK, 7, 22); c.text(1460, 830, "MORE THAN", 60); c.text(1460, 920, "300 MILES", 110, RED)
    return c
def fires(k):
    c = channel("night", 4, fires=True, sail=False); hud(c, "OCT–NOV 1520", 4)
    if k == 0: L(c, "FIRES ON THE SOUTHERN SHORE", 210, 1160, 62)
    if k == 1: L(c, "THE LAND OF FIRE", 210, 1160, 80)
    if k == 2: L(c, "TIERRA DEL FUEGO", 210, 1160, 92, bg=MARI)
    return c
def vanish(k):
    if k == 0:
        g = app("sa", .6, .6) > .5; c = channel("cold", 4, lost=(0,) if g else ()); hud(c, "OCT–NOV 1520", 3 if g else 4); L(c, "THE SAN ANTONIO VANISHES", 210, 1100, 70); return c
    if k == 1:
        c = channel("night", 4, lost=(0,), sail=False); hud(c, "OCT–NOV 1520", 3)
        for i, x in enumerate((1080, 760, 440)): y = 780-(i % 2)*30-150; c.da.ellipse([(x-34)*S, (y-34)*S, (x+34)*S, (y+34)*S], fill=(255, 220, 130, 120)); c.rect(x-8, y-10, x+8, y+12, (250, 216, 130), INK, 3, 3)
        c.text(1420, 620, "?", 160, PAPER); L(c, "THE FLEET THINKS SHE'S LOST", 210, 1100, 66); return c
    c, P = wmap(-40, -4, 9.5, 10.4); back = [(-71, -53.4), (-68, -52.3), (-60, -46), (-48, -36), (-38, -28), (-28, -10), (-25, 10), (-20, 28), (-6.4, 36.8)]; q = T.ease(T.LP); n = max(2, int(q*(len(back)-1))+1); px = [P(*p) for p in back[:n]]
    for a, b in zip(px, px[1:]):
        m = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1])/30))
        for j in range(m): x = lerp(a[0], b[0], j/m); y = lerp(a[1], b[1], j/m); c.ell(x-7, y-7, x+7, y+7, NAVY, None)
    c.naoicon(px[-1][0], px[-1][1]+6, 1.4); place(c, P, "SANLUCAR", "SPAIN", 190, -30); hud(c, "OCT–NOV 1520", 3); L(c, "SHE HAS TURNED ROUND AND GONE HOME", 880, 1330, 54, bg=MARI); return c
def out(k):
    if k == 0:
        c = sea("gold", calm=True, sx=420); c.poly([(W+10, 250), (1760, 270), (1600, 380), (1470, 470), (1400, 544), (W+10, 544)], ROCKC, INK, 7)
        for i, x in enumerate((1240, 900, 560)): c.nao(x-T.GP*160, 780-(i % 2)*20, 300, flip=True, bob=T.TT*1.2+i, wind=T.TT+i)
        wash(c, 790, "gold", calm=True); hud(c, "28 NOV 1520", 3); L(c, "THREE SHIPS COME OUT THE FAR END", 210, 1100, 60); return c
    c = deck("gold", mast=1640, sx=300); m = captain(c, 900, 1030, 460, "stand", "sad"); u = m["u"]; hx, hy = m["head"]; ty = hy+.6*u+(T.TT*60) % (.5*u)
    c.ell(hx-.3*u-9, ty-4, hx-.3*u+9, ty+22, WATER, INK, 4); hud(c, "28 NOV 1520", 3); L(c, "MAGELLAN, THEY SAY, CRIED", 210, 1100, 66); return c
def qdone(n, kind="day", ships=3, hidden=None):
    c = sea(kind, sx=300, calm=kind == "gold"); xs = (470,) if ships == 1 else ((300, 640) if ships == 2 else (220, 500, 780))
    for i, x in enumerate(xs): c.nao(x, 800-(i % 2)*20, 520 if ships == 1 else (330 if ships == 2 else 270), flip=True, bob=T.TT*1.5+i, wind=T.TT+i)
    wash(c, 812, kind, calm=kind == "gold"); return Q(c, 4, n, hidden)

# ================= quest two: the other side =================
def pacific(k):
    c = sea("day", calm=True); fleet(c, 780, [x-T.GP*80 for x in (620, 1000, 1380)], 300, calm=True); hud(c, "NOV 1520", 3)
    L(c, "THE WATER IS CALM" if k == 0 else "SO MAGELLAN CALLS IT THE PACIFIC", 210, 1120, 70 if k == 0 else 60, bg=PAPER if k == 0 else MARI); return c
def nofood(k):
    c, P = wmap(-140, -8, 8.2, 10); a, b = ((12, 15), (15, 18), (18, 19.7))[k]; route(c, P, lerp(a, b, T.ease(T.LP)), 9, k=1.3); hud(c, ("DEC 1520", "JAN 1521", "FEB 1521")[k], 3)
    if k == 0: L(c, "NO FRESH FOOD", 240, 700, 80)
    if k == 1: L(c, "MORE THAN THREE MONTHS", 240, 700, 70)
    if k == 2: L(c, "PIGAFETTA: 3 MONTHS AND 20 DAYS", 180, 1240, 58, bg=MARI)
    return c
def board(col=DECKC):
    """A table top seen from the side and a little above: the top, its front edge, the dark under it."""
    c = C((70, 54, 44)); c.rect(-10, 180, W+10, 900, col, INK, 7)
    for yy in (360, 540, 720): c.line([(0, yy), (W, yy)], 5, DECKL, False)
    c.rect(-10, 900, W+10, 980, DECKL, INK, 7)
    return c
def bisc(k):
    c = board(); c.biscuit(960, 520, 3.0, min(1, T.LP*1.4) if k == 0 else 1)
    if k >= 1:
        for i in range(8): c.worm(480+i*120, 660+34*math.sin(i*2.1)+(i % 2)*60, 1.8, T.TT+i)
    if k == 2:
        c.rat(1380, 880, 1.7, flip=True, t=T.TT)
        for i in range(4): x = 700+i*170; y0 = 520-((T.TT*70+i*40) % 160); c.line([(x, y0), (x+16, y0-40), (x-10, y0-80), (x+10, y0-120)], 7, (196, 190, 90), False)
    L(c, ("THE BISCUIT HAS TURNED TO POWDER", "CRAWLING WITH WORMS", "IT STINKS OF RAT URINE")[k], 110, 960, 60, bg=PAPER if k < 2 else MARI); return c
def water(k=0):
    c = below(1400); c.barrel(1500, 1030, 1.7, lid=False); c.ell(1500-88, 1030-290, 1500+88, 1030-240, (214, 196, 70), INK, 6); s = sidp(c, 800, 1030, 420, "hold", "worry"); hx, hy = s["hand"]
    c.poly([(hx-6, hy-70), (hx+90, hy-70), (hx+78, hy+30), (hx+6, hy+30)], WOOD, INK, 6); c.ell(hx-6, hy-84, hx+90, hy-56, (224, 206, 76), INK, 5); L(c, "THE WATER IS YELLOW", 240, 760, 76); return c
def sawdust(k=0):
    c = below(500); s = sidp(c, 760, 1030, 420, "hold", "sad"); hx, hy = s["hand"]; c.bowl(hx+70, hy-10, 1.2); c.puff([(hx+30, hy-24, 30), (hx+70, hy-44, 40), (hx+112, hy-24, 30)], (226, 200, 150), INK, 5)
    for i in range(14): c.ell(hx+10+(i*37) % 120, hy-60+(i*23) % 44, hx+16+(i*37) % 120, hy-54+(i*23) % 44, (170, 130, 84), None)
    L(c, "YOU EAT SAWDUST", 240, 1180, 80); return c
def hides(k):
    if k == 0:
        c = deck("grey", mast=1500); c.line([(1000, 170), (1920, 170)], 20, HULLD, False); c.rect(1040, 176, 1920, 226, SAILC, INK, 6, 20); n = 5-min(3, int(T.LP*4))
        for i, x in enumerate((1090, 1250, 1410, 1680, 1830)): c.rect(x-64, 150, x+64, 244, (186, 160, 128) if i < n else None, INK if i < n else PAPER, 6, 10)
        f = sidp(c, 760, 1030, 380, "hold", "sad"); c.hide(f["hand"][0]+40, f["hand"][1]+10, .7, (186, 160, 128)); L(c, "THE OX HIDES OFF THE MAIN YARD", 330, 620, 58); return c
    if k == 1:
        c = sea("grey", sun=False); v = c.nao(1250, 760, 620, bob=T.TT*1.4, wind=T.TT); bx, by = v["boat"]; hx = 420+30*math.sin(T.TT*1.3); wash(c, 790, "grey"); c.line([(bx+60, by-120), (lerp(bx, hx, .5), 830), (hx+110, 880)], 6, PAPER, False); c.hide(hx, 900, 1.0, (186, 160, 128)); L(c, "FOUR OR FIVE DAYS IN THE SEA, TO SOFTEN THEM", 210, 960, 54); return c
    c = C((70, 54, 44)); c.rect(-10, 760, W+10, H+10, (150, 146, 150), INK, 7); c.da.ellipse([460*S, 360*S, 1460*S, 1000*S], fill=(255, 140, 50, 50+int(16*math.sin(T.TT*6))))
    for i in range(11): x = 600+i*72; y = 760-(i % 3)*26; g = 90+int(50*math.sin(T.TT*5+i)); c.ell(x-48, y-40, x+48, y+30, COALC, INK, 5); c.ell(x-20, y-22, x+16, y-2, (230, g, 40), None)
    c.hide(960, 610+6*math.sin(T.TT*8), 2.0, (186, 160, 128))
    for i in range(3): c.smoke(800+i*160, 520, 2)
    L(c, "THEN ONTO THE COALS", 160, 960, 76); return c
def ratsell(k):
    if k == 0:
        c = below(300); a = sailor(c, 620, 1030, 380, "hold", "smug", "brown"); hx, hy = a["hand"]; c.line([(hx, hy), (hx+20, hy+80)], 6, (196, 150, 150), False); c.rat(hx+60, hy+190, 1.2, t=T.TT)
        b = sailor(c, 1300, 1030, 380, "hold", "worry", "blue", flip=True); c.ducat(b["hand"][0]-30, b["hand"][1]-30, 40, True); L(c, "RATS SELL FOR HALF A DUCAT EACH", 240, 960, 62); return c
    c = C((250, 238, 214)); c.rat(430, 640, 1.9); c.text(760, 560, "=", 200); c.ducat(960, 560, 90, True); c.text(1180, 560, "≈", 200) ; sack(c, 1500, 700, 1.9); c.text(1500, 790, "100 LB", 76)
    L(c, "ABOUT THE PRICE OF 100 POUNDS OF CLOVES", 200, 960, 60)
    if k == 2: L(c, "WHERE YOU'RE GOING", 930, 1300, 70, bg=MARI)
    return c
def gums(k=0):
    c = deck("grey", mast=0, sx=1640); s = sailor(c, 960, 1560, 860, "stand", "sleep", "slate"); u = s["u"]; hx, hy = s["head"]; mx, my = hx+.1*u, hy+.7*u
    c.rect(mx-.34*u, my-.2*u, mx+.34*u, my+.22*u, (60, 30, 34), INK, max(4, u*.05), .12*u)
    for sgn in (-1, 1):
        yy = my+sgn*.13*u; c.rect(mx-.3*u, yy-.07*u, mx+.3*u, yy+.07*u, (226, 84, 84), INK, max(3, u*.03), .06*u)
        for j in range(4): tx = mx-.2*u+j*.13*u; c.rect(tx-.035*u, yy-sgn*.1*u-.04*u, tx+.035*u, yy-sgn*.1*u+.04*u, PAPER, INK, max(2, u*.02))
    L(c, "THEN MEN'S GUMS BEGIN TO SWELL", 190, 960, 62); return c
def dead19(k):
    c = C((226, 222, 214)); n = 19 if k == 0 else 30
    for i in range(n): icon(c, 250+(i % 10)*156, 420+(i//10)*210, (150, 144, 136) if i < 19 else (214, 208, 200), 1.9)
    L(c, "PIGAFETTA'S COUNT: 19 DIE OF IT", 150, 700, 62)
    if k: L(c, "OTHER ACCOUNTS: NEARER 30", 270, 1240, 58, bg=MARI)
    return c
def never(k):
    c = below(0); dimc(c, 90); table(c, 760, 1500, 1030, 190); c.candle(1380, 810, 1.6, T.TT); p = piga(c, 620, 1030, 420, "write", "sad", bk=False); book(c, 1060, 780, 1.6)
    c.line([(p["hand"][0], p["hand"][1]), (p["hand"][0]+40+6*math.sin(T.TT*9), p["hand"][1]-70)], 6, PAPER, False)
    if k: L(c, "HE DOESN'T BELIEVE SUCH A VOYAGE\nWILL EVER BE REPEATED", 260, 1000, 56)
    else: L(c, "PIGAFETTA WRITES", 210, 1000, 70)
    return c
def land(k):
    if k == 0:
        c = sea("day", sx=1640); c.islet(420, 548, 760, 170, palms=4, seed=2); fleet(c, 790, [x-T.GP*110 for x in (980, 1320, 1660)], 290, torn=True); hud(c, "6 MAR 1521", 3); L(c, "LAND", 210, 1200, 120, bg=MARI); return c
    c = sea("day", sx=300); fleet(c, 640, (1280, 1530, 1780), 190, furl=1, calm=True, torn=True); beach(c, 800); c.palm(110, 1010, 1.3, T.TT)
    for i, x in enumerate((360, 680, 1000)): sailor(c, x, 1030, 330, ("cheer", "wave", "cheer")[i], "joy", CREW[i])
    c.bowl(1500, 980, 2.6, (196, 150, 96))
    for i in range(4): x = 1350+i*100; c.ell(x-34, 920-(i % 2)*16, x+34, 986-(i % 2)*16, (120, 84, 58), INK, 6)
    for i in range(2): c.fishp(1400+i*200, 900, .6)
    hud(c, "6 MAR 1521", 3); L(c, "AND FRESH FOOD", 210, 1100, 80); return c
def thieves(k):
    c = sea("day", sun=False); c.islet(1640, 548, 480, 110, palms=2, seed=4); v = c.nao(430, 760, 700, flip=True, bob=T.TT*1.2, furl=1, torn=True); q = T.ease(T.GP*1.1) if k >= 1 else 0; bx = lerp(1000, 1640, q); by = 850
    if k == 0: c.line([(v["boat"][0]-80, v["boat"][1]-110), (bx-140, by-24)], 5, PAPER, False)
    wash(c, 790, n=6); c.rowboat(bx, by, 1.1, empty=True)
    for i in range(2):
        x = lerp(2000+i*200, 1330+i*260, T.ease(T.LP)) if k == 0 else lerp(1330+i*260, 1900+i*200, q); y = 930+i*70
        islander(c, x+30, y+4, 170, "hold", "smile", ("rose", "brown")[i], flip=(k == 0)); c.proa(x, y, 1.0, flip=(k == 0), bob=T.TT*3+i)
        if k >= 1 and i == 0: c.line([(x-150, y-20), (bx+140, by-20)], 5, PAPER, False)
    hud(c, "MARCH 1521", 3)
    if k == 0: L(c, "THE FLAGSHIP'S SMALL BOAT", 190, 1300, 60)
    if k == 1: L(c, "THE ISLANDERS TAKE IT", 190, 1300, 64)
    if k == 2: L(c, "THE FLEET'S NAME FOR THE PLACE:\nTHE ISLANDS OF THIEVES", 200, 1300, 50, bg=MARI)
    return c
def nameyou(k=0):
    c = sea("day", sx=300); fleet(c, 640, (700, 1000, 1300), 200, furl=1, calm=True, torn=True); beach(c, 800); c.palm(1760, 1010, 1.3, T.TT, flip=True)
    for i, x in enumerate((420, 700, 980)): islander(c, x, 1030, 330, ("point", "chin", "shrug")[i], ("n", "bored", "n")[i], ("rose", "brown", "blue")[i])
    L(c, "THEY PROBABLY HAD A NAME FOR YOU, TOO", 210, 1060, 56); return c
def leagues(k=0):
    c, P = wmap(-140, -8, 8.2, 10); route(c, P, 20, 12, k=1.3); c.rect(100, 740, 1120, 990, PAPER, INK, 7, 22); c.text(610, 820, "ABOUT "+format(count(0, 4000, 1.0, .1, "c4k"), ",")+" LEAGUES", 92, RED); c.text(610, 930, "BY PIGAFETTA'S RECKONING", 54); return c

# ================= quest three: cloves =================
def phil(k):
    c, P = wmap(128, 10, 15, 18); route(c, P, lerp(20, 21, T.ease(T.LP)) if k == 0 else 21, 19.4, k=1.4); x, y = P(123, 12.5); hud(c, "16 MAR 1521", 3)
    for i in range(2): r = 150+14*i+8*math.sin(T.TT*3); c.ell(x-r*.7, y-r, x+r*.7, y+r, None, RED, 5)
    if k == 0: L(c, "TEN DAYS LATER", 240, 1300, 76)
    else: L(c, "THE ISLANDS THAT WILL BE\nCALLED THE PHILIPPINES", 250, 1320, 54, bg=MARI)
    return c
def isle(kind="day", palms=True, hz=560, sx=1560):
    """A beach on an island: sea behind, sand in front, palms at the edges."""
    c = sea(kind, hz=hz, sx=sx, calm=True); wash(c, hz+90, kind, calm=True); beach(c, 790)
    if palms: c.palm(120, 1000, 1.35, T.TT); c.palm(1810, 1010, 1.25, T.TT+1, flip=True)
    return c
def cross(c, x, y, h=420):
    c.line([(x, y), (x, y-h)], 26, INK, False); c.line([(x, y), (x, y-h)], 16, TIMBER, False); c.line([(x-h*.24, y-h*.7), (x+h*.24, y-h*.7)], 26, INK, False); c.line([(x-h*.24, y-h*.7), (x+h*.24, y-h*.7)], 16, TIMBER, False)
def cebu(k):
    c = isle(sx=790); cross(c, 960, 960); r = islander(c, 620, 1030, 360, "stand", "smile", "blue"); c.crown(r); q = islander(c, 400, 1036, 330, "stand", "n", "rose"); c.crown(q)
    f = c.person(1240, 1030, 350, "up", "smile", "brown", flip=True); c.tonsure(f); captain(c, 1480, 1030, 360, "stand", "smile", flip=True); hud(c, "1521", 3)
    L(c, "THE ISLAND OF CEBU" if k == 0 else "THE RULERS CONVERT TO CHRISTIANITY", 210, 1140, 70 if k == 0 else 54, bg=PAPER if k == 0 else MARI); return c
def stops(k=0):
    c = isle(); m = captain(c, 700, 1030, 440, "up", "det"); sword(c, m); sack(c, 1340, 1030, 1.5); c.text(1340, 720, "?", 170, RED); hud(c, "1521", 3); L(c, "NOT LIKE A MAN ON A SPICE RUN", 210, 1160, 60); return c
def lapu(k):
    if k == 0:
        c = C(SEAM); c.poly([(300, 1080), (420, 760), (560, 520), (760, 300), (900, 120), (1000, 200), (940, 470), (840, 760), (760, 1080)], (214, 220, 178), INK, 7); c.poly([(1110, 540), (1230, 470), (1330, 520), (1300, 640), (1170, 680)], (198, 208, 170), INK, 7)
        c.text(640, 760, "CEBU", 90); c.label(1420, 420, "MACTAN", 70, bg=MARI); mapnote(c, "SKETCH, NOT TO SCALE"); hud(c, "1521", 3); return c
    c = isle(sx=420); l = islander(c, 900, 1030, 460, "stand", "det", "brown", spear=True, back=True); c.bubble(1330, 470, "NO.", 150, (-220, 110)); hud(c, "1521", 3); L(c, "LAPULAPU, A CHIEF ON MACTAN", 210, 1180, 60); return c
def advise(k):
    c = deck("day", mast=1700); captain(c, 500, 1030, 420, "point", "angry")
    if k == 0: L(c, "MAGELLAN DECIDES TO MAKE HIM OBEY", 210, 1060, 62); return c
    for i, x in enumerate((960, 1200, 1440)): sailor(c, x, 1030, 350, ("shrug", "stand", "shrug")[i], "worry", CREW[i], flip=True)
    L(c, "HIS OWN MEN ADVISE AGAINST IT", 210, 1060, 66, bg=MARI); return c
def boats(k=0):
    c = sea("dawn", sx=300); c.islet(1540, 548, 760, 130, palms=3, seed=1)
    for i in range(3): c.rowboat(lerp(200, 520, T.ease(T.GP))+i*420, 760+i*70, 1.25, bob=T.TT*4+i, n=4)
    wash(c, 900, "dawn", n=6); hud(c, "27 APRIL 1521", 3); L(c, "60 MEN GO OVER IN BOATS", 210, 1100, 70); return c
def shallows(kind="dawn", y=880):
    c = sea(kind, hz=470, sx=300, calm=True); c.islet(1500, 478, 1100, 150, palms=4, seed=3); return c
def wade(k=0):
    c = shallows()
    for i, x in enumerate((300, 560, 820, 1080)): f = sailor(c, x+T.GP*60, 1040, 400, "hold", "det", CREW[i]); sword(c, f)
    wash(c, 912, "dawn", amp=7, n=4); hud(c, "27 APRIL 1521", 3); L(c, "49 WADE IN, UP TO THEIR THIGHS", 210, 1100, 62); return c
def waiting(k=0):
    c = shallows(); wash(c, 600, "dawn", calm=True); beach(c, 720)
    for r in range(3):
        for i in range(13 - r): islander(c, 150+i*(136+r*8)+r*40, 830+r*100, 190+r*30, "hold", "det", ("rose", "brown", "blue")[(i+r) % 3], spear=True, flip=True)
    hud(c, "27 APRIL 1521", 3); L(c, "PIGAFETTA COUNTS MORE THAN 1,500 WAITING", 210, 1120, 54, bg=MARI); return c
def killed(k):
    c = shallows("dusk"); wash(c, 620, "dusk", amp=7, n=8); c.swell(800, T.TT*.8, (120, 128, 160), 6, 340, ph=1); x = 980+16*math.sin(T.TT*.8); y = 850+6*math.sin(T.TT*1.6)
    c.d.pieslice([(x-90)*S, (y-80)*S, (x+90)*S, (y+80)*S], 180, 360, fill=(44, 40, 50), outline=INK, width=7*S); c.line([(x-130, y), (x+130, y)], 16, INK, False)
    c.line([(1300, 900), (1360, 690)], 12, INK, False); c.line([(1300, 900), (1360, 690)], 6, SILVER, False); c.swell(880, T.TT, (140, 146, 172), 7, 300, ph=2); beach(c, 970, (196, 170, 140)); dimc(c, 50); hud(c, "27 APRIL 1521", 3)
    if k == 0: L(c, "MAGELLAN IS KILLED IN THE SHALLOWS", 210, 1000, 62); return c
    c.rect(180, 560, 780, 800, PAPER, INK, 7, 22); icons(c, 240, 610, 8, 8, (150, 144, 136), 1.0, 62, 110); c.text(480, 740, "8 OF THE CREW DEAD WITH HIM", 40); L(c, "PIGAFETTA'S COUNT", 210, 1000, 62); return c
def mirror(k):
    c = C((226, 214, 190)); c.roll(300, 110, 1620, 970, 40); rows = ["“OUR MIRROR,", "OUR LIGHT,", "OUR COMFORT,", "AND OUR TRUE GUIDE”"]; n = (2 if k == 0 else 4)
    for i, t in enumerate(rows[:n]): c.text(960, 280+i*140, t, 104*(.8+.2*app(("mr", i), .25, .1+.5*(i % 2))), INKP)
    if k: c.text(960, 880, "PIGAFETTA, ON MAGELLAN", 52, FAINT)
    return c
def banquet(k):
    if k == 0:
        c = isle(); table(c, 700, 1500, 1030, 170); r = islander(c, 420, 1030, 380, "wave", "smile", "blue"); c.crown(r)
        for i, x in enumerate((820, 1000, 1180, 1360)): (c.bowl(x, 830, .6) if i % 2 == 0 else c.fishp(x, 826, .5))
        c.jug(1450, 834, .6); hud(c, "1 MAY 1521", 3); L(c, "THE KING OF CEBU INVITES\nTHE COMMANDERS TO A BANQUET", 250, 1120, 56); return c
    c = sea("day", sx=300); c.islet(1500, 548, 900, 150, palms=4, seed=1)
    for i in range(3): c.rowboat(lerp(300, 560, T.ease(T.LP))+i*360, 760+i*60, 1.2, bob=T.TT*4+i, n=4)
    wash(c, 890, n=6); hud(c, "1 MAY 1521", 3); L(c, "ABOUT TWO DOZEN MEN GO ASHORE", 210, 1100, 62); return c
def trap(k=0):
    c = sea("dusk", sun=False); c.islet(1380, 548, 1000, 160, palms=4, seed=1)
    for i in range(3): c.smoke(1200+i*170, 430, 3)
    fleet(c, 800, (240, 600, 960), 330, kind="dusk", furl=1); dimc(c, 110*app("td", .4), (90, 16, 16)); hud(c, "1 MAY 1521", 3); c.label(560, 260, "IT'S A TRAP", 90, PAPER, RED); return c
def countc(k):
    c = C((238, 226, 204)); n = count(0, 100, 1.0, .1, "c100") if k == 0 else 100; icons(c, 170, 360, n, 20, TEAL, 1.0, 83, 104)
    c.text(700, 200, f"ABOUT {n} OF YOU LEFT", 110, RED)
    if k:
        for i in range(3): c.naoicon(1420+i*170, 240, 1.7)
        L(c, "TOO FEW TO SAIL THREE SHIPS", 940, 960, 64, bg=MARI)
    return c
def burn(k):
    if k == 0:
        c = sea("day"); v = c.nao(860, 760, 640, bob=T.TT, furl=1, flag=None); wash(c, 790, n=5); xa = lerp(700, 300, T.ease(T.GP)); xb = lerp(1100, 1560, T.ease(T.GP))
        c.rowboat(xa, 900, 1.15, flip=True, bob=T.TT*4, n=2); c.barrel(xa-110, 884, .5); c.rowboat(xb, 940, 1.15, bob=T.TT*4+1, n=2); c.barrel(xb+110, 924, .5)
        hud(c, "MAY 1521", 3); L(c, "YOU STRIP THE CONCEPCIÓN", 210, 1120, 66); return c
    c = sea("night"); v = c.nao(960, 780, 640, furl=1, flag=None, hull=(70, 52, 44), tilt=4)
    for i, (dx, s) in enumerate(((-200, 1.3), (-60, 1.9), (90, 1.5), (220, 1.1))): c.fire(960+dx, 700-(i % 2)*30, s)
    c.da.ellipse([460*S, 200*S, 1460*S, 1000*S], fill=(255, 150, 60, 50)); c.smoke(900, 380, 3); c.smoke(1050, 420, 3); wash(c, 800, "night"); hud(c, "MAY 1521", 2); L(c, "AND BURN HER", 210, 1300, 90, bg=MARI); return c
def two(k):
    c = C((238, 226, 204)); rows = [("TWO SHIPS", TEAL), ("NO MAGELLAN", RED), ("STILL NO CLOVES", RED)]
    for i, (t, col) in enumerate(rows[:k+1]):
        y = 220+i*320; q = app(("tw", i), .3)
        if i == 0: c.naoicon(330, y+60, 2.6*q); c.naoicon(570, y+60, 2.6*q)
        if i == 1: f = captain(c, 450, y+120, 190, "stand", "n"); c.redx(450, y, 100, 20)
        if i == 2: c.clove(450, y, 1.6, 20); c.redx(450, y, 100, 20)
        c.text(800, y, t, 140, col, "lm")
    return c
def sixm(k=0):
    c, P = wmap(123, 5, 30, 34); route(c, P, lerp(22, 26, T.ease(T.LP)), 22, k=1.5); place(c, P, "CEBU", "CEBU", 150, -60, 46); place(c, P, "TIDORE", "TIDORE", 170, 40, 46); hud(c, "MAY TO NOV 1521", 2); L(c, "SIX MORE MONTHS", 240, 520, 76); return c
def tidore(k):
    if k == 0:
        c = sea("day", sx=300); c.poly([(900, 548), (1180, 300), (1290, 200), (1380, 210), (1470, 300), (1760, 548)], (120, 170, 110), INK, 7); c.puff([(1300, 170, 40), (1350, 140, 50), (1400, 170, 40)], WHITE, (150, 150, 150), 4)
        for i in range(6): c.tree(980+i*130, 552, .42+.06*(i % 2), (86, 132, 96))
        fleet(c, 770, (420, 900), 380, furl=1, calm=True, torn=True); beach(c, 920); hud(c, "8 NOV 1521", 2); L(c, "TIDORE", 210, 560, 100); return c
    c = isle(); c.tree(1500, 1010, 2.4, (86, 132, 96))
    for i, (dx, dy) in enumerate(((-150, -420), (-60, -500), (60, -470), (150, -400), (0, -380))): c.clove(1500+dx, 1010+dy, .42, 180+(i*37) % 40-20)
    s = sidp(c, 800, 1030, 420, "cheer", "joy"); hud(c, "8 NOV 1521", 2); L(c, "THE SPICE ISLANDS", 210, 900, 86, bg=MARI); return c
def late(k):
    c = C((238, 226, 204)); n = 3 if k else min(3, int(T.LP*3.4)+1)
    for i in range(n): c.calpage(520+i*440, 620, 1.35, "YEAR", str(i+1), c=TEAL if i < 2 else RED)
    if k == 0: L(c, "MORE THAN TWO YEARS AFTER LEAVING SPAIN", 220, 960, 58)
    else: L(c, "SO MUCH FOR TWO YEARS, THERE AND BACK", 220, 960, 58, bg=MARI); c.strike(330, 620, 1150, 20)
    return c
def share(k=0):
    c = deck("day", mast=1700)
    for i in range(5): sack(c, 1000+i*130, 1030-(i % 2)*10, 1.1)
    for i in range(3): sack(c, 1130+i*130, 900, 1.1)
    s = sidp(c, 520, 1030, 400, "hold", "smile"); sack(c, s["hand"][0]+70, s["hand"][1]+60, .55); L(c, "SAILORS ARE ENTITLED TO A SHARE OF THE CARGO", 210, 1000, 52); return c
def sell(k):
    c = isle(); t = islander(c, 1380, 1030, 380, "hold", "smile", "blue", flip=True); c.cloves(1150, 990, 9+k*5, .5, 2); a = sailor(c, 600, 1030, 380, "hold", ("smile", "n", "worry")[k], "slate"); hx, hy = a["hand"]
    if k == 0: c.poly([(hx+10, hy-60), (hx+150, hy-40), (hx+170, hy+110), (hx+90, hy+90), (hx+20, hy+120)], RED, INK, 6)
    if k == 1: c.line([(hx, hy), (hx+90, hy+60)], 5, INK, False); c.line([(hx, hy), (hx+150, hy+70)], 5, INK, False); c.shoe(hx+90, hy+150, .8); c.shoe(hx+210, hy+160, .8)
    if k == 2: c.poly([(hx+20, hy-50), (hx+70, hy-70), (hx+120, hy-50), (hx+180, hy-10), (hx+150, hy+20), (hx+120, hy), (hx+120, hy+110), (hx+20, hy+110), (hx+20, hy), (hx-10, hy+20), (hx-40, hy-10)], WHITE, INK, 6)
    L(c, ("SO MEN SELL THEIR CAPES", "THEIR SHOES", "EVEN THEIR SHIRTS")[k], 210, 1000, 70, bg=PAPER if k < 2 else MARI); hud(c, "NOV 1521", 2); return c

# ================= the hidden quest: get home =================
def job(k):
    c, P = wmap(); route(c, P, 26 if k else lerp(0, 26, T.ease(T.LP*1.15)), 0, k=1.0)
    if k == 0: L(c, "NOBODY SET OUT TO SAIL AROUND THE WORLD", 900, 700, 54)
    if k >= 1: L(c, "THE JOB: A NEW ROAD TO THESE ISLANDS", 900, 660, 54)
    if k == 2: c.tick(1470, 880, 60); c.label(1690, 880, "DONE", 100, TEAL)
    return c
def leak(k):
    c = sea("day", sx=300); c.poly([(1300, 548), (1500, 380), (1600, 330), (1700, 380), (W+40, 548)], (120, 170, 110), INK, 7); c.nao(1380, 770, 400, furl=1, bob=T.TT, torn=True)
    lo = 34*app("lk", 1.0, .2) if k else 0; c.nao(600, 780+lo, 620, furl=1, bob=T.TT*.8, tilt=-5*(lo/34), torn=True)
    if k:
        for i in range(3): x = 430+i*150; h = 60+30*abs(math.sin(T.TT*5+i)); c.line([(x, 780), (x-10, 780-h), (x+14, 780-h*.5)], 9, FOAM, False)
    wash(c, 800, n=6)
    if not k:
        for i in range(2): c.rowboat(lerp(1560, 1060, T.ease(T.GP))+i*300, 900+i*50, 1.0, flip=True, bob=T.TT*4+i, n=2); sack(c, lerp(1560, 1060, T.ease(T.GP))+i*300+100, 884+i*50, .5)
    hud(c, "LATE 1521", 2); L(c, "LOADING CLOVES" if k == 0 else "THE FLAGSHIP SPRINGS A SERIOUS LEAK", 180, 1300, 70 if k == 0 else 50, bg=PAPER if k == 0 else MARI); return c
EAST = [(127.4, .7), (134, 8), (142, 20), (150, 32), (158, 40), (152, 30), (140, 14), (128.5, 2)]
def eastpath(c, P, q, col=NAVY):
    n = max(2, int(q*(len(EAST)-1))+1); px = [P(*p) for p in EAST[:n]]
    for a, b in zip(px, px[1:]):
        m = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1])/26))
        for j in range(m): x = lerp(a[0], b[0], j/m); y = lerp(a[1], b[1], j/m); c.ell(x-7, y-7, x+7, y+7, col, None)
    c.naoicon(px[-1][0], px[-1][1]+6, 1.2); return px[-1]
def split(k):
    c, P = wmap(118, 8, 11, 13); x, y = place(c, P, "TIDORE", "TIDORE", -40, 90, 44); hud(c, "LATE 1521", 2)
    if k == 0: c.naoicon(x-70, y, 1.5); c.naoicon(x+70, y, 1.5); L(c, "SO THEY SPLIT UP", 210, 1100, 80); return c
    tx, ty = eastpath(c, P, lerp(.1, .5, T.ease(T.LP))); c.label(640, 300, "THE TRINIDAD:\nBACK EAST, ACROSS THE PACIFIC", 46); return c
def trin(k):
    if k == 0:
        c, P = wmap(118, 8, 11, 13); place(c, P, "TIDORE", "TIDORE", -40, 90, 44); eastpath(c, P, lerp(.5, 1, T.ease(T.LP))); hud(c, None, 1); L(c, "SHE DOESN'T MAKE IT. SHE TURNS BACK.", 210, 1140, 54); return c
    if k == 1:
        c = sea("grey", sun=False); c.nao(1250, 780, 520, flip=True, bob=T.TT, flag=DGREEN, wind=T.TT); c.nao(560, 790, 480, bob=T.TT+1, furl=1, torn=True, flag=None, tilt=-4); wash(c, 800, "grey"); L(c, "THE PORTUGUESE CAPTURE HER", 210, 960, 66); return c
    c = C((238, 226, 204)); icons(c, 560, 420, 5, 5, TEAL, 3.0, 62, 110, cols=lambda i: TEAL if i < 4 else (160, 206, 200)); L(c, "BY ONE COUNT", 180, 960, 56, bg=MARI); L(c, "FOUR OR FIVE OF HER MEN EVER SEE EUROPE AGAIN", 800, 960, 54); return c
def west(k):
    c, P = wmap(72, -8, 9.4, 11.4); place(c, P, "TIDORE", "TIDORE", 60, -70, 44); q = T.ease(T.LP); route(c, P, lerp(26, 30, q) if k == 0 else lerp(30, 33.4, q), 26, col=TEAL, dots=True, k=1.2); hud(c, None, 1)
    if k == 0: L(c, "YOUR SHIP GOES THE OTHER WAY: WEST", 210, 1060, 56)
    else: L(c, "ROUND THE BOTTOM OF AFRICA", 210, 1060, 62, bg=MARI)
    return c
def elc(k):
    c = deck("day", mast=1700); e = elcano(c, 860, 1030, 390, "point" if k == 0 else "stand", "det" if k == 0 else "smug")
    L(c, "HER CAPTAIN NOW: JUAN SEBASTIÁN ELCANO", 180, 1000, 54)
    if k: L(c, "THE PARDONED MUTINEER", 310, 1000, 62, bg=MARI)
    hud(c, None, 1); return c
def q4(k):
    if k == 0: c = C(); c.questlog(ROWS, 4, 3, HID, x=545, y=200); return c
    c, P = wmap(); route(c, P, 26, 0, ship=False); route(c, P, lerp(26, 40, T.ease(T.LP)), 26, col=TEAL, dots=True); L(c, "ELCANO'S WAY HOME: THE REST OF THE WAY ROUND", 900, 760, 50, bg=MARI); return c
def sixty(k):
    if k == 0:
        c = sea("dusk", sx=300); vict(c, lerp(1150, 900, T.GP), 800, 600, flip=True, torn=True); wash(c, 812, "dusk"); hud(c, "21 DEC 1521", 1); L(c, "THE VICTORIA SAILS, WITH 60 ON BOARD", 210, 1120, 54); return c
    c = C((238, 226, 204)); icons(c, 150, 270, 47, 16, TEAL, 1.25, 84, 110, shown=47*app("i47", .8)); c.text(960, 160, "47 OF THE CREW", 80, (20, 120, 116))
    icons(c, 150, 860, 13, 16, MARI, 1.25, 84, 110, shown=13*app("i13", .5, .7)); c.text(960, 770, "13 ISLANDERS", 80, (176, 120, 20)); return c
def away(k):
    c, P = wmap(72, -8, 9.4, 11.4); q = T.ease(T.LP); route(c, P, lerp(26, 29.5, q) if k == 0 else lerp(29.5, 31, q), 26, col=TEAL, k=1.2); hud(c, "EARLY 1522", 1)
    for lo, la in ((76, 6), (62, 16), (46, -8), (38, -22)): x, y = P(lo, la); c.naoicon(x, y, 1.0, col=DGREEN, sail=(214, 232, 206))
    c.label(P(60, 16)[0], P(60, 16)[1]-90, "PORTUGUESE SHIPS", 40, bg=(214, 232, 206))
    L(c, "ELCANO KEEPS WELL AWAY FROM THE COAST" if k == 0 else "SO THE PORTUGUESE CAN'T CATCH YOU", 930, 1380, 46, bg=PAPER if k == 0 else MARI); return c
def months(k=0):
    c = sea("day", hz=420, sx=300); x = lerp(1500, 1000, T.GP)
    for i in range(1, 9): c.ell(x+70+i*60-5, 712-5, x+70+i*60+5, 712+5, FOAM, None)
    vict(c, x, 700, 150, flip=True, torn=True); wash(c, 706, n=20); hud(c, "1522", 1); L(c, "MONTHS WITHOUT TOUCHING LAND", 240, 960, 66); return c
def moz(k):
    if k == 0:
        c = deck("day", mast=300, sx=620)
        for i, x in enumerate((760, 1040, 1320)): sailor(c, x, 1030, 370, "point", "worry", CREW[i])
        c.bubble(1600, 430, "LAND?", 90, (-150, 110)); hud(c, "1522", 1); L(c, "MANY WANT TO PUT IN AT MOZAMBIQUE", 210, 1100, 56); return c
    c, P = wmap(44, -24, 20, 24); place(c, P, "MOZAMBIQUE", "MOZAMBIQUE:\nPORTUGUESE", 330, -40, 48, bg=(214, 232, 206)); route(c, P, lerp(30.3, 31.2, T.ease(T.LP)), 29.6, col=TEAL, k=1.5); hud(c, "1522", 1); L(c, "THE SHIP SAILS ON", 930, 520, 76, bg=MARI); return c
def capegh(k):
    c = sea("storm", sun=False); c.swell(600, T.TT*1.4, SEAC["storm"][0], 30, 520, ph=1); c.nao(900+24*math.sin(T.TT*1.7), 800+18*math.sin(T.TT*2.2), 520, flip=True, bob=T.TT*5, tilt=12*math.sin(T.TT*1.9), torn=True, wind=T.TT*3)
    wash(c, 810, "storm", amp=34); rain(c, 90); hud(c, "1522", 1)
    if k == 0: L(c, "THE CAPE OF GOOD HOPE TAKES WEEKS", 210, 1100, 58)
    if k >= 1: c.label(520, 250, "ONE VERSION OF\nPIGAFETTA: 9 WEEKS", 52)
    if k == 2: c.label(1440, 250, "ANOTHER:\n7 WEEKS", 52, bg=MARI)
    return c
def roundc(k=0):
    c, P = wmap(14, -28, 20, 24); route(c, P, lerp(31.2, 33.3, T.ease(T.LP)), 30.6, col=TEAL, k=1.5); place(c, P, "GOODHOPE"); hud(c, "MAY 1522", 1); L(c, "YOU GET ROUND IT", 230, 520, 80); return c
def die21(k=0):
    c = sea("dusk", sx=1560); vict(c, 520, 800, 520, flip=True, torn=True); wash(c, 812, "dusk"); c.rect(1020, 200, 1840, 930, PAPER, INK, 7, 22); icons(c, 1090, 270, 21, 7, (150, 144, 136), 1.5, 68, 108, shown=21*app("i21", 1.0))
    c.text(1430, 850, "21 MEN DIE IN TWO MONTHS", 54); hud(c, "MAY TO JULY 1522", 1); return c
def cv(k):
    if k == 0:
        c, P = wmap(-10, 8, 16, 19); x, y = P(-23.6, 15)
        for dx, dy, r in ((-40, -30, 16), (-4, -44, 13), (34, -20, 15), (-30, 24, 14), (16, 30, 18)): c.ell(x+dx-r, y+dy-r*.7, x+dx+r, y+dy+r*.7, ISLE, INK, 4)
        route(c, P, lerp(33.3, 37, T.ease(T.LP)), 32, col=TEAL, k=1.4); c.label(x-380, y-120, "THE CAPE VERDE ISLANDS", 46); hud(c, "1522", 1); L(c, "STARVING, ELCANO RISKS ONE STOP", 900, 1000, 56); return c
    c = harbour(); vict(c, 560, 790, 520, torn=True, furl=1, flag=None); wash(c, 800, n=6); hud(c, "1522", 1); chip(c, 1500, 420, "PORTUGUESE", DGREEN, 64); return c
def harbour(kind="day"):
    """A Portuguese island port: hill, a small fort with a green pennant, a quay on the right."""
    c = sea(kind, sx=300); c.poly([(1000, 548), (1250, 380), (1500, 330), (1760, 400), (W+40, 548)], (176, 170, 130), INK, 7); c.rect(1420, 250, 1640, 340, RWALL, INK, 6)
    for x in range(1420, 1640, 44): c.rect(x, 230, x+24, 254, RWALL, INK, 5)
    c.line([(1530, 250), (1530, 150)], 7, TIMBER, False); c.poly([(1530, 152), (1620+8*math.sin(T.TT*3), 172), (1530, 194)], DGREEN, INK, 5)
    return c
def hquay(c, y=860):
    c.rect(1100, y, W+10, H+10, CONC, INK, 6)
    for yy in (y+70, y+140): c.line([(1100, yy), (W, yy)], 3, (180, 172, 160), False)
    for x in (1180, 1700): c.rect(x-16, y-50, x+16, y+6, (70, 62, 58), INK, 5, 6)
def boat(k):
    c = harbour(); vict(c, 330, 790, 440, torn=True, furl=1, flag=None); x = lerp(560, 900, T.ease(T.GP)); c.rowboat(x, 900, 1.3, bob=T.TT*4, n=3); wash(c, 940, n=6); hquay(c); portu(c, 1500, 870, 330, "stand", "n", flip=True); hud(c, "1522", 1)
    if k == 0: L(c, "A BOAT GOES ASHORE", 210, 800, 70)
    else: c.bubble(x+120, 560, "WHAT DAY IS IT?", 76, (-90, 130)); L(c, "TOLD TO ASK ONE THING", 210, 800, 60)
    return c
def thu(k=0):
    c = harbour(); vict(c, 330, 790, 440, torn=True, furl=1, flag=None); c.rowboat(900, 900, 1.3, bob=T.TT*4, n=3); wash(c, 940, n=6); hquay(c); portu(c, 1560, 870, 360, "shrug", "smile", flip=True); c.bubble(1120, 380, "THURSDAY.", 110, (300, 150)); hud(c, "1522", 1); return c
def wed(k=0):
    c = deck("day", mast=300, sx=620); c.line([(1040, 800), (980, 1030)], 16, TIMBER, False); c.line([(1560, 800), (1620, 1030)], 16, TIMBER, False); c.rect(900, 330, 1700, 800, PARCH, INK, 8, 10); c.line([(1300, 330), (1300, 800)], 6, INK, False)
    c.text(1100, 420, "SHIP'S COUNT", 48, INKP); c.text(1500, 420, "TODAY IS", 48, INKP)
    for i in range(5):
        for j in range(4): c.line([(1000+j*26, 500+i*56), (1000+j*26, 540+i*56)], 6, INKP, False)
        c.line([(988, 540+i*56), (1090, 500+i*56)], 6, INKP, False)
    c.text(1500, 610, "WED", 190, RED); piga(c, 560, 1030, 400, "point", "worry", bk=False); hud(c, "1522", 1); return c
def amazed(k):
    if k == 0:
        c = deck("day", mast=0)
        for i, x in enumerate((420, 760, 1100, 1440)): (sailor(c, x, 1030, 380, "shrug" if i % 2 else "stand", "wow", CREW[i]) if i != 1 else sidp(c, x, 1030, 400, "shrug", "wow"))
        chip(c, 620, 330, "SHIP: WEDNESDAY", NAVY, 60); chip(c, 1320, 330, "SHORE: THURSDAY", DGREEN, 60); c.text(972, 326, "≠", 100, RED); hud(c, "1522", 1); return c
    c = below(0); dimc(c, 90); table(c, 760, 1500, 1030, 190); c.candle(1380, 810, 1.6, T.TT); p = piga(c, 620, 1030, 420, "write", "det", bk=False); book(c, 1060, 780, 1.6); L(c, "LATER, PIGAFETTA WRITES DOWN THE REASON", 210, 1000, 54); return c
def sunsc(k):
    """Looking down on the world: it turns under the sun; the ship creeps the other way round the rim."""
    c = C((24, 30, 58)); cx, cy, r = 760, 590, 300; g = T.GP
    for i in range(40): x = (i*197) % W; y = (i*89) % H; c.da.ellipse([(x-3)*S, (y-3)*S, (x+3)*S, (y+3)*S], fill=(255, 248, 236, 200))
    c.da.ellipse([(1660-260)*S, (590-260)*S, (1660+260)*S, (590+260)*S], fill=(255, 220, 120, 60)); c.ell(1660-130, 590-130, 1660+130, 590+130, MARI, INK, 8)
    for a in range(0, 360, 30): ra = math.radians(a+T.TT*8); c.line([(1660+160*math.cos(ra), 590+160*math.sin(ra)), (1660+210*math.cos(ra), 590+210*math.sin(ra))], 8, MARI, False)
    c.ell(cx-r, cy-r, cx+r, cy+r, (150, 196, 214), INK, 8); c.d.pieslice([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], 90, 270, fill=(60, 90, 124), outline=INK, width=8*S)
    spin = T.TT*.9; home = spin
    for a, w in ((0, 1.0), (2.1, .7), (3.8, .9)): ra = home+a; c.ell(cx+r*.55*math.cos(ra)-60*w, cy+r*.55*math.sin(ra)-44*w, cx+r*.55*math.cos(ra)+60*w, cy+r*.55*math.sin(ra)+44*w, (196, 206, 150), INK, 5)
    hx, hy = cx+r*math.cos(home), cy+r*math.sin(home); c.ell(hx-22, hy-22, hx+22, hy+22, RED, INK, 6)
    lag = {0: lerp(0, 2.2, g), 1: lerp(2.2, 4.4, g), 2: lerp(4.4, 6.283, g), 3: 6.283}[k]; sa = home-lag
    for j in range(int(lag/.12)): a2 = home-j*.12; c.ell(cx+(r+50)*math.cos(a2)-6, cy+(r+50)*math.sin(a2)-6, cx+(r+50)*math.cos(a2)+6, cy+(r+50)*math.sin(a2)+6, PAPER, None)
    sx, sy = cx+(r+50)*math.cos(sa), cy+(r+50)*math.sin(sa); c.naoicon(sx, sy+24, 1.9)
    c.label(cx+(r-130)*math.cos(home), cy+(r-130)*math.sin(home), "SPAIN", 44)
    L(c, ("YOU SAILED WEST THE WHOLE WAY", "THE SAME WAY AS THE SUN", "AND CAME BACK TO WHERE YOU STARTED", "YOU SAW ONE SUNRISE FEWER THAN SPAIN DID")[k], 130, 960, 56, bg=PAPER if k < 3 else MARI); return c
def lostday(k=0):
    c = C((238, 226, 204)); c.calpage(560, 620, 1.5, "SHIP", "WED", c=NAVY); c.calpage(1360, 620, 1.5, "SHORE", "THU", c=DGREEN); c.text(960, 610, "≠", 190, RED); L(c, "AS FAR AS ANYONE KNOWS, THE FIRST\nCREW TO LOSE A DAY THIS WAY", 200, 960, 54); return c
def seized(k=0):
    c = harbour(); vict(c, 330, 790, 440, torn=True, furl=1, flag=None); c.rowboat(900, 900, 1.3, n=3, oars=False); wash(c, 940, n=6); hquay(c)
    for i, x in enumerate((1240, 1480, 1720)): f = portu(c, x, 890+(i % 2)*24, 330, "hold", "angry", flip=True); hx, hy = f["hand"]; c.line([(hx, hy-330), (hx, 890+(i % 2)*24)], 9, TIMBER, False); c.poly([(hx-12, hy-330), (hx, hy-390), (hx+12, hy-330)], SILVER, INK, 4)
    hud(c, "1522", 1); L(c, "THE BOAT IS SEIZED, WITH 13 MEN IN IT", 210, 860, 58, bg=MARI); return c
def flee(k):
    c = harbour(); vict(c, lerp(700, 380, T.ease(T.GP)), 800, 520, flip=True, torn=True); wash(c, 812); hud(c, "1522", 1); L(c, "ELCANO DOESN'T WAIT" if k == 0 else "THE VICTORIA SETS SAIL AT ONCE", 210, 700, 62, bg=PAPER if k == 0 else MARI); return c
def home(k):
    c = sea("gold", sx=300); coast(c, 548, 1250, W+40, 150, (190, 196, 150), 2); c.rect(1560, 440, 1620, 548, RWALL, INK, 5); c.poly([(1550, 440), (1590, 396), (1630, 440)], TILE, INK, 5)
    vict(c, lerp(300, 760, T.ease(T.GP)), 800+16, 540 if k == 0 else 600, torn=True, tilt=-3); wash(c, 808, "gold"); hud(c, "SAT 6 SEPT 1522", 1); L(c, "YOU ENTER THE BAY AT SANLÚCAR", 210, 1160, 60); return c
def pumps(k=0):
    c = below(300); a = 16*math.sin(T.TT*6); ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); px, py = 960, 470
    c.rect(px-40, py, px+40, 830, (96, 92, 98), INK, 7, 8); c.rect(px-60, 800, px+60, 836, (70, 66, 72), INK, 6, 6); c.poly([(px+40, 640), (px+150, 640), (px+150, 690), (px+40, 680)], (96, 92, 98), INK, 6)
    for i in range(6): y = 690+((T.TT*320+i*56) % 300); c.ell(px+112, y, px+142, y+34, WATER, INK, 4)
    c.line([(px-420*ca, py+420*sa), (px+420*ca, py-420*sa)], 24, INK, False); c.line([(px-420*ca, py+420*sa), (px+420*ca, py-420*sa)], 14, TIMBER, False); c.ell(px-18, py-18, px+18, py+18, (70, 66, 72), INK, 5)
    sailor(c, px-420, 1030, 380, "up" if a < 0 else "carry", "strain", "slate"); sailor(c, px+420, 1030, 380, "carry" if a < 0 else "up", "strain", "brown", flip=True)
    c.swell(1000, T.TT*1.4, (90, 140, 170), 8, 300); L(c, "SHE ONLY FLOATS BECAUSE THE PUMPS NEVER STOP", 210, 1100, 50, bg=MARI); return c
def three(k=0):
    c = C((238, 226, 204)); c.text(960, 440, "3 YEARS", 330, NAVY); q = app("l2", .3, .6)
    if q > 0: c.text(960, 760, "LESS TWO WEEKS", 130*q, RED)
    return c
def eighteen(k):
    c = quay("gold", ships=1, sun=False)
    for i in range(18):
        x = 150+(i % 9)*190+(i//9)*90; y = 1000+(i//9)*56
        if i == 4: piga(c, x, y, 230, "write", "det")
        else: c.fig(x, y, 230, "stand", ("sad", "sleep", "worry", "n")[i % 4], "sci", flip=i % 2 == 0)
    L(c, "PIGAFETTA COUNTS 18 OF THE CREW LEFT" if k == 0 else "MOST OF THEM SICK", 210, 700, 60, bg=PAPER if k == 0 else MARI); hud(c, "SEPT 1522", 1); return c
def islanders3(k=0):
    c = C((238, 226, 204)); icons(c, 230, 420, 13, 13, MARI, 2.2, 52, 110, cols=lambda i: (176, 120, 20) if i < 3 else ((226, 180, 90) if i == 3 else (226, 220, 206)))
    L(c, "THREE OR FOUR OF THE 13 ISLANDERS ARE STILL ABOARD", 200, 960, 50); L(c, "THE SOURCES DIFFER", 800, 960, 62, bg=MARI); return c
def guns(k):
    c = quay("day", ships=0, sun=False); v = c.nao(760, 720, 640, furl=1, torn=True, bob=T.TT)
    c.swell(730, T.TT*.6, SEAC["day"][1], 5, 380, y1=812)
    if k:
        for i, gx in enumerate((-80, -20, 40)): t = (T.TT*1.3+i*.33) % 1; x = 760+gx*640/560; y = 662; c.puff([(x-20*t, y-50*t, 26+44*t), (x+36, y-30-70*t, 22+40*t), (x+10, y+8-20*t, 20+26*t)], (206, 204, 204), (120, 118, 120), 4)
    c.rect(-10, 810, W+10, H+10, CONC, INK, 6)
    for yy in (880, 950, 1020): c.line([(0, yy), (W, yy)], 3, (180, 172, 160), False)
    for i, x in enumerate((1300, 1500, 1700)): sailor(c, x, 1030, 300, "cheer" if k else "stand", "joy" if k else "wow", ("rose", "blue", "brown")[i], flip=True, cap=False)
    hud(c, "MON 8 SEPT 1522", 1); c.label(1180, 220, "SEVILLE" if k == 0 else "SHE FIRES\nALL HER GUNS", 90 if k == 0 else 54, bg=PAPER if k == 0 else MARI); return c
def shirt(c, x, y, h, ex, flip=False):
    """One of the eighteen: in his shirt, bare feet."""
    f = c.fig(x, y, h, "hold", ex, "sci", flip=flip); u = f["u"]
    for dx in (-.1, .3): bx = x+(dx if not flip else -dx)*u; c.ell(bx-.19*u, y-.19*u, bx+.19*u, y+.06*u, PAPER, INK, max(3, u*.06))
    return f
def walk(k):
    c = C((238, 226, 204)); sky(c, 520, "dusk" if k == 2 else "gold", sun=False); c.church(1280, 800, 1.5, RWALL)
    for i, (x, w, h) in enumerate(((40, 380, 420), (460, 340, 360), (840, 360, 400))): c.rect(x, 800-h, x+w, 800, (RWALL, OCHRE, PINK)[i], INK, 6); c.poly([(x-12, 800-h), (x+w/2, 800-h-70), (x+w+12, 800-h)], TILE, INK, 6); c.rect(x+w*.38, 800-230, x+w*.62, 800, (90, 64, 44), INK, 5, 8); c.rect(x+w*.1, 800-h+50, x+w*.3, 800-h+130, GLASSD, INK, 5)
    c.rect(0, 800, W, H, (206, 190, 160), None); c.line([(0, 800), (W, 800)], 6, INK, False)
    if k == 2: dimc(c, 90)
    for r in (0, 1):
        for i in range(9):
            x = 90+i*172+r*80+T.GP*110; y = 930+r*120+5*math.sin(T.TT*6+i+r); f = shirt(c, x, y, 190+r*24, ("sad", "n", "sleep", "worry")[(i+r) % 4])
            if k == 2: c.candle(f["hand"][0]+6, f["hand"][1]+26, .7, T.TT+i)
    L(c, ("THE EIGHTEEN WALK TO CHURCH", "IN THEIR SHIRTS. BAREFOOT.", "EACH ONE HOLDING A CANDLE")[k], 160, 640, 60, bg=PAPER if k < 2 else MARI); return c
def one13(k):
    c = C(); icons(c, 230, 440, 13, 13, k=2.0, gx=48, gy=110, cols=lambda i: RED if i == 6 and k else GREY); s = sidp(c, 1680, 1010, 380, "self", "worry")
    L(c, "ARE YOU ONE OF THE EIGHTEEN?" if k == 0 else "ROUGHLY ONE MAN IN THIRTEEN WAS", 220, 800, 66, bg=PAPER if k == 0 else MARI); return c
def notall(k=0):
    c = C(); icons(c, 200, 300, 18, 9, TEAL, 1.9, 66, 124)
    for i in range(3): c.text(1380+i*130, 480-16*math.sin(T.TT*3+i), "?", 190, RED)
    L(c, "BUT 18 ISN'T EVERYONE WHO LIVED", 850, 960, 70, bg=MARI); return c
def sanant(k):
    if k == 0:
        c = channel("cold", 1, sail=False, w=10); c.nao(lerp(900, 1500, T.ease(T.LP)), 780, 420, bob=T.TT*1.5, wind=T.TT); wash(c, 792, "cold"); L(c, "THE SAN ANTONIO: TURNED ROUND IN THE STRAIT", 210, 960, 52); return c
    if k == 1:
        c, P = wmap(-40, -4, 9.5, 10.4); back = [(-71, -53.4), (-68, -52.3), (-60, -46), (-48, -36), (-38, -28), (-28, -10), (-25, 10), (-20, 28), (-6.4, 36.8)]; px = [P(*p) for p in back]
        for a, b in zip(px, px[1:]):
            m = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1])/30))
            for j in range(m): x = lerp(a[0], b[0], j/m); y = lerp(a[1], b[1], j/m); c.ell(x-7, y-7, x+7, y+7, NAVY, None)
        c.naoicon(px[-1][0], px[-1][1]+6, 1.4); place(c, P, "SEVILLE", "SEVILLE", 190, -30); L(c, "SHE REACHED SEVILLE IN MAY 1521", 880, 1330, 58, bg=MARI); return c
    c = quay("day", ships=1, sun=False)
    if k == 2:
        c.rect(240, 170, 1680, 800, PAPER, INK, 7, 22); n = count(0, 55, 1.0, .1, "c55"); icons(c, 320, 250, n, 19, NAVY, 1.05, 70, 140); c.text(960, 720, f"BY ONE COUNT: ABOUT {n} MEN", 64); return c
    for i, x in enumerate((240, 480, 720)): sailor(c, x, 1030, 330, "cheer", "joy", CREW[i])
    c.rect(1080, 330, 1840, 990, PAPER, INK, 8, 22); sidp(c, 1380, 960, 300, "shrug", "sad"); c.clove(1680, 640, 1.0, 20); c.redx(1680, 640, 80, 16); c.text(1460, 410, "MEANWHILE, YOU", 54)
    L(c, "HOME BEFORE YOU'D SEEN A SINGLE CLOVE", 210, 960, 56, bg=MARI); return c
def tally(k):
    c = C((238, 226, 204)); rows = [("BROUGHT IN THE VICTORIA", "18"), ("THE SAN ANTONIO", "ABOUT 55"), ("CREW SEIZED AT CAPE VERDE", "12"), ("THE TRINIDAD", "4 OR 5")]; n = 3 if k == 0 else 4
    c.rect(200, 90, 1720, 1000 if k >= 2 else 810, PAPER, INK, 7, 22); c.text(960, 160, "WHO LIVED, BY ONE TALLY", 64)
    for i, (a, b) in enumerate(rows[:n]):
        y = 290+i*130; hi = (k == 0 and i == 2) or (k == 1 and i == 3) or (k == 3 and i == 0)
        if hi: c.rect(230, y-56, 1690, y+56, MARI, None, 0, 14)
        c.text(280, y, a, 60, INK, "lm"); c.text(1640, y, b, 70, RED, "rm")
    if k >= 2: c.line([(260, 800), (1660, 800)], 7, INK, False); c.text(280, 900, "OUTLIVED THE VOYAGE", 66, INK, "lm"); c.text(1640, 900, "ABOUT 90", 110, RED, "rm")
    return c
def clovesc(k):
    c = quay("day", ships=0)
    for r in range(3):
        for i in range(9-r): sack(c, 250+i*150+r*75, 1040-r*118, 1.05)
    c.rect(1120, 150, 1840, 500 if k == 0 else 650, PAPER, INK, 7, 22); c.text(1480, 260, str(count(0, 381, 1.2, .1, "c381")), 190, RED); c.text(1480, 410, "SACKS OF CLOVES", 60)
    if k: c.rect(1160, 490, 1800, 610, MARI, INK, 6, 16); c.text(1480, 546, "ABOUT 26 TONS", 76)
    return c
def profit(k):
    c = C((238, 226, 204)); t = -7*app("tip", .8, .2); ca, sa = math.cos(math.radians(t)), math.sin(math.radians(t)); px, py = 960, 430
    c.rect(930, 430, 990, 930, TIMBER, INK, 6); c.rect(760, 920, 1160, 960, TIMBER, INK, 6, 8); lx, ly = px-520*ca, py-520*sa; rx, ry = px+520*ca, py+520*sa; c.line([(lx, ly), (rx, ry)], 22, INK, False); c.line([(lx, ly), (rx, ry)], 12, TIMBER, False)
    for (x, y), side in (((lx, ly), 0), ((rx, ry), 1)):
        c.line([(x, y), (x-170, y+250)], 5, INK, False); c.line([(x, y), (x+170, y+250)], 5, INK, False); c.rect(x-210, y+250, x+210, y+276, BRASS, INK, 6, 8)
        if side == 0:
            for i in range(4): sack(c, x-150+i*100, y+250, .8)
            c.text(x, y+340, "ONE CARGO OF CLOVES", 46)
        else:
            for i in range(5): c.naoicon(x-150+i*76, y+236, 1.0)
            c.text(x, y+340, "WHAT ALL FIVE SHIPS COST", 46)
    L(c, "WORTH MORE THAN ALL FIVE SHIPS COST" if k == 0 else "THE VOYAGE STILL MADE A PROFIT", 170, 960, 62, bg=PAPER if k == 0 else MARI); return c
def arms(k):
    c = C((238, 226, 204))
    if k == 0: elcano(c, 520, 1010, 460, "hold", "smile"); c.shield(1240, 560, 2.6, (226, 214, 190)); c.globe(1240, 500, 170, T.TT*.3); L(c, "ELCANO GETS A COAT OF ARMS", 170, 960, 66); return c
    c.shield(960, 440, 3.0, (226, 214, 190)); c.globe(960, 370, 200, T.TT*.3)
    if k == 1: c.label(1560, 400, "A GLOBE", 100); return c
    c.rect(260, 830, 1660, 1030, PAPER, INK, 7, 20); c.text(960, 892, "PRIMUS CIRCUMDEDISTI ME", 74, INKP); c.text(960, 978, "YOU WERE THE FIRST TO ENCIRCLE ME", 50); return c
def credit(k):
    if k == 0: c = straitmap(.9, west="PACIFIC"); c.label(960, 240, "THE STRAIT OF MAGELLAN", 80, bg=MARI); return c
    c = C((238, 226, 204)); sky(c, 800, "day", sun=False); c.rect(0, 800, W, H, (206, 190, 160), None); c.line([(0, 800), (W, 800)], 6, INK, False); c.rect(780, 700, 1140, 1000, MARBLE, INK, 8); c.rect(740, 670, 1180, 710, MARBLE, INK, 8); c.rect(720, 990, 1200, 1030, MARBLE, INK, 8); c.text(960, 850, "MAGELLAN", 64)
    m = captain(c, 960, 674, 330, "point", "det")
    for i, x in enumerate((330, 1560)): sailor(c, x, 1020, 300, "cheer", "joy", CREW[i], flip=i == 1, cap=False)
    L(c, "AND MOST OF THE CREDIT", 170, 960, 64); return c
def never2(k):
    c, P = wmap(); route(c, P, 22.4, 0, ship=False); x, y = P(124, 10.3); c.redx(x, y, 34, 12)
    if k == 0: c.label(x-250, y-110, "MAGELLAN'S VOYAGE ENDS HERE", 44); L(c, "HE NEVER WENT AROUND THE WORLD", 900, 700, 60); return c
    route(c, P, lerp(22.4, 40, T.ease(T.LP*1.2)), 22.4, col=TEAL, dots=True); L(c, "HE NEVER MEANT TO", 900, 700, 76, bg=MARI); return c
def finq(k=0):
    c = sea("gold", sx=300); coast(c, 548, 1250, W+40, 150, (190, 196, 150), 2); vict(c, 470, 800, 520, torn=True, furl=1); wash(c, 812, "gold"); Q(c, 4, 4, HID); return c
def signed(k=0):
    c = quay("day", ships=1, sun=False); sidp(c, 900, 1030, 400, "self", "smile"); c.line([(1280, 1030), (1280, 560)], 14, TIMBER, False); c.calpage(1280, 600, 1.0, "PLAN", "2", "YEARS", c=TEAL); sack(c, 1620, 1030, 1.5); L(c, "YOU SIGNED ON FOR TWO YEARS AND A SPICE RUN", 210, 720, 52); return c
def came(k):
    if k == 0: c = C((238, 226, 204)); c.calpage(660, 580, 1.4, "PLAN", "2", "YEARS", c=GREY); c.strike(500, 600, 820, 20); c.calpage(1260, 580, 1.5, "TOOK", "3", "YEARS", c=RED); L(c, "YOU CAME HOME IN THREE", 180, 960, 70); return c
    if k == 1: c, P = wmap(); route(c, P, 26, 0, ship=False); route(c, P, lerp(30, 40, T.ease(T.LP)), 26, col=TEAL); place(c, P, "SANLUCAR"); L(c, "FROM THE WRONG DIRECTION", 900, 660, 66, bg=MARI); return c
    c = C((238, 226, 204)); c.calpage(560, 600, 1.4, "SHIP", "WED", c=NAVY); c.calpage(1360, 600, 1.4, "SPAIN", "THU", c=DGREEN); c.text(960, 590, "≠", 190, RED); L(c, "WITH A DAY MISSING", 190, 960, 80, bg=MARI); return c
def fin(k):
    if k == 0:
        c = C((238, 226, 204)); sidp(c, 520, 1010, 400, "chin", "smug"); f = sailor(c, 1400, 1010, 380, "point", "smile", "rose", flip=True, cap=False); c.bubble(1220, 330, "MAGELLAN SAILED\nAROUND THE WORLD!", 62, (120, 150)); return c
    if k == 1:
        c = C((60, 52, 92)); sky(c, 760, "dusk", sun=False); c.rect(0, 760, W, H, (120, 104, 110), None); c.line([(0, 760), (W, 760)], 6, INK, False)
        for i in range(18): x = 110+(i % 9)*186+(i//9)*90; y = 920+(i//9)*110; f = shirt(c, x, y, 220+(i//9)*30, ("sad", "n", "sleep", "worry")[i % 4]); c.candle(f["hand"][0]+6, f["hand"][1]+26, .7, T.TT+i)
        L(c, "EIGHTEEN MEN, MOST OF THEM SICK", 190, 960, 70); return c
    c = deck("gold", mast=1640); e = elcano(c, 760, 1040, 540, "self", "smug"); L(c, "LED BY A PARDONED MUTINEER", 210, 1040, 66, bg=MARI)
    if k == 3: c.label(1300, 560, "JUAN SEBASTIÁN ELCANO", 60)
    return c

def Fq(n, t): g = lambda: qcard(n, t); g.scene = "qcard"+n; return g
# (narration, [frames], chime?)   Respellings are for the voice only; CAPTION_FIX restores the display forms.
U = [
 ("You're chewing ox hide that was part of the ship.", [F(chew, 0), F(chew, 1)]),
 ("A rat costs half a duckit, and you can't find one.", [F(ratp, 0), F(ratp, 1)]),
 ("Five ships left Spain. One finishes, with eighteen of the crew.", [F(five, 0), F(five, 1), F(five, 2)]),
 ("So here's the question. Are you one of the eighteen?", [F(q18, 0), F(q18, 1)], "chime"),
 ("It's fifteen nineteen. You're a sailor in Seville, and you've just signed on.", [F(card, "SEVILLE. 1519."), F(intro), F(signon)]),
 ("You are made up. The voyage isn't. A man named Antonio Pigafetta sailed with it and wrote it down.", [F(madeup), F(pigaf, 0), F(pigaf, 1)]),
 ("Here's your quest log. One: find a way through a continent.", [F(qsea, 0), F(qsea, 1)], "tick"),
 ("Two: cross whatever is on the other side.", [F(qsea, 2)], "tick"),
 ("Three: fill the ship with cloves.", [F(qsea, 3)], "tick"),
 ("There's a fourth quest hidden near the end. Nobody planned it. Not even the captain.", [F(qsea, 4), F(hiddenq, 1, 0), F(nocap)], "tick"),
 ("Why go at all? Cloves.", [F(why, 0), F(why, 1)]),
 ("They come from the Mo-luck-as, on the far side of the world. The Spice Islands.", [F(molmap, 0), F(molmap, 1)]),
 ("By one account, a hundred pounds of cloves costs about half a duckit out there. In Seville, the same hundred pounds is worth forty-two.", [F(price, 0), F(price, 1), F(price, 2), F(price, 3)]),
 ("Spain wants its own road to those islands. A captain named Ferdinand Magellan says he can find one by sailing west.", [F(road, 0), F(road, 1), F(road, 2)]),
 ("He's Portuguese. His own king turned him down.", [F(port, 0), F(port, 1)]),
 ("Recruiting goes badly. High risk, low pay, and mistrust of a Portuguese captain.", [F(recruit, 0), F(recruit, 1), F(recruit, 2)]),
 ("So foreigners are let in. Under two thirds of the crew are Spaniards.", [F(foreign, 0), F(foreign, 1)]),
 ("The trip is expected to take two years.", [F(twoy)]),
 ("Your ship is the Victoria. Forty-five men on the crew list, and a hull sixty-odd feet long.", [F(vic, 0), F(vic, 1), F(vic, 2)]),
 ("On the twentieth of September, fifteen nineteen, five ships and about two hundred and forty men leave Sanlúcar for the Atlantic.", [F(card, "20 SEPTEMBER 1519"), F(depart, 0), F(depart, 1)]),
 ("The headcounts don't agree. Pigafetta says two thirty-seven. Some histories say two seventy.", [F(heads, 0), F(heads, 1), F(heads, 2)]),
 ("Quest one. Find the way through.", [Fq("ONE", "FIND THE WAY THROUGH")], "tick"),
 ("By mid-December you're anchored in the bay that will be Rio de Janeiro.", [F(rio, 0), F(rio, 1)]),
 ("Then south. One huge river mouth looks like the gap. It's a river.", [F(plate, 0), F(plate, 1), F(plate, 2)]),
 ("On the last day of March, fifteen twenty, the fleet stops for the winter at Port Saint Julian.", [F(card, "31 MARCH 1520"), F(julian, 0), F(julian, 1)]),
 ("Within days, at midnight, the Spanish captains mutiny.", [F(mutiny, 0), F(mutiny, 1)]),
 ("Your ship is one of the ones that turns. Nobody asks you.", [F(turns, 0), F(turns, 1)]),
 ("Magellan wins. The accounts differ on the details. In one common version, your captain is killed in the fighting and another is executed.", [F(wins, 0), F(wins, 1), F(wins, 2), F(wins, 3)]),
 ("A nobleman who helped lead it is left on the shore with a priest when the fleet sails.", [F(maroon, 0), F(maroon, 1)]),
 ("Other mutineers are pardoned. One of them is an officer named Juan Sebastián Elcano. Remember that name.", [F(pardon, 0), F(pardon, 1), F(pardon, 2)]),
 ("You stay about five months. Pigafetta writes about a local man so tall that the sailors reach only to his waist. His measurement, not ours.", [F(stay), F(giant, 0), F(giant, 1), F(giant, 2)]),
 ("One ship, the Santiago, is wrecked in a storm while scouting south. The crew survives. Four ships.", [F(wreck, 0), F(wreck, 1), F(wreck, 2)]),
 ("In late August you sail again. On the twenty-first of October you round a cape, and the coast opens.", [F(again), F(cape, 0), F(cape, 1)]),
 ("This one isn't a river.", [F(notriver)]),
 ("It takes thirty-eight days. More than three hundred miles of rock, storms and currents.", [F(strait, 0), F(strait, 1), F(strait, 2)]),
 ("There are fires burning on the southern shore. It gets a name: the land of fire. Tierra del Fuego.", [F(fires, 0), F(fires, 1), F(fires, 2)]),
 ("Somewhere in the strait, the San Antonio vanishes. The fleet thinks she's lost. She has turned round and gone home.", [F(vanish, 0), F(vanish, 1), F(vanish, 2)]),
 ("On the twenty-eighth of November, three ships come out the far end. Magellan, they say, cried.", [F(card, "28 NOVEMBER 1520"), F(out, 0), F(out, 1)]),
 ("Quest one, complete.", [F(qdone, 1, "gold")], "chime"),
 ("Quest two. Cross whatever this is.", [Fq("TWO", "CROSS WHATEVER THIS IS")], "tick"),
 ("The water is calm, so Magellan calls it the Pacific.", [F(pacific, 0), F(pacific, 1)]),
 ("Then more than three months with no fresh food. Pigafetta makes it three months and twenty days.", [F(nofood, 0), F(nofood, 1), F(nofood, 2)]),
 ("The biscuit has turned to powder. It's crawling with worms, and it stinks of rat urine.", [F(bisc, 0), F(bisc, 1), F(bisc, 2)]),
 ("The water is yellow.", [F(water)]),
 ("You eat sawdust. You eat the ox hides off the main yard: four or five days in the sea to soften them, then onto the coals.", [F(sawdust), F(hides, 0), F(hides, 1), F(hides, 2)]),
 ("And rats sell for half a duckit each. About the price of a hundred pounds of cloves, where you're going.", [F(ratsell, 0), F(ratsell, 1), F(ratsell, 2)]),
 ("Then men's gums begin to swell.", [F(gums)]),
 ("Nineteen of the crew die of it, by Pigafetta's count. Other accounts say nearer thirty.", [F(dead19, 0), F(dead19, 1)]),
 ("He writes that he doesn't believe such a voyage will ever be repeated.", [F(never, 0), F(never, 1)]),
 ("On the sixth of March, fifteen twenty-one: land. And fresh food.", [F(card, "6 MARCH 1521"), F(land, 0), F(land, 1)]),
 ("The islanders steal the small boat tied to the flagship's stern. So the fleet names the place the Islands of Thieves.", [F(thieves, 0), F(thieves, 1), F(thieves, 2)]),
 ("The islanders probably had a name for you, too.", [F(nameyou)]),
 ("Quest two, complete. About four thousand leagues, by Pigafetta's reckoning.", [F(qdone, 2), F(leagues)], "chime"),
 ("Quest three. Cloves.", [Fq("THREE", "CLOVES")], "tick"),
 ("Ten days later you reach the islands that will be called the Philippines.", [F(phil, 0), F(phil, 1)]),
 ("On the island of Cebu, the rulers convert to Christianity.", [F(cebu, 0), F(cebu, 1)]),
 ("And here, Magellan stops behaving like a man on a spice run.", [F(stops)]),
 ("On nearby Mac-tahn, a chief named Lapulapu refuses to obey the king of Spain.", [F(lapu, 0), F(lapu, 1)]),
 ("Magellan decides to make him. His own men advise against it.", [F(advise, 0), F(advise, 1)]),
 ("On the twenty-seventh of April, sixty men go over in boats. Forty-nine wade in, up to their thighs.", [F(card, "27 APRIL 1521"), F(boats), F(wade)]),
 ("Pigafetta counts more than fifteen hundred waiting.", [F(waiting)]),
 ("Magellan is killed in the shallows. Pigafetta counts eight of the crew dead with him.", [F(killed, 0), F(killed, 1)]),
 ("Pigafetta calls him our mirror, our light, our comfort and our true guide.", [F(mirror, 0), F(mirror, 1)]),
 ("Four days later, the king of Cebu invites the commanders to a banquet. About two dozen men go ashore.", [F(banquet, 0), F(banquet, 1)]),
 ("It's a trap. They're killed while they eat.", [F(trap)]),
 ("Count heads. About a hundred of you are left. Too few to sail three ships.", [F(countc, 0), F(countc, 1)]),
 ("So you strip the Concepción and burn her.", [F(burn, 0), F(burn, 1)]),
 ("Two ships. No Magellan. Still no cloves.", [F(two, 0), F(two, 1), F(two, 2)]),
 ("It takes six more months. On the eighth of November, fifteen twenty-one, you anchor at Tee-door-ay, in the Spice Islands.", [F(sixm), F(card, "8 NOVEMBER 1521"), F(tidore, 0), F(tidore, 1)]),
 ("More than two years after leaving Spain. So much for two years, there and back.", [F(late, 0), F(late, 1)]),
 ("The sailors are entitled to a share of the cargo. So men sell their capes, their shoes, even their shirts.", [F(share), F(sell, 0), F(sell, 1), F(sell, 2)]),
 ("Quest three, complete.", [F(qdone, 3, "day", 2)], "chime"),
 ("Now the hidden one.", [F(hiddenq, 1, 3)]),
 ("Nobody set out to sail around the world. The job was a new road to these islands, and that's done.", [F(job, 0), F(job, 1), F(job, 2)]),
 ("Then, while the two ships are loading, the flagship springs a serious leak.", [F(leak, 0), F(leak, 1)]),
 ("So they split up. The Trinidad will be repaired and try to go back east, across the Pacific.", [F(split, 0), F(split, 1)]),
 ("She doesn't make it. She turns back, and the Portuguese capture her. By one count, four or five of her men ever see Europe again.", [F(trin, 0), F(trin, 1), F(trin, 2)]),
 ("Your ship goes the other way. West. Across the Indian Ocean and round the bottom of Africa.", [F(west, 0), F(west, 1)]),
 ("Her captain now is Juan Sebastián Elcano. The pardoned mutineer.", [F(elc, 0), F(elc, 1)]),
 ("Quest four: get home. And the way Elcano picks is the rest of the way round.", [F(q4, 0), F(q4, 1)], "tick"),
 ("On the twenty-first of December, the Victoria sails with sixty on board. Forty-seven of the crew and thirteen islanders.", [F(card, "21 DECEMBER 1521"), F(sixty, 0), F(sixty, 1)]),
 ("Elcano keeps well away from the coast, so the Portuguese can't catch you.", [F(away, 0), F(away, 1)]),
 ("That means months without touching land.", [F(months)]),
 ("Many of the men want to put in at Mozambique, which is Portuguese. The ship sails on.", [F(moz, 0), F(moz, 1)]),
 ("The Cape of Good Hope takes weeks. One version of Pigafetta says nine. Another says seven.", [F(capegh, 0), F(capegh, 1), F(capegh, 2)]),
 ("You get round it in May, fifteen twenty-two.", [F(roundc)]),
 ("In the two months after it, twenty-one men die.", [F(die21)]),
 ("Starving, Elcano risks one stop. The Cape Verde Islands. Portuguese.", [F(cv, 0), F(cv, 1)]),
 ("A boat goes ashore, and the men in it are told to ask one thing. What day is it?", [F(boat, 0), F(boat, 1)]),
 ("The Portuguese say Thursday.", [F(thu)]),
 ("On the ship, it's Wednesday.", [F(wed)]),
 ("The crew is amazed. Later, Pigafetta writes down the reason.", [F(amazed, 0), F(amazed, 1)]),
 ("You sailed west the whole way, the same way as the sun, and came back to where you started. Somewhere out there, you saw one sunrise fewer than Spain did.", [F(sunsc, 0), F(sunsc, 1), F(sunsc, 2), F(sunsc, 3)]),
 ("As far as anyone knows, no crew had ever lost a day this way before.", [F(lostday)]),
 ("Then the boat is seized, with thirteen men in it.", [F(seized)]),
 ("Elcano doesn't wait. The Victoria sets sail at once.", [F(flee, 0), F(flee, 1)]),
 ("On Saturday the sixth of September, fifteen twenty-two, you enter the bay at Sanlúcar. The ship only floats because the pumps never stop.", [F(card, "6 SEPTEMBER 1522"), F(home, 0), F(home, 1), F(pumps)]),
 ("Three years, less two weeks.", [F(three)]),
 ("Pigafetta counts eighteen of the crew left. Most of them sick.", [F(eighteen, 0), F(eighteen, 1)]),
 ("Three or four of the thirteen islanders are still aboard too. The sources differ.", [F(islanders3)]),
 ("Two days later, in Seville, the ship fires all her guns.", [F(guns, 0), F(guns, 1)]),
 ("The day after that, the eighteen walk to church. In their shirts. Barefoot. Each one holding a candle.", [F(walk, 0), F(walk, 1), F(walk, 2)]),
 ("So. Are you one of the eighteen? Roughly one man in thirteen was.", [F(one13, 0), F(one13, 1)]),
 ("But eighteen isn't everyone who lived.", [F(notall)]),
 ("The San Antonio, the ship that turned round in the strait, reached Seville in May fifteen twenty-one. By one count, about fifty-five men, home before you'd seen a single clove.", [F(sanant, 0), F(sanant, 1), F(sanant, 2), F(sanant, 3)]),
 ("The men seized at Cape Verde are counted among the survivors. So are the four or five from the Trinidad.", [F(tally, 0), F(tally, 1)]),
 ("Add them up, and about ninety men outlived the voyage. Eighteen of them brought the ship in.", [F(tally, 2), F(tally, 3)]),
 ("And the cloves? Three hundred and eighty-one sacks. About twenty-six tons.", [F(clovesc, 0), F(clovesc, 1)]),
 ("Worth more than all five ships cost. One cargo from five ships, and the voyage still made a profit.", [F(profit, 0), F(profit, 1)]),
 ("Elcano gets a coat of arms. A globe, and a line of Latin: you were the first to encircle me.", [F(arms, 0), F(arms, 1), F(arms, 2)]),
 ("Magellan gets his name on the strait, and most of the credit.", [F(credit, 0), F(credit, 1)]),
 ("He never went around the world. He never meant to.", [F(never2, 0), F(never2, 1)]),
 ("Quest four, complete.", [F(finq)], "chime"),
 ("You signed on for two years and a spice run.", [F(signed)]),
 ("You came home in three, from the wrong direction, with a day missing.", [F(came, 0), F(came, 1), F(came, 2)]),
 ("And the next time someone says Magellan sailed around the world, you'll know who finished it. Eighteen men, most of them sick, led by a pardoned mutineer.", [F(fin, 0), F(fin, 1), F(fin, 2), F(fin, 3)]),
]

CAPTION_FIX = [("Tee-door-ay", "Tidore"), ("duckit", "ducat"), ("Mo-luck-as", "Moluccas"), ("Mac-tahn", "Mactan"), ("fifteen nineteen", "1519"), ("fifteen twenty-one", "1521"), ("fifteen twenty-two", "1522"), ("fifteen twenty,", "1520,"),
               ("eighteen of the crew", "18 of the crew"), ("one of the eighteen", "one of the 18"), ("the eighteen walk", "the 18 walk"), ("eighteen isn't", "18 isn't"), ("Eighteen of them", "18 of them"), ("Eighteen men", "18 men"),
               ("Forty-five men", "45 men"), ("sixty-odd", "60-odd"), ("two hundred and forty", "240"), ("two thirty-seven", "237"), ("two seventy", "270"), ("thirty-eight days", "38 days"), ("three hundred miles", "300 miles"),
               ("forty-two", "42"), ("a hundred pounds", "100 pounds"), ("same hundred pounds", "same 100 pounds"), ("Nineteen of the crew", "19 of the crew"), ("nearer thirty", "nearer 30"), ("four thousand leagues", "4,000 leagues"),
               ("sixty men", "60 men"), ("Forty-nine wade", "49 wade"), ("fifteen hundred", "1,500"), ("About a hundred of you", "About 100 of you"), ("sixty on board", "60 on board"), ("Forty-seven of the crew", "47 of the crew"),
               ("thirteen islanders", "13 islanders"), ("twenty-one men", "21 men"), ("thirteen men", "13 men"), ("one man in thirteen", "one man in 13"), ("fifty-five men", "55 men"), ("ninety men", "90 men"),
               ("Three hundred and eighty-one", "381"), ("twenty-six tons", "26 tons"), ("twentieth of September", "20th of September"), ("twenty-first of October", "21st of October"), ("twenty-eighth of November", "28th of November"),
               ("sixth of March", "6th of March"), ("twenty-seventh of April", "27th of April"), ("eighth of November", "8th of November"), ("twenty-first of December", "21st of December"), ("sixth of September", "6th of September")]
