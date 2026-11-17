"""Cut vertical Shorts from a finished long episode.

    cd 03_episodes/EP002/work && THSQ_EP=ep02 PYTHONPATH=../../../engine python3 ../../../engine/make_shorts.py EP002 ../../../out/THSQ_EP002_slug.mp4 clips.json

clips.json: [{"n": 1, "units": [0, 6], "title": "TWO LINE\\nTITLE", "slug": "two-line-title", "cover_unit": 3}, ...]
units = first and last narration line (inclusive) of the clip. Pick ranges that open on a hook and end on a
complete thought. For each clip this writes the mp4 (1080x1920, burned-in word captions), a cover png, an .srt
and a .words.json used by QC. Audio is muted right after the last line so the next sentence cannot leak in.
"""
import csv, json, os, re, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw
import thsq as T
from thsq import NAVY, PAPER, MARI, INK, TEAL
from brand import dfont, hfont, title, header, fit
import epload, importlib

FPS = 30
U = epload.U
FIX = getattr(importlib.import_module(os.environ.get("THSQ_EP", "ep01")), "CAPTION_FIX", [])
rows = list(csv.reader(open("shotlist.csv")))[1:]
D = json.load(open("durations.json"))["dur"]
us = {}
for r in rows:
    us.setdefault(int(r[3]), float(r[1]))
us[0] = 0.25


def words(ui):
    t = U[ui][0]
    for a, b in FIX:
        t = t.replace(a, b)
    ws = t.split(); wt = [len(re.sub(r"\W", "", w)) + 1.5 for w in ws]; tot = sum(wt); out = []; a = us[ui]
    for w, x in zip(ws, wt):
        out.append((w.upper(), a, a + D[ui] * x / tot)); a += D[ui] * x / tot
    return out


def chunks(units):
    ch = []; cur = []
    for ui in units:
        for w in words(ui):
            cur.append(w)
            if len(cur) >= 3 or sum(len(x[0]) for x in cur) >= 13 or w[0][-1] in ".?!,:":
                ch.append(cur); cur = []
        if cur:
            ch.append(cur); cur = []
    return ch


def ts(t):
    t = max(0, t)
    return f"{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round((t%1)*1000))%1000:03d}"


def make(epid, src, clip, outdir):
    a, b = clip["units"]; ttl = clip["title"]
    t0 = max(0, us[a] - 0.12); end = us[b] + D[b]; t1 = end + 0.5; n = int((t1 - t0) * FPS); ch = chunks(range(a, b + 1))
    stem = os.path.join(outdir, f"THSQ_{epid}_short{clip['n']}_{clip['slug']}")
    base = Image.new("RGB", (1080, 1920), NAVY); d = ImageDraw.Draw(base); header(d, 170)
    title(d, (540, 400), ttl, fit(d, ttl, 980, 150), MARI, INK)
    d.rounded_rectangle([0, 612, 1080, 1244], radius=0, fill=PAPER); d.text((540, 1650), "FULL EPISODE ON THE CHANNEL", font=hfont(46), fill=PAPER, anchor="mm")
    cap = cv2.VideoCapture(src); cap.set(cv2.CAP_PROP_POS_FRAMES, int(t0 * FPS)); x = end + 0.06 - t0
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS), "-i", "-", "-ss", f"{t0:.3f}", "-t", f"{t1-t0:.3f}", "-i", src,
                          "-map", "0:v", "-map", "1:a", "-af", f"afade=t=in:d=0.15,afade=t=out:st={x:.3f}:d=0.10,volume=enable='gte(t,{x+0.10:.3f})':volume=0",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", stem + ".mp4"], stdin=subprocess.PIPE)
    navy = np.array(NAVY, np.float32)[None, None, :]; ci = 0
    for f in range(n):
        t = t0 + f / FPS; ok, fr = cap.read()
        if not ok:
            break
        im = base.copy(); v = Image.fromarray(cv2.cvtColor(cv2.resize(fr, (1080, 608), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB))
        im.paste(v, (0, 624 + int((1 - min(1, f / 8)) ** 2 * 120))); dd = ImageDraw.Draw(im)
        while ci + 1 < len(ch) and t >= ch[ci + 1][0][1]:
            ci += 1
        c = ch[ci]
        if c[0][1] - 0.05 <= t <= c[-1][2] + 0.7:
            txt = " ".join(w[0] for w in c); s2 = 96
            while s2 > 50 and dd.textlength(txt, font=dfont(s2)) > 980:
                s2 -= 6
            xx = 540 - dd.textlength(txt, font=dfont(s2)) / 2
            for w in c:
                on = w[1] <= t < w[2] or (w is c[-1] and t >= w[1])
                dd.text((xx, 1420), w[0], font=dfont(s2), fill=MARI if on else PAPER, stroke_width=int(s2 * 0.09), stroke_fill=INK, anchor="lm")
                xx += dd.textlength(w[0] + " ", font=dfont(s2))
        dd.rectangle([0, 1716, int(1080 * f / max(1, n - 1)), 1728], fill=TEAL)
        arr = np.asarray(im, np.float32); k = min(1, f / 6, (n - 1 - f) / 8)
        if k < 1:
            arr = arr * k + navy * (1 - k)
        p.stdin.write(arr.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    json.dump([(w, round(s - t0, 3), round(e - t0, 3)) for u in range(a, b + 1) for w, s, e in words(u)], open(stem + ".words.json", "w"))
    srt = []
    for k, c in enumerate(ch):
        s = c[0][1] - t0; e = (min(c[-1][2] + 0.7, ch[k + 1][0][1]) if k + 1 < len(ch) else c[-1][2] + 0.5) - t0
        srt.append(f"{k+1}\n{ts(s)} --> {ts(e)}\n{' '.join(w[0] for w in c)}\n")
    open(stem + ".srt", "w").write("\n".join(srt))
    cu = clip.get("cover_unit", a); cap.set(cv2.CAP_PROP_POS_MSEC, (us[cu] + 0.6 * D[cu]) * 1000); ok, fr = cap.read()
    art = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)).crop((420, 0, 1500, 1080)).resize((960, 960), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), NAVY); d = ImageDraw.Draw(im); header(d, 170); title(d, (540, 470), ttl, fit(d, ttl, 980, 190), MARI, INK)
    d.rounded_rectangle([48, 728, 1032, 1712], radius=36, fill=PAPER, outline=INK, width=8)
    m = Image.new("L", (960, 960), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, 960, 960], radius=28, fill=255); im.paste(art, (60, 740), m)
    d.text((540, 1800), "WATCH THE FULL QUEST", font=hfont(56), fill=PAPER, anchor="mm"); im.save(stem + "_cover.png")
    return stem + ".mp4", round(t1 - t0, 1)


if __name__ == "__main__":
    epid, src, cj = sys.argv[1:4]
    outdir = os.path.join(T.OUTROOT, "shorts"); os.makedirs(outdir, exist_ok=True)
    only = set(map(int, sys.argv[4:]))
    for clip in json.load(open(cj)):
        if not only or clip["n"] in only:
            print(make(epid, os.path.abspath(src), clip, outdir), flush=True)
