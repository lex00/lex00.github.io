---
title: "Policy belongs left of the platform"
date: 2026-07-17
---

Everyone is shifting policy left. HashiCorp just shipped tfpolicy, a policy-as-code framework in HCL, and it moves the catch earlier than Sentinel ever did. Provider and module rules run pre-plan before a download, resource rules run at plan, and computed values get checked at apply. One language does all of it, so the second one that Sentinel and OPA made you learn is gone.

It still runs at the platform. tfpolicy evaluates inside HCP Terraform, against a plan, with credentials. Its rules are HCL over `attrs`, a dynamic bag nothing type-checks. `attrs.encryption_settings_collection[0].enabled` is a string path you either get right or find out about at evaluation time, in the run, not in your editor.

{{< inline-svg src="policy-shift-left.svg" alt="A left-to-right pipeline axis from Editor to Apply. chant policy sits at Editor and Build, left of a dashed HCP-plus-credentials boundary; tfpolicy spans pre-plan to apply and Sentinel and OPA span plan to apply, both to the right of the boundary." >}}

Read the axis by the boundary. tfpolicy reaches earlier than Sentinel and covers more of the run, and every inch of it sits right of the platform line. chant is the only one left of it.

chant policy is typed TypeScript over the resource graph, and it runs in your build, offline, with no HCP and no credentials. A wrong attribute is a red squiggle, and a cross-resource rule reads a typed reference instead of a string filter. The check that gates the apply already passed at your desk.

tfpolicy shifted the catch to pre-plan. chant put it at the keystroke. Go take a closer look.

## Read more

- [Organizational policy](https://intentius.io/chant/guide/organizational-policy/) — typed policy that gates the build
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) — why it is typed, not stringly
