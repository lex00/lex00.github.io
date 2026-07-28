---
title: "Anthropic reached the same list"
date: 2026-07-26
featured_image: "img/anthropic-same-list-cover.svg"
draft: true
---

Anthropic published [how they secure an AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle). Claude writes roughly 80% of the code that gets merged there. At that ratio, any control that depends on a human reading everything has already stopped working.

So they built controls that scale instead. Automated project security reviews at planning. Specialized review agents at CI, each scoped narrowly, with separate blindspots. Continuous dynamic scans against staging. An incident response agent with its own identity and its own limits.

I keep [fourteen principles](https://accessibleops.net) for infrastructure operations, written for the same pressure from the other end. Most of their controls land on my rows.

## Least agency

Their governing rule is to draw hard boundaries around what an agent can access and do, rather than around what it is told. They call it the Principle of Least Agency.

That distinction is the one worth carrying home. An instruction is a request the system can decline to honor. A boundary is a property of the thing.

It is also the argument chant is having with itself right now. `chant build` imports your TypeScript and runs it, and what keeps that safe is the evaluability lint rules. Lint is an instruction. `chant build --fold` reduces the source to a value without executing the module, and `chant build --sandbox` locks down filesystem, process spawn, and environment for whatever falls back. Those are boundaries.

I have written before that a configuration language like Pkl gets this property by construction, because the capability to execute is absent from the language, and that chant is chasing it rather than born with it. Anthropic reached the same rule from an unrelated problem. That is a good reason to move fold from a flag toward the default.

## Where the rows line up

Their incident response agent can read production logs, write documentation, and post to channels. It cannot deploy a fix. Deploying requires a separate agent and a human. That is row VII, reversible before risky, and row VIII, escalate the judgment, built at the code layer.

Every agent gets a single-purpose identity carrying the minimum permission it needs, and the authority to diagnose is split from the authority to deploy. Rows V and VI, named secrets and bounded blast radius.

Approvals, tool calls, and agent-to-agent messages all route to their SIEM with the reasoning signal attached. Agents talk to each other in shared channels where people can watch. Row IX, attributable, and a stronger version of it than most teams run on humans.

Security guidance lives in CLAUDE.md files and organizational skills, so the generating agent holds it while writing rather than meeting it at review. Row III, documentation is law. Their framing is that an agent cannot absorb what was never written down, which is the same reason the row exists.

Fourteen rows written for infrastructure. A security team at another company built most of the same list for code, working on a different problem, in a different vocabulary.

## Free scanning already has an answer

Their closing reframe is the best line in the post. The useful question is what you would run if scanning were nearly free.

Row II answers it. A change proves itself at the keystroke, with the same check for a human and an agent. When the check is a type and a lint rule in the editor, scanning is free and universal already, and it runs before the code exists in a branch.

Their version runs specialized agents at pull request time. Mine runs a compiler at authoring time. Both are correct, at different distances from the keystroke, and the compiler is cheaper where it reaches because a type system costs nothing to invoke.

The reason I care about the distinction is agents. An agent that writes chant source gets the same red squiggle a person gets, from the same language server, before anything is proposed. That is the cheapest possible place to catch it.

## Where chant stops

Their architecture is heavily runtime, and mine is heavily build time. Reading their post makes the gap legible.

They run continuous dynamic scans against staging to catch logic vulnerabilities that only appear across components. They treat agents as a new class of insider threat and alert when one deviates from its normal pattern. They sample automated approvals by risk weight and keep humans in a third of them. New reviewers run in shadow mode, posting comments for human approval until they earn trust.

chant has none of that. The lifecycle layer covers deployment and observation through Ops and WatchOp, and there is no SIEM story, no behavioral monitoring of agents, and no graduated-trust path for automation. Their use of several narrow reviewers with deliberately different blindspots is also a different shape from lexicon lint, which is rules rather than agents.

Those are real gaps and I would rather name them than let a mapping paper over them.

## The size of the claim

Anthropic is not writing about chant, or about these principles, or about infrastructure. They are describing what they run internally to secure their own development, and the tooling they name is their own.

So this is not an endorsement and it would be dishonest to present it as one.

The claim is narrower. Two teams, working on different problems, arrived at nearly the same set of rules for letting an agent touch production. They got there from application security with a model writing most of the code. I got there from infrastructure operations with the same pressure arriving a little later. When a list shows up twice, from two directions, it is more likely to be the shape of the problem than the taste of the person who wrote it.

The one rule I would take from their side to mine is least agency. Boundaries on what a thing can do outlast instructions about what it should do, and that applies to a coding agent and a build step equally well.

---

## Read more

- [TypeScript is the right choice for infra](https://lex00.github.io/posts/typescript-is-the-right-choice-for-infra/)
- [Governance is what IaC depends on](https://lex00.github.io/posts/governance-is-load-bearing/)
- [Policy belongs left of the platform](https://lex00.github.io/posts/policy-belongs-left-of-the-platform/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Accessible Ops](https://accessibleops.net)
- [chant](https://intentius.io/chant/)
