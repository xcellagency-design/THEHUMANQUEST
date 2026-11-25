"""Transcribe narration lines with a larger recogniser and print the ones that differ from the script (names said wrong show up here).

    THSQ_EP=ep06 python3 engine/tools/hear.py EP006 [line numbers...]      all lines when none are given; run after tts.py"""
import sys, os, subprocess, difflib, re, importlib, tempfile
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
ep = importlib.import_module(os.environ.get("THSQ_EP", "ep01"))
import soundfile as sf
from faster_whisper import WhisperModel
m = WhisperModel("small.en", compute_type="int8"); W_ = os.path.join(os.path.dirname(HERE), "work", sys.argv[1], "audio")
want = [int(a) for a in sys.argv[2:]] or range(len(ep.U)); tot = 0; n = 0; tmp = os.path.join(tempfile.gettempdir(), f"_hear{os.getpid()}.wav")
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower().replace("-", " ")).split()
for i in want:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{W_}/u{i:03d}.wav", "-ac", "1", "-ar", "16000", tmp], check=True)
    x, sr = sf.read(tmp, dtype="float32"); segs, _ = m.transcribe(x); heard = " ".join(s.text.strip() for s in segs)   # samples, not a path: the recogniser cannot read a wav path in this image
    r = difflib.SequenceMatcher(None, norm(ep.U[i][0]), norm(heard)).ratio(); tot += r; n += 1
    if r < .93: print(f"{i:3d} {r:.2f}\n   SCRIPT: {ep.U[i][0]}\n   HEARD:  {heard}", flush=True)
print("mean match", round(tot/max(1, n), 3), "lines", n, "(numbers heard as digits lower the score; a line cut short may be the recogniser: listen again from a later start)")
