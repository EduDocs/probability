---
slug: 31-derived-cdf-method
title: Derived Distributions — the CDF Method
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/31-derived-cdf-method.tex
source_sha256: 7c91a09f784bbdf3d5af3f1433210909e87bc606c7686af4e399619680d116bc
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/derived_distributions.tex
companion: sources/31-derived-cdf-method.md
companion_sha256: af8623dfc2346b019e3e5f41f532c43d3eb0800478e576aef14c19a60a613439
prereqs:
  - 30-additional-distributions
audience: undergraduate engineering, first probability course
concepts:
  - id: function-of-continuous-rv
    name: A function of a continuous random variable
    importance: core
    one_liner: Y = g(X) is itself a random variable — the same two-hop picture as the discrete case (video 17), Omega to X to Y, now with a continuum in the middle.
  - id: preimage-probability
    name: Probabilities travel through preimages
    importance: core
    one_liner: Pr(Y in S) = Pr(X in g^{-1}(S)) = the integral of f_X over the preimage — no masses to regroup, so events do the work.
  - id: cdf-method
    name: The CDF method
    importance: core
    one_liner: F_Y(y) = Pr(g(X) <= y) — describe the event {g(X) <= y} as a set of x-values, integrate f_X over it, and the derived CDF falls out.
  - id: rayleigh-squared
    name: Worked example — a Rayleigh, squared
    importance: highlight
    one_liner: X Rayleigh with sigma^2 = 1, Y = X^2 - F_Y(y) = 1 - e^{-y/2}; the square of a Rayleigh is exponential — video 30's claim, now proved.
  - id: shape-not-guaranteed
    name: Y need not be continuous
    importance: optional        # one-sentence beat; cut first if over budget
    one_liner: Continuity of X promises nothing about Y = g(X) — it can be continuous, discrete, or neither, which is why we study structured cases.
  - id: monotone-sup
    name: Monotone functions — the supremum formula
    importance: core
    one_liner: For non-decreasing g, F_Y(y) = F_X(sup{g^{-1}((-inf, y])}) — the sup absorbs flat stretches (many preimages) and jumps (empty ones).
  - id: uniform-doubled
    name: Worked example — doubling a uniform
    importance: core
    one_liner: X uniform on [0,1], Y = 2X - F_Y(y) = y/2 on [0,2], f_Y = 1/2; an affine function of a uniform is uniform.
  - id: decreasing-mirror
    name: The decreasing mirror
    importance: core
    one_liner: For monotone decreasing g, F_Y(y) = 1 - F_X(inf{g^{-1}((-inf, y])}) — same argument, order reversed.
estimated_runtime_sec: 310
---

# Derived Distributions — the CDF Method — Concept Map

This video covers the opening of book chapter 9 ("Functions and Derived
Distributions") plus Section 9.1, Monotone Functions. It is the continuous
mirror of video 17, where functions of *discrete* random variables were
handled by regrouping PMF masses; with a continuum there are no masses to
regroup, so the CDF machinery of videos 26–27 takes over. Video 32
differentiates today's CDFs into a density formula; video 33 turns the whole
apparatus into a sampling algorithm.

## What
Applying a real-valued function g to a continuous random variable X yields a
new random variable Y = g(X), and its distribution must be *derived* from
the distribution of X. The master move is to push every question about Y
back through the preimage: `Pr(Y in S) = Pr(X in g^{-1}(S)) =
int_{g^{-1}(S)} f_X(u) du`. In particular the CDF of Y is
`F_Y(y) = Pr(g(X) <= y)` — integrate f_X over the set of x-values where
`g(x) <= y`. When g is monotone that set is a half-line, and the derived CDF
has a closed form: `F_X(sup{g^{-1}((-inf, y])})` for non-decreasing g,
`1 - F_X(inf{...})` for decreasing g.

## Why it matters
Engineering constantly transforms signals: amplitudes get squared into
energies, voltages get scaled and shifted, phases get passed through
nonlinearities. Each transform drags the distribution along, and the CDF
method is the *universal* tool — it needs nothing from g beyond the ability
to describe the event `{g(x) <= y}`. It also settles a promissory note: video
30 stated that the squared magnitude of a Rayleigh fade is exponential; this
video proves it in four lines. And it sets up video 32, where differentiating
today's answer produces the change-of-variables formula.

## Key ideas (in dependency order)
1. **Y = g(X) is a random variable.** The two-arrow picture from the notes:
   omega in Omega maps to X(omega) on one real line, then g carries it to a
   second real line. The composite arrow is Y — exactly video 17's diagram
   with a continuous middle.
2. **Preimages carry the probability.** For a set S,
   `Pr(Y in S) = Pr(g(X) in S) = Pr(X in g^{-1}(S)) = int_{g^{-1}(S)} f_X(u) du`,
   where `g^{-1}(S) = {u | g(u) in S}` is the preimage (video 2's image /
   preimage vocabulary, finally load-bearing).
3. **The CDF method.** Specialize S to `(-inf, y]`:
   `F_Y(y) = Pr(g(X) <= y) = int_{{u | g(u) <= y}} f_X(u) du`. Every derived
   distribution in this chapter starts here.
4. **Worked: Rayleigh squared.** X Rayleigh with sigma^2 = 1
   (`f_X(u) = u e^{-u^2/2}`, u >= 0), Y = X^2. For y > 0,
   `F_Y(y) = Pr(-sqrt(y) <= X <= sqrt(y)) = int_0^{sqrt(y)} u e^{-u^2/2} du
   = 1 - e^{-y/2}` (substitute v = u^2; the lower limit is 0 because X >= 0).
   That is the exponential CDF from videos 26 and 29 — the square of a
   Rayleigh is exponential.
5. **No structural guarantee.** X continuous does not make Y = g(X)
   continuous — Y can be continuous, discrete, or neither. Hence the
   strategy: study structured cases, starting with monotone g.
6. **Monotone functions.** g is monotone increasing if `x_1 <= x_2` implies
   `g(x_1) <= g(x_2)` (decreasing: reversed; strict versions with < and >).
   For non-decreasing g, the event `{g(X) <= y}` is a half-line, and
   `F_Y(y) = F_X(sup{g^{-1}((-inf, y])})`. The supremum is doing real work:
   a flat stretch of g means g^{-1}(y) holds many points, and a jump of g
   means g^{-1}(y) can be empty — taking the sup of the *preimage of the
   half-line* handles both.
7. **Worked: doubling a uniform.** X uniform on [0,1], Y = 2X. For y in
   [0,2], `F_Y(y) = Pr(X <= y/2) = y/2`, so `f_Y(y) = 1/2` on [0,2]:
   uniform on [0,2]. More generally, an affine function of a uniform random
   variable is uniform.
8. **The decreasing mirror.** For monotone decreasing g,
   `F_Y(y) = Pr(X >= inf{g^{-1}((-inf, y])}) = 1 - F_X(inf{g^{-1}((-inf, y])})`
   — the same argument with sup traded for inf and F for 1 - F.

## What else (connections, to seed callbacks in narration)
- Video 17 solved this exact problem for discrete X by summing PMF masses
  over preimages — same picture, sums replaced by integrals.
- Videos 26–27 built everything used here: CDFs, densities, and
  interval-probabilities-as-differences.
- Video 30 introduced the Rayleigh as a fading amplitude and *stated* that
  its square is exponential; idea 4 is the proof.
- The preimage `g^{-1}(S)` is video 2's set-theoretic preimage, returning
  after twenty-nine videos.
- The uniform example quietly previews video 33, where uniforms become the
  raw material for generating everything else.

## Conceptual progression (drives the storyboard)
Video 17's two-line diagram recalled → the middle line becomes a continuum:
no masses to regroup → probability must flow through preimages → specialize
to {g(X) <= y}: the CDF method → Rayleigh squared worked start to finish,
stamped "exponential" (video 30's debt paid) → a caution: Y can be anything
→ restrict to monotone g: the preimage of a half-line is a half-line → the
sup formula, with flats and jumps as the reason for the sup → doubling a
uniform: the gentlest instance → the decreasing mirror in one breath.

## Visual opportunities
- **Two-hop diagram**: the notes' figure animated — Omega blob, dashed arcs
  to the X line, second arcs to the Y line, then the composite arrows drawn
  straight through.
- **Preimage shading**: a plot of g with a horizontal threshold at y; the
  region of the x-axis where the curve sits at or below the threshold lights
  up, and the area of f_X over that lit region fills a bar labelled F_Y(y).
  Slide y upward and watch both grow.
- **Rayleigh squared**: the Rayleigh density with [0, sqrt(y)] shaded; a
  y-slider drags sqrt(y) and traces F_Y(y) point by point until the curve is
  recognized as 1 - e^{-y/2} and labelled with video 29's exponential.
- **The sup at work**: a monotone g with one plateau and one jump (the
  notes' pair of figures); as y sweeps upward, the sup point glides along
  the x-axis, racing across the plateau's preimage and freezing during the
  jump.
- **Uniform stretch**: the height-1 density on [0,1] stretched horizontally
  to [0,2] while its height drops to 1/2 — area visibly conserved.

## Notation (per project.yaml)
- Probabilities via `\Pr`; CDFs `F_X, F_Y`; densities `f_X, f_Y`.
- Preimage `g^{-1}(S)`; set-builder with `\mid`, never a bare bar in
  rendered math; `\sup` and `\inf` as operators.

## Deliberately out of scope
- Differentiating F_Y to get f_Y — the change-of-variables formula
  `f_X(x)/|dg/dx|` and everything downstream of it is video 32.
- The sum-over-roots formula for non-monotone g — video 32.
- Redoing the Rayleigh example via densities (the notes' "Channel Fading
  and Energy") — that comparison belongs to video 32.
- Generating random variables from uniforms — video 33.

## Cut first (if the script runs over budget)
The shape-not-guaranteed beat (idea 5) compresses to one spoken sentence;
the decreasing mirror (idea 8) compresses to "swap sup for inf, F for
1 - F" over the final formula, with no derivation shown.
