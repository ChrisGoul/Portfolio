---
title: "Training a 154M Dense LLM on my RTX 3050"
order: 1
lede: >-
  
  I wanted to see how useful of an LLM I could train myself. After some architecture optimization, I fit a 154M-parameter model on my consumer GPU, and trained it for 46 hours. It lands near GPT-2 on several pretraining benchmarks.
  
  
description: >-
  Training a 154M language model from scratch on a single RTX 3050 and
  benchmarking it properly against GPT-2-small.
meta: ["153.8M params", "0.81B tokens", "46.5 h", "RTX 3050 8 GB"]
---

## What I built

The motivation for this project was simple, I wanted to see how useful of an LLM I could train myself. More specifically though, I was curious to understand:

  - What does it take, in terms of data, infrastructure, time, and money, to train an LLM?
  - At what scale do these models start to feel 'intelligent'?

I started small- my PC has a RTX 3050 GPU, with a measly 8GB of memory. The [SmolLM training playbook](https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook#training-compass-why--what--how) was a great reference for training small models that I heavily borrowed ideas from.

For a first pass I wanted to do a short training run. I settled on a 150M model since I could just barely fit it on my GPU with gradient checkpointing. I used Muon, RoPE, tied embedding weights, and a 16K-token vocabulary. I wanted to keep vocab as small as possible, since at these model sizes it takes up a larger portion of the total parameters- 16k = 12M parameters. That may have been an incorrect choice, since my already undertrained model (only 0.8B tokens) effectively sees even fewer, since the corpus grows.

My model trained for 99,000 steps on 0.81B tokens of FineWeb-Edu, Cosmopedia and synthetic
chain-of-thought. Final validation loss was 3.10- because I chose to end my run early, I only got to around ~5 tokens/parameter,
so not very [optimal](https://arxiv.org/abs/2001.08361) per the scaling laws paper. Then a quick
supervised fine-tune on 107k instruction examples. 

One interesting note is that competitive small models lately (Llama, Qwen, SmolLM2) train on vastly more tokens/parameter. SmolLM2-125M actually goes to a staggering 2T tokens on their 135M parameter model- over 2000x the amount of data I fed mine. It makes sense to pour resources into training small models- they are cheap to train, and cheap to run during inference. But for my setup such scales were simply not practical.

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
<figcaption>Loss on a log axis across all 46.5 hours. A little spiky, but validation loss on the holdout set tracks training the whole way.</figcaption>
</figure>

## Results

For base models, the fairest comparison is cloze-style likelihood. You score each
candidate continuation, normalize by length, and pick the most
likely answer. I used HuggingFace's LightEval to evaluate my 154M checkpoint, GPT-2-small, and SmolLM2-135M with
their latest cloze-format setup. I chose to rerun all of these models' benchmarks to ensure the comparison is accurate, as opposed to relying on published numbers.

<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 820 500" role="img" aria-label="Cloze benchmark bars comparing the 154M model, GPT-2-small, and SmolLM2-135M">
<line class="c-grid" x1="78" y1="366.0" x2="790" y2="366.0"/>
<text class="c-tick" x="66" y="370.0" text-anchor="end">0</text>
<line class="c-grid" x1="78" y1="306.0" x2="790" y2="306.0"/>
<text class="c-tick" x="66" y="310.0" text-anchor="end">15</text>
<line class="c-grid" x1="78" y1="246.0" x2="790" y2="246.0"/>
<text class="c-tick" x="66" y="250.0" text-anchor="end">30</text>
<line class="c-grid" x1="78" y1="186.0" x2="790" y2="186.0"/>
<text class="c-tick" x="66" y="190.0" text-anchor="end">45</text>
<line class="c-grid" x1="78" y1="126.0" x2="790" y2="126.0"/>
<text class="c-tick" x="66" y="130.0" text-anchor="end">60</text>
<line class="c-grid" x1="78" y1="66.0" x2="790" y2="66.0"/>
<text class="c-tick" x="66" y="70.0" text-anchor="end">75</text>
<rect x="113.0" y="121.8" width="16" height="244.2" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="121.0" y="116.8" text-anchor="middle">61.0</text>
<rect x="141.0" y="116.2" width="16" height="249.8" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="149.0" y="111.2" text-anchor="middle">62.5</text>
<rect x="169.0" y="94.8" width="16" height="271.2" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="177.0" y="89.8" text-anchor="middle">67.8</text>
<text class="c-tick" x="142.0" y="392" text-anchor="middle">PIQA</text>
<rect x="219.0" y="255.7" width="16" height="110.3" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="227.0" y="250.7" text-anchor="middle">27.6</text>
<rect x="247.0" y="247.7" width="16" height="118.3" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="255.0" y="242.7" text-anchor="middle">29.6</text>
<rect x="275.0" y="201.2" width="16" height="164.8" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="283.0" y="196.2" text-anchor="middle">41.2</text>
<text class="c-tick" x="248.0" y="392" text-anchor="middle">HellaSwag</text>
<rect x="325.0" y="246.3" width="16" height="119.7" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="333.0" y="241.3" text-anchor="middle">29.9</text>
<rect x="353.0" y="244.4" width="16" height="121.6" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="361.0" y="239.4" text-anchor="middle">30.4</text>
<rect x="381.0" y="186.3" width="16" height="179.7" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="389.0" y="181.3" text-anchor="middle">44.9</text>
<text class="c-tick" x="354.0" y="392" text-anchor="middle">ARC avg.</text>
<rect x="431.0" y="269.7" width="16" height="96.3" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="439.0" y="264.7" text-anchor="middle">24.1</text>
<rect x="459.0" y="249.4" width="16" height="116.6" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="467.0" y="244.4" text-anchor="middle">29.2</text>
<rect x="487.0" y="227.4" width="16" height="138.6" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="495.0" y="222.4" text-anchor="middle">34.6</text>
<text class="c-tick" x="460.0" y="392" text-anchor="middle">CSQA</text>
<rect x="537.0" y="162.0" width="16" height="204.0" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="545.0" y="157.0" text-anchor="middle">51.0</text>
<rect x="565.0" y="163.3" width="16" height="202.7" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="573.0" y="158.3" text-anchor="middle">50.7</text>
<rect x="593.0" y="155.7" width="16" height="210.3" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="601.0" y="150.7" text-anchor="middle">52.6</text>
<text class="c-tick" x="566.0" y="392" text-anchor="middle">Winogrande</text>
<rect x="643.0" y="250.0" width="16" height="116.0" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="651.0" y="245.0" text-anchor="middle">29.0</text>
<rect x="671.0" y="258.8" width="16" height="107.2" fill="var(--mark)" opacity="0.75"/>
<text class="c-lab" x="679.0" y="253.8" text-anchor="middle">26.8</text>
<rect x="699.0" y="238.8" width="16" height="127.2" fill="#2f7d5c" opacity="0.9"/>
<text class="c-lab" x="707.0" y="233.8" text-anchor="middle">31.8</text>
<text class="c-tick" x="672.0" y="392" text-anchor="middle">OpenBookQA</text>
<line class="c-axis" x1="78" y1="366" x2="790" y2="366"/>
<line class="c-axis" x1="78" y1="36" x2="78" y2="366"/>
<rect x="105" y="410" width="12" height="12" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-tick" x="123" y="420">154M</text>
<rect x="275" y="410" width="12" height="12" fill="var(--mark)" opacity="0.75"/>
<text class="c-tick" x="293" y="420">GPT-2-small</text>
<rect x="475" y="410" width="12" height="12" fill="#2f7d5c" opacity="0.9"/>
<text class="c-tick" x="493" y="420">SmolLM2-135M</text>
</svg>
</div>
<figcaption>All bars are local latest-LightEval cloze-format evals, plotted as
length-normalized multiple-choice accuracy.</figcaption>
</figure>

<div class="tbl">
<table>
<thead><tr><th>benchmark</th><th class="n">154M</th><th class="n">GPT-2-small</th><th class="n">SmolLM2-135M</th></tr></thead>
<tbody>
<tr><td>PIQA (1,838)</td><td class="n">61.04</td><td class="n">62.46</td><td class="n good">67.79</td></tr>
<tr><td>HellaSwag (10,042)</td><td class="n">27.57</td><td class="n">29.58</td><td class="n good">41.21</td></tr>
<tr><td>ARC-Easy (2,376)</td><td class="n">36.20</td><td class="n">38.01</td><td class="n good">59.47</td></tr>
<tr><td>ARC-Challenge (1,172)</td><td class="n">23.63</td><td class="n">22.78</td><td class="n good">30.38</td></tr>
<tr><td>CommonsenseQA (1,221)</td><td class="n">24.08</td><td class="n">29.16</td><td class="n good">34.64</td></tr>
<tr><td>Winogrande (1,267)</td><td class="n">50.99</td><td class="n">50.67</td><td class="n good">52.57</td></tr>
<tr><td>OpenBookQA (500)</td><td class="n">29.00</td><td class="n">26.80</td><td class="n good">31.80</td></tr>
</tbody>
</table>
</div>

Across these benchmarks, my model is reasonably close to GPT 2-Small, but lags behind SmolLM2 135M. Since I followed a similar data mix and recipe to SmolLM2, excepting the amount of training data.  Perhaps these differences are attributable to my model seeing less data. I plan to investigate this in a further ablation.

## Some learnings

My live benchmark during pretraining were quite useless- they reported HellaSwag ~ 40, comfortably above GPT-2's published 31.1. It turns out this was mostly noise, since I had been: 

- Only testing 100 samples from HellaSwag to speed training, vs. the whole ~10k
- using **`items[:n]` ** and taking the first 100 samples. Since the head of HellaSwag's validation split is easier than the tail, I later confirmed that the same model scored **39.0** on the first 100,
  **35.0** on the first 2,000, and **27.6** on all 10,042 in the full test suite.

## What the model is actually like

Anecdotally, grammar was pretty coherent by ~step 20,000; after that, it seemed to get a little better at staying on topic. It never really learned facts, so perhaps 0.81B tokens is simply too few to be useful...  

Results after fine-tuning, when asked to add 17 and 25:

> 17 plus 25 is the number of base wins it is played on. So that means the number
> of base wins is 25/4 = `<<25/4=5>>`5 base wins.

For comparison, I asked GPT-2-small and SmolLM2-135M-Instruct the same question
with greedy decoding:

<div class="samples">
  <div class="s user"><div class="k">prompt</div><div class="v">What is 17 plus 25?</div></div>
  <div class="s"><div class="k">GPT-2-small</div><div class="v">17 plus 25 is the number of years that a person has been in the United States. 17 plus 25 is the number of years that a person has been in the United States. 17 plus 25 is the number of years that a person has been in the United States.</div></div>
  <div class="s"><div class="k">SmolLM2-135M-Instruct</div><div class="v">17 plus 25 is 42.</div></div>
</div>

My model reproduced GSM8K's answer syntax, but clearly failed to understand the
question and the math. GPT-2-small was fluent but just kept completing the
phrase. SmolLM2-135M-Instruct was more interesting: same rough
parameter count, but enough training and post-training to answer correctly.

I also tried a tiny relational reasoning prompt, and an easy
chat prompt. These are not benchmarks, just quick "what does it feel like?"
probes:

<div class="samples">
  <div class="s user"><div class="k">prompt</div><div class="v">Alice is older than Bob. Bob is older than Carla. Who is the youngest? Answer in one sentence.</div></div>
  <div class="s"><div class="k">154M SFT</div><div class="v">Alice is older than Carla. Bob was over the age of 80 and had a younger sibling with him, so he must have been in his late thirties!</div></div>
  <div class="s"><div class="k">GPT-2-small</div><div class="v">Answer in one sentence. Answer in one sentence. Answer in one sentence. Answer in one sentence. Answer in one sentence...</div></div>
  <div class="s"><div class="k">SmolLM2-135M-Instruct</div><div class="v">Alice is the youngest.</div></div>
</div>

<div class="samples">
  <div class="s user"><div class="k">prompt</div><div class="v">Tell me a joke.</div></div>
  <div class="s"><div class="k">154M SFT</div><div class="v">What happened?</div></div>
  <div class="s"><div class="k">GPT-2-small</div><div class="v">I'm not going to tell you a joke. I'm not going to tell you a joke. I'm not going to tell you a joke...</div></div>
  <div class="s"><div class="k">SmolLM2-135M-Instruct</div><div class="v">A: "What's the best joke ever?"</div></div>
</div>

General takeaway is that my model learned
chat formatting and a little local coherence, but fails even simple symbolic reasoning, math,
and is not useful as a chat model.

## Takeaways

- Don't take the first *n* rows of a benchmark. Shuffle, or use all of it.
- Make sure you have a sufficiently large sample for live benchmarks- so you aren't just tracking noise
- Score your baseline/other open models with the same harness- harness-to-harness differences made it tough to compare back to published numbers
- My model felt quite weak, especially for it's weight class. May experiment in the future with longer training runs to show the model more data
