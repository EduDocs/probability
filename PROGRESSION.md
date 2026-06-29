# Chapter Progression: from sidecar scratch to shipped prose

> Not a project status log or a roadmap. This document defines how each chapter
> is authored across its lifecycle, using a paired `.tex` / `.md` "sidecar," and how
> concepts move between the two. The folder/file layout lives in `../CLAUDE.md`.

This book separates **thinking** from **authoring** by pairing every LaTeX chapter file
with a same-named Markdown *sidecar*, and it treats a chapter as something that **progresses**
through stages rather than something written once.

## The pairing

For each chapter in `chapters/`, there are two files:

| File         | Register / layer | Role                                                              |
| ------------ | ---------------- | ---------------------------------------------------------------- |
| `<name>.tex` | Authoring        | The polished prose that actually ships in the compiled PDF.      |
| `<name>.md`  | Thinking         | The design log: scratch, ideas, the conceptual spine, decisions. |

Example: `chapters/probability_models.tex` (shipped) ↔ `chapters/probability_models.md` (sidecar).

The sidecar is **never** `\include`d by `UndergraduateProbabilityI.tex`, so it is invisible to
the LaTeX build and can never leak into the PDF. Both files are tracked in git.

## The progression (and the source-of-truth flip)

A chapter does not have one fixed "source of truth." Which file *leads* changes as the work
matures — this is the central fact the tooling is built around.

```
   early                                                          late
   |  think in the .md  ──►  harmonize concepts  ──►  author into the .tex  ──► push in the .tex
   |  (scratch, ideas)       (the conceptual spine)    (/md2tex realizes)        (/tex2md feeds back)
   |
   |  .md LEADS ───────────────────────────────────────────────► .tex LEADS
```

1. **Think in the `.md` first.** Rough out purpose, key points, structure, open questions,
   and source notes before writing a single LaTeX sentence. Early on, the sidecar is ahead.
2. **Harmonize the concepts.** The sidecar settles into a coherent conceptual spine — the
   claims and the order of argument the chapter will make.
3. **Realize into the `.tex` (`/md2tex`).** Translate the *settled* concepts into polished,
   house-style prose. The sidecar's scratch and open questions stay behind.
4. **Push happens in the `.tex` (`/tex2md`).** Later, the argument is sharpened directly in the
   prose. When that changes a *concept* (not just wording), feed it back so the sidecar's spine
   and decision log stay honest.

For the probability book, the existing chapters were authored long before the sidecars existed,
so most of them start the lifecycle in the **late** stage: `.tex` already leads, and the
sidecars were bootstrapped from the prose via the `tex2md` bootstrap path. New chapters added
later should follow the normal early-to-late progression.

The lead flips from `.md` to `.tex` over the lifecycle. Neither skill assumes a fixed
direction; each is invoked deliberately for the move you intend, and warns (via a git-aware age
check) when the file you're propagating *from* looks older than the one you're propagating
*to* — a hint that you may want the other direction.

## What lives where (exclusive zones + the shared spine)

The two files overlap only on the **conceptual spine**. Each also holds material the other must
never contain — protecting these zones is the first rule of every sync.

- **`.md`-only (never copy into the `.tex`):** scratch and half-formed ideas, rejected
  alternatives, open questions, design rationale ("the decision, taken with the author"),
  implementation/source detail, author-preference notes, and pointers/anchors back into the
  prose.
- **`.tex`-only (never overwrite from the `.md`):** the exact published wording and voice,
  citations, and the actual figure/table/math LaTeX.
- **Shared spine (the only thing that syncs):** the concepts, claims, framing, and order of
  argument.

So the two sync directions are **asymmetric — not inverses**:

- **`/md2tex` realizes** (expands): settled spine → polished prose. It *ignores* the `.md`'s
  exclusive zones and writes in the `.tex` house style (one sentence per line, `~` ties,
  restrained `---`; see the `format-tex` skill).
- **`/tex2md` distills** (compresses): an advanced argument → updated spine + decision-log
  entries (close an open question, record "changed because…"). It *never* pastes prose verbatim
  and keeps the sidecar's markdown voice (see the `format-md` skill).

## Discipline (both directions)

- **Surgical and additive.** Propose targeted edits to the follower's shared-spine content;
  never wholesale-replace, never touch its exclusive zones.
- **Ask first.** Concept propagation is interpretive and lossy. Show the proposed change and
  confirm before writing. One direction per invocation; no round-trip ping-pong.
- **Preserve each register.** `.tex` stays submission-ready prose; `.md` stays a readable
  design log.

## Sidecar skeleton

Each sidecar follows a light, consistent structure so it stays useful rather than becoming a
dumping ground:

```markdown
# <Chapter> — scratch

> Scratch/ideas only. The shipped prose lives in `<name>.tex`. Not part of the LaTeX build.

## Purpose
What this chapter must accomplish for the reader.

## Key points / outline
-

## Open questions
-

## Notes & references
-
```

As the chapter matures, the body grows toward a high-level conceptual explanation (the spine),
with a `## Decisions` or "resolved" trail recording why it reads the way it does.

## Tooling

- **`/md2tex`** — realize settled sidecar concepts into the shipped `.tex` prose (horizontal,
  within one chapter).
- **`/tex2md`** — feed concept changes made in the `.tex` back into the sidecar (horizontal).
- **`/progression`** — audit the conceptual coherence of the sidecars *across* chapters
  (vertical): setup↔payoff, ordering, consistency, and branch coherence. Uses the optional
  progression map below.
- **`/format-tex`**, **`/format-md`** — keep each register's source tidy and diff-friendly.

## Progression map (optional)

By default the chapter order is the `\include{chapters/<name>}` sequence in
`UndergraduateProbabilityI.tex`, and the progression is read as a **linear chain**. When the
document **branches** — parallel case studies, an appendix that depends on a specific result,
two studies that share a model but not each other — declare the conceptual dependency structure
here as a `parent -> child` edge list. `/progression` reads it to build the dependency
tree/DAG; omit it for a linear book.

The default linear chain (no map needed) for this book is:

```
preface ->
sets_and_functions -> combinatorics -> probability_models -> conditional_probability ->
discrete_random_variables -> discrete_expectations -> discrete_vectors ->
continuous_random_variables -> derived_distributions -> expectations_and_bounds ->
random_vectors -> empirical_sums
```

The appendix (`chapters/appendix.tex`) is currently parked — its `\include` line is commented
out in the main file, so the audit treats it as out of scope.

Match the node names to the chapter file stems (`<name>.tex` / `<name>.md`). Keep the map in
sync with `UndergraduateProbabilityI.tex`; `/progression` flags a chapter whose `.tex` is not
`\include`d as parked.

## Git

Sidecars are **tracked** — they are valuable design history, not disposable scratch.
(Throwaway experiments still belong in a `scratch/` or `misc/` folder.)
