"""Review sheets for the reviewer agents: 3x3 sheets of 640-px stills from work/<EP>/frames (run render.py first), each with its
still number, scene and narration line.

    THSQ_EP=ep06 python3 engine/tools/sheets.py EP006 OUTDIR [first last]"""
import sys, os, json, importlib
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
ep = importlib.import_module(os.environ.get("THSQ_EP", "ep01"))
from PIL import Image, ImageDraw, ImageFont
W_ = os.path.join(os.path.dirname(HERE), "work", sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
idx = json.load(open(W_+"/frames.json")); font = ImageFont.truetype(HERE+"/fonts/PatrickHandSC-Regular.ttf", 20)
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0; hi = int(sys.argv[4]) if len(sys.argv) > 4 else len(idx)-1
sel = [x for x in idx if lo <= x[2] <= hi]
for s in range(0, len(sel), 9):
    sh = Image.new("RGB", (3*640, 3*440), "white"); d = ImageDraw.Draw(sh)
    for j, (ui, fi, n) in enumerate(sel[s:s+9]):
        im = Image.open(f"{W_}/frames/f{n:03d}.png").resize((640, 360)); x, y = (j % 3)*640, (j//3)*440; sh.paste(im, (x, y)); f = ep.U[ui][1][fi]
        d.text((x+6, y+362), f"STILL {n}  (line {ui}, picture {fi+1} of {len(ep.U[ui][1])}, scene {getattr(f, 'scene', '')})", fill="black", font=font)
        t = ep.U[ui][0]; d.text((x+6, y+386), t[:84], fill=(50, 50, 50), font=font); d.text((x+6, y+408), t[84:168], fill=(50, 50, 50), font=font)
    nm = f"{out}/sheet_{sel[s][2]:03d}.jpg"; sh.save(nm, quality=85); print(nm)
