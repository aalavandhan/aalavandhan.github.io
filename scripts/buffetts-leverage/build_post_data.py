"""Build assets/js/buffetts-leverage/data.js from the CSVs in this folder.

leverage: [year, leverage_mv, blended_cost_pct, tbill_pct]         1995-2025
cost:     [year, blended_cost_pct, tbill_pct, estimated(0/1)]       1977-2025
stock:    [year, share_price_change_pct, assets_per_share_change_pct, estimated(0/1)] 1977-2025
race:     [month, then one value per name in race_cols]: growth of $1 from the end of 1975, from screeners/series.csv
metrics:  [name, colour key, return % a year, $1 becomes, volatility %, Sharpe, worst drawdown %, worst month %]
"""
import csv
import json
import collections
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "assets" / "js" / "buffetts-leverage" / "data.js"

tb = collections.defaultdict(list)
for r in csv.reader(open(HERE / "tb3ms.csv")):
    if r[0][:4].isdigit() and r[1] not in ("", "."):
        tb[int(r[0][:4])].append(float(r[1]))
tb = {y: round(sum(v) / len(v), 2) for y, v in tb.items()}

lev = []
for r in csv.DictReader(open(HERE / "leverage_cost.csv")):
    y = int(r["year"])
    b = r.get("blend_pct")
    # 1999-2001 interest is overstated (finance-business repos), so no blended cost for those years
    blend = round(float(b), 2) if b and y not in (1999, 2000, 2001) else None
    lev.append([y, round(float(r["lev_mv"]), 2), blend, tb[y]])

# Blended cost of borrowing for the whole period. Measured from 1996 (leverage_cost.csv); estimated before
# that and for 1999-2001, where the balance-sheet lines are missing or unreliable. ILLUSTRATIVE ONLY.
#   estimate = (cost of float x float + bond yield x debt + 0 x deferred taxes) / (float + debt + deferred taxes)
# Before 1996: debt assumed at 0.35x float (the 1996-97 ratio) and deferred taxes at 0.5x float (below the
#   1996-97 ratio of 1.0-1.5x, since unrealised gains were smaller earlier); debt costed at the long-term
#   government bond yield Buffett quotes in the letters (float.csv).
# 1999-2001: actual year-end float, debt and deferred taxes; debt costed at 5.4% (the 1998 and 2002 average).
frow = {int(r["year"]): r for r in csv.DictReader(open(HERE / "float.csv"))}
lrow = {int(r["year"]): r for r in csv.DictReader(open(HERE / "leverage_cost.csv"))}
cost = []
for y in range(1977, 2026):
    b = lrow.get(y, {}).get("blend_pct")
    if b and y not in (1999, 2000, 2001):
        cost.append([y, round(float(b), 2), tb[y], 0])
    elif y in (1999, 2000, 2001):
        r = lrow[y]
        F, D, T = float(r["fl"]), float(r["debt"]), float(r["dt"])
        cost.append([y, round(100 * (-float(r["uw"]) + 0.054 * D) / (F + D + T), 2), tb[y], 1])
    else:
        r = frow[y]
        est = (float(r["cost_of_float_pct"]) + 0.35 * float(r["letter_lt_govt_bond_yield_pct"])) / (1 + 0.35 + 0.5)
        cost.append([y, round(est, 2), tb[y], 1])

# Yearly change in Berkshire's share price and in the market value of its assets per Class A share, 1977-2025.
# Asset value = market cap + liabilities (total assets - book equity + market cap), the paper's definition.
# It is built from the share price, so it is not an independent measure of what the holdings are worth.
# 1996-2025: measured from the annual reports (leverage_cost.csv, share counts in debt.csv).
# 1977-1995: share price change is from the letters (screeners/series.csv). The asset change is an ILLUSTRATIVE
#   ESTIMATE: stock return / 1.4 + (1 - 1/1.4) x growth in average float. That is, assets are 1.4x equity
#   (leverage was 1.26 at the end of 1995 and 1.44 at the end of 1996) and liabilities grow in line with float.
#   Run over 1997-2011, the same formula with actual leverage lands within about 10 points of the measured
#   figure in most years (1999 is the worst miss).
shares = {int(r["year"]): float(r["value_usd_m"]) for r in csv.DictReader(open(HERE / "debt.csv"))
          if r["item"] == "class_a_equivalent_shares"}
wealth = {1975: 1.0}
for r in csv.DictReader(open(HERE / "screeners" / "series.csv")):
    if r["date"][5:7] == "12" and r["w_berkshire"]:
        wealth[int(r["date"][:4])] = float(r["w_berkshire"])
avg_float = {y: float(r["average_float_usd_m"]) for y, r in frow.items() if r["average_float_usd_m"]}
def per_share(y, assets):
    r = lrow[y]
    A, E, mc = float(r["A"]), float(r["E"]), float(r["mc"])
    return (A - E + mc if assets else mc) / shares[y]
stock = []
for y in range(1977, 2026):
    if y >= 1996:
        pc = per_share(y, False) / per_share(y - 1, False) - 1
        ac = per_share(y, True) / per_share(y - 1, True) - 1
        stock.append([y, round(100 * pc, 1), round(100 * ac, 1), 0])
    else:
        pc = wealth[y] / wealth[y - 1] - 1
        ac = pc / 1.4 + (1 - 1 / 1.4) * (avg_float[y] / avg_float[y - 1] - 1)
        stock.append([y, round(100 * pc, 1), round(100 * ac, 1), 1])

data = {"leverage": lev, "cost": cost, "stock": stock}
series = HERE / "screeners" / "series.csv"
if series.exists():
    # value of $1 invested at the end of 1975; Berkshire is year-end only for 1976-79, monthly after
    cols = ["w_berkshire", "w_market", "w_a11"]
    # plus the screen at 2.2x, borrowing at the T-bill rate and reset monthly: 2.2 x screen return - 1.2 x T-bill.
    # (The same formula at 1.6x reproduces the a11_16x_tbill column to 7 decimal places.)
    data["race_cols"] = cols + ["w_a11_22x_tbill"]
    # every line starts at $1 at the end of 1975 (the series file begins with January 1976)
    data["race"] = [["1975-12"] + [1.0] * (len(cols) + 1)]
    w22 = 1.0
    for r in csv.DictReader(open(series)):
        row = [r["date"][:7]]
        for c in cols:
            row.append(None if r[c] in ("", "nan") else float("%.4g" % float(r[c])))
        w22 *= 1 + 2.2 * float(r["a11"]) - 1.2 * float(r["rf"])
        row.append(float("%.4g" % w22))
        data["race"].append(row)

    # Summary table under the growth chart. Return and final value cover 1976-2025. Volatility, Sharpe ratio,
    # worst drawdown and worst month use monthly returns from April 1980, when monthly Berkshire prices start.
    import math, statistics
    srows = [r for r in csv.DictReader(open(series))]
    sub = [r for r in srows if r["berkshire"] not in ("", "nan")]
    rf = [float(r["rf"]) for r in sub]
    def risk(rets):
        ex = [a - b for a, b in zip(rets, rf)]
        w = peak = 1.0
        dd = 0.0
        for a in rets:
            w *= 1 + a
            peak = max(peak, w)
            dd = min(dd, w / peak - 1)
        return [round(100 * statistics.stdev(rets) * math.sqrt(12), 1),
                round(statistics.mean(ex) * 12 / (statistics.stdev(ex) * math.sqrt(12)), 2),
                round(100 * dd), round(100 * min(rets))]
    last = dict(zip(data["race_cols"], data["race"][-1][1:]))
    def row(name, key, rets):
        return [name, key, round(100 * (last[key] ** (1 / 50) - 1), 1), round(last[key])] + risk(rets)
    # [name, colour key, return % a year, $1 becomes, volatility %, Sharpe, worst drawdown %, worst month %]
    data["metrics"] = [
        row("Berkshire", "w_berkshire", [float(r["berkshire"]) for r in sub]),
        row("Synthetic at 2.2\u00d7", "w_a11_22x_tbill", [2.2 * float(r["a11"]) - 1.2 * float(r["rf"]) for r in sub]),
        row("Synthetic at 1\u00d7", "w_a11", [float(r["a11"]) for r in sub]),
        row("US market", "w_market", [float(r["market"]) for r in sub]),
    ]

OUT.write_text("// Generated by scripts/buffetts-leverage/build_post_data.py. Do not edit by hand.\nwindow.BLV_DATA = "
               + json.dumps(data, separators=(",", ":")) + ";\n")
print("wrote", OUT, {k: len(v) for k, v in data.items()})
