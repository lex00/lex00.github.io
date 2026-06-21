---
title: "Governance without the state file"
date: 2026-06-20
---

How easily can you prove that all your repositories have aligned configuration according to policy?

Governance is easy when it comes to things people rarely touch. I'll bet a lot of you reading this manually tune your repo settings, and have already thought about how you might make them more consistent.

## Why policy drifts

Platform settings are stateful and the typical case is that nothing reconciles them. You set branch protection once. After that it is a value in a database that any admin can change.

As use cases for new repos proliferate, this problem grows along with them.

Clicking through settings does not scale and Terraform will have you taking on a state file, HCL, and an import for every existing repo.

## A warden

The answer is a reconciliation loop based on a simple YAML file.

It is selective by omission, managing only what you declare. A field you leave out is a field it never reads, diffs, or touches.

Its deletes are ownership-gated. A typo in the config does not become a purge, and a guardrail caps how much one apply can remove, so a mistake stops before it spreads.

There is no state file to host, lock, or corrupt, because the live platform is the source of truth.

The 3 CI wardens share the same [reconcile engine](https://intentius.github.io/chant/) underneath. The interesting part is what changes between them.

## Three platforms

**GitHub.** [github-warden](https://github.com/intentius/github-warden): authenticates as a GitHub App and reconciles rulesets, the security features behind GHAS, deployment environments, tokens and apps.

**Forgejo, and Codeberg.** [forgejo-warden](https://github.com/intentius/forgejo-warden): self-hosted, so the warden takes a host URL and a token instead of an app.

**GitLab.** [gitlab-warden](https://github.com/intentius/gitlab-warden): re-asserts push rules on every run.

## Knowing is half the battle

These wardens are designed to be easy to set up and manage without placing the burden of state management on the owner.

Give them a try and see how they can help you with your security reviews, and your peace of mind.
