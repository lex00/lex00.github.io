---
title: "aws-bench: chant vs Pulumi scenario 1"
date: 2026-07-29
featured_image: "img/aws-bench-s1-pulumi-cover.svg"
---

chant beats Pulumi on an infrastructure-agent benchmark.

Same model on both sides, Haiku 4.5, fixed. Same estate authored both ways, and both tools are TypeScript, so the difference is what the tool hands the agent. On aws-bench's task set chant scored 15/15 against Pulumi's 12/15, at 24% lower cost and 13% fewer tokens generated. The gap is the multi-hop questions.

{{< figure src="/img/aws-bench-s1-pulumi-table-headline.svg" alt="Metrics table. Tasks correct, Pulumi 12 of 15, chant 15 of 15. SSH reachability, 2 of 3 against 3 of 3. Public subnets, 1 of 3 against 3 of 3. Input tokens 7.27M against 6.37M. Output tokens 60.4k against 52.6k. Cost 1.76 against 1.33 dollars. The chant column is highlighted." >}}

## What Pulumi got wrong

find-in-public-subnets, 1/3 against 3/3. The answer is a route-table walk, instance to subnet to route table to a default route at an internet gateway, plus the account default VPC. Pulumi has the pieces in its state, and the agent does the join by hand from the export, getting it right one time in three. chant folds the walk into a single attribute on each instance, and the question becomes one query.

```
chant search "kind:EC2::Instance attr:internetFacing=true" --live --env floci
```

ssh-reachability is closer, 2/3 against 3/3. The instance is reachable on port 22 only through a security group attached via its launch template. Pulumi's state carries the launch template and its groups, so the agent resolves the hop most of the time. chant folds that too and answers 3/3.

Pulumi also costs more per question. `pulumi stack export` hands the model the whole estate every time, 7.27M input tokens against chant's 6.37M of scoped queries. More tokens, more cost, lower accuracy.

## The numbers

{{< figure src="/img/aws-bench-s1-pulumi-table-board.svg" alt="Board table, five tasks at k equals 3 per configuration. Haiku plus chant, highlighted, 15 of 15 correct, 6.37M in, 52.6k out, 1.33 dollars. Haiku plus Pulumi 12 of 15, 7.27M, 60.4k, 1.76." >}}

Pulumi gives the agent a real model, its applied state, with every resource and its resolved attributes. The data is all there and the joins are not. chant gives the agent a typed model with the joins already folded onto each node, so one scoped query answers each question.

Both models answer the easy questions. The typed one wins across the board and does it cheapest.

## Caveats

This is the quickstart tier. Three of the five tasks saturate, so the signal is thin. Real differentiation needs scenarios where joins are the norm.

## Methodology

aws-bench is an infrastructure agent benchmark built on Harbor. This run used the ec2-multiregion scenario against the [Floci](https://github.com/floci-io/floci) AWS emulator, so it cost nothing in real AWS. Haiku 4.5 ran both configurations, three trials per task, on a freshly wiped estate. Five tasks count. A sixth grades the IaC generator instead of the agent and is excluded for both sides.

The Pulumi side got what a real Pulumi shop would have. The applied program with `pulumi stack export` as the source of truth. The briefings match in wording and neither explains how to compute reachability. The agents work that out themselves.

Everything needed to rerun this is in [aws-bench](https://github.com/lex00/aws-bench) under `benchmarks/arms/pulumi-ec2-multiregion/`. The estate is a TypeScript port of the same six instances across three regions, and it deploys with plain `pulumi up` against the emulator.

## Next

Run the comparison on a harder scenario, compute-and-data or serverless, where multi-hop joins dominate. Expect the cost gap to widen and the accuracy lead to grow.

---

## Read more

- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [Flame graphing the leftness of infra tooling](/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [aws-bench](https://github.com/lex00/aws-bench)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
