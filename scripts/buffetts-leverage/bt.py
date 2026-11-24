import csv,json,datetime,math,sys
FF=sys.argv[1]; BRK=sys.argv[2]
def block(path,title):
    rows=open(path).read().splitlines(); out={}; hdr=None; on=False
    for i,l in enumerate(rows):
        if title is None and hdr is None and l.startswith(',') : hdr=[c.strip() for c in l.split(',')][1:]; on=True; continue
        if title and l.strip()==title: hdr=[c.strip() for c in rows[i+1].split(',')][1:]; on='skip'; continue
        if on=='skip': on=True; continue
        if on:
            p=[c.strip() for c in l.split(',')]
            if len(p[0])==6 and p[0].isdigit(): out[int(p[0])]=dict(zip(hdr,[float(x)/100 for x in p[1:]]))
            elif out: break
    return out
f=block(FF+'/F-F_Research_Data_Factors.csv',None)
p32=block(FF+'/32_Portfolios_ME_BEME_OP_2x4x4.csv','Average Value Weighted Returns -- Monthly')
pb=block(FF+'/Portfolios_Formed_on_BETA.csv','Value Weighted Returns -- Monthly')
r=json.load(open(BRK))['chart']['result'][0]
px={}
for t,c in zip(r['timestamp'],r['indicators']['quote'][0]['close']):
    d=datetime.datetime.fromtimestamp(t,datetime.timezone.utc)+datetime.timedelta(days=2)
    if c: px[d.year*100+d.month]=c   # close of that month
months=sorted(m for m in f if m in p32 and m in pb)
def prev(m): return m-1 if m%100>1 else (m//100-1)*100+12
brk={m:px[m]/px[prev(m)]-1 for m in months if m in px and prev(m) in px}
cq=['ME2 BM3 OP3','ME2 BM3 OP4','ME2 BM4 OP3','BIG HiBM HiOP']
S={}
S['Berkshire']=brk
S['Market']={m:f[m]['Mkt-RF']+f[m]['RF'] for m in months}
S['Big cheap profitable']={m:sum(p32[m][c] for c in cq)/4 for m in months}
S['Low beta (Lo 20)']={m:pb[m]['Lo 20'] for m in months}
S['Blend 50/50']={m:(S['Big cheap profitable'][m]+S['Low beta (Lo 20)'][m])/2 for m in months}
def lev(base,L,spread): return {m:L*base[m]-(L-1)*(f[m]['RF']+spread/12) for m in base}
for b in ['Market','Big cheap profitable','Blend 50/50']:
    S[b+' 1.6x @Tbill']=lev(S[b],1.6,0)
    S[b+' 1.6x @Tbill+1']=lev(S[b],1.6,0.01)
    S[b+' 1.6x @Tbill-3']=lev(S[b],1.6,-0.03)
def stats(s,a,b):
    ms=[m for m in sorted(s) if a<=m<=b]
    ex=[s[m]-f[m]['RF'] for m in ms]; n=len(ex)
    mu=sum(ex)/n*12; sd=(sum((x-sum(ex)/n)**2 for x in ex)/(n-1))**.5*12**.5
    w=1;pk=1;dd=0
    for m in ms:
        w*=1+s[m]; pk=max(pk,w); dd=min(dd,w/pk-1)
    mk=[S['Market'][m]-f[m]['RF'] for m in ms]; mm=sum(mk)/n
    beta=sum((x-sum(ex)/n)*(y-mm) for x,y in zip(ex,mk))/sum((y-mm)**2 for y in mk)
    return mu,sd,mu/sd,beta,w**(12/n)-1,w,dd,ms[0],ms[-1]
for a,b in [(198502,201112),(198502,202609),(201201,202609)]:
    print(f"\n{a}-{b}   excess  vol  sharpe  beta  cagr   $1->   maxDD")
    for k,s in S.items():
        mu,sd,sh,be,cg,w,dd,m0,m1=stats(s,a,b)
        print(f"{k:36s} {mu*100:6.1f} {sd*100:5.1f} {sh:5.2f} {be:5.2f} {cg*100:6.1f} {w:8.1f} {dd*100:6.1f}")
json.dump({k:{str(m):v for m,v in s.items()} for k,s in S.items()},open('bt_series.json','w'))
