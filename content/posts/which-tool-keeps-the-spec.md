---
title: "chant keeps the spec"
date: 2026-05-27
---

[chant](https://intentius.io/chant/) is built around the target spec. Its types come from the spec, and its output is the spec.

## The spec

Every target has a native format, a CloudFormation template or a Kubernetes manifest. A tool is spec native when your types match that format one to one and the artifact you ship is that format, unwrapped.

## Synthesis

chant's synthesis compiles TypeScript to the target spec and stops there. Deployment is a separate layer, chant ops, and it consumes the same artifact you could hand to anything else.

The types are generated. The AWS lexicon reads the schema AWS publishes and emits a constructor for each of its 1,500-plus resource types, so a schema change regenerates the lexicon. The output is a standard CloudFormation template that never mentions chant. Delete chant and the templates keep working, because they were always CloudFormation. Seventeen lexicons ship today.

Lint runs on top of the spec. A bucket without encryption is reported at file, line and column, and the output is untouched.

## Composites

A composite is a function returning several related resources, so at the call site it is an abstraction. At build it expands by static substitution into native resources, and no composite reaches the template. CDK resolves its abstractions by running a program. chant resolves them by expansion.

## Limits

Synthesis does not deploy and keeps no authoritative state. `chant build` imports your files, so your object literals are evaluated, and the evaluability lint rejects function calls in props and control flow around resources so that conforming source is equivalent to static data.

Drift is observed rather than owned. `chant lifecycle diff --live` compares your declaration, the last snapshot and the live cloud, and the snapshot is a baseline you are allowed to lose. Acting on a diff is left to a pipeline or a person.

If you run Terraform or OpenTofu, [choudoufu](https://intentius.io/choudoufu/) brings the same live ownership to your HCL. If you run Pulumi, [plunge](https://intentius.io/plunge/) does it for your programs.

Generated types keep the model from drifting. Native output leaves nothing to walk away from. That is the whole design.
