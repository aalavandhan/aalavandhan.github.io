# LETF Universe — Tweet Thread

## 1/
[IMAGE: fig_letf_decomposition.pdf — TQQQ vs zero-cost 3x wealth paths]

@sumitroy2 showed that leveraged ETFs embed large, undisclosed financing costs above the stated expense ratio. We extended his decomposition to 109 long US-listed leveraged ETFs ($126B in AUM). The results are consistent with his findings and the pattern holds across the full universe.

## 2/
[IMAGE: fig_letf_scatter.pdf — financing premium vs volatility scatter]

Most leveraged ETFs get their exposure through total return swaps. The fund pays a dealer a financing rate in exchange for leveraged returns. The cost of that leverage does not appear to be driven by volatility. It seems to be driven by hedging infrastructure, specifically how cheaply the swap dealer can lay off risk in derivatives markets. The variance across asset classes seems to track derivatives depth, not vol.

## 3/
[IMAGE: fig_letf_class_summary.pdf — financing premium by asset class box plot]

The financing premium, what the dealer charges above the risk-free rate, varies enormously. Equity index LETFs borrow at close to the risk-free rate. Single stocks pay premiums anywhere from 1% to >50%.

TSLL (2x Tesla) has a premium of just 1.3%, possibly because Tesla has one of the deepest single-stock options books in existence. MicroStrategy (MSTU, 2x) has a premium of 37%. Both are high-volatility single stocks. The difference appears to be liquidity, not risk.

Competition does not appear to compress premiums. Nvidia has three competing 2x ETFs with premiums ranging from 10% to 28%.

These costs exhibit diseconomies of scale. TSLL's premium nearly tripled as AUM grew. TQQQ's expense ratio fell just 7 bps in 15 years.

## 4/

Fewer than four in ten LETFs outperform their own underlying over the fund's lifetime. The standard explanation is volatility drag. As Roy points out, the financing costs embedded in the swap layer are an additional, largely invisible drag that compounds alongside it.

## 5/
Full decomposition, per-fund results, and methodology:

Paper: https://drive.google.com/file/d/14E0phxNhliy_Qc-kBPPbRAkaedBxe3ma/view
Results: https://drive.google.com/file/d/1VPu2SOqdjIAz22j7rs_k-D0upghCBoWm/view
Interactive LETF dashboard: https://frg-public-data.s3.amazonaws.com/durable-leverage/viz/letf_explorer.html

@sumitroy2's original article:
https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0
