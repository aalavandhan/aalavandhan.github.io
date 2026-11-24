"""Margin-account simulation. Run after analyze.py: python3 -I margin.py
Weekly closes for the stock screens; daily closes for Berkshire, funds and Ken French daily portfolios. Writes out/margin.txt."""
import sys, os, csv, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
D = datetime.date
out = open(os.path.join(OUT, 'margin.txt'), 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
SPREAD = 0.01
WIN = [('1987', D(1987, 8, 1), D(1987, 12, 31)), ('1998-2002', D(1998, 4, 1), D(2002, 12, 31)), ('2007-09', D(2007, 6, 1), D(2009, 6, 30)), ('2020', D(2020, 1, 15), D(2020, 4, 30))]

series = {}   # name -> (dates, returns dict, rf dict, periods per year, label of frequency)
# weekly
rows = list(csv.DictReader(open(os.path.join(OUT, 'series_weekly.csv'))))
for k in rows[0]:
    if k in ('week_monday', 'rf_weekly'): continue
    if not (k.endswith('_net') or k.endswith('_adj') or k in ('C1_gross', 'BRK-A', 'VFINX')): continue
    ds = []; r = {}; rf = {}
    for x in rows:
        if x[k] == '' or x['rf_weekly'] == '': continue
        d = friday(D.fromisoformat(x['week_monday']))
        if d > D(2025, 12, 31): continue
        ds.append(d); r[d] = float(x[k]); rf[d] = float(x['rf_weekly'])
    series[k + ' [weekly]'] = (ds, r, rf, 52)
# daily
ffd = french_daily()
def dkey(d): return d.year * 10000 + d.month * 100 + d.day
for t in ['BRK-A', 'VFINX', 'VIVAX', 'VIG', 'SPLV', 'USMV', 'QUAL']:
    b = load_bars(t, 'daily')
    pts = [(datetime.datetime.fromtimestamp(ts, UTC).date(), a) for ts, a in zip(b['t'], b['a']) if a]
    ds = []; r = {}; rf = {}
    for (d0, a0), (d1, a1) in zip(pts, pts[1:]):
        if d1 > D(2025, 12, 31) or dkey(d1) not in ffd: continue
        ds.append(d1); r[d1] = a1 / a0 - 1; rf[d1] = ffd[dkey(d1)]['RF']
    series[t + ' [daily]'] = (ds, r, rf, 252)
ds = [D(k // 10000, k // 100 % 100, k % 100) for k in sorted(ffd) if 19760101 <= k <= 20251231]
series['FF market [daily]'] = (ds, {d: ffd[dkey(d)]['Mkt-RF'] + ffd[dkey(d)]['RF'] for d in ds}, {d: ffd[dkey(d)]['RF'] for d in ds}, 252)
A_FR = os.path.join(HERE, '..', 'A', 'data', 'french')
for fn, col, nm in [('Portfolios_Formed_on_BE-ME_Daily.csv', 'Hi 20', 'FF cheap quintile (BE/ME Hi 20)'), ('Portfolios_Formed_on_OP_Daily.csv', 'Hi 20', 'FF profitable quintile (OP Hi 20)')]:
    try:
        blk = french_block(os.path.join(A_FR, fn), 'Value Weight Returns -- Daily')
        if not blk: blk = french_block(os.path.join(A_FR, fn), 'Value Weighted Returns -- Daily')
        ds2 = [d for d in ds if dkey(d) in blk and blk[dkey(d)][col] > -0.99]
        series[nm + ' [daily]'] = (ds2, {d: blk[dkey(d)][col] for d in ds2}, {d: ffd[dkey(d)]['RF'] for d in ds2}, 252)
    except Exception as ex:
        say('could not load', fn, ex)

def window_dd(ds, r, a, b):
    w = 1.0; pk = 1.0; dd = 0.0; t = None
    for d in ds:
        if d < a or d > b: continue
        w *= 1 + r[d]; pk = max(pk, w)
        if w / pk - 1 < dd: dd = w / pk - 1; t = d
    return dd, t

say('== A. Unlevered peak-to-trough fall inside each window, and the equity ratio a 1.6x / 2.0x account would show at the trough if it was exactly at target at the peak and did not sell.')
say('   Equity ratio = 1 - (1 - 1/L) / (1 + fall), ignoring interest. A call comes below 0.30 or 0.25. Falls that cause a call: 46.4% / 50.0% at 1.6x and 28.6% / 33.3% at 2.0x.')
say('%-36s' % 'series' + ''.join('%26s' % w[0] for w in WIN) + '%26s' % 'whole sample')
for nm, (ds, r, rf, ppy) in series.items():
    row = '%-36s' % nm
    for lab, a, b in WIN + [('all', D(1900, 1, 1), D(2100, 1, 1))]:
        if ds[0] > a and lab != 'all': row += '%26s' % 'no data'; continue
        dd, t = window_dd(ds, r, a, b)
        e16 = 1 - (1 - 1 / 1.6) / (1 + dd); e20 = 1 - 0.5 / (1 + dd)
        row += '%26s' % ('%.1f%% (%.2f / %.2f)' % (100 * dd, e16, e20))
    say(row)

say('\n== B. Full-sample margin account, financed at T-bill + 1%.')
say('   ratchet = borrow back up to target each year-end, never sell voluntarily. month = reset to target every month-end.')
say('   For each maintenance requirement: number of forced sales, final wealth of $1, and the worst fall in account equity.')
say('%-36s %4s %-7s | %-22s | %-30s | %-30s | %-30s' % ('series', 'L', 'policy', 'lowest equity ratio', 'no requirement: final, maxDD', '25%: calls, final, maxDD', '30%: calls, final, maxDD'))
CALLS = {}
for nm, (ds, r, rf, ppy) in series.items():
    for L in (1.6, 2.0):
        for pol in ('ratchet', 'month'):
            res = {m: margin_sim(ds, r, rf, SPREAD / ppy, L, m, pol) for m in (None, .25, .30)}
            n = res[None]
            fin = lambda x: ('wiped %s' % x['wiped']) if x['wiped'] else '%.1f' % x['final']
            say('%-36s %4.1f %-7s | %-22s | %-30s | %-30s | %-30s' % (nm, L, pol, '%.2f on %s' % (n['min_ratio'], n['min_date']),
                '%s, %.0f%%' % (fin(n), 100 * n['maxdd']),
                '%d, %s, %.0f%%' % (len(res[.25]['calls']), fin(res[.25]), 100 * res[.25]['maxdd']),
                '%d, %s, %.0f%%' % (len(res[.30]['calls']), fin(res[.30]), 100 * res[.30]['maxdd'])))
            CALLS[(nm, L, pol)] = res
say('\n== C. Dates of forced sales, ratchet policy (date: equity ratio at the breach, share of assets sold)')
for (nm, L, pol), res in CALLS.items():
    if pol != 'ratchet': continue
    for m in (.25, .30):
        c = res[m]['calls']
        if c: say('%-36s %.1fx maint %.0f%%: ' % (nm, L, 100 * m) + '; '.join('%s: %.2f, sold %.0f%%' % (d, q, 100 * s) for d, q, s in c[:12]) + (' ...' if len(c) > 12 else ''))

say('\n== D. Berkshire share price itself, daily closes: worst falls inside each window (the 2017 letter lists 59.1% in 1973-75, 37.1% in October 1987, 48.9% in 1998-2000 and 50.7% in 2008-09, using intraday highs and lows).')
ds, r, rf, ppy = series['BRK-A [daily]']
for lab, a, b in WIN + [('1998-06 to 2000-03', D(1998, 6, 1), D(2000, 3, 31)), ('all', D(1900, 1, 1), D(2100, 1, 1))]:
    dd, t = window_dd(ds, r, a, b); say('  %-20s %.1f%% (trough %s)' % (lab, 100 * dd, t))
