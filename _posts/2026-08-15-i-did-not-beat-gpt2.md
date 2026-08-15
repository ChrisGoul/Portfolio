---
title: "I did not beat GPT-2. I got within 1.7 points of it on a $250 GPU."
eyebrow: Machine learning
lede: >-
  A 154M-parameter model, trained from scratch in 46 hours on one RTX 3050, on
  about two dollars of electricity. It lands 1.7 points behind GPT-2-small on
  HellaSwag and ties it on ARC-Easy — using a tenth of the training compute.
  Here's the run, and the three measurement mistakes I had to fix before I could
  believe any of it.
description: >-
  Training a 154M language model from scratch on a single RTX 3050, benchmarked
  properly against GPT-2-small, and the evaluation errors that nearly produced a
  false claim.
date: 2026-08-15
tags: [llm, pretraining, evaluation]
reading_time: 12 min read
---

<dl class="specs full">
  <div><dt>HellaSwag (10,042 items)</dt><dd>28.3 vs 30.0</dd></div>
  <div><dt>Training compute</dt><dd>7.5 &times; 10<sup>17</sup> FLOPs</dd></div>
  <div><dt>Electricity</dt><dd>~$2</dd></div>
</dl>

My benchmark said I had beaten GPT-2-small on HellaSwag. I nearly published that.
Then I looked at the first row of my own training log — the one recorded at step
zero, before the model had learned anything — and found that a randomly
initialised network had scored **31.0** on the same harness. GPT-2-small's
published number is **31.1**.

An untrained model had matched the baseline I spent six weeks trying to beat.
That is a loud signal that the harness, not the model, was doing the talking.

The gap turned out to be three independent measurement errors that all pushed the
same direction, plus a fourth in how I picked the number to compare against. None
of them were exotic. Every one is a two-line convenience that I suspect is sitting
in a lot of small-model write-ups right now.

Here's the real result first, then how I got there.

## What the run cost

GPT-2's original training cost was never published, so the honest modern anchor is
Karpathy's [llm.c reproduction](https://github.com/karpathy/llm.c/discussions/481)
of GPT-2 124M: 8&times;A100 80GB for about 90 minutes, roughly $20 of rented time,
on 10B tokens.

<div class="tbl">
<table>
<thead><tr><th></th><th class="n">this run</th><th class="n">llm.c GPT-2 124M</th><th class="n">ratio</th></tr></thead>
<tbody>
<tr><td>hardware</td><td class="n">1 &times; RTX 3050 8GB</td><td class="n">8 &times; A100 80GB</td><td class="n dim">—</td></tr>
<tr><td>wall clock</td><td class="n">46.5 h</td><td class="n">1.5 h</td><td class="n bad">31&times; longer</td></tr>
<tr><td>training tokens</td><td class="n">0.81 B</td><td class="n">10 B</td><td class="n good">12.3&times; fewer</td></tr>
<tr><td>training FLOPs (6ND)</td><td class="n">7.5 &times; 10<sup>17</sup></td><td class="n">7.4 &times; 10<sup>18</sup></td><td class="n good">9.9&times; less</td></tr>
<tr><td>effective throughput</td><td class="n">4.5 TFLOP/s</td><td class="n">1,378 TFLOP/s</td><td class="n bad">308&times; slower</td></tr>
<tr><td>marginal cost</td><td class="n">~$2 electricity</td><td class="n">~$20 rented</td><td class="n good">~10&times; cheaper</td></tr>
</tbody>
</table>
</div>

The trade is worth stating plainly: the consumer card is **308&times; slower** in
effective throughput, so the same job takes 31&times; longer in wall clock even
though it is a tenth of the work. What you buy with that patience is a training
run that costs about the price of a coffee and needs no cloud account, no
reservation, and no 8-GPU node.

One caveat: my model is 153.8M parameters against GPT-2's 124M, so it is 24%
larger and still lost. The efficiency claim is about tokens and compute, not
about having found a better architecture.

## The run

99,000 steps, batch 32, sequence length 256 — 811M tokens processed over two
epochs of a 405M-token corpus of FineWeb-Edu, Cosmopedia and synthetic
chain-of-thought, tokenised at a 16K vocabulary. Median throughput 4,841
tokens/second, held flat for the entire 46 hours.

<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 720 300" role="img" aria-label="Training and validation loss over 99,000 steps, falling from about 6.0 to 3.10 on a log scale">
<line class="c-grid" x1="52" y1="266.0" x2="706" y2="266.0"/>
<line class="c-grid" x1="52" y1="202.8" x2="706" y2="202.8"/>
<line class="c-grid" x1="52" y1="125.5" x2="706" y2="125.5"/>
<line class="c-grid" x1="52" y1="79.2" x2="706" y2="79.2"/>
<line class="c-grid" x1="52" y1="25.8" x2="706" y2="25.8"/>
<text class="c-tick" x="44" y="269.5" text-anchor="end">6.0</text>
<text class="c-tick" x="44" y="206.3" text-anchor="end">5.0</text>
<text class="c-tick" x="44" y="129.0" text-anchor="end">4.0</text>
<text class="c-tick" x="44" y="82.7" text-anchor="end">3.5</text>
<text class="c-tick" x="44" y="29.3" text-anchor="end">3.0</text>
<polyline fill="none" stroke="var(--ink-soft)" stroke-width="1.4" stroke-opacity=".55" stroke-linejoin="round"
 points="61.8,215.3 68.3,190.4 74.9,172.9 81.4,158.5 88.0,148.3 94.5,140.5 101.0,134.9 107.6,128.1 114.1,123.7 120.7,119.4 127.2,116.1 133.8,112.7 140.3,110.5 146.8,106.5 153.4,105.1 159.9,103.0 166.4,101.2 173.0,96.5 179.5,97.5 186.1,95.9 192.6,92.4 199.2,93.2 205.7,90.2 212.2,89.3 218.8,88.3 225.3,86.6 231.9,84.6 238.4,84.4 244.9,82.6 251.5,80.2 258.0,79.8 264.6,78.8 271.1,79.0 277.6,77.5 284.2,76.6 290.7,76.6 297.2,76.3 303.8,75.6 310.3,73.4 316.9,74.4 323.4,73.1 329.9,73.8 336.5,74.1 343.0,73.0 349.6,74.0 356.1,70.8 362.6,71.7 369.2,71.7 375.7,71.4 382.3,71.0 388.8,70.1 395.4,65.4 401.9,64.7 408.4,65.3 415.0,65.9 421.5,65.4 428.0,63.3 434.6,63.9 441.1,64.5 447.7,62.1 454.2,61.5 460.8,62.2 467.3,60.2 473.8,58.9 480.4,58.3 486.9,57.4 493.5,57.6 500.0,54.5 506.5,54.8 513.1,55.0 519.6,54.6 526.1,52.0 532.7,52.7 539.2,51.8 545.8,50.8 552.3,51.0 558.9,48.2 565.4,48.2 571.9,45.1 578.5,43.3 585.0,40.3 591.5,41.4 598.1,40.7 604.6,40.2 611.2,38.7 617.7,38.2 624.2,36.8 630.8,37.9 637.3,36.8 643.9,38.2 650.4,34.9 657.0,34.6 663.5,35.0 670.0,33.5 676.6,32.5 683.1,31.6 689.6,31.4 696.2,31.5 702.7,30.2"/>
<polyline fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"
 points="58.6,233.6 65.2,199.7 71.8,181.9 78.4,163.9 85.0,154.8 91.6,141.2 98.2,137.3 104.8,131.9 111.5,127.2 118.1,123.1 124.7,118.5 131.3,118.1 137.9,113.3 144.5,107.7 151.1,106.3 157.7,104.9 164.3,103.9 170.9,100.8 177.5,101.9 184.1,100.5 190.7,94.2 197.3,96.4 203.9,94.4 210.5,93.0 217.2,92.6 223.8,88.8 230.4,92.0 237.0,89.7 243.6,84.4 250.2,86.4 256.8,87.7 263.4,88.3 270.0,82.8 276.6,82.0 283.2,81.3 289.8,85.9 296.4,79.9 303.0,81.2 309.6,80.5 316.2,80.5 322.8,80.7 329.5,83.4 336.1,76.1 342.7,78.0 349.3,78.8 355.9,77.4 362.5,77.7 369.1,76.7 375.7,76.9 382.3,74.9 388.9,77.6 395.5,69.9 402.1,73.2 408.7,75.7 415.3,73.0 421.9,68.7 428.5,68.8 435.2,73.2 441.8,74.1 448.4,67.5 455.0,69.2 461.6,69.6 468.2,67.5 474.8,68.4 481.4,70.9 488.0,59.6 494.6,68.5 501.2,64.5 507.8,65.0 514.4,63.9 521.0,61.7 527.6,61.5 534.2,61.2 540.8,63.6 547.5,57.4 554.1,60.3 560.7,54.9 567.3,56.2 573.9,54.6 580.5,54.2 587.1,51.2 593.7,51.2 600.3,51.6 606.9,52.0 613.5,47.7 620.1,47.0 626.7,44.3 633.3,46.3 639.9,46.1 646.5,46.4 653.2,43.9 659.8,42.5 666.4,48.4 673.0,45.8 679.6,43.1 686.2,43.3 692.8,42.2 699.4,42.8 706.0,37.2"/>
<circle cx="706" cy="37.2" r="3.5" fill="var(--accent)"/>
<text class="c-lab" x="698" y="55" text-anchor="end" fill="var(--accent)">final val loss 3.10</text>
<text class="c-lab" x="300" y="88" fill="var(--ink-soft)">train (median per bucket)</text>
<text class="c-lab" x="196" y="128" fill="var(--accent)">validation</text>
<line class="c-axis" x1="52" y1="266" x2="706" y2="266"/>
<line class="c-axis" x1="52" y1="14" x2="52" y2="266"/>
<text class="c-tick" x="52" y="280" text-anchor="middle">0</text>
<text class="c-tick" x="217.2" y="280" text-anchor="middle">25k</text>
<text class="c-tick" x="382.3" y="280" text-anchor="middle">50k</text>
<text class="c-tick" x="547.5" y="280" text-anchor="middle">75k</text>
<text class="c-tick" x="706" y="280" text-anchor="middle">99k</text>
<text class="c-tick" x="379" y="295" text-anchor="middle">training step</text>
</svg>
</div>
<figcaption>Loss on a log axis across the full 46.5-hour run. Validation tracks training the whole way with no divergence — at 0.81B tokens on 154M parameters the model is still firmly undertrained, which is the clearest thing the curve says. The steepening after ~75k steps is the trapezoidal schedule's linear decay to zero.</figcaption>
</figure>

### What it sounds like, over the run

Same prompt — *"The best way to learn"* — sampled at four points:

<div class="samples">
<div class="s"><div class="k">step 500</div><div class="v">…out as complex and find its language. pindlely, we often will help teach us beyond its statistical sexual smaller fires from used to other aromatic software.</div></div>
<div class="s"><div class="k">step 3,000</div><div class="v">…the other is to respond to the situations of impulsivity, as well as culminating the perspective of evolution. I hope to meditate that it means, however, it is a target for groups to discuss reasons for change.</div></div>
<div class="s"><div class="k">step 20,000</div><div class="v">…how to treat a pharmacist is to help friends and family go online with the doctor, a doctor, or a pharmacist. Call us at 2228-8385 (207) or call us at 975-991-2342 (8002)…</div></div>
<div class="s"><div class="k">step 98,999 — final</div><div class="v"><b>…to read well is to get more experience identifying difficult words. This means that improve your vocabulary so that you retain information, which allows you to analyze the meaning better. Try taking a few minutes to practice.</b></div></div>
</div>

Grammar is essentially solved by step 20,000. What keeps improving after that is
*staying on topic* — the pharmacist sample is fluent English that wanders into
invented phone numbers, while the final sample holds a single coherent thread for
four sentences. Knowledge never arrives. At this scale it can't: facts track
tokens, and 0.81B tokens does not buy many facts.

## Fine-tuning: format is cheap, knowledge is not

I then fine-tuned it into a chat model on 107k instruction examples — dialogue,
Dolly, GSM8K, CommonsenseQA, SQuAD — with the loss masked to assistant turns only,
so roughly 8% of tokens carry gradient.

<figure>
<div class="chartbox" style="max-width:420px">
<svg viewBox="0 0 340 190" role="img" aria-label="Supervised fine-tuning loss dropping fast then plateauing near 2.0 after about step 800">
<line class="c-grid" x1="40" y1="152.3" x2="330" y2="152.3"/>
<line class="c-grid" x1="40" y1="93.8" x2="330" y2="93.8"/>
<line class="c-grid" x1="40" y1="35.4" x2="330" y2="35.4"/>
<text class="c-tick" x="33" y="155.8" text-anchor="end">4.0</text>
<text class="c-tick" x="33" y="97.3" text-anchor="end">3.0</text>
<text class="c-tick" x="33" y="38.9" text-anchor="end">2.0</text>
<rect x="107.7" y="12" width="222.3" height="152" fill="var(--mark-soft)"/>
<polyline fill="none" stroke="var(--accent)" stroke-width="1.8" stroke-linejoin="round"
 points="40.0,106.4 49.7,60.7 59.3,56.8 69.0,38.5 78.7,35.9 88.3,32.3 98.0,42.7 107.7,50.3 117.3,43.6 127.0,33.1 136.7,35.7 146.3,38.8 156.0,33.7 165.7,33.9 175.3,39.9 185.0,41.7 194.7,41.6 204.3,30.6 214.0,15.5 223.7,33.6 233.3,48.8 243.0,43.3 252.7,34.3 262.3,28.1 272.0,34.1 281.7,43.9 291.3,41.1 301.0,30.2 310.7,24.6 320.3,30.2 330.0,39.3"/>
<line class="c-axis" x1="40" y1="164" x2="330" y2="164"/>
<line class="c-axis" x1="40" y1="12" x2="40" y2="164"/>
<text class="c-tick" x="40" y="177" text-anchor="middle">0</text>
<text class="c-tick" x="136.7" y="177" text-anchor="middle">2k</text>
<text class="c-tick" x="233.3" y="177" text-anchor="middle">4k</text>
<text class="c-tick" x="330" y="177" text-anchor="middle">6k</text>
<text class="c-lab" x="218" y="140" text-anchor="middle" fill="var(--mark)">4,500 wasted steps</text>
</svg>
</div>
<figcaption>SFT loss over 6,000 steps (2.9 hours). It reaches ~2.0 by step 800 and then oscillates there for the remaining 5,200 steps — mean 2.084 over steps 800–1500, mean 1.976 over the last 1,500. Everything after the shaded boundary bought nothing.</figcaption>
</figure>

The fine-tuned model learns the *shape* of a chat turn almost immediately — when
to start, when to stop, how an answer is supposed to be structured. What it cannot
learn is anything that requires actually knowing things:

<div class="samples">
<div class="s user"><div class="k">user</div><div class="v">What is a dog?</div></div>
<div class="s"><div class="k">model</div><div class="v">A dog is a small, round animal that is a type of bird. They are typically hairy and slim. They are also known for their song and songs.</div></div>
<div class="s user"><div class="k">user</div><div class="v">What is 17 plus 25?</div></div>
<div class="s"><div class="k">model</div><div class="v">17 plus 25 is the number of base wins it is played on. So that means the number of base wins is 25/4 = &lt;&lt;25/4=5&gt;&gt;5 base wins. And the total amount of wins is 5+5+5+5+5+5+5…</div></div>
<div class="s user"><div class="k">user</div><div class="v">Why is the sky blue?</div></div>
<div class="s"><div class="k">model</div><div class="v">Theneast is blue because it is blue because it has &lt;&lt;+&gt;&gt; ground to form and because it is blue because it is at its equinoxes.</div></div>
</div>

That arithmetic answer is my favourite artifact of the whole project. It has
perfectly reproduced GSM8K's calculator-annotation syntax — `<<25/4=5>>` — while
doing arithmetic that is wrong in three separate ways and then falling into a
repetition loop. It learned the *notation of reasoning* from 107k examples without
learning any reasoning.

> **Cost of that lesson:** 2.9 GPU-hours, of which about 2.5 were spent after the
> loss had already flattened. A five-minute look at the curve before launching
> would have saved most of it.

## Then I checked my benchmark

<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 720 330" role="img" aria-label="HellaSwag accuracy logged during training with the uncertainty band of a single 100-item measurement and the true full-set value">
<rect x="48" y="31.7" width="658" height="179.2" fill="var(--mark-soft)"/>
<line class="c-grid" x1="48" y1="266.0" x2="706" y2="266.0"/>
<line class="c-grid" x1="48" y1="219.3" x2="706" y2="219.3"/>
<line class="c-grid" x1="48" y1="172.7" x2="706" y2="172.7"/>
<line class="c-grid" x1="48" y1="126.0" x2="706" y2="126.0"/>
<line class="c-grid" x1="48" y1="79.3" x2="706" y2="79.3"/>
<line class="c-grid" x1="48" y1="32.7" x2="706" y2="32.7"/>
<text class="c-tick" x="40" y="269.5" text-anchor="end">25</text>
<text class="c-tick" x="40" y="222.8" text-anchor="end">30</text>
<text class="c-tick" x="40" y="176.2" text-anchor="end">35</text>
<text class="c-tick" x="40" y="129.5" text-anchor="end">40</text>
<text class="c-tick" x="40" y="82.8" text-anchor="end">45</text>
<text class="c-tick" x="40" y="36.2" text-anchor="end">50</text>
<polyline fill="none" stroke="var(--mark)" stroke-width="2" stroke-linejoin="round"
 points="48.0,210.0 67.9,172.7 87.9,200.7 107.8,126.0 127.8,154.0 147.7,144.7 167.6,144.7 187.6,163.3 207.5,144.7 227.5,154.0 247.4,135.3 267.3,107.3 287.3,144.7 307.2,116.7 327.2,79.3 347.1,107.3 367.0,135.3 387.0,154.0 406.9,163.3 426.8,126.0 446.8,79.3 466.7,116.7 486.7,88.7 506.6,116.7 526.5,126.0 546.5,144.7 566.4,88.7 586.4,107.3 606.3,88.7 626.2,116.7 646.2,135.3 666.1,154.0 686.1,144.7 706.0,116.7"/>
<line x1="48" y1="235.2" x2="706" y2="235.2" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="7 4"/>
<line class="c-axis" x1="48" y1="294" x2="706" y2="294"/>
<line class="c-axis" x1="48" y1="14" x2="48" y2="294"/>
<text class="c-tick" x="48" y="308" text-anchor="middle">0</text>
<text class="c-tick" x="214.2" y="308" text-anchor="middle">25k</text>
<text class="c-tick" x="380.3" y="308" text-anchor="middle">50k</text>
<text class="c-tick" x="546.5" y="308" text-anchor="middle">75k</text>
<text class="c-tick" x="706" y="308" text-anchor="middle">99k</text>
<text class="c-tick" x="377" y="324" text-anchor="middle">training step</text>
<text class="c-lab" x="335" y="60" fill="var(--mark)">what I logged (100 items)</text>
<text class="c-lab" x="60" y="228" fill="var(--accent)">truth: 28.3 on all 10,042 items</text>
<text class="c-tick" x="698" y="46" text-anchor="end" fill="var(--mark)">95% range of a single 100-item measurement</text>
</svg>
</div>
<figcaption>Every HellaSwag score logged during the run. The shaded band is the 95% interval of a <em>single</em> 100-item measurement — the entire apparent learning curve fits inside one error bar. The dashed line is what the same weights score on the full validation set. The trace never touches it.</figcaption>
</figure>

I rebuilt the evaluation as one scoring path shared by every model, cached every
per-item result, and re-ran everything. Here is what each error was worth.

### 1. Sampling noise at n = 100

I benchmarked on 100 items because it ran every 3,000 steps and I wanted it cheap.
Bootstrapping 100-item draws from the fully scored set, 10,000 times, gives a
standard deviation of **4.55** and a 95% range of **20 to 38**. My trace ran 31 to
45 and I read it as a learning curve. It is consistent with flat.

### 2. The first N items are not a random sample

This is the one that cost me the claim. My loader did `items[:n]`, and the head of
HellaSwag's validation split is much easier than the tail:

<div class="tbl">
<table>
<thead><tr><th>slice</th><th class="n">acc_norm</th></tr></thead>
<tbody>
<tr><td>first 100</td><td class="n bad">39.0</td></tr>
<tr><td>first 2,000</td><td class="n">35.0</td></tr>
<tr><td>all 10,042</td><td class="n good">28.3</td></tr>
</tbody>
</table>
</div>

10.7 points of pure slice effect — same weights, same scoring. Every checkpoint I
own shows it, from +3.2 to +9.5 points.

### 3. Two disagreeing scorers in one repo

I had written the scoring twice. The training loop scored
`enc(ctx) + enc(" " + choice)`; the offline script scored `enc(ctx) + enc(choice)`,
no leading space. Under BPE those are different token sequences. Worth **3.6
points** on HellaSwag and ARC-Easy, 0.2 on PIQA — mean spread 1.91, max 3.7. Two
columns in my own experiment log had never been comparable.

And a fourth, in the comparison itself: I was checking a number I measured locally,
on a biased slice, with one tokenisation convention, against a number I read on the
internet, measured on the full set by a different harness.

## The comparison, run properly

Same code, same items, same 256-token context budget, length-normalised accuracy,
paired significance tests. I downloaded GPT-2 and ran it through my own harness
instead of quoting its published numbers.

<div class="tbl">
<table>
<thead><tr><th>benchmark</th><th class="n">mine<br>153.8M</th><th class="n">GPT-2-small<br>124.4M</th><th class="n">Δ</th><th class="n">McNemar p</th><th>verdict</th></tr></thead>
<tbody>
<tr><td>HellaSwag <span class="dim">(10,042)</span></td><td class="n">28.30</td><td class="n">30.01</td><td class="n bad">−1.71</td><td class="n">6.0e−6</td><td>GPT-2 better</td></tr>
<tr><td>ARC-Easy <span class="dim">(2,000)</span></td><td class="n">39.10</td><td class="n">39.80</td><td class="n dim">−0.70</td><td class="n">0.53</td><td class="good">tie</td></tr>
<tr><td>PIQA <span class="dim">(1,838)</span></td><td class="n">59.74</td><td class="n">62.24</td><td class="n bad">−2.50</td><td class="n">0.010</td><td>GPT-2 better</td></tr>
<tr><td>WikiText-2 <span class="dim">(bits/byte)</span></td><td class="n">1.374</td><td class="n">1.133</td><td class="n bad">+0.24</td><td class="n dim">—</td><td>GPT-2 better</td></tr>
</tbody>
</table>
</div>

Bits-per-byte is there because perplexity cannot be compared across tokenisers — my
vocabulary is 16K and GPT-2's is 50,257, so the same string costs a different
number of tokens and per-token perplexity measures different things for each. Bits
per byte normalises by the text instead, and is the one language-modelling number
that is legitimately comparable.

> **What survives.** A 153.8M model trained for 46.5 hours on a single 8 GB
> consumer GPU, on 0.81B tokens and roughly two dollars of electricity, lands
> **1.7 points** behind GPT-2-small on HellaSwag and **ties it** on ARC-Easy, using
> about a **tenth of the training compute**. It is a smaller claim than the one I
> nearly published, and unlike that one it is true.

## How I know the new harness is right

A rebuilt evaluation that produces a more convenient answer is worth nothing
without calibration, so it gets checked before it gets to say anything.

<div class="tbl">
<table>
<thead><tr><th>check</th><th class="n">expected</th><th class="n">got</th></tr></thead>
<tbody>
<tr><td>Config inferred from tensor shapes</td><td class="n">153.8M params</td><td class="n good">153.8M</td></tr>
<tr><td>Validation loss reproduced from checkpoint</td><td class="n">3.1009</td><td class="n good">3.1422</td></tr>
<tr><td>GPT-2-small vs its published HellaSwag</td><td class="n">~31.1</td><td class="n good">30.01</td></tr>
<tr><td>First-100 rescore vs the live bench I logged</td><td class="n">36 – 45</td><td class="n good">39.0</td></tr>
</tbody>
</table>
</div>

The last row matters most: scoring the same 100 items the same way the training
loop did reproduces what the training loop reported, so the new harness is a
superset of the old one rather than a different thing that happens to disagree. The
old numbers were computed correctly — they were answering a much narrower question
than I thought. And the GPT-2 row is the external anchor: within 1.1 points of a
widely published figure, with a 256-token cap against its native 1024.

## What I'd tell anyone training a small model

- **Never take the first *n* rows of a benchmark.** Shuffle with a fixed seed or use
  the whole set. This one cost me 10.7 points and nearly a false claim.
- **Put an interval on every number.** At n=100 the 95% interval is about ±9 points —
  wider than almost any effect worth reporting.
- **Score your baseline with your own code.** The gap between two harnesses is bigger
  than the gap you are trying to detect.
- **Use paired tests.** My model and GPT-2 disagree on 1,430 of 10,042 HellaSwag
  items; comparing two independent confidence intervals throws that structure away.
- **Watch the fine-tuning curve before committing to a step count.** 4,500 of my
  6,000 SFT steps were wasted.
- **Grep for a second copy of your scoring function.** Mine had two, three points apart.

None of these are exotic bugs. Every one is a two-line convenience — take the first
hundred, skip the error bar, quote the published baseline, write the scorer twice —
and together they turned a legitimate result into an illegitimate one. The
measurement was harder than the training.

---

**Model.** 20 layers, 768 dim, 12 heads, 16K tied vocabulary. Muon on 2D hidden
matrices with Adam on embeddings and head, RoPE, QK-norm, ReLU² MLPs, zero-init
residual projections, parameter-free RMSNorm, logit soft-capping, trapezoidal LR,
gradient checkpointing. Corpus: FineWeb-Edu + Cosmopedia + synthetic
chain-of-thought, 405M unique tokens, 2 epochs. Final validation loss 3.10.

**Cost basis.** Electricity assumes ~225 W system draw over 46.5 h at US average
residential rates; the range across plausible assumptions is $1.20–$3.50.
Comparison figures for llm.c are as published. GPT-2's original training cost was
never disclosed by OpenAI.
