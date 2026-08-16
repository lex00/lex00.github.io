---
title: "Defending Terraform is a tough job in 2026"
date: 2026-07-28
draft: true
---

Are you in the difficult position of defending a tool built on Terraform in 2026?

Positioning Terraform as the best infra toolchain available today is more difficult than ever. The problem is not the state file. It is the workflow the record binds you to.

The problems:

- mistakes surface at plan and apply, not in the editor
- a plan means nothing without credentials and a cloud round trip
- before you may manage anything that already exists, you import it, resource by resource, into the record
- adopting a spec means converting it to the tool's format, and leaving means converting back
- two people touching the same estate coordinate through the record, however the record is stored
- a delete is authorized by [absence from the record](/posts/your-infra-database-is-a-road-to-hell/)
- when the record and reality disagree, reconciling them is your job, on your calendar
- day-two operations get a [trigger with no executor](/posts/a-lifecycle-needs-an-orchestrator/)
- the output is not the platform's spec, so there is [nothing to hand back](/posts/honor-the-lower-layer/) when you leave
- an [entire industry](/posts/fix-terraform/) staffs and tools this workflow
- the license changed, and the community forked rather than leave the workflow

The narrative that answers them:

- concede the language complaints, call them beside the point
- grant every state problem
- declare the core sound and settled long ago
- attribute remaining criticism to inexperience
- call infrastructure inherently hard at scale
- note that no language fixes the clouds
- declare it the best tool available, by a wide margin
- invite alternatives

Every problem is in the first list. The answer to each is in the second.

---

## Read more

- [An entire industry exists to fix Terraform](/posts/fix-terraform/)
- [Your infra database is a road to hell](/posts/your-infra-database-is-a-road-to-hell/)
- [A lifecycle needs an orchestrator](/posts/a-lifecycle-needs-an-orchestrator/)
- [Honor the lower layer](/posts/honor-the-lower-layer/)
- [Flame graphing the leftness of infra tooling](/posts/flame-graphing-the-leftness-of-infra-tooling/)
- [chant](https://intentius.io/chant/)
