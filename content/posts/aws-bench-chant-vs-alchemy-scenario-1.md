---
title: "aws-bench: chant vs Alchemy scenario 1"
date: 2026-07-29
featured_image: "img/aws-bench-s1-alchemy-cover.svg"
---

chant beats Alchemy on an infrastructure-agent benchmark.

Same model on both sides, Haiku 4.5, fixed. Same estate authored both ways, and both tools are TypeScript, so the difference is what the tool hands the agent. On aws-bench's task set chant scored 15/15 against Alchemy's 10/15, at 16% lower cost and 16% fewer tokens generated. The gap is the multi-hop questions, plus a failure mode none of the other tools produced.

{{< figure src="/img/aws-bench-s1-alchemy-table-headline.svg" alt="Metrics table. Tasks correct, Alchemy 10 of 15, chant 15 of 15. SSH reachability, 1 of 3 against 3 of 3. Public subnets, 1 of 3 against 3 of 3. Input tokens 7.42M against 6.37M. Output tokens 62.8k against 52.6k. Cost 1.59 against 1.33 dollars. The chant column is highlighted." >}}

## What Alchemy got wrong

ssh-reachability, 1/3 against 3/3. The agent gets the join right, both open instances, including the launch-template hop that sank CDK. Then it argues itself out of the answer. Floci's emulated public IPs read as loopback addresses, so the agent decides there is no valid internet connectivity and drops both. The join survives, the argument around it decays.

find-in-public-subnets, 1/3 against 3/3. The route-table walk, the same trap that took Terraform and Pulumi to the same score. chant folds both walks into attributes on each instance, and each question becomes one query.

```
chant search "kind:EC2::Instance attr:internetFacing=true" --live --env floci
```

Alchemy also pays more per question. Its state is one JSON file per resource under `.alchemy/`, and the agent reads the estate through them, 7.42M input tokens against chant's 6.37M of scoped queries.

## The Effect beta

James Ward called Alchemy's Effect line the best in this space, so it got its own run, pinned to `alchemy@2.0.0-beta.65`. It scored 4/15 at $1.39. A prior run of the same configuration landed 6/15. The low cluster is stable.

The failure is not reachability. It is the census. The Effect line has no native way to launch an instance from a launch template, so that instance became a custom resource with its own type name. Agents census an estate by grepping state for the exact resource type, so they silently count five of six instances, and every counting task decays with them. Trials that fell through to the live API passed. Trials that trusted the state census failed.

To rule out naming unfairness, the custom type was renamed into the `AWS.EC2.*` family between runs. It did not matter. Exact-match greps still miss it. The published line dodged the whole problem by accident. It has no native EC2 instance at all, so all six instances share one custom type and the census stays whole.

That is a sharper finding than the one the run was designed for. When a tool's resource surface has gaps, an owned state file doesn't just fail to fold joins. Its type census fractures, and the agent inherits the fracture.

## The numbers

{{< figure src="/img/aws-bench-s1-alchemy-table-board.svg" alt="Board table, five tasks at k equals 3 per configuration. Haiku plus chant, highlighted, 15 of 15 correct, 6.37M in, 52.6k out, 1.33 dollars. Haiku plus Alchemy 10 of 15, 7.42M, 62.8k, 1.59. Haiku plus Alchemy Effect beta 4 of 15, 5.73M, 61.5k, 1.39 dollars." >}}

The Effect row reads cheapest and lightest after chant. That is the fracture, not efficiency. It reads less because its census misses an instance.

Alchemy gives the agent the Pulumi shape, an executed TypeScript program with an owned state file. The data is mostly there and the joins are not. chant gives the agent a typed model with the joins already folded onto each node, so one scoped query answers each question.

Both models answer the easy questions. The typed one wins across the board and does it cheapest.

## Caveats

This is the quickstart tier. Three of the five tasks saturate, so the signal is thin. Real differentiation needs scenarios where joins are the norm.

Two Alchemy-specific caveats. Neither line could reach the emulator out of the box. The published provider has no endpoint override, filed upstream as [alchemy-run/alchemy#991](https://github.com/alchemy-run/alchemy/issues/991), and the Effect line has one in its API that nothing populates yet, so both runs carry small documented patches. And the Effect line is a fast-moving beta, so its score is a snapshot, not a verdict. Alchemy stays out of the scenario 1 rankings until v2 ships.

## Methodology

aws-bench is an infrastructure agent benchmark built on Harbor. This run used the ec2-multiregion scenario against the [Floci](https://github.com/floci-io/floci) AWS emulator, so it cost nothing in real AWS. Haiku 4.5 ran every configuration, three trials per task, on a freshly wiped estate. Five tasks count. A sixth grades the IaC generator instead of the agent and is excluded for both sides.

The Alchemy side got what an Alchemy shop would have. The applied program with its state as the source of truth, one JSON file per resource, committed like the Terraform workspace's state. The briefings match in wording and neither explains how to compute reachability. EC2 instances, launch templates, and instance profiles are not in the published provider outside its Cloud Control proxy, so the estate supplies them as custom resources written in the framework's own async style.

The Effect run pinned `alchemy@2.0.0-beta.65` with `effect@4.0.0-beta.102`, deployed as three per-region stacks because its environment is single-region, with one custom Effect-style provider for the launch-template instance and three documented patch sites. The estate was verified against the emulator before every run.

Everything needed to rerun both configurations lives in my fork, each with a REPRODUCE.md, linked at the bottom.

## Next

Rerun the Effect line when it leaves beta. Then the harder scenarios, compute-and-data or serverless, where multi-hop joins dominate. Expect the cost gap to widen and the accuracy lead to grow.

---

## Read more

- [aws-bench: scenario 1 wrap](/posts/aws-bench-scenario-1-wrap/)
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [aws-bench](https://github.com/aws-bench/aws-bench)
- [Reproduce the Alchemy run](https://github.com/lex00/aws-bench/blob/feat/alchemy-arm-handoff/benchmarks/arms/alchemy-ec2-multiregion/REPRODUCE.md)
- [Reproduce the Alchemy Effect run](https://github.com/lex00/aws-bench/blob/feat/alchemy-arm-handoff/benchmarks/arms/alchemy-effect-ec2-multiregion/REPRODUCE.md)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
