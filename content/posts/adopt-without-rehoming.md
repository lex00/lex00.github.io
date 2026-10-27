---
title: "Adopt infrastructure without re-homing it"
date: 2026-09-10
draft: false
featured_image: "img/adopt-stamps-hero.svg"
---

Lots of us are familiar with the set of decisions faced when inheriting a Terraform or Pulumi estate.

I build three tools that give you new choices in this situation.

## Option 1) Keep your Terraform and move identity to the resource

[choudoufu](https://intentius.io/choudoufu/) adopts a live Terraform estate without touching your resources. Simply use the [live backend](https://intentius.io/choudoufu/docs/use/migrate/) and you now can use IAM to gate your resources, and state files are demoted to a safely deleted cache.

choudoufu is AWS only and experimental.

[Click here for a demo](https://intentius.io/choudoufu/docs/examples/terralith-migration/)

## Option 2) Generate native templates with chant

[chant](https://intentius.io/chant/) compiles typed source into the platform's own spec.

It supports many providers and it has a [carve](https://intentius.io/chant/cli/carve/) feature that reads your Terraform to help you get started.

## Option 3) Keep your Pulumi programs and run them on plunge

[plunge](https://intentius.io/plunge/) is a fork of Pulumi with a drop-in CLI. It runs your programs as they are and writes two ownership tags on each cloud object.

plunge is early and has run on emulators only so far.

## No separate ownership record

choudoufu leaves your HCL alone and moves ownership onto the resource, and plunge does the same for your Pulumi programs. chant takes the resource out to CloudFormation or a Kubernetes manifest, where the platform keeps the binding itself.

Some go a slice at a time and some go all at once, but the property is the same. Nothing of yours ends up in a store any of these tools owns.

Adoption is easier with tags. Give it a try.

---

## Read more

- [Adopt in place](https://accessibleops.net/adopt-in-place/), Accessible Ops XII
- [choudoufu](https://intentius.io/choudoufu/) · [plunge](https://intentius.io/plunge/) · [chant](https://intentius.io/chant/)
