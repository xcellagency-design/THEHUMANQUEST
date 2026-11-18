"""EP004 thumbnail (1280x720): one figure, four words (three in the title, one on the sign). Run from the repo root: python3 engine/thumb04.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thsq as T, life
from thsq import *
from PIL import Image, ImageDraw
from brand import title
import ep04

def thumb(out):
    c = C(GRASS); ep04.sky(c, 700, "dusk", clouds=False, sun=False); c.da.ellipse([900*S, 250*S, 1900*S, 1250*S], fill=(255, 190, 110, 70))
    c.rect(0, 700, W, H, (150, 170, 110), None); c.line([(0, 700), (W, 700)], 7, INK, False); c.wheat(0, W, 820, 150, 0.3, 30); c.wheat(10, W, 950, 170, 0.8, 34, seed=2)
    s = c.fig(430, 1100, 620, "hold", "smug", "modern"); hx, hy = s["hand"]
    for i, (dx, dy) in enumerate(((70, -60), (190, -130), (60, -200))): c.penny(hx+dx, hy+dy, 64)
    ep04.bigcrown(c, 1420, 520, 1.25); c.rect(1090, 690, 1750, 900, PAPER, RED, 16, 18); c.text(1420, 790, "NO.", 190, RED)
    im = c.im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    title(d, (640, 92), "KING BANS RAISES", 130, MARI, INK, 12)
    im.save(out); return im

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(T.HERE), "03_episodes", "EP004", "09_package"); os.makedirs(out, exist_ok=True)
    thumb(os.path.join(out, "THSQ_EP004_thumbnail.png")); print("ok")
