import json,os,sys
from urllib.request import Request,urlopen
U=os.getenv("MAKEFUN_ENV_URL")or sys.exit("MAKEFUN_ENV_URL is not set")
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000}
D={'P':(-10,-20,-9,-11),'N':(-21,-19,-12,-8,8,12,19,21),'B':(-11,-9,9,11),'R':(-10,-1,1,10),'Q':(-11,-10,-9,-1,1,9,10,11),'K':(-11,-10,-9,-1,1,9,10,11)}
T='0000000001222221012333210123443211234432101233321012222100000000'
N=0;L=30000;X={};H={};K={}
def P(x,y):
 return json.load(urlopen(Request(U+x,json.dumps(y).encode(),headers={'content-type':'application/json'})))
def I(x):return 91+ord(x[0])-97-10*(ord(x[1])-49)
def F(f):
 z=f.split();a=''.join('.'*int(x)if x.isdigit()else x for x in z[0]if x!='/');b=' '*20+''.join(' '+a[i:i+8]+' 'for i in range(0,64,8))+' '*20
 w=('Q'in z[2],'K'in z[2]);c=('q'in z[2],'k'in z[2]);e=0 if z[3]=='-'else I(z[3])
 if z[1]=='b':b,w,c,e=b[::-1].swapcase(),(c[1],c[0]),w,119-e if e else 0
 return b,w,c,e
def R(p):
 b,w,c,e=p;return b[::-1].swapcase(),c,w,119-e if e else 0
def G(p):
 b,w,c,e=p
 for i,x in enumerate(b):
  if not x.isupper():continue
  for d in D[x]:
   j=i+d
   while b[j]!=' ':
    q=b[j]
    if q.isupper():break
    if x=='P':
     if d%10<1:
      if q!='.'or(d==-20 and(i<81 or b[i-10]!='.')):break
     elif q=='.'and j!=e:break
    yield i,j
    if x in'PNK'or q.islower():break
    j+=d
  if x=='K':
   if w[0]and b[91]=='R'and all(b[j]=='.'for j in range(92,i)):yield i,i-2
   if w[1]and b[98]=='R'and all(b[j]=='.'for j in range(i+1,98)):yield i,i+2
def M(p,m):
 b,w,c,e=p;i,j,*z=m;x=b[i];q=b[j];b=b[:j]+x+b[j+1:];b=b[:i]+'.'+b[i+1:];E=0
 if x=='P':
  if j<29:b=b[:j]+(z[0]if z else'Q')+b[j+1:]
  if j==e:b=b[:j+10]+'.'+b[j+11:]
  if i-j==20:E=i-10
 if x=='K':
  w=(0,0)
  if abs(i-j)==2:
   r=91 if j<i else 98;t=j+1 if j<i else j-1;b=b[:r]+'.'+b[r+1:];b=b[:t]+'R'+b[t+1:]
 if x=='R':w=(0,w[1])if i==91 else(w[0],0)if i==98 else w
 if q=='r':c=(0,c[1])if j==28 else(c[0],0)if j==21 else c
 return R((b,w,c,E))
def E(b):
 s=0
 for i,x in enumerate(b):
  if x.isalpha():
   j=i if x.isupper()else 119-i;y=V[x.lower()]+ord(T[(j//10-2)*8+j%10-1])-48
   if x.lower()=='p':y+=9-j//10
   s+=y if x.isupper()else-y
 return s
def O(b,m):return V.get(b[m[1]].lower(),0)*16-V[b[m[0]].lower()]+80*(m[1]<29)+H.get(m,0)
def S(p,a,b,d):
 global N
 N+=1;v=E(p[0])
 if'K'not in p[0]:return-30000
 if N>L or d<-4:return v
 t=X.get(p)
 if t and t[0]>=d:
  if t[2]==0:return t[1]
  if t[2]<0:b=min(b,t[1])
  else:a=max(a,t[1])
  if a>=b:return t[1]
 A=a
 if d<1:
  if v>=b:return v
  if v>a:a=v
 if d>2 and any(x in p[0]for x in'QRBN'):
  v=-S(R((p[0],p[1],p[2],0)),-b,-b+1,d-3)
  if v>=b:X[p]=d,v,1;return v
 for m in sorted(G(p),key=lambda m:O(p[0],m)+(K.get(d)==m)*10000,reverse=1):
  if d<1 and p[0][m[1]]=='.'and m[1]!=p[3]and not(p[0][m[0]]=='P'and m[1]<29):continue
  v=-S(M(p,m),-b,-a,d-1)
  if v>=b:
   X[p]=d,v,1
   if p[0][m[1]]=='.':H[m]=H.get(m,0)+d*d;K[d]=m
   return v
  if v>a:a=v
 X[p]=d,a,0 if a>A else-1
 return a
def C(f,l):
 global N,X,H,K
 N=0;X={};H={};K={};p=F(f);h=f.split()[1]=='b';u=[]
 for x in l:
  m=(I(x),I(x[2:]),x[4].upper()if len(x)>4 else'Q')
  if h:m=119-m[0],119-m[1],m[2]
  u+=[(m,x)]
 r=u[0]
 for d in range(1,10):
  q=r;a=-30001
  for m,x in sorted(u,key=lambda z:(O(p[0],z[0]),z[1]),reverse=1):
   v=-S(M(p,m),-30001,-a,d-1)
   if v>a or v==a and x<q[1]:a,q=v,(m,x)
  if N>L:break
  r=q
 return r[1]
while 1:
 g=P('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=P('/move',{'game':g['game'],'move':C(g['fen'],g['legal_moves'])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
