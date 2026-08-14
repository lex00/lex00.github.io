---
title: "Take a whiff of choudoufu"
date: 2026-08-14
featured_image: "img/choudoufu-hero.png"
draft: false
---

Terraform bundles three jobs into state and that model has survived for too long. Ownership, estate boundaries, and effect memory all live in the same artifact, behind the same lock, at the same access level.

This is an extremely convenient workflow for the folks who get to drive it.  It can also make life terribly difficult for operators who are blessed with inheriting the estate as teams are "restructured". Orgs who share a single production account across many teams see the worst of this.  

While OpenTofu gives you Terraform with some new features and a better license, it still carries the same state model. When you have to maintain a separate ownership ledger from the live system, it is a reconciliation burden on migration.

Choudoufu is stinky tofu.  It's famous for having a strong flavor that is an acquired taste. It's fermented and I think it's a great name for an OpenTofu counterpart that allows your state to be stale.

[choudoufu](https://github.com/INTENTIUS/choudoufu) slices the state model into three components:
   - ownership and estate markers - tagged on the resource
   - micro state backend - stores values of logical resources
   - receipts - track the staleness of effects

All three of these jobs are easily serviced by ordinary IAM governance. Together they make estates easy to carve up into smaller domains, shrink your blast radius, and drop the locks you manage.

choudoufu is experimental and AWS only. If the smell doesn't put you off, [intentius.io/choudoufu](https://intentius.io/choudoufu/) is ready for you to try migrating an existing estate or start fresh.
