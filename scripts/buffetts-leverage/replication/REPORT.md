# Replicating "Buffett's Alpha" (Frazzini, Kabiller, Pedersen, NBER WP 19681) with free data

Written 2026-11-19. Every number in the "mine" columns comes from the scripts in this folder and is saved in `results/`. Numbers in the "paper" columns are copied from the working paper's text and tables. Nothing was tuned to match: each method was written down in the script before it was run, and where a diagnostic suggested a different choice would match better (see the September 2011 note in section 1), the headline number was left alone and the diagnostic is reported separately.

## The short version

- The Berkshire return series is right. Five-year average excess returns for 1981-2005 match the paper to within 0.4 points, and the 1998-2000 drawdown matches to the decimal.
- The full-sample statistics come out a little lower than the paper's (Sharpe 0.72 against 0.76, alpha 10.1% against 12.1%). The reason is that free monthly prices start in April 1980, so the 41 strongest months of the paper's sample (November 1976 to March 1980) are missing. This is a data gap, not a disagreement.
- The paper's central regression result reproduces in shape: adding BAB and QMJ cuts the four-factor alpha by a bit more than half and makes it statistically insignificant, and both new factors load significantly.
- The systematic Buffett-style portfolio reproduces closely (Sharpe 1.15 against 1.14, correlation with Berkshire 0.49 against 0.47).
- After 2011 Berkshire's alpha is statistically indistinguishable from zero under every specification, including the plain market model. Its Sharpe ratio (0.76) was below the market's (0.93).
- The 13F and private-holdings columns, and the comparison with all stocks and mutual funds, could not be attempted with free data.

## Summary table

"Mine" uses monthly data from April 1980 to December 2011 (381 months) unless the sample column says otherwise. The paper's sample is November 1976 to December 2011.

| # | Paper result | Paper | Mine | My sample | Verdict | Reason |
|---|---|---|---|---|---|---|
| 1a | Berkshire average excess return | 19.0% | 17.1% | 1980-04 to 2011-12 monthly | Close | 41 early, very strong months are missing. A bridged estimate for 1977-2011 is about 18.1%. |
| 1b | Berkshire volatility | 24.9% | 23.6% | same | Close | Same gap. |
| 1c | Berkshire Sharpe ratio | 0.76 | 0.72 | same | Close | Same gap. |
| 1d | Market beta | 0.68 (text: 0.7) | 0.64 | same | Close | Same gap. |
| 1e | Information ratio | 0.66 | 0.59 | same | Close | Same gap. |
| 1f | Same statistics from annual data | 19.0% / 24.9% / 0.76 / 0.68 / 0.66 | 20.8% / 29.9% / 0.69 / 0.85 / 0.56 | 1977-2011, 35 calendar years from the letters | Not comparable | Annual arithmetic means and volatilities are not the same quantities as annualised monthly ones. |
| 1g | Market excess return, volatility, Sharpe | 6.1% / 15.8% / 0.39 | 6.5% / 15.9% / 0.41 | 1976-11 to 2011-12 (full paper window) | Close | Ending in September 2011 gives 6.2% / 15.8% / 0.39. |
| 1h | Sub-period excess returns 1981-85, 86-90, 91-95, 96-00, 01-05 | 28.6 / 17.3 / 29.7 / 14.9 / 3.2% | 29.0 / 17.3 / 29.7 / 14.9 / 3.2% | same five buckets | Reproduced | Largest gap 0.4 points. |
| 1i | Sub-period 2006-2011 | 3.3% | 4.4% | 2006-01 to 2011-12 | Not reproduced | Ending in September 2011 gives 3.2%; the paper's data probably stop there. |
| 1j | Sub-period 1976-1980 | 42.1% | not available | | Not attempted | No monthly prices before April 1980. |
| 1k | Drawdown June 1998 to February 2000 | -44%, market +32%, shortfall 76% | -43.8%, +32.2%, 76.0% | month-end closes | Reproduced | |
| 1l | $1 in November 1976 becomes more than $1,500 by end 2011 | > $1,500 | $1,221 from end of December 1976 | letters and Yahoo | Not testable | November and December 1976 are missing; the claim needs a gain of at least 23% in those two months. |
| 2a | Four-factor alpha (t) | 12.1% (3.19) | 10.1% (2.68) | 1980-04 to 2011-12 | Close | Missing early months. |
| 2b | Alpha after adding BAB | 9.2% (2.42) | 7.6% (2.02) | same | Close | |
| 2c | Alpha after adding BAB and QMJ | 6.3% (1.58) | 4.1% (1.02) | same | Close | Insignificant in both. Mine falls 60% from the four-factor alpha; the paper's falls 48%. |
| 2d | BAB loading (t), five- and six-factor | 0.37 (3.61), 0.29 (2.67) | 0.35 (3.96), 0.29 (3.24) | same | Reproduced | |
| 2e | QMJ loading (t) | 0.43 (2.34) | 0.47 (2.46) | same | Reproduced | |
| 2f | MKT loading, three specifications | 0.84 / 0.83 / 0.95 | 0.79 / 0.79 / 0.92 | same | Close | |
| 2g | SMB loading, three specifications | -0.32 / -0.32 / -0.15 | -0.38 / -0.40 / -0.24 | same | Close | Same sign and pattern, more negative. |
| 2h | HML loading, three specifications | 0.63 / 0.38 / 0.46 | 0.41 / 0.19 / 0.31 | same | Not reproduced | Same sign, about 0.2 lower throughout. Sample or factor vintage; I cannot tell which. |
| 2i | Adjusted R2 | 0.25 / 0.27 / 0.28 | 0.25 / 0.28 / 0.29 | same | Reproduced | |
| 2j | SMB loading positive in the first half of the sample | "positive (not shown)" | +0.18 (t = 0.9) 1980-95; -0.52 (t = -4.8) 1996-2011 | four-factor model | Reproduced | Sign reproduces; the early loading is not significant. |
| 3a | Buffett-style portfolio excess return, Sharpe, information ratio | 28.2% / 1.14 / 1.07 | 27.2% / 1.15 / 1.06 | 1980-04 to 2011-12, in-sample weights | Reproduced | |
| 3b | Correlation with Berkshire | 0.47 | 0.49 | same | Reproduced | |
| 3c | Berkshire regressed on the style portfolio: alpha (t) | 5.6% (1.44) | 3.7% (0.97) | same | Close | Insignificant in both. |
| 3d | Style portfolio regressed on Berkshire: alpha (t) | 19.3% (5.07) | 18.9% (5.05) | same | Reproduced | |
| 3e | Style portfolio leverage | 3.73 | not defined | | Not attempted | The paper never says how this is computed. My volatility scale factor is 2.69. |
| 3f | Appendix C, out-of-sample style portfolio: excess, volatility, Sharpe | 39.3% / 30.9% / 1.27 (1981-2011) | 36.1% / 30.5% / 1.18 | 1985-04 to 2011-12 | Close | My first out-of-sample month is later because my data start later. |
| 3g | Appendix C correlation; alphas both ways | 0.42; 3.7% (0.88); 30.4% (5.81) | 0.41; 3.0% (0.68); 28.4% (5.18) | same | Reproduced | |
| 3h | Long-only top-50 style portfolio | 7.0% excess, Sharpe 0.45 | | | Not attempted | Needs stock-level factor weights (CRSP and Compustat). |
| 4a | Table 3 cost of float, 1981-85, 1986-90, 1991-95 | 10.95 / 3.07 / 2.21 | 10.95 / 3.07 / 2.21 | letters | Reproduced | |
| 4b | Table 3, 1996-2000 | 2.36 | 2.00, or 2.35 if 1998 is set to zero | letters | Close | Depends on how one treats 1998, a small underwriting profit with no cost printed. |
| 4c | Table 3, 2001-05 and 2006-11 | 1.29 / -4.00 | 1.27 / -4.11 | letters | Close | |
| 4d | Table 3, 1976-1980 | cost 1.67, 79% of years negative | cost 0.00, 100% negative | letters | Not reproduced | The letters' float table shows "less than zero" for every year 1976-80. |
| 4e | Table 3, full sample cost and spread to T-bills | 2.20, -3.09 | 2.02 to 2.07, -3.37 to -3.32 | 1976-2011 | Close | The gap is the 1976-80 row. |
| 4f | Leverage, total assets measure | 1.6 (Table 2: 1.64) | 1.66 | 1996-2011 year-ends | Close | Different window; balance sheets before 1995 were not collected. |
| 4g | Leverage, debt plus float | 1.4 | 1.45 | 1997-2011 year-ends | Close | Different window. |
| 4h | Leverage, volatility ratio | 1.4 | arithmetic only: 24.8 / 17.2 = 1.44 | paper's own inputs | Not attempted | Needs the 13F portfolio's volatility. |
| 4i | Float as a share of liabilities | 36% | 37% | 1997-2011 | Close | Different window. |
| 5a | Table 4, 13F portfolio columns | alpha 5.3% falling to 0.3% | | | Not attempted | Needs Thomson 13F history from 1980 and CRSP returns including delisted stocks. |
| 5b | Table 4, private holdings columns | alpha 5.6% to 4.9% | | | Not attempted | Built from 5a plus monthly balance sheet data. |
| 5c | Table 1, Figures 1 and 2 (rank among all stocks and funds) | top Sharpe among stocks with 30-year history | | | Not attempted | Needs the complete CRSP stock file and the CRSP mutual fund file, including dead securities. |
| 6 | Extension, 2012-01 to 2026-08/09 | not in paper | CAPM alpha 3.0% (t = 0.9); six-factor alpha -0.5% (t = -0.1); Sharpe 0.76 against market 0.93 | 176-177 months | New result | See section 6. |

## 1. Berkshire's track record (Table 2, Section 3)

**Method.** Month-end closing prices of BRK-A were built from Yahoo's daily bars (the monthly interval is truncated, so daily bars were used). Berkshire has never paid a dividend in this period, so the price return is the total return; Yahoo's adjusted and unadjusted closes are identical. Excess return is the monthly return minus Ken French's one-month T-bill return. The market is French's Mkt-RF. Average excess return is the monthly mean times 12, volatility is the monthly standard deviation times the square root of 12, beta and alpha come from a regression on the market, and the information ratio is the annualised alpha divided by the annualised residual volatility. These are the paper's definitions.

**Check on the price series.** Calendar-year returns computed from the Yahoo month-ends agree with the "annual percentage change in per-share market value" table in the 2025 shareholder letter to within 0.05 points in every year from 1981 to 2025.

**Results, monthly.**

| | 1980-04 to 2011-12 | Paper, 1976-11 to 2011-12 | 2012-01 to 2026-09 | 1980-04 to 2026-09 |
|---|---|---|---|---|
| Months | 381 | 422 | 177 | 558 |
| Average excess return | 17.1% | 19.0% | 12.5% | 15.6% |
| Volatility | 23.6% | 24.9% | 16.4% | 21.6% |
| Sharpe ratio | 0.72 | 0.76 | 0.76 | 0.72 |
| Beta | 0.64 | 0.68 | 0.71 | 0.66 |
| CAPM alpha (t) | 12.5% (3.28) | not printed | 3.0% (0.86) | 9.6% (3.40) |
| Idiosyncratic volatility | 21.3% | 22.4% | 12.8% | 19.0% |
| Information ratio | 0.59 | 0.66 | 0.23 | 0.51 |
| Market excess return | 7.1% | 6.1% | 13.4% | 9.1% |
| Market Sharpe ratio | 0.45 | 0.39 | 0.93 | 0.59 |

**The missing 41 months.** Yahoo's first BRK-A bar is 17 March 1980. The paper's sample starts in November 1976, and the missing stretch was Berkshire's best: the letters give calendar-year gains of 46.8%, 14.5% and 102.5% for 1977-79. I did not find a free monthly price source for those years.

Two partial substitutes are reported, and neither is a replacement.

- *Annual data from the letters.* Over the 35 calendar years 1977-2011 the average annual excess return is 20.8%, the standard deviation of annual excess returns is 29.9%, the Sharpe ratio is 0.69, the beta against French's annual market return is 0.85 and the information ratio is 0.56. Including calendar 1976 (a 129% year, of which the paper's sample covers only the last two months) gives 23.7% / 34.2% / 0.69 / 0.99 / 0.54. These should not be set against the paper's numbers. An arithmetic mean of annual compounded returns is larger than twelve times a monthly mean, annual volatility is larger than scaled monthly volatility when returns are this skewed, and a 35-observation beta is imprecise. As a calibration: over 1981-2011, where both exist, the annual method gives 18.2% / 28.6% / 0.64 and the monthly method gives 16.0% / 23.5% / 0.68.
- *A bridged estimate.* The letter returns and the Yahoo closes pin down the price at the end of December 1976 ($94.0) and at the end of March 1980 ($260), so the average monthly log return over those 39 months is known exactly (2.61% a month). Converting that to an arithmetic mean needs an assumption about monthly volatility. Assuming 8% a month (the 1980-85 sample value is 7.5%), the average excess return for January 1977 to March 1980 was about 28% a year, and the average for January 1977 to December 2011 was about 18.1%. With assumed volatility between 6% and 10% the answer moves between 17.9% and 18.3%. This is an estimate with a stated assumption, saved in `results/diag_bridge_1977_1980.csv`. It still excludes November and December 1976.

The same arithmetic says the paper's 42.1% for 1976-1980 requires Berkshire's excess return to have summed to roughly 40% over November and December 1976. I cannot check that. It is not implausible given that the stock rose 129% in calendar 1976, and it is consistent with the paper's "more than $1,500" claim, which needs at least a 23% gain in those two months on top of the $1,221 multiple I get from December 1976.

**Sub-periods.**

| Period | Berkshire, mine | Berkshire, paper | Market, mine | Market, paper |
|---|---|---|---|---|
| 1981-1985 | 29.0% | 28.6% | 4.9% | 4.3% |
| 1986-1990 | 17.3% | 17.3% | 5.7% | 5.4% |
| 1991-1995 | 29.7% | 29.7% | 12.6% | 12.0% |
| 1996-2000 | 14.9% | 14.9% | 12.1% | 11.8% |
| 2001-2005 | 3.2% | 3.2% | 0.9% | 1.6% |
| 2006-2011 | 4.4% | 3.3% | 2.4% | 0.7% |
| 2012-2016 | 15.9% | | 14.5% | |
| 2017-2021 | 12.8% | | 17.3% | |
| 2022-2026 (Sept) | 8.6% | | 8.3% | |

**The 2006-2011 bucket and the paper's end date.** This is the one sub-period that does not reproduce. As a diagnostic I recomputed it for every possible end month in 2011 (`results/diag_2006_2011_end_month.csv`). Ending in September 2011 gives Berkshire 3.2% and the market 0.5%, against the paper's 3.3% and 0.7%; ending in December gives 4.4% and 2.4%. October 2011 was an 11% month for the market. The full-window market statistics tell the same story: November 1976 to September 2011 gives 6.2% / 15.8% / 0.39, against the paper's 6.1% / 15.8% / 0.39, while ending in December gives 6.5% / 15.9% / 0.41. My reading is that the working paper's return data stop at the end of September 2011 even though the tables are labelled 1976-2011. I have not changed my headline sample to exploit this; had I done so, the 1980-04 to 2011-09 figures would be 16.9% / 23.6% / 0.72 / 0.64 / 0.59, which is no closer to the paper overall.

The smaller market differences in other buckets (for example 0.9% against 1.6% in 2001-05) come from the factor source. AQR's own market series gives 1.6% for 2001-05, which suggests the paper used AQR's in-house market factor and not French's; see `results/diag_market_subperiods.csv`.

**Share classes.** The paper value-weights class A and class B. I use class A only. Over the 366 months where Yahoo has both, their monthly returns have a correlation of 0.989 and differ by 0.06% a year on average, so this choice does not matter.

**Drawdown.** The month-end close fell from $78,305 (June 1998) to $44,000 (February 2000), a loss of 43.8%. French's market returned 32.2% over the same 20 months. The gap is 76.0 points. This reproduces the paper.

## 2. Factor regressions (Table 4, Berkshire stock columns)

**Method.** Ordinary least squares on monthly excess returns with conventional standard errors. MKT, SMB, HML and RF are from Ken French's three-factor file and UMD from his momentum file. BAB and QMJ are the "USA" columns of AQR's two monthly Excel files. The same months are used in all specifications within a window. A second run replaces French's four factors and risk-free rate with AQR's own versions from the same Excel files.

**Paper window, 1980-04 to 2011-12, 381 months, French factors.** t-statistics are in brackets.

| | Market only | Four-factor | + BAB | + BAB + QMJ | Paper: four-factor | Paper: + BAB | Paper: + BAB + QMJ |
|---|---|---|---|---|---|---|---|
| Alpha, annualised | 12.5% (3.28) | 10.1% (2.68) | 7.6% (2.02) | 4.1% (1.02) | 12.1% (3.19) | 9.2% (2.42) | 6.3% (1.58) |
| MKT | 0.64 (9.33) | 0.79 (10.96) | 0.79 (11.28) | 0.92 (10.60) | 0.84 (11.65) | 0.83 (11.70) | 0.95 (10.98) |
| SMB | | -0.38 (-3.67) | -0.40 (-3.90) | -0.24 (-2.05) | -0.32 (-3.05) | -0.32 (-3.13) | -0.15 (-1.15) |
| HML | | 0.41 (3.66) | 0.19 (1.55) | 0.31 (2.36) | 0.63 (5.35) | 0.38 (2.79) | 0.46 (3.28) |
| UMD | | 0.04 (0.64) | -0.04 (-0.63) | -0.09 (-1.21) | 0.06 (0.90) | -0.03 (-0.40) | -0.05 (-0.71) |
| BAB | | | 0.35 (3.96) | 0.29 (3.24) | | 0.37 (3.61) | 0.29 (2.67) |
| QMJ | | | | 0.47 (2.46) | | | 0.43 (2.34) |
| Adjusted R2 | 0.18 | 0.25 | 0.28 | 0.29 | 0.25 | 0.27 | 0.28 |

**What reproduces.** The order of the alphas, the loss of significance once BAB and QMJ are both in, the BAB and QMJ loadings and their significance, the negative size loading, the absence of a momentum loading, and the R2. The paper says the alpha "only drops by about half"; mine drops from 10.1% to 4.1%.

**What does not.** My alphas are about two points lower in every column, which is what one expects from losing 41 months in which Berkshire earned about 28% a year over bills. My HML loading is about 0.2 lower in every column. I do not know whether that is the missing months, the difference between French's HML and whatever HML the paper used, or revisions to the factors since 2013, and I have not tried to find out by experiment because that would be tuning.

**AQR's standard factors instead of French's** (`results/table4_berkshire_aqr_standard_factors.csv`): alphas of 10.9% (2.83), 8.1% (2.14) and 4.3% (1.06), BAB 0.42 and 0.33, QMJ 0.52 (2.52), HML 0.36 / 0.04 / 0.22. The conclusions are the same and the HML gap is larger, not smaller.

**The two halves of the paper window.** The paper mentions, without showing it, that the SMB loading was positive early on. In the four-factor model it is +0.18 (t = 0.87) for 1980-04 to 1995-12 and -0.52 (t = -4.81) for 1996-2011. The more striking split is in the alpha. The market-model alpha is 18.9% (t = 3.39) in 1980-1995 and 5.1% (t = 1.00) in 1996-2011. Within the paper's own sample, the statistically significant alpha comes from the first half.

**Caveat on the AQR factors.** The files say they are "an updated and extended version" of the paper's portfolios, that "there can be differences in data sources and methodology", and that AQR "reconstructs the full history each time the portfolios are updated". The QMJ definition in the 2013 working paper is not necessarily the one behind today's file. I am therefore regressing on a 2026 vintage of the factors, not the 2013 vintage.

## 3. The systematic Buffett-style portfolio (Section 7, Tables 2 and 5, Appendix C)

**Method.** Exactly as in Section 7. Beta is the slope of Berkshire's excess return on the market. The active return is the fitted value of the six-factor regression with the market loading reduced by that beta. It is rescaled so that its volatility equals Berkshire's idiosyncratic volatility, and beta times the market is added back. Everything is in excess returns. The out-of-sample version follows Appendix C: for each month, beta, the six loadings and both volatilities are estimated on all earlier months, with at least 60 required. I added one test of my own: the weights and scale estimated on 1980-04 to 2011-12 are frozen and applied to 2012 onward.

**In-sample, 1980-04 to 2011-12.**

| | Mine | Paper (1976-2011) |
|---|---|---|
| Average excess return | 27.2% | 28.2% |
| Volatility (equal to Berkshire's by construction) | 23.6% | 24.8% |
| Sharpe ratio | 1.15 | 1.14 |
| Information ratio | 1.06 | 1.07 |
| Correlation with Berkshire | 0.49 | 0.47 |
| Berkshire on style portfolio: alpha (t), loading | 3.7% (0.97), 0.49 | 5.6% (1.44), 0.47 |
| Style portfolio on Berkshire: alpha (t), loading | 18.9% (5.05), 0.49 | 19.3% (5.07), 0.47 |
| Adjusted R2 | 0.24 | 0.22 |

Sub-period excess returns of my style portfolio against the paper's: 45.2% against 54.8% (1981-85), 23.9% against 23.7%, 31.7% against 38.5%, 37.0% against 33.2%, 25.9% against 33.0%, and 4.8% against 4.7% (2006-11). The overall level matches; individual buckets differ by up to ten points, which is unsurprising given different loadings and factor vintages.

**Leverage.** Table 2 prints a leverage of 3.73 for this portfolio. The paper does not define it, and with only factor returns it cannot be computed as dollars long per dollar of capital. What I can report is that the active return had to be scaled up 2.69 times to reach Berkshire's idiosyncratic volatility, and that the resulting weights are 1.39 on the market (0.64 beta plus 0.75 active), -0.65 SMB, 0.84 HML, -0.23 UMD, 0.79 BAB and 1.26 QMJ. Each of the long-short factors is itself a dollar long and a dollar short (BAB more, because it levers its low-beta leg), so the true gross exposure is several times capital. I mark the 3.73 as not attempted, not as failed.

**Appendix C, out-of-sample.** My first out-of-sample month is April 1985; the paper's is in 1981.

| | Mine, 1985-04 to 2011-12 | Paper, 1981-2011 |
|---|---|---|
| Average excess return | 36.1% | 39.3% |
| Volatility | 30.5% | 30.9% |
| Sharpe ratio | 1.18 | 1.27 |
| Beta | 0.65 | 0.66 |
| Information ratio | 1.10 | 1.20 |
| Correlation with Berkshire | 0.41 | 0.42 |
| Berkshire on style: alpha (t), loading | 3.0% (0.68), 0.31 | 3.7% (0.88), 0.32 |
| Style on Berkshire: alpha (t), loading | 28.4% (5.18), 0.54 | 30.4% (5.81), 0.55 |

**After the paper.** With the weights frozen at their 2011 values, the style portfolio earned 27.2% a year over bills from 2012-01 to 2026-08 with a Sharpe ratio of 1.10, against 12.7% and 0.77 for Berkshire and 13.6% and 0.94 for the market. Its correlation with Berkshire rose to 0.64. Its market beta out of sample was 0.88, not the 0.64 it was built to have, and its CAPM alpha was 15.3% (t = 2.65). The expanding-window version gives nearly the same figures (26.4%, Sharpe 1.13).

These numbers need heavy discounting, more than the paper's own caution suggests. The portfolio holds 1.39 units of the market in a period when the market earned 13.6% a year, which accounts for 18.9 of the 27.2 points. BAB contributed about 5 points and QMJ about 3. The factor returns are AQR's paper portfolios with no trading costs, no shorting costs and no financing spread, and their history is rebuilt at each update. It is evidence that the factor recipe kept earning on paper, not evidence that an investor could have collected it.

## 4. Cost of float and leverage (Table 3, Section 4)

Nothing was re-collected. `float_leverage.py` reads `../float.csv` and `../leverage_cost.csv`.

**Table 3.** The rule, fixed in advance: where the letter's float table prints a cost, use it; where it prints "less than zero", use zero, as the paper's footnote says; for the years after Berkshire stopped printing that table (1998 onward), use minus the underwriting result divided by average float, which can be negative. T-bill averages are calendar-year compounded returns from French's file.

| Period | Share of years with negative cost: mine / paper | Average cost: mine / paper | Spread over T-bills: mine / paper |
|---|---|---|---|
| 1976-1980 | 1.00 / 0.79 | 0.00 / 1.67 | -7.81 / -4.59 |
| 1981-1985 | 0.20 / 0.20 | 10.95 / 10.95 | 0.62 / 1.10 |
| 1986-1990 | 0.00 / 0.00 | 3.07 / 3.07 | -3.77 / -3.56 |
| 1991-1995 | 0.60 / 0.60 | 2.21 / 2.21 | -2.09 / -2.00 |
| 1996-2000 | 0.60 / 0.60 | 2.00 (2.35 with 1998 at zero) / 2.36 | -3.18 (-2.82) / -2.70 |
| 2001-2005 | 0.60 / 0.60 | 1.27 / 1.29 | -0.86 / -0.82 |
| 2006-2011 | 1.00 / 1.00 | -4.11 / -4.00 | -5.99 / -5.84 |
| 1976-2011 | 0.58 / 0.60 | 2.02 (2.07) / 2.20 | -3.37 (-3.32) / -3.09 |
| 2012-2025 | 0.86 | -2.19 | -3.71 |

Six of the seven rows reproduce or come close. The 1976-1980 row does not: the float table in the letters shows "less than zero" for 1976, 1977, 1978, 1979 and 1980, which gives a truncated cost of zero and a negative-cost share of 100%. The paper has 1.67% and 79%. A share of 0.79 cannot come from five whole years, so the paper is probably weighting by month from November 1976 and treating part of the period as having a positive cost, but I cannot identify which part from the letters. The 1996-2000 row matches the paper only if 1998, a year with a small underwriting profit and no cost figure printed, is set to zero. The T-bill spreads differ by a few tenths because my bill series is not the paper's.

The paper's headline, that float cost about 2.2% a year and more than three points less than T-bills, stands. On my figures it is 2.0% to 2.1% and 3.3 to 3.4 points.

**Leverage.** Using year-end balance sheets (available in the files from 1995) and year-end market capitalisation:

| Measure | 1996-2011 | 2012-2025 | Paper (1976-2011) |
|---|---|---|---|
| (Total assets at market value - cash) / market value of equity | 1.66 | 1.52 | 1.6 in the text, 1.64 in Table 2 |
| (Market equity + debt + float) / market equity | 1.45 (1997-2011) | 1.44 | 1.4 |
| Float / total liabilities | 37% (1997-2011) | 32% | 36% |
| Berkshire volatility / 13F portfolio volatility | not available | not available | 24.8% / 17.2% = 1.44 |

The first two are close to the paper, with the caveat that my window starts 20 years later than the paper's. From 2016 Berkshire's large Treasury bill holdings are counted as cash; without that the recent numbers would be higher.

**Reconciling 1.6, 1.4 and 1.4.** These are three different quantities that happen to be near each other.

- 1.6 puts every liability in the numerator: debt, float, deferred taxes, payables and derivative liabilities.
- The first 1.4 counts only debt and float. The 0.2 difference is the other liabilities, mainly deferred tax. In my data debt and float together are 52% of total liabilities over 1997-2011.
- The second 1.4 is not a balance sheet number. It is the ratio of Berkshire's share price volatility to the volatility of its listed stock portfolio, and it equals leverage only if the private businesses are as volatile as the listed holdings, everything is perfectly correlated, and the share price has no noise of its own. The paper states the first two assumptions.

The sentence "1.6-to-1 leverage on the market gives about 10%" checks: 1.6 times 6.1% is 9.8%.

## 5. 13F portfolio, private holdings, and the cross-section (Table 4 columns 4-9, Table 1, Figures 1-2)

None of this was attempted, for the following reasons.

- **13F portfolio, 1980-2009.** The paper uses Thomson's 13F database. EDGAR's filing list for Berkshire starts in August 1998, the filings are free-form text until mid-2013, and they are XML after that. There is no free machine-readable source for 1980-1998. The letters list major holdings once a year, not quarterly, and only above a size threshold.
- **Returns on the holdings.** Even with holdings in hand, the portfolio needs monthly total returns for every stock held, including the many that no longer trade (Capital Cities/ABC, GEICO, General Foods, Gillette, Freddie Mac, and so on). CRSP has them. Yahoo drops delisted tickers, so a free reconstruction would be missing a large share of the portfolio by value in exactly the years that matter.
- **Private holdings.** These are a residual: total assets at market value less the 13F portfolio less cash, month by month. Without the 13F series there is nothing to subtract.
- **A 2013-2026 13F portfolio as an extension.** This is feasible in principle from EDGAR's XML filings and I started it (`fetch_13f.py`). The filing list downloaded from data.sec.gov, but www.sec.gov refused the filing documents with HTTP 403. The SEC asks automated clients to put contact details in the User-Agent, and my instructions were to send only a generic one, so I stopped. The script reads `SEC_USER_AGENT` from the environment; if you set your own, it should fetch 54 quarterly filings (untested beyond the filing list). It would still need a hand-built CUSIP-to-ticker map and would lose delisted holdings.
- **Table 1 and Figures 1-2.** Ranking Berkshire against every stock with a 30-year history needs the full CRSP file with dead stocks, and the fund comparison needs the CRSP mutual fund database. A ranking among today's survivors would answer a different and easier question, so I did not produce one.

## 6. Has anything changed since 2011?

**Method.** The same regressions on 2012-01 to 2026-08 (176 months; BAB and QMJ end in August 2026), and a pooled regression over 1980-04 to 2026-08 in which the intercept and every loading is allowed to shift after 2011. Ten-year rolling statistics are in `results/rolling_10y.csv`.

**Regressions, 2012-01 to 2026-08.**

| | Market only | Four-factor | + BAB | + BAB + QMJ |
|---|---|---|---|---|
| Alpha, annualised | 3.1% (0.88) | 1.1% (0.35) | 0.2% (0.06) | -0.5% (-0.15) |
| MKT | 0.71 (10.54) | 0.80 (12.51) | 0.79 (12.52) | 0.85 (12.27) |
| SMB | | -0.45 (-4.41) | -0.45 (-4.42) | -0.36 (-3.22) |
| HML | | 0.48 (6.32) | 0.46 (5.88) | 0.44 (5.65) |
| UMD | | 0.01 (0.20) | -0.02 (-0.27) | 0.00 (0.06) |
| BAB | | | 0.15 (1.47) | 0.08 (0.72) |
| QMJ | | | | 0.21 (1.91) |
| Adjusted R2 | 0.39 | 0.53 | 0.54 | 0.54 |

**What changed.**

- *Alpha.* The market-model alpha fell from 12.5% a year to about 3%, and it is not statistically different from zero. The four-factor alpha is 1%. BAB and QMJ are no longer needed to explain Berkshire's return: size and value do it.
- *Sharpe ratio.* Berkshire's is 0.76, the same as the paper's full-sample figure, but the market's was 0.93 over the same months. Before 2012 Berkshire's Sharpe was 0.72 against the market's 0.45.
- *Volatility and fit.* Volatility fell from 23.6% to 16.4%, idiosyncratic volatility from 21.3% to 12.8%, and the six-factor R2 rose from 0.29 to 0.54. Berkshire now behaves much more like a diversified large-cap value portfolio.
- *Loadings.* The market, size and value loadings are about where they were. The BAB loading fell from 0.29 to 0.08 and is insignificant. The QMJ loading fell from 0.47 to 0.21 and is borderline.
- *The factors themselves.* On AQR's and French's numbers the premia shrank: HML from 4.0% to 0.2% a year, QMJ from 6.1% to 2.2%, BAB from 11.6% to 6.4%, while the market's went from 7.1% to 13.6% (`results/factor_premia.csv`).

**What I cannot claim.** The formal test does not reject stability. In the pooled regression the post-2011 shift in the market-model alpha is -9.4 points with a t-statistic of -1.53, and the joint test that all coefficients are unchanged has p-values between 0.30 and 0.72 depending on the specification. With idiosyncratic volatility of 13% to 21% a year, fifteen years is not enough to distinguish a true alpha of 3% from one of 10%. The honest statement is that the post-2011 alpha is small and indistinguishable from zero, and also not statistically distinguishable from the earlier one.

**The decline predates 2011.** Among ten-year windows ending each December, the six-factor alpha has not had a t-statistic above 2 in any window ending after 1996, and the market-model alpha for 1996-2011 alone is 5.1% (t = 1.00). The significant alpha in my 1980-2011 sample is carried by 1980-1995.

## Caveats that apply throughout

- Free monthly prices start in April 1980. Every "paper window" number of mine is missing November 1976 to March 1980.
- The factor data are 2026 vintages. French's files and AQR's files are both revised over time.
- The paper's tables are labelled 1976-2011 but appear to end in September 2011.
- t-statistics use conventional OLS standard errors, which is what the paper appears to use. No adjustment for heteroskedasticity or autocorrelation was made.
- Yahoo's 1980 daily data for BRK-A are thin (70% of daily price changes are zero). I could not check 1980 month-ends against a second source, and the 1980 calendar-year return cannot be checked either because Yahoo has no December 1979 close.

## Files

Code: `fetch_data.sh` (downloads), `build_series.py` (builds the two shared CSVs), `common.py`, `replicate.py` (items 1, 2, 3, 6), `diagnostics.py`, `float_leverage.py` (item 4), `fetch_13f.py` (item 5, not completed). Run the Python files with the virtualenv's interpreter and `-I`.

Shared data: `data/berkshire_monthly.csv`, `data/factors_monthly.csv`, `data/berkshire_annual_letter.csv`. Results: `results/*.csv`.

## Data sources

All downloaded on 2026-11-19 unless noted.

| Data | Source | Notes |
|---|---|---|
| BRK-A and BRK-B daily prices | `https://query1.finance.yahoo.com/v8/finance/chart/BRK-A?period1=0&period2=<now>&interval=1d` (and `BRK-B`) | BRK-A from 1980-03-17, BRK-B from 1996-05-09. Raw JSON in `data/raw/`. |
| MKT-RF, SMB, HML, RF | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip` | File header: "created using the 202609 CRSP database". Monthly to 2026-09. |
| UMD (momentum) | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip` | Same vintage. |
| BAB | `https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Betting-Against-Beta-Equity-Factors-Monthly.xlsx` | AQR data library, "Betting Against Beta: Equity Factors, Monthly". Sheet "BAB Factors", column USA, 1930-12 to 2026-08. The file carries no version stamp that I could find; the vintage is identified by download date and last observation. Automated download was not blocked. |
| QMJ, and AQR's MKT, SMB, HML FF, HML Devil, UMD, RF | `https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Quality-Minus-Junk-Factors-Monthly.xlsx` | AQR data library, "Quality Minus Junk: Factors, Monthly". Sheet "QMJ Factors", column USA, 1957-07 to 2026-08. Same remark on vintage. |
| Berkshire annual market-value change and S&P 500 total return, 1976-2025 | 2025 shareholder letter, performance table, read from the scratchpad copy `brk/dl/2025.txt` | Transcribed into `data/berkshire_annual_letter.csv`. |
| Insurance float and underwriting result, 1967-2025 | `../float.csv` (collected earlier from the shareholder letters) | Not re-collected. |
| Balance sheet items and leverage, 1995-2025 | `../leverage_cost.csv`, `../debt.csv` (collected earlier) | Not re-collected. |
| Berkshire filing list | `https://data.sec.gov/submissions/CIK0001067983.json` | Downloaded; the filing documents on www.sec.gov were refused (HTTP 403), so no 13F data were obtained. |
| The paper | scratchpad copy `ba.txt`, a text conversion of NBER Working Paper 19681 | Source of every "paper" number above. |
