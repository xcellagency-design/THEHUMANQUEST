"""EP006 thumbnail (1280x720): one figure, four words. Run from the repo root: python3 engine/thumb06.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thsq as T, life
from thsq import *
from PIL import Image, ImageDraw
from brand import title
import ep06

def thumb(out):
    T.TT = 1.4; T.LT = 9.0; T.LP = 1.0; T.GP = 1.0
    c = ep06.land("dusk", "snow", 560, (1500, 470), seed=3); c.da.ellipse([900*S, 0, 2100*S, 1000*S], fill=(255, 190, 110, 50))
    c.poly([(-10, H+10), (-10, 800), (500, 760), (1300, 770), (W+10, 810), (W+10, H+10)], ICEC, INK, 8)
    for i in range(7): x = 120+i*270; c.line([(x, 900+(i % 2)*70), (x+130, 888+(i % 2)*70)], 6, ICED, False)
    c.longhouse(1480, 760, 620, 240, snow=True, lit=True)
    for px, k in ((1080, 1.1), (1860, 1.5)): c.pine(px, 760, k, True)
    ep06.skater(c, 560, 1010, 640, "wow")
    c.snowfall(40, 2.0, 1, 8)
    im = c.im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    title(d, (900, 100), "180 DAYS", 156, MARI, INK, 14); title(d, (900, 236), "OF WINTER", 104, PAPER, INK, 11)
    im.save(out); return im

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(T.HERE), "03_episodes", "EP006", "09_package"); os.makedirs(out, exist_ok=True)
    thumb(os.path.join(out, "THSQ_EP006_thumbnail.png")); print("ok")
