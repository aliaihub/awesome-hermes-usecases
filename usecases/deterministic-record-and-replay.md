# Deterministic Record and Replay of Hermes Runs

**Class:** Ecosystem integration · **Confidence:** High · **Demo status:** Runnable

## Pain Point

A Hermes run that goes wrong is hard to examine twice. Re-running the same
prompt gives a different answer, because the model is sampled and the system
prompt carries the date and session; and the transcript on screen is not the
request that was sent — the 7,742-character system prompt, the 19 tool
schemas, and the exact SSE the provider streamed back are all invisible from
the terminal. So "why did it do that?" gets answered from memory rather than
from evidence, and a fix cannot be checked against the run that motivated it.

Worse for autonomous work: to ask "would a different model have made the same
call here?" you have to re-run the whole job on the other model and hope the
divergence reproduces.

## What It Does

OrcaReplay records a Hermes run at the process and socket boundary, then
re-executes it with the network switched off, serving the recorded exchanges
back byte for byte. From any checkpoint the run can be forked onto a different
model to see where behaviour diverges.

Capture sits **outside** Hermes. Nothing is installed into `~/.hermes`, no
plugin is loaded, and `config.yaml` is not touched — which matters here,
because Hermes has no base-URL variable to move. `OPENAI_BASE_URL` appears in
one place in the shipped source, an advisory warning for when it is set and
the provider is not `custom`; the origin itself lives in `config.yaml` under
`model.base_url`. So capture terminates the TLS Hermes established itself,
with a certificate authority minted for the single run and deleted when it
ends.

What one turn produced, from the verified run below:

- The full request: 42,305 bytes, 19 tools, a 7,742-character system prompt.
- The response: status 200, streamed, 10,615 input and 88 output tokens.
- Every shell command Hermes ran, with exit codes, and a per-turn diff of the
  files it touched, on one timeline with the model calls.
- `orca replay` reproducing all of it offline.

One Hermes-specific detail worth knowing, because it is the difference between
a full capture and a confusing half of one. Hermes makes two different kinds
of HTTP call with two different libraries: the model catalogue with
`requests`, and the completion with httpx under the OpenAI SDK. httpx pins
certifi and honours neither `REQUESTS_CA_BUNDLE` nor `SSL_CERT_FILE`; Hermes
resolves that client's CA itself, from `HERMES_CA_BUNDLE`
(`agent/ssl_verify.py`). A recorder that does not set that variable captures
the catalogue read and none of the completions.

## Setup

Node 20 or newer. The Hermes adapter is on the `hermes-adapter` branch,
pending review in the PR linked below; until it lands in a release, build from
the checkout:

```bash
git clone https://github.com/Continuum-AI-Corp/OrcaReplay.git
cd OrcaReplay
git checkout hermes-adapter   # or main, once PR #33 has landed
npm ci && npm run build
```

Record a run. `--tls-intercept` is required — there is no origin to redirect —
and `opencode.ai` is named explicitly because it is a website as much as a
gateway, so it is not in the default allowlist:

```bash
node packages/cli/dist/cli.js record hermes \
  --tls-intercept --tls-hosts '+opencode.ai' -- \
  --provider opencode-free -m nemotron-3.5-lightning-free \
  -z 'Compute 212000 plus 8 and reply with only the number.'
```

For Hermes on Nous' own models, drop `--tls-hosts`:
`inference-api.nousresearch.com` is in the default list.
`portal.nousresearch.com` deliberately is not — that is where the API key is
issued, and it stays tunnelled and unread.

Then, with no network:

```bash
node packages/cli/dist/cli.js replay <run-id>          # reproduce it exactly
node packages/cli/dist/cli.js show <run-id>            # the timeline
node packages/cli/dist/cli.js replay <run-id> --from 3 --model claude-sonnet-5
```

`-z` is the non-interactive flag. Without it Hermes opens a session and waits,
and the recording ends when you do.

## Prompts

The prompt used for the verified run — arithmetic on purpose, so the answer is
checkable and the run is short:

```text
Compute 212000 plus 8 and reply with only the number.
```

Hermes answered `212008`. The point of the example is not the arithmetic: it
is that the recording holds the 7,742-character system prompt and 19 tool
schemas that the terminal never showed, and that `orca replay` returns the
same bytes with the network off.

A second run, to see the same question answered by the recording rather than
the provider:

```bash
node packages/cli/dist/cli.js replay <run-id>
```

reported `reused=3/3`, exit 0. It also reported three `major` divergences,
which is the honest result and worth stating: Hermes' system prompt carries
the date and session identity, so the replayed request has an identical
trailing message and a different prefix. Divergence reporting is doing its
job — that is what a dynamic system prompt looks like on the wire.

## Skills Needed

None of Hermes'. No plugin, no skill, no gateway, and no change to
`config.yaml` — the recorder launches `hermes` as a child process and reads
the socket.

- Node 20+ for the recorder.
- The provider used above, `opencode-free`, is served anonymously, so the run
  needs no API key and no credential enters the recording. Any configured
  Hermes provider works; a credential is forwarded upstream and never written
  to the trace.
- Verified on Windows against **Hermes Agent v0.21.0 (2026.8.31)**, installed
  from git.

## Sources

- [Hermes configuration reference](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
  — the official docs for the behaviour this whole use case turns on: "When
  `base_url` is set, Hermes ignores the provider and calls that endpoint
  directly... When only `provider` is set, Hermes uses that provider's built-in
  auth and base URL." The origin is a config key, not an environment variable,
  which is why capture happens at the transport instead of by redirection.
- [OrcaReplay PR #33](https://github.com/Continuum-AI-Corp/OrcaReplay/pull/33)
  — the adapter, with the verification transcript: the recorded sizes, token
  counts, and the `orca replay` result quoted above. Also documents the
  `OPENAI_BASE_URL` finding, established against a listener with
  `model.base_url` pointed at a dead port.
- [`packages/adapters/src/hermes.ts`](https://github.com/Continuum-AI-Corp/OrcaReplay/blob/8399fb18773e26e000f548a7f978df5f064b64b0/packages/adapters/src/hermes.ts)
  and its recorded contract
  [`fixtures/harness/hermes.json`](https://github.com/Continuum-AI-Corp/OrcaReplay/blob/8399fb18773e26e000f548a7f978df5f064b64b0/packages/adapters/fixtures/harness/hermes.json),
  which carries the date the adapter was last confirmed against a running
  Hermes.
- [`prompt/HERMES/`](https://github.com/Continuum-AI-Corp/OrcaReplay/tree/8399fb18773e26e000f548a7f978df5f064b64b0/prompt/HERMES)
  — the captured system prompt as recorded, scrubbed of local paths.
- `agent/ssl_verify.py` in Hermes itself, for the `HERMES_CA_BUNDLE`
  resolution order that the setup above depends on.
