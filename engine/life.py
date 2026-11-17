import math, random, numpy as np
import thsq as T
from thsq import *
from PIL import Image, ImageDraw
T.TT = 0.0; T.LT = 9.0; T.LP = 1.0; T.GP = 1.0; T.FR = 0; T.PREV = set(); T.CUR = set()
def ease(x): x = max(0.0, min(1.0, x)); return 1-(1-x)**3
T.ease = ease
def _new(k): T.CUR.add(k); return k not in T.PREV
C = T.C
_init = C.__init__
def init(s, bg=PAPER): _init(s, bg); s.da = ImageDraw.Draw(s.im, "RGBA")
C.__init__ = init
_line = C.line
def line(s, pts, w=6, c=INK, boil=True):
    if boil and w <= 16 and len(pts) >= 2:
        r = random.Random(hash((T.FR//4, int(pts[0][0]), int(pts[0][1]), len(pts), int(pts[-1][0]))))
        a = 1.5 if math.hypot(pts[-1][0]-pts[0][0], pts[-1][1]-pts[0][1]) < 700 else 0.5
        pts = [(x+r.uniform(-a, a), y+r.uniform(-a, a)) for x, y in pts]
    _line(s, pts, w, c)
C.line = line
_label = C.label
def label(s, x, y, t, size=64, c=INK, bg=PAPER, o=INK):
    if _new(("L", t)):
        if T.LT < 0.03: return
        k = ease(T.LT/0.2); size = size*(0.6+0.4*k+0.12*math.sin(k*math.pi)); y = y+(1-k)*26
    w = s.tw(t, size*1.22)+52; x = min(max(x, w/2+84), W-w/2-84); y = min(max(y, size*0.9+70), H-size*0.9-70)
    _label(s, x, y, t, size, c, bg, o)
C.label = label
def redx(s, x, y, r=120, w=26):
    n = _new(("X", x, y)); a = ease(T.LT/0.14) if n else 1; b = ease((T.LT-0.12)/0.14) if n else 1
    if a > 0: s.line([(x-r, y-r), (x-r+2*r*a, y-r+2*r*a)], w, RED, False)
    if b > 0: s.line([(x+r, y-r), (x+r-2*r*b, y-r+2*r*b)], w, RED, False)
C.redx = redx
def strike(s, x0, y, x1, w=14):
    a = ease(T.LT/0.22) if _new(("S", x0, y)) else 1
    if a > 0: s.line([(x0, y+8), (x0+(x1-x0)*a, y+8-16*a)], w, RED, False)
C.strike = strike
def tick(s, x, y, r=22, c=TEAL):
    a = ease(T.LT/0.25) if _new(("T", int(x), int(y))) else 1
    p = [(x-r, y), (x-r*0.3, y+r*0.7), (x+r, y-r*0.8)]
    if a <= 0: return
    if a < 0.4: q = a/0.4; s.line([p[0], (p[0][0]+(p[1][0]-p[0][0])*q, p[0][1]+(p[1][1]-p[0][1])*q)], 10, c, False)
    else: q = (a-0.4)/0.6; s.line([p[0], p[1], (p[1][0]+(p[2][0]-p[1][0])*q, p[1][1]+(p[2][1]-p[1][1])*q)], 10, c, False)
C.tick = tick
def card(s, t, size=150, sub=None, c=INK):
    s.rect(0, 0, W, H, PAPER, None); new = _new(("C", t)); n = len(t) if not new else int(len(t)*min(1, T.LT/0.45)+0.999)
    w = s.tw(t, size); yy = H/2-(40 if sub else 0)
    if n > 0: s.text(W/2-w/2, yy, t[:n], size, c, "lm")
    if sub and (not new or T.LT > 0.7): s.text(W/2, H/2+130, sub, 70*(0.7+0.3*ease((T.LT-0.7)/0.2) if new else 1), INK)
C.card = card
_marker = C.marker
def marker(s, x, y, r=34): _marker(s, x, y+math.sin(T.TT*3.2+x*.01)*r*0.18, r)
C.marker = marker
def smoke(s, x, y, n=3):
    for i in range(n+2):
        q = ((i*0.2+T.TT*0.22) % 1.0); r = 16+q*34; xx = x+q*90+math.sin(T.TT*1.3+i)*8; yy = y-q*190
        s.da.ellipse([(xx-r)*S, (yy-r)*S, (xx+r)*S, (yy+r)*S], fill=(255, 255, 255, int(235*(1-q*0.8))), outline=(140, 140, 140, int(200*(1-q))), width=3*S)
C.smoke = smoke
_fire = C.fire
def fire(s, x, y, k=1.0):
    s.da.ellipse([(x-260*k)*S, (y-200*k)*S, (x+260*k)*S, (y+90*k)*S], fill=(255, 170, 60, 38+int(14*math.sin(T.TT*9))))
    _fire(s, x, y, k*(1+0.07*math.sin(T.TT*12)+0.04*math.sin(T.TT*19)))
C.fire = fire
_quest = C.quest
def quest(s, shown=4, done=0, hidden=None, x=1040, y=170, z=1.36):
    x = min(x, 990)
    if _new(("Q",)): x = x+(1-ease(T.LT/0.32))*950
    _quest(s, shown, done, hidden, x, y, z)
C.quest = quest
_G = {}
def _grad(h, c0, c1):
    k = (h, c0, c1)
    if k not in _G:
        t = np.linspace(0, 1, h*S)[:, None, None]; a = (np.array(c0)[None, None, :]*(1-t)+np.array(c1)[None, None, :]*t).astype(np.uint8)
        _G[k] = Image.fromarray(np.repeat(a, W*S, axis=1), "RGB")
    return _G[k]
SKIES = {"sand": ((140, 200, 226), (232, 242, 236)), "field": ((140, 200, 226), (232, 242, 236)), "flood": ((150, 196, 216), (226, 236, 232)),
         "river": ((140, 200, 226), (232, 242, 236)), "night": ((16, 22, 48), (58, 70, 112)), "dusk": ((52, 56, 108), (238, 156, 122))}
_bg = C.bg
def bg(s, kind="sand", hz=700):
    _bg(s, kind, hz)
    if kind in SKIES:
        s.im.paste(_grad(hz, *SKIES[kind]), (0, 0))
        if kind == "night":
            for i in range(60):
                x = (i*197) % W; y = (i*89) % (hz-40)+10; r = 3+2*math.sin(T.TT*2+i); s.da.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=(255, 248, 236, 230))
        else:
            if kind != "dusk":
                s.da.ellipse([1560*S, -10*S, 1870*S, 300*S], fill=(255, 220, 120, 60)); s.ell(1640, 70, 1790, 220, MARI, INK, 6)
            for i, (cx, cy, k) in enumerate(((300, 150, 1.0), (980, 90, .7), (1380, 230, .85))):
                xx = (cx+T.TT*(7+3*i)) % (W+400)-200
                for dx, dy, r in ((-70, 10, 44), (0, -14, 60), (70, 12, 46), (0, 22, 50)): s.da.ellipse([(xx+dx*k-r*k*1.5)*S, (cy+dy*k-r*k)*S, (xx+dx*k+r*k*1.5)*S, (cy+dy*k+r*k)*S], fill=(255, 255, 255, 215 if kind != "dusk" else 120))
        if kind == "sand":
            s.poly([(0, hz), (0, hz-50), (380, hz-110), (760, hz-40), (1100, hz-90), (1500, hz-30), (W, hz-70), (W, hz)], (226, 196, 140), None)
        s.line([(0, hz), (W, hz)], 6, INK, False)
        if kind in ("flood", "river"):
            pass
    return s
C.bg = bg
_fig = C.fig
def fig(s, x, y, h=300, pose="stand", ex="n", who="sid", flip=False, rot=0, sit=False, **o):
    ph = x*0.013+y*0.007; br = 1+0.014*math.sin(T.TT*2.4+ph*9)
    if pose == "pull": x = x+7*math.sin(T.TT*6+ph*3); br = 1+0.03*math.sin(T.TT*6+ph*3)
    if pose in ("cheer", "wave"): br = 1+0.03*math.sin(T.TT*7+ph*5)
    if ((T.TT+ph*5.3) % 3.3) < 0.13 and ex not in ("wow", "sleep", "pain", "joy2"): o["blink"] = True
    if rot == 0:
        w = h*0.42; s.da.ellipse([(x-w)*S, (y-14)*S, (x+w)*S, (y+22)*S], fill=(40, 30, 20, 46))
    return _fig(s, x, y, h*br if rot == 0 else h, pose, ex, who, flip, rot, sit, **o)
C.fig = fig

_questlog = C.questlog
def questlog(s, rows, shown=4, done=0, hidden=None, x=1040, y=170, z=1.36):
    x = min(x, 990)
    if _new(("Q",)): x = x+(1-ease(T.LT/0.32))*950
    _questlog(s, rows, shown, done, hidden, x, y, z)
C.questlog = questlog
