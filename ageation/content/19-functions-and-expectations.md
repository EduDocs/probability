---
slug: 19-functions-and-expectations
title: Functions and Expectations
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03 ("Proceed")
source: sources/19-functions-and-expectations.tex
source_sha256: 7d9dd7a05900c28f44df3fc44020688a88d369c496d80b458771ff4f674a8d25
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_expectations.tex
companion: sources/19-functions-and-expectations.md
companion_sha256: b99ba1690b46f38674b6e913054edefe24cd3d73c2dae1d2e1702b69fed80027
prereqs:
  - 18-expected-values
audience: undergraduate engineering, first probability course
concepts:
  - id: expectation-of-g
    name: The expectation of g(X)
    importance: core
    one_liner: E[g(X)] = sum over x of g(x) p_X(x) — computed directly from the PMF of X, no derived distribution needed; the mean is the special case g(X) = X.
  - id: two-routes-agree
    name: Two routes, one answer
    importance: core
    one_liner: Deriving the PMF of Y = g(X) and averaging y p_Y(y) gives the same value as summing g(x) p_X(x); grouping x's by their image y proves it.
  - id: constant-and-indicator
    name: Constants and indicators
    importance: highlight
    one_liner: E[c] = c by normalization, and E[1_S(X)] = Pr(X in S) — expectation subsumes probability itself.
  - id: extreme-trio
    name: Worked example — the Extreme Trio contest
    importance: core
    one_liner: David holds 50 of 100 cards, three are drawn, winners get $1000 once; g(k) = 1000 min{k,1} gives an expected prize of 1000·29/33 ≈ $878.79, by both routes.
  - id: mean-center-of-mass
    name: The mean as a center of mass
    importance: highlight       # the visual climax
    one_liner: Place a particle of mass p_X(x) at each x — the mean is exactly the center of mass; geometric(p) has mean 1/p, binomial(n, p) has mean np.
  - id: variance-def
    name: The variance
    importance: core
    one_liner: Var[X] = E[(X - E[X])^2] >= 0 measures dispersion around the mean; its square root is the standard deviation sigma; Bernoulli(p) has p(1-p), Poisson(lambda) has lambda.
  - id: affine-rules
    name: Affine functions and linearity
    importance: core
    one_liner: E[aX + b] = a E[X] + b and Var[aX + b] = a^2 Var[X] — expectation is linear, variance ignores shifts and scales by a squared factor.
estimated_runtime_sec: 600      # ~10 min (six beats in project.yaml)
---

# Functions and Expectations — Concept Map

This video covers Section 6.2 with its three subsections: The Mean (6.2.1),
The Variance (6.2.2), and Affine Functions (6.2.3). Video 18 defined E[X];
video 20 (Moments) builds on both.

## What
Expectation combines with ordinary functions to produce a whole family of
summary quantities. For a real-valued g on the range of X,
`E[g(X)] = sum_{x in X(Omega)} g(x) p_X(x)` — computed straight from the PMF
of X, with no need to first derive the distribution of `Y = g(X)`. Two
special cases dominate practice: the **mean** (g(x) = x, a center of mass)
and the **variance** `Var[X] = E[(X - E[X])^2]` (a measure of spread), and
both transform predictably under affine maps `aX + b`.

## Why it matters
Last video the viewer met functions of random variables and had to build the
PMF of `Y = g(X)` from preimages. This video's formula short-circuits that
work: average `g` directly against the PMF of X. That single move unlocks
every summary statistic that matters — mean, variance, and (next video) all
higher moments — and the affine rules are the everyday algebra of
expectations (unit changes, centering, rescaling).

## Key ideas (in dependency order)
1. **The direct formula.** `E[g(X)] = sum_x g(x) p_X(x)`. The mean is the
   special case `g(x) = x`, so this definition subsumes video 18's.
2. **Consistency.** The two-step route (derive `p_Y`, then average) agrees:
   group the x's by their image `y = g(x)` — summing over all y and then
   over each preimage is the same as summing over all x. (Sketch, not a
   full proof, on screen.)
3. **Sanity checks with content.** `E[c] = c` (normalization). Indicators:
   `E[1_S(X)] = Pr(X in S)` — probabilities *are* expectations, an idea that
   pays off repeatedly later.
4. **Extreme Trio.** A concrete contest: 100 cards, David wrote 50, three
   drawn, one prize per person. `X` = David's cards drawn is hypergeometric;
   `g(k) = 1000 min{k, 1}`. Route one sums `g(k) p_X(k)`; route two builds
   the two-point PMF of `Y` (p_Y(0) = 4/33). Both give `1000 · 29/33`.
5. **The mean, revisited (6.2.1).** Geometric(p): `E[X] = 1/p`.
   Binomial(n, p): `E[X] = np` (the sum rearranges into a smaller binomial).
   Physical reading: particles of mass `p_X(x)` at positions x balance
   exactly at `E[X]` — Bernoulli(0.75) balances at 0.75.
6. **The variance (6.2.2).** `Var[X] = E[(X - E[X])^2]`, nonnegative,
   dispersion around the mean; `sigma = sqrt(Var[X])`. Bernoulli(p):
   `p(1-p)`, maximal at p = 1/2. Poisson(lambda): mean *and* variance both
   equal lambda.
7. **Affine functions (6.2.3).** `E[aX + b] = a E[X] + b`;
   more generally `E[a g(X) + h(X)] = a E[g(X)] + E[h(X)]` (expectation is
   a linear functional). `Var[aX + b] = a^2 Var[X]`: shifts don't spread a
   distribution, scaling spreads it quadratically.

## What else (connections, to seed callbacks in narration)
- `Y = g(X)` and its PMF via preimages is video 17 — the consistency
  argument is a callback, not new machinery.
- The indicator function was introduced in video 2 (Functions); the
  indicator RV reappears here as a bridge between probability and
  expectation.
- Bernoulli/binomial/geometric/Poisson PMFs are from video 16 — reuse their
  established chart looks.
- The center-of-mass picture returns in video 20: variance as the moment of
  inertia (mentioned there, not here).

## Conceptual progression (drives the storyboard)
"To average Y = g(X), must we rebuild its PMF?" → the direct formula → both
routes computed side by side on the Extreme Trio contest, same number →
indicator: expectation contains probability → the mean as the balance point
of the PMF (center of mass) → spread: same balance point, different widths →
variance definition → the affine dial: slide b (balance moves, spread fixed),
stretch a (spread grows like a²).

## Visual opportunities
- **Two-column two-routes**: left, X's PMF with `g` applied bar by bar;
  right, the two-point PMF of Y; both columns converge on `1000 · 29/33`.
- **Balance beam**: the Bernoulli(0.75) PMF drawn as two disks of mass 0.25
  and 0.75 on a rod; a fulcrum slides until it balances at 0.75 (book's
  center-of-mass figure, animated).
- **Spread**: two PMFs with the same mean, one tight and one wide, with
  `(x - E[X])^2` weights lighting up to show why the wide one scores higher.
- **Affine dial**: the whole PMF translating by b (fulcrum follows, spread
  unchanged), then stretching by a (spread visibly grows, fulcrum scales).

## Notation (per project.yaml)
- Expectation `\mathrm{E}[\cdot]`, variance `\mathrm{Var}(\cdot)` via the
  _style helpers; indicator `\mathbf{1}_S` (never the blackboard-bold form).
- Hypergeometric PMF written with binomials:
  `p_X(k) = \binom{50}{k}\binom{50}{3-k}/\binom{100}{3}`.

## Deliberately out of scope
- Moments `E[X^n]`, central moments, and `Var = E[X^2] - (E[X])^2` — video 20.
- Full algebraic derivations of the geometric/binomial means — shown as
  results with one visual hint each, not derived line by line.
- Independence and expectations of products — later chapters.

## Cut first (if the script runs over budget)
The consistency sketch (idea 2) compresses to one sentence over the
two-routes visual; the binomial-mean derivation drops to a stated result.
