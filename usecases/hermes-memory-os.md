# Hermes Memory OS

**Class:** Ecosystem integration · **Confidence:** High · **Demo status:** Runnable local stack

## Pain Point

Long-running Hermes users accumulate decisions, preferences, project history, and facts across many sessions. Flat memory files alone eventually become hard to search and expensive to inject, while retrieved context can still be ignored or redundantly rediscovered by the model.

## What It Does

Memory OS adds seven cooperating layers to Hermes:

1. Workspace memory files injected every turn.
2. FTS5 search across session history.
3. Structured facts with entity resolution and trust scoring.
4. A modified Icarus/Fabric layer for cross-session extraction and recall.
5. Qdrant hybrid semantic search with lexical and SQLite fallbacks.
6. A self-curating wiki ingested into the vector store.
7. A `SOUL.md` and rulebook hierarchy that tells the agent how to treat injected ground truth.

Hooks recall relevant context before model calls, extract learnings afterward, deduplicate per session, and skip trivial social messages.

## Setup

Requirements are Hermes Agent, Docker, and Python 3.11+. The repository provides a one-command installer:

```bash
curl -sSL https://raw.githubusercontent.com/ClaudioDrews/memory-os/main/setup.sh | bash
```

The installer brings up Qdrant, Redis, and the ARQ worker, initializes the SQLite stores, and installs the Hermes-side components. The repository also provides a manual installation guide and smoke tests for troubleshooting.

## Prompts

Memory OS operates through Hermes hooks; it does not need a special prompt for every recall. A useful verification pattern is to record a concrete project decision in one session, start a new session, and ask:

```text
What decision did we make about this project's deployment, and why?
```

The expected behavior is retrieval from existing memory, not re-investigation with tools.

## Skills Needed

- Hermes Agent hook/plugin support
- Docker and Python 3.11+
- Qdrant, Redis, ARQ worker, and the bundled SQLite databases
- Optional local LLM provider; the memory infrastructure is provider-agnostic

## Notes

- This is substantially heavier than native `MEMORY.md`, `USER.md`, and session search. Use it when cross-session scale and structured recall justify additional services.
- The project is local-first, but the selected LLM provider may still receive recalled context. Local memory storage does not automatically make inference local.
- Review what the automatic extractor stores; durable memory can preserve sensitive or obsolete information.

## Sources

- Memory OS repository: <https://github.com/ClaudioDrews/memory-os>
- Hermes Agent repository: <https://github.com/NousResearch/hermes-agent>

