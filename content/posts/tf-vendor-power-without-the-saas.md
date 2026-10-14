---
title: "TF vendor power - without the SaaS"
date: 2026-10-13
draft: false
featured_image: "img/tf-vendor-power-cover.svg"
share_image: "img/tf-vendor-power-share.png"
---

Terraform vendors sell plan and apply on pull requests, approvals, policy, drift checks and an audit trail, run on their servers with your cloud credentials. [terragucci](https://intentius.io/terragucci/) is those pipelines, ready to run in your own CI on GitHub, GitLab or Forgejo, with state and reports in your own bucket. There's no account to create and no platform to log into, and it's Apache-2.0.

[choudoufu](https://intentius.io/choudoufu/docs/) is optional. It's OpenTofu that tags each resource with its owner, so the state file becomes a cache and locking goes per resource. It runs on AWS and Kubernetes under MPL-2.0, and since the cache is a stock state file, [going back to stock](https://intentius.io/choudoufu/docs/model/cache/#the-cache-is-also-the-exit) is a copy.

## What you'd pay a SaaS for

![What you'd pay a Terraform SaaS for, and the terragucci page that does each one in your own CI](/img/tf-vendor-power-saas-table.png)

## State and locking

![State and locking, terragucci with stock Terraform or OpenTofu against terragucci with choudoufu](/img/tf-vendor-power-state-table.png)

[Sources](#sources) at the end links every cell to its doc.

## Kill an apply

`kill -9` an apply right after it creates a VPC, then run it again. choudoufu tags the VPC in the create request, so the next plan finds it by that tag and the re-run binds it instead of building a second one. Stock Terraform and OpenTofu record the VPC only after the create call returns, so a kill in that window leaves one the re-run doesn't know about. The [ten types](https://intentius.io/choudoufu/docs/claims/recovery-is-a-rerun/) that take no tags at create keep that window under choudoufu too.

## A plan that costs its change

`plan -cone` plans only the changed resources, what they depend on and what depends on them. It's opt-in for pull requests and approved with the plan. A change that touches providers, the lock file or more than 30% of the estate gets a full plan instead.

## A plan across state files

When a pull request changes a root and the roots that read its state, the readers plan on its [planned outputs](https://intentius.io/terragucci/concepts/waves-and-approvals/#linked-roots), so what's downstream is checked against the infrastructure as it will be after the merge. That works with stock Terraform and OpenTofu through `terraform_remote_state`, with Terragrunt `dependency` blocks, and between [choudoufu estates](https://intentius.io/choudoufu/docs/use/cross-estate/#a-value-the-producer-has-not-applied-yet).

Some values don't exist until the upstream applies, like the ID of a network the same change creates. No plan can show those. terragucci writes `(known after apply)` and names them in the plan note, and the wave that reads one plans again on the real value once its upstream has applied, then waits for its own approval. choudoufu won't plan on such a value at all, and it won't apply a reader until its upstream has applied the values the reader was planned on.

The applies go in waves, in dependency order. A wave that fails leaves the waves before it applied, since the cloud has already made those changes, and [plans again](https://intentius.io/terragucci/reference/pipeline/#stopped-applies) on what's actually there when it next runs.

## The detail

![Each state and locking claim in full, for stock Terraform or OpenTofu and for choudoufu](/img/tf-vendor-power-detail-table.png)

Most rows are backed by a smoke claim named on the [locking page](https://intentius.io/terragucci/concepts/locking-and-staleness/). The [glossary](https://intentius.io/terragucci/concepts/glossary/) defines wave, root and forge.

## Prove it to yourself with your own agent

{{< agent-prompt >}}
For each row of "What you'd pay a SaaS for", open the page listed for it under Sources and say whether it does what the row says.

For each row of "The detail", give three verdicts, each with a source link:

- terragucci: does the doc listed for it under Sources support the cell as written? Find the smoke claim behind it in https://github.com/INTENTIUS/terragucci (stack/smoke.sh, docs-site/src/data/smoke.json) and say whether its latest result passes.
- choudoufu: the same, in https://github.com/INTENTIUS/choudoufu (live/smoke/claims/).
- The industry, as of today: which Terraform state backends, TACOs and hosted Terraform platforms document the same capability? Quote their current docs and give the date you read them.

Mark a cell unverified when you can't find a source, rather than inferring one.

Then run the post's "Kill an apply" test if you have Docker: against a local AWS emulator, once with stock OpenTofu and once with choudoufu, and report how many VPCs exist after each re-run. Never run it against a real cloud account.
{{< /agent-prompt >}}

---

## Read more

- [terragucci: locking and staleness](https://intentius.io/terragucci/concepts/locking-and-staleness/)
- [choudoufu: concurrency](https://intentius.io/choudoufu/docs/model/concurrency/)
- [Tofu tastes better with live markers](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/)
- [choudoufu cuts terralith optimization time in half](https://lex00.github.io/posts/choudoufu-cuts-terralith-optimization-time-in-half/)

## Sources

What you'd pay a SaaS for:

- Plans on pull requests, applies after approval: [One grouped plan note, then applies in waves](https://intentius.io/terragucci/getting-started/)
- Policy: [Rego checks in the plan note, and recorded overrides](https://intentius.io/terragucci/guides/write-a-policy/)
- Drift detection: [Every root planned on a schedule, one grouped report](https://intentius.io/terragucci/guides/turn-on-drift-checks/)
- Cost estimates: [Infracost in the plan note, on your own key](https://intentius.io/terragucci/guides/estimate-cost/)
- An audit trail: [Every approval, apply and override as JSON lines in your bucket](https://intentius.io/terragucci/reference/audit-trail/)
- One view of every project: [A page in your bucket with every project's latest plan and drift](https://intentius.io/terragucci/guides/see-every-project/)
- Approvals in Slack or Teams: [Through a relay you run in your own cloud](https://intentius.io/terragucci/guides/approve-from-chat/)
- Holding your credentials: [Nobody else does: separate plan and apply roles over OIDC, in your CI](https://intentius.io/terragucci/reference/threat-model/)
- Scale: [1,361 roots and 10,069 resources across 12 repos](https://intentius.io/terragucci/reference/scale/)
- Moving off it: [HCP Terraform, Scalr and OTF](https://intentius.io/terragucci/guides/coming-from-hcp-terraform-scalr-or-otf/), [Spacelift and env zero](https://intentius.io/terragucci/guides/coming-from-spacelift-or-env-zero/), [Atlantis and OpenTaco](https://intentius.io/terragucci/guides/coming-from-atlantis-or-opentaco/)

State and locking, and the detail:

- Resource-level locking: [applies kept apart per root](https://intentius.io/terragucci/concepts/locking-and-staleness/#terragucci-layers), [a wave holds each resource its plan changes](https://intentius.io/terragucci/concepts/locking-and-staleness/#two-applies-of-one-estate)
- Disjoint changes apply in parallel: [Different roots side by side](https://intentius.io/terragucci/reference/pipeline/#applies-side-by-side), [Inside one estate too](https://intentius.io/terragucci/concepts/locking-and-staleness/#two-applies-of-one-estate)
- Plans take no lock: [Pull request plans and drift runs](https://intentius.io/terragucci/concepts/locking-and-staleness/#lock-waits), [Every plan](https://intentius.io/choudoufu/docs/claims/no-self-managed-locks/)
- A conflicting apply is refused, naming the other: [A held root is refused with the holder named](https://intentius.io/terragucci/concepts/locking-and-staleness/#pull-request-locks), [a stale plan is refused](https://intentius.io/terragucci/concepts/locking-and-staleness/#stale-plans), [only when one of its own changes moved](https://intentius.io/choudoufu/docs/claims/apply-what-was-approved/)
- One saved plan to review: [One grouped note for N plans](https://intentius.io/terragucci/concepts/why-plans-are-grouped/), [the approval bound to their digest](https://intentius.io/terragucci/concepts/waves-and-approvals/#approval-binding)
- Multi-state transaction: [each wave plans after the one before it applied](https://intentius.io/terragucci/concepts/how-it-works/), [a wave whose approved plans moved applies nothing](https://intentius.io/terragucci/concepts/locking-and-staleness/#stale-plans), [a failed wave plans again when it next runs](https://intentius.io/terragucci/reference/pipeline/#stopped-applies), [a reading estate's apply is refused](https://intentius.io/choudoufu/docs/use/cross-estate/#a-value-the-producer-has-not-applied-yet)
- A killed apply: [The state lock stays held until `terragucci unlock-state` frees it after an approval](https://intentius.io/terragucci/guides/release-a-state-lock/), [a resource created after the last state write gets created twice](https://intentius.io/choudoufu/docs/claims/recovery-is-a-rerun/), [Nothing to release](https://intentius.io/choudoufu/docs/claims/no-self-managed-locks/), [the wave resumes under the same approval](https://intentius.io/terragucci/reference/pipeline/#stopped-applies)
- Applies from outside the pipeline: [The state lock still serializes them](https://intentius.io/terragucci/concepts/locking-and-staleness/#stock-and-choudoufu), [Different resources both land; on one record, one lands and the other fails naming it](https://intentius.io/choudoufu/docs/model/concurrency/#the-record-store-is-not-locked-either)
- Scoped permissions: [Per state file and role](https://intentius.io/terragucci/guides/scope-state-access/), [A role scoped by the estate tag](https://intentius.io/choudoufu/docs/use/governance/scope-a-role/)
- Query your infrastructure: [SQL over every run's reports](https://intentius.io/terragucci/guides/query-with-sql/), [a read-only MCP server](https://intentius.io/terragucci/guides/agent-read-over-mcp/), [any cloud tool can list an estate by its tag](https://intentius.io/choudoufu/docs/claims/identity-is-a-tag/)
- Nothing mocked: [a plan that reads `mock_outputs` fails its wave](https://intentius.io/terragucci/guides/use-terragrunt/#later-layers), [pull requests plan on the upstream's planned outputs](https://intentius.io/terragucci/concepts/waves-and-approvals/#linked-roots), [a downstream estate plans on its upstream's planned outputs](https://intentius.io/choudoufu/docs/use/cross-estate/#a-value-the-producer-has-not-applied-yet)
- A plan walks only what the change touches: [only the roots a change reaches are planned](https://intentius.io/terragucci/concepts/how-it-works/)
