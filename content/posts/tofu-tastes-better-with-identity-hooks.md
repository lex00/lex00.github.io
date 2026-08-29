---
title: "Tofu tastes better with identity hooks"
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

choudoufu treats these tags as hooks at plan time.

## What makes a tag a live marker?

Moving identity off a private ledger and onto the resource is the first step. choudoufu also handles this at create time, leaving a newly created resource properly marked. That behavior on create and on plan time together makes a tag into an authoritative marker.

## Migration

A central policy where resources can be migrated with a simple tag change requires cooperation from the tool you use as well. Because choudoufu plans read the hooks live, you pick up the latest ownership markers.

This allows both migration and renaming to be handled with a tag, instead of a ledger edit. Handing a whole estate to another team becomes a simple change in a central IAM policy.

## An industry of solutions

[An entire industry](https://lex00.github.io/posts/fix-terraform/) exists to deal with the issue of ownership in a localized ledger. These paid control planes offer a workaround that lives in their layer. What you want is to have this control right in your cloud-native IAM.

If you want to see a tool that takes this even further than [choudoufu](https://intentius.io/choudoufu/), look at [chant](https://intentius.io/chant/concepts/overview/).

---

## Read more

- [Terraform state has three pieces](https://lex00.github.io/posts/terraform-state-has-three-pieces/)
- [Take a whiff of choudoufu](https://lex00.github.io/posts/take-a-whiff-of-choudoufu/)
- [choudoufu](https://intentius.io/choudoufu/)
