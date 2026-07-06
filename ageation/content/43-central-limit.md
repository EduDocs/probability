---
slug: 43-central-limit
title: The Central Limit Theorem
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-04
source: sources/43-central-limit.tex
source_sha256: c13bf4618eb4bbe38d3a7468994a46bd69e62bf1753311394259509f2466e2c5
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/empirical_sums.tex
companion: sources/43-central-limit.md
companion_sha256: 51341fb22e74140f95766dd58eb5134122f48455900bc4f5c1726b03d683b956
prereqs:
  - 42-law-large-numbers
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: clt-statement
    name: The central limit theorem
    importance: core
    one_liner: For iid X_i with mean E[X] and variance sigma^2, (S_n - nE[X])/(sigma sqrt(n)) converges in distribution to a standard normal — Pr(... <= x) -> integral of the standard Gaussian density.
  - id: gaussian-case-exact
    name: The Gaussian case was exact
    importance: core
    one_liner: Video 41's invariant sequence — for Gaussian inputs the standardized sum is EXACTLY normal for every n; the CLT says every finite-variance input reaches that same shape in the limit.
  - id: log-mgf-tools
    name: The log-moment generating function
    importance: core
    one_liner: Lambda_X(s) = log M_X(s) with Lambda(0) = 0, Lambda'(0) = E[X] = 0, Lambda''(0) = E[X^2] = 1 — three numbers that pin the curve near the origin.
  - id: sums-become-products
    name: Independence turns the sum into n copies
    importance: core
    one_liner: log E[e^{s S_n / sqrt(n)}] = n Lambda_X(s n^{-1/2}) — expectations of products of independent factors split, so one function of one variable controls the whole sum.
  - id: limit-is-gaussian
    name: The limit is the Gaussian's MGF
    importance: highlight
    one_liner: L'Hopital twice gives n Lambda_X(s n^{-1/2}) -> s^2/2, so the MGF converges pointwise to e^{s^2/2} — the standard normal's; pointwise MGF convergence implies convergence in distribution (quoted).
  - id: normal-approximation
    name: The normal approximation
    importance: core
    one_liner: For large n, F_{S_n}(x) ≈ Phi((x - nE[X])/(sigma sqrt(n))) — the CLT as an everyday computational tool.
estimated_runtime_sec: 310
---

# The Central Limit Theorem — Concept Map

This video covers Section 12.3 of book chapter 12, together with its
Normal Approximation subsection. It is the final video of the course:
video 41 defined convergence in distribution, video 42 showed the
average settling onto the mean — this video reveals the shape of what is
left, and closes the 43-video series where video 28's bell curve
promised it would end.

## What
The **central limit theorem**: for iid `X_1, X_2, ...` with mean `E[X]`
and variance `sigma^2`, the standardized sum
`(S_n - nE[X]) / (sigma sqrt(n))` converges *in distribution* to a
standard normal — for every x,
`Pr((S_n - nE[X])/(sigma sqrt(n)) <= x) -> integral_{-inf}^x
(1/sqrt(2 pi)) e^{-u^2/2} du`. The proof runs through the log-moment
generating function: independence turns the sum's log-MGF into
`n Lambda_X(s n^{-1/2})`, and two applications of L'Hopital's rule send
that to `s^2/2` — the log-MGF of the standard normal. The practical
payoff is the **normal approximation**:
`F_{S_n}(x) ≈ Phi((x - nE[X])/(sigma sqrt(n)))` for large n.

## Why it matters
This is the payoff of the whole course — the theorem that partly
explains why Gaussians are everywhere. Video 28 introduced the bell
curve as the model for "many small independent effects" and promised the
justification later; this is later. The individual distribution of the
`X_i` is *forgotten* in the limit: only the mean and variance survive,
and the shape is always the same bell. That universality is what lets
engineers model noise, aggregate errors, and large sums they know almost
nothing about — and the normal approximation turns the statement into a
tool: one table of `Phi` serves every large sum with finite variance.

## Key ideas (in dependency order)
1. **The statement.** For iid `X_i` with mean `E[X]` and variance
   `sigma^2`, `(S_n - nE[X])/(sigma sqrt(n))` converges in distribution
   (video 41's third notion) to a standard normal:
   `lim_{n -> inf} Pr((S_n - nE[X])/(sigma sqrt(n)) <= x) =
   integral_{-inf}^x (1/sqrt(2 pi)) e^{-u^2/2} du`.
2. **The Gaussian case was exact.** Video 41's second sequence showed
   this scaling holds *exactly* at every n when the inputs are Gaussian
   — mean 0, variance `sigma^2`, never moving. The theorem's claim is
   that every finite-variance input flows to that same shape.
3. **The tool: the log-MGF.** Assume `E[X] = 0`, `sigma^2 = 1` (proper
   scaling recovers the general case), and that `M_X` exists and is
   finite. `Lambda_X(s) = log M_X(s) = log E[e^{sX}]`; differentiating
   and evaluating at zero: `Lambda_X(0) = 0`,
   `Lambda_X'(0) = E[X] = 0`, `Lambda_X''(0) = E[X^2] = 1`.
4. **Sums become products.** By independence, the expectation of the
   product factors:
   `log E[e^{s S_n / sqrt(n)}] = log(M_X(s/sqrt(n)) ... M_X(s/sqrt(n)))
   = n Lambda_X(s n^{-1/2})` — the whole sum compressed into n copies
   of one function, sampled ever closer to the origin.
5. **The limit.** Two rounds of L'Hopital's rule on
   `Lambda_X(s n^{-1/2}) / n^{-1}` peel off the derivatives until
   `Lambda_X''(0) = 1` is exposed: the limit is `s^2/2`. So the MGF of
   `S_n/sqrt(n)` converges pointwise to `e^{s^2/2}` — precisely the
   standard normal's MGF. That pointwise MGF convergence implies
   convergence in distribution is a sophisticated result the notes (and
   we) quote without proof.
6. **The normal approximation.** For large n,
   `F_{S_n}(x) = Pr(S_n <= x) = Pr((S_n - nE[X])/(sigma sqrt(n)) <=
   (x - nE[X])/(sigma sqrt(n))) ≈ Phi((x - nE[X])/(sigma sqrt(n)))`,
   where `Phi` is the standard normal CDF — the CDF of any large iid
   sum, estimated by standardize-and-look-up.

## What else (connections, to seed callbacks in narration)
- Video 28's Gaussian was sold on the "sum of many small effects" story
  — the promise is finally kept, and the course ends where that video
  pointed.
- MGFs are video 34's; "sums become products" is video 25's generating-
  function move, now with `e^{sX}` instead of `z^X` — third time the
  transform trick pays off.
- Convergence in distribution is video 41's definition, and this limit
  joins the family of video 29's geometric-to-exponential and video
  16's binomial-to-Poisson — the grandest of the three.
- Video 42's law of large numbers is the companion statement: divide by
  n and the fluctuations die; divide by `sqrt(n)` and they *stabilize*
  into a bell. Two scalings, two theorems, one sum.
- Video 40 computed exact densities of sums by convolution — the CLT is
  the reason those convolutions kept looking more and more Gaussian.

## Conceptual progression (drives the storyboard)
Video 42 left `S_n/n` collapsing to a point — zoom in by `sqrt(n)`
instead: what shape are the fluctuations? → the Gaussian case answers
exactly (video 41's invariant bell recalled) → the theorem: EVERY
finite-variance iid input, standardized, flows to the standard normal →
the proof idea: watch the MGF, not the density → Lambda's three values
at the origin → independence: n factors, one function →
L'Hopital twice, `s^2/2` emerges → the bell is the only possible limit →
the normal approximation: standardize, look up `Phi` → the arrival: the
course's founding promise (video 28) redeemed — mean, variance, and the
bell are all a large sum remembers.

## Visual opportunities
- **Two scalings side-by-side in time**: the `S_n/n` squeeze (video
  42's animation recalled) followed by the `(S_n - nE[X])/(sigma
  sqrt(n))` sequence holding a fixed bell — divide-by-n kills the
  story, divide-by-sqrt(n) reveals it.
- **The shape-forgetting**: a standardized-sum density drawn for n = 1,
  2, 8, 32 starting from a decidedly non-Gaussian density (video 40's
  convolution pictures reprised), each curve visibly nearer the bell —
  the theorem as an animation, the video's centerpiece.
- **MGF convergence**: the curves `n Lambda_X(s n^{-1/2})` settling
  onto the parabola `s^2/2` — convergence happening in transform space,
  a parabola as the fingerprint of the bell.
- **L'Hopital cascade**: the limit computation compressed to its
  skeleton — each application of the rule peeling one derivative, until
  `Lambda''(0) = 1` is exposed and `s^2/2` drops out.
- **Normal approximation**: a discrete-sum CDF staircase overlaid by
  the smooth `Phi((x - nE[X])/(sigma sqrt(n)))` ramp; a probability
  read off as an area under the standard bell.
- **The finale card**: the standard normal density alone on screen —
  the destination of the whole series.

## Notation (per project.yaml)
- Probabilities `\Pr`, expectation `\mathrm{E}`, variance `\mathrm{Var}`;
  standardized sum `\frac{S_n - n\mathrm{E}[X]}{\sigma\sqrt{n}}`; MGF
  `M_X(s)`, log-MGF `\Lambda_X(s)`; standard normal CDF `\Phi(\cdot)`.

## Deliberately out of scope
- The rigorous proof that pointwise MGF convergence implies convergence
  in distribution — quoted, not proved, exactly as in the notes.
- The general-mean/general-variance bookkeeping — the notes wave it
  through by "proper scaling"; we do the same in one sentence.
- Rates of convergence and continuity corrections — not in the notes.
- The law of large numbers and heavy-tailed failures — video 42's
  territory; here they appear only as the recalled contrast.
- The Hoeffding bound (commented out of the chapter) stays out.

## Cut first (if the script runs over budget)
The L'Hopital computation compresses to its first and last lines around
the animation (the two-rule cascade spoken, not written); the
gaussian-case-exact beat folds into the statement beat as one recalled
picture. The normal approximation and the finale stay.
