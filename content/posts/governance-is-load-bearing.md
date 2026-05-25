---
title: "Governance is load-bearing in IaC"
date: 2026-05-25
---

State is load-bearing. Anyone who has run infrastructure past a toy project knows this. I take the phrase from [William Collins](https://wcollins.io/posts/2026/ai-through-iac-not-instead-of-it/), who makes the case for AI through IaC rather than instead of it, and I agree with most of it. The argument I want to make is narrower. Load-bearing is not the same as authoritative. Almost everything you value about state lives on the load-bearing side, not the authoritative side.

## What the file actually costs

Start with what a state file charges you. A global mutex on every apply. An all-or-nothing changeset. Secrets sitting in the file because the tool needs them to diff. A corruption surface that can take a stack down. None of that is the language. None of it is the providers. It is a flat file doing the work of a database, and the database has no tooling.

But notice what those costs actually are. They are the costs of hosting the file yourself. That is a Terraform and Pulumi problem, not a property of authoritative state. Once you see that, the field sorts into a spectrum.

## The spectrum of who babysits the file

Self-hosted state. You run the backend. You own the lock, the backups, and the corruption risk. Maximum control and maximum operational burden.

A third-party SaaS managing state. This one is not really a file. It is a queryable database, sometimes the real-time graph people picture state becoming. The vendor hosts and operates it, so the operational burden goes away. In its place you take a vendor dependency, and your state and often your secrets now live in someone else's system. The model has not changed. A faster, better-indexed source of truth is still a source of truth, and it still has to be correct and current.

The platform managing state. CloudFormation and CDK are authoritative state too, but AWS hosts the file as part of the service. No backend to run, no lock to manage, no file to corrupt. You keep cloud lock-in and all-or-nothing applies. Here the file costs almost nothing to operate.

No authoritative state. This is where chant sits. There is no file to host, outsource, or trust. State is observational. A snapshot records what was seen, and it is allowed to be stale.

Every step except the last keeps authoritative state and only moves who babysits the file. The whole market is an argument about who should host the thing. chant asks a different question. What if you do not need to host it at all.

## Separate the need from the mechanism

The things you cannot give up are governance. A known changeset before apply. A lock so two operators do not collide. An audit trail you can read later. Blast-radius limits so one change cannot touch everything.

Authoritative state is one mechanism that delivers those. It is not the only one. When someone says state is load-bearing they are usually pointing at the governance and crediting the mechanism. The governance is load-bearing. The authoritative state is a way to get it.

## A real example, not hyperscale

Picture an engineer who is not at hyperscale. They manage many clients. Some estates are small. A few are large. Some clients are fine with an observational model. Some feel they require authoritative state.

This is the common case, and the objections show up here in their real shape.

## The client who feels they require it

Take that client at face value. They are not wrong to have a requirement. The question is what the requirement buys them. Almost always it is one of the governance properties. A precise plan before a regulated change window. A lock because several people touch the estate. An audit trail. Name the property out loud. Then ask whether the property needs authoritative state or whether that was just the first tool that offered it.

Often it does not need it. Sometimes it does. And when a client already runs CloudFormation or CDK, there is nothing to argue about. chant emits CloudFormation. They apply it the way they always have. AWS keeps the authoritative state. chant is the authoring and pre-apply layer underneath, and the two sit together with no conflict.

The boundary is Terraform. chant does not emit HCL. So a Terraform shop does not get a drop-in. chant owns a slice of infrastructure end to end and runs beside Terraform rather than retrofitting into its state. And "we require authoritative state" most often means a Terraform shop, which is exactly where the easy coexistence story does not hold.

## A diff, not a plan

[chant](https://intentius.github.io/chant/) gives you a diff, not a plan.

There are two modes. The default is offline. It builds the project, fingerprints the declarations, and compares against the last snapshot. Fast feedback on what you changed. The other mode queries the cloud and compares the live result against both the last snapshot and the current build. That one catches the change someone made by hand.

The diff is informational. chant does not apply it. What to do about it is the orchestration's decision. A cron, an agent, a human, a workflow engine. The client who is fine with the observational model wires the diff to automation. The client who wants a strict gate wires the same artifact into their own approval flow. chant does not force either, because it does not own the apply. For the engineer with many clients that is the point. One way to author. Many ways to govern.

## But at scale even the blast radius is too big

The reflex objection is that a large change touches so many resources that verifying its blast radius is just reading the whole estate again.

It does not hold. Blast radius scales with the change, not the estate. A one-subnet change touches one subnet and its dependents whether the account has a hundred resources or a hundred thousand. The read is bounded by the write you already accepted. Reading that scope first is strictly less work than writing it. And you do not discover the radius by scanning the cloud. You compute it from the dependency graph against the last snapshot, then verify only that closure.

There is one case where the radius really does approach the whole estate. Rotating a root credential. Re-tagging everything. That is not a counterexample. A change whose blast radius is the entire estate is the exact change a human or a policy should gate. The observational model surfaces it. The authoritative model makes the same giant apply frictionless, which is the danger. A radius that large is a signal to decompose or stage the change. It is not a cost to optimize away.

## Where truth lives

Put truth where it belongs. The live system is the source of truth. The snapshot is a baseline for the diff, and it is allowed to be stale, because a stale baseline is inconvenient and a stale source of truth is dangerous.

The file was never the load-bearing part. The governance around it was. Keep the governance and the authoritative file becomes a choice rather than a requirement.
