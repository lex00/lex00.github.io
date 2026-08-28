---
title: "A plan preview for k8s"
date: 2026-08-28
featured_image: "img/a-plan-preview-for-k8s-cover.svg"
---

kubectl can already dry-run an apply against the real API server and show you what it would produce.

[chant](https://intentius.io/chant/)'s k8s client adds ownership knowledge.

## Ownership at two granularities

kubectl's manager identity is generic, stamping whatever invoked it as the name on the field.

chant derives identity from your project instead using the bare string "chant", or "chant:\<stack\>".

Two mechanisms share this identity which otherwise can drift.
   - A label-based marker, set by chant, for ownership of the whole object
   - A field manager, set by the API server, for ownership of each field

Both come from the same "ownership.stack" config, so they can't disagree with each other about who owns what.

## A conflict kubectl users have to notice themselves

The field manager deliberately leaves environment out of the identity.

kubectl hands you whatever conflict the API server reports on the raw field-manager string, so reading meaning into that is up to you.

Fold environment into the identity, and staging and prod could each think they own the same object. Leave it out, and they collide on the next apply instead. 

Loud failures are much better than a silent split.

## chant kube get and chant kube source read your source, not just the cluster

`chant kube get` lists live resources with an extra column: declared, owned, drifted, or foreign-owned. 

`chant kube source` goes the other way. Handed a live object, it traces back to the `.ts` file and composite that declared it.

kubectl has no opinion on either question. Alignment is something you reconstruct by hand.

## Read more

- [chant](https://intentius.io/chant/), the tool this post is about
- [chant's k8s API client](https://intentius.io/chant/lexicons/k8s/api-client/), the read/write layer `kube` runs on
- [Which infrastructure tool actually keeps the spec?](/posts/which-tool-keeps-the-spec/), on chant's observational, non-authoritative state
