---
title: "aws-bench: chant vs CDK scenario 1"
date: 2026-07-28
featured_image: "img/aws-bench-s1-cover.svg"
---

chant beats CDK on an infrastructure-agent benchmark.

Same model on both sides: Haiku 4.5, fixed. The only variable was the tooling, a CDK-driven agent vs a chant-driven one. On aws-bench's fair task set, chant scored 15/15 against CDK's 11/15, at 29% lower cost and 36% fewer tokens generated. Sonnet bare, a stronger model with no special tooling, also scored 11/15. Three of the four extra tasks come down to one question: which EC2 instances are SSH-reachable from the internet?

| | Sonnet bare | CDK | chant |
| --- | --- | --- | --- |
| fair-set valid | 11/15 | 11/15 | 15/15 |
| ssh-reachability | 0/3 | 0/3 | 3/3 |
| input tokens | 2.66M | 7.88M | 6.37M |
| output tokens | 39k | 82k | 53k |
| cost (USD) | 2.02 | 1.87 | 1.32 |

## The question that separated them

The scenario is six EC2 instances across three regions. The discriminating task: which are reachable via SSH from the internet? The ground truth is 2 instances, and answering takes a multi-hop join:

1. Is the instance's subnet internet-facing? instance → subnet → route table → route → internet gateway.
2. Does a security group allow TCP 22 from 0.0.0.0/0, attached directly or through the instance's launch template?

The CDK agent assembles this from raw describe calls and consistently misses the launch-template path, so it under-counts: 1 instead of 2. Every configuration that relied on CLI reasoning scored 0/3 here.

chant resolves the join in its typed graph. An enrichment folds two derived facts onto each instance node: `effectiveIngress`, the normalized ingress rules from all reachable security groups, direct and via launch template, and `internetFacing`, whether the subnet routes to an internet gateway. The whole question becomes one query a small model can run:

```
chant search "kind:EC2::Instance
              attr:internetFacing=true
              attr:effectiveIngress=tcp:22:0.0.0.0/0"
  --live --env floci --explain --show InstanceId
```

Output: the correct 2, including the launch-template instance the CLI path drops, with the `--explain` footer stating why each near-miss was excluded. The agent used this query on every ssh-reach trial, with zero fallback to the raw AWS CLI.

## The full board

Every configuration tested, fair set, k=3 per task:

| configuration | pass | valid | in-tok | out-tok | $ |
| --- | --- | --- | --- | --- | --- |
| Sonnet bare | 16 | 11/15 | 2.66M | 39k | 2.02 |
| Haiku bare | 12 | 9/15 | 2.85M | 44k | 0.81 |
| Haiku + CDK | 14 | 11/15 | 7.88M | 82k | 1.87 |
| Haiku + chant | 17 | 15/15 | 6.37M | 53k | 1.32 |

ssh-reach: CDK 0/3, Sonnet bare 0/3, chant 3/3.

## What the board says

chant uses 6.4M input tokens to CDK's 7.9M, and the fewest output tokens of any configuration. CLI analysis grows with the resource count. A scoped query stays roughly flat, so the gap should widen on larger estates.

The tasks that separate tools are multi-hop joins. The list and describe tasks saturate for everyone, bare Haiku included.

## Caveats

This is the quickstart tier. Three of the five fair tasks saturate, so the signal is thin. Real differentiation needs scenarios where joins are the norm.

## Methodology

aws-bench is a Harbor-based infrastructure-agent benchmark. This run: the ec2-multiregion scenario, locally against the [Floci](https://github.com/floci-io/floci) AWS emulator, $0 of real AWS. Haiku 4.5 fixed on every configuration, tooling the only variable, k=3 trials per task. The Sonnet-bare row is a stronger-model reference, not a comparator. chant's features here: `chant search` scoped estate queries, the `--explain` footer, multi-stack live identity, and the effective-topology enrichment. Floci needed four fidelity fixes to match real AWS for these tasks: subnet MapPublicIpOnLaunch, public IP gated on subnet, a cidr-block filter, and an aws-faithful private-IP toggle.

## Next

Run the enrichment on a harder scenario, compute-and-data or serverless, where multi-hop joins dominate. Expect the cost gap to widen and the accuracy lead to grow.

---

## Read more

- [Flame graphing the leftness of infra tooling](/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [TypeScript is the right choice for infra](/posts/typescript-is-the-right-choice-for-infra/)
- [aws-bench](https://github.com/lex00/aws-bench)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
