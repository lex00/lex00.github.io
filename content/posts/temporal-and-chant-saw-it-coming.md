---
title: "Temporal and chant saw it coming"
date: 2026-07-22
draft: false
featured_image: "img/temporal-and-chant-cover.svg"
---

A common line drawn about AI and infrastructure: "It changes how things get written, not how they get operated." It casts the near term as a moment when AI reshapes authoring while operations waits without an answer.

This tends to come from people observing the shift rather than shipping on it, and it already reads as dated. It also has the timing backwards, treating writing and operating as a sequence when they are moving together. Temporal and chant are already built for it.

## Operating is mostly execution

The real line is between execution and judgment. Judgment is the call that a change is allowed and that now is a safe time to make it. Everything on the execution side of that call is what agents are already good at, and operating lives mostly on the execution side, because most of it is applying changes and recovering from failures.

Ops looked safe for one reason, that running it took a reliability layer agents did not have.

## What Temporal already built

Temporal built this years before the word agentic attached to it. Durable execution grew out of the Cadence project at Uber, meant for long business workflows, and it happens to be the exact shape an autonomous agent needs before you let it near production. 

The funding caught up to what the engineering already was. In February 2026 Temporal [raised $300M at a $5B valuation](https://temporal.io/news/temporal-raises-300M-to-make-agentic-ai-real-for-companies), led by Andreessen Horowitz, on an openly agentic pitch, revenue up more than 380% on the year. The OpenAI Agents SDK integration reached GA in March 2026, running each agent step as a durable activity. The layer under it had been carrying Snap, Netflix, and Datadog in production for years, while the rest of the conversation stayed on whether agents can write YAML.

## The "not ready" hedge

The fallback view is that agentic ops is coming but not here yet. Remember when this was being said about AI writing production code a few months before it did? The capability shipped. What is still early is how many teams have adopted it, which is a different claim from whether it works. 

Saying agentic ops is "not ready" means predicting that a curve which already bent once, for authoring, stays flat for operating, while both get built in the same window with the same money.

Agents are not running most production estates today, and the visible proof is still a short list. The tooling works and teams are wiring it up now.

## chant made the same call

chant lines up with Temporal because it made the same architectural call. It keeps synthesis and execution apart. The synthesis side compiles your TypeScript down to the cloud's own spec. On the execution side chant runs the lifecycle and makes it durable, with [Temporal as a supported backend](https://intentius.io/chant/lexicons/temporal/) and worked tutorials that deploy on it, [Fly](https://intentius.io/chant/tutorials/fly-durable-deploy/) and [Temporal with CockroachDB](https://intentius.io/chant/tutorials/temporal-crdb-deploy/).

Temporal and chant fit together closely. When an agent proposes a change, the lint and the diff answer for it, a human approves at the gate, and the apply runs as a durable workflow that survives a crash and resumes where it left off. 

{{< inline-svg src="agentic-ops-loop.svg" alt="A left-to-right loop of four boxes. Agent proposes a change, chant runs lint and diff so it is checkable first, a human approves at the gate, and Temporal applies it as a durable workflow that resumes on crash. A dashed return arrow observes the live system back to the agent. A note reads: the gate is judgment, everything else is execution, and execution is what agents do." >}}

chant + Temporal is agentic infrastructure ops, working today, on the layer the market just funded at five billion dollars. chant was standing there before the demand showed up.

## The same wave

Writing and operating are the same wave. Writing is the visible part, since you can watch an agent produce a file. Operating changes underneath, in funding rounds and durable-execution SDKs that look like plumbing, so it is easy to miss. 

The teams that end up looking early are the ones already on that layer, Temporal below and chant above. Anyone still drawing the line at "AI writes, humans operate" is standing on ground that is already moving, right next to the ground they can see. What stays with the human is judgment, the call that a change is allowed, which was always the smaller part of the job.

---

## Read more

- [The long road back to cloud native](https://lex00.github.io/posts/the-long-road-back-to-native/)
- [Governance is what IaC depends on](https://lex00.github.io/posts/governance-is-load-bearing/)
- [chant durable workflows](https://intentius.io/chant/concepts/durable-workflows/)
- [chant](https://intentius.io/chant/)
