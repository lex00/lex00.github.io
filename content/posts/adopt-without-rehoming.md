---
title: "Adopt infrastructure without re-homing it"
date: 2026-09-10
draft: false
---

{{< inline-svg src="adopt-stamps-hero.svg" alt="A database cylinder carrying two ownership marker tags, tofu-estate and tofu-address, clipped to its side like luggage tags. Two rubber stamps labelled choudoufu and chant are poised above them. The caption reads: ownership rides on the resource, not in a state file." >}}

Lots of us are familiar with the set of decisions faced when inheriting a Terraform estate.

I build two infra toolchains that give you new choices in this situation.

## Option 1) Keep your Terraform and move identity to the resource

[choudoufu](https://intentius.io/choudoufu/) adopts a live Terraform estate without touching your resources. Simply use the [live backend](https://intentius.io/choudoufu/docs/use/migrate/) and you now can use IAM to gate your resources, and state files are demoted to a safely deleted cache.

choudoufu is AWS only and experimental.

[Click here for a demo](https://intentius.io/choudoufu/docs/examples/terralith-migration/)

## Option 2) Move back to platform native

[chant](https://intentius.io/chant/) goes the other direction, out of Terraform and into the platform's own spec.

It supports many providers and it has a [carve](https://intentius.io/chant/cli/carve/) feature for Terraform to help you get started.

## Neither keeps a separate ownership record

choudoufu leaves your HCL alone and moves ownership onto the resource. chant takes the resource out to CloudFormation or a Kubernetes manifest, where the platform keeps the binding itself.

One goes a slice at a time and the other goes all at once, but the property is the same. Nothing of yours ends up in a store either tool owns, so neither can charge you rent on the way out.

Adoption is easier with tags. Give it a try.

---

## Read more

- [Adopt in place](https://accessibleops.net/adopt-in-place/), Accessible Ops XII
- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
- [The revolving door of authoritative state](/posts/the-revolving-door-of-authoritative-state/)
- [Invisible ownership is ridiculous](/posts/invisible-ownership-is-ridiculous/)
- [choudoufu](https://intentius.io/choudoufu/) · [chant](https://intentius.io/chant/)
