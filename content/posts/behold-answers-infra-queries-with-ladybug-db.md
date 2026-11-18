---
title: "Behold answers infra queries with Ladybug DB"
date: 2026-11-18
draft: false
featured_image: "img/behold-answers-infra-queries-with-ladybug-db-hero.svg"
---

The picture above is a small cloud setup drawn as a graph. Boxes are pieces of infrastructure like DNS records and load balancers. Each line means one piece depends on another. The lit path shows which web addresses go down when Google Cloud does.

[behold](https://intentius.io/behold/) is free and open source. It builds this graph from a team's own projects and answers Cypher over it. Its graph engine is [LadybugDB](https://ladybugdb.com/).

## Infrastructure is a graph

Code declares infrastructure and cloud accounts run it. Clusters build on top. Each piece points at others. A DNS record points at a load balancer, which points at a proxy. A Kubernetes service account points at an AWS role.

The questions engineers ask before a change follow those links. What depends on this? What can reach that? What runs beyond the code? behold loads every source into one LadybugDB database, with resources as nodes and references as edges, so each question fits in a few lines of Cypher.

## One question

Here is that question, which domains a GCP outage takes with it, in Cypher.

```cypher
MATCH (rec:Resource {kind: 'AWS::Route53::RecordSet'})-[:REF*1..4]->(dep:Resource {source: 'chant'})
WHERE dep.scopeKey <> rec.scopeKey
RETURN DISTINCT rec.name AS record, dep.key AS reaches
```

On the sample setup, two domain names depend on four Google Cloud resources behind its load balancer.

![The ask demo after the agent's reply](/img/behold-answers-infra-queries-with-ladybug-db-1.png)

Coding agents ask through behold's MCP server, whose `ask` tool takes Cypher. People ask in a pane in the browser. Everything is read-only.

## In the browser

LadybugDB also ships a WebAssembly build. A behold export carries the database inside a static page, which answers on its own.

The [ask demo](https://behold-ask-demo.intentius.workers.dev/) is one of those pages. It replays a coding agent asking behold about a sample setup, recorded from a real run. After each answer the box is yours, and what you type runs in your browser on LadybugDB.

![The visitor's turn in the ask demo](/img/behold-answers-infra-queries-with-ladybug-db-2.png)

## Read more

- [The ask demo](https://behold-ask-demo.intentius.workers.dev/)
- [The graph database](https://intentius.io/behold/using/graph-database/)
- [The same loop on your own projects](https://intentius.io/behold/using/ask-demo/#the-same-loop-on-your-estate)
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [LadybugDB](https://ladybugdb.com/)
