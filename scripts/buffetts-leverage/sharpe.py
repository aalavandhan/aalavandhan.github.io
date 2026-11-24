import json,re,statistics as st
L=open('../brk/dl/2025.txt').read().splitlines()
brk={};sp={}
for l in L:
    m=re.match(r'^\s*(19[6-9]\d|20[0-2]\d)\s[ .]+\s+(\(?[\d.]+\)?)%?\s+(\(?[\d.]+\)?)%?\s*$',l)
    if m:
        f=lambda x: (-1 if x.startswith('(') else 1)*float(x.strip('()'))/100
        brk[int(m.group(1))]=f(m.group(2)); sp[int(m.group(1))]=f(m.group(3))
rf={}
on=False
for l in open('../ff/F-F_Research_Data_Factors.csv'):
    if 'Annual Factors' in l: on=True; continue
    p=[x.strip() for x in l.split(',')]
    if on and len(p)==5 and p[0].isdigit(): rf[int(p[0])]=float(p[4])/100
Y=json.load(open('yearend.json'))
def sharpe(ret,a,b):
    ex=[ret[y]-rf[y] for y in range(a,b+1)]
    return st.mean(ex)/st.stdev(ex), st.mean(ex), st.stdev(ex)
res={}
for a,b in [(1976,2025),(1981,2025),(1976,2011)]:
    print(f"\n== {a}-{b}  Berkshire SR %.2f (excess %.1f%%, vol %.1f%%) | S&P500 SR %.2f (%.1f%%, %.1f%%)"%(sharpe(brk,a,b)[0],sharpe(brk,a,b)[1]*100,sharpe(brk,a,b)[2]*100,sharpe(sp,a,b)[0],sharpe(sp,a,b)[1]*100,sharpe(sp,a,b)[2]*100))
    S={}
    for t,v in Y.items():
        ye={int(k):x for k,x in v.get('ye',{}).items()}
        if t in('BRK-B','BRK-A'): continue
        if all(y in ye for y in range(a-1,b+1)):
            S[t]=sharpe({y:ye[y]/ye[y-1]-1 for y in range(a,b+1)},a,b)[0]
    v=sorted(S.values()); n=len(v); bs=sharpe(brk,a,b)[0]
    q=lambda p: v[min(n-1,int(p*n))]
    print(f"   N={n} median {q(.5):.2f} p95 {q(.95):.2f} p99 {q(.99):.2f} max {v[-1]:.2f}; Berkshire rank {1+sum(1 for x in v if x>bs)} of {n+1}")
    print('   top:',[(t,round(s,2)) for t,s in sorted(S.items(),key=lambda x:-x[1])[:8]])
    res[f"{a}-{b}"]={"berkshire":bs,"sp500":sharpe(sp,a,b)[0],"stocks":S}
json.dump(res,open('sharpes.json','w'))
print(len(brk),brk[1976],brk[2025],sp[2025])
