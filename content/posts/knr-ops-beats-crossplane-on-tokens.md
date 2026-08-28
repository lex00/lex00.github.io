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

| task | knr-ops | Crossplane | knr-ops saves |
|---|---:|---:|---:|
| comprehend | 5,075 | 6,431 | 21% |
| generate | 9,009 | 9,836 | 8% |
| modify | 3,433 | 3,434 | ~0% |
| debug | 3,440 | 4,011 | 14% |

Crossplane does better on two task types, review and deep semantic questions.  This is because Crossplane's CRDs are cheaper than a Flux/kustomize overlay.

## The buried number: chant beats everyone

| stack | avg tokens / run |
|---|---:|
| **chant** | **4,584** |
| pulumi-typescript | 5,212 |
| Crossplane | 5,274 |
| bare | 5,354 |
| knr-ops | 5,756 |
| pulumi-python | 5,785 |
| terraform | 6,067 |

[chant](https://intentius.io/chant/) is 24% cheaper than Terraform here. The saving comes from compiling TypeScript into the same plain manifests other tools hand an agent directly.

## Two new tools heading the same direction

knr-ops gains an advantage by keeping nothing between the agent and the YAML. The manifest it reads is the manifest the cluster runs. This is a smart way to save tokens.

With chant, the agent also sees only plain YAML. The types behind it are what keep the source from drifting off spec.

Terraform, Pulumi, and Crossplane all require an agent to stage a representation layer before they can hold the infrastructure. That representation layer is expensive.

## Read more

- [iac-cd-bench](https://github.com/lex00/iac-cd-bench), the benchmark this round is from
- [chant-bench](https://intentius.io/chant-bench/), how chant's own runs are gated and what gets published
- [aws-bench: scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/), on chant's cost advantage against a live AWS estate
- [Which infrastructure tool actually keeps the spec?](/posts/which-tool-keeps-the-spec/), on why chant's output has nothing left to walk away from
