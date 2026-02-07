---
title: "Finding Root Causes with Spec Driven Research"
date: 2026-02-07
---

Spec driven research means producing a document at each phase of an investigation before moving to the next one. Each spec records what was tried, what was ruled out, and where to look next. [chant](/chant/) enables this through structured workflows where specs are the primary output, not code. The specs persist in git, so investigation progress doesn't decay between sessions or contributors.

I used the [chant OSS maintainer workflow](/chant/guides/oss-maintainer-workflow/) to untangle Zed [#38109](https://github.com/zed-industries/zed/issues/38109), "Zed out of sync with changes made outside of editor." 71 comments across every platform, at least six distinct bugs sharing one umbrella. Contributors had opened PRs for sub-problems, but the core cross-platform cause was still unidentified.

## The specs

**Comprehension** sorted the comments into clusters. Not one bug, at least six sharing symptoms but not causes.

**Reproducibility** designed a test that isolated the exact timing window. The bug is a race condition during file writes that won't surface in manual testing.

**Root cause** traced the problem to a single comparison in `buffer.rs` that checks only mtime, not file size. Each eliminated layer was documented in the spec.

**Sprawl** cataloged the other bugs in the umbrella, assessed existing PRs, and identified what still needed work. One confusing mega-issue became a table of six discrete problems.

## The fix

[PR #48691](https://github.com/zed-industries/zed/pull/48691) adds file size to the reload comparison so changes get caught even when timestamps collide.

## What worked

The issue had been open for months with plenty of attention and no single root cause. Each spec narrowed the search. Failed hypotheses got recorded and pointed toward the next one. Six specs later, the gate was exposed and the fix was small.

In a long-running issue thread, context decays with every new comment. The specs kept it durable.

&nbsp;

---

[chant](https://github.com/lex00/chant) is an agentic coding framework. The [OSS maintainer workflow](/chant/guides/oss-maintainer-workflow/) used here is one of several built-in workflows for spec-driven research and contribution.
