---
title: "Tofu tastes better with live markers"
date: 2026-08-23
draft: false
---

Outside of k8s, infra tooling generally has pretty specific way of looking at ownership. They keep a ledger, and if a resource is in the ledger, the tool owns it. This simplicity feels so powerful, and it is, as long as you never get tasked with migration of the ledger across org boundaries.

## Defining ownership in AWS

choudoufu writes the answer onto the resource itself, as two tags.

```
tofu-estate  = prod-networking
tofu-address = aws_vpc.main
```

choudoufu reads these tags at plan time.

## Tags become live markers

Moving identity off a private ledger and onto the resource is the first step. choudoufu also handles this at create time, leaving a newly created resource properly marked. Writing on create and reading on plan together make a tag into a marker the plan can trust.

## Migration

A central policy where resources can be migrated with a simple tag change requires cooperation from the tool you use as well. Because choudoufu plans read the markers live, you pick up the latest ownership.

This allows both migration and renaming to be handled with a tag, instead of a ledger edit. Handing a whole estate to another team becomes a simple change in a central IAM policy.

## Pipelines and enforcement

[terragucci](https://intentius.io/terragucci/) runs the pipelines for choudoufu and OpenTofu roots in your own forge. The markers are tags, so [IAM ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html) can gate on them.

---

## Read more

- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [choudoufu](https://intentius.io/choudoufu/)
