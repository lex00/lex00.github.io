---
title: "A release is a compile target"
date: 2026-07-14
---

Call something a compile target and you have said two things about it. It can be correct by construction, and it is cheap to produce. A compiler checks the output before it emits it, and it emits it from a description shorter than the output itself. That is the whole reason to have one.

Say it about a release and both claims carry. The deploy can be correct before it runs, and adding one costs a declaration instead of a pipeline.

## The bespoke process is the problem

Kubernetes made deploy uniform by giving everyone one apply verb. A manifest describes the desired state, `kubectl apply` hands it over, a controller makes it real. Because the verb is shared, the pipeline around it is shared. One platform team writes it and a hundred services ride it. I wrote about this in [The apply verb you only get on Kubernetes](https://lex00.github.io/posts/the-apply-verb-you-only-get-on-kubernetes/).

Step off the cluster and the verb is gone. Building an image is one step, promoting it another, applying a stack a third, wiring one stack's outputs into the next a fourth. None of it is standardized, so all of it lands in the pipeline, and the pipeline multiplies. Every component grows its own process, each a near copy of the last, drifting apart until no two match.

Teams accept the per-component process as the way it is. A compile target says otherwise. It says the process is derivable, not authored.

## Correct by construction

A component described as data is typed and linted before anything runs. A cross-stack reference resolves by name instead of getting scraped out of another stack with `jq`. A bad reference or a missing output is a build error at author time, not a failure halfway through the deploy.

The deploy stops being a script you hope is right and becomes output a compiler checked.

## Cheap to produce

One generic runner deploys every component, with no per-component code in the runner. Adding a component is one declaration and no new pipeline. The order comes from the dependency graph. The CI you already run is generated from the same declarations, one thin job per component, outputs handed across job edges as artifacts.

The hundredth component stays as cheap as the first. That is what the shared apply verb bought on Kubernetes, recovered off the cluster by describing the component as data and compiling the release from it.
