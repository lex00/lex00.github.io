---
title: "Adopt infrastructure without re-homing it"
date: 2026-07-18
draft: true
---

You rarely start infrastructure from nothing. You adopt it. Either you inherited it, a CloudFormation stack or a folder of manifests you now have to keep running, or you chose it, an open source platform you pulled in for a need. Both hide the same question: to keep this thing, what does the tool make you do to it?

[Accessible Ops](https://accessibleops.net) calls the property [adopt in place](https://accessibleops.net/adopt-in-place/), and states it in the abstract. This is the concrete version, in both directions.

## Inherited

You already have a spec, and most tools give it a second home before they will manage it. Terraform imports it into state, and from then on the state file is the record that decides what is yours. Modern Terraform will generate the HCL for you, so the rewrite is less of a chore than it used to be, but the resource is now bound to a file you have to host, lock, and keep honest. ConfigHub holds it as data in its store, which it does on purpose and which is what buys it a real control plane. I worked through that trade in [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/) and I am not relitigating it here.

The narrower point is the one that matters for adoption. When the tool keeps its own copy, leaving means getting your config back out of it.

chant adds types and hands the same spec back. A CloudFormation template stays a CloudFormation template. It is spec-native, with no format of its own for your config to move into. So you take upstream updates, you can quit chant and keep deploying, and you never bet the config on a database or runtime to keep it alive.

## Chosen

Adopting an open source platform into a real account usually means forking it. You cut it open and wire in your VPC, DNS, and IAM by hand, because upstream cannot know your environment. Now you own a fork that drifts with every release.

The healthier version does not fork. You build a toolkit around the upstream and leave the upstream intact. The seams, tiers, CI, and naming live in a layer above it, and you adopt by setting parameters, not by editing the platform.

[loomster](https://github.com/INTENTIUS/loomster) is that toolkit for [awslabs/loom](https://github.com/awslabs/loom). It wraps Loom, pinned at v1.6.0, and every composite exposes a provision, reference-existing, or omit choice where the piece is load-bearing: network, identity, KMS, certificates, database, DNS, and registries. Nothing is forked, so upstream stays trackable.

The evidence comes in two parts. Both production tiers are validated end to end on a real AWS account at seven of seven stacks, `production-ha` adding Multi-AZ RDS and a live credential rotation, running as a second instance alongside `production`. And `src/examples/byo` deploys against pre-existing everything with zero composite edits. The enterprise gets Loom on its own network and identity, at production scale, holding standard specs.

## Both halves

Re-homing arrives as either a conversion of your spec or a fork of the upstream. chant avoids both because it works on the spec directly and keeps adoption in a layer above the platform. You put types on what you inherited, or a toolkit around what you chose. It stays what it was.

---

## Read more

- [Adopt in place](https://accessibleops.net/adopt-in-place/) — Accessible Ops XII
- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [loomster](https://github.com/INTENTIUS/loomster)
