---
title: "The revolving door of authoritative state"
date: 2026-08-04
draft: false
---

Pulumi, an infra company founded on TypeScript, is now shipping HCL.

Every argument Pulumi opened with has been repackaged as a feature.

This pivot gave me whiplash reading it today. Imagine moving out of one authoritative state prison into another.

I build chant, an infra compiler. You write TypeScript, it compiles to CloudFormation or Kubernetes YAML, and nothing runs.

# TypeScript as Data was Pulumi's to have

Luke Hoban co-created TypeScript and then brought it to infrastructure.

TypeScript as Data is an obvious answer to HCL. Pulumi picked runnable TypeScript.

chant leaves a platform native artifact in your hands, and it keeps working the day chant goes away.

Coupling synthesis to execution and authoritative state means the only way to reproduce your artifact is to run the toolchain again.

[TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) was on the table in 2018, in front of the person best placed on earth to pick it up.

# The cure is the disease

I wrote before that vendors [indict Terraform state](/posts/your-infra-database-is-a-road-to-hell/) as a database crammed into a flat file, then sell you a real one as the cure.

This week it happened again.

[The industry that exists to fix Terraform](/posts/fix-terraform/) has a new member, one that spent eight years saying the problem was the language.

# The revolving door

Pulumi is offering to rehome HCL and your authoritative state.

The path out of HCL then takes you back into Pulumi's own state. A revolving door with no exit.

# The real escape hatch is back to platform native

chant's [carve-out](https://intentius.io/chant/tutorials/terraform-carve-out/) takes a slice of a Terraform estate out to typed source and emits CloudFormation, or a Kubernetes manifest, or `.gitlab-ci.yml`. Nothing chant-specific rides along in it.

{{< inline-svg src="carve-out-to-native.svg" alt="One path running left to right. A Terraform estate holding HCL and state is carved out into typed TypeScript that keeps no state and runs nothing. From there the build fans out to three destinations, CloudFormation, Kubernetes YAML, and ARM JSON, each of which your platform already reads." >}}

You stop re-homing your infra in authoritative state. You move it back home, into the platform native tooling. It goes one slice at a time.

You can leave Terraform and state behind in the same move.

---

## Read more

- [Bring your Terraform estate into the agentic era](https://www.pulumi.com/blog/bring-your-terraform-estate-into-the-agentic-era/) — Pulumi
- [An entire industry exists to fix Terraform](/posts/fix-terraform/)
- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
- [Which infrastructure tool actually keeps the spec?](/posts/which-tool-keeps-the-spec/)
- [The long road back to cloud native](/posts/the-long-road-back-to-native/)
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) · [chant](https://intentius.io/chant/)
