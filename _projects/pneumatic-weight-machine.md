---
title: Pneumatic Weight Machine
order: 3
lede: >-
  A portable home gym with constant concentric and eccentric loading up to 150 kg,
  using pneumatic actuators and closed-loop cable tension control.
description: >-
  Three generations of a compact pneumatic home gym with constant-force cable
  loading and a digital force readout.
meta: ["Three versions", "150 kg", "Closed-loop tension control"]
---

The majority of smart home gym systems, like Tonal, are resistance based- they can apply huge loads when you pull away from the device, but are much weaker on the return path. This is very different from what you feel when you lift physical weights, which weigh the same whether you are lifting them or putting them back down.

During COVID, I wanted a home gym system that felt more like a real gym. I chose pneumatics since it lets you pressurize the system over a long period of time- which greatly reduces the power requirement during operation.

As you pull a cable the piston travels and its pressure rises. This meanss the load the user
feels climbs through the rep. Each version of this machine is a slightly different way to address this fundamental problem.s

<figure class="full">
<video controls preload="metadata"><source src="{{ '/assets/YC_LIFTS.mp4' | relative_url }}" type="video/mp4"></video>
<figcaption>V3 in use.</figcaption>
</figure>

<figure class="full">
<video controls preload="metadata"><source src="{{ '/assets/SET_WEIGHT.mp4' | relative_url }}" type="video/mp4"></video>
<figcaption>Setting the force, with a seven-segment digital readout.</figcaption>
</figure>

## Three attempts at constant force

**V1** — a large air tank. Make the reservoir big enough relative to the swept
volume and the pressure rise over a stroke becomes small. It works, buts it is
bulky.

<figure class="full">
<img src="{{ '/assets/V1.png' | relative_url }}" alt="Version 1 of the pneumatic weight machine" loading="lazy">
</figure>

**V2** — a mechanical fix instead. A pulley with a changing radius winds the
cable, so as the pressure rises the moment arm shrinks and the cable tension stays
flat. Proof of concept, but not so polished.

<figure class="full">
<img src="{{ '/assets/V2_Machine.png' | relative_url }}" alt="Version 2, using a variable-radius sprocket" loading="lazy">
</figure>

**V3** — closed-loop control  built with the V2 architecture. The most compact, portable, polished version- with a digital force readout.

<figure class="full">
<img src="{{ '/assets/Gym.png' | relative_url }}" alt="Version 3 of the pneumatic weight machine" loading="lazy">
</figure>
