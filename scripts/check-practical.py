#!/usr/bin/env python3
"""Check the practical guides' structure, local links, and Bash syntax offline."""

from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def heading_ids(text):
    seen = {}
    ids = set()
    for title in re.findall(r"^#{1,6} (.+)$", text, re.M):
        base = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = seen.get(base, 0)
        seen[base] = count + 1
        ids.add(base + (f"-{count}" if count else ""))
    return ids


def main():
    recipes = sorted((ROOT / "recipes").glob("[0-9][0-9]-*.md"))
    if len(recipes) != 10:
        raise ValueError("Expected exactly ten indexed recipes")
    index = (ROOT / "recipes/README.md").read_text(encoding="utf-8")
    for recipe in recipes:
        if index.count(f"]({recipe.name})") != 1:
            raise ValueError(f"Recipe missing or duplicated in index: {recipe.name}")
        text = recipe.read_text(encoding="utf-8")
        for heading in ("Goal", "Requires", "Steps", "Expected result", "Failure check", "Sources"):
            if f"\n## {heading}\n" not in text:
                raise ValueError(f"Missing {heading}: {recipe.name}")
    pages = recipes + [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "recipes/README.md",
                        ROOT / "demos/README.md", ROOT / "docs/tested-results.md"]
    pages += [ROOT / "demos" / name / "README.md" for name in ("daily-briefing", "team-telegram", "openwebui")]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^\s)]+)\)", text):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            destination = (page.parent / unquote(url.path)).resolve() if url.path else page
            if not destination.exists():
                raise ValueError(f"Missing local link in {page.relative_to(ROOT)}: {target}")
            if url.fragment and destination.is_file() and destination.suffix == ".md":
                if url.fragment not in heading_ids(destination.read_text(encoding="utf-8")):
                    raise ValueError(f"Missing anchor in {page.relative_to(ROOT)}: {target}")
    scripts = sorted((ROOT / "demos").glob("*/*.sh"))
    for script in scripts:
        subprocess.run(["bash", "-n", str(script)], check=True)
    print(f"PASS: {len(recipes)} indexed recipes, {len(pages)} linked pages, and {len(scripts)} Bash entry points.")


if __name__ == "__main__":
    main()
