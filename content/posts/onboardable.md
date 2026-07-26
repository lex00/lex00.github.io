---
title: "Onboardable"
date: 2026-07-23
draft: true
---

Every argument about AI agents in operations gets easier once you stop treating the agent as special. An agent is the newest hire. It reads what is written, works through the paths you give it, touches what its credentials allow, and asks when it is unsure. The uncomfortable part is that a lot of infrastructure was not safe to hand a new hire either. We hid that behind the fact that new hires are slow and cautious, and there were rarely many of them at once.

Jake Gaylor put the test plainly in [Agent-Ready Infrastructure](https://jakegaylor.com/blog/posts/agent-ready-infrastructure/). Could a competent stranger operate your system on day one, using only what is written down, through paths you can review, with consequences you can survive? That is an onboarding test, and it does not care whether the stranger is a person or a model. The properties that make a new engineer productive and safe in week one are the properties that make an agent safe. Agents and people both have to onboard.

We are wary of the phrase agentic ops. An agent reading an error and picking a tool is the old kind of operation done faster, with the judgment calls easier to surface to a human. What follows is the set of properties that make infrastructure onboardable, for a person or an agent, so the judgment stays with the human and the rest is safe to delegate.

## 1. Honor the lower layer

The thing a newcomer changes should be the platform's own spec, with nothing reimplemented underneath it. When a tool wraps the platform in a second model with its own hidden state, a newcomer has to reason about the wrapper, the state, and the drift between them. When the source compiles to the native spec, there is one honest artifact and nothing behind it. What they read is what ships, because the output cannot drift between the read and the apply. And they can read it before anything runs, because the read needs nothing but the source.

## 2. The same feedback guides both

A bad change should be caught the same way whether a person or a machine makes it. When the rules are a static check over the source, the editor draws a red squiggle for a human and the language server hands the same diagnostic to an agent. Both learn the valid move at the keystroke, before the change goes anywhere. A rule that only lives in a reviewer's head catches nothing until review, and a machine cannot read a reviewer's head at all.

## 3. Written down

The parts a machine cannot infer belong in writing. Types and schemas tell a newcomer what is valid. They do not tell anyone why the database lives in that region, or why that service is held at four replicas. That knowledge has to exist as text, because a competent stranger, human or agent, has no other way in. Tribal knowledge is the thing an agent cannot absorb, and the thing a new hire spends a year absorbing badly.

## 4. One reviewable path

Every change should arrive as a diff, in one place, so review scales. When changes scatter across dashboards and consoles, no one can see the whole of what a newcomer did, and nothing queues up for a second set of eyes. One path means one place to look, one place to approve, and one place to say no.

## 5. Least privilege by handle

A newcomer gets scoped, revocable access, and references secrets by name rather than holding them. You would not hand a new hire the root credential on day one, and an agent should have less standing power, not more. Access that is narrow and revocable is what lets you say yes to delegation at all.

## 6. Bounded blast radius

One mistake should not be able to take down everything. Cap what a single change can touch, by scope, by rate, by environment. The point of a bound is that you can survive the newcomer's worst day, which is the only way delegation is ever safe.

## 7. Reversible before risky

An action that can be cleanly undone is one you can let a newcomer take. An action that cannot be undone is one a human signs off first. Sorting changes by whether they are reversible is how you decide what needs a gate and what does not.

## 8. Escalate the judgment

The newcomer executes, and the human owns the call that matters. Approval is a precondition to a privileged change landing, not a message the agent sends after deciding on its own. When authority or confidence is unclear, the safe move is to stop and ask rather than proceed. This is the whole point of the exercise. Make the judgment calls easy to surface, and let everything else run.

## 9. Attributable

Every change should trace to who made it, what they changed, and who approved it. A newcomer's work is safe to accept only if you can see it afterward, and an agent's work is safe to accept on the same terms. The record is what turns "we let it make changes" into something you can audit.

## A compiler has no day two

Read those nine back and notice how many are properties of the change itself. Reviewable, predictable, checkable before it runs, bounded, reversible. A compiler turns those from habits you maintain into facts you get for free, and it does it with two guarantees people usually blur together. It runs on your machine, with no cloud and no credentials, so the check costs nothing and touches nothing. And it gives you the same output tomorrow as today, because the output is a pure function of the source. A red squiggle needs both. If the check needs the cloud, it is a plan, not a squiggle. If the check's answer can drift, the squiggle lied.

The deeper thing a compiler does is erase day two. In most shops, day one is standing the system up, and day two is the rest of its life, the changes and the drift and the state surgery and the runbooks no one wrote. Day two is a different and scarier discipline, and it is where the tribal knowledge accretes. A compiler collapses it. A change on day two is the same act as day one. Edit the source, recompile, read the diff, apply. Operating is authoring, so everything that made authoring safe carries into every change the system ever takes.

That is why the onboarding test holds past the first day. You onboard a newcomer, a person or an agent, into one loop, and that loop is the entire operational surface. There is no second apprenticeship in the dark arts, because there are no dark arts. Day two is day one again.

## Where this comes from

chant is our attempt to build exactly this. It compiles a typed subset of TypeScript to the platform's native spec, lints it in your editor and through an agent's language server, computes the diff against the live system, and puts every change up for approval before it applies. The wardens do the same for the platforms you do not usually call infrastructure. None of the nine properties needs chant, and a shop with good discipline can reach most of them by hand. A compiler is just the shortest path we have found to all of them at once, and to the one that matters most, that operating never becomes a second thing you have to learn.

Jake's competent stranger and this list are the same idea from two sides. Build the system so a stranger can operate it on day one, and you have built the system an agent can operate on every day after.

---

## Read more

- [Agent-Ready Infrastructure](https://jakegaylor.com/blog/posts/agent-ready-infrastructure/) — Jake Gaylor
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Temporal and chant saw it coming](https://lex00.github.io/posts/temporal-and-chant-saw-it-coming/)
- [chant](https://intentius.io/chant/)
