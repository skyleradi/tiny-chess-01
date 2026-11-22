import json,os,random,urllib.request as u
ENV_URL=os.environ.get("MAKEFUN_ENV_URL")
MATE=10**6
INF=10*MATE
N_OFF=(-21,-19,-12,-8,8,12,19,21)
K_OFF=(-11,-10,-9,-1,1,9,10,11)
B_DIR=(-11,-9,9,11)
R_DIR=(-10,-1,1,10)
VAL=(0,100,320,330,500,900,20000)
PHASE=(0,0,1,1,2,4,0)
CMASK=[15]*120
for j,mk in ((25,12),(21,13),(28,14),(95,3),(91,7),(98,11)):CMASK[j]=mk
CMASK=tuple(CMASK)
RC={27:(28,26),23:(21,24),97:(98,96),93:(91,94)}
G=random.Random(0x5EED).getrandbits
ZP=[[G(64) for _ in range(120)] for _ in range(13)]
ZS=G(64)
ZC=[G(64) for _ in range(16)]
ZE=[G(64) for _ in range(8)]
P_MG=(0,)*8+(60,)*8+sum((r+r[::-1] for r in ((18,18,26,34),(8,10,14,26),(2,4,8,22),(2,-2,-4,5),(4,8,8,-18))),())+(0,)*8
P_EG=sum(([v]*8 for v in (0,90,55,34,18,8,2,0)),[])
N_MG=sum((r+r[::-1] for r in ((-50,-38,-30,-30),(-38,-18,0,4),(-30,4,14,20),(-30,2,20,26),(-30,4,20,26),(-30,6,14,20),(-38,-18,0,6),(-50,-38,-30,-30))),())
B_MG=sum((r+r[::-1] for r in ((-20,-10,-10,-10),(-10,0,0,0),(-10,0,6,10),(-10,6,6,12),(-10,0,12,12),(-10,10,10,10),(-10,8,0,0),(-20,-10,-14,-10))),())
R_MG=(0,)*8+(10,16,16,16,16,16,16,10)+(-4,0,0,0,0,0,0,-4)*5+(0,0,2,6,6,2,0,0)
K_MG=sum((r+r[::-1] for r in ((-60,-70,-70,-76),(-56,-62,-66,-70),(-46,-52,-56,-62),(-36,-42,-46,-52),(-24,-30,-36,-42),(-14,-18,-24,-30),(4,-2,-10,-16))),())+(20,30,12,0,0,10,32,20)
Ae=((-50,-30,-20,-14),(-30,-12,0,6),(-20,0,14,20),(-14,6,20,28))
K_EG=sum((r+r[::-1] for r in Ae+Ae[::-1]),())
VMG=(None,P_MG,N_MG,B_MG,R_MG,R_MG,K_MG)
PW=(0,5,10,18,30,55,95)
VEG=(None,P_EG,N_MG,B_MG,R_MG,R_MG,K_EG)
def sq_of(u):
 return 21+10*(int(u[1])-1)+(ord(u[0])-97)
def nm(i):
 q=i-21
 return chr(97+q % 10)+str(q//10+1)
def pf(fen):
 parts=fen.split()
 b=[7]*21+([0]*8+[7]*2)*7+[0]*8+[7]*21
 for i,row in enumerate(parts[0].split("/")):
  r=7-i
  f=0
  for c in row:
   if c.isdigit():
    f += int(c)
   else:
    p="PNBRQK".index(c.upper())+1
    b[21+10*r+f]=p if c.isupper() else -p
    f += 1
 s=1 if parts[1]=="w" else -1
 cs=0
 if "-" not in parts[2]:
  for c in parts[2]:
   cs |= {"K": 1,"Q": 2,"k": 4,"q": 8}.get(c,0)
 ep=sq_of(parts[3]) if parts[3]!="-" else 0
 hf=int(parts[4]) if len(parts)>4 else 0
 return b,s,cs,ep,hf
def key0(b,s,cs,ep):
 k=0
 for i in range(21,99):
  p=b[i]
  if p and p!=7:
   k ^= ZP[p+6][i]
 if s<0:
  k ^= ZS
 k ^= ZC[cs]
 if ep:
  k ^= ZE[ep & 7]
 return k
def att(b,q2,by,N_OFF=N_OFF,K_OFF=K_OFF,B_DIR=B_DIR,R_DIR=R_DIR):
 if by>0:
  if b[q2-9]==1 or b[q2-11]==1:
   return True
  n,bi,r,q,k=2,3,4,5,6
 else:
  if b[q2+9]==-1 or b[q2+11]==-1:
   return True
  n,bi,r,q,k=-2,-3,-4,-5,-6
 for d in N_OFF:
  if b[q2+d]==n:
   return True
 for d in K_OFF:
  if b[q2+d]==k:
   return True
 for d in B_DIR:
  t=q2+d
  while b[t]==0:
   t+=d
  e=b[t]
  if e==bi or e==q:
   return True
 for d in R_DIR:
  t=q2+d
  while b[t]==0:
   t+=d
  e=b[t]
  if e==r or e==q:
   return True
 return False
def gen(b,s,cs,ep,K,att=att,CMASK=CMASK,
  N_OFF=N_OFF,K_OFF=K_OFF,B_DIR=B_DIR,R_DIR=R_DIR):
 
 ms=[]
 ap=ms.append
 for i in range(21,99):
  p=b[i]
  if not p or p==7 or (p>0)!=(s>0):
   continue
  a=p if p>0 else -p
  if a==1:
   fwd=10*s
   t=i+fwd
   if b[t]==0:
    r=(i-21)//10
    if r==6 if s>0 else r==1:
     for pr in (5,4,3,2):
      ap((i,t,pr*s,0))
    else:
     ap((i,t,0,0))
     if b[t+fwd]==0 and (r==1 if s>0 else r==6):
      ap((i,t+fwd,0,1))
   for d in (fwd-1,fwd+1):
    t=i+d
    q=b[t]
    if q!=7 and q and (q>0)!=(s>0):
     r=(i-21)//10
     if r==6 if s>0 else r==1:
      for pr in (5,4,3,2):
       ap((i,t,pr*s,0))
     else:
      ap((i,t,0,0))
    elif ep and t==ep:
     ap((i,t,0,2))
  elif a==2 or a==6:
   for d in (N_OFF if a==2 else K_OFF):
    t=i+d
    q=b[t]
    if q!=7 and (q==0 or (q>0)!=(s>0)):
     ap((i,t,0,0))
  else:
   dirs=B_DIR if a==3 else R_DIR if a==4 else B_DIR+R_DIR
   for d in dirs:
    t=i+d
    while b[t]==0:
     ap((i,t,0,0))
     t += d
    q=b[t]
    if q!=7 and (q>0)!=(s>0):
     ap((i,t,0,0))
 for bi,fr,to,es in ((1,25,27,(26,27)),(2,25,23,(22,23,24)),
   (4,95,97,(96,97)),(8,95,93,(92,93,94))):
  sg=(to-fr)//2
  if cs&bi and (to>90)==(s<0) and not any(b[j] for j in es) and not any(
    att(b,j,-s) for j in range(fr,to+sg,sg)):
   ap((fr,to,0,3))
 return ms
def make(b,s,cs,ep,hf,K,ky,m,ZP=ZP,ZC=ZC,ZE=ZE,ZS=ZS,
  CMASK=CMASK):
 f,t,pr,fl=m
 p=b[f]
 cap=b[t]
 nk=ky ^ ZP[p+6][f] ^ ZC[cs]
 b[f]=0
 np=pr if pr else p
 b[t]=np
 nk ^= ZP[np+6][t]
 if cap:
  nk ^= ZP[cap+6][t]
 nh=0 if (cap or p==1 or p==-1) else hf+1
 nep=0
 if fl:
  if fl==1:
   nep=(f+t) >> 1
   nk ^= ZE[t & 7]
  elif fl==2:
   xq=t-10*s
   cp=b[xq]
   b[xq]=0
   nk ^= ZP[cp+6][xq]
  else:
   rf,rk=RC[t]
   b[rf]=0
   b[rk]=4*s
   nk ^= ZP[4*s+6][rf] ^ ZP[4*s+6][rk]
   K[0 if s>0 else 1]=t
 elif p==6:
  K[0]=t
 elif p==-6:
  K[1]=t
 nc=cs & CMASK[f] & CMASK[t]
 nk ^= ZC[nc] ^ ZS
 if ep:
  nk ^= ZE[ep & 7]
 return cap,nep,nc,nh,nk
def um(b,s,K,m,cap):
 f,t,pr,fl=m
 p=b[t]
 b[f]=s if pr else p
 b[t]=cap
 if fl==2:
  b[t-10*s]=-s
 elif fl==3:
  rf,rk=RC[t]
  b[rk]=0
  b[rf]=4*s
  K[0 if s>0 else 1]=f
 elif p==6:
  K[0]=f
 elif p==-6:
  K[1]=f
def ev(b,s,VMG=VMG,VEG=VEG,VAL=VAL,PHASE=PHASE):
 mg=eg=ph=0
 wb=bb=0
 wf,bf,wt=[[0]*10 for _ in range(3)];bt=[9]*10
 wp=[];bp=[]
 for i in range(21,99):
  p=b[i]
  if p in (0,7):continue
  q=i-21;r=q//10;j=q%10+1
  a=p if p>0 else -p
  t64=(7-r if p>0 else r)*8+j-1
  sg=p//a
  mg+=sg*(VMG[a][t64]+VAL[a])
  eg+=sg*(VEG[a][t64]+VAL[a])
  ph+=PHASE[a]
  if a==3:
   if p>0:wb+=1
   else:bb+=1
  elif a==1:
   if p>0:
    wf[j]+=1
    if r>wt[j]:wt[j]=r
    wp.append(i)
   else:
    bf[j]+=1
    if r<bt[j]:bt[j]=r
    bp.append(i)
 if wb>1:mg+=28;eg+=42
 if bb>1:mg-=28;eg-=42
 for L,c in ((wp,1),(bp,-1)):
  for i in L:
   q=i-21;r=q//10;j=q%10+1
   O,T=(bf,bt) if c>0 else (wf,wt)
   if not O[j] and (T[j-1]-r)*c>0 and (T[j+1]-r)*c>0:eg+=PW[r if c>0 else 7-r]*c
 ph=min(ph,24)
 z=(mg*ph+eg*(24-ph))//24
 return (z if s>0 else -z)+8
TT={}
KL=[[0,0]for _ in range(100)]
HB=[0]*14400
def qs(b,s,cs,ep,hf,K,ky,al,be,py,att=att,gen=gen,make=make,
  um=um,ev=ev,VAL=VAL,MATE=MATE,INF=INF):
 global ND
 ND += 1
 if ND>HD:
  raise OverflowError
 if att(b,K[1] if s>0 else K[0],s):
  return MATE-py
 inchk=att(b,K[0] if s>0 else K[1],-s)
 if inchk:
  ms=gen(b,s,cs,ep,K)
  if not ms:
   return -MATE+py+1
  bs=-INF
 else:
  bs=ev(b,s)
  if bs>=be or py>=60:
   return bs
  if bs>al:
   al=bs
  ms=[m for m in gen(b,s,cs,ep,K)
   if b[m[1]] or m[2] or m[3]==2]
  if not ms:
   return bs
 scd=[]
 for m in ms:
  v=b[m[1]]
  z=VAL[v if v>0 else -v]*10-VAL[b[m[0]] if b[m[0]]>0 else -b[m[0]]] if v else 0
  if m[2]:
   z += 900+abs(m[2])
  if m[3]==2:
   z=1000
  scd.append((z,m))
 scd.sort(reverse=True)
 for z,m in scd:
  cap,nep,nc,nh,nk=make(b,s,cs,ep,hf,K,ky,m)
  sc=-qs(b,-s,nc,nep,nh,K,nk,-be,-al,py+1)
  um(b,s,K,m,cap)
  if sc>bs:
   bs=sc
   if sc>al:
    al=sc
    if al>=be:
     break
 return bs
def sx(b,s,cs,ep,hf,K,ky,dp,al,be,py,att=att,gen=gen,make=make,
  um=um,ev=ev,qs=qs,VAL=VAL,HB=HB,KL=KL,MATE=MATE,INF=INF,
  ZS=ZS,ZE=ZE):
 global ND
 ND += 1
 if ND>HD:
  raise OverflowError
 if att(b,K[1] if s>0 else K[0],s):
  return MATE-py
 inchk=att(b,K[0] if s>0 else K[1],-s)
 if inchk and py<60:
  dp += 1
 if hf>=100:
  return 0
 if ky in HSET:
  return 0
 e=TT.get(ky)
 tm=0
 if e is not None:
  ed,ef,es,tm=e
  if ed>=dp:
   if ef==0:
    return es
   if ef==1 and es>=be:
    return es
   if ef==2 and es<=al:
    return es
 if dp<=0:
  return qs(b,s,cs,ep,hf,K,ky,al,be,py)
 if not inchk and dp>=3 and py>0 and any(1<p*s<6 for p in b):
   nk=ky ^ ZS ^ (ZE[ep & 7] if ep else 0)
   sc=-sx(b,-s,cs,0,hf,K,nk,
      dp-3,-be,-be+1,py+1)
   if sc>=be:
    return be
 ms=gen(b,s,cs,ep,K)
 if not ms:
  return ev(b,s)
 scd=[]
 kl=KL[py]
 for m in ms:
  v=b[m[1]]
  if v:
   z=100000+VAL[v if v>0 else -v]*10-VAL[b[m[0]] if b[m[0]]>0 else -b[m[0]]]
  elif m[2]:
   z=90000+abs(m[2])
  elif m==kl[0] or m==kl[1]:
   z=80000
  else:
   z=HB[m[0]*120+m[1]]
  if e is not None and m==e[3]:
   z=1 << 30
  scd.append((z,m))
 scd.sort(reverse=True)
 bs=-INF
 bm=ms[0]
 fst=True
 ncut=0
 for z,m in scd:
  cap,nep,nc,nh,nk=make(b,s,cs,ep,hf,K,ky,m)
  quiet=not cap and not m[2] and m[3]!=2
  if fst:
   sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1,-be,-al,py+1)
   fst=False
  else:
   red=1 if (dp>=3 and quiet and ncut>=3 and not inchk) else 0
   sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1-red,
      -al-1,-al,py+1)
   if sc>al and sc<be:
    sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1,
       -be,-al,py+1)
  um(b,s,K,m,cap)
  ncut += 1
  if sc>bs:
   bs=sc
   bm=m
   if sc>al:
    al=sc
    if al>=be:
     if quiet:
      if kl[0]!=m:
       kl[1]=kl[0]
       kl[0]=m
      HB[m[0]*120+m[1]] += dp*dp
     break
 if bs>-MATE+2000 and bs<MATE-2000:
  if bs>=be:
   TT[ky]=(dp,1,bs,bm)
  elif bs<=al:
   TT[ky]=(dp,2,bs,bm)
  else:
   TT[ky]=(dp,0,bs,bm)
 return bs
def uof(m):
 f,t,pr,fl=m
 u=nm(f)+nm(t)
 if pr:
  u+="  nbrq"[abs(pr)]
 return u
def mof(b,s,cs,ep,u):
 f=sq_of(u[:2])
 t=sq_of(u[2:4])
 pr=0
 if len(u)>4:
  pr="  nbrq".index(u[4])*s
 fl=0
 p=b[f]
 if p in (1,-1):
  if ep and t==ep:
   fl=2
  elif abs(t-f)==20:
   fl=1
 elif p in (6,-6) and abs(t-f)==2:
  fl=3
 return (f,t,pr,fl)
def think(g):
 
 global ND,HD,HSET
 b,s,cs,ep,hf=pf(g["start_fen"])
 K=[b.index(6),b.index(-6)]
 ky=key0(b,s,cs,ep)
 HSET={ky}
 for u in g["moves"]:
  m=mof(b,s,cs,ep,u)
  cap,nep,nc,nh,ky=make(b,s,cs,ep,hf,K,ky,m)
  cs,ep,hf=nc,nep,nh
  s=-s
  HSET.add(ky)
 TT.clear()
 for k in KL:
  k[0]=k[1]=0
 ND=0
 HD=320000
 rt=[mof(b,s,cs,ep,u) for u in g["legal_moves"]]
 if len(rt)==1:
  return uof(rt[0]),0,0
 scs={}
 bs=bd=rt[0]
 try:
  for dp in range(1,64):
   if ND>HD:
    break
   al=-INF
   if scs:rt.sort(key=scs.get,reverse=True)
   fst=True
   for m in rt:
    cap,nep,nc,nh,nk=make(b,s,cs,ep,hf,K,ky,m)
    if fst:
     sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1,
        -INF,-al,1)
     fst=False
    else:
     sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1,
        -al-1,-al,1)
     if sc>al:
      sc=-sx(b,-s,nc,nep,nh,K,nk,dp-1,
         -INF,-al,1)
    um(b,s,K,m,cap)
    scs[m]=sc
    if sc>al:
     al=sc
     bs=m
    bd=bs
 except:pass
 return uof(bd),dp,ND
def post(path,body):
 req=u.Request(
  ENV_URL+path,
  data=json.dumps(body).encode())
 try:
  with u.urlopen(req) as res:
   return json.load(res)
 except:return{}
def main():
 while ENV_URL:
  g=post("/game",{})
  if g.get("status")=="done":
   break
  while g.get("status")=="your_move":
   mv=think(g)[0]
   if mv not in g["legal_moves"]:
    mv=g["legal_moves"][0]
   g=post("/move",{"game": g["game"],"move": mv})
main()
