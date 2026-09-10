---
title: "Infra tooling expectations in 2026"
date: 2026-09-09
draft: false
---

{{< inline-svg src="expectations-hero.svg" alt="chant and choudoufu are two independent tools. chant takes typed source across many platforms; choudoufu is an OpenTofu fork for AWS. Either or both feed your git forge, on GitHub, GitLab or Forgejo, where the pipeline is generated and the gate lives in git. From there the estate is applied, and every resource in your cloud carries an owner tag. Your IAM gates on that tag, including calls made from the CLI or console that never went through the tool. behold sits alongside, reading the whole estate as a read-only graph." >}}

Infra tooling should ship with CI/CD and a control plane. It should work with the git forge you already have and run on your own infra.

Paid offerings reduce to glorified gates that rely on a third-party permission structure. Anything with IAM credentials goes right around them.

Your IAM can already gate on a tag. It cannot gate on a Terraform state file.

So [chant](https://intentius.io/chant/) and [choudoufu](https://intentius.io/choudoufu/) keep ownership on the resource, where your IAM enforces it.

## What shipping with CI/CD looks like

choudoufu ships five Ops over one live root. GitHub, Forgejo and GitLab pipelines are generated from them and checked in.

{{< figure src="/img/expectations-ops.svg" alt="The five Ops that make up a choudoufu estate's CI, generated for GitHub, Forgejo and GitLab. live-check runs on a pull request and may do nothing at all: no cloud call, no state, no credential. live-plan runs on a pull request and may read the live system and post the plan. live-adopt runs on a push to staging and may write two tags per adoptable resource, after an approval. live-apply runs on a push to main and may change the estate, after an approval. live-discover runs on cron and may read the account and open an issue." >}}

Three are read-only. The two that write sit on a push trigger and stop at a gate first. The Op names are the job names, so branch protection can require them.

None of it is hosted by me. The gates are facts in git, so an outage cannot lose them. Neither can walking away.

A local smoke proves all five, gate included. End-to-end runs exist for GitLab only.

## What to expect from a control plane

You should get to look at the estate. The question is where it runs.

[behold](https://github.com/INTENTIUS/behold) reads the whole estate as one graph colored by drift. `npx @intentius/behold demo` puts it on `localhost:4600` with no cloud account. Against a real estate it wants read credentials and nothing else. Every write leaves through a gated chant Op.

Meeting that bar costs nothing. All of it is open source and runs on a laptop. With no tenancy and no seat, nobody has a lever to pull later.

## Introducing choudoufu and chant

[choudoufu](https://intentius.io/choudoufu/) is an OpenTofu fork, AWS only. Each resource carries its identity as two tags, so the state file becomes a cache you are allowed to lose.

[chant](https://intentius.io/chant/) is a TypeScript infra toolchain that splits synthesis from execution and keeps ownership on the resource.

{{< figure src="/img/expectations-claims.svg" alt="The 2026 pitch answered for choudoufu and chant. One governed run across Terraform, Ansible and Helm is out of scope for choudoufu, and chant's Ops span seventeen lexicons. On approving every change first, choudoufu re-plans and exits 3 on drift, and chant's gate is a fact in git. On nothing running off-plan, choudoufu holds against drift and chant does not hold against an edited root. On scale, choudoufu has 745 resources against real AWS at call parity and chant only a synthetic bench to 200. On brownfield adoption, choudoufu uses live-adopt behind a gate and chant uses carve one resource at a time. On cost allocation, choudoufu writes the marker on create and chant does nothing. On seeing the whole estate, choudoufu is what behold reads and chant is the graph behold renders." >}}

Cost is worth pressing on, though not as a feature anyone should ship. Most orgs solved this years ago with allocation tags. What breaks it is unreliable tags.

## The question to ask

Ask a vendor what stops someone using the CLI.

Then ask where ownership is written, and whether IAM can read it there.

---

## Read more

- [The intoxicating mix of synthesis and execution](/posts/the-intoxicating-mix-of-synthesis-and-execution/)
- [Invisible ownership is ridiculous](/posts/invisible-ownership-is-ridiculous/)
- [Honor the lower layer](/posts/honor-the-lower-layer/)
- [Governance for GitHub, GitLab and Forgejo](/posts/governance-for-github-gitlab-and-forgejo/)
- [choudoufu](https://intentius.io/choudoufu/) · [chant](https://intentius.io/chant/) · [behold](https://github.com/INTENTIUS/behold)
