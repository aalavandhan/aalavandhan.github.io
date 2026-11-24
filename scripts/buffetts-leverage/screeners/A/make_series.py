"""Write screeners/series.csv for charting. Run: python -I make_series.py <A-folder> <out-csv>"""
import sys, os, calendar, pandas as pd, numpy as np
A, OUTF = sys.argv[1], sys.argv[2]
m = pd.read_csv(os.path.join(A, 'out', 'monthly_unlevered.csv'), index_col=0)
la = pd.read_csv(os.path.join(A, 'out', 'berkshire_annual_letter.csv'), index_col=0).iloc[:, 0]
SC = {'a11': 'A11', 'a2': 'A2', 'a10': 'A10'}
o = pd.DataFrame(index=m.index)
o['date'] = ['%04d-%02d-%02d' % (i // 100, i % 100, calendar.monthrange(i // 100, i % 100)[1]) for i in m.index]
o['berkshire'] = m['berkshire']; o['market'] = m['market']; o['rf'] = m['rf']
o['market_16x_tbill1'] = 1.6 * m['market'] - 0.6 * (m['rf'] + 0.01 / 12)
for k, c in SC.items():
    o[k] = m[c]
    o[k + '_16x_tbill'] = 1.6 * m[c] - 0.6 * m['rf']
    o[k + '_16x_tbill1'] = 1.6 * m[c] - 0.6 * (m['rf'] + 0.01 / 12)
    o[k + '_16x_tbill1_cost'] = 1.6 * (m[c] - 0.005 / 12) - 0.6 * (m['rf'] + 0.01 / 12)
ret_cols = [c for c in o.columns if c != 'date']
# wealth indices: $1 at 31 December 1975
for c in ret_cols:
    if c in ('berkshire',): continue
    o['w_' + c] = (1 + o[c]).cumprod()
# Berkshire wealth: letter year-ends 1976-1980, then Yahoo monthly path; back-filled inside 1980 from December 1980
w = pd.Series(np.nan, index=m.index); lvl = 1.0
for y in range(1976, 1981):
    lvl *= 1 + la[y]; w[y * 100 + 12] = lvl
for i in [198011, 198010, 198009, 198008, 198007, 198006, 198005, 198004, 198003]:
    nxt = i + 1
    w[i] = w[nxt] / (1 + m.loc[nxt, 'berkshire'])
idx = list(m.index); p = idx.index(198012)
for j in range(p + 1, len(idx)):
    w[idx[j]] = w[idx[j - 1]] * (1 + m.loc[idx[j], 'berkshire'])
o['w_berkshire'] = w
o.to_csv(OUTF, index=False, float_format='%.6f')
print(o.iloc[[0, 50, -1]].T)
print('berkshire wealth end', w.iloc[-1], 'letter product', (1 + la.loc[1976:2025]).prod())
