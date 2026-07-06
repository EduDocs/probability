---
slug: 28-uniform-gaussian
title: The Uniform and Gaussian Distributions
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/28-uniform-gaussian.tex
source_sha256: 97aed752ea5c0b160dea541368e4cd64a021b6399ffd9be0c700af4b14c4bb41
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/continuous_random_variables.tex
companion: sources/28-uniform-gaussian.md
companion_sha256: 03278c8dbecd26d8dca205580ba51bc9f97be65ef64ad47c706c28ed082efb4c
prereqs:
  - 27-pdfs-expectation
audience: undergraduate engineering, first probability course
concepts:
  - id: uniform
    name: The continuous uniform distribution
    importance: core
    one_liner: f_X = 1/(b-a) on [a, b] — equal-length intervals are equally likely; the CDF is a straight ramp.
  - id: bus-stop
    name: Worked example — waiting for the bus
    importance: core
    one_liner: Arrival uniform over a 30-minute window makes the wait uniform on [0, 30]; Pr(wait < 5) = 5/30 = 1/6 — probability as length ratio.
  - id: gaussian
    name: The Gaussian (normal) distribution
    importance: core
    one_liner: The bell curve (1/sqrt(2 pi) sigma) e^{-(x-m)^2 / 2 sigma^2} — the model for quantities built from many small random effects; m centers it, sigma sets the spread.
  - id: standardization
    name: Standardization and Phi
    importance: core
    one_liner: No closed-form CDF exists, but every Gaussian question reduces to the ONE tabulated function - F_X(x) = Phi((x - m)/sigma).
  - id: q-function
    name: The error-function family (erf, Q)
    importance: highlight
    one_liner: erf and Q are renamed, rescaled pieces of Phi — Q(x) = 1 - Phi(x) is the engineer's tail probability.
  - id: noisy-channel
    name: Worked example — a noisy channel
    importance: core
    one_liner: Send plus or minus 1 through additive Gaussian noise; by symmetry the error probability is exactly Q(1/sigma) — reliability read off a tail.
  - id: gaussian-integral
    name: Why the bell curve integrates to one
    importance: highlight
    one_liner: Square the integral, go polar, and the un-integrable e^{-x^2/2} surrenders — the classic trick; the same normalization then yields mean m and variance sigma^2.
estimated_runtime_sec: 320
---

# The Uniform and Gaussian Distributions — Concept Map

This video covers Sections 8.4.1–8.4.2 of book chapter 8 — the first two
entries of the "important distributions" catalog. Video 27 supplied the
density machinery; video 29 continues the catalog with the exponential.

## What
Two canonical densities. The **uniform** on [a, b] is the simplest:
constant density `1/(b-a)`, straight-ramp CDF, probability = length ratio.
The **Gaussian** is the most important: the bell curve with parameters m
(center) and sigma (spread), the default model for quantities shaped by
many small independent effects. Its CDF has no closed form — instead,
*standardization* reduces every Gaussian to the single tabulated function
`Phi`, with the engineer's variants erf and `Q(x) = 1 - Phi(x)`. The
noisy-channel example turns a tail probability into a bit-error rate, and
the polar-coordinates trick shows the bell curve really is a density.

## Why it matters
These two distributions bracket the continuous world: the uniform is the
"fair die" of the continuum (and the base for simulation), while the
Gaussian is the distribution the whole of statistics leans on — the
central limit theorem (later in the course) will explain its ubiquity,
but engineers meet it first as noise. The standardization idea — one
table serves every m and sigma — is the practical skill; Q(1/sigma) is
the archetype of how communication engineers measure reliability.

## Key ideas (in dependency order)
1. **Uniform.** `f_X = 1/(b-a)` on [a, b], zero elsewhere; CDF ramps
   linearly from 0 to 1. Equal lengths, equal probabilities — video 9's
   geometric models reborn as a density.
2. **Worked: the bus stop.** Wait time uniform on [0, 30] minutes;
   `Pr(T < 5) = ∫_0^5 dt/30 = 1/6`. Probability as a length ratio, done
   honestly with an integral.
3. **Gaussian.** `f_X(x) = (1/(sqrt(2 pi) sigma)) e^{-(x-m)^2/(2 sigma^2)}`;
   m slides the bell, sigma^2 widens it (three bells, one at a time).
   m = 0, sigma = 1 is the *standard* normal.
4. **Standardization.** The CDF integral has no closed form; substituting
   `v = (u - m)/sigma` gives `F_X(x) = Phi((x - m)/sigma)` — every
   Gaussian question routed through one function.
5. **The function family.** `erf` (statistics) and `Q(x) = 1 - Phi(x)`
   (engineering) are the same information re-dressed; the conversion
   formulas matter only when your software has one but not the other.
6. **Worked: the noisy channel.** X = ±1 equiprobable, Y = X + Z with Z
   Gaussian; decide by the sign of Y. Total probability + symmetry give
   `Pr(error) = Pr(Z > 1) = Q(1/sigma)` — noise level in, error rate out.
7. **The polar trick.** `(∫ f)^2` becomes a 2-D integral; polar
   coordinates produce `r e^{-r^2/2}`, which integrates in one line — so
   the bell curve has total area one. The same normalization identity,
   differentiated with respect to sigma, delivers E[X] = m and
   Var[X] = sigma^2.

## What else (connections, to seed callbacks in narration)
- The uniform echoes video 9's geometric probability (dartboard, video 27)
  and the discrete uniform of video 20's worked example.
- The noisy channel is video 12's total probability theorem plus a
  continuous tail — the first payoff marrying the two halves of the
  course.
- The Gaussian "many small effects" line plants the central limit theorem
  flag for the empirical-sums chapter.
- The polar trick returns in video 30 to evaluate Gamma(1/2) — worth a
  spoken breadcrumb here.
- Sign-based decision under noise foreshadows detection theory (Cauchy
  cameo in video 30).

## Conceptual progression (drives the storyboard)
Catalog opens: what makes a distribution "important" → the flattest
density: uniform, ramp CDF → bus-stop wait as length ratio → from flat to
bell: the Gaussian family, m and sigma on display → the CDF that will not
integrate → standardize: one curve to rule them all, Phi → erf and Q as
renamings → the channel: ±1 through noise, error = Q(1/sigma) → "but is
it even a density?" — the polar trick closes the loop.

## Visual opportunities
- **Uniform ramps**: three uniform PDFs ([0,1], [0,2], [0,4]) shown in
  sequence — taller means narrower, area pinned at one.
- **Bus window**: a 30-minute strip; the first 5 minutes shaded; the
  ratio annotated as the integral.
- **Bell family**: one bell morphing as m slides and sigma widens —
  parameters as motions, not formulas.
- **Standardization**: the shaded area under an (m, sigma) bell sliding
  and rescaling onto the standard bell — same area, new coordinates.
- **Channel**: two bells centered at -1 and +1 with the decision
  threshold at 0; the error tail shaded; symmetry mirrors one tail onto
  the other.
- **Polar trick**: the 2-D surface e^{-(u^2+v^2)/2} viewed from above;
  circular level sets invite polar coordinates; the radial integral
  collapses.

## Notation (per project.yaml)
- Gaussian parameters written m and sigma^2 (as in the notes);
  `\Phi(\cdot)` for the standard normal CDF, `Q(\cdot)` for its tail,
  `\mathrm{erf}` for the error function.

## Deliberately out of scope
- WHY sums of small effects are Gaussian — the central limit theorem
  belongs to the empirical-sums chapter; here it is one motivating
  sentence.
- The full mean/variance integration-by-parts details — the derivation is
  compressed to its two ideas (odd function vanishes; differentiate the
  normalization).
- Numerical values of Phi/Q tables.

## Cut first (if the script runs over budget)
The erf/Q conversion beat compresses to one caption ("Q(x) = 1 - Phi(x),
different fields, same curve"); the mean/variance derivation drops,
keeping only the polar normalization trick.
