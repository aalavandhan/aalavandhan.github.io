---
layout: post
title: "Programs run on physical machines"
date: 2026-04-20
categories: programming
---

Programmers cosplay mathematicians.

We write functions, prove invariants, compose abstractions. The work *feels* like mathematics — a deep refactor has the same satisfaction as solving a complex equation. And like other theoreticians, we believe our objects are beyond physics.

Programs run on physical machines. They flip bits in physical memory, spin disks, wear out flash cells. They push pixels onto displays, heat up processors, draw power from grids. Every function call is a tiny physical event — transistors switch, heat escapes into the air, current is drawn from the grid.

![Physical landscape of a function call](/assets/images/programs-run-on-physical-machines/fig_landscape.svg)
*From fuel to grid to silicon to heat. Every time.*

The abstraction is so neat that we forget the messy atoms underneath. But physics doesn't disappear. And all physical objects break down.

Code doesn't age. Computers do.

![Physical cascade of a single function call](/assets/images/programs-run-on-physical-machines/fig_cascade.svg)
*What a single `add(a, b)` does to the machine.*

Modern infrastructure has gotten spectacularly good at hiding this.

You deploy to *the cloud*, Your database *scales*, <br/>Your functions are *serverless*, And your machine is *virtual*.

And so you start believing your code is timeless. Same input, same program, same output. You go about your life shipping features, fixing bugs, force pushing to main. Physics is someone else's problem.

Then one day your AWS bill jumps 3x.

![AWS monthly bill](/assets/images/programs-run-on-physical-machines/fig_aws_bill.svg)
*Wait what?*

I rage-open the billing console to find the EC2 generation my instances ran on was being retired. The hardware had aged out.

The [second law](https://en.wikipedia.org/wiki/Second_law_of_thermodynamics) doesn't care about my abstractions. Silicon is fatiguing, fans are spinning and capacitors are leaking. Matter degrades.

Reluctantly, I venture into the blizzard that is the physical world to briefly deal with atoms. Upgrade a few dependencies so my code can run on new silicon.

Then back to the armchair by the fire — until entropy knocks politely on the door again and hands me another invoice.
