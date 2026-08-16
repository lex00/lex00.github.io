---
title: "An agent with no credentials"
date: 2026-08-09
draft: true
---

Most arguments about letting an agent touch production are arguments about the model. Is it good enough, how often is it confidently wrong, what happens on the bad day. Those are fair questions and they are a poor foundation, because the answer moves every few months and your security review does not.

There is another place to put the boundary. Give the agent no cloud credentials at all, and make the only artifact it can produce typed source. It cannot call an API because it holds no key to call one with. It can write a file. Everything after the file is a machine reading it.

What you review then is a diff that a compiler has already had a pass at.

## What the compiler gets to say no to

Types go first, and they end the whole class of failure where a field name is invented or a value is the wrong shape. That is the cheap half.

Semantic lint is the interesting half, because it is a different question. Types say the manifest is well formed. The rules say a well-formed manifest is still a bad idea: a workload with write access and unrestricted egress, a resource carrying no ownership marker, a secret read out of an environment variable. chant ships 128 of those rule modules across 14 lexicons today. They are accumulated judgement about what a coherent change looks like, written down once and applied to every change after, which is the part a prompt cannot do for you.

Then the change set, computed against the live system rather than a state file. That distinction earns its keep here more than anywhere else. An agent proposing changes against a stale record proposes plausible nonsense, and the staleness does not show up in review. Ownership markers sit on the live resource, so a delete needs the resource to be both owned and undeclared before anything removes it.

Last, the gate. A change can clear all of the above and still be one a person should see. A chant gate is a step in a workflow that compiles to Temporal, so it holds for days across restarts with nobody babysitting a process.

## The part that already runs

`examples/alert-triage` in the chant repo is the capstone of the teaching examples, and it wires the shape end to end. A webhook takes an alert. A Temporal workflow classifies it, gathers context, and proposes a remediation. Safe ones go straight through. Risky ones wait on a human signal for twelve hours, and if nobody answers they are held rather than applied. A second event source runs `chant lifecycle plan --json` and feeds every drifted resource into the same path.

What is stubbed should be said plainly. The proposal is a summary and a risk flag, not chant source, and the apply activity is deliberately a stub. The example exists to demonstrate the boundary between proposed and executed, and a gate that survives a restart, and it does that. The step where the agent's own output is typed source is the step not yet wired.

## Why bother

An agent holding credentials is bounded by its own judgement, and you audit it afterward by reading a transcript. An agent holding none is bounded by what a type checker, a lint pass, an ownership marker, and a gate will pass, and you audit it beforehand by reading a diff. Only the second one gives a security team something mechanical to sign.

The eighth Accessible Ops property is [escalate the judgment](https://accessibleops.net/escalate-the-judgment/): the newcomer executes, and the human owns the call that matters. An agent that can only emit source is the mechanical form of it. The judgment reaches a person because a rule fired, not because the agent chose to ask.

---

## Read more

- [Escalate the judgment](https://accessibleops.net/escalate-the-judgment/) — Accessible Ops VIII
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [alert-triage tutorial](https://intentius.io/chant/tutorials/alert-triage-local/)
