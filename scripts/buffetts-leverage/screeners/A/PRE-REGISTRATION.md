# Pre-registration: builder A, portfolio-level screens

Written on 2026-11-19 before any screen in this folder was run. This file is not edited after results exist. Changes go in the AMENDMENTS section at the bottom, with a reason.

## Question

Is there a simple, systematic, long-only stock screen that, run with moderate leverage (target 1.6x, at most about 2x) financed at a realistic rate, would have come close to Berkshire Hathaway's returns over 1976-2025?

## What I had already seen when writing this

I had read `bt.py`, the author's first backtest, and its output for February 1985 to December 2011. That backtest contains two of the screens below (A7 and A10) and the lowest-beta quintile (A1). I therefore know that A10 at 1.6x came out below Berkshire in that window ($54 against $82 with Treasury-bill financing). I had not seen any result for the other screens, for 1976-1984, or for 2012-2025. I had looked at the header text of the French files to check formation dates, and at Berkshire's cost-of-float table. I had not looked at any return series.

## Data

- Ken French data library, monthly value-weighted returns, United States. All portfolios used are formed at the end of June of year t on accounting data from fiscal years ending in calendar year t-1 and (for beta and variance) on returns up to June. I will confirm this from the header of each file and record it in FINDINGS.md.
- AQR data library, "Quality Minus Junk: 10 Quality-Sorted Portfolios, Monthly" (United States), if it can be downloaded. If it cannot, A12 is reported as "not built".
- Risk-free rate: the one-month Treasury bill return in the French factor file.
- Berkshire Hathaway: class A share price. Monthly returns from month-end closes built from Yahoo daily data (available from March 1980, so the first full month is April 1980). For 1976-1979 only calendar-year returns exist, taken from the table of annual changes in per-share market value in the 2025 shareholder letter. Berkshire has paid no dividend in this period, so price change equals total return.
- Effective federal funds rate: FRED series FEDFUNDS (monthly average), if it can be downloaded.

## Candidate screens

All are long-only, value-weighted within each French portfolio, and need no rule beyond "hold the published portfolio". Where a screen averages several portfolios the average is equal-weighted and rebalanced monthly.

| ID | Name | One-sentence definition |
|---|---|---|
| A1 | Low beta | The lowest-beta quintile ("Lo 20") of French's portfolios formed on beta. |
| A2 | Low variance | The lowest-variance quintile ("Lo 20") of French's portfolios formed on variance of daily returns. |
| A3 | Cheap (book) | The highest book-to-market quintile ("Hi 20") of French's portfolios formed on BE/ME. |
| A4 | Cheap (earnings) | The highest earnings-to-price quintile ("Hi 20") of French's portfolios formed on E/P. |
| A5 | Profitable | The highest operating-profitability quintile ("Hi 20") of French's portfolios formed on OP. |
| A6 | Conservative | The lowest asset-growth quintile ("Lo 20") of French's portfolios formed on investment. |
| A7 | Big, cheap, profitable | The average of the four big-stock cells of French's 2x4x4 size / book-to-market / profitability sort that are in the top two book-to-market quartiles and the top two profitability quartiles (the definition already used in `bt.py`). |
| A8 | Big, profitable, conservative | The average of the four big-stock cells of French's 2x4x4 size / profitability / investment sort that are in the top two profitability quartiles and the bottom two investment quartiles. |
| A9 | Big, low beta | The average of the two lowest-beta cells in the largest size quintile of French's 5x5 size / beta sort. |
| A10 | Blend: A7 + A1 | Half in A7 (big, cheap, profitable) and half in A1 (low beta), rebalanced monthly (the blend already used in `bt.py`). |
| A11 | Blend: cheap + safe + quality | One third each in A3 (cheap), A1 (low beta) and A5 (profitable), rebalanced monthly. |
| A12 | AQR quality | The top decile ("P10") of AQR's ten quality-sorted United States portfolios. |
| A13 | All-cap cheap and profitable | The average of the four cells of French's 5x5 book-to-market / profitability sort that are in the top two book-to-market quintiles and the top two profitability quintiles. |

Benchmarks reported alongside: the United States market (French Mkt-RF plus RF), the market at each leverage level, and Berkshire.

If a column label in a downloaded file differs from what I expect (for example the 5x5 size / beta file uses different cell names), I will use the cells that match the sentence above and note the exact labels in FINDINGS.md.

## Designated primary screens

To limit the freedom to pick a winner afterwards, I name the headline screens now, on the grounds that they are the closest portfolio-level translation of the paper's description ("cheap, safe, high-quality"):

- **A10** is the primary screen, because the author already has it. Its 1985-2011 result was seen in advance.
- **A11** is the clean second primary: it uses only one-way sorts, and I have not seen any result for it.

The other eleven screens exist to show the spread. If one of them beats A10 and A11, the report will say so, and will also say that it was not the designated screen.

## Leverage rule

- Constant leverage L, rebalanced back to L at each month end. Monthly return of the levered account: `L * r_assets - (L - 1) * r_borrow`.
- L = 1.6 is the headline. L = 1.3 and L = 2.0 are also reported, together with L = 1.0.

## Financing scenarios

`r_borrow` is one of:

1. F0: one-month Treasury bill rate (the rate the paper assumes; not available to any real borrower).
2. F1: Treasury bill + 1% a year. This is the headline scenario.
3. F2: Treasury bill + 2% a year.
4. F3: effective federal funds rate + 0.5% a year (FRED FEDFUNDS divided by 12), if the series can be downloaded.
5. F4: Berkshire's own cost of float for that calendar year from `float.csv` (underwriting loss divided by average float; negative when underwriting was profitable), divided by 12 for each month. For 1976, where the letter says only "less than zero", I use 0%.
6. F5: as F4 up to 1995, then Berkshire's blended cost of float plus debt from `leverage_cost.csv` (column `blend_pct`) from 1996.

F4 and F5 are not available to an outside investor. They are there to show how much of the gap cheap funding closes.

## Trading-cost haircut

French and AQR portfolio returns include no trading costs, fees or taxes. I subtract a flat haircut from the unlevered asset return before leverage is applied: 0% (as published), 0.5% a year (headline) and 1% a year. At 1.6x the account therefore pays 1.6 times the haircut.

## Margin rules

A constant-leverage account rebalanced monthly sells into every fall, so it almost never breaches a maintenance requirement at a month end. That is itself a form of forced deleveraging, and its cost is already inside the constant-leverage numbers. To model a borrower who, like Berkshire, does not sell when prices fall, I add:

- **M-A**: constant 1.6x (and 2.0x), monthly rebalance, maintenance requirement equity / assets >= 30% checked at month end. I expect this never to trigger and will report whether it does.
- **M-B**: leverage reset to L once a year at the end of December; in between, the holding is not traded and the loan accrues interest. Equity / assets is checked at every month end. If it is below 30%, the account is sold down to 1.0x (the loan is repaid in full) and stays unlevered until the next December reset. Reported: number of triggers, dates, and the difference in CAGR and terminal wealth against the same annual-reset account with no margin rule.
- **M-B40**: as M-B with a 40% requirement, to stand for a lender who tightens terms in a crisis.
- **M-D**: a daily check for the market portfolio only (French daily factors), with the same annual-reset rule and 30% requirement, to show how much monthly checks understate the number of triggers. If French daily files exist for the cells of A1 and A3 I will run those too.

Monthly checks understate the problem, because the low inside a month is below the month-end value, and because lenders raise requirements exactly when prices fall.

## Windows and statistics

- Windows: January 1976 to December 2025 (full), January 1976 to December 2011 (the paper's window, which strictly starts in October 1976), January 2012 to December 2025.
- For each screen, window, leverage and financing scenario: mean excess return over Treasury bills (arithmetic monthly mean times 12), annualised volatility, Sharpe ratio, market beta, CAGR, growth of $1, maximum drawdown (month-end), worst rolling 12 months, and the gap to Berkshire's CAGR.
- Comparison with Berkshire for 1976-2025 and 1976-2011 is at calendar-year frequency, because Berkshire has no monthly data before 1980. Monthly statistics for Berkshire use April 1980 onward, and the screens are also reported on that same sample so the monthly numbers are like for like.

## Success metric

Fixed in advance:

- **Primary test**: over calendar years 1976-2025, with 1.6x leverage, Treasury bill + 1% financing and a 0.5% a year cost haircut, does the screen end with at least half of Berkshire's terminal wealth? Over 50 years that is the same as a CAGR within about 1.4 percentage points of Berkshire's. If yes, the screen "came close". If no, it did not.
- **Secondary tests**: (a) the same test in each sub-window, 1976-2011 and 2012-2025, so that a pass cannot come from one period only; (b) the unlevered Sharpe ratio of the screen against Berkshire's, monthly from April 1980; (c) the levered account survives margin rule M-B without a trigger, or the cost of the triggers is stated.
- **Multiple comparisons**: with thirteen screens, the best one will look better than it is. The report gives the median and the full range across all thirteen, and the verdict rests on the two designated screens (A10, A11), not on the best of thirteen.

## AMENDMENTS

(none yet)

### Amendment 1 (2026-11-19, after the first run)

- F3 (federal funds + 0.5%) was not built. FRED timed out on four attempts and the Federal Reserve's H.15 download returned an empty file. No substitute was invented. T-bill + 1% and T-bill + 2% bracket it.
- A12 was built. AQR's file states that its returns are in excess of Treasury bills, so the French one-month bill return was added back.
- M-D (daily checks) was run for the market, A3, A5 and a half-and-half mix of A3 and A5. French publishes no daily file for the beta sort, so A1, A10 and A11 could not be checked daily; the A3 + A5 mix is the nearest available stand-in for A11 and is labelled as such.
- The windows labelled "1980.04" use monthly data from April 1980. Their calendar-year figures start in 1981, the first full year.
- Nothing else in the plan changed. The list of screens, the cells, the designated primaries and the success metric are as written above.
