---
title: "The abstraction that compiles away"
date: 2026-07-18
draft: true
---

A platform team has one real job: encode the opinions once so a hundred developers don't. The SecurityContext, the resource limits, the probes, the HPA, the NetworkPolicy. Get them right in one place and nobody ships a pod without them. The only question is where that one place lives.

The Kubernetes world has two answers. chant is a third.

## In the cluster

Kro, Crossplane, and Kratix put the opinion inside the cluster. The platform team writes a CRD and a controller. A developer submits a small custom resource and a reconciler expands it into the real objects. The abstraction is a running thing now. It has a version, a reconcile loop, a failure mode, and a seat in your upgrade plan. You did not define a WebApplication. You are operating one.

## Outside, as a new format

Helm, Timoni, and Score keep the opinion outside the cluster and generate manifests from it. Better instinct. The catch is what you author. Helm is untyped templating, so a wrong value surfaces as rendered garbage. Score is a cleaner idea, a platform-agnostic workload spec, but it is still a second format pointed at the spec, and it keeps state the way Terraform does. Re-init with different provisioners and it warns you, because now there is a file that has to stay correct.

Notice the pattern. The in-cluster tools leave a controller running. The CLI tools leave a new language, and the good one leaves a state file. Every answer leaves something behind.

## Compile it away

chant puts the opinion in a typed preset and then compiles it out of existence. The platform team writes the secure defaults once, as a typed composite. The developer imports it and fills a few typed fields. `chant build` expands it to the real manifest and stops. The abstraction is everywhere you author and nowhere you run. No CRD in the cluster. No new format. No state file. The output is a standard manifest that works whether or not chant was ever installed.

That is the difference between hiding the spec and compiling to it. Kro hides the manifest behind a CRD. Score hides it behind a spec with state. chant hands you the manifest, typed, and gets out of the way.

## Developers wanted less YAML, not another language

The complaint was never that YAML is verbose. It is that you write it blind, patch it with three tools, and learn at apply time what you got wrong. A typed preset fixes the real problem. Completion comes from the schema. Errors land in your editor before you commit. What you write is what ships, so there is no rendered output to reverse-engineer and no mapping to keep in your head.

An agent gets the same deal. It writes typed source against a known schema and knows exactly what manifest falls out. No reconciler to model, no template engine to guess at.

The best abstraction leaves nothing behind. No controller, no format, no state. Everywhere you author it, nowhere you run it.
