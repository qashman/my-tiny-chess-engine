P={1:5,8:12}
def apply_move(b,m):
 b=b[:];a=(ord(m[1])-49)*8+(ord(m[0])-97);z=(ord(m[3])-49)*8+(ord(m[2])-97);p=b[a];b[a]=0;r=P.get(p)
 if r is not None and(z>=56 if p==1 else z<=7):b[z]=r
 else:b[z]=p
 return b
def agent(o,c):
 ms=o.legal_moves
 if not ms:return None
 v={1:10,2:30,3:30,4:50,5:90,6:0,8:-10,9:-30,10:-30,11:-50,12:-90,13:0}
 p=[0,0,0,0,0,0,0,0,5,10,10,-20,-20,10,10,5,5,-5,-10,0,0,-10,-5,5,0,0,0,20,20,0,0,0,5,5,10,25,25,10,5,5,10,10,20,30,30,20,10,10,50,50,50,50,50,50,50,50,0,0,0,0,0,0,0,0]
 def e(b):
  s=0
  for i,q in enumerate(b):
   if q in v:
    s+=v[q]
    if q in(2,9):j=i if q==2 else 63-i;s+=5 if p[j]>0 else 0
  return s if o.mark==1 else -s
 bm=ms[0];bs=-999999
 def cv(m):
  z=(ord(m[3])-49)*8+(ord(m[2])-97);return v.get(o.board[z],0)
 for m in sorted(ms,key=cv,reverse=True):
  s=e(apply_move(o.board,m))
  if s>bs:bs=s;bm=m
 return bm
