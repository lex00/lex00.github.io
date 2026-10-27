---
title: "Policy belongs left of the platform"
date: 2026-07-17
---

HashiCorp shipped tfpolicy, and it is a good step. tfpolicy puts provider and module rules next to resource rules in one HCL policy language and runs them earlier than Sentinel did. Provider and module rules run pre-plan before a download. Resource rules run at plan and computed values get checked at apply. Teams write their policy in the same language as their infrastructure.

It still runs at the platform. tfpolicy evaluates inside HCP Terraform, against a plan, with credentials. Its rules are HCL over `attrs`, and a path like `attrs.encryption_settings_collection[0].enabled` is checked when the run evaluates it.

{{< inline-svg src="policy-shift-left.svg" alt="A left-to-right pipeline axis from Editor to Apply. chant policy sits at Editor and Build, left of a dashed HCP-plus-credentials boundary; tfpolicy spans pre-plan to apply and Sentinel and OPA span plan to apply, both to the right of the boundary." >}}

Read the axis by the boundary. tfpolicy reaches earlier than Sentinel and covers more of the run, inside the platform. chant policy sits left of that line, in the build.

chant policy is typed TypeScript over the resource graph. It runs offline in your build with no HCP and no credentials. A wrong attribute is a red squiggle, and a cross-resource rule reads a typed reference instead of a string filter. The check that gates the apply already passed at your desk.

chant's typed policy runs in the build, before tfpolicy runs at plan. Teams can use both.

## Read more

- [Organizational policy](https://intentius.io/chant/guide/organizational-policy/) is typed policy that gates the build
- [TypeScript as data](https://intentius.io/chant/concepts/typescript-as-data/) explains why it is typed instead of stringly
