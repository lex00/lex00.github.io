---
title: "Your infra database is a road to hell"
date: 2026-07-17
---

The authoritative model Terraform made famous has always been a poor fit for teams just trying to automate a little infra. The state file is only its most visible cost. Give up the model and three questions decide the tool: how the truth is represented, where it lives, and what lifecycle runs around it. [ConfigHub](https://confighub.com/) and [formae](https://github.com/platform-engineering-labs/formae) are already past it, and [chant](https://intentius.github.io/chant/) answers the same three again.

- **Representation.** ConfigHub makes the truth data in a store. formae makes it Pkl. chant makes it typed TypeScript that is the spec itself.
- **Location.** ConfigHub puts the truth in a database. formae pushes it into the source code and reconciles the cloud back to it. chant leaves it in the live system, where it already is.
- **Lifecycle.** ConfigHub builds one around its store. formae builds one that pulls reality into code. chant hands the lifecycle to you, dialed per environment.
- **Ownership.** Here ConfigHub slips: like Terraform, it derives ownership from state, so absence from the store authorizes the delete.
- **Verdict.** Three tools past the authoritative model, and one that also refuses to own you: typed source you already write, truth left live, artifacts that outlive the tool.

{{< inline-svg src="where-truth-lives.svg" alt="Three panels showing where each tool keeps the truth. ConfigHub in a database, formae in the source code with a reconcile loop, chant in the live system as typed TypeScript. Above them, the discarded authoritative model where state, truth, and ownership are one locked box." >}}

## ConfigHub owns all three

ConfigHub replaces the file with a database, and the database is the truth. You author in it through an API. It actuates from it. Brian Grant is right that configuration is data and that Git is a poor place to keep it, and the product follows honestly from that.

The representation is where it overshot. Configuration is still written by developers, and it is already hard enough with abstractions stacked on everything. Moving it into database records adds one more layer between the author and the spec. That is the case for staying spec-native: the thing you write should be the thing that ships.

And look at what you signed. The store is your authoring surface, your source of truth, and your control plane at once. Three kinds of lock-in wearing one login.

## Ownership is not state

Every deploy tool answers two questions: what is true, and what is mine to delete. The defect is deriving the second from the first.

Terraform reads ownership off presence in state. In the file, it's yours; drop it, the file authorizes the delete. I've made this case about Terraform before.

ConfigHub does the same by design, and builds its whole lifecycle on it. The store is the truth, so absence from it authorizes the delete, and the entire actuate-and-reconcile loop runs on that identity. Server-side apply tracks field ownership live, which helps, but never decides whether a resource should exist. That call comes from the store.

It never had to. Ownership can be its own fact: a marker on the live resource, read directly, independent of any record of truth. chant deletes only what is owned and undeclared, two signals agreeing. ConfigHub built a product on a conflation that did not need to exist.

{{< inline-svg src="ownership-conflation.svg" alt="Two models compared. Conflated: a single band where in-the-record equals true equals owned equals deletable. Separated: two overlapping bands, Declared and Owned, where a delete happens only in the owned-and-undeclared sliver." >}}

ConfigHub is Terraform's conflation with a query planner.

## formae gets the truth right, and the wrong language

formae drops the file and keeps the source code as the truth. It reconciles out-of-band changes back into code instead of fighting them. On the calls that matter, formae and chant agree, and the inversion of truth to source is a fine choice.

Then it hands you Pkl. Pkl is a real config language, typed and deterministic, but it is not better than TypeScript. It just looks less like JavaScript. Its one edge is value constraints in the type: a port that refuses anything outside 1 to 65535 before you can save. chant answers that in semantic lint, and the lint reaches farther than Pkl's constraints do, because it checks meaning across resources, not bounds on a single field.

## Both of them require a database

Vendors love to indict Terraform state as a database crammed into a flat file, then sell you a real one as the cure. The cure is the disease.

ConfigHub keeps the truth in a database. formae requires one too. Either way you are running a server before your first resource ships.

The truth already exists in the live system. A second copy you must keep correct and current is the state file's burden again, in nicer clothes. chant needs none of it. State, when there is any, lives in git, and a database is something you add at scale as an index, never a dependency.

{{< inline-svg src="database-smell.svg" alt="A required store and the live system linked by a reconcile arrow with a caution marker, labeled two truths to keep in sync. Beside it, chant with one truth in the live system, git for history, and a database added only at scale as an index." >}}

## TypeScript is the spec with types on it

A JSON document is almost already a TypeScript object. Same nesting, same values, the keys just lose their quotes. chant leans all the way in. `BucketEncryption` in your file is `BucketEncryption` in the template. What you author is what ships, with no second language pointed at the spec and no store between you and it.

And you are about to hand this to agents. They write TypeScript fluently and Pkl by guessing. When the machine authors the source, you want the surface it already speaks.

{{< inline-svg src="three-approaches-matrix.svg" alt="A comparison matrix. Rows for representation, location, lifecycle, and ownership across ConfigHub, formae, and chant, with the chant column highlighted. Terraform and Pulumi kept the authoritative model and are not in the comparison." >}}

## chant owns none of you

Score the three questions. Truth stays in the live system, not a store chant hosts. The lifecycle is yours: hand the native artifact to your pipeline, or run chant's own durable Ops, dialed per environment from observe to apply. The authoring surface is TypeScript you already write, and the output keeps working the day you stop using chant.

ConfigHub owns the truth and the lifecycle. formae owns the lifecycle and a language you had to learn first. chant owns none of it. That is the case, and it is why chant is better.
