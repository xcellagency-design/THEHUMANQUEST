import sys, json, numpy as np
from epload import U
from PIL import Image
idx=[]; n=0
for ui,u in enumerate(U):
    for fi,f in enumerate(u[1]):
        try: im=f().out()
        except Exception as e:
            import traceback; print("ERR unit",ui,"frame",fi,repr(e)); traceback.print_exc(limit=2); raise SystemExit(1)
        im.save(f"frames/f{n:03d}.png"); idx.append((ui,fi,n)); n+=1
json.dump(idx,open("frames.json","w")); print("frames",n,"units",len(U),"words",sum(len(u[0].split()) for u in U))
# contact sheets
cols,rows=8,6; per=cols*rows
for k in range(0,n,per):
    sheet=Image.new("RGB",(cols*240,rows*135),"white")
    for j in range(k,min(n,k+per)):
        t=Image.open(f"frames/f{j:03d}.png").resize((240,135)); sheet.paste(t,(((j-k)%cols)*240,((j-k)//cols)*135))
    sheet.save(f"sheet{k//per}.jpg",quality=80)
