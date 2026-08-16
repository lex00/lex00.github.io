---
title: "Onboardable"
date: 2026-07-23
draft: true
---

Every argument about AI agents in operations gets easier once you stop treating the agent as special. An agent is the newest hire. It reads what is written, works through the paths you give it, touches what its credentials allow, and asks when it is unsure. The uncomfortable part is that a lot of infrastructure was not safe to hand a new hire either. That was easy to miss, because new hires are slow and cautious and there were rarely many of them at once.

Jake Gaylor put the test plainly in [Agent-Ready Infrastructure](https://jakegaylor.com/blog/posts/agent-ready-infrastructure/). Could a competent stranger operate your system on day one, using only what is written down, through paths you can review, with consequences you can survive? That is an onboarding test, and it does not care whether the stranger is a person or a model. The properties that make a new engineer productive and safe in week one are the properties that make an agent safe. Agents and people both have to onboard.

I am wary of the phrase agentic ops. An agent reading an error and picking a tool is the old kind of operation done faster, with the judgment calls easier to surface to a human. What I want to know is which properties keep the judgment with the human and make the rest safe to delegate.

I started listing those properties at the end of a post and the list kept outgrowing the post. It lives at [accessibleops.net](https://accessibleops.net) now, fourteen of them, in the format borrowed from 12factor.net.

Synthesis, I through III, is what the stranger can work out before anything runs. [Honor the lower layer](https://accessibleops.net/honor-the-lower-layer/) so the thing they read is the thing that ships. [The same check, left of the commit](https://accessibleops.net/correctness-left-of-the-commit/) so the editor's red squiggle and the agent's language server give the same answer at the same keystroke. [Documentation is law](https://accessibleops.net/documentation-is-law/) for the parts a machine cannot infer, like why the database sits in that region.

Ops and lifecycle, IV through X, is what happens when a change meets a live system. One path to prod, named secrets under least privilege, bounded blast radius, reversible before risky, escalate the judgment, attributable, and rotation cheap enough that you actually do it.

Truth and trust, XI through XIV, came out of arguments about where authoritative state belongs. The live system is the truth, adopt in place, manage only what you declare, verify the artifact.

Two things the list will not do.

It names no product, anywhere in the spec text. Every factor is written so a shop with discipline can reach it with whatever tooling it already runs. A spec that names a product is an ad, and nobody else can adopt an ad. There is a [scorecard](https://accessibleops.net/scorecard/) that does name tools, kept separate on purpose, and every tool on it is a peer column.

It also does not stop at day one. The onboarding test sounds like a first-week question and the synthesis band reads that way, but the lifecycle band is the second job, the one that starts after a change is authored and has to apply against something running. [The two halves of day two](https://accessibleops.net/blog/two-halves-of-day-two/) is the argument for why one test covers both.

Jake's competent stranger and the list are the same idea from two sides. Build the system so a stranger can operate it on day one, and you have built the system an agent can operate on every day after.

---

## Read more

- [Agent-Ready Infrastructure](https://jakegaylor.com/blog/posts/agent-ready-infrastructure/) — Jake Gaylor
- [Accessible Ops](https://accessibleops.net)
- [The two halves of day two](https://accessibleops.net/blog/two-halves-of-day-two/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
