# New-use-case research — October 8, 2026

Compared candidates against the 68 existing catalog entries, their linked sources, and the unverified backlog at repository commit `6461920`. The previous badge said 67; counting the actual files and index rows exposed that stale count. Nine additions bring the catalog to 77. “New” means missing from this catalog, not necessarily first released this week.

Discovery began with the [official user-stories page](https://hermes-agent.nousresearch.com/docs/user-stories), then followed original repositories and first-person reports. Catalog entries distinguish implemented code, documented deployments, private configurations, and vendor demos. Exact prompts are reproduced only when published; otherwise their absence is stated.

## Added to the catalog

| Entry | Primary evidence | What makes it distinct |
| --- | --- | --- |
| [Service-business lead to payment](../usecases/service-business-lead-to-payment.md) | `hewi333/Mom-n-Pop-Skills`, including the current orchestrator skill | Service-job pricing and owner-approved customer/payment steps, rather than general ERP. |
| [Lead research to YouTrack](../usecases/lead-research-youtrack.md) | Halfbit Studio's first-person company workflow | Prospect-specific qualification and durable tickets, rather than a news digest. |
| [Box renewal copilot](../usecases/box-renewal-copilot.md) | Box developer tutorial plus bundled Hermes `box` skill | Cited cross-document briefing through Box AI for Hubs, followed by a verified Box Note. |
| [Document structuring](../usecases/document-structuring-spec-to-code.md) | `barnetwang/document_structuring` README and current skill | Indexed source specifications and firmware symbols, rather than conversation memory. |
| [Declarative Kubernetes agents](../usecases/kubernetes-declarative-agent-fleet.md) | `hermeum/hermes-agent-operator` | Reconciliation from desired-state manifests, rather than manual VPS setup. |
| [Razorpay employee agents](../usecases/razorpay-isolated-employee-agents.md) | Razorpay Engineering's detailed first-person deployment report | Complete per-employee runtime isolation, rather than model-provider configuration. |
| [Receipt extraction](../usecases/receipt-to-structured-json.md) | Nous' `plugin-llm-example` README and Python implementation | Implemented image/text-to-JSON extraction. |
| [Translation back-check](../usecases/translation-backcheck-plugin.md) | Nous' `plugin-llm-async-example` | Implemented concurrent translation/classification with a dependent back-translation. |
| [Final-reply number masking](../usecases/final-response-pii-redaction.md) | Nous' `plugin-hook-example` README and Python implementation | Output transformation before final transcript persistence, rather than execution sandboxing. |

## Evidence corrections retained in the entries

- Mom-n-Pop's current `lead-to-payment` skill says Stripe test mode and QuickBooks not wired. The catalog follows that implementation over the README's broader lead-to-books story.
- `document_structuring` now supports optional embeddings and hybrid search. Its original keyword-only description is incomplete. Retrieval budgets are estimates and ingestion still needs quality checks.
- The translation confidence label is a heuristic; it is not a measured accuracy score.
- Output masking can occur after raw CLI tokens have streamed, and covers specific number formats.
- Halfbit's future automation roadmap is separated from its reported research-and-ticket workflow.
- Box uses fabricated account documents. Razorpay's fleet size is author-reported and its deployment scripts are private.

## Candidates held back

| Candidate | Finding | Disposition |
| --- | --- | --- |
| Company Brain Kit / standup and reporting loop | A first-person guide and Hermes-specific repository now exist, but `sanjuacodez/company-brain-kit` has 2 stars and is not nascent. Its flat skill files also need adaptation to current skill discovery. | Updated the existing backlog row with sources and the remaining requirements; not promoted. |
| Local email gatekeeper | The first-person Reddit account links to a guide that currently renders “post not found.” A working public implementation was not established. | Not added to the catalog. |
| More voice interfaces, generic digests, and multi-agent coding teams | Substantial overlap with existing voice, briefing, and orchestration entries. | No duplicate catalog files. |

## Repository checks

Live public GitHub metadata checked during research:

| Repository | Stars at check | Catalog threshold |
| --- | ---: | --- |
| `hewi333/Mom-n-Pop-Skills` | 122 | Pass |
| `barnetwang/document_structuring` | 29 | Pass |
| `hermeum/hermes-agent-operator` | 46 | Pass |
| `NousResearch/hermes-example-plugins` | 42 | Pass |
| `sanjuacodez/company-brain-kit` | 2 | Hold |

All nine new entries passed `scripts/verify-usecase.py --check all --ci`. The script scored eight green and one yellow: Razorpay's article returned HTTP 403 to the HEAD checker, while its content was readable through web retrieval and manually inspected. Per-entry reports are committed alongside the entries. These scores measure the script's link and engagement signals, not application correctness or deployment success.

The index, badge, and 77 non-report use-case files agree; each new entry has the contribution-template sections and valid local links. `git diff --check` passed.

Source inspection and the repository's verification script check evidence and links. They do not demonstrate successful execution of paid services, provider calls, third-party deployments, or the private case-study stacks. No customer messages, payments, or deployments were performed for this update.
