---
title: "Infrastructure deserves a compiler"
date: 2026-02-23
---

Every IaC tool tries to own the full lifecycle. Provisioning, state management, drift detection, rollback. The synthesis step got bundled in with the rest. Turning source code into deployable output is a compilation problem. It deserves to be treated like one.

## What bundling synthesis costs you

When synthesis is embedded in a provisioning tool, it inherits that tool's constraints. You get the type system the tool provides. You get the validation the tool exposes. You lint what the tool lets you lint.

You also get the tool's opinions about how to write infrastructure. Every DSL starts simple. Then it needs loops, conditionals, references, modules, overrides. Eventually it needs escape hatches. At that point you have an accidental programming language.

TypeScript already has a type system. It has modules, generics, unions, intersections, mapped types. It has an ecosystem of linters, formatters, editors, and language servers. The type system is the escape hatch.

## What a compiler approach looks like

I built [chant](https://intentius.github.io/chant/) to treat infrastructure synthesis as a compilation problem.

You write TypeScript. The compiler parses it as data, not as imperative instructions. Every resource is typed against the target spec. All 1,100+ CloudFormation resource types become TypeScript types with attribute-level constraints.

Semantic linting happens at the data model level. Structural analysis of the resource graph instead of string matching on YAML keys. Linting rules are TypeScript files with access to the typed model. They can reason about relationships between resources instead of individual fields.

The output is standard CloudFormation JSON. Or GitLab CI YAML. The spec-native format the platform already understands. No runtime, no state file, no daemon. If you stop using chant tomorrow, your output files still work. Walk-away cost is zero.

## This was always possible

The approach predates the current generation of IaC tools. Parse a host language as data. Type-check it against a spec. Emit a target format. This is what compilers do. Infrastructure synthesis is a good fit for the same pattern.

The pieces were available. TypeScript's type system is expressive enough to model infrastructure specs. The specs themselves are public, machine-readable data. The output formats are well-defined. The remaining step was treating synthesis as a standalone concern worth engineering on its own.

## Compilers and agents compose

Agents are good at operations. Reading logs. Diagnosing failures. Executing runbooks. Making decisions in context. That work is fundamentally interactive and sequential.

Compilation is the opposite. It is deterministic and parallelizable. You can analyze it without running it. You can inspect the output. You can diff it. You can review it in a pull request. You can run static analysis on it before it touches any infrastructure.

These are complementary. An agent can invoke a compiler. A compiler's output is machine-readable input for an agent. They compose well precisely because they do different things.

The abstractions that last are the ones that are both human-reviewable and machine-generatable. Typed data with contracts fits that shape.

## Infrastructure as data with typed contracts

The core idea is small. Infrastructure definitions are data. Data has a schema. Schemas can be expressed as types. Types can be checked at compile time.

When your infrastructure is typed data you get a lot for free. Editor completions that know every valid attribute of an S3 bucket. Hover documentation pulled from the spec. Lint rules that traverse the full resource graph. Refactoring tools that understand what a reference means.

There's a less obvious benefit. The entire definition is analyzable without executing it. No sandbox. No credentials. No provider plugins. The compiler reads TypeScript and emits JSON. Everything in between is pure computation over typed data.

## The path from here

CDKTF is discontinued. Pulumi requires a runtime. CDK still owns the full lifecycle. TypeScript users who want typed infrastructure have fewer options than they did a year ago.

Chant takes a different position. It is only a compiler. It turns typed TypeScript into spec-native output and gets out of the way. You deploy with whatever you already use.

If this framing resonates, the [docs](https://intentius.github.io/chant/getting-started/introduction/) walk through the model in detail. The [comparison page](https://intentius.github.io/chant/concepts/comparison/) maps chant against CDK, Pulumi, SST, and Terraform side by side.
