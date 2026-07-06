---
slug: 32-change-of-variables
title: The Change-of-Variables Formula
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/32-change-of-variables.tex
source_sha256: 7c91a09f784bbdf3d5af3f1433210909e87bc606c7686af4e399619680d116bc
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/derived_distributions.tex
companion: sources/32-change-of-variables.md
companion_sha256: af8623dfc2346b019e3e5f41f532c43d3eb0800478e576aef14c19a60a613439
prereqs:
  - 31-derived-cdf-method
audience: undergraduate engineering, first probability course
concepts:
  - id: invert-then-differentiate
    name: Invert, then differentiate
    importance: core
    one_liner: For differentiable, strictly increasing g, F_Y(y) = F_X(g^{-1}(y)); one derivative in y gives f_Y(y) = f_X(g^{-1}(y)) dx/dy — video 31's CDF method, run through the chain rule.
  - id: slope-rescales-density
    name: The slope rescales the density
    importance: highlight
    one_liner: A width-delta strip on the y-axis pulls back to an x-interval whose size is set by dg/dx — shallow slope, wide interval, more probability; steep slope, narrow interval, less.
  - id: change-of-variables-formula
    name: The change-of-variables formula
    importance: core
    one_liner: For differentiable, strictly monotone g - f_Y(y) = f_X(g^{-1}(y)) |dx/dy| = f_X(x)/|dg/dx(x)| with x = g^{-1}(y); the absolute value absorbs the decreasing case's minus sign.
  - id: gaussian-affine
    name: Worked example — an affine Gaussian stays Gaussian
    importance: core
    one_liner: Y = aX + b of a standard Gaussian has f_Y(y) = e^{-(y-b)^2/(2a^2)} / (sqrt(2 pi) |a|) — a Gaussian again; affine maps never leave the family.
  - id: rayleigh-energy
    name: Worked example — channel fading and energy
    importance: optional        # comparison beat; cut first if over budget
    one_liner: The Rayleigh-squared problem of video 31, redone in one line - f_Y(y) = f_X(sqrt(y)) / |dg/dx(sqrt(y))| = (1/2) e^{-y/2} — same exponential, no integral.
  - id: sum-over-roots
    name: Non-monotone g — sum over the roots
    importance: core
    one_liner: With finitely many local extrema g is piecewise monotone, so f_Y(y) = sum over {x - g(x) = y} of f_X(x)/|dg/dx(x)| — each root of g(x) = y contributes its own rescaled density.
  - id: cosine-arcsine
    name: Worked example — signal phase and amplitude
    importance: highlight
    one_liner: X uniform on [0, 2 pi), Y = cos(X) - two roots per y give f_Y(y) = 1/(pi sqrt(1 - y^2)) on (-1, 1) — the density piles up at the amplitude extremes.
estimated_runtime_sec: 320
---

# The Change-of-Variables Formula — Concept Map

This video covers Section 9.2 of book chapter 9 (Differentiable Functions).
Video 31 derived CDFs by chasing the event `{g(X) <= y}`; here one extra
assumption — differentiability — lets us differentiate that answer and go
*straight to densities*. Video 33 will point this formula at the CDF itself
and turn it into a recipe for generating random variables.

## What
When g is differentiable and strictly monotone it is invertible, so
`F_Y(y) = F_X(g^{-1}(y))` (increasing case) has no sup left in it — and
differentiating with the chain rule yields the **change-of-variables
formula** `f_Y(y) = f_X(g^{-1}(y)) |dx/dy| = f_X(x) / |dg/dx(x)|` where
`x = g^{-1}(y)`. The derivative is not a technicality: it is the local
stretch factor that keeps probability conserved as g reshapes the axis.
When g is merely piecewise monotone (finitely many local extrema), each
root x of `g(x) = y` contributes one such term, and
`f_Y(y) = sum_{x: g(x)=y} f_X(x) / |dg/dx(x)|`.

## Why it matters
This is the workhorse formula of derived distributions — the one engineers
actually memorize. It explains in one stroke why the Gaussian family is
closed under amplification and offset (video 28's noisy channel can be
rescaled at will), it collapses video 31's four-line Rayleigh-energy
integral to a single line, and its sum-over-roots form handles genuinely
non-invertible transforms like sampling the phase of a sinusoid. It is also
the continuous twin of video 17's PMF regrouping sum — the discrete formula
needed no derivative because masses travel whole; densities must be
rescaled by how much the axis stretches.

## Key ideas (in dependency order)
1. **Invertibility.** Differentiable + strictly increasing means g is
   invertible: `x = g^{-1}(y)` is unambiguous, and video 31's sup formula
   simplifies to `F_Y(y) = Pr(X <= g^{-1}(y)) = F_X(g^{-1}(y))`.
2. **Differentiate.** By the chain rule,
   `f_Y(y) = f_X(g^{-1}(y)) d/dy g^{-1}(y) = f_X(x) dx/dy = f_X(x) / (dg/dx)(x)`.
   Since g is strictly increasing, `dg/dx > 0` and Y is a continuous random
   variable.
3. **Why the derivative belongs there.** The notes' figure: a strip of
   width delta on the y-axis corresponds, through g, to an interval on the
   x-axis whose width is governed by the slope — a small slope produces a
   wide x-interval (much probability funneled into that y-strip), a steep
   slope a narrow one. The derivative is the exchange rate between the two
   axes.
4. **The decreasing case and the combined formula.** For strictly
   decreasing g, `F_Y(y) = 1 - F_X(g^{-1}(y))`, and differentiating gives
   `f_Y(y) = f_X(x) / (-dg/dx(x))` — the slope is negative, and the minus
   sign makes the density positive. Both cases in one statement:
   `f_Y(y) = f_X(g^{-1}(y)) |dx/dy| = f_X(x) / |dg/dx(x)|`, `x = g^{-1}(y)`.
5. **Worked: the affine Gaussian.** X standard Gaussian
   (`f_X(x) = e^{-x^2/2} / sqrt(2 pi)`), Y = aX + b with a != 0. Then
   `g^{-1}(y) = (y - b)/a`, `dx/dy = 1/a`, and
   `f_Y(y) = e^{-(y-b)^2 / (2 a^2)} / (sqrt(2 pi) |a|)` — a Gaussian. The
   same progression shows an affine function of *any* Gaussian remains
   Gaussian.
6. **Worked: channel fading and energy.** X Rayleigh with sigma^2 = 1
   (`f_X(x) = x e^{-x^2/2}`, x >= 0), Y = X^2. X is non-negative and
   `g(x) = x^2` is strictly monotone on [0, inf), so
   `f_Y(y) = f_X(sqrt(y)) / |dg/dx(sqrt(y))| = sqrt(y)/(2 sqrt(y)) e^{-y/2}
   = (1/2) e^{-y/2}` for y >= 0 — the exponential with parameter 1/2, in
   one line where video 31 needed an integral.
7. **Sum over the roots.** If g is differentiable with a finite number of
   local extrema, it is piecewise monotonic, and
   `f_Y(y) = sum_{{x | g(x) = y}} f_X(x) / |dg/dx(x)|`: find every x with
   `g(x) = y`, apply the monotone formula locally, add the contributions.
   This is the continuous version of video 17's
   `p_Y(y) = sum_{x: g(x)=y} p_X(x)` — with the stretch factor the discrete
   sum never needed.
8. **Worked: signal phase and amplitude.** X uniform on [0, 2 pi),
   Y = cos(X) — sampling a sinusoid at a random phase. For y in (-1, 1) the
   preimage holds two points, `arccos(y)` and `2 pi - arccos(y)`; with
   `d/dx cos(x) = -sin(x)`, each contributes `1 / (2 pi sqrt(1 - y^2))`,
   so `f_Y(y) = 1 / (pi sqrt(1 - y^2))` on (-1, 1). The density diverges at
   the amplitude extremes y = ±1, where the sinusoid lingers.

## What else (connections, to seed callbacks in narration)
- Video 31's CDF method is the parent: this formula IS that method plus one
  derivative, and the Rayleigh-energy example is deliberately the same
  problem solved twice.
- Video 28 introduced the Gaussian and its noisy channel; idea 5 is the
  license to scale and shift that noise freely.
- Video 17's sum over preimages returns as idea 7's continuous twin — the
  notes themselves invite the comparison.
- Video 27 defined the density as the derivative of the CDF; ideas 1–2 are
  that definition doing its first real transform work.
- The arccos-root picture foreshadows video 33, where inverting a CDF is
  the entire algorithm.

## Conceptual progression (drives the storyboard)
Video 31's sup formula recalled → add differentiability: the sup dies,
g^{-1} is a genuine function → differentiate the CDF identity → the slope
as an exchange rate between axes (delta-strip picture) → the decreasing
case folds in via the absolute value → the formula stamped as the section's
centerpiece → affine Gaussian: the family is closed → Rayleigh energy: one
line beats last video's integral → g loses monotonicity: split it into
monotone pieces, one term per root → the sinusoid sampled at random phase:
two roots, an arcsine-shaped density spiking at ±1.

## Visual opportunities
- **The delta-strip machine**: a strip of width delta sliding up the y-axis
  of a monotone curve; its pullback interval on the x-axis visibly widening
  on shallow stretches and pinching on steep ones, while a density bar
  rescales reciprocally — the |dg/dx| made kinetic.
- **Formula assembly**: `F_Y = F_X(g^{-1})` differentiating term by term,
  the chain-rule factor sliding out and landing as the denominator.
- **Affine Gaussian**: the bell curve shifting by b and stretching by a
  while the label updates — silhouette unchanged, still a bell.
- **Two derivations, one answer**: video 31's multi-line Rayleigh integral
  shown, then wiped and replaced by the single change-of-variables line
  ending in the same (1/2) e^{-y/2}.
- **Roots stacking**: the notes' wavy g with a horizontal line at y cutting
  it three times; from each intersection a contribution drops to a running
  stack that totals f_Y(y).
- **Cosine pile-up**: uniform phase dots on [0, 2 pi) flowing through
  cos(x) onto the y-axis, accumulating into a histogram that hugs the
  arcsine density with its walls at ±1.

## Notation (per project.yaml)
- Densities `f_X, f_Y`; CDFs `F_X, F_Y`; probabilities via `\Pr`.
- Inverse `g^{-1}(y)`; derivative magnitude written
  `\left| \frac{dg}{dx}(x) \right|`; sums over root sets with set-builder
  `\mid`, never a bare bar in rendered math.

## Deliberately out of scope
- The sup/inf CDF formulas for non-differentiable monotone g — video 31
  owns them; here they are only recalled.
- Generating random variables (F_X(X) uniform, inverse-CDF sampling) —
  video 33 in its entirety.
- The CDF of the cosine example — the notes note the integral needs a
  trigonometric substitution and stop there; so do we.
- Multivariate transforms and Jacobians — this chapter is one-dimensional;
  random vectors return in videos 37–40.

## Cut first (if the script runs over budget)
The channel-fading example (idea 6) compresses to a one-line caption under
the formula — "video 31's Rayleigh, one line, same exponential." Next, the
decreasing-case derivation (idea 4) reduces to "the minus sign the absolute
value absorbs," shown over the combined formula only.
