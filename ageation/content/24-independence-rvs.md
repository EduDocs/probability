---
slug: 24-independence-rvs
title: Independent Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03
source: sources/24-independence-rvs.tex
source_sha256: 720b9deaf084fab02fbf89e2487f4ad3594bbd53458a78dc1975eca3293c6b7b
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/discrete_vectors.tex
companion: sources/24-independence-rvs.md
companion_sha256: 24365e9d6b861b146df44bdc5fd758e3aedc15ae905f595e143aacdc613a4a68
prereqs:
  - 23-conditional-expectation
audience: undergraduate engineering, first probability course
concepts:
  - id: factorization
    name: Independence as factorization
    importance: core
    one_liner: X and Y are independent when p_{X,Y}(x,y) = p_X(x) p_Y(y) at every pair — the joint table is the outer product of its margins.
  - id: events-connection
    name: Back to independent events
    importance: core
    one_liner: X and Y are independent iff the events {X = x} and {Y = y} are independent for every pair — chapter 4's notion, applied cell by cell.
  - id: product-expectation
    name: Expectations of products factor
    importance: core
    one_liner: Independence gives E[XY] = E[X] E[Y], and more generally E[g(X) h(Y)] = E[g(X)] E[h(Y)] — the double sum separates.
  - id: variance-of-sum
    name: The variance of a sum
    importance: highlight       # the payoff computation
    one_liner: Var(X + Y) = Var(X) + Var(Y) + twice a cross term; independence kills the cross term, so variances add — unlike means, which always add.
  - id: independent-of-event
    name: Independence from an event
    importance: optional        # cut first if over budget
    one_liner: X independent of S means p_{X|S} = p_X — conditioning that changes nothing.
  - id: iid
    name: iid — the standing assumption
    importance: core
    one_liner: Independent and identically distributed - repeated draws with no interaction; the modeling default for the sums and limit theorems ahead.
estimated_runtime_sec: 420      # ~7 min (five beats in project.yaml)
---

# Independent Random Variables — Concept Map

This video covers Section 7.5 of book chapter 7. Video 21's
with-replacement table finally gets its name; video 25 puts independence to
work on sums.

## What
Random variables X and Y are **independent** when the joint PMF factors:
`p_{X,Y}(x,y) = p_X(x) p_Y(y)` for every pair — equivalently, when every
pair of events `{X = x}`, `{Y = y}` is independent in chapter 4's sense.
Independence makes expectations of products factor
(`E[XY] = E[X] E[Y]`, and `E[g(X) h(Y)] = E[g(X)] E[h(Y)]`), and its
signature computational payoff: **the variance of a sum of independent
variables is the sum of the variances**. Repeated independent draws from
one distribution — **iid** — become the standing assumption for the rest
of the course.

## Why it matters
Independence is the modeling assumption that makes large systems
computable: joints collapse into products, double sums split, and
fluctuation budgets add. The variance-of-a-sum identity is the quiet engine
behind every averaging argument to come — it is *why* sample means settle
down — and the iid framing is the license to use it at scale.

## Key ideas (in dependency order)
1. **Factorization.** `p_{X,Y}(x,y) = p_X(x) p_Y(y)` everywhere. Video
   21's with-replacement urn is the worked instance: every cell 1/9 =
   (1/3)(1/3) — the table *is* the outer product of its margins. The
   without-replacement table (zeros on the diagonal) visibly is not.
2. **Cell-by-cell events.** Independence of X and Y ⇔ independence of
   `{X = x}` and `{Y = y}` for every pair — the chapter-4 definition,
   organized into a table.
3. **Products factor.** `E[XY] = E[X]E[Y]`: substitute the factorization
   into the double sum and it separates. Two dice: `E[XY] = 3.5 × 3.5 =
   12.25`. Generalizes to `E[g(X) h(Y)] = E[g(X)] E[h(Y)]`.
4. **Variance of a sum.** Expand `Var(X + Y)` around the means:
   `Var(X) + Var(Y) + 2 E[(X - E[X])(Y - E[Y])]`. The cross term is a
   product of independent, zero-mean factors — it dies. Means always add
   (video 21); variances add *when independent*. That asymmetry is the
   lesson.
5. **Independence from an event.** `Pr({X = x} ∩ S) = p_X(x) Pr(S)`, i.e.
   `p_{X|S} = p_X` — conditioning that changes nothing (video 22's slice
   returns unchanged).
6. **iid.** Independent and identically distributed draws — one marginal
   PMF, factored joints at every size. Named here, used relentlessly from
   video 25 onward.

## What else (connections, to seed callbacks in narration)
- Video 21's two urn tables were built for this moment: with replacement
  factors, without does not.
- Chapter 4's independence of events (video 14) supplies the definition;
  this video lifts it to random variables.
- The cross term `E[(X-E[X])(Y-E[Y])]` is covariance in all but name — the
  book names it later; we show it and let it die without naming it.
- Variances adding under independence is the seed of the law of large
  numbers arc (empirical sums, video 25 and beyond).

## Conceptual progression (drives the storyboard)
The two urn tables side by side (one at a time, per house rule) → margins
peeled off the factorable table and outer-produced back into it → products
separating in the double sum → dice product 12.25 → the variance expansion
with the cross term isolated, then dying under independence → the
conditioning slice that changes nothing → iid as n identical PMF cards.

## Visual opportunities
- **Outer product**: the marginal bars along the table's edges sweep
  across/down, tinting each cell as row-value × column-value — the
  factorization *performed*, not stated.
- **The dying cross term**: the variance expansion with the cross term in
  accent, factoring into two centered expectations, each collapsing to
  zero at its fulcrum.
- **Unchanged slice**: video 22's slice-and-renormalize animation replayed
  on a factorable table — the lifted row matches the marginal exactly.
- **iid**: a row of identical small PMF cards (same shape), joints written
  as products beneath.

## Notation (per project.yaml)
- Factorization `p_{X,Y}(x,y) = p_X(x)\, p_Y(y)`; expectations and
  variance via the `\mathrm{E}` / `\mathrm{Var}` helpers.

## Deliberately out of scope
- Covariance and correlation as named objects — later chapter; the cross
  term appears and vanishes, unnamed.
- Sums' distributions (convolution, OGFs) — video 25.
- Independence of many variables beyond the product formula — video 25.

## Cut first (if the script runs over budget)
Independence-from-an-event (idea 5) drops to one caption; the
`E[g(X)h(Y)]` generalization becomes a spoken aside over the `E[XY]` line.
