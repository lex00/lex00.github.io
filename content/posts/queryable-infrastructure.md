---
title: "Queryable Infrastructure"
date: 2026-07-28
featured_image: "img/queryable-infrastructure-cover.svg"
---

Agentic ops means agents need to query your infra on demand. If the live details of your estate are fragmented this can lead to extra lookups costing time and tokens.

I measured this on [aws-bench](/posts/aws-bench-scenario-1-wrap/): asked which security groups were attached to nothing, every toolchain that reads a stored copy of the estate scored 0 out of 3.

Many things can be queried like a database without being one. The live cloud is one of them.

Typed source is another. chant tooling reads [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) through the syntax tree, so an agent queries your infra code instead of grepping it.

The fragmentation of truth between the live system and a stored copy is far more serious than IaC spread across repos.

When many repos deploy changes they converge in the live system which is already authoritative and already queryable. The repo layout never enters into it.

Agents benefit from queryable infrastructure, and the spec [covers most of it](/posts/the-long-tail-is-a-tail/).

---

## Read more

- [aws-bench: scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/)
- [Scenario 1 results on chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/)
- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
- [Honor the lower layer](/posts/honor-the-lower-layer/)
- [The long tail is a tail](/posts/the-long-tail-is-a-tail/)
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/)
- [chant](https://intentius.io/chant/)
