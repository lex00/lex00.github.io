---
title: "Solving the stress of infrastructure inheritance"
date: 2026-09-12
draft: false
featured_image: "img/inheritance-import-adopt-hero.svg"
---

You just inherited a Terraform estate. The state file is the only thing telling you which resources are yours.

[choudoufu](https://intentius.io/choudoufu/) fixes that in place. It stamps every resource with the estate that owns it. Your IAM enforces the stamp from then on, and the state file demotes to a cache you can safely delete.

## Identity on the resource

Identity is a record of which estate created a resource and under what name. In stock Terraform that record is the state file. choudoufu puts it on the resource too.

## Adoption writes it on the resource

Terraform import records your resources in state. choudoufu adoption writes two tags onto the resources themselves, behind an approval gate you control. choudoufu reads those tags on every run. So does your IAM.

Your resources sit in your account under your own policies. The tags stay on them whether you keep choudoufu or not.

## On Monday

"Who owns this" becomes a tag query. A tag carries exactly one owner, so the answer is always a single name.

Your IAM gates on that tag, including console calls that bypass your pipeline entirely.

All of it runs on the estate you already have. Your approval is the only one required.

Adoption is one gate and two tags. [Try it on a live estate](https://intentius.io/choudoufu/docs/use/migrate/).

---

## Read more

- [Adopt infrastructure without re-homing it](/posts/adopt-without-rehoming/)
- [Down to earth infra dependencies](/posts/down-to-earth-infra-dependencies/)
- [choudoufu](https://intentius.io/choudoufu/) · [chant](https://intentius.io/chant/)
