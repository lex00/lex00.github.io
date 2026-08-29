---
title: "Guardrails that survive the round trip"
date: 2026-08-10
---

{{< inline-svg src="guardrails-hero.svg" alt="Bird's eye view of a road curving hard through the frame. Along the outside of the curve runs a cliff edge drawn with hachure ticks, black void beyond it. A big rig labelled chant on its trailer rounds the upper curve tightly in the inner lane. A guardrail lines the cliff side, intact below the bend and intact beyond it, but torn open at the apex: gray rail fragments twist outward and skid marks point at the gap, where a big rig with CLICKOPS on its trailer is jackknifing mid-air past the edge, over the void." >}}

Kubectl and its cousins operate on your estate based on domain knowledge they carry.

chant puts a compiler under your estate, and that knowledge moves into [TypeScript](https://intentius.io/chant/concepts/typescript-as-data/).

Rules that live in typed source move in two directions. They check what exists and predict what will happen when enforced.

<!-- TODO: link the post that prompted this -->

# The matrix

{{< inline-svg src="guardrail-matrix.svg" alt="A four column table. Rows compare where each shape writes and where its rules live and how it handles drift and ownership. The chant column is highlighted. chant writes typed source in git and the compiler applies one lint rule to every surface. It round trips via import and carve. Drift is attributed field by field and ownership is shared and surfaced and never seized for you. Its exit is platform native and in-language. kubectl and its variants write to live state with rules hand-written in each command and the console as the exit. Config-store tools write to config records with rules in tool code and triggers and see only their own records with break glass as the exit. Both of those shapes create drift." >}}

# What the compiler enables

A chant lexicon is a round-trip spec compiler with semantic linting.

- Types come from the provider's own spec. Invalid shapes don't get validated. They don't exist.
- Lint judgments run at build, audit, and carve. Written once.
- Round-trip means the same judgments apply to existing resources as well.

A config store can import live state too. Import copies it into records. carve decompiles it into the language the lint runs in, and scores what the move will cost before you make it.

cdk8s and Pulumi compile source as well but they [bundle execution](/posts/a-typescript-compiler-for-kubernetes-manifests/). The program runs through an engine and the engine keeps state. chant stops at synthesis and the artifact is the spec.

<!-- TODO: WAW042 beat — carve pulled a bucket out of Terraform, lint caught a policy gap Terraform had no layer capable of noticing -->

# What makes chant-k8s-client so different

[chant's k8s client](https://www.npmjs.com/package/@intentius/chant-k8s-client) is not a small kubectl. Every unique choice in it is downstream of the compiler.

{{< inline-svg src="client-choices.svg" alt="A two column table pairing each choice with its reason. Kinds resolve from the spec pass that made the types since they cannot skew. Raw JSON with no model coercion since coercion drops what drift attribution needs. managedFields as primitives since every field is attributed and ownership is surfaced. Provenance on every read since a read is evidence and not all of it is equal. Typed failures since the callers are programs. No watch or exec or port-forward since cockpit features belong in a cockpit. Credentials behind an import-graph test since synthesis stays pure." >}}

The ownership machinery is Kubernetes' own server-side apply field managers. Most tools ignore it but chant treats it as a primitive.

Reacting to estate events is a different job owned by chant [ops and lifecycle](/posts/an-ecosystem-of-gruel/).

# Thin tools on top

When the compiler already did the work, everything above it gets to stay thin.

The real way out is [back to platform native](/posts/the-revolving-door-of-authoritative-state/).

See [intentius.io](https://intentius.io) and the method behind it at [accessibleops.net](https://accessibleops.net).

## Read more

- [Infrastructure deserves a compiler](/posts/infrastructure-deserves-a-compiler/)
- [A TypeScript compiler for Kubernetes manifests](/posts/a-typescript-compiler-for-kubernetes-manifests/)
- [An ecosystem of gruel](/posts/an-ecosystem-of-gruel/)
- [The revolving door of authoritative state](/posts/the-revolving-door-of-authoritative-state/)
- [chant how it compares](https://intentius.io/chant/concepts/comparison/) · [chant](https://intentius.io/chant/)
