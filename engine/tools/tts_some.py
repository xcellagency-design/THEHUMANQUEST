"""Re-record only the narration lines that changed (the line count must be the same), then run assemble.py again.

    cd work/EP006 && THSQ_EP=ep06 PYTHONPATH=../../engine python3 ../../engine/tools/tts_some.py 24 34 62"""
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from epload import U
k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin"); D = json.load(open("durations.json"))
for i in map(int, sys.argv[1:]):
    a, sr = k.create(U[i][0], voice="am_michael", speed=1.22, lang="en-us"); a = np.asarray(a, dtype=np.float32); nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz): a = a[max(0, nz[0]-int(.03*sr)):min(len(a), nz[-1]+int(.10*sr))]
    sf.write(f"audio/u{i:03d}.wav", a, sr); D["dur"][i] = len(a)/sr; print(i, round(len(a)/sr, 2), U[i][0][:70])
json.dump(D, open("durations.json", "w"))
