"""Build data/factors_monthly.csv and data/berkshire_monthly.csv from data/raw/.

Run with:  python -I build_series.py
All returns are decimal monthly returns (0.01 = 1%).
"""
import csv, json, datetime, os
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "raw")
OUT = os.path.join(HERE, "data")


def french_monthly(fname, cols):
    """Read the monthly block (YYYYMM rows) of a Ken French CSV."""
    rows = {}
    started = False
    with open(os.path.join(RAW, fname)) as f:
        for line in f:
            p = [x.strip() for x in line.strip().split(",")]
            if len(p) == len(cols) + 1 and len(p[0]) == 6 and p[0].isdigit():
                started = True
                vals = [float(x) for x in p[1:]]
                if any(v <= -99.99 for v in vals):
                    continue
                rows[p[0][:4] + "-" + p[0][4:]] = [v / 100 for v in vals]
            elif started and p[0] and not p[0].isdigit():
                break  # annual block follows
    return pd.DataFrame.from_dict(rows, orient="index", columns=cols)


def aqr_usa(fname, sheet):
    wb = openpyxl.load_workbook(os.path.join(RAW, fname), read_only=True, data_only=True)
    ws = wb[sheet]
    out = {}
    col = None
    for r in ws.iter_rows(values_only=True):
        if col is None:
            if r and r[0] == "DATE":
                names = list(r)
                # the RF sheet has a single unnamed/"Risk Free Rate" column
                col = names.index("USA") if "USA" in names else 1
            continue
        d, v = r[0], r[col]
        if d in (None, "") or v in (None, ""):
            continue
        if isinstance(d, str):
            try:
                d = datetime.datetime.strptime(d.strip(), "%m/%d/%Y")
            except ValueError:
                continue  # footer / disclosure text
        out[d.strftime("%Y-%m")] = float(v)
    return pd.Series(out)


def month_end_prices(ticker):
    r = json.load(open(os.path.join(RAW, f"yahoo_{ticker}_1d.json")))["chart"]["result"][0]
    ts = r["timestamp"]
    close = r["indicators"]["quote"][0]["close"]
    adj = r["indicators"]["adjclose"][0]["adjclose"]
    rows = []
    for t, c, a in zip(ts, close, adj):
        if c is None:
            continue
        d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date()
        rows.append((d, c, a))
    df = pd.DataFrame(rows, columns=["date", "close", "adjclose"])
    df["month"] = df["date"].map(lambda d: d.strftime("%Y-%m"))
    last = df.groupby("month").last()
    last["ndays"] = df.groupby("month").size()
    return last, df


def main():
    ff = french_monthly("F-F_Research_Data_Factors.csv", ["MKT_RF", "SMB", "HML", "RF"])
    mom = french_monthly("F-F_Momentum_Factor.csv", ["UMD"])
    fac = ff.join(mom, how="left")
    bab_f = "Betting-Against-Beta-Equity-Factors-Monthly.xlsx"
    qmj_f = "Quality-Minus-Junk-Factors-Monthly.xlsx"
    fac["BAB"] = aqr_usa(bab_f, "BAB Factors")
    fac["QMJ"] = aqr_usa(qmj_f, "QMJ Factors")
    # AQR's own versions of the standard factors (USA), kept for a robustness check
    for sheet, name in [("MKT", "AQR_MKT_RF"), ("SMB", "AQR_SMB"), ("HML FF", "AQR_HML"),
                        ("HML Devil", "AQR_HML_DEVIL"), ("UMD", "AQR_UMD"), ("RF", "AQR_RF")]:
        fac[name] = aqr_usa(qmj_f, sheet)
    fac.index.name = "month"
    fac = fac[fac.index >= "1957-01"]
    fac.to_csv(os.path.join(OUT, "factors_monthly.csv"), float_format="%.6f")

    a, a_daily = month_end_prices("BRK-A")
    b, _ = month_end_prices("BRK-B")
    brk = pd.DataFrame({"close_A": a["close"], "adjclose_A": a["adjclose"], "ndays_A": a["ndays"],
                        "last_trade_date_A": a["date"]})
    brk["ret_A"] = brk["close_A"].pct_change()
    brk["ret_B"] = b["adjclose"].pct_change()
    brk = brk.join(fac[["RF", "MKT_RF"]], how="left")
    brk["exret_A"] = brk["ret_A"] - brk["RF"]
    brk.index.name = "month"
    # drop the current, incomplete month if factor data do not cover it
    brk.to_csv(os.path.join(OUT, "berkshire_monthly.csv"), float_format="%.6f")
    print(fac.dropna(subset=["BAB", "QMJ"]).index[[0, -1]].tolist(), "BAB/QMJ span")
    print(fac.dropna(subset=["UMD"]).index[-1], "last French month")
    print(brk.head(4)); print(brk.tail(4))
    print("max |close-adjclose|/close for A:", ((brk.close_A - brk.adjclose_A).abs() / brk.close_A).max())
    print("corr(ret_A, ret_B):", brk[["ret_A", "ret_B"]].dropna().corr().iloc[0, 1],
          "mean diff x12:", (brk.ret_A - brk.ret_B).dropna().mean() * 12)
    # staleness check on early daily data
    d80 = a_daily[a_daily.date < datetime.date(1981, 1, 1)]
    print("1980 daily obs:", len(d80), "distinct closes:", d80.close.nunique(),
          "share of zero daily changes:", (d80.close.diff() == 0).mean())
    print(fac.loc["2011-10":"2011-12"]); print(fac.tail(3))
    print(fac[["MKT_RF","AQR_MKT_RF","SMB","AQR_SMB","HML","AQR_HML","UMD","AQR_UMD","RF","AQR_RF"]].loc["1976-11":"2011-12"].corr().round(3).iloc[::2, 1::2])


if __name__ == "__main__":
    main()
