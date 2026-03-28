---
title: "The consolidation problem"
date: 2026-03-28
---

The pull request didn't start as a bureaucratic institution. It started because someone needed a way to propose changes to code they didn't own. The only mechanism for that was to ask the owner. The queue, the approval chain, the blocked deploy: none of it was planned. It followed from that one fact.

The person holding the key usually didn't ask for the job. A senior engineer merges things because she has the access and nobody else does. She goes on vacation and the team waits. She burns out and the PRs pile up. She never wanted to be a gatekeeper. The tool made her one.

---

The same logic plays out everywhere, just more slowly.

A company runs one package registry because running multiple is an ops burden. Someone has to own it. That team gets a queue of publishing requests. They write a policy. The policy needs enforcement. A year later there's a committee. Nobody scheduled the committee. It materialized because ownership needs stewardship and stewardship needs process.

Repositories accumulate unrelated code because starting a new one costs something real. Not money. Time, coordination, the two-hour conversation about which team owns this one, the CI configuration that needs to be copied and modified, the access control request that needs to be filed. The path of least resistance is the repo that's already set up. So a service ends up next to a CLI tool next to a shared library next to three things nobody can quite name.

Deployment pipelines become political the same way. When a pipeline is shared infrastructure, its owners become the final word on when and how things ship. They didn't volunteer for that authority. It came with the ownership of the resource.

---

The pattern is the same in each case. When the cost of creating a new unit is high enough, people reuse existing ones. Reused units become shared resources. Shared resources need owners. Owners become gates.

The unit cost doesn't have to be high in absolute terms. It just has to be high enough that the default is to reuse rather than create. A few hours of setup is enough. A single approval step is enough. Anything that makes starting a new thing feel heavier than adding to an existing one will produce consolidation, reliably, across teams and organizations and ecosystems.

---

The usual response is cultural. Keep the review queue short. Don't let any one person become a bottleneck. Ship smaller things more often. These are good practices. They also require constant maintenance because they work against the structure of the tools rather than with it.

The bottleneck keeps forming because the tools keep creating the conditions for it. The key has to go somewhere. Whoever holds it is the gate. You can rotate who holds it or ask them to be more available or split it among a committee. Now you have a committee. The mechanism that produces the bottleneck hasn't changed.

---

There's a version of this that used to be easy to dismiss. Code is valuable intellectual property. Valuable things need protection. Protection requires ownership. That logic justified the whole model.

It's harder to make that argument now. A growing fraction of code is written by an LLM responding to a prompt. Developers are increasingly the people who specify what they need and review what comes back. If you didn't write the code, it's hard to have strong feelings about who owns it. The asset is the running service, or the domain expertise, or the judgment about what to build. For those developers, the ownership model imposes all its costs and delivers none of its benefits.

---

The consolidation problem is downstream of unit cost. When creating a new unit costs nothing, there's no pressure toward consolidation. No reason to bundle things that shouldn't be together. No surface for ownership to attach to.

What that looks like in practice is an open question. But that's where the lever is.
