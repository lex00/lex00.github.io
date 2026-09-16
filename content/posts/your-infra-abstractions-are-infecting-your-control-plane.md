---
title: "Your infra abstractions are infecting your control plane"
date: 2026-09-15
featured_image: "img/two-lanes.svg"
draft: false
---

Infrastructure abstractions are sexy. It's alluring to think that you can encode your opinions once and nobody else ever has to think about them.

When you invent an abstraction for infra, you are going to end up holding it somewhere. That somewhere is your control plane, and where you get to run it is decided by your abstraction.

## Where does the abstraction live?

You can stick your opinions anywhere you like and at some point they have to get reconciled. If the opinion is a controller the control plane is a cluster. If it's a store, it has to query that store.

{{< inline-svg src="abstraction-picks-the-venue.svg" alt="Three columns pairing what you invent at the bottom with where your control plane is left to live at the top. Invent a CRD and a controller, as Kro, Crossplane and Kratix do, and a red arrow reaches up to say your control plane lives in a cluster. Invent a store holding desired state as rows and another arrow reaches up to say it lives in a query against a store that must be right. Invent nothing and there is no arrow at all: the control plane runs anywhere, on a cluster and off one." >}}

chant invents no abstractions to begin with. A composite is assembly, a plain function returning spec-native resources. That's [configuration as data](/posts/code-as-config-config-as-data/) arrived at by compiling rather than by storing. The control plane above it can deploy anywhere.

Stores answer for ownership. Using a provider-native tag at create time means truth stays on the resource itself.

{{< inline-svg src="what-each-answer-leaves.svg" alt="Four rows naming where a platform team's opinions live, what that invents, and what you are left operating. Kro, Crossplane and Kratix invent a CRD with a controller behind it, leaving you a cluster and the abstraction inside it. Helm, Timoni and Score invent a values format, and in Score's case state, leaving a format to learn and a file to keep correct. ConfigHub invents a store holding desired state as rows, leaving a store that has to be right. chant invents nothing, because a composite assembles spec-native resources, leaving the spec your platform already defines." >}}

## Nothing to stand up

The best control plane requires no special configuration with your resources. The read access you already have is all you should need to get started.

[behold](https://intentius.io/behold/) is the abstraction free control plane. Cloud drift on AWS sits directly beside supply-chain drift on GitHub Actions. It keeps no copy of your estate, and completed live results are not cached. What it does write down is derived. Nothing about it assumes a cluster.

behold is still in development but available for you to try. The graph and the drift overlay work today, the delegated actions are still in progress.

## Anything can be a database

TypeScript queried through its syntax tree already answers questions about the estate. I measure what the abstractions cost on [aws-bench](/posts/aws-bench-scenario-1-wrap/): asked which security groups were attached to nothing, every toolchain that reads a stored copy scored 0 out of 3.

A model of your cloud that differs from native is always a release behind the thing it models. That's [where the other tools drift from the spec](/posts/which-tool-keeps-the-spec/), and it's the same invented layer reaching upward to tell your control plane where it may live.

Abstractions drift. Why do we keep infecting infrastructure with them?

---

## Read more

- [Configuration as code, and as data](/posts/code-as-config-config-as-data/)
- [Queryable infrastructure](/posts/queryable-infrastructure/)
- [Accessible Ops](https://accessibleops.net/)
- [State and Governance](https://intentius.io/chant/concepts/governance/)
