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

Six configurations ran it on the same model Haiku 4.5. Those were chant and Pulumi and Terraform and AWS CDK and Alchemy and an agent holding nothing but the AWS CLI. Eight questions, three attempts each, 24 trials apiece, against six EC2 instances spread over three regions.

## The results live on chant-bench

I used to keep a post per matchup. That stopped working the first time I re-ran the benchmark and half the numbers moved, so the results now live where they are generated.

[chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/) publishes every run. Each one carries the score and per-question breakdown along with what the agent ran and what it cost and the logs. A run whose tooling broke is published as invalid rather than as a low score.

The table below lists each configuration's three most recent runs that passed every gate, and ranks on the middle one. Everything else in this post is aggregated over every valid run each configuration has: 26 for chant, 6 to 8 for the others, 1,584 trials in total. I have rewritten this post's numbers three times because I quoted single runs, and three attempts at a question does not pin one down. These configurations move about three trials in 24 between identical runs.

{{< figure src="/img/aws-bench-s1-wrap-table-metrics.svg" alt="Board table ranked by cost per correct answer over eight questions at k equals 3 with tokens per question. chant scores 22 and 24 and 22 correct at 0.033 dollars per correct answer with 125k in and 2.1k out and is marked unranked while winning all. The aws cli baseline with no tool scores 18 and 16 and 19 at 0.050 with 124k and 2.8k and crowns for cost and input and output. pulumi scores 17 and 18 and 18 at 0.089 with 262k and 4.0k. terraform scores 19 and 20 and 19 at 0.099 with 351k and 4.1k and a crown for correct. aws cdk scores 13 and 18 and 15 at 0.133 with 330k and 5.4k. alchemy scores 19 and 15 and 14 at 0.158 with 485k and 5.2k." >}}

## The baseline is the story

The board is ranked by what a correct answer costs, and an agent with no infrastructure tooling at all comes second.

Bare AWS CLI answers at about five cents per correct answer. Pulumi is the best of the real toolchains on that measure and costs $0.089, and CDK and Alchemy both cost more than twice the baseline. Terraform sits just under twice.

chant is the only configuration that comes in under an agent holding nothing.

I want to be careful about what that does and does not say. Accuracy is the thing you are actually buying, and over every run on record the baseline answers 72% of trials correctly. The best of the field is Terraform at 81% with Pulumi at 77%. CDK is at 70% and Alchemy 67%, which puts both below an agent with no infrastructure tooling at all while costing two to three times as much.

The finding is not that the tools fail. Terraform buys you nine points of accuracy over the baseline, and on a real estate that is worth paying for. It is that the premium is large, it varies by a factor of three across tools that look interchangeable from the outside, and nobody has been measuring it.

## Where a tool actually earns it

One question separates the baseline from everything else. Asked which instances are reachable on port 22 from the internet, the bare agent has now scored 0 out of 18. Not low. Zero, every time it has been asked.

Pulumi gets it 96% of the time, Terraform 95%, chant 85%, CDK 71%. Alchemy manages 19%.

The answer is two instances, and one of them is only reachable through a security group attached via its launch template. An agent walking describe calls by hand does not find that hop, and eighteen attempts have not found it once. A tool that keeps a model of the estate does whether that model is a state file or a typed graph.

That is one question out of eight, and it is the clearest thing a toolchain buys anyone here.

## The question nobody answers

The eighth question is unused security groups, and it is the one place the board turns over.

Pulumi, Terraform and CDK have never answered it. Not once, across 66 attempts between them. Alchemy has managed it once in 21. The bare agent gets it 28% of the time, and chant 51%.

The two configurations that do best here are the one with a query engine and the one with no tooling at all. Every arm that keeps a state file is at zero.

The reason is that the answer is a negative, and it is a negative about things the state file does not contain. Four groups are attached to nothing, so they are not referenced by any instance a state file knows about. Reading your own state tells you what you built, and the question asks what nothing points at. An agent with the raw API at least has the option of sweeping every group in every region and checking each one; it is expensive and it works about a quarter of the time. An agent reading Terraform state is looking in a place the answer cannot be.

That is worth more than the two points of accuracy it costs on the scoreboard, because it is the shape of a whole class of real questions. What is unattached, what is unreferenced, what is safe to delete.

## chant is not perfect

The three runs in the table are 22 and 24 and 22 and the middle one is what ranks. Across 26 runs it averages 88% and has scored anywhere from 15 to 24. On the unused security groups question it is right about half the time, which is the best on the board and still a coin flip. A benchmark I always win is a benchmark I built wrong, so the site publishes every replicate including the ones that undercut this post.

What holds steady across every replicate is the cost. chant answers a question in under 3 commands against Pulumi's 7 and Alchemy's 14, for roughly a third of the tokens the average toolchain spends, and it does it without reading the account at all.

## The benchmark is not mine

[aws-bench](https://github.com/aws-bench/aws-bench) open sourced the harness and the estate and the questions and the reference answers. What is mine is a fork that runs it against an emulator with one deployment per toolchain and the gates that decide whether a run counts at all.

Everything runs against the [Floci](https://github.com/floci-io/floci) emulator, so a full pass costs nothing in real AWS.

## Losing to chant is no shame

chant is an infra compiler, and it was built to be at the top of this benchmark. With a typed graph and folded joins and scoped queries it answers in one query what the others assemble by hand. That is the whole design, aimed directly at this.

The cost column is the part I would pay attention to. Accuracy converges as the models get better. Token cost does not.

## How chant was born

Have you ever lost a chunk of your humanity untangling a state hairball that got handed down to you from a previous owner? Found yourself asking why opaque layers of infra tooling seem to pop up everywhere?

I have...

I started chant as a Python prototype in December 2025 because I knew this result was mine for the taking if I could finish it fast enough. A Go rewrite came next, then TypeScript, where it has stayed because it's the most 1:1 for cloud specs. chant's first commit is February 18, 2026, five months before this run.

chant is 100% prompted. It's a scope of work I simply could not have delivered alone without AI.

## Next

Alchemy v2 (the Effect line) has since run and is [on the results page](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/). I have left it off the board above because this post was written around six configurations and I would rather add it properly than bolt a row on. Formae and ConfigHub next.

Then the harder scenarios, compute-and-data and serverless, where multi-hop joins are the norm rather than one question out of eight. That is where the baseline should fall away, and where I expect the cost gap to widen.

---

## Read more

- [Scenario 1 results on chant-bench](https://intentius.io/chant-bench/aws-bench/ec2-multiregion/results/) lists every run per question with the commands each agent ran
- [chant-bench](https://intentius.io/chant-bench/) explains how the runs are gated and what gets published
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [TypeScript is the right choice for infra](/posts/typescript-is-the-right-choice-for-infra/)
- [aws-bench](https://github.com/aws-bench/aws-bench)
- [Floci](https://github.com/floci-io/floci)
- [chant](https://intentius.io/chant/)
