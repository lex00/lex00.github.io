<!-- Source for the table images in tf-vendor-power-without-the-saas.
     Edit here, then run python3 scripts/gen_vendor_power_tables.py. -->

## What you'd pay a SaaS for

| You'd pay a SaaS for | terragucci, in your CI |
|---|---|
| Plans on pull requests, applies after approval | [One grouped plan note, then applies in waves](https://intentius.io/terragucci/getting-started/) |
| Policy | [Rego checks in the plan note, and recorded overrides](https://intentius.io/terragucci/guides/write-a-policy/) |
| Drift detection | [Every root planned on a schedule, one grouped report](https://intentius.io/terragucci/guides/turn-on-drift-checks/) |
| Cost estimates | [Infracost in the plan note, on your own key](https://intentius.io/terragucci/guides/estimate-cost/) |
| An audit trail | [Every approval, apply and override as JSON lines in your bucket](https://intentius.io/terragucci/reference/audit-trail/) |
| One view of every project | [A page in your bucket with every project's latest plan and drift](https://intentius.io/terragucci/guides/see-every-project/) |
| Approvals in Slack or Teams | [Through a relay you run in your own cloud](https://intentius.io/terragucci/guides/approve-from-chat/) |
| Holding your credentials | [Nobody else does: separate plan and apply roles over OIDC, in your CI](https://intentius.io/terragucci/reference/threat-model/) |
| Scale | [1,361 roots and 10,069 resources across 12 repos](https://intentius.io/terragucci/reference/scale/) |
| Moving off it | Guides from [HCP Terraform, Scalr and OTF](https://intentius.io/terragucci/guides/coming-from-hcp-terraform-scalr-or-otf/), [Spacelift and env zero](https://intentius.io/terragucci/guides/coming-from-spacelift-or-env-zero/), and [Atlantis and OpenTaco](https://intentius.io/terragucci/guides/coming-from-atlantis-or-opentaco/) |

## State and locking

| | terragucci + Terraform/OpenTofu | terragucci + choudoufu |
|---|---|---|
| Resource-level locking | Per root | Per resource |
| Disjoint changes apply in parallel | Across roots | Inside one estate too |
| Plans take no lock | Pull request plans and drift runs | Every plan |
| A conflicting apply is refused, naming the other | Yes | Yes, only when its own changes moved |
| One saved plan to review | Yes, one note for N plans | The same |
| Multi-state transaction | No | No |
| A killed apply | Lock held until an approved release | Nothing to release; the wave resumes |
| Applies from outside the pipeline | Serialized by the state lock | Both land; on one record the second fails |
| Scoped permissions | Per state file and role | Per estate tag |
| Query your infrastructure | SQL and a read-only MCP server | The same, plus listing by tag |
| Nothing mocked | Yes | Yes, between estates too |
| A plan walks only what the change touches | The roots it reaches, each in full | The change's cone |

## The detail

| Claim | terragucci + Terraform/OpenTofu | terragucci + choudoufu |
|---|---|---|
| Resource-level locking | Per root: the backend's state lock, and [applies kept apart per root](https://intentius.io/terragucci/concepts/locking-and-staleness/#terragucci-layers) | Per resource: [a wave holds each resource its plan changes](https://intentius.io/terragucci/concepts/locking-and-staleness/#two-applies-of-one-estate), all or none in one commit |
| Disjoint changes apply in parallel | [Different roots side by side](https://intentius.io/terragucci/reference/pipeline/#applies-side-by-side); inside one root the second apply waits | [Inside one estate too](https://intentius.io/terragucci/concepts/locking-and-staleness/#two-applies-of-one-estate): changes to different resources apply side by side |
| Plans take no lock | [Pull request plans and drift runs](https://intentius.io/terragucci/concepts/locking-and-staleness/#lock-waits); a wave's plan waits for the state lock | [Every plan](https://intentius.io/choudoufu/docs/claims/no-self-managed-locks/): there is no lock to take |
| A conflicting apply is refused, naming the other | [A held root is refused with the holder named](https://intentius.io/terragucci/concepts/locking-and-staleness/#pull-request-locks); [a stale plan is refused](https://intentius.io/terragucci/concepts/locking-and-staleness/#stale-plans) if anything in the root moved | An apply started from a comment is refused naming the run; a push's wave waits for it, then plans again. A saved plan is refused [only when one of its own changes moved](https://intentius.io/choudoufu/docs/claims/apply-what-was-approved/) |
| One saved plan to review | [One grouped note for N plans](https://intentius.io/terragucci/concepts/why-plans-are-grouped/), [the approval bound to their digest](https://intentius.io/terragucci/concepts/waves-and-approvals/#approval-binding) | The same |
| Multi-state transaction | No: gated waves, and [a wave whose approved plans moved applies nothing](https://intentius.io/terragucci/concepts/locking-and-staleness/#stale-plans) | No, the same |
| A killed apply | [The state lock stays held until `terragucci unlock-state` frees it after an approval](https://intentius.io/terragucci/guides/release-a-state-lock/), and [a resource created after the last state write gets created twice](https://intentius.io/choudoufu/docs/claims/recovery-is-a-rerun/) on the re-run | [Nothing to release](https://intentius.io/choudoufu/docs/claims/no-self-managed-locks/): the next wave takes over the killed run's hold once the forge reports it ended, or after two hours. The next plan finds what was created, and [the wave resumes under the same approval](https://intentius.io/terragucci/reference/pipeline/#stopped-applies) |
| Applies from outside the pipeline | [The state lock still serializes them](https://intentius.io/terragucci/concepts/locking-and-staleness/#stock-and-choudoufu) | [Different resources both land; on one record, one lands and the other fails naming it](https://intentius.io/choudoufu/docs/model/concurrency/#the-record-store-is-not-locked-either) |
| Scoped permissions | [Per state file and role](https://intentius.io/terragucci/guides/scope-state-access/) | [A role scoped by the estate tag](https://intentius.io/choudoufu/docs/use/governance/scope-a-role/) is refused on another estate's resources |
| Query your infrastructure | [SQL over every run's reports](https://intentius.io/terragucci/guides/query-with-sql/), and [a read-only MCP server](https://intentius.io/terragucci/guides/agent-read-over-mcp/) | The same, plus [any cloud tool can list an estate by its tag](https://intentius.io/choudoufu/docs/claims/identity-is-a-tag/) |
| Nothing mocked | Yes: [a plan that reads `mock_outputs` fails its wave](https://intentius.io/terragucci/guides/use-terragrunt/#later-layers), and [pull requests plan on the upstream's planned outputs](https://intentius.io/terragucci/concepts/waves-and-approvals/#linked-roots) | Yes, between estates too: a downstream estate plans on its upstream's planned outputs, and [an output only known after apply is refused](https://intentius.io/choudoufu/docs/use/cross-estate/) rather than guessed |
| A plan walks only what the change touches | Half: [only the roots a change reaches are planned](https://intentius.io/terragucci/concepts/how-it-works/), but each one in full | Yes: `plan -cone` plans the change and everything that depends on it, and falls back to a full plan when it can't be sure |
