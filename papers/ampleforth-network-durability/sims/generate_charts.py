#!/usr/bin/env python3
"""
Generate charts for the Ampleforth Network Durability paper.
Fetches AMPL rebase history and produces PDF figures.

BTC/ETH comparison charts require a CoinGecko API key:
  COINGECKO_API_KEY=... python generate_charts.py
"""

import os
import json
import requests

import pandas as pd
import numpy as np
import scipy.stats as stats

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["font.family"] = "STIXGeneral"
matplotlib.rcParams["figure.dpi"] = 300

FIGURES_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

DAY_SECONDS = 24 * 3600
DAY_MSECONDS = 1000 * DAY_SECONDS
START_DATE_MS = 1576368000000  # Dec 15 2019
END_DATE_S = 1635724800       # Nov 1 2021 (Oct 2021 cutoff)


def save(fig, name):
    fig.savefig(os.path.join(FIGURES_DIR, name), bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {name}")


# ---------------------------------------------------------------------------
# 1. Fetch AMPL rebase history
# ---------------------------------------------------------------------------
print("Fetching AMPL rebase history...")
resp = requests.get("https://web-api.ampleforth.org/eth/token-rebase-history")
resp.raise_for_status()
ampl_history = json.loads(resp.content)

ampl_df = pd.DataFrame(
    ampl_history, columns=["epoch", "price", "price_target", "supply", "time"]
)
ampl_df = ampl_df[(ampl_df["time"] >= START_DATE_MS / 1000) & (ampl_df["time"] < END_DATE_S)]
ampl_df["time"] = ampl_df["time"] - (ampl_df["time"] % DAY_SECONDS)
ampl_df["time"] = pd.to_datetime(ampl_df["time"], unit="s")
ampl_df = ampl_df.set_index("time")
ampl_df["marketcap"] = ampl_df["price"] * ampl_df["supply"]
print(f"  {len(ampl_df)} AMPL data points")

# ---------------------------------------------------------------------------
# 2. Optionally fetch BTC/ETH prices from CoinGecko (requires API key)
# ---------------------------------------------------------------------------
cg_api_key = os.environ.get("COINGECKO_API_KEY", "")
df_combined = None

if cg_api_key:
    print("Fetching BTC/ETH prices from CoinGecko (Pro API)...")
    headers = {"x-cg-pro-api-key": cg_api_key}
    base_url = "https://pro-api.coingecko.com/api/v3"

    dfs = []
    for token in ["bitcoin", "ethereum"]:
        url = f"{base_url}/coins/{token}/market_chart?vs_currency=usd&days=max"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        prices = r.json()["prices"]
        p = np.array(prices)
        df = pd.DataFrame({"time": p[:, 0], f"{token}_price": p[:, 1]})
        df["time"] = df["time"] - (df["time"] % DAY_MSECONDS)
        dfs.append(df[df.time >= START_DATE_MS])

    df_combined = pd.DataFrame(dfs[0]["time"])
    for df in dfs:
        df_combined = df_combined.join(df.set_index("time"), on="time")
    df_combined["time"] = pd.to_datetime(df_combined["time"], unit="ms")
    df_combined = df_combined.set_index("time")

    ampl_prices = ampl_df[["marketcap", "price", "supply"]].rename(
        columns={"marketcap": "ampl_mc", "price": "ampl_price", "supply": "ampl_supply"}
    )
    df_combined = ampl_prices.join(df_combined, on="time").dropna()
    print(f"  {len(df_combined)} combined data points")
else:
    print("No COINGECKO_API_KEY set — skipping BTC/ETH comparison charts.")
    # Build df_combined from AMPL data only (for log distribution charts)
    df_combined = ampl_df[["marketcap", "price", "supply"]].rename(
        columns={"marketcap": "ampl_mc", "price": "ampl_price", "supply": "ampl_supply"}
    )

# ---------------------------------------------------------------------------
# Chart 1: Price over time with thresholds
# ---------------------------------------------------------------------------
print("Generating charts...")

fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.set_ylabel("Price (USD)")
ax1.plot(ampl_df.index, ampl_df["price"], color="black", label="price")
ax1.plot(
    ampl_df.index, ampl_df["price_target"] * 1.05,
    color="grey", linestyle="dotted", label="upper threshold",
)
ax1.plot(
    ampl_df.index, ampl_df["price_target"] * 0.95,
    color="grey", linestyle="dotted", label="lower threshold",
)
ax1.tick_params(axis="y")
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%1.2f"))
ax1.legend(loc="upper left")
save(fig, "price_over_time.pdf")

# ---------------------------------------------------------------------------
# Chart 2: Price + Supply overlay
# ---------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.set_ylabel("Price (USD)")
ax1.plot(ampl_df.index, ampl_df["price"], color="#FF2D55", label="price")
ax1.plot(
    ampl_df.index, ampl_df["price_target"] * 1.05,
    color="grey", linestyle="dotted", label="upper threshold",
)
ax1.plot(
    ampl_df.index, ampl_df["price_target"] * 0.95,
    color="grey", linestyle="dotted", label="lower threshold",
)
ax1.tick_params(axis="y")
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%1.2f"))

ax2 = ax1.twinx()
ax2.set_ylabel("#Stock (Millions)")
ax2.plot(ampl_df.index, ampl_df["supply"], color="#5ac8fa", label="stock")
ax2.tick_params(axis="y")
ax2.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: "%1.0fM" % (x * 1e-6))
)
ax1.legend(loc="upper left")
ax2.legend()
save(fig, "price_supply_overlay.pdf")

# ---------------------------------------------------------------------------
# Chart 3: Price deviation distribution
# ---------------------------------------------------------------------------
dt_price = (ampl_df["price"] - ampl_df["price_target"]) / ampl_df["price_target"]

N_BINS = 40
fig = plt.figure(figsize=(7, 2.5))
N = len(dt_price)
x = np.linspace(dt_price.min(), dt_price.max(), N)

ax = fig.add_subplot(1, 1, 1)
ax.hist(dt_price, bins=N_BINS, range=(-1, 1.5), color="#bbb", label="Price Deviation")
ax.set_xlabel("Distribution of AMPL Price Deviation from Target")
ax.set_ylabel("Days")

binwidth = 10 / N_BINS
scale_factor = N * binwidth
ax.plot(
    x, stats.norm.pdf((x - dt_price.mean()) / dt_price.std()) * scale_factor,
    color="black", linewidth=2, label="Normal",
)
plt.axvline(0, color="black", linestyle="dashed", linewidth=1)
ax.legend()
save(fig, "price_deviation_dist.pdf")

# ---------------------------------------------------------------------------
# Chart 4: Daily supply change distribution
# ---------------------------------------------------------------------------
dt_supply = ampl_df["supply"].pct_change(periods=1).fillna(0)

N_BINS = 20
fig = plt.figure(figsize=(7, 4))
N = len(dt_supply)
x = np.linspace(dt_supply.min(), dt_supply.max(), N)

ax = fig.add_subplot(1, 1, 1)
ax.hist(
    dt_supply, bins=N_BINS, range=(dt_supply.min(), dt_supply.max()),
    color="#007AFF", label="stock deviation",
)
ax.set_xlabel("Supply change %")
ax.set_ylabel("#days")

binwidth = 10 / N_BINS
scale_factor = N * binwidth
ax.plot(
    x, stats.norm.pdf((x - dt_supply.mean()) / dt_supply.std()) * scale_factor,
    color="black", linewidth=2, label="fit",
)
plt.axvline(dt_supply.mean(), color="black", linestyle="dashed", linewidth=1)
ax.legend()
save(fig, "supply_change_dist.pdf")

# ---------------------------------------------------------------------------
# Chart 5: Rolling monthly log supply changes distribution
# ---------------------------------------------------------------------------
dt_log_supply = np.log(
    df_combined["ampl_supply"] / df_combined["ampl_supply"].shift(30)
).iloc[30:]

N_BINS = 50
fig = plt.figure(figsize=(7, 4))
N = len(dt_log_supply)
x = np.linspace(dt_log_supply.min(), dt_log_supply.max(), N)

ax = fig.add_subplot(1, 1, 1)
ax.hist(
    dt_log_supply, bins=N_BINS,
    range=(dt_log_supply.min(), dt_log_supply.max()),
    color="#007AFF", label="log supply change",
)
ax.set_xlabel("Log of rolling monthly supply changes")
ax.set_ylabel("#days")

binwidth = 10 / N_BINS
scale_factor = N * binwidth
ax.plot(
    x, stats.norm.pdf((x - dt_log_supply.mean()) / dt_log_supply.std()) * scale_factor,
    color="black", linewidth=2, label="fit",
)
plt.axvline(dt_log_supply.mean(), color="black", linestyle="dashed", linewidth=1)
ax.legend()
save(fig, "log_supply_change_dist.pdf")

# ---------------------------------------------------------------------------
# Charts 6-9: Volatility comparisons (only if BTC/ETH data available)
# ---------------------------------------------------------------------------
if cg_api_key and "bitcoin_price" in df_combined.columns:
    vol_cols = ["ampl_mc", "bitcoin_price", "ethereum_price", "ampl_price", "ampl_supply"]
    daily_vol = df_combined[vol_cols].pct_change(periods=1).iloc[1:, :].abs()

    # Chart 6: Daily vol - AMPL price vs supply
    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Daily volatility")
    ax1.plot(daily_vol.index, daily_vol["ampl_price"], label="ampl price", color="#FF2D55")
    ax1.plot(daily_vol.index, daily_vol["ampl_supply"], label="ampl supply", color="#007AFF")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "daily_vol_ampl.pdf")

    # Chart 7: Daily vol - AMPL mc vs BTC vs ETH
    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Daily volatility")
    ax1.plot(daily_vol.index, daily_vol["ampl_mc"], label="ampl market cap", color="#FF2D55")
    ax1.plot(daily_vol.index, daily_vol["bitcoin_price"], label="bitcoin price", color="#ffbb11")
    ax1.plot(daily_vol.index, daily_vol["ethereum_price"], label="ethereum price", color="#3c3c3d")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "daily_vol_comparison.pdf")

    # Chart 8: Monthly vol - AMPL price vs supply
    monthly_vol = df_combined[vol_cols].pct_change(periods=30).iloc[30:, :].abs()

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Monthly volatility")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_price"], label="ampl price", color="#FF2D55")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_supply"], label="ampl supply", color="#007AFF")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "monthly_vol_ampl.pdf")

    # Chart 9: Monthly vol - AMPL mc vs BTC vs ETH
    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Monthly volatility")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_mc"], label="ampl market cap", color="#FF2D55")
    ax1.plot(monthly_vol.index, monthly_vol["bitcoin_price"], label="bitcoin price", color="#ffbb11")
    ax1.plot(monthly_vol.index, monthly_vol["ethereum_price"], label="ethereum price", color="#3c3c3d")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "monthly_vol_comparison.pdf")
else:
    # Generate AMPL-only volatility charts
    ampl_only = df_combined[["ampl_mc", "ampl_price", "ampl_supply"]]
    daily_vol = ampl_only.pct_change(periods=1).iloc[1:, :].abs()

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Daily volatility")
    ax1.plot(daily_vol.index, daily_vol["ampl_price"], label="ampl price", color="#FF2D55")
    ax1.plot(daily_vol.index, daily_vol["ampl_supply"], label="ampl supply", color="#007AFF")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "daily_vol_ampl.pdf")

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Daily volatility")
    ax1.plot(daily_vol.index, daily_vol["ampl_mc"], label="ampl market cap", color="#FF2D55")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "daily_vol_comparison.pdf")

    monthly_vol = ampl_only.pct_change(periods=30).iloc[30:, :].abs()

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Monthly volatility")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_price"], label="ampl price", color="#FF2D55")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_supply"], label="ampl supply", color="#007AFF")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "monthly_vol_ampl.pdf")

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.set_ylabel("Monthly volatility")
    ax1.plot(monthly_vol.index, monthly_vol["ampl_mc"], label="ampl market cap", color="#FF2D55")
    ax1.tick_params(axis="y")
    ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("%1.2f"))
    ax1.legend()
    save(fig, "monthly_vol_comparison.pdf")

# ---------------------------------------------------------------------------
# Chart 10: Max negative rebase by period
# ---------------------------------------------------------------------------
periods = range(1, 84)
max_neg = list(
    map(lambda x: ampl_df["supply"].pct_change(periods=x).min() * 100, periods)
)

fig, ax1 = plt.subplots(figsize=(6, 2))
ax1.set_ylabel("Max -ve supply change")
ax1.set_xlabel("Period (days)")
ax1.plot(periods, max_neg, label="-ve rebase %", color="#3c3c3d")
ax1.tick_params(axis="y")
ax1.yaxis.set_major_formatter(ticker.PercentFormatter())
ax1.legend()
save(fig, "max_neg_rebase.pdf")

# ---------------------------------------------------------------------------
# Print summary statistics
# ---------------------------------------------------------------------------
print("\n--- Price Deviation Stats ---")
dt = (ampl_df["price"] - ampl_df["price_target"]) / ampl_df["price_target"]
total = len(dt)
print(f"  Mean: {dt.mean():.4f}")
print(f"  Std:  {dt.std():.4f}")
print(f"  Within +-5%:  {len(dt[(dt >= -0.05) & (dt <= 0.05)]) / total:.2%}")
print(f"  Within +-10%: {len(dt[(dt >= -0.10) & (dt <= 0.10)]) / total:.2%}")
print(f"  Within +-20%: {len(dt[(dt >= -0.20) & (dt <= 0.20)]) / total:.2%}")

print("\n--- Supply Change Stats ---")
dt2 = ampl_df["supply"].pct_change(periods=1).fillna(0)
print(f"  Mean: {dt2.mean():.6f}")
print(f"  Std:  {dt2.std():.6f}")
print(f"  Days supply increased: {len(dt2[dt2 > 0]) / total:.2%}")
print(f"  Days supply decreased: {len(dt2[dt2 < 0]) / total:.2%}")

# ===========================================================================
# APPENDIX: Full-period analysis (Dec 2019 - present)
# ===========================================================================
print("\n=== Generating appendix charts (full period) ===")

ampl_full = pd.DataFrame(
    ampl_history, columns=["epoch", "price", "price_target", "supply", "time"]
)
ampl_full = ampl_full[(ampl_full["time"] >= START_DATE_MS / 1000) & (ampl_full["price_target"] > 0)]
ampl_full["time"] = ampl_full["time"] - (ampl_full["time"] % DAY_SECONDS)
ampl_full["time"] = pd.to_datetime(ampl_full["time"], unit="s")
ampl_full = ampl_full.set_index("time")
ampl_full["marketcap"] = ampl_full["price"] * ampl_full["supply"]
print(f"  {len(ampl_full)} full-period AMPL data points")

# Appendix Chart 1: Price deviation distribution (full period)
dt_full = (ampl_full["price"] - ampl_full["price_target"]) / ampl_full["price_target"]

N_BINS = 40
fig = plt.figure(figsize=(7, 2.5))
N = len(dt_full)
x = np.linspace(dt_full.min(), dt_full.max(), N)

ax = fig.add_subplot(1, 1, 1)
ax.hist(dt_full, bins=N_BINS, range=(-1, 1.5), color="#bbb", label="Price Deviation")
ax.set_xlabel("Distribution of AMPL Price Deviation from Target")
ax.set_ylabel("Days")

binwidth = 10 / N_BINS
scale_factor = N * binwidth
ax.plot(
    x, stats.norm.pdf((x - dt_full.mean()) / dt_full.std()) * scale_factor,
    color="black", linewidth=2, label="Normal",
)
plt.axvline(0, color="black", linestyle="dashed", linewidth=1)
ax.legend()
save(fig, "appendix_price_deviation_dist.pdf")

# Appendix Chart 2: Price + Supply overlay (full period)
fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.set_ylabel("Price (USD)")
ax1.plot(ampl_full.index, ampl_full["price"], color="#FF2D55", label="price")
ax1.plot(
    ampl_full.index, ampl_full["price_target"] * 1.05,
    color="grey", linestyle="dotted", label="upper threshold",
)
ax1.plot(
    ampl_full.index, ampl_full["price_target"] * 0.95,
    color="grey", linestyle="dotted", label="lower threshold",
)
ax1.tick_params(axis="y")
ax1.yaxis.set_major_formatter(ticker.FormatStrFormatter("$%1.2f"))

ax2 = ax1.twinx()
ax2.set_ylabel("#Stock (Millions)")
ax2.plot(ampl_full.index, ampl_full["supply"], color="#5ac8fa", label="stock")
ax2.tick_params(axis="y")
ax2.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: "%1.0fM" % (x * 1e-6))
)
ax1.legend(loc="upper left")
ax2.legend()
save(fig, "appendix_price_supply_overlay.pdf")

# Appendix Chart 3: Rolling monthly log supply changes (full period)
df_full_combined = ampl_full[["marketcap", "price", "supply"]].rename(
    columns={"marketcap": "ampl_mc", "price": "ampl_price", "supply": "ampl_supply"}
)
dt_log_full = np.log(
    df_full_combined["ampl_supply"] / df_full_combined["ampl_supply"].shift(30)
).iloc[30:]

N_BINS = 50
fig = plt.figure(figsize=(7, 4))
N = len(dt_log_full)
x = np.linspace(dt_log_full.min(), dt_log_full.max(), N)

ax = fig.add_subplot(1, 1, 1)
ax.hist(
    dt_log_full, bins=N_BINS,
    range=(dt_log_full.min(), dt_log_full.max()),
    color="#007AFF", label="log supply change",
)
ax.set_xlabel("Log of rolling monthly supply changes")
ax.set_ylabel("#days")

binwidth = 10 / N_BINS
scale_factor = N * binwidth
ax.plot(
    x, stats.norm.pdf((x - dt_log_full.mean()) / dt_log_full.std()) * scale_factor,
    color="black", linewidth=2, label="fit",
)
plt.axvline(dt_log_full.mean(), color="black", linestyle="dashed", linewidth=1)
ax.legend()
save(fig, "appendix_log_supply_change_dist.pdf")

# Full-period statistics
print("\n--- Full Period Price Deviation Stats ---")
total_full = len(dt_full)
print(f"  Data points: {total_full}")
print(f"  Date range: {ampl_full.index.min().date()} to {ampl_full.index.max().date()}")
print(f"  Mean: {dt_full.mean():.4f}")
print(f"  Std:  {dt_full.std():.4f}")
print(f"  Within +-5%:  {len(dt_full[(dt_full >= -0.05) & (dt_full <= 0.05)]) / total_full:.2%}")
print(f"  Within +-10%: {len(dt_full[(dt_full >= -0.10) & (dt_full <= 0.10)]) / total_full:.2%}")
print(f"  Within +-20%: {len(dt_full[(dt_full >= -0.20) & (dt_full <= 0.20)]) / total_full:.2%}")

print("\n--- Full Period Supply Change Stats ---")
dt2_full = ampl_full["supply"].pct_change(periods=1).fillna(0)
print(f"  Mean: {dt2_full.mean():.6f}")
print(f"  Std:  {dt2_full.std():.6f}")
print(f"  Days supply increased: {len(dt2_full[dt2_full > 0]) / total_full:.2%}")
print(f"  Days supply decreased: {len(dt2_full[dt2_full < 0]) / total_full:.2%}")
print(f"  Days no change:        {len(dt2_full[dt2_full == 0]) / total_full:.2%}")

# Market cap extremes
mc = ampl_full["marketcap"]
print(f"\n--- Full Period Market Cap ---")
print(f"  Min: ${mc.min():,.0f}")
print(f"  Max: ${mc.max():,.0f}")
print(f"  Max expansion (trough to peak): {(mc.max() / mc.min() - 1) * 100:,.0f}%")
print(f"  Max contraction (peak to trough): {(1 - mc.min() / mc.max()) * 100:.1f}%")

print("\nDone.")
