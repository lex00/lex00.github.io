---
title: "Which infrastructure tool actually keeps the spec?"
date: 2026-05-27
---

*In the IaC world, who is truly spec native?*

Most infrastructure tools put a layer between you and the target spec. The layer is the product. It owns state, deployment, and a model of your cloud that is not quite the cloud's own model. [Chant](https://intentius.github.io/chant/) makes a different choice. Its types come from the target spec. Its output is the target spec. Nothing chant specific survives in the artifact.

This post explains that choice. It also shows where Terraform, AWS CDK, and Pulumi drift from the spec, and what staying close to the spec buys you.

## What "the spec" means

Every target has a native format. CloudFormation has a JSON or YAML template. GitLab CI has `.gitlab-ci.yml`. Kubernetes has its manifest schema. The spec is the contract the platform actually reads.

A tool is spec native when two things remain true. First, the types you write match the spec one to one. Second, the output you ship is the spec's own format, with no wrapper.

Drift from the spec happens when a tool breaks either property. Some break the code property by abstracting above the spec. Some break the output property by emitting state instead of an artifact. The three common tools each drift in their own way.

## Terraform drifts in the model

Terraform speaks HCL. HCL is a custom language, not the provider's API. Each provider remaps a cloud API into an HCL schema. The resource `aws_instance` is Terraform's shape, not the EC2 API shape. New cloud features wait for a provider release before you can write them.

The artifact Terraform produces is not a spec document. It is a state file plus your HCL. State is authoritative. It is the source of truth for what Terraform believes exists. Drift detection compares state against reality through `plan` and `refresh`.

Authoritative state has a cost. It must be locked during writes. It must be stored in a backend with access control. Secrets land in it because the tool needs them to diff. If you stop using Terraform you are left with HCL and the coupled state.

## CDK drifts in the workflow

CDK lets you write TypeScript, Python, and other languages. Then it runs them. Synthesis executes your program. Constructors run, methods run, side effects run. The captured result is a CloudFormation template, which CDK then deploys.

Two kinds of drift follow.

The first is the abstraction. CDK L1 constructs map to CloudFormation one to one. L2 and L3 constructs sit above it. An L2 bucket adds defaults and helper methods that are not in the template you wrote, only in the template CDK emits. The source stops mirroring the deployed artifact. That is the point of L2, and it is also the cost.

The second is execution. Because synthesis runs code, the output can depend on the environment. Context lookups can reach into an AWS account during synth. Same source, different account, different template. The output is CloudFormation, so walk away cost is lower than Terraform. The path to that output is a program, not a document.

## Pulumi drifts in both

Pulumi also runs your program. During an update it executes the code and calls provider APIs directly. There is no intermediate template. The result is direct API calls plus state.

Many Pulumi providers are bridged from Terraform providers. When that is the case the resource model is the Terraform schema, one more remap away from the cloud API. State lives in Pulumi Cloud or a backend you run. As with Terraform, that state is authoritative and carries the same operational weight. Stop using Pulumi and you keep SDK code and a state file.

## Chant's spec native design

Chant is a synthesis compiler. TypeScript in, the target spec out. It does one thing and stops at the boundary where deployment begins.

The types are generated from the spec, not hand modeled. The AWS lexicon fetches the CloudFormation Registry schema, the same `CloudformationSchema.zip` AWS publishes, and generates a constructor for every resource type. That is roughly 1560 resource types today. When AWS updates the schema, the lexicon regenerates. There is no human in the loop deciding what shape a bucket should have.

The output is the spec's own format. The AWS serializer emits a standard CloudFormation template. `AWSTemplateFormatVersion` is `2010-09-09`. Resources are a map of logical name to `{ Type, Properties }`. You can hand that file to the CloudFormation CLI, to a pipeline, or to an agent. Nothing in it mentions chant.

Walk away cost is zero. If you delete chant the templates keep working, because the templates were never chant's format. They were always CloudFormation. The same holds for the other lexicons. GitLab CI output is `.gitlab-ci.yml`. Kubernetes output is plain manifests. Eleven lexicons ship today.

Zero walk away cost is not unique on its own. A single target tool like cdk8s emits plain manifests and leaves nothing behind. The distinction is breadth and types. The multi-cloud tools that own deployment all keep authoritative state, so they lock you in. The ones with no lock in cover a single target, or give you a language with no provider types. Chant covers many targets, generates spec-true types for each, and locks you into none.

Validation runs on top of the spec rather than replacing it. Lint rules check configuration for meaning. The AWS lexicon flags a bucket declared without encryption, an IAM policy with a wildcard, a hardcoded region. The rules read your source through the TypeScript compiler API and report file, line, and column. They do not change the output. They tell you when the spec compliant thing you wrote is probably not the thing you meant.

## Composites abstract, the output does not

Chant has composites. A composite is a function that returns several related resources from one call. A CockroachDB cluster composite returns a stateful set, a service, and the supporting resources. So what makes this different from the CDK abstractions cited above?

At the authoring surface it is abstraction. A composite is not a CloudFormation type. When you call one, the thing you write does not match a spec resource one to one. Defaults and shared values can enter the output without appearing at the call site. By the strict reading of spec native, the first property bends here.

Composites are an abstraction that collapse at build. A composite expands into its member resources, each a native type, serialized like any other. There is no composite in the template. Nothing chant specific to walk away from. The second property holds in full.

This expansion is static substitution, not arbitrary synthesis. Same props, same members. It does not read your cloud account the way a CDK construct can. And the spec true resource stays the primary surface. A composite is an opt in function over it, not a privileged tier the tool steers you toward. You can read the body, inline it, or never use it.

So the drift, if you call it that, is confined to the source you write. It never reaches what you ship. AWS CDK abstracts and runs a program to resolve it. Chant abstracts and resolves it by static expansion to native output.

## What it does not do, stated plainly

Chant does not deploy. It does not call cloud APIs at build time. It does not keep an authoritative state file. This is a scope boundary, not a missing feature.

It is worth being precise about execution, because the contrast with CDK and Pulumi is easy to overstate. Chant build runs under a TypeScript runtime and imports your files. Your constructors do run. The object literals are evaluated by the language. What does not run is any lifecycle around that. No API calls. No state. No reconciliation.

A separate lint pass keeps the executed code honest. The evaluability rules reject function calls in resource props, control flow around resources, dynamic property access, and other patterns that would make the result depend on more than literals and constants. With those rules satisfied, the executed result is equivalent to static data. The determinism is real for code that passes the rules. It is enforced by the lint layer, not by refusing to run anything.

Chant executes a constrained subset for synthesis only. There is no deployment workflow wrapped around it. That is the difference from CDK and Pulumi, which execute a full program and then act on the cloud.

## State, without the state file

Chant still has a story for drift. It is observational, not authoritative. `chant state snapshot` records what was seen in the cloud at a point in time and stores it on a git branch. `chant state diff --live` queries the live API for the declared resources and compares three axes. What is declared now. What the last snapshot held. What the cloud reports now.

The snapshot is a baseline, not a source of truth. A stale snapshot is inconvenient. A stale source of truth is dangerous. There is no lock, because nothing breaks if two people snapshot at once. There are no secrets in the file, because it records metadata only. The diff is informational. Chant does not apply it. What to do about a diff is left to a pipeline, an agent, or a person.

This gives up the precise plan and apply that authoritative state enables. In return it removes the file you have to host, lock, secure, and trust.

## Why the choice holds together

The pieces reinforce each other. Generated types mean the model cannot quietly drift from the spec. Native output means there is no wrapper to walk away from. Synthesis only execution means the build is deterministic for conforming code and has no side effects to reason about. Observational state means there is no authoritative file to operate.

None of this replaces your cloud tooling. Chant is a semantic layer that hands off a native artifact. The deployment step is still yours. That is the boundary, and it is the reason the output stays true to the spec.
