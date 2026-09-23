---
title: "Fidelity matters for infrastructure-as-code"
featured_image: "img/fidelity-three-shapes.svg"
date: 2026-09-20
draft: false
---

Most cloud specs are JSON. Most IaC (infrastructure as code) is not.

A typed config language approach for IaC preserves the lifecycle as a daemon that reconciles cloud state back into the config. It also preserves tooling details in the form of a schema in every file. And it does those things while failing to preserve the look and format of the JSON specs.

AWS did this right with CDK L1. The L1 TypeScript classes are instantly recognizable to an AWS operator. This matters so much during an incident when you want to compare your definition of a cloud resource to a cloud error.

[TypeScript as Data](https://intentius.io/typescript-as-data/) is not a typed configuration language. TypeScript as Data types a spec as an object literal, and a build compiles it directly to the target and stops.

[chant](https://intentius.io/chant) gives you that CDK L1 experience across the big cloud vendors and K8s. I did not pick a typed config language for chant. I did what CDK L1 does, for every platform.

Reaching for a typed config language is [the intoxicating mix of synthesis and execution](https://lex00.github.io/posts/the-intoxicating-mix-of-synthesis-and-execution/) again.

## Can you ship what you write?

Config language: looks nothing like the artifact you ship.

TaD: the CloudFormation template is the artifact. Nothing sits between.

## Is the interface up to date and operational?

Config language: both imply a daemon reconciling the cloud into your config.

TaD: types regenerate from the schema the vendor publishes. Live is read on demand, so a local snapshot is allowed to go stale. Resources carry live markers, so nothing needs reconciling.

## Who handles translation?

Config language: the tool. A `Resolvable` type becomes a `Ref`, and you learn what else changed at plan.

TaD: no one. `BucketEncryption` in the file is `BucketEncryption` in the template. The build folds TypeScript into data before plan.

## How usable is the representation?

Config language: usable inside its own tooling. Everything else in your day speaks JSON and TypeScript.

TaD: usable in your editor as is. Completion comes from the spec. Red squigglies, and you are still looking at the original spec.

## Where is the spec during an incident?

Config language: in the tool's output. The console shows CloudFormation and your source shows something else.

TaD: in your source, because that is what you write and ship. It matches the console.

## Can it separate synthesis from ops?

Config language: no. The lifecycle is a reconciliation daemon and the tool-specific detail is the schema, in every file you open. The design requires both.

TaD: synthesis compiles and stops. Observe by default, reconcile if you choose. The template never mentions the ops. Delete them and the templates keep working.

## Fidelity matters for IaC

An interface that renames the contract has lost fidelity, and it is married to a lifecycle.

A typed config language generated around a schema loses fidelity by reshaping the contract.

The answer for IaC is [TypeScript as Data](https://intentius.io/typescript-as-data/).

---

## Read more

- [Honor the lower layer](/posts/honor-the-lower-layer/)
- [Configuration as code, and as data](/posts/code-as-config-config-as-data/)
- [TypeScript vs Pkl for IaC](/posts/typescript-vs-pkl-for-iac/)
- [TypeScript as Data](https://intentius.io/typescript-as-data/)
- [Accessible Ops](https://accessibleops.net/)
