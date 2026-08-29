---
title: "knr-ops beats Crossplane on the token bill"
date: 2026-08-28
featured_image: "img/knr-ops-token-burndown-cover.svg"
---

Token savings in IaC is so hot right now.

It pays to understand which tools save you the most money and why.

## knr-ops beats Crossplane where the work happens

Here is a new round of [iac-cd-bench](https://github.com/lex00/iac-cd-bench) with a result showing Crossplane losing on token spend to [knr-ops](https://github.com/polarsquad/knr-ops)

Haiku 4.5, k=3, all seven stacks, cold and warm, 252 runs.

{{< figure src="/img/knr-ops-token-tasks.svg" alt="knr-ops versus Crossplane in average tokens per run by task. On comprehend knr-ops averages 5076 against 6431 and saves 21%. generate runs 9010 against 9836 for 8%. The two tie near 3433 on modify. debug runs 3440 against 4011 for 14%." >}}

Crossplane does better on review and deep semantic questions.  Its CRDs are cheaper than a Flux/kustomize overlay.

## The buried number: chant beats everyone

{{< figure src="/img/knr-ops-token-overall.svg" alt="Average tokens per run across all seven stacks, cheapest first. chant 4,585. pulumi-typescript 5,212. Crossplane 5,275. bare 5,354. knr-ops 5,757. pulumi-python 5,785. terraform 6,068." >}}

[chant](https://intentius.io/chant/) is 24% cheaper than Terraform here. The saving comes from compiling TypeScript into the same plain manifests other tools hand an agent directly.

## Two new tools heading the same direction

knr-ops gains an advantage by keeping nothing between the agent and the YAML. The manifest it reads is the manifest the cluster runs. This is a smart way to save tokens.

With chant, the agent also sees only plain YAML. The types behind it are what keep the source from drifting off spec.

Terraform, Pulumi, and Crossplane all require an agent to stage a representation layer before they can hold the infrastructure. That representation layer is expensive.

## Read more

- [iac-cd-bench](https://github.com/lex00/iac-cd-bench) is the benchmark this round is from
- [chant-bench](https://intentius.io/chant-bench/) shows how chant's own runs are gated and what gets published
- [aws-bench: scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/) covers chant's cost advantage against a live AWS estate
- [Which infrastructure tool actually keeps the spec?](/posts/which-tool-keeps-the-spec/) explains why chant's output has nothing left to walk away from
