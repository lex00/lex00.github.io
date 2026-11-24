---
title: "Chainguard for your IaC pipelines"
date: 2026-11-23
draft: false
featured_image: "img/chainguard-for-your-iac-pipelines-header.jpg"
---

The jobs that plan and apply your infrastructure hold your cloud credentials. They can now run on Chainguard Images™, a minimal base that runs as a non-root user, pinned by digest.

Each product publishes a Chainguard set of its CI images next to the Debian one, and one line of config switches a repo over:

- <a href="https://intentius.io/terragucci/"><img src="/img/terragucci-icon.svg" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">terragucci</a> 0.4.65 and later: Terraform, OpenTofu and Terragrunt, with `image.base: chainguard`
- <a href="https://intentius.io/plywood/"><img src="/img/plywood-icon.png" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">plywood</a> 0.4.2 and later: Pulumi, with `image_base: chainguard`
- <a href="https://intentius.io/sql-yodeler/"><img src="/img/sql-yodeler-icon.svg" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">SQL Yodeler</a> 0.15.1 and later: database migrations, with `ci.imageBase: "chainguard"`

All three are built on <a href="https://intentius.io/chant/concepts/ci-products/"><img src="/img/chant-icon.svg" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">chant</a> and run on GitHub Actions, GitLab CI and Forgejo Actions. A CI product you build on chant gets the same with `base: "chainguard"`.

Every Intentius product here is free and open source under Apache 2.0.

---

## Read more

- [terragucci versions and pins](https://intentius.io/terragucci/reference/versions-and-pins/)
- [plywood versions and pins](https://intentius.io/plywood/reference/versions-and-pins/)
- [The SQL Yodeler CI image](https://intentius.io/sql-yodeler/workflows/#the-ci-image)
- [CI products in chant](https://intentius.io/chant/concepts/ci-products/)
- [Infra approvals at scale](https://lex00.github.io/posts/infra-approvals-at-scale/)

[Chainguard](https://www.chainguard.dev/) is a trademark of Chainguard, Inc. Terraform is a trademark of HashiCorp, an IBM Company. OpenTofu is a trademark of The Linux Foundation. Pulumi is a trademark of Pulumi Corporation. ClickHouse is a trademark of ClickHouse, Inc. PostgreSQL is a trademark of the PostgreSQL Community Association of Canada. GitHub, GitLab and Forgejo are trademarks of their owners.
