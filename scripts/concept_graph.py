#!/usr/bin/env python3
"""Build a concept dependency graph from chapter sidecar frontmatter.

Walks ``chapters/*.md``, parses each file's YAML frontmatter
(``introduces:`` / ``requires:`` lists), reads the canonical reading order
from the main ``.tex`` file's ``\\include{chapters/<name>}`` lines, and
writes ``CONCEPT_MAP.md`` at the project root with the reading order, a
Mermaid dependency graph, and audit sections for forward references,
undefined concepts, and aliasing.

Idempotent and diff-friendly: same inputs produce byte-identical output.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CHAPTERS_DIR = PROJECT_ROOT / "chapters"
MAIN_TEX = PROJECT_ROOT / "UndergraduateProbabilityI.tex"
OUTPUT_MD = PROJECT_ROOT / "CONCEPT_MAP.md"


# --------------------------------------------------------------------------
# Frontmatter parsing
# --------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> str | None:
    """Return the raw YAML body between the opening ``---`` markers, or None."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return m.group(1)


def _parse_flow_list(s: str) -> list[str]:
    """Parse a possibly multi-line flow-style list of bare strings.

    Accepts forms like ``[a, b, c]``, ``[]``, or a flow list whose ``[`` and
    ``]`` are on separate lines with one item per line. Items are stripped
    of surrounding whitespace and optional quotes.
    """
    s = s.strip()
    if not (s.startswith("[") and s.endswith("]")):
        raise ValueError(f"expected flow-style list, got: {s!r}")
    inner = s[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    for raw in inner.split(","):
        item = raw.strip().strip("'\"")
        if item:
            items.append(item)
    return items


def _fallback_parse_frontmatter(body: str) -> dict[str, list[str]]:
    """Minimal YAML-frontmatter parser for ``introduces:`` / ``requires:``.

    Supports single-line flow lists (``key: [a, b]``) and multi-line flow
    lists (``key: [`` ... ``]`` spanning multiple lines). Block-style
    (``-`` per line) lists are also tolerated.
    """
    result: dict[str, list[str]] = {}
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest.startswith("["):
            # Possibly multi-line flow list: accumulate until matching ']'.
            buf = rest
            while "]" not in buf:
                i += 1
                if i >= len(lines):
                    raise ValueError(f"unterminated flow list for key {key!r}")
                buf += " " + lines[i].strip()
            # Truncate at the first ']' to ignore any trailing junk.
            buf = buf[: buf.index("]") + 1]
            result[key] = _parse_flow_list(buf)
            i += 1
            continue
        if rest == "":
            # Possibly a block-style list following the key.
            items: list[str] = []
            j = i + 1
            while j < len(lines):
                ln = lines[j]
                lstripped = ln.lstrip()
                if not lstripped or lstripped.startswith("#"):
                    j += 1
                    continue
                if lstripped.startswith("- "):
                    items.append(lstripped[2:].strip().strip("'\""))
                    j += 1
                    continue
                break
            result[key] = items
            i = j
            continue
        # Scalar value — not relevant here, but record as a singleton string.
        result[key] = [rest.strip("'\"")]
        i += 1
    return result


def parse_frontmatter(text: str) -> dict[str, list[str]]:
    """Return ``{key: [strings]}`` from the YAML frontmatter of ``text``."""
    body = extract_frontmatter(text)
    if body is None:
        return {}
    if HAVE_YAML:
        data = yaml.safe_load(body) or {}
        out: dict[str, list[str]] = {}
        for k, v in data.items():
            if isinstance(v, list):
                out[k] = [str(x) for x in v]
            elif v is None:
                out[k] = []
            else:
                out[k] = [str(v)]
        return out
    return _fallback_parse_frontmatter(body)


# --------------------------------------------------------------------------
# Reading order
# --------------------------------------------------------------------------

INCLUDE_RE = re.compile(r"^\s*\\include\{chapters/([A-Za-z0-9_\-]+)\}")


def read_chapter_order(tex_path: Path) -> list[str]:
    """Return the ordered list of chapter stems from non-commented ``\\include`` lines."""
    order: list[str] = []
    for raw in tex_path.read_text(encoding="utf-8").splitlines():
        # Skip any line whose first non-whitespace character is ``%``.
        if raw.lstrip().startswith("%"):
            continue
        m = INCLUDE_RE.match(raw)
        if m:
            order.append(m.group(1))
    return order


# --------------------------------------------------------------------------
# Graph construction
# --------------------------------------------------------------------------

def load_chapters() -> dict[str, dict[str, list[str]]]:
    """Return ``{chapter_stem: {introduces: [...], requires: [...]}}``."""
    chapters: dict[str, dict[str, list[str]]] = {}
    for md in sorted(CHAPTERS_DIR.glob("*.md")):
        stem = md.stem
        fm = parse_frontmatter(md.read_text(encoding="utf-8"))
        chapters[stem] = {
            "introduces": fm.get("introduces", []),
            "requires": fm.get("requires", []),
        }
    return chapters


def build_graph(
    chapters: dict[str, dict[str, list[str]]],
    reading_order: list[str],
) -> tuple[set[tuple[str, str]], list[tuple[str, str, str]], dict[str, list[str]], dict[str, list[str]]]:
    """Return (edges, forward_refs, undefined, aliases).

    edges: set of (introducer, requirer) directed edges.
    forward_refs: list of (requirer, concept, introducer) triples where
        introducer comes after requirer in ``reading_order``.
    undefined: ``{concept: [chapters that require it]}``.
    aliases: ``{concept: [chapters introducing it]}`` for concepts with >1 introducer.
    """
    # Map: concept -> list of chapters that claim to introduce it.
    introducers: dict[str, list[str]] = {}
    for stem, fm in chapters.items():
        for c in fm["introduces"]:
            introducers.setdefault(c, []).append(stem)

    aliases = {c: sorted(ch) for c, ch in introducers.items() if len(ch) > 1}

    # Position lookup for the forward-reference check.
    pos = {stem: i for i, stem in enumerate(reading_order)}

    edges: set[tuple[str, str]] = set()
    forward_refs: list[tuple[str, str, str]] = []
    undefined: dict[str, list[str]] = {}

    for stem, fm in chapters.items():
        for c in fm["requires"]:
            chs = introducers.get(c)
            if not chs:
                undefined.setdefault(c, []).append(stem)
                continue
            # Pick a deterministic primary introducer. If aliased, prefer the
            # earliest in reading order (falling back to alphabetical).
            primary = sorted(
                chs,
                key=lambda x: (pos.get(x, len(reading_order)), x),
            )[0]
            edges.add((primary, stem))
            if stem in pos and primary in pos and pos[primary] > pos[stem]:
                forward_refs.append((stem, c, primary))

    # Sort the chapter lists in ``undefined`` for stable output.
    undefined = {c: sorted(set(chs)) for c, chs in undefined.items()}

    return edges, forward_refs, undefined, aliases


# --------------------------------------------------------------------------
# Markdown rendering
# --------------------------------------------------------------------------

NOTICE = (
    "*Auto-generated by `just concept md`. "
    "Do not edit by hand — edit the `introduces:` / `requires:` "
    "frontmatter in the chapter sidecars and re-run.*"
)


def render_markdown(
    chapters: dict[str, dict[str, list[str]]],
    reading_order: list[str],
    edges: set[tuple[str, str]],
    forward_refs: list[tuple[str, str, str]],
    undefined: dict[str, list[str]],
    aliases: dict[str, list[str]],
) -> str:
    lines: list[str] = []
    lines.append("# Concept Map")
    lines.append("")
    lines.append(NOTICE)
    lines.append("")

    # Reading order.
    lines.append("## Reading order")
    lines.append("")
    included = set(reading_order)
    for i, stem in enumerate(reading_order, start=1):
        lines.append(f"{i}. `{stem}`")
    parked = sorted(s for s in chapters if s not in included)
    if parked:
        next_i = len(reading_order) + 1
        for stem in parked:
            lines.append(f"{next_i}. `{stem}` (parked)")
            next_i += 1
    lines.append("")

    # Dependency graph.
    lines.append("## Dependency graph")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    for src, dst in sorted(edges):
        lines.append(f"    {src} --> {dst}")
    lines.append("```")
    lines.append("")

    # Forward references.
    lines.append("## Forward references")
    lines.append("")
    if not forward_refs:
        lines.append("None.")
    else:
        # Sort alphabetical by requirer, then concept, then introducer.
        for requirer, concept, introducer in sorted(forward_refs):
            lines.append(
                f"- `{requirer}` requires `{concept}`, introduced later in `{introducer}`"
            )
    lines.append("")

    # Undefined concepts.
    lines.append("## Undefined concepts")
    lines.append("")
    if not undefined:
        lines.append("None.")
    else:
        for concept in sorted(undefined):
            chs = ", ".join(f"`{c}`" for c in undefined[concept])
            lines.append(f"- `{concept}` required by {chs}")
    lines.append("")

    # Aliasing / redundancy.
    lines.append("## Aliasing / redundancy")
    lines.append("")
    if not aliases:
        lines.append("None.")
    else:
        for concept in sorted(aliases):
            chs = ", ".join(f"`{c}`" for c in aliases[concept])
            lines.append(f"- `{concept}` introduced by {chs}")
    lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> int:
    if not MAIN_TEX.is_file():
        print(f"error: main tex not found: {MAIN_TEX}", file=sys.stderr)
        return 1
    if not CHAPTERS_DIR.is_dir():
        print(f"error: chapters dir not found: {CHAPTERS_DIR}", file=sys.stderr)
        return 1

    reading_order = read_chapter_order(MAIN_TEX)
    chapters = load_chapters()
    edges, forward_refs, undefined, aliases = build_graph(chapters, reading_order)
    md = render_markdown(chapters, reading_order, edges, forward_refs, undefined, aliases)

    OUTPUT_MD.write_text(md, encoding="utf-8")
    print(f"wrote {OUTPUT_MD.relative_to(PROJECT_ROOT)}")
    print(
        f"  chapters: {len(chapters)}  edges: {len(edges)}  "
        f"forward-refs: {len(forward_refs)}  undefined: {len(undefined)}  "
        f"aliases: {len(aliases)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
