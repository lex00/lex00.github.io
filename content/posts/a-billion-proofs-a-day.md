---
title: "A billion proofs a day"
date: 2026-08-15
draft: false
---

Amazon's Automated Reasoning Group just published [a decade of reflections](https://www.amazon.science/blog/a-decade-of-mathematical-certainty-reflections-on-the-automated-reasoning-group).

It's the story of a decade spent proving AWS correct. Their policy engine Zelkova answers [a billion SMT queries a day](https://www.amazon.science/blog/a-billion-smt-queries-a-day) about what policies permit. Every one of these queries happens after the artifact exists.  The queries are against normal JSON that nothing upstream cleans up or constrains.

CDK has a miniature version of this. It runs a risky statement merge at synth, so a machine-checked [Alloy model](https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-iam/docs/policy-merging.als) in the repo proves the merge algorithm safe in advance.

To the left of CDK is an infra compiler named [chant](https://intentius.io/chant/). Zelkova is at the far right, answering questions about existing artifacts.

chant features synthesis as a pure function of the source. Every output value traces to a literal, a constant, or a reference. You ship an artifact that is typed, linted, planned, and signed.

None of chant's guarantees are a formal proof.  Types cannot answer what a policy permits. The output is spec-native JSON though, so Zelkova's own tooling can check it directly. A wrapper with its own representation would need its own Zelkova.

Now stop and consider how every property chant catches at the keystroke is one less query for Zelkova.

To see a visual of this, check out my blog about [flame graphing the leftness of infra tooling](https://lex00.github.io/posts/flame-graphing-the-leftness-of-infra-tooling/).

---

## Read more

- [Infrastructure deserves a compiler](https://lex00.github.io/posts/infrastructure-deserves-a-compiler/)
- [Flame graphing the leftness of infra tooling](https://lex00.github.io/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Which infrastructure tool actually keeps the spec?](https://lex00.github.io/posts/which-tool-keeps-the-spec/)
- [chant](https://intentius.io/chant/)
