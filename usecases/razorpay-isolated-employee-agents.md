# Razorpay: Isolated, Always-On Employee Agents

**Class:** Independent deployment · **Confidence:** Medium-High · **Demo status:** Production case study; private deployment code

## Pain Point

Giving employees agents that hold code and credentials needs tenant isolation, controlled network access, and attributable activity.

## What It Does

Razorpay Engineering reports 220+ employee Hermes agents, each assigned its own Kubernetes namespace, encrypted volume, cloud identity, and network policy. A Google-authenticated gateway maps each user to their agent. Outbound requests go through a screened audit proxy; model access is routed through an internal gateway or Bedrock. Users retain agent state and can run scheduled work.

## Setup

The onboarding scripts, model gateway, and manifests are private. Reproduction requires an identity-aware entry point, per-user workloads and storage, explicit egress policy, and an attributable audit path. The article includes troubleshooting details rather than a public install package.

## Prompts

No employee task prompts are published.

## Skills Needed

- Hermes runtime, dashboard, memory, and scheduling
- Kubernetes storage, identity, and network-policy infrastructure
- Organization-specific authentication, model gateway, and egress audit proxy

## Notes

- Counts are author-reported. The screening layer is not a guarantee against every harmful request.
- Unlike [enterprise cloud providers](enterprise-cloud-deployment.md), this covers the complete per-employee runtime boundary.
- For a public declarative deployment tool, see the [Kubernetes operator](kubernetes-declarative-agent-fleet.md).

## Sources

- First-person engineering article: <https://engineering.razorpay.com/running-hermes-at-razorpay-a-network-isolated-self-improving-second-brain-for-every-employee-f91d56bea3f1>
- Hermes substrate: <https://github.com/NousResearch/hermes-agent>
