---
title: "Governance for GitHub, GitLab, and Forgejo"
date: 2026-09-01
featured_image: "img/governance-wardens-cover.svg"
tags: ["governance", "wardens"]
draft: false
---

Getting all your forge settings and repo configs aligned can take some effort.
  
The forge wardens are here to help you:
   - [github-warden](https://intentius.io/github-warden/)
   - [gitlab-warden](https://intentius.io/gitlab-warden/)
   - [forgejo-warden](https://intentius.io/forgejo-warden/)

## One policy file

Each warden is driven by a single YAML policy. 

Anything you don't declare is never read, diffed or touched, and nothing gets deleted unless you meant it.

## A collection of pipelines

That one policy drives every pipeline. 

A pull request gets the plan, a merge gets the apply, and the audit runs overnight.

## Audit comes standard

All three integrate [chant](https://intentius.io/chant/)'s audit engine. 

This sweeps your managed repos for security and correctness posture, and `report` prints a compliance snapshot as JSON you can commit. The snapshot is perfect for auditors.

## Chant under the hood

The wardens all sit on [chant reconcile](https://intentius.io/chant/guide/reconciling-lifecycle/), a provider-agnostic reconcile core. 

Each warden adds the client and the cycles for its own forge, giving all 3 consistent behavior.

## Where they differ

{{< figure src="/img/governance-wardens-table.svg" alt="Coverage table for the three wardens. All three manage org and repo settings, membership, branch rules, secrets and variables, and repo provisioning. gitlab-warden and forgejo-warden manage webhooks. github-warden adds GHAS security features, environments, fine-grained PAT governance, and Dependabot hygiene. gitlab-warden adds security policies and compliance frameworks, protected environments, access and deploy tokens, MR approval settings, and instance settings on self-managed. Auth is a token or GitHub App, a PAT, or a plain token. Hosts are github.com, GitLab SaaS or self-managed, and any Forgejo instance." >}}

Every row is driven by the same policy file and checked by the same audit.

All you need is an API token and about ten minutes to see a dry-run in your forge.

---

## Read more

- [github-warden](https://intentius.io/github-warden/)
- [gitlab-warden](https://intentius.io/gitlab-warden/)
- [forgejo-warden](https://intentius.io/forgejo-warden/)
- [chant](https://intentius.io/chant/)
- [Invisible ownership is ridiculous](https://lex00.github.io/posts/invisible-ownership-is-ridiculous/)
