---
slug: 39-independence-continuous
title: Independent Continuous Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/39-independence-continuous.tex
source_sha256: 2da1958c9d3a0c53407034836104566198687b16e6087b0eaddaae49bc5824f8
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/random_vectors.tex
companion: sources/39-independence-continuous.md
companion_sha256: 844e4470fe388913fc5a31a5b72b6646b968aeac5a4f499cf40952e94bdf1277
prereqs:
  - 38-conditioning-densities
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: indep-cdf-def
    name: Independence as a factoring joint CDF
    importance: core
    one_liner: X and Y are independent when F_{X,Y}(x,y) = F_X(x) F_Y(y) for ALL x, y — the definition lives at the CDF level, so it covers every kind of random variable.
  - id: pdf-factorizes
    name: The joint density factors too
    importance: core
    one_liner: Differentiating the product CDF gives f_{X,Y}(x,y) = f_X(x) f_Y(y) — the density surface is a product of its two marginal profiles.
  - id: conditional-is-marginal
    name: Conditioning tells you nothing new
    importance: core
    one_liner: f_{Y|X}(y|x) = f_X(x) f_Y(y) / f_X(x) = f_Y(y) — under independence every slice of the surface is the same marginal; observing X leaves Y's density untouched.
  - id: events-factor
    name: Derived events inherit independence
    importance: core
    one_liner: Pr(X in S, Y in T) = Pr(X in S) Pr(Y in T) — the double integral splits into a product, so independence of variables delivers independence of all the events they generate.
  - id: unit-square
    name: Worked example — the unit square, X vs Y and X vs W
    importance: highlight
    one_liner: Uniform on the unit square - F_{X,Y}(x,y) = xy = F_X(x) F_Y(y), so X and Y are independent; but for W = X + Y, F_{X,W}(0.5, 1) = 3/8 differs from F_X(0.5) F_W(1) = 1/4 — one counterexample point suffices.
estimated_runtime_sec: 290
---

# Independent Continuous Variables — Concept Map

This video covers Section 11.3 of book chapter 11 (Independence, up to but
not including the sums subsection). It is the continuous twin of video 24:
there the joint PMF table factored into a product of margins; here the
density surface does. Video 38 built the conditional slices this video
declares identical; video 40 cashes independence in for the convolution
formula.

## What
Two random variables are **independent** when the joint CDF factors:
`F_{X,Y}(x,y) = F_X(x) F_Y(y)` for every x and y. For jointly continuous
pairs the mixed partial derivative carries the product down to densities,
`f_{X,Y}(x,y) = f_X(x) f_Y(y)`, and dividing by f_X collapses the
conditional to the marginal: `f_{Y|X}(y|x) = f_Y(y)` — observing X changes
nothing about Y. The product then propagates upward to every pair of
derived events, `Pr(X in S, Y in T) = Pr(X in S) Pr(Y in T)`. The unit
square is the complete worked example: its coordinates X and Y are
independent, but X and the sum W = X + Y are not — one evaluation point,
`F_{X,W}(0.5, 1) = 3/8 ≠ 1/4`, settles it.

## Why it matters
Independence is the assumption that makes models computable — noise
independent of signal, one sample independent of the next — and this video
gives its continuous certificate: check whether the joint factors. The
three equivalent faces (CDF product, PDF product, conditional = marginal)
are used interchangeably in every field that touches probability, and the
unit-square counterexample teaches the equally important negative skill:
dependence created not by exotic distributions but by simply *building one
variable from another*. Video 40's convolution — and, one chapter later,
the law of large numbers — stand entirely on this definition.

## Key ideas (in dependency order)
1. **The definition, at the CDF level.**
   `F_{X,Y}(x,y) = F_X(x) F_Y(y)` for all `x, y in R` — mutual
   independence means the accumulation quadrant's probability always
   splits. Stated with CDFs (video 26's universal object), so it needs no
   density to exist.
2. **Densities factor.** For jointly continuous pairs,
   `f_{X,Y}(x,y) = d^2 F_{X,Y}/dx dy = (dF_X/dx)(dF_Y/dy)
   = f_X(x) f_Y(y)` — the product of one-variable profiles; video 37's
   Gaussian example was secretly built this way.
3. **Conditional = marginal.** From video 38's definition,
   `f_{Y|X}(y|x) = f_{X,Y}(x,y)/f_X(x) = f_X(x) f_Y(y)/f_X(x) = f_Y(y)`
   (wherever f_X(x) ≠ 0): every slice of the surface, renormalized, is
   the same curve. Video 24's "the rows are all proportional," said with
   densities.
4. **Events factor.** `Pr(X in S, Y in T) = int_S int_T f_{X,Y} dy dx
   = int_S f_X dx · int_T f_Y dy = Pr(X in S) Pr(Y in T)` — the double
   integral separates, recovering chapter 4's event independence (video
   14) for every S and T at once.
5. **Worked: the unit square, both verdicts.** Pick (ω1, ω2) uniformly
   from the unit square; X = ω1, Y = ω2, W = ω1 + ω2.
   *Independent:* for x, y in [0,1], `F_{X,Y}(x,y) = xy = F_X(x) F_Y(y)`,
   and the indicator form `int 1_{[0,1]}(u) du · int 1_{[0,1]}(v) dv`
   extends the product to all of R^2.
   *Not independent:* `F_W(1) = 0.5`, `F_X(0.5) = 0.5`, but
   `F_{X,W}(0.5, 1) = int_0^{1/2} (1-x) dx = 3/8 ≠ 1/4` — knowing X
   shifts where W can be, and a single point of failure disproves the
   product for good.

## What else (connections, to seed callbacks in narration)
- Video 24 is the discrete twin beat for beat: factoring joint PMF ->
  factoring joint PDF, table rows proportional -> surface slices
  identical.
- Video 14 defined independent *events*; idea 4 shows variable
  independence manufacturing event independence wholesale.
- Video 37's two-Gaussian example wrote `f_{X,Y} = f_X f_Y` on faith; this
  video supplies the license, and its rotationally symmetric surface is
  the picture of idea 2.
- Video 38's slice family is the right mental test: independence iff the
  sweeping slice never changes shape.
- The X-vs-W half of the example is the perfect on-ramp to video 40: the
  sum W = X + Y is the next object studied — there with the two summands
  independent.

## Conceptual progression (drives the storyboard)
"When does knowing X tell you nothing about Y?" → the definition: the
joint CDF factors, everywhere → differentiate twice: the density surface
is a product of two profiles → divide: the conditional slice equals the
marginal — video 38's sweeping slice frozen → integrate: every event pair
factors, video 14 recovered at scale → the unit square: verify the
product honestly (both on [0,1] and via indicators) → build W = X + Y
from the same coordinates → test one point: 3/8 vs 1/4 — dependence by
construction → the sum W carries us into video 40.

## Visual opportunities
- **Product surface**: two marginal density profiles standing on
  perpendicular walls; the joint surface woven out of their product, each
  height literally f_X times f_Y.
- **Frozen slice family**: video 38's cutting plane sweeps across the
  surface; under independence the lifted, renormalized slice never
  changes — played against a dependent surface where it visibly morphs.
- **Splitting integral**: the double integral over S x T pulling apart
  into two one-dimensional shaded areas, the region on the plane
  factoring into a strip times a strip.
- **Unit square check**: the square with the quadrant [0,x] x [0,y]
  shaded; its area xy against the two side lengths F_X(x) and F_Y(y).
- **The counterexample**: the region {X <= 0.5, W <= 1} drawn inside the
  square (a trapezoid under the line x + w cut by x = 0.5), area 3/8
  computed on screen next to the failed product 1/4 — one red inequality
  sign as the verdict.

## Notation (per project.yaml)
- Joint objects `F_{X,Y}`, `f_{X,Y}`; conditionals `f_{Y \mid X}(y \mid
  x)` with `\mid`; probabilities via `\Pr` with commas for joint events;
  indicator `\mathbf{1}_{[0,1]}`.

## Deliberately out of scope
- Sums of independent variables and the convolution integral — video 40
  in its entirety (W = X + Y appears here only as a dependence
  counterexample, never distributed).
- Expectations of products, variance of sums, and iid — covered
  discretely in video 24 and not restated in this section of the notes.
- Covariance, correlation, and "uncorrelated vs independent" — scratch-
  note themes outside the shipped section.
- Independence of more than two variables — the notes stay with pairs
  here.

## Cut first (if the script runs over budget)
The indicator-function extension of the unit-square verification (the
all-of-R^2 case) compresses to one sentence over the [0,1]^2 computation;
idea 4's derivation reduces to the statement with the integral split shown
but not narrated line by line.
