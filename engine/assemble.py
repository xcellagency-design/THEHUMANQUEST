import json, numpy as np, soundfile as sf, subprocess, math, csv
from epload import U
D=json.load(open("durations.json")); sr=D["sr"]; dur=D["dur"]; idx=json.load(open("frames.json"))
LEAD=0.25; t=LEAD; starts=[]; voice=[np.zeros(int(LEAD*sr),np.float32)]; events=[]
for i,u in enumerate(U):
    a,_=sf.read(f"audio/u{i:03d}.wav",dtype="float32"); flag=u[2] if len(u)>2 else None
    gap=0.55 if flag=="chime" else 0.16
    starts.append((t,len(a)/sr+gap)); voice.append(a); voice.append(np.zeros(int(gap*sr),np.float32))
    if flag: events.append((t+len(a)/sr+0.02,flag))
    t+=len(a)/sr+gap
TAIL=1.6; voice.append(np.zeros(int(TAIL*sr),np.float32)); v=np.concatenate(voice); total=len(v)/sr
# frame timings
rows=[]; lines=[]
byu={}
for ui,fi,n in idx: byu.setdefault(ui,[]).append(n)
for ui,(st,du) in enumerate(starts):
    fr=byu[ui]; each=du/len(fr)
    for j,n in enumerate(fr): rows.append((n,round(st+j*each,3),round(each,3),ui,U[ui][0]))
rows[0]=(rows[0][0],0.0,rows[0][2]+rows[0][1],rows[0][3],rows[0][4]); rows[-1]=rows[-1][:2]+(round(rows[-1][2]+TAIL,3),)+rows[-1][3:]
with open("concat.txt","w") as f:
    for n,st,du,ui,tx in rows: f.write(f"file 'frames/f{n:03d}.png'\nduration {du}\n")
    f.write(f"file 'frames/f{rows[-1][0]:03d}.png'\n")
csv.writer(open("shotlist.csv","w",newline="")).writerows([("still","start_s","hold_s","line","narration")]+rows)
holds=[r[2] for r in rows]; print("total",round(total,1),"s; stills",len(rows),"mean hold",round(np.mean(holds),2),"max",max(holds),"min",min(holds))
# ---- music bed + chimes (synthesised here, original) ----
SR=sr; N=len(v); bed=np.zeros(N,np.float32); rng=np.random.default_rng(7)
def pluck(f,d=1.6,amp=1.0):
    n=int(SR/f); buf=rng.uniform(-1,1,n).astype(np.float32); out=np.zeros(int(d*SR),np.float32)
    for i in range(len(out)):
        out[i]=buf[i%n]; buf[i%n]=0.996*0.5*(buf[i%n]+buf[(i+1)%n])
    return out*amp
notes={k:pluck(f) for k,f in {"D3":146.83,"A3":220.0,"D4":293.66,"F4":349.23,"G4":392.0,"A4":440.0,"C5":523.25}.items()}
beat=60/96; pat=["D3",None,"A3","D4",None,"F4","A3",None,"D3",None,"G4","D4",None,"A4","A3",None,"D3",None,"A3","D4",None,"C5","A3",None,"D3",None,"F4","D4",None,"A3",None,None]
i=0; tt=0.0
while tt<total-2:
    k=pat[i%len(pat)]
    if k:
        s0=int(tt*SR); x=notes[k]; e=min(N,s0+len(x)); bed[s0:e]+=x[:e-s0]*0.5
    if i%8==0:
        s0=int(tt*SR); n=int(0.25*SR); tr=np.arange(n)/SR; th=np.sin(2*np.pi*(70-60*tr)*tr)*np.exp(-tr*18); e=min(N,s0+n); bed[s0:e]+=th[:e-s0].astype(np.float32)*0.8
    i+=1; tt+=beat/2
fx=np.zeros(N,np.float32)
def bell(f,d=0.9): tr=np.arange(int(d*SR))/SR; return (np.sin(2*np.pi*f*tr)+0.4*np.sin(2*np.pi*2.01*f*tr))*np.exp(-tr*5)
for et,kind in events:
    s0=int(et*SR)
    seq=[(0,880.0),(0.13,1174.66)] if kind=="chime" else [(0,1318.5)]
    for off,f in seq:
        b=bell(f,0.9 if kind=="chime" else 0.35).astype(np.float32); a0=s0+int(off*SR); e=min(N,a0+len(b)); fx[a0:e]+=b[:e-a0]
vr=np.sqrt(np.mean(v[np.abs(v)>0.02]**2)); br=np.sqrt(np.mean(bed**2)); bed*=vr*10**(-25/20)/br
fx*=vr*10**(-9/20)/np.max(np.abs(fx)+1e-9)*1.6
fade=int(1.5*SR); bed[-fade:]*=np.linspace(1,0,fade); bed[:int(.4*SR)]*=np.linspace(0,1,int(.4*SR))
mix=v+bed+fx; mix/=max(1.0,np.max(np.abs(mix))/0.95); sf.write("mix.wav",mix,SR); sf.write("voice.wav",v,SR)
json.dump({"total":total,"events":events},open("timing.json","w"))
