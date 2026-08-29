---
title: "TypeScript is the right choice for infra"
date: 2026-07-26
featured_image: "img/config-as-code-as-data-cover.svg"
---

Typed configuration languages are one fix for YAML hell.  [Pkl](https://pkl-lang.org/), [CUE](https://cuelang.org/), and [KCL](https://kcl-lang.io/) give you types, value constraints, and a compiler.

TypeScript solves the same problem, but it keeps going. It is the ideal foundation for an infrastructure toolchain, and chant is the proof.

## The config languages take Wheeler's deal

David Wheeler's [line](https://en.wikipedia.org/wiki/Fundamental_theorem_of_software_engineering) is that any problem in computer science can be solved by adding another level of indirection. Kevlin Henney's addendum is that this fails on the problem of too many levels of indirection.

Configuration languages have their answer. Place one of us in front of your YAML.

chant rejects this conclusion for infrastructure.

## What a config language buys, and what it costs

Configuration languages offer guarantees that TypeScript alone does not. Pkl cannot execute code, because the capability is absent from the language. 

chant chases the same properties by folding source instead of running it, and sandboxing the files that fall back.

A config language pays for that guarantee. Every spec it targets needs a library, and somebody writes it by hand, one spec at a time.

## TypeScript - just look at it

The industry's configuration formats descend from JavaScript, and TypeScript is the type system built for JavaScript. A typed object literal is typed JSON by descent.

[YAML 1.2](https://yaml.org/spec/1.2.2/) is a JSON superset, and [JSON](https://www.json.org/json-en.html) was carved directly out of JavaScript's object literal syntax in the first place.

TypeScript was designed for large-scale applications, and its [design goals](https://github.com/microsoft/TypeScript-wiki/blob/main/TypeScript-Design-Goals.md) say so.

Goal nine is "a consistent, fully erasable, structural type system."

Erasable types leave the output untouched. Structural types describe a shape. A shape is a schema.

Non-goal six directs you to "use TypeScript to describe existing libraries."

## Three people looked at this and picked differently

[James Ward's Pkl talk](https://youtu.be/yUmA5bA50H0) is the strongest case anyone has made for a purpose built configuration language. Watch it before you argue with any of this.

[Luke Hoban](https://infoq.com/presentations/cloud-programming-typescript) co-created TypeScript and took it to infrastructure at Pulumi. Pulumi executes your TypeScript. Constructors run and API calls happen and the program's result is the infrastructure. TypeScript as a program.

[Brian Grant](https://itnext.io/introducing-confighub-b127736641c5) wrote the Kubernetes Resource Model and has argued for years that configuration is data. ConfigHub follows that through. The config lives as data in a store, and tools manipulate it. No language at all.

A new language and an executed language and no language.

## TypeScript as data

chant takes the language Hoban chose and the data model Grant argued for. Resources are typed object literals and the build reduces them to the spec while synthesis never touches the cloud.

Configuration as code and configuration as data, [at the same time](/posts/code-as-config-config-as-data/).

## Where the abstractions end

Below are the [accessible ops](https://accessibleops.net) principles. 

Here is the configuration language column beside chant, from the [full chart](https://intentius.io).

{{< figure src="/img/typescript-infra-principles-table.svg" alt="Table of the fourteen accessible ops principles comparing chant and the config languages Pkl, CUE, and KCL. chant meets all fourteen by design. The config languages meet the first three which are honor the lower layer and the same check left of the commit and documentation is law. Adopt in place is partial. The live system is the truth is not met. The remaining ten are out of scope." >}}

This is Intentius' chart and is biased toward chant, so read it accordingly.

On value constraints the config languages reach past TypeScript. A port that refuses anything under 1024 is expressible there.

By design, eleven rows get answered somewhere else, in a second abstraction that shares no types with what you authored.

TypeScript-as-data gives you more. The same abstraction stays with you in your editor, and in your ops lifecycle.

## The verdict

Config languages are good, so use them where appropriate.

An infrastructure toolchain answers all fourteen rows, and one abstraction should carry them. 

TypeScript does. It's already fluent in every editor and every model and already shaped like the spec.

TypeScript is the right choice for infra.

## The benchmark agrees

aws-bench scenario 1 put this argument on the record. Same model on every side, Haiku 4.5, against Terraform, Pulumi, CDK, Alchemy, and an agent with no infrastructure tooling at all. The details are in the [scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/), and every run is published on [chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/).

{{< figure src="/img/aws-bench-s1-wrap-table-metrics.svg" alt="Board table ranked by cost per correct answer over eight questions at k equals 3 with tokens per question. chant scores 22 of 24 correct at 0.033 dollars per correct answer with 111k in and 2.1k out and is marked unranked while winning all. The aws cli baseline with no tool scores 17 of 24 at 0.050 with 108k and 2.7k and crowns for cost and input and output. pulumi scores 19 of 24 at 0.086 with 282k and 3.9k. terraform scores 19 of 24 at 0.111 with 357k and 4.8k. aws cdk scores 17 of 24 at 0.120 with 318k and 5.6k. alchemy scores 20 of 24 at 0.123 with 515k and 5.3k and a crown for correct." >}}

---

## Read more

- [aws-bench: scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/)
- [Scenario 1 results on chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/)
- [TypeScript vs Pkl for IaC](https://lex00.github.io/posts/typescript-vs-pkl-for-iac/)
- [Configuration as code, and as data](https://lex00.github.io/posts/code-as-config-config-as-data/)
- [Infrastructure deserves a compiler](https://lex00.github.io/posts/infrastructure-deserves-a-compiler/)
- [A TypeScript compiler for Kubernetes manifests](https://lex00.github.io/posts/a-typescript-compiler-for-kubernetes-manifests/)
- [chant TypeScript as Data](https://intentius.io/chant/concepts/typescript-as-data/)
- [chant](https://intentius.io/chant/)
