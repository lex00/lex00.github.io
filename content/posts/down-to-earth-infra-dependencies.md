---
title: "Down to earth infra dependencies"
date: 2026-09-11
draft: false
featured_image: "img/down-to-earth-hero.svg"
---

Choudoufu gives you a model where dependencies come for free. One team's stack reads what another team's stack owns, straight from the cloud, and nobody has to bind the two together.

The orchestrators sell that binding as the product. Stack dependencies get a diagram and a pricing tier. Underneath, one stack's output is copied into a variable for the next, and keeping that copy fresh is where the toggles and workarounds come from.

The binding lives in their platform, and nobody reading your repository can see it.

## The old stack reach pattern

Say Terraform builds some servers and Ansible configures them. When your ops model cannot express that dependency, the Ansible job reaches into the Terraform stack for the addresses. An orchestrator does the same reach on your behalf and charges for it.

The reach pattern is the problem, whether free or paid.

## The tags drive the lookups

In choudoufu every resource carries two tags: the estate that owns it and the address it was declared at. They are derived from source and enforced, so a lookup can trust them. Plain default tags never gave you that.

Ansible finds the servers by those tags, live, on every run. There is no copy to keep fresh and nothing to trigger.

## Dependencies do not need new machinery

Ownership already expresses the dependency. Put it on the resource and your jobs read from the thing itself instead of a platform hovering above it.

Choudoufu: dependencies without the middleman.

---

## Read more

- [A release is a compile target](https://lex00.github.io/posts/a-release-is-a-compile-target/)
- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [Take a whiff of choudoufu](https://lex00.github.io/posts/take-a-whiff-of-choudoufu/)
- [choudoufu](https://intentius.io/choudoufu/)
