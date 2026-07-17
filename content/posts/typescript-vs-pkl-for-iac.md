---
title: "TypeScript vs Pkl for IaC"
date: 2026-05-27
---

Two tools have made the same uncommon choice. [chant](https://intentius.io/chant/) and [formae](https://github.com/platform-engineering-labs/formae) both refuse the authoritative state file. Most infrastructure tools keep one. These two do not. That shared move is the right place to start, because it is the right move.

## The state file was never the part that matters

An authoritative state file is a flat file doing a database's job. It needs a lock on every change. It holds secrets because the tool needs them to diff. It can corrupt and take a deploy down. Teams carry all of that because they believe state is essential. What is actually essential is governance. A known change before apply. An audit trail. A limit on blast radius. State was one way to get those. It was never the only way.

formae and chant both drop the file and keep the governance.

formae treats code as the source of truth. It reads live reality, sees changes made outside it, and merges them back into the code. There is no file to host.

chant treats live reality as the truth and the snapshot as a baseline. It synthesizes a native artifact, hands it off, and observes drift through snapshots in git. There is no file either.

Different mechanisms. Same rejection. Both are past the model that has defined IaC for a decade.

## Past that, the question is the language

Once the file is gone, what is left is how you write infrastructure. This is where the two part.

formae has you write Pkl, a configuration language built for the job. Typed, deterministic, with value constraints in the language itself.

chant has you write TypeScript. A resource is a typed object literal.

Both are code. One is a new language. The other is the one your team already writes. And one of them is structurally the spec.

## The spec is JSON, and so is a TypeScript object

Cloud specs are JSON or YAML. A CloudFormation template is JSON. A Kubernetes manifest is YAML, which is the same shape. A JSON document is almost already a TypeScript object literal. Same nesting, same values, the keys just lose their quotes.

chant leans all the way into this. The resource you write is the spec's data, typed. The AWS lexicon keeps CloudFormation's own property names and casing. `BucketEncryption` in your file is `BucketEncryption` in the template. The distance between what you author and what ships is almost nothing.

Pkl renders to the spec, but it is its own grammar. Amends, assignments, unquoted keys, no commas. It reads as Pkl. Between the Pkl you write and the JSON it becomes there is a translation, small but real, that lives in your head.

So for someone who already knows the spec, chant is the spec with types on it. Pkl is a second language pointed at the spec. Nothing gets closer to a JSON spec than writing it as a typed JSON object. That is what chant is.

## What about the constraints

There is an honest objection here, and it cuts the other way. The spec declares more than shape. The CloudFormation schema carries enums, patterns, and numeric bounds. Pkl can encode all of it in the type. A port can be an integer that refuses anything outside 1 to 65535, and a developer cannot even write the bad value.

TypeScript cannot say that. It can express an enum as a union, but not a numeric range or a regex bound. So chant carries those constraints as documentation and checks them in a separate semantic layer, not in the type. On that axis Pkl is more complete. It holds more of the spec inside the type than chant can.

The trade is what that completeness costs. To put constraints in the type, you need a type language rich enough to hold them, and that language is a step away from the spec's plain shape. chant makes the opposite trade. It keeps the authoring surface identical to the spec's data and moves constraint enforcement into linting. One choice is constraints in the type and a language of its own. The other is the spec's plain shape and constraints in a separate pass.

## Why the spec author wants the plain shape

If you already live in CloudFormation or Kubernetes manifests, the plain shape is the thing you know. chant lets you write it, typed, with completion drawn from the spec, and the object you write is the artifact that ships. There is no second language to learn and no mapping to maintain. Your knowledge transfers one to one. So do your editor, your tooling, and the model you ask to generate it, because all of them already speak TypeScript.

That is the case for chant over a config language. Not that constraints do not matter. They do, and Pkl holds more of them. But the closer you want to stay to the spec you already deploy, the less you want a new language in the middle. TypeScript as data is the smallest possible step from the spec, because the spec is already almost TypeScript.

## Both made the right call

Start where they agree. Dropping the authoritative state file is the correct move, and both tools made it while most of the field has not. That is the headline they share.

The split is the language. formae is the fuller tool. It deploys and reconciles where chant synthesizes and hands off. But on the narrow question of staying the spec instead of becoming another abstraction over it, TypeScript wins by construction. The spec is JSON. A typed object is JSON. There is nothing in between.
