---
title: "Terraform state at scale the easy way"
date: 2026-09-06
draft: false
featured_image: "img/state-easy-way-cover.svg"
---

An RDBMS might seem like a cost effective way to centralize your Terraform state.

The better choice is the "live" backend. It answers the same set of concerns much more efficiently.

[choudoufu](https://intentius.io/choudoufu/) ships the live backend with a smoke scenario for each claim it makes.

{{< figure src="/img/state-easy-way-claims.svg" alt="Table of five concerns comparing an RDBMS with the live backend. For global locks the RDBMS only locks runs that use the database, while the live backend has no lock and the cloud rejects the duplicate create. For agent governance the RDBMS only governs agents that go through the server, while the ownership tag is an IAM rule the cloud enforces. For live inventory the RDBMS holds a stored copy that goes stale between runs, while the live backend is one tag query against the cloud. For the audit timeline the RDBMS log expires with no export, while the plan is in git and tag writes are in the cloud audit log. For atomic apply the RDBMS promise is not true because a failed apply leaves resources behind, while tags ride the create call so nothing is lost." >}}

## RDBMS vs Live Backend on pricing

{{< figure src="/img/state-easy-way-cost.svg" alt="Cost table comparing an RDBMS with the live backend. The RDBMS needs a small two-zone database instance at 1,500 to 2,500 dollars a year, storage and backups at 150 to 300 dollars, and 12 hours a year of ops, for a total of 1,650 to 2,800 dollars, 12 hours and a pager. The live backend uses tags and standard parameters at zero dollars, API calls measured at zero on 745 resources, and one IAM policy at 2 hours, for a total of zero dollars, 2 hours and no pager." >}}

I think my numbers above are fair and I welcome challenges to my claims here.

Just imagine operating the left column vs the right.

---

## Read more

- [choudoufu claims, each with a runnable smoke scenario](https://intentius.io/choudoufu/docs/claims/)
- [Terraform state has three pieces](/posts/terraform-state-has-three-pieces/)
- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
