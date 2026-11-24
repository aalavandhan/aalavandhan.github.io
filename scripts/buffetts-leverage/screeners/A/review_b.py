"""Independent recomputation of builder B's headline numbers, with my own code (no import from B).
Run: python -I review_b.py <A-folder> <B-folder>"""
import sys, os, json, re, datetime, glob
import numpy as np, pandas as pd
A, B = sys.argv[1], sys.argv[2]
def french(path, title_re, n=6):
    rows = open(path, encoding='latin-1').read().splitlines()
    s = next(i for i, l in enumerate(rows) if l.startswith(',')) if title_re is None else next(i for i, l in enumerate(rows) if re.search(title_re, l)) + 1
    hdr = [c.strip() for c in rows[s].split(',')][1:]; idx = []; d = []
    for l in rows[s + 1:]:
        p = [c.strip() for c in l.split(',')]
        if len(p[0]) == n and p[0].isdigit(): idx.append(int(p[0])); d.append([float(x) for x in p[1:1 + len(hdr)]])
        elif idx: break
    return pd.DataFrame(d, index=idx, columns=hdr) / 100
FR = os.path.join(A, 'data', 'french')
ff = french(os.path.join(FR, 'F-F_Research_Data_Factors.csv'), None); rf = ff['RF']
la = pd.read_csv(os.path.join(A, 'out', 'berkshire_annual_letter.csv'), index_col=0).iloc[:, 0]

# 1. B's weekly screen returns -> months (by the Friday of each week) -> 1.6x at T-bill + 1%
w = pd.read_csv(os.path.join(B, 'out', 'screens_weekly.csv'))
fri = pd.to_datetime(w['week_monday']) + pd.Timedelta(days=4)
w['ym'] = fri.dt.year * 100 + fri.dt.month
print('1. B weekly series, compounded to months by me, then 1.6x at T-bill + 1% (monthly reset). Calendar 1976-2025.')
for c in ['B5_net', 'B5_gross', 'B1_net', 'B3_net', 'C1_gross']:
    m = (1 + w[c]).groupby(w['ym']).prod() - 1
    m = m[(m.index >= 197601) & (m.index <= 202512)]
    lev = 1.6 * m - 0.6 * (rf.reindex(m.index) + 0.01 / 12)
    wl = (1 + lev).cumprod()
    print(f'   {c:9s} unlevered CAGR {((1+m).prod()**(12/len(m))-1)*100:5.1f}%   1.6x CAGR {((1+lev).prod()**(12/len(m))-1)*100:5.1f}%   $1 -> {(1+lev).prod():8.0f}   max DD (month-end) {((wl/wl.cummax()).min()-1)*100:.0f}%')
print(f'   Berkshire letter CAGR {((1+la.loc[1976:2025]).prod()**(1/50)-1)*100:.1f}%')

# 2. survivorship gap: C1 (large half of survivors, equal weight) minus French equal-weighted top-30%-by-size
me = french(os.path.join(FR, 'Portfolios_Formed_on_ME.csv'), r'Equal Weight(ed)? Returns -- Monthly')
m1 = (1 + w['C1_gross']).groupby(w['ym']).prod() - 1; m1 = m1[(m1.index >= 197601) & (m1.index <= 202512)]
c1a = (1 + m1).groupby(m1.index // 100).prod() - 1
h = me['Hi 30'].loc[197601:202512]; ha = (1 + h).groupby(h.index // 100).prod() - 1
g = c1a - ha
print(f'2. C1 minus French EW Hi 30, mean annual gap {g.mean()*100:.2f}% (B reports 2.27%); 1976-1998 {g.loc[:1998].mean()*100:.2f}%, 1999-2025 {g.loc[1999:].mean()*100:.2f}%')
print(f'   CAGR C1 {((1+c1a).prod()**(1/50)-1)*100:.1f}%  French EW Hi30 {((1+ha).prod()**(1/50)-1)*100:.1f}%')

# 3. survivorship-free analogue of B5 (high yield): French highest dividend-yield quintile, value weighted
dp = french(os.path.join(FR, 'Portfolios_Formed_on_D-P.csv'), r'Value Weight(ed)? Returns -- Monthly')
print('3. French highest dividend-yield quintile (Hi 20, VW), 1976-2025, survivorship-free:')
for nm, col in [('D/P Hi 20', dp['Hi 20']), ('D/P Hi 10', dp['Hi 10'])]:
    r = col.loc[197601:202512]
    for hair in [0, 0.005]:
        lev = 1.6 * (r - hair / 12) - 0.6 * (rf.loc[r.index] + 0.01 / 12); wl = (1 + lev).cumprod()
        print(f'   {nm} haircut {hair*100:.1f}%: unlevered CAGR {((1+r).prod()**(1/50)-1)*100:.1f}%, 1.6x T-bill+1% CAGR {((1+lev).prod()**(1/50)-1)*100:.1f}%, $1 -> {(1+lev).prod():.0f}, max DD {((wl/wl.cummax()).min()-1)*100:.0f}%')

# 4. Re-derive B5's picks for three years from the raw weekly bars with my own code
hold = json.load(open(os.path.join(B, 'out', 'holdings.json')))['holdings']['B5']
bars = {}
for fn in glob.glob(os.path.join(B, 'data', 'yahoo_weekly', '*.json')):
    t = os.path.basename(fn)[:-5]
    if t.startswith('_'): continue
    try: b = json.load(open(fn))
    except Exception: continue
    d = pd.DataFrame({'t': b['t'], 'a': b['a'], 'c': b['c'], 'v': b['v']})
    d['date'] = pd.to_datetime(d['t'], unit='s', utc=True).dt.tz_localize(None).dt.normalize()
    d['mon'] = d['date'] - pd.to_timedelta(d['date'].dt.weekday, unit='D')
    d = d.dropna(subset=['a', 'c']).query('a > 0 and c > 0').drop_duplicates('mon', keep='last').set_index('mon')
    dv = pd.Series({pd.Timestamp(int(k), unit='s').normalize(): float(x) for k, x in (b.get('d') or {}).items() if x})
    bars[t] = (d, dv)
print('4. B5 picks re-derived from raw bars (top 100 by 52-week dollar volume among stocks with 3 years of history, then 30 highest trailing yield):')
for Y in [1977, 1990, 2008, 2020]:
    cut = pd.Timestamp(Y - 1, 12, 31); rows = []
    for t, (d, dv) in bars.items():
        x = d[d.index + pd.Timedelta(days=4) <= cut]
        if len(x) < 157: continue
        last = x.index[-1]
        if (cut - last).days > 10: continue
        if (last - x.index[-157]).days > 7 * 163: continue  # about 156 weeks with few gaps
        y = x.iloc[-52:]
        dol = (y['c'] * y['v'].fillna(0)).sum()
        asof = last + pd.Timedelta(days=4)
        ttm = dv[(dv.index > asof - pd.Timedelta(days=365)) & (dv.index <= asof)].sum() if len(dv) else 0.0
        rows.append((t, dol, ttm / x['c'].iloc[-1]))
    df = pd.DataFrame(rows, columns=['t', 'dol', 'dy']).sort_values('dol', ascending=False)
    mine = set(df.head(100).sort_values('dy', ascending=False).head(30)['t'])
    theirs = set(hold[str(Y)])
    print(f'   {Y}: eligible {len(df)}, my 30 vs B\'s {len(theirs)}: overlap {len(mine & theirs)}; stocks with zero trailing dividend in top 100: {(df.head(100).dy <= 0).sum()}; lowest yield among my 30: {df.head(100).sort_values("dy", ascending=False).head(30).dy.min()*100:.1f}%')
