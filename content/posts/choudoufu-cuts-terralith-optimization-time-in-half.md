---
title: "choudoufu cuts terralith optimization time in half"
date: 2026-08-25
featured_image: "img/tofu-electrodes-hero.png"
draft: false
---

[choudoufu](https://intentius.io/choudoufu/docs/) is a fork of OpenTofu with [identity hooks](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/).

This blog takes a look at Cursor's recent migration from Terraform to OpenTofu, and how it could have gone differently if it wasn't held back by state.

## choudoufu writes ownership on the resource itself

choudoufu adopts by stamping. Terraform adopts by fixing resolution in state.

Two tags on the resource, read live at plan time. That's the whole trick of [identity hooks](/posts/tofu-tastes-better-with-identity-hooks/).

![The state world translated to the tag world](/img/cursor-migration/translation.svg)

![One monolith split with a state file vs with identity hooks](/img/cursor-migration/split-mechanics.svg)

## What takes less time

choudoufu's import pass stamps identity markers onto the resources as tags.

![Moving one workspace: to a new state backend vs to choudoufu](/img/cursor-migration/workspace-move.svg)

This means moving resources is as easy as changing tag values. Each plan reads the cloud directly, avoiding costly drift workarounds.

## The slowest part sets the calendar

![Migration work sorted: thinking that survives any tool vs work that exists because the file does](/img/cursor-migration/work-shape.svg)

In the actual migration the slowest chain was state. State work is 38% of the engineering weeks and a larger share of the calendar, since parallel work shares the schedule while the serialized chain sets it.

Removing the state chain reduces the timeline driver to the decision making on boundaries.

## Half the time

The top track is Cursor's timeline. The bottom two are the same estate on identity hooks.

![OpenTofu actual vs choudoufu replay vs chant projection](/img/cursor-migration/timeline.svg)

Either of the bottom tracks offers you a migration path taking half the time.

People problems stay at full price in my math. The months I subtract for choudoufu are all about Terraform's state model.

![Waterfall from 7 months to roughly 3.9](/img/cursor-migration/waterfall.svg)

My claim is the same migration to choudoufu would be 3.5 to 4 months against the actual 7, with error margin about a month either way.

Every before-and-after figure here comes from the migration's public case study. Only the step-size estimates are mine.

## What is chant?

[chant](https://intentius.io/chant/) is the reason choudoufu exists. It also works with live markers, among other useful changes from our favorite infra tools.

[choudoufu](https://intentius.io/choudoufu/docs/) is experimental and AWS only, for now...

---

## Read more

- [Tofu tastes better with identity hooks](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/)
- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [Take a whiff of choudoufu](https://lex00.github.io/posts/take-a-whiff-of-choudoufu/)
- [The revolving door of authoritative state](https://lex00.github.io/posts/the-revolving-door-of-authoritative-state/)
- [choudoufu docs](https://intentius.io/choudoufu/docs/)
- [chant](https://intentius.io/chant/)
