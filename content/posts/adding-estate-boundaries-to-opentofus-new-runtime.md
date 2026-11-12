---
title: "Adding estate boundaries to OpenTofu's new runtime"
date: 2026-11-12
draft: false
featured_image: "img/choudoufu-new-engine-toggle-hero.svg"
---

[choudoufu](https://intentius.io/choudoufu/) runs OpenTofu's new runtime with its live backend, which adds estate boundaries.

- In choudoufu v0.34.0, `TOFU_X_EXPERIMENTAL_RUNTIME=1`, upstream's own variable, runs plan and apply on the new runtime in any build, and live mode writes its ownership markers there ([release notes](https://github.com/INTENTIUS/choudoufu/releases/tag/v0.34.0)).
- A run the new runtime can't handle yet runs on the default runtime instead, and its output says so.
- Without the variable, the default runtime runs as before.

choudoufu is a fork of OpenTofu. Its live backend writes one [ownership marker](https://intentius.io/choudoufu/how-it-works/identity/) onto each cloud resource and reads it back on the next plan. That one marker gives:

- boundaries between estates, drawn by IAM, [from one backend](https://intentius.io/choudoufu/how-it-works/across-estates/)
- [applies across estates](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/) with no coordination, and a [conditional write](https://intentius.io/choudoufu/how-it-works/locking/) per resource in place of a held lock
- moved resources [found by marker](https://github.com/INTENTIUS/choudoufu/issues/2374)
- the live system [read before planning](https://intentius.io/choudoufu/how-it-works/identity/)

OpenTofu co-maintainer Laurence Bordowitz opened OpenTofu Day North America on 2026-11-09 with [An Overview of OpenTofu's Engine Rewrite](https://cncf-hosted-co-located-events-north-america-2026.sessionize.com/session/1266401); the project calls the new engine the new runtime, and it is still being built.

## One backend serves many estates, with boundaries drawn by IAM

IAM conditions on the marker tag [draw the boundaries between estates](https://intentius.io/choudoufu/how-it-works/across-estates/).

## Every race on the shared backend ends in a re-plan or a named collision

Each resource has [one record](https://intentius.io/choudoufu/how-it-works/locking/) in a bucket the team already runs, and each write is conditional on that record being unchanged. The live backend holds no lock across a run.

- A race ends in a clean re-plan or a named collision, and none orphans a resource silently.
- A crash mid-create is recovered, because the marker rides the create call.
- A saved plan refuses, with exit 3, if the live system moved since approval.
- Separate estates [apply with no coordination](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/).
- Inside one estate, plain applies to the same attribute are last-writer-wins. The docs say to serialize per estate in CI.

![Apply A changes db and apply B changes subnet. Under Terraform B waits for A's lock on the whole state file. Under choudoufu the resources sit in two estates, so both applies land. A stale saved plan on db is refused](/img/concurrency-lock-scope.png)

[terragucci](https://intentius.io/terragucci/) runs the fork as an optional engine from a team's own CI, and its [waves](https://intentius.io/terragucci/concepts/waves-and-approvals/) hold per resource, keyed by estate and address: applies to different resources of one estate run at the same time, and an overlapping one waits.

Under `strict { secrets = "refuse" }`, [nothing choudoufu keeps holds a secret](https://github.com/INTENTIUS/choudoufu/blob/main/live/smoke/claims/no-secret-survives-in-what-the-tool-keeps.md). Under `strict { secrets = "ssm" }`, new in v0.34.0 and proven on real AWS, each secret value goes to an SSM Parameter Store SecureString and the record keeps a reference to it.

Per-object state for OpenTofu is proposed in the open issue [#2662](https://github.com/opentofu/opentofu/issues/2662), filed 2025-04-15. It would store each object of one configuration's state separately, behind a new storage API with [per-key locking](https://github.com/opentofu/opentofu/pull/2723) that every backend would implement.

## Live reads find what exists and find moved resources by marker

- Before planning, choudoufu [reads the live system](https://intentius.io/choudoufu/how-it-works/identity/) to learn what exists, in place of the engine's refresh.
- In live mode a moved resource is found by the address marker it already carries, so a `moved` block leaves state as it is ([#2374](https://github.com/INTENTIUS/choudoufu/issues/2374)). Outside live mode, upstream's new runtime executes `moved` blocks itself.
- A known issue in v0.34.0: applying a `moved` block that renames a whole module panics on the new runtime with "invalid move". A fix is under way.

## choudoufu follows OpenTofu main and deletes each patch once upstream ships its own

- The next sync after OpenTofu ships a piece the fork patched takes the project's code and deletes the patch.
- choudoufu builds on OpenTofu's main branch and syncs every two weeks while the new runtime is under way, and at each OpenTofu release tag ([#2256](https://github.com/INTENTIUS/choudoufu/issues/2256)).
- The details are in [how choudoufu differs from upstream](https://intentius.io/choudoufu/how-it-works/upstream/).

## What the new runtime has yet to handle runs on the default runtime

A run that reaches a row of the [gap table](https://github.com/INTENTIUS/choudoufu/blob/main/live/NEW-RUNTIME.md) still open falls back to the default runtime for the whole run and prints "Ran on the default runtime, not the new runtime", naming the rows and the upstream issues they wait on. `CHOUDOUFU_NEW_RUNTIME_STRICT=1` refuses those runs instead.

Fork ports fill most of the gaps until upstream's own code lands:

- in-run estates
- cancel and stop
- tracing spans
- conditions and variable validation
- `removed` blocks, through forget
- check rules and check results
- sensitive values
- data sources, from upstream's own pull request [`#4740`](https://github.com/opentofu/opentofu/pull/4740), cherry-picked

Each port is commented with the upstream issue that retires it. `CHOUDOUFU_NEW_RUNTIME_NO_PORT_<NAME>=1` turns one off and `CHOUDOUFU_NEW_RUNTIME_NO_FORK_PORTS=1` turns them all off, and the gap row's refusal comes back.

The experimental test lane runs choudoufu's tests with the toggle on, and its expected failures went from 209 to 42 in this release. With the toggle on in strict mode, the gauntlet estates corpus-iam-policy, reference-ec2-vpc, reference-azure and reference-k8s all clear. corpus-lambda-simple fails on the module-rename `moved` issue above.

---

## Read more

- [A live demo](https://demo.intentius.io): terragucci runs choudoufu across three estates with one record store
- [Resource-level concurrency for Terraform](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/)
- [How choudoufu differs from upstream](https://intentius.io/choudoufu/how-it-works/upstream/)
- [Tofu tastes better with live markers](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/)

## Sources

- Talk, 2026-11-09: [An Overview of OpenTofu's Engine Rewrite](https://cncf-hosted-co-located-events-north-america-2026.sessionize.com/session/1266401)
- choudoufu: [#2256](https://github.com/INTENTIUS/choudoufu/issues/2256), [#2374](https://github.com/INTENTIUS/choudoufu/issues/2374), the [v0.34.0 release notes](https://github.com/INTENTIUS/choudoufu/releases/tag/v0.34.0), the [gap table](https://github.com/INTENTIUS/choudoufu/blob/main/live/NEW-RUNTIME.md)
