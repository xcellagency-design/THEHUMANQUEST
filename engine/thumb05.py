"""EP005 thumbnail (1280x720): one figure, three words. Run from the repo root: python3 engine/thumb05.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thsq as T, life
from thsq import *
from PIL import Image, ImageDraw
from brand import title
import ep05

def thumb(out):
    c = ep05.sea("storm", hz=600, sun=False, clouds=False); c.da.ellipse([1000*S, 80*S, 1900*S, 980*S], fill=(255, 200, 120, 46))
    c.swell(660, 1.3, SEAC_D, 30, 520, ph=1); c.nao(1330, 830, 760, flip=True, bob=2.0, tilt=9, torn=True, wind=1.0); c.swell(840, .4, SEAC_L, 30, 420, ph=2); c.crests(880, 1060, 0, 10, (190, 206, 216))
    c.rect(-10, 930, 900, 1100, HULL, INK, 9); c.rect(-10, 900, 920, 946, HULLD, INK, 9, 8); s = c.fig(400, 1500, 780, "chin", "worry", "modern")
    im = c.im.resize((1280, 720), Image.LANCZOS); d = ImageDraw.Draw(im)
    title(d, (640, 96), "ONLY 18 FINISHED", 132, MARI, INK, 12)
    im.save(out); return im

SEAC_D, SEAC_L = ep05.SEAC["storm"]
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(T.HERE), "03_episodes", "EP005", "09_package"); os.makedirs(out, exist_ok=True)
    thumb(os.path.join(out, "THSQ_EP005_thumbnail.png")); print("ok")
