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
        tc = {"sid": MARI, "modern": MARI, "extra": GREY, "boss": TEAL, "scribe": GREY, "greek": WHITE, "sci": WHITE, "chain": (190, 150, 140)}.get(who, GREY)
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
