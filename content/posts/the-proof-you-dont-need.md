---
title: "The best proof is the one you don't need"
date: 2026-07-18
draft: true
---

AWS CDK ships a machine-checked Alloy model that proves its IAM statement merging preserves the meaning of your policy. It is careful, serious work, maintained upstream. It is also worth asking why it has to exist at all.

It exists because the merge is risky. CDK runs an algorithm at synth that combines IAM statements, and a wrong combination silently changes what your policy allows. `Principal: "*"` and `Principal: {"AWS": "*"}` are not the same, and merging them would be a real security bug. So they proved the algorithm safe. You prove the thing you run.

## Don't run the risky thing

chant's answer to a risky synth-time algorithm is not to run one. There is no statement merge, so there is no merge to prove. If you need two statements you write two statements, or a composite writes them, and the output is exactly what you wrote.

That is the general shape. The behavior that would need a proof is the behavior chant does not have. Same source, same output, every time.

## What you get instead

None of this is a formal proof, and I am not going to call it one. It is three plainer things.

Synthesis is a pure function of the source, so every value in the output traces to a literal, a constant, or a reference. You do not prove the derivation. You re-run it and read it. That is auditability by construction.

Type checking, semantic lint, and a plan against the live system run before anything ships. They are computed and machine-checkable, and they answer the questions that matter: is this valid, and what will it touch. That is validation before apply.

A component attaches an SBOM, SLSA provenance, and a keyless signature to the artifact, and a verify gate stops the deploy if any of it fails to check. That is a chain of custody from source to signed output.

## Two different things to prove

CDK proves an algorithm. The Alloy model answers whether the merge is safe, because the merge is the dangerous part.

chant proves provenance and reproducibility. The signature answers whether the artifact came from this source. Determinism answers whether the same source gives the same output. Neither is a proof of the machinery, because there is almost none to prove.

That is the trade under all of it. CDK earns trust by proving its synth-time behavior safe. chant earns it by not having synth-time behavior worth proving, and by signing what comes out.

## The proof you skip

The strongest proof is the one you never write, because you removed the thing that needed it. A merge you do not run cannot combine two principals by mistake. A value that is never computed at synth cannot drift there. Remove the behavior and its questions leave with it. Then sign what is left.
