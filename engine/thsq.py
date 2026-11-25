from PIL import Image, ImageDraw, ImageFont
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)); FDIR = HERE + "/fonts/"
OUTROOT = _os.environ.get("THSQ_OUT", _os.path.join(_os.path.dirname(HERE), "out"))
import math
S = 2; W, H = 1920, 1080
INK=(31,27,22); PAPER=(255,248,236); MARI=(242,179,61); TEAL=(31,167,160); RED=(224,79,58); NAVY=(35,48,74); EARTH=(184,135,90)
SAND=(238,212,158); DSAND=(214,180,120); SKY=(202,230,234); GREY=(206,194,174); WATER=(126,186,208); STONE=(240,232,212)
MUD=(178,132,92); WHITE=(255,255,255); BARLEY=(222,196,104); DUSK=(74,84,120); PINK=(236,170,150)
_F = {}
def FONT(size, name="PatrickHandSC-Regular.ttf"):
    k = (name, int(size))
    if k not in _F: _F[k] = ImageFont.truetype(FDIR + name, int(size))
    return _F[k]

def rr_pts(cx, cy, w, h, r, n=6):
    pts = []
    for ox, oy, a0 in ((w/2-r, h/2-r, 0), (-w/2+r, h/2-r, 90), (-w/2+r, -h/2+r, 180), (w/2-r, -h/2+r, 270)):
        for i in range(n+1):
            a = math.radians(a0 + 90*i/n); pts.append((cx+ox+r*math.cos(a), cy+oy+r*math.sin(a)))
    return pts

class C:
    def __init__(s, bg=PAPER):
        s.im = Image.new("RGB", (W*S, H*S), bg); s.d = ImageDraw.Draw(s.im)
    def P(s, pts): return [(x*S, y*S) for x, y in pts]
    def line(s, pts, w=6, c=INK):
        p = s.P(pts); s.d.line(p, fill=c, width=max(1, int(w*S)), joint="curve")
        r = w*S/2
        for x, y in (p[0], p[-1]): s.d.ellipse([x-r, y-r, x+r, y+r], fill=c)
    def poly(s, pts, f, o=INK, w=6):
        if f: s.d.polygon(s.P(pts), fill=f)
        if o: s.line(list(pts)+[pts[0]], w, o)
    def rect(s, x0, y0, x1, y1, f, o=INK, w=6, r=0):
        s.d.rounded_rectangle([x0*S, y0*S, x1*S, y1*S], radius=r*S, fill=f, outline=o, width=int(w*S) if o else 0)
    def ell(s, x0, y0, x1, y1, f, o=INK, w=6):
        s.d.ellipse([x0*S, y0*S, x1*S, y1*S], fill=f, outline=o, width=int(w*S) if o else 0)
    def text(s, x, y, t, size=90, c=INK, anchor="mm"):
        s.d.multiline_text((x*S, y*S), t, font=FONT(size*S), fill=c, anchor=anchor, align="center", spacing=size*S*0.15)
    def tw(s, t, size): return max(s.d.textlength(l, font=FONT(size*S)) for l in t.split("\n"))/S
    def out(s): return s.im.resize((W, H), Image.LANCZOS)

    # ---------- overlays ----------
    def label(s, x, y, t, size=64, c=INK, bg=PAPER, o=INK):
        size = size*1.22; w = s.tw(t, size)+52; x = min(max(x, w/2+24), W-w/2-24); y = max(y, size*0.8+24)
        w = w; n = t.count("\n")+1; h = size*1.25*n+24
        s.rect(x-w/2, y-h/2, x+w/2, y+h/2, bg, o, 5, 14); s.text(x, y-4, t, size, c)
    def card(s, t, size=150, sub=None, c=INK):
        s.rect(0, 0, W, H, PAPER, None); s.text(W/2, H/2-(40 if sub else 0), t, size, c)
        if sub: s.text(W/2, H/2+130, sub, 70, INK)
    def marker(s, x, y, r=34):
        s.poly([(x, y-r*1.3), (x+r, y), (x, y+r*1.3), (x-r, y)], TEAL, INK, 6)
    def redx(s, x, y, r=120, w=26):
        s.line([(x-r, y-r), (x+r, y+r)], w, RED); s.line([(x+r, y-r), (x-r, y+r)], w, RED)
    def strike(s, x0, y, x1, w=14): s.line([(x0, y+8), (x1, y-8)], w, RED)
    def tick(s, x, y, r=22, c=TEAL): s.line([(x-r, y), (x-r*0.3, y+r*0.7), (x+r, y-r*0.8)], 10, c)
    def quest(s, shown=4, done=0, hidden=None, x=1040, y=170, z=1.36):
        rows = ["GET TO GIZA", "EARN YOUR BREAD", "GET HOME IN ONE PIECE", hidden or "? ? ?"]
        s.rect(x, y, x+610*z, y+(150+shown*92)*z, PAPER, INK, 8, 26)
        s.marker(x+62*z, y+70*z, 24*z); s.text(x+110*z, y+66*z, "QUEST LOG", 70*z, INK, "lm")
        s.line([(x+30*z, y+125*z), (x+580*z, y+125*z)], 6)
        for i in range(shown):
            yy = y+(180+i*92)*z
            s.rect(x+34*z, yy-24*z, x+82*z, yy+24*z, WHITE, INK, 6, 8)
            if i < done: s.tick(x+58*z, yy, 18*z)
            if i == 3 and not hidden:
                s.rect(x+44*z, yy-8*z, x+72*z, yy+16*z, INK, None, 0, 4); s.d.arc([(x+48*z)*S, (yy-24*z)*S, (x+68*z)*S, (yy+4*z)*S], 180, 360, fill=INK, width=6*S)
            s.text(x+104*z, yy-4, rows[i], 52*z, INK if i >= done else (120, 110, 98), "lm")

    # ---------- backgrounds ----------
    def bg(s, kind="sand", hz=700):
        sky, ground = {"sand": (SKY, SAND), "field": (SKY, BARLEY), "flood": (SKY, WATER), "river": (SKY, WATER), "night": (NAVY, (120, 96, 70)),
                       "dusk": (DUSK, (150, 118, 92)), "room": ((244, 226, 196), (206, 160, 112)), "hall": ((150, 108, 74), (196, 152, 104)),
                       "paper": (PAPER, PAPER), "cave": ((120, 104, 92), (176, 132, 96))}[kind]
        s.rect(0, 0, W, hz, sky, None); s.rect(0, hz, W, H, ground, None)
        if kind != "paper": s.line([(0, hz), (W, hz)], 6)
        if kind in ("sand", "field", "flood", "river"): s.ell(1640, 70, 1790, 220, MARI, INK, 6)
        if kind == "field":
            for i in range(60):
                x = (i*137) % W; y = hz+30+(i*71) % (H-hz-60); s.line([(x, y), (x+6, y-34)], 5, (170, 140, 60))
        if kind in ("flood", "river"):
            for i in range(14):
                x = (i*263) % W; y = hz+50+(i*97) % (H-hz-90); s.line([(x, y), (x+50, y)], 5, WHITE)
        if kind == "night":
            for i in range(40): x = (i*197) % W; y = (i*89) % (hz-40)+10; s.ell(x, y, x+6, y+6, PAPER, None)
        if kind == "room": s.rect(1380, 150, 1700, 430, SKY, INK, 6)
        return s

    # ---------- props ----------
    def block(s, x, y, w=260, h=180, f=STONE): s.rect(x, y-h, x+w, y, f, INK, 7, 8)
    def sledge(s, x, y, w=320): s.rect(x-20, y-22, x+w+20, y, EARTH, INK, 6, 10); s.line([(x+w+20, y-12), (x+w+60, y-40)], 7)
    def pyramid(s, cx, by, w, h, f=STONE, prog=1.0, steps=0):
        if prog >= 1: s.poly([(cx-w/2, by), (cx, by-h), (cx+w/2, by)], f, INK, 7)
        else:
            t = prog; s.poly([(cx-w/2, by), (cx-w/2*(1-t), by-h*t), (cx+w/2*(1-t), by-h*t), (cx+w/2, by)], f, INK, 7)
        for i in range(1, steps):
            yy = by-h*min(prog, 1)*i/steps; k = (by-yy)/h; s.line([(cx-w/2*(1-k), yy), (cx+w/2*(1-k), yy)], 4, (190, 176, 150))
    def hut(s, x, y, w=200, h=140): s.rect(x, y-h, x+w, y, MUD, INK, 6, 6); s.rect(x+w*0.4, y-h*0.55, x+w*0.62, y, (90, 64, 44), INK, 5)
    def silo(s, x, y, w=120, h=190): s.d.pieslice([x*S, (y-h-w/2)*S, (x+w)*S, (y-h+w/2)*S], 180, 360, fill=MUD); s.rect(x, y-h, x+w, y, MUD, None); s.line([(x, y), (x, y-h)]); s.line([(x+w, y), (x+w, y-h)]); s.d.arc([x*S, (y-h-w/2)*S, (x+w)*S, (y-h+w/2)*S], 180, 360, fill=INK, width=6*S)
    def smoke(s, x, y, n=3):
        for i in range(n): r = 22+i*10; s.ell(x+i*26-r, y-i*46-r, x+i*26+r, y-i*46+r, WHITE, (150, 150, 150), 4)
    def boat(s, x, y, w=520):
        s.poly([(x, y-50), (x+w, y-50), (x+w-70, y+20), (x+70, y+20)], EARTH, INK, 7)
        s.line([(x, y-50), (x-40, y-110)], 9); s.line([(x+w, y-50), (x+w+40, y-110)], 9)
    def jar(s, x, y, k=1.0, foam=True):
        s.poly([(x-34*k, y), (x-48*k, y-70*k), (x-26*k, y-120*k), (x+26*k, y-120*k), (x+48*k, y-70*k), (x+34*k, y)], (200, 120, 80), INK, 6)
        if foam:
            for dx in (-22, 0, 22): s.ell(x+(dx-20)*k, y-150*k, x+(dx+20)*k, y-112*k, WHITE, INK, 5)
    def loaf(s, x, y, k=1.0): s.ell(x-46*k, y-44*k, x+46*k, y, (226, 168, 92), INK, 6); s.line([(x-14*k, y-32*k), (x+2*k, y-14*k)], 4); s.line([(x+8*k, y-34*k), (x+24*k, y-16*k)], 4)
    def papyrus(s, x, y, k=1.0):
        s.rect(x-90*k, y-60*k, x+90*k, y+60*k, (236, 214, 160), INK, 6, 6)
        for i in range(4): s.line([(x-66*k, y-34*k+i*22*k), (x+66*k-(i % 2)*30*k, y-34*k+i*22*k)], 4, (120, 100, 70))
        s.ell(x-104*k, y-66*k, x-76*k, y+66*k, (220, 196, 140), INK, 6)
    def bone(s, x0, y0, x1, y1, c=WHITE, brk=False):
        s.line([(x0, y0), (x1, y1)], 26, INK); s.line([(x0, y0), (x1, y1)], 16, c)
        for x, y in ((x0, y0), (x1, y1)): s.ell(x-18, y-18, x+18, y+18, c, INK, 5)
        if brk:
            mx, my = (x0+x1)/2, (y0+y1)/2; s.line([(mx-14, my-22), (mx+4, my-4), (mx-6, my+6), (mx+14, my+22)], 7, RED)
    def animal(s, x, y, k=1.0, body=(170, 120, 80), horn=True):
        s.ell(x-80*k, y-120*k, x+70*k, y-40*k, body, INK, 6)
        for dx in (-50, -20, 20, 48): s.line([(x+dx*k, y-50*k), (x+dx*k, y)], 7)
        s.ell(x+50*k, y-150*k, x+118*k, y-92*k, body, INK, 6); s.ell(x+92*k, y-128*k, x+100*k, y-120*k, INK, None)
        if horn: s.line([(x+70*k, y-146*k), (x+62*k, y-176*k)], 6); s.line([(x+96*k, y-146*k), (x+108*k, y-174*k)], 6)
    def fire(s, x, y, k=1.0):
        s.poly([(x-40*k, y), (x-52*k, y-60*k), (x-20*k, y-40*k), (x, y-110*k), (x+22*k, y-44*k), (x+50*k, y-66*k), (x+40*k, y)], (240, 120, 50), INK, 6)
        s.poly([(x-16*k, y), (x-20*k, y-36*k), (x, y-62*k), (x+18*k, y-34*k), (x+16*k, y)], MARI, None)
    def tomb(s, x, y, w=130, h=90): s.d.pieslice([x*S, (y-h-30)*S, (x+w)*S, (y-h+50)*S], 180, 360, fill=MUD, outline=INK, width=6*S); s.rect(x, y-h+10, x+w, y, MUD, INK, 6); s.rect(x+w*0.38, y-h*0.5, x+w*0.62, y, (80, 58, 42), None)
    def truck(s, x, y, k=1.0):
        s.rect(x, y-90*k, x+300*k, y-30*k, TEAL, INK, 6, 10); s.rect(x+170*k, y-150*k, x+270*k, y-90*k, TEAL, INK, 6, 10); s.rect(x+190*k, y-138*k, x+255*k, y-96*k, SKY, INK, 4)
        for dx in (60, 235): s.ell(x+(dx-34)*k, y-64*k, x+(dx+34)*k, y+4*k, INK, None); s.ell(x+(dx-12)*k, y-42*k, x+(dx+12)*k, y-18*k, GREY, None)

    # ---------- figure ----------
    def fig(s, x, y, h=300, pose="stand", ex="n", who="sid", flip=False, rot=0, sit=False, **o):
        P = {"stand": ((-.45, 1.0), (.45, 1.0), -.2, .2, 0), "walk": ((-.55, .9), (.6, .8), -.45, .45, .05), "run": ((-.8, .3), (.85, .5), -.75, .7, .3),
             "pull": ((.95, .3), (1.05, .5), -.7, .3, .5), "point": ((-.45, 1.0), (1.15, -.05), -.2, .2, 0), "self": ((-.45, 1.0), (.12, .5), -.2, .2, 0),
             "shrug": ((-.85, .15), (.85, .15), -.2, .2, 0), "wave": ((-.45, 1.0), (.7, -.95), -.2, .2, 0), "cheer": ((-.7, -.95), (.7, -.95), -.25, .25, 0),
             "hold": ((.45, .5), (.8, .45), -.2, .2, 0), "carry": ((-.35, -.95), (.35, -.95), -.3, .3, 0), "chin": ((-.45, 1.0), (.22, -.15), -.2, .2, 0),
             "drop": ((-.6, 1.05), (.6, 1.05), -.2, .2, 0), "write": ((.3, .6), (.7, .35), -.2, .2, .1), "pour": ((.6, .2), (.9, .0), -.4, .35, .2),
             "up": ((-.45, 1.0), (.5, -1.0), -.2, .2, -.05)}[pose]
        h = h*1.25; u = h/3.5; d = -1 if flip else 1; ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        dn = 1.1*u if sit else 0
        def T(px, py):
            px *= d; py += dn if py < -0.01 else 0
            return (x+px*ca-py*sa, y+px*sa+py*ca)
        lw = max(4, u*0.075); lean = P[4]*u
        hip = (0, -1.3*u); sh = (lean, -2.3*u); hc = (lean*1.15, -3.0*u)
        # legs
        if sit: feet = ((0.95*u, -1.2*u-0.0), (1.1*u, -1.05*u))
        else: feet = ((P[2]*u, 0), (P[3]*u, 0))
        for i, (fx, fy) in enumerate(feet):
            hp = (hip[0]+(-.16 if i == 0 else .16)*u, hip[1])
            s.line([T(*hp), T(fx, fy)], lw); bx, by = T(fx+0.1*u, fy-0.06*u)
            s.ell(bx-0.17*u, by-0.11*u, bx+0.17*u, by+0.11*u, INK, None)
        # back arm
        hands = []
        for i in (0, 1):
            a = P[i]; shp = (sh[0]+(-.3 if i == 0 else .3)*u, sh[1]+0.15*u); hd = (shp[0]+a[0]*u, shp[1]+a[1]*u); hands.append((shp, hd))
        def arm(i):
            shp, hd = hands[i]; s.line([T(*shp), T(*hd)], lw); hx, hy = T(*hd); s.ell(hx-.12*u, hy-.12*u, hx+.12*u, hy+.12*u, PAPER, INK, max(3, lw*0.7))
        arm(0)
        # torso
        tc = {"sid": MARI, "modern": MARI, "extra": GREY, "boss": TEAL, "scribe": GREY, "greek": WHITE, "sci": WHITE, "chain": (190, 150, 140)}.get(who, TORSO2.get(who, GREY))
        a0, a1 = T(hip[0], hip[1]-0.1*u), T(sh[0]*0.9, sh[1]+0.05*u)
        s.line([a0, a1], 0.86*u+lw*2, INK); s.line([a0, a1], 0.86*u, tc)
        if who in ("sid", "extra", "boss", "scribe", "chain"):
            k = [(-.47, -1.8), (.47, -1.8), (.6, -1.05), (-.6, -1.05)]
            s.poly([T(lean*.3+a*u, b*u) for a, b in k], WHITE, INK, lw)
            s.line([T(lean*.3-.47*u, -1.8*u), T(lean*.3+.47*u, -1.8*u)], lw*2.2, MARI if who == "sid" else EARTH)
        if who in ("greek", "sci"):
            k = [(-.5, -2.2), (.5, -2.2), (.62, -.35), (-.62, -.35)]
            s.poly([T(lean*.3+a*u, b*u) for a, b in k], WHITE if who == "sci" else (226, 214, 236), INK, lw)
        # head
        hw, hh = 1.18*u, 1.0*u
        s.poly([T(px, py) for px, py in rr_pts(hc[0], hc[1], hw, hh, 0.3*u)], PAPER, INK, lw)
        if who in ("sid", "modern"):
            top = hc[1]-hh/2; s.line([T(hc[0]-.06*u, top), T(hc[0]+.04*u, top-.26*u), T(hc[0]+.3*u, top-.32*u), T(hc[0]+.36*u, top-.12*u), T(hc[0]+.22*u, top-.1*u)], lw)
        if who == "greek": s.poly([T(hc[0]+.0*u, hc[1]+.38*u), T(hc[0]+.5*u, hc[1]+.38*u), T(hc[0]+.3*u, hc[1]+.85*u)], (120, 110, 100), INK, lw*.8)
        if who == "boss": s.line([T(hc[0]-.6*u, hc[1]-.5*u), T(hc[0]+.6*u, hc[1]-.5*u)], lw*2.4, TEAL)
        fx = hc[0]+.1*u; ey = hc[1]-.05*u
        def seg(pts, w=None, c=INK): s.line([T(fx+a*u, ey+b*u) for a, b in pts], w or lw*.9, c)
        def arcpts(cx, cy, r, a0, a1, n=8): return [(cx+r*math.cos(math.radians(a0+(a1-a0)*i/n)), cy+r*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]
        el, er = -.22, .24
        if ex in ("sleep", "pain", "joy2") or o.get("blink"): seg([(el-.08, 0), (el+.08, 0)]); seg([(er-.08, 0), (er+.08, 0)])
        elif ex == "bored": seg([(el, -.02), (el, .08)]); seg([(er, -.02), (er, .08)]); seg([(el-.1, -.08), (el+.1, -.08)], lw*.6); seg([(er-.1, -.08), (er+.1, -.08)], lw*.6)
        elif ex == "wow":
            for e in (el, er): cx, cy = T(fx+e*u, ey); s.ell(cx-.07*u, cy-.09*u, cx+.07*u, cy+.09*u, INK, None)
        else: seg([(el, -.1), (el, .1)]); seg([(er, -.1), (er, .1)])
        if ex in ("worry", "sad"): seg([(el-.12, -.2), (el+.1, -.28)], lw*.6); seg([(er-.1, -.28), (er+.12, -.2)], lw*.6)
        if ex in ("strain", "det", "smug", "angry"): seg([(el-.12, -.28), (el+.1, -.2)], lw*.6); seg([(er-.1, -.2), (er+.12, -.28)], lw*.6)
        my = .28
        if ex in ("n", "bored", "det"): seg([(-.1, my), (.14, my)])
        elif ex in ("smile", "smug"): seg(arcpts(.02, my-.1, .16, 30, 150))
        elif ex in ("joy", "joy2"): s.poly([T(fx+a*u, ey+b*u) for a, b in [(-.16, my-.06), (.2, my-.06)]+arcpts(.02, my-.06, .18, 0, 180)], RED, INK, lw*.7)
        elif ex in ("worry", "sad"): seg(arcpts(.02, my+.14, .15, 210, 330))
        elif ex in ("wow", "sleep", "pain"): cx, cy = T(fx+.02*u, ey+my*u); r = .09*u if ex != "pain" else .13*u; s.ell(cx-r, cy-r, cx+r, cy+r, INK, None)
        elif ex in ("strain", "angry"): seg([(-.14, my), (-.05, my-.05), (.04, my), (.13, my-.05), (.2, my)])
        if ex == "strain": cx, cy = T(hc[0]-.75*u, hc[1]-.2*u); s.poly([(cx, cy-16), (cx+10, cy+8), (cx-10, cy+8)], WATER, INK, 3)
        arm(1)
        if o.get("staff"): hx, hy = T(*hands[1][1]); s.line([(hx, hy-0.9*u), (hx, y)], lw*1.2, EARTH)
        return {"hand": T(*hands[1][1]), "hand0": T(*hands[0][1]), "head": T(hc[0], hc[1]-hh/2), "u": u}

# ================= EP002 kit: New York, 1929 (new methods only; nothing above is changed) =================
CONC = (214, 206, 196); BRICK = (188, 108, 84); GREEN = (140, 178, 128); DGREEN = (86, 132, 96); BRASS = (214, 170, 80)
WOOD = (150, 108, 74); WALL = (244, 226, 196); MARBLE = (236, 232, 224); CREAM = (250, 240, 214); SLATE = (104, 112, 136)
TORSO2 = {"broker": NAVY, "banker": (88, 84, 96), "teal": TEAL, "brown": EARTH, "rose": PINK, "blue": WATER, "green": GREEN, "red": RED, "slate": SLATE}
import random as _rnd

def _kit(f): setattr(C, f.__name__, f); return f

@_kit
def person(s, x, y, h=300, pose="stand", ex="n", coat="slate", hat=None, tie=None, flip=False, hc=None, **o):
    """A 1929 extra: plain figure in a coloured coat (a TORSO2 key), optional hat and tie. Returns the fig dict."""
    f = s.fig(x, y, h, pose, ex, coat, flip, **o); u = f["u"]; hx, hy = f["head"]
    if tie and not o.get("rot"):
        nx, ny = hx, hy+1.16*u
        s.poly([(nx-.1*u, ny), (nx+.1*u, ny), (nx+.07*u, ny+.46*u), (nx, ny+.6*u), (nx-.07*u, ny+.46*u)], tie, INK, max(3, u*.04))
    if hat and not o.get("rot"): s.hat(f, hat, hc or {"fedora": (96, 88, 84), "top": INK, "cap": EARTH, "bowler": (70, 64, 60), "cloche": RED}.get(hat, INK))
    return f

@_kit
def hat(s, f, kind="fedora", c=(96, 88, 84)):
    u = f["u"]; x, y = f["head"]; lw = max(4, u*0.075)
    if kind == "fedora":
        s.poly([(x-.5*u, y+.06*u), (x-.42*u, y-.4*u), (x-.08*u, y-.33*u), (x+.3*u, y-.42*u), (x+.5*u, y+.06*u)], c, INK, lw)
        s.line([(x-.5*u, y+.0*u), (x+.5*u, y+.0*u)], lw*2, INK); s.line([(x-.86*u, y+.1*u), (x+.86*u, y+.1*u)], lw*1.6, INK)
    elif kind == "top":
        s.rect(x-.48*u, y-.82*u, x+.48*u, y+.08*u, c, INK, lw); s.line([(x-.47*u, y-.08*u), (x+.47*u, y-.08*u)], lw*2, RED); s.line([(x-.84*u, y+.1*u), (x+.84*u, y+.1*u)], lw*1.6, INK)
    elif kind == "cap":
        s.d.pieslice([(x-.62*u)*S, (y-.42*u)*S, (x+.62*u)*S, (y+.5*u)*S], 180, 360, fill=c, outline=INK, width=int(lw*S)); s.line([(x-.62*u, y+.05*u), (x+.95*u, y+.08*u)], lw*1.5, INK)
    elif kind == "bowler":
        s.d.pieslice([(x-.56*u)*S, (y-.6*u)*S, (x+.56*u)*S, (y+.6*u)*S], 180, 360, fill=c, outline=INK, width=int(lw*S)); s.line([(x-.8*u, y+.04*u), (x+.8*u, y+.04*u)], lw*1.6, INK)
    elif kind == "cloche":
        s.d.pieslice([(x-.66*u)*S, (y-.5*u)*S, (x+.66*u)*S, (y+.7*u)*S], 180, 360, fill=c, outline=INK, width=int(lw*S)); s.line([(x-.66*u, y+.1*u), (x+.66*u, y+.1*u)], lw*1.3, INK)

@_kit
def glasses(s, f):
    u = f["u"]; x, y = f["head"]; cy = y+.45*u
    for dx in (-.14, .34): s.ell(x+(dx-.19)*u, cy-.17*u, x+(dx+.19)*u, cy+.17*u, None, INK, max(3, u*.05))
    s.line([(x+.05*u, cy), (x+.15*u, cy)], max(3, u*.05))

@_kit
def skyline(s, hz, seed=3, c=(170, 178, 200), lit=(250, 236, 180), x0=0, x1=W, hmin=120, hmax=420, o=INK, win=True, dens=.6):
    r = _rnd.Random(seed); x = x0
    while x < x1:
        w = min(r.randint(96, 190), x1-x); h = r.randint(hmin, hmax); t = r.random()
        if w < 40: break
        if t < .3: s.rect(x+w*.3, hz-h-46, x+w*.7, hz-h+6, c, o, 5); s.line([(x+w*.5, hz-h-46), (x+w*.5, hz-h-96)], 5, o or INK)
        elif t < .45: s.poly([(x+w*.2, hz-h+4), (x+w*.5, hz-h-70), (x+w*.8, hz-h+4)], c, o, 5)
        s.rect(x, hz-h, x+w, hz+4, c, o, 5)
        if win:
            for wy in range(int(hz-h+24), int(hz-34), 46):
                for wx in range(int(x+18), int(x+w-30), 36):
                    if r.random() < dens: s.rect(wx, wy, wx+16, wy+26, lit, None)
        x += w-5

@_kit
def bankfront(s, x, y, w=560, h=420, name="BANK", closed=False, f=MARBLE, size=None, door=(90, 64, 44)):
    """Classical bank: steps, four columns, pediment, name on the frieze. (x, y) = left end of the ground line."""
    s.rect(x-34, y-22, x+w+34, y, CONC, INK, 6); s.rect(x-16, y-44, x+w+16, y-22, CONC, INK, 6)
    top = y-44-h; s.rect(x, top+h*.3, x+w, y-44, f, INK, 7)
    dw = w*.2; s.rect(x+w/2-dw/2, y-44-h*.44, x+w/2+dw/2, y-44, door, INK, 6, 6); s.line([(x+w/2, y-44-h*.44), (x+w/2, y-44)], 4)
    for q in (.09, .31, .69, .91):
        cx = x+w*q; s.rect(cx-w*.036, top+h*.33, cx+w*.036, y-62, WHITE, INK, 6)
        for dx in (-.014, .014): s.line([(cx+w*dx, top+h*.37), (cx+w*dx, y-70)], 3, (190, 186, 178))
        s.rect(cx-w*.054, top+h*.3, cx+w*.054, top+h*.345, WHITE, INK, 5); s.rect(cx-w*.054, y-66, cx+w*.054, y-44, WHITE, INK, 5)
    s.rect(x-22, top+h*.15, x+w+22, top+h*.3, f, INK, 7)
    s.poly([(x-36, top+h*.15), (x+w/2, top-h*.08), (x+w+36, top+h*.15)], f, INK, 7)
    sz = size or min(h*.105, (w-30)/max(4, len(name))*1.75); s.text(x+w/2, top+h*.222, name, sz)
    if closed:
        s.rect(x+w/2-dw*1.1, y-44-h*.33, x+w/2+dw*1.1, y-44-h*.17, PAPER, INK, 5, 6); s.text(x+w/2, y-44-h*.255, "CLOSED", h*.1, RED)
    return (x+w/2, y-44)

@_kit
def shopfront(s, x, y, w=480, h=380, name="BROKER", f=BRICK, awn=TEAL, glass=SKY):
    s.rect(x, y-h, x+w, y, f, INK, 7); s.rect(x+w*.08, y-h*.62, x+w*.56, y-h*.14, glass, INK, 6)
    s.rect(x+w*.66, y-h*.62, x+w*.9, y, (90, 64, 44), INK, 6, 4); s.ell(x+w*.84, y-h*.3, x+w*.87, y-h*.26, BRASS, INK, 3)
    s.rect(x+w*.06, y-h*.92, x+w*.94, y-h*.72, PAPER, INK, 6, 8); s.text(x+w/2, y-h*.825, name, min(h*.13, (w*.84)/max(4, len(name))*1.7))
    n = 7
    for i in range(n):
        xa = x-10+(w+20)*i/n; xb = x-10+(w+20)*(i+1)/n
        s.poly([(xa, y-h*.7), (xb, y-h*.7), (xb, y-h*.6), ((xa+xb)/2, y-h*.56), (xa, y-h*.6)], awn if i % 2 == 0 else PAPER, INK, 4)

@_kit
def door(s, x, y, w=250, h=440, n="1", col=TEAL, name=None, open=0.0, dim=False):
    """Numbered door. (x, y) = bottom centre. open 0..1 swings it; dim greys it out."""
    fc = (218, 212, 204) if dim else col; fr = (150, 144, 136) if dim else WOOD
    s.rect(x-w/2-18, y-h-18, x+w/2+18, y, fr, INK, 7, 6); s.rect(x-w/2, y-h, x+w/2, y, (48, 40, 36), INK, 5)
    dw = w*(1-0.72*open)
    s.rect(x-w/2, y-h, x-w/2+dw, y, fc, INK, 6)
    if dw > w*.5:
        for yy0, yy1 in ((.92, .56), (.46, .08)): s.rect(x-w/2+dw*.14, y-h*yy0, x-w/2+dw*.86, y-h*yy1, None, INK, 4, 4)
    s.ell(x-w/2+dw*.8-11, y-h*.5-11, x-w/2+dw*.8+11, y-h*.5+11, BRASS, INK, 4)
    s.ell(x-58, y-h-150, x+58, y-h-34, PAPER if not dim else (232, 226, 216), INK, 7); s.text(x, y-h-96, str(n), 84, INK if not dim else (150, 144, 136))
    if name:
        tw = s.tw(name, 50)+44; s.rect(x-tw/2, y+26, x+tw/2, y+96, PAPER if not dim else (236, 230, 220), INK, 5, 12); s.text(x, y+58, name, 50, INK if not dim else (150, 144, 136))

@_kit
def bill(s, x, y, k=1.0, c=GREEN, t="$"):
    s.rect(x-80*k, y-38*k, x+80*k, y+38*k, c, INK, max(3, 5*k), 6*k); s.rect(x-66*k, y-26*k, x+66*k, y+26*k, None, DGREEN, max(2, 3*k), 4*k)
    s.ell(x-22*k, y-22*k, x+22*k, y+22*k, CREAM, INK, max(2, 3*k)); s.text(x, y-2*k, t, 38*k)

@_kit
def cash(s, x, y, n=6, k=1.0, c=GREEN):
    """A stack of n notes standing on y, centred on x. Returns the y of the top."""
    n = max(0, int(n))
    for i in range(n):
        yy = y-i*13*k
        s.rect(x-80*k, yy-16*k, x+80*k, yy, c, INK, max(3, 4*k), 3*k)
    if n:
        yy = y-(n-1)*13*k-16*k
        s.poly([(x-80*k, yy), (x-56*k, yy-30*k), (x+104*k, yy-30*k), (x+80*k, yy)], c, INK, max(3, 4*k)); s.text(x+12*k, yy-16*k, "$", 26*k)
        s.rect(x-14*k, y-(n-1)*13*k-16*k, x+14*k, y, PAPER, INK, max(2, 3*k))
    return y-n*13*k-30*k

@_kit
def coin(s, x, y, r=40, t="$", c=MARI):
    s.ell(x-r, y-r, x+r, y+r, c, INK, max(3, r*.14)); s.ell(x-r*.74, y-r*.74, x+r*.74, y+r*.74, None, (190, 140, 40), max(2, r*.07)); s.text(x, y-r*.06, t, r*1.1)

@_kit
def moneybag(s, x, y, k=1.0, c=(196, 170, 120)):
    s.ell(x-70*k, y-130*k, x+70*k, y, c, INK, 6*k); s.poly([(x-30*k, y-124*k), (x-44*k, y-176*k), (x+44*k, y-176*k), (x+30*k, y-124*k)], c, INK, 6*k)
    s.line([(x-34*k, y-128*k), (x+34*k, y-128*k)], 7*k, EARTH); s.text(x, y-64*k, "$", 72*k)

@_kit
def bed(s, x, y, w=620, lift=0.0, cashn=0, k=1.0):
    """Iron bed seen from the side. (x, y) = floor under the left leg. lift raises the mattress corner; cashn notes hide under it."""
    h = 150*k
    for xx in (x, x+w): s.line([(xx, y), (xx, y-h-(150*k if xx == x else 60*k))], 12*k, (70, 64, 60))
    s.line([(x, y-h-150*k), (x, y-h-150*k)], 22*k, (70, 64, 60))
    s.rect(x, y-h, x+w, y-h+26*k, (120, 108, 100), INK, 5)
    if cashn:
        for i in range(cashn): s.bill(x+w*.3+i*74*k, y-h-14*k-(i % 2)*10*k, .62*k)
    my = y-h-lift*90*k
    s.poly([(x+8, y-h-70*k), (x+w-8, my-70*k), (x+w-8, my), (x+8, y-h)], (236, 222, 214), INK, 6)
    for i in range(1, 9):
        q = i/9; s.line([(x+8+(w-16)*q, y-h-70*k+(my-y+h)*q+6), (x+8+(w-16)*q, y-h+(my-y+h)*q-6)], 4, (150, 170, 200))
    s.rect(x+20, y-h-118*k, x+190*k, y-h-66*k, WHITE, INK, 5, 20*k)
    return (x+w*.5, y-h-70*k)

@_kit
def tickerm(s, x, y, k=1.0, tape=260, wav=0.0):
    """Stock ticker under a glass dome on a stand. (x, y) = floor. tape = length of paper spilling out."""
    s.rect(x-16*k, y-210*k, x+16*k, y, WOOD, INK, 5); s.rect(x-70*k, y-18*k, x+70*k, y, WOOD, INK, 5, 6); s.rect(x-64*k, y-236*k, x+64*k, y-206*k, WOOD, INK, 5, 6)
    s.d.pieslice([(x-56*k)*S, (y-356*k)*S, (x+56*k)*S, (y-116*k)*S], 180, 360, fill=(226, 240, 240), outline=INK, width=int(5*S))
    s.ell(x-26*k, y-300*k, x+26*k, y-248*k, BRASS, INK, 4); s.rect(x-40*k, y-250*k, x+40*k, y-236*k, (70, 64, 60), INK, 3)
    if tape > 0:
        pts = [(x+40*k, y-262*k)]; n = 14
        for i in range(1, n+1):
            q = i/n; pts.append((x+40*k+tape*q, y-262*k+(250*k)*q*q+math.sin(q*9+wav)*10*k))
        s.line(pts, 15*k, INK); s.line(pts, 10*k, PAPER)
    return (x+40*k+tape, y-12*k)

@_kit
def chartbox(s, x0, y0, x1, y1, title=None, f=WHITE, grid=4, ylab=None):
    s.rect(x0, y0, x1, y1, f, INK, 7, 14)
    for i in range(1, grid): yy = y0+(y1-y0)*i/grid; s.line([(x0+28, yy), (x1-28, yy)], 3, (222, 214, 200))
    s.line([(x0+40, y0+30), (x0+40, y1-40), (x1-30, y1-40)], 6)
    if title: s.text((x0+x1)/2, y0-46, title, 60)
    return (x0+40, y0+50, x1-50, y1-40)

@_kit
def plot(s, box, pts, prog=1.0, c=RED, w=12, dot=True, fill=None):
    """Draw a polyline of normalised (x 0..1, y 0..1 up) points inside box, up to prog 0..1 along x. Returns the tip (x, y)."""
    bx0, by0, bx1, by1 = box; P = lambda p: (bx0+(bx1-bx0)*p[0], by1-(by1-by0)*p[1])
    xm = pts[0][0]+(pts[-1][0]-pts[0][0])*max(0.0, min(1.0, prog)); out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        if b[0] <= xm: out.append(b)
        elif a[0] < xm:
            q = (xm-a[0])/(b[0]-a[0]); out.append((xm, a[1]+(b[1]-a[1])*q)); break
        else: break
    px = [P(p) for p in out]
    if fill and len(px) > 1: s.poly(px+[(px[-1][0], by1), (px[0][0], by1)], fill, None)
    if len(px) > 1: s.line(px, w+6, INK); s.line(px, w, c)
    if dot: tx, ty = px[-1]; s.ell(tx-w*1.3, ty-w*1.3, tx+w*1.3, ty+w*1.3, c, INK, 5)
    return px[-1]

@_kit
def newspaper(s, x, y, k=1.0, head="STOCKS CRASH", sub=None):
    s.rect(x-210*k, y-150*k, x+210*k, y+150*k, CREAM, INK, 6*k, 4)
    s.text(x, y-112*k, "THE DAILY LEDGER", 30*k); s.line([(x-190*k, y-88*k), (x+190*k, y-88*k)], 4*k)
    s.text(x, y-40*k, head, min(70*k, 380*k/max(4, len(head))*1.9), INK)
    s.line([(x-190*k, y+8*k), (x+190*k, y+8*k)], 3*k)
    for col in range(3):
        cx = x-190*k+col*132*k
        for i in range(5): s.line([(cx, y+34*k+i*22*k), (cx+110*k-(i % 3)*14*k, y+34*k+i*22*k)], 3*k, (150, 140, 128))
    if sub: s.text(x, y+20*k, sub, 24*k)

@_kit
def desk(s, x, y, w=520, h=150, c=WOOD):
    s.rect(x, y-h, x+w, y-h+26, c, INK, 6, 4); s.rect(x+14, y-h+26, x+w*.34, y, c, INK, 6); s.rect(x+w-40, y-h+26, x+w-16, y, c, INK, 6)
    for i in range(3): yy = y-h+40+i*36; s.rect(x+26, yy, x+w*.34-12, yy+28, None, INK, 4); s.ell(x+w*.17-6, yy+8, x+w*.17+6, yy+20, BRASS, INK, 3)

@_kit
def typewriter(s, x, y, k=1.0):
    s.rect(x-90*k, y-60*k, x+90*k, y, (70, 64, 60), INK, 5*k, 10*k); s.rect(x-110*k, y-86*k, x+110*k, y-60*k, (96, 88, 84), INK, 5*k, 8*k)
    s.rect(x-60*k, y-150*k, x+60*k, y-84*k, WHITE, INK, 4*k)
    for i in range(3): s.line([(x-44*k, y-136*k+i*16*k), (x+40*k-(i % 2)*20*k, y-136*k+i*16*k)], 3*k, (150, 150, 150))
    for r in range(2):
        for i in range(6): s.ell(x-70*k+i*26*k+r*8*k, y-46*k+r*20*k, x-54*k+i*26*k+r*8*k, y-30*k+r*20*k, PAPER, INK, 2*k)

@_kit
def phone(s, x, y, k=1.0, ring=0.0):
    """Candlestick telephone standing on y. ring > 0 draws shake lines."""
    s.ell(x-50*k, y-24*k, x+50*k, y+4*k, (60, 56, 54), INK, 5*k); s.rect(x-9*k, y-170*k, x+9*k, y-14*k, (60, 56, 54), INK, 4*k)
    s.ell(x-30*k, y-214*k, x+30*k, y-160*k, (60, 56, 54), INK, 5*k); s.ell(x-14*k, y-200*k, x+14*k, y-174*k, (120, 112, 106), INK, 3*k)
    s.line([(x+9*k, y-120*k), (x+52*k, y-120*k)], 6*k); s.poly([(x+44*k, y-150*k), (x+74*k, y-160*k), (x+74*k, y-70*k), (x+44*k, y-90*k)], (60, 56, 54), INK, 4*k)
    if ring:
        for i, a in enumerate((-150, -120, -60, -30)):
            r0 = 70*k; r1 = (96+18*math.sin(ring*20+i))*k; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            s.line([(x+r0*ca, y-190*k+r0*sa), (x+r1*ca, y-190*k+r1*sa)], 8*k, RED)

@_kit
def radio(s, x, y, k=1.0):
    """Cathedral radio set standing on y."""
    s.d.pieslice([(x-120*k)*S, (y-330*k)*S, (x+120*k)*S, (y-90*k)*S], 180, 360, fill=WOOD, outline=INK, width=int(7*k*S))
    s.rect(x-120*k, y-212*k, x+120*k, y, WOOD, INK, 7*k); s.rect(x-116*k, y-216*k, x+116*k, y-200*k, WOOD, None)
    s.ell(x-70*k, y-290*k, x+70*k, y-150*k, (226, 200, 150), INK, 6*k)
    for i in range(-2, 3): s.line([(x+i*24*k, y-276*k+abs(i)*14*k), (x+i*24*k, y-164*k-abs(i)*14*k)], 5*k, (120, 84, 58))
    s.rect(x-60*k, y-124*k, x+60*k, y-84*k, CREAM, INK, 4*k, 6*k)
    for dx in (-70, 0, 70): s.ell(x+(dx-17)*k, y-62*k, x+(dx+17)*k, y-28*k, (60, 56, 54), INK, 4*k)

@_kit
def cert(s, x, y, k=1.0, t="STOCK", c=CREAM, seal=RED):
    s.rect(x-150*k, y-100*k, x+150*k, y+100*k, c, INK, 6*k, 4); s.rect(x-134*k, y-84*k, x+134*k, y+84*k, None, DGREEN, 4*k, 4)
    s.text(x, y-44*k, t, min(56*k, 250*k/max(3, len(t))*1.9), DGREEN)
    for i in range(3): s.line([(x-100*k, y+2*k+i*22*k), (x+50*k-(i % 2)*30*k, y+2*k+i*22*k)], 3*k, (150, 140, 128))
    s.ell(x+70*k, y+16*k, x+122*k, y+68*k, seal, INK, 4*k)

@_kit
def calpage(s, x, y, k=1.0, top="OCT", big="24", sub=None, c=RED):
    """Tear-off calendar page centred on (x, y)."""
    s.rect(x-130*k, y-160*k, x+130*k, y+160*k, WHITE, INK, 7*k, 12*k); s.rect(x-130*k, y-160*k, x+130*k, y-84*k, c, INK, 7*k, 12*k)
    s.text(x, y-124*k, top, 58*k, PAPER); s.text(x, y+18*k if sub else y+34*k, big, (150 if len(str(big)) < 3 else 104)*k)
    if sub: s.text(x, y+122*k, sub, 44*k)
    for dx in (-70, 70): s.ell(x+(dx-12)*k, y-178*k, x+(dx+12)*k, y-150*k, (70, 64, 60), INK, 3*k)

@_kit
def pricetag(s, x, y, k=1.0, t="$5", c=CREAM, tc=INK):
    s.poly([(x-110*k, y), (x-60*k, y-52*k), (x+110*k, y-52*k), (x+110*k, y+52*k), (x-60*k, y+52*k)], c, INK, 6*k)
    s.ell(x-82*k, y-10*k, x-62*k, y+10*k, WHITE, INK, 3*k); s.text(x+26*k, y-4*k, t, min(64*k, 150*k/max(2, len(t))*1.9), tc)

@_kit
def shoe(s, x, y, k=1.0, c=(120, 84, 58)):
    s.poly([(x-90*k, y), (x-90*k, y-84*k), (x-34*k, y-84*k), (x-20*k, y-44*k), (x+70*k, y-34*k), (x+100*k, y-10*k), (x+100*k, y)], c, INK, 6*k)
    s.rect(x-94*k, y-4*k, x+104*k, y+12*k, (60, 56, 54), INK, 4*k); s.rect(x-94*k, y+8*k, x-56*k, y+26*k, (60, 56, 54), INK, 4*k)
    for i in range(3): s.line([(x-26*k+i*16*k, y-56*k+i*4*k), (x-12*k+i*16*k, y-70*k+i*4*k)], 4*k, PAPER)

@_kit
def keyp(s, x, y, k=1.0, c=BRASS):
    s.ell(x-90*k, y-44*k, x-10*k, y+44*k, c, INK, 6*k); s.ell(x-66*k, y-18*k, x-34*k, y+18*k, PAPER, INK, 4*k)
    s.rect(x-14*k, y-12*k, x+100*k, y+12*k, c, INK, 5*k)
    for dx in (56, 84): s.rect(x+dx*k, y+10*k, x+(dx+16)*k, y+40*k, c, INK, 4*k)

@_kit
def megaphone(s, x, y, k=1.0, flip=False, c=RED):
    d = -1 if flip else 1
    s.poly([(x, y-18*k), (x+d*120*k, y-70*k), (x+d*120*k, y+70*k), (x, y+18*k)], c, INK, 6*k); s.rect(min(x, x-d*34*k), y-18*k, max(x, x-d*34*k), y+18*k, (70, 64, 60), INK, 4*k)
    for i, a in enumerate((-34, 0, 34)):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); s.line([(x+d*(150*k)*ca, y+150*k*sa), (x+d*(210*k)*ca, y+210*k*sa)], 10*k, INK)

@_kit
def bubble(s, x, y, t, size=60, tail=(-60, 90), c=INK, f=WHITE, pad=34):
    """Speech bubble centred on (x, y) with its tail pointing by the offset tail."""
    w = s.tw(t, size)+pad*2; n = t.count("\n")+1; h = size*1.2*n+pad*1.3
    tx, ty = x+tail[0], y+h/2+tail[1]
    s.poly([(x+tail[0]*.2-26, y+h/2-8), (tx, ty), (x+tail[0]*.2+26, y+h/2-8)], f, INK, 6)
    s.rect(x-w/2, y-h/2, x+w/2, y+h/2, f, INK, 6, 26); s.rect(x+tail[0]*.2-22, y+h/2-12, x+tail[0]*.2+22, y+h/2-3, f, None)
    s.text(x, y-4, t, size, c)

@_kit
def plaque(s, x, y, k=1.0, t="FDIC", sub=None, c=BRASS):
    s.rect(x-150*k, y-80*k, x+150*k, y+80*k, c, INK, 7*k, 10*k); s.rect(x-134*k, y-64*k, x+134*k, y+64*k, None, (150, 110, 40), 4*k, 6*k)
    s.text(x, y-(18*k if sub else 2*k), t, 84*k); 
    if sub: s.text(x, y+40*k, sub, 28*k)
    for dx, dy in ((-136, -66), (136, -66), (-136, 66), (136, 66)): s.ell(x+dx*k-6*k, y+dy*k-6*k, x+dx*k+6*k, y+dy*k+6*k, (150, 110, 40), INK, 2*k)

@_kit
def flag(s, x, y, h=300, k=1.0, wav=0.0):
    s.line([(x, y), (x, y-h)], 9*k, (90, 84, 80)); s.ell(x-10*k, y-h-16*k, x+10*k, y-h+4*k, BRASS, INK, 3*k)
    fw, fh = 150*k, 90*k; top = y-h+8*k
    for i in range(7):
        yy = top+fh*i/7; off = math.sin(wav+i*.5)*5*k
        s.poly([(x+4, yy), (x+fw+off, yy+off*.4), (x+fw+off, yy+fh/7+off*.4), (x+4, yy+fh/7)], RED if i % 2 == 0 else WHITE, None)
    s.rect(x+4, top, x+fw*.42, top+fh*.56, NAVY, None); s.poly([(x+4, top), (x+fw, top), (x+fw, top+fh), (x+4, top+fh)], None, INK, 4*k)

@_kit
def bell(s, x, y, k=1.0, c=BRASS, swing=0.0):
    a = swing*22; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    R = lambda px, py: (x+px*ca-py*sa, y+px*sa+py*ca)
    s.poly([R(-34*k, 0), R(-50*k, 110*k), R(-78*k, 150*k), R(78*k, 150*k), R(50*k, 110*k), R(34*k, 0)], c, INK, 6*k)
    cx, cy = R(0, 166*k); s.ell(cx-20*k, cy-20*k, cx+20*k, cy+20*k, (150, 110, 40), INK, 4*k); s.ell(x-16*k, y-22*k, x+16*k, y+8*k, c, INK, 5*k)

@_kit
def house(s, x, y, k=1.0, c=PINK):
    s.rect(x-90*k, y-110*k, x+90*k, y, c, INK, 6*k); s.poly([(x-110*k, y-110*k), (x, y-190*k), (x+110*k, y-110*k)], BRICK, INK, 6*k)
    s.rect(x-22*k, y-66*k, x+22*k, y, (90, 64, 44), INK, 4*k); s.rect(x+38*k, y-84*k, x+72*k, y-50*k, SKY, INK, 4*k)

@_kit
def factory(s, x, y, k=1.0, c=(196, 178, 160)):
    s.rect(x-120*k, y-90*k, x+120*k, y, c, INK, 6*k)
    for i in range(3): s.poly([(x-120*k+i*80*k, y-90*k), (x-120*k+i*80*k, y-140*k), (x-40*k+i*80*k, y-90*k)], c, INK, 6*k)
    s.rect(x+70*k, y-220*k, x+104*k, y-90*k, BRICK, INK, 6*k)
    for i in range(3): s.rect(x-100*k+i*66*k, y-60*k, x-66*k+i*66*k, y-26*k, SKY, INK, 4*k)

@_kit
def vault(s, x, y, r=200):
    s.rect(x-r*1.25, y-r*1.25, x+r*1.25, y+r*1.25, (150, 156, 170), INK, 8, 12); s.ell(x-r, y-r, x+r, y+r, (190, 196, 208), INK, 8)
    s.ell(x-r*.72, y-r*.72, x+r*.72, y+r*.72, None, INK, 5)
    for a in range(0, 360, 60):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); s.line([(x+r*.16*ca, y+r*.16*sa), (x+r*.5*ca, y+r*.5*sa)], 12, (90, 96, 110))
    s.ell(x-r*.18, y-r*.18, x+r*.18, y+r*.18, BRASS, INK, 6)
    for dy in (-.6, .6): s.rect(x-r*1.34, y+r*dy-22, x-r*1.1, y+r*dy+22, (90, 96, 110), INK, 5, 4)

@_kit
def shield(s, x, y, k=1.0, c=TEAL, t=None):
    s.poly([(x-90*k, y-100*k), (x, y-130*k), (x+90*k, y-100*k), (x+84*k, y+10*k), (x, y+120*k), (x-84*k, y+10*k)], c, INK, 7*k)
    if t: s.text(x, y-14*k, t, 60*k, PAPER)
    else: s.line([(x-40*k, y-10*k), (x-8*k, y+30*k), (x+46*k, y-50*k)], 16*k, PAPER)

@_kit
def umbrella(s, x, y, k=1.0, c=RED):
    s.line([(x, y), (x, y-220*k)], 8*k, (90, 84, 80)); s.d.pieslice([(x-150*k)*S, (y-330*k)*S, (x+150*k)*S, (y-110*k)*S], 180, 360, fill=c, outline=INK, width=int(6*k*S))
    for dx in (-75, 0, 75): s.line([(x+dx*k, y-220*k), (x, y-328*k)], 4*k)

@_kit
def questlog(s, rows, shown=4, done=0, hidden=None, x=1040, y=170, z=1.36):
    """The quest-log panel with this episode's own rows (rows = three objectives; hidden = the fourth once revealed)."""
    rows = list(rows)[:3]+[hidden or "? ? ?"]
    s.rect(x, y, x+610*z, y+(150+shown*92)*z, PAPER, INK, 8, 26)
    s.marker(x+62*z, y+70*z, 24*z); s.text(x+110*z, y+66*z, "QUEST LOG", 70*z, INK, "lm")
    s.line([(x+30*z, y+125*z), (x+580*z, y+125*z)], 6)
    for i in range(shown):
        yy = y+(180+i*92)*z
        s.rect(x+34*z, yy-24*z, x+82*z, yy+24*z, WHITE, INK, 6, 8)
        if i < done: s.tick(x+58*z, yy, 18*z)
        if i == 3 and not hidden:
            s.rect(x+44*z, yy-8*z, x+72*z, yy+16*z, INK, None, 0, 4); s.d.arc([(x+48*z)*S, (yy-24*z)*S, (x+68*z)*S, (yy+4*z)*S], 180, 360, fill=INK, width=6*S)
        sz = 52*z
        while sz > 30 and s.tw(rows[i], sz) > 470*z: sz -= 3
        s.text(x+104*z, yy-4, rows[i], sz, INK if i >= done else (120, 110, 98), "lm")

# ================= EP003 kit: Pompeii, AD 79 (new methods only) =================
TERRA = (196, 96, 70); OCHRE = (226, 186, 110); RWALL = (238, 222, 192); TILE = (200, 106, 76); LAVA = (104, 100, 106); ASHC = (168, 164, 160)
PUM = (218, 214, 204); SEA = (98, 152, 182); VINE = (126, 164, 108); DARK = (34, 32, 40); BURNT = (62, 52, 48)

@_kit
def rhouse(s, x, y, w=420, h=360, col=RWALL, band=TERRA, door=True, shop=False, upper=True, roof=True):
    """Roman street front: plaster wall with a coloured lower band, tiled roof edge, door or open shop, small high windows. (x, y) = bottom left."""
    s.rect(x, y-h, x+w, y, col, INK, 6); s.rect(x+3, y-h*.34, x+w-3, y-3, band, None); s.line([(x, y-h*.34), (x+w, y-h*.34)], 4)
    if roof:
        s.poly([(x-16, y-h), (x+w+16, y-h), (x+w+2, y-h-36), (x-2, y-h-36)], TILE, INK, 6)
        for i in range(int(w/38)): s.line([(x+12+i*38, y-h-31), (x+8+i*38, y-h-5)], 3, (150, 72, 52))
    if shop: s.rect(x+w*.1, y-h*.52, x+w*.9, y, (64, 50, 42), INK, 5); s.rect(x+w*.1-8, y-h*.52-16, x+w*.9+8, y-h*.52, WOOD, INK, 4)
    elif door: dw = w*.2; s.rect(x+w*.5-dw/2, y-h*.5, x+w*.5+dw/2, y, (92, 66, 46), INK, 5, 4); s.ell(x+w*.5+dw*.2, y-h*.26, x+w*.5+dw*.2+12, y-h*.26+12, BRASS, INK, 3)
    if upper:
        for q in (.2, .8): s.rect(x+w*q-22, y-h*.84, x+w*q+22, y-h*.68, (64, 50, 42), INK, 4)

@_kit
def puff(s, blobs, col=ASHC, o=INK, w=6):
    """A cartoon cloud from circles [(x, y, r), ...]: outlined as one shape, with no lines inside."""
    if o:
        for x, y, r in blobs: s.ell(x-r-w, y-r-w, x+r+w, y+r+w, o, None)
    for x, y, r in blobs: s.ell(x-r, y-r, x+r, y+r, col, None)

@_kit
def vesuvius(s, cx, by, w=900, h=420, col=VINE, rows=True, peak=True):
    top = [(cx-w*.5, by), (cx-w*.14, by-h*.92), (cx-w*.05, by-h), (cx+w*.06, by-h*.97), (cx+w*.16, by-h*.9), (cx+w*.5, by)] if peak else [(cx-w*.5, by), (cx-w*.16, by-h*.8), (cx-w*.06, by-h*.72), (cx+w*.05, by-h*.76), (cx+w*.17, by-h*.8), (cx+w*.5, by)]
    s.poly(top, col, INK, 7)
    if rows:
        for i in range(1, 5):
            q = i/5; yy = by-h*q*.8; half = w*.5*(1-q*.82)
            for j in range(int(half*2/46)): xx = cx-half+20+j*46; s.line([(xx, yy+12), (xx+8, yy-6)], 4, (88, 128, 76))
    return (cx-w*.04, by-h*(1 if peak else .76))

@_kit
def plume(s, cx, by, hgt=500, spread=600, t=0.0, col=ASHC, grow=1.0, o=INK):
    """Eruption column shaped like an umbrella pine: a trunk from (cx, by) and a flat spreading top. t animates the billow; grow 0..1 raises it."""
    hg = hgt*max(0.02, grow); blobs = []; n = max(2, int(hg/46))
    for i in range(n):
        q = i/max(1, n-1); r = 40+q*46+8*math.sin(t*3+i*1.7); blobs.append((cx+10*math.sin(t*2+i), by-q*hg, r))
    sp = spread*max(0, (grow-.55)/.45)
    if sp > 10:
        m = int(sp/70)+2
        for i in range(m):
            q = i/(m-1)-.5; blobs.append((cx+q*sp, by-hg-20+abs(q)*46+6*math.sin(t*2.5+i), 78-abs(q)*34+8*math.sin(t*3+i*2)))
            blobs.append((cx+q*sp*.8, by-hg-90+abs(q)*30, 66-abs(q)*26))
    s.puff(blobs, col, o)

@_kit
def stones(s, n=40, t=0.0, y1=H, k=1.0, col=PUM, x0=0, x1=W, seed=0):
    """Falling pumice. t is time in seconds."""
    for i in range(n):
        j = i+seed*31; sp = 420+(j*53) % 260; x = x0+(j*211+(j*j*7) % 97) % (x1-x0); y = ((j*173) % 1000)/1000*y1+t*sp; y = y % y1; r = (6+(j*29) % 9)*k
        s.ell(x-r, y-r*.8, x+r, y+r*.8, col, INK, max(2, 3*k))

@_kit
def mill(s, x, y, k=1.0):
    """Donkey mill: lava-stone hourglass on a round base, wooden beam through the waist. (x, y) = floor centre."""
    s.rect(x-120*k, y-40*k, x+120*k, y, (150, 146, 150), INK, 6*k, 8*k)
    s.poly([(x-70*k, y-40*k), (x-34*k, y-150*k), (x+34*k, y-150*k), (x+70*k, y-40*k)], LAVA, INK, 6*k)
    s.poly([(x-34*k, y-150*k), (x-84*k, y-290*k), (x+84*k, y-290*k), (x+34*k, y-150*k)], (124, 120, 126), INK, 6*k)
    s.rect(x-250*k, y-166*k, x+250*k, y-138*k, WOOD, INK, 5*k, 6*k); s.rect(x-40*k, y-176*k, x+40*k, y-128*k, WOOD, INK, 5*k, 4*k)
    for dx in (-40, 0, 40): s.ell(x+dx*k-7*k, y-250*k, x+dx*k+7*k, y-236*k, (84, 80, 86), None)

@_kit
def donkey(s, x, y, k=1.0, flip=False, c=(150, 138, 128), step=0.0):
    d = -1 if flip else 1; sw = 14*k*math.sin(step)
    for i, dx in enumerate((-60, -34, 34, 60)): s.line([(x+d*dx*k, y-70*k), (x+d*dx*k+(sw if i % 2 else -sw), y)], 12*k)
    s.ell(x-92*k, y-150*k, x+92*k, y-60*k, c, INK, 6*k)
    hx = x+d*116*k; s.poly([(x+d*60*k, y-140*k), (hx-d*10*k, y-196*k), (hx+d*30*k, y-176*k), (x+d*84*k, y-96*k)], c, INK, 6*k)
    s.ell(hx-44*k, y-222*k, hx+52*k, y-150*k, c, INK, 6*k) if not flip else s.ell(hx-52*k, y-222*k, hx+44*k, y-150*k, c, INK, 6*k)
    for e in (-12, 16): s.poly([(hx+(e-10)*k, y-214*k), (hx+e*k-d*6*k, y-282*k), (hx+(e+12)*k, y-216*k)], c, INK, 5*k)
    s.ell(hx+d*16*k-6*k, y-198*k, hx+d*16*k+6*k, y-186*k, INK, None); s.ell(hx+d*30*k-16*k, y-180*k, hx+d*30*k+16*k, y-156*k, (214, 204, 196), INK, 4*k)
    s.line([(x-d*90*k, y-120*k), (x-d*112*k, y-60*k)], 7*k); s.ell(x-d*112*k-9*k, y-64*k, x-d*112*k+9*k, y-40*k, INK, None)

@_kit
def oven(s, x, y, k=1.0, glow=1.0):
    """Brick bread oven. (x, y) = floor centre."""
    s.rect(x-230*k, y-150*k, x+230*k, y, (176, 120, 96), INK, 7*k, 6*k)
    s.d.pieslice([(x-210*k)*S, (y-420*k)*S, (x+210*k)*S, (y+120*k)*S], 180, 360, fill=TERRA, outline=INK, width=int(7*k*S)); s.rect(x-208*k, y-154*k, x+208*k, y-146*k, (176, 120, 96), None)
    for r in range(4):
        yy = y-190*k-r*46*k; hw = math.sqrt(max(0, 1-((yy-(y-150*k))/(270*k))**2))*200*k
        s.line([(x-hw, yy), (x+hw, yy)], 3*k, (150, 70, 52))
    s.d.pieslice([(x-96*k)*S, (y-280*k)*S, (x+96*k)*S, (y-30*k)*S], 180, 360, fill=(48, 34, 30), outline=INK, width=int(6*k*S)); s.rect(x-96*k, y-158*k, x+96*k, y-150*k, (48, 34, 30), None)
    if glow > 0:
        f = 1+.08*math.sin(glow*11); s.poly([(x-60*k, y-152*k), (x-40*k, y-206*k*f), (x-14*k, y-176*k), (x+4*k, y-236*k*f), (x+26*k, y-180*k), (x+48*k, y-210*k*f), (x+62*k, y-152*k)], (240, 130, 50), None)
        s.poly([(x-30*k, y-152*k), (x-12*k, y-188*k*f), (x+6*k, y-166*k), (x+24*k, y-190*k*f), (x+34*k, y-152*k)], MARI, None)

@_kit
def rloaf(s, x, y, k=1.0, burnt=False):
    """Round Roman loaf scored into wedges, seen from slightly above. (x, y) = centre."""
    c = BURNT if burnt else (226, 168, 92); l = (30, 24, 22) if burnt else (150, 96, 50)
    s.ell(x-60*k, y-34*k, x+60*k, y+40*k, c, INK, max(3, 5*k))
    for a in range(0, 180, 45):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); s.line([(x-52*k*ca, y+2*k-30*k*sa), (x+52*k*ca, y+2*k+30*k*sa)], max(2, 3*k), l)
    s.ell(x-9*k, y-5*k, x+9*k, y+9*k, l, None)

@_kit
def barcounter(s, x, y, w=560, h=200, jars=3):
    """Street-bar counter with jars sunk in the top. (x, y) = bottom left of the front."""
    s.rect(x, y-h, x+w, y, OCHRE, INK, 7, 4)
    for i in range(3):
        cx = x+w*(i+.5)/3; s.poly([(cx, y-h*.82), (cx+w*.1, y-h*.5), (cx, y-h*.18), (cx-w*.1, y-h*.5)], TERRA if i % 2 == 0 else (90, 130, 110), INK, 4)
    s.poly([(x-14, y-h), (x+w+14, y-h), (x+w+44, y-h-56), (x+16, y-h-56)], (204, 200, 196), INK, 6)
    for i in range(jars):
        cx = x+30+(w-10)*(i+.5)/jars; s.ell(cx-52, y-h-48, cx+52, y-h-10, (150, 96, 70), INK, 5); s.ell(cx-36, y-h-40, cx+36, y-h-18, (52, 38, 34), None)

@_kit
def amphora(s, x, y, k=1.0, c=(196, 132, 96)):
    s.poly([(x-20*k, y-200*k), (x+20*k, y-200*k), (x+16*k, y-168*k), (x+50*k, y-120*k), (x+40*k, y-50*k), (x, y), (x-40*k, y-50*k), (x-50*k, y-120*k), (x-16*k, y-168*k)], c, INK, 5*k)
    s.rect(x-26*k, y-212*k, x+26*k, y-196*k, c, INK, 4*k, 4*k)
    for d in (-1, 1): s.line([(x+d*18*k, y-190*k), (x+d*48*k, y-176*k), (x+d*44*k, y-134*k)], 7*k)

@_kit
def arena(s, cx, cy, w=1200, h=520):
    s.ell(cx-w/2, cy-h/2, cx+w/2, cy+h/2, (214, 204, 190), INK, 8)
    for q in (.86, .72, .58): s.ell(cx-w/2*q, cy-h/2*q, cx+w/2*q, cy+h/2*q, None, (150, 140, 128), 4)
    s.ell(cx-w*.2, cy-h*.2, cx+w*.2, cy+h*.2, SAND, INK, 6)
    for i in range(22):
        a = math.radians(8+i*7.8); x = cx-w/2*math.cos(a)*.99; y = cy+h/2*math.sin(a)*.93
        s.d.pieslice([(x-16)*S, (y+6)*S, (x+16)*S, (y+62)*S], 180, 360, fill=(70, 58, 50), outline=INK, width=3*S)

@_kit
def galley(s, x, y, w=520, flip=False, sail=WHITE, bob=0.0):
    d = -1 if flip else 1; y = y+6*math.sin(bob); P = lambda px, py: (x+d*px, y+py)
    for i in range(7): s.line([P(-w*.3+i*w*.09, -10), P(-w*.36+i*w*.09, 62+8*math.sin(bob*2+i))], 5)
    s.poly([P(-w*.46, -60), P(w*.4, -60), P(w*.56, -30), P(w*.4, -14), P(w*.3, 14), P(-w*.36, 14), P(-w*.5, -30)], WOOD, INK, 6)
    s.line([P(-w*.46, -60), P(-w*.56, -120), P(-w*.48, -150)], 9); s.line([P(0, -60), P(0, -300)], 9, (90, 70, 54))
    s.poly([P(-w*.24, -290), P(w*.24, -290), P(w*.2, -120), P(-w*.2, -120)], sail, INK, 6); s.line([P(-w*.26, -292), P(w*.26, -292)], 8, (90, 70, 54))
    ex, ey = P(w*.36, -40); s.ell(ex-12, ey-10, ex+12, ey+10, WHITE, INK, 3); s.ell(ex-4, ey-4, ex+4, ey+4, INK, None)

@_kit
def cart(s, x, y, k=1.0, c=WOOD, turn=0.0):
    s.rect(x-110*k, y-150*k, x+110*k, y-70*k, c, INK, 6*k, 6*k); s.line([(x+110*k, y-90*k), (x+230*k, y-110*k)], 9*k, (90, 70, 54))
    for dx in (-60, 60):
        cx = x+dx*k; s.ell(cx-62*k, y-124*k, cx+62*k, y, (120, 96, 76), INK, 7*k); s.ell(cx-14*k, y-76*k, cx+14*k, y-48*k, INK, None)
        for a in range(0, 180, 45):
            ca, sa = math.cos(math.radians(a)+turn), math.sin(math.radians(a)+turn); s.line([(cx-54*k*ca, y-62*k-54*k*sa), (cx+54*k*ca, y-62*k+54*k*sa)], 4*k)

@_kit
def pillow(s, f, c=WHITE):
    """A pillow tied on the head with a strip of cloth (takes a fig dict)."""
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07)
    s.line([(x-.5*u, y+.1*u), (x-.36*u, y+1.02*u), (x+.36*u, y+1.02*u), (x+.5*u, y+.1*u)], lw, (170, 150, 130))
    s.rect(x-.74*u, y-.36*u, x+.74*u, y+.14*u, c, INK, lw, .2*u); s.line([(x-.3*u, y-.2*u), (x+.3*u, y-.2*u)], max(2, lw*.5), (190, 186, 180))

@_kit
def castfig(s, x, y, k=1.0, plaster=True):
    """A lying human shape: a hollow in ash (plaster=False, dashed outline) or its plaster cast. (x, y) = centre of the body."""
    body = [(x-150*k, y), (x-40*k, y-26*k), (x+90*k, y-18*k), (x+170*k, y+6*k), (x+90*k, y+30*k), (x-40*k, y+34*k)]
    if plaster:
        s.poly(body, (240, 236, 226), INK, 5*k); s.ell(x-214*k, y-34*k, x-146*k, y+30*k, (240, 236, 226), INK, 5*k); s.line([(x-60*k, y-10*k), (x-130*k, y-52*k), (x-190*k, y-46*k)], 16*k, INK, False); s.line([(x-60*k, y-10*k), (x-130*k, y-52*k), (x-190*k, y-46*k)], 9*k, (240, 236, 226), False)
    else:
        pts = body+[body[0]]
        for a, b in zip(pts, pts[1:]):
            for q in (0, .5): s.line([(a[0]+(b[0]-a[0])*q, a[1]+(b[1]-a[1])*q), (a[0]+(b[0]-a[0])*(q+.3), a[1]+(b[1]-a[1])*(q+.3))], 5*k, (90, 84, 80), False)
        s.d.arc([(x-214*k)*S, (y-34*k)*S, (x-146*k)*S, (y+30*k)*S], 20, 340, fill=(90, 84, 80), width=int(5*k*S))

# ================= EP004 kit: England, 1349-1381 (new methods only) =================
THATCH = (212, 178, 98); DAUB = (238, 226, 202); TIMBER = (98, 72, 52); GRASS = (150, 188, 118); DGRASS = (112, 152, 96); SOIL = (156, 116, 84)
WHEATC = (228, 196, 100); SILVER = (208, 212, 218); PARCH = (240, 224, 182); FLINT = (192, 188, 180); WOOL = (244, 240, 230); OXC = (176, 124, 88); GLASSD = (70, 80, 110)

@_kit
def cottage(s, x, y, w=300, h=170, lit=True, dead=False):
    """Wattle-and-daub cottage with a timber frame and a thatched roof. (x, y) = bottom left. dead: dark door and window, faded thatch. Returns the ridge."""
    wall = DAUB if not dead else (214, 208, 196); th = THATCH if not dead else (176, 162, 126)
    s.rect(x, y-h, x+w, y, wall, INK, 6)
    for q in (.33, .66): s.line([(x+w*q, y-h), (x+w*q, y)], 7, TIMBER)
    s.line([(x, y-h*.5), (x+w, y-h*.5)], 7, TIMBER); s.line([(x+w*.66, y-h), (x+w, y-h*.5)], 6, TIMBER)
    s.rect(x+w*.4, y-h*.62, x+w*.58, y, (70, 52, 40) if not dead else (40, 34, 32), INK, 5, 4)
    s.rect(x+w*.74, y-h*.42, x+w*.9, y-h*.16, (250, 214, 130) if (lit and not dead) else (60, 54, 52), INK, 4)
    s.poly([(x-26, y-h+8), (x+w*.16, y-h-h*.78), (x+w*.84, y-h-h*.78), (x+w+26, y-h+8)], th, INK, 6)
    for i in range(1, 7): s.line([(x-26+(w+52)*i/7, y-h+2), (x+w*.16+(w*.68)*i/7, y-h-h*.72)], 3, (170, 138, 70) if not dead else (140, 128, 100))
    return (x+w*.5, y-h-h*.78)

@_kit
def church(s, x, y, k=1.0, col=FLINT):
    """Parish church: nave, square tower with battlements, short spire and cross. (x, y) = bottom left of the tower."""
    s.rect(x+120*k, y-170*k, x+420*k, y, col, INK, 6*k); s.poly([(x+108*k, y-170*k), (x+270*k, y-272*k), (x+432*k, y-170*k)], (160, 108, 88), INK, 6*k)
    for i in range(3):
        cx = x+190*k+i*90*k; s.ell(cx-16*k, y-142*k, cx+16*k, y-102*k, GLASSD, INK, 4*k); s.rect(cx-16*k, y-122*k, cx+16*k, y-50*k, GLASSD, INK, 4*k); s.rect(cx-12*k, y-126*k, cx+12*k, y-110*k, GLASSD, None)
    s.poly([(x+18*k, y-316*k), (x+65*k, y-420*k), (x+112*k, y-316*k)], (160, 108, 88), INK, 6*k)
    s.rect(x, y-300*k, x+130*k, y, col, INK, 6*k)
    for i in range(4): s.rect(x-3*k+i*37*k, y-324*k, x+19*k+i*37*k, y-298*k, col, INK, 5*k)
    s.line([(x+65*k, y-420*k), (x+65*k, y-474*k)], 6*k); s.line([(x+47*k, y-452*k), (x+83*k, y-452*k)], 6*k)
    s.ell(x+45*k, y-92*k, x+85*k, y-52*k, (70, 52, 40), INK, 5*k); s.rect(x+45*k, y-72*k, x+85*k, y, (70, 52, 40), INK, 5*k); s.rect(x+49*k, y-76*k, x+81*k, y-60*k, (70, 52, 40), None)
    s.rect(x+50*k, y-230*k, x+80*k, y-180*k, GLASSD, INK, 4*k)

@_kit
def manor(s, x, y, w=620, h=300, col=FLINT):
    """Stone manor hall: tiled roof, chimney, buttresses, tall windows, arched door. (x, y) = bottom left. Returns the door's foot."""
    s.rect(x+w*.3, y-h-h*.74, x+w*.38, y-h-h*.2, col, INK, 6)
    s.poly([(x-20, y-h), (x+w*.08, y-h-h*.5), (x+w*.92, y-h-h*.5), (x+w+20, y-h)], (166, 98, 78), INK, 7)
    for i in range(1, 12): s.line([(x-20+(w+40)*i/12, y-h-4), (x+w*.08+w*.84*i/12, y-h-h*.46)], 3, (130, 74, 58))
    s.rect(x, y-h, x+w, y, col, INK, 7)
    for q in (.05, .5, .95): s.poly([(x+w*q-24, y), (x+w*q-14, y-h*.8), (x+w*q+14, y-h*.8), (x+w*q+24, y)], (172, 168, 160), INK, 5)
    for q in (.17, .33, .64):
        cx = x+w*q; s.ell(cx-24, y-h*.72-24, cx+24, y-h*.72+24, GLASSD, INK, 5); s.rect(cx-24, y-h*.72, cx+24, y-h*.3, GLASSD, INK, 5); s.rect(cx-19, y-h*.72-4, cx+19, y-h*.72+14, GLASSD, None); s.line([(cx, y-h*.72-20), (cx, y-h*.3)], 4)
    dx = x+w*.8; s.ell(dx-46, y-h*.5-46, dx+46, y-h*.5+46, (84, 60, 46), INK, 6); s.rect(dx-46, y-h*.5, dx+46, y, (84, 60, 46), INK, 6); s.rect(dx-41, y-h*.5-6, dx+41, y-h*.5+20, (84, 60, 46), None); s.line([(dx, y-h*.5-42), (dx, y)], 4)
    return (dx, y)

@_kit
def strips(s, y0, y1=H, n=9, vx=W/2, cols=((176, 200, 120), (212, 194, 112), (166, 128, 94)), x0=-400, x1=W+400, o=True, squeeze=.12):
    """Open-field strips running from the bottom edge towards a vanishing point on the horizon line y0."""
    for i in range(n):
        xa = x0+(x1-x0)*i/n; xb = x0+(x1-x0)*(i+1)/n
        s.poly([(vx+(xa-vx)*squeeze, y0), (vx+(xb-vx)*squeeze, y0), (xb, y1), (xa, y1)], cols[i % len(cols)], INK if o else None, 4)

@_kit
def ox(s, x, y, k=1.0, flip=False, c=OXC, step=0.0):
    d = -1 if flip else 1; sw = 12*k*math.sin(step)
    for i, dx in enumerate((-74, -48, 44, 70)): s.line([(x+d*dx*k, y-80*k), (x+d*dx*k+(sw if i % 2 else -sw), y)], 14*k)
    s.ell(x-112*k, y-176*k, x+104*k, y-62*k, c, INK, 6*k); hx = x+d*128*k
    for e in (-1, 1):
        pts = [(hx+e*28*k, y-180*k), (hx+e*54*k, y-200*k), (hx+e*68*k, y-236*k)]; s.line(pts, 15*k, INK, False); s.line(pts, 8*k, (240, 232, 212), False)
    s.ell(hx-52*k, y-192*k, hx+52*k, y-100*k, c, INK, 6*k); s.ell(hx+d*22*k-24*k, y-140*k, hx+d*22*k+24*k, y-102*k, (228, 198, 172), INK, 4*k)
    s.ell(hx+d*2*k-6*k, y-164*k, hx+d*2*k+6*k, y-152*k, INK, None); s.line([(x-d*108*k, y-150*k), (x-d*128*k, y-78*k)], 7*k)

@_kit
def plough(s, x, y, k=1.0, flip=False):
    """Wooden plough. (x, y) = where the share meets the soil; the beam runs forward (to the right unless flip). Returns (handle tip, beam tip)."""
    d = -1 if flip else 1
    s.line([(x-d*40*k, y-36*k), (x+d*250*k, y-96*k)], 13*k, TIMBER); s.line([(x+d*70*k, y-62*k), (x+d*62*k, y+4*k)], 8*k, (120, 124, 132))
    s.poly([(x-d*30*k, y-50*k), (x+d*56*k, y+10*k), (x-d*40*k, y+6*k)], (120, 124, 132), INK, 5*k)
    s.line([(x-d*36*k, y-30*k), (x-d*150*k, y-170*k)], 11*k, TIMBER); s.line([(x-d*16*k, y-44*k), (x-d*112*k, y-176*k)], 9*k, TIMBER)
    return (x-d*150*k, y-170*k), (x+d*250*k, y-96*k)

@_kit
def scythe(s, x, y, k=1.0, a=0.0, flip=False):
    """Scythe; (x, y) = middle of the handle; a rotates it (degrees)."""
    d = -1 if flip else 1; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); R = lambda px, py: (x+d*(px*ca-py*sa), y+px*sa+py*ca)
    s.line([R(-20*k, -150*k), R(20*k, 170*k)], 9*k, TIMBER); s.line([R(-4*k, 0), R(-40*k, 14*k)], 8*k, TIMBER)
    pts = [R(20*k, 170*k), R(90*k, 190*k), R(170*k, 176*k), R(230*k, 140*k)]; s.line(pts, 15*k, INK); s.line(pts, 8*k, SILVER)

@_kit
def sickle(s, x, y, k=1.0, flip=False):
    """Sickle; (x, y) = bottom of the handle."""
    d = -1 if flip else 1; cx, cy = x+d*62*k, y-84*k
    pts = [(cx+d*58*k*math.cos(math.radians(t)), cy-58*k*math.sin(math.radians(t))) for t in range(200, -70, -20)]
    s.line([(x, y), (x+d*8*k, y-64*k)], 12*k, TIMBER); s.line(pts, 14*k, INK); s.line(pts, 7*k, SILVER)

@_kit
def sheaf(s, x, y, k=1.0):
    s.poly([(x-34*k, y), (x-16*k, y-86*k), (x-52*k, y-170*k), (x+52*k, y-170*k), (x+16*k, y-86*k), (x+34*k, y)], WHEATC, INK, 5*k)
    for dx in (-30, -10, 10, 30): s.line([(x+dx*.4*k, y-92*k), (x+dx*1.3*k, y-164*k)], 3*k, (176, 140, 60))
    s.line([(x-18*k, y-86*k), (x+18*k, y-86*k)], 9*k, TIMBER)

@_kit
def wheat(s, x0, x1, y, h=120, t=0.0, gap=22, col=WHEATC, droop=0.0, seed=0):
    """A row of standing wheat on the line y. t sways it; droop 0..1 bends and greys it (a crop left in the field)."""
    c2 = tuple(int(a+(b-a)*droop) for a, b in zip(col, (150, 140, 120))); i = 0; x = x0; st = (170, 138, 60) if droop < .5 else (120, 112, 96)
    while x <= x1:
        hh = h*(.86+.28*((i*37+seed*11) % 10)/10); sw = 10*math.sin(t*2+i*.7)+droop*46*(1 if i % 2 else -1); tip = (x+sw, y-hh*(1-.4*droop))
        s.line([(x, y), (x+sw*.4, y-hh*.55), tip], 5, st, False); s.ell(tip[0]-7, tip[1]-22, tip[0]+7, tip[1]+10, c2, INK, 3); x += gap; i += 1

@_kit
def roll(s, x0, y0, x1, y1, curl=34, col=PARCH):
    """A parchment roll hanging open, with a curled rod top and bottom. Returns the writing area (x0, y0, x1, y1)."""
    s.rect(x0, y0, x1, y1, col, INK, 7)
    for yy in (y0, y1): s.rect(x0-22, yy-curl, x1+22, yy+curl, (226, 206, 160), INK, 7, curl); s.line([(x0+10, yy-curl*.3), (x1-10, yy-curl*.3)], 3, (190, 168, 120))
    return (x0+50, y0+curl+20, x1-50, y1-curl-20)

@_kit
def stocks(s, x, y, k=1.0, open=0.0):
    """Wooden stocks. (x, y) = ground centre. open 0..1 lifts the top board."""
    for dx in (-190, 190): s.rect(x+dx*k-16*k, y-240*k, x+dx*k+16*k, y, TIMBER, INK, 6*k)
    s.rect(x-210*k, y-130*k, x+210*k, y-60*k, WOOD, INK, 6*k, 6*k); top = y-200*k-open*70*k
    s.rect(x-210*k, top, x+210*k, top+70*k, WOOD, INK, 6*k, 6*k)
    if open < .1:
        for dx in (-90, 90): s.ell(x+dx*k-30*k, y-160*k, x+dx*k+30*k, y-100*k, (60, 46, 38), INK, 5*k)
    s.ell(x+170*k, y-150*k, x+192*k, y-108*k, (70, 64, 60), INK, 3*k)

@_kit
def penny(s, x, y, r=30, c=SILVER):
    """A silver penny with the long cross."""
    s.ell(x-r, y-r, x+r, y+r, c, INK, max(3, r*.14))
    s.line([(x-r*.6, y), (x+r*.6, y)], max(2, r*.12), (130, 136, 146), False); s.line([(x, y-r*.6), (x, y+r*.6)], max(2, r*.12), (130, 136, 146), False)

@_kit
def halfpenny(s, x, y, r=30):
    s.d.pieslice([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], 90, 270, fill=SILVER, outline=INK, width=int(max(3, r*.14)*S)); s.line([(x-r*.6, y), (x, y)], max(2, r*.12), (130, 136, 146), False)

@_kit
def pennies(s, x, y, n, r=24, per=10, gap=None):
    """n pennies laid out in rows of `per` from the top left (x, y). Returns the y under the last row."""
    g = gap or r*2.3
    for i in range(int(n)): s.penny(x+(i % per)*g, y+(i//per)*g, r)
    return y+((max(1, int(n))-1)//per+1)*g

@_kit
def cog(s, x, y, w=560, flip=False, sail=(238, 226, 200), bob=0.0, furl=0.0):
    """Single-masted medieval cog with a stern castle. (x, y) = waterline centre. furl 0..1 gathers the sail up."""
    d = -1 if flip else 1; y = y+7*math.sin(bob); P = lambda px, py: (x+d*px, y+py)
    s.line([P(0, -70), P(0, -410)], 11, TIMBER); sh = 240*(1-.82*furl)
    s.poly([P(-w*.3, -386), P(w*.3, -386), P(w*.27, -386+sh), P(-w*.27, -386+sh)], sail, INK, 6); s.line([P(-w*.33, -388), P(w*.33, -388)], 9, TIMBER)
    if furl < .5: s.line([P(0, -380), P(0, -386+sh)], 4, (200, 180, 150))
    s.poly([P(-w*.5, -90), P(w*.5, -90), P(w*.38, 20), P(-w*.34, 20)], WOOD, INK, 7)
    for j in (1, 2): s.line([P(-w*.46+j*10, -90+j*36), P(w*.46-j*14, -90+j*36)], 4, TIMBER)
    xa, xb = sorted((P(-w*.52, 0)[0], P(-w*.3, 0)[0])); s.rect(xa, y-152, xb, y-90, WOOD, INK, 6)
    for i in range(3): s.rect(xa+i*(xb-xa)/3+4, y-174, xa+(i+1)*(xb-xa)/3-6, y-152, WOOD, INK, 5)
    s.line([P(w*.5, -90), P(w*.62, -140)], 9, TIMBER); s.poly([P(0, -410), P(64, -428), P(0, -448)], RED, INK, 4)

@_kit
def pennon(s, x, y, h=420, t=None, c=RED, w=300, wav=0.0, size=44):
    """A banner on a pole planted at (x, y). t = the words on the cloth."""
    s.line([(x, y), (x, y-h)], 10, TIMBER); top = y-h+10; bh = 140 if t and "\n" in t else 96; off = 8*math.sin(wav)
    s.poly([(x+5, top), (x+w, top+off), (x+w-30, top+bh/2+off), (x+w, top+bh+off), (x+5, top+bh)], c, INK, 6)
    if t: s.text(x+w*.47, top+bh/2+off*.5-3, t, size, PAPER)

@_kit
def crown(s, f, c=MARI):
    """A crown on a fig's head (takes a fig dict)."""
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07)
    s.poly([(x-.5*u, y+.08*u), (x-.58*u, y-.42*u), (x-.28*u, y-.16*u), (x, y-.52*u), (x+.28*u, y-.16*u), (x+.58*u, y-.42*u), (x+.5*u, y+.08*u)], c, INK, lw)
    for dx, dy in ((-.58, -.42), (0, -.52), (.58, -.42)): s.ell(x+dx*u-.08*u, y+dy*u-.1*u, x+dx*u+.08*u, y+dy*u+.06*u, RED, INK, max(2, lw*.5))

@_kit
def hood(s, f, c=EARTH, flip=False):
    """A medieval hood over a fig's head: covers the crown and falls down the back of the neck (takes a fig dict)."""
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07); d = -1 if flip else 1
    s.poly([(x-d*.5*u, y+1.06*u), (x-d*.74*u, y+.5*u), (x-d*.66*u, y-.1*u), (x-d*.2*u, y-.3*u), (x+d*.44*u, y-.2*u), (x+d*.68*u, y+.16*u), (x-d*.3*u, y+.14*u), (x-d*.42*u, y+.5*u)], c, INK, lw)

@_kit
def coif(s, f, c=WHITE):
    """A plain linen cap (clerks, justices)."""
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07)
    s.d.pieslice([(x-.66*u)*S, (y-.36*u)*S, (x+.66*u)*S, (y+.64*u)*S], 180, 360, fill=c, outline=INK, width=int(lw*S)); s.line([(x-.66*u, y+.14*u), (x+.66*u, y+.14*u)], lw)

@_kit
def tonsure(s, f, c=(120, 84, 58)):
    """A monk's ring of hair."""
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07); s.line([(x-.6*u, y+.34*u), (x-.56*u, y+.03*u), (x+.56*u, y+.03*u), (x+.6*u, y+.34*u)], lw*2.4, c, False)

@_kit
def strawhat(s, f, c=THATCH):
    u = f["u"]; x, y = f["head"]; lw = max(4, u*.07)
    s.d.pieslice([(x-.5*u)*S, (y-.44*u)*S, (x+.5*u)*S, (y+.4*u)*S], 180, 360, fill=c, outline=INK, width=int(lw*S)); s.line([(x-.96*u, y+.02*u), (x+.96*u, y+.02*u)], lw*2.4, INK, False); s.line([(x-.9*u, y+.02*u), (x+.9*u, y+.02*u)], lw*1.2, c, False)

@_kit
def sheep(s, x, y, k=1.0, flip=False, step=0.0):
    d = -1 if flip else 1; sw = 8*k*math.sin(step)
    for i, dx in enumerate((-34, -14, 18, 38)): s.line([(x+d*dx*k, y-40*k), (x+d*dx*k+(sw if i % 2 else -sw), y)], 9*k)
    s.puff([(x-36*k, y-74*k, 34*k), (x, y-86*k, 40*k), (x+36*k, y-74*k, 34*k), (x-18*k, y-56*k, 32*k), (x+20*k, y-56*k, 32*k)], WOOL, INK, 5*k)
    hx = x+d*70*k; s.ell(hx-24*k, y-104*k, hx+24*k, y-52*k, (70, 64, 60), INK, 4*k); s.ell(hx+d*6*k-4*k, y-86*k, hx+d*6*k+4*k, y-78*k, PAPER, None)

@_kit
def horse(s, x, y, k=1.0, flip=False, c=(150, 104, 72), step=0.0):
    d = -1 if flip else 1; sw = 12*k*math.sin(step); dk = (70, 52, 40)
    for i, dx in enumerate((-80, -54, 54, 80)): s.line([(x+d*dx*k, y-110*k), (x+d*dx*k+(sw if i % 2 else -sw), y)], 13*k)
    s.line([(x-d*112*k, y-170*k), (x-d*150*k, y-90*k)], 12*k, dk)
    s.poly([(x+d*60*k, y-180*k), (x+d*124*k, y-296*k), (x+d*176*k, y-270*k), (x+d*110*k, y-120*k)], c, INK, 6*k)
    s.ell(x-116*k, y-200*k, x+110*k, y-96*k, c, INK, 6*k); hx = x+d*172*k
    s.poly([(hx-d*30*k, y-316*k), (hx-d*22*k, y-358*k), (hx-d*4*k, y-318*k)], c, INK, 5*k)
    s.poly([(hx-d*44*k, y-320*k), (hx+d*10*k, y-316*k), (hx+d*72*k, y-232*k), (hx+d*44*k, y-210*k), (hx-d*30*k, y-262*k)], c, INK, 6*k)
    s.ell(hx-6*k, y-292*k, hx+6*k, y-280*k, INK, None); s.line([(x+d*78*k, y-200*k), (x+d*124*k, y-296*k)], 14*k, dk)

@_kit
def grave(s, x, y, k=1.0):
    s.ell(x-70*k, y-26*k, x+70*k, y+22*k, SOIL, INK, 5*k); s.line([(x, y-10*k), (x, y-130*k)], 11*k, TIMBER); s.line([(x-34*k, y-92*k), (x+34*k, y-92*k)], 11*k, TIMBER)

@_kit
def sack(s, x, y, k=1.0, c=(214, 190, 140), t=None):
    s.poly([(x-56*k, y), (x-66*k, y-90*k), (x-30*k, y-140*k), (x+30*k, y-140*k), (x+66*k, y-90*k), (x+56*k, y)], c, INK, 6*k)
    s.poly([(x-30*k, y-140*k), (x-40*k, y-176*k), (x+40*k, y-176*k), (x+30*k, y-140*k)], c, INK, 5*k); s.line([(x-32*k, y-142*k), (x+32*k, y-142*k)], 7*k, TIMBER)
    if t: s.text(x, y-66*k, t, 34*k, (120, 96, 60))

@_kit
def charter(s, x, y, k=1.0, t="CHARTER", lines=4, seal=RED, stamp=None):
    """A sealed charter centred on (x, y). stamp = a word struck across it in red."""
    s.rect(x-170*k, y-120*k, x+170*k, y+120*k, PARCH, INK, 6*k, 4)
    s.text(x, y-78*k, t, min(52*k, 300*k/max(4, len(t))*1.9))
    for i in range(lines): s.line([(x-130*k, y-30*k+i*26*k), (x+130*k-(i % 2)*40*k, y-30*k+i*26*k)], 4*k, (150, 130, 96))
    s.line([(x+70*k, y+110*k), (x+90*k, y+170*k)], 9*k, (150, 60, 50)); s.ell(x+56*k, y+140*k, x+124*k, y+208*k, seal, INK, 5*k)
    if stamp: s.rect(x-150*k, y-36*k, x+150*k, y+44*k, PARCH, RED, 9*k, 8*k); s.text(x, y+2*k, stamp, 60*k, RED)

@_kit
def citywall(s, y, x0=0, x1=W, h=260, gate=None, col=FLINT):
    """A battlemented town wall standing on y. gate = x of a gatehouse with two towers."""
    s.rect(x0, y-h, x1, y, col, INK, 7); xx = x0
    while xx < x1: s.rect(xx, y-h-34, xx+44, y-h, col, INK, 5); xx += 88
    for r in range(1, 4):
        for i in range(int((x1-x0)/140)+1): s.line([(x0+i*140+(r % 2)*70, y-h+r*h/4-18), (x0+i*140+(r % 2)*70+60, y-h+r*h/4-18)], 3, (160, 156, 148), False)
    if gate is not None:
        for dx in (-150, 150):
            s.rect(gate+dx-64, y-h-150, gate+dx+64, y, col, INK, 7)
            for i in range(3): s.rect(gate+dx-64+i*46, y-h-184, gate+dx-64+i*46+36, y-h-150, col, INK, 5)
            s.rect(gate+dx-10, y-h-90, gate+dx+10, y-h-30, (60, 54, 52), INK, 4)
        s.ell(gate-86, y-h*.72-70, gate+86, y-h*.72+70, (64, 50, 42), INK, 7); s.rect(gate-86, y-h*.72, gate+86, y, (64, 50, 42), INK, 7); s.rect(gate-80, y-h*.72-8, gate+80, y-h*.72+30, (64, 50, 42), None)

@_kit
def pitchfork(s, x, y, k=1.0, a=0.0):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); R = lambda px, py: (x+px*ca-py*sa, y+px*sa+py*ca)
    s.line([R(0, 0), R(0, -300*k)], 9*k, TIMBER); s.line([R(-26*k, -300*k), R(26*k, -300*k)], 7*k, (90, 84, 80))
    for dx in (-26, 0, 26): s.line([R(dx*k, -300*k), R(dx*k, -372*k)], 7*k, (90, 84, 80))

@_kit
def tree(s, x, y, k=1.0, col=DGRASS):
    s.rect(x-12*k, y-110*k, x+12*k, y, TIMBER, INK, 5*k); s.puff([(x-50*k, y-150*k, 54*k), (x+50*k, y-150*k, 54*k), (x, y-210*k, 66*k), (x, y-140*k, 50*k)], col, INK, 5*k)

@_kit
def hedge(s, y, x0=0, x1=W, r=34, col=DGRASS):
    s.puff([(x, y-r*.5+8*math.sin(x*.05), r+8*math.sin(x*.11)) for x in range(int(x0), int(x1)+1, int(r*1.3))], col, INK, 5)

@_kit
def gaol(s, x, y, w=420, h=520, n=5):
    """Prison bars in a stone frame. (x, y) = bottom centre. Draw the prisoner first, then this over them."""
    s.rect(x-w/2-30, y-h-30, x+w/2+30, y+12, None, (130, 126, 122), 34, 10); s.rect(x-w/2-44, y-h-44, x+w/2+44, y+26, None, INK, 6, 14)
    for i in range(n): xx = x-w/2+w*(i+.5)/n; s.line([(xx, y-h), (xx, y)], 18, INK, False); s.line([(xx, y-h), (xx, y)], 10, (124, 128, 136), False)
    for q in (.3, .72): s.line([(x-w/2, y-h*q), (x+w/2, y-h*q)], 18, INK, False); s.line([(x-w/2, y-h*q), (x+w/2, y-h*q)], 10, (124, 128, 136), False)

BRITAIN = [(410, 60), (440, 150), (470, 230), (505, 290), (525, 340), (515, 380), (500, 396), (540, 420), (556, 470), (536, 500), (562, 506), (600, 495), (645, 510), (660, 560), (640, 620), (612, 665), (586, 690), (546, 700), (590, 714), (626, 720), (616, 755), (570, 776), (520, 790), (450, 796), (410, 790), (360, 806), (320, 805), (296, 800), (250, 810), (216, 840), (170, 830), (110, 852), (62, 876), (50, 860), (110, 816), (166, 780), (200, 746), (250, 740), (300, 726), (326, 700), (336, 676), (300, 690), (250, 700), (200, 690), (150, 696), (110, 680), (150, 650), (186, 600), (180, 556), (130, 546), (170, 520), (160, 496), (216, 500), (266, 496), (280, 470), (286, 430), (300, 390), (266, 370), (256, 320), (286, 280), (320, 266), (270, 256), (220, 250), (216, 200), (250, 140), (270, 80), (300, 30), (350, 10), (400, 20)]
PLACES = {"DORSET": (320, 803), "LONDON": (535, 703), "BRISTOL": (322, 702), "SOUTHAMPTON": (404, 786), "YORK": (470, 345), "WARBOYS": (540, 590), "FORNHAM": (604, 606), "MEOPHAM": (566, 724), "COLCHESTER": (606, 660), "ESSEX": (584, 674), "KENT": (590, 742), "NORTH": (430, 200)}

@_kit
def britain(s, ox=520, oy=40, k=1.1, col=(214, 226, 180)):
    """Sketch outline of Britain (not to scale). Returns a dict of named places in screen coordinates."""
    s.poly([(ox+x*k, oy+y*k) for x, y in BRITAIN], col, INK, 7)
    return {n: (ox+x*k, oy+y*k) for n, (x, y) in PLACES.items()}

@_kit
def fishp(s, x, y, k=1.0, c=(150, 176, 190)):
    s.poly([(x+70*k, y), (x+110*k, y-34*k), (x+110*k, y+34*k)], c, INK, 5*k); s.ell(x-90*k, y-36*k, x+80*k, y+36*k, c, INK, 5*k); s.ell(x-66*k, y-12*k, x-54*k, y, INK, None)
    s.line([(x-30*k, y-26*k), (x-20*k, y), (x-30*k, y+26*k)], 4*k, (110, 136, 150))

@_kit
def ham(s, x, y, k=1.0):
    s.ell(x-80*k, y-56*k, x+50*k, y+50*k, (196, 110, 90), INK, 6*k); s.ell(x-50*k, y-30*k, x+10*k, y+22*k, (226, 150, 130), None)
    s.line([(x+40*k, y-10*k), (x+110*k, y-40*k)], 22*k, INK, False); s.line([(x+40*k, y-10*k), (x+110*k, y-40*k)], 13*k, (244, 238, 224), False)

@_kit
def cabbage(s, x, y, k=1.0, old=True):
    c = (150, 160, 110) if old else (140, 190, 120); s.ell(x-56*k, y-50*k, x+56*k, y+46*k, c, INK, 5*k)
    for a in (-30, 30, 90): s.line([(x, y+40*k), (x+44*k*math.sin(math.radians(a)), y-30*k)], 4*k, (104, 120, 80))

@_kit
def jug(s, x, y, k=1.0, c=(170, 120, 90)):
    s.poly([(x-40*k, y), (x-52*k, y-70*k), (x-30*k, y-130*k), (x+30*k, y-130*k), (x+52*k, y-70*k), (x+40*k, y)], c, INK, 6*k); s.rect(x-34*k, y-150*k, x+34*k, y-126*k, c, INK, 5*k, 6*k)
    s.d.arc([(x+30*k)*S, (y-116*k)*S, (x+92*k)*S, (y-40*k)*S], 270, 90, fill=INK, width=int(8*k*S))

@_kit
def bowl(s, x, y, k=1.0, c=WOOD):
    s.d.pieslice([(x-80*k)*S, (y-70*k)*S, (x+80*k)*S, (y+70*k)*S], 0, 180, fill=c, outline=INK, width=int(6*k*S)); s.line([(x-80*k, y), (x+80*k, y)], 6*k)

# ================= EP005 kit: at sea, 1519-1522 (new methods only) =================
HULL = (136, 94, 62); HULLD = (98, 68, 48); SAILC = (242, 232, 208); OCEAN = (78, 138, 172); OCEAND = (54, 104, 142); FOAM = (236, 244, 244)
CLOVEC = (124, 72, 50); HIDEC = (176, 128, 86); ISLE = (150, 188, 122); ROCKC = (124, 120, 128); COALC = (58, 50, 48); GOLD = (236, 190, 70)

@_kit
def swell(s, y, t=0.0, col=OCEAN, amp=10, wl=260, y1=H, o=True, ph=0.0, x0=0, x1=W):
    """A band of sea from the wavy line y down to y1. t moves the waves. Draw the far band, then the ships, then a nearer band over their keels."""
    pts = [(x, y+amp*math.sin(x/wl*6.283+t*1.6+ph)+amp*.4*math.sin(x/(wl*.37)*6.283-t*2.3+ph)) for x in range(int(x0), int(x1)+41, 40)]
    s.poly(pts+[(x1, y1), (x0, y1)], col, None)
    if o: s.line(pts, 5, INK, False)
    return s

@_kit
def crests(s, y0, y1, t=0.0, n=16, col=FOAM, seed=0, x0=0, x1=W):
    """Short white wave marks drifting across the water between y0 and y1."""
    for i in range(n):
        j = i+seed*31; x = x0+((j*263+int(t*(22+j % 5*6))) % (x1-x0+200))-100; y = y0+(j*97) % max(1, int(y1-y0)); w = 40+(j*13) % 40
        s.line([(x, y), (x+w*.5, y-7), (x+w, y)], 5, col, False)

@_kit
def nao(s, x, y, w=560, flip=False, bob=0.0, furl=0.0, sail=SAILC, hull=HULL, tilt=0.0, torn=False, flag=RED, ghost=False, wind=0.0):
    """Three-masted nao (carrack) of about 1519. (x, y) = waterline centre; the bow points right unless flip. furl 0..1 gathers the sails,
    tilt leans her (degrees), torn rips the canvas, ghost draws only a broken outline (a ship that is gone). Returns named points."""
    d = -1 if flip else 1; k = w/560; y = y+7*k*math.sin(bob); a = math.radians(tilt+1.4*math.sin(bob*.7)); ca, sa = math.cos(a), math.sin(a)
    P = lambda px, py: (x+d*(px*ca-py*sa)*k, y+(px*sa*d+py*ca)*k)
    lw = max(3, 6*k); G = (222, 230, 236)
    hp = [(-250, -6), (-278, -160), (-150, -160), (-140, -96), (118, -96), (132, -132), (240, -132), (292, -104), (222, -6), (160, 30), (-196, 30)]
    if ghost:
        pts = [P(*p) for p in hp]+[P(*hp[0])]
        for i in range(len(pts)-1):
            (x0, y0), (x1, y1) = pts[i], pts[i+1]; n = max(1, int(math.hypot(x1-x0, y1-y0)/(26*k+6)))
            for j in range(n):
                if j % 2 == 0: s.line([(x0+(x1-x0)*j/n, y0+(y1-y0)*j/n), (x0+(x1-x0)*(j+1)/n, y0+(y1-y0)*(j+1)/n)], lw, G, False)
        for mx, top, bot in ((0, -500, -96), (150, -390, -132), (-190, -370, -160)):
            for j in range(0, 8, 2): s.line([P(mx, bot+(top-bot)*j/8), P(mx, bot+(top-bot)*(j+1)/8)], lw, G, False)
        return {"deck": P(0, -96), "stern": P(-214, -160), "bow": P(292, -104), "top": P(0, -520), "mid": P(0, -260), "k": k}
    # masts and bowsprit behind the hull
    for mx, top, bot, mw in ((0, -520, -90, 13), (150, -400, -126, 11), (-190, -380, -154, 10)): s.line([P(mx, bot), P(mx, top)], mw*k, HULLD, False)
    s.line([P(236, -130), P(360, -200)], 10*k, HULLD, False)
    # rigging
    for mx, top, feet in ((0, -500, (-96, 96)), (150, -390, (86, 214)), (-190, -370, (-262, -150))):
        for fx in feet: s.line([P(mx, top), P(fx, -110 if abs(fx) < 130 else -140)], max(2, 2.5*k), (90, 80, 70), False)
    s.poly([P(*p) for p in hp], hull, INK, lw)
    s.line([P(-268, -104), P(-142, -100)], lw*.8, HULLD, False); s.line([P(-262, -62), P(232, -66)], lw, HULLD, False); s.line([P(-256, -30), P(226, -34)], lw*.7, HULLD, False)
    for wx in (-236, -196): s.rect(*P(wx-12 if d > 0 else wx+12, -146)[:2], *P(wx+12 if d > 0 else wx-12, -122)[:2], (60, 50, 44), INK, max(2, 3*k)) if abs(a) < .12 else None
    for gx in (-80, -20, 40): s.ell(P(gx, -50)[0]-9*k, P(gx, -50)[1]-9*k, P(gx, -50)[0]+9*k, P(gx, -50)[1]+9*k, (50, 42, 38), None)
    s.line([P(-262, -8), P(-272, 26)], lw*1.3, HULLD, False)
    s.rect(min(P(-18, -452)[0], P(18, -452)[0]), P(0, -452)[1], max(P(-18, -452)[0], P(18, -452)[0]), P(0, -430)[1], hull, INK, max(2, 4*k)) if abs(a) < .12 else None
    # sails
    f = 1-.86*max(0.0, min(1.0, furl)); b = (18+10*math.sin(wind*1.7))*f
    def sq(mx, yt, hw, hh, key):
        hh2 = hh*f; yb = yt+hh2
        pts = [(mx-hw, yt), (mx+hw, yt), (mx+hw+b, yt+hh2*.5), (mx+hw+4, yb), (mx, yb+10*f), (mx-hw+10, yb), (mx-hw+b*.6, yt+hh2*.5)]
        if torn and f > .5: pts = [(mx-hw, yt), (mx+hw, yt), (mx+hw+b, yt+hh2*.5), (mx+hw+4, yb), (mx+hw*.5, yb-hh2*.22), (mx+hw*.2, yb+6), (mx-hw*.1, yb-hh2*.34), (mx-hw*.5, yb+2), (mx-hw+10, yb-hh2*.16), (mx-hw+b*.6, yt+hh2*.5)]
        s.poly([P(*p) for p in pts], sail, INK, lw)
        if f > .5:
            for q in (-.4, .1, .55): s.line([P(mx+hw*q, yt+8), P(mx+hw*q+b*.7, yb-10)], max(2, 2.5*k), (206, 194, 168), False)
        s.line([P(mx-hw-10, yt), P(mx+hw+10, yt)], 9*k, HULLD, False)
    sq(0, -420, 122, 196, 0); sq(0, -506, 66, 70, 1); sq(150, -356, 88, 150, 2)
    ly0, ly1 = (-268, -196), (-150, -376)
    if f > .5: s.poly([P(*ly0), P(*ly1), P(-160, -186+0)], sail, INK, lw)
    s.line([P(*ly0), P(*ly1)], 8*k, HULLD, False)
    if flag:
        tx, ty = P(0, -520); fw = 74*k; wv = 8*k*math.sin(wind*3+1); s.poly([(tx, ty), (tx-d*fw, ty+14*k+wv), (tx, ty+30*k)], flag, INK, max(2, 4*k))
    return {"deck": P(0, -96), "stern": P(-214, -160), "bow": P(292, -104), "top": P(0, -520), "mid": P(0, -260), "yard": (P(-132, -420), P(132, -420)), "boat": P(-300, 6), "k": k}

@_kit
def naoicon(s, x, y, k=1.0, flip=False, col=HULL, lost=False, sail=SAILC):
    """A small ship mark for maps and counters. (x, y) = waterline centre. lost: greyed with a red cross."""
    d = -1 if flip else 1; hc = (190, 184, 176) if lost else col; sc = (226, 222, 214) if lost else sail; o = (140, 134, 128) if lost else INK
    s.line([(x, y-8*k), (x, y-58*k)], max(2, 4*k), o, False)
    s.poly([(x-24*k, y-52*k), (x+24*k, y-52*k), (x+28*k*d+2*k, y-34*k), (x+22*k, y-16*k), (x-22*k, y-16*k)], sc, o, max(2, 3.5*k))
    s.poly([(x-34*k, y-14*k), (x+34*k, y-14*k), (x+26*k, y+6*k), (x-26*k, y+6*k)] if not flip else [(x-34*k, y-14*k), (x+34*k, y-14*k), (x+26*k, y+6*k), (x-26*k, y+6*k)], hc, o, max(2, 3.5*k))
    s.line([(x-d*34*k, y-14*k), (x-d*36*k, y-26*k)], max(2, 3.5*k), o, False)
    if lost: s.line([(x-26*k, y-50*k), (x+26*k, y+4*k)], max(3, 6*k), RED, False); s.line([(x+26*k, y-50*k), (x-26*k, y+4*k)], max(3, 6*k), RED, False)

@_kit
def rowboat(s, x, y, k=1.0, flip=False, bob=0.0, n=3, coats=("blue", "brown", "slate", "green"), oars=True, empty=False):
    """A ship's boat with n rowers. (x, y) = waterline centre."""
    d = -1 if flip else 1; y = y+4*k*math.sin(bob)
    if not empty:
        for i in range(n):
            px = x+(i-(n-1)/2)*74*k; f = s.person(px, y+8*k, 150*k, "hold", "n", coats[i % len(coats)], flip=flip)
    s.poly([(x-150*k, y-34*k), (x+150*k, y-34*k), (x+118*k, y+22*k), (x-118*k, y+22*k)], HULL, INK, max(3, 5*k)); s.line([(x-140*k, y-12*k), (x+140*k, y-12*k)], max(2, 3*k), HULLD, False)
    if oars and not empty:
        sw = math.sin(bob*1.5)*30*k
        for i in range(n): px = x+(i-(n-1)/2)*74*k; s.line([(px, y-30*k), (px-d*(60*k+sw), y+50*k)], max(3, 5*k), HULLD, False)

@_kit
def proa(s, x, y, k=1.0, flip=False, bob=0.0, col=(206, 150, 96)):
    """An outrigger canoe with a triangular mat sail. (x, y) = waterline centre."""
    d = -1 if flip else 1; y = y+4*k*math.sin(bob)
    s.line([(x, y-6*k), (x, y-190*k)], max(3, 5*k), HULLD, False); s.poly([(x+d*6*k, y-186*k), (x+d*120*k, y-40*k), (x+d*6*k, y-30*k)], (232, 214, 160), INK, max(3, 4*k))
    s.poly([(x-170*k, y-26*k), (x-120*k, y+10*k), (x+120*k, y+10*k), (x+170*k, y-26*k), (x+110*k, y-10*k), (x-110*k, y-10*k)], col, INK, max(3, 5*k))
    s.line([(x-60*k, y+2*k), (x-60*k, y+40*k)], max(2, 4*k), HULLD, False); s.line([(x+60*k, y+2*k), (x+60*k, y+40*k)], max(2, 4*k), HULLD, False); s.line([(x-110*k, y+42*k), (x+110*k, y+42*k)], max(3, 7*k), col, False)

@_kit
def clove(s, x, y, k=1.0, a=0.0):
    """One dried clove, shaped like a small nail. (x, y) = centre; a rotates it (degrees)."""
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); R = lambda px, py: (x+(px*ca-py*sa)*k, y+(px*sa+py*ca)*k)
    s.line([R(0, 78), R(0, -30)], 26*k, INK, False); s.line([R(0, 76), R(0, -30)], 16*k, CLOVEC, False)
    for dx in (-1, 1): s.poly([R(dx*6, -22), R(dx*40, -58), R(dx*22, -66), R(0, -44)], CLOVEC, INK, max(2, 5*k))
    cx, cy = R(0, -62); s.ell(cx-24*k, cy-24*k, cx+24*k, cy+24*k, (150, 92, 62), INK, max(2, 5*k))

@_kit
def cloves(s, x, y, n=7, k=.5, seed=0):
    """A small heap of cloves around (x, y)."""
    r = _rnd.Random(seed)
    for i in range(n): s.clove(x+r.randint(-70, 70)*k*2, y+r.randint(-26, 26)*k*2, k, r.randint(-80, 80))

@_kit
def biscuit(s, x, y, k=1.0, crumble=0.0):
    """Ship's biscuit. crumble 0..1 breaks it down into pieces and powder."""
    c0 = (222, 196, 142); r = _rnd.Random(5)
    if crumble < .3:
        s.ell(x-110*k, y-84*k, x+110*k, y+84*k, c0, INK, max(3, 6*k))
        for i in range(9): px = x+(i % 3-1)*52*k; py = y+(i//3-1)*40*k; s.ell(px-7*k, py-7*k, px+7*k, py+7*k, (150, 120, 80), None)
        if crumble > .05: s.line([(x-30*k, y-80*k), (x-6*k, y-20*k), (x-34*k, y+20*k), (x-10*k, y+80*k)], max(2, 4*k), INK, False)
        return
    q = (crumble-.3)/.7
    s.ell(x-190*k, y+40*k, x+190*k, y+96*k, (214, 190, 140), INK, max(3, 5*k))
    for i in range(46): px = x+r.randint(-170, 170)*k; py = y+r.randint(30, 90)*k; s.ell(px-5*k, py-5*k, px+5*k, py+5*k, (180, 150, 100), None)
    for i in range(int(5*(1-q))+1):
        px = x+(i*83 % 260-130)*k; py = y+(10-i*17 % 60)*k; s.poly([(px-40*k, py+20*k), (px-24*k, py-28*k), (px+30*k, py-20*k), (px+44*k, py+18*k)], c0, INK, max(3, 5*k))

@_kit
def worm(s, x, y, k=1.0, t=0.0, col=(244, 236, 214)):
    pts = [(x+i*12*k, y+8*k*math.sin(i*1.1+t*7)) for i in range(7)]; s.line(pts, 15*k, INK, False); s.line(pts, 9*k, col, False)

@_kit
def rat(s, x, y, k=1.0, flip=False, t=0.0, col=(128, 120, 116)):
    """A rat standing on y, facing right unless flip."""
    d = -1 if flip else 1; sw = 6*k*math.sin(t*9)
    s.line([(x-d*70*k, y-30*k), (x-d*120*k, y-44*k), (x-d*160*k, y-20*k+sw), (x-d*200*k, y-36*k)], max(3, 6*k), (196, 150, 150), False)
    for dx in (-44, 40): s.line([(x+d*dx*k, y-20*k), (x+d*dx*k+sw*.6, y)], max(3, 7*k), INK, False)
    s.ell(x-80*k, y-76*k, x+60*k, y-8*k, col, INK, max(3, 5*k))
    hx = x+d*70*k; s.poly([(hx-d*34*k, y-70*k), (hx+d*52*k, y-36*k), (hx-d*30*k, y-16*k)], col, INK, max(3, 5*k))
    s.ell(hx-d*30*k-16*k, y-94*k, hx-d*30*k+16*k, y-62*k, (196, 150, 150), INK, max(2, 4*k)); s.ell(hx+d*4*k-5*k, y-54*k, hx+d*4*k+5*k, y-44*k, INK, None)
    s.ell(hx+d*52*k-7*k, y-43*k, hx+d*52*k+7*k, y-29*k, PINK, INK, max(2, 3*k))

@_kit
def barrel(s, x, y, k=1.0, col=WOOD, lid=True):
    """A cask standing on y, centred on x."""
    s.poly([(x-56*k, y), (x-70*k, y-80*k), (x-56*k, y-160*k), (x+56*k, y-160*k), (x+70*k, y-80*k), (x+56*k, y)], col, INK, max(3, 6*k))
    for yy, hw in ((-30, 61), (-80, 70), (-130, 61)): s.line([(x-hw*k, y+yy*k), (x+hw*k, y+yy*k)], max(3, 7*k), (84, 78, 74), False)
    if lid: s.ell(x-56*k, y-172*k, x+56*k, y-148*k, (176, 132, 92), INK, max(3, 5*k))

@_kit
def cannon(s, x, y, k=1.0, flip=False, fire=0.0):
    """A ship's gun on a truck carriage; the muzzle points right unless flip. fire 0..1 draws the flash and smoke."""
    d = -1 if flip else 1
    s.poly([(x-d*100*k, y-74*k), (x+d*130*k, y-66*k), (x+d*130*k, y-34*k), (x-d*100*k, y-26*k)], (86, 84, 90), INK, max(3, 6*k)); s.rect(min(x+d*120*k, x+d*142*k), y-72*k, max(x+d*120*k, x+d*142*k), y-28*k, (86, 84, 90), INK, max(3, 5*k))
    s.rect(x-90*k, y-30*k, x+70*k, y-6*k, WOOD, INK, max(3, 5*k))
    for dx in (-60, 40): s.ell(x+dx*k-20*k, y-26*k, x+dx*k+20*k, y+14*k, HULLD, INK, max(3, 5*k))
    if fire > 0:
        mx = x+d*142*k; my = y-50*k; q = min(1.0, fire)
        if q < .5: s.poly([(mx, my-16*k), (mx+d*110*k, my-50*k), (mx+d*70*k, my-8*k), (mx+d*150*k, my), (mx+d*70*k, my+10*k), (mx+d*110*k, my+50*k), (mx, my+16*k)], MARI, INK, max(3, 5*k))
        s.puff([(mx+d*(60+90*q)*k, my-10*k-40*q*k, (34+40*q)*k), (mx+d*(120+110*q)*k, my-30*k-50*q*k, (44+46*q)*k), (mx+d*(100+80*q)*k, my+16*k-30*q*k, (36+30*q)*k)], (236, 232, 226), (150, 146, 140), max(3, 4*k))

@_kit
def candle(s, x, y, k=1.0, t=0.0):
    """A lit taper; (x, y) = the bottom of the candle."""
    s.rect(x-9*k, y-120*k, x+9*k, y, CREAM, INK, max(2, 4*k)); fl = 1+.16*math.sin(t*11+x*.05)
    s.da.ellipse([(x-60*k)*S, (y-210*k)*S, (x+60*k)*S, (y-90*k)*S], fill=(255, 210, 110, 60))
    s.poly([(x-12*k, y-124*k), (x, y-124*k-44*k*fl), (x+12*k, y-124*k)], MARI, INK, max(2, 3*k))

@_kit
def palm(s, x, y, k=1.0, sway=0.0, flip=False):
    d = -1 if flip else 1; tx = x+d*(50+10*math.sin(sway))*k; ty = y-300*k
    s.line([(x, y), (x+d*10*k, y-110*k), (x+d*34*k, y-220*k), (tx, ty)], 26*k, INK, False); s.line([(x, y), (x+d*10*k, y-110*k), (x+d*34*k, y-220*k), (tx, ty)], 16*k, (170, 128, 88), False)
    for a in (-160, -120, -75, -30, 15, 200):
        r = math.radians(a+6*math.sin(sway+a)); ex, ey = tx+150*k*math.cos(r), ty+110*k*math.sin(r)+30*k
        s.poly([(tx, ty), ((tx+ex)/2+14*k*math.sin(r), (ty+ey)/2-36*k), (ex, ey), ((tx+ex)/2, (ty+ey)/2+4*k)], (110, 160, 100), INK, max(2, 4*k))
    for dx in (-12, 14): s.ell(tx+dx*k-12*k, ty+2*k, tx+dx*k+12*k, ty+28*k, (120, 84, 58), INK, max(2, 3*k))

@_kit
def islet(s, x, y, w=600, h=160, col=ISLE, palms=0, sand=True, seed=0):
    """A low island sitting on the waterline y, centred on x."""
    pts = [(x-w/2, y)]+[(x-w/2+w*q, y-h*(math.sin(q*math.pi)**.7)*(1+.12*math.sin(q*9+seed))) for q in (.08, .2, .34, .5, .66, .8, .92)]+[(x+w/2, y)]
    s.poly(pts, col, INK, 6)
    if sand: s.poly([(x-w/2, y), (x-w*.4, y-h*.12), (x+w*.4, y-h*.12), (x+w/2, y)], SAND, INK, 5)
    for i in range(palms): q = (i+1)/(palms+1); s.palm(x-w/2+w*q, y-h*.12-h*.5*math.sin(q*math.pi), h/260+.25, seed+i, flip=i % 2 == 1)

@_kit
def ducat(s, x, y, r=40, half=False):
    """A gold ducat; half draws half of one."""
    if half:
        s.d.pieslice([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], 90, 270, fill=GOLD, outline=INK, width=int(max(3, r*.14)*S)); s.line([(x, y-r), (x, y+r)], max(3, r*.14), INK, False); return
    s.ell(x-r, y-r, x+r, y+r, GOLD, INK, max(3, r*.14)); s.ell(x-r*.72, y-r*.72, x+r*.72, y+r*.72, None, (186, 140, 40), max(2, r*.08)); s.line([(x, y-r*.4), (x, y+r*.4)], max(2, r*.1), (186, 140, 40), False); s.line([(x-r*.4, y), (x+r*.4, y)], max(2, r*.1), (186, 140, 40), False)

@_kit
def hide(s, x, y, k=1.0, col=HIDEC):
    """A stiff piece of ox hide, centred on (x, y)."""
    s.poly([(x-120*k, y-50*k), (x-40*k, y-66*k), (x+60*k, y-54*k), (x+130*k, y-30*k), (x+110*k, y+44*k), (x+20*k, y+60*k), (x-90*k, y+50*k), (x-136*k, y+6*k)], col, INK, max(3, 6*k))
    for dx, dy in ((-60, -10), (10, 14), (60, -16)): s.line([(x+dx*k, y+dy*k), (x+dx*k+26*k, y+dy*k+8*k)], max(2, 4*k), (130, 92, 60), False)

@_kit
def globe(s, x, y, r=260, rot=0.0, sea=(150, 196, 214), land=(196, 206, 150)):
    """A plain globe: sea, a few land shapes that drift with rot, meridians and an equator."""
    s.ell(x-r, y-r, x+r, y+r, sea, INK, 8)
    for i, (lo, la, rw, rh) in enumerate(((-.9, -.1, .26, .5), (-.75, .42, .3, .26), (.25, .35, .46, .3), (.3, -.25, .22, .4), (1.2, .3, .4, .3), (1.45, -.35, .2, .18), (2.2, .1, .3, .5), (-2.0, .3, .4, .3))):
        ang = lo+rot; cz = math.cos(ang)
        if cz <= .05: continue
        cx = x+r*math.sin(ang)*.96; cy = y-r*la; ww = r*rw*cz; hh = r*rh*math.sqrt(max(0, 1-la*la))
        s.ell(cx-ww, cy-hh, cx+ww, cy+hh, land, INK, 4)
    for q in (.36, .72): s.ell(x-r*q, y-r, x+r*q, y+r, None, (90, 120, 136), 3)
    s.line([(x-r, y), (x+r, y)], 3, (90, 120, 136), False); s.ell(x-r, y-r, x+r, y+r, None, INK, 8)

WORLD = {
 "americas": [(-166, 66), (-158, 57), (-140, 60), (-128, 50), (-124, 40), (-117, 32), (-110, 23), (-105, 20), (-96, 15), (-87, 13), (-83, 8), (-78, 7), (-80, 0), (-81, -5), (-76, -14), (-70, -18), (-71, -30), (-73, -40), (-75, -50), (-73, -53), (-68, -53),
              (-68, -50), (-66, -46), (-65, -41), (-62, -39), (-57, -37), (-58, -34), (-54, -34), (-48, -27), (-41, -22), (-39, -13), (-35, -7), (-38, -3), (-50, 0), (-52, 5), (-60, 8), (-64, 10), (-72, 12), (-76, 9), (-80, 9), (-83, 10), (-84, 15), (-88, 16), (-87, 21), (-90, 21), (-91, 18), (-95, 18),
              (-97, 22), (-97, 27), (-94, 29), (-90, 29), (-85, 30), (-83, 28), (-81, 25), (-80, 27), (-81, 31), (-76, 35), (-75, 39), (-70, 42), (-66, 44), (-60, 46), (-65, 49), (-58, 52), (-62, 58), (-64, 60), (-75, 68), (-90, 72), (-110, 70), (-125, 70), (-140, 70), (-156, 71)],
 "fuego": [(-74, -54), (-69, -54.2), (-65, -54.6), (-67, -55.6), (-72, -55.4)],
 "afroeurasia": [(-9, 43), (-9, 37), (-6, 36), (0, 38), (3, 42), (8, 44), (12, 44), (16, 40), (18, 40), (13, 45), (20, 40), (23, 37), (26, 40), (29, 41), (36, 37), (36, 32), (34, 31), (25, 32), (20, 31), (11, 33), (10, 37), (0, 36), (-6, 35), (-10, 30), (-17, 21), (-17, 15), (-14, 10), (-8, 5), (5, 5), (9, 4), (9, -1), (13, -8), (12, -17),
                 (15, -27), (18, -34), (20, -35), (26, -34), (33, -26), (35, -20), (40, -15), (39, -5), (44, 2), (51, 12), (43, 11), (39, 16), (35, 26), (35, 28), (39, 20), (43, 13), (52, 16), (59, 22), (56, 26), (50, 29), (57, 25), (66, 25), (72, 21), (73, 16), (77, 8), (80, 13), (82, 17), (87, 21), (91, 22), (94, 17), (97, 16), (98, 8), (103, 1), (104, 5), (101, 13), (105, 9), (109, 12),
                 (108, 18), (106, 20), (110, 21), (114, 22), (120, 27), (122, 31), (119, 35), (122, 37), (121, 40), (125, 39), (126, 34), (129, 36), (130, 42), (135, 45), (140, 52), (143, 59), (155, 60), (160, 53), (163, 60), (170, 62), (178, 65), (180, 68), (170, 70), (140, 73), (110, 74), (80, 73), (60, 69), (44, 67), (40, 65), (30, 70), (20, 69), (12, 65), (5, 60), (8, 57), (10, 54), (5, 53), (-2, 48), (-4, 48), (-1, 44)],
 "britain": [(-5, 50), (1, 51), (0, 54), (-3, 58), (-6, 57), (-4, 54), (-5, 52)], "madagascar": [(44, -16), (49, -13), (50, -17), (47, -25), (44, -23)],
 "sumatra": [(95, 5), (99, 3), (104, -3), (106, -6), (102, -5), (97, 1)], "borneo": [(109, 1), (113, 4), (117, 7), (119, 4), (117, 0), (116, -4), (111, -3)], "java": [(105, -7), (110, -7), (115, -8), (110, -8.6)],
 "luzon": [(120, 18), (122, 18), (122, 14), (124, 13), (121, 13.5), (120, 15)], "visayas": [(122, 12), (124, 12.4), (125.6, 11.6), (125, 10), (123.4, 9.2), (122.4, 10)], "mindanao": [(122, 8), (125, 9.6), (126.5, 7.4), (125.4, 5.8), (123, 6.8)],
 "celebes": [(119, 1), (121, 1), (125, 1.6), (121, -1), (123, -4), (120, -5.4), (119.4, -2)], "newguinea": [(131, -1), (138, -2), (146, -6), (150, -10), (141, -9), (137, -5), (132, -3)], "japan": [(130, 32), (135, 35), (140, 37), (142, 42), (140, 41), (136, 37), (131, 34)],
 "australia": [(114, -22), (122, -17), (130, -12), (136, -12), (142, -11), (146, -19), (153, -26), (150, -37), (144, -38), (135, -34), (126, -32), (116, -35), (114, -28)]}
# Sketch positions (longitude, latitude) for the places named in EP005.
SEAPLACES = {"SANLUCAR": (-6.4, 36.8), "SEVILLE": (-6, 37.4), "RIO": (-43.2, -23), "PLATE": (-57, -35.5), "SANJULIAN": (-67.7, -49.3), "STRAIT": (-70.5, -53.2), "VIRGINS": (-68.4, -52.3), "THIEVES": (144.8, 13.5), "PHILIPPINES": (125.6, 11),
             "CEBU": (123.9, 10.3), "MACTAN": (124, 10.3), "TIDORE": (127.4, .7), "MOZAMBIQUE": (40.7, -15), "GOODHOPE": (18.5, -34.4), "CAPEVERDE": (-23.6, 15), "LISBON": (-9.1, 38.7)}

@_kit
def worldmap(s, lonc=0.0, latc=8.0, sx=5.1, sy=6.6, land=(214, 220, 178), cx=W/2, cy=H/2, grid=True, lw=6):
    """Sketch map of the world (not to scale; modern coastlines, roughly). Centre it on (lonc, latc); sx, sy = pixels per degree.
    Returns P(lon, lat) -> screen point. The outline is drawn three times so a Pacific-centred view shows both shores."""
    P = lambda lon, lat: (cx+(lon-lonc)*sx, cy-(lat-latc)*sy)
    if grid:
        for lon in range(-180, 181, 30):
            for off in (-360, 0, 360): s.line([P(lon+off, 80), P(lon+off, -70)], 2, (176, 204, 214), False)
        for lat in range(-60, 61, 30): s.line([(0, P(0, lat)[1]), (W, P(0, lat)[1])], 2, (176, 204, 214), False)
    for off in (-360, 0, 360):
        if not (-200 < P(off-180, 0)[0] < W+200 or -200 < P(off+180, 0)[0] < W+200 or P(off-180, 0)[0] < 0 < P(off+180, 0)[0]): continue
        for name, pts in WORLD.items():
            small = len(pts) < 9; s.poly([P(lon+off, lat) for lon, lat in pts], land, INK, max(3, lw*.6) if small else lw)
    return P

# ================= EP006 kit: a Norse farm in winter, about AD 950 (new methods only) =================
TURF = (118, 150, 98); SNOWC = (244, 247, 251); SNOWD = (214, 224, 236); PINEC = (62, 104, 86); ICEC = (206, 228, 238); ICED = (170, 202, 220); HAYC = (216, 188, 98)
PLANK = (140, 100, 70); PLANKD = (92, 64, 46); WOOLC = (234, 224, 198); BONEC = (238, 230, 206); AMBER = (226, 150, 50); GLASSG = (110, 170, 160); ANTLER = (200, 176, 140); CODC = (190, 198, 192); CODD = (220, 200, 150)
NORTH = {
 "scand": [(5, 58.5), (7, 58), (8.5, 58.2), (10.5, 59.2), (11, 59), (11.3, 58.3), (12, 57), (12.8, 56), (13, 55.4), (14.3, 55.5), (16, 56.2), (16.6, 57.5), (17, 58.7), (18.5, 59.5), (17.2, 60.7), (17.3, 62), (18.5, 63), (20.5, 63.8), (21.5, 65), (22.2, 65.8),
           (24.5, 65.7), (25.3, 65), (24, 64.2), (21.5, 63), (21.3, 61.5), (21.5, 60.5), (23, 59.9), (25, 60.2), (28, 60.5), (30, 60), (80, 60), (80, 68), (40, 67), (35, 69.2), (31, 70.2), (28, 71), (25.8, 71.1), (22, 70.3), (19, 69.8), (16.5, 68.8), (15, 68.2),
           (14.5, 67.3), (13, 66.2), (12.2, 65), (11, 64.5), (10, 63.8), (8.5, 63.2), (7, 62.7), (5.3, 62), (5, 61), (5.1, 60), (5.3, 59.2)],
 "lofoten": [(12.8, 67.9), (13.6, 68.15), (14.6, 68.35), (15.4, 68.6), (14.8, 68.1), (13.5, 67.85)],
 "europe": [(8.1, 57.1), (10.6, 57.7), (10.3, 56.5), (10.9, 56.3), (10, 55.5), (9.6, 54.9), (10, 54.5), (11, 54), (12.5, 54.3), (14, 54), (18.5, 54.7), (19.5, 54.4), (21, 55.2), (21, 57), (22, 57.6), (24, 57.2), (24.5, 58.3), (23.5, 59.2), (28, 59.5), (30, 59.9), (80, 59.9), (80, 40), (-1.5, 40),
            (-1.5, 43.5), (-1.2, 46), (-2.5, 47.3), (-4.7, 48.4), (-1.2, 48.6), (-1.8, 49.7), (1.5, 50.1), (1.6, 50.9), (3.2, 51.3), (4, 52), (4.8, 53.2), (7, 53.6), (8.8, 54.3), (8.6, 55.4), (8.2, 56)],
 "zealand": [(11.2, 55.7), (12.5, 56.1), (12.6, 55.6), (12.2, 54.9), (11.3, 55.2)],
 "britain": [(-5.7, 50.1), (-3.5, 50.3), (-1, 50.7), (1.3, 51.1), (1.4, 51.4), (.6, 51.5), (1.7, 52.7), (.3, 53), (-.1, 53.7), (-1.2, 54.6), (-1.6, 55.6), (-3, 56), (-2, 57.6), (-4, 57.6), (-3.1, 58.6), (-5, 58.6), (-6.2, 57.3), (-5.5, 56), (-5, 55), (-3.3, 54.9), (-3, 53.5), (-4.5, 53.2), (-4.3, 52.2), (-5.2, 51.8), (-3.2, 51.4), (-4.5, 51)],
 "ireland": [(-10, 51.6), (-6.3, 52.2), (-6, 53.5), (-5.6, 54.7), (-7.3, 55.3), (-10, 54.2), (-9.5, 53.2), (-10.3, 52.2)],
 "orkney": [(-3.4, 58.9), (-2.6, 59.05), (-2.8, 59.4), (-3.4, 59.25)], "shetland": [(-1.6, 60), (-1, 60.5), (-1.3, 60.85), (-1.7, 60.35)], "faroe": [(-7.2, 62), (-6.5, 62.25), (-7.1, 62.4)],
 "iceland": [(-24, 65.5), (-22, 66.4), (-20, 65.8), (-18, 66.2), (-16, 66.5), (-14.5, 65.8), (-13.6, 65), (-15, 64.3), (-18.5, 63.4), (-20.5, 63.6), (-22.7, 63.8), (-22, 64.5), (-24, 64.9)]}
# Sketch positions (longitude, latitude) for the places named in EP006.
NORTHPLACES = {"FARM": (10.8, 63.6), "LOFOTEN": (13.9, 68.2), "HAITHABU": (9.6, 54.5), "YORK": (-1.1, 53.96), "ICELAND": (-19, 65), "HRISBRU": (-21.6, 64.2), "ORKNEY": (-3, 59.1), "THANET": (1.35, 51.37), "DENMARK": (9.4, 56.2)}

@_kit
def northmap(s, lonc=4.0, latc=60.0, sy=38.0, land=(214, 220, 178), cx=W/2, cy=H/2, grid=True, lw=6):
    """Sketch map of northern Europe (not to scale; modern coastlines, roughly). sy = pixels per degree of latitude; a degree of longitude is drawn half as wide.
    Returns P(lon, lat) -> screen point."""
    sx = sy*.5; P = lambda lon, lat: (cx+(lon-lonc)*sx, cy-(lat-latc)*sy)
    if grid:
        for lon in range(-40, 61, 10): s.line([P(lon, 80), P(lon, 40)], 2, (176, 204, 214), False)
        for lat in range(40, 81, 5): s.line([(0, P(0, lat)[1]), (W, P(0, lat)[1])], 2, (176, 204, 214), False)
    for name, pts in NORTH.items():
        s.poly([P(lon, lat) for lon, lat in pts], land, INK, max(3, lw*.6) if len(pts) < 9 else lw)
    a, b = P(30.5, 66.4), P(79, 42); s.rect(a[0], a[1], b[0], b[1], land, None)   # hides the seam where the two land outlines meet in the east
    return P

@_kit
def peaks(s, y, x0=0, x1=W, h=260, seed=0, col=(150, 160, 184), snow=True, o=True):
    """A range of mountains standing on the line y."""
    n = max(3, int((x1-x0)/230)); pts = [(x0, y)]; tops = []
    for i in range(n):
        xa = x0+(x1-x0)*(i+.5)/n+40*math.sin(i*2.3+seed); hh = h*(.55+.45*abs(math.sin(i*1.7+seed*1.3)))
        pts += [(xa-(x1-x0)/n*.42, y-hh*.28), (xa, y-hh), (xa+(x1-x0)/n*.42, y-hh*.34)]; tops.append((xa, y-hh, hh))
    pts.append((x1, y)); s.poly(pts, col, INK if o else None, 6)
    if snow:
        for xa, ya, hh in tops: s.poly([(xa, ya), (xa+hh*.2, ya+hh*.3), (xa+hh*.06, ya+hh*.24), (xa-hh*.03, ya+hh*.34), (xa-hh*.1, ya+hh*.22), (xa-hh*.2, ya+hh*.3)], SNOWC, INK, 4)

@_kit
def pine(s, x, y, k=1.0, snow=False, col=PINEC):
    s.rect(x-9*k, y-50*k, x+9*k, y, TIMBER, INK, max(2, 4*k))
    for i, (yy, hw) in enumerate(((-40, 74), (-104, 58), (-164, 42))):
        s.poly([(x-hw*k, y+yy*k), (x, y+(yy-98)*k), (x+hw*k, y+yy*k)], col, INK, max(3, 5*k))
        if snow: s.poly([(x-hw*.5*k, y+(yy-48)*k), (x, y+(yy-98)*k), (x+hw*.5*k, y+(yy-48)*k), (x+hw*.2*k, y+(yy-58)*k), (x, y+(yy-44)*k), (x-hw*.22*k, y+(yy-58)*k)], SNOWC, None)

@_kit
def longhouse(s, x, y, w=760, h=260, snow=False, smoke=True, lit=False, door=.24, roof=TURF):
    """A Viking Age longhouse from outside: low plank walls, a long bowed roof, one door, smoke from a hole in the ridge. (x, y) = middle of the base."""
    wh = h*.36; rh = h*.64; x0, x1 = x-w/2, x+w/2
    s.rect(x0, y-wh, x1, y, PLANK, INK, 6)
    for xx in range(int(x0)+34, int(x1), 34): s.line([(xx, y-wh+4), (xx, y-4)], 3, PLANKD, False)
    pts = [(x0-26, y-wh+6)]+[(x0+w*q, y-wh-rh*(.5+.5*math.sin(math.pi*q))) for q in (.03, .15, .3, .5, .7, .85, .97)]+[(x1+26, y-wh+6)]
    s.poly(pts, SNOWC if snow else roof, INK, 6)
    if snow: s.line([(x0+w*.1, y-wh-rh*.2), (x0+w*.3, y-wh-rh*.5), (x0+w*.6, y-wh-rh*.52), (x0+w*.9, y-wh-rh*.2)], 4, SNOWD, False)
    else:
        for i in range(9): q = .08+i*.105; s.line([(x0+w*q, y-wh-rh*(.5+.5*math.sin(math.pi*q))+10), (x0+w*q-10, y-wh-4)], 3, (92, 122, 80), False)
    if door is not None:
        dx = x0+w*door; s.rect(dx-34, y-wh+12, dx+34, y, (250, 204, 120) if lit else (70, 50, 38), INK, 5, 4)
    rx, ry = x, y-wh-rh
    s.rect(rx-26, ry-6, rx+26, ry+10, (60, 48, 40), INK, 4, 4)
    if smoke: s.smoke(rx, ry-10)
    return (rx, ry)

@_kit
def haycock(s, x, y, k=1.0, col=HAYC):
    s.poly([(x-96*k, y), (x-78*k, y-74*k), (x-34*k, y-128*k), (x+34*k, y-128*k), (x+78*k, y-74*k), (x+96*k, y)], col, INK, max(3, 6*k))
    for dx, dy in ((-50, -60), (-10, -96), (34, -70), (0, -34), (56, -30), (-62, -22)): s.line([(x+dx*k, y+dy*k), (x+(dx+16)*k, y+(dy-26)*k)], max(2, 3*k), (170, 140, 60), False)

@_kit
def pig(s, x, y, k=1.0, flip=False, c=(232, 176, 164)):
    d = -1 if flip else 1
    for dx in (-52, -28, 28, 52): s.line([(x+d*dx*k, y-44*k), (x+d*dx*k, y)], 11*k)
    s.ell(x-92*k, y-124*k, x+84*k, y-30*k, c, INK, 6*k); hx = x+d*96*k
    s.ell(hx-40*k, y-122*k, hx+40*k, y-46*k, c, INK, 6*k); s.ell(hx+d*30*k-16*k, y-92*k, hx+d*30*k+16*k, y-62*k, (244, 200, 190), INK, 4*k)
    s.poly([(hx-d*26*k, y-116*k), (hx-d*14*k, y-150*k), (hx+d*2*k, y-118*k)], c, INK, 4*k); s.ell(hx+d*4*k-5*k, y-100*k, hx+d*4*k+5*k, y-90*k, INK, None)
    s.line([(x-d*90*k, y-88*k), (x-d*110*k, y-100*k), (x-d*104*k, y-78*k), (x-d*122*k, y-84*k)], 5*k)

@_kit
def cod(s, x, y, k=1.0, dry=False, sw=0.0):
    """One split, headless cod hanging by its tail from (x, y). sw swings it. dry = stockfish colour."""
    c = CODD if dry else CODC; ax, ay = x, y+30*k; bx, by = x+sw, y+170*k; L = math.hypot(bx-ax, by-ay); nx, ny = (by-ay)/L, -(bx-ax)/L
    P = lambda q, w: (ax+(bx-ax)*q+nx*w*k, ay+(by-ay)*q+ny*w*k)
    s.poly([(x-24*k, y-6*k), (x, y+12*k), (x+24*k, y-6*k), (x+9*k, y+36*k), (x-9*k, y+36*k)], c, INK, max(2, 4*k))
    s.poly([P(0, 9), P(.35, 22), P(.8, 26), P(1, 20), P(1, -20), P(.8, -26), P(.35, -22), P(0, -9)], c, INK, max(2, 5*k))
    s.line([P(.2, 0), P(.96, 0)], max(2, 3*k), (150, 156, 150) if not dry else (170, 146, 96), False)

@_kit
def fishrack(s, x, y, w=700, h=420, n=9, t=0.0, dry=False, rows=2):
    """A wooden drying rack (two A-frames and poles) hung with cod. (x, y) = middle of the base."""
    for xx in (x-w/2, x+w/2):
        s.line([(xx-70, y), (xx, y-h)], 14, TIMBER, False); s.line([(xx+70, y), (xx, y-h)], 14, TIMBER, False)
    for r in range(rows):
        yy = y-h+30+r*h*.42; s.line([(x-w/2-40, yy), (x+w/2+40, yy)], 12, TIMBER, False)
        for i in range(n): xx = x-w/2+40+(w-80)*i/max(1, n-1); s.cod(xx, yy+8, h/520, dry, 9*math.sin(t*1.7+i*.9+r))

@_kit
def boneskate(s, x, y, k=1.0, flip=False, laces=True):
    """A bone skate seen from the side; (x, y) = middle of its flat underside. The toe (right unless flip) is trimmed upward."""
    d = -1 if flip else 1; pts = [(x-d*150*k, y-24*k), (x+d*110*k, y-24*k), (x+d*168*k, y-46*k)]
    s.line(pts, 58*k, INK, False); s.line(pts, 44*k, BONEC, False)
    s.ell(x-d*178*k-30*k, y-58*k, x-d*178*k+30*k, y+6*k, BONEC, INK, max(3, 6*k)); s.line([(x-d*150*k, y+3*k), (x+d*110*k, y+3*k)], max(3, 6*k), INK, False)
    for hx in (-100, 70): s.ell(x+d*hx*k-9*k, y-34*k, x+d*hx*k+9*k, y-16*k, (120, 96, 70), INK, max(2, 3*k))
    if laces:
        for hx in (-100, 70): s.line([(x+d*hx*k, y-26*k), (x+d*(hx+20)*k, y-80*k), (x+d*(hx-24)*k, y-104*k)], max(3, 5*k), (120, 84, 58), False)

@_kit
def ski(s, x0, y0, x1, y1, w=16, col=(176, 132, 86)):
    """A wooden ski from heel (x0, y0) to toe (x1, y1); the tip turns up."""
    L = math.hypot(x1-x0, y1-y0); ux, uy = (x1-x0)/L, (y1-y0)/L; tip = (x1+ux*L*.08-uy*L*.05*(1 if ux > 0 else -1), y1+uy*L*.08-abs(ux)*L*.05)
    s.line([(x0, y0), (x1, y1), tip], w+8, INK, False); s.line([(x0, y0), (x1, y1), tip], w, col, False)
    mx, my = (x0+x1)/2, (y0+y1)/2; s.line([(mx-ux*L*.06, my-uy*L*.06), (mx+ux*L*.06, my+uy*L*.06)], w*.5, (120, 84, 58), False)

@_kit
def taflboard(s, x, y, k=1.0, n=9, pieces=True):
    """A gaming board seen from above, with a few pieces on it (no particular position is shown)."""
    a = 150*k; s.rect(x-a-16*k, y-a-16*k, x+a+16*k, y+a+16*k, (190, 150, 104), INK, max(3, 6*k), 8*k)
    for i in range(n+1): q = -a+2*a*i/n; s.line([(x+q, y-a), (x+q, y+a)], max(2, 3*k), PLANKD, False); s.line([(x-a, y+q), (x+a, y+q)], max(2, 3*k), PLANKD, False)
    if pieces:
        c = 2*a/n
        for i, (gx, gy, col) in enumerate(((1, 2, BONEC), (3, 1, BONEC), (4, 3, BONEC), (6, 5, (70, 62, 60)), (2, 6, (70, 62, 60)), (7, 2, BONEC), (5, 7, (70, 62, 60)), (3, 4, BONEC))):
            px, py = x-a+c*(gx+.5), y-a+c*(gy+.5); s.ell(px-c*.34, py-c*.34, px+c*.34, py+c*.34, col, INK, max(2, 4*k))

@_kit
def die(s, x, y, k=1.0, n=5, col=BONEC):
    r = 44*k; s.rect(x-r, y-r, x+r, y+r, col, INK, max(3, 6*k), 10*k)
    P = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)], 5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}[n]
    for a, b in P: s.ell(x+a*r*.5-r*.14, y+b*r*.5-r*.14, x+a*r*.5+r*.14, y+b*r*.5+r*.14, INK, None)

@_kit
def gpiece(s, x, y, k=1.0, col=BONEC):
    """A domed gaming piece standing on y."""
    s.d.pieslice([(x-50*k)*S, (y-76*k)*S, (x+50*k)*S, (y+60*k)*S], 180, 360, fill=col, outline=INK, width=int(max(3, 6*k)*S)); s.line([(x-50*k, y-8*k), (x+50*k, y-8*k)], max(3, 6*k), INK, False)
    s.line([(x-22*k, y-52*k), (x-8*k, y-64*k)], max(2, 5*k), WHITE, False)

@_kit
def horn(s, x, y, k=1.0, flip=False, col=(214, 196, 150)):
    """A drinking horn held upright; (x, y) = the middle of its rim."""
    d = -1 if flip else 1; pts = [(x, y), (x-d*4*k, y+44*k), (x-d*20*k, y+86*k), (x-d*52*k, y+116*k), (x-d*92*k, y+128*k)]
    for i in range(len(pts)-1):
        wd = (40-9*i)*k; s.line([pts[i], pts[i+1]], wd+8*k, INK, False)
    for i in range(len(pts)-1): s.line([pts[i], pts[i+1]], (40-9*i)*k, col, False)
    s.ell(x-24*k, y-10*k, x+24*k, y+8*k, (236, 200, 110), INK, max(2, 4*k))

@_kit
def loom(s, x, y, k=1.0, prog=.4, t=0.0, n=13):
    """A warp-weighted loom leaning against the wall: two uprights, a beam, hanging threads held taut by stone weights, the cloth growing down from the top.
    (x, y) = middle of its foot. Returns (x of cloth edge, y of the working edge)."""
    hw = 190*k; top = y-600*k
    for sgn in (-1, 1): s.line([(x+sgn*hw, y), (x+sgn*hw, top-30*k)], 20*k, INK, False); s.line([(x+sgn*hw, y), (x+sgn*hw, top-30*k)], 12*k, PLANK, False)
    s.line([(x-hw-40*k, top), (x+hw+40*k, top)], 34*k, INK, False); s.line([(x-hw-40*k, top), (x+hw+40*k, top)], 24*k, PLANK, False)
    wy = top+14*k+prog*330*k
    for i in range(n):
        xx = x-hw+26*k+(2*hw-52*k)*i/(n-1); sw = 3*k*math.sin(t*2+i); by = y-110*k+(i % 2)*16*k
        s.line([(xx, wy), (xx+sw, by)], max(2, 3*k), (150, 134, 104), False); s.ell(xx+sw-13*k, by, xx+sw+13*k, by+36*k, (150, 146, 140), INK, max(2, 4*k))
    s.rect(x-hw+18*k, top+14*k, x+hw-18*k, wy, WOOLC, INK, max(3, 5*k))
    yy = top+34*k
    while yy < wy-6*k: s.line([(x-hw+26*k, yy), (x+hw-26*k, yy)], max(1, 2*k), (200, 186, 154), False); yy += 16*k
    s.line([(x-hw-24*k, y-300*k), (x+hw+24*k, y-300*k)], 12*k, INK, False); s.line([(x-hw-24*k, y-300*k), (x+hw+24*k, y-300*k)], 6*k, PLANK, False)
    return (x+hw-18*k, wy)

@_kit
def spindle(s, x, y, k=1.0, t=0.0, top=None):
    """A drop spindle hanging at (x, y) on its thread; top = where the thread comes from. It turns with t."""
    if top: s.line([top, (x, y-70*k)], max(2, 3*k), WOOLC, False); s.line([top, (x, y-70*k)], max(1, 1.5*k), (150, 134, 104), False)
    s.line([(x, y-70*k), (x, y+70*k)], 9*k, INK, False); s.line([(x, y-70*k), (x, y+70*k)], 5*k, PLANK, False)
    s.ell(x-22*k, y-44*k, x+22*k, y+22*k, WOOLC, INK, max(2, 4*k)); s.ell(x-36*k, y+24*k, x+36*k, y+50*k, (150, 146, 140), INK, max(2, 4*k))
    a = t*9; s.ell(x+26*k*math.cos(a)-5*k, y+37*k-5*k, x+26*k*math.cos(a)+5*k, y+37*k+5*k, INK, None)

@_kit
def longship(s, x, y, w=700, flip=False, bob=0.0, sail=1.0, oars=0, ghost=False, wind=0.0, mast=True, sailc=WOOLC, hull=None):
    """A Viking Age ship: a long low hull with a high curled stem and stern, one mast, one square sail made of sewn strips. (x, y) = waterline middle.
    sail 0..1 = how far the sail is let down from the yard. Plain stems (no carved head). Returns the middle of the sail."""
    d = -1 if flip else 1; y = y+w*.008*math.sin(bob); hull = hull or (136, 94, 62); u = w
    H_ = [(-.52, -.23), (-.465, -.10), (-.38, -.055), (-.30, -.045), (.30, -.045), (.38, -.055), (.465, -.10), (.52, -.23), (.50, -.10), (.44, -.01), (.34, .035), (-.34, .035), (-.44, -.01), (-.50, -.10)]
    pts = [(x+d*a*u, y+b*u) for a, b in H_]
    if ghost:
        for a, b in zip(pts, pts[1:]+pts[:1]):
            n = max(1, int(math.hypot(b[0]-a[0], b[1]-a[1])/26))
            for j in range(0, n, 2): s.line([(a[0]+(b[0]-a[0])*j/n, a[1]+(b[1]-a[1])*j/n), (a[0]+(b[0]-a[0])*(j+1)/n, a[1]+(b[1]-a[1])*(j+1)/n)], 5, (120, 130, 150), False)
        return (x, y-.36*u)
    if mast:
        s.line([(x, y-.04*u), (x, y-.64*u)], max(6, u*.016), INK, False); s.line([(x, y-.04*u), (x, y-.64*u)], max(3, u*.009), (110, 80, 56), False)
        yt = y-.60*u; hwid = .27*u
        if sail > .03:
            yb = yt+(.47*u)*sail; bl = .03*u*math.sin(wind*1.3)+d*.035*u
            poly = [(x-hwid, yt), (x+hwid, yt), (x+hwid+bl*.5, (yt+yb)/2), (x+hwid, yb), (x+bl, yb+.02*u*sail), (x-hwid, yb), (x-hwid+bl*.5, (yt+yb)/2)]
            s.poly(poly, sailc, INK, max(4, u*.008))
            for i in range(1, 6): xx = x-hwid+2*hwid*i/6; s.line([(xx, yt+6), (xx+bl*.6, yb-4)], max(2, u*.004), (196, 180, 146), False)
            for sgn in (-1, 1): s.line([(x+sgn*hwid, yb), (x+sgn*.42*u, y-.07*u)], max(2, u*.004), (84, 70, 58), False)
        else: s.line([(x-hwid, yt+.012*u), (x+hwid, yt+.012*u)], max(10, u*.03), INK, False); s.line([(x-hwid, yt+.012*u), (x+hwid, yt+.012*u)], max(6, u*.02), sailc, False)
        s.line([(x-hwid-.02*u, yt), (x+hwid+.02*u, yt)], max(6, u*.014), INK, False); s.line([(x-hwid-.02*u, yt), (x+hwid+.02*u, yt)], max(3, u*.007), (110, 80, 56), False)
        for sgn in (-1, 1): s.line([(x, y-.64*u), (x+sgn*.47*u, y-.11*u)], max(2, u*.004), (84, 70, 58), False)
    s.poly(pts, hull, INK, max(4, u*.009))
    for off in (.012, .034): s.line([(x+d*a*u, y+(b+off)*u) for a, b in ((-.47, -.10), (-.38, -.055), (-.30, -.045), (.30, -.045), (.38, -.055), (.47, -.10))], max(2, u*.004), (98, 68, 48), False)
    for sgn in (-1, 1):
        cx_, cy_ = x+sgn*.508*u, y-.25*u; r = .028*u; s.ell(cx_-r, cy_-r, cx_+r, cy_+r, hull, INK, max(3, u*.007))
    for i in range(oars):
        ox_ = x+(-.26+.52*i/max(1, oars-1))*u; sw = .03*u*math.sin(bob*2.2+i*.0); s.line([(ox_, y-.03*u), (ox_-d*(.05*u)+sw, y+.11*u)], max(3, u*.006), (98, 68, 48), False)
    return (x, y-.36*u)

@_kit
def vat(s, x, y, k=1.0, fill=(246, 242, 226)):
    """A big wooden vat standing on y; the top shows what is in it."""
    s.poly([(x-150*k, y), (x-170*k, y-220*k), (x+170*k, y-220*k), (x+150*k, y)], PLANK, INK, max(3, 6*k))
    for i in range(1, 8): xx = x-150*k+300*k*i/8; s.line([(xx, y-6*k), (xx+(xx-x)*.12, y-214*k)], max(2, 3*k), PLANKD, False)
    for yy in (-60, -160): s.line([(x-(154+(-yy)*.08)*k, y+yy*k), (x+(154+(-yy)*.08)*k, y+yy*k)], max(3, 8*k), (84, 78, 74), False)
    s.ell(x-170*k, y-250*k, x+170*k, y-190*k, fill, INK, max(3, 6*k))

@_kit
def rushlamp(s, x, y, k=1.0, t=0.0):
    """A small open lamp on a stand; (x, y) = its foot."""
    s.line([(x, y), (x, y-150*k)], 10*k, INK, False); s.line([(x-40*k, y), (x+40*k, y)], 12*k, INK, False)
    s.d.pieslice([(x-52*k)*S, (y-200*k)*S, (x+52*k)*S, (y-120*k)*S], 0, 180, fill=(120, 116, 112), outline=INK, width=int(max(3, 5*k)*S))
    fl = 1+.2*math.sin(t*12+x*.03); s.poly([(x-12*k, y-160*k), (x+2*k, y-160*k-58*k*fl), (x+14*k, y-160*k)], MARI, INK, max(2, 3*k))

@_kit
def sock(s, x, y, k=1.0, col=(214, 186, 150)):
    """A short wool sock; (x, y) = under the heel."""
    pts = [(x-60*k, y-210*k), (x+44*k, y-210*k), (x+50*k, y-80*k), (x+170*k, y-58*k), (x+196*k, y-20*k), (x+170*k, y), (x-40*k, y), (x-66*k, y-40*k)]
    s.poly(pts, col, INK, max(3, 6*k))
    for i in range(6):
        yy = y-196*k+i*30*k
        for j in range(4): s.line([(x-48*k+j*24*k, yy), (x-36*k+j*24*k, yy+10*k)], max(2, 3*k), (176, 140, 104), False)
    for i in range(4): xx = x+70*k+i*28*k; s.line([(xx, y-52*k+i*4*k), (xx-6*k, y-34*k)], max(2, 3*k), (176, 140, 104), False)

@_kit
def roundshield(s, x, y, r=70, col=RED):
    s.ell(x-r, y-r, x+r, y+r, col, INK, max(3, r*.09))
    for a in (-.5, 0, .5): s.line([(x+a*r, y-r*math.sqrt(1-a*a)+4), (x+a*r, y+r*math.sqrt(1-a*a)-4)], max(2, r*.035), INK, False)
    s.ell(x-r*.26, y-r*.26, x+r*.26, y+r*.26, (150, 150, 156), INK, max(3, r*.07))

@_kit
def clothbolt(s, x, y, k=1.0, col=WOOLC, n=4):
    """A folded length of woollen cloth lying on y."""
    for i in range(n):
        yy = y-i*34*k; s.rect(x-120*k, yy-34*k, x+120*k, yy, col, INK, max(3, 5*k), 14*k)
        for j in range(5): s.line([(x-96*k+j*48*k, yy-28*k), (x-96*k+j*48*k, yy-6*k)], max(1, 2*k), (200, 186, 154), False)

@_kit
def lyre(s, x, y, k=1.0):
    """A small lyre held upright; (x, y) = its foot."""
    s.poly([(x-60*k, y), (x-70*k, y-150*k), (x-50*k, y-250*k), (x+50*k, y-250*k), (x+70*k, y-150*k), (x+60*k, y)], (176, 132, 86), INK, max(3, 6*k))
    s.rect(x-40*k, y-226*k, x+40*k, y-130*k, None, INK, max(3, 5*k), 16*k); s.rect(x-38*k, y-224*k, x+38*k, y-132*k, (60, 48, 40), None, 0, 14*k)
    for i in range(5): xx = x-28*k+i*14*k; s.line([(xx, y-240*k), (xx, y-40*k)], max(1, 2*k), PAPER, False)

@_kit
def snowfall(s, n=70, t=0.0, seed=0, big=5):
    """Falling snow over the whole frame."""
    d = getattr(s, "da", s.d)
    for i in range(n):
        j = i+seed*17; x = (j*211+int(t*46)+int(34*math.sin(t*.9+j))) % W; y = (j*137+int(t*(110+j % 5*14))) % H; r = big*(.6+(j % 4)*.2)
        d.ellipse([(x-r)*S, (y-r)*S, (x+r)*S, (y+r)*S], fill=(255, 255, 255, 225) if hasattr(s, "da") else WHITE)
