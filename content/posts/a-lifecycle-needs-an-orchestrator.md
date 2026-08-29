---
title: "A lifecycle needs an orchestrator"
date: 2026-07-17
---

Terraform 1.14 shipped Actions, its biggest language change in years. An Action fires a provider operation when a resource gets created or updated or destroyed. That operation could be a Lambda invoke or a cache invalidation. The run-this-now work that used to hide in `null_resource` finally has a place to sit.

Then you ask what runs it, and the answer is nothing. No typed input, no retry, no timeout, no gate, no record it ran. An Action is a trigger with no executor, and every one of those gaps is that same missing piece.

{{< inline-svg src="lifecycle-executor-matrix.svg" alt="A capability matrix comparing Terraform Actions and chant Ops. They tie on attaching to the lifecycle. Every other row is an executor feature like typed input and retries and human gates. Actions is empty on all of them and chant is full." >}}

Read the diagram by its empty column. They tie on the easy row. Everything under it is the executor Actions neglect.

[chant](https://intentius.io/chant/) makes a day-two step typed TypeScript that runs on Temporal. Retries and timeouts come with the step rather than a flag. So do human gates and the durable record. Go take a closer look.

Bring your own lifecycle. Just bring one that can finish the job.

## Read more

- [Ops](https://intentius.io/chant/guide/ops/) covers day-two work as a typed step
- [Local vs Temporal](https://intentius.io/chant/guide/local-vs-temporal/) covers the executor and what it costs
