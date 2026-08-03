---
title: "An ecosystem of gruel"
date: 2026-08-03
---

Configuration tooling keeps getting thrown into one cauldron. Start with eye of newt, then add a splash of versioning, a pinch of transformation, and a few sprigs of authoritative state.

Gruel ends up tasting the same no matter how it gets started.  Once cooked you have no way to cleanly extract any of the ingredients.

{{< inline-svg src="bowl-of-gruel.svg" alt="A bowl of gruel seen front on, steaming, with a few flies circling. Lumps break the surface, three of them labelled with pairs that got cooked together: state plus ownership, authoring plus delivery, index plus authority." >}}

Clean separation of concerns with toolchains like this boils down to the fact that you get to drink yours from one bowl.  This sounds pretty convenient at first. If you like your food served this way then everything is fine.

# The chant dining experience

{{< inline-svg src="no-system-to-run.svg" alt="Developer, on the left, holds TypeScript, your own IDE, and checked before live. In the middle sit three separate floating sections. chant synth is marked REQUIRED and runs chant build into spec-native artifacts, deterministic with no network, no state and nothing running. chant ops is marked OPT IN and DURABLE, covering gates, rollback and apply. chant lifecycle is marked OPT IN and GITOPS, covering observe, diff, plan and reconcile. Delivery, on the right, is your platform unchanged: kubectl, Argo, Flux, CFN deploy, CI pipeline. A dashed return path runs from Delivery back through chant lifecycle to Developer." >}}

chant gives you a menu of choices.

You write TypeScript. It compiles to your platform's own spec.

When your produced artifacts are your platform's native format, they continue to be deployable even if you dump the toolchain that produced them.

{{< inline-svg src="chant-synth.svg" alt="chant synth, marked REQUIRED. chant build, which folds, resolves and serializes, produces spec-native artifacts: Kubernetes YAML, CloudFormation, .gitlab-ci.yml. Deterministic, no network, no state, nothing running." >}}

# Serving gruel vs ingredients

{{< inline-svg src="gruel-vs-ingredients.svg" alt="A three column table. The problem, gruel, and solvable with. Versioning config: units, revisions, head pointers and more, or git. What changed a value: per-path provenance and back-indexes, or the line that sets it. Environment variants: spaces, lineage links and three-way merge, or a build parameter. Transforming config: typed functions, an executor registry, workers and more, or a compiler pass. Understanding a format: converters, semantic paths, merge keys and more, or types from the spec. Finding things: a semantic index, attribute registry and link graph, or query the artifact. Cutting a release: release objects, exact revisions and digests, or the build output. Approving a change: gates, apply-gates and apply-warnings, or a gate step in a workflow. Answering is this mine: delegated out to the actuators, or the marker on the resource." >}}

Every entry in the left column is a real problem with more than one answer.

The column on the right offers us a path forward that routes around vendor lock-in.

# Gruel is not queryable

You cannot pick the versioning back out of a cooked pot. You can only ask it questions in the query
language it shipped with.

Plenty of things [answer questions without being a database](/posts/queryable-infrastructure/). The
live cloud is one. Typed source is
another, because chant reads [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/)
through the syntax tree, so an agent queries your infra code instead of grepping it.

On [aws-bench](/posts/aws-bench-scenario-1-wrap/), asked which security groups were attached to
nothing, every toolchain reading a stored copy scored zero out of three.

# The half that gets skipped

Handing exact revisions to a reconciler is the easy half. Everyone does that one.

The other half typically gets scoped out.

{{< inline-svg src="chant-ops.svg" alt="chant ops, marked OPT IN and DURABLE, covering three things: gates, a durable approval; rollback, auto compensation; and apply, over server-side apply, CloudFormation and ARM. It survives a crash, holds an approval for days, and unwinds a partial apply." >}}

A gate is a durable wait for a signal. If an apply dies halfway, each capability unwinds
its own step and the half-applied change comes back.

{{< inline-svg src="chant-lifecycle.svg" alt="chant lifecycle, marked OPT IN and GITOPS, covering three things: observe, a live read across 11 categories; diff and plan, producing a typed change set; and reconcile, which opens a PR. It reads the live system, or you commit the artifact and let Argo or Flux do it." >}}

When live drifts from source, `ReconcileOp` regenerates the TypeScript and opens a pull request. It
never merges and it never commits to main. Cloud back into code is the direction most out-of-band changes actually travel, and it tends to lack strong support.

Releases carry an SBOM, a signature and provenance, and publish promotes by digest so the bytes
tested in dev are the bytes in prod. [behold](https://github.com/INTENTIUS/behold) renders the whole
estate live off `chant graph` and never mutates anything.

# A word on OCI bundles

chant publishes images to any OCI registry and promotes them by digest, with SBOMs and signatures
attached through the standard referrers API. All of it is optional. There is a registry-free path
that loads straight onto the host, and a missing `oras` binary reports itself instead of failing your
publish.

What chant leaves in your hands is the push itself. The bundle exists and is content-addressed, and
an Op puts it wherever your reconciler pulls from.

Content-addressing gives identity to output you cannot reproduce. Where synthesis is closed the
source is already the identity. Where a generator leaves its inputs open, as Helm does, the render
needs a digest, and chant is building that for charts.

# What a toolchain should cost you

Gruel architectures are sold on a fleet story centered around hundreds of clusters and a massive bulk change story to solve.

If your story of scale is a smaller one, the gruel machinery will not shrink for you.

Teams that do have fleet problems are typically the ones least in need of an opinion. What they want is a spec-true artifact and a set of capabilities they can compose on their own terms.

chant's drift detection ships with a section on determining if it has value for you. The lifecycle is a dial you set per environment. Temporal is opt-in.

chant's output is CloudFormation, or Kubernetes YAML, or `.gitlab-ci.yml`, with nothing chant-specific in
it. The day you walk, your artifacts keep deploying.

So, gruel or Korean BBQ?  I know what I'm having for lunch.

{{< inline-svg src="chant-dishes.svg" alt="Three small dishes side by side under the word chant, seen from the same angle as the bowl. Each holds a different ingredient, neatly arranged and kept apart: green rounds, amber cubes, purple strips." >}}

---

## Read more

- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [Configuration as code, and as data](https://lex00.github.io/posts/code-as-config-config-as-data/)
- [The gap closes faster this time](https://lex00.github.io/posts/the-gap-closes-faster-this-time/)
- [chant how it compares](https://intentius.io/chant/concepts/comparison/) · [chant](https://intentius.io/chant/)
