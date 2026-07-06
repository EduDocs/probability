---
slug: 27-pdfs-expectation
title: Densities and Expectation
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/27-pdfs-expectation.tex
source_sha256: 97aed752ea5c0b160dea541368e4cd64a021b6399ffd9be0c700af4b14c4bb41
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/continuous_random_variables.tex
companion: sources/27-pdfs-expectation.md
companion_sha256: 03278c8dbecd26d8dca205580ba51bc9f97be65ef64ad47c706c28ed082efb4c
prereqs:
  - 26-cdfs
audience: undergraduate engineering, first probability course
concepts:
  - id: pdf-definition
    name: The probability density function
    importance: core
    one_liner: f_X = dF_X/dx, and back again F_X(x) = integral of f_X up to x — the fundamental theorem of calculus links density and CDF.
  - id: probability-as-area
    name: Probabilities are areas
    importance: core
    one_liner: Pr(x_1 < X <= x_2) = integral of f_X over the interval — the continuous analog of summing PMF bars.
  - id: zero-point-mass
    name: Single points carry no probability
    importance: core
    one_liner: Pr(X = x) = 0 for every x, so endpoints never matter — and f_X(x) is a DENSITY, not a probability (it may exceed one).
  - id: density-axioms
    name: What a density must satisfy
    importance: core
    one_liner: f_X >= 0 and its total integral is one; Pr(X in S) = integral of f_X over S — the axioms, translated to integrals.
  - id: expectation-integral
    name: Expectation as an integral
    importance: core
    one_liner: E[g(X)] = integral of g(x) f_X(x) dx — the discrete weighted sum with the sum replaced by an integral; mean and variance follow verbatim.
  - id: tail-formula
    name: The tail formula for nonnegative variables
    importance: highlight
    one_liner: E[X] = integral of Pr(X > x) dx — compute a mean straight from tail probabilities, no density required.
  - id: dartboard
    name: Worked example — darts on a unit target
    importance: core
    one_liner: Uniform dart on a unit disk, Pr(R > r) = 1 - r^2, so E[R] = 2/3 by the tail formula — without ever writing f_R.
estimated_runtime_sec: 300
---

# Densities and Expectation — Concept Map

This video covers Sections 8.2–8.3 of book chapter 8. Video 26 built the
CDF bridge; this video differentiates it into the density and re-founds
expectation on integrals. Videos 28–30 then populate the theory with the
named distributions.

## What
For a continuous random variable, the derivative of the CDF is the
**probability density function** `f_X = dF_X/dx`; the fundamental theorem
of calculus runs it backwards, `F_X(x) = ∫_{-inf}^x f_X`. Probabilities of
intervals become areas under the density, single points carry zero
probability, and the axioms translate into two conditions: `f_X >= 0` and
total area one. **Expectation** carries over with the sum replaced by an
integral: `E[g(X)] = ∫ g(u) f_X(u) du`, with mean and variance as before.
A bonus tool: for nonnegative X, `E[X] = ∫_0^inf Pr(X > x) dx` — means
from tails.

## Why it matters
The density is the continuous world's working object — every distribution
in the rest of the course is specified by its PDF. Getting its *meaning*
right (a density, not a probability; areas, not heights) prevents the
classic misconceptions, and the expectation integral means every tool from
chapter 6 — LOTUS, mean, variance, the variance shortcut — survives with
sums swapped for integrals. The tail formula is the first genuinely new
trick, and the dartboard shows it paying off.

## Key ideas (in dependency order)
1. **Definition, both directions.** `f_X(x) = dF_X/dx(x)` and
   `F_X(x) = ∫_{-inf}^x f_X(u) du` — differentiate to get the density,
   integrate to get back the CDF.
2. **Intervals are areas.** Combining with video 26's interval formula:
   `Pr(x_1 < X <= x_2) = ∫_{x_1}^{x_2} f_X(u) du`.
3. **Points are massless.** Shrink the interval: `Pr(X = x) = 0` — so
   `Pr(x_1 < X < x_2) = Pr(x_1 <= X <= x_2)`: endpoints never matter.
   Corollary of the corollary: f_X(x) is NOT `Pr(X = x)`; a density can
   exceed one.
4. **The axioms, translated.** Total area one (normalization), `f_X >= 0`
   (nonnegativity), and `Pr(X in S) = ∫_S f_X` for admissible S.
5. **Expectation revisited.** `E[g(X)] = ∫ g(u) f_X(u) du`; the mean
   `E[X] = ∫ u f_X(u) du`; the variance and its shortcut
   `Var[X] = E[X^2] - (E[X])^2` verbatim from chapter 6.
6. **The tail formula.** For nonnegative X with finite mean,
   `E[X] = ∫_0^inf Pr(X > x) dx` — proved by swapping the order of a
   double integral (picture: integrating the same region by rows instead
   of columns).
7. **Worked: the dartboard.** A dart uniform on a unit disk;
   `Pr(R > r) = 1 - r^2` by area ratio; the tail formula gives
   `E[R] = ∫_0^1 (1 - r^2) dr = 2/3` — no density ever written.

## What else (connections, to seed callbacks in narration)
- The whole beat structure mirrors chapter 6 (videos 18–19): definition,
  properties, LOTUS, worked example — now with integrals. Narration can
  lean on "same sentence, new symbol."
- `Pr(X = x) = 0` echoes video 10's continuity of probability measures
  (shrinking nested intervals).
- The area-swap proof of the tail formula is the continuous cousin of
  video 18's layered-sum picture for `E[X] = sum Pr(X >= k)`.
- The dartboard's area-ratio step reuses video 9's geometric probability
  models.

## Conceptual progression (drives the storyboard)
Ramp CDF recalled → its slope, the density → area under the curve as
interval probability → the shrinking interval kills point mass →
"density, not probability" (a tall thin PDF as counterexample) → the two
axioms as area statements → expectation: the discrete sum morphing
symbol-by-symbol into the integral → mean/variance restated → the tail
formula via the order-swap picture → darts: geometry gives the tail, the
tail gives the mean.

## Visual opportunities
- **Slope-to-area duality**: the CDF above, its derivative below; a moving
  point x drags a shaded area under f that always equals the CDF height.
- **Shrinking interval**: the shaded strip under the density narrows to a
  line of zero area — Pr(X = x) = 0 as a vanishing sliver.
- **Sum morphs to integral**: chapter 6's `E[g(X)] = Σ g(x) p_X(x)` with
  the Σ transforming into ∫ and the bars melting into a smooth curve.
- **Order swap**: the region {0 < x < u} shaded and integrated by vertical
  strips, then by horizontal strips — the tail-formula proof as one
  picture.
- **Dartboard**: a unit disk, a ring at radius r; the ring's outside area
  as Pr(R > r); the tail curve 1 - r^2 integrated to 2/3.

## Notation (per project.yaml)
- Density `f_X(x)`, CDF `F_X(x)`; expectation `\mathrm{E}[\cdot]`,
  variance `\mathrm{Var}[\cdot]` via the _style helpers; integrals over
  `\mathbb{R}` written with explicit limits.

## Deliberately out of scope
- Any named density beyond the anonymous examples (uniform is video 28's
  opener).
- Joint densities and multiple continuous variables (a later book
  chapter).
- Rigorous treatment of "admissible sets" — one honest sentence, no
  measure theory.

## Cut first (if the script runs over budget)
The tail-formula *proof* compresses to the order-swap picture with one
spoken sentence (keep the statement and the dartboard); the corollary
chain about endpoints compresses to "endpoints never matter."
