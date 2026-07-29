---
title: "aws-bench: chant vs Terraform scenario 1"
date: 2026-07-28
featured_image: "img/aws-bench-s1-tf-cover.svg"
---

chant beats Terraform on an infrastructure-agent benchmark.

Same model on both sides, Haiku 4.5, fixed. Same estate authored both ways. On aws-bench's task set chant scored 15/15 against Terraform's 13/15, at 39% lower cost and 36% fewer tokens generated. The gap comes down to one question. Which EC2 instances sit in public subnets?

{{< figure src="/img/aws-bench-s1-tf-table-headline.svg" alt="Metrics table. Tasks correct, Terraform 13 of 15, chant 15 of 15. SSH reachability, 3 of 3 both. Public subnets, 1 of 3 against 3 of 3. Input tokens 10.9M against 6.37M. Output tokens 82.6k against 52.6k. Cost 2.17 against 1.33 dollars. The chant column is highlighted." >}}

## What Terraform got wrong

find-in-public-subnets, 3/3 against 1/3. The answer is a route-table walk, instance to subnet to route table to a default route at an internet gateway, plus the account default VPC. The Terraform agent does that join by hand from the state JSON and gets it right one time in three. chant folds the walk into a single attribute on each instance, and the question becomes one query.

```
chant search "kind:EC2::Instance attr:internetFacing=true" --live --env floci
```

Terraform is also the most expensive configuration. `terraform show -json` hands the model the entire applied state on every question, 10.9M input tokens against chant's 6.37M of scoped queries. More tokens, more cost, lower accuracy.

## The numbers

{{< figure src="/img/aws-bench-s1-tf-table-board.svg" alt="Board table, five tasks at k equals 3 per configuration. Haiku plus chant, highlighted, 15 of 15 correct, 6.37M in, 52.6k out, 1.33 dollars. Haiku plus Terraform 13 of 15, 10.9M, 82.6k, 2.17." >}}

Terraform has a real model, untyped and unfolded. Its agent gets the data it needs but assembles joins by hand, winning the launch-template hop, fumbling the route-table walk, and paying the most tokens to read the dump. chant has a typed model with the joins already folded onto each node, so one scoped query answers each question.

Both models answer the easy questions. The typed one wins across the board and does it cheapest.

## Caveats

This is the quickstart tier. Three of the five tasks saturate, so the signal is thin. Real differentiation needs scenarios where joins are the norm.

## Methodology

aws-bench is an infrastructure agent benchmark built on Harbor. This run used the ec2-multiregion scenario against the [Floci](https://github.com/floci-io/floci) AWS emulator, so it cost nothing in real AWS. Haiku 4.5 ran both configurations, three trials per task. Five tasks count. A sixth grades the IaC generator instead of the agent and is excluded for both sides.

The Terraform side got what a real Terraform shop would have. An applied workspace with `terraform show -json` and `terraform state list`. The briefings match in wording and neither explains how to compute reachability. The agents work that out themselves.

Everything needed to rerun this is in [aws-bench](https://github.com/lex00/aws-bench) under `benchmarks/arms/terraform-ec2-multiregion/`. The estate is an HCL port of the same six instances across three regions, and the agent runs a real terraform binary in the container.

## Next

Run the comparison on a harder scenario, compute-and-data or serverless, where multi-hop joins dominate. Expect the cost gap to widen and the accuracy lead to grow.

---

## Read more

- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [Flame graphing the leftness of infra tooling](/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [aws-bench](https://github.com/lex00/aws-bench)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
