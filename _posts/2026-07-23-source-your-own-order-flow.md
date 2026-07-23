---
layout: post
title: "Source your own order flow"
subtitle: "A permissionless solution to an AMM's discoverability problem"
hero: /assets/images/integrating-a-bespoke-amm-with-cowswap/fig_forest.svg
hero_alt: "A bare tree in a dense autumn forest, seen from above"
date: 2026-07-23
categories: defi
theme: autumn
---

DeFi promises to tokenize everything. Smart contract platforms offer flexibility to codify asset-specific trading strategies that execute trustlessly. With liquidity open to anyone, anywhere, markets compete on price alone. The best quote *should* win the trade.

But it doesn't play out that way. A new AMM can go on-chain with deep liquidity and competitive quotes, and still never trade, because none of it matters without order flow.

Traders move through established channels: aggregators and routers your AMM isn't wired into. They usually stick with the venues they know, even when they get a worse quote.

In 2024 we built a bespoke [AMM](https://chain.link/education-hub/what-is-an-automated-market-maker-amm), the [Bill Broker](https://docs.spot.cash/spot-documentation/spot-documentation/about-the-bill-broker), with pricing logic that traded [SPOT](https://spot.cash) (the flatcoin) around its fair market value. Bootstrapping volume proved hard. There are a few options to try, but no silver bullet:

<div class="options" markdown="1">

**Get listed by an aggregator**: put your AMM on the routers where retail order flow already sits: [1inch](https://1inch.io/), [Matcha](https://help.matcha.xyz/en/articles/6698969-how-can-my-project-become-a-liquidity-source), and others.

**Integrate with a searcher**: an [MEV bot](https://ethereum.org/en/developers/docs/mev/) arbitrages your AMM and, as a side effect, holds your price in line with the market.

**Run the arbitrage yourself**: operate a bot that trades your AMM against other venues whenever they diverge.

</div>

**Aggregators don't let you list yourself.** Their engineers have to write the connector, and the group that owns the source list (Matcha's, for instance, runs through the [0x API](https://docs.0x.org/)) prioritizes venues that already carry volume. An unfamiliar AMM with no track record sits in a backlog they may never get to.

**Searchers take their pound of flesh.** Their bot keeps your price aligned with the market, taking real risk to do it: unaudited code and a winner-take-all race. They're paid from the arbitrage spread, your value leaking to a mercenary. And their incentive runs against yours: the better your quote, the wider the spread, the more they take.

**Self-arbitrage needs liquidity you don't have.** Running the bot yourself keeps the spread in-house, but only works when the asset already trades deep elsewhere. Newer assets don't: the bot has nothing to arbitrage against until you've seeded liquidity on established AMMs.

## A solution

In our [latest iteration](https://2factor.finance) we built an integration with [CoW Swap](https://docs.cow.fi/) using [Programmatic Orders](https://docs.cow.fi/cow-protocol/concepts/order-types/programmatic-orders) and [flash loans](https://docs.cow.fi/cow-protocol/concepts/flash-loans/Introduction). The approach can work for any on-chain swap protocol facing the discoverability problem.

<blockquote class="callout">
  <p class="how-label">{% include icons/gear.svg %}How it works</p>
  <p>Instead of waiting and praying for order flow, the AMM publishes its own intent to trade into CoW's batch auction for any solver to fill.</p>
  <p>Flash loans handle atomic, multi-party settlement between the AMM and takers from the CoW network.</p>
</blockquote>

<div class="pieces">
  <button class="piece" data-figure="/assets/images/integrating-a-bespoke-amm-with-cowswap/fig_pool.svg" data-alt="The AMM: a pool exposing swap methods over a BTC/USD pair"><span class="piece-n">AMM</span></button>
  <button class="piece" data-figure="/assets/images/integrating-a-bespoke-amm-with-cowswap/fig_swapper.svg" data-alt="The publisher: an on-chain swapper reading the AMM's price, and an off-chain keeper submitting the order to CoW's orderbook"><span class="piece-n">Publisher</span></button>
  <button class="piece" data-figure="/assets/images/integrating-a-bespoke-amm-with-cowswap/fig_auction.svg" data-alt="Settlement: a solver flash-borrows USD, swaps on the AMM, settles against the CoW batch, and repays the loan atomically"><span class="piece-n">Settlement</span></button>
</div>
<div class="piece-view"></div>

**1) The AMM.** Your pool or trading strategy: it exposes swap methods over a pair, say BTC ↔ USD.

**2) The publisher.** An on-chain swapper contract that reads the AMM's price and publishes a matching order, and an off-chain keeper that submits that order and its execution recipe to CoW's orderbook.

**3) Settlement.** The winning solver executes everything in one atomic transaction: flash-borrow USD (from an on-chain pool like Morpho, or one you run yourself), swap that USD for BTC on the AMM, settle the trade against the CoW batch, and repay the loan from the proceeds.

## Benefits

**Permissionless.** No connector, no listing, no approval. Your order goes straight into CoW's public orderbook, live the moment you deploy.

**Surplus capture.** CoW settles in a batch auction where solvers compete to return the most surplus. Your order enters floored at the AMM's own quote, so a solver wins only by beating it. Because your own contract is the receiver, everything above that floor flows back to the pool instead of leaking to whoever routed the fill. Incentives stay aligned: the solver takes its nominal batch fee, and the surplus goes to your LPs.

**No upfront capital.** Someone has to front the USD to buy the BTC the pool is selling. The flash loan supplies it just in time and is repaid from the swap proceeds within the same settlement, so no one (not the AMM, not the solver) has to lock up inventory to be the counterparty. CoW supports this natively via [CIP-66](https://forum.cow.fi/t/cip-66-flash-loan-router-integration/2939).

## Conclusion

The approach clears all three dead ends: it's permissionless, the swap surplus stays with your LPs, and it needs no capital up front.

---

{% include code-viewer.html
     file="code/source-your-own-order-flow/amm-interface.md"
     label="The AMM interface"
     lang="Solidity"
     meta="Solidity · what the publisher reads" %}

{% include code-viewer.html
     file="code/source-your-own-order-flow/cow-swapper.md"
     label="The publisher — on-chain"
     lang="Solidity"
     meta="Solidity · builds and signs the order" %}

{% include code-viewer.html
     file="code/source-your-own-order-flow/keeper.md"
     label="The publisher — off-chain keeper"
     lang="TypeScript"
     meta="TypeScript · posts it to the orderbook" %}

{% include code-viewer.html
     file="code/source-your-own-order-flow/flash-loan-router.md"
     label="The flash loan router"
     lang="Solidity"
     meta="Solidity · funds the settlement" %}
