---
layout: post
title: "Who Meets Whom"
subtitle: "The Privacy Cost of Location Data"
date: 2017-11-29
categories: privacy research
description: "We assume our physical meetings stay private. But location data can reconstruct who met whom, when, and where — at a far larger privacy cost than most people assume."
image: /assets/images/og/who-meets-whom.png
---

Most people understand the implications of virtual meetings through emails and phone calls. Some of us are even aware that they are being constantly tracked. However, we assume that our physical meetings remain private. It is extremely unlikely that someone would follow everyone around all the time. Thus we seem to care less, if not at all, about the privacy of our physical meetings.

Multiple systems collect location data at scale. Telecom, tech companies, and [governments](https://www.washingtonpost.com/news/the-switch/wp/2013/12/10/new-documents-show-how-the-nsa-infers-relationships-based-on-mobile-location-data/) log user location with more precision than most people expect.

![Tracking technologies: Cellular location identification, GPS systems, Wi-Fi Localization](/assets/images/who-meets-whom/tracking_technologies.webp)

Google [was found to be collecting](https://www.theverge.com/2017/11/21/16684818/google-location-tracking-cell-tower-data-android-os-firebase-privacy) location data from Android devices even when GPS was explicitly turned off, potentially affecting over two billion monthly active users worldwide.

You'd think this volume of data, spanning zettabytes, is too much to make any sense out of. There has been research into [location privacy](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42852.pdf) and customer pushback has led to adoption of privacy techniques into how some companies collect data.

But scale and algorithms are good at exactly this kind of problem. Patterns that would be invisible to a human analyst combing through raw data are easy for machines to pick out. Moreover these [privacy techniques are at a relatively nascent stage](https://arxiv.org/pdf/1709.02753.pdf) and they do not hide everything about the user.

[Recent research](https://arxiv.org/pdf/1708.08221.pdf) shows that location data alone is enough to piece together who you know, where you go, and when you meet. With enough data, it's possible to [infer social connections](https://infolab.usc.edu/DocsDemos/sigra619.pdf) across large populations.

<div class="coloc-figure">
<style>
.coloc-figure { margin: 40px 0; }
.coloc-figure svg#viz {
  display: block; width: 100%; height: auto;
  background: #d9e8eb;
  border: 1px solid #e6e6e6; border-radius: 4px;
  box-shadow: 0 2px 14px rgba(0, 0, 0, .06);
  cursor: pointer; -webkit-user-select: none; user-select: none;
}
.coloc-figure .hud-label { fill: #fff; font-weight: 800; letter-spacing: .08em; }
</style>
<svg id="viz" viewBox="0 0 600 376" role="img" aria-labelledby="colocTitle colocDesc">
<title id="colocTitle">Moving user co-location map</title>
<desc id="colocDesc">A red tracked user and 28 contacts move through a street network. Contacts turn red when they enter the tracked user's moving co-location radius, and each entry is counted.</desc>
<defs>
<linearGradient id="mapWash" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#dcecef" />
<stop offset="1" stop-color="#d3e5e9" />
</linearGradient>
<linearGradient id="edgeGlow" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#6389cb" stop-opacity=".95" />
<stop offset=".05" stop-color="#6389cb" stop-opacity="0" />
<stop offset=".95" stop-color="#6389cb" stop-opacity="0" />
<stop offset="1" stop-color="#6389cb" stop-opacity=".95" />
</linearGradient>
<filter id="softGlow" x="-100%" y="-100%" width="300%" height="300%">
<feGaussianBlur stdDeviation="2.6" result="blur" />
<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="paper" x="-10%" y="-10%" width="120%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="2" seed="11" result="noise" />
<feColorMatrix in="noise" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .045 0" result="faint" />
<feBlend in="SourceGraphic" in2="faint" mode="multiply" />
</filter>
<clipPath id="mapClip"><rect x="14" y="10" width="572" height="356" rx="1"/></clipPath>
</defs>
<rect width="600" height="376" fill="#eef4f4" />
<rect x="8" y="7" width="584" height="362" fill="url(#mapWash)" stroke="#718fd1" stroke-width="3" filter="url(#paper)" />
<rect x="8" y="7" width="584" height="362" fill="url(#edgeGlow)" pointer-events="none" />
<g clip-path="url(#mapClip)">
<g id="roads"></g>
<g id="cellFills"></g>
<g id="cells"></g>
<g id="sites"></g>
<g id="links"></g>
<g id="contacts"></g>
<g id="target"></g>
<g id="entryBursts"></g>
</g>
<g id="hud" transform="translate(432 32)" pointer-events="none">
<rect width="144" height="31" rx="4" fill="#18304c" opacity=".72" />
<circle cx="13" cy="10" r="3.5" fill="#d94232" />
<text id="hudCurrent" class="hud-label" x="23" y="13" font-size="9">0 IN RANGE</text>
<text id="hudTotal" x="13" y="25" fill="#d9e5ea" font-size="8">0 co-location entries</text>
</g>
<rect x="8" y="7" width="584" height="362" fill="none" stroke="#6a86c8" stroke-width="3" pointer-events="none" />
</svg>
<script src="/assets/js/who-meets-whom/co_location.js"></script>
</div>

Two people who meet frequently are likely connected — friends, relatives, co-workers, partners. Where and when they meet can reveal the nature of the relationship. Frequent meetings at a coffee shop near an office might indicate colleagues, while a weekly visit to a hospital might indicate a health situation.

Working with the [InfoLab at USC](https://infolab.usc.edu/), my [thesis](https://drive.google.com/file/d/1XdZ7jh8FBSiUH5pZo3D13o9MLjXy8LKF/view?usp=drivesdk) introduced this problem and proposed methods to preserve the privacy of meetings. The core idea is co-location k-anonymity: if you're going to release location data, make sure any meeting implied by the data could plausibly involve at least k different people, so no specific pair can be singled out. The work was [published in IEEE TKDE](https://ieeexplore.ieee.org/document/8847050).
