---
title: "Infrastructure change coordination"
date: 2026-11-17
draft: false
featured_image: "img/infrastructure-change-coordination-hero.svg"
---

Coordinating applies comes down to ownership and boundaries, and the way you implement them shapes every operation that follows.

Terraform and Pulumi draw a boundary with a backend. Each backend carries one lock, so the lock sets where an estate ends, and every new boundary means another backend to run.

[choudoufu](https://intentius.io/choudoufu/) for OpenTofu and [plunge](https://intentius.io/plunge/) for Pulumi draw boundaries with labels on the resources. One backend holds a record and a lock per resource, and [chant](https://intentius.io/chant/) runs both kinds of root in one workspace.

Five everyday operations show the difference. In each picture the top half has a backend per boundary and the bottom half has boundaries by label.

## Two changes to one resource

A backend lock keeps the state file consistent. A reviewed plan catches two people changing the same resource, in either model.

![Run 1 sets the database to 2 CPU and run 2 sets it to 4 CPU. With a backend per boundary, run 2 waits for the lock and then overwrites. With boundaries by label, both write at once and the last write stands. Both end at 4 CPU, and a reviewed plan catches the conflict](/img/infrastructure-change-coordination-1.png)

The queue on top buys file integrity. Coordinating people is the job of review, in both models.

## Two applies at once

A lock per backend makes runs in one estate take turns. A lock per resource lets runs on different resources go together.

![Run 1 holds the edge backend's lock and run 2 waits for it. With a lock per resource, runs 1 and 2 write the DNS record and the certificate together](/img/infrastructure-change-coordination-2.png)

## Moving a resource to another estate

Handing a resource to another owner means moving its state between backends, or editing one label.

![With a backend per boundary: lock both backends, move the state, move the code. With boundaries by label: edit the label, and the edge estate takes the firewall in](/img/infrastructure-change-coordination-3.png)

## An apply killed part way

A run that dies holds its backend's lock until someone clears it. With a lock per resource, the next run starts straight away.

![With a backend per boundary: find the held lock, clear the lock, run again. With boundaries by label: run again](/img/infrastructure-change-coordination-4.png)

## Starting a new estate

Under a backend per boundary, a new estate brings a new backend. Under labels, it joins the backend you already run.

![With a backend per boundary: create a backend, configure its lock, add the root. With boundaries by label: add the root](/img/infrastructure-change-coordination-5.png)

The same cards, with comparison tables for each fork, are at [intentius.io/compare/coordinating-changes](https://intentius.io/compare/coordinating-changes/).

## Read more

- [terragucci](https://intentius.io/terragucci/): plans and approvals from pull requests for Terraform, OpenTofu and Terragrunt, in your own CI, with choudoufu as an engine
- [plywood](https://intentius.io/plywood/): the same for Pulumi, with plunge as its engine
- [Resource-level concurrency for Terraform](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/)
- [Solving the stress of infrastructure inheritance](https://lex00.github.io/posts/solving-the-stress-of-infrastructure-inheritance/)
- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [choudoufu runs on OpenTofu's new runtime](https://lex00.github.io/posts/adding-estate-boundaries-to-opentofus-new-runtime/)
