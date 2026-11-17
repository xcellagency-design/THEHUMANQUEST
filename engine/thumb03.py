"""EP003 thumbnail (1280x720): one figure, three words. Run from the repo root: python3 engine/thumb03.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thsq as T, life
from thsq import *
from PIL import Image, ImageDraw
from brand import title
import ep03

def thumb(out):
    c = C(PUM); ep03.sky(c, 760, "glow"); c.vesuvius(1330, 800, 1300, 520, (84, 72, 76), False, False); c.plume(1290, 430, 130, 1150, 0.4, (120, 108, 110), 1.0)
    c.da.ellipse([1180*S, 360*S, 1400*S, 470*S], fill=(255, 150, 60, 110))
    c.rect(0, 800, W, H, (150, 140, 134), None); c.line([(0, 800), (W, 800)], 7, INK, False)
    c.stones(26, 0.37, 1080, 2.6, x0=760)
    s = c.fig(470, 1090, 600, "run", "wow", "modern"); c.pillow(s)
    im = c.im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    title(d, (640, 88), "WOULD YOU RUN?", 132, MARI, INK, 14)
    im.save(out); return im

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(T.HERE), "03_episodes", "EP003", "09_package"); os.makedirs(out, exist_ok=True)
    thumb(os.path.join(out, "THSQ_EP003_thumbnail.png")); print("ok")
