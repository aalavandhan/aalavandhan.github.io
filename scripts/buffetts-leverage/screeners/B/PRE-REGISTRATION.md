# Pre-registration, builder B (written 2026-11-19, before any screen was run)

## The question

Is there a simple, systematic, long-only stock screen that, run with moderate leverage (target 1.6x, at most 2x) and financed at a realistic rate, would have come close to Berkshire Hathaway's share-price return over 1976-2025?

## What I already knew when writing this

I have not run any of the screens below. I do know the following, and a reader should discount my choices accordingly.

- The paper's own long-only, unlevered Buffett-style portfolio earned 7.0% a year over Treasury bills with a Sharpe ratio of 0.45, against 6.1% and 0.39 for the market (Table 2, 1976-2011).
- A first backtest in this project (bt.py) found that a 50/50 blend of two Ken French portfolios at 1.6x earned 13.6% excess with a Sharpe ratio of 0.59 and a 66% drawdown over 1985-2011, against 15.2% and 0.64 for Berkshire.
- It is common knowledge in the literature that low-volatility and dividend stocks did well after 1970. Every screen below is therefore chosen with some hindsight about the style, even though I have not seen its numbers.

## Data

- Weekly Yahoo bars (split-adjusted close, dividend-adjusted close, volume, dividend events) for the tickers in today's S&P 1500 list. This universe contains only companies that are still listed and in an index today. Every stock-level result is survivorship-biased and will be labelled as such.
- Yahoo daily or weekly adjusted prices for index funds and ETFs. These are real investable products with real fees, and they are not survivorship-biased at the stock level.
- Ken French monthly risk-free rate (one-month Treasury bill) and market return.
- Berkshire: Yahoo BRK-A from March 1980 (weekly and daily), and the annual per-share market-value changes in the 2025 shareholder letter for 1976-2025.
- FRED bank prime loan rate, if it can be fetched, as a proxy for a retail margin rate.

## Screens

Stock-level screens use only prices, volumes and dividends that were public on the selection date. Selection happens on the last weekly close of each December, the portfolio is equal-weighted and held for the next calendar year. "History" means weekly dividend-adjusted returns. The "large half" is the top half of eligible stocks ranked by dollar trading volume (split-adjusted close times split-adjusted volume) over the prior 52 weeks; eligible stocks have at least 156 weeks of history. Where a screen says "50 stocks", it takes 50 or one fifth of the large half, whichever is smaller, because the survivor universe is small in the early years.

| Id | Name | Rule in one sentence | Investable from |
|---|---|---|---|
| C0 | Survivor universe, equal weight | Hold every eligible stock in equal weight; this is a control that measures the survivorship bias, not a screen. | n/a |
| B1 | Low volatility 50 | From the large half, hold the 50 stocks with the lowest standard deviation of weekly returns over the prior 156 weeks. | 1976 in principle (prices were public; the low-risk anomaly was published by Black, Jensen and Scholes in 1972 and Haugen and Heins in 1975), though realistically it needed a computer and a price tape. |
| B2 | Low beta 50 | From the large half, hold the 50 stocks with the lowest beta to the S&P 500 price index over the prior 156 weeks. | 1976, same caveat. |
| B3 | High yield, low volatility | From the large half, take the half with the higher trailing-12-month dividend yield, then hold the 50 with the lowest 156-week volatility. | 1976, same caveat. |
| B4 | Dividend growers | Hold every eligible stock (any size) whose trailing-12-month dividend has not fallen in any of the last 10 years and is higher than 10 years ago; start in the first year with at least 20 names. | About 1979 (Moody's began publishing a "Dividend Achievers" list then). |
| B5 | High yield 30 | From the 100 largest by dollar volume, hold the 30 with the highest trailing-12-month dividend yield. | 1976 in principle; popularised in 1991 as "Dogs of the Dow". |
| F1 | S&P 500 index fund (VFINX) | Buy and hold the fund; a no-screen benchmark. | August 1976 (Yahoo history starts 1980). |
| F2 | Value index fund (VIVAX) | Buy and hold Vanguard Value Index. | November 1992. |
| F3 | Dividend-growth index (VIG) | Buy and hold Vanguard Dividend Appreciation ETF. | April 2006. |
| F4 | Low-volatility ETFs (SPLV, USMV) | Buy and hold each; reported separately. | 2011. |
| F5 | Quality ETF (QUAL) | Buy and hold. | July 2013. |

If a ticker in F1-F5 has no usable Yahoo history I will say so and not substitute another without recording it under Amendments.

## Leverage rule

- Main case: constant 1.6x, reset at each month-end, with interest charged on the borrowed 0.6.
- Also 1.3x and 2.0x.
- Also annual reset (leverage drifts within the year), because that is what the annual Berkshire data allow and what a lazy investor would do.

## Financing scenarios

1. One-month Treasury bill rate (unrealistically cheap for a retail investor; it is the paper's convention).
2. Treasury bill + 1%.
3. Treasury bill + 2%.
4. Bank prime rate, as a proxy for what a retail margin account was charged for most of the period (only if FRED is reachable).

Headline scenario: Treasury bill + 1%.

## Trading costs

Stock-level screens are reported gross and net. Net applies a one-way cost to the turnover at each annual reconstitution: 1.0% for 1976-1989, 0.5% for 1990-2004, 0.1% from 2005. Funds already include their expense ratios; no further cost is applied.

## Survivorship adjustment

The bias will be estimated as the return of C0 minus the return of the actual market over the same years (Ken French value-weighted market, and an equal-weighted large-stock portfolio from Ken French if I can download one). Each stock-level screen will be reported raw and with that annual gap subtracted. The subtraction is crude: it assumes the screen's stocks are flattered by as much as the average stock in the universe. I will state which direction I think the error goes.

## Margin simulation

Using weekly data for the stock screens and daily data for funds, Berkshire and any daily Ken French portfolios I can download for agent A's screens:

- Policy "ratchet": start at the target leverage; at each year-end borrow more to get back up to target if leverage has fallen below it; never sell voluntarily. This is the policy that produces margin calls.
- Policy "monthly reset": back to target every month-end in both directions.
- Maintenance requirement: equity of 25% and of 30% of assets. A call is triggered at a close below the requirement; the account then sells enough to return to the target leverage, at that close, paying the trading cost of the era on the amount sold.
- Reported for 1.6x and 2.0x: the lowest equity ratio reached and its date, the number of forced sales, the worst drawdown of account equity, and the terminal-wealth cost of the maintenance rule compared with the same account without one. Windows of interest: 1987, 1998-2002, 2008-09, 2020.
- Weekly closes understate intraweek lows, so the weekly results are a lower bound on the stress. I will show the daily Berkshire and fund figures next to the weekly ones to gauge the gap.

## Success metric

Fixed in advance: a screen "comes close" if, at 1.6x with monthly reset, financed at Treasury bill + 1%, net of trading costs and after the survivorship subtraction, its compound annual return over the longest common period with Berkshire is within 2 percentage points of Berkshire's, and it does this without the account being wiped out or its equity falling more than 75% from a peak. I will also report the Sharpe ratio, and the two halves 1976-1998 and 1999-2025 separately, because a screen that matches only in the second half has matched a different Berkshire.

Comparison periods: 1976-2025 on annual data (Berkshire from the shareholder letter), April 1980 to December 2025 on monthly data, and each fund from its own first full month.

## Reporting rule

Every screen above is reported, including any that fail to run, with the reason. No screen is added to the headline table after results are seen; anything added later goes under Amendments and is labelled post hoc.

## Amendments

### Amendment 1, 2026-11-19 23:05 EST, before any screen was run

- Added a second control, C1: the large half of the eligible survivor universe in equal weight. Four of the five stock screens select from the large half, so C1 minus an equal-weighted portfolio of genuinely large stocks is a better estimate of their bias than C0 minus the market. The headline survivorship subtraction is C1 minus the equal-weighted top-30%-by-size portfolio from Ken French ("Hi 30", equal-weighted). For B4, which uses all sizes, the subtraction is C0 minus the same Ken French portfolio. I will also show the gap against the value-weighted market.
- As a direct cross-check that needs no adjustment, I will compare B1 and B2 with the survivorship-free Ken French low-variance and low-beta portfolios over the same years.
- FRED did not respond from this machine, so financing scenario 4 (prime rate) cannot be run. Scenario 3 (Treasury bill + 2%) is the closest stand-in for a broker rate.
- While downloading I also fetched VEIPX, VDIGX, SDY, RSP and SPY. They are not pre-registered. If I report any of them, it will be in a separate table labelled post hoc.


### Note on timing, added 2026-11-19 at 23:13 EST by the system clock

The time "23:05 EST" in the heading of Amendment 1 was my estimate and is wrong. By the file system, this file was last modified (with Amendment 1) at 23:00:59 and the first screen output (`out/screens_weekly.csv`) was written at 23:03:40, so the amendment did precede the first run, as it says. Nothing else in this file has been changed since.
