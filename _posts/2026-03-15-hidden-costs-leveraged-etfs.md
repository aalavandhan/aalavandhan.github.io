---
layout: post
title: "Hidden cost of leverage in LETFs"
date: 2026-03-15
categories: finance research
---

Most leveraged ETFs underperform their own underlying. Not because leverage is inherently bad, but because it typically costs way more than you think.

[Leveraged ETFs](https://www.investopedia.com/terms/l/leveraged-etf.asp) (LETFs) have exploded in popularity among retail. If you want 2x Tesla, 3x QQQ, or levered bitcoin, there is now a fund for it. Because they trade like ordinary ETFs, buyers evaluate them the same way: look at the chart and the expense ratio.

The standard explanation for this underperformance is [volatility drag](https://www.investopedia.com/articles/financial-advisors/082515/why-leveraged-etfs-are-not-longterm-bet.asp): daily resets lose ground in choppy markets. That is real, but it is only half the story. The other half is [financing drag](https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0). It does not appear in the expense ratio. Nor is it disclosed in any standardized way.

[We analyzed 109 long-only LETFs](https://data.2factor.finance/durable-leverage/viz/letf_explorer.html) covering over $125 billion in assets to measure this hidden cost.

![The Leverage Expansion Pack](/assets/images/hidden-costs-leveraged-etfs/fig_letf_sims.jpg)

So how do these funds get leverage?

A 3x fund that has $100 of investor capital needs $300 of exposure. It gets the extra $200 through [total return swap agreements](https://www.investopedia.com/terms/t/totalreturnswap.asp) with swap dealers. The dealer provides the leverage in exchange for a financing rate. What's actually paid only shows up in the price chart.

For each fund we compared the actual return against what a version borrowing at the risk-free rate would have delivered, net of the stated expense ratio. The residual is the [financing premium](https://drive.google.com/file/d/14E0phxNhliy_Qc-kBPPbRAkaedBxe3ma/view): the hidden cost of leverage paid entirely by ETF holders.

The premia vary enormously. And they do not track the underlying's volatility.

![Financing premium vs volatility](/assets/images/hidden-costs-leveraged-etfs/fig_letf_scatter.png)
*The financing premium does not move with volatility.*

Rather, they track the underlying's hedging infrastructure. Swap dealers who can offload risk onto deep derivatives markets offer lower rates. Where those markets are thin, the dealer's hedge is harder and the premia are high.

The pattern is clear when we group by asset class.

![Financing premium by asset class](/assets/images/hidden-costs-leveraged-etfs/fig_letf_class_summary.png)
*Asset class is the dominant predictor of financing premium.*

Deep futures markets make equity index and fixed income funds easy to hedge — the premia are low and tightly clustered. Sector funds cost more; a semiconductor basket is harder to offset than the broad index. Commodities split in two. Gold and crude oil sit in the low group. Others like uranium and natural gas are all over the map.

Single-stock and crypto funds are where costs climb. The dealer hedges in thinner, more fragmented markets — and the premia are both high and widely dispersed.

> Where hedging is easy, leverage is cheap;<br/>when hedging is hard, leverage cuts deep.
{: .highlight}

Take [TSLL](https://finance.yahoo.com/quote/TSLL/) (2x Tesla) and [MSTU](https://finance.yahoo.com/quote/MSTU/) (2x MicroStrategy). Both single-stock LETFs. Comparable volatility. But TSLL's premium is 1.30% and MSTU's is 37%. Nearly 30x higher.

Tesla has one of the deepest single-stock derivatives markets in the world — liquid options, deep borrow market, plenty of ways to hedge at scale. MicroStrategy has a thinner options book and harder-to-source hedges. The dealer passes the costs through.

<img src="/assets/images/hidden-costs-leveraged-etfs/fig_letf_aum_map.png" alt="LETF AUM Map" style="max-width: 380px; margin: 40px auto; display: block;">
*Size = AUM. Green beats the underlying, pink lags it.*

Take [TQQQ](https://finance.yahoo.com/quote/TQQQ/), the largest and oldest 3x fund. Over the past 16 years it turned $1 into $262. An extraordinary return. But a 3x QQQ portfolio with zero financing premium would have delivered roughly a third more.

The stated expense ratio on TQQQ is 88 bps. The total financing premium is roughly double that. And TQQQ is one of the cheaper LETFs in the market.

![TQQQ vs zero-premium 3x QQQ](/assets/images/hidden-costs-leveraged-etfs/fig_letf_decomposition.png)

You might expect competition to compress these costs. It does not. Three competing 2x Nvidia ETFs ([NVDL](https://finance.yahoo.com/quote/NVDL/) and others) from different issuers have premiums ranging from 10% to 28%. Same underlying. Nearly identical labels. Very different economics.

Scale does not help either. TSLL's premium nearly tripled as its AUM grew. TQQQ grew to $29 billion and the financing premium has barely budged in 15 years. From the dealer's side this makes sense. Hedging a modest amount of notional is easy. Hedging tens of billions is a different problem.

For buy-and-hold investors, the compounding drag is the real price of leverage — and it is nowhere on the label.

The full per-fund breakdown is in the paper and interactive dashboard below. Hat tip to [Sumit Roy](https://x.com/sumitroy2) whose original article on LETF financing costs inspired this analysis.

---

Additional reading:

- [Durable Leverage](https://drive.google.com/file/d/14E0phxNhliy_Qc-kBPPbRAkaedBxe3ma/view)
- [Interactive dashboard](https://data.2factor.finance/durable-leverage/viz/letf_explorer.html)
- [Roy's original article](https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0)
