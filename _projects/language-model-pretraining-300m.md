---
title: "Training a Bigger Small Model"
order: 2
lede: >-
  After the 154M parameter RTX 3050 run, it was quite clear that my model was not very capable.
  One simple follow up to my previous training run was to increase the size- both in terms of data and parameters.
  After some planning, I rented an H100, trained a 293M-parameter model on the same dataset,
  and did indeed get a stronger base model.
description: >-
  Scaling my home-trained 154M language model to a 293M model on a rented H100.
meta: ["293.2M params", "2.95B tokens", "29.4 h", "H100 80 GB"]
---

## What I built

After training the 154M model on my RTX 3050, the next question was pretty
obvious: did the model feel weak because it was too few parameters, or because my recipe was bad?

I kept the content of the dataset the same, although did repeat it over multiple epochs, and increased the parameter count to 293M.
The model did improve on various benchmarks, but still 'feels' quite dumb- even compared to SmolLM2-135M.

I used the same tokenizer, same
`mix16` corpus, same general architecture. The difference was mostly
parameters and hardware. I moved the run to a rented H100, bumped the model to
293M parameters, and used a much larger batch/sequence setup: 64 &times; 1024 tokens
for 45,000 steps.

That works out to **2.95B tokens processed**, or about **7.3 epochs over the
405M-token corpus**. So this was not a clean Chinchilla-style data scale-up. It
was more like asking: if I keep my data fixed and rent real hardware, does the
same training recipe get meaningfully better?


<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 720 300" role="img" aria-label="Validation loss over the 293M H100 run, falling from 3.72 at step 2,000 to 2.762 at step 44,999">
<line class="c-grid" x1="58" y1="18" x2="706" y2="18"/>
<line class="c-grid" x1="58" y1="83.5" x2="706" y2="83.5"/>
<line class="c-grid" x1="58" y1="149.1" x2="706" y2="149.1"/>
<line class="c-grid" x1="58" y1="214.5" x2="706" y2="214.5"/>
<line class="c-grid" x1="58" y1="258" x2="706" y2="258"/>
<text class="c-tick" x="48" y="21.5" text-anchor="end">3.8</text>
<text class="c-tick" x="48" y="87" text-anchor="end">3.5</text>
<text class="c-tick" x="48" y="152.6" text-anchor="end">3.2</text>
<text class="c-tick" x="48" y="218" text-anchor="end">2.9</text>
<text class="c-tick" x="48" y="261.5" text-anchor="end">2.7</text>
<polyline fill="none" stroke="var(--accent)" stroke-width="2.2" stroke-linejoin="round"
 points="86.8,36.2 115.6,100.3 144.4,136.3 173.2,153.9 202.0,163.2 230.8,175.6 259.6,180.1 288.4,188.0 317.2,194.4 346.0,196.4 374.8,202.1 403.6,201.9 432.4,211.2 461.2,213.6 490.0,220.7 518.8,223.3 547.6,225.3 576.4,229.8 605.2,236.9 634.0,240.8 662.8,242.1 691.6,248.0 706.0,244.5"/>
<circle cx="706" cy="244.5" r="3.8" fill="var(--accent)"/>
<text class="c-lab" x="696" y="235" text-anchor="end" fill="var(--accent)">2.762</text>
<line class="c-axis" x1="58" y1="268" x2="706" y2="268"/>
<line class="c-axis" x1="58" y1="18" x2="58" y2="268"/>
<text class="c-tick" x="58" y="282" text-anchor="middle">0</text>
<text class="c-tick" x="202" y="282" text-anchor="middle">10k</text>
<text class="c-tick" x="346" y="282" text-anchor="middle">20k</text>
<text class="c-tick" x="490" y="282" text-anchor="middle">30k</text>
<text class="c-tick" x="634" y="282" text-anchor="middle">40k</text>
<text class="c-tick" x="379" y="297" text-anchor="middle">training step</text>
</svg>
</div>
<figcaption>The first step is clipped off because the untrained model's loss was
36.17 and would flatten the useful part of the chart. By step 2,000 it was
already at 3.72; the final validation loss was 2.762. The run stoped and resumed once, so
the combined wall time was about 29.4 hours.</figcaption>
</figure>

The speed difference was huge. My 154M run processed about 4,841 tokens/sec
on the RTX 3050. The H100 run settled around 58k tokens/sec near the end, with
about 38% MFU and 25 GB of VRAM used. My previous experiment could have been done in an afternoon.

## Result

Measured locally with the same latest-LightEval cloze-format scorer for the
models that matter for this page: my 154M starting point, my 293M follow-up, and
SmolLM2-360M as the nearby public reference.

<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 820 500" role="img" aria-label="Cloze benchmark bars comparing the 154M model, the 293M model, and SmolLM2-360M">
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
<rect x="141.0" y="105.7" width="16" height="260.3" fill="var(--accent)"/>
<text class="c-lab" x="149.0" y="100.7" text-anchor="middle">65.1</text>
<rect x="169.0" y="80.0" width="16" height="286.0" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="177.0" y="75.0" text-anchor="middle">71.5</text>
<text class="c-tick" x="142.0" y="392" text-anchor="middle">PIQA</text>
<rect x="219.0" y="255.7" width="16" height="110.3" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="227.0" y="250.7" text-anchor="middle">27.6</text>
<rect x="247.0" y="235.6" width="16" height="130.4" fill="var(--accent)"/>
<text class="c-lab" x="255.0" y="230.6" text-anchor="middle">32.6</text>
<rect x="275.0" y="152.3" width="16" height="213.7" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="283.0" y="147.3" text-anchor="middle">53.4</text>
<text class="c-tick" x="248.0" y="392" text-anchor="middle">HellaSwag</text>
<rect x="325.0" y="246.3" width="16" height="119.7" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="333.0" y="241.3" text-anchor="middle">29.9</text>
<rect x="353.0" y="230.9" width="16" height="135.1" fill="var(--accent)"/>
<text class="c-lab" x="361.0" y="225.9" text-anchor="middle">33.8</text>
<rect x="381.0" y="157.0" width="16" height="209.0" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="389.0" y="152.0" text-anchor="middle">52.3</text>
<text class="c-tick" x="354.0" y="392" text-anchor="middle">ARC avg.</text>
<rect x="431.0" y="269.7" width="16" height="96.3" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="439.0" y="264.7" text-anchor="middle">24.1</text>
<rect x="459.0" y="258.6" width="16" height="107.4" fill="var(--accent)"/>
<text class="c-lab" x="467.0" y="253.6" text-anchor="middle">26.9</text>
<rect x="487.0" y="201.9" width="16" height="164.1" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="495.0" y="196.9" text-anchor="middle">41.0</text>
<text class="c-tick" x="460.0" y="392" text-anchor="middle">CSQA</text>
<rect x="537.0" y="162.0" width="16" height="204.0" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="545.0" y="157.0" text-anchor="middle">51.0</text>
<rect x="565.0" y="157.0" width="16" height="209.0" fill="var(--accent)"/>
<text class="c-lab" x="573.0" y="152.0" text-anchor="middle">52.2</text>
<rect x="593.0" y="147.8" width="16" height="218.2" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="601.0" y="142.8" text-anchor="middle">54.5</text>
<text class="c-tick" x="566.0" y="392" text-anchor="middle">Winogrande</text>
<rect x="643.0" y="250.0" width="16" height="116.0" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-lab" x="651.0" y="245.0" text-anchor="middle">29.0</text>
<rect x="671.0" y="252.4" width="16" height="113.6" fill="var(--accent)"/>
<text class="c-lab" x="679.0" y="247.4" text-anchor="middle">28.4</text>
<rect x="699.0" y="223.6" width="16" height="142.4" fill="#8a4f2a" opacity="0.9"/>
<text class="c-lab" x="707.0" y="218.6" text-anchor="middle">35.6</text>
<text class="c-tick" x="672.0" y="392" text-anchor="middle">OpenBookQA</text>
<line class="c-axis" x1="78" y1="366" x2="790" y2="366"/>
<line class="c-axis" x1="78" y1="36" x2="78" y2="366"/>
<rect x="105" y="410" width="12" height="12" fill="var(--ink-soft)" opacity="0.55"/>
<text class="c-tick" x="123" y="420">154M</text>
<rect x="235" y="410" width="12" height="12" fill="var(--accent)"/>
<text class="c-tick" x="253" y="420">293M</text>
<rect x="405" y="410" width="12" height="12" fill="#8a4f2a" opacity="0.9"/>
<text class="c-tick" x="423" y="420">SmolLM2-360M</text>
</svg>
</div>
<figcaption>All bars are latest-LightEval cloze-format runs, plotted as
length-normalized multiple-choice accuracy. </figcaption>
</figure>

<div class="tbl">
<table>
<thead><tr><th>benchmark</th><th class="n">154M</th><th class="n">293M</th><th class="n">SmolLM2-360M</th><th class="n">293M vs 154M</th></tr></thead>
<tbody>
<tr><td>PIQA (1,838)</td><td class="n">61.04</td><td class="n good">65.07</td><td class="n good">71.49</td><td class="n good">+4.03</td></tr>
<tr><td>HellaSwag (10,042)</td><td class="n">27.57</td><td class="n good">32.59</td><td class="n good">53.43</td><td class="n good">+5.02</td></tr>
<tr><td>ARC avg.</td><td class="n">29.92</td><td class="n good">33.76</td><td class="n good">52.25</td><td class="n good">+3.85</td></tr>
<tr><td>CommonsenseQA (1,221)</td><td class="n">24.08</td><td class="n good">26.86</td><td class="n good">41.03</td><td class="n good">+2.78</td></tr>
<tr><td>Winogrande (1,267)</td><td class="n">50.99</td><td class="n good">52.25</td><td class="n good">54.54</td><td class="n good">+1.26</td></tr>
<tr><td>OpenBookQA (500)</td><td class="n">29.00</td><td class="n">28.40</td><td class="n good">35.60</td><td class="n bad">-0.60</td></tr>
</tbody>
</table>
</div>

This is a much cleaner result than the 154M run. Same data (more epochs), same tokenizer, more
parameters, and the model moves up across the benchmarks I care about.
SmolLM2-360M is the sobering nearby-size comparison: it is a serious public
model trained with much more data. The 360M version saw **4T tokens** across
**64 H100s** ([model card](https://huggingface.co/HuggingFaceTB/SmolLM2-360M)).

The post-training comparison has the same trend. SmolLM2 reports an instruction
suite; my 293M SFT run has a smaller chat-form eval, so the scores below are
just a rough sanity check.

<div class="tbl">
<table>
<thead><tr><th>instruction benchmark</th><th class="n">293M SFT</th><th class="n">SmolLM2-360M-Instruct</th></tr></thead>
<tbody>
<tr><td>IFEval</td><td class="n">15.0 prompt-strict</td><td class="n good">41.0 avg</td></tr>
<tr><td>HellaSwag</td><td class="n">28.2 MCF/chat</td><td class="n good">52.1</td></tr>
<tr><td>ARC-Easy / ARC avg.</td><td class="n">22.8 MCF/chat</td><td class="n good">43.7</td></tr>
<tr><td>PIQA</td><td class="n">50.0 MCF/chat</td><td class="n good">70.8</td></tr>
<tr><td>MMLU (cloze)</td><td class="n">20.0 MCF/chat</td><td class="n good">32.8</td></tr>
<tr><td>BBH (3-shot)</td><td class="n dim">not run</td><td class="n">27.3</td></tr>
<tr><td>GSM8K (5-shot)</td><td class="n">1.7 exact</td><td class="n good">7.43</td></tr>
</tbody>
</table>
</div>

The base model was still not "smart". It wrote
coherent text and stayed on topic better, but it still felt like an auto complete. The pleasant surprise was that
scaling parameters alone did move the benchmark needle. The unpleasant surprise
was that it did not magically produce a useful assistant.

## Fine-tuning it into a chatbot

I ran supervised fine-tuning on 107,816 instruction examples. This was the
same idea as the 154M page: teach the model the chat format, score only assistant
tokens with a loss mask, and see whether the pretraining knowledge becomes more
usable.

The format definitely clicked. The model answered in the right place, stopped
more often, and sometimes gave something that looked like an answer.

<figure class="full">
<div class="chartbox">
<svg viewBox="0 0 760 330" role="img" aria-label="Instruction evaluation bars for the fine-tuned 293M model compared with chance levels">
<line class="c-grid" x1="78" y1="38" x2="730" y2="38"/>
<line class="c-grid" x1="78" y1="82" x2="730" y2="82"/>
<line class="c-grid" x1="78" y1="126" x2="730" y2="126"/>
<line class="c-grid" x1="78" y1="170" x2="730" y2="170"/>
<line class="c-grid" x1="78" y1="214" x2="730" y2="214"/>
<line class="c-grid" x1="78" y1="258" x2="730" y2="258"/>
<text class="c-tick" x="66" y="262" text-anchor="end">0</text>
<text class="c-tick" x="66" y="218" text-anchor="end">10</text>
<text class="c-tick" x="66" y="174" text-anchor="end">20</text>
<text class="c-tick" x="66" y="130" text-anchor="end">30</text>
<text class="c-tick" x="66" y="86" text-anchor="end">40</text>
<text class="c-tick" x="66" y="42" text-anchor="end">50</text>
<rect x="105" y="38" width="46" height="220" fill="var(--accent)"/>
<line x1="98" y1="38" x2="158" y2="38" stroke="var(--mark)" stroke-width="2"/>
<text class="c-lab" x="128" y="31" text-anchor="middle" fill="var(--accent)">50.0</text>
<text class="c-tick" x="128" y="282" text-anchor="middle">PIQA</text>
<rect x="212" y="157.7" width="46" height="100.3" fill="var(--accent)"/>
<line x1="205" y1="148" x2="265" y2="148" stroke="var(--mark)" stroke-width="2"/>
<text class="c-lab" x="235" y="151" text-anchor="middle" fill="var(--accent)">22.8</text>
<text class="c-tick" x="235" y="282" text-anchor="middle">ARC</text>
<rect x="319" y="133.9" width="46" height="124.1" fill="var(--accent)"/>
<line x1="312" y1="148" x2="372" y2="148" stroke="var(--mark)" stroke-width="2"/>
<text class="c-lab" x="342" y="127" text-anchor="middle" fill="var(--accent)">28.2</text>
<text class="c-tick" x="342" y="282" text-anchor="middle">Hella</text>
<rect x="426" y="170" width="46" height="88" fill="var(--accent)"/>
<line x1="419" y1="148" x2="479" y2="148" stroke="var(--mark)" stroke-width="2"/>
<text class="c-lab" x="449" y="164" text-anchor="middle" fill="var(--accent)">20.0</text>
<text class="c-tick" x="449" y="282" text-anchor="middle">MMLU</text>
<rect x="533" y="128.2" width="46" height="129.8" fill="var(--accent)"/>
<line x1="526" y1="170" x2="586" y2="170" stroke="var(--mark)" stroke-width="2"/>
<text class="c-lab" x="556" y="122" text-anchor="middle" fill="var(--accent)">29.5</text>
<text class="c-tick" x="556" y="282" text-anchor="middle">TruthfulQA</text>
<rect x="640" y="192" width="46" height="66" fill="var(--accent)"/>
<text class="c-lab" x="663" y="186" text-anchor="middle" fill="var(--accent)">15.0</text>
<text class="c-tick" x="663" y="282" text-anchor="middle">IFEval</text>
<line class="c-axis" x1="78" y1="258" x2="730" y2="258"/>
<line class="c-axis" x1="78" y1="38" x2="78" y2="258"/>
<rect x="240" y="308" width="12" height="12" fill="var(--accent)"/>
<text class="c-tick" x="258" y="318">293M SFT score</text>
<line x1="410" y1="314" x2="442" y2="314" stroke="var(--mark)" stroke-width="2"/>
<text class="c-tick" x="450" y="318">chance where defined</text>
</svg>
</div>
<figcaption>After SFT, the multiple-choice/chat-form benchmarks mostly hover
around chance. The two better benches were TruthfulQA MC1 at 29.5% on 400 examples
and IFEval prompt-strict at 15.0% on a 60-example subset.</figcaption>
</figure>

Some sample outputs from the second SFT run:

<div class="samples">
  <div class="s user"><div class="k">prompt</div><div class="v">What is the capital of France?</div></div>
  <div class="s"><div class="k">293M SFT</div><div class="v">The capital of France is Paris</div></div>
  <div class="s user"><div class="k">prompt</div><div class="v">What is 17 plus 25?</div></div>
  <div class="s"><div class="k">293M SFT</div><div class="v">17 plus 25 is the number of people who are blind in one eye. It is the number of people who are blind in one eye.</div></div>
  <div class="s user"><div class="k">prompt</div><div class="v">Why is the sky blue?</div></div>
  <div class="s"><div class="k">293M SFT</div><div class="v">The sky is blue because the wavelengths of light are bent by the atmosphere.</div></div>
</div>

A little more coherent, but far from useful. 

## Some learnings

The biggest lesson is that **parameter count helped more reliably than my clever
ideas**. Earlier in the project I tried data filtering, synthetic reasoning data,
abacus embeddings, and a bunch of training-loop tweaks. Some were useful
engineering, but the clear benchmark jump came from making the dense model
bigger and training it on better hardware.

The second lesson is that hardware changes what experiments are emotionally
available. On the 3050, a bad choice costs days and made me reluctant to touch
anything. On the H100, I could actually run, evaluate, inspect, restart, and
still have a weekend left.

The third lesson is that SFT can make a tiny model behave like a chatbot without
making it know very much. It learned how to answer questions, but did not learn arithmetic,
and did not stop hallucinating. 

## Takeaways

- Scaling from 154M to 293M on the same data clearly improved base-model benchmarks.
- The 293M model reached 2.762 validation loss versus 3.10 for the 154M run.
- The H100 run was about 12x faster in tokens/sec than my RTX 3050 run, even while training a much larger model.
- Reusing the same 405M-token corpus for 2.95B processed tokens probably overtrained the data side; next I should plan to scale the dataset.
- SFT made the model answer in chat format, but that was it
- Simple dense scaling beat most of the fancy scaffolding I tried
