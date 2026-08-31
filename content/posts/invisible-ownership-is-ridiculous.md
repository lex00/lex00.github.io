---
title: "Invisible ownership is ridiculous"
date: 2026-08-30
featured_image: "img/invisible-ownership-cover.svg"
tags: ["invisible ownership"]
draft: false
---

Terraform has an ownership problem.

From an org perspective, ownership is usually about who is accountable. This accountability gets encoded into permission structures that get stamped out across concerns. Permission gets stamped on IAM roles, while ownership gets stamped nowhere.

Kubernetes, Argo and Flux all have a place for ownership. The API server tracks which manager owns each field. Argo and Flux stamp labels for the rest.

Terraform doesn't think about ownership at all. If it knows about something and has access it will apply the diff anyway no matter who may in fact be accountable for the resources affected. Tools that behave this way subscribe to what I like to call 'Invisible Ownership'.

Companies who sell services to solve Invisible Ownership usually have a sales pitch that dismisses the mechanics of this as 'the easy part'. The fix is always misplaced as training, review and runbooks.

Nowhere in these sales pitches is Terraform rightly blamed for lacking support for ownership. That's exactly where the blame belongs and if you have ever done state surgery you already know this.

I have two infra toolchains for good people who are still reading.

[choudoufu](https://intentius.io/choudoufu/) puts ownership on the live resource in an OpenTofu fork, AWS only. [chant](https://intentius.io/chant/) is an infra compiler that does the same across more platforms.

Right now the record lands nowhere and the blame lands on whoever holds the pager.

---

## Read more

- [An entire industry exists to fix Terraform](https://lex00.github.io/posts/fix-terraform/)
- [Good tools can survive great "culture"](https://lex00.github.io/posts/good-tools-can-survive-great-culture/)
- [A plan preview for k8s with ownership](https://lex00.github.io/posts/a-plan-preview-for-k8s-with-ownership/)
- [choudoufu](https://intentius.io/choudoufu/)
- [chant](https://intentius.io/chant/)
