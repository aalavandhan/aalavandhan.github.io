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

<p style="text-align:center; margin: 2em 0;">
<svg viewBox="0 0 500 473" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" style="max-width:500px; width:100%; height:auto;">
  <defs>
    <marker id="hp-arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/>
    </marker>
  </defs>
  <rect x="50" y="392" width="400" height="55" rx="6" fill="#eff6ff" stroke="#3b82f6"/>
  <text x="250" y="416" text-anchor="middle" font-size="14" font-weight="600">Saver / household</text>
  <text x="250" y="434" text-anchor="middle" font-size="11" fill="#64748b">demand-redeemable claim, no maturity</text>
  <line x1="250" y1="389" x2="250" y2="359" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#hp-arr)"/>
  <text x="265" y="379" font-size="10" fill="#94a3b8" font-style="italic">duration risk</text>
  <rect x="50" y="299" width="400" height="55" rx="6" fill="#dbeafe" stroke="#3b82f6"/>
  <text x="250" y="323" text-anchor="middle" font-size="14" font-weight="600">Commercial bank</text>
  <text x="250" y="341" text-anchor="middle" font-size="11" fill="#64748b">long assets, demand liabilities, equity buffer</text>
  <line x1="250" y1="296" x2="250" y2="266" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#hp-arr)"/>
  <text x="265" y="286" font-size="10" fill="#94a3b8" font-style="italic">duration risk</text>
  <rect x="50" y="206" width="400" height="55" rx="6" fill="#cfe4fc" stroke="#3b82f6"/>
  <text x="250" y="230" text-anchor="middle" font-size="14" font-weight="600">FDIC / deposit insurance</text>
  <text x="250" y="248" text-anchor="middle" font-size="11" fill="#64748b">guarantees deposits up to $250k</text>
  <line x1="250" y1="203" x2="250" y2="173" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#hp-arr)"/>
  <text x="265" y="193" font-size="10" fill="#94a3b8" font-style="italic">duration risk</text>
  <rect x="50" y="113" width="400" height="55" rx="6" fill="#bfdbfe" stroke="#3b82f6"/>
  <text x="250" y="137" text-anchor="middle" font-size="14" font-weight="600">Central bank</text>
  <text x="250" y="155" text-anchor="middle" font-size="11" fill="#64748b">long assets, demand liabilities</text>
  <line x1="250" y1="110" x2="250" y2="80" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#hp-arr)"/>
  <text x="265" y="100" font-size="10" fill="#94a3b8" font-style="italic">duration risk</text>
  <rect x="50" y="20" width="400" height="55" rx="6" fill="#fecaca" stroke="#dc2626"/>
  <text x="250" y="44" text-anchor="middle" font-size="14" font-weight="600">Currency holder</text>
  <text x="250" y="62" text-anchor="middle" font-size="11" fill="#64748b">no backstop above — bears the residual via inflation</text>
</svg>
<br/>
<em style="font-size: 0.9em; color: #64748b;">Duration risk starts at the bank and gets passed up the stack. The top layer has no one above it.</em>
</p>


## Demand deposits are puts

Depositors hold the right to convert their balance into cash on demand at face value, regardless of what the bank's assets are actually worth at that moment. The bank has to honor this no matter what.

Each deposit is a perpetual [American put](https://www.investopedia.com/terms/p/putoption.asp) on the bank's solvency, struck at par. It's what protects depositors when the bank's assets fall below par. They still get par, and the loss runs up the stack: bank equity, then FDIC, then Fed, then taxpayer.

<p style="text-align:center; margin: 2em 0;">
<svg viewBox="0 0 500 360" xmlns="http://www.w3.org/2000/svg" font-family="system-ui, sans-serif" style="max-width:480px; width:100%; height:auto;">
  <!-- Zone fills within put payoff triangle (below par) -->
  <!-- Fed/taxpayer: $0 to $50 -->
  <polygon points="90,280 90,80 215,80 215,180" fill="#fecaca" stroke="none"/>
  <!-- FDIC: $50 to $90 -->
  <polygon points="215,180 215,80 315,80 315,100" fill="#dbeafe" stroke="none"/>
  <!-- Bank equity absorbs: $90 to $100 -->
  <polygon points="315,100 315,80 340,80" fill="#eff6ff" stroke="none"/>
  <!-- Bank's spread (above par) -->
  <polygon points="340,80 405,80 405,28" fill="#dcfce7" stroke="none"/>
  <!-- Axes -->
  <line x1="90" y1="280" x2="440" y2="280" stroke="#94a3b8" stroke-width="1"/>
  <line x1="90" y1="280" x2="90" y2="15" stroke="#94a3b8" stroke-width="1"/>
  <!-- Par dashed line -->
  <line x1="340" y1="80" x2="340" y2="280" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
  <!-- Zone boundary dashed lines -->
  <line x1="315" y1="80" x2="315" y2="280" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="215" y1="80" x2="215" y2="280" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
  <!-- Asset value line (diagonal, full range) -->
  <polyline points="90,280 340,80 405,28" fill="none" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,3"/>
  <!-- Depositor payoff line (solid): flat at $100 -->
  <line x1="90" y1="80" x2="430" y2="80" stroke="#3b82f6" stroke-width="2.5"/>
  <!-- X-axis ticks and labels -->
  <line x1="90" y1="277" x2="90" y2="283" stroke="#94a3b8" stroke-width="1"/>
  <text x="90" y="296" text-anchor="middle" font-size="10" fill="#64748b">$0</text>
  <line x1="215" y1="277" x2="215" y2="283" stroke="#94a3b8" stroke-width="1"/>
  <text x="215" y="296" text-anchor="middle" font-size="10" fill="#64748b">$50</text>
  <line x1="315" y1="277" x2="315" y2="283" stroke="#94a3b8" stroke-width="1"/>
  <text x="315" y="296" text-anchor="middle" font-size="10" fill="#64748b">$90</text>
  <line x1="340" y1="277" x2="340" y2="283" stroke="#94a3b8" stroke-width="1"/>
  <text x="340" y="296" text-anchor="middle" font-size="10" fill="#64748b">$100</text>
  <line x1="405" y1="277" x2="405" y2="283" stroke="#94a3b8" stroke-width="1"/>
  <text x="405" y="296" text-anchor="middle" font-size="10" fill="#64748b">$120</text>
  <!-- Y-axis ticks and labels -->
  <line x1="87" y1="280" x2="93" y2="280" stroke="#94a3b8" stroke-width="1"/>
  <text x="82" y="283" text-anchor="end" font-size="10" fill="#64748b">$0</text>
  <line x1="87" y1="180" x2="93" y2="180" stroke="#94a3b8" stroke-width="1"/>
  <text x="82" y="183" text-anchor="end" font-size="10" fill="#64748b">$50</text>
  <line x1="87" y1="80" x2="93" y2="80" stroke="#94a3b8" stroke-width="1"/>
  <text x="82" y="83" text-anchor="end" font-size="10" fill="#64748b">$100</text>
  <!-- Axis labels -->
  <text x="265" y="340" text-anchor="middle" font-size="11" fill="#475569">bank's assets per $100 of deposits</text>
  <text x="28" y="160" font-size="11" fill="#475569" transform="rotate(-90 28 160)">$ per $100 of deposits</text>
  <!-- Zone labels (below par) -->
  <text x="145" y="185" text-anchor="middle" font-size="10" fill="#991b1b" font-style="italic">Fed / taxpayer</text>
  <text x="262" y="125" text-anchor="middle" font-size="10" fill="#1e40af" font-style="italic">FDIC</text>
  <!-- Bank equity callout (zone too narrow for inline label) -->
  <text x="355" y="110" font-size="10" fill="#64748b" font-style="italic">bank equity</text>
  <line x1="350" y1="108" x2="332" y2="92" stroke="#94a3b8" stroke-width="0.75"/>
  <!-- Bank's spread label (above par) -->
  <text x="390" y="60" font-size="10" fill="#15803d" font-style="italic">bank's spread</text>
  <!-- Line labels -->
  <text x="95" y="68" font-size="11" fill="#3b82f6" font-weight="600">depositor always gets $100</text>
  <text x="130" y="265" font-size="11" fill="#64748b">asset value</text>
</svg>
<br/>
<em style="font-size: 0.9em; color: #64748b;">Below par, losses run up the stack. Above par, the bank keeps the spread. The depositor gets $100 either way.</em>
</p>

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

