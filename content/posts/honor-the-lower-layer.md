---
title: "Honor the lower layer"
date: 2026-07-19
draft: false
---

This post makes one narrow claim, one you should check rather than take on faith.

Every tool sits on a lower layer. For infrastructure it is a cloud's native spec or a Kubernetes API. For a programming language it is the machine itself. Good abstractions honor that layer, while poor ones reimplement it with something that only pretends to match, up until the pretense breaks.

Two people in two fields, [Gregor Hohpe](https://www.linkedin.com/in/ghohpe) in software architecture and [Adam Chlipala](https://www.linkedin.com/in/adamch/) in formal verification, describe that same failure and the same fix.

<p style="text-align: center; font-size: 1.3em; font-weight: 700;"><a href="https://intentius.io/chant/">chant</a> is what the fix looks like for infrastructure: what you write is what you ship.</p>

The deployed spec is fixed by your source alone, readable before anything runs. That is the part people do not believe at first, and the part you can check. I can show where it lands and where other tools fall short. None of it rests on personal taste.

{{< inline-svg src="honor-the-lower-layer.svg" alt="A Venn of Hohpe and Chlipala, whose overlap is one shared rule: an abstraction is good only while it honors the layer below" >}}

## Hohpe: compiler, not illusion

His complaint, in his YOW! 2022 talk [*Infrastructure as Actual Code*](https://www.youtube.com/watch?v=uzc6p3qvH_k), is that our infrastructure tools are documents wearing the word code. The old automation formats, he argues, all look like documents, YAML and JSON, when he would rather write infrastructure in the language he writes applications in. He calls that document style "XML smell."

Hohpe's test for whether it is really code is the line between a compiler and code generation. A compiler emits a lower layer you do not read, the way almost no Java developer reads bytecode. Code generation only pretends to: it looks like a higher-level thing until it breaks and drops you back into the layer below. His slogan is "abstractions, not illusions."

Two properties keep it a compiler. A model with behavior you can predict, and errors that, when something goes wrong, point back at the line you wrote instead of the generated output. Done right, the generated spec ends up like machine code, something you never read. His own example of a tool that reaches this is AWS CDK.

## Chlipala: abstraction, not fiction

His work is formal verification, machine-checked proofs that a program does what it should. Lately, in [*The Expensive Fictions of Low-Level Programming Languages*](https://stng.substack.com/p/the-expensive-fictions-of-low-level), he wrote about using "formal verification as a fitness function to evaluate intermediate and final program variants," which is to say languages a machine can search over. He wants two things from a notation at once: "Some notations allow us to describe complex systems succinctly, and those notations are convenient to understand and manipulate algebraically. Some notations give us the control to describe every last detail of harnessing hardware for maximum performance."

Low-level languages give the second and lie about the first. They "pretend code looks like sequences of instructions that run one-at-a-time" and "pretend that there is one big shared memory that all parts of a program access." The bill is that "programming simplicity is sacrificed for control, making automated understanding of programs and their behavior ... formally impossible." Those are the expensive fictions.

## The same failure

Set them beside each other and the field is the only difference. Hohpe's illusion and Chlipala's fiction are one thing: an abstraction that reimplements the layer beneath it without honoring it. It works until it doesn't, and then it drops you into the very layer it was supposed to spare you, the generated spec or the real hardware. The abstraction that wins is the one that honors what is below, so you build on top and leave the lower layer alone.

## Why most infra tools clear one line

The rule sorts infrastructure tools cleanly, and almost none clear both lines.

{{< inline-svg src="where-the-tools-land.svg" alt="The two criteria as circles. CDK clears the real-language line but not the checkable-without-running line. Raw YAML clears the second but not the first. Terraform clears neither. chant is the overlap." >}}

Two ways an infra tool can honor its lower layer: it is a real language compiled to the spec, and its result is fixed enough that a machine can check it without running it.

Terraform and raw YAML both miss the first. Terraform reimplements the cloud as HCL plus a state file, a layer you cannot hand back and a road to hell of its own. Raw YAML is just data, fixed and readable but not a language you compile. Neither compiles a real language into the native spec, so no amount of care gets them to the first line. It is a limit built into their design.

Executing tools clear the first and miss the second. CDK is a real language compiled to a spec, which is why Hohpe points at it. But it synthesizes by running your program, so the output is known only after the run, and a lookup or an environment value or a tree-rewriting aspect can change it. You cannot check it without running it. The faithfulness is real, earned by careful code rather than guaranteed by design.

## What CDK proved

CDK is not the villain here. It is the closest any widely used tool with real success has come to both lines, which is why Hohpe cites it. It proved a real language compiled to a spec can carry production infrastructure.

You might expect the exception to be CDK's lowest level. The L1 constructs are close to a typed CloudFormation, and a careful L1-only project can produce the same spec every time. But it still produces that spec by running, so you cannot know it without a run, and the discipline that keeps it stable is yours, not the tool's. CDK executes at every level, L1 included, so a later loop over a lookup, or an aspect that rewrites the tree, undoes it. chant never runs, so the property holds whatever you write. The difference is not the construct level, it is execution versus compilation.

chant reaches the same place and carries it two steps further. It compiles the same way to CloudFormation, Kubernetes, and more, where CDK is AWS only. And the same-spec-every-time property that CDK holds only by hand, chant gets for free by never running. Neither step is a mark against CDK. They are simply where the idea goes once you drop the single platform and the runtime.

## Why chant is the overlap

chant honors the spec completely, and that is the only reason it can make this claim. You write a constrained subset of TypeScript, a real language, and it compiles straight to the native spec. The evaluability rules forbid a function call, a runtime branch, or a reach outside the source, so the same source always compiles to the same spec, checkable against the live system without a run. That is compilation, not execution: like a compiler folding constants, chant reduces your source and nothing else, so the output can depend on nothing but the text you wrote. Those are the two lines, and chant clears both by construction, not by hand.

The spec is never wrapped or reimplemented. It is the output, handed back exactly as the platform defines it. The reverse works too: chant imports an existing template, or a live cloud, into typed source, with roundtrip tests keeping the two faithful, so the native format is an input as much as an output. That output is data, the native spec itself, so chant reaches configuration as data by compiling a real language, where raw YAML gets there by making you write the data by hand. You author in code and ship data.

Hohpe wants that spec to read like machine code, something you never have to open, and chant gives you that. But nothing is opaque at either end. What you author is plain TypeScript you can read, type-check, and lint; what ships is the platform's own format. You never have to look down, and nothing is hidden when you do.

That openness is why agents work so well with chant. Because its lint rules are a static pass over the TypeScript AST, chant's language server runs them in your editor, so a bad change surfaces at the keystroke. Its MCP server then puts each change up for approval before it applies, so infrastructure becomes conversational: the agent proposes, the lint and the diff answer, you approve. The candidate is always checkable before it runs, Chlipala's fitness function arriving in infrastructure just as agents started writing it.

{{< inline-svg src="chant-compile-path.svg" alt="chant's path from source to native spec: TypeScript source, then parse and lint over the AST with the EVL rules in your editor, then a static compile, then the native spec. No stage executes your program." >}}

## The size of the claim

Neither Hohpe nor Chlipala is endorsing chant. Chlipala is not writing about infrastructure at all. Hohpe is, and the tool he holds up as his own example is AWS CDK, not chant. So this is not an appeal to their authority.

The claim is only this: two people, working apart in different fields, reached the same rule, and chant is the one infrastructure tool that keeps it. Whether that puts it ahead of CDK for your work is yours to decide. That it honors the lower layer is not.

## Sources

- Gregor Hohpe, [*Infrastructure as Actual Code*](https://www.youtube.com/watch?v=uzc6p3qvH_k), YOW! 2022. Quotations are transcribed from the talk.
- Adam Chlipala, [*The Expensive Fictions of Low-Level Programming Languages*](https://stng.substack.com/p/the-expensive-fictions-of-low-level), Structure and Guarantees.
