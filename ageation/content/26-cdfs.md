---
slug: 26-cdfs
title: Cumulative Distribution Functions
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/26-cdfs.tex
source_sha256: 97aed752ea5c0b160dea541368e4cd64a021b6399ffd9be0c700af4b14c4bb41
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/continuous_random_variables.tex
companion: sources/26-cdfs.md
companion_sha256: 03278c8dbecd26d8dca205580ba51bc9f97be65ef64ad47c706c28ed082efb4c
prereqs:
  - 25-sums-and-many
audience: undergraduate engineering, first probability course
concepts:
  - id: why-no-pmf
    name: Why the PMF machinery runs out
    importance: core
    one_liner: A random variable over a continuum cannot be described by a PMF — the third axiom only sums countably many disjoint events; a new object is needed.
  - id: cdf-definition
    name: The cumulative distribution function
    importance: core
    one_liner: F_X(x) = Pr(X <= x) — one function, defined for EVERY random variable, that packages the probability of all events {X <= x}.
  - id: cdf-properties
    name: What every CDF must look like
    importance: core
    one_liner: Limits 0 at -infinity and 1 at +infinity, non-decreasing, and Pr(x_1 < X <= x_2) = F_X(x_2) - F_X(x_1) — interval probabilities are differences of heights.
  - id: discrete-staircase
    name: Discrete random variables have staircase CDFs
    importance: core
    one_liner: Summing the PMF up to x gives a step function; each jump height IS the mass at that point, so the PMF can be recovered from the CDF.
  - id: geometric-cdf
    name: Worked example — the geometric CDF
    importance: core
    one_liner: F_X(x) = 1 - (1-p)^floor(x) for the geometric; differencing consecutive steps hands back (1-p)^{k-1} p exactly.
  - id: continuous-cdf
    name: Continuous random variables
    importance: core
    one_liner: A random variable whose CDF is continuous (and differentiable almost everywhere) is called continuous — no jumps means no point carries mass.
  - id: mixed-rvs
    name: Mixed random variables
    importance: optional        # starred section; cut first if over budget
    one_liner: CDFs that ramp AND jump — no PMF, no PDF, but the CDF still tells the whole story.
estimated_runtime_sec: 300
---

# Cumulative Distribution Functions — Concept Map

This video covers Section 8.1 of book chapter 8 (all three subsections:
discrete, continuous, mixed*). It opens the continuous half of the course:
video 27 differentiates the CDF into a density; videos 28–30 catalog the
canonical continuous distributions.

## What
Discrete random variables and their PMFs cover only a sliver of the models
engineering needs — measurement noise, waiting times, and signal amplitudes
range over a continuum. A PMF cannot describe them: the third axiom of
probability adds up only *countably* many disjoint events. The bridge
object is the **cumulative distribution function**,
`F_X(x) = Pr(X <= x)` — defined for every random variable, discrete or not.
Its shape classifies the variable: staircases are discrete (jumps carry
the PMF), continuous ramps are continuous random variables, and hybrids
are mixed.

## Why it matters
This is the single unifying object of the whole course: every random
variable — discrete, continuous, or mixed — has a CDF, and everything we
can ask about intervals is a difference of two CDF values. The chapter's
strategy is to carry the discrete intuition across the bridge: what the
PMF did by summing, the CDF does by accumulating, and (next video) the
density does by differentiating.

## Key ideas (in dependency order)
1. **The PMF runs out.** An uncountable range means we cannot list masses;
   the axioms themselves (countable additivity) block a "continuous PMF."
   Motivation, not machinery.
2. **The CDF.** `F_X(x) = Pr(X <= x) = Pr(X^{-1}((-inf, x]))` — the
   probability that X lands at or left of x, as a function of x. Exists
   for every well-behaved X.
3. **Its shape is constrained.** `F_X -> 0` as `x -> -inf`, `F_X -> 1` as
   `x -> +inf`; splitting `{X <= x_2}` into `{X <= x_1} ∪ {x_1 < X <= x_2}`
   shows F is non-decreasing AND gives the interval formula
   `Pr(x_1 < X <= x_2) = F_X(x_2) - F_X(x_1)`.
4. **Discrete = staircase.** `F_X(x) = sum_{u <= x} p_X(u)`: flat between
   the values, a jump of height `p_X(u)` at each value u. Recover the PMF
   as `p_X(x) = F_X(x) - lim_{u ↑ x} F_X(u)` — jump heights.
5. **Worked: the geometric.** `F_X(x) = 1 - (1-p)^floor(x)` for x > 0;
   differencing consecutive integer steps returns `(1-p)^{k-1} p`. The CDF
   and PMF are two faces of one object.
6. **Continuous = smooth ramp.** If F_X is continuous and differentiable
   almost everywhere, X is a *continuous random variable*. Example:
   `F_X(x) = 1 - e^{-x}` (x >= 0) — differentiable, derivative `e^{-x}`
   (the exponential, foreshadowing video 29).
7. **Mixed (starred).** Ramps with jumps — no PMF, no PDF, yet the CDF
   still answers every interval question.

## What else (connections, to seed callbacks in narration)
- The geometric PMF's halving bars (videos 16, 18, 22) return one more
  time — now accumulated into a staircase.
- The interval formula is chapter 2's difference-of-nested-events argument
  (video 8, probability laws) in random-variable clothing.
- `F_X(x) = 1 - e^{-x}` quietly introduces the exponential distribution
  two videos early — video 29 will name it.
- The "which axiom breaks" opening ties back to video 8's three axioms and
  video 10's continuity of probability measures.

## Conceptual progression (drives the storyboard)
The discrete world recapped in one breath → a variable that ranges over a
continuum (a spinner / a noise voltage) → why no PMF can exist → define
F_X as accumulated probability → watch it sweep left-to-right, filling
from 0 to 1 → its three properties → the discrete staircase and jump
heights → the geometric worked both directions → smooth ramps as the new
citizens: continuous random variables → the mixed hybrid, briefly.

## Visual opportunities
- **The sweep**: a vertical line sweeping rightward across a PMF while a
  CDF curve accrues beneath it — accumulation made literal.
- **Staircase**: the geometric bars re-stacked cumulatively; each bar hops
  on top of the running total, leaving the familiar staircase.
- **Jump recovery**: zoom on one step; the jump height detaches and drops
  down as the PMF bar it equals.
- **Interval formula**: two heights marked on a CDF; the vertical gap
  between them slides over to measure Pr(x_1 < X <= x_2).
- **Ramp vs staircase**: discrete staircase and continuous ramp side by
  side (one at a time per house rule: shown in sequence), then the mixed
  curve with both features.

## Notation (per project.yaml)
- CDF `F_X(x)`, PMF `p_X(x)`; probabilities via `\Pr` with `\mid` for
  conditionals; floor written `\lfloor x \rfloor`.

## Deliberately out of scope
- The PDF and its properties — that is video 27 in its entirety.
- Any named continuous distribution beyond the cameo `1 - e^{-x}` CDF
  (uniform/Gaussian in 28, exponential in 29, the gallery in 30).
- Right-continuity subtleties and measure-theoretic caveats — the notes
  keep them implicit; so do we.

## Cut first (if the script runs over budget)
The mixed-random-variables beat (starred in the notes) compresses to one
sentence over a single hybrid-CDF picture, or drops entirely.
