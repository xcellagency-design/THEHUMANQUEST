import sys, csv, math, subprocess, numpy as np, random
from multiprocessing import Pool
import thsq as T, life
from epload import U
from PIL import Image
W,H,S=1920,1080,2; FPS=30
rows=list(csv.reader(open("shotlist.csv")))[1:]
ST=[(float(r[1]),float(r[2])) for r in rows]
FN=[f for u in U for f in u[1]]; assert len(FN)==len(ST)
total=ST[-1][0]+ST[-1][1]; N=int(total*FPS)
# camera groups
G=[]; g0=0
for j in range(len(FN)):
    a=getattr(FN[j],"scene",id(FN[j])); b=getattr(FN[j-1],"scene",id(FN[j-1])) if j else None
    if j and a!=b: g0=j
    G.append(g0)
GE={}
for j,g in enumerate(G): GE[g]=ST[j][0]+ST[j][1]
rs=np.random.RandomState(3); yy,xx=np.mgrid[0:H,0:W]; rr=((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2
M=((251+rs.randint(-6,6,(H,W)))*(1-0.10*rr)).clip(0,256).astype(np.uint16)[:,:,None]
def still_at(t):
    lo,hi=0,len(ST)-1
    while lo<hi:
        m=(lo+hi+1)//2
        if ST[m][0]<=t: lo=m
        else: hi=m-1
    return lo
def setg(fi,t,j,lt):
    T.TT=t; T.FR=fi; T.LT=lt; T.LP=min(1,lt/ST[j][1]); g=G[j]; gs=ST[g][0]; T.GP=min(1,(t-gs)/max(.1,GE[g]-gs))
def frame(fi,cache={}):
    t=fi/FPS; j=still_at(t)
    if cache.get("j")!=j:
        if j>0:
            setg(fi,t,j-1,ST[j-1][1]); T.PREV=set(); T.CUR=set(); FN[j-1](); cache["prev"]=set(T.CUR)
        else: cache["prev"]=set()
        cache["j"]=j
    setg(fi,t,j,t-ST[j][0]); T.PREV=cache["prev"]; T.CUR=set()
    im=FN[j]().im
    g=G[j]; gd=GE[g]-ST[g][0]; zmax=1+min(0.055,0.02*gd); p=T.GP; z=1+(zmax-1)*(p if g%4!=3 else 1-p)
    fx=0; fy=0
    cw,ch=W*S/z,H*S/z; cx=W*S/2+fx*(W*S-cw)/2; cy=H*S/2+fy*(H*S-ch)/2
    im=im.resize((W,H),Image.BILINEAR,box=(cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2),reducing_gap=2.0)
    a=np.asarray(im,dtype=np.uint16); k=(fi//4)%7
    m=np.roll(M,(k*131,k*211),(0,1)) if k else M
    return ((a*m)>>8).astype(np.uint8).tobytes()
def seg(args):
    k,a,b=args
    p=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",f"seg/s{k:03d}.mp4"],stdin=subprocess.PIPE)
    for fi in range(a,b): p.stdin.write(frame(fi))
    p.stdin.close(); p.wait(); return k
if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="test":
        import traceback; bad=0
        for j in range(len(FN)):
            for lt in (0.0,0.1,ST[j][1]*0.5,ST[j][1]-0.01):
                try: frame(int((ST[j][0]+lt)*FPS))
                except Exception as e: bad+=1; print("ERR still",j,getattr(FN[j],"scene","?"),repr(e)[:160]); break
        print("test done, errors:",bad); sys.exit()
    import os; os.makedirs("seg",exist_ok=True)
    P=int(sys.argv[1]) if len(sys.argv)>1 else 8; n=P*3; step=math.ceil(N/n)
    jobs=[(k,k*step,min(N,(k+1)*step)) for k in range(n) if k*step<N]
    with Pool(P) as pool:
        for k in pool.imap_unordered(seg,jobs): print("seg",k,flush=True)
    open("segs.txt","w").write("".join(f"file 'seg/s{k:03d}.mp4'\n" for k,_,_ in jobs)); print("frames",N)
