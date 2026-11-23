---
title: "Infra approvals at scale"
date: 2026-11-23
draft: false
featured_image: "img/infra-approvals-at-scale-dominoes.jpg"
---

Applying from the pull request is what people love about Atlantis. When one change plans many stacks, you also want one approval that cascades through all of them and stops at any stack whose plan changed.

I built [terragucci](https://intentius.io/terragucci/) for Terraform and OpenTofu, and [plywood](https://intentius.io/plywood/) for Pulumi, to do both. The approval is a digest of the plan, so it only covers that plan. Stacks then apply in waves, with production after staging.

They are free and open source under Apache 2.0. There is no server or database to run. Everything happens in your pull requests and in your GitHub Actions, GitLab CI or Forgejo Actions pipelines. The approvals are commits in your repo.

---

## Read more

- [terragucci](https://intentius.io/terragucci/): plans and approvals from pull requests for Terraform, OpenTofu and Terragrunt
- [plywood](https://intentius.io/plywood/): the same for Pulumi
- [Waves and approvals in terragucci](https://intentius.io/terragucci/concepts/waves-and-approvals/)
- [Apply before merge with terragucci](https://intentius.io/terragucci/guides/apply-before-merge/)
- [Update before merge with plywood](https://intentius.io/plywood/guides/update-before-merge/)
- [Infrastructure change coordination](https://lex00.github.io/posts/infrastructure-change-coordination/)
- [TF vendor power - without the SaaS](https://lex00.github.io/posts/tf-vendor-power-without-the-saas/)
