# Findings: builder A, portfolio-level screens

Written 2026-11-19. Code: `screens.py` (all numbers) and `make_tables.py` (tables). Output: `out/`. Plan: `PRE-REGISTRATION.md`, written before the first run; one amendment, listed there.

## Answer

No. Neither of the two screens I designated in advance comes close to Berkshire over 1976-2025 once the leverage is financed at a rate an investor could get.

At 1.6x leverage, financed at the Treasury-bill rate plus 1%, with a 0.5% a year allowance for trading costs:

| | CAGR 1976-2025 | $1 grows to | Share of Berkshire's final wealth | Largest drawdown (month-end) |
|---|---|---|---|---|
| Berkshire Hathaway | 21.7% | $18,368 | 100% | -44% (monthly data from April 1980 only) |
| A11: a third each in the cheapest, lowest-beta and most profitable quintiles, 1.6x | 17.0% | $2,575 | 14% | -67% |
| A10: half big-cheap-profitable, half lowest-beta quintile, 1.6x | 15.5% | $1,339 | 7% | -67% |
| US market, 1.6x (no cost allowance) | 15.2% | $1,200 | 7% | -70% |
| US market, unlevered | 12.2% | $323 | 2% | -50% |

The test I fixed in advance was "at least half of Berkshire's final wealth", which over 50 years means a CAGR within about 1.4 points. A11 falls short by 4.7 points a year and A10 by 6.2.

## The spread across all thirteen screens

Same scenario (1.6x, T-bill + 1%, 0.5% haircut), 1976-2025:

- Lowest CAGR 14.2% (A1, lowest-beta quintile), median 16.2%, highest 20.5% (A13).
- Median share of Berkshire's final wealth: 10%.
- One screen of thirteen passes: A13, the four cheapest-and-most-profitable cells of the 5x5 book-to-market / profitability sort, at 20.5% a year and 62% of Berkshire's final wealth.

A13 was not a designated screen, and I do not recommend it as the answer, for these reasons:

1. It is the best of thirteen. One pass in thirteen tries is weak evidence.
2. It passes only in the first window. Over 2012-2025 it earned 11.3% a year at 1.6x against Berkshire's 14.4% and the unlevered market's 14.9%. It fails the sub-window test I set in advance.
3. Its cells are thin. Over the sample the four cells hold a median of 89, 41, 55 and 30 firms, and the cheapest-and-most-profitable cell falls to 11. The cells are averaged equally, so the smallest cell has a quarter of the weight. This is a small-stock, concentrated portfolio, and the 0.5% cost allowance is probably too kind to it.
4. Levered 1.6x it has 33% volatility, a 72% drawdown and a worst month of -44%. Berkshire's worst month from 1980 was -21%.

The same thinness affects A7, and through it A10. The "big, high book-to-market, high profitability" cell of the 2x4x4 sort holds a median of 8 firms and at one point a single firm. I kept the definition because it was pre-registered, but a quarter of A7 is a handful of stocks.

## What the gap is made of

**The window matters more than the screen.**

| Window | Berkshire CAGR | Market CAGR | A10 at 1.6x | A11 at 1.6x | Screens passing (of 13) |
|---|---|---|---|---|---|
| 1976-2011 (the paper's window) | 24.7% | 11.3% | 16.3% | 16.0% | 1 (A13) |
| 2012-2025 | 14.4% | 14.9% | 13.4% | 19.6% | 13 |
| 1976-2025 | 21.7% | 12.2% | 15.5% | 17.0% | 1 (A13) |

In the paper's window nothing designated is within 8 points a year. After 2011 Berkshire earned slightly less than the unlevered market, so every screen "passes", and so does the market at 1.6x. That is not evidence that the screens found Buffett's method; it is evidence that Berkshire stopped being hard to match.

**Berkshire's first four years are a large part of it.** Berkshire's share price rose 129%, 47%, 15% and 103% in 1976-1979, which multiplies $1 by 7.8. From April 1980, where monthly data begin, the picture is closer:

| April 1980 - December 2025, monthly | Excess return | Volatility | Sharpe | Beta | CAGR | $1 grows to | Max drawdown |
|---|---|---|---|---|---|---|---|
| Berkshire | 15.9% | 21.7% | 0.73 | 0.67 | 19.0% | $2,903 | -44% |
| A11 unlevered, as published | 9.9% | 14.0% | 0.71 | 0.86 | 13.6% | $348 | -47% |
| A10 unlevered, as published | 9.0% | 14.5% | 0.62 | 0.81 | 12.6% | $225 | -47% |
| A11 at 1.6x, T-bill, no costs (the paper's assumptions) | 15.9% | 22.4% | 0.71 | 1.38 | 18.7% | $2,534 | -66% |
| A11 at 1.6x, T-bill + 1%, 0.5% haircut | 14.5% | 22.4% | 0.65 | 1.38 | 17.1% | $1,345 | -67% |
| A10 at 1.6x, T-bill + 1%, 0.5% haircut | 13.1% | 23.2% | 0.56 | 1.29 | 15.2% | $655 | -67% |
| US market at 1.6x, T-bill + 1% | 13.9% | 24.7% | 0.56 | 1.60 | 15.7% | $777 | -70% |

Three things follow.

1. Unlevered, A11's Sharpe ratio (0.71) is about Berkshire's (0.73). The paper's claim that Berkshire's risk-adjusted return is good but not miraculous survives. Two non-designated screens (A2 low variance and A8 big-profitable-conservative) have a Sharpe of 0.78.
2. Under the paper's own frictionless assumptions (T-bill funding, no costs), A11 at 1.6x from 1980 gets to 18.7% a year against Berkshire's 19.0%. So the paper's story roughly works on paper from 1980.
3. The realistic version loses 1.6 points a year to the 1% borrowing spread and the cost allowance, ends with under half of Berkshire's money, and gets there with twice Berkshire's market beta and a 67% drawdown against Berkshire's 44%.

**Funding cost.** For A11 at 1.6x with the 0.5% haircut, 1976-2025:

| Borrowing rate | CAGR | Share of Berkshire's final wealth |
|---|---|---|
| T-bill | 17.7% | 19% |
| T-bill + 1% | 17.0% | 14% |
| T-bill + 2% | 16.3% | 10% |
| Berkshire's cost of float | 20.4% | 59% |
| Berkshire's float until 1995, float-plus-debt blend from 1996 | 19.4% | 39% |

Borrowing at Berkshire's cost of float adds about 3.4 points a year over T-bill + 1% and is the only scenario in which a designated screen passes at 1.6x. With float-cost funding six of thirteen screens pass; with T-bill + 2% none do.

**Leverage.** At 2.0x and T-bill + 1%, A11 reaches 19.1% a year (34% of Berkshire's wealth) and A10 17.1% (15%), with drawdowns of 76%. At 1.3x they reach 15.2% and 14.0%.

**Cost allowance.** Moving the haircut from 0% to 1% a year takes A11 at 1.6x from 17.9% to 16.1% and A10 from 16.4% to 14.6% (T-bill + 1%). The French and AQR portfolios carry no trading costs, fees or taxes. A taxable investor rebalancing every June and re-levering monthly would also pay tax that Berkshire deferred; that is not modelled.

## Margin

Berkshire's float and long-dated debt could not be called. A margin loan can. Results at T-bill + 1%:

- **Constant leverage, rebalanced monthly (M-A).** At 1.6x the month-end ratio of equity to assets never fell below 47% for any screen, so a 30% maintenance rule never triggered at a month end. At 2.0x it triggered once (A3, the cheap quintile). But this account avoids margin calls by selling after every fall: it is deleveraging itself all the time. Inside a month, on daily data, the 1.6x market account reached 46% on 26 October 1987 and the 2.0x account 29%; the 2.0x cheap-quintile account reached 16% on 23 March 2020.
- **Leverage reset once a year, held through falls (M-B), month-end checks.** At 1.6x no screen breached 30%. The lowest ratios were 33% (A6, A7), 36% (A3) and 38% (market, A13); A10 touched 40% and A11 43%. With a 40% requirement, seven of the fourteen series (market included) were sold out at least once, mostly in November 2008. At 2.0x every screen except the low-variance quintile was sold out at least once under the 30% rule, and the cheap screens three or four times.
- **The same account checked daily (M-D).** The 1.6x market account that looked safe at month ends breached 30% on 20 November 2008 (lowest ratio 26%), was sold down to 1.0x a few weeks before the low, and finished with $703 instead of $1,054. The 1.6x cheap-quintile account was called twice (19 November 2008, 18 March 2020) and finished with $1,754 instead of $5,256. A half-cheap, half-profitable mix (the nearest stand-in for A11 with daily data) was called once in November 2008 and finished with $2,476 instead of $3,863. At 2.0x the market was called four times and the cheap quintile five times; with no rule at all the 2.0x cheap-quintile account went to negative equity in March 2009.

Month-end checks therefore miss calls that daily checks catch, at 1.6x as well as 2.0x. Daily checks still understate the problem, because brokers raise requirements in a crisis and can call intraday. In a few cells of the tables the margin rule improves the outcome (the account was sold before a further fall). That is luck in the timing of the annual reset, not a feature.

A fixed-leverage account rebalanced monthly is the cleanest way to stay inside the rule, and all the headline numbers use it. Its price is the 67% drawdown and the need to sell every month in a falling market.

## Checks on look-ahead and data

- French files used, all "created using the 202609 CRSP database", value-weighted monthly returns: `Portfolios_Formed_on_BETA` (A1), `_VAR` (A2), `_BE-ME` (A3), `_E-P` (A4), `_OP` (A5), `_INV` (A6), `32_Portfolios_ME_BEME_OP_2x4x4` (A7), `32_Portfolios_ME_OP_INV_2x4x4` (A8), `25_Portfolios_ME_BETA_5x5` (A9), `25_Portfolios_BEME_OP_5x5` (A13), `F-F_Research_Data_Factors` (market, T-bill).
- Formation dates, read from each file's header: all are formed at the end of June of year t on accounting data from fiscal years ending in year t-1, with market equity from December t-1 (book-to-market, E/P) and beta from the prior 60 months. The exception is the variance sort (A2), which is re-formed every month on the prior 60 days of returns. That is not look-ahead, but it means far more trading than the others, so the flat cost allowance flatters A2.
- These are today's versions of the files. French revises history when CRSP and Compustat are corrected, and the profitability and investment sorts were first published in 2014-2015. An investor in 1976 could not have known that profitability would be a published sort. The screens are fixed rules, but the choice of which rules to try was made with hindsight, by the literature if not by me.
- AQR quality deciles (A12): US "long sample", value-weighted, published as returns in excess of T-bills; I added the French T-bill return back.
- Berkshire: my month-end series from Yahoo daily closes matches agent 1's `replication/data/berkshire_monthly.csv` exactly (549 months) and matches the shareholder-letter annual figures to within 0.05 points in every year 1981-2025. The 1976-1979 figures are the letter's.
- Berkshire's volatility and beta on the 1976-2025 rows are from 50 annual observations and are not comparable with monthly figures. The like-for-like monthly comparison starts in April 1980.

## How to recompute a headline number

A11 at 1.6x, T-bill + 1%, 0.5% haircut, January 1976 - December 2025:

1. Take the monthly value-weighted column `Hi 20` from `Portfolios_Formed_on_BE-ME.csv`, `Lo 20` from `Portfolios_Formed_on_BETA.csv`, and `Hi 20` from `Portfolios_Formed_on_OP.csv`. Divide by 100.
2. `r = (bm + beta + op) / 3` each month.
3. `RF` from `F-F_Research_Data_Factors.csv`, divided by 100.
4. Monthly account return `= 1.6 * (r - 0.005/12) - 0.6 * (RF + 0.01/12)`.
5. Compound over the 600 months. I get $2,574.66, a CAGR of 17.0%.

A10 uses step 4 with `r = 0.5 * mean('ME2 BM3 OP3', 'ME2 BM3 OP4', 'ME2 BM4 OP3', 'BIG HiBM HiOP' from 32_Portfolios_ME_BEME_OP_2x4x4.csv) + 0.5 * 'Lo 20' from the beta file`. I get $1,338.87, a CAGR of 15.5%. Berkshire is the compounded product of the letter's annual changes for 1976-2025: $18,367.80, 21.7%.

Files others can reuse:

- `out/monthly_unlevered.csv`: `yyyymm, rf, market, berkshire (blank before 198004), A1..A13`, decimal monthly total returns, as published (no haircut).
- `out/annual_returns.csv`: calendar-year returns for Berkshire (letter), market, T-bill, each screen unlevered and each screen at 1.6x under the headline scenario.
- `out/stats_all.csv`: every screen x leverage x financing x haircut x window. `out/margin_monthly.csv`, `out/margin_daily.csv`: margin simulations. `out/tables.md`: the tables below.

## Limits

- The federal funds scenario (F3) was not built because the download failed.
- No taxes, no fees, no bid-ask or market impact beyond the flat allowance, no borrowing limits, no change in the borrowing spread in crises.
- Thirteen screens were tried. The verdict rests on the two named in advance. A10 had been seen for 1985-2011 before the plan was written.
- Maximum drawdown is measured at month ends; daily lows are deeper.

# Appendix: full tables

### T1. Unlevered, as published (no cost haircut), monthly data, 1976-2025

| Screen | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|
| US market | 8.6% | 15.5% | 0.56 | 1.00 | 12.2% | $323 | -50% | -43% |
| A1 Low beta | 7.7% | 11.8% | 0.65 | 0.63 | 11.8% | $263 | -43% | -37% |
| A2 Low variance | 8.5% | 11.9% | 0.72 | 0.67 | 12.7% | $394 | -36% | -30% |
| A3 Cheap (B/M) | 12.0% | 18.9% | 0.64 | 1.04 | 15.4% | $1,278 | -58% | -48% |
| A4 Cheap (E/P) | 11.6% | 17.4% | 0.66 | 0.99 | 15.2% | $1,158 | -51% | -46% |
| A5 Profitable | 9.6% | 15.3% | 0.63 | 0.96 | 13.3% | $525 | -43% | -37% |
| A6 Conservative | 11.1% | 16.9% | 0.66 | 1.01 | 14.8% | $991 | -54% | -47% |
| A7 Big cheap profitable | 10.3% | 19.2% | 0.54 | 1.01 | 13.4% | $546 | -53% | -48% |
| A8 Big profitable conservative | 10.5% | 14.0% | 0.75 | 0.85 | 14.6% | $910 | -43% | -37% |
| A9 Big low beta | 8.3% | 12.8% | 0.65 | 0.75 | 12.3% | $329 | -45% | -38% |
| A10 Blend A7+A1 | 9.0% | 14.6% | 0.62 | 0.82 | 12.8% | $420 | -47% | -43% |
| A11 Blend cheap+safe+quality | 9.8% | 14.1% | 0.69 | 0.87 | 13.7% | $626 | -47% | -41% |
| A12 AQR quality P10 | 9.0% | 14.9% | 0.60 | 0.91 | 12.8% | $404 | -45% | -33% |
| A13 All-cap cheap profitable | 13.6% | 20.7% | 0.65 | 1.07 | 16.7% | $2,296 | -52% | -47% |
| Berkshire (calendar-year data) | 20.8% | 31.2% | 0.70 | 0.79 | 21.7% | $18,368 |  | worst year -32% |

### T1. Unlevered, as published (no cost haircut), monthly data, 1976-2011

| Screen | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|
| US market | 6.8% | 15.8% | 0.43 | 1.00 | 11.3% | $46.4 | -50% | -43% |
| A1 Low beta | 7.1% | 12.1% | 0.59 | 0.63 | 12.2% | $63.5 | -43% | -37% |
| A2 Low variance | 6.9% | 11.9% | 0.58 | 0.64 | 12.1% | $60.2 | -36% | -30% |
| A3 Cheap (B/M) | 10.9% | 17.8% | 0.61 | 0.98 | 15.5% | $178 | -58% | -48% |
| A4 Cheap (E/P) | 10.8% | 17.1% | 0.63 | 0.96 | 15.6% | $182 | -51% | -46% |
| A5 Profitable | 7.8% | 15.6% | 0.50 | 0.95 | 12.4% | $68.3 | -43% | -37% |
| A6 Conservative | 10.3% | 17.4% | 0.59 | 1.03 | 14.9% | $150 | -54% | -47% |
| A7 Big cheap profitable | 10.5% | 18.0% | 0.58 | 0.97 | 15.0% | $153 | -53% | -48% |
| A8 Big profitable conservative | 9.3% | 14.4% | 0.65 | 0.85 | 14.3% | $125 | -43% | -37% |
| A9 Big low beta | 6.9% | 13.2% | 0.53 | 0.74 | 11.9% | $56.7 | -45% | -38% |
| A10 Blend A7+A1 | 8.8% | 14.3% | 0.61 | 0.80 | 13.8% | $104 | -47% | -43% |
| A11 Blend cheap+safe+quality | 8.6% | 14.2% | 0.61 | 0.86 | 13.6% | $97.8 | -47% | -41% |
| A12 AQR quality P10 | 7.5% | 15.5% | 0.49 | 0.92 | 12.2% | $62.2 | -45% | -33% |
| A13 All-cap cheap profitable | 14.6% | 20.0% | 0.73 | 1.04 | 19.4% | $589 | -52% | -47% |
| Berkshire (calendar-year data) | 23.7% | 35.3% | 0.69 | 0.99 | 24.7% | $2,793 |  | worst year -32% |

### T1. Unlevered, as published (no cost haircut), monthly data, 2012-2025

| Screen | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|
| US market | 13.5% | 14.5% | 0.93 | 1.00 | 14.9% | $6.9 | -25% | -20% |
| A1 Low beta | 9.3% | 11.1% | 0.84 | 0.63 | 10.7% | $4.1 | -17% | -9% |
| A2 Low variance | 12.7% | 12.1% | 1.05 | 0.75 | 14.4% | $6.5 | -18% | -4% |
| A3 Cheap (B/M) | 15.0% | 21.5% | 0.70 | 1.23 | 15.1% | $7.2 | -42% | -33% |
| A4 Cheap (E/P) | 13.5% | 18.2% | 0.74 | 1.10 | 14.1% | $6.4 | -39% | -30% |
| A5 Profitable | 14.2% | 14.4% | 0.99 | 0.96 | 15.7% | $7.7 | -24% | -17% |
| A6 Conservative | 13.2% | 15.4% | 0.86 | 0.96 | 14.4% | $6.6 | -21% | -13% |
| A7 Big cheap profitable | 10.0% | 22.1% | 0.45 | 1.16 | 9.5% | $3.6 | -49% | -45% |
| A8 Big profitable conservative | 13.6% | 13.0% | 1.05 | 0.84 | 15.2% | $7.3 | -20% | -11% |
| A9 Big low beta | 11.8% | 11.9% | 0.99 | 0.78 | 13.4% | $5.8 | -21% | -15% |
| A10 Blend A7+A1 | 9.6% | 15.2% | 0.63 | 0.89 | 10.5% | $4.0 | -26% | -26% |
| A11 Blend cheap+safe+quality | 12.8% | 14.1% | 0.91 | 0.94 | 14.2% | $6.4 | -25% | -13% |
| A12 AQR quality P10 | 12.8% | 13.4% | 0.96 | 0.89 | 14.3% | $6.5 | -26% | -19% |
| A13 All-cap cheap profitable | 10.8% | 22.5% | 0.48 | 1.18 | 10.2% | $3.9 | -52% | -47% |
| Berkshire (calendar-year data) | 13.6% | 12.8% | 1.05 | 0.50 | 14.4% | $6.6 | -23% | worst year -12% |

### T2. Headline scenario: 1.6x, T-bill + 1%, 0.5% a year cost haircut. Monthly statistics 1976-2025; CAGR by window

| Screen | Excess | Vol | Sharpe | Beta | CAGR 76-25 | $1 grows to | Max DD | Worst 12m | CAGR gap to BRK | Wealth / BRK | Passes (>= 0.5) | CAGR 76-11 | gap | CAGR 12-25 | gap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| US market | 13.2% | 24.7% | 0.53 | 1.60 | 15.2% | $1,200 | -70% | -61% | -6.5% | 0.07 | no | 12.8% | -11.8% | 21.7% | 7.3% |
| A1 Low beta | 11.0% | 18.9% | 0.58 | 1.00 | 14.2% | $754 | -62% | -55% | -7.5% | 0.04 | no | 14.1% | -10.5% | 14.3% | -0.1% |
| A2 Low variance | 12.3% | 19.1% | 0.64 | 1.07 | 15.6% | $1,434 | -54% | -46% | -6.1% | 0.08 | no | 13.9% | -10.8% | 20.3% | 5.9% |
| A3 Cheap (B/M) | 17.8% | 30.2% | 0.59 | 1.67 | 18.7% | $5,303 | -78% | -68% | -3.0% | 0.29 | no | 18.4% | -6.2% | 19.4% | 5.0% |
| A4 Cheap (E/P) | 17.1% | 27.9% | 0.61 | 1.58 | 18.7% | $5,198 | -72% | -65% | -3.0% | 0.28 | no | 18.7% | -6.0% | 18.6% | 4.2% |
| A5 Profitable | 13.9% | 24.5% | 0.57 | 1.53 | 16.2% | $1,788 | -62% | -55% | -5.5% | 0.10 | no | 13.9% | -10.8% | 22.1% | 7.7% |
| A6 Conservative | 16.4% | 27.0% | 0.61 | 1.61 | 18.2% | $4,347 | -73% | -66% | -3.5% | 0.24 | no | 17.6% | -7.1% | 19.9% | 5.5% |
| A7 Big cheap profitable | 15.1% | 30.8% | 0.49 | 1.62 | 15.6% | $1,394 | -72% | -68% | -6.1% | 0.08 | no | 17.6% | -7.0% | 10.5% | -3.9% |
| A8 Big profitable conservative | 15.4% | 22.4% | 0.69 | 1.36 | 18.4% | $4,746 | -62% | -55% | -3.2% | 0.26 | no | 17.2% | -7.4% | 21.6% | 7.2% |
| A9 Big low beta | 11.9% | 20.5% | 0.58 | 1.20 | 14.8% | $1,015 | -64% | -56% | -6.8% | 0.06 | no | 13.4% | -11.3% | 18.6% | 4.2% |
| A10 Blend A7+A1 | 13.0% | 23.3% | 0.56 | 1.31 | 15.5% | $1,339 | -67% | -61% | -6.2% | 0.07 | no | 16.3% | -8.3% | 13.4% | -1.0% |
| A11 Blend cheap+safe+quality | 14.2% | 22.6% | 0.63 | 1.40 | 17.0% | $2,575 | -67% | -59% | -4.7% | 0.14 | no | 16.0% | -8.7% | 19.6% | 5.2% |
| A12 AQR quality P10 | 13.0% | 23.9% | 0.54 | 1.45 | 15.3% | $1,213 | -66% | -50% | -6.4% | 0.07 | no | 13.5% | -11.2% | 19.9% | 5.5% |
| A13 All-cap cheap profitable | 20.3% | 33.1% | 0.61 | 1.71 | 20.5% | $11,376 | -72% | -68% | -1.2% | 0.62 | yes | 24.3% | -0.3% | 11.3% | -3.1% |
| Berkshire | 20.8% | 31.2% (annual) | 0.70 (annual) | 0.79 (annual) | 21.7% | $18,368 |  | worst year -32% | 0 | 1.00 |  | 24.7% | 0 | 14.4% | 0 |

### T3. A10: leverage and financing, 1976-2025, 0.5% haircut

| L | Financing | CAGR | $1 grows to | Gap to BRK | Wealth / BRK | Vol | Sharpe | Max DD | Worst 12m | Worst month |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.3x | F0 Tbill | 14.3% | $808 | -7.4% | 0.04 | 18.9% | 0.59 | -58% | -53% | -23% |
| 1.3x | F1 Tbill+1 | 14.0% | $697 | -7.7% | 0.04 | 18.9% | 0.57 | -58% | -53% | -23% |
| 1.3x | F2 Tbill+2 | 13.7% | $601 | -8.0% | 0.03 | 18.9% | 0.55 | -58% | -53% | -23% |
| 1.3x | F4 BRK float | 15.6% | $1,435 | -6.0% | 0.08 | 18.9% | 0.65 | -57% | -52% | -22% |
| 1.3x | F5 BRK blend | 15.2% | $1,158 | -6.5% | 0.06 | 18.9% | 0.62 | -57% | -53% | -22% |
| 1.6x | F0 Tbill | 16.2% | $1,802 | -5.5% | 0.10 | 23.3% | 0.59 | -66% | -61% | -28% |
| 1.6x | F1 Tbill+1 | 15.5% | $1,339 | -6.2% | 0.07 | 23.3% | 0.56 | -67% | -61% | -28% |
| 1.6x | F2 Tbill+2 | 14.8% | $995 | -6.9% | 0.05 | 23.3% | 0.53 | -67% | -62% | -28% |
| 1.6x | F4 BRK float | 18.9% | $5,672 | -2.8% | 0.31 | 23.3% | 0.69 | -64% | -60% | -27% |
| 1.6x | F5 BRK blend | 17.9% | $3,697 | -3.8% | 0.20 | 23.3% | 0.65 | -66% | -61% | -28% |
| 2.0x | F0 Tbill | 18.3% | $4,474 | -3.4% | 0.24 | 29.1% | 0.59 | -75% | -71% | -35% |
| 2.0x | F1 Tbill+1 | 17.1% | $2,727 | -4.6% | 0.15 | 29.1% | 0.55 | -76% | -71% | -35% |
| 2.0x | F2 Tbill+2 | 16.0% | $1,661 | -5.7% | 0.09 | 29.1% | 0.52 | -76% | -71% | -35% |
| 2.0x | F4 BRK float | 22.9% | $30,170 | 1.2% | 1.64 | 29.1% | 0.72 | -73% | -69% | -34% |
| 2.0x | F5 BRK blend | 21.2% | $14,803 | -0.5% | 0.81 | 29.1% | 0.67 | -75% | -70% | -35% |

### T3. A11: leverage and financing, 1976-2025, 0.5% haircut

| L | Financing | CAGR | $1 grows to | Gap to BRK | Wealth / BRK | Vol | Sharpe | Max DD | Worst 12m | Worst month |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.3x | F0 Tbill | 15.5% | $1,366 | -6.2% | 0.07 | 18.4% | 0.66 | -58% | -50% | -26% |
| 1.3x | F1 Tbill+1 | 15.2% | $1,178 | -6.5% | 0.06 | 18.4% | 0.64 | -58% | -51% | -26% |
| 1.3x | F2 Tbill+2 | 14.9% | $1,015 | -6.8% | 0.06 | 18.4% | 0.62 | -58% | -51% | -26% |
| 1.3x | F4 BRK float | 16.9% | $2,425 | -4.8% | 0.13 | 18.4% | 0.72 | -57% | -50% | -26% |
| 1.3x | F5 BRK blend | 16.4% | $1,958 | -5.3% | 0.11 | 18.4% | 0.70 | -57% | -50% | -26% |
| 1.6x | F0 Tbill | 17.7% | $3,464 | -4.0% | 0.19 | 22.6% | 0.66 | -67% | -59% | -32% |
| 1.6x | F1 Tbill+1 | 17.0% | $2,575 | -4.7% | 0.14 | 22.6% | 0.63 | -67% | -59% | -32% |
| 1.6x | F2 Tbill+2 | 16.3% | $1,913 | -5.4% | 0.10 | 22.6% | 0.60 | -67% | -59% | -32% |
| 1.6x | F4 BRK float | 20.4% | $10,887 | -1.3% | 0.59 | 22.6% | 0.76 | -64% | -57% | -32% |
| 1.6x | F5 BRK blend | 19.4% | $7,102 | -2.3% | 0.39 | 22.6% | 0.72 | -66% | -58% | -32% |
| 2.0x | F0 Tbill | 20.3% | $10,232 | -1.4% | 0.56 | 28.3% | 0.66 | -76% | -68% | -40% |
| 2.0x | F1 Tbill+1 | 19.1% | $6,241 | -2.6% | 0.34 | 28.3% | 0.62 | -76% | -69% | -40% |
| 2.0x | F2 Tbill+2 | 17.9% | $3,805 | -3.8% | 0.21 | 28.3% | 0.59 | -77% | -69% | -40% |
| 2.0x | F4 BRK float | 25.0% | $68,763 | 3.3% | 3.74 | 28.3% | 0.79 | -73% | -66% | -40% |
| 2.0x | F5 BRK blend | 23.2% | $33,803 | 1.5% | 1.84 | 28.3% | 0.74 | -75% | -68% | -40% |

### T3. A13: leverage and financing, 1976-2025, 0.5% haircut

| L | Financing | CAGR | $1 grows to | Gap to BRK | Wealth / BRK | Vol | Sharpe | Max DD | Worst 12m | Worst month |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.3x | F0 Tbill | 18.9% | $5,839 | -2.8% | 0.32 | 26.9% | 0.63 | -63% | -58% | -36% |
| 1.3x | F1 Tbill+1 | 18.6% | $5,034 | -3.1% | 0.27 | 26.9% | 0.62 | -63% | -59% | -36% |
| 1.3x | F2 Tbill+2 | 18.2% | $4,340 | -3.5% | 0.24 | 26.9% | 0.61 | -63% | -59% | -36% |
| 1.3x | F4 BRK float | 20.3% | $10,359 | -1.4% | 0.56 | 26.9% | 0.67 | -63% | -58% | -36% |
| 1.3x | F5 BRK blend | 19.8% | $8,362 | -1.9% | 0.46 | 26.9% | 0.66 | -63% | -58% | -36% |
| 1.6x | F0 Tbill | 21.3% | $15,307 | -0.4% | 0.83 | 33.1% | 0.63 | -72% | -68% | -44% |
| 1.6x | F1 Tbill+1 | 20.5% | $11,376 | -1.2% | 0.62 | 33.1% | 0.61 | -72% | -68% | -44% |
| 1.6x | F2 Tbill+2 | 19.8% | $8,454 | -1.9% | 0.46 | 33.1% | 0.59 | -72% | -68% | -44% |
| 1.6x | F4 BRK float | 24.1% | $48,121 | 2.4% | 2.62 | 33.1% | 0.70 | -71% | -67% | -44% |
| 1.6x | F5 BRK blend | 23.0% | $31,368 | 1.3% | 1.71 | 33.1% | 0.67 | -72% | -67% | -44% |
| 2.0x | F0 Tbill | 23.5% | $38,443 | 1.8% | 2.09 | 41.4% | 0.63 | -82% | -78% | -55% |
| 2.0x | F1 Tbill+1 | 22.3% | $23,420 | 0.6% | 1.28 | 41.4% | 0.61 | -83% | -78% | -55% |
| 2.0x | F2 Tbill+2 | 21.1% | $14,262 | -0.6% | 0.78 | 41.4% | 0.58 | -84% | -79% | -55% |
| 2.0x | F4 BRK float | 28.3% | $259,455 | 6.6% | 14.13 | 41.4% | 0.72 | -81% | -77% | -55% |
| 2.0x | F5 BRK blend | 26.5% | $127,071 | 4.8% | 6.92 | 41.4% | 0.69 | -82% | -78% | -55% |

### T3. Market: leverage and financing, 1976-2025, no haircut

| L | Financing | CAGR | $1 grows to | Gap to BRK | Wealth / BRK | Vol | Sharpe | Max DD | Worst 12m | Worst month |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.3x | F0 Tbill | 14.2% | $766 | -7.5% | 0.04 | 20.1% | 0.56 | -61% | -52% | -30% |
| 1.3x | F1 Tbill+1 | 13.9% | $660 | -7.8% | 0.04 | 20.1% | 0.54 | -61% | -53% | -30% |
| 1.3x | F2 Tbill+2 | 13.5% | $569 | -8.2% | 0.03 | 20.1% | 0.53 | -61% | -53% | -30% |
| 1.3x | F4 BRK float | 15.5% | $1,359 | -6.2% | 0.07 | 20.1% | 0.62 | -60% | -52% | -29% |
| 1.3x | F5 BRK blend | 15.0% | $1,097 | -6.7% | 0.06 | 20.1% | 0.59 | -60% | -52% | -29% |
| 1.6x | F0 Tbill | 15.9% | $1,616 | -5.8% | 0.09 | 24.7% | 0.56 | -69% | -61% | -37% |
| 1.6x | F1 Tbill+1 | 15.2% | $1,200 | -6.5% | 0.07 | 24.7% | 0.53 | -70% | -61% | -37% |
| 1.6x | F2 Tbill+2 | 14.6% | $892 | -7.1% | 0.05 | 24.7% | 0.51 | -71% | -61% | -37% |
| 1.6x | F4 BRK float | 18.6% | $5,075 | -3.1% | 0.28 | 24.8% | 0.65 | -68% | -59% | -36% |
| 1.6x | F5 BRK blend | 17.6% | $3,313 | -4.1% | 0.18 | 24.7% | 0.62 | -69% | -60% | -36% |
| 2.0x | F0 Tbill | 17.8% | $3,616 | -3.9% | 0.20 | 30.9% | 0.56 | -79% | -70% | -46% |
| 2.0x | F1 Tbill+1 | 16.6% | $2,203 | -5.1% | 0.12 | 30.9% | 0.53 | -81% | -71% | -46% |
| 2.0x | F2 Tbill+2 | 15.5% | $1,341 | -6.2% | 0.07 | 30.9% | 0.49 | -83% | -71% | -46% |
| 2.0x | F4 BRK float | 22.4% | $24,271 | 0.7% | 1.32 | 31.0% | 0.68 | -77% | -68% | -46% |
| 2.0x | F5 BRK blend | 20.7% | $11,946 | -1.0% | 0.65 | 30.9% | 0.64 | -77% | -70% | -46% |

### T4. Like-for-like monthly comparison with Berkshire, 1980.04-2025

| Series | Version | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|---|
| Berkshire |  | 15.9% | 21.7% | 0.73 | 0.67 | 19.0% | $2,903 | -44% | -44% |
| US market | unlevered, as published | 9.0% | 15.5% | 0.58 | 1.00 | 12.4% | $210 | -50% | -43% |
| A2 Low variance | unlevered, as published | 9.3% | 12.0% | 0.78 | 0.67 | 13.2% | $292 | -36% | -30% |
| A8 Big profitable conservative | unlevered, as published | 10.8% | 13.8% | 0.78 | 0.84 | 14.7% | $533 | -43% | -37% |
| A10 Blend A7+A1 | unlevered, as published | 9.0% | 14.5% | 0.62 | 0.81 | 12.6% | $225 | -47% | -43% |
| A11 Blend cheap+safe+quality | unlevered, as published | 9.9% | 14.0% | 0.71 | 0.86 | 13.6% | $348 | -47% | -41% |
| A13 All-cap cheap profitable | unlevered, as published | 13.3% | 20.6% | 0.64 | 1.05 | 16.1% | $927 | -52% | -47% |
| US market | 1.6x, T-bill+1%, 0.5% haircut | 13.9% | 24.7% | 0.56 | 1.60 | 15.7% | $777 | -70% | -61% |
| A2 Low variance | 1.6x, T-bill+1%, 0.5% haircut | 13.4% | 19.1% | 0.70 | 1.07 | 16.7% | $1,153 | -54% | -46% |
| A8 Big profitable conservative | 1.6x, T-bill+1%, 0.5% haircut | 16.0% | 22.1% | 0.72 | 1.34 | 18.8% | $2,690 | -62% | -55% |
| A10 Blend A7+A1 | 1.6x, T-bill+1%, 0.5% haircut | 13.1% | 23.2% | 0.56 | 1.29 | 15.2% | $655 | -67% | -61% |
| A11 Blend cheap+safe+quality | 1.6x, T-bill+1%, 0.5% haircut | 14.5% | 22.4% | 0.65 | 1.38 | 17.1% | $1,345 | -67% | -59% |
| A13 All-cap cheap profitable | 1.6x, T-bill+1%, 0.5% haircut | 19.8% | 32.9% | 0.60 | 1.68 | 19.7% | $3,737 | -72% | -68% |

### T4. Like-for-like monthly comparison with Berkshire, 1980.04-2011

| Series | Version | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|---|
| Berkshire |  | 17.0% | 23.6% | 0.72 | 0.64 | 21.1% | $441 | -44% | -44% |
| US market | unlevered, as published | 7.1% | 15.9% | 0.45 | 1.00 | 11.3% | $30.2 | -50% | -43% |
| A2 Low variance | unlevered, as published | 7.8% | 11.9% | 0.65 | 0.64 | 12.7% | $44.6 | -36% | -30% |
| A8 Big profitable conservative | unlevered, as published | 9.6% | 14.2% | 0.68 | 0.83 | 14.5% | $73.1 | -43% | -37% |
| A10 Blend A7+A1 | unlevered, as published | 8.8% | 14.2% | 0.62 | 0.78 | 13.5% | $55.7 | -47% | -43% |
| A11 Blend cheap+safe+quality | unlevered, as published | 8.7% | 13.9% | 0.62 | 0.84 | 13.4% | $54.4 | -47% | -41% |
| A13 All-cap cheap profitable | unlevered, as published | 14.3% | 19.7% | 0.73 | 1.01 | 18.8% | $238 | -52% | -47% |
| US market | 1.6x, T-bill+1%, 0.5% haircut | 10.7% | 25.4% | 0.42 | 1.60 | 13.1% | $49.9 | -70% | -61% |
| A2 Low variance | 1.6x, T-bill+1%, 0.5% haircut | 11.0% | 19.1% | 0.58 | 1.02 | 15.1% | $87.0 | -54% | -46% |
| A8 Big profitable conservative | 1.6x, T-bill+1%, 0.5% haircut | 14.0% | 22.7% | 0.62 | 1.33 | 17.6% | $174 | -62% | -55% |
| A10 Blend A7+A1 | 1.6x, T-bill+1%, 0.5% haircut | 12.6% | 22.7% | 0.56 | 1.25 | 16.1% | $113 | -67% | -61% |
| A11 Blend cheap+safe+quality | 1.6x, T-bill+1%, 0.5% haircut | 12.4% | 22.2% | 0.56 | 1.34 | 15.9% | $109 | -67% | -59% |
| A13 All-cap cheap profitable | 1.6x, T-bill+1%, 0.5% haircut | 21.6% | 31.5% | 0.68 | 1.61 | 23.6% | $836 | -72% | -68% |

### T4. Like-for-like monthly comparison with Berkshire, 2012-2025

| Series | Version | Excess | Vol | Sharpe | Beta | CAGR | $1 grows to | Max DD | Worst 12m |
|---|---|---|---|---|---|---|---|---|---|
| Berkshire |  | 13.4% | 16.6% | 0.81 | 0.75 | 14.4% | $6.6 | -23% | -16% |
| US market | unlevered, as published | 13.5% | 14.5% | 0.93 | 1.00 | 14.9% | $6.9 | -25% | -20% |
| A2 Low variance | unlevered, as published | 12.7% | 12.1% | 1.05 | 0.75 | 14.4% | $6.5 | -18% | -4% |
| A8 Big profitable conservative | unlevered, as published | 13.6% | 13.0% | 1.05 | 0.84 | 15.2% | $7.3 | -20% | -11% |
| A10 Blend A7+A1 | unlevered, as published | 9.6% | 15.2% | 0.63 | 0.89 | 10.5% | $4.0 | -26% | -26% |
| A11 Blend cheap+safe+quality | unlevered, as published | 12.8% | 14.1% | 0.91 | 0.94 | 14.2% | $6.4 | -25% | -13% |
| A13 All-cap cheap profitable | unlevered, as published | 10.8% | 22.5% | 0.48 | 1.18 | 10.2% | $3.9 | -52% | -47% |
| US market | 1.6x, T-bill+1%, 0.5% haircut | 21.0% | 23.1% | 0.91 | 1.60 | 21.7% | $15.6 | -39% | -33% |
| A2 Low variance | 1.6x, T-bill+1%, 0.5% haircut | 18.9% | 19.3% | 0.98 | 1.20 | 20.3% | $13.3 | -28% | -10% |
| A8 Big profitable conservative | 1.6x, T-bill+1%, 0.5% haircut | 20.4% | 20.7% | 0.98 | 1.35 | 21.6% | $15.5 | -32% | -20% |
| A10 Blend A7+A1 | 1.6x, T-bill+1%, 0.5% haircut | 14.0% | 24.4% | 0.58 | 1.43 | 13.4% | $5.8 | -40% | -40% |
| A11 Blend cheap+safe+quality | 1.6x, T-bill+1%, 0.5% haircut | 19.1% | 22.6% | 0.85 | 1.50 | 19.6% | $12.3 | -38% | -24% |
| A13 All-cap cheap profitable | 1.6x, T-bill+1%, 0.5% haircut | 15.9% | 35.9% | 0.44 | 1.88 | 11.3% | $4.5 | -71% | -66% |

### T5. Spread across all thirteen screens, 1976-2025, 0.5% haircut (Berkshire CAGR 21.7%)

| L | Financing | Lowest CAGR | Median CAGR | Highest CAGR | Median wealth / BRK | Screens passing | Which |
|---|---|---|---|---|---|---|---|
| 1.3x | F0 Tbill | 13.1% | 14.9% | 18.9% | 0.06 | 0 |  |
| 1.3x | F1 Tbill+1 | 12.8% | 14.6% | 18.6% | 0.05 | 0 |  |
| 1.3x | F2 Tbill+2 | 12.4% | 14.2% | 18.2% | 0.04 | 0 |  |
| 1.3x | F4 BRK float | 14.4% | 16.3% | 20.3% | 0.10 | 1 | A13 |
| 1.3x | F5 BRK blend | 13.9% | 15.8% | 19.8% | 0.08 | 0 |  |
| 1.6x | F0 Tbill | 14.8% | 16.8% | 21.3% | 0.13 | 1 | A13 |
| 1.6x | F1 Tbill+1 | 14.2% | 16.2% | 20.5% | 0.10 | 1 | A13 |
| 1.6x | F2 Tbill+2 | 13.5% | 15.5% | 19.8% | 0.07 | 0 |  |
| 1.6x | F4 BRK float | 17.5% | 19.6% | 24.1% | 0.41 | 6 | A3, A4, A6, A8, A11, A13 |
| 1.6x | F5 BRK blend | 16.5% | 18.5% | 23.0% | 0.27 | 5 | A3, A4, A6, A8, A13 |
| 2.0x | F0 Tbill | 17.0% | 19.0% | 23.5% | 0.33 | 6 | A3, A4, A6, A8, A11, A13 |
| 2.0x | F1 Tbill+1 | 15.8% | 17.8% | 22.3% | 0.20 | 5 | A3, A4, A6, A8, A13 |
| 2.0x | F2 Tbill+2 | 14.7% | 16.7% | 21.1% | 0.12 | 1 | A13 |
| 2.0x | F4 BRK float | 21.5% | 23.6% | 28.3% | 2.20 | 13 | A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13 |
| 2.0x | F5 BRK blend | 19.8% | 21.9% | 26.5% | 1.09 | 12 | A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, A12, A13 |

### T6. Margin rules, month-end checks, T-bill + 1%, 0.5% haircut, 1976-2025

| Screen | L | M-A: lowest month-end equity/assets (monthly rebalance) | M-A triggers | Annual reset: lowest equity/assets | Annual reset, no rule: $1 to | M-B 30% triggers | M-B dates | M-B: $1 to | M-B40 triggers | M-B40: $1 to |
|---|---|---|---|---|---|---|---|---|---|---|
| Market | 1.6x | 51% | 0 | 38% | $1,063 | 0 |  | $1,063 | 1 | $1,036 |
| Market | 2.0x | 35% | 0 | 18% | $1,561 | 1 | 200810 | $1,977 | 10 | $667 |
| A1 | 1.6x | 56% | 0 | 46% | $707 | 0 |  | $707 | 0 | $707 |
| A1 | 2.0x | 42% | 0 | 28% | $1,337 | 1 | 200811 | $1,336 | 4 | $925 |
| A2 | 1.6x | 55% | 0 | 48% | $1,364 | 0 |  | $1,364 | 0 | $1,364 |
| A2 | 2.0x | 40% | 0 | 30% | $3,133 | 0 |  | $3,133 | 2 | $2,272 |
| A3 | 1.6x | 47% | 0 | 36% | $5,149 | 0 |  | $5,149 | 2 | $2,831 |
| A3 | 2.0x | 29% | 1 | 14% | $9,310 | 3 | 200207 200810 202003 | $3,981 | 7 | $7,820 |
| A4 | 1.6x | 48% | 0 | 38% | $5,634 | 0 |  | $5,634 | 2 | $3,244 |
| A4 | 2.0x | 31% | 0 | 17% | $13,641 | 3 | 199009 200810 202003 | $5,113 | 6 | $2,599 |
| A5 | 1.6x | 50% | 0 | 43% | $1,649 | 0 |  | $1,649 | 0 | $1,649 |
| A5 | 2.0x | 34% | 0 | 25% | $3,050 | 1 | 200810 | $3,403 | 6 | $4,454 |
| A6 | 1.6x | 51% | 0 | 33% | $3,672 | 0 |  | $3,672 | 1 | $3,636 |
| A6 | 2.0x | 34% | 0 | 11% | $5,333 | 1 | 200810 | $9,716 | 6 | $7,687 |
| A7 | 1.6x | 50% | 0 | 33% | $1,203 | 0 |  | $1,203 | 1 | $1,294 |
| A7 | 2.0x | 34% | 0 | 11% | $1,087 | 4 | 199009 200810 201512 202003 | $885 | 8 | $1,137 |
| A8 | 1.6x | 53% | 0 | 43% | $4,444 | 0 |  | $4,444 | 0 | $4,444 |
| A8 | 2.0x | 37% | 0 | 24% | $11,698 | 1 | 200810 | $13,023 | 6 | $7,446 |
| A9 | 1.6x | 55% | 0 | 44% | $922 | 0 |  | $922 | 0 | $922 |
| A9 | 2.0x | 39% | 0 | 25% | $1,694 | 1 | 200810 | $1,959 | 6 | $1,223 |
| A10 | 1.6x | 55% | 0 | 40% | $1,216 | 0 |  | $1,216 | 0 | $1,216 |
| A10 | 2.0x | 39% | 0 | 20% | $2,076 | 1 | 200810 | $2,680 | 6 | $1,407 |
| A11 | 1.6x | 53% | 0 | 43% | $2,425 | 0 |  | $2,425 | 0 | $2,425 |
| A11 | 2.0x | 37% | 0 | 23% | $5,396 | 1 | 200810 | $6,432 | 6 | $2,097 |
| A12 | 1.6x | 52% | 0 | 44% | $1,140 | 0 |  | $1,140 | 0 | $1,140 |
| A12 | 2.0x | 36% | 0 | 26% | $2,033 | 1 | 200810 | $2,244 | 7 | $1,199 |
| A13 | 1.6x | 48% | 0 | 38% | $11,094 | 0 |  | $11,094 | 1 | $9,541 |
| A13 | 2.0x | 31% | 0 | 17% | $21,034 | 4 | 199009 200810 201509 202003 | $13,543 | 10 | $4,388 |

### T7. Margin rule M-D: same annual-reset account checked daily against month-end, T-bill + 1%, 1976-2025

| Portfolio | L | Lowest daily equity/assets with no rule | No rule: $1 to | 30% rule, month-end checks: triggers | $1 to | 30% rule, daily checks: triggers | Dates | $1 to | 40% month-end triggers | 40% daily triggers | 40% daily: $1 to |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Market | 1.6x | 26% | $1,054 | 0 | $1,054 | 1 | 20081120 | $703 | 1 | 1 | $1,058 |
| Market | 2.0x | 2% | $1,546 | 1 | $1,957 | 4 | 20010921 20020723 20081007 20200320 | $617 | 10 | 11 | $703 |
| A3 | 1.6x | 20% | $5,256 | 0 | $5,256 | 2 | 20081119 20200318 | $1,754 | 2 | 4 | $1,527 |
| A3 | 2.0x | -6% | $9,348 | 3 | $3,991 | 5 | 20020716 20081009 20090223 20111003 20200309 | $2,255 | 7 | 8 | $11,067 |
| A5 | 1.6x | 32% | $1,655 | 0 | $1,655 | 0 |  | $1,655 | 0 | 1 | $1,502 |
| A5 | 2.0x | 10% | $3,042 | 1 | $3,387 | 2 | 20020723 20081007 | $3,059 | 6 | 10 | $1,101 |
| A3+A5 half each | 1.6x | 27% | $3,863 | 0 | $3,863 | 1 | 20081120 | $2,476 | 0 | 2 | $1,978 |
| A3+A5 half each | 2.0x | 3% | $8,452 | 3 | $4,607 | 4 | 20020719 20081009 20090305 20200312 | $1,868 | 6 | 9 | $4,413 |

### T8. Constant leverage rebalanced monthly: lowest equity/assets reached inside a month (daily path)

| Portfolio | L | Lowest equity/assets | Date |
|---|---|---|---|
| Market | 1.6x | 46% | 19871026 |
| Market | 2.0x | 29% | 19871026 |
| A3 | 1.6x | 37% | 20200323 |
| A3 | 2.0x | 16% | 20200323 |
| A5 | 1.6x | 45% | 19871026 |
| A5 | 2.0x | 26% | 19871026 |
| A3+A5 half each | 1.6x | 45% | 20200323 |
| A3+A5 half each | 2.0x | 27% | 20200323 |

# Corrections after builder B's review (added 2026-11-19; the text above is unchanged)

B's review is at `B/REVIEW-OF-A.md`. I checked each point with my own code (`response_to_b.py`, output in `out/response_to_b.txt`). These checks are post hoc.

1. **A13 does not pass when its cells are weighted sensibly. Accepted.** With the four cells weighted by their market value (weights lagged one month) I get 18.5% a year and $4,782, which is 26% of Berkshire's final wealth; weighted by number of firms, 19.9% and 47%. B gets 18.4% and 20.0%. The cheapest-and-most-profitable cell holds a median of 3.9% of the four cells' market value and has 25% of the weight in my definition. The summary should read "no screen passes", not "one of thirteen passes".
2. **My margin rule M-B sells every December. Accepted.** The sentence "At 1.6x no screen breached 30%" is true only for an account that resets downward each December. For an account that borrows back up to 1.6x each December and never sells unless called, on month-end data: A11 and A10 both reach an equity ratio of 0.28 in February 2009 and are called under a 30% rule; the market is called in September 2002 and February 2009; the cheap quintile reaches 0.08; A13 is called twice. A11 ends with $1,721 instead of $2,575 (my rule sells to 1.0x on a call; B's sells back to 1.6x and gets $2,066). Only the low-risk screens are not called: A2 (low variance) bottoms at 0.41 and A1 (low beta) at 0.32.
3. **Split at 1998/1999. Accepted.** At 1.6x, T-bill + 1%, 0.5% haircut: Berkshire 38.2% then 9.2%; A11 23.8% then 11.5%; A10 23.7% then 8.9%; market (no haircut) 20.2% then 11.2%. Across the thirteen screens the 1976-1998 range is 20.2% to 31.7% with a median of 23.8%, so the median gap in the first 23 years is 14 points a year. In 1999-2025 ten of thirteen beat Berkshire. (B's review quotes 19.3% and 10.3% for the market; that figure includes the 0.5% haircut.)
4. **Daily stand-in for A11.** Accepted as stated: the half-cheap, half-profitable mix leaves out A11's low-beta third and overstates its daily stress somewhat.
5. **Flat costs.** Accepted. The 0.5% allowance is too low for A2 (re-formed monthly) and A13 (small cells).
6. **Berkshire's drawdown.** Accepted. On daily closes Berkshire's deepest fall is 51.5% (5 March 2009), with 37.1% in 1987 and 48.9% in 1998-2000. The 44% in my tables is month-end. The screens' 67% is also month-end.
