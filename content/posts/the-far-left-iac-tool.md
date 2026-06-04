---
title: "The far-left IaC tool"
date: 2026-06-03
---

Everyone is shifting left. It's the safest opinion in infrastructure, and most tools honor it by shifting left exactly one notch and calling it a platform.

Terraform shifted left with `plan`, Bicep with `what-if`. Same idea, see the change before you apply it. Both are real improvements, and both still wait until you're talking to the cloud to tell you something is wrong. That's the centrist position. It's good, but it isn't the leftmost spot on the line.

{{< figure src="/img/iac-shift-left.svg" alt="The infrastructure pipeline left to right, with chant catching mistakes at the keystroke and Terraform and Bicep catching them at preview" >}}

Picture the pipeline running left to right, idea to code to apply to incident. The cloud is on the right, and `plan` and `what-if` sit just to its left because both need an API to mean anything. The leftmost seat is the red squiggle in your editor, the type checker, the lint rule that fires before you save. No network, no credentials, no deploy. That's the spot [chant](https://intentius.github.io/chant/) took.

You write infrastructure as constrained, deterministic TypeScript, not the arbitrary kind CDK lets phone home and do anything. Get a property wrong and the type checker stops you. Violate a naming rule and lint stops you. Reference a resource that can't exist and synthesis stops you, all with zero connection to any cloud. The bad deploy was never assembled in the first place.

Then it compiles to plain ARM JSON, CloudFormation, or Kubernetes YAML, so you still get `what-if` and `plan` exactly as before. We didn't replace the safety nets, we moved most of the catching to the left of them. Centrist IaC catches your mistake at apply. Far-left IaC catches it at the keystroke.

A preview still matters, because people change resources by hand and drift is real. Chant doesn't pretend the cloud sits still, it just makes sure the type errors, the policy violations, and the impossible resource are already gone by the time the output meets the API.

Newer tools like formae go the other way. It drops the state file too, but it's agentic and reconciles against live infrastructure, so its real checking happens at the cloud, not the keystroke. That's not a competitor to far-left synthesis, it's a lifecycle. The kind of thing you plug in, not the thing you replace chant with.

Bring your own lifecycle. We'll see you on the left.

## Read more

- [TypeScript as data](https://intentius.github.io/chant/concepts/typescript-as-data/) — why it's constrained, not CDK
- [Lint rules overview](https://intentius.github.io/chant/lint-rules/overview/) — the checks that run offline
- [Lifecycle models](https://intentius.github.io/chant/concepts/lifecycle-models/) — where `plan` and `what-if` fit
