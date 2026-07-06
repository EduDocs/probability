---
slug: 40-continuous-sums
title: Sums of Continuous Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/40-continuous-sums.tex
source_sha256: ef89abce190ca6564704c55877c2f10d89c6d17eb67f14322b820b3eed1a3d8b
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/random_vectors.tex
companion: sources/40-continuous-sums.md
companion_sha256: 844e4470fe388913fc5a31a5b72b6646b968aeac5a4f499cf40952e94bdf1277
prereqs:
  - 39-independence-continuous
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: convolution-def
    name: The convolution of two densities
    importance: core
    one_liner: (f_X * f_Y)(w) = integral of f_X(u) f_Y(w - u) du (equivalently f_X(w - v) f_Y(v)) — and for independent X, Y the sum W = X + Y has PDF f_W = f_X * f_Y.
  - id: cdf-proof
    name: Why convolution — the CDF derivation
    importance: core
    one_liner: F_W(w) = Pr(X + Y <= w) integrates the factored joint over the half-plane below the line u + v = w, giving int F_Y(w - u) f_X(u) du; differentiating under the integral hands back the convolution.
  - id: uniform-sum
    name: Worked example — sum of two uniforms
    importance: highlight
    one_liner: Two independent uniform[0,1] draws - f_W(w) = w on [0,1] and 2 - w on (1,2] — two rectangles convolve into a triangle.
  - id: exponential-sum
    name: Worked example — sum of two exponentials
    importance: core
    one_liner: Independent exponentials with rate lambda - f_W(w) = lambda^2 w e^{-lambda w}, the Erlang distribution with m = 2 — video 30's gallery entry, now derived.
  - id: gaussian-sum
    name: Worked example — sum of two Gaussians
    importance: core
    one_liner: Standard normals convolve, via completing the square, into f_W(w) = (1/sqrt(4 pi)) e^{-w^2/4} — Gaussian again; in general means add and variances add.
  - id: mgf-product
    name: Sums become products — the MGF shortcut
    importance: core
    one_liner: M_W(s) = E[e^{s(X+Y)}] = M_X(s) M_Y(s) for independent X, Y; the Gaussian sum redone in two lines, exponents adding to (m_1 + m_2)s + (sigma_1^2 + sigma_2^2)s^2/2.
estimated_runtime_sec: 310
---

# Sums of Continuous Random Variables — Concept Map

This video covers Section 11.3.1 of book chapter 11 (Sums of Continuous
Random Variables) and closes the chapter. It is the continuous twin of
video 25: there independent PMFs convolved by summation and the generating
function turned sums into products; here densities convolve by integration
and the MGF (video 34's tool) plays the same trick. Video 39 supplied the
independence this whole video spends; the next book chapter — empirical
sums and the limit theorems, videos 41–43 — is built directly on top of
these formulas.

## What
For independent X and Y, the density of the sum `W = X + Y` is the
**convolution** of the marginal densities:
`f_W(w) = (f_X * f_Y)(w) = int f_X(u) f_Y(w - u) du`, symmetric in the two
factors. The proof runs through the CDF — integrate the factored joint
density over the half-plane `x + y <= w`, then differentiate — and three
canonical examples run the integral: two uniforms make a triangle, two
exponentials make an Erlang, and two Gaussians make another Gaussian. The
closing shortcut is the moment generating function: independence turns the
MGF of a sum into a product, `M_W(s) = M_X(s) M_Y(s)`, which re-derives the
Gaussian sum in two lines.

## Why it matters
Sums of independent random quantities are everywhere in engineering —
accumulated noise, total service time, aggregated errors — and this
section delivers the exact distribution of a sum, not just its mean and
variance (video 24 already gave those). Each example is load-bearing:
the triangle shows convolution smoothing things out, the Erlang connects
to waiting for two arrivals, and the Gaussian's closure under addition is
the single most-used stability fact in the field. The MGF product rule is
the scalable version — and the door through which chapter 12 walks to the
law of large numbers and the central limit theorem.

## Key ideas (in dependency order)
1. **The convolution operator.**
   `(f_X * f_Y)(w) = int_{-inf}^{inf} f_X(u) f_Y(w - u) du
   = int_{-inf}^{inf} f_X(w - v) f_Y(v) dv` — for each target w, weigh
   every way to split w into u + (w - u). For independent X and Y, the
   claim: `f_W = f_X * f_Y` where `W = X + Y`. Video 25's
   `sum_k p_X(k) p_Y(n-k)` with the sum ripened into an integral.
2. **The derivation, through the CDF.**
   `F_W(w) = Pr(X + Y <= w) = int int_{v <= w - u} f_{X,Y}(u,v) dv du`;
   independence factors the joint (video 39), the inner integral becomes
   `F_Y(w - u)`, so `F_W(w) = int F_Y(w - u) f_X(u) du`. Differentiate in
   w under the integral (the fundamental theorem of calculus, used
   judiciously): `f_W(w) = int f_Y(w - u) f_X(u) du`. Claim proved.
3. **Worked: two uniforms.** `f_X = f_Y = 1` on [0,1]. The integrand
   `1_{[0,1]}(w - u)` is nonzero only for `w - 1 <= u <= w`, so the
   overlap of two unit windows gives `f_W(w) = w` on [0,1] and
   `f_W(w) = 2 - w` on (1,2], zero elsewhere — flat plus flat equals
   triangle. Two dice from video 25, gone continuous.
4. **Worked: two exponentials.** Rate lambda each; for w >= 0,
   `f_W(w) = int_0^w lambda e^{-lambda(w-u)} lambda e^{-lambda u} du
   = lambda^2 w e^{-lambda w}` — the exponentials' product is constant in
   u, so the integral just measures the interval [0, w]. This is the
   **Erlang** distribution with m = 2 (video 30): the wait for the
   *second* arrival.
5. **Worked: two Gaussians.** For standard normals, complete the square:
   `f_W(w) = (1/(2 pi)) e^{-w^2/4} int e^{-(u - w/2)^2} du
   = (1/sqrt(4 pi)) e^{-w^2/4}` — the leftover integral is a Gaussian
   density (m = w/2, sigma^2 = 1/2) integrating to one, a trick video 28
   already used. W is Gaussian with mean 0 and variance 2; in general,
   Gaussian + Gaussian is Gaussian with `m_1 + m_2` and
   `sigma_1^2 + sigma_2^2`.
6. **Sums become products — MGFs.** For independent X and Y,
   `M_W(s) = E[e^{sW}] = E[e^{sX} e^{sY}] = E[e^{sX}] E[e^{sY}]
   = M_X(s) M_Y(s)`. Rerun the Gaussian sum: multiply
   `e^{m_1 s + sigma_1^2 s^2 / 2}` by `e^{m_2 s + sigma_2^2 s^2 / 2}` and
   the exponents *add* — `M_W(s) = exp((m_1 + m_2)s +
   (sigma_1^2 + sigma_2^2) s^2 / 2)`, the general Gaussian-sum fact with
   no convolution integral in sight.

## What else (connections, to seed callbacks in narration)
- Video 25 is the discrete twin throughout: PMF convolution -> PDF
  convolution, OGF product rule -> MGF product rule; the two-dice
  triangle-ish histogram returns as an actual triangle.
- Video 39's factored joint is the one licensed step in the derivation —
  the whole video runs on last video's definition.
- Erlang (m = 2) lands on video 30's gamma-family entry; video 29's
  exponential is the summand.
- The completing-the-square move and the "a Gaussian density integrates
  to one" trick both echo video 28's bell-curve integral.
- MGFs were defined in video 34; here they earn their keep, exactly as
  the OGF did in video 25.
- Videos 41–43 (next chapter) take sums of *many* iid variables; the
  Gaussian's closure under addition is the first hint of the central
  limit theorem.

## Conceptual progression (drives the storyboard)
The chapter's last question: X + Y is a new random variable — what is its
density? → video 25's discrete convolution recalled in one shot → the
continuous claim: f_W = f_X * f_Y → why: the half-plane below the line
u + v = w, joint factored, inner integral named F_Y, one derivative →
run the integral three times: rectangles overlap into a triangle →
exponentials into the Erlang ramp-and-decay → Gaussians, square
completed, into a wider Gaussian → the shortcut: MGF of a sum is a
product of MGFs → Gaussian redone in two lines, exponents adding → sums
of many, next chapter.

## Visual opportunities
- **The flip-and-slide**: f_Y mirrored to f_Y(w - u) and dragged across
  f_X; the overlap area plotting f_W(w) point by point as w sweeps — the
  canonical convolution animation, and the video's workhorse.
- **Half-plane derivation**: the (u, v) plane with the line u + v = w and
  the region below it shaded over the joint density; the line sliding
  up-right as F_W accumulates.
- **Triangle build**: two unit rectangles sliding across each other, the
  overlap window growing then shrinking, tracing the tent function —
  next to video 25's two-dice bar chart for the twin moment.
- **Erlang**: two exponential decays in the flip-and-slide; the product
  inside [0, w] visibly flat at height lambda^2 e^{-lambda w}, so the
  overlap integral is just a widening base — the w factor made visible.
- **Gaussian stability**: two standard bells convolving into a lower,
  wider bell; variance tick marks showing 1 + 1 = 2.
- **Exponents add**: the two Gaussian MGFs side by side, their exponents
  lifting off and summing term by term into the target MGF — video 25's
  "sums become products" title card returning verbatim.

## Notation (per project.yaml)
- Convolution `(f_X \ast f_Y)(w)`; densities `f_X`, `f_Y`, `f_W`; CDFs
  `F_W`; expectation `\mathrm{E}[e^{sW}]` (the project's roman-E form);
  MGF `M_X(s)`; probabilities via `\Pr`; indicator `\mathbf{1}_{[0,1]}`.

## Deliberately out of scope
- The definition and basic properties of the MGF itself — video 34 built
  the tool; here it is only applied.
- Sums of n > 2 variables, empirical averages, and any limit theorem —
  videos 41–43 (the notes stop at pairs here too).
- The general (non-standard) Gaussian convolution by direct integral —
  the notes call it tedious and prove it by MGF instead; we follow suit.
- Erlang/gamma in general (m > 2) — video 30 owns the family; this video
  derives only the m = 2 member.
- Dependent sums — without independence neither the convolution nor the
  MGF product applies; one cautionary breath at most.

## Cut first (if the script runs over budget)
The CDF derivation (idea 2) compresses to the half-plane picture with the
first and last lines of algebra; the exponential example (idea 4) can
shrink to its flip-and-slide picture plus the boxed Erlang answer, keeping
the uniform triangle and the Gaussian/MGF pair as the full-length beats.
