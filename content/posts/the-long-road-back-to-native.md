---
title: "The long road back to cloud native"
date: 2026-07-22
draft: false
featured_image: "img/the-long-road-cover.svg"
---

The sensible answer about Terraform and AI goes like this: the agent writes the HCL, and Terraform keeps the parts that matter, governance and lifecycle. [William Collins](https://wcollins.io/posts/2026/ai-through-iac-not-instead-of-it/) makes that case well, and I agree with more of it than you might expect. That case rests on one thing: the value it credits to Terraform lives in the tool itself.

Look at what Terraform is, underneath. It takes your cloud's native spec, the CloudFormation template or the Kubernetes object the platform already defines, and reimplements it as HCL plus a state file. It is a layer over the platform's own API, one that [stands in for the native spec instead of compiling to it](https://lex00.github.io/posts/honor-the-lower-layer/). For a while that was a fine trade.

## The layer was worth it once

Terraform shipped in July 2014. Consider what platform-native authoring was that year. CloudFormation was hand-written JSON. AWS CDK would not exist for 5 years. Kubernetes reached 1.0 in 2015. cdk8s and Bicep are 2020. For a few years there was a real vacuum, and Terraform filled it well, one language across clouds when every platform's own authoring was absent or miserable. The layer had value, because what sat underneath was not yet pleasant to write.

That has changed. Against CDK, cdk8s, and a mature Kubernetes API, HCL does not win on merit in 2026. It wins because your estate is already inside it. The layer that was once a convenience is now mostly the reason your infrastructure cannot move.

## The value people credit is not in the tool

Set syntax aside, as everyone now does, and the case for keeping Terraform rests on the governance engine: state tracking, plan/apply, provider abstractions, declarative reconciliation. Be exact about those. State tracking is a ledger. Plan/apply is a diff and an executor. Provider abstraction is an API client. Declarative reconciliation is a control loop. None of them is governance. Governance is policy, approval, who may change what, an audit trail, a cap on blast radius.

So where does Terraform do those? Download it and run it. All the CLI gives you for governance is four per-resource validation blocks, `terraform validate`, `terraform fmt`, a `plan` you run by hand to catch drift, and a `yes/no` prompt before apply with no reviewer behind it. No policy engine, no roles, no approval gate tied to identity, no audit log, no continuous drift detection. Everything people mean by Terraform governance is a second product.

{{< inline-svg src="governance-is-a-separate-product.svg" alt="Two columns. Left, the free Terraform CLI, holding only four validation blocks, validate and fmt, a manual plan for drift, and a yes/no prompt. Right, HCP Terraform, the paid platform priced per resource per month, holding Sentinel, OPA, tfpolicy, RBAC and teams, approval gates, continuous drift detection, private module registry, and audit logs. Every engine enforces on the paid platform, not in the free CLI." >}}

Sentinel, the flagship policy engine, is proprietary, closed source, and written in a dynamically typed language you use nowhere else. It runs inside HCP Terraform, the paid platform, billed per managed resource. OPA fills the same slot with a different language on the same platform. RBAC, approval gates, the private module registry, continuous drift detection, audit logs: every one is the paid platform.

The other half of governance is not Terraform at all. The pull request, the review, the approval, the record of who changed what, that is GitOps, and GitOps does not care which tool sits inside it. Governance splits in two. The part that is already yours, the version control and CI wrapped around any tool. And the part you rent, a platform holding your credentials and checking policy late in the run. Neither half is the tool everyone downloads.

## chant takes the layer off

[chant](https://intentius.io/chant/) does the opposite of standing in for the spec. It compiles a real language, a constrained subset of TypeScript, straight to the platform's own format, and hands that format back exactly as the platform defines it. No HCL in the middle. No state file to host. No proprietary policy language. No platform between you and your cloud. The check that gates a change is typed policy over the resource graph, runs in your build offline, and presents as a red squiggle in the editor before anything is planned. 

The shift-left instinct is exactly right: validate a static artifact before it touches the cloud. chant just puts that artifact one step earlier than a plan, at the keystroke instead of the run.

What you keep is the native spec and nothing on top of it. Your cloud's own format, authored in a language you already write, checkable at your desk.

## The exodus will be slow

An estate that took years to build in HCL takes time to lift back out, slice by slice, and every slice has to be sequenced, verified, and governed while the old and the new run side by side. If you keep infrastructure running today, it is more work for you, for a long time. The installed base is enormous, enough that when the license changed the community forked the whole tool rather than lose it, and a base that large moves on its own schedule and no one else's.

The migration itself is a lifecycle problem. Sequencing it, gating it, holding blast radius down while two systems overlap, that is the discipline infrastructure genuinely needs, and AI does not remove the need for it. What AI lowers is the cost of each individual lift. The judgment that runs the transition safely stays human, stays valuable, and for years is in higher demand.

## What was stuck, and what frees it

If HCL is held up by an estate too expensive to move, the only question is what makes moving cheaper. Getting a slice out of Terraform has always meant a person reverse-engineering it back into native form, resource by resource. That labor is a moat. It is why every challenger that tried to win on the language lost. Pulumi and the rest bounced off it. Winglang compiled down to Terraform because it could not escape the model, and [shut down in 2025](https://lex00.github.io/posts/fix-terraform/) anyway. None of them drained the moat, because the moat is not the language.

This goes both ways. The tooling that writes infrastructure from a description also runs in reverse. Point it at a live estate slice and it carves that slice out into typed source, emits the native spec, and holds the two faithful with roundtrip tests. chant already does this for [a live cloud or an existing template](https://lex00.github.io/posts/honor-the-lower-layer/), and a [carve-out from a Terraform estate](https://intentius.io/chant/tutorials/terraform-carve-out/) is the same move aimed at the corners no one has had time to move. The reverse-engineering that looks like weeks now begins to look like a build step.

## Back to native

Terraform is not going away this year, or the year after. It is held up by an estate that was expensive to move and a wave it caught when the alternatives were weak, and for a long time those were reason enough to stay. 

What changes now is the cost of leaving. As that cost falls, the layer shows itself for what it is, a place your infrastructure is parked rather than the ground it stands on, and the native spec underneath comes back within reach.

None of it is fast. The layers come off one slice at a time, over years, and the ground under them was your cloud's own spec all along.

---

## Read more

- [Governance is what IaC depends on](https://lex00.github.io/posts/governance-is-load-bearing/)
- [Policy belongs left of the platform](https://lex00.github.io/posts/policy-belongs-left-of-the-platform/)
- [An entire industry exists to fix Terraform](https://lex00.github.io/posts/fix-terraform/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Carve a Terraform estate into chant](https://intentius.io/chant/tutorials/terraform-carve-out/) — the migration, step by step
- [AI through IaC, not instead of it](https://wcollins.io/posts/2026/ai-through-iac-not-instead-of-it/) · [chant](https://intentius.io/chant/)
