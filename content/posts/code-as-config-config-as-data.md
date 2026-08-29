---
title: "Configuration as code, and as data"
date: 2026-07-20
featured_image: "img/code-as-config-cover.svg"
---

[Brian Grant](https://medium.com/@bgrant0607) coined the [Kubernetes Resource Model](https://kube.fm/krm-brian) and argues that configuration should be data, not a program you run to find out what it is. chant agrees, and most of the industry is still catching up to him.

His argument is that declarative configuration is data. It is separated from the code that transforms it. This is a huge part of what makes Kubernetes manageable.

# chant is configuration as data

chant compiles a typed source to the platform's own spec and hands that spec back untouched. 

The output is declarative data in the format the platform already speaks. It sits apart from the compiler that produced it and can be read and checked before anything runs. 

[Brian's definition](https://itnext.io/what-is-configuration-as-data-210b0c4be324) has two halves. Represent configuration as data, and store and manage it like data.

chant takes the first half. The spec it emits holds up to reading and checking before anything runs. ConfigHub takes both, and keeps the data in a store. chant leaves it in git.

# chant is configuration as code

You author chant in a real typed language, and a compiler turns it into the data. Code on the way in, data on the way out. 

The compiler changes the format, not the config.

# Accessible Ops

[Being both is the better combination, for agents and for people](https://accessibleops.net)

Configuration as code is what makes configuration as data comfortable for a person and reliable for an agent. 

chant is both.

For the language side of this, and why TypeScript lets a tool be both at once, see [TypeScript is the right choice for infra](/posts/typescript-is-the-right-choice-for-infra/).

---

## Read more

- [TypeScript is the right choice for infra](https://lex00.github.io/posts/typescript-is-the-right-choice-for-infra/)
- [Your infra database is a road to hell](https://lex00.github.io/posts/your-infra-database-is-a-road-to-hell/)
- [Honor the lower layer](https://lex00.github.io/posts/honor-the-lower-layer/)
- [Which infrastructure tool actually keeps the spec?](https://lex00.github.io/posts/which-tool-keeps-the-spec/)
- [chant how it compares](https://intentius.io/chant/concepts/comparison/)
- [chant](https://intentius.io/chant/)
