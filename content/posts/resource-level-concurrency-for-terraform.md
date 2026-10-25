---
title: "Resource-level concurrency for Terraform"
date: 2026-10-24
draft: false
featured_image: "img/concurrency-hero.svg"
share_image: "img/concurrency-share.png"
---

Terraform needs a lock around applies because it lacks resource-level concurrency. The apply boundary is at the state file, so everything in it gets locked together.

[choudoufu](https://intentius.io/choudoufu/) moves the boundary to each resource. This change prevents state corruption without a lock.

![Apply A changes db and apply B changes subnet. Under Terraform B waits for A's lock on the whole state file; under choudoufu, with the resources in two estates, both land and a stale saved plan on db is refused](/img/concurrency-lock-scope.png)

Each resource's estate comes from the `live` block of the directory that declares it. See [concurrency](https://intentius.io/choudoufu/docs/model/concurrency/) and [locks](https://intentius.io/choudoufu/docs/claims/no-self-managed-locks/).

## Across roots

Teams split state into roots to shrink what one lock covers. Across roots, a changed value is planned on its last applied version, and Terragrunt and Atmos plan a new ID on a mock.

![Scorecard of one plan, changed values, new IDs, approved plans and applies across roots, on stock backends and on the choudoufu live backend](/img/concurrency-scorecard.png)

![Two changes across network and app. On a stock backend the pull request shows app with no change or a mocked subnet ID, and the apply does something else. On the choudoufu live backend the pull request shows the real change and that plan applies](/img/concurrency-review-flow.png)

Keep Terragrunt, Atmos or terragucci. On the live backend, the saved plan you review is the plan that applies.

## The demos

Each one builds `network`, `app` and `edge` and runs its pipeline on a local Forgejo.

- [terragucci `waves.compose` on choudoufu](https://github.com/INTENTIUS/terragucci/tree/main/example-demo-choudoufu-compose)
- [Terragrunt with choudoufu as its binary](https://github.com/INTENTIUS/choudoufu/tree/main/examples/demo-terragrunt)
- [Atmos with choudoufu as its binary](https://github.com/INTENTIUS/choudoufu/tree/main/examples/demo-atmos)
## Prove it to yourself with your own agent

{{< agent-prompt >}}
Check every mark in this post's scorecard against the current docs and source of each tool, including https://intentius.io/terragucci/ and https://intentius.io/choudoufu/. Quote the supporting passage with a link and the date read, or mark it unsupported.

Use a local AWS emulator, never a real account. Make three Terragrunt units where app reads a new subnet from network through a `dependency` block. Run `terragrunt run --all --out-dir plans` to plan and then apply, once with OpenTofu and again with `terraform_binary = "choudoufu"`. Report the subnet id in app's saved plan and the one it applied.
{{< /agent-prompt >}}

---

## Read more

- [TF vendor power - without the SaaS](https://lex00.github.io/posts/tf-vendor-power-without-the-saas/)

## Sources

- Terragrunt reads dependency outputs from state by default since 1.2.0: [dependency-fetch-output-from-state](https://docs.terragrunt.com/reference/cli/commands/run#dependency-fetch-output-from-state)
- Terragrunt saved plans and mock outputs: [Saving OpenTofu/Terraform plan output](https://docs.terragrunt.com/features/stacks/run-queue/#saving-opentofuterraform-plan-output), [terragrunt#2178](https://github.com/gruntwork-io/terragrunt/issues/2178)
- Atmos `!terraform.output` and its defaults: [atmos.tools](https://atmos.tools/functions/yaml/terraform.output)
- Atmos plan files with multi-component flags, and bulk deploy verification: [cloudposse/atmos errors.go](https://github.com/cloudposse/atmos/blob/main/errors/errors.go), [bulk deploy planfile verification](https://github.com/cloudposse/atmos/blob/main/docs/fixes/2026-10-16-bulk-deploy-planfile-verification.md)
- terragucci linked roots and composed runs: [waves and approvals](https://intentius.io/terragucci/concepts/waves-and-approvals/)
- choudoufu across estates and locking: [across estates](https://intentius.io/choudoufu/how-it-works/across-estates/), [locking](https://intentius.io/choudoufu/how-it-works/locking/)
