---
title: "Behold answers infra queries with Ladybug DB"
date: 2026-11-18
draft: false
featured_image: "img/behold-answers-infra-queries-with-ladybug-db-hero.svg"
---

The picture above is a small cloud setup drawn as a graph. Boxes are pieces of infrastructure like DNS records and load balancers. Each line means one piece depends on another. The lit path shows which web addresses go down when Google Cloud does.

<a href="https://intentius.io/behold/"><img src="/img/behold-icon.svg" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">behold</a> is free and open source. It builds this graph from a team's own projects and answers Cypher over it. Its graph engine is <a href="https://ladybugdb.com/"><img src="/img/ladybugdb-icon.png" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;border-radius:50%;background:#fff;">LadybugDB</a>.

## Querying the graph

Infrastructure tools already keep a graph of your resources and the links between them, and use it to plan each change. behold loads that graph into LadybugDB so you can query it directly.

## One question

Here is that question, which domains a GCP outage takes with it, in Cypher.

```cypher
MATCH (rec:Resource {kind: 'AWS::Route53::RecordSet'})-[:REF*1..4]->(dep:Resource {source: 'chant'})
WHERE dep.scopeKey <> rec.scopeKey
RETURN DISTINCT rec.name AS record, dep.key AS reaches
```

On a sample three-cloud setup, two domain names depend on four Google Cloud resources behind its load balancer.

Coding agents ask through behold's MCP server, whose `ask` tool takes Cypher. People ask in a pane in the browser. Everything is read-only.

## In the browser

LadybugDB also ships a WebAssembly build. `behold export --graphdb` writes a static page that carries the database. Anyone who opens it can run Cypher in their own browser.

## Read more

- [The graph database](https://intentius.io/behold/using/graph-database/): what behold loads, and how to query it
- [Exporting a static page](https://intentius.io/behold/using/export/)
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [LadybugDB](https://ladybugdb.com/)
