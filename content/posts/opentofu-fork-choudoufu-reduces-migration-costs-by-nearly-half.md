---
title: "OpenTofu fork choudoufu reduces migration costs by nearly half"
date: 2026-08-25
draft: false
---

Cursor spent seven months migrating Terraform to OpenTofu.

The top track in this graphic is their timeline, the bottom two are the same estate on identity hooks.

![OpenTofu actual vs choudoufu replay vs chant projection](/img/cursor-migration/timeline.svg)

Either of the bottom tracks offers you a migration path taking half the time.

This claim sounds a bit outrageous at first, but it's actually quite conservative.

People problems stay at full price in my math. The months I subtract for choudoufu are all about Terraform's state model.

## Keeping a separate ledger is costly

Terraform's state model bundles multiple concerns together.

It moves when you change vendors, and Terraform Cloud bills it by the line.

![Migration work sorted: thinking that survives any tool vs work that exists because the file does](/img/cursor-migration/work-shape.svg)

## choudoufu writes ownership on the resource itself

Two tags on the resource, read live at plan time. That's the whole trick of [identity hooks](/posts/tofu-tastes-better-with-identity-hooks/).

The traditional migration pattern becomes a tag rename. Your Terraform code stays where it is.

The orchestration bill becomes your own CI plus [one IAM policy](/posts/terraform-state-has-three-pieces/).

Because choudoufu observes the tags live at plan time, you are protected from stale-inventory problems.

![One monolith split with a state file vs with identity hooks](/img/cursor-migration/split-mechanics.svg)

## What took less time

The state never moves again, because one import pass stamps its contents onto the resources as tags.

With no file, there is no platform to stand up. A split stops being surgery and becomes a rename. Drift workarounds have nothing to work around, since every plan reads the cloud directly.

Adopting choudoufu is one verified pass over the estate you already run. A traditional migration is months of carrying a fragile file between vendors without dropping it.

That gap is the whole claim.

## Half the time

![Waterfall from 7 months to roughly 3.9](/img/cursor-migration/waterfall.svg)

My claim is the same migration to choudoufu would be 3.5 to 4 months against the actual 7, with error margin about a month either way.

Every before-and-after figure here comes from the migration's public case study. Only the step-size estimates are mine.

My math leans conservative pricing adoption at parity, and adoption is precisely the thing [choudoufu](https://intentius.io/choudoufu/docs/use/migrate/) is better at.

## What is chant?

[chant](https://intentius.io/chant/) is the reason choudoufu exists. It also works with live markers, among other useful changes from our favorite infra tools.

[intentius.io/choudoufu/docs](https://intentius.io/choudoufu/docs/) is experimental and AWS only, for now...

---

## Read more

- [Tofu tastes better with identity hooks](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/)
- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [Take a whiff of choudoufu](https://lex00.github.io/posts/take-a-whiff-of-choudoufu/)
- [The revolving door of authoritative state](https://lex00.github.io/posts/the-revolving-door-of-authoritative-state/)
- [choudoufu docs](https://intentius.io/choudoufu/docs/)
- [chant](https://intentius.io/chant/)
