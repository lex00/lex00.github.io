---
title: "Guardrails that survive the round trip"
date: 2026-08-10
---

{{< inline-svg src="guardrails-hero.svg" alt="Bird's eye view of a road curving hard through the frame. Along the outside of the curve runs a cliff edge drawn with hachure ticks, black void beyond it. A big rig labelled chant on its trailer rounds the upper curve tightly in the inner lane. A guardrail lines the cliff side, intact below the bend and intact beyond it, but torn open at the apex: gray rail fragments twist outward and skid marks point at the gap, where a big rig with CLICKOPS on its trailer is jackknifing mid-air past the edge, over the void." >}}

Kubectl and its cousins operate on your estate based on domain knowledge they carry.

chant puts a compiler under your estate, and that knowledge moves into [TypeScript](https://intentius.io/chant/concepts/typescript-as-data/).

Guardrails that live in typed source can move in two directions. They can check what exists, and they can predict what will happen when they get enforced.

<!-- TODO: link the post that prompted this -->

# The matrix

{{< inline-svg src="guardrail-matrix.svg" alt="A four column table. Rows compare where each shape writes, where truth lives, where guardrails live, the cost of adding one, whether the tool sees backwards, how drift is handled, the ownership model, and the escape hatch. The chant column is highlighted: typed source, git, the compiler, one lint rule for every surface, round trip via import and carve, drift attributed field by field, ownership shared and surfaced and never seized for you, escape hatch platform native and in-language. kubectl and its variants write to live state with guardrails hand-written in each command and the console as escape hatch, which creates drift. Config-store tools write to config records with guardrails in tool code and triggers, see only their own records, and break glass as escape hatch, which creates drift." >}}

# What the compiler enables

A chant lexicon is a round-trip spec compiler with semantic linting.

- Types come from the provider's own spec. Invalid shapes don't get validated. They don't exist.
- Lint judgments run at build, audit, and carve. Written once.
- Round-trip means the same judgments apply to existing resources as well.

A config store can import live state too. Import copies it into records. carve decompiles it into the language the lint runs in, and scores what the move will cost before you make it.

cdk8s and Pulumi compile source as well, but they [bundle execution](/posts/a-typescript-compiler-for-kubernetes-manifests/) — the program runs through an engine, and the engine keeps state. chant stops at synthesis, and the artifact is the spec.

<!-- TODO: WAW042 beat — carve pulled a bucket out of Terraform, lint caught a policy gap Terraform had no layer capable of noticing -->

# What makes chant-k8s-client so different

[chant's k8s client](https://www.npmjs.com/package/@intentius/chant-k8s-client) is not a small kubectl. Every unique choice in it is downstream of the compiler.

{{< inline-svg src="client-choices.svg" alt="A two column table, the choice and because. Kinds resolve from the spec pass that made the types, because they cannot skew. Raw JSON with no model coercion, because coercion drops what drift attribution needs. managedFields as primitives, because every field is attributed and ownership is surfaced. Provenance on every read, because a read is evidence and not all of it is equal. Typed failures, because the callers are programs. No watch, exec, or port-forward, because cockpit features belong in a cockpit. Credentials behind an import-graph test, because synthesis stays pure." >}}

The ownership machinery is Kubernetes' own — server-side apply field managers. Most tools ignore it. chant treats it as a primitive.

Reacting to estate events is a different job, owned by chant [ops and lifecycle](/posts/an-ecosystem-of-gruel/).

# Thin tools on top

When the compiler already did the work, everything above it gets to stay thin.

The real escape hatch is [back to platform native](/posts/the-revolving-door-of-authoritative-state/).

See [intentius.io](https://intentius.io) and the method behind it at [accessibleops.net](https://accessibleops.net).

## Read more

- [Infrastructure deserves a compiler](/posts/infrastructure-deserves-a-compiler/)
- [A TypeScript compiler for Kubernetes manifests](/posts/a-typescript-compiler-for-kubernetes-manifests/)
- [An ecosystem of gruel](/posts/an-ecosystem-of-gruel/)
- [The revolving door of authoritative state](/posts/the-revolving-door-of-authoritative-state/)
- [chant how it compares](https://intentius.io/chant/concepts/comparison/) · [chant](https://intentius.io/chant/)
