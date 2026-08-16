---
title: "Syntax error at position (1,76)"
date: 2026-08-16
draft: true
---

<!-- OPEN: the bug itself. lowercase principal key in a trust policy. -->

```json
"Principal": { "aws": "arn:aws:iam::123456789012:root" }
```

<!-- facts: IAM accepts only exact Title Case keys here (AWS / Service / Federated / CanonicalUser).
     you measured where this gets caught. same defect, same machine, warm runs. -->

<!-- CDK PATH: note that the prop carrying the doc is typed `any` (CFN spec says Json). -->

| check | wall time | verdict |
|---|---|---|
| `tsc --noEmit` | 0.24s | passes |
| synth | 0.76s | passes, bad key lands in the template |
| cfn-lint 1.55.1 | 0.35s | passes, no findings |
| `aws iam create-role` | real API call | MalformedPolicyDocument |

<!-- point: ~1.4s of dev-side pipeline, three yeses, cloud is the first no.
     the entire diagnostic is: -->

> Syntax error at position (1,76)

<!-- facts: char offset into generated JSON. bare API call is the CHEAP version.
     via CloudFormation: changeset + stack events + rollback before you even see the position. -->

<!-- CHANT PATH: types generated from same spec, but policy doc is closed.
     Principal = "*" | { exact keys }. tested against the full 135k-line generated .d.ts. -->

| check | wall time | verdict |
|---|---|---|
| `tsc --noEmit` | 0.29s | caught |

> 'aws' does not exist in type '{ AWS?: string | string[]; Service?: string | string[]; Federated?: string | string[]; }'. Did you mean to write 'AWS'?

<!-- point: cloud gives a position, compiler gives the correction.
     same check runs in the editor, so really it's caught before save. -->

<!-- FORMULA: burned team time per day. -->

```
burned minutes per day = F x C_fail + P x C_lint + A
```

<!-- conservative fill, 20-person infra team:
     F      = cloud-side validation failures/day. 1/dev/month -> 1/day
     C_fail = rollback + diagnose from stack events + redeploy -> 25 min
     P      = pipeline runs/day -> 30
     C_lint = synth+lint wall time every clean run pays. toy app 1.4s, real app minutes -> call it 1 min
     A      = second-toolchain upkeep (bumps, rule config) -> 5 min/day
     total ~1 hour/day. key point: at F=0 the standing tax (P*C_lint + A) remains. -->

<!-- FENCES (concede before they nitpick):
     - cfn-lint DOES catch the neighbors: Effect case, Version date, statement-not-an-object. not claimed.
     - fail closed: IAM rejects these. cost is time/iterations, never a breach.
     - pinned: cfn-lint 1.55.1, current aws-cdk-lib. one rule addition could close this exact gap.
     - chant has post-synth checks too. claim = earliest check + one toolchain, not who checks last. -->

<!-- CLOSE: tie to a-billion-proofs-a-day. this is one keystroke-enforced property, timed. -->

---

## Read more

- [A billion proofs a day](https://lex00.github.io/posts/a-billion-proofs-a-day/)
- [Flame graphing the leftness of infra tooling](https://lex00.github.io/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [Infrastructure deserves a compiler](https://lex00.github.io/posts/infrastructure-deserves-a-compiler/)
- [chant](https://intentius.io/chant/)
