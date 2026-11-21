import os,json,urllib.request
V=[0,100,320,330,500,900,20000]
D=[[],[],[31,33,14,18,-31,-33,-14,-18],[15,17,-15,-17],[1,16,-1,-16],[1,16,-1,-16,15,17,-15,-17],[1,16,-1,-16,15,17,-15,-17]]
S=[i for i in range(128) if not i&136]
def hit(b,k,c):
 for i in S:
  p=b[i]*c
  if p<=0:continue
  if p==1:
   if k-i in (15*c,17*c):return True
  else:
   for d in D[p]:
    j=i+d
    while not j&136:
     if j==k:return True
     if b[j] or p in (2,6):break
     j+=d
 return False
def moves(b,c,r,e):
 for i in S:
  p=b[i]*c
  if p<=0:continue
  if p==1:
   j=i+16*c
   if not j&136 and not b[j]:
    for q in ([5,2,3,4] if j//16 in (0,7) else [0]):yield i,j,q
    k=j+16*c
    if i//16==(1 if c==1 else 6) and not b[k]:yield i,k,0
   for d in (15*c,17*c):
    j=i+d
    if not j&136 and (b[j]*c<0 or j==e):
     for q in ([5,2,3,4] if j//16 in (0,7) else [0]):yield i,j,q
  else:
   for d in D[p]:
    j=i+d
    while not j&136 and b[j]*c<=0:
     yield i,j,0
     if b[j] or p in (2,6):break
     j+=d
   if p==6 and i==(4 if c==1 else 116) and not hit(b,i,-c):
    for t,h,empty in ((2,'K' if c==1 else 'k',[1,2]),(-2,'Q' if c==1 else 'q',[-1,-2,-3])):
     if h in r and all(not b[i+x] for x in empty) and not hit(b,i+t//2,-c):yield i,i+t,0
def play(b,c,r,e,m):
 i,j,q=m;p=b[i];a=b[:];a[i]=0;a[j]=q*c if q else p
 if abs(p)==1 and j==e:a[j-16*c]=0
 if abs(p)==6 and abs(j-i)==2:
  x=i+3 if j>i else i-4;a[(i+j)//2]=a[x];a[x]=0
 for x,h in ((0,'Q'),(7,'K'),(112,'q'),(119,'k')):
  if x in (i,j):r=r.replace(h,'')
 if abs(p)==6:
  for h in ('KQ' if c==1 else 'kq'):r=r.replace(h,'')
 return a,-c,r,(i+j)//2 if abs(p)==1 and abs(j-i)==32 else -1
def ev(b,c):
 v=0;bish=[0,0];end=sum(abs(p) in (4,5) for p in b)<3
 for i in S:
  p=b[i]
  if not p:continue
  s=1 if p>0 else -1;p=abs(p);x=i%16;y=i//16 if s==1 else 7-i//16;z=7-abs(2*x-7)-abs(2*y-7)
  t=V[p]+([0,y*9-abs(2*x-7)*2,z*7,z*4,y*2,z*2,z*6 if end else -y*12-abs(2*x-7)*2][p])
  v+=s*t
  if p==3:bish[s==1]+=1
 return c*(v+30*((bish[1]>1)-(bish[0]>1)))
def search(b,c,r,e,d,alpha,beta,ply):
 global N
 N+=1
 if N>30000:raise RuntimeError
 key=(tuple(b),c,r,e);old=tt.get(key);a0=alpha;best=None
 if key in path:return 0
 if old and old[0]>=d and (old[2]==0 or old[2]==1 and old[1]>=beta or old[2]==-1 and old[1]<=alpha):return old[1]
 C=hit(b,b.index(6*c),-c)
 if ply>40:return ev(b,c)
 val=-30000
 if d<=0 and not C:
  val=ev(b,c)
  if val>=beta:return val
  alpha=max(alpha,val)
 order=old[3] if old else None
 ms=list(moves(b,c,r,e))
 ms.sort(key=lambda m:100000*(m==order)+10*V[abs(b[m[1]])]-V[abs(b[m[0]])]+V[m[2]],reverse=True)
 n=0;path.add(key)
 try:
  for m in ms:
   if d<=0 and not C and not (b[m[1]] or m[2] or abs(b[m[0]])==1 and m[1]==e):continue
   a,s,t,f=play(b,c,r,e,m)
   if hit(a,a.index(6*c),-c):continue
   n+=1
   score=-search(a,s,t,f,d-1,-beta,-alpha,ply+1)
   if score>val:val=score;best=m
   alpha=max(alpha,val)
   if alpha>=beta:break
 finally:path.remove(key)
 if not n and (d>0 or C):val=-29000+ply if C else 0
 if d>0:tt[key]=(d,val,1 if val>=beta else -1 if val<=a0 else 0,best)
 return val
def uci(m):
 i,j,q=m
 return ''.join(chr(97+x%16)+str(1+x//16) for x in (i,j))+(' pnbrqk'[q] if q else '')
def choose(fen,legal):
 global tt,path,N
 F=fen.split();b=[0]*128
 for y,row in enumerate(F[0].split('/')):
  x=0
  for p in row:
   if p.isdigit():x+=int(p)
   else:b[(7-y)*16+x]=(1 if p.isupper() else -1)*' pnbrqk'.index(p.lower());x+=1
 c=1 if F[1]=='w' else -1;r=F[2];ep=F[3];e=-1 if ep=='-' else ord(ep[0])-97+16*(int(ep[1])-1)
 tt={};path=set();N=0;ans=sorted(legal)[0];key=(tuple(b),c,r,e)
 for d in range(1,64):
  try:search(b,c,r,e,d,-30000,30000,0)
  except RuntimeError:break
  m=tt[key][3]
  if m and uci(m) in legal:ans=uci(m)
 return ans
def post(p,b):
 return json.load(urllib.request.urlopen(urllib.request.Request(os.environ['MAKEFUN_ENV_URL']+p,json.dumps(b).encode(),{'Content-type':'application/json'})))
while True:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
