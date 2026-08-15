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
