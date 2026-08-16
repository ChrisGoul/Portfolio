---
title: "I did not beat GPT-2"
order: 1
lede: >-
  A 154M-parameter model trained from scratch in 46 hours on one RTX 3050. It
  lands 1.7 points behind GPT-2-small at a tenth the training compute — and I
  only found that out after fixing three mistakes in how I was measuring it.
description: >-
  Training a 154M language model from scratch on a single RTX 3050 and
  benchmarking it properly against GPT-2-small.
meta: ["153.8M params", "0.81B tokens", "46.5 h", "RTX 3050 8 GB"]
---

## What I built

A transformer and its whole training harness, written from scratch in PyTorch,
sized to fit an 8 GB consumer GPU: Muon on the 2D hidden matrices with Adam on
embeddings and head, RoPE, QK-norm, ReLU² MLPs, zero-init residual projections,
logit soft-capping, trapezoidal LR. Gradient checkpointing is what makes 154M
fit at all — activations were the wall, and recomputing them cut memory from
7.9 GB to 2.8 GB.

99,000 steps on 0.81B tokens of FineWeb-Edu, Cosmopedia and synthetic
chain-of-thought at a 16K vocabulary. Final validation loss 3.10. Then a
supervised fine-tune into a chat model on 107k instruction examples.

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
<text class="c-lab" x="698" y="55" text-anchor="end" fill="var(--accent)">3.10</text>
<text class="c-lab" x="300" y="88" fill="var(--ink-soft)">train</text>
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
<figcaption>Loss on a log axis across all 46.5 hours. Validation tracks training the
whole way with no divergence — at 0.81B tokens on 154M parameters the model is
still firmly undertrained, which is the clearest thing the curve says.</figcaption>
</figure>

## Result

Measured against GPT-2-small under one shared harness — same code, same items,
same context budget, paired significance tests:

<div class="tbl">
<table>
<thead><tr><th>benchmark</th><th class="n">mine</th><th class="n">GPT-2-small</th><th class="n">Δ</th></tr></thead>
<tbody>
<tr><td>HellaSwag (10,042)</td><td class="n">28.30</td><td class="n">30.01</td><td class="n bad">−1.71</td></tr>
<tr><td>ARC-Easy (2,000)</td><td class="n">39.10</td><td class="n">39.80</td><td class="n dim">tie</td></tr>
<tr><td>PIQA (1,838)</td><td class="n">59.74</td><td class="n">62.24</td><td class="n bad">−2.50</td></tr>
<tr><td>WikiText-2 (bits/byte)</td><td class="n">1.374</td><td class="n">1.133</td><td class="n bad">worse</td></tr>
</tbody>
</table>
</div>

I lost. But 1.7 points behind on HellaSwag and level on ARC-Easy, at **~12×
fewer tokens**, **~10× less compute** and about **$2 of electricity** against
$20 of rented A100 time, is a result I'll take.

## Three things I got wrong

My live benchmark said HellaSwag ≈ 40, comfortably above GPT-2's published 31.1.
Then I noticed my *untrained* model had scored 31.0 on the same harness. Three
ordinary mistakes, all pushing the same way:

- **n = 100 is noise.** Bootstrapped, a 100-item HellaSwag run on this model
  returns anywhere from 20 to 38. My whole "learning curve" fit inside one error bar.
- **`items[:n]` is not a random sample.** The head of HellaSwag's validation split
  is much easier than the tail: same weights scored **39.0** on the first 100,
  **35.0** on the first 2,000, **28.3** on all 10,042.
- **I had written the scoring twice.** Training loop used `enc(ctx) + enc(" " + choice)`,
  offline script used no leading space. Under BPE those differ by up to 3.6 points,
  so two columns in my own experiment log were never comparable.

## What the model is actually like

Grammar is solved by ~step 20,000; what keeps improving after that is staying on
topic. Knowledge never arrives — 0.81B tokens doesn't buy facts. After
fine-tuning, asked to add 17 and 25:

> 17 plus 25 is the number of base wins it is played on. So that means the number
> of base wins is 25/4 = `<<25/4=5>>`5 base wins.

It reproduced GSM8K's calculator-annotation syntax perfectly while getting the
arithmetic wrong three ways. It learned the *notation* of reasoning from 107k
examples without learning any reasoning. Format is cheap; knowledge is not.

## Takeaways

- Never take the first *n* rows of a benchmark. Shuffle, or use all of it.
- Put an interval on every number. At n=100 that interval is ±9 points.
- Score your baseline with your own code — harness-to-harness differences are
  bigger than the effect you're chasing.
- Watch the fine-tuning curve before picking a step count. 4,500 of my 6,000 SFT
  steps bought nothing.

The measurement turned out to be harder than the training.
