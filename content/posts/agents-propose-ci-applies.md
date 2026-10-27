---
title: "Agents propose, CI applies"
date: 2026-10-27
tags: ["agents", "ci"]
draft: true
---

<!-- The plywood paragraphs in "Keep your tool" are written ahead of the build. Building it makes them true: https://github.com/INTENTIUS/plywood/issues/1 -->

A reader on Hacker News described two problems with infrastructure and agents, starting with applies.

> Terraform feels very non-ergonomic when using agents... I don't want to give them access to apply terraform given the blast radius, but hunting around a million worktrees and planning and applying is awkward. I am moving it to CICD which I normally think of as an early optimization for startups.

Their second problem was about change history.

> If AWS would just version and keep an audit log per service of changes/config/state (I know cloudtrail etc.) there would be no real need for Terraform... just run aws cli in CICD, rollback would be targeting the last revision at the service level... ideally they would have some notion of transactions that package multiple changes across services. This would be very operator and agent friendly.

Moving applies to CI is the right call, and it can be a small step. [chant](https://intentius.io/chant/) generates that pipeline around the Terraform, OpenTofu or Pulumi code you already have.

## Agents propose, CI applies

An agent opens a pull request. CI plans the components the change reaches and the ones that depend on them, then posts one note with the plan and its digest. A reviewer approves that digest:

```bash
chant approve pr-12 pr-apply --plan jcs1-sha256:3e43... --approver github:alice --sign
```

A push that changes the plan changes the digest, so the old approval no longer counts. The pipeline is generated for GitHub, GitLab or Forgejo:

```bash
chant build --components --generate github --pr-loop --env prod --output .github/workflows/chant-pr.yml
```

With [`ci.identity.cloud`](https://intentius.io/chant/guide/security-cloud-identities/), plan and apply get a cloud identity each on AWS, GCP and Azure. The plan job trades its OIDC token for the plan identity before it checks out the change, and only apply jobs hold the apply identity. The agent never holds apply credentials. No step that runs the change's code holds a forge token either, since a [separate job posts the note](https://intentius.io/chant/guide/security-forge-token-handover/).

A merge records the plan and applies nothing, and a release deploys it. `--apply-on-merge` applies the approved plan on merge instead, and `--wave-gate release` gives each wave its own gate. [Applying before merge](https://intentius.io/chant/guide/apply-before-merge/) is opt-in, through `ci.workflow: "apply-before-merge"` and a `/chant apply` comment.

A [review agent](https://intentius.io/chant/guide/review-agent/) step has a model check the pull request's description against its diff and change set. It posts a note with a risk rating and approves nothing.

For Terraform, [`terragucci mcp`](https://intentius.io/terragucci/guides/agent-read-over-mcp/) gives an agent read-only MCP access to each root's last apply and the audit trail.

## One workspace instead of a pile of worktrees

A [chant workspace](https://intentius.io/chant/reference/workspace-declaration/) lists Terraform roots, choudoufu estates, Pulumi programs and chant projects as members of one `chant.workspace.json`, in one checkout. Inside a project, each Terraform root is a component, and `dependsOn` says which root reads which:

```typescript
export const app: Component = {
  name: "app",
  dependsOn: ["a"],
  deploy: [phase("Apply", [{ kind: "terraform-apply", root: "app", vars: { subnet: stackOutput("a", "id") } }])],
};
```

`chant run --components app` runs `app` and everything it depends on, wave by wave, and prints the order first:

```bash
chant run --components app --env staging
# run order: net, then a, then app
# added as dependencies: a, net
```

Across members, `chant workspace run web/deploy api/deploy` runs a producer before the members that link to it. `npx @intentius/behold demo three-cloud` serves a workspace of four members on chant, choudoufu and plunge.

## A change log and rollback you own

The pipeline records its runs and gates on a `chant/lifecycle` branch in your repo, beside each deploy and release. [`chant ledger`](https://intentius.io/chant/cli/ledger/) reads it as JSON with typed filters, and [`chant query`](https://intentius.io/chant/cli/query/) runs read-only SQL over it:

```bash
chant ledger gates --where op=pr-12 --since 7d
chant query "SELECT env, component, digest, actor FROM deploys ORDER BY timestamp DESC LIMIT 5"
```

`chant lifecycle snapshot prod` saves the resources the cloud reports, and both commands read them as the `resources` table.

A [release](https://intentius.io/chant/cli/release/) is the compiled output of one green commit, tagged `release/<label>`. Cut it, promote it, and roll back to it by name:

```bash
chant release cut v1.4.0 --build "npm run build" --yes
chant components promote --to prod --release v1.4.0
chant components rollback prod --release v1.4.0
```

This covers components that publish an artifact or deploy recorded templates, such as CloudFormation stacks and Kubernetes manifests. A Terraform root rolls back in source: `chant lifecycle rollback prod --to release/v1.4.0` opens a pull request that restores it, and the pipeline plans and applies that under a new approval.

A [composed run](https://intentius.io/chant/guide/composed-runs/) puts every component a change reaches under one digest and one approval. With a gate per wave, a component that fails [blocks only the components that read from it](https://intentius.io/chant/guide/failed-member-blocks/), and the rest apply. Rolling back atomically across clouds isn't possible, because the cloud APIs offer no transaction across services. A failed run leaves the applied members in place, and a re-run finishes the rest under the same approval when the plan hasn't moved.

## Keep your tool

Terraform and OpenTofu users keep their roots. [choudoufu](https://intentius.io/choudoufu/) is OpenTofu that writes an owner tag on each resource in the create call and keeps a record per resource in a bucket you own. A root takes one file, `estate.chdf.hcl`, in place of its `backend` block. [terragucci](https://intentius.io/terragucci/) is the CI for those roots, on Terraform, OpenTofu, Terragrunt or choudoufu:

```bash
npm i -D @intentius/terragucci
npx terragucci init
```

Pulumi users keep their programs. [plunge](https://intentius.io/plunge/) runs stock Pulumi programs, SDKs and providers with the same model: markers on each resource and a record per resource behind a `plunge+s3://` backend. It's at `v0.1.0`, proven so far on local emulators. [plywood](https://github.com/INTENTIUS/plywood) is the CI for Pulumi and plunge stacks on chant's runtime, as terragucci is for roots. Each pull request gets one grouped preview note, and the approval binds the preview's digest. Plan and apply run as separate identities, and stacks apply in gated waves after merge:

```bash
npm i -D @intentius/plywood
npx plywood init
```

[behold](https://intentius.io/behold/) draws the whole workspace in one graph, coloured by drift, with Terraform roots and Pulumi stacks beside chant projects.

## Prove it to yourself with your own agent

{{< agent-prompt >}}
Follow https://intentius.io/chant/guide/pull-request-ci/ in a scratch repo with three Terraform roots as components. Generate the pipeline with `chant build --components --generate forgejo --pr-loop --env local`, then tell me which step first runs the change's code and which job holds a forge token.

Use a local Forgejo and a local AWS emulator, never a real account. Never approve, merge, or apply.
{{< /agent-prompt >}}

---

## Read more

- [Generated CI for pull requests](https://intentius.io/chant/guide/pull-request-ci/)
- [Resource-level concurrency for Terraform](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/)
- [TF vendor power - without the SaaS](https://lex00.github.io/posts/tf-vendor-power-without-the-saas/)

## Sources

- Digest-bound approvals and the merge record: [Generated CI for pull requests](https://intentius.io/chant/guide/pull-request-ci/#approve-a-plan)
- Plan and apply identities: [Plan and apply as separate cloud identities](https://intentius.io/chant/guide/security-cloud-identities/)
- Forge tokens: [Keep the forge token from the plan](https://intentius.io/chant/guide/security-forge-token-handover/)
- Waves: [chant build](https://intentius.io/chant/cli/build/), [Keep going past a failed member](https://intentius.io/chant/guide/failed-member-blocks/)
- Ordering: [chant run](https://intentius.io/chant/cli/run/), [chant workspace run](https://intentius.io/chant/cli/workspace-run/)
- Releases and rollback: [chant release](https://intentius.io/chant/cli/release/), [chant components](https://intentius.io/chant/cli/components/), [chant lifecycle](https://intentius.io/chant/cli/lifecycle/)
- Three engines in one workspace: [behold three-cloud](https://intentius.io/behold/using/three-cloud/)
