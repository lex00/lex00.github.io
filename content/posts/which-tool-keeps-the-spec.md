---
title: "Which infrastructure tool actually keeps the spec?"
date: 2026-05-27
---

Most infrastructure tools put a layer between you and the target spec. The layer is the product. It owns state, deployment and a model of your cloud that is not the cloud's own. [chant](https://intentius.io/chant/) makes a different choice. Its types come from the spec, and its output is the spec.

## What "the spec" means

Every target has a native format, a CloudFormation template or a Kubernetes manifest. A tool is spec native when your types match that format one to one and the artifact you ship is that format, unwrapped. The common tools each break one of those.

## Terraform drifts in the model

Each Terraform provider remaps a cloud API into an HCL schema. `aws_instance` is Terraform's shape of EC2. A new cloud feature waits for a provider release. You are left with HCL and an authoritative state file to lock, host and scrub of secrets.

## CDK drifts in the workflow

CDK runs your program to produce a template. L2 and L3 constructs add defaults that appear in the output and nowhere in your source, and a context lookup during synth can reach into an account, so one source can yield different templates. The output is CloudFormation, reached by running a program.

## Pulumi drifts in both

Pulumi runs your program and calls provider APIs directly. Many of its providers are bridged from Terraform's, so the resource model is Terraform's schema, one more step from the cloud. Stop using it and you keep SDK code and a state file.

## What chant does instead

chant's synthesis compiles TypeScript to the target spec and stops there. Deployment is a separate layer, chant ops, and it consumes the same artifact you could hand to anything else.

The types are generated. The AWS lexicon reads the schema AWS publishes and emits a constructor for each of its 1,500-plus resource types, so a schema change regenerates the lexicon. The output is a standard CloudFormation template that never mentions chant. Delete chant and the templates keep working, because they were always CloudFormation. Seventeen lexicons ship today.

Lint runs on top of the spec. A bucket without encryption is reported at file, line and column, and the output is untouched.

## Composites

A composite is a function returning several related resources, so at the call site it is an abstraction. At build it expands by static substitution into native resources, and no composite reaches the template. CDK resolves its abstractions by running a program. chant resolves them by expansion.

## What it does not do

Synthesis does not deploy and keeps no authoritative state. `chant build` imports your files, so your object literals are evaluated, and the evaluability lint rejects function calls in props and control flow around resources so that conforming source is equivalent to static data.

Drift is observed rather than owned. `chant lifecycle diff --live` compares your declaration, the last snapshot and the live cloud, and the snapshot is a baseline you are allowed to lose. Acting on a diff is left to a pipeline or a person.

Generated types keep the model from drifting. Native output leaves nothing to walk away from. That is the whole design.
