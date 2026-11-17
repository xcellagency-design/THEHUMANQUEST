import json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from epload import U
k=Kokoro("models/kokoro-v1.0.onnx","models/voices-v1.0.bin")
d=[]
for i,u in enumerate(U):
    a,sr=k.create(u[0],voice="am_michael",speed=1.22,lang="en-us")
    a=np.asarray(a,dtype=np.float32)
    # trim leading/trailing silence, keep small pads
    nz=np.where(np.abs(a)>0.01)[0]
    if len(nz): a=a[max(0,nz[0]-int(.03*sr)):min(len(a),nz[-1]+int(.10*sr))]
    sf.write(f"audio/u{i:03d}.wav",a,sr); d.append(len(a)/sr)
json.dump({"sr":sr,"dur":d},open("durations.json","w")); print("done",sum(d))
