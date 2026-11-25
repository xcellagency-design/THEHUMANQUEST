"""Every word drawn on screen, still by still, under its narration line. On-screen words are claims: give this list, the script and
the fact table to a reader who has nothing else, before the long render.

    THSQ_EP=ep06 python3 engine/tools/labels.py > labels.txt"""
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import thsq as T, life
ep = importlib.import_module(os.environ.get("THSQ_EP", "ep01")); seen = []; _t = T.C.text
def text(s, x, y, t, size=90, c=T.INK, anchor="mm"): seen.append(str(t).replace("\n", " / ")); return _t(s, x, y, t, size, c, anchor)
T.C.text = text; n = 0
for ui, u in enumerate(ep.U):
    print(f"\nLINE {ui}: {u[0]}")
    for fi, f in enumerate(u[1]):
        seen.clear(); T.LT = 9.0; T.LP = 1.0; T.GP = 1.0; T.TT = 0.0; T.PREV = set(); T.CUR = set(); f()
        print(f"  STILL {n} ({getattr(f, 'scene', '')}): " + " | ".join(dict.fromkeys(seen))); n += 1
