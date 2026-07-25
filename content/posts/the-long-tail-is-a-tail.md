---
title: "The long tail is a tail"
date: 2026-07-25
draft: false
---

By definition a tail is the small, infrequent remainder. The long tail of spec-less APIs never touches chant. Here's why.

chant compiles a typed source to the platform's native spec, while some platforms are a pure API with nothing declarative underneath.

{{< inline-svg src="the-long-tail.svg" alt="A golden spiral. The specced platforms, AWS, Kubernetes, the clouds, CI, are the wide outer sweep, and the long tail tapers to a point at the center." >}}

The platforms that run most production infrastructure all have specs. AWS is the [largest cloud most shops build on](https://www.statista.com/chart/18819/worldwide-market-share-of-leading-cloud-infrastructure-service-providers/), and its spec is deep, [over 1,500 resource types](https://awsfundamentals.com/cloudformation) in CloudFormation. The specced surface is the ground everyone stands on.

The tail is smaller than it sounds. The [Terraform Registry alone carries thousands of providers](https://www.hashicorp.com/en/blog/hashicorp-terraform-ecosystem-passes-3-000-providers-with-over-250-partners), so much of what gets called spec-less, the SaaS control planes, the third-party services, already has a declarative surface to compile against. What has nothing to synth is a genuine remainder.

chant composes with your stack. It owns the declarative surface and runs alongside whatever handles the rest, a script, a provider, a controller, a vendor CLI.

Compiling specs is the whole job, and chant does it across every platform that has one.
