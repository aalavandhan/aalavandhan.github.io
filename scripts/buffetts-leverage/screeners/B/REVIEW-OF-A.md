# Review of builder A's work, by builder B (sceptic)

Written 2026-11-19 after reading `A/PRE-REGISTRATION.md`, `A/FINDINGS.md` and `A/screens.py`. My recomputation is in `B/review_a.py`, with output in `B/out/review_a.txt`. It uses my own downloads of the Ken French files (byte-identical to A's) and my own parser, not A's code.

## Verdict

A's answer is "no: neither designated screen comes close, the realistic levered version reaches 15.5% to 17.0% a year against Berkshire's 21.7%". That answer is supported. I reproduce the headline numbers exactly, my stock-level screens land in the same range by a different route, and the one screen of A's that passes does not survive a reasonable change in how it is weighted. My objections below make the "no" firmer, not weaker. The one place where I think A's write-up is too kind to the screens is the margin section.

## What I recomputed

1.6x, monthly reset, Treasury bill + 1%, 0.5% a year haircut, January 1976 to December 2025.

| | A reports | I get |
|---|---|---|
| A11 (thirds of cheap, low-beta, profitable quintiles) | $2,575, 17.0% | $2,575, 17.0% |
| A10 (half big-cheap-profitable, half low-beta) | $1,339, 15.5% | $1,339, 15.5% |
| A13 (four cheap-and-profitable cells, equal weight) | $11,376, 20.5% | $11,376, 20.5% |
| Berkshire, letter table | $18,368, 21.7% | $18,368, 21.7% |

Cross-check between the two approaches, unlevered, 1976-2025: my low-volatility stock screen earns 11.3% a year against 12.7% for A2 (French lowest-variance quintile) and 11.3% for the French big-size lowest-variance cell. My low-beta screen earns 11.6% against 11.8% for A1. From April 1980 A measures Berkshire at 19.0% with a Sharpe ratio of 0.73; I get 18.9% and 0.73 from weekly bars. The two builds agree to within about a point wherever they overlap.

## Objections

### 1. The one screen that passes, A13, fails when its cells are weighted by size

A13 averages four cells of the 5x5 book-to-market and profitability sort with a quarter of the weight each. Over the sample the cheapest-and-most-profitable cell holds a median of 30 firms (minimum 11) and a median of 4% of the four cells' combined market value, but it gets 25% of the portfolio. Weighting the same four cells by their market value, which is what an investor of any size would have to do:

| A13 at 1.6x, T-bill + 1%, 0.5% haircut | 1976-2025 | $1 grows to | Share of Berkshire's wealth |
|---|---|---|---|
| Equal weight across the four cells (A's definition) | 20.5% | $11,376 | 62% |
| Weighted by number of firms | 20.0% | $9,044 | 49% |
| Weighted by cell market value | 18.4% | $4,703 | 26% |

On A's own test (at least half of Berkshire's wealth) the market-value version fails clearly and the firm-count version fails narrowly. A already declined to recommend A13 on four grounds. This is a fifth, and I think the strongest: the pass is produced by overweighting a cell that holds a twenty-fifth of the money. The report should say that no screen passes once A13 is weighted sensibly, not that one of thirteen passes.

### 2. A's margin rule sells every December, so it understates what "not selling" costs

A's rule M-B resets leverage to target at the end of each December in both directions. After a bad year that is a large voluntary sale. In December 2008 the account sells after a 37% fall, and in December 2000 and 2001 it sells again. A then reports that "at 1.6x no screen breached 30%" at month ends and that A11 "touched 43%".

A borrower who behaves like Berkshire does not sell in December either. I ran A's screens with the same haircut and financing, borrowing back up to target each December but never selling unless called, still with month-end checks only:

| 1.6x, never sell, month-end checks | Lowest equity ratio | Calls under a 30% rule | $1 grows to (with rule) | A's monthly-reset figure |
|---|---|---|---|---|
| A11 | 0.28, February 2009 | 1 (February 2009) | $2,066 | $2,575 |
| A10 | 0.28, February 2009 | 1 (February 2009) | $1,116 | $1,339 |
| A13 (A's weights) | 0.25, February 2016 | 2 (February 2009, February 2016) | $6,396 | $11,376 |
| A3 cheap quintile | 0.08, February 2009 | 1 (November 2008) | $6,300 | $5,303 |
| Market (with the haircut) | 0.09, February 2009 | 2 (September 2002, February 2009) | $377 | $808 |

So both designated screens are called at 1.6x in February 2009 even on month-end data, and the market is called in 2002 as well, which A's rule never sees because the December resets had already cut the loan. On daily data (my `out/margin.txt`) the never-sell market account at 1.6x is called on 19 July 2002 and 20 November 2008, and the cheap quintile on 12 November 2008 and 18 March 2020. A's daily table catches 2008 and 2020 but not 2002, for the same reason.

The sentence in A's findings that needs changing is "At 1.6x no screen breached 30%". It is true only for an account that deleverages every December. The honest statement is that at 1.6x the designated screens are called once, near the low of 2008-09, if the investor tries to hold through.

### 3. The window split at 2011/2012 hides how front-loaded the gap is

A splits at the end of the paper's sample. Splitting where Berkshire's own record changes character gives a starker picture:

| 1.6x, T-bill + 1%, 0.5% haircut | 1976-1998 | 1999-2025 |
|---|---|---|
| Berkshire | 38.2% | 9.2% |
| A11 | 23.8% | 11.5% |
| A10 | 23.7% | 8.9% |
| A13 (A's weights) | 31.7% | 11.7% |
| Market | 19.3% | 10.3% |

In the 23 years in which Berkshire was built, the designated screens trail by 14 points a year. In the 27 years since, A11 beats Berkshire and so does the levered market. A's table shows a gap of 8 to 9 points for 1976-2011, which is an average of those two very different regimes. The report should show both splits.

### 4. The stand-in used for A11 in the daily margin test leaves out its safest third

French publishes no daily beta-sorted file, so A tests a half-cheap, half-profitable mix on daily data and labels it the nearest stand-in for A11. A11 is one third low beta, and that third is what keeps A11's lowest ratio above the cheap quintile's. The stand-in therefore overstates A11's daily stress somewhat. This cuts against my objection 2, and I mention it for balance. My weekly low-beta stock screen fell 38% in 2008-09 against 55% for the index fund, which suggests the true A11 daily path lies between A's stand-in and the profitable quintile. It would still have been at about 0.28 or below in early 2009.

### 5. Costs are flat, but turnover is not

A notes that A2 (low variance) is re-formed every month and that A13's cells are small. The same 0.5% a year is charged to all thirteen screens and to the blends, which are also rebalanced monthly between their parts. My stock screens, rebalanced once a year at 28% to 37% one-way turnover, lose 0.3 to 0.5 points a year at the cost levels I assumed, so 0.5% is fair for the annual sorts on large stocks and too low for A2 and A13. This does not change the verdict because neither is a designated screen, but the "median 16.2%" across thirteen is a little generous.

### 6. Drawdowns are month-end for the screens and compared with a month-end Berkshire

A reports Berkshire's worst drawdown as 44% from month-end data. On daily closes it is 51.5% (the 2017 letter says 50.7%). The screens' 67% is also month-end and would be deeper daily. The comparison is like for like, so this is a labelling point: the report should give Berkshire's fall as about 51% and say the screen figures are month-end.

### 7. Things I checked and have no objection to

- Look-ahead: the French sorts use June formation with prior-year accounting data, as A states. The portfolios include delisted firms, so there is no survivorship bias of the kind that affects my stock universe.
- The cells used for A7, A8, A9 and A13 match the pre-registered sentences.
- The Berkshire series: A's April 1980 to 2025 figures match mine from an independent download.
- The designation of A10 and A11 before running, and the reporting of all thirteen, were done as promised. The one amendment is procedural.
- A's point that profitability and investment sorts were unknown to an investor in 1976 is correct and should stay in the report.

## What the joint report can claim

Supported by both builds: a simple long-only screen at 1.6x, financed at Treasury bills plus 1% and charged modest costs, compounded at about 14% to 17% a year over 1976-2025 against Berkshire's 21.7%, ending with roughly a tenth of Berkshire's wealth. The shortfall is all in 1976-1998. The screens match Berkshire's Sharpe ratio from 1980 but not its return, and a margin account running them at 1.6x would have faced a call in 2008-09 unless it held only the lowest-risk stocks or sold on the way down.

Not supported: any statement that a screen "passes". A13 passes only with weights no real portfolio could hold, and my two raw passes (high yield, dividend growers) come from the survivor universe.
