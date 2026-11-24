import json,urllib.request,time,datetime,sys
from concurrent.futures import ThreadPoolExecutor
P1=int(datetime.datetime(1975,12,1,tzinfo=datetime.timezone.utc).timestamp())
def get(t):
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1={P1}&period2=1795000000&interval=1wk"
    for a in range(4):
        try:
            r=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=40).read())['chart']['result'][0]
            ts=r.get('timestamp') or []; adj=r['indicators']['adjclose'][0]['adjclose'] if ts else []
            ye={}
            for x,v in zip(ts,adj):
                if v is None: continue
                d=datetime.datetime.fromtimestamp(x,datetime.timezone.utc)
                ye[d.year]=v            # last weekly obs of each year
            first=datetime.datetime.fromtimestamp(ts[0],datetime.timezone.utc).date().isoformat() if ts else None
            return t,{"first":first,"ftd":r['meta'].get('firstTradeDate'),"ye":ye}
        except Exception as e:
            err=str(e); time.sleep(2*(a+1))
    return t,{"err":err}
ticks=open('tickers.txt').read().split()
out={}
with ThreadPoolExecutor(4) as ex:
    for i,(t,v) in enumerate(ex.map(get,ticks),1):
        out[t]=v
        if i%250==0: print(i,sum(1 for x in out.values() if 'err' in x),flush=True)
json.dump(out,open('yearend.json','w'))
print('done',len(out),'errors',sum(1 for x in out.values() if 'err' in x),'since1975',sum(1 for x in out.values() if x.get('first') and x['first']<'1976-01-01'))
