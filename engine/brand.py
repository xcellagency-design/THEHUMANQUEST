import math, os, numpy as np
import thsq as T, life, ep01
from thsq import *
from PIL import Image, ImageDraw, ImageFont
OUT=T.OUTROOT+"/brand/"
DF=next(f for f in ("LuckiestGuy-Regular.ttf","Bangers-Regular.ttf","PatrickHandSC-Regular.ttf") if os.path.exists(T.FDIR+f) and os.path.getsize(T.FDIR+f)>20000)
def dfont(sz): return ImageFont.truetype(T.FDIR+DF, int(sz))
def hfont(sz): return ImageFont.truetype(T.FDIR+"PatrickHandSC-Regular.ttf", int(sz))
def title(d, xy, t, sz, fill=PAPER, stroke=INK, sw=None, anchor="mm", font=None):
    d.multiline_text(xy, t, font=(font or dfont)(sz), fill=fill, stroke_width=int(sw if sw is not None else sz*0.09), stroke_fill=stroke, anchor=anchor, align="center", spacing=sz*0.12)
def fit(d, t, maxw, sz):
    while sz>30 and max(d.textlength(l, font=dfont(sz)) for l in t.split("\n"))>maxw: sz-=4
    return sz
# ---- avatar ----
def avatar():
    c=C(NAVY); c.da.ellipse([200*S,-100*S,1720*S,1300*S], fill=(31,167,160,60))
    c.fig(960,1900,1180,"stand","smile","sid"); c.marker(985,150,62)
    im=c.im.crop((420*S,0,1500*S,1080*S)).resize((800,800),Image.LANCZOS); im.save(OUT+"THSQ_avatar_800.png"); return im
# ---- banner ----
def banner():
    c=C().bg("sand",640); c.pyramid(1660,640,560,340,STONE,1,8); c.pyramid(1330,640,260,160,(232,220,196),1,5)
    c.fig(462,696,206,"walk","smile","sid"); c.marker(462,392,22)
    for x in (110,250): c.hut(x,700,120,90)
    c.sledge(40,930,260); c.block(55,908,230,150)
    im=c.im.resize((2560,1440),Image.LANCZOS); d=ImageDraw.Draw(im); k=2560/1920
    title(d,(1055*k,500*k),"THE HUMAN SIDE QUEST",88*k,PAPER,INK)
    tw=d.textlength("HISTORY'S SIDE QUESTS, PLAYED BY YOU",font=hfont(50*k))
    d.rounded_rectangle([1055*k-tw/2-34,600*k-44,1055*k+tw/2+34,600*k+44],radius=22,fill=MARI,outline=INK,width=6)
    d.text((1055*k,598*k),"HISTORY'S SIDE QUESTS, PLAYED BY YOU",font=hfont(50*k),fill=INK,anchor="mm")
    im.save(OUT+"THSQ_banner_2560x1440.png"); return im
# ---- main thumbnail ----
def thumb():
    c=C().bg("sand",760); c.pyramid(1250,760,900,520,(232,222,200),.62,7)
    c.da.ellipse([1300*S,330*S,1900*S,930*S], fill=(255,214,90,120))
    c.sledge(560,960,520); c.block(590,938,470,400)
    s=c.fig(300,1010,540,"pull","strain","sid"); c.line([(610,760),s["hand"]],14,EARTH)
    c.jar(1590,930,3.5)
    im=c.im.resize((1280,720),Image.LANCZOS); d=ImageDraw.Draw(im)
    title(d,(800,118),"PAID IN BEER",136,MARI,INK,13)
    d.line([(500,206),(1100,194)],fill=RED,width=13)
    im.save(OUT+"THSQ_EP001_thumbnail.png"); return im
# ---- short covers ----
def art(i):
    if i==0: c=C().bg("sand",700); c.pyramid(960,700,900,520); c.fig(960,980,520,"shrug","worry","sid"); c.redx(1290,300,95,30)
    if i==1:
        c=C().bg("sand",700); c.da.ellipse([900*S,880*S,1500*S,1000*S],fill=(150,110,60,150)); c.sledge(380,960,300); c.block(400,938,260,220)
        p=c.fig(900,960,470,"pour","smile","sid"); hx,hy=p["hand"]; c.jar(hx+30,hy+60,1.5,False)
        for k in range(5): c.line([(hx+110+k*22,hy+40+k*60),(hx+120+k*22,hy+78+k*60)],12,WATER)
    if i==2: c=C().bg("river",600); c.pyramid(1250,600,520,300,WHITE); m=c.fig(880,940,500,"write","det","scribe"); c.papyrus(m["hand"][0]+110,m["hand"][1]+10,1.3); c.boat(560,980,820)
    if i==3:
        c=C().bg("sand",760); s=c.fig(820,1010,520,"hold","joy","sid"); hx,hy=s["hand"]
        for k in range(6): c.loaf(hx+30+(k%2)*14,hy-k*58,1.5)
        c.jar(1240,1000,2.6)
    if i==4:
        c=C().bg("hall",560); c.rect(520,985,1400,1015,(226,200,150),INK,6,8); s=c.fig(820,985,470,"wave","smile","sid",sit=True)
        for y in (905,962): c.line([(860,y),(1090,y+14)],18,EARTH)
        for x in (900,975,1050): c.line([(x,892),(x,990)],16,PAPER); c.line([(x-10,892),(x-10,990)],5); c.line([(x+10,892),(x+10,990)],5)
        c.loaf(s["hand"][0]+10,s["hand"][1]-20,1.7)
    if i==5:
        c=C(STONE)
        for y in (360,720): c.line([(0,y),(W,y)],6,(190,176,150))
        c.line([(560,330),(820,270),(1060,350),(1340,280)],54,RED); s=c.fig(960,1010,520,"cheer","joy","sid"); hx,hy=s["head"]; c.ell(hx+10,hy+110,hx+50,hy+150,RED,None)
    x0=420
    return c.im.crop((x0*S,0,(x0+1080)*S,1080*S)).resize((960,960),Image.LANCZOS)
TITLES=["THE PYRAMID\nLIE","THE WET SAND\nTRICK","THE OLDEST\nTIMESHEET","PAID\nIN BEER","HEALTHCARE\nIN 2560 BC","THEY\nSIGNED IT"]
def header(d, y=150):
    tw=d.textlength("THE HUMAN SIDE QUEST",font=hfont(50)); x=540-tw/2+30
    d.polygon([(x-58,y),(x-36,y-30),(x-14,y),(x-36,y+30)],fill=TEAL,outline=INK); d.text((x,y),"THE HUMAN SIDE QUEST",font=hfont(50),fill=PAPER,anchor="lm")
def cover(i):
    im=Image.new("RGB",(1080,1920),NAVY); d=ImageDraw.Draw(im); header(d,170)
    sz=fit(d,TITLES[i],980,190); title(d,(540,470),TITLES[i],sz,MARI,INK)
    d.rounded_rectangle([48,728,1032,1712],radius=36,fill=PAPER,outline=INK,width=8); a=art(i); m=Image.new("L",(960,960),0); ImageDraw.Draw(m).rounded_rectangle([0,0,960,960],radius=28,fill=255); im.paste(a,(60,740),m)
    d.text((540,1800),"WATCH THE FULL QUEST",font=hfont(56),fill=PAPER,anchor="mm")
    im.save(T.OUTROOT+f"/shorts/THSQ_short{i+1}_cover.png"); return im
if __name__=="__main__":
    a=avatar(); b=banner(); t=thumb(); cs=[cover(i) for i in range(6)]
    sh=Image.new("RGB",(1920,1080),"white"); sh.paste(a.resize((360,360)),(0,0)); sh.paste(b.resize((640,360)),(360,0)); sh.paste(t.resize((640,360)),(1000,0))
    # safe-area guide on banner preview
    ImageDraw.Draw(sh).rectangle([360+640*507/2560,360*508/1440,360+640*2053/2560,360*931/1440],outline=(255,0,0),width=2)
    for i,cimg in enumerate(cs): sh.paste(cimg.resize((320,569)),(i*320,400))
    sh.save("brand_check.jpg",quality=82); print("font",DF)
