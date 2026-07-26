---
title: "Adopt infrastructure without re-homing it"
date: 2026-07-18
draft: true
---

You rarely start infrastructure from nothing. You adopt it. Either you inherited it, a CloudFormation stack or a folder of manifests you now have to keep running, or you chose it, an open source platform you pulled in for a need. Both hide the same question: to keep this thing, what does the tool make you do to it?

## Inherited

You already have a spec. Most tools convert it. Terraform imports into state and has you rewrite it as HCL. ConfigHub imports it into its store as data. Idem describes it into SLS files. Either way your config now lives in the tool's format, and leaving means exporting and rewriting it again. You did not adopt it. You moved it.

chant adds types and hands the same spec back. A CloudFormation template stays a CloudFormation template. It is spec-native, with no format of its own for your config to move into. So you take upstream updates, you can quit chant and keep deploying, and you never bet the config on a database or runtime to keep it alive.

## Chosen

Adopting an open source platform into a real account usually means forking it. You cut it open and wire in your VPC, DNS, and IAM by hand, because upstream cannot know your environment. Now you own a fork that drifts with every release.

The healthier version does not fork. You build a toolkit around the upstream in chant and leave the upstream intact. The seams, tiers, CI, and naming live in a layer above it, and you adopt by setting parameters, not by editing the platform.

loomster is that toolkit for [awslabs/loom](https://github.com/awslabs/loom). It wraps Loom, pinned at v1.6.0, and every load-bearing piece, network, IAM, KMS, database, DNS, is a seam you provision, reference existing, or omit through parameters. Nothing is forked, so upstream stays trackable. Its bring-your-own example wires every seam to resources you already run, validated end to end on a real account, both production tiers at seven of seven stacks. The enterprise gets Loom on its own network and identity, at production scale, holding standard specs.

## Both halves

Re-homing wears two faces: conversion of your spec, or a fork of the upstream. chant avoids both because it works on the spec directly and keeps adoption in a layer. You put types on what you inherited, or a toolkit around what you chose. It stays what it was.
