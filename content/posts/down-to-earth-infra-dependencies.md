---
title: "Down to earth infra dependencies"
date: 2026-09-11
draft: false
featured_image: "img/down-to-earth-hero.svg"
---

Choudoufu gives you a model where dependencies come for free. One team's stack reads what another team's stack owns, straight from the cloud, and nobody has to bind the two together.

The usual binding copies one stack's output into a variable for the next, and the next stack only runs when the copy changes. That is where the toggles and workarounds come from.

The binding lives outside your repository, and nobody reading the repository can see it.

## The old stack reach pattern

Say Terraform builds some servers and Ansible configures them. With no way to declare that dependency, the Ansible job reaches into the Terraform stack for the addresses. Nobody would call that crazy. The reach is standing in for a model that does not exist, so the dependency lives in a job step, or in an orchestrator that does the same reach for you.

The missing model is the problem in both cases.

## The tags drive the lookups

In choudoufu every resource carries two tags: the estate that owns it and its declared address. They are derived from source and enforced, so a lookup can trust them. Every estate is visible to the whole org the moment it creates a resource, with nothing to register.

Ansible finds the servers by those tags, live, on every run. There is no copy, so nothing but you decides when Ansible runs.

## Dependencies do not need new machinery

Ownership already expresses the dependency. Put it on the resource and your jobs read from the thing itself instead of a copy. Declare it once, as data in a chant component in your repository, and the graph works out the order and checks the wiring before anything runs. The tag is how the value resolves when it does.

Two tags, read live, are the dependency.

---

## Read more

- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [choudoufu](https://intentius.io/choudoufu/)
