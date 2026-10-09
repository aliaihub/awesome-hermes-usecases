# Declarative Hermes Agents on Kubernetes

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Public operator + runbook

## Pain Point

Team agents configured by editing running containers develop drift. Their skills, schedules, credentials, and workspaces lack a reviewable desired state.

## What It Does

`hermeum/hermes-agent-operator` reconciles a `HermesAgent` custom resource into a running Hermes deployment. Manifests can declare configuration, skills, cron jobs, workspace content, plugins, and storage. Teams can review those declarations through Git before Kubernetes applies them.

## Setup

The source requires a Kubernetes cluster and Helm v3:

```bash
helm upgrade hermes-agent-operator oci://ghcr.io/hermeum/charts/hermes-agent-operator \
  --install --namespace hermes-agent --create-namespace
```

Create `my-hermes-secret` in the agent's namespace with its provider credentials, then save and apply an adapted upstream manifest:

```yaml
apiVersion: agents.hermeum.app/v1alpha1
kind: HermesAgent
metadata:
  name: my-agent
spec:
  hermes:
    config:
      raw:
        model:
          provider: anthropic
          default: claude-sonnet-4-6
    envFrom:
      - secretRef:
          name: my-hermes-secret
    storage:
      persistence:
        enabled: true
        size: 10Gi
```

```bash
kubectl apply -f my-agent.yaml
kubectl get hermesagent my-agent
kubectl get pods -l app.kubernetes.io/instance=my-agent
```

The cluster needs a suitable storage class for the persistent volume. Review the upstream CRD and Helm values for your deployment.

## Prompts

The operator also publishes an actual scaffolding skill:

```bash
hermes skills install hermeum/hermes-agent-operator/skills/hermes-agent-operator
```

Invoke `/hermes-agent-operator` in Hermes to scaffold a custom resource. The manifest remains the reviewable deployment artifact.

## Skills Needed

- Kubernetes and Helm v3
- HermesAgent CRD and operator
- Provider secret; persistent storage for durable agent state
- Optional operator scaffolding skill

## Notes

- Declarative reconciliation is the addition here; it is different from choosing an [enterprise model endpoint](enterprise-cloud-deployment.md).
- Skill instructions do not replace Kubernetes RBAC and network policy.
- This is a community operator, not a first-party Nous deployment service.

## Sources

- Operator, complete schema, and install guide: <https://github.com/hermeum/hermes-agent-operator>
- Hermes profiles and state: <https://hermes-agent.nousresearch.com/docs/user-guide/profiles>
