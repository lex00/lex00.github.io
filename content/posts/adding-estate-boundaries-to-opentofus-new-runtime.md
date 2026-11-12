---
title: "choudoufu runs on OpenTofu's new runtime"
date: 2026-11-12
draft: false
featured_image: "img/choudoufu-new-engine-toggle-hero.svg"
---

[choudoufu](https://intentius.io/choudoufu/) now runs on OpenTofu's new runtime.

OpenTofu is rebuilding the engine that plans and applies your infrastructure. Laurence Bordowitz, one of OpenTofu's maintainers, opened OpenTofu Day North America on November 9 with [a talk about the rewrite](https://cncf-hosted-co-located-events-north-america-2026.sessionize.com/session/1266401). The project calls it the new runtime, and it's still being built.

choudoufu is a fork of OpenTofu, and it now runs on that new engine too. You can try it on your own configurations today, with choudoufu's estate boundaries working on top of it.

## Trying it

Set one environment variable:

```
TOFU_X_EXPERIMENTAL_RUNTIME=1 choudoufu plan
```

That's the same variable upstream OpenTofu uses, so nothing choudoufu-specific to learn. Leave it unset and choudoufu behaves exactly as it did before.

If your configuration uses something the new runtime can't do yet, choudoufu runs that plan on the old engine and tells you so in the output. You don't get a half-working plan, and you don't have to work out which features are supported before you try.

## What estate boundaries give you

choudoufu's live backend puts a small ownership tag on every cloud resource it manages and reads it back on the next plan. That tag is what lets one team's infrastructure sit next to another's without a shared state file in the middle:

- IAM decides which estate can touch which resources, using the tag ([how that works](https://intentius.io/choudoufu/how-it-works/across-estates/)).
- Two teams can apply at the same time without waiting on each other's lock ([more on that](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/)).
- A resource that moved in your code is found by its tag, so renaming things doesn't destroy and recreate them.
- A plan that went stale while it waited for approval is refused instead of applied.

All of that now works on the new runtime as well as the old one.

![Apply A changes db and apply B changes subnet. Under Terraform B waits for A's lock on the whole state file. Under choudoufu the resources sit in two estates, so both applies land. A stale saved plan on db is refused](/img/concurrency-lock-scope.png)

## Also new: secrets in SSM

choudoufu can already refuse to keep secrets at all. Now there's a second option: secret values go to AWS SSM Parameter Store, encrypted under your own KMS key, and choudoufu's records keep only a pointer to them.

## Staying close to OpenTofu

choudoufu tracks OpenTofu's main branch and syncs every two weeks while the new runtime is under construction. Where choudoufu has had to fill a gap itself, the patch is marked with the upstream issue that will replace it, and it gets deleted once OpenTofu ships its own version. The goal is a fork that gets smaller over time. [How choudoufu differs from upstream](https://intentius.io/choudoufu/how-it-works/upstream/) lists every difference.

## One known issue

On the new runtime, a `moved` block that renames a whole module crashes the apply. A fix is in progress. The old engine isn't affected, so leave the variable unset for that change until the fix ships.

## Read more

- [A live demo](https://demo.intentius.io): terragucci running choudoufu across three estates
- [Release notes](https://github.com/INTENTIUS/choudoufu/blob/main/CHANGELOG.md)
- [Resource-level concurrency for Terraform](https://lex00.github.io/posts/resource-level-concurrency-for-terraform/)
- [Tofu tastes better with live markers](https://lex00.github.io/posts/tofu-tastes-better-with-identity-hooks/)
