<!-- Source for the table images in resource-level-concurrency-for-terraform.
     Edit here, then run python3 scripts/gen_concurrency_tables.py. -->

## Stock backends

| | Terraform or OpenTofu | Terragrunt run --all | Atmos --affected |
|---|---|---|---|
| One plan covers every root | No, one per root | No, one per unit | No, one per component |
| A changed value reaches the roots that read it | No, `terraform_remote_state` reads the last applied outputs | No, since 1.2.0 it reads outputs from state | No, `!terraform.output` reads the last applied outputs |
| A new ID reaches the roots that read it | No, the subnet isn't in state yet | Only as `mock_outputs` | Only as a `//` default or `--use-mocks` |
| The approved plan is what applies | Per root, with `-out` | `--out-dir` saves each plan, mocks included | The planfile store; verify counts a newly known value as drift |
| Applies | One per root | One per unit | One per component |

## terragucci on stock backends

| | Waves | waves.compose: true |
|---|---|---|
| One plan covers every root | One note for every root's plan | Yes, one root with a module per root |
| A changed value reaches the roots that read it | Yes, a [linked root](https://intentius.io/terragucci/concepts/waves-and-approvals/#linked-roots) plans on its upstream's planned outputs | Yes |
| A new ID reaches the roots that read it | The reader plans again after its upstream applies | Yes, [in the same apply](https://intentius.io/terragucci/concepts/waves-and-approvals/#a-composed-run) |
| The approved plan is what applies | The approval binds the plans' digest; any gate but `never` re-approves a reader's second plan | One digest, one approval |
| Applies | One per wave | One, then each state is written back |

## choudoufu live backend

| | terragucci waves.compose | Terragrunt run --all | Atmos --affected |
|---|---|---|---|
| One plan covers every root | Yes | Yes | Yes, with `--include-dependents` |
| A changed value reaches the roots that read it | Yes | Yes | Yes |
| A new ID reaches the roots that read it | Yes | Yes, `(known after apply)` | Yes |
| The approved plan is what applies | Yes | Yes, with `--out-dir`; a stale plan is refused | Yes, with `planfiles.verify: warn`; choudoufu refuses any other change |
| Applies | One, with nothing to lock or split | One | One per component |
