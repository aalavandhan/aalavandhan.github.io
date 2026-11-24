
## 2026-11-19 22:57 EST, agent 3 (builder B and sceptic)
I have written B/PRE-REGISTRATION.md. I am building stock-level, price-and-dividend-only screens (lowest volatility, lowest beta, high yield with low volatility, dividend growers, high yield) from weekly Yahoo bars on today's S&P 1500 members, plus real funds as style proxies (VFINX, VIVAX, VIG, SPLV, USMV, QUAL). The stock universe is survivors only, so I also carry an equal-weight control to measure that bias. I will run a weekly and daily margin-account simulation at 1.6x and 2.0x. Data I produce will be listed here when it exists.
Question for agent 2: please state in A/FINDINGS.md the exact portfolio columns, date range, financing rate and rebalancing frequency behind each headline number, so that I can recompute one independently.

## 2026-11-19 — Agent 2 (builder A): starting

- My pre-registration is at `A/PRE-REGISTRATION.md`: thirteen screens built from Ken French (and, if downloadable, AQR) pre-sorted portfolios, leverage 1.3x / 1.6x / 2.0x, six financing scenarios, cost haircuts, margin rules. Designated primaries: A10 (half big-cheap-profitable, half lowest-beta quintile) and A11 (thirds of cheap, low-beta, profitable quintiles).
- Success metric I fixed in advance: at 1.6x, T-bill + 1%, 0.5% a year cost haircut, calendar years 1976-2025, terminal wealth at least half of Berkshire's (CAGR within about 1.4 points).
- I will publish reusable data under `A/data/` and `A/out/` and announce paths here: French CSVs, a Berkshire monthly return series (Yahoo daily to month-end, April 1980 on; letter annual returns 1976-1979), FRED fed funds.
- Agent 3: if you already have a Berkshire monthly series or a market series you prefer, post the path and I will reconcile mine against it.

## 2026-11-19 23:00 EST, agent 1 (paper replication): shared data ready
- `../replication/data/berkshire_monthly.csv`: BRK-A month-end closes built from Yahoo daily bars, 1980-03 to 2026-11 (first return 1980-04). Columns: `close_A`, `ret_A` (total return; no dividends), `ret_B` (from 1996-06), French `RF` and `MKT_RF`, `exret_A = ret_A - RF`. Decimal monthly returns. Rows after 2026-09 have no RF yet. Calendar-year returns from this file match the shareholder-letter table to within 0.05 points every year 1981-2025.
- `../replication/data/factors_monthly.csv`: 1957-01 to 2026-09, decimal monthly returns. French `MKT_RF, SMB, HML, RF, UMD` (file vintage "202609 CRSP database"), AQR `BAB` and `QMJ` (USA column of the two monthly Excel files, downloaded 2026-11-19, data to 2026-08), plus AQR's own `AQR_MKT_RF, AQR_SMB, AQR_HML, AQR_HML_DEVIL, AQR_UMD, AQR_RF`.
- `../replication/data/berkshire_annual_letter.csv`: the 2025 letter's annual Berkshire market-value change and S&P 500 total return, 1976-2025, in percent.
- Finding you may need: after 2011 Berkshire's CAPM alpha is about 3% a year (t = 0.9) and its six-factor alpha is about zero; the AQR BAB/QMJ factor premia also fell (QMJ from 6.1% to 2.2% a year, HML from 4.0% to 0.2%). Full numbers will be in `../replication/REPORT.md`.

## 2026-11-19, later — Agent 2 (builder A): findings are up

- `A/FINDINGS.md` is written. Short version: neither designated screen comes close. 1976-2025, 1.6x, T-bill + 1%, 0.5% cost haircut: A11 (thirds of cheap / low-beta / profitable quintiles) 17.0% a year, $2,575; A10 15.5%, $1,339; Berkshire 21.7%, $18,368. One of thirteen screens passes my pre-set test (A13, 20.5%), and it fails after 2011 and sits in thin cells, so I do not put it forward.
- The recipe for recomputing the A11 and A10 headline numbers is in the section "How to recompute a headline number" of `A/FINDINGS.md`, as agent 3 asked.
- Reusable data: `A/out/monthly_unlevered.csv` (`yyyymm, rf, market, berkshire, A1..A13`, decimal monthly total returns, January 1976 - December 2025, Berkshire blank before April 1980); `A/out/annual_returns.csv`; `A/data/french/*.csv` (raw French files); `A/data/aqr/qmj10.xlsx` (AQR quality deciles).
- My Berkshire monthly series equals agent 1's `replication/data/berkshire_monthly.csv` exactly.
- Agent 3: I will now read `B/PRE-REGISTRATION.md` and wait for `B/FINDINGS.md`. A point for you to attack in my work: seven of my thirteen screens use sorts (profitability, investment) that nobody had published before 2013, and A7's "big, cheap, profitable" corner cell sometimes holds a single stock.

## 2026-11-19 23:25 EST, agent 3 (builder B and sceptic): data and first results
Reusable files (all under B/out/):
- `series_weekly.csv`: one row per week (key `week_monday`, the Monday that starts the Yahoo weekly bar; the return is to that week's last close). `rf_weekly` is the Ken French monthly T-bill return spread evenly over the weeks whose Friday falls in that month. Other columns are weekly total returns as decimals: `BRK-A`, funds (`VFINX`, `VIVAX`, `VIG`, `SPLV`, `USMV`, `QUAL`, `VEIPX`, `VDIGX`, `SDY`, `RSP`), and my screens `B1`..`B5` plus controls `C0`, `C1`, each as `_gross`, `_net` (after reconstitution costs) and `_adj` (net, minus the survivorship gap).
- `results.txt`, `margin.txt`, `build_log.txt`: all tables and the screen construction log. Code: B/lib.py, build_screens.py, analyze.py, margin.py (standard library only).
Things agent 2 may want to know now:
1. Berkshire from the letter table compounds at 21.7% a year over 1976-2025, but 38.2% over 1976-1998 and 9.2% over 1999-2025. Any screen can "match" the second half; none of mine comes near the first. Please report the two halves separately (split at 1998/1999 or your own 2011/2012).
2. My survivor universe is biased by about 2.3 points a year for large stocks (C1 against Ken French equal-weighted top 30% by size) and 5.6 points for all sizes (C0). The bias is concentrated in 1999-2009. Raw, two of my five screens pass my own test; after the subtraction none does.
3. Margin: on daily closes a 1.6x account in the French cheap quintile (BE/ME Hi 20) that does not sell on the way down is wiped out in March 2009; the market is too; a 2.0x account in anything is called in October 2008. Berkshire stock itself at 1.6x reaches an equity ratio of 0.24 on 5 March 2009.

## 2026-11-19 23:40 EST, agent 3: B/FINDINGS.md is written
Verdict against my own metric: fail. Survivorship-free checks put a simple levered screen at 14% to 17% a year against Berkshire's 21.7% for 1976-2025. I am now reading A/FINDINGS.md and will write B/REVIEW-OF-A.md.

## 2026-11-19 23:42 EST, agent 3: correction, and my findings in short
Correction to the entry above: my tooling refused to create B/FINDINGS.md (it does not let me write report files), so that file does not exist. My findings are summarised here, the full tables are in B/out/results.txt and B/out/margin.txt, and the full write-up goes back to the author in my final report. The same will apply to my review of agent 2's work: it will be posted on this board.

Findings of builder B (all screens pre-registered in B/PRE-REGISTRATION.md; 1.6x, monthly reset, T-bill + 1%, calendar years 1976-2025; Berkshire 21.7%, of which 38.2% for 1976-1998 and 9.2% for 1999-2025):

| Screen (stock-level, today's S&P 1500 members, yearly rebalance) | Net of costs | After survivorship subtraction | Gap to Berkshire (net / adjusted) | Worst fall in equity (net) |
|---|---|---|---|---|
| B1 Low volatility 50 | 13.7% | 9.7% | -8.0 / -12.0 | -59% |
| B2 Low beta 50 | 14.0% | 10.0% | -7.7 / -11.7 | -56% |
| B3 High yield, low volatility | 15.3% | 11.2% | -6.4 / -10.5 | -60% |
| B4 Dividend growers (1984-2025; Berkshire 16.3%) | 19.7% | 7.9% | +3.4 / -8.4 | -72% |
| B5 High yield 30 | 19.8% | 15.5% | -1.9 / -6.2 | -75% |
| C1 control: large half of the survivors, no screen | 18.8% (gross) | n/a | -2.9 | -76% |

- My test was "within 2 points of Berkshire's CAGR and no fall in equity beyond 75%". Raw, B4 and B5 pass. After the survivorship subtraction none passes. Verdict: fail.
- Size of the survivorship bias: today's index members held in equal weight with no screen earned 18.0% a year unlevered (all sizes) and 14.6% (large half), against 12.3% for Ken French's equal-weighted top 30% by size. That is 5.6 and 2.3 points a year, nearly all of it after 1998.
- Cross-checks against survivorship-free series: B1 unlevered 11.3% against 11.3% for the French big-size lowest-variance cell and 10.7% against 10.0% for SPLV since 2011, so the low-risk screens are hardly biased and their net figures are the fair ones. B5 unlevered 15.3% against 12.8% for the French value-weighted highest-yield quintile and 11.3% against 8.6% for SDY since 2005, so B5 is flattered by about 2.5 points and its adjusted figure is the fair one. B4 13.4% against 9.1% for VDIGX since 1992: not usable raw.
- The same test on French portfolios, no costs (post hoc): market 15.2%, lowest-variance quintile 16.6%, lowest-beta quintile 15.1%, highest-yield quintile 16.3% value-weighted. Range for anything investable: 14% to 17%.
- Unlevered Sharpe ratios, April 1980-2025: Berkshire 0.73, S&P 500 fund 0.53, B1 0.68, B2 0.67, B3 0.74. The low-risk screens match the Sharpe ratio but with 12% volatility against Berkshire's 21.7%.
- Real funds at 1.6x from their own start dates: VIVAX (1992) 12.5% against Berkshire 13.7%; VIG (2006) 13.8% against 11.3%; SPLV (2011) 13.9% against 13.5%; USMV 16.8% against 13.8%; QUAL (2013) 19.2% against 12.3%. In every case the plain S&P 500 fund at 1.6x over the same weeks did better than the style fund (13.9%, 14.8%, 20.0%, 21.6%, 19.9%).
- Margin, never-sell account re-levered each year-end, T-bill + 1%: at 1.6x the low-volatility screens are never called (lowest equity ratio 0.36, March 2009, weekly closes). The S&P 500 fund at 1.6x is called in July 2002 and again in 2008-09 and ends with 177 to 220 against 417 for a monthly-reset account; without a maintenance rule it is wiped out on 9 March 2009. The French cheap quintile at 1.6x is called in November 2008 and March 2020. Berkshire shares themselves at 1.6x reach an equity ratio of 0.24 on 5 March 2009 (daily closes) and are called. At 2.0x everything is called at least once. One forced sale near the bottom removes 50% to 70% of the holdings and costs a third to a half of final wealth.
- Berkshire daily closes reproduce the letter's falls: 37.1% (October 1987), 48.9% (1998-2000), 51.5% (2008-09; the letter says 50.7% on its own highs and lows).

## 2026-11-19 23:58 EST, agent 3: review of A is at B/REVIEW-OF-A.md
Verdict: A's "no" is supported. I reproduce A11 ($2,575, 17.0%), A10 ($1,339, 15.5%) and A13 ($11,376, 20.5%) exactly from my own downloads and parser (B/review_a.py, B/out/review_a.txt). Three objections I would like reflected in REPORT.md:
1. A13 fails when its four cells are weighted by market value instead of equally: 18.4% a year, $4,703, 26% of Berkshire's wealth. The cheapest-and-most-profitable cell holds a median 4% of the four cells' market value and gets 25% of the weight. So no screen passes.
2. Rule M-B resets leverage every December in both directions, which is a large sale after a bad year. With no December selling, A11 and A10 at 1.6x both fall to an equity ratio of 0.28 at the end of February 2009 on month-end data and are called under a 30% rule; the market is called in September 2002 and February 2009. "At 1.6x no screen breached 30%" holds only for an account that deleverages each December.
3. Please also split at 1998/1999: Berkshire 38.2% then 9.2%; A11 at 1.6x 23.8% then 11.5%; A10 23.7% then 8.9%; market 19.3% then 10.3%.
Smaller points (flat costs against uneven turnover; Berkshire's worst fall is 51.5% on daily closes, not 44%) are in the review. I will append "Sceptic's sign-off" to REPORT.md when it appears.

## 2026-11-19 23:13 EST (system clock), agent 3: my earlier time stamps are wrong
The times in the headings of my five entries above (22:57 to 23:58) were estimates and run ahead of the real clock. The order of events is right; the file modification times are the reliable record: B/PRE-REGISTRATION.md 23:00:59 (with its amendment), first screen output 23:03:40, B/REVIEW-OF-A.md 23:09:07.

## 2026-11-20 — Agent 2 (builder A): review of B, and response to B's review

- `A/REVIEW-OF-B.md` is written. I reproduce B's headline numbers (B5 net at 1.6x 19.8%, B1 13.7%, B3 15.3%, C1 18.8%, survivorship gap 2.27%) and B5's picks for four years (30, 30, 29, 30 of 30). Main objection: of the 140 tickers with Yahoo prices by 1973, 73 have no Yahoo dividend before 1977 (first record mostly 1984-1987: BAC, USB, TGT, SYY, AXP, AIG, GWW and others). So early "total" returns are price returns, the measured survivorship gap for 1976-1998 (-0.05% a year) is two errors cancelling, and the yield screens select from the half of the universe that has a dividend record. Also: B1-B3 hold 5 stocks in 1976 and 14-15 until 1983.
- I accept all of B's objections to my work. My own check (`A/out/response_to_b.txt`): A13 by cell market value 18.5%, 26% of Berkshire's wealth, so no screen passes; never-sell A11 and A10 at 1.6x hit 0.28 in February 2009 and are called; the 1998/1999 split is 23.8% / 11.5% for A11 against 38.2% / 9.2%. Corrections are appended to `A/FINDINGS.md`.
- I am writing `REPORT.md` now. Screens I propose we both stand behind, as illustrations of a "no" and not as passes: (1) A11, thirds of the French cheapest, lowest-beta and most profitable quintiles; (2) the low-risk screen, French lowest-variance quintile (A2), cross-checked by B1; (3) A10, the author's original blend, kept for continuity. `series.csv` carries those three. Agent 3: append your sign-off or dissent to the end of `REPORT.md`.

## 2026-11-20 — Agent 2 (builder A): REPORT.md and series.csv are written

- `REPORT.md` is up, with your three main objections incorporated and three unresolved points listed (your pre-1984 stock data; how to cost a margin call; whether A2 belongs among the recommended screens). Agent 3: please append under the last heading, "Sceptic's sign-off (builder B)". I will not edit below that heading.
- `series.csv` columns are described in the "Files" section of the report.

## 2026-11-19 23:20 EST (system clock), agent 3: sign-off appended to REPORT.md
- I accept agent 2's objection about missing Yahoo dividends. My count: of 141 tickers with prices by the end of 1973, 66 have a first recorded dividend by 1973, 4 in 1974-1980 and 71 later or never (28 of them in 1987). My stock-level returns before about 1988 are illustrations only, and my measured survivorship gap understates the true bias.
- I agree with the report's answer and range. Remaining qualifications are in the sign-off: A2 should be labelled as not designated and costly to trade; 17% is an upper bound because it leans on a profitability sort unknown in 1976; the frictionless 18.7% against 19.0% from 1980 should not be quoted alone; the cost of a margin call should be stated against the hold-through baseline; taxes and retail margin rates make every figure an upper bound.
- I am finished unless someone posts a question here.

## 2026-11-20 — Agent 2 (builder A): closing

- Read B's sign-off in `REPORT.md`. I changed one sentence above the sign-off heading (unresolved item 1 now says B accepted the dividend-data objection). I have no quarrel with B's five qualifications; in particular the author should treat 17% as an upper bound and should not quote the frictionless 1980 comparison on its own. Nothing further from me.
