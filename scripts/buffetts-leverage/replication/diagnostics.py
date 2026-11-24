"""Diagnostics that explain gaps between this replication and the paper.
Run:  python -I diagnostics.py
None of these feed back into the headline numbers; they are reported as diagnostics only.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # needed under python -I
import numpy as np
import pandas as pd
from common import *

df = load()
fac = pd.read_csv(os.path.join(DATA, "factors_monthly.csv"), index_col=0)
brk = pd.read_csv(os.path.join(DATA, "berkshire_monthly.csv"), index_col=0)
rows = []

# (a) the market over the paper's full window: this part needs no Berkshire data
for name, col in [("French Mkt-RF", "MKT_RF"), ("AQR MKT (USA)", "AQR_MKT_RF")]:
    m = fac.loc["1976-11":"2011-12", col]
    rows.append(dict(item=f"market 1976-11..2011-12, {name}", avg_excess=m.mean() * 12, vol=m.std() * np.sqrt(12),
                     sharpe=m.mean() / m.std() * np.sqrt(12), paper="6.1% / 15.8% / 0.39"))
    print(rows[-1])

# (b) sub-period market excess returns, French vs AQR vs paper
sp = []
for (a, b), p in zip([("1976-11", "1980-12"), ("1981-01", "1985-12"), ("1986-01", "1990-12"), ("1991-01", "1995-12"),
                      ("1996-01", "2000-12"), ("2001-01", "2005-12"), ("2006-01", "2011-12")],
                     [.078, .043, .054, .120, .118, .016, .007]):
    sp.append(dict(period=f"{a}..{b}", french=fac.loc[a:b, "MKT_RF"].mean() * 12, aqr=fac.loc[a:b, "AQR_MKT_RF"].mean() * 12,
                   paper=p))
sp = pd.DataFrame(sp); print(sp)
sp.to_csv(os.path.join(RES, "diag_market_subperiods.csv"), index=False)

# (c) is the 2006-2011 gap an end-date effect? Show the mean for each possible end month in 2011.
e = []
for end in [f"2011-{m:02d}" for m in range(1, 13)]:
    w = df.loc["2006-01":end]
    e.append(dict(end=end, brk_excess=w.ex.mean() * 12, mkt_excess=w.MKT.mean() * 12, n=len(w)))
e = pd.DataFrame(e); print(e, "\npaper: brk 3.3%, mkt 0.7%")
e.to_csv(os.path.join(RES, "diag_2006_2011_end_month.csv"), index=False)
# full-sample stats if the sample ended at each of those months
for end in ["2011-03", "2011-09", "2011-12"]:
    w = df.loc[PAPER_START:end]
    print(end, {k: round(v, 4) for k, v in perf(w.ex, w.MKT).items() if k in ("avg_excess", "vol", "sharpe", "beta", "info_ratio")})

# (d) class A vs class B (the paper value-weights the two classes)
d = brk[["ret_A", "ret_B"]].dropna()
print("A vs B monthly returns:", len(d), "months, corr", round(d.corr().iloc[0, 1], 4),
      "mean A-B annualised", round((d.ret_A - d.ret_B).mean() * 12, 5),
      "2006-2011 A", round(d.loc["2006-01":"2011-12", "ret_A"].mean() * 12, 4), "B", round(d.loc["2006-01":"2011-12", "ret_B"].mean() * 12, 4))

# (e) bridging estimate for the months Yahoo lacks (Jan 1977 - Mar 1980).
# Known: letter calendar-year returns 1977-1980, Yahoo closes for Mar 1980 and Dec 1980.
ann = pd.read_csv(os.path.join(DATA, "berkshire_annual_letter.csv"), index_col=0)["brk_pct"] / 100
p_dec80 = brk.loc["1980-12", "close_A"]; p_mar80 = brk.loc["1980-03", "close_A"]
p_dec79 = p_dec80 / (1 + ann[1980]); p_dec76 = p_dec79 / ((1 + ann[1977]) * (1 + ann[1978]) * (1 + ann[1979]))
n = 39
mean_log = np.log(p_mar80 / p_dec76) / n
rf = fac.loc["1977-01":"1980-03", "RF"].mean()
mine = df.loc[PAPER_START:PAPER_END, "ex"]
print(f"implied closes: Dec-1976 {p_dec76:.1f}, Dec-1979 {p_dec79:.1f}; Yahoo Mar-1980 {p_mar80}; mean log return {mean_log:.4f}/month over {n} months; mean RF {rf:.4f}")
br = []
for sig in [0.06, 0.07, 0.08, 0.10]:   # assumed monthly volatility in the missing months; sample 1980-85 value printed below
    arith = np.exp(mean_log + sig ** 2 / 2) - 1
    ex39 = arith - rf
    comb = (ex39 * n + mine.sum()) / (n + len(mine))
    sub = (ex39 * n + df.loc["1980-04":"1980-12", "ex"].sum()) / (n + 9)
    br.append(dict(assumed_monthly_vol=sig, est_excess_1977_01_1980_03_ann=ex39 * 12, est_avg_excess_1977_2011_ann=comb * 12,
                   est_avg_excess_1977_1980_ann=sub * 12))
br = pd.DataFrame(br); print(br); print("monthly vol 1980-04..1985-12:", round(df.loc["1980-04":"1985-12", "ex"].std(), 4))
br.to_csv(os.path.join(RES, "diag_bridge_1977_1980.csv"), index=False)
pd.DataFrame(rows).to_csv(os.path.join(RES, "diag_market_full_window.csv"), index=False)
# what Nov+Dec 1976 would have to be for the paper's 42.1% (50 months) to hold, at 8% vol
ex39 = np.exp(mean_log + 0.08 ** 2 / 2) - 1 - rf
need = 0.421 / 12 * 50 - ex39 * n - df.loc["1980-04":"1980-12", "ex"].sum()
print("sum of Nov+Dec 1976 excess returns needed to reach paper's 42.1% for 1976-1980:", round(need, 3))

# (f) market over the full window for alternative end months (follow-up to (c))
ff = []
for end in ["2011-06", "2011-09", "2011-12"]:
    for col in ["MKT_RF", "AQR_MKT_RF"]:
        m = fac.loc["1976-11":end, col]
        ff.append(dict(end=end, source=col, avg_excess=m.mean() * 12, vol=m.std() * np.sqrt(12), sharpe=m.mean() / m.std() * np.sqrt(12)))
ff = pd.DataFrame(ff); print(ff); ff.to_csv(os.path.join(RES, "diag_market_end_month.csv"), index=False)
