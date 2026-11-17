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
