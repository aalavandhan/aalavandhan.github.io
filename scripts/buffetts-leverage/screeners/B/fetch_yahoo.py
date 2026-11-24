"""Fetch weekly (or daily) Yahoo chart bars with dividend events. Usage:
   python3 -I fetch_yahoo.py <tickers.txt> <outdir> <1wk|1d>
Writes one compact JSON per ticker: {"t":[unix],"c":[split-adj close],"a":[div-adj close],"v":[volume],"d":{unix:dividend}}.
Generic User-Agent, 3 workers with a pause, well under 5 requests a second."""
import json,urllib.request,time,datetime,sys,os
from concurrent.futures import ThreadPoolExecutor
P1=int(datetime.datetime(1962,1,1,tzinfo=datetime.timezone.utc).timestamp())
P2=int(datetime.datetime(2026,11,1,tzinfo=datetime.timezone.utc).timestamp())
tick=open(sys.argv[1]).read().split(); out=sys.argv[2]; iv=sys.argv[3]
os.makedirs(out,exist_ok=True)
def r6(x): return None if x is None else float(f"{x:.6g}")
def get(t):
    fn=os.path.join(out,t.replace('^','_')+'.json')
    if os.path.exists(fn): return t,'cached'
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1={P1}&period2={P2}&interval={iv}&events=div"
    err=None
    for a in range(4):
        try:
            time.sleep(0.6)
            r=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=60).read())['chart']['result'][0]
            ts=r.get('timestamp') or []
            q=r['indicators']['quote'][0] if ts else {}
            adj=r['indicators']['adjclose'][0]['adjclose'] if ts else []
            div={k:r6(v['amount']) for k,v in (r.get('events',{}).get('dividends',{}) or {}).items()}
            json.dump({"t":ts,"c":[r6(x) for x in q.get('close',[])],"a":[r6(x) for x in adj],"v":q.get('volume',[]),"d":div},open(fn,'w'),separators=(',',':'))
            return t,'ok'
        except Exception as e:
            err=str(e); time.sleep(3*(a+1))
    return t,'ERR '+str(err)
n=0;bad=[]
with ThreadPoolExecutor(3) as ex:
    for t,s in ex.map(get,tick):
        n+=1
        if s.startswith('ERR'): bad.append((t,s))
        if n%200==0: print(n,len(bad),flush=True)
print('done',n,'errors',bad)
