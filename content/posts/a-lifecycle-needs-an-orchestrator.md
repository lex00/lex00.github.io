---
title: "A lifecycle needs an orchestrator"
date: 2026-07-17
---

Terraform 1.14 shipped Actions, its biggest language change in years. An Action fires a provider operation, a Lambda invoke or a cache invalidation, on a resource's create, update, or destroy. The imperative work that used to hide in `null_resource` finally has a place to sit.

Then you ask what runs it, and the answer is nothing. No typed input, no retry, no timeout, no gate, no record it ran. An Action is a trigger with no executor, and every one of those gaps is that same missing piece.

{{< inline-svg src="lifecycle-executor-matrix.svg" alt="A capability matrix comparing Terraform Actions and chant Ops. They tie on attaching to the lifecycle; on typed input, any operation, retry, timeout, human gate, durable record, and policy gate, Actions is empty and chant is full." >}}

Read the diagram by its empty column. They tie on the easy row. Everything under it is the executor Actions neglect.

[chant](https://intentius.io/chant/) makes a day-two step typed TypeScript that runs on Temporal, so retries, timeouts, human gates, and a durable record come with the step, not a flag. Go take a closer look.

Bring your own lifecycle. Just bring one that can finish the job.

## Read more

- [Ops](https://intentius.io/chant/guide/ops/) — day-two work as a typed step
- [Local vs Temporal](https://intentius.io/chant/guide/local-vs-temporal/) — the executor, and what it costs
