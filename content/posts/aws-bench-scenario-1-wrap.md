---
title: "aws-bench: scenario 1 wrap"
date: 2026-07-29
featured_image: "img/aws-bench-s1-wrap-cover.svg"
---

Scenario 1 is done. aws-bench puts an agent in front of a live AWS estate and grades its answers. Three matchups, [CDK](/posts/aws-bench-chant-vs-cdk-scenario-1/), [Terraform](/posts/aws-bench-chant-vs-terraform-scenario-1/), and [Pulumi](/posts/aws-bench-chant-vs-pulumi-scenario-1/), each against chant, same model, Haiku 4.5.

## The benchmark is open source

This benchmark is not mine. [aws-bench](https://github.com/aws-bench/aws-bench) open sourced the harness and the scenarios. The configurations I ran live in my fork, each with a REPRODUCE.md, linked at the bottom. Everything runs against the [Floci](https://github.com/floci-io/floci) emulator, for free.

## This is the beginning

Scenario 1 is the quickstart tier. It separates tools on two questions that are both multi-hop joins.

Harder scenarios combining compute, data, and serverless are coming next. I expect chant to do even better with more complexity.

## Losing to chant is no shame

chant is an infra compiler, and it was built to be at the top of this benchmark.

With a typed graph, folded joins, and scoped queries, chant answers in one query what the others assemble by hand.

## The metrics

{{< figure src="/img/aws-bench-s1-wrap-table-metrics.svg" alt="Board table with a wins column of crowns. chant, 15 of 15, 1.33 dollars, 6.4M in, 53k out, marked unranked, wins all. Pulumi, 12 of 15, 1.76, 7.3M, 60k, three crowns for cost, input, and output. Terraform, 13 of 15, 2.17, 10.9M, 83k, one crown for tasks correct. AWS CDK, 11 of 15, 1.87, 7.9M, 82k, no wins." >}}

## How chant was born

Have you ever lost a chunk of your humanity untangling a state hairball that got handed down to you from a previous owner? Found yourself asking why opaque layers of infra tooling seem to pop up everywhere?

I have...

I started chant as a Python prototype in December 2025 because I knew this result was mine for the taking if I could finish it fast enough. A Go rewrite came next, then TypeScript, where it has stayed because it's the most 1:1 for cloud specs. chant's first commit is February 18, 2026, five months before this run.

chant is 100% prompted. It's a scope of work I simply could not have delivered alone without AI.

## Next

Formae and ConfigHub runs are coming, along with more scenarios.

---

## Read more

- [aws-bench: chant vs CDK scenario 1](/posts/aws-bench-chant-vs-cdk-scenario-1/)
- [aws-bench: chant vs Terraform scenario 1](/posts/aws-bench-chant-vs-terraform-scenario-1/)
- [aws-bench: chant vs Pulumi scenario 1](/posts/aws-bench-chant-vs-pulumi-scenario-1/)
- [aws-bench](https://github.com/aws-bench/aws-bench)
- [Reproduce the chant run](https://github.com/lex00/aws-bench/blob/feat/emulator-floci/benchmarks/arms/chant-ec2-multiregion-search-v2/REPRODUCE.md)
- [Reproduce the Terraform run](https://github.com/lex00/aws-bench/blob/feat/emulator-floci/benchmarks/arms/terraform-ec2-multiregion/REPRODUCE.md)
- [Reproduce the Pulumi run](https://github.com/lex00/aws-bench/blob/feat/emulator-floci/benchmarks/arms/pulumi-ec2-multiregion/REPRODUCE.md)
- [chant](https://intentius.io/chant/)
