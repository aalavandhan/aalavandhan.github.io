"""Item 4: Table 3 (cost of float) and Section 4 (leverage), verified from the already-collected files
../float.csv and ../leverage_cost.csv. Nothing is re-collected here.
Run:  python -I float_leverage.py

Cost-of-float rule, fixed before computing:
  rule A ("letter-literal"): where the letter's float table prints a number, use it; where it prints
     "less than zero", use 0 (the paper's footnote); for years after the table was discontinued (1998 on)
     use -underwriting result / average float, which can be negative.
  rule B: same, but 1998 (a small underwriting profit, no cost printed) is also set to 0.
Spread over T-bills uses the calendar-year compounded one-month bill return from Ken French's file.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
from common import DATA, RES, HERE

f = pd.read_csv(os.path.join(HERE, "..", "float.csv")).set_index("year")
fac = pd.read_csv(os.path.join(DATA, "factors_monthly.csv"), index_col=0)
fac["year"] = fac.index.str[:4].astype(int)
tb = fac.groupby("year")["RF"].apply(lambda x: ((1 + x).prod() - 1) * 100)

lt0 = f["letter_cost_pct"].astype(str).str.contains("less than zero")
costA = f["cost_of_float_pct"].where(~lt0, 0.0)
costB = costA.copy(); costB[1998] = 0.0
neg = lt0 | (f["cost_of_float_pct"] < 0)
paper = {"1976-1980": (0.79, 1.67, -4.59), "1981-1985": (0.20, 10.95, 1.10), "1986-1990": (0.00, 3.07, -3.56),
         "1991-1995": (0.60, 2.21, -2.00), "1996-2000": (0.60, 2.36, -2.70), "2001-2005": (0.60, 1.29, -0.82),
         "2006-2011": (1.00, -4.00, -5.84), "1976-2011": (0.60, 2.20, -3.09)}
rows = []
for per, p in list(paper.items()) + [("2012-2025", (np.nan,) * 3), ("1976-2025", (np.nan,) * 3)]:
    a, b = map(int, per.split("-"))
    idx = range(a, b + 1)
    rows.append(dict(period=per, frac_negative=neg.loc[idx].mean(), cost_ruleA=costA.loc[idx].mean(), cost_ruleB=costB.loc[idx].mean(),
                     tbill=tb.loc[idx].mean(), spread_ruleA=costA.loc[idx].mean() - tb.loc[idx].mean(),
                     spread_ruleB=costB.loc[idx].mean() - tb.loc[idx].mean(),
                     paper_frac=p[0], paper_cost=p[1], paper_spread_tbill=p[2]))
t3 = pd.DataFrame(rows)
t3.to_csv(os.path.join(RES, "table3_float_cost.csv"), index=False)
pd.set_option("display.width", 250); print(t3.round(2).to_string())

# ---- leverage, three definitions, from leverage_cost.csv (balance sheets 1995-2025)
l = pd.read_csv(os.path.join(HERE, "..", "leverage_cost.csv")).set_index("year")
l["cash_all"] = l["cash"] + l["tbills"]
l["L_paper"] = (l["A"] + l["mc"] - l["E"] - l["cash_all"]) / l["mc"]          # (TA_MV - cash) / Equity_MV
l["L_debt_float"] = (l["mc"] + l["debt"] + l["fl"]) / l["mc"]                 # (Equity_MV + debt + float) / Equity_MV
l["L_book"] = (l["A"] - l["cash_all"]) / l["E"]
l["float_share_of_liabilities"] = l["fl"] / (l["A"] - l["E"])
l["debt_float_share"] = (l["debt"] + l["fl"]) / (l["A"] - l["E"])
cols = ["L_paper", "L_debt_float", "L_book", "float_share_of_liabilities", "debt_float_share"]
l[cols].to_csv(os.path.join(RES, "leverage_by_year.csv"))
rows = []
for a, b in [(1996, 2011), (1997, 2011), (2012, 2025), (1996, 2025)]:
    w = l.loc[a:b, cols]
    rows.append(dict(window=f"{a}-{b}", **w.mean().to_dict(), n_L_debt_float=int(w.L_debt_float.notna().sum())))
lv = pd.DataFrame(rows); lv.to_csv(os.path.join(RES, "leverage_summary.csv"), index=False); print(lv.round(3).to_string())
print("paper: 1.6 (total assets, 1976-2011), 1.4 (debt + float), 1.4 (vol ratio 24.8/17.2 =", round(24.8 / 17.2, 2), "), Table 2 prints 1.64; float = 36% of liabilities")
print("1.6x the market's 6.1% =", round(1.6 * 6.1, 1), "% (paper: 'about 10%')")
