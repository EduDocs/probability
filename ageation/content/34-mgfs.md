---
slug: 34-mgfs
title: Moment Generating Functions
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/34-mgfs.tex
source_sha256: ed51482cf6eb97cf3db7069cb4b2b7be472baea9b4a953de39f301327a986252
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/expectations_and_bounds.tex
companion: sources/34-mgfs.md
companion_sha256: e034200c86458961206f714159e3abfba75bddd45e4e1c74f4980f14a60bd496
prereqs:
  - 33-generating-rvs
audience: undergraduate engineering, first probability course
concepts:
  - id: mgf-definition
    name: The moment generating function
    importance: core
    one_liner: M_X(s) = E[e^{sX}] — one expectation with a dial s; for continuous X it is the integral of f_X(x) e^{sx}, a variant of the Laplace transform.
  - id: moments-by-differentiation
    name: Moments by differentiation
    importance: core
    one_liner: Differentiate n times, set s = 0 — out comes E[X^n]; the first derivative is the mean, the second is the second moment.
  - id: exponential-mgf
    name: Worked example — the exponential
    importance: core
    one_liner: M_X(s) = lambda / (lambda - s) — one easy integral, then EVERY moment n!/lambda^n falls out by differentiation; variance 1/lambda^2 for free.
  - id: ogf-bridge
    name: The OGF connection
    importance: core
    one_liner: For integer-valued X, M_X(s) = G_X(e^s) — video 25's generating function and the MGF are the same machine in different coordinates.
  - id: discrete-uniform-mgf
    name: Worked example — the discrete uniform
    importance: optional        # the notes call it contrived; cut first
    one_liner: M_U(s) = e^s(e^{ns} - 1) / (n(e^s - 1)); two rounds of l'Hopital at s = 0 recover E[U] = (n+1)/2 without knowing any special sums.
  - id: gaussian-mgf
    name: Worked example — the standard normal
    importance: highlight
    one_liner: Complete the square inside the integral and a Gaussian PDF appears — the leftover factor IS the answer, M_X(s) = e^{s^2/2}.
  - id: affine-property
    name: Affine transformations, and the general Gaussian
    importance: core
    one_liner: M_{aX+b}(s) = e^{sb} M_X(as); applied to Y = sigma X + m it gives e^{sm + s^2 sigma^2 / 2}, whose derivatives confirm mean m and variance sigma^2.
estimated_runtime_sec: 310
---

# Moment Generating Functions — Concept Map

This video covers the first section of book chapter 10 (Expectations and
Bounds). Video 33 closed the derived-distributions chapter; videos 35–36
spend this chapter's remaining sections turning expectations into bounds —
and the Chernoff bound in video 36 will run on the MGF built here.

## What
The **moment generating function** of a random variable is
`M_X(s) = E[e^{sX}]` — for continuous X, the integral of `f_X(x) e^{sx}`,
which the experienced reader recognizes as a variant of the Laplace
transform. Its name is earned: differentiate n times and evaluate at
`s = 0`, and the n-th moment `E[X^n]` appears. The definition works for
discrete variables too, and for integer-valued X it ties directly to
video 25's ordinary generating function via `M_X(s) = G_X(e^s)`. Three
worked transforms anchor the section: the exponential
(`lambda/(lambda - s)`), the discrete uniform, and — the jewel — the
standard normal (`e^{s^2/2}`), extended to any Gaussian by the affine rule
`M_{aX+b}(s) = e^{sb} M_X(as)`.

## Why it matters
Video 20 computed moments one integral (or sum) at a time; the MGF packages
*all* of them into a single function — compute one transform, then
differentiate instead of integrating, forever after. This is the same
transform-domain bargain engineers strike with the Laplace transform in
circuits and signals. And beyond moments, the MGF is this chapter's
load-bearing tool: the Chernoff bound (video 36) is built directly on
`E[e^{sX}]`, so this video is where that machinery gets forged.

## Key ideas (in dependency order)
1. **Definition.** `M_X(s) = E[e^{sX}]`; for continuous X,
   `M_X(s) = \int_{-\infty}^{\infty} f_X(x) e^{sx} dx` — expectation of an
   exponential probe, one number per value of the dial s. A variant of the
   Laplace transform.
2. **Moments by differentiation.** When M_X exists on an open interval
   around 0, `d^n/ds^n M_X(s)|_{s=0} = E[X^n e^{sX}]|_{s=0} = E[X^n]`:
   the derivative slips inside the expectation, each pass pulls down one
   factor of X, and s = 0 erases the exponential. In particular
   `M_X'(0) = E[X]` and `M_X''(0) = E[X^2]`.
3. **Worked: the exponential.** `M_X(s) = \int_0^\infty lambda
   e^{-(lambda - s)x} dx = lambda/(lambda - s)`. Then
   `E[X] = lambda/(lambda - s)^2 |_{s=0} = 1/lambda`, and in general
   `E[X^n] = n! lambda/(lambda - s)^{n+1} |_{s=0} = n!/lambda^n` — every
   moment from one integral; video 20's two-moment formula gives
   `Var[X] = 1/lambda^2`.
4. **The OGF bridge.** For integer-valued X,
   `M_X(s) = sum_k e^{sk} p_X(k) = G_X(e^s)` — the MGF is video 25's
   generating function with `z = e^s`; discrete and continuous now share
   one transform language.
5. **Worked: the discrete uniform (optional).** `M_U(s) =
   e^s(e^{ns} - 1)/(n(e^s - 1))`; differentiating and applying l'Hopital's
   rule twice yields `E[U] = (n+1)/2`, and similar steps give
   `E[U^2] = (n+1)(2n+1)/6`, hence `Var[U] = (n^2 - 1)/12`. Contrived, the
   notes admit — but it needs no special sums (video 20 needed them).
6. **Worked: the standard normal.** Merge `e^{sx}` into the Gaussian
   exponent, complete the square: the integrand becomes a Gaussian PDF
   centered at s, which integrates to one, leaving `M_X(s) = e^{s^2/2}` —
   the simplest MGF in the catalog.
7. **Affine rule, general Gaussian.** `M_Y(s) = E[e^{s(aX+b)}] =
   e^{sb} M_X(as)`. With `Y = sigma X + m` (affine in a Gaussian is
   Gaussian, video 31/32 territory): `M_Y(s) = e^{sm + s^2 sigma^2/2}`;
   its first two derivatives at 0 return `E[Y] = m` and
   `E[Y^2] = sigma^2 + m^2` — mean m, variance sigma^2, as anticipated.

## What else (connections, to seed callbacks in narration)
- Video 25 introduced the OGF for discrete variables and the
  "sums become products" magic; the MGF is its continuous sibling, and
  `M_X(s) = G_X(e^s)` makes the kinship literal.
- Video 20 defined the n-th moment and built the variance from the first
  two moments — both formulas return here as derivative read-outs.
- The exponential density (video 29) and the Gaussian (video 28) supply
  the worked examples; the completing-the-square move echoes video 28's
  handling of the bell curve.
- Laplace transforms from circuits/signals courses: same integral, same
  transform-domain payoff — worth one spoken breath for engineers.
- Forward flag: video 36 bounds `Pr(X >= a)` by `e^{-sa} M_X(s)` — "keep
  this function in your pocket."

## Conceptual progression (drives the storyboard)
Expectation recapped as a summary → probe the distribution with e^{sX}:
a function of the dial s → differentiate under the expectation, set s = 0,
a moment pops out → the exponential worked end-to-end: one integral, all
moments → integer-valued case: the MGF is the OGF at z = e^s →
(optionally) the discrete uniform via l'Hopital → the standard normal:
complete the square, a Gaussian hides inside the integral → the affine
rule lifts it to every Gaussian → mean m and variance sigma^2 confirmed —
the transform knows everything.

## Visual opportunities
- **The probe**: a density f_X with the weight e^{sx} overlaid; as s
  increases from 0, the weight tilts rightward and the product curve
  shifts its mass — M_X(s) plotted point by point as the area.
- **Moment extraction**: the graph of M_X(s) for the exponential; a
  tangent line at s = 0 whose slope detaches and lands as E[X] = 1/lambda;
  repeat with curvature for the second moment.
- **Derivative cascade**: `d^n/ds^n e^{sX}` pulling down one X per
  differentiation — the factors X, X^2, X^3 accumulating in front of the
  exponential, then s = 0 fading the exponential to 1.
- **Completing the square**: the Gaussian integrand's exponent rearranged
  term by term; the shifted bell slides to center s, its area locks to 1,
  and the freed factor e^{s^2/2} floats out front — the visual climax.
- **OGF bridge**: video 25's `G_X(z)` card returning; `z = e^s` morphing
  it into `M_X(s)`.

## Notation (per project.yaml)
- Expectation `\mathrm{E}`; variance `\mathrm{Var}`; probability `\Pr`.
- MGF `M_X(s)`; OGF `G_X(z)`; densities `f_X`, PMFs `p_X`; rate `\lambda`,
  Gaussian parameters `m, \sigma^2`.

## Deliberately out of scope
- All bounding material — dominating functions, Markov, Chebyshev
  (video 35), Chernoff, Jensen (video 36).
- Uniqueness/inversion of the MGF (mentioned in the companion notes, not
  developed in the chapter) — at most one spoken aside.
- Sums of independent variables becoming MGF products — flagged as the
  OGF inheritance in one breath, but the formal continuous treatment
  belongs to book chapter 11 (videos 37–40).

## Cut first (if the script runs over budget)
The discrete-uniform example drops entirely (the notes themselves call it
contrived); next, the affine-rule derivation compresses to the boxed
result `M_Y(s) = e^{sb} M_X(as)` applied to the Gaussian in one step.
