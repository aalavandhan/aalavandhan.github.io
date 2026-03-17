---
layout: post
title: "Who Meets Whom: The Privacy Cost of Location Data"
date: 2017-11-29
categories: privacy research
---

Most people understand the implications of virtual meetings through emails and phone calls. Some of us are even aware that they are being constantly tracked. However, we assume that our physical meetings remain private. It is extremely unlikely that a bad actor will follow around everyone on earth all the time. Thus we seem to care less, if not at all, about the privacy of our physical meetings.

Multiple systems are already recording your location. Government agencies, telecom and tech companies use technologies to track user mobility with surprising precision, often without users realizing it. Back in 2014, [The Post revealed](https://www.washingtonpost.com/apps/g/page/world/how-the-nsa-is-tracking-people-right-now/634/) that the NSA was collecting location data of people living in the US through hidden back-doors into mobile phone companies.

![Tracking technologies: Cellular location identification, GPS systems, Wi-Fi Localization](/assets/images/who-meets-whom/tracking_technologies.webp)

Google recently [admitted to secretly tracking](https://www.theverge.com/2017/11/21/16684818/google-location-tracking-cell-tower-data-android-os-firebase-privacy) location data from android devices, even when the GPS was explicitly turned off, potentially affecting over two billion monthly active android users worldwide.

You'd think this volume of data, spanning zettabytes, is too much to make any sense out of. Making sense is equivalent to finding needles in a hay stack. There has also been research into [location privacy](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42852.pdf) and customer pushback has led to adoption of recent privacy techniques into how some companies collect data.

But scale and algorithms are good at exactly this kind of problem. Patterns that would be invisible to a human analyst combing through raw data are easy for machines to pick out. Moreover these [privacy techniques are at a relatively nascent stage](https://arxiv.org/pdf/1709.02753.pdf) and they do not hide everything about the user.

[Recent research](https://arxiv.org/pdf/1708.08221.pdf) has pointed out that we can infer sensitive information about people and who they meet, just from location data.

At a population scale, location tracking can reveal who you know, where you go, and when you meet, without anyone physically following anyone.

![NSA Co-Traveller Program](/assets/images/who-meets-whom/nsa_co_traveller.gif)

With this much location data available, organizations can track nearly everyone's physical meetings. The Post revelations document the [NSA co-traveller program](https://www.washingtonpost.com/apps/g/page/world/how-the-nsa-is-tracking-people-right-now/634/) which looks out for physical meetings between a known perpetrator to identify potential co-conspirators, at a global level.

A couple who meet frequently are likely to be socially connected — friends, relatives, co-workers, partners. Using this intuition, researchers show that one can [accurately infer users' social connections](https://infolab.usc.edu/DocsDemos/sigra619.pdf) from location data of a significant population. Where and when people meet can also reveal the nature of relationship between the pair. For example, frequent meetings at a coffee shop near an office might indicate colleagues, while a weekly visit to a hospital might indicate a health situation.

Working with the [InfoLab at USC](https://infolab.usc.edu/), my [thesis](https://search.proquest.com/openview/e0a489c76222242421780cda54c6714c/1?pq-origsite=gscholar&cbl=18750) introduced this problem and proposed methods to preserve the privacy of meetings, including co-location k-anonymity. The work was [published in IEEE TKDE](https://ieeexplore.ieee.org/document/8847050).
