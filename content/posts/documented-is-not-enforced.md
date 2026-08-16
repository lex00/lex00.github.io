---
title: "Documented is not enforced"
date: 2026-08-03
draft: true
---

Valerio Uberti wrote a [sharp piece on AI agents in CI/CD](https://www.valeriouberti.dev/articles/ai-cicd).
One line carries the whole thing: the thing which reasons should not be the thing which has
credentials.

His pattern splits the pipeline in two. An analyst job reads test output and writes markdown, holding
a single write scope. An actor job holds the credentials and waits behind a human. The analyst cannot
reach the actor.

He is right, and the numbers are good. Twenty-two minutes to four, fifteen cents a run.

Then he spends the back half of the post listing what breaks if you wire it wrong. Keep
`pull_request_target` away from a checkout. Turn off `persist-credentials`. Never interpolate agent
output into a shell command. Never grant `write-all`.

That list is correct, and it is the part that rots.

# Eight rules instead of a list

Every one of those warnings is already a lint rule in chant's github lexicon, checked against the
workflow it just generated.

| The warning | The rule |
|---|---|
| `pull_request_target` beside a checkout, his most-exploited misconfiguration | GHA018 |
| `workflow_run` checking out untrusted code, the fork fix done unsafely | GHA038 |
| `persist-credentials` left on where an artifact can sweep it up | GHA049 |
| `write-all` handed to a job that needs one scope | GHA033 |
| No explicit `permissions:` block on the workflow | GHA017 |
| No job-level `permissions:` under a sensitive trigger | GHA013 |
| Untrusted input interpolated into a `run:` step | GHA036 |
| Untrusted input written to `GITHUB_ENV` or `GITHUB_PATH` | GHA037 |

A pattern in a blog post survives exactly as long as the person who read it. A pattern in a lint rule
survives the person who wrote it, the intern who copies the workflow, and the agent that generates
the next one.

His post is the specification. These are the tests.

# The part he leaves open

The risk he names and cannot close is nondeterminism. Agents are inconsistent, so he labels their
output a hypothesis rather than a verdict, and tracks how often it agrees with the engineer.

That is the right call when the agent's product is prose. You cannot check prose, so you discount it.

When the agent's product is chant source, you check it. Types, semantic lint, and the evaluability
rules all run before anything executes. You do not have to trust what the agent wrote, and you do not
have to grade it later.

His injection worry shrinks for the same reason. chant folds source to a value instead of running it,
so a config file an agent wrote reaches no network, spawns no process, and writes no file at build
time. Give the agent the keyboard, not the runtime.

# What chant does not do

He is solving failure triage. Four thousand lines of log, eighteen percent of three hundred PRs, and a
senior engineer reading all of it. chant does none of that and should not pretend to.

The overlap is the boundary, not the product. He drew it in a pipeline. chant draws it in a compiler,
where the build path holds no credentials because there is nowhere to put them.

# Give the agent the logs

His closing line is better than any of mine: give the agent the logs, not the keys. The reading was
always the expensive part.

The follow-on is that the reading gets cheaper when the thing being read is typed. An agent parsing a
4,000-line log is doing archaeology. An agent reading
[TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) through the syntax tree
is doing a query.

---

## Read more

- [AI Agents Belong in CI/CD. Not in the Deploy Step](https://www.valeriouberti.dev/articles/ai-cicd) — Valerio Uberti
- [Queryable infrastructure](https://lex00.github.io/posts/queryable-infrastructure/)
- [Policy belongs left of the platform](https://lex00.github.io/posts/policy-belongs-left-of-the-platform/)
- [chant github lint rules](https://intentius.io/chant/lexicons/github/lint-rules/) · [chant](https://intentius.io/chant/)
