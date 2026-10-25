# Create a separate workspace profile

## Goal

Keep a new workflow's configuration, memory, and sessions separate from your everyday agent.

## Requires

Hermes and access to the model/provider you intend to configure.

## Steps

```bash
hermes profile create recipe-demo
hermes --profile recipe-demo setup
hermes --profile recipe-demo version
hermes --profile recipe-demo skills list
```

Create a fresh profile for a new trust boundary. A clone can copy credentials and memory; use cloning only when that is intentional. Profiles are configuration/state separation, not OS-user, filesystem, network, or full tenant isolation.

## Expected result

Commands targeting `recipe-demo` use that profile's configuration and state. Configure its model before attempting recipes that invoke the agent.

## Failure check

If the workflow sees unexpected settings, check that every setup, chat, cron, and gateway command uses the same `--profile` name. Starting a different profile's gateway does not validate this workflow.

## Sources

- [Profiles and cloning semantics](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
