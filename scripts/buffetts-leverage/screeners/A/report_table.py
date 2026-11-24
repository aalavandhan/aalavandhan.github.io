"""Results table for REPORT.md, computed from screeners/series.csv. Run: python -I report_table.py <series.csv> <A-folder>"""
import sys, os, pandas as pd, numpy as np
s = pd.read_csv(sys.argv[1]); s.index = [int(d[:4]) * 100 + int(d[5:7]) for d in s.date]
la = pd.read_csv(os.path.join(sys.argv[2], 'out', 'berkshire_annual_letter.csv'), index_col=0).iloc[:, 0]
p = lambda x, d=1: f'{x*100:.{d}f}%'; g = lambda x: f'${x:,.0f}'
def row(name, r, cost=False):
    ex = r - s.rf; mk = s.market - s.rf; w = (1 + r).cumprod()
    c = lambda a, b: (1 + r.loc[a:b]).prod() ** (12 / len(r.loc[a:b])) - 1
    r12 = ((1 + r).rolling(12).apply(np.prod, raw=True) - 1).min()
    return [name, p(c(197601, 202512)), g(w.iloc[-1]), p(w.iloc[-1] / bw, 0), p(c(197601, 199812)), p(c(199901, 202512)), p(c(197601, 201112)), p(c(201201, 202512)),
            p(ex.std() * 12 ** .5), f'{ex.mean()/ex.std()*12**.5:.2f}', f'{np.cov(ex, mk)[0,1]/mk.var():.2f}', p((w / w.cummax()).min() - 1, 0), p(r12, 0)]
bw = (1 + la.loc[1976:2025]).prod(); bc = lambda a, b: (1 + la.loc[a:b]).prod() ** (1 / (b - a + 1)) - 1
b = s.berkshire.dropna(); bex = b - s.rf.loc[b.index]; bm = (s.market - s.rf).loc[b.index]; wb = (1 + b).cumprod()
rows = [['Berkshire Hathaway', p(bc(1976, 2025)), g(bw), '100%', p(bc(1976, 1998)), p(bc(1999, 2025)), p(bc(1976, 2011)), p(bc(2012, 2025)),
         p(bex.std() * 12 ** .5) + '*', f'{bex.mean()/bex.std()*12**.5:.2f}*', f'{np.cov(bex, bm)[0,1]/bm.var():.2f}*', p((wb / wb.cummax()).min() - 1, 0) + '*', p(((1 + b).rolling(12).apply(np.prod, raw=True) - 1).min(), 0) + '*']]
rows.append(row('US market, unlevered', s.market)); rows.append(row('US market, 1.6x, T-bill + 1%', s.market_16x_tbill1))
for k, nm in [('a11', 'A11 cheap + safe + quality'), ('a2', 'A2 low variance'), ('a10', 'A10 big-cheap-profitable + low beta')]:
    rows.append(row(nm + ', unlevered', s[k])); rows.append(row(nm + ', 1.6x, T-bill, no costs', s[k + '_16x_tbill']))
    rows.append(row(nm + ', 1.6x, T-bill + 1%, no costs', s[k + '_16x_tbill1'])); rows.append(row(nm + ', 1.6x, T-bill + 1%, 0.5% costs (headline)', s[k + '_16x_tbill1_cost']))
h = ['Series', 'CAGR 1976-2025', '$1 grows to', 'Share of Berkshire\'s final wealth', 'CAGR 1976-1998', 'CAGR 1999-2025', 'CAGR 1976-2011', 'CAGR 2012-2025', 'Volatility', 'Sharpe', 'Beta', 'Largest fall (month-end)', 'Worst 12 months']
print('| ' + ' | '.join(h) + ' |'); print('|' + '---|' * len(h))
for r in rows: print('| ' + ' | '.join(r) + ' |')
