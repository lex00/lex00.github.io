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

[Luke Hoban](https://infoq.com/presentations/cloud-programming-typescript) co-created TypeScript and took it to infrastructure at Pulumi. Pulumi executes your TypeScript. Constructors run, API calls happen, and the program's result is the infrastructure. TypeScript as a program.

[Brian Grant](https://itnext.io/introducing-confighub-b127736641c5) wrote the Kubernetes Resource Model and has argued for years that configuration is data. ConfigHub follows that through. The config lives as data in a store, and tools manipulate it. No language at all.

A new language, an executed language, and no language.

## TypeScript as data

chant takes the language Hoban chose and the data model Grant argued for. Resources are typed object literals, the build reduces them to the spec, and synthesis never touches the cloud.

Configuration as code and configuration as data, [at the same time](/posts/code-as-config-config-as-data/).

## Where the abstractions end

Below are the [accessible ops](https://accessibleops.net) principles. 

Here is the configuration language column beside chant, from the [full chart](https://intentius.io).

| | | chant | Pkl / CUE / KCL |
|---|---|:---:|:---:|
| **I** | [Honor the lower layer](https://accessibleops.net) | ● | ● |
| **II** | [The same check, left of the commit](https://accessibleops.net) | ● | ● |
| **III** | [Documentation is law](https://accessibleops.net) | ● | ● |
| **IV** | [One path to prod](https://accessibleops.net) | ● | – |
| **V** | [Named secrets, least privilege](https://accessibleops.net) | ● | – |
| **VI** | [Bounded blast radius](https://accessibleops.net) | ● | – |
| **VII** | [Reversible before risky](https://accessibleops.net) | ● | – |
| **VIII** | [Escalate the judgment](https://accessibleops.net) | ● | – |
| **IX** | [Attributable](https://accessibleops.net) | ● | – |
| **X** | [Secret rotation is cheap](https://accessibleops.net) | ● | – |
| **XI** | [The live system is the truth](https://accessibleops.net) | ● | ✗ |
| **XII** | [Adopt in place](https://accessibleops.net) | ● | ◐ |
| **XIII** | [Manage only what you declare](https://accessibleops.net) | ● | – |
| **XIV** | [Verify the artifact](https://accessibleops.net) | ● | – |

● by design, ◐ partial, ✗ not met, – out of scope. 

This is Intentius' chart and is biased toward chant, so read it accordingly.

On value constraints the config languages reach past TypeScript. A port that refuses anything under 1024 is expressible there.

By design, eleven rows get answered somewhere else, in a second abstraction that shares no types with what you authored.

TypeScript-as-data gives you more. The same abstraction stays with you in your editor, and in your ops lifecycle.

## The verdict

Config languages are good, so use them where appropriate.

An infrastructure toolchain answers all fourteen rows, and one abstraction should carry them. 

TypeScript does, and it's already fluent in every editor and every model, and it's already shaped like the spec.

TypeScript is the right choice for infra.

---

## Read more

- [TypeScript vs Pkl for IaC](https://lex00.github.io/posts/typescript-vs-pkl-for-iac/)
- [Configuration as code, and as data](https://lex00.github.io/posts/code-as-config-config-as-data/)
- [Infrastructure deserves a compiler](https://lex00.github.io/posts/infrastructure-deserves-a-compiler/)
- [A TypeScript compiler for Kubernetes manifests](https://lex00.github.io/posts/a-typescript-compiler-for-kubernetes-manifests/)
- [chant TypeScript as Data](https://intentius.io/chant/concepts/typescript-as-data/)
- [chant](https://intentius.io/chant/)
