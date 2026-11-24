# Can a simple levered stock screen match Berkshire? Joint report of builders A and B

Written 2026-11-20 by builder A (portfolio-level screens), after reading builder B's findings and B's review of A. Builder B (stock-level screens, sceptic) adds a sign-off or dissent at the end.

## The answer

No. Over 1976-2025 a simple long-only screen of cheap, safe, high-quality stocks, run at 1.6x and financed at the Treasury-bill rate plus 1% with a modest allowance for trading costs, compounded at about 14% to 17% a year against Berkshire's 21.7%, and ended with roughly a tenth of Berkshire's wealth ($1 became about $1,300 to $2,600, against $18,368). The whole shortfall is in 1976-1998, when Berkshire compounded at 38% a year and the screens at about 24%; since 1999 most of the screens, and the plain market at 1.6x, have beaten Berkshire, which says more about Berkshire than about the screens.

## How the question was tested

- Two independent builds. A used published, pre-sorted portfolios from the Ken French data library (and AQR's quality deciles), which include delisted firms and whose sorting rules were fixed by someone else. B built screens stock by stock from Yahoo prices and dividends on today's S&P 1500 members, plus real index funds.
- Each builder wrote down its screens, leverage rule, financing scenarios and pass mark before running anything (`A/PRE-REGISTRATION.md`, `B/PRE-REGISTRATION.md`). A named two primary screens in advance (A10 and A11) so that the verdict would not rest on the best of many. All 13 of A's screens and all 5 of B's are reported in `A/FINDINGS.md` and on `BOARD.md`.
- Each builder recomputed the other's headline numbers with its own code and reproduced them (`A/review_b.py`, `B/review_a.py`).
- Headline scenario: constant 1.6x leverage reset every month end; borrowing at the one-month Treasury bill rate plus 1% a year; 0.5% a year taken off the unlevered return for trading costs (A) or era-specific costs on measured turnover (B). Berkshire is the class A share price: the shareholder letter's annual figures for 1976-2025, and Yahoo month-end closes from April 1980.
- A's pass mark: at least half of Berkshire's final wealth, which over 50 years is a CAGR within about 1.4 points. B's pass mark: within 2 points a year, with no fall in account equity beyond 75%.

## The screens we both stand behind

We stand behind these as fair, rebuildable tests of the idea. None of them passes.

**1. A11: cheap + safe + quality, in thirds (the main screen).** Each month hold one third in each of three Ken French value-weighted portfolios: the highest book-to-market quintile (`Portfolios_Formed_on_BE-ME.csv`, column `Hi 20`), the lowest-beta quintile (`Portfolios_Formed_on_BETA.csv`, column `Lo 20`), and the highest operating-profitability quintile (`Portfolios_Formed_on_OP.csv`, column `Hi 20`), using the "Value Weight Returns -- Monthly" block of each file. French re-forms each portfolio once a year at the end of June from accounting data for the previous fiscal year and betas from the previous 60 months. Rebalance the three thirds monthly. In stock terms: every June, rank all US stocks, and buy the cheapest fifth by book-to-market, the fifth with the lowest beta and the fifth with the highest operating profit to book equity, each weighted by market value.

**2. A2: the low-risk screen.** The lowest-variance quintile of French's `Portfolios_Formed_on_VAR.csv` (column `Lo 20`, value-weighted): each month, the fifth of stocks with the lowest variance of daily returns over the previous 60 days. B's stock-level version (the lowest-volatility stocks among large, liquid names, chosen once a year from three years of weekly returns, equal-weighted) lands in the same place: 11.3% a year unlevered against 12.7% for A2 and 11.3% for the French big-stock lowest-variance cell. This is the one kind of screen that a 1.6x margin account could have held through 2008-09 without a call. It was not one of A's designated screens; it is here because both builds agree on it and because of the margin result. Its monthly re-formation means more trading than the 0.5% allowance assumes.

**3. A10: the author's original blend.** Half in the average of four big-stock cells of French's 2x4x4 size / book-to-market / profitability sort (`32_Portfolios_ME_BEME_OP_2x4x4.csv`, columns `ME2 BM3 OP3`, `ME2 BM3 OP4`, `ME2 BM4 OP3`, `BIG HiBM HiOP`), half in the lowest-beta quintile. This is the screen in `bt.py` and is kept for continuity. It is the weakest of the three: one of its cells holds a median of 8 firms and at one point a single firm, and it has lagged badly since 2012. If the post uses one screen, use A11.

To lever any of them: monthly account return = `1.6 x (screen return - 0.5%/12) - 0.6 x (T-bill return + 1%/12)`.

## Results

Monthly data, January 1976 to December 2025, from `series.csv`. Starred Berkshire figures use monthly data from April 1980, because nothing more frequent than annual exists before then.

| Series | CAGR 1976-2025 | $1 grows to | Share of Berkshire's final wealth | CAGR 1976-1998 | CAGR 1999-2025 | CAGR 1976-2011 | CAGR 2012-2025 | Volatility | Sharpe | Beta | Largest fall (month-end) | Worst 12 months |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Berkshire Hathaway | 21.7% | $18,368 | 100% | 38.2% | 9.2% | 24.7% | 14.4% | 21.7%* | 0.73* | 0.67* | -44%* | -44%* |
| US market, unlevered | 12.2% | $323 | 2% | 16.4% | 8.9% | 11.3% | 14.9% | 15.5% | 0.56 | 1.00 | -50% | -43% |
| US market, 1.6x, T-bill + 1% | 15.2% | $1,200 | 7% | 20.2% | 11.2% | 12.8% | 21.7% | 24.7% | 0.53 | 1.60 | -70% | -61% |
| A11, unlevered | 13.7% | $626 | 3% | 19.0% | 9.5% | 13.6% | 14.2% | 14.1% | 0.69 | 0.87 | -47% | -41% |
| A11, 1.6x, T-bill, no costs (the paper's assumptions) | 18.6% | $5,144 | 28% | 25.6% | 13.0% | 17.6% | 21.3% | 22.6% | 0.69 | 1.40 | -66% | -58% |
| A11, 1.6x, T-bill + 1%, no costs | 17.9% | $3,824 | 21% | 24.8% | 12.4% | 16.9% | 20.6% | 22.6% | 0.66 | 1.40 | -67% | -59% |
| **A11, 1.6x, T-bill + 1%, 0.5% costs (headline)** | **17.0%** | **$2,575** | **14%** | 23.8% | 11.5% | 16.0% | 19.6% | 22.6% | 0.63 | 1.40 | -67% | -59% |
| A2, unlevered | 12.7% | $394 | 2% | 16.7% | 9.4% | 12.1% | 14.4% | 11.9% | 0.72 | 0.67 | -36% | -30% |
| A2, 1.6x, T-bill, no costs | 17.3% | $2,865 | 16% | 22.0% | 13.4% | 15.5% | 21.9% | 19.1% | 0.72 | 1.07 | -53% | -45% |
| A2, 1.6x, T-bill + 1%, no costs | 16.6% | $2,130 | 12% | 21.3% | 12.7% | 14.8% | 21.2% | 19.1% | 0.68 | 1.07 | -54% | -45% |
| **A2, 1.6x, T-bill + 1%, 0.5% costs (headline)** | **15.6%** | **$1,434** | **8%** | 20.3% | 11.8% | 13.9% | 20.3% | 19.1% | 0.64 | 1.07 | -54% | -46% |
| A10, unlevered | 12.8% | $420 | 2% | 18.9% | 7.9% | 13.8% | 10.5% | 14.6% | 0.62 | 0.82 | -47% | -43% |
| A10, 1.6x, T-bill, no costs | 17.1% | $2,677 | 15% | 25.5% | 10.4% | 17.9% | 14.9% | 23.3% | 0.62 | 1.31 | -66% | -61% |
| A10, 1.6x, T-bill + 1%, no costs | 16.4% | $1,989 | 11% | 24.7% | 9.8% | 17.2% | 14.3% | 23.3% | 0.59 | 1.31 | -66% | -61% |
| **A10, 1.6x, T-bill + 1%, 0.5% costs (headline)** | **15.5%** | **$1,339** | **7%** | 23.7% | 8.9% | 16.3% | 13.4% | 23.3% | 0.56 | 1.31 | -67% | -61% |

On daily closes Berkshire's deepest fall is 51.5% (5 March 2009), not the 44% that month-end data show. The screens' falls are also month-end and would be deeper daily.

Other leverage and funding, A11 with 0.5% costs, 1976-2025 (full grid in `A/FINDINGS.md`, table T3):

| | T-bill | T-bill + 1% | T-bill + 2% | Berkshire's cost of float | Float to 1995, float-plus-debt blend from 1996 |
|---|---|---|---|---|---|
| 1.3x | 15.5% | 15.2% | 14.9% | 16.9% | 16.4% |
| 1.6x | 17.7% | 17.0% | 16.3% | 20.4% | 19.4% |
| 2.0x | 20.3% | 19.1% | 17.9% | 25.0% | 23.2% |

Spread across all of A's thirteen screens at 1.6x, T-bill + 1%, 0.5% costs: 14.2% to 20.5% a year, median 16.2%, median share of Berkshire's wealth 10%. B's stock-level screens, judged by the figure B's survivorship-free cross-checks support: low volatility 13.7%, low beta 14.0%, high yield with low volatility between 11% and 15%, high yield about 15.5%.

## What the gap is made of

1. **Mostly the first 23 years.** Berkshire's share price rose 129%, 47%, 15% and 103% in 1976-1979 alone. Over 1976-1998 the median of A's thirteen levered screens earned 23.8% a year, 14 points behind Berkshire. Over 1999-2025 ten of the thirteen beat it.
2. **Risk-adjusted, the screens are in Berkshire's neighbourhood.** From April 1980, unlevered, A11 has a Sharpe ratio of 0.71 and B's low-volatility screens 0.67 to 0.74, against Berkshire's 0.73. Under the paper's frictionless assumptions (T-bill funding, no costs) A11 at 1.6x from April 1980 earns 18.7% a year against Berkshire's 19.0%. So the paper's account holds up as a description from 1980, on paper.
3. **Frictions cost about 1.6 points a year at 1.6x**: 0.6 points from the 1% borrowing spread and 0.8 from the cost allowance. That is the difference between 28% and 14% of Berkshire's final wealth.
4. **Funding is the largest lever.** Borrowing at Berkshire's cost of float instead of T-bill + 1% adds about 3.4 points a year to A11 at 1.6x (20.4%, 59% of Berkshire's wealth). It is the only scenario in which a designated screen passes A's test at 1.6x. An outside investor cannot borrow at that rate.
5. **The screens take more market risk.** A11 at 1.6x has a beta of 1.4 and fell 67% at month ends. Berkshire's beta was 0.67 and its worst fall 51%.

## Margin: what "cannot be called" was worth

- An account held at a constant 1.6x by rebalancing every month is never called at a month end, because it sells after every fall. All the headline numbers assume this. Its cost is the selling itself and the 54% to 67% falls in the table.
- An investor who tries to do what Berkshire did, borrow and hold through, is in a different position. With leverage topped back up to 1.6x each December and no voluntary selling, on month-end data with a 30% maintenance requirement: A11 and A10 both fall to an equity-to-assets ratio of 0.28 in February 2009 and are called; the market at 1.6x is called in September 2002 and February 2009; the cheap quintile falls to 0.08. A call near the low costs A11 between a fifth and a third of its final wealth, depending on how much the broker sells. On daily closes the calls come earlier and more often (the market on 19 July 2002 and 20 November 2008; the cheap quintile in November 2008 and March 2020), and with no maintenance rule at all the 1.6x cheap-quintile and market accounts are wiped out or nearly so in March 2009.
- Only the low-risk screens survive at 1.6x: A2's lowest ratio is 0.41, the low-beta quintile's 0.32, and B's low-volatility stock screens 0.36 on weekly closes.
- At 2.0x everything is called at least once.
- Berkshire's own shares, held at 1.6x on margin, reach a ratio of 0.24 on 5 March 2009 and are called. Berkshire the company was not, because its leverage was insurance float and long-dated debt.
- Month-end and even daily checks understate the problem: brokers raise requirements in a crisis and can call intraday.

## What did not work

- **A13, the only screen that passed A's test.** The four cheapest-and-most-profitable cells of French's 5x5 book-to-market / profitability sort, averaged equally: 20.5% a year, 62% of Berkshire's wealth. It was not a designated screen, it fails after 2011 (11.3% against 14.4%), and its pass comes from giving a quarter of the weight to a cell that holds a median of 30 firms and 4% of the four cells' market value. Weighted by market value it earns 18.5% and 26% of Berkshire's wealth. So no screen passes.
- **Quality alone.** The most profitable quintile (A5) and AQR's top quality decile (A12) at 1.6x earn 16.2% and 15.3%, no better than the levered market's 15.2%, over the full period.
- **Low beta alone.** The lowest-beta quintile at 1.6x earns 14.2%, the lowest of the thirteen.
- **Big-cheap-profitable (A7).** 15.6% over the full period and 10.5% since 2012, from cells holding a handful of stocks.
- **B's raw stock-level passes.** High yield 30 (19.8%) and dividend growers (19.7% from 1984) pass B's test only because the universe is today's index members. The same universe with no screen at all, in equal weight, earns 18.8% at 1.6x. The survivorship-free French highest-yield quintile at 1.6x earns 15.4% to 16.3%.
- **Style funds.** VIVAX (from 1992), VIG (2006), SPLV and USMV (2011) and QUAL (2013) at 1.6x: over each fund's life, the plain S&P 500 fund at 1.6x did better than the style fund.
- **More leverage.** At 2.0x and T-bill + 1%, A11 reaches 19.1% a year, still 2.6 points short, with a 76% fall and at least one margin call.
- **Not built:** a federal funds or prime-rate financing scenario. FRED was unreachable from both builders' machines. T-bill + 1% and T-bill + 2% bracket a broker rate.

## Cautions for the post

- **Hindsight in the choice of screens.** The rules are mechanical and use only information available at each June, but the idea of sorting on profitability or low beta comes from papers published after most of the sample. An investor in 1976 had book-to-market and dividend yield, and not much else.
- **The French files are today's vintage** ("202609 CRSP database"). History is revised when the underlying databases are corrected.
- **Costs are a flat allowance.** 0.5% a year is reasonable for annual sorts on large stocks (B measured 0.3 to 0.5 points on its yearly-rebalanced screens) and too low for A2 and anything in small cells. Taxes are not modelled; a levered investor rebalancing monthly pays tax that Berkshire deferred.
- **A10 was seen before the plan was written** (its 1985-2011 result was in `bt.py`). A11 was not.
- **Survivor universes flatter backtests by a lot.** B measured 2.3 points a year for large stocks and 5.6 for all sizes on today's S&P 1500 members, nearly all of it after 1998. Any reader who tries this with a current ticker list will get a pass that is not real.
- **Berkshire's 1976-2025 volatility, beta and drawdown** in monthly terms exist only from April 1980.

## Disagreements left unresolved

1. **How far to trust B's stock-level returns before the mid-1980s.** A's review found that Yahoo records no dividends before 1977 for 73 of the 140 tickers with prices by 1973 (the first record is mostly 1984-1987), so early "total" returns are partly price returns and the yield screens choose from the half of the universe that has a record; and that B1-B3 hold 5 stocks in 1976 and 14 or 15 until 1983. A's view is that B1-B5 are illustrations before about 1984 and that the measured survivorship gap for 1976-1998 (about zero) is two opposite errors cancelling. B had not responded to this when the report was first written; B has since accepted it in the sign-off below, so this point is resolved (the remaining open points are items 2 and 3 here and the five qualifications B lists in the sign-off). It does not change the verdict: B's fair figures (14% to 15.5%) rest on survivorship-free cross-checks.
2. **How to state the cost of a margin call.** A's simulation sells to 1.0x on a call (A11 ends with $1,721); B's sells back to 1.6x ($2,066). The no-call monthly-reset figure is $2,575. Both are shown; neither is "the" answer, because it depends on the broker.
3. **Whether A2 belongs among the recommended screens.** It was not designated in advance and is re-formed monthly. It is included at A's proposal because both builds agree on the low-risk leg and it is the only type of screen that avoids a call at 1.6x. B may disagree below.

Points on which B objected and A agreed (A13's weights, the December selling in A's margin rule, the 1998/1999 split, Berkshire's daily drawdown, flat costs) are incorporated above; the detail is at the end of `A/FINDINGS.md`.

## Files

- `series.csv`: monthly, January 1976 to December 2025. `date` (month end), then decimal monthly total returns: `berkshire` (blank before April 1980), `market`, `rf` (one-month Treasury bill), `market_16x_tbill1`, and for each of `a11`, `a2`, `a10`: the unlevered screen as published, `_16x_tbill` (1.6x, T-bill, no costs), `_16x_tbill1` (1.6x, T-bill + 1%, no costs) and `_16x_tbill1_cost` (1.6x, T-bill + 1%, 0.5% a year costs: the headline). The `w_` columns are the same series as the value of $1 invested at the end of December 1975. `w_berkshire` has year-end values only for 1976-1979 (from the letter), then monthly from March 1980; it ends at $18,408 against $18,368 from the letter's rounded annual figures.
- `A/out/annual_returns.csv`: calendar-year returns, for a chart that includes Berkshire from 1976.
- `A/PRE-REGISTRATION.md`, `A/FINDINGS.md` (all thirteen screens, every window, leverage, financing and margin table, plus corrections), `A/REVIEW-OF-B.md`, `A/screens.py`, `A/response_to_b.py`, `A/make_series.py`, `A/report_table.py`.
- `B/PRE-REGISTRATION.md`, `B/REVIEW-OF-A.md`, `B/out/results.txt`, `B/out/margin.txt`; B's findings are on `BOARD.md`.

## Sceptic's sign-off (builder B)

Written by builder B after reading the report above and `A/REVIEW-OF-B.md`. I have not edited anything above this heading.

### What I agree with

- The answer. No simple long-only screen at 1.6x, financed at a rate an investor could get, came close to Berkshire over 1976-2025. I reproduced A11 ($2,575, 17.0%), A10 ($1,339, 15.5%) and A13 ($11,376, 20.5%) from my own downloads with my own parser, and my stock-level screens reach the same range by a different route.
- The range of 14% to 17% a year against 21.7%, and "about a tenth of Berkshire's final wealth".
- That the whole shortfall is in 1976-1998 (38.2% against about 24%), and that beating Berkshire since 1999 is no achievement, because the plain market at 1.6x did it too.
- That no screen passes. A13 passes only with a quarter of its weight in a cell holding 4% of the market value, and my two raw passes come from using today's index members.
- The margin section as now written. A accepted that its original rule sold every December, and the report now says that A11 and A10 at 1.6x are called in February 2009 if held through.

### A's objection to my data, which I accept

A found that Yahoo has no dividend record before 1977 for about half of the early tickers. I checked: of the 141 tickers in my files with prices by the end of 1973, 66 have a first recorded dividend in 1962-1973, 4 in 1974-1980, and 71 only later or never, most of them in 1984-1987 (28 in 1987 alone). For those stocks my early "total" returns are price returns. The consequences are as A states them:

- My stock-level returns before about 1988 are understated for any holding without a dividend record. In the low-volatility screen that is 3 of 14 holdings in 1977 and 5 of 32 in 1984, and none by 1988. The controls C0 and C1 are affected more, because they hold everything.
- My measured survivorship gap for 1976-1998, which is about zero, is an upward survivorship bias and a downward missing-dividend bias roughly cancelling. The gap of 2.3 points a year over the full period is therefore an underestimate of the true survivorship bias, not an overestimate.
- The yield screens (B3, B5) chose only among stocks with a dividend record until the mid-1980s, and the dividend-growers screen (B4) started in 1984 for that reason.
- My statement that the low-risk screens show "little or no survivorship bias" is only established from the late 1980s. After 1999 the low-volatility screen earns 9.3% a year against 8.0% for the French big-stock lowest-variance cell and 9.4% for the lowest-variance quintile, and 10.7% against 10.0% for SPLV since 2011, so a bias of zero to about one point is the right reading for that period.

None of my B1-B5 return figures should be quoted in the post for 1976-1987 as more than an illustration. What survives from my side is: the size of the survivor-universe trap, the agreement with the French low-risk portfolios after the late 1980s, the fund comparison, and the margin simulation, none of which depends on the early dividend data.

### What I still dispute or would qualify

1. **A2 as a recommended screen.** I do not object to showing it, but it should not be described as a screen we "stand behind" on the same footing as A11. It was not designated in advance, it is re-formed every month from 60 days of daily variance so its real trading cost is well above the 0.5% allowance, and its 1.6x return (15.6%) is no better than the levered market's (15.2%). Its merit is the smaller fall, not the return. Its lowest equity ratio of 0.41 is a month-end figure; French publishes no daily file for it, and my weekly stock version reached 0.36. It probably avoids a call at 1.6x, but that has not been shown on daily data.
2. **The top of the range leans on things a 1976 investor did not have.** A11's 17.0% uses a profitability sort first published in 2013 and a cheap quintile that is the part of the portfolio that gets called on margin. Using only what was knowable in 1976 (book-to-market, dividend yield, low volatility), at 1.6x and Treasury bills plus 1%, the survivorship-free figures run from about 14% to 16.5% before costs for anything a large investor could hold. The cheap quintile alone reaches 18.7%, but it is the screen that a 1.6x margin account loses in November 2008. I would treat 17% as an upper bound.
3. **The frictionless comparison from April 1980 (18.7% against 19.0%) should not be quoted on its own.** It starts after Berkshire's price had risen 7.8 times in four years, it borrows at the Treasury bill rate with no costs, and it reaches Berkshire's return with a beta of 1.4 against 0.67 and a month-end fall of 66% against 44%. It shows that the paper's arithmetic is not absurd. It does not show that the screen matched Berkshire.
4. **The cost of a margin call depends on the baseline.** Against the monthly-reset account, one call costs A11 a fifth to a third of final wealth ($2,066 or $1,721 against $2,575). Against what the investor was trying to do, which is hold through without selling ($3,353 if no rule had applied), it costs 38% to 49%. In my daily simulations a single forced sale near the low cost a third to a half of final wealth in most cases. The post should say "roughly a third to a half of the gain from holding on", and note that this is the mild case of a broker who sells only what the rule requires.
5. **Taxes and the financing spread make all of this an upper bound.** Treasury bills plus 1% is what a large account pays today. For most of 1976-2005 a retail margin account paid 2 points or more over bills, which takes a further 0.7 points a year off a 1.6x account. A yearly-reconstituted, monthly-relevered portfolio also pays tax that a Berkshire shareholder deferred for fifty years.

### The sentence the post can safely say

From 1976 to 2025, a mechanical portfolio of cheap, low-risk, profitable US stocks levered 1.6 times at the Treasury bill rate plus 1% would have compounded at roughly 14% to 17% a year against 21.7% for Berkshire's shares, ending with about a tenth of the money, with the entire shortfall coming before 1999; and a margin account that tried to hold such a portfolio through 2008-09 without selling would have been called, as would one holding Berkshire's own shares at 1.6 times.
