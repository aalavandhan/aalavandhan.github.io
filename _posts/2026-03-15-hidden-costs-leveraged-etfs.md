---
layout: post
title: "Hidden cost of leverage in LETFs"
date: 2026-03-15
categories: finance research
---

[Leveraged ETFs](https://www.investopedia.com/terms/l/leveraged-etf.asp) (LETFs) have exploded among retail. 2x Tesla, 3x QQQ, levered bitcoin. There's a fund for everything now.

Most people believe, 2x LETF gives them 2x returns. In practice though, most of these funds underperform the underlying, even over periods where the underlying asset is consistently going up in value.

![BTC vs 2x LETF](/assets/images/hidden-costs-leveraged-etfs/fig_btc_2x_underperformance.svg)
*Double the leverage, less return.*

The standard explanation is [volatility drag](https://www.investopedia.com/articles/financial-advisors/082515/why-leveraged-etfs-are-not-longterm-bet.asp): daily leverage resets lose ground in choppy markets. That's real, but it's only half the story. The other half is [financing drag](https://www.etf.com/sections/features/leveraged-etfs-hidden-costs-eat-your-returns-0). It doesn't appear in the [expense ratio](https://www.investopedia.com/terms/e/expenseratio.asp). It isn't disclosed in any standardized way.

## Where the leverage comes from

A 3x fund with $100 of investor capital needs $300 of exposure. The extra $200 comes from [total return swaps](https://www.investopedia.com/terms/t/totalreturnswap.asp) with dealers. The dealer provides the leverage and charges a financing rate.

![How a 3x LETF creates leverage](/assets/images/hidden-costs-leveraged-etfs/fig_leverage_mechanics.svg)

That rate never shows up in the expense ratio. It shows up in the price chart. [We measured it](https://drive.google.com/file/d/14E0phxNhliy_Qc-kBPPbRAkaedBxe3ma/view) across 109 long-only LETFs covering $125 billion in assets. For each fund, we compared the actual return against what a version borrowing at the [risk-free rate](https://www.investopedia.com/terms/r/risk-freerate.asp) would have delivered, net of stated expenses. The residual is the [financing premium](https://drive.google.com/file/d/14E0phxNhliy_Qc-kBPPbRAkaedBxe3ma/view), or the hidden cost of leverage.

The premia vary a lot.

## It's about hedging, not volatility

<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_funds.js"></script>
<div id="letf-tooltip" style="position:fixed;pointer-events:none;background:#fff;border:1px solid #e6e6e6;border-radius:4px;padding:10px 14px;font-size:13px;line-height:1.5;z-index:1000;opacity:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#292929;max-width:320px;box-shadow:0 2px 8px rgba(0,0,0,.08);transition:opacity 0.25s ease,left 0.15s ease-out,top 0.15s ease-out;"></div>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_shared.js"></script>

<div id="letf-scatter" style="position:relative; width:100%; height:420px; margin:40px 0; overflow:hidden;"></div>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_scatter.js"></script>

*No relationship between volatility and financing premium.*

What the premium tracks is hedging infrastructure. Dealers who can offload risk onto deep derivatives markets charge less. Where those markets are thin, the hedge is harder, and the cost is higher.

Group by asset class and the pattern is clear.

<div id="letf-boxplot" style="position:relative; width:100%; height:400px; margin:40px 0; overflow:hidden;"></div>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_boxplot.js"></script>

*It's the asset class.*

1) Equity index and fixed income funds sit on deep futures markets. Premia are low and tight. 2) Sector funds cost more. A semiconductor basket is harder to offset than the broad index. 3) Commodities split in two. Gold and crude oil are cheap. Uranium and natural gas are all over the map. 4) Single-stock and crypto is where costs climb.

Thinner markets. Premia are high and all over the place.

## Same label, very different economics

[TSLL](https://finance.yahoo.com/quote/TSLL/) (2x Tesla) and [MSTU](https://finance.yahoo.com/quote/MSTU/) (2x MicroStrategy). Both single-stock LETFs. Comparable volatility. TSLL's financing premium is 1.30%. MSTU's is 37%.

Nearly 30x higher.

Tesla has the deepest single-stock derivatives market on the planet. MicroStrategy trades like a mid-cap with a bitcoin habit. The dealer charges accordingly.

<div id="letf-bubble-viz" style="position:relative; width:100%; height:420px; margin:40px 0; overflow:hidden;"></div>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_bubbles.js"></script>

*Green beats spot, pink lags it. [Full dashboard](https://data.2factor.finance/durable-leverage/viz/letf_explorer.html){:target="_blank"}*

You might expect scale to help. It doesn't. TSLL's premium nearly tripled as AUM grew — more notional to hedge, same thin options book.

TQQQ grew to $29 billion and the premium barely budged in 15 years. When the underlying market is deep, size is free. When it isn't, size is the problem.

## The compounding trap

[TQQQ](https://finance.yahoo.com/quote/TQQQ/) is the largest and oldest 3x fund. It's had a great run. But compare it to what a 3x QQQ portfolio would have done if it could borrow at the risk-free rate — same leverage, no financing premium.

![TQQQ vs zero-premium 3x QQQ](/assets/images/hidden-costs-leveraged-etfs/fig_letf_decomposition.svg)

That gap is the financing premium compounding over 16 years. It doesn't look like much in any single year. But a small annual drag, reinvested against you for a decade and a half, eats roughly half the total return.

TQQQ is one of the *cheapest* LETFs in our sample, but its financing premium is still roughly double its stated expense ratio.

The longer you hold, the wider the gap between the leverage you paid for and the returns you actually get.
