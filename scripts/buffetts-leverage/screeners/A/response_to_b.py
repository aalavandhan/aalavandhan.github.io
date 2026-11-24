"""Post hoc checks prompted by B/REVIEW-OF-A.md. Not pre-registered. Run: python -I response_to_b.py <A-folder>"""
import sys, os, re, json, datetime, numpy as np, pandas as pd
A = sys.argv[1]; FR = os.path.join(A, 'data', 'french')
m = pd.read_csv(os.path.join(A, 'out', 'monthly_unlevered.csv'), index_col=0)
la = pd.read_csv(os.path.join(A, 'out', 'berkshire_annual_letter.csv'), index_col=0).iloc[:, 0]
rf = m['rf']
def blk(name, title):
    rows = open(os.path.join(FR, name + '.csv'), encoding='latin-1').read().splitlines()
    i = next(i for i, l in enumerate(rows) if title in l)
    hdr = [c.strip() for c in rows[i + 1].split(',')][1:]; out = {}
    for l in rows[i + 2:]:
        p = [c.strip() for c in l.split(',')]
        if len(p[0]) == 6 and p[0].isdigit(): out[int(p[0])] = [float(x) for x in p[1:1 + len(hdr)]]
        elif out: break
    return pd.DataFrame(out, index=hdr).T
head = lambda r, L=1.6: L * (r - 0.005 / 12) - (L - 1) * (rf.loc[r.index] + 0.01 / 12)
cagr = lambda r: (1 + r).prod() ** (12 / len(r)) - 1
bw = (1 + la.loc[1976:2025]).prod()
print('1. A13 with different cell weights (1.6x, T-bill + 1%, 0.5% haircut, 1976-2025)')
cells = ['BM4 OP4', 'BM4 OP5', 'BM5 OP4', 'HiBM HiOP']
ret = blk('25_Portfolios_BEME_OP_5x5', 'Average Value Weighted Returns -- Monthly')[cells] / 100
nf = blk('25_Portfolios_BEME_OP_5x5', 'Number of Firms in Portfolios')[cells]
sz = blk('25_Portfolios_BEME_OP_5x5', 'Average Market Cap')[cells]
mv = (nf * sz)
for nm, wts in [('equal across cells (pre-registered)', None), ('by number of firms', nf), ('by cell market value', mv)]:
    if wts is None: r = ret.mean(axis=1)
    else:
        w = wts.shift(1).reindex(ret.index); w = w.div(w.sum(axis=1), axis=0); r = (ret * w).sum(axis=1)
    r = r.loc[197601:202512]; l = head(r)
    print(f'   {nm:38s} unlevered {cagr(r)*100:.1f}%  levered {cagr(l)*100:.1f}%  $1 -> {(1+l).prod():,.0f}  share of Berkshire {(1+l).prod()/bw:.2f}')
share = mv.div(mv.sum(axis=1), axis=0).loc[197601:202512]
print('   median share of the four cells\' market value:', share.median().round(3).to_dict())

print('2. Never-sell account: borrow back up to 1.6x each December, never sell unless called; 30% rule, month-end checks; headline costs')
def ratchet(r, L, maint):
    rb = (rf.loc[r.index] + 0.01 / 12).values; ra = (r - 0.005 / 12).values; idx = list(r.index)
    Aa = L; D = L - 1.0; lo = 1; lod = None; calls = []; wiped = None
    for i in range(len(ra)):
        Aa *= 1 + ra[i]; D *= 1 + rb[i]; E = Aa - D
        if E <= 0: wiped = idx[i]; E = 0; break
        if E / Aa < lo: lo = E / Aa; lod = idx[i]
        if maint and E / Aa < maint: calls.append(idx[i]); Aa = E; D = 0.0     # sold down to 1.0x
        if idx[i] % 100 == 12 and Aa / E < L: Aa = L * E; D = (L - 1) * E
    return E, lo, lod, calls, wiped
m['A3+A1+A5'] = m['A11']
for k in ['A11', 'A10', 'A2', 'A1', 'A3', 'A13', 'market']:
    E0, lo, lod, _, wiped = ratchet(m[k], 1.6, None)
    E1, _, _, calls, _ = ratchet(m[k], 1.6, 0.30)
    const = (1 + head(m[k])).prod()
    print(f'   {k:7s} lowest equity/assets {lo:.2f} in {lod}; no rule: $1 -> {E0:,.0f} (wiped {wiped}); 30% rule: calls {calls}, $1 -> {E1:,.0f}; monthly-reset account $1 -> {const:,.0f}')

print('3. Split at 1998/1999 (1.6x, T-bill + 1%, 0.5% haircut; market without haircut)')
b1 = (1 + la.loc[1976:1998]).prod() ** (1 / 23) - 1; b2 = (1 + la.loc[1999:2025]).prod() ** (1 / 27) - 1
print(f'   Berkshire {b1*100:.1f}% / {b2*100:.1f}%')
rows = []
for k in ['market'] + ['A%d' % i for i in range(1, 14)]:
    l = head(m[k]) if k != 'market' else 1.6 * m[k] - 0.6 * (rf + 0.01 / 12)
    c1, c2 = cagr(l.loc[197601:199812]), cagr(l.loc[199901:202512]); u1, u2 = cagr(m[k].loc[197601:199812]), cagr(m[k].loc[199901:202512])
    rows.append((k, u1, u2, c1, c2))
    print(f'   {k:7s} unlevered {u1*100:5.1f}% / {u2*100:5.1f}%   1.6x {c1*100:5.1f}% / {c2*100:5.1f}%   gap {100*(c1-b1):+5.1f} / {100*(c2-b2):+5.1f}')
x = pd.DataFrame(rows[1:], columns=['k', 'u1', 'u2', 'c1', 'c2'])
print(f'   thirteen screens at 1.6x: 1976-1998 min {x.c1.min()*100:.1f}% median {x.c1.median()*100:.1f}% max {x.c1.max()*100:.1f}%; 1999-2025 min {x.c2.min()*100:.1f}% median {x.c2.median()*100:.1f}% max {x.c2.max()*100:.1f}%; beating Berkshire in 1999-2025: {(x.c2 > b2).sum()} of 13')

print('4. Berkshire worst falls on daily closes')
r = json.load(open(os.path.join(A, 'data', 'brk', 'brk_daily.json')))['chart']['result'][0]
s = pd.Series(r['indicators']['quote'][0]['close'], index=pd.to_datetime(r['timestamp'], unit='s')).dropna(); s = s[:'2025-12-31']
dd = s / s.cummax() - 1
print(f'   deepest {dd.min()*100:.1f}% on {dd.idxmin().date()}; 1987: {dd["1987":"1988"].min()*100:.1f}%; 1998-2000: {dd["1998":"2000"].min()*100:.1f}%')
