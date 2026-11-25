"""Preview stills of the episode module named in THSQ_EP while writing it (no narration needed).

    THSQ_EP=ep06 python3 engine/tools/prev.py out.jpg wake:0,1 where:2 sol      scene functions by name, with their first argument
    THSQ_EP=ep06 python3 engine/tools/prev.py out.jpg @0-12                     every still of narration lines 0 to 12

Each still is drawn three quarters of the way through an assumed 2.2 s hold (so arriving labels and counters are mostly in),
shrunk to 640 px and captioned. Look at the sheet: the code cannot tell whether a drawing reads well."""
import sys, os, math, importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import thsq as T, life
from PIL import Image, ImageDraw
ep = importlib.import_module(os.environ.get("THSQ_EP", "ep01")); out = sys.argv[1]; items = []
for a in sys.argv[2:]:
    if a.startswith("@"):
        lo, hi = map(int, a[1:].split("-"))
        for ui in range(lo, hi+1):
            for fi, f in enumerate(ep.U[ui][1]): items.append((f"line {ui}.{fi} {getattr(f, 'scene', '')}", f, ep.U[ui][0]))
    else:
        nm, _, ks = a.partition(":")
        for k in (ks.split(",") if ks else [None]):
            fn = getattr(ep, nm); items.append((f"{nm}:{k}", (lambda fn=fn, k=k: fn(*([int(k)] if k is not None else []))), ""))
tiles = []
for i, (cap, f, nar) in enumerate(items):
    T.TT = 3.0+i*1.7; T.LT = 1.65; T.LP = .75; T.GP = .6; T.FR = i*40; T.PREV = set(); T.CUR = set()
    try: im = f().out().resize((640, 360))
    except Exception:
        import traceback; traceback.print_exc(limit=3); im = Image.new("RGB", (640, 360), "red")
    t = Image.new("RGB", (640, 410), "white"); t.paste(im, (0, 0)); d = ImageDraw.Draw(t); d.text((6, 362), cap, fill="black"); d.text((6, 378), nar[:104], fill=(60, 60, 60)); d.text((6, 392), nar[104:208], fill=(60, 60, 60)); tiles.append(t)
cols = 3; rows = math.ceil(len(tiles)/cols); sh = Image.new("RGB", (cols*640, rows*410), "white")
for i, t in enumerate(tiles): sh.paste(t, ((i % cols)*640, (i//cols)*410))
sh.save(out, quality=82); print(len(tiles), "stills ->", out)
