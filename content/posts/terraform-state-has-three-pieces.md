---
title: "Terraform state has three pieces"
date: 2026-08-19
featured_image: "img/three-pieces-cover.svg"
draft: false
---

A state file does three jobs.

It says which live resource an address refers to. It holds values the cloud has nowhere to put. And it records that an effect happened.

Those got bundled because one file happened to do all of them. Bundling is what turns persistence into a permission boundary, a secret, and a thing to lock.

Take them apart and each goes somewhere AWS already has. Identity becomes two tags on the resource. Values go in a record store. Effects get a receipt you declare, so the plan shows the migration coming before anything fires.

That is [choudoufu](https://intentius.io/choudoufu/), an OpenTofu fork I have been building.

## No lock to manage

No state file means no lock table to provision, permission, or force open at 3am.

Concurrent runs settle at the API instead. Two creates of the same named resource resolve on the cloud's uniqueness constraint, and the loser re-plans clean.

## One ABAC policy for every team

Ownership is a tag derived from the configuration address, so IAM can read it.

```json
"Condition": {
  "StringEquals": {
    "aws:ResourceTag/tofu-estate": "${aws:PrincipalTag/team}"
  }
}
```

One policy covers every team, and onboarding is a session tag rather than a new policy. The same shape takes `aws:CurrentTime` for a change window, or `aws:MultiFactorAuthPresent` to touch production.

You could always write conditions like that. What you could not do is trust the tag. `default_tags` misses types that take none and modules that override them, nothing checks it, and stock OpenTofu never reads tags back anyway.

## Where it actually is

Experimental, AWS only, and per-resource scoping reaches only the services that honour the condition key.

26 of 145 real third-party configurations pass the offline check today. That number leads the front page, rendered from a committed test artifact.

---

## Read more

- [choudoufu](https://intentius.io/choudoufu/)
- [The revolving door of authoritative state](https://lex00.github.io/posts/the-revolving-door-of-authoritative-state/)
- [Queryable infrastructure](https://lex00.github.io/posts/queryable-infrastructure/)
- [Governance is load-bearing](https://lex00.github.io/posts/governance-is-load-bearing/)
- [Fix Terraform](https://lex00.github.io/posts/fix-terraform/)
