---
title: "Behold answers infra queries with LadybugDB"
date: 2026-11-18
draft: false
featured_image: "img/behold-answers-infra-queries-with-ladybug-db-hero.svg"
---

The picture above is a small cloud setup drawn as a graph. Boxes are pieces of infrastructure like DNS records and load balancers. Each line means one piece depends on another. The lit path shows which web addresses go down when Google Cloud does.

<a href="https://intentius.io/behold/"><img src="/img/behold-icon.svg" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;">behold</a> is free and open source. It builds this graph from a team's own projects. A person asks their coding agent a question, and the agent writes the Cypher. Its graph engine is <a href="https://ladybugdb.com/"><img src="/img/ladybugdb-icon.png" alt="" style="display:inline;height:1.2em;width:1.2em;vertical-align:-0.25em;margin:0 0.3em 0 0;border-radius:50%;background:#fff;">LadybugDB</a>.

## Querying the graph

Infrastructure tools already keep a graph of your resources and the links between them. behold loads that graph into LadybugDB so an agent can query it for you.

## One question

A person types a question to their coding agent in plain words.

```text
> Which of our domains depend on another cloud?
```

The agent writes the Cypher for them and sends it to behold.

```cypher
MATCH (rec:Resource {kind: 'AWS::Route53::RecordSet'})-[:REF*1..4]->(dep:Resource)
...
```

Two domain names depend on four Google Cloud resources. The agent reaches behold through its MCP server.

## In the browser

LadybugDB also ships a WebAssembly build. This command writes a static page that carries the database.

```sh
npx behold export . --out ./behold-export --graphdb
```

Anyone who opens the page can run Cypher in their own browser.

## Read more

- [The graph database](https://intentius.io/behold/using/graph-database/)
- [Exporting a static page](https://intentius.io/behold/using/export/)
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [LadybugDB](https://ladybugdb.com/)
