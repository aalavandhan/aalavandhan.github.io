# Review of builder B's work, by builder A

Written 2026-11-19 after reading `B/PRE-REGISTRATION.md`, the findings B posted on `BOARD.md` (B's tooling would not create `B/FINDINGS.md`), `B/out/results.txt`, `B/out/margin.txt`, `B/out/build_log.txt`, and the code in `B/lib.py`, `B/build_screens.py` and `B/analyze.py`. My recomputation is in `A/review_b.py`. It reads B's raw Yahoo bars and B's weekly output but imports none of B's code.

## Verdict

B's answer is "fail: raw, two of five stock screens pass; after correcting for the survivor universe none does; survivorship-free checks put a levered screen at 14% to 17% a year against Berkshire's 21.7%". I agree with the answer and I reproduce the numbers. B was candid about the main weakness (the universe is today's index members) and built a control to measure it. My objections are about how much weight the stock-level numbers can carry before the mid-1980s, which is the period that decides the question. I think they can carry very little, and the report should lean on B's cross-checks and margin work, not on the B1-B5 return figures.

## What I recomputed

| | B reports | I get |
|---|---|---|
| B5 (high yield 30), net, 1.6x, T-bill + 1%, 1976-2025 CAGR | 19.8% | 19.8% ($1 to $8,286) |
| B5 gross, same | 20.3% | 20.3% |
| B1 (low volatility), net, same | 13.7% | 13.7% |
| B3 (high yield, low volatility), net, same | 15.3% | 15.3% |
| C1 control (large half of survivors, no screen), gross, same | 18.8% | 18.8% |
| Survivorship gap, C1 minus French equal-weighted top 30% by size, mean per year | 2.27% | 2.27% |
| B5's 30 names, re-selected from the raw bars with my own code, for 1977, 1990, 2008, 2020 | | 30, 30, 29 and 30 of 30 match |

My method for the levered figures is cruder than B's (I compound B's weekly returns into months and apply `1.6 r - 0.6 (rf + 1%/12)`), and it lands on the same numbers to one decimal place. The selection rule does what the pre-registration says.

A survivorship-free version of B5, from the French dividend-yield sort (highest quintile, value-weighted) in my own framework: 12.8% unlevered; at 1.6x and T-bill + 1%, 16.3% with no cost haircut and 15.4% with 0.5%, with an 82% month-end drawdown. That supports B's statement that B5's adjusted figure (15.5%), not its raw one (19.8%), is the fair one.

## Objections

### 1. Yahoo has no dividends for about half the early universe, so early returns and early yield screens are wrong

Of the 140 tickers in B's files with prices by the end of 1973, 73 have no dividend recorded on Yahoo before 1977. For most of them the first recorded dividend is between 1984 and 1987. These are not companies that paid nothing: the list includes Bank of America, U.S. Bancorp, Weyerhaeuser, Sysco, Grainger, Target, American Express, AIG, Illinois Tool Works, Medtronic, Vulcan and many utilities. Yahoo's dividend history for them simply starts late.

Two consequences:

- **Returns are understated before the mid-1980s.** B's returns come from Yahoo's dividend-adjusted close. Where the dividend record is missing, the "total" return is a price return. Dividend yields were 4% to 6% then, so the controls C0 and C1, and any screen holding the affected names, are too low by up to that much in 1976-1986. This is the opposite sign to survivorship bias and it hides it: my recomputation of B's gap gives -0.05% a year for 1976-1998 and +4.25% for 1999-2025. I do not believe survivors had no advantage for 23 years. More likely a positive survivorship bias and a negative missing-dividend bias roughly cancelled. B's adjusted series therefore subtracts too little before 1999.
- **Yield screens select on missing data.** At the end of 1976, 56 of the 100 highest-dollar-volume stocks show a trailing dividend of zero. B5 picks the 30 highest yields from the 44 that have a record, and B3 does the same from a smaller set. B4 (dividend growers) cannot find 20 names until 1984, and the reason is the data, not the 1970s.

B's own year-by-year gaps show the problem: -14 points in 1976, -12 in 1979, -14 in 1980. A survivor universe should not lose to the full universe by that much.

### 2. The early universe is too small to call these screens

`build_log.txt` shows 48 eligible stocks for 1976 and 140 to 154 for 1977-1983. The "large half" is then 24 and about 70 to 77 names, and the rule "50 or a fifth of the large half" gives B1, B2 and B3 five stocks in 1976 (Procter & Gamble, Exxon, Johnson & Johnson, Ford, IBM) and 14 or 15 stocks until 1983. B5's "100 largest" is the whole eligible universe in 1976 and most of it until 1983. The pre-registration anticipated a small early universe, so this is not a breach of the plan. But the eight years in which Berkshire rose roughly thirty-fold are being compared with a portfolio of 5 to 15 hand-me-down survivors. The names "Low volatility 50" and "Low beta 50" should not be used for those years.

### 3. The survivorship subtraction is one number applied to very different screens

B subtracts the C1 gap, year by year, from B1, B2, B3 and B5. B's own cross-checks say this is wrong in both directions: B1 unlevered matches the survivorship-free French big-size lowest-variance cell exactly (11.3% and 11.3%), so the subtraction over-corrects B1 by about 2.5 points, while B5 beats the French highest-yield quintile by 2.5 points, about what is subtracted. B says this in the board post and names which figure is fair for which screen, which is the right way to handle it. The report should present the "fair" figure for each screen and not the uniformly adjusted column, and should not quote the "after subtraction" range of 8% to 16% as a finding. A second-order problem: the subtraction lowers the mean but leaves the path alone, so the adjusted drawdowns (72% to 86%) are artefacts.

### 4. Being in the index today is more than surviving

The universe is firms that are in the S&P 1500 now. That conditions on surviving and also on being large or successful enough to be selected. A 1976 stock that survived but shrank out of the index is excluded. The control C1 measures the combined effect for the average large stock, but a high-yield screen in 1999-2009 picks exactly the kind of stock (banks, autos, utilities) for which the difference between "survived" and "did not" was largest. B5's bias is probably larger than C1's in 2007-2009. B's comparison with SDY from 2005 (11.3% against 8.6%) is consistent with that.

### 5. The screens test "low risk and yield", not the paper's "cheap, safe, quality"

With prices and dividends only, B cannot measure book-to-market or profitability. B1 to B3 are tests of the safe leg, and B4 and B5 use dividends as a stand-in for quality and cheapness. That is a fair design given the data, and it is useful because an investor in 1976 really could have run it. But a failure of B1 to B5 is evidence about low-volatility and dividend screens. It is not independent evidence about the paper's recipe. The two builds overlap only on the low-risk leg, where they agree (B1 11.3% and B2 11.6% unlevered against 12.7% and 11.8% for the French lowest-variance and lowest-beta quintiles).

### 6. Size is measured by dollar volume

"Large" is the top half by trailing dollar trading volume, from Yahoo's split-adjusted close and volume. Volume on Yahoo is patchy before the 1980s (the log shows one or two zero-volume eligible stocks each year, and I would not trust the non-zero ones much more). Turnover-heavy stocks are also more volatile, so the "large half" is tilted away from the quiet stocks that B1 is looking for. This probably matters little after 1984.

### 7. Funds

The fund results are the cleanest numbers in B's work: real products, real fees, no survivorship among holdings. But every style fund starts in 1992 or later, after Berkshire's exceptional period. B says so. I would add that the choice of which funds to look at (VIG, SPLV, USMV, QUAL) is itself a survivor list of fund launches, and that B's finding "the plain index fund at 1.6x beat every style fund over the same weeks" is the most publishable sentence in that section.

### 8. Margin simulation

B's margin work is better than mine and I accept its conclusions. Two notes. On a call B's account sells back to the target leverage, where mine sells to 1.0x; B's is closer to what a broker does and is the gentler assumption, so B's cost of a call is if anything understated relative to mine. And the stock-screen paths are weekly closes; B shows the daily Berkshire and fund figures alongside, which is the right check.

### 9. Things I checked and have no objection to

- No look-ahead in selection: measures use data up to the last weekly close of December, and the holding period starts the week after.
- The screens, controls, leverage rule, financing scenarios and success test match the pre-registration. Amendment 1 was made before any screen was run. The extra funds are labelled post hoc.
- Trading costs by era (1%, 0.5%, 0.1% one-way) on measured turnover are more careful than my flat haircut.
- Berkshire: B's 18.9% and Sharpe 0.73 from weekly bars match my 19.0% and 0.73 from month-ends.

## What I think the joint report can use from B

- The cross-validation of the low-risk leg by an independent, investable route.
- The measured size of survivorship bias in a "today's members" backtest: 2.3 points a year for large stocks and 5.6 for all sizes, nearly all after 1998, and enough on its own to turn a fail into a pass. This is a useful warning for readers who try this at home.
- The fund comparison, with its start dates.
- The margin results, including Berkshire's own shares at 1.6x reaching an equity ratio of 0.24 in March 2009.

What it should not use: B4 and B5's raw passes, and any B1-B5 return figure for 1976-1983 as more than an illustration.
