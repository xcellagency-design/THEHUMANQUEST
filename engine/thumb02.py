"""EP002 thumbnail (1280x720): one figure, three words. Run from the repo root: python3 engine/thumb02.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thsq as T, life
from thsq import *
from PIL import Image, ImageDraw
from brand import title, dfont
import ep02

def thumb(out):
    c = ep02.street("dusk", 700, 7, hmax=520)
    xs = [1010, 1250, 1490, 1730]
    for i, x in enumerate(xs): c.door(x, 930, 200, 420, i+1, ep02.DCOL[i])
    s = c.fig(420, 1060, 560, "hold", "worry", "modern"); hx, hy = s["hand"]; c.cash(hx+110, hy+70, 9, 1.9)
    im = c.im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    title(d, (640, 96), "$1,000 IN 1929", 150, MARI, INK, 14)
    im.save(out); return im

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(T.HERE), "03_episodes", "EP002", "09_package"); os.makedirs(out, exist_ok=True)
    thumb(os.path.join(out, "THSQ_EP002_thumbnail.png")); print("ok")
