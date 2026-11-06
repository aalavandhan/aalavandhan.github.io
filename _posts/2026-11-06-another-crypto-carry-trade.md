---
layout: post
title: "Another crypto carry trade"
subtitle: "Allies, not rivals."
date: 2026-11-06
categories: defi
image: /assets/images/og/another-crypto-carry-trade.png
description: "Perps charge a persistent premium for leverage, and the basis trade harvests it. 2factor's Jr is cheaper leverage, which opens a second way to collect it. Allies, not rivals."
---

<script defer src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<script defer src="/assets/js/another-crypto-carry-trade/data.js"></script>
<script defer src="/assets/js/another-crypto-carry-trade/shared.js"></script>

> **TL;DR:** Perps charge a persistent premium for leverage, and the basis trade harvests it. 2factor creates cheaper leverage, sourced from yield seekers rather than shorts. The "Jr carry" is a second way to harvest perp premia, viable today and mutually beneficial.
{: .tldr}

[Perpetual futures](https://en.wikipedia.org/wiki/Perpetual_futures) (perps) have become a [widely used tool for speculation](https://arxiv.org/abs/2212.06888), offering high leverage multiples beyond 100×.[^perp-history]

In 2025, they accounted for [68% of all bitcoin trading volume](https://blockchain.news/news/crypto-perpetual-trading-dex-cex-2026), more than twice the volume on underlying spot markets. They've since spread beyond cryptocurrencies to traditional assets like [commodities and equities](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals).

[^perp-history]: Fixed-term futures contracts, [in various forms](https://en.wikipedia.org/wiki/Confusion_of_Confusions), have existed alongside spot markets for about 400 years.

    Perpetual futures, contracts that never expire and settle in cash against an index, are very recent.

    [Robert Shiller](https://ideas.repec.org/a/bla/jfinan/v48y1993i3p911-31.html) first formalized perps in 1993.

    [BitMEX](https://web.archive.org/web/20160513131955/https://blog.bitmex.com/announcing-the-launch-of-the-perpetual-xbtusd-leveraged-swap/) turned them into a product at scale in 2017, with one key innovation: [funding set by relative demand](https://web.archive.org/web/20180402084948/https://www.bitmex.com/app/perpetualContractsGuide).

When speculators are overwhelmingly long, perps trade above spot, and longs pay shorts a periodic fee called [funding](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding). Funding is *positive* when longs pay shorts, and *negative* when shorts pay longs.

Crypto markets have, in aggregate, been long. On Binance, the largest perp exchange, bitcoin funding averaged about +8% a year from late 2021 through 2025, and was positive in 96% of weeks.[^natural]

[^natural]: Perps trading above spot is called [contango](https://en.wikipedia.org/wiki/Contango). The reverse, when perps trade below spot and shorts pay funding to longs, is [backwardation](https://en.wikipedia.org/wiki/Normal_backwardation).

    For all assets with positive expected drift, contango is the natural state. Reversals (or backwardation) are transient.

<div id="jpc-funding" class="jpc-viz"></div>
<script defer src="/assets/js/another-crypto-carry-trade/funding.js"></script>

Funding is roughly the risk-free rate plus a [premium](https://www.bis.org/publ/work1087.htm). When the premium is persistent, market makers harvest it by taking the short side while hedging.

This is the classic [cash-and-carry](https://www.investopedia.com/terms/c/cash-and-carry-arbitrage.asp), aka the basis trade.[^reverse]

[^reverse]: When funding direction flips, it runs in reverse: market makers go long the perp, collect funding from the shorts, and hedge by shorting spot.

    This [reverse cash and carry](https://www.investopedia.com/terms/r/reverse-cash-and-carry-arbitrage.asp) is less common and arguably even harder to execute. Negative funding rarely lasts, and shorting spot requires borrowing the underlying asset.

<blockquote class="callout">
  <p class="how-label">{% include icons/gear.svg %}How it works</p>
  <ol>
    <li>Hold the asset and short the same notional value on a perp exchange.</li>
    <li>The two positions cancel each other out, so price moves don’t matter.</li>
    <li>The short leg collects funding.</li>
  </ol>
</blockquote>

Executing it, however, takes some sophistication. One has to actively manage the short position so it doesn't get liquidated, [constantly rebalancing](#modal-rebalance) spot positions.

<dialog id="modal-rebalance" class="modal">
<div id="jpc-rebalance" class="jpc-viz"></div>
<p class="modal-caption">The basis trade</p>
</dialog>
<script defer src="/assets/js/another-crypto-carry-trade/rebalance.js"></script>

Crypto premia were high early on, when markets were nascent. In 2021, bitcoin funding's 30-day average peaked above 35%.

[Ethena](https://ethena.fi/) automated execution and opened it to anyone through a simple staking vault, basically the basis trade in a box. They handle [off-exchange custody](https://docs.ethena.fi/overview/off-exchange-custody), hedging across exchanges, deep entry and exit liquidity, and a [reserve fund](https://docs.ethena.fi/solution-design/reserve-fund) for when funding temporarily turns negative.

Ethena quickly scaled to $14.7 billion and helped bring premiums down. The yield offered by their system fell to about 5% in 2025, a point above T-bills.

<div id="jpc-ethena" class="jpc-viz"></div>
<script defer src="/assets/js/another-crypto-carry-trade/ethena.js"></script>

Ethena was a godsend for exchanges, because it brought the cost of leverage down for their users and smoothed fluctuations in funding rates.

## Perp leverage is still expensive

Even after the industrialization of the basis trade, perps are still costly compared to [other forms of leverage](https://chat.2factor.finance/durable-leverage-appendix.pdf).

<div id="jpc-landscape" class="jpc-viz"></div>
<script defer src="/assets/js/another-crypto-carry-trade/landscape.js"></script>

*Ref: [2factor white paper supplement](https://chat.2factor.finance/durable-leverage-appendix.pdf).*

This is likely to stay true for the foreseeable future, for structural reasons and market reasons.

**The structural reason** is that funding is charged on the full notional value of the position.

Say Alice and Bob each have $100 and want $200 of bitcoin exposure. Alice opens a 2× perp long and pays funding on all $200, or $20 a year at a 10% funding rate.

Bob buys $200 of bitcoin with his $100 and a $100 margin loan at the same 10%, and pays interest only on the $100 he borrowed, or $10 a year. On his $200 of bitcoin, Bob pays an effective rate of just 5%.[^low-lev]

[^low-lev]: The financing cost gap between a perp and a margin loan is widest at low leverage.

    With $100 in a 1.33× position, the perp charges funding on $133, while the loan charges only on the $33 you borrow: a quarter of the cost.

    At 10×, it's $1,000 against $900, and the difference nearly disappears.

**The market reason** is the distribution of demand. The long side is mostly speculators who want high leverage for a short duration, so the cost of financing barely matters to them.

Shorts carry real risks (exchange and custody risk, capital split across venues, negative funding and auto-deleveraging in a crash) and need to be paid to hold them.

I expect bitcoin's arc to repeat as [tokenized assets open up](https://cointelegraph.com/news/sec-approves-nasdaq-tokenized-trading-pilot). The premium will start wide and compress as markets mature, but it won't go away. Speculative demand for long leverage [keeps growing](https://cryptobriefing.com/on-chain-perp-futures-volume-market-share/), and for any asset that tends to rise, [contango](https://en.wikipedia.org/wiki/Contango) is the natural state.

The basis trade will only grow.

## WTF is a 2factor?

We recently launched [2factor](https://2factor.finance/), a novel instrument based on [perpetual tranching](https://2factor.finance/primer/). It splits the volatility of an underlying asset into a basket of rotating senior (Sr) and junior (Jr) tranches. Sr holds a stable position and harvests yield. Jr takes the price moves, which makes it a levered long on the underlying ([white paper](https://chat.2factor.finance/durable-leverage.pdf)).

<div id="jpc-tranche" class="jpc-viz"></div>
<script defer src="/assets/js/another-crypto-carry-trade/tranche.js"></script>

Perps source leverage from shorts, unlike 2factor, which sources directly from yield seekers. The basis trade in a box taps into demand for stable yield, but still warehouses the risk of holding a short position, which inevitably demands a premium.

The 2factor capital structure, and where it sources leverage from, make leverage *significantly* cheaper than perps.[^sr-risk]

[^sr-risk]: Why is 2factor cheaper?

    **Moderate leverage.** Like Bob's margin loan, Jr pays only on the Sr capital backing it, not on its full exposure. At 1.33×, that's a third of a dollar per Jr dollar.

    **The capital split.** Jr's capital takes price moves first. With three Jr dollars for every Sr dollar, the underlying would have to fall about 75% before Sr lost anything. Jr–Sr ratios are tuned per asset so that Sr only takes a loss on a 4-sigma drawdown within a single maturity period.

    **Settled in the underlying.** Both tranches are claims on the same pool of the underlying asset and are paid out in it, so there's no cash leg, no outside counterparty and nothing to liquidate.

    **No duration mismatch.** Long-term leverage is funded by long-term yield.

<div id="jpc-jrcost" class="jpc-viz"></div>
<script defer src="/assets/js/another-crypto-carry-trade/jrcost.js"></script>

*The [bitcoin Jr market](https://app.2factor.finance/), at 1.33×, has been live since September 22.*

But perps and 2factor aren't adversaries.

Perps serve short-term, high-leverage speculation, while Jr excels at long-duration, moderate leverage: cheap and passive.

They cover different parts of the market. They have a mutually beneficial relationship through carry arbitrage.

## Junior carry

The [Jr carry](#modal-jrcarry) works like the basis trade.

<dialog id="modal-jrcarry" class="modal">
<div id="jpc-jrcarry" class="jpc-viz"></div>
<p class="modal-caption">Jr carry</p>
</dialog>

<blockquote class="callout">
  <p class="how-label">{% include icons/gear.svg %}How it works</p>
  <ol>
    <li>Hold Jr on 2factor and short the same notional exposure on a perp exchange.</li>
    <li>The two positions cancel each other out, so price moves don’t matter.</li>
    <li>In aggregate the yield is positive: the short leg collects funding on the perp, and Jr pays Sr’s yield on the Sr capital backing it.</li>
  </ol>
</blockquote>

At today's rates, the [yield is competitive](#modal-crossover), and it's a viable carry strategy in its own right.

| On $100 | Basis trade | Jr carry |
|---|---|---|
| Long | $83 spot | $79 Jr, $105 of exposure |
| Short | $83 at 5× | $105 at 5× |
| Yield | ~8.3% | ~8.5%[^yield] |
{: .highlight-last}

[^yield]: At 10% funding, before rebalancing costs. The basis trade earns funding on its $83 short.

    The Jr carry earns funding on its $105 short and pays Sr's yield, about 8% in October, on the $26 of Sr capital backing Jr.

    Jr carry has a small edge.

<dialog id="modal-crossover" class="modal">
<div id="jpc-vs-carry" class="jpc-viz"></div>
<p class="modal-caption">Yield on capital from the basis trade and the Jr carry</p>
</dialog>
<script defer src="/assets/js/another-crypto-carry-trade/vs_carry.js"></script>

However, it doesn't replace the basis trade. It provides a second source of demand. Its risks are largely the same.[^risks]

Insofar as leverage through Jr is cheaper than perps, the cost differential can be arbitraged. For the reasons above, (1) the perp funding premium won't go away, and (2) perps will stay more expensive than Jr. So the Jr carry should continue producing a competitive yield.

That's a win for perp exchanges, much as Ethena was. Capital flowing into the Jr carry adds to the short side. More shorts bring funding down for the short-term speculators, who make up the vast majority of perp users. And the Jr carry is more capital efficient than the basis trade at bootstrapping short open interest.[^oi] 

It also adds demand for Jr, which grows 2factor.

[^oi]: $1 million in the Jr carry adds about $1.05 million of short open interest, against $830,000 from the basis trade. That's over 25% more per dollar.

[^risks]: **Shared with the basis trade.** Funding can turn negative. The short can be liquidated in a fast rally.

    **Specific to the Jr carry.** Smart contract risk, and exits that depend on Jr's liquidity.

Btw, we have a working prototype vault that harvests the Jr carry, running fully on-chain on [Base](https://base.org) with no custodian and earning about 9.5% a year.[^vault]

[^vault]: The vault takes deposits in USDC and splits them in two: it holds BTC-Jr, and takes a 5× bitcoin short on [Veranta](https://veranta.xyz), a perp DEX on Base. Its net exposure is zero, so it's delta neutral.

    It rebalances when its exposure drifts too far from neutral.

    It earns a positive return by collecting funding on Veranta and paying Sr’s yield on the Sr capital backing the Jr position.

    As of November 4, it was earning around 9.5% a year in dollar terms.

    You can think of it as an on-chain Ethena.

## Fin

Perps are here to stay, and so is their funding premium. Risk seekers will keep paying it willingly, and as more markets open up, the total carry harvested will keep growing.

2factor adds a cheaper source of leverage. The Jr carry allows 2factor to tap into perp liquidity, bringing leverage costs down for everyone.

Perps and 2factor aren't rivals. They're allies.
