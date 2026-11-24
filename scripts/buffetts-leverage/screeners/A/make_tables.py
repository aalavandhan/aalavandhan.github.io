"""Turn out/*.csv into markdown tables (out/tables.md). Run: python -I make_tables.py <A-folder>"""
import sys, os, pandas as pd
A = sys.argv[1]; O = os.path.join(A, 'out')
st = pd.read_csv(os.path.join(O, 'stats_all.csv')); bk = pd.read_csv(os.path.join(O, 'stats_berkshire.csv')).set_index('window')
af = pd.read_csv(os.path.join(O, 'stats_annual_freq.csv')); mm = pd.read_csv(os.path.join(O, 'margin_monthly.csv')); md = pd.read_csv(os.path.join(O, 'margin_daily.csv'))
p = lambda x, d=1: '' if pd.isna(x) else f'{x*100:.{d}f}%'
f2 = lambda x: f'{x:.2f}'
g = lambda x: f'${x:,.0f}' if x >= 100 else f'${x:,.1f}'
out = []
def table(title, hdr, rows):
    out.append(f'\n### {title}\n'); out.append('| ' + ' | '.join(hdr) + ' |'); out.append('|' + '---|' * len(hdr))
    for r in rows: out.append('| ' + ' | '.join(str(x) for x in r) + ' |')
lab = lambda r: f"{r.screen} {r['name']}" if r.screen != 'Market' else 'US market'
def sel(w, L, fin, h):
    x = st[(st.window == w) & (st.L == L) & (st.fin == fin) & ((st.haircut == h) | (st.screen == 'Market'))]
    return x[(x.screen != 'Market') | (x.haircut == 0)]
# T1
for w in ['1976-2025', '1976-2011', '2012-2025']:
    rows = [[lab(r), p(r.excess), p(r.vol), f2(r.sharpe), f2(r.beta), p(r.cagr), g(r.growth), p(r.maxdd, 0), p(r.worst12m, 0)] for _, r in sel(w, 1.0, 'F0 Tbill', 0).iterrows()]
    b = bk.loc[w]
    rows.append(['Berkshire (calendar-year data)', p(b.excess_a), p(b.vol_a), f2(b.sharpe_a), f2(b.beta_a), p(b.cagr_a), g(b.growth_a), '' if pd.isna(b.maxdd) else p(b.maxdd, 0), f'worst year {p(b.worst_year,0)}'])
    table(f'T1. Unlevered, as published (no cost haircut), monthly data, {w}', ['Screen', 'Excess', 'Vol', 'Sharpe', 'Beta', 'CAGR', '$1 grows to', 'Max DD', 'Worst 12m'], rows)
# T2 headline
x = {w: sel(w, 1.6, 'F1 Tbill+1', 0.005).set_index('screen') for w in ['1976-2025', '1976-2011', '2012-2025']}
rows = []
for s, r in x['1976-2025'].iterrows():
    rows.append([lab(r.rename(None).to_frame().T.assign(screen=s).iloc[0]), p(r.excess), p(r.vol), f2(r.sharpe), f2(r.beta), p(r.cagr), g(r.growth), p(r.maxdd, 0), p(r.worst12m, 0), p(r.gap_cagr_a), f2(r.wealth_ratio_vs_brk), 'yes' if r.wealth_ratio_vs_brk >= .5 else 'no',
                 p(x['1976-2011'].loc[s].cagr), p(x['1976-2011'].loc[s].gap_cagr_a), p(x['2012-2025'].loc[s].cagr), p(x['2012-2025'].loc[s].gap_cagr_a)])
b = bk.loc['1976-2025']
rows.append(['Berkshire', p(b.excess_a), p(b.vol_a) + ' (annual)', f2(b.sharpe_a) + ' (annual)', f2(b.beta_a) + ' (annual)', p(b.cagr_a), g(b.growth_a), '', f'worst year {p(b.worst_year,0)}', '0', '1.00', '', p(bk.loc['1976-2011'].cagr_a), '0', p(bk.loc['2012-2025'].cagr_a), '0'])
table('T2. Headline scenario: 1.6x, T-bill + 1%, 0.5% a year cost haircut. Monthly statistics 1976-2025; CAGR by window',
      ['Screen', 'Excess', 'Vol', 'Sharpe', 'Beta', 'CAGR 76-25', '$1 grows to', 'Max DD', 'Worst 12m', 'CAGR gap to BRK', 'Wealth / BRK', 'Passes (>= 0.5)', 'CAGR 76-11', 'gap', 'CAGR 12-25', 'gap'], rows)
# T3 financing x leverage for designated + market
for s in ['A10', 'A11', 'A13', 'Market']:
    x = st[(st.screen == s) & (st.window == '1976-2025') & (st.haircut == (0.005 if s != 'Market' else 0))]
    fins = [f for f in ['F0 Tbill', 'F1 Tbill+1', 'F2 Tbill+2', 'F3 FedFunds+0.5', 'F4 BRK float', 'F5 BRK blend'] if f in set(x.fin)]
    rows = []
    for L in [1.3, 1.6, 2.0]:
        for fn in fins:
            r = x[(x.L == L) & (x.fin == fn)].iloc[0]
            rows.append([f'{L}x', fn, p(r.cagr), g(r.growth), p(r.gap_cagr_a), f2(r.wealth_ratio_vs_brk), p(r.vol), f2(r.sharpe), p(r.maxdd, 0), p(r.worst12m, 0), p(r.worst1m, 0)])
    table(f'T3. {s}: leverage and financing, 1976-2025' + (', 0.5% haircut' if s != 'Market' else ', no haircut'), ['L', 'Financing', 'CAGR', '$1 grows to', 'Gap to BRK', 'Wealth / BRK', 'Vol', 'Sharpe', 'Max DD', 'Worst 12m', 'Worst month'], rows)
# T4 like-for-like monthly from April 1980
for w in ['1980.04-2025', '1980.04-2011', '2012-2025']:
    b = bk.loc[w]
    rows = [['Berkshire', '', p(b.excess), p(b.vol), f2(b.sharpe), f2(b.beta), p(b.cagr), g(b.growth), p(b.maxdd, 0), p(b.worst12m, 0)]]
    for L, fn, h, t in [(1.0, 'F0 Tbill', 0, 'unlevered, as published'), (1.6, 'F1 Tbill+1', 0.005, '1.6x, T-bill+1%, 0.5% haircut')]:
        for _, r in sel(w, L, fn, h).iterrows():
            if r.screen in ('Market', 'A10', 'A11', 'A13', 'A8', 'A2'):
                rows.append([lab(r), t, p(r.excess), p(r.vol), f2(r.sharpe), f2(r.beta), p(r.cagr), g(r.growth), p(r.maxdd, 0), p(r.worst12m, 0)])
    table(f'T4. Like-for-like monthly comparison with Berkshire, {w}', ['Series', 'Version', 'Excess', 'Vol', 'Sharpe', 'Beta', 'CAGR', '$1 grows to', 'Max DD', 'Worst 12m'], rows)
# T5 spread
h = st[(st.window == '1976-2025') & (st.screen != 'Market') & (st.haircut == 0.005) & (st.L > 1)]
rows = []
for (L, fn), x in h.groupby(['L', 'fin']):
    rows.append([f'{L}x', fn, p(x.cagr_a.min()), p(x.cagr_a.median()), p(x.cagr_a.max()), f2(x.wealth_ratio_vs_brk.median()), int((x.wealth_ratio_vs_brk >= .5).sum()), ', '.join(x[x.wealth_ratio_vs_brk >= .5].screen)])
table('T5. Spread across all thirteen screens, 1976-2025, 0.5%% haircut (Berkshire CAGR %s)' % p(bk.loc['1976-2025'].cagr_a), ['L', 'Financing', 'Lowest CAGR', 'Median CAGR', 'Highest CAGR', 'Median wealth / BRK', 'Screens passing', 'Which'], rows)
# T6 margin monthly
x = mm[mm.fin == 'F1 Tbill+1']
rows = [[r.screen, f'{r.L}x', p(r.MA_min_ratio, 0), int(r.MA_triggers30), p(r.annreset_min_ratio, 0), g(r.annreset_growth), int(r.MB30_n), '' if pd.isna(r.MB30_dates) else r.MB30_dates, g(r.MB30_growth), int(r.MB40_n), g(r.MB40_growth)] for _, r in x.iterrows()]
table('T6. Margin rules, month-end checks, T-bill + 1%, 0.5% haircut, 1976-2025', ['Screen', 'L', 'M-A: lowest month-end equity/assets (monthly rebalance)', 'M-A triggers', 'Annual reset: lowest equity/assets', 'Annual reset, no rule: $1 to', 'M-B 30% triggers', 'M-B dates', 'M-B: $1 to', 'M-B40 triggers', 'M-B40: $1 to'], rows)
x = md[md.worst_date.isna() & (md.spread == 0.01)]
rows = [[r.screen, f'{r.L}x', p(r.min_ratio_daily, 0), g(r.noMargin_growth), int(r.monthend30_n), g(r.monthend30_growth), int(r.daily30_n), r.daily30_dates if isinstance(r.daily30_dates, str) else '', g(r.daily30_growth), int(r.monthend40_n), int(r.daily40_n), g(r.daily40_growth)] for _, r in x.iterrows()]
table('T7. Margin rule M-D: same annual-reset account checked daily against month-end, T-bill + 1%, 1976-2025', ['Portfolio', 'L', 'Lowest daily equity/assets with no rule', 'No rule: $1 to', '30% rule, month-end checks: triggers', '$1 to', '30% rule, daily checks: triggers', 'Dates', '$1 to', '40% month-end triggers', '40% daily triggers', '40% daily: $1 to'], rows)
x = md[md.worst_date.notna()]
rows = [[r.screen, f'{r.L}x', p(r.const_monthly_rebal_worst_intramonth_ratio, 0), int(r.worst_date)] for _, r in x.iterrows()]
table('T8. Constant leverage rebalanced monthly: lowest equity/assets reached inside a month (daily path)', ['Portfolio', 'L', 'Lowest equity/assets', 'Date'], rows)
open(os.path.join(O, 'tables.md'), 'w').write('\n'.join(out) + '\n')
