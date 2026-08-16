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
<svg viewBox="0 0 720 300" role="img" aria-label="Training and validation loss over 99,000 steps, descending from about 6.0 to 3.10 on a log scale">
<line class="c-grid" x1="52" y1="14.0" x2="706" y2="14.0"/>
<line class="c-grid" x1="52" y1="77.2" x2="706" y2="77.2"/>
<line class="c-grid" x1="52" y1="154.5" x2="706" y2="154.5"/>
<line class="c-grid" x1="52" y1="200.8" x2="706" y2="200.8"/>
<line class="c-grid" x1="52" y1="254.2" x2="706" y2="254.2"/>
<text class="c-tick" x="44" y="17.5" text-anchor="end">6.0</text>
<text class="c-tick" x="44" y="80.7" text-anchor="end">5.0</text>
<text class="c-tick" x="44" y="158.0" text-anchor="end">4.0</text>
<text class="c-tick" x="44" y="204.3" text-anchor="end">3.5</text>
<text class="c-tick" x="44" y="257.7" text-anchor="end">3.0</text>
<polyline fill="none" stroke="var(--ink-soft)" stroke-width="1.4" stroke-opacity=".55" stroke-linejoin="round"
 points="61.8,64.7 68.3,89.6 74.9,107.1 81.4,121.5 88.0,131.7 94.5,139.5 101.0,145.1 107.6,151.9 114.1,156.3 120.7,160.6 127.2,163.9 133.8,167.3 140.3,169.5 146.8,173.5 153.4,174.9 159.9,177.0 166.4,178.8 173.0,183.5 179.5,182.5 186.1,184.1 192.6,187.6 199.2,186.8 205.7,189.8 212.2,190.7 218.8,191.7 225.3,193.4 231.9,195.4 238.4,195.6 244.9,197.4 251.5,199.8 258.0,200.2 264.6,201.2 271.1,201.0 277.6,202.5 284.2,203.4 290.7,203.4 297.2,203.7 303.8,204.4 310.3,206.6 316.9,205.6 323.4,206.9 329.9,206.2 336.5,205.9 343.0,207.0 349.6,206.0 356.1,209.2 362.6,208.3 369.2,208.3 375.7,208.6 382.3,209.0 388.8,209.9 395.4,214.6 401.9,215.3 408.4,214.7 415.0,214.1 421.5,214.6 428.0,216.7 434.6,216.1 441.1,215.5 447.7,217.9 454.2,218.5 460.8,217.8 467.3,219.8 473.8,221.1 480.4,221.7 486.9,222.6 493.5,222.4 500.0,225.5 506.5,225.2 513.1,225.0 519.6,225.4 526.1,228.0 532.7,227.3 539.2,228.2 545.8,229.2 552.3,229.0 558.9,231.8 565.4,231.8 571.9,234.9 578.5,236.7 585.0,239.7 591.5,238.6 598.1,239.3 604.6,239.8 611.2,241.3 617.7,241.8 624.2,243.2 630.8,242.1 637.3,243.2 643.9,241.8 650.4,245.1 657.0,245.4 663.5,245.0 670.0,246.5 676.6,247.5 683.1,248.4 689.6,248.6 696.2,248.5 702.7,249.8"/>
<polyline fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"
 points="58.6,46.4 61.9,66.6 65.2,80.3 68.5,90.3 71.8,98.1 75.1,106.2 78.4,116.1 81.7,121.2 85.0,125.2 88.3,131.0 91.6,138.8 94.9,141.9 98.2,142.7 101.5,144.8 104.8,148.1 108.2,153.2 111.5,152.8 114.8,154.7 118.1,156.9 121.4,160.6 124.7,161.5 128.0,160.0 131.3,161.9 134.6,167.0 137.9,166.7 141.2,171.6 144.5,172.3 147.8,171.6 151.1,173.7 154.4,174.1 157.7,175.1 161.0,177.7 164.3,176.1 167.6,174.6 170.9,179.2 174.2,177.7 177.5,178.1 180.8,178.9 184.1,179.5 187.4,179.6 190.7,185.8 194.0,180.7 197.3,183.6 200.6,188.8 203.9,185.6 207.2,188.1 210.5,187.0 213.8,187.0 217.2,187.4 220.5,186.0 223.8,191.2 227.1,188.7 230.4,188.0 233.7,197.9 237.0,190.3 240.3,192.5 243.6,195.6 246.9,191.3 250.2,193.6 253.5,190.0 256.8,192.3 260.1,193.2 263.4,191.7 266.7,198.4 270.0,197.2 273.3,199.1 276.6,198.0 279.9,193.4 283.2,198.7 286.5,196.2 289.8,194.1 293.1,199.1 296.4,200.1 299.7,197.3 303.0,198.8 306.3,198.3 309.6,199.5 312.9,199.4 316.2,199.5 319.5,197.9 322.8,199.3 326.2,202.5 329.5,196.6 332.8,198.8 336.1,203.9 339.4,196.0 342.7,202.0 346.0,201.7 349.3,201.2 352.6,198.4 355.9,202.6 359.2,202.8 362.5,202.3 365.8,205.7 369.1,203.3 372.4,203.0 375.7,203.1 379.0,202.6 382.3,205.1 385.6,202.9 388.9,202.4 392.2,207.6 395.5,210.1 398.8,207.4 402.1,206.8 405.4,204.0 408.7,204.3 412.0,203.3 415.3,207.0 418.6,204.9 421.9,211.3 425.2,209.9 428.5,211.2 431.8,207.8 435.2,206.8 438.5,206.3 441.8,205.9 445.1,211.9 448.4,212.5 451.7,211.0 455.0,210.8 458.3,210.1 461.6,210.4 464.9,211.0 468.2,212.5 471.5,212.1 474.8,211.6 478.1,216.4 481.4,209.1 484.7,214.6 488.0,220.4 491.3,214.9 494.6,211.5 497.9,221.4 501.2,215.5 504.5,219.2 507.8,215.0 511.1,220.0 514.4,216.1 517.7,216.6 521.0,218.3 524.3,216.1 527.6,218.5 530.9,215.5 534.2,218.8 537.5,222.1 540.8,216.4 544.2,220.2 547.5,222.6 550.8,218.1 554.1,219.7 557.4,225.5 560.7,225.1 564.0,224.4 567.3,223.8 570.6,223.9 573.9,225.4 577.2,224.4 580.5,225.8 583.8,228.1 587.1,228.8 590.4,228.9 593.7,228.8 597.0,230.0 600.3,228.4 603.6,231.3 606.9,228.0 610.2,229.1 613.5,232.3 616.8,230.4 620.1,233.0 623.4,230.5 626.7,235.7 630.0,231.8 633.3,233.7 636.6,233.7 639.9,233.9 643.2,228.9 646.5,233.6 649.8,233.4 653.2,236.1 656.5,233.9 659.8,237.5 663.1,235.5 666.4,231.6 669.7,232.1 673.0,234.2 676.3,236.7 679.6,236.9 682.9,236.0 686.2,236.7 689.5,233.4 692.8,237.8 696.1,236.7 699.4,237.2 702.7,237.7 706.0,242.8"/>
<circle cx="706" cy="242.8" r="3.5" fill="var(--accent)"/>
<text class="c-lab" x="698" y="233" text-anchor="end" fill="var(--accent)">3.10</text>
<text class="c-lab" x="196" y="176" fill="var(--accent)">validation</text>
<text class="c-lab" x="300" y="222" fill="var(--ink-soft)">train</text>
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
