---
title: "chant dropped Temporal for fountain"
date: 2026-09-17
featured_image: "img/same-ball.svg"
draft: false
---

[chant](https://intentius.io/chant/) is a TypeScript toolchain for infrastructure. You declare resources as typed source. chant compiles them to the platform's own spec. It also runs ops such as applies that wait for a human.

Until this month the durable half of chant ops ran on Temporal. It now runs on [fountain](https://github.com/managoat/fountain) and the Temporal lexicon is deleted.

## What chant used Temporal for

Each item is about an apply surviving something.

- A gated apply waited for a human.
- Ops ran on a clock, like a drift watch.
- A crashed apply picked up where it stopped.
- Finished runs stayed searchable.

## How the waiting gets billed

Temporal Cloud bills storage by the hour while a workflow is open at forty times the closed rate. A gated apply stays open until someone releases it, so a workload full of them pays for every hour of human latency.

The alternative is self-hosting, which chant's own tutorial did.

## Durability with fountain

fountain runs coding agents on sandboxed machines. Its meter runs only while an agent works. [chant's steward](https://intentius.io/chant/tutorials/fountain-steward/) is one such agent on a persistent sandbox.

- A gated apply holds nothing open. While the human decides, the sandbox goes idle and parks.
- A scheduled op becomes a schedule on the steward.
- Crash recovery is a re-run, because chant's ops are safe to rerun.
- Run history is the steward's thread, logging what was changed in the environment.

## Temporal is powerful, and you may not need it

Temporal resumes an arbitrary program exactly where it stopped, across services it does not control.

chant's problem is smaller. It needs a decision to outlive a process and a machine that stays put. Neither of those requires replaying a program. Yours may be smaller too.

---

## Read more

- [Ops as teammates](https://intentius.io/chant/concepts/durable-workflows/)
- [The Steward](https://intentius.io/chant/lexicons/fountain/steward/)
- [fountain](https://github.com/managoat/fountain)
