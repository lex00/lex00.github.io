---
title: "An entire industry exists to fix Terraform"
date: 2026-07-21
draft: false
---

This is what an industry of coping mechanisms looks like. One attempt to leave Terraform's model outright, [Winglang](https://www.winglang.io/), compiled a new language down to Terraform and shut down in 2025. When Terraform's own license changed, the community forked the whole thing rather than let it go. The tool is too entrenched to abandon, so the market lines up to patch it.

{{< inline-svg src="industry-matrix.svg" alt="A matrix of the tools built around Terraform, with a column for whether each keeps its own state store. The fix industry: Terragrunt wraps it, TerraConstructs puts a typed object model over it, Atlantis and Spacelift and env0 run it for you, Terraform Cloud hosts the store and gives you apply, Stategraph keeps state as a dependency graph, compliance.tf adds guardrails on the modules. Every one keeps its own store, yes. Set apart, not in the industry: chant, which drives no raw API and reads the substrate, so it keeps no store of its own. State's real job is to bind the name you wrote to the id the provider hands back; Terraform drives a raw API, catches that id, and makes you keep the pair, while chant compiles to the substrate's own spec, which keeps the binding itself." >}}

The last column is the whole story. State's real job is to bind the name you wrote, `MyResource`, to the opaque id the provider hands back, so the next run knows the two are the same thing. Terraform drives a raw API, catches that id, and makes you hold on to it. chant drives no raw API. It compiles to the platform's own spec, which keeps the binding itself, so there is no pair to store.

## The theme is state

The file Terraform keeps has to be hosted, locked so two applies do not corrupt it, and reconciled with a reality that drifts. Every one of those is a gap, and at every gap someone built a product. Remote backends, locking services, state surgery tools, drift detection, a real database to hold it all. It is not the binding of state that seeded this market, but rather the storage requirement.

## A fix that needs the problem

A tool that sells you a better store needs the store to stay two things at once: bad enough that you will pay to fix it, and permanent enough that you cannot just drop it.

State is corruption, locking, drift, the whole horror show, which is the fear that sells the fix. When someone proposes dropping the store instead of improving it, the same pain gets waved off as solvable, not worth the fight. 

The severity moves with the argument because the business underneath needs the store to be a problem and a fixture in the same breath.

## chant keeps no store

chant reads the binding where it already lives. It does not create a resource and catch an id it then has to remember. chant compiles to the platform's own spec and hands it over. There is no pair to record, so there is nothing to host or lock behind it.

This is the same move as [honoring the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/). Among the tools here it makes chant the only spec-native one. The fair objection is CDK which also compiles to a cloud's own spec rather than wrapping it. But CDK requires execution, and it speaks a single cloud.

That does not make chant a replacement for the whole industry. It removes one need where most infrastructure lives. What goes away is the state store and everything built to make it bearable.

## The measure of a problem

You can size a problem by how many companies exist to soften it. Storing state yourself has produced a lot of them. Fork the license, wrap the CLI, host the store, graph the store, or leave the model behind, all of it follows from driving a raw API and catching the id yourself.

The cheapest state store is the one you never have to keep.

---

## Read more

- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [Governance without the state file](https://lex00.github.io/posts/governance-without-the-state-file/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [chant](https://intentius.io/chant/)

Tools mentioned: [Terragrunt](https://terragrunt.gruntwork.io/) · [TerraConstructs](https://terraconstructs.dev/) · [Atlantis](https://www.runatlantis.io/) · [Spacelift](https://spacelift.io/) · [env0](https://www.env0.com/) · [Terraform Cloud](https://www.hashicorp.com/products/terraform) · [Stategraph](https://stategraph.com/) · [compliance.tf](https://compliance.tf/) · [Winglang](https://www.winglang.io/)
