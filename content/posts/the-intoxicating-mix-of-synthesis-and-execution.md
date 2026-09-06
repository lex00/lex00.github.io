---
title: "The intoxicating mix of synthesis and execution"
date: 2026-09-06
draft: false
featured_image: "img/intoxicating-mix-cover.svg"
---

When software engineers build infra toolchains they always mix synthesis with execution. It's hard to resist when you carry a bag of golden hammers in the form of a full featured language.

Look closely and you'll see that what these toolchains are celebrated for is managing a mess they made by fusing synthesis with execution.

## How the experts price this problem

The industry is focused on the cost of splitting synthesis from execution. This cost is framed as the latency of downstream edits being reconciled, and patches piling up outside a generator.

When you consider that this is the particular cost being focused on, it makes sense that these architects reach for a fusion model.

## The boring way to price the problem

When I have to respond to an infra alarm, I assure you I do not care how interesting the effect model responsible may be.

I care what was approved, I care what ran, and I care about resolving the problem.

When it comes to reviewing what was approved, a platform native artifact is much easier to look at than error logs.

## TypeScript as Data

[TypeScript as Data](https://intentius.io/chant/concepts/typescript-as-data/) is what happens when you put a particular set of constraints on TypeScript to avoid dynamic output.

On top of that, splitting synthesis from execution means:
- linting rejects lookups at synth
- network calls are rejected at synth
- a socket-layer mock provides proof

This approach leaves you with pure data in hand and no effects to manage.

## Take a look at chant

[chant](https://intentius.io/chant/) is waiting for you to point your agent at it. Ask your agent what your infra would look like with chant instead.

---

## Read more

- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
- [Configuration as code, and as data](/posts/code-as-config-config-as-data/)
- [Which infrastructure tool actually keeps the spec?](/posts/which-tool-keeps-the-spec/)
- [The far-left IaC tool](/posts/the-far-left-iac-tool/)
- [Effect receipts](https://intentius.io/chant/concepts/effect-receipts/) · [Lifecycle models](https://intentius.io/chant/concepts/lifecycle-models/) · [chant](https://intentius.io/chant/)
