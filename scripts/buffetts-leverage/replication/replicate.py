"""Replication of Frazzini, Kabiller, Pedersen, "Buffett's Alpha" (NBER WP 19681)
with free data. Run:  python -I replicate.py
Writes CSVs into results/ and prints the same numbers.
Methods are fixed here before looking at results; nothing is tuned to match the paper.
"""
import os
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # needed under python -I
from common import *

pd.set_option("display.width", 250, "display.max_columns", 40, "display.float_format", lambda v: f"{v:.4f}")
F4 = ["MKT", "SMB", "HML", "UMD"]
SPECS = [("MKT", ["MKT"]), ("FF4", F4), ("FF4+BAB", F4 + ["BAB"]), ("FF4+BAB+QMJ", F4 + ["BAB", "QMJ"])]


def section(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


# ---------------------------------------------------------------- 1. Table 2 / Section 3
def item1(df):
    section("1. Table 2 Berkshire column / Section 3")
    last = df["ex"].dropna().index[-1]
    rows = []
    for name, a, b in [("paper window (monthly data available)", PAPER_START, PAPER_END),
                       ("1981-2011", "1981-01", PAPER_END),
                       ("post-paper", "2012-01", last), ("full", PAPER_START, last)]:
        s = df.loc[a:b]
        rows.append(dict(sample=name, **perf(s["ex"], s["MKT"])))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RES, "table2_berkshire_monthly.csv"), index=False)
    print(out.T)

    # sub-periods (paper's buckets, then post-paper)
    rows = []
    for a, b in [("1980-04", "1980-12"), ("1981-01", "1985-12"), ("1986-01", "1990-12"), ("1991-01", "1995-12"),
                 ("1996-01", "2000-12"), ("2001-01", "2005-12"), ("2006-01", "2011-12"),
                 ("2012-01", "2016-12"), ("2017-01", "2021-12"), ("2022-01", last)]:
        s = df.loc[a:b].dropna(subset=["ex"])
        rows.append(dict(period=f"{a}..{b}", n=len(s), brk_excess=s["ex"].mean() * 12, mkt_excess=s["MKT"].mean() * 12))
    sp = pd.DataFrame(rows)
    sp["paper_brk"] = [np.nan, .286, .173, .297, .149, .032, .033, np.nan, np.nan, np.nan]
    sp["paper_mkt"] = [np.nan, .043, .054, .120, .118, .016, .007, np.nan, np.nan, np.nan]
    sp.to_csv(os.path.join(RES, "table2_subperiods.csv"), index=False)
    print(sp)

    # drawdown June 30 1998 -> Feb 29 2000
    p0, p1 = df.loc["1998-06", "close"], df.loc["2000-02", "close"]
    w = df.loc["1998-07":"2000-02"]
    mk = (1 + w["MKT_RF"] + w["RF"]).prod() - 1
    dd = dict(brk_close_1998_06=p0, brk_close_2000_02=p1, brk_return=p1 / p0 - 1, mkt_total_return=mk,
              shortfall=(p1 / p0 - 1) - mk, paper_brk=-0.44, paper_mkt=0.32, paper_shortfall=-0.76)
    pd.DataFrame([dd]).to_csv(os.path.join(RES, "drawdown_1998_2000.csv"), index=False)
    print(dd)

    # annual version from the shareholder letters (covers 1976-1979, which Yahoo does not)
    ann = pd.read_csv(os.path.join(DATA, "berkshire_annual_letter.csv"), index_col=0) / 100
    fac = pd.read_csv(os.path.join(DATA, "factors_monthly.csv"), index_col=0)
    fac["year"] = fac.index.str[:4].astype(int)
    g = fac.groupby("year")
    ann["rf"] = g["RF"].apply(lambda x: (1 + x).prod() - 1)
    ann["mkt"] = g.apply(lambda x: (1 + x["MKT_RF"] + x["RF"]).prod() - 1)
    ann["nmo"] = g.size()
    ann = ann[ann.nmo == 12]
    ann["ex"] = ann["brk_pct"] - ann["rf"]
    ann["mex"] = ann["mkt"] - ann["rf"]
    # cross-check: Yahoo calendar-year returns vs the letter table
    ye = df["close"].dropna()
    ye = ye[ye.index.str[5:] == "12"]
    ye.index = ye.index.str[:4].astype(int)
    ann["yahoo_brk"] = ye.pct_change()
    chk = ann.dropna(subset=["yahoo_brk"])
    print("Yahoo vs letter calendar-year return, max abs diff (pct pts):",
          ((chk.yahoo_brk - chk.brk_pct).abs() * 100).max().round(2),
          "years with diff > 1pt:", chk.index[((chk.yahoo_brk - chk.brk_pct).abs() > 0.01)].tolist())
    ann.to_csv(os.path.join(RES, "berkshire_annual.csv"))
    rows = []
    for a, b in [(1976, 2011), (1977, 2011), (1981, 2011), (1977, 1980), (1976, 1980), (2012, 2025), (1977, 2025)]:
        s = ann.loc[a:b]
        r = ols(s["ex"], s["mex"])
        iv = r.resid.std(ddof=2)
        rows.append(dict(sample=f"{a}-{b}", n_years=len(s), avg_excess=s.ex.mean(), vol=s.ex.std(),
                         sharpe=s.ex.mean() / s.ex.std(), beta=r.params.iloc[1], capm_alpha=r.params.iloc[0],
                         info_ratio=r.params.iloc[0] / iv, geo_brk=(1 + s.brk_pct).prod() ** (1 / len(s)) - 1,
                         mkt_avg_excess=s.mex.mean(), mkt_vol=s.mex.std(), mkt_sharpe=s.mex.mean() / s.mex.std(),
                         growth_of_1=(1 + s.brk_pct).prod()))
    a_out = pd.DataFrame(rows)
    a_out.to_csv(os.path.join(RES, "table2_berkshire_annual.csv"), index=False)
    print(a_out.T)


# ---------------------------------------------------------------- 2. Table 4
PAPER_T4 = {  # Berkshire stock 1976-2011, columns 1-3 of Table 4 (4-factor, +BAB, +QMJ)
    "FF4": dict(alpha_ann=.121, alpha_t=3.19, MKT=.84, MKT_t=11.65, SMB=-.32, SMB_t=-3.05, HML=.63, HML_t=5.35,
                UMD=.06, UMD_t=.90, adj_r2=.25),
    "FF4+BAB": dict(alpha_ann=.092, alpha_t=2.42, MKT=.83, MKT_t=11.70, SMB=-.32, SMB_t=-3.13, HML=.38, HML_t=2.79,
                    UMD=-.03, UMD_t=-.40, BAB=.37, BAB_t=3.61, adj_r2=.27),
    "FF4+BAB+QMJ": dict(alpha_ann=.063, alpha_t=1.58, MKT=.95, MKT_t=10.98, SMB=-.15, SMB_t=-1.15, HML=.46, HML_t=3.28,
                        UMD=-.05, UMD_t=-.71, BAB=.29, BAB_t=2.67, QMJ=.43, QMJ_t=2.34, adj_r2=.28),
}


def item2(df, tag=""):
    section("2. Table 4 Berkshire stock regressions " + tag)
    last = df[["ex", "BAB", "QMJ"]].dropna().index[-1]
    rows = []
    for wname, a, b in [("paper window 1980-04..2011-12", PAPER_START, PAPER_END),
                        ("post-paper 2012-01..latest", "2012-01", last),
                        ("full 1980-04..latest", PAPER_START, last),
                        ("first half 1980-04..1995-12", PAPER_START, "1995-12"),
                        ("second half 1996-01..2011-12", "1996-01", PAPER_END)]:
        # same sample for all four specs: require BAB and QMJ to be present
        s = df.loc[a:b].dropna(subset=["ex", "BAB", "QMJ"] + F4)
        for label, xs in SPECS:
            row, _ = reg_row(s, "ex", xs, label)
            rows.append(dict(window=wname, **row))
    for label, p in PAPER_T4.items():
        rows.append(dict(window="PAPER 1976-11..2011-12", spec=label, **p))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(RES, f"table4_berkshire{tag}.csv"), index=False)
    cols = ["window", "spec", "n", "alpha_ann", "alpha_t", "MKT", "MKT_t", "SMB", "SMB_t", "HML", "HML_t", "UMD", "UMD_t",
            "BAB", "BAB_t", "QMJ", "QMJ_t", "adj_r2"]
    print(out[cols].to_string())
    return out


# ---------------------------------------------------------------- 3. Section 7 / Table 5 / Appendix C
SIX = F4 + ["BAB", "QMJ"]


def style_insample(s):
    """Section 7 construction on sample s. Returns (excess return series, info dict)."""
    uni = ols(s["ex"], s[["MKT"]])
    beta = uni.params["MKT"]
    sig_i = uni.resid.std(ddof=2)
    six = ols(s["ex"], s[SIX])
    coef = six.params[SIX].copy()
    coef["MKT"] -= beta
    rA = s[SIX] @ coef
    k = sig_i / rA.std()
    style = beta * s["MKT"] + k * rA
    info = dict(beta_buffett=beta, target_idio_vol_ann=sig_i * np.sqrt(12), scale_k=k, **{"w_" + c: coef[c] * k for c in SIX},
                gross_factor_notional=float(np.abs(coef * k).sum() + abs(beta)))
    return style, info


def two_way(a, b, la, lb):
    """Table 5: regress a on b and b on a (monthly excess returns)."""
    d = pd.concat([a, b], axis=1).dropna()
    d.columns = ["a", "b"]
    r1, r2 = ols(d["a"], d[["b"]]), ols(d["b"], d[["a"]])
    return dict(n=len(d), first=d.index[0], last=d.index[-1], corr=d.corr().iloc[0, 1],
                **{f"{la}_on_{lb}_alpha": r1.params["const"] * 12, f"{la}_on_{lb}_alpha_t": r1.tvalues["const"],
                   f"{la}_on_{lb}_loading": r1.params["b"], f"{la}_on_{lb}_loading_t": r1.tvalues["b"],
                   f"{lb}_on_{la}_alpha": r2.params["const"] * 12, f"{lb}_on_{la}_alpha_t": r2.tvalues["const"],
                   f"{lb}_on_{la}_loading": r2.params["a"], f"{lb}_on_{la}_loading_t": r2.tvalues["a"],
                   "adj_r2": r1.rsquared_adj})


def style_oos(df, min_obs=60):
    """Appendix C: for month t+1 use coefficients, beta and vol scale estimated on data through month t."""
    s = df.dropna(subset=["ex"] + SIX)
    out = {}
    for i in range(min_obs, len(s)):
        h = s.iloc[:i]
        uni = ols(h["ex"], h[["MKT"]])
        beta = uni.params["MKT"]
        coef = ols(h["ex"], h[SIX]).params[SIX].copy()
        coef["MKT"] -= beta
        k = uni.resid.std(ddof=2) / (h[SIX] @ coef).std()
        nxt = s.iloc[i]
        out[s.index[i]] = beta * nxt["MKT"] + k * float(nxt[SIX] @ coef)
    return pd.Series(out)


def item3(df):
    section("3. Systematic Buffett-style portfolio (Section 7, Tables 2 and 5, Appendix C)")
    last = df[["ex"] + SIX].dropna().index[-1]
    base = df.dropna(subset=["ex"] + SIX)
    perf_rows, t5_rows, series = [], [], pd.DataFrame(index=base.index)
    series["berkshire_ex"] = base["ex"]

    def add(name, st, bk_sample, extra=None):
        p = perf(st, base.loc[st.index, "MKT"])
        pb = perf(bk_sample.loc[st.index, "ex"], base.loc[st.index, "MKT"])
        perf_rows.append(dict(portfolio=name, **p, brk_avg_excess_same_sample=pb["avg_excess"],
                              brk_sharpe_same_sample=pb["sharpe"], **(extra or {})))
        t5_rows.append(dict(portfolio=name, **two_way(bk_sample.loc[st.index, "ex"], st, "brk", "style")))
        series[name] = st

    # (a) in-sample, paper window
    s = base.loc[PAPER_START:PAPER_END]
    st, info = style_insample(s)
    add("in-sample 1980-04..2011-12", st, base, info)
    # (b) in-sample, full window
    s2 = base.loc[PAPER_START:last]
    st2, info2 = style_insample(s2)
    add("in-sample 1980-04..latest", st2, base, info2)
    # (c) coefficients and scale frozen at the 2011 estimate, applied to 2012 onward
    uni = ols(s["ex"], s[["MKT"]]); beta = uni.params["MKT"]
    coef = ols(s["ex"], s[SIX]).params[SIX].copy(); coef["MKT"] -= beta
    k = uni.resid.std(ddof=2) / (s[SIX] @ coef).std()
    post = base.loc["2012-01":last]
    st3 = beta * post["MKT"] + k * (post[SIX] @ coef)
    add("frozen 2011 weights, 2012-01..latest", st3, base)
    # (d) Appendix C expanding window
    oos = style_oos(base.loc[PAPER_START:last])
    add("Appendix C expanding, to 2011-12", oos.loc[:PAPER_END], base)
    add("Appendix C expanding, 2012-01..latest", oos.loc["2012-01":], base)
    add("Appendix C expanding, all", oos, base)

    pr, t5 = pd.DataFrame(perf_rows), pd.DataFrame(t5_rows)
    pr.to_csv(os.path.join(RES, "buffett_style_performance.csv"), index=False)
    t5.to_csv(os.path.join(RES, "table5_two_way.csv"), index=False)
    series.to_csv(os.path.join(RES, "buffett_style_series.csv"), float_format="%.6f")
    print(pr.T); print(t5.T)

    # sub-period returns of the in-sample style portfolio next to the paper's Table 2 column
    rows = []
    for (a, b), pp in zip([("1981-01", "1985-12"), ("1986-01", "1990-12"), ("1991-01", "1995-12"), ("1996-01", "2000-12"),
                           ("2001-01", "2005-12"), ("2006-01", "2011-12")], [.548, .237, .385, .332, .330, .047]):
        rows.append(dict(period=f"{a}..{b}", style_excess=st.loc[a:b].mean() * 12, brk_excess=base.loc[a:b, "ex"].mean() * 12,
                         paper_style=pp))
    sp = pd.DataFrame(rows); sp.to_csv(os.path.join(RES, "buffett_style_subperiods.csv"), index=False); print(sp)


# ---------------------------------------------------------------- 6. has anything changed after 2011?
def item6(df):
    section("6. Stability: post-2011 dummy interactions and rolling statistics")
    s = df.loc[PAPER_START:].dropna(subset=["ex"] + SIX).copy()
    s["POST"] = (s.index >= "2012-01").astype(float)
    rows = []
    for label, xs in SPECS:
        X = s[xs].copy()
        X["POST"] = s["POST"]
        for x in xs:
            X[x + "_xPOST"] = s[x] * s["POST"]
        r = ols(s["ex"], X)
        row = dict(spec=label, n=len(s), alpha_pre_ann=r.params["const"] * 12, alpha_change_ann=r.params["POST"] * 12,
                   alpha_change_t=r.tvalues["POST"])
        for x in xs:
            row[x + "_change"] = r.params[x + "_xPOST"]; row[x + "_change_t"] = r.tvalues[x + "_xPOST"]
        ft = r.f_test(" , ".join([f"{c} = 0" for c in X.columns if "POST" in c]))
        row["joint_F_p"] = float(ft.pvalue)
        rows.append(row)
    out = pd.DataFrame(rows); out.to_csv(os.path.join(RES, "stability_post2011.csv"), index=False); print(out.T)

    # rolling 10-year Sharpe, beta, 6-factor alpha, sampled each December
    rows = []
    idx = s.index
    for i in range(120, len(idx) + 1):
        if idx[i - 1][5:] != "12" and i != len(idx):
            continue
        w = s.iloc[i - 120:i]
        r6 = ols(w["ex"], w[SIX]); r1 = ols(w["ex"], w[["MKT"]])
        rows.append(dict(window_end=idx[i - 1], sharpe=w.ex.mean() / w.ex.std() * np.sqrt(12),
                         mkt_sharpe=w.MKT.mean() / w.MKT.std() * np.sqrt(12), beta=r1.params["MKT"],
                         capm_alpha=r1.params["const"] * 12, six_alpha=r6.params["const"] * 12,
                         six_alpha_t=r6.tvalues["const"], vol=w.ex.std() * np.sqrt(12),
                         **{c: r6.params[c] for c in SIX}))
    ro = pd.DataFrame(rows); ro.to_csv(os.path.join(RES, "rolling_10y.csv"), index=False); print(ro.to_string())

    # factor premia themselves, before and after
    rows = []
    for a, b in [(PAPER_START, PAPER_END), ("2012-01", idx[-1])]:
        w = s.loc[a:b]
        rows.append(dict(window=f"{a}..{b}", **{c + "_mean_ann": w[c].mean() * 12 for c in SIX},
                         **{c + "_sharpe": w[c].mean() / w[c].std() * np.sqrt(12) for c in SIX}))
    fp = pd.DataFrame(rows); fp.to_csv(os.path.join(RES, "factor_premia.csv"), index=False); print(fp.T)


if __name__ == "__main__":
    df = load()
    item1(df)
    item2(df)
    item2(load(aqr_std=True), tag="_aqr_standard_factors")
    item3(df)
    item6(df)
