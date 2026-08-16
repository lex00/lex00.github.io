---
title: "The byproduct is one layer lower"
date: 2026-08-04
draft: true
---

Adam Chlipala has a new post, [*Rewrite All the Code, All the Time*](https://stng.substack.com/p/rewrite-all-the-code-all-the-time). I borrowed from their last one in [Honor the lower layer](/posts/honor-the-lower-layer/), so I read this one expecting to agree.

I mostly do. We both think the low layer is disposable. We put it in different places, about three layers apart.

## What it says

Reimplementation gets cheap enough to run every release. So "code as we know it will become a throw-away automatic byproduct of the real long-lived artifacts, joining formats like assembly language that we mostly think of in that way today." What you keep is different too: "Instead of storing conventional code in repositories, we would prefer to store the highest-level description of requirements that we can get away with." For the cycle to run at that rate it needs "absolute minimization of the need for human oversight."

This is not the prompt-your-way-to-production argument. Chlipala rules that out directly. "I doubt we will ever have fully automatic generation of production-ready systems from specifications in natural language." EARS and the structured-English formats get the same treatment, "that kind of hybrid beast that we'd be better-off replacing with a proper, unambiguous language."

The artifact you keep is a formal spec. The implementation falls out of it.

## The agreement

chant's output is disposable by design. Delete the compiler and the CloudFormation still deploys. Zero walk-away cost is the same sentence as throw-away byproduct.

Infrastructure is friendly ground for the rest of it. The specs are published and machine-readable. `AWS::EC2::Instance` has no ambiguity in it.

The regeneration already runs. chant imports a live cloud into typed source, [carves a slice out of a Terraform estate](/posts/the-long-road-back-to-native/), and `ReconcileOp` regenerates the TypeScript on drift and opens a PR. Roundtrip tests hold the two faithful.

## The layer

Chlipala draws the line above source code. The program is the byproduct and a requirements document lives in git.

I draw it one down. The CloudFormation is the byproduct. The typed TypeScript lives in git and takes the blame.

## Assembly had a compiler over it

Nobody reads assembly because the translation is deterministic, the contract underneath held for decades, and the error points at the line you wrote. Hohpe's test for a compiler against a code generator is that last one. A generator drops you into the lower layer at the moment you can least afford it.

Chlipala's earlier post is where I got my version of this. The expensive fictions are abstractions that reimplement the layer below without honoring it.

The new post assumes the compiler and reasons forward. For infrastructure I can point at one. For a payroll system there is no notation to compile from, and the missing notation is the problem rather than a step on the way to it.

## What review hinges on

Full regeneration removes the implementation diff. Every line is new.

Four of the nine properties in [Onboardable](/posts/onboardable/) need a diff. One reviewable path, attributable, bounded blast radius, reversible before risky. All four describe a delta.

The answer available is that the spec diff takes over. That needs a bound on how much implementation moves per line of spec, and there is none. Unbounded implementation change from bounded spec change is the condition blast radius limits exist to stop.

The compiler defense does not reach it either. We skip reviewing compiler output because the output is stable. Chlipala wants regeneration that picks up new security concerns, new algorithms, and new performance requirements on its own. That output changes when the spec did not, which is the one way it is unlike a compiler and the one way that matters to operations.

Verification does not cover the gap. A proof that the implementation matches the spec says nothing about how much of the running system moved. Canary width, migration order, whether it ships on a Friday. None of those are correctness questions.

And a proof covers the properties someone wrote down. Review catches the thing nobody specified. That is unglamorous and it is most of what review earns.

## Generation was never the expensive part

Generation cost is falling. Specification cost is a separate number and nothing here moves it. Writing the unambiguous version has been the binding constraint in formal methods for fifty years, for human reasons that cheap compute does not touch.

The post concedes this sideways. EARS gets dismissed for smuggling freeform English into a template, which is accurate, and is also the reason EARS exists.

Fiat Cryptography works because its spec is small, closed, stable for decades, and attached to a catastrophic failure cost. Payroll has none of the four.

## The requirements add up to a compiler

Regeneration with no oversight needs a translation that is a pure function of the spec and checkable before it emits. That is a compiler. Once you have one you stop regenerating and start rebuilding, because the output is boring.

Rewriting all the time needs the translation unstable enough to keep rerunning and trustworthy enough to skip review. Pick either and you land on ordinary compilation.

## The size of the claim

Chlipala is not writing about infrastructure, and this is not a rebuttal of their field. Where the spec is small and stable and the failure cost is high, they are describing finished work. The verified artifacts are running on every machine I own.

The claim is about distance. One layer up, into typed data shaped like the spec, is available this year with the diff intact. Several layers up, into a notation nobody has written for general software, spends the diff to get there.

The byproduct does keep moving down. Mine is already below the source. I would like to keep the diff while we find out how much further it goes.

---

## Read more

- [Rewrite All the Code, All the Time](https://stng.substack.com/p/rewrite-all-the-code-all-the-time) — Adam Chlipala
- [The Expensive Fictions of Low-Level Programming Languages](https://stng.substack.com/p/the-expensive-fictions-of-low-level) — Adam Chlipala
- [Honor the lower layer](/posts/honor-the-lower-layer/)
- [Onboardable](/posts/onboardable/)
- [The best proof is the one you don't need](/posts/the-proof-you-dont-need/)
- [TypeScript is the right choice for infra](/posts/typescript-is-the-right-choice-for-infra/)
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) · [chant](https://intentius.io/chant/)
