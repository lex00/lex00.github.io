---
title: "Git is perfect for portable provenance"
date: 2026-09-29
featured_image: "img/provenance-in-the-repo.svg"
draft: false
---

Provenance is the record of why a change exists and who stands behind it. It belongs with the code. Anyone who clones a repo can ask why a line exists and get an answer.

[Accessible Ops](https://accessibleops.net/) holds provenance to two tests: people can trust it, and it goes wherever the code goes. A [chant workspace](https://intentius.io/chant/reference/workspace-declaration/) passes both with plain git. It keeps the why as files in the same repo and reviews them in the same pull requests as the code.

## Does the reason travel with the change?

History gets rewritten and commits move with it. chant gives each decision a permanent id. Every commit names the decision it carries out and keeps that name through each rebase. That is the property [The reason travels with the change](https://accessibleops.net/the-reason-travels-with-the-change/) describes.

## Who stands behind it?

[Attributable](https://accessibleops.net/attributable/) holds engineers and agents to the same record. An agent's proposal records its model and session and pins its transcript by hash. It takes effect when a person decides it.

## Can anyone verify it?

chant seals decisions and review verdicts with the ssh key each person already signs commits with. Each seal covers the exact text it signed, and anyone holding the repo can check it offline. [Provenance verifies anywhere](https://accessibleops.net/provenance-verifies-anywhere/) asks for this.

## Provenance that comes with your existing workflow

The records live in the repo and reach whoever holds the code next, as [Provenance stays with the code](https://accessibleops.net/provenance-stays-with-the-code/) requires. They work with everything your team already runs on git.

Ask your agent to take a look at chant workspace today.

---

## Read more

- [Workspace Declaration](https://intentius.io/chant/reference/workspace-declaration/)
- [Work Items](https://intentius.io/chant/guide/work-items/)
- [Recording Decisions by Hand](https://intentius.io/chant/guide/recording-decisions-by-hand/)
- [Accessible Ops](https://accessibleops.net/)
