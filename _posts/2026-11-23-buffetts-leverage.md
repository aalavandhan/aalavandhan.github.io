---
layout: post
title: "Buffett's leverage"
subtitle: "Moderate, cheap and non-callable"
date: 2026-11-23
categories: finance
image: /assets/images/og/buffetts-leverage.png
description: "Berkshire's edge comes from its innovative capital structure. This lets the company borrow hundreds of billions at rates often lower than the risk-free rate."
---

<script defer src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<script defer src="/assets/js/buffetts-leverage/data.js"></script>
<script defer src="/assets/js/buffetts-leverage/shared.js"></script>
<script defer src="/assets/js/buffetts-leverage/book.js"></script>

Warren Buffett is visibly exceptional.

You can look at the distribution of [risk-adjusted returns](https://en.wikipedia.org/wiki/Sharpe_ratio) of stocks that have traded for 50 years, and Berkshire Hathaway stands out.

{% include buffetts-leverage/sharpe-distribution.svg %}

In [*Fooled by Randomness*](https://en.wikipedia.org/wiki/Fooled_by_Randomness), Nassim Taleb describes a thought experiment. Say there were 1,024 fund managers. Everyone flips a coin. Heads, they stay in the game; tails, they get wiped out. After ten rounds there is one person standing. He wins a large pot of money.

So is Buffett simply this lucky winner?

<script defer src="/assets/js/buffetts-leverage/knockout.js"></script>
<div id="blv-knockout" class="blv-viz"></div>

[Empirical analysis](https://www.nber.org/papers/w19681) suggests that his success was not random. Rather, it was the result of measured, deliberate action.

His returns are largely explained by two complementary factors.

1) Asset selection, guided by [Ben Graham](https://en.wikipedia.org/wiki/Benjamin_Graham)'s principles: buy undervalued businesses with durable cash flows. Graham's [*The Intelligent Investor*](https://en.wikipedia.org/wiki/The_Intelligent_Investor) came out in 1949. And Buffett has reiterated these principles in his [annual letters](#modal-letters-assets) for decades.

2) Using leverage, to magnify returns. Popular belief is that Buffett despises leverage. On many occasions, he has vehemently [warned against it](#modal-letters-leverage). His actual views, though, are [nuanced](#modal-letters-nuance). He strictly differentiates between [callable](https://en.wikipedia.org/wiki/Margin_(finance)) and [non-callable](https://capitalgains.thediff.co/p/leverageconstraint) forms.

Berkshire runs moderate leverage (1–2x), averaging about 1.6x over 50 years.

<div id="blv-leverage" class="blv-viz"></div>
<script defer src="/assets/js/buffetts-leverage/leverage.js"></script>

*Berkshire's reconstructed leverage multiple over time.*

<hr class="soft">

Buffett's asset selection rules are widely known and well understood by investors. And anyone *can* replicate them.

However, Berkshire's edge comes from its [innovative capital structure](https://www.zacks.com/stock/news/3002110/how-berkshire-turns-insurance-float-into-investment-power). This lets the company borrow hundreds of billions at rates often *lower* than the risk-free rate. That is far beyond the reach of major institutions, let alone individuals.

<div id="blv-cost" class="blv-viz"></div>
<script defer src="/assets/js/buffetts-leverage/cost.js"></script>

*Berkshire's estimated cost of borrowing against the Treasury bill rate.*

Berkshire's insurance business is essentially a leverage machine. They collect premiums from policyholders upfront and pay claims months or years later, as they arise.

This works like a loan from the buyers of insurance. They invest the borrowed money (the [insurance float](#modal-letters-float)) in private businesses, public stocks and US Treasuries. They keep all the upside in these assets beyond the claims.[^banks]

[^banks]: Investing the float creates a [duration mismatch](https://www.investopedia.com/terms/m/maturitymismatch.asp): claims fall due within years, while the premiums sit in assets held for decades.

    But claims are not callable on demand and are largely uncorrelated, so on average the payouts are predictable. In Buffett's words, "though individual policies and claims come and go, the amount of float we hold remains remarkably stable".

    I've written about two other instances of perilous duration mismatch. A [bank]({% post_url 2026-04-09-demand-deposits-are-mispriced-options %})'s deposits and a hedge fund's [margin loan]({% post_url 2026-08-13-borrow-short-bet-long %}) can both be called on demand, usually at the worst moment.

The corporate structure also defers taxes on unrealized gains and benefits from accelerated depreciation — effectively a [zero-interest loan](#modal-letters-taxes) from the government, most of it payable only at Berkshire's election.

Lastly, its track record and [top-tier credit rating](#modal-letters-debt) let Berkshire sell bonds in public markets at low rates.

<hr class="soft">

Put plainly, Buffett buys and holds high-quality assets with moderate, non-callable leverage and cheap financing. Passive strategies that mimic this idea can achieve similar performance on paper.

To illustrate, we built a rudimentary synthetic index[^synthetic] of public stocks, chosen along the lines of Buffett's own preferences, and applied 2.2x leverage. Over the same 50 years, the levered index finishes more than 50% ahead of Berkshire. *However, it takes more leverage to get there. Without Berkshire's financing, you have to take more risk.*

[^synthetic]: The synthetic index is constructed as follows.

    Every year we screen US public stocks using three filters:

    **Cheap** is book-to-market: net worth on the balance sheet divided by value on the stock market.

    **Safe** is low beta: how little the stock has moved with the market over the past five years.

    **Profitable** is operating profit divided by net worth.

    We construct three market-weighted portfolios from the top 20% on each filter: the cheapest, the safest (lowest beta) and the most profitable.
    Then we simply invest a third of the money in each portfolio.

    For the leveraged index, we assume monthly resets, financing at the T-bill rate, and no trading costs or forced liquidations.

<div id="blv-race" class="blv-viz"></div>
<script defer src="/assets/js/buffetts-leverage/race.js"></script>

*Value of $1 invested from 1975 to 2025, on a log scale.*

The example above is only illustrative. We have the benefit of hindsight. To Buffett's credit, he has been doing this for over 50 years, long before any of it was documented.

Today, the average investor's options for leverage are limited. Embedded leverage, through leveraged ETFs and options, is expensive.[^embedded] Margin is cheaper, but it carries liquidation risk and needs active management.

[^embedded]: Embedded leverage products come with [volatility drag]({% post_url 2026-03-15-hidden-costs-leveraged-etfs %}). The multiples the market offers are too high, and the drag grows with the square of the multiple.

We built [2factor](https://2factor.finance/) to close that gap and offer durable long-term leverage that is relatively cheap and bears no risk of liquidation.

Leverage is a double-edged sword. Even without margin calls, leverage magnifies drawdowns, and not everyone can stomach the volatility. Buffett's [warnings](#modal-letters-warnings) hold for good reason.

{% include buffetts-leverage/letters-leverage.html %}
{% include buffetts-leverage/letters-nuance.html %}
{% include buffetts-leverage/letters-float.html %}
{% include buffetts-leverage/letters-taxes.html %}
{% include buffetts-leverage/letters-debt.html %}
{% include buffetts-leverage/letters-assets.html %}
{% include buffetts-leverage/letters-warnings.html %}
