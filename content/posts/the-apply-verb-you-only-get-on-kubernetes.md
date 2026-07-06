---
title: "The apply verb you only get on Kubernetes"
date: 2026-07-06
---

Kubernetes made something uniform that people forget was ever a choice. Every service deploys the same way. A manifest describes the desired state, `kubectl apply` hands it over, and a controller makes it real. Because the verb is shared, the CI around it is shared too. A platform team writes one pipeline and a hundred services ride it, since from the pipeline's point of view they are all the same operation.

Step off the cluster and that uniformity is gone.

On EC2, ECS, and CloudFormation there is no shared apply verb. Building an image is one thing, promoting it is another, applying a stack is a third, and handing one stack's outputs to the next is a fourth. None of it is standardized, so all of it ends up in the pipeline. And because the pipeline is where the variance lives, the pipeline is what multiplies. Every service grows its own.

You know what this turns into. Somewhere in each service's deploy job is a block that reaches into another stack to find the values it needs.

```bash
OUTPUTS=$(aws cloudformation describe-stacks --stack-name shared-alb \
  --query 'Stacks[0].Outputs' --output json)
LISTENER_ARN=$(echo "$OUTPUTS" | jq -r '.[] | select(.OutputKey=="ListenerArn") | .OutputValue')
aws cloudformation deploy --stack-name my-service \
  --parameter-overrides ListenerArn="$LISTENER_ARN" Image="$IMAGE_URI"
```

Two services behind one load balancer means two copies of that. Add a third and you copy it again. Change how you deploy and you edit every copy. The pipeline count tracks the service count, and the glue drifts service by service until no two are quite the same.

---

Plenty of tools attack a piece of this. None of them attack all of it, and the way each one falls short is consistent enough to draw.

{{< inline-svg src="off-cluster-deploy-venn.svg" alt="A three-circle Venn of composable components, generates the pipeline, and your runner on any cloud, with CDK and Copilot in one overlap, Pulumi in another, CI components in a third, and chant alone in the center" >}}

Start with the frameworks that give you composition. AWS CDK builds services out of constructs, and CDK Pipelines emits a pipeline that deploys your stacks in order with the cross-stack references resolved for you. It is a real answer. It is also AWS only, the pipeline it generates is CodePipeline rather than the GitLab or GitHub you already run, and the whole thing is a framework you commit to. AWS Copilot tells the same story pointed at ECS, with a manifest per service and a generated pipeline that stops hard at the edge of ECS. Both give you composition and both generate the pipeline. Neither runs on the CI you have.

Pulumi sits in a different overlap. Its components are real, it spans clouds, and you run it wherever you like. But it does not generate the pipeline. You still write the orchestration that calls it. Composition and openness, without the generation.

Then there is the answer a good engineer reaches for first, which is to use what the CI platform already gives you. GitLab CI/CD Components and GitHub reusable workflows are genuine reuse. They are also reuse of pipeline code, not a model of your services. You still hand-write the deploy logic and the `jq` inside the reusable job. No generic runner, no dependency-derived ordering, no cross-stack wiring. It moves the copy-paste up a level without removing it.

A couple of tools do not sit cleanly in any of the three regions. Terragrunt passes outputs between modules in dependency order, which is exactly the cross-stack move, but it is Terraform only and has no build or publish story. Spinnaker and Harness will template pipelines across clouds, but you adopt their platform to get it, which is the thing you were trying to avoid. They belong in the table more than on the diagram.

{{< inline-svg src="off-cluster-deploy-matrix.svg" alt="A capability matrix comparing chant, CDK Pipelines, AWS Copilot, Pulumi, Terragrunt, CI components, and Spinnaker across composable components, generates plain CI, your existing runner, any cloud, cross-stack wiring, and build and publish" >}}

---

Read the diagram by its empty spaces. Each tool is missing exactly one circle. CDK and Copilot do not run on your CI. Pulumi does not generate the pipeline. The CI-native components are not a component model. The center, where all three overlap, is where the pain actually goes away, and it is mostly empty.

[chant](https://intentius.github.io/chant/) is built to sit there. You describe each service as data. One generic runner deploys them all, with no per-service code in the runner itself. Adding a service is one declaration and no new pipeline. And it generates the CI you already run, turning the dependency graph into one thin job per service, with each stack's outputs handed to the next job as an artifact instead of scraped back out with `jq`. There is a [runnable version](https://github.com/INTENTIUS/chant/tree/main/examples/adopt-alb-services) with two services on a shared load balancer, the bespoke pipeline and the generated one side by side.

None of the individual moves are novel. Composition, pipeline generation, and cross-stack wiring all exist already. What is missing everywhere else is having them in one place, on the runner you already have, without picking a cloud first. Kubernetes got deploy uniformity by giving everyone one verb. Off the cluster you get it by describing your services as data and generating the pipeline from them, so the hundredth service stays as cheap as the first.
