"""Shared helpers for the Buffett's Alpha replication."""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RES = os.path.join(HERE, "results")

PAPER_START = "1980-04"   # first monthly return available from Yahoo (paper: 1976-11)
PAPER_END = "2011-12"


def load(aqr_std=False):
    """Monthly panel: Berkshire excess return + factors.

    aqr_std=True swaps in AQR's own MKT/SMB/HML/UMD (and RF) instead of Ken French's.
    """
    fac = pd.read_csv(os.path.join(DATA, "factors_monthly.csv"), index_col=0)
    brk = pd.read_csv(os.path.join(DATA, "berkshire_monthly.csv"), index_col=0)
    df = fac.copy()
    df["ret"] = brk["ret_A"]
    df["close"] = brk["close_A"]
    if aqr_std:
        for k in ["MKT_RF", "SMB", "HML", "UMD", "RF"]:
            df[k] = df["AQR_" + k]
    df["ex"] = df["ret"] - df["RF"]
    df["MKT"] = df["MKT_RF"]
    return df


def ols(y, X):
    return sm.OLS(y, sm.add_constant(X), missing="drop").fit()


def perf(ex, mkt):
    """Table 2 style statistics from monthly excess returns."""
    d = pd.concat([ex, mkt], axis=1).dropna()
    y, m = d.iloc[:, 0], d.iloc[:, 1]
    r = ols(y, m)
    resid_vol = r.resid.std(ddof=2) * np.sqrt(12)
    return dict(n_months=len(y), first=y.index[0], last=y.index[-1],
                avg_excess=y.mean() * 12, vol=y.std() * np.sqrt(12),
                sharpe=y.mean() / y.std() * np.sqrt(12), beta=r.params.iloc[1],
                capm_alpha=r.params.iloc[0] * 12, alpha_t=r.tvalues.iloc[0],
                idio_vol=resid_vol, info_ratio=r.params.iloc[0] * 12 / resid_vol,
                mkt_avg_excess=m.mean() * 12, mkt_vol=m.std() * np.sqrt(12),
                mkt_sharpe=m.mean() / m.std() * np.sqrt(12))


def reg_row(df, ycol, xcols, label):
    d = df[[ycol] + xcols].dropna()
    r = ols(d[ycol], d[xcols])
    row = dict(spec=label, n=len(d), first=d.index[0], last=d.index[-1],
               alpha_ann=r.params["const"] * 12, alpha_t=r.tvalues["const"], adj_r2=r.rsquared_adj)
    for k in xcols:
        row[k] = r.params[k]
        row[k + "_t"] = r.tvalues[k]
    return row, r
