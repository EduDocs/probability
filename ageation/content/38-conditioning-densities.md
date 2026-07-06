---
slug: 38-conditioning-densities
title: Conditioning with Densities
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/38-conditioning-densities.tex
source_sha256: ef89abce190ca6564704c55877c2f10d89c6d17eb67f14322b820b3eed1a3d8b
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/random_vectors.tex
companion: sources/38-conditioning-densities.md
companion_sha256: 844e4470fe388913fc5a31a5b72b6646b968aeac5a4f499cf40952e94bdf1277
prereqs:
  - 37-joint-continuous
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: cond-given-event
    name: Conditional CDF and PDF given an event
    importance: core
    one_liner: F_{X|A}(x) = Pr(X <= x | A) = Pr({X <= x} ∩ A) / Pr(A), and f_{X|A} is its derivative — chapter 4's ratio, applied to accumulation events.
  - id: interval-conditioning
    name: Conditioning on an interval renormalizes the density
    importance: core
    one_liner: For A = {X in I}, f_{X|A}(x) = f_X(x) / Pr(X in I) on I and zero elsewhere — the truncate-and-rescale move of the discrete arc, run on a smooth curve.
  - id: exp-race
    name: Worked example — conditioning on Y <= X
    importance: optional        # cut first if over budget
    one_liner: For the joint density lambda^2 e^{-lambda(x+y)}, the event A = {Y <= X} has Pr(A) = 1/2 by symmetry and yields f_{X|A}(x) = 2 lambda e^{-lambda x}(1 - e^{-lambda x}).
  - id: cond-pdf-values
    name: Conditioning on a value of Y
    importance: core
    one_liner: f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y) — defined with care because Pr(Y = y) = 0; the shrinking-box argument shows f_{X|Y}(x|y) Δx ≈ Pr(X near x | Y near y).
  - id: circle-slice
    name: Worked example — slicing the unit circle
    importance: core
    one_liner: Uniform on the disk, given Y = 0.5 - f_Y(0.5) = sqrt(3)/pi and f_{X|Y}(x|0.5) = 1/sqrt(3) on |x| <= sqrt(3)/2 — a slice of the surface, renormalized to area one.
  - id: cond-expectation
    name: Conditional expectation with densities
    importance: core
    one_liner: E[g(Y) | X = x] = integral of g(y) f_{Y|X}(y|x) dy, and h(x) = E[Y | X = x] defines a random variable — video 23's object, rebuilt with integrals.
  - id: mmse-channel
    name: Worked example — estimating a signal through noise
    importance: highlight
    one_liner: Y = X + N with X, N standard Gaussians - f_{X|Y}(x|y) is Gaussian with m = y/2, sigma^2 = 1/2, so the MMSE estimate is E[X | Y = y] = y/2.
  - id: jacobian-derived
    name: Derived distributions via the Jacobian
    importance: core
    one_liner: For an invertible pair Y_i = g_i(X_1, X_2), f_{Y_1,Y_2}(y_1,y_2) = f_{X_1,X_2}(x_1,x_2) / |J(x_1,x_2)| — chapter 9's change-of-variables with the Jacobian determinant replacing |g'|.
  - id: gaussian-affine
    name: Affine maps preserve Gaussian vectors
    importance: optional        # compress to a statement if over budget
    one_liner: If X is a jointly Gaussian vector and Y = AX + b with A invertible, the Jacobian formula shows Y is jointly Gaussian with mean Am + b and covariance A Sigma A^T.
estimated_runtime_sec: 320
---

# Conditioning with Densities — Concept Map

This video covers Section 11.2 of book chapter 11 (the conditional-CDF
preamble plus all three subsections: Conditioning on Values, Conditional
Expectation, Derived Distributions). Video 37 built the density surface
this video slices; video 39 asks when the slices are all the same. It is
the continuous twin of videos 22–23: in chapter 7 we sliced a table and
averaged the slices; now we slice a surface and integrate.

## What
Conditioning crosses into the continuous world in two steps. Given an
event A, the **conditional CDF** `F_{X|A}(x) = Pr(X <= x | A)` is chapter
4's ratio, and its derivative is the conditional density; when
`A = {X in I}` this simply renormalizes f_X over the interval. The harder
and more useful step is conditioning on a *value*: `{Y = y}` has
probability zero, yet `f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y)` works — a
shrinking-box limit justifies it. Conditional expectation follows by
integration, `E[g(Y) | X = x] = int g(y) f_{Y|X}(y|x) dy`, and
`h(x) = E[Y | X = x]` is again a random variable. The section closes with
derived distributions for pairs: the Jacobian change-of-variables formula
`f_{Y_1,Y_2} = f_{X_1,X_2} / |J|`, whose star application is that affine
maps of Gaussian vectors stay Gaussian.

## Why it matters
Observation is the engine of inference, and in the continuous world every
interesting observation — "the received voltage was 1.3" — is an event of
probability zero. The conditional density is the tool that makes such
statements meaningful, and the Gaussian channel example shows it doing
real engineering: the MMSE estimator, the workhorse of communication and
control, is nothing but a conditional expectation. The Jacobian formula is
the same story for transformations: chapter 9 taught one variable; real
systems mix two.

## Key ideas (in dependency order)
1. **Conditioning on an event.** For Pr(A) > 0,
   `F_{X|A}(x) = Pr(X <= x | A) = Pr({X <= x} ∩ A) / Pr(A)`, and
   `f_{X|A}(x) = dF_{X|A}/dx` — the event A may itself involve X and Y
   (e.g. `A = {Y <= X}`). Nothing new is postulated; video 11's ratio
   meets video 26's CDF.
2. **Interval conditioning = renormalization.** For `A = {X in I}`,
   differentiating `Pr(X in (-inf,x] ∩ I) / Pr(X in I)` gives
   `f_{X|A}(x) = f_X(x) / Pr(X in I)` for x in I, zero otherwise — the
   truncated-geometric move of video 22 and the memoryless rescaling of
   video 29, now stated in full generality.
3. **Worked: the race.** For `f_{X,Y}(x,y) = lambda^2 e^{-lambda(x+y)}`
   on x, y >= 0 and `A = {Y <= X}`:
   `Pr({X <= x} ∩ A) = (1 - e^{-lambda x})^2 / 2`, `Pr(A) = 1/2` by
   symmetry, so `f_{X|A}(x) = 2 lambda e^{-lambda x}(1 - e^{-lambda x})`.
   A region event, integrated over a triangle.
4. **Conditioning on a value.** For jointly continuous (X, Y) and
   f_Y(y) > 0, define `f_{X|Y}(x|y) = f_{X,Y}(x,y) / f_Y(y)`. The
   justification: for small boxes,
   `Pr(x <= X <= x+Δx | y <= Y <= y+Δy) ≈ (f_{X,Y}(x,y)/f_Y(y)) Δx` — the
   Δy cancels, so the limit is honest even though `Pr(Y = y) = 0`. Then
   `Pr(X in S | Y = y) = int_S f_{X|Y}(x|y) dx`. The caution is part of
   the content: conditional probability needs a non-vanishing condition;
   this construction only makes sense for jointly continuous pairs.
5. **Worked: the circle slice.** Uniform on the unit disk, condition on
   Y = 0.5: `f_Y(0.5) = int f_{X,Y}(x, 0.5) dx = sqrt(3)/pi` (marginals by
   integrating out — video 37's move), and
   `f_{X|Y}(x|0.5) = 1/sqrt(3)` on `|x| <= sqrt(3)/2` — a chord of the
   disk, and the conditional is uniform on it.
6. **Conditional expectation.** `E[g(Y) | X = x] = int g(y) f_{Y|X}(y|x)
   dy` and `E[g(Y) | A] = int g(y) f_{Y|A}(y) dy` — the weighted average,
   with the correct conditional density as the weight. As x varies,
   `h(x) = E[Y | X = x]` varies: a conditional expectation is itself a
   random variable, exactly as video 23 discovered discretely.
7. **Worked: the noisy channel (MMSE).** Transmit X, receive Y = X + N,
   with X and N independent standard Gaussians. The joint density is
   `f_{X,Y}(x,y) = (1/(2 pi)) exp(-(2x^2 - 2xy + y^2)/2)`; dividing by
   f_Y(y) leaves a Gaussian in x with `m = y/2`, `sigma^2 = 1/2`. The
   minimum-mean-square-error estimator is the conditional expectation:
   `E[X | Y = y] = y/2` — split the difference between what was received
   and the zero-mean prior.
8. **Derived distributions in two dimensions.** For totally
   differentiable `g_1, g_2` with nonvanishing Jacobian determinant
   `|J(x_1,x_2)| = det[dg_i/dx_j]` and a unique inverse
   `x_i = h_i(y_1, y_2)`:
   `f_{Y_1,Y_2}(y_1,y_2) = f_{X_1,X_2}(x_1,x_2) / |J(x_1,x_2)|` — the
   two-dimensional sibling of chapter 9's monotone-function formula, with
   |J| playing the role of |g'|. The general derivation is vector
   calculus; the notes state the clean invertible case.
9. **Payoff: Gaussian vectors under affine maps.** With mean vector m and
   covariance matrix Sigma defining the jointly Gaussian density, apply
   the Jacobian formula to `Y = AX + b` (A invertible, |J| = |det A|):
   the result has the Gaussian form again, with mean `Am + b` and
   covariance `A Sigma A^T`. Gaussianity survives every affine map — in
   any dimension — which is why Gaussian models dominate engineering.

## What else (connections, to seed callbacks in narration)
- Video 22's slice-a-row-and-renormalize is the exact template: the joint
  table became a surface (video 37), so the row becomes a slice curve.
- Video 23's "E[Y | X] is a random variable" and tower property return
  with integrals in place of sums; the MMSE estimator is that idea
  earning a salary.
- The truncate-and-rescale picture ran in video 22 (geometric) and video
  29 (memorylessness); idea 2 is its general statement.
- Chapter 9 (videos 31–32) did derived distributions for one variable;
  the Jacobian formula is the promised two-dimensional upgrade, and the
  notes point back explicitly.
- Video 28's Gaussian appears twice: as the channel model and as the
  family closed under affine maps (the scratch notes' bivariate-normal
  themes live here).
- If X and Y are independent, the slice never changes — one breath,
  pointing at video 39.

## Conceptual progression (drives the storyboard)
Chapter 4's ratio recalled → conditional CDF given an event, then its
derivative → interval conditioning: truncate and rescale a density →
(the race example, if time allows) → the hard question: condition on
Y = y when Pr(Y = y) = 0 → the shrinking box, Δy cancelling → the
conditional density as a renormalized slice of video 37's surface → the
circle chord worked out → averages of slices: conditional expectation,
again a random variable → the noisy channel: slice the Gaussian surface,
read off y/2 — estimation achieved → transform pairs: the Jacobian
formula → Gaussians stay Gaussian under affine maps.

## Visual opportunities
- **Truncate and rescale**: a density curve with an interval I
  highlighted; the outside fades, the inside grows uniformly until the
  area is one — the smooth version of video 22's bar animation.
- **The shrinking box**: a small Δx-by-Δy rectangle on the joint support,
  volume above it highlighted; Δy shrinks to zero and the box becomes a
  sliver of the slice at y — the Δy factors visibly cancelling in the
  formula.
- **The slice family**: video 37's surface cut by a plane at Y = y; the
  cut curve lifts out and inflates to area one; the plane then sweeps
  through other y values, the conditional reshaping as it goes.
- **Circle chord**: the disk with the horizontal line y = 0.5; the chord
  endpoints at ±sqrt(3)/2; the flat conditional density sitting on the
  chord.
- **MMSE climax**: the elliptical joint-Gaussian surface; the slice at
  the received y; its peak projecting down to x = y/2, with the line
  E[X | Y = y] = y/2 drawn through the peaks of all slices.
- **Jacobian**: a small square in the (x1, x2) plane mapping to a
  parallelogram in the (y1, y2) plane; density scaling by 1/|J| to keep
  the probability of the patch fixed.

## Notation (per project.yaml)
- Conditional densities `f_{X \mid A}(x)`, `f_{X \mid Y}(x \mid y)` — all
  conditionals with `\mid`, never a bare bar.
- Expectation `\mathrm{E}[X \mid Y = y]`; probabilities via `\Pr`.
- Jacobian determinant `|J(x_1, x_2)|`; vectors/matrices bold upright
  (`\mathbf{m}`, `\Sigma`, `A`).

## Deliberately out of scope
- Independence (`f_{X|Y} = f_X`) — one forward-looking sentence at most;
  video 39 owns it.
- Sums W = X + Y and convolution — video 40 (the channel example stops at
  estimation; it does not derive f_Y via convolution).
- The general non-invertible / many-to-one change of variables — the notes
  explicitly forgo it; we do too.
- Covariance, correlation, and the scalar five-parameter bivariate normal
  — scratch-note themes not in the shipped section.
- The full tower-property replay — video 23 owns it; here it is a callback
  only.

## Cut first (if the script runs over budget)
The race example (idea 3) drops entirely — the interval picture already
carries event conditioning. Next, the Gaussian-affine payoff (idea 9)
compresses to one spoken statement over the mean/covariance formulas,
leaving the Jacobian formula itself as the beat; the shrinking-box
justification reduces to its first and last lines.
