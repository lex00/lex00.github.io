---
title: "Terraform state has three pieces"
date: 2026-08-19
featured_image: "img/three-pieces-cover.svg"
draft: false
---

Terraform's state file does three jobs: it says which live resource an address refers to, it holds values the cloud has nowhere to put, and it records that an effect happened. One file ended up doing all three, so everything it persists sits behind a single permission boundary and a single lock.

Separated, each job fits somewhere AWS already provides. Identity is two tags on the resource. Values go in a record store, which holds secrets and is guarded like one. An effect gets a receipt you declare, so the plan shows a migration coming before anything fires.

I have been building this as [choudoufu](https://intentius.io/choudoufu/), an OpenTofu fork.

Choudoufu is stinky tofu. It's famous for a strong flavor that is an acquired taste. It's fermented, and I think it's a great name for an OpenTofu fork that lets your state go stale.

## No lock to manage

The state file is now a cache on the machine that ran, so there is no lock table to provision or force open. Concurrent runs are settled by the cloud and the record store. Two creates of the same named resource resolve on the cloud's uniqueness constraint. A record write lands only if nobody changed that record first, and the loser re-plans clean.

## One ABAC policy for every team

Ownership is a tag derived from the configuration address, so IAM can read it.

```json
"Condition": {
  "StringEquals": {
    "aws:ResourceTag/tofu-estate": "${aws:PrincipalTag/team}"
  }
}
```

One policy covers every team, and onboarding a team means adding a session tag. The same shape takes `aws:CurrentTime` for a change window, or `aws:MultiFactorAuthPresent` to touch production.

IAM conditions like that have always been possible, but the tag could not be trusted. `default_tags` misses types that take none and modules that override them, nothing checks it, and stock OpenTofu never reads tags back.

Because a plan reads the markers live, handing an estate to another team is a policy change, and a rename is a tag rewrite.

---

## Read more

- [choudoufu](https://intentius.io/choudoufu/)
- [Queryable infrastructure](https://lex00.github.io/posts/queryable-infrastructure/)
