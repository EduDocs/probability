---
slug: 33-generating-rvs
title: Generating Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/33-generating-rvs.tex
source_sha256: 7c91a09f784bbdf3d5af3f1433210909e87bc606c7686af4e399619680d116bc
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/derived_distributions.tex
companion: sources/33-generating-rvs.md
companion_sha256: af8623dfc2346b019e3e5f41f532c43d3eb0800478e576aef14c19a60a613439
prereqs:
  - 32-change-of-variables
audience: undergraduate engineering, first probability course
concepts:
  - id: uniform-from-anything
    name: F_X(X) is uniform
    importance: core
    one_liner: Feed a continuous X into its own invertible CDF - f_Y(y) = f_X(x)/|dF_X/dx(x)| = f_X(x)/f_X(x) = 1 on (0,1) — every continuous random variable flattens to Uniform(0,1).
  - id: inverse-cdf-method
    name: The inverse-CDF method
    importance: highlight
    one_liner: Run it backwards - with Y uniform on [0,1], V = F_X^{-1}(Y) has density f_X — one uniform routine generates ANY continuous distribution.
  - id: exponential-recipe
    name: Worked example — generating an exponential
    importance: core
    one_liner: F_X^{-1}(y) = -(1/lambda) log(1 - y), so X = -(1/lambda) log(1 - Y) turns uniform draws into exponential(lambda) draws.
  - id: discrete-binning
    name: Generating discrete random variables
    importance: core
    one_liner: Chop [0,1] into intervals (F_X(x_{i-1}), F_X(x_i)] and output x_i when Y lands in bin i - Pr(X = x_i) = F_X(x_i) - F_X(x_{i-1}) = p_X(x_i).
  - id: efficiency-caveat
    name: The case statement can be slow
    importance: optional        # closing aside; cut first if over budget
    one_liner: Binning by cases works for any PMF but may be an excessively slow routine — many discrete distributions have much more efficient generators.
estimated_runtime_sec: 300
---

# Generating Random Variables — Concept Map

This video covers Section 9.3 of book chapter 9 (both subsections:
continuous, then discrete). It is the chapter's payoff: video 32's
change-of-variables formula, pointed at the CDF itself, becomes an
algorithm — one Uniform(0,1) routine suffices to simulate any distribution
in the course. It closes book chapter 9; book chapter 10, "Expectations and
Bounds," begins with video 34.

## What
Computer simulations need draws from arbitrary distributions, but the
machine offers only a routine that outputs a value uniformly distributed
between zero and one. Two observations bridge the gap. Forward: if X is
continuous with invertible CDF, then `Y = F_X(X)` has density
`f_Y(y) = f_X(x)/|dF_X/dx(x)| = 1` on (0,1) — every continuous random
variable, passed through its own CDF, becomes uniform. Backward: since
`F_X^{-1}(F_X(X)) = X`, applying `F_X^{-1}` to a Uniform[0,1] variable Y
produces `V = F_X^{-1}(Y)` with `f_V(v) = f_X(v)` — the **inverse-CDF
method**. Discrete targets work the same way with bins: partition [0,1] at
the CDF's plateau heights and output `x_i` when Y falls in the i-th bin,
whose length is exactly `p_X(x_i)`.

## Why it matters
This is where nine chapters of theory touch engineering practice:
simulation is the first step of most design projects, and this section is
the reason a single uniform generator is enough. It is also a satisfying
full-circle moment for the machinery — video 26's CDF, video 28's uniform,
video 29's exponential, and video 32's formula all reappear as moving parts
of one algorithm. The discrete half quietly reuses video 26's
jump-heights-are-probabilities fact in reverse: the CDF's risers become the
bins a uniform draw falls into.

## Key ideas (in dependency order)
1. **The engineering problem.** Simulations for validating concepts and
   comparing designs need random variables of every shape; the available
   primitive is one routine returning a uniform value on [0,1]. Goal:
   manufacture everything else from it.
2. **Forward — flattening.** Let X be continuous with invertible CDF and
   set `Y = F_X(X)`. F_X is differentiable and strictly increasing on the
   support of X, so video 32's formula applies with g = F_X:
   `f_Y(y) = f_X(x)/|dF_X/dx(x)| = f_X(x)/|f_X(x)| = 1` for y in (0,1)
   (and 0 outside, since `0 <= F_X(x) <= 1`). Any continuous X yields a
   Uniform(0,1).
3. **Backward — the inverse-CDF method.** When F_X is invertible,
   `F_X^{-1}(F_X(X)) = X`, so try `V = F_X^{-1}(Y)` with Y uniform on
   [0,1]. Derived distributions again:
   `f_V(v) = f_Y(y) / |dF_X^{-1}/dy(y)| = f_Y(y) (dF_X/dv)(v) = f_X(v)`
   with `y = F_X(v)` and `f_Y = 1` on [0,1]. To create X with CDF F_X,
   apply `F_X^{-1}` to a uniform draw.
4. **Worked: the exponential.** Target: exponential with parameter lambda,
   `F_X(x) = 1 - e^{-lambda x}` for x >= 0. Inverting:
   `F_X^{-1}(y) = -(1/lambda) log(1 - y)`, so
   `X = -(1/lambda) log(1 - Y)`. Check by the formula:
   `f_X(x) = f_Y(y) / (1/(lambda(1 - y))) = lambda e^{-lambda x}` with
   `y = 1 - e^{-lambda x}` — the desired density.
5. **Discrete targets — binning.** Let p_X have support
   `x_1 < x_2 < ...` and CDF `F_X(x) = sum_{x_i <= x} p_X(x_i)`. Define
   the case function `g(y) = x_i` when `F_X(x_{i-1}) < y <= F_X(x_i)`
   (convention `x_0 = 0`). With X = g(Y),
   `Pr(X = x_i) = Pr(F_X(x_{i-1}) < Y <= F_X(x_i)) = F_X(x_i) - F_X(x_{i-1})
   = p_X(x_i)` — each bin's length is exactly the mass it must deliver.
6. **A practical caveat.** Implementing the case statement naively may be
   excessively slow; for many discrete random variables there are much more
   efficient generation routines. The principle stands; the engineering
   refines it.

## What else (connections, to seed callbacks in narration)
- Video 32's change-of-variables formula powers both directions of the
  argument (ideas 2 and 3) — this video is that formula's victory lap.
- Video 26 proved that a discrete CDF's jump heights ARE the PMF values;
  idea 5 runs that fact backwards, turning risers into sampling bins.
- Video 28's uniform distribution graduates from example to raw material;
  video 29's exponential CDF `1 - e^{-lambda x}` gets inverted rather than
  differentiated.
- Video 31's warning that Y = g(X) can be discrete comes true
  constructively: idea 5's g manufactures a discrete variable from a
  continuous one on purpose.
- The forward observation (idea 2) is the classical probability integral
  transform — the companion notes' name for it.

## Conceptual progression (drives the storyboard)
A simulation needs exponential arrivals, Gaussian noise, discrete packet
counts — the computer offers only Uniform(0,1) → feed X through its own
CDF: the density flattens to 1 (video 32's formula, g = F_X) → so the CDF
is a bridge to uniformity — cross it backwards: F_X^{-1} of a uniform has
exactly the law of X → the exponential recipe worked end to end,
X = -(1/lambda) log(1 - Y) → discrete targets: the unit interval sliced
into bins of lengths p_X(x_i), a uniform dot falls, the bin names the
output → a closing caveat on speed → chapter 9 complete: derive forward,
generate backward.

## Visual opportunities
- **Flattening**: dots sampled under a bumpy density f_X rise through the
  CDF curve (x-position mapped to height F_X(x)) and land on the vertical
  unit interval spread perfectly evenly — the forward transform as
  migration.
- **The uniform rain** (centerpiece): uniform dots falling down the
  vertical (0,1) axis, each traveling horizontally until it meets the CDF
  curve, then dropping to the x-axis; the accumulating histogram grows into
  f_X. Steep CDF stretches catch many dots into narrow zones — video 32's
  slope intuition replayed.
- **Exponential recipe**: the curve `y = 1 - e^{-lambda x}` with the
  inversion steps assembling algebraically into
  `X = -(1/lambda) log(1 - Y)`; a few uniform draws animate through the
  formula to become waiting times.
- **Discrete bins**: video 26's staircase CDF rotated into service — the
  unit interval on the vertical axis partitioned at the plateau heights,
  each bin tinted and labeled p_X(x_i); a uniform dot falls into a bin and
  the output x_i lights up on the horizontal axis.
- **Closing frame**: the chapter's three tools side by side in sequence —
  CDF method, change-of-variables formula, inverse-CDF sampler — one
  machine, run in both directions.

## Notation (per project.yaml)
- CDF `F_X`, inverse `F_X^{-1}`; densities `f_X, f_Y, f_V`; PMF `p_X`;
  probabilities via `\Pr`; conditionals (if any) with `\mid`.
- Rate `\lambda`; logarithm written `\log` as in the notes.

## Deliberately out of scope
- Deriving the change-of-variables formula itself — video 32; here it is
  only applied.
- CDFs that are not invertible (flat stretches, jumps in the continuous
  case) — the notes assume invertibility and so do we.
- The named efficient generators hinted at by the closing caveat — the
  notes say they exist and stop; we do the same.
- The book's starred discrete-approximations material is commented out of
  the chapter and stays out of the video.

## Cut first (if the script runs over budget)
The efficiency caveat (idea 6) drops to a single spoken sentence over the
final frame; next, the verification step inside the exponential example
(the f_X check) compresses to "and the formula confirms it," leaving only
the inversion itself on screen.
