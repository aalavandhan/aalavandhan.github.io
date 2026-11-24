import csv,json,datetime,collections
D=collections.defaultdict(lambda: collections.defaultdict(float)); seen=set()
for r in csv.DictReader(open('debt.csv')):
    y=int(r['year']); it=r['item']; seg=r['segment_label']
    if not r['value_usd_m'] or 'PRO FORMA' in seg: continue
    try: v=float(r['value_usd_m'])
    except: continue
    if (y,it,seg) in seen: continue
    seen.add((y,it,seg)); D[it][y]+=v
X={int(r['year']):r for r in csv.DictReader(open('xbrl.csv'))}
F={int(r['year']):r for r in csv.DictReader(open('float.csv'))}
tb=collections.defaultdict(list)
for r in csv.reader(open('tb3ms.csv')):
    if r[0][:4].isdigit() and r[1] not in('','.'): tb[int(r[0][:4])].append(float(r[1]))
tb={y:sum(v)/len(v) for y,v in tb.items()}
r=json.load(open('../ff/brk_all.json'))['chart']['result'][0]; px={}
for t,c in zip(r['timestamp'],r['indicators']['quote'][0]['close']):
    d=datetime.datetime.fromtimestamp(t,datetime.timezone.utc)+datetime.timedelta(days=2)
    if d.month==12 and c: px[d.year]=c
def fl(y):
    r=F[y]; v=r['yearend_float_usd_m'].replace('~','').replace(',','')
    return float(v) if v else None
T={}
for y in range(1995,2026):
    A=D['total_assets'].get(y) or float(X[y]['assets'])/1e6
    E=D['total_shareholders_equity'].get(y) or float(X[y]['equity'])/1e6
    cash=D['cash_and_cash_equivalents'].get(y)
    if 2008<=y<=2016: cash=float(X[y]['cash_tag'])/1e6
    tbills=D['short_term_investments_us_treasury_bills'].get(y,0)
    mc=D['class_a_equivalent_shares'][y]*px[y]/1e6
    debt=D['notes_payable_and_other_borrowings'].get(y); ie=D['interest_expense'].get(y)
    dt=D['income_taxes_principally_deferred'].get(y)
    T[y]=dict(A=A,E=E,cash=cash,tbills=tbills,mc=mc,debt=debt,ie=ie,dt=dt,fl=fl(y),uw=float(F[y]['underwriting_result_usd_m']),tb=tb[y])
out=[]
print("year  assets equity  cash+bills  mcap  P/B | lev_book lev_mv(paper) | debt float deftax | int% float% blended% tbill | (D+F+T)/liab")
for y in range(1995,2026):
    t=T[y]; c=t['cash']+t['tbills']
    lb=(t['A']-c)/t['E']; lm=(t['A']+t['mc']-t['E']-c)/t['mc']
    row=dict(year=y,lev_book=lb,lev_mv=lm,**t)
    if y>1995 and T[y-1]['debt'] and t['debt']:
        p=T[y-1]; ad=(t['debt']+p['debt'])/2; af=(t['fl']+p['fl'])/2 if t['fl'] and p['fl'] else float(F[y]['average_float_usd_m']); at=(t['dt']+p['dt'])/2 if t['dt'] and p['dt'] else None
        row['int_pct']=t['ie']/ad*100; row['float_pct']=-t['uw']/af*100
        if at: row['blend_pct']=(t['ie']-t['uw'])/(ad+af+at)*100; row['blend_df']=(t['ie']-t['uw'])/(ad+af)*100
        row['share']=(t['debt']+(t['fl'] or af)+(t['dt'] or 0))/(t['A']-t['E'])
    out.append(row)
    g=lambda k,f="{:6.2f}": f.format(row[k]) if row.get(k) is not None else "    NA"
    print(y, f"{t['A']/1e3:7.1f} {t['E']/1e3:6.1f} {c/1e3:7.1f} {t['mc']/1e3:7.1f} {t['mc']/t['E']:5.2f} | {lb:5.2f} {lm:5.2f} | {(t['debt'] or 0)/1e3:6.1f} {(t['fl'] or 0)/1e3:6.1f} {(t['dt'] or 0)/1e3:6.1f} | {g('int_pct')} {g('float_pct')} {g('blend_pct')} {t['tb']:5.2f} | {g('share')}")
keys=sorted({k for r in out for k in r}); w=csv.DictWriter(open('leverage_cost.csv','w'),fieldnames=['year']+[k for k in keys if k!='year']); w.writeheader(); w.writerows(out)
def avg(k,a,b):
    v=[r[k] for r in out if a<=r['year']<=b and r.get(k) is not None]; return sum(v)/len(v),len(v)
for a,b in [(1996,2011),(2012,2025),(1996,2025)]:
    print(a,b,{k:round(avg(k,a,b)[0],2) for k in ['lev_book','lev_mv','int_pct','float_pct','blend_pct','blend_df','tb','share']})
    rs=[r for r in out if a<=r['year']<=b and r.get('blend_pct') is not None]
    print('   years blended<tbill:',sum(1 for r in rs if r['blend_pct']<r['tb']),'of',len(rs))
