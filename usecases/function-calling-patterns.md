# Function-Calling Patterns (Hermes-Function-Calling)

**Class:** Official companion · **Confidence:** High · **Demo status:** Companion repo

## Pain Point

You want to wire a Hermes-family model into a custom tool-calling loop — live financial data, structured JSON output, multi-step planning — but the generic OpenAI tool-calling examples don't map cleanly onto the Hermes prompt format. You need runnable, maintainer-shipped reference scripts that show the exact template, decorator, and recursion flags that work with the Hermes function-calling stack.

## What It Does

The `Hermes-Function-Calling` companion repo is the reference implementation for tool use on Hermes models. It ships example scripts that double as patterns — copy the shape, swap in your tools.

- **`functioncall.py`** — the main entry point. Default demo wraps `yfinance` to pull live stock prices and fundamentals. Flags that matter:
  - `--query` — the natural-language request (default: current TSLA price)
  - `--max_depth` — maximum recursive iterations (default 5); tool results feed back into the model for **multi-hop** function calling
  - `--num_fewshot` — include few-shot examples in context
  - `--load_in4bit` — bitsandbytes 4-bit loading
  - `--chat_template` — prompt format (default `chatml`)
- **`jsonmode.py`** — structured JSON output. Defines a Pydantic schema (the shipped example is a `Character` for a *Dragon Ball Z* entity: name, species, role, traits, special attacks) and validates model output against it.
- **`functions.py`** — the idiomatic tool-registration layer. Tools are defined with a `@tool` decorator, collected in `get_openai_tools()`, and converted via `convert_to_openai_tool(f)`.
- **`prompter.py`** — prompt builder. Reads the system prompt from YAML and fills `tools, examples, schema`. Supports the **GOAP-style `<scratch_pad>`** block (Goal / Actions / Observation / Reflection) shown in the Hermes-3 template for multi-step reasoning.

## Setup

```bash
git clone https://github.com/NousResearch/Hermes-Function-Calling
cd Hermes-Function-Calling
# follow repo's dependency install (transformers, pydantic, yfinance, bitsandbytes optional)
```

Run the shipped demos:

```bash
# live financial data via yfinance, single-hop
python functioncall.py --query "Current stock price and 52-week range of NVDA"

# recursive multi-hop: let the model chain tool calls up to depth 5
python functioncall.py --query "Compare P/E ratios of AAPL, MSFT, GOOGL" --max_depth 5

# structured JSON output against a Pydantic schema
python jsonmode.py --query "Return a JSON object for Goku from Dragon Ball Z"

# few-shot augmented function calling
python functioncall.py --query "..." --num_fewshot 3
```

## Prompts

The GOAP scratch-pad shape (from `prompter.py`, Hermes-3 template):

```
<scratch_pad>
Goal: <what the user wants>
Actions: <candidate tool calls, with args>
Observation: <result of the last action>
Reflection: <what to do next, or final answer>
</scratch_pad>
```

Registering a custom tool (`functions.py` pattern):

```python
from functions import tool, get_openai_tools, convert_to_openai_tool

@tool
def get_stock_price(ticker: str) -> dict:
    """Return the latest price for the given ticker."""
    ...

tools = [convert_to_openai_tool(get_stock_price)]
```

## Skills Needed

- A Hermes function-calling-capable model (Hermes-2-Pro-Llama-3-8B is the repo default; Hermes-3 for the GOAP template)
- GPU or API endpoint to serve the model (the repo loads locally via transformers; 4-bit if VRAM-tight)
- `yfinance` for the financial demo; Pydantic for JSON mode

## Notes

- **`--max_depth` is the multi-hop lever.** Depth 1 = one tool call then answer; higher depths let the model call a tool, read the result, call another, and synthesize. Watch for loops on ambiguous queries.
- **Pydantic is the contract in `jsonmode.py`.** The model is prompted to emit JSON; the validator enforces the schema. If your schema has optional fields, mark them `Optional` or the validator rejects valid-but-partial output.
- **`@tool` + `convert_to_openai_tool` is the project's idiomatic pattern** — don't hand-write the OpenAI tool JSON if you can decorate a function and let the converter build it.
- This repo predates the in-agent Hermes tool system; it's the reference for *model-level* function calling and for serving Hermes-FC over an OpenAI-compatible endpoint, not for the agent's own skill/MCP tools.

## Sources

- Companion repo: <https://github.com/NousResearch/Hermes-Function-Calling>
- Programmatic integration docs (rendered): <https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration/>