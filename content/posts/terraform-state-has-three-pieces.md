---
title: "Terraform state has three pieces"
date: 2026-08-19
featured_image: "img/three-pieces-cover.svg"
draft: false
---

A state file does three unrelated jobs.

It says which live resource an address refers to. It holds values the cloud has nowhere to put. And it records that an effect happened.

Those three got bundled because one file happened to do all of them. Bundling is what turns persistence into a permission boundary, a secret, and a thing to lock.

Take them apart and each one goes somewhere AWS already has. Identity becomes two tags on the resource. Values go in a record store backed by Parameter Store or S3. Effects get a receipt, which is an ordinary resource you declare, so the plan shows the migration coming before anything fires.

That is [choudoufu](https://intentius.io/choudoufu/), an OpenTofu fork I have been building.

## The part that surprised me

You can already scope IAM with tags. Tag your resources, condition a policy on `aws:ResourceTag`, done. AWS has had this the whole time and choudoufu adds nothing to it.

So for a while I could not answer what the fork was actually for.

The answer is that a tag you apply is a convention. `default_tags` gets it onto most things, until a module overrides `tags`, or a type takes none, or someone edits one by hand. Nothing checks it. Strip a tag and IAM stops guarding a resource that Terraform still owns, and your permission boundary has quietly drifted from your management boundary.

A marker is derived from the configuration address. The tag *is* the ownership, so the two cannot disagree.

And stock OpenTofu never reads tags back anyway. They are decoration to it. It still needs the state file, so tagging your resources leaves the bucket policy, the lock table, and a file holding every attribute value sitting outside the IAM you just scoped.

## What that buys

Once ownership lives on the resource, every IAM feature that works on resources works on your infrastructure.

Deny a staging role on anything belonging to another estate, and pointing the wrong config at production fails at the cloud instead of at review. Match `aws:PrincipalTag/team` against the resource's estate tag and one ABAC policy covers every team, where onboarding costs a session tag rather than a new policy. Deny creates carrying no estate tag with an SCP and ownership becomes a precondition of existing, which turns tag compliance from a scanner chase into a guarantee.

There is also no lock. Concurrent runs settle at the API, so nothing gets stuck and nothing needs forcing open.

## Where it actually is

Experimental, AWS only, and the reach of per-resource scoping depends on which services honour the condition key, which is fewer than you would like.

26 of 145 real third-party configurations pass the offline check today. That number leads the front page, rendered from a committed test artifact rather than typed by hand, because a coverage claim nobody can reproduce is worth nothing.

---

## Read more

- [choudoufu](https://intentius.io/choudoufu/)
- [The revolving door of authoritative state](https://lex00.github.io/posts/the-revolving-door-of-authoritative-state/)
- [Queryable infrastructure](https://lex00.github.io/posts/queryable-infrastructure/)
- [Governance is load-bearing](https://lex00.github.io/posts/governance-is-load-bearing/)
- [Fix Terraform](https://lex00.github.io/posts/fix-terraform/)
