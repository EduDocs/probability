---
slug: 30-additional-distributions
title: A Gallery of Densities
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/30-additional-distributions.tex
source_sha256: 97aed752ea5c0b160dea541368e4cd64a021b6399ffd9be0c700af4b14c4bb41
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/continuous_random_variables.tex
companion: sources/30-additional-distributions.md
companion_sha256: 03278c8dbecd26d8dca205580ba51bc9f97be65ef64ad47c706c28ed082efb4c
prereqs:
  - 29-exponential
audience: undergraduate engineering, first probability course
concepts:
  - id: gamma
    name: The gamma distribution and the gamma function
    importance: core
    one_liner: f_X = lambda (lambda x)^{alpha-1} e^{-lambda x} / Gamma(alpha) — a two-parameter family flexible enough to fit a wide range of data; Gamma generalizes the factorial.
  - id: gamma-function
    name: The gamma function's key values
    importance: highlight
    one_liner: Gamma(z+1) = z Gamma(z), Gamma(k+1) = k!, and Gamma(1/2) = sqrt(pi) — the last one by the same polar trick that integrated the bell curve.
  - id: special-cases
    name: Exponential, chi-square, Erlang — one family
    importance: core
    one_liner: alpha = 1 is the exponential; lambda = 1/2, alpha = k/2 is chi-square (sums of squared normals); integer alpha = m is Erlang — the time of the m-th arrival.
  - id: rayleigh
    name: The Rayleigh distribution
    importance: core
    one_liner: The length of a 2-D Gaussian vector — sqrt(X^2 + Y^2) for independent normals; the fading model of wireless links; its sigma^2 names the Gaussians inside, not its own variance.
  - id: laplace
    name: The Laplace distribution
    importance: highlight
    one_liner: An exponential and its mirror image spliced at zero — the law of the DIFFERENCE of two iid exponentials.
  - id: cauchy
    name: The Cauchy distribution
    importance: core
    one_liner: gamma / (pi (gamma^2 + x^2)) — tails so heavy that the mean is undefined, and averaging n Cauchys changes nothing; the cautionary tale of the gallery.
estimated_runtime_sec: 310
---

# A Gallery of Densities — Concept Map

This video covers Section 8.5 of book chapter 8 and closes both the
chapter and the five-video arc: the machinery (26–27), the triad (28–29),
and now the wider family — with the running theme that new distributions
are built FROM old ones.

## What
Four more named densities, each defined by a construction rather than a
formula alone. The **gamma** family — powered by the gamma function, the
factorial's continuous extension — contains the exponential (alpha = 1),
the **chi-square** (sums of squared standard normals), and the **Erlang**
(sums of iid exponentials: the time of the m-th arrival). The
**Rayleigh** is the length of a two-dimensional Gaussian vector — the
wireless-fading distribution. The **Laplace** splices an exponential with
its mirror image (the difference of two iid exponentials), and the
**Cauchy** brings the warning: tails so heavy that no mean exists, and
sample averaging accomplishes nothing.

## Why it matters
The gallery teaches the meta-lesson of distribution theory: named
densities are not arbitrary curves but *records of constructions* — sum
exponentials, square normals, take a vector's length, subtract two waits
— and knowing the construction is knowing when to reach for the model.
The Cauchy earns its place as the counterexample every engineer needs
once: not every distribution has a mean, and averaging is not a universal
cure.

## Key ideas (in dependency order)
1. **The gamma function.** `Gamma(z) = ∫_0^inf u^{z-1} e^{-u} du`;
   `Gamma(z+1) = z Gamma(z)` (integration by parts), so
   `Gamma(k+1) = k!` — the factorial, extended off the integers.
   `Gamma(1/2) = sqrt(pi)` by the polar trick from video 28.
2. **The gamma distribution.** `f_X(x) = lambda (lambda x)^{alpha-1}
   e^{-lambda x} / Gamma(alpha)`, x > 0 — shape alpha and rate lambda
   sweep a family that fits data from steep decay to bell-ish humps.
3. **Special cases.** alpha = 1: the exponential (video 29's star).
   lambda = 1/2, alpha = k/2: chi-square with k degrees of freedom — the
   distribution of a sum of k squared standard normals, the workhorse of
   statistical inference. alpha = m integer: Erlang — the sum of m iid
   exponentials, i.e., the time of the m-th arrival at video 29's server.
4. **Rayleigh.** `f_R(r) = (r/sigma^2) e^{-r^2/(2 sigma^2)}`, r >= 0 —
   the norm sqrt(X^2 + Y^2) of two independent zero-mean Gaussians; the
   amplitude-fading model in urban radio. Mean `sqrt(2 pi) sigma / 2`,
   second moment `2 sigma^2`; the parameter sigma^2 honors the Gaussians
   inside, NOT the Rayleigh's own variance (which is (4 - pi) sigma^2/2)
   — a naming trap worth one clear sentence. R^2 is exponential.
5. **Laplace.** `f_X(x) = e^{-|x|/b} / (2b)` — a double exponential; the
   law of the difference of two iid exponentials. Symmetric, but sharper
   at the peak and heavier in the tails than a Gaussian.
6. **Cauchy.** `f_X(x) = gamma / (pi (gamma^2 + x^2))` — heavy tails: no
   mean, no variance, no higher moments. The sample mean of n iid Cauchys
   is Cauchy with the SAME parameter: averaging does not concentrate.
   Physics calls it Lorentz; detection theory uses it for extreme noise.

## What else (connections, to seed callbacks in narration)
- Gamma(1/2) = sqrt(pi) reuses video 28's polar trick — an explicit
  callback ("the bell curve's trick, second encore").
- Erlang = summed exponentials extends video 25's sums-of-variables
  theme into continuous time, and completes video 29's arrival story
  (m-th arrival, not just the first).
- Chi-square squares video 28's normals; Rayleigh takes their 2-D norm —
  three constructions from one bell curve.
- The Cauchy's failed averaging is the anti-example that sharpens the
  law-of-large-numbers story in the empirical-sums chapter to come.
- Laplace's splice recalls video 29's exponential shape, mirrored.

## Conceptual progression (drives the storyboard)
The theme declared: distributions are built, not decreed → the factorial
extended: Gamma, its recursion, Gamma(1/2) via the polar encore → the
gamma density as a two-parameter dial → three settings of the dial:
exponential, chi-square, Erlang — each with its construction → sideways
to constructions on the Gaussian: Rayleigh as vector length (and its
naming trap) → Laplace as spliced exponentials → the finale and the
warning: Cauchy, where the mean fails and averages refuse to settle →
gallery recap: every curve tagged with its construction.

## Visual opportunities
- **The dial**: one gamma density morphing as (alpha, lambda) moves —
  exponential to chi-square to Erlang, each pausing with its label.
- **Erlang stacking**: video 22/29's dot stream; the waits to the 1st,
  2nd, ..., m-th dot bracketed and summed — the density humping rightward
  as m grows.
- **Rayleigh construction**: a 2-D scatter of Gaussian points; one point's
  radius drawn; the histogram of radii settling onto the Rayleigh curve.
- **Laplace splice**: an exponential density flipped across zero and
  glued, with the seam at the peak.
- **Cauchy vs Gaussian tails**: both curves in sequence with a log-scale
  tail comparison; then running sample means — the Gaussian's settling,
  the Cauchy's refusing (jittering line that never converges).
- **Gallery wall**: closing card with the five curves as thumbnails,
  each captioned by its construction.

## Notation (per project.yaml)
- `\Gamma(\cdot)` for the gamma function; parameters alpha, lambda, b,
  gamma as in the notes; expectations/variances via the _style helpers.

## Deliberately out of scope
- The full Gamma(1/2) change-of-variables computation — stated with the
  polar-encore picture, not re-derived line by line.
- The Rayleigh mean/variance integration-by-parts details — results
  stated, one-line why.
- Proof that the Cauchy sample mean is Cauchy (needs transform tools the
  course does not have yet) — asserted as the punchline fact.

## Cut first (if the script runs over budget)
The Laplace beat compresses to one sentence + the splice picture inside
the gallery recap; the Rayleigh mean/variance numbers drop (keep the
construction and the naming trap).
