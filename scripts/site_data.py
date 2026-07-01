#!/usr/bin/env python3
"""Generate ``site/data/graph.json`` for the interactive concept map.

Reuses the frontmatter parsing and dependency-graph logic from
``concept_graph.py`` (same directory) and enriches each chapter node with a
display title and a short summary pulled from the sidecar prose. The result is
a single JSON file the static site loads to draw the graph.

Idempotent and diff-friendly: same inputs produce byte-identical output.

Run:  python3 scripts/site_data.py   (or ``just web-data``)
"""

from __future__ import annotations

import json
import re
import sys

try:
    import yaml
    HAVE_YAML = True
except ImportError:  # video links need PyYAML; everything else degrades cleanly
    HAVE_YAML = False

# concept_graph.py lives beside this file; sys.path[0] is this dir when run as
# ``python3 scripts/site_data.py``, so a plain import resolves it.
import concept_graph as cg

SITE_DATA = cg.PROJECT_ROOT / "site" / "data" / "graph.json"
PDF_NAME = "probability.pdf"

# A single ``# `` heading line (not ``## ``).
HEADING_RE = re.compile(r"^#\s+(.*?)\s*$", re.MULTILINE)
# Separator between the title and a trailing tag like "— scratch".
TITLE_TAIL_RE = re.compile(r"\s+[–—-]\s+")
PURPOSE_RE = re.compile(r"^##\s+Purpose\b", re.IGNORECASE)


def strip_frontmatter(text: str) -> str:
    """Return the document body with the leading YAML frontmatter removed."""
    m = cg.FRONTMATTER_RE.match(text)
    return text[m.end():] if m else text


def display_title(body: str, stem: str) -> str:
    """Chapter title from the first ``# `` heading, minus any trailing tag."""
    m = HEADING_RE.search(body)
    if m:
        title = TITLE_TAIL_RE.split(m.group(1))[0].strip()
        if title:
            return title
    return stem.replace("_", " ").title()


def extract_summary(body: str) -> str:
    """One-paragraph summary: prefer the ``## Purpose`` section, else the first
    ordinary paragraph (skipping headings and blockquotes)."""
    lines = body.splitlines()

    for i, ln in enumerate(lines):
        if PURPOSE_RE.match(ln.strip()):
            para: list[str] = []
            for ln2 in lines[i + 1:]:
                s = ln2.strip()
                if s.startswith("#"):
                    break
                if not s:
                    if para:
                        break
                    continue
                para.append(s)
            if para:
                return " ".join(para)

    para = []
    for ln in lines:
        s = ln.strip()
        if not s:
            if para:
                break
            continue
        if s.startswith("#") or s.startswith(">"):
            if para:
                break
            continue
        para.append(s)
    return " ".join(para)


def prettify(slug: str) -> str:
    """Turn a concept slug like ``sample-space`` into ``sample space``."""
    return slug.replace("-", " ")


def extract_videos(text: str) -> list[dict]:
    """Pertinent videos for a chapter, from the sidecar's ``videos:`` frontmatter.

    Each entry is ``{title, url}``. Needs PyYAML (the nested list is beyond the
    flat fallback parser); returns [] when PyYAML is unavailable, so the rest of
    the site still builds.
    """
    if not HAVE_YAML:
        return []
    body = cg.extract_frontmatter(text)
    if not body:
        return []
    data = yaml.safe_load(body) or {}
    out: list[dict] = []
    for item in data.get("videos") or []:
        if isinstance(item, dict) and item.get("title") and item.get("url"):
            out.append({"title": str(item["title"]), "url": str(item["url"])})
    return out


def main() -> int:
    if not HAVE_YAML:
        print(
            "warning: PyYAML not installed; video links skipped (pip install pyyaml)",
            file=sys.stderr,
        )
    reading_order = cg.read_chapter_order(cg.MAIN_TEX)
    chapters = cg.load_chapters()
    edges, _fwd, _und, _aliases = cg.build_graph(chapters, reading_order)

    # Nodes: reading-order chapters that actually carry concept metadata. This
    # drops the preface (no concepts) and any parked/appendix material.
    node_stems = [
        s for s in reading_order
        if s in chapters and (chapters[s]["introduces"] or chapters[s]["requires"])
    ]
    node_set = set(node_stems)

    nodes = []
    for i, stem in enumerate(node_stems):
        text = (cg.CHAPTERS_DIR / f"{stem}.md").read_text(encoding="utf-8")
        body = strip_frontmatter(text)
        nodes.append({
            "id": stem,
            "title": display_title(body, stem),
            "order": i + 1,
            "introduces": chapters[stem]["introduces"],
            "requires": chapters[stem]["requires"],
            "summary": extract_summary(body),
            "videos": extract_videos(text),
            "pdf": PDF_NAME,
        })

    edge_list = [
        {"source": s, "target": t}
        for (s, t) in sorted(edges)
        if s in node_set and t in node_set
    ]

    data = {
        "reading_order": node_stems,
        "nodes": nodes,
        "edges": edge_list,
    }

    SITE_DATA.parent.mkdir(parents=True, exist_ok=True)
    SITE_DATA.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"wrote {SITE_DATA.relative_to(cg.PROJECT_ROOT)}  "
        f"nodes: {len(nodes)}  edges: {len(edge_list)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
