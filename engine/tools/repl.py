"""Replace top-level functions in an episode module with the ones in a patch file (new ones go in just before 'def Fq').
Use it for a round of review fixes: write the corrected scene functions into one file, apply, preview.

    python3 engine/tools/repl.py engine/ep06.py patch.py"""
import re, sys
def blocks(src):
    out = []; cur = None
    for ln in src.split("\n"):
        m = re.match(r"def (\w+)\(", ln)
        if m: cur = [m.group(1), [ln]]; out.append(cur)
        elif cur is not None and (ln.startswith(" ") or ln.startswith("\t")): cur[1].append(ln)
        else: cur = None; out.append([None, [ln]])
    return out
P = sys.argv[1]; src = blocks(open(P).read()); new = [(n, b) for n, b in blocks(open(sys.argv[2]).read()) if n]; names = {n for n, _ in src if n}; nd = dict(new); done = []; res = []
for n, b in src:
    if n == "Fq":
        for m, bb in new:
            if m not in names: res.append("\n".join(bb)); done.append("+"+m)
    if n in nd: res.append("\n".join(nd[n])); done.append(n)
    else: res.append("\n".join(b))
open(P, "w").write("\n".join(res)); print(len(done), "defs:", " ".join(done))
