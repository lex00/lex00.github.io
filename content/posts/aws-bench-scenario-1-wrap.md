---
title: "aws-bench: scenario 1 wrap"
date: 2026-07-31
featured_image: "img/aws-bench-s1-wrap-cover.svg"
aliases:
  - /posts/aws-bench-chant-vs-cdk-scenario-1/
  - /posts/aws-bench-chant-vs-terraform-scenario-1/
  - /posts/aws-bench-chant-vs-pulumi-scenario-1/
  - /posts/aws-bench-chant-vs-alchemy-scenario-1/
---

Scenario 1 is done. aws-bench puts an agent in front of a live AWS estate and grades its answers.

Six configurations ran it on the same model, Haiku 4.5: chant, Pulumi, Terraform, AWS CDK, Alchemy, and an agent holding nothing but the AWS CLI. Eight questions, three attempts each, 24 trials apiece, against six EC2 instances spread over three regions.

## The results live on chant-bench

I used to keep a post per matchup. That stopped working the first time I re-ran the benchmark and half the numbers moved, so the results now live where they are generated.

[chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/) publishes every run: the score, the per-question breakdown, what each agent actually ran to get its answer, what it cost, and the logs. A run whose tooling broke is published as invalid rather than as a low score.

This post quotes one named run per configuration, `chant-m1`, `bare-m3`, `pulumi-m1`, `terraform-m1`, `cdk-m1`, and `alchemy-m3`. The site carries the replicates too, including the ones that disagree with these.

{{< figure src="/img/aws-bench-s1-wrap-table-metrics.svg" alt="Board table ranked by cost per correct answer, eight questions at k equals 3, tokens per question. chant 22 of 24 correct, 0.033 dollars per correct answer, 111k in, 2.1k out, marked unranked, wins all. no tool, the aws cli baseline, 17 of 24, 0.050, 108k, 2.7k, with crowns for cost, input and output. pulumi 19 of 24, 0.086, 282k, 3.9k. terraform 19 of 24, 0.111, 357k, 4.8k. aws cdk 17 of 24, 0.120, 318k, 5.6k. alchemy 20 of 24, 0.123, 515k, 5.3k, with a crown for correct." >}}

## The baseline is the story

The board is ranked by what a correct answer costs, and an agent with no infrastructure tooling at all comes second.

Bare AWS CLI answers 17 of 24 at five cents per correct answer. Pulumi is the best of the real toolchains on that measure and costs $0.086. Terraform, CDK, and Alchemy all cost more than twice the baseline. CDK matches the baseline's score exactly, 17 of 24, for 2.4 times the money.

chant is the only configuration that comes in under an agent holding nothing.

I want to be careful about what that does and does not say. Three of the toolchains are more accurate than the baseline, and accuracy is the thing you are actually buying. Pulumi and Terraform each add two correct answers over bare, Alchemy adds three. The finding is not that the tools fail. It is that on this scenario they charge a large premium for a small accuracy gain, and nobody has been measuring the premium.

## Where a tool actually earns it

One question separates the baseline from everything else. Asked which instances are reachable on port 22 from the internet, the bare agent scored 0 out of 3. chant, Pulumi, Terraform, and CDK all scored 3 out of 3, and Alchemy 2 out of 3.

The answer is two instances, and one of them is only reachable through a security group attached via its launch template. An agent walking describe calls by hand does not find that hop. A tool that keeps a model of the estate does, whether the model is a state file or a typed graph.

That is one question out of eight, and it is the clearest thing any tool bought anyone in this run.

## The question nobody answers

The eighth question is unused security groups, and there the whole field reads close to zero. Pulumi, Terraform, CDK, Alchemy, and the bare agent all went 0 for 3. chant went 1 for 3, which is the best score on the board and still mostly a miss.

The reason it is hard is that the answer is a negative. Four groups are attached to nothing, and establishing that means proving no instance and no interface in any of the three regions references them. Every other question can be answered by finding things. This one can only be answered by finishing a sweep.

It says the same thing about all six configurations: none of them makes an exhaustive negative cheap.

## chant is not perfect

22 of 24, and the two misses are on that same question.

I would rather publish that than a clean sweep, because a benchmark I always win is a benchmark I built wrong. The runs behind this post include chant scoring 21, 22, 23, and 24 on the same estate. Three attempts per question is not enough to pin a number down, and the site shows the spread instead of hiding it.

What holds steady across every replicate is the cost. chant answers a question for about a third of the tokens of the cheapest real toolchain, in 2.6 commands against Pulumi's 7.8 and Alchemy's 14.4, and it does it without reading the account at all.

## The benchmark is not mine

[aws-bench](https://github.com/aws-bench/aws-bench) open sourced the harness, the estate, the questions, and the reference answers. What is mine is a fork that runs it against an emulator, one deployment per toolchain, and the gates that decide whether a run counts at all.

Everything runs against the [Floci](https://github.com/floci-io/floci) emulator, so a full pass costs nothing in real AWS.

## Losing to chant is no shame

chant is an infra compiler, and it was built to be at the top of this benchmark. With a typed graph, folded joins, and scoped queries, it answers in one query what the others assemble by hand. That is the whole design, aimed directly at this.

The cost column is the part I would pay attention to. Accuracy converges as the models get better. Token cost does not.

## How chant was born

Have you ever lost a chunk of your humanity untangling a state hairball that got handed down to you from a previous owner? Found yourself asking why opaque layers of infra tooling seem to pop up everywhere?

I have...

I started chant as a Python prototype in December 2025 because I knew this result was mine for the taking if I could finish it fast enough. A Go rewrite came next, then TypeScript, where it has stayed because it's the most 1:1 for cloud specs. chant's first commit is February 18, 2026, five months before this run.

chant is 100% prompted. It's a scope of work I simply could not have delivered alone without AI.

## Next

Alchemy v2, the Effect line, is the one gap left on this scenario. It will show up on the results page when it runs. Formae and ConfigHub after that.

Then the harder scenarios, compute-and-data and serverless, where multi-hop joins are the norm rather than one question out of eight. That is where the baseline should fall away, and where I expect the cost gap to widen.

---

## Read more

- [Scenario 1 results on chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/) — every run, per question, with the commands each agent ran
- [chant-bench](https://intentius.io/chant-bench/) — how the runs are gated and what gets published
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [TypeScript is the right choice for infra](/posts/typescript-is-the-right-choice-for-infra/)
- [aws-bench](https://github.com/aws-bench/aws-bench)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
