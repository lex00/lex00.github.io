---
title: "Leave GitHub and take your CI with you"
date: 2026-09-02
featured_image: "img/gitlab-migrate-cover.svg"
tags: ["governance", "wardens", "migration"]
draft: false
---

Forge governance should be policy driven, and simple enough for anyone to setup.

It also helps if you can carry the same pattern across forges in case you migrate.

## In a pipeline

[gitlab-warden](https://intentius.io/gitlab-warden/) now ships `chant migrate`. Point it at `.github/workflows/` and it emits GitLab CI.

The [CI docs](https://intentius.io/gitlab-warden/CI/#running-migrate-in-a-pipeline) show it as a job that re-translates whenever a workflow changes:

```yaml
migrate:translate:
  stage: governance
  image: node:22
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes: [".github/workflows/*"]
  script:
    - npx @intentius/gitlab-warden migrate .github/workflows/
      -o migrated/
      --report migrate-findings.sarif
  artifacts:
    paths: [migrated/, migrate-findings.sarif]
    expire_in: 1 week
```

Migrate at your own pace. Keep the GitHub workflows as the source of truth for the transition window and let this job re-translate them on every change.

There's a [github-warden](https://intentius.io/github-warden/) version too, if you want to run it from the other direction.

## What maps in the migration

Not everything translates, and the warden never guesses. Anything lossy lands as a finding in the job log and in a SARIF report your reviewers can open.

## Chant under the hood

[chant migrate](https://intentius.io/chant/lexicons/gitlab/migration/) powers all the forge wardens. 

---

## Read more

- [gitlab-warden CI docs](https://intentius.io/gitlab-warden/CI/)
- [gitlab-warden](https://intentius.io/gitlab-warden/)
- [chant](https://intentius.io/chant/)
- [Governance for GitHub, GitLab, and Forgejo](https://lex00.github.io/posts/governance-for-github-gitlab-and-forgejo/)
