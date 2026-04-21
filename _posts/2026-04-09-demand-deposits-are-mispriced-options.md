---
layout: post
title: "Demand deposits are mispriced options"
date: 2026-04-09
categories: finance
---

*And everyone is cool with this? Lol*

Banks are in the business of taking [deposits](https://www.investopedia.com/terms/d/demanddeposit.asp) and making loans. The deposits are short-duration: redeemable on demand, no notice required. The loans are long-duration: 5-year corporate term loans, 10-year commercial mortgages, 30-year residential mortgages. The bank earns the spread between what it pays depositors and what it charges borrowers — the classic [duration mismatch](https://www.investopedia.com/terms/m/maturitymismatch.asp).

## The mismatch is structural

Depositors want optionality — they don't know whether they'll need the cash next month or next year, so they want the right to withdraw whenever.

Borrowers want commitment — a homeowner with a 30-year mortgage can't afford to have their rate reset or their loan recalled.

This is a structural conflict between optionality and commitment, not a coordination failure better matching could solve. Even a depositor and borrower with identical time horizons would disagree on the *shape* of the contract. One wants it cancellable, the other wants it locked. Someone has to bear the gap.


## Banks try to patch it

The traditional fix is [statistical pooling](https://www.investopedia.com/terms/f/fractionalreservebanking.asp). Most depositors don't withdraw on most days, so even though everyone *can* pull their money at any time, only a small fraction actually does. The bank keeps enough cash on hand for that fraction and lends the rest out long-term. A thin equity buffer absorbs the day-to-day variance, and most of the time everyone is happy.

Until a panic hits, everyone wants out at once, the buffer isn't sized for it, and the central bank steps in as [lender of last resort](https://www.investopedia.com/terms/l/lenderoflastresort.asp). The mismatch doesn't go away — the loss just gets passed up the stack, from depositor to bank equity to FDIC to central bank to taxpayer. (*Credit risk, operational risk, market risk all matter too, but duration is the structural one — it exists even when every loan performs.*)

![Duration risk stack](/assets/images/demand-deposits-are-mispriced-options/fig_duration_stack.svg)
*Duration risk starts at the bank and gets passed up the stack. The top layer has no one above it.*


## Demand deposits are puts

Depositors hold the right to convert their balance into cash on demand at face value, regardless of what the bank's assets are actually worth at that moment. The bank has to honor this no matter what.

Each deposit is a perpetual [American put](https://www.investopedia.com/terms/p/putoption.asp) on the bank's solvency, struck at par. It's what protects depositors when the bank's assets fall below par. They still get par, and the loss runs up the stack: bank equity, then FDIC, then Fed, then taxpayer.

![Put payoff diagram](/assets/images/demand-deposits-are-mispriced-options/fig_put_payoff.svg)
*Below par, losses run up the stack. Above par, the bank keeps the spread. The depositor gets $100 either way.*

Depositors are shopping for an APY, not pricing a put. The APY is set downstream of central bank rates, not by what the put is actually worth.

You could argue the spread *is* the put premium — the price the bank charges for guaranteeing on-demand par redemption. But the spread doesn't track the put. When the bank extends duration, the put becomes worth more, but depositor rates don't move to reflect it. The cost shows up in bank equity, not in deposit rates. Equity holders are short the put and their mark-to-market reflects it. Depositors never see the signal.

## Puts are mispriced

The value of that put comes from the duration mismatch. A cash-only bank has no mismatch and nothing to protect against. The put is worthless. (*This is [narrow banking](https://en.wikipedia.org/wiki/Narrow_banking), which is what [GENIUS](https://www.congress.gov/bill/119th-congress/senate-bill/394) [stablecoins](https://www.investopedia.com/terms/s/stablecoin.asp) are.*) 

A bank holding 30-year mortgages funded on demand has a big mismatch and a lot to protect against. The put is worth a lot.

The bigger the mismatch, the more risk embedded in the bank's balance sheet, and the more of it gets passed up the stack instead of falling on depositors. Depositors hold the put for free, and the gap between what it's worth and what they pay for it is the mispricing.

The mismatch never goes away, and neither does the mispricing. Every checking account, savings account, money market account — any balance redeemable at par on demand — carries it.


## Mispricing is accepted

This mispricing is deliberate. Society accepts that a stable, par-value payments system is worth more than making depositors pay for the put.

Depositors get a subsidized lunch — guaranteed by the rest of society. And everyone is cool with this. Because nobody sees the itemized bill.

---

**Further reading:**
- [Banking the Future](https://thinking.farm/essays/2023-03-29-banking-the-future-p1/) — a deeper exploration of banking's structural fragility.
- [Diamond and Dybvig (1983)](https://www.bu.edu/econ/files/2012/01/DD83jpe.pdf) formalized banks as providers of liquidity insurance against privately-known consumption shocks — the paper that won the [2022 Nobel](https://www.nobelprize.org/prizes/economic-sciences/2022/summary/).
- [Robert Merton (1977)](https://www.sciencedirect.com/science/article/abs/pii/0378426677900152) modeled deposit insurance as a put option written by the FDIC on the bank's assets — the foundational framing for deposits-as-puts.

