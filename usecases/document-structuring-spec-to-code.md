# Large-Spec Retrieval and Spec-to-Code Evidence

**Class:** Ecosystem integration · **Confidence:** Medium-High · **Demo status:** Public CLI + Hermes-compatible skill

## Pain Point

Loading a hardware manual or firmware codebase into a chat can exhaust the context window before the agent finds the relevant section.

## What It Does

Barnet Wang's `document_structuring` toolkit gives Hermes a `doc-str` skill: index PDF/DOCX documents, C/H symbols, and EDK2 configuration sections in SQLite, inspect the table of contents, then retrieve small evidence chunks. Current code supports FTS5 plus optional CPU embeddings and hybrid search; the original keyword-only account no longer describes the full implementation.

## Setup

For the default Hermes profile, adapt the repository's skill-copy instructions to the official skills directory:

```bash
git clone https://github.com/barnetwang/document_structuring.git
mkdir -p ~/.hermes/skills
cp -r document_structuring ~/.hermes/skills/doc-str
python -m pip install -e ~/.hermes/skills/doc-str
```

Run indexing and retrieval from one stable working directory, or specify a stable base directory. Use a Python environment accessible to Hermes' terminal.

## Prompts

The upstream skill specifies this CLI workflow; its filenames and query are examples from the public README:

```bash
doc-str parse --file "AMD_PPR_Spec.pdf" --tags "bios,amd,ppr" --output parse_result.json
doc-str list --output documents.json
# Use the returned document ID, rather than assuming it is 1.
doc-str toc --doc-id <document-id> --output toc.json
doc-str search --query "S3ResumeBoot gEfiSmmBase2ProtocolGuid" --mode fts --limit 3 --output search.json
doc-str get-chunk --chunk-id <returned-chunk-id> --format xml --output chunk.xml
```

Replace the angle-bracket IDs before running. For hybrid retrieval, run `doc-str embed` for the selected document first.

## Skills Needed

- `doc-str` skill and its Python CLI dependencies
- Hermes terminal and file tools
- SQLite FTS5; optional fastembed CPU embedding model

## Notes

- Check chunk counts, TOC quality, and sample content after ingestion.
- Ingest serially; same-named files share document identity.
- Token budgets are estimates, and extraction has documented table and code-coverage limits.
- Retrieved spec/code pairs are evidence to inspect, not proof of implementation conformance.
- Unlike [Memory OS](hermes-memory-os.md), this indexes source documents and code rather than agent conversations.

## Sources

- Toolkit, CLI, and limitations: <https://github.com/barnetwang/document_structuring>
- Current agent workflow: <https://github.com/barnetwang/document_structuring/blob/main/SKILL.md>
- Official Hermes skill directory: <https://hermes-agent.nousresearch.com/docs/user-guide/features/skills>
