#!/usr/bin/env python3
"""Render the README catalog and page summaries from catalog.json (stdlib only)."""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- catalog-summary:start -->"
END = "<!-- catalog-summary:end -->"
FORMATS = {"Guide", "Plugin", "Skill", "Project", "Case study", "Local demo", "Walkthrough"}


def anchor(title):
    return title.lower().replace("&", "").replace(" ", "-")


def load_catalog():
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    entries = data["entries"]
    slugs = [entry["slug"] for entry in entries]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Duplicate use case in catalog.json")
    pages = {p.stem for p in (ROOT / "usecases").glob("*.md") if not p.name.endswith(".verification.md")}
    if set(slugs) != pages:
        raise ValueError(f"Catalog/page mismatch: {set(slugs) ^ pages}")
    categories = [category for group in data["groups"] for category in group["categories"]]
    if len(categories) != len(set(categories)):
        raise ValueError("Duplicate category")
    for entry in entries:
        if entry["category"] not in categories or entry["format"] not in FORMATS:
            raise ValueError(f"Invalid category or format: {entry['slug']}")
        for field in ("title", "outcome", "requires"):
            if not entry[field].strip() or any(c in entry[field] for c in "|\n\r"):
                raise ValueError(f"Invalid {field}: {entry['slug']}")
    featured = data["featured"]
    if len(featured) != 6 or len(set(featured)) != 6 or not set(featured) <= set(slugs):
        raise ValueError("Featured list must contain six distinct catalog entries")
    return data


def row(entry):
    return f"| [{entry['title']}](usecases/{entry['slug']}.md) | {entry['outcome']} | {entry['format']} |"


def render_readme(data):
    entries = data["entries"]
    by_slug = {entry["slug"]: entry for entry in entries}
    counts = Counter(entry["category"] for entry in entries)
    lines = [
        '<p align="center">',
        '  <img src="assets/hermes-agent-usecases.png" alt="Hermes Agent — Real-World Use Cases" width="800">',
        "</p>", "", "# Awesome Hermes Agent Use Cases", "",
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        f"![Use Cases](https://img.shields.io/badge/usecases-{len(entries)}-blue?style=flat-square)",
        "![Last Update](https://img.shields.io/github/last-commit/aliaihub/awesome-hermes-usecases?label=Last%20Update&style=flat-square)",
        "![Stars](https://img.shields.io/github/stars/aliaihub/awesome-hermes-usecases?style=flat-square)",
        "![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)", "",
        "**Practical workflows, community projects, and deployment guides for [Hermes Agent](https://github.com/NousResearch/hermes-agent).**",
        "", "Browse by the result you want, then open a page for requirements, setup, prompts, and sources. Public evidence and execution testing are different: each page states its validation limits.",
        "", "**Build something:** [Starter kits](demos/README.md) · [10 reusable recipes](recipes/README.md) · [Tested results](docs/tested-results.md)",
        "", "## Start here", "",
        "Six entry points, from everyday automation to specialist tools. These are featured examples, not a difficulty ranking.",
        "", "| Use case | What you get | Format |", "| --- | --- | --- |",
    ]
    lines += [row(by_slug[slug]) for slug in data["featured"]]
    lines += ["", "## Find a use case", ""]
    for group in data["groups"]:
        lines += [f"**{group['title']}**", ""]
        for category in group["categories"]:
            lines.append(f"- [{category}](#{anchor(category)}) · {counts[category]}")
        lines.append("")
    lines += [
        "**Formats:** **Local demo** includes a starter in this repo; **Plugin**, **Skill**, and **Project** link to an implementation; **Guide** provides a runbook or configuration; **Case study** describes a deployment that may include private components; **Walkthrough** includes planning examples.",
        "", "A format label describes what is available. It does not mean we ran or audited the integration.",
        "", "<!-- catalog-list:start -->",
    ]
    for group in data["groups"]:
        lines += ["", f"## {group['title']}"]
        for category in group["categories"]:
            lines += ["", f"### {category}", "", "| Use case | What you get | Format |", "| --- | --- | --- |"]
            lines += [row(entry) for entry in entries if entry["category"] == category]
            lines += ["", "[↑ Browse categories](#find-a-use-case)"]
    lines += [
        "", "<!-- catalog-list:end -->", "", "## Install Hermes", "",
        "Choose a workflow first, then follow its setup. For a new Hermes installation:", "", "```bash",
        "curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash",
        "hermes setup", "```", "", "## Demos and walkthroughs", "",
        "Three starter demos are included in this repo. They require their own provider and platform configuration:", "",
        "| Starter | What it demonstrates |",
        "| --- | --- |",
        "| [Daily Briefing](demos/daily-briefing/) | Scheduled research and Telegram delivery |",
        "| [Open WebUI](demos/openwebui/) | Hermes API server with a browser frontend |",
        "| [Team Telegram](demos/team-telegram/) | Shared messaging gateway and Docker terminal backend |", "",
        "The [Matt Pocock skills walkthrough](demos/matt-pocock-skills/) contains sample plans, PRDs, and issue breakdowns. It is a planning example, rather than a fourth executable starter.",
        "", "## Evidence and contributing", "",
        "New entries need a primary public source: official docs, a companion repository, a deployment issue, or a first-person account. Social posts alone belong in the [research backlog](research/unverified.md). Historical evidence gaps are called out in page summaries.",
        "", "Automated [verification](docs/verification-criteria.md) checks source availability and repository engagement. Those checks do not establish that a workflow works end to end. See [tested results](docs/tested-results.md) for execution evidence and its limits.",
        "", "See [CONTRIBUTING.md](CONTRIBUTING.md) for the page template and evidence rules. The [catalog data](catalog.json) keeps categories, summaries, and counts in sync:", "",
        "```bash", "python scripts/render-catalog.py", "python scripts/render-catalog.py --check", "```", "",
        "Run the source checker for a new or substantively changed workflow:", "", "```bash",
        "python scripts/verify-usecase.py --usecase usecases/my-topic.md --check all", "```", "",
        "## License", "", "[MIT](LICENSE) for code and configs. Docs and diagrams under [CC BY 4.0](LICENSE-docs).", "",
        "## Acknowledgements", "",
        "Catalog format inspired by [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases). Hermes Agent is built by [Nous Research](https://nousresearch.com).", "",
    ]
    return "\n".join(lines)


def render_page(entry, text):
    title, body = text.split("\n", 1)
    if not title.startswith("# "):
        raise ValueError(f"Missing page title: {entry['slug']}")
    if START in body:
        if body.count(START) != 1 or body.count(END) != 1:
            raise ValueError(f"Invalid summary markers: {entry['slug']}")
        body = re.sub(re.escape(START) + r".*?" + re.escape(END), "", body, count=1, flags=re.S)
    validation = entry.get("validation", "Sources linked below; workflow not run during this catalog redesign.")
    summary = "\n".join([
        START,
        f"[← Browse use cases](../README.md#{anchor(entry['category'])}) · **{entry['category']}**", "",
        "| At a glance | Details |", "| --- | --- |",
        f"| **Outcome** | {entry['outcome']} |",
        f"| **Requires** | {entry['requires']} |",
        f"| **Available** | {entry['format']} |",
        f"| **Validation** | {validation} |", END,
    ])
    return title + "\n\n" + summary + "\n\n" + body.lstrip("\n").rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated content is out of date; write nothing")
    args = parser.parse_args()
    try:
        data = load_catalog()
        outputs = {ROOT / "README.md": render_readme(data)}
        for entry in data["entries"]:
            path = ROOT / "usecases" / f"{entry['slug']}.md"
            outputs[path] = render_page(entry, path.read_text(encoding="utf-8"))
    except (ValueError, KeyError) as error:
        parser.error(str(error))
    changed = [path for path, content in outputs.items() if path.read_text(encoding="utf-8") != content]
    if args.check and changed:
        for path in changed:
            print(f"Out of date: {path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    if not args.check:
        for path in changed:
            path.write_text(outputs[path], encoding="utf-8")
    print(f"Catalog {'checked' if args.check else 'rendered'}: {len(data['entries'])} use cases, {sum(len(g['categories']) for g in data['groups'])} categories; {len(changed)} files {'out of date' if args.check else 'updated'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
