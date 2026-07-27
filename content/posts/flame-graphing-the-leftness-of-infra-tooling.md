---
title: "Flame graphing the leftness of infra tooling"
date: 2026-07-27
featured_image: "img/leftness-cover.svg"
---

Last month I claimed [chant](https://intentius.io/chant/) sits to the left of other infra toolchains when it comes to execution.

{{< figure src="/img/leftness-cartoon.svg" alt="Two bars. cdk synth: your code and its infrastructure library execute from almost the start until the plan exists. chant build: the tool reads your files like a recipe without cooking it, and your code never runs." >}}

To prove this claim, I wrote the same small app for both CDK and chant. Next, I verified both produce the same resources, and ran each tool with Node's profiler recording.

A recording reads from left to right, with time on the X axis. Every block is code that ran, and highlighted blocks are caused by *your* app, meaning your files, plus the infrastructure library they pull in.

Here are both runs, same recorder, same lighting rule:

{{< figure src="/img/leftness-pair.svg" alt="Two recorded timelines stacked. The cdk synth strip is mostly bright: user code and aws-cdk-lib executing from a marker near the left edge to the end. The chant build strip below is busy but uniformly dim: nothing qualifies as user code executing." >}}

The top strip is CDK. The yellow line near the left edge is your program starting, and from there the strip stays lit to the end. Everything CDK knows about your infrastructure, it learned by running your code and watching what it constructs. Zoom in and you can read it happening:

{{< figure src="/img/leftness-cdk-resource.svg" alt="A magnified section of the cdk synth recording showing constructor frames named ItemsStack, Table2, Role2 and Function2 highlighted." >}}

`Table2` is your database table. `Role2` is your IAM role. `Function2` is your Lambda. Each one came into existence because a constructor executed inside `cdk synth`. 

This is CDK's design. There is no way to know what a CDK app builds without running it, which means whatever your code does happens *before* the tool knows what it's looking at.

The bottom strip is chant, and it's just as busy, but nothing lights up. That's not a lucky sample from a profiler that happened to look away: the build refuses to finish unless it can account for every file without running it.

Don't take the pictures' word for it. Both recordings are live in [spicypath](https://github.com/INTENTIUS/spicypath), my profile viewer — no install, no login:

- [The CDK recording](https://spicypath.intentius.workers.dev/#eyJ2dCI6ImZsYW1lIiwibW9kZSI6ImNoYXJ0IiwicSI6ImZpbGU6Y2RrLWFwcCIsIm1rIjpbWzEwNTc1MTg3MzQ1OSwieW91ciBjb2RlIHN0YXJ0cyBoZXJlIiwiI2ZmNDQ0NCJdXSwic3JjIjoic2FtcGxlcy9sZWZ0bmVzcy1jZGstc3ludGguY3B1cHJvZmlsZSIsInNyY1R5cGUiOiJzYW1wbGUifQ==), with a marker on the moment your code starts.
- [The chant recording](https://spicypath.intentius.workers.dev/#eyJ2dCI6ImZsYW1lIiwibW9kZSI6ImNoYXJ0Iiwic3JjIjoic2FtcGxlcy9sZWZ0bmVzcy1jaGFudC1idWlsZC5jcHVwcm9maWxlIiwic3JjVHlwZSI6InNhbXBsZSJ9), where there is no such moment to mark.

One caveat, this works for code written in chant's supported style. Files that are deliberately programs still run, in a sandbox, with intention. What sits left of the execution line is exactly the part of your repo that describes infrastructure rather than computes it.

Everything regenerates from committed inputs and the procedure lives in [the harness](https://github.com/INTENTIUS/chant/tree/main/test/leftness). No timing numbers anywhere in it, on purpose. This is not a benchmark.

## Read more

- [The far-left IaC tool](/posts/the-far-left-iac-tool/) — the claim this post records
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) — the supported style that makes reading-without-running possible
- [spicypath](https://spicypath.intentius.workers.dev/) — the viewer, which also eats your pprof, JFR, and heap dumps
