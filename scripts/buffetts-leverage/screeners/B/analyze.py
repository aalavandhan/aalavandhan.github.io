"""Tables for builder B. Run after build_screens.py: python3 -I analyze.py <path to letter 2025 text>
Writes out/results.txt and out/series_weekly.csv (every series used, weekly, for agent A to reuse)."""
import sys, os, csv, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

LETTER = sys.argv[1]
A_FR = os.path.join(HERE, '..', 'A', 'data', 'french')
D = datetime.date
out = open(os.path.join(OUT, 'results.txt'), 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
pc = lambda x, w=6: ('%*.1f' % (w, x * 100)) if x is not None else ' ' * (w - 2) + 'na'

ffm, ffa = french_factors()
mkt_m = {k: v['Mkt-RF'] for k, v in ffm.items()}
letter = brk_letter(LETTER)

# ---- load screens
S = {}
rows = list(csv.DictReader(open(os.path.join(OUT, 'screens_weekly.csv'))))
weeks = [D.fromisoformat(r['week_monday']) for r in rows]
for k in rows[0]:
    if k == 'week_monday': continue
    S[k] = {D.fromisoformat(r['week_monday']): float(r[k]) for r in rows if r[k] != ''}
rf = weekly_rf(weeks, ffm)
SCR = ['B1', 'B2', 'B3', 'B4', 'B5']
NAMES = {'C0': 'Survivor universe EW (control)', 'C1': 'Large half of survivors EW (control)', 'B1': 'Low volatility 50', 'B2': 'Low beta 50',
         'B3': 'High yield, low volatility', 'B4': 'Dividend growers', 'B5': 'High yield 30'}

# ---- funds and Berkshire, weekly
FUNDS = ['BRK-A', 'VFINX', 'VIVAX', 'VIG', 'SPLV', 'USMV', 'QUAL', 'VEIPX', 'VDIGX', 'SDY', 'RSP']
for t in FUNDS:
    p = weekly_series(t); ks = sorted(p); r = {}
    for a, b in zip(ks, ks[1:]):
        if (b - a).days <= 21: r[b] = p[b] / p[a] - 1
    S[t] = {w: r[w] for w in weeks if w in r}

def annual(r):
    o = {}; n = {}
    for w in weeks:
        if w in r:
            y = friday(w).year; o[y] = (1 + o.get(y, 0)) * (1 + r[w]) - 1; n[y] = n.get(y, 0) + 1
    return {y: v for y, v in o.items() if n[y] >= 50}

# ---- survivorship
me = os.path.join(DATA, 'french', 'Portfolios_Formed_on_ME.csv')
ew_a = french_block(me, 'Equal Weight Returns -- Annual from January to December', annual=True)
vw_a = french_block(me, 'Value Weight Returns -- Annual from January to December', annual=True)
AN = {k: annual(S[k]) for k in S}
mkt_a = {y: ffa[y]['Mkt-RF'] + ffa[y]['RF'] for y in ffa}
def cagr(d, y0, y1):
    w = 1.0
    for y in range(y0, y1 + 1):
        if y not in d: return None
        w *= 1 + d[y]
    return w ** (1 / (y1 - y0 + 1)) - 1
say('== 1. Survivorship: equal-weight survivor controls against survivorship-free benchmarks (compound annual return, %)')
say('%-12s %8s %8s %8s %8s %8s %8s' % ('years', 'C0', 'C1', 'FF VW', 'FF EWHi30', 'FF EWMed40', 'S&P(letter)'))
for y0, y1 in [(1976, 2025), (1976, 1985), (1986, 1995), (1996, 2005), (2006, 2015), (2016, 2025), (1976, 1998), (1999, 2025)]:
    say('%d-%d    %8s %8s %8s %8s %8s %8s' % (y0, y1, pc(cagr(AN['C0_gross'], y0, y1)), pc(cagr(AN['C1_gross'], y0, y1)), pc(cagr(mkt_a, y0, y1)),
        pc(cagr({y: v['Hi 30'] for y, v in ew_a.items()}, y0, y1)), pc(cagr({y: v['Med 40'] for y, v in ew_a.items()}, y0, y1)),
        pc(cagr({y: v[1] for y, v in letter.items()}, y0, y1))))
gapC1 = {y: AN['C1_gross'][y] - ew_a[y]['Hi 30'] for y in AN['C1_gross']}
gapC0 = {y: AN['C0_gross'][y] - ew_a[y]['Hi 30'] for y in AN['C0_gross']}
say('Mean annual gap C1 minus FF EW Hi30: %.2f%%; C0 minus FF EW Hi30: %.2f%%; C1 minus FF VW market: %.2f%%' % (
    100 * sum(gapC1.values()) / len(gapC1), 100 * sum(gapC0.values()) / len(gapC0),
    100 * sum(AN['C1_gross'][y] - mkt_a[y] for y in gapC1) / len(gapC1)))
say('Gap C1 minus FF EW Hi30 by year:', ' '.join('%d:%+.0f' % (y, 100 * g) for y, g in sorted(gapC1.items())))

# survivorship-adjusted series: net return minus that year's control gap, spread evenly over the weeks
for s in SCR:
    gap = gapC0 if s == 'B4' else gapC1
    cnt = {}
    for w in S[s + '_net']: cnt[friday(w).year] = cnt.get(friday(w).year, 0) + 1
    S[s + '_adj'] = {w: r - gap[friday(w).year] / cnt[friday(w).year] for w, r in S[s + '_net'].items()}
    AN[s + '_adj'] = annual(S[s + '_adj'])

# cross-check against survivorship-free French low-risk portfolios
def monthly_to_annual(m, col):
    o = {}; n = {}
    for k, v in m.items():
        y = k // 100; o[y] = (1 + o.get(y, 0)) * (1 + v[col]) - 1; n[y] = n.get(y, 0) + 1
    return {y: v for y, v in o.items() if n[y] == 12}
say('\n== 2. Cross-check: my survivor-universe low-risk screens against survivorship-free Ken French portfolios (compound annual return, %)')
xc = {}
try:
    var = french_block(os.path.join(A_FR, 'Portfolios_Formed_on_VAR.csv'), 'Value Weight Returns -- Monthly')
    var_e = french_block(os.path.join(A_FR, 'Portfolios_Formed_on_VAR.csv'), 'Equal Weight Returns -- Monthly')
    bet = french_block(os.path.join(A_FR, 'Portfolios_Formed_on_BETA.csv'), 'Value Weight Returns -- Monthly')
    bet_e = french_block(os.path.join(A_FR, 'Portfolios_Formed_on_BETA.csv'), 'Equal Weight Returns -- Monthly')
    xc = {'FF LoVAR quintile VW': monthly_to_annual(var, 'Lo 20'), 'FF LoVAR quintile EW': monthly_to_annual(var_e, 'Lo 20'),
          'FF LoBETA quintile VW': monthly_to_annual(bet, 'Lo 20'), 'FF LoBETA quintile EW': monthly_to_annual(bet_e, 'Lo 20')}
    mv = french_block(os.path.join(A_FR, '25_Portfolios_ME_VAR_5x5.csv'), 'Average Value Weighted Returns -- Monthly')
    mb = french_block(os.path.join(A_FR, '25_Portfolios_ME_BETA_5x5.csv'), 'Average Value Weighted Returns -- Monthly')
    say('columns of 5x5 ME/VAR file:', list(next(iter(mv.values())))[-5:], ' ME/BETA:', list(next(iter(mb.values())))[-5:])
    c = list(next(iter(mv.values())))[-5]; xc['FF big-size, lowest VAR cell (%s)' % c] = monthly_to_annual(mv, c)
    c = list(next(iter(mb.values())))[-5]; xc['FF big-size, lowest BETA cell (%s)' % c] = monthly_to_annual(mb, c)
except Exception as ex:
    say('could not read French low-risk files from A/data/french:', ex)
say('%-46s %9s %9s %9s' % ('', '1976-2025', '1976-1998', '1999-2025'))
for k in ['B1_gross', 'B1_net', 'B1_adj', 'B2_gross', 'B2_net', 'B2_adj']:
    say('%-46s %9s %9s %9s' % (k, pc(cagr(AN[k], 1976, 2025)), pc(cagr(AN[k], 1976, 1998)), pc(cagr(AN[k], 1999, 2025))))
for k, v in xc.items():
    say('%-46s %9s %9s %9s' % (k, pc(cagr(v, 1976, 2025)), pc(cagr(v, 1976, 1998)), pc(cagr(v, 1999, 2025))))

# ---- unlevered table
say('\n== 3. Unlevered, weekly data compounded to months. Excess = arithmetic mean over T-bills, annualised. Drawdown from weekly closes.')
hdr = '%-40s %-10s %-10s %6s %6s %6s %6s %5s %6s %10s' % ('series', 'from', 'to', 'CAGR', 'excess', 'vol', 'Sharpe', 'beta', 'maxDD', '$1 grows to')
def line(name, r, start=None, end=None):
    st = stats(weeks, r, rf, mkt_m, start, end)
    if not st: say('%-40s insufficient data' % name); return None
    say('%-40s %-10s %-10s %6s %6s %6s %6.2f %5.2f %6s %10.1f' % (name, st['start'], st['end'], pc(st['cagr']), pc(st['excess']), pc(st['vol']), st['sharpe'], st['beta'] or 0, pc(st['maxdd']), st['wealth']))
    return st
for (a, b, lab) in [(D(1976, 1, 1), D(2025, 12, 31), '1976-2025 (no weekly Berkshire before April 1980)'), (D(1980, 4, 1), D(2025, 12, 31), 'April 1980 - 2025'),
                    (D(1980, 4, 1), D(1998, 12, 31), 'April 1980 - 1998'), (D(1999, 1, 1), D(2025, 12, 31), '1999 - 2025')]:
    say('\n-- ' + lab); say(hdr)
    for t in ['BRK-A', 'VFINX']: line(t, S[t], a, b)
    for s in ['C0', 'C1']: line(NAMES[s] + ' gross', S[s + '_gross'], a, b)
    for s in SCR:
        for v, lab2 in [('gross', 'gross'), ('net', 'net of costs'), ('adj', 'net, survivorship-adjusted')]:
            line('%s %s: %s' % (s, NAMES[s][:16], lab2), S[s + '_' + v], a, b)

# ---- levered tables
say('\n== 4. Levered, monthly reset, weekly accrual. Period April 1980 - December 2025 so Berkshire is like for like.')
a, b = D(1980, 4, 1), D(2025, 12, 31)
bst = stats(weeks, S['BRK-A'], rf, mkt_m, a, b)
say('Berkshire: CAGR %s, Sharpe %.2f, max drawdown %s, $1 grows to %.0f' % (pc(bst['cagr']), bst['sharpe'], pc(bst['maxdd']), bst['wealth']))
say('%-34s %4s %7s | %6s %6s %6s %8s %10s | %s' % ('series', 'L', 'finance', 'CAGR', 'Sharpe', 'maxDD', '$1 to', 'vs BRK $', 'CAGR gap to BRK'))
RES = {}
for s in ['VFINX'] + [x + v for x in SCR for v in ('_net', '_adj')]:
    for L in (1.0, 1.3, 1.6, 2.0):
        for sp in ((0.0,) if L == 1.0 else (0.0, 0.01, 0.02)):
            lv = lever_weekly(weeks, S[s], rf, L, sp)
            st = stats(weeks, lv, rf, mkt_m, a, b)
            if not st: continue
            RES[(s, L, sp)] = st
            say('%-34s %4.1f %7s | %6s %6.2f %6s %8.1f %10.2f | %+.1f' % (s, L, 'TB+%d%%' % round(sp * 100), pc(st['cagr']), st['sharpe'], pc(st['maxdd']), st['wealth'], st['wealth'] / bst['wealth'], 100 * (st['cagr'] - bst['cagr'])))

say('\n== 5. Headline test, calendar years 1976-2025. Screens: 1.6x, monthly reset, T-bill + 1%, compounded from weekly data. Berkshire: letter table.')
bl = {y: v[0] for y, v in letter.items()}
say('Berkshire CAGR 1976-2025 %s; 1976-1998 %s; 1999-2025 %s' % (pc(cagr(bl, 1976, 2025)), pc(cagr(bl, 1976, 1998)), pc(cagr(bl, 1999, 2025))))
say('S&P 500 with dividends (letter) CAGR 1976-2025 %s; 1976-1998 %s; 1999-2025 %s' % tuple(pc(cagr({y: v[1] for y, v in letter.items()}, *p)) for p in [(1976, 2025), (1976, 1998), (1999, 2025)]))
say('%-34s %10s %10s %10s %8s %8s  %s' % ('series (1.6x, TB+1%)', '1976-2025', '1976-1998', '1999-2025', 'gap', 'maxDD', 'within 2 points and drawdown above -75%?'))
HEAD = {}
for s in [x + v for x in SCR for v in ('_gross', '_net', '_adj')] + ['C1_gross']:
    lv = lever_weekly(weeks, S[s], rf, 1.6, 0.01)
    an = annual(lv)
    y0 = min(an)
    st = stats(weeks, lv, rf, mkt_m, D(1976, 1, 1), D(2025, 12, 31))
    c = cagr(an, max(1976, y0), 2025); cb = cagr(bl, max(1976, y0), 2025)
    HEAD[s] = (c, cb, st['maxdd'])
    say('%-34s %10s %10s %10s %+8.1f %8s  %s%s' % (s, pc(c), pc(cagr(an, 1976, 1998)), pc(cagr(an, 1999, 2025)), 100 * (c - cb), pc(st['maxdd']),
        'YES' if (c - cb > -0.02 and st['maxdd'] > -0.75) else 'no', '' if y0 <= 1976 else ' (starts %d; Berkshire same years %s)' % (y0, pc(cb))))
say('\nSame test at other leverage and financing, survivorship-adjusted net series, CAGR 1976-2025 (%):')
say('%-10s' % 'screen' + ''.join('%12s' % ('%.1fx TB+%d' % (L, sp * 100)) for L in (1.3, 1.6, 2.0) for sp in (0, .01, .02)))
for s in SCR:
    row = '%-10s' % s
    for L in (1.3, 1.6, 2.0):
        for sp in (0, .01, .02):
            an = annual(lever_weekly(weeks, S[s + '_adj'], rf, L, sp)); row += '%12s' % pc(cagr(an, max(1976, min(an)), 2025))
    say(row)
say('Annual-reset leverage (drift within the year), 1.6x TB+1%, survivorship-adjusted net, CAGR 1976-2025:',
    '  '.join('%s %s' % (s, pc(cagr(annual(lever_weekly(weeks, S[s + '_adj'], rf, 1.6, .01, reset='year')), max(1976, min(AN[s + '_adj'])), 2025))) for s in SCR))

say('\n== 6. Real funds, each from its first full month on Yahoo to December 2025, against Berkshire over the same weeks.')
say('%-8s %-10s | %6s %6s %6s | %6s %6s %6s | %6s %6s %6s  (CAGR, Sharpe, maxDD: fund unlevered | fund 1.6x TB+1%% | Berkshire)' % ('fund', 'from', 'CAGR', 'Sharpe', 'maxDD', 'CAGR', 'Sharpe', 'maxDD', 'CAGR', 'Sharpe', 'maxDD'))
for t in ['VFINX', 'VIVAX', 'VIG', 'SPLV', 'USMV', 'QUAL', None, 'VEIPX', 'VDIGX', 'SDY', 'RSP']:
    if t is None: say('  post hoc, not pre-registered:'); continue
    f0 = min(S[t]); f0 = max(D(1980, 4, 1), (f0 + datetime.timedelta(days=35)).replace(day=1))
    u = stats(weeks, S[t], rf, mkt_m, f0, b); l = stats(weeks, lever_weekly(weeks, {w: r for w, r in S[t].items() if friday(w) >= f0}, rf, 1.6, .01), rf, mkt_m, f0, b)
    k = stats(weeks, S['BRK-A'], rf, mkt_m, f0, b)
    say('%-8s %-10s | %6s %6.2f %6s | %6s %6.2f %6s | %6s %6.2f %6s' % (t, u['start'], pc(u['cagr']), u['sharpe'], pc(u['maxdd']), pc(l['cagr']), l['sharpe'], pc(l['maxdd']), pc(k['cagr']), k['sharpe'], pc(k['maxdd'])))

say('\n== 7. Direct bias checks: each stock screen against a survivorship-free counterpart over the same years (compound annual return, %, unlevered, gross for screens; funds are after fees).')
def span(r, a, b):
    st = stats(weeks, r, rf, mkt_m, a, b); return st['cagr'] if st else None
for scr, fund in [('B1_gross', 'SPLV'), ('B1_gross', 'USMV'), ('B2_gross', 'USMV'), ('B4_gross', 'VIG'), ('B4_gross', 'VDIGX'), ('B5_gross', 'SDY'), ('B3_gross', 'VEIPX'), ('C1_gross', 'VFINX'), ('C1_gross', 'RSP'), ('C0_gross', 'RSP')]:
    f0 = (min(S[fund]) + datetime.timedelta(days=35)).replace(day=1); f0 = max(f0, min(S[scr]))
    say('%-10s %s  vs  %-6s %s   from %s' % (scr, pc(span(S[scr], f0, b)), fund, pc(span(S[fund], f0, b)), f0))
try:
    dp = french_block(os.path.join(DATA, 'french', 'Portfolios_Formed_on_D-P.csv'), 'Value Weight Returns -- Monthly')
    dpe = french_block(os.path.join(DATA, 'french', 'Portfolios_Formed_on_D-P.csv'), 'Equal Weight Returns -- Monthly')
    say('%-46s %9s %9s %9s' % ('', '1976-2025', '1976-1998', '1999-2025'))
    for k in ['B5_gross', 'B5_net', 'B5_adj', 'B3_gross', 'B3_adj']:
        say('%-46s %9s %9s %9s' % (k, pc(cagr(AN[k], 1976, 2025)), pc(cagr(AN[k], 1976, 1998)), pc(cagr(AN[k], 1999, 2025))))
    for nm, blk, col in [('FF high dividend yield quintile VW', dp, 'Hi 20'), ('FF high dividend yield quintile EW', dpe, 'Hi 20'), ('FF high dividend yield 30% VW', dp, 'Hi 30'), ('FF high dividend yield 30% EW', dpe, 'Hi 30')]:
        v = monthly_to_annual(blk, col)
        say('%-46s %9s %9s %9s' % (nm, pc(cagr(v, 1976, 2025)), pc(cagr(v, 1976, 1998)), pc(cagr(v, 1999, 2025))))
except Exception as ex:
    say('no D/P cross-check:', ex)

say('\n== 8. Post hoc cross-check (not pre-registered): the same headline test on survivorship-free Ken French portfolios. 1.6x, monthly reset, T-bill + 1%, no trading costs, calendar years.')
def lev_m(blk, col, L=1.6, sp=0.01):
    o = {}
    for k, v in blk.items():
        if k in ffm and v[col] > -0.99: o[k] = {'x': L * v[col] - (L - 1) * (ffm[k]['RF'] + sp / 12)}
    return monthly_to_annual(o, 'x')
say('%-46s %9s %9s %9s' % ('', '1976-2025', '1976-1998', '1999-2025'))
say('%-46s %9s %9s %9s' % ('Berkshire (letter)', pc(cagr(bl, 1976, 2025)), pc(cagr(bl, 1976, 1998)), pc(cagr(bl, 1999, 2025))))
try:
    mk = {k: {'m': v['Mkt-RF'] + v['RF']} for k, v in ffm.items()}
    for nm, blk, col in [('FF market VW', mk, 'm'), ('FF lowest-variance quintile VW', var, 'Lo 20'), ('FF big-size lowest-variance cell', mv, 'BIG LoVAR'), ('FF lowest-beta quintile VW', bet, 'Lo 20'),
                         ('FF big-size lowest-beta cell', mb, 'BIG LoBETA'), ('FF high dividend yield quintile VW', dp, 'Hi 20'), ('FF high dividend yield quintile EW', dpe, 'Hi 20')]:
        v = lev_m(blk, col); u = monthly_to_annual(blk, col)
        say('%-46s %9s %9s %9s   (unlevered %s)' % (nm + ' 1.6x', pc(cagr(v, 1976, 2025)), pc(cagr(v, 1976, 1998)), pc(cagr(v, 1999, 2025)), pc(cagr(u, 1976, 2025)).strip()))
except Exception as ex:
    say('failed', ex)
say('\n== 9. Funds again, with the plain index fund at the same leverage over the same weeks (CAGR %, 1.6x, T-bill + 1%).')
for t in ['VIVAX', 'VIG', 'SPLV', 'USMV', 'QUAL', 'VEIPX', 'VDIGX', 'SDY', 'RSP']:
    f0 = (min(S[t]) + datetime.timedelta(days=35)).replace(day=1)
    g = lambda x: stats(weeks, lever_weekly(weeks, {w: r for w, r in S[x].items() if friday(w) >= f0}, rf, 1.6, .01), rf, mkt_m, f0, b)
    say('%-6s from %s: fund %s (maxDD %s) | VFINX %s (maxDD %s) | Berkshire unlevered %s' % (t, f0, pc(g(t)['cagr']), pc(g(t)['maxdd']), pc(g('VFINX')['cagr']), pc(g('VFINX')['maxdd']), pc(stats(weeks, S['BRK-A'], rf, mkt_m, f0, b)['cagr'])))

# ---- export
keys = sorted(S)
with open(os.path.join(OUT, 'series_weekly.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['week_monday', 'rf_weekly'] + keys)
    for d in weeks:
        w.writerow([d.isoformat(), '%.7f' % rf[d] if rf.get(d) is not None else ''] + [('%.6f' % S[k][d]) if d in S[k] else '' for k in keys])
json.dump({'headline': {k: v for k, v in HEAD.items()}}, open(os.path.join(OUT, 'headline.json'), 'w'))
