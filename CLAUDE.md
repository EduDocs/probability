# Probability

Undergraduate probability book (Probability). Currently in a
classical LaTeX layout, being slowly transformed into an agentic-ready folder.
Part of the larger `EduDocs` collection; lessons learned here feed into a
generalized `template-book/`.

## Bash style

- Avoid compound commands (pipes, `&&`, `||`, `;`, `$()`, backticks, `if`/`for`/`while` shells).
- Break multi-step work into separate sequential tool calls instead.
- If a pipe is truly necessary, note it explicitly so the user can approve.

## Layout

- `chapters/*.tex` — source chapters, included from `probability.tex`.
- `chapters/*.md` — Markdown sidecars mirroring the chapters.
- `scripts/concept_graph.py` — generates `CONCEPT_MAP.md`.
- `output/` — build artifacts (gitignored; regenerated, never committed).

## Build (via `just`)

- `just build latex` → `output/probability.pdf`
- `just build md` → `output/probability_sidecars.pdf` (pandoc)
- `just view latex` / `just view md` — build then open the PDF
- `just concept md` — regenerate `CONCEPT_MAP.md`
- `just clean` — remove `output/`

Chapter order is defined by the `\include` sequence in the main `.tex` and
mirrored in the `md_files` list in the `justfile`.

## Environment

- System tools: `brew bundle` (see `Brewfile`) installs `just`, `uv`, `pandoc`,
  `gh`, and a TeX distribution.
- Python tooling: `uv sync` creates `.venv` and installs deps from
  `pyproject.toml` (currently just PyYAML, used by the site/concept generators).
  The generator `just` recipes call `uv run`; the CI Pages build installs PyYAML
  with pip instead.

## Working approach

Each concrete change here is an opportunity to generalize a reusable pattern for
the agentic book template. Don't build speculative structure — let it follow
real needs.
