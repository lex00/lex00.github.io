---
title: "Behold answers infra queries with Ladybug DB"
date: 2026-11-18
draft: false
featured_image: "img/behold-answers-infra-queries-with-ladybug-db-hero.svg"
---

[behold](https://intentius.io/behold/) now loads an estate into [LadybugDB](https://ladybugdb.com/), an embedded graph database, and answers Cypher queries over it.

An estate has more in it than its source. behold reads each member's resources from chant, the graph documents engines like choudoufu write for OpenTofu roots, and the cloud listings `behold index` takes from an AWS account or a Kubernetes cluster. All of it goes into one read-only database. A resource is a node, a reference between resources is an edge, and resources that carry the same cloud id are joined through that id.

An agent asks through `behold mcp`. Its `ask` tool takes a Cypher query with parameters, or a resource and a template from chant's catalog. A person asks in the graph pane at `/graph` on a served estate. Every query is checked as read-only before it runs and capped at 2,000 rows.

## One question

Asked "If GCP has an outage, which of our domains go with it?", the agent reads it as the DNS records that depend on GCP resources, and sends this with `{"record": "AWS::Route53::RecordSet"}`:

```cypher
MATCH (rec:Resource {kind: $record})-[:REF*1..4]->(dep:Resource {source: 'chant'})
WHERE dep.scopeKey <> rec.scopeKey
RETURN DISTINCT rec.key AS key, rec.name AS record, dep.key AS reaches, dep.kind AS kind
ORDER BY record, reaches
```

On the three-cloud example it returns 7 rows. Two Route 53 records reach into the GCP member and depend on four resources there: the forwarding rule and the address, proxy and URL map it uses.

![The ask demo after the agent's reply: the question and the agent's reading of it in the terminal, the Cypher query and its parameters in the pane, and the rows it returned](/img/behold-answers-infra-queries-with-ladybug-db-1.png)

The same estate answers questions that cross what any one tool declares: what breaks if the forwarding rule goes, what in the AWS account nothing in the workspace owns, and which IAM roles the cluster's pods can use through their ServiceAccounts. One question, whether SSH is open to the internet anywhere in the account, reads a real AWS account's ingress rules, indexed once with the account id redacted.

## In the browser

LadybugDB also ships a WebAssembly build. `behold export --graphdb` writes the loaded rows into the bundle with that build, so an exported graph pane answers Cypher with no server behind it.

The [ask demo](https://behold-ask-demo.intentius.workers.dev/) is one of those bundles. It plays a coding agent loading the three-cloud example into behold and asking it a question. The answers are a recording of a real run on emulators, plus that one read of a real account. After each answer the query box is yours, and what you type runs in the page over the same rows.

![The visitor's turn: the conversation has closed, the Cypher box and Ask button are lit, and the answer's rows and drawing show beside the estate graph](/img/behold-answers-infra-queries-with-ladybug-db-2.png)

## Read more

- [The graph database](https://intentius.io/behold/using/graph-database/): what behold loads, the model, and the ways to query it
- [The ask demo](https://intentius.io/behold/using/ask-demo/): how it's recorded, and how to run the same loop on your own estate
- [Queryable Infrastructure](/posts/queryable-infrastructure/)
- [behold](https://intentius.io/behold/)
- [LadybugDB](https://ladybugdb.com/)
