---
title: "The gap closes faster this time"
date: 2026-07-22
draft: true
---

One of the bets ConfigHub is placing is on [estate search](https://confighub.com/blog/querying-kubernetes-fleets-like-a-database-with-confighubs-where-data-a6ffaaa360a1): query your whole fleet like a database, find every config that matches a predicate, change them together. It is a real pain and they are early to name it. The bet I would not place is that this stays a gap long enough to build on.

The reason people assume it will is 2014. When Terraform arrived, the clouds' own authoring was weak, and it stayed weak for years. CloudFormation was hand-written JSON, and AWS CDK did not ship until 2019. That gap held long enough for a wedge to become an estate, which is [the wave I wrote about, and why it is ending](https://lex00.github.io/posts/the-long-road-back-to-native/). The assumption underneath is that the platforms are always slow, so getting out ahead of them is safe.

Estate search is already table stakes.

## Querying your estate is already a commodity

Every major cloud ships estate query as a free, first-party feature, and it backs their own consoles.

- Azure Resource Graph runs KQL across every resource in a tenant, and it powers the portal's search bar.
- AWS Config Advanced Query runs a SQL dialect over resource configuration and relationships, across accounts and regions. It shipped in 2019.
- GCP Cloud Asset Inventory gives you a search language and a BigQuery export you can run arbitrary SQL against.

Off the platforms, [Steampipe](https://steampipe.io/) runs live SQL over cloud APIs for AWS, Azure, GCP, and Kubernetes. CloudQuery syncs your estate into Postgres. Cloud Custodian queries and then acts. Someone who wants to query their fleet like a database can already do it three ways without buying anything.

## AI is taking the last hard part

The one piece of estate search that took skill was writing the query, and that is going away in front of us. Azure Copilot generates Resource Graph KQL from plain English in the portal today. AWS is retiring its purpose-built natural-language-to-SQL feature for Config in January 2026 and folding the job into Amazon Q.

That last move is the tell. When a cloud kills its own query assistant and hands the work to a general agent, text-to-query has stopped being a product and become a capability every tool gets for free. Nobody pays for a nicer WHERE box.

## Be exact about what is left

Not all of it is solved, and the open part is worth naming precisely. Everything above queries live state, the resources as they actually run. The slice still open is the desired config: the rendered manifests and templates before they apply, queried across a fleet, and changed in bulk from the same predicate. That is the bet ConfigHub is really making, and it is a genuine one. Selecting declared units by a predicate, patching them, applying, and reconciling drift, all from one store, is a combination no incumbent bundles today.

Two things keep it from being a moat. The query half is not new, because Steampipe already runs SQL over rendered Helm and manifests. And every other piece already lives in a neighbor: live query in the clouds, query-then-change in Custodian, desired state and drift in GitOps. What ConfigHub holds is the integration, and an integration lead runs on a clock, especially when the platforms own the query surface and the AI sitting on top of it.

## The durable question was never search

The question was never whether you can query your estate. It is whether you have to keep a store to do it.

[chant](https://intentius.io/chant/) compiles your source to the platform's native spec and hands back the rendered artifact. That artifact is data, the CloudFormation or the Kubernetes object itself, and it is the same every build. Point Steampipe at it, sync it into a warehouse, index it the way your team already indexes things. You get search over your desired config with tools people already run, and you never stood up a database to get it.

That chant ships no query language is not a gap in it. It is the same call as keeping no state file. [A database is something you add at scale as an index, never a dependency](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/). Building a search product on a surface the platforms are busy commoditizing is the opposite call.

The clouds will close the search gap fast this time, faster than they closed authoring, because most of it is already closed and AI is taking the rest. What lasts is the artifact you can hand to the tools your team already runs, with no store underneath.

---

## Read more

- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [The long road back to cloud native](https://lex00.github.io/posts/the-long-road-back-to-native/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [chant](https://intentius.io/chant/)
