---
slug: 21-joint-pmfs
title: Joint PMFs and Expectations
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03
source: sources/21-joint-pmfs.tex
source_sha256: 720b9deaf084fab02fbf89e2487f4ad3594bbd53458a78dc1975eca3293c6b7b
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_vectors.tex
companion: sources/21-joint-pmfs.md
companion_sha256: 24365e9d6b861b146df44bdc5fd758e3aedc15ae905f595e143aacdc613a4a68
prereqs:
  - 20-moments
audience: undergraduate engineering, first probability course
concepts:
  - id: joint-pmf
    name: The joint PMF
    importance: core
    one_liner: p_{X,Y}(x, y) = Pr(X = x, Y = y) — one function characterizing the random pair (X, Y), which maps every outcome to a point in the plane.
  - id: set-probability
    name: Probabilities of sets of pairs
    importance: core
    one_liner: Pr(S) = sum of p_{X,Y}(x, y) over the pairs in S; summing over everything gives 1, exactly as in one dimension.
  - id: marginals
    name: Marginal PMFs by summing out
    importance: core
    one_liner: p_X(x) = sum over y of p_{X,Y}(x, y) — fix a row of the joint table and add across it; likewise for columns.
  - id: marginals-not-enough
    name: Marginals do not determine the joint
    importance: highlight
    one_liner: Drawing two balls with vs without replacement gives identical marginals but different joint tables — the joint carries strictly more information.
  - id: function-of-pair
    name: Functions of a random pair
    importance: core
    one_liner: V = g(X, Y) is a random variable; its PMF sums the joint over level sets — the two-dice sum U = X + Y is the canonical example.
  - id: linearity
    name: E[g(X,Y)] and linearity of expectation
    importance: core
    one_liner: E[g(X,Y)] is a double sum against the joint PMF, and E[X + Y] = E[X] + E[Y] falls out with no independence assumption.
estimated_runtime_sec: 480      # ~8 min (five beats in project.yaml)
---

# Joint PMFs and Expectations — Concept Map

This video opens book chapter 7 ("Multiple Discrete Random Variables"),
covering Sections 7.1 and 7.2. Videos 22–25 cover conditioning, conditional
expectation, independence, and sums.

## What
When two random variables ride the same experiment, one function describes
the pair completely: the **joint PMF**
`p_{X,Y}(x, y) = Pr(X = x, Y = y)`. Its **marginals** are recovered by
summing out the other variable, set probabilities are sums over pairs, and
expectations of functions of the pair are double sums — with **linearity of
expectation** (`E[X + Y] = E[X] + E[Y]`, no independence needed) as the
first structural payoff.

## Why it matters
Everything so far watched one random variable at a time; real models track
several at once — a source and its noise, a header and its payload. The
joint PMF is the two-dimensional generalization of the single-variable PMF,
and it sets up every idea in the rest of the chapter: conditioning slices
this table, independence factors it, and sums convolve it. The
marginals-are-not-enough example is the crucial early warning: you cannot
reconstruct dependence from per-variable summaries.

## Key ideas (in dependency order)
1. **The pair as a map.** `(X, Y)` sends each outcome to a point in the
   plane (the book's Ω-to-R² figure). The joint PMF weights those points.
2. **Same axioms, one dimension up.** `Pr(S)` for a set of pairs is the sum
   of the joint over S; the grand total over all pairs is one.
3. **Marginals by summing out.** Fix x, sum across y — a row sum of the
   joint table. Urn, two draws *without* replacement: the 3×3 table has
   zeros on the diagonal, sixths elsewhere; every row and column sums to
   one third, so both marginals are uniform.
4. **Marginals are not enough.** Redo the urn *with* replacement: every
   cell becomes one ninth. Same uniform marginals — different joint. The
   dependence lives strictly in the table.
5. **Functions of the pair.** `V = g(X, Y)` is again a random variable;
   `p_V(v)` sums the joint over the level set `g(x, y) = v`. The two-dice
   sum U = X + Y: the level sets are the anti-diagonals of the 6×6 table,
   giving the triangular PMF from 2 to 12.
6. **Expectations and linearity.** `E[g(X,Y)] = double sum of
   g(x,y) p_{X,Y}(x,y)`. Split g(x,y) = x + y and the double sum falls
   apart into the two marginal means: `E[X + Y] = E[X] + E[Y]` — proved
   from the table alone. Urn example: 2 + 2 = 4.

## What else (connections, to seed callbacks in narration)
- The urn with three balls is the running example of videos 15 and 19 —
  same glyphs, now upgraded to two draws.
- The dice pair reprises video 24's... (careful: dice appeared in videos 18
  and 19) — the two-dice sum table also foreshadows convolution
  anti-diagonals in video 25.
- Linearity of expectation extends video 19's single-variable linearity;
  the "no independence needed" refrain pays off in video 24 when variance,
  unlike the mean, does pick up a cross term.

## Conceptual progression (drives the storyboard)
Ω-box with a pair of arrows to the plane → the joint table as the object →
row/column sums produce marginals at the table's edges → two tables, same
margins, different insides → the dice table with anti-diagonals lighting up
by sum → the double-sum expectation splitting into two marginal sums.

## Visual opportunities
- **The joint table** as the chapter's home visual: a 3×3 grid of cells
  with masses, marginals appearing in a summary row/column at the edges
  (row sums sweep right, column sums sweep down).
- **Side-by-side tables** for with/without replacement with identical
  margins highlighted, then the differing interiors flashed.
- **The 6×6 dice table** with anti-diagonals `x + y = k` lighting up one k
  at a time, building the triangular PMF of the sum beneath it.
- **Linearity**: the double sum splitting visually — x-terms streaming to
  a row-sum column, y-terms to a column-sum row.

## Notation (per project.yaml)
- Joint PMF `p_{X,Y}(x, y)`; `\Pr(X = x, Y = y)` via the `pr()` helper.
- Expectation `\mathrm{E}[\cdot]` via the helper; double sums
  `\sum_{x \in X(\Omega)} \sum_{y \in Y(\Omega)}`.

## Deliberately out of scope
- Conditional PMFs (video 22) and independence (video 24) — this video
  never divides or factors the table, only sums it.
- Convolution and generating functions (video 25) — the dice diagonals are
  shown, not named as convolution.
- More than two variables (video 25).

## Cut first (if the script runs over budget)
The set-probability formula (idea 2) compresses to one spoken sentence over
the table; the with-replacement table can appear without its own build.
