---
layout: post
title: "Who Meets Whom: The Privacy Cost of Location Data"
date: 2017-11-29
categories: privacy research
---

Most people understand the implications of virtual meetings through emails and phone calls. Some of us are even aware that they are being constantly tracked. However, we assume that our physical meetings remain private. It is extremely unlikely that someone would follow everyone around all the time. Thus we seem to care less, if not at all, about the privacy of our physical meetings.

Multiple systems collect location data at scale. Telecom, tech companies, and [governments](https://www.washingtonpost.com/news/the-switch/wp/2013/12/10/new-documents-show-how-the-nsa-infers-relationships-based-on-mobile-location-data/) log user location with more precision than most people expect.

![Tracking technologies: Cellular location identification, GPS systems, Wi-Fi Localization](/assets/images/who-meets-whom/tracking_technologies.webp)

Google [was found to be collecting](https://www.theverge.com/2017/11/21/16684818/google-location-tracking-cell-tower-data-android-os-firebase-privacy) location data from Android devices even when GPS was explicitly turned off, potentially affecting over two billion monthly active users worldwide.

You'd think this volume of data, spanning zettabytes, is too much to make any sense out of. There has been research into [location privacy](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/42852.pdf) and customer pushback has led to adoption of privacy techniques into how some companies collect data.

But scale and algorithms are good at exactly this kind of problem. Patterns that would be invisible to a human analyst combing through raw data are easy for machines to pick out. Moreover these [privacy techniques are at a relatively nascent stage](https://arxiv.org/pdf/1709.02753.pdf) and they do not hide everything about the user.

[Recent research](https://arxiv.org/pdf/1708.08221.pdf) shows that location data alone is enough to piece together who you know, where you go, and when you meet. With enough data, it's possible to [infer social connections](https://infolab.usc.edu/DocsDemos/sigra619.pdf) across large populations.

![Co-location tracking visualization](/assets/images/who-meets-whom/nsa_co_traveller.gif)

Two people who meet frequently are likely connected — friends, relatives, co-workers, partners. Where and when they meet can reveal the nature of the relationship. Frequent meetings at a coffee shop near an office might indicate colleagues, while a weekly visit to a hospital might indicate a health situation.

Working with the [InfoLab at USC](https://infolab.usc.edu/), my [thesis](https://drive.google.com/file/d/1XdZ7jh8FBSiUH5pZo3D13o9MLjXy8LKF/view?usp=drivesdk) introduced this problem and proposed methods to preserve the privacy of meetings. The core idea is co-location k-anonymity: if you're going to release location data, make sure any meeting implied by the data could plausibly involve at least k different people, so no specific pair can be singled out. The work was [published in IEEE TKDE](https://ieeexplore.ieee.org/document/8847050).
