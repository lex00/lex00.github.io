---
title: "Solving the stress of infrastructure inheritance"
date: 2026-09-12
draft: false
featured_image: "img/inheritance-import-adopt-hero.svg"
---

You just inherited a Terraform estate. The state file is the only thing telling you which resources are yours.

[choudoufu](https://intentius.io/choudoufu/) fixes that in place. It stamps every resource with the estate that owns it. Your IAM enforces the stamp from then on, and the state file demotes to a cache you can safely delete.

## You are being sold a process

An orchestrator's marketing page says the "real blocker is ownership not the tooling." It adds that "multiple teams share responsibility, none own the outcome," and asks "who decides which team takes ownership."

The ownership in those quotes is accountability. Who gets paged, who takes the blame. Every vendor leaves that to you, theirs included.

Identity is the other kind, and the one you can buy. It is a record on the resource of which estate created it and under what name. Terraform has no place to keep it. Inherit an estate and you inherit a state file and a prayer.

Their pitch skips identity entirely. I don't think they know it is a separate thing.

## Import hands it to them, adoption hands it to you

What the orchestrator calls importing, choudoufu calls adoption. Import copies your resources into a record the vendor holds. Adoption writes two tags onto the resources themselves, behind an approval gate you control. choudoufu reads those tags on every run. So does your IAM.

Your resources sit in your account under your own policies. The tags stay on them whether you keep choudoufu or not.

## What you get on Monday

"Who owns this" becomes a tag query. A tag carries exactly one owner, so the answer is always a single name.

Your IAM gates on that tag, including console calls that bypass your pipeline entirely.

All of it runs on the estate you already have. Your approval is the only one required.

Adoption is one gate and two tags. [Try it on a live estate](https://intentius.io/choudoufu/docs/use/migrate/).

---

## Read more

- [Adopt infrastructure without re-homing it](/posts/adopt-without-rehoming/)
- [Invisible ownership is ridiculous](/posts/invisible-ownership-is-ridiculous/)
- [Good tools can survive great "culture"](/posts/good-tools-can-survive-great-culture/)
- [Down to earth infra dependencies](/posts/down-to-earth-infra-dependencies/)
- [choudoufu](https://intentius.io/choudoufu/) · [chant](https://intentius.io/chant/)
