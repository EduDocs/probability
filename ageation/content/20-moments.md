---
slug: 20-moments
title: Moments
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03 ("Proceed")
source: sources/20-moments.tex
source_sha256: 7d9dd7a05900c28f44df3fc44020688a88d369c496d80b458771ff4f674a8d25
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_expectations.tex
companion: sources/20-moments.md
companion_sha256: b99ba1690b46f38674b6e913054edefe24cd3d73c2dae1d2e1702b69fed80027
prereqs:
  - 19-functions-and-expectations
audience: undergraduate engineering, first probability course
concepts:
  - id: moments-def
    name: The nth moment
    importance: core
    one_liner: E[X^n] = sum over x of x^n p_X(x) — a ladder of summary quantities; the mean is the first moment.
  - id: variance-from-moments
    name: Variance from the first two moments
    importance: core
    one_liner: Var[X] = E[X^2] - (E[X])^2 — expand the square, use linearity, and the cross term collapses; usually the easiest way to compute a variance.
  - id: uniform-example
    name: Worked example — the uniform PMF
    importance: core
    one_liner: For X uniform on {1,...,n}, E[X] = (n+1)/2 and the moment formula gives Var[X] = (n^2 - 1)/12 via the standard sum of squares.
  - id: central-moments
    name: Central moments, skewness, kurtosis
    importance: highlight
    one_liner: E[(X - E[X])^k] centers before powering; variance is the second central moment, skewness measures asymmetry, kurtosis weighs tails — each reveals a different trait.
estimated_runtime_sec: 480      # ~8 min (five beats in project.yaml)
---

# Moments — Concept Map

This video covers Section 6.3, closing book chapter 6. Video 18 defined
E[X]; video 19 built E[g(X)], the variance, and the affine rules — all of
which this video reuses.

## What
The **moments** of X are the expectations of its powers:
`E[X^n] = sum_{x in X(Omega)} x^n p_X(x)` — the mean is the first moment.
The chapter's payoff identity, `Var[X] = E[X^2] - (E[X])^2`, expresses the
variance through the first two moments and is usually the most convenient
way to compute it. Centering before powering gives the **central moments**
`E[(X - E[X])^k]`, of which the variance is the k = 2 case; the third and
fourth standardized versions are the skewness and kurtosis.

## Why it matters
Each moment adds one more brushstroke to the portrait of a distribution:
the first locates it, the second (about the mean) spreads it, the third
tilts it, the fourth weighs its tails. Practically, the two-moment variance
formula turns a messy centered sum into two standard sums — the uniform
example collapses to a textbook sum of squares — and this trick is used
constantly in the chapters ahead.

## Key ideas (in dependency order)
1. **The ladder of moments.** `E[X^n] = sum_x x^n p_X(x)` — nothing new,
   just `g(x) = x^n` in video 19's formula. Mean = first moment.
2. **The identity.** Expand `(x - E[X])^2 = x^2 - 2x E[X] + (E[X])^2` inside
   the variance sum; linearity (video 19's affine algebra) collapses it to
   `Var[X] = E[X^2] - (E[X])^2`.
3. **Put it to work.** X uniform on `{1, ..., n}`: `E[X] = (n+1)/2`;
   `E[X^2] = sum k^2/n = (n+1)(2n+1)/6`; subtract the squared mean and
   simplify to `Var[X] = (n^2 - 1)/12`. The centered sum would have been
   much uglier — that is the point of the identity.
4. **Central moments.** `E[(X - E[X])^k]`: center first, then power.
   Variance is the second central moment. Skewness (k = 3, standardized)
   measures asymmetry; kurtosis (k = 4) distinguishes rare-extreme
   deviations from frequent modest ones. Named, pictured, not computed —
   they belong to statistics, but the viewer should recognize them.

## What else (connections, to seed callbacks in narration)
- `g(x) = x^n` is the cleanest possible callback to video 19's E[g(X)].
- The uniform PMF is from video 16.6 (discrete uniform RV) — reuse its look.
- Poisson had mean = variance = lambda (video 19); the two-moment formula
  gives its second moment lambda^2 + lambda for free — a one-line callback.
- Bridge forward: with single-variable summaries complete, the series turns
  to several random variables at once (book chapter 7).

## Conceptual progression (drives the storyboard)
Mean = first moment → the whole ladder E[X^n] → variance rewritten in two
moments (the algebra, three short lines) → the uniform worked example where
the formula visibly saves labor → centering: the PMF slides so its balance
point is at zero, then k-th powers → skewness/kurtosis as portraits
(asymmetric PMF vs heavy-tailed PMF).

## Visual opportunities
- **The ladder**: one PMF, a column of stacked chips `E[X], E[X^2], E[X^3]`
  filling in — each moment one more number extracted from the same bars.
- **Three-line algebra**: the expansion of `(x - E[X])^2` with the cross
  term visibly canceling into `E[X^2] - (E[X])^2` (TransformMatchingTex
  territory; one ACCENT on the surviving terms).
- **Uniform example**: the flat PMF on {1,...,n}; the two sums appear as
  overlays; the result `(n^2 - 1)/12` checked at n = 6 against the fair die.
- **Centering**: the PMF translating left by E[X] (video 19's affine slide,
  replayed), then squares/cubes/fourth powers weighting the bars.
- **Portraits**: a skewed PMF vs a symmetric one (skewness), a spiky-with-
  tails PMF vs a shoulder-heavy one (kurtosis) — side-by-side stills, one
  caption each.

## Notation (per project.yaml)
- `\mathrm{E}[X^n]`, `\mathrm{Var}(X)` via the _style helpers.
- Sums `\sum_{x \in X(\Omega)}`; the sum of squares
  `\sum_{k=1}^{n} k^2 = n(n+1)(2n+1)/6`.

## Deliberately out of scope
- Ordinary generating functions — the book's OGF section is disabled
  (\iffalse) and stays out of the video series.
- Numeric skewness/kurtosis formulas and computations — named and pictured
  only.
- Moments of sums of independent RVs — later chapters.

## Cut first (if the script runs over budget)
The skewness/kurtosis portraits compress to a single two-still beat; the
n = 6 die check drops to a spoken aside.
