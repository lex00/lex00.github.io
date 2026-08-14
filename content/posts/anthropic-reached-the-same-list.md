---
title: "Anthropic reached the same list"
date: 2026-08-14
featured_image: "img/anthropic-same-list-cover.svg"
draft: false
---

Anthropic published [how they secure an AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle). Claude writes roughly 80% of the code merged there, so no control that depends on a human reading everything survives. They run security reviews at planning, narrow review agents at CI, dynamic scans against staging, and an incident response agent with its own identity and limits.

[Accessible Ops](https://accessibleops.net) is fourteen principles for infrastructure operations, written for the same pressure from the other end. Most of what Anthropic describes lands on rows in that list.

Their governing rule, the Principle of Least Agency, draws hard boundaries around what an agent can access and do rather than relying on what it is told. chant is partway there. `chant build` imports your TypeScript and runs it, held safe only by lint rules. `chant build --fold` reduces the source to a value without executing the module, and `--sandbox` confines whatever falls back. Anthropic's rule is a good argument for making fold the default.

The rest of the mapping goes quickly. Their incident response agent can read production logs and post to channels but cannot deploy a fix; that takes a separate agent and a human. Rows VII and VIII, reversible before risky and escalate the judgment. Every agent gets a single-purpose identity with the minimum permission it needs: rows V and VI. Every approval, tool call, and agent-to-agent message lands in their SIEM, and agents talk in shared channels people can watch: row IX, attributable. Security guidance lives in CLAUDE.md files so the generating agent holds it while writing: row III, documentation is law. And their closing question, what would you run if scanning were nearly free, is row II. Put the check at the keystroke. They run review agents at pull request time; a compiler runs earlier and costs nothing to invoke.

The mapping has holes. Their architecture is heavily runtime: behavioral monitoring of agents, risk-weighted human sampling of automated approvals, new reviewers in shadow mode until they earn trust. chant is build time and has none of that.

This is no endorsement. Anthropic is describing its own internal tooling and is not writing about infrastructure at all. But two teams starting from different problems arrived at nearly the same rules for letting an agent near production, which suggests the list is the shape of the problem. The rule worth carrying into Accessible Ops is least agency. Boundaries on what a thing can do outlast instructions about what it should do.

---

## Read more

- [TypeScript is the right choice for infra](https://lex00.github.io/posts/typescript-is-the-right-choice-for-infra/)
- [Governance is what IaC depends on](https://lex00.github.io/posts/governance-is-load-bearing/)
- [Policy belongs left of the platform](https://lex00.github.io/posts/policy-belongs-left-of-the-platform/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Accessible Ops](https://accessibleops.net)
- [chant](https://intentius.io/chant/)
