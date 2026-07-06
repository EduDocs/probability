---
slug: 37-joint-continuous
title: Joint Continuous Distributions
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/37-joint-continuous.tex
source_sha256: ef89abce190ca6564704c55877c2f10d89c6d17eb67f14322b820b3eed1a3d8b
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/random_vectors.tex
companion: sources/37-joint-continuous.md
companion_sha256: 844e4470fe388913fc5a31a5b72b6646b968aeac5a4f499cf40952e94bdf1277
prereqs:
  - 36-chernoff-jensen
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: joint-cdf
    name: The joint cumulative distribution function
    importance: core
    one_liner: F_{X,Y}(x,y) = Pr(X <= x, Y <= y) — one function on the plane recording the probability of the quadrant at or below-left of (x, y).
  - id: marginal-cdfs
    name: Marginals as limits of the joint CDF
    importance: core
    one_liner: Push y to infinity and the quadrant becomes a half-plane — F_{X,Y}(x,y) -> F_X(x); push either argument to -infinity and it collapses to 0.
  - id: joint-pdf
    name: The joint probability density function
    importance: core
    one_liner: f_{X,Y} = d^2 F_{X,Y} / dx dy — nonnegative, integrates to one over the plane, and rebuilds the CDF by double integration; when it exists the pair is called jointly continuous.
  - id: prob-as-volume
    name: Probability of a region is a volume
    importance: core
    one_liner: Pr((X,Y) in S) = double integral of f_{X,Y} over S — probability is the volume under the density surface above the region; rectangles reduce to iterated integrals.
  - id: marginal-pdf
    name: Marginal densities by integrating out
    importance: core
    one_liner: f_Y(y) = integral of f_{X,Y}(x,y) dx — integrate the unwanted variable away, the continuous mirror of summing a joint-PMF table's rows.
  - id: unit-circle
    name: Worked example — uniform on the unit circle
    importance: core
    one_liner: f_{X,Y} = 1/pi on the disk; Pr(inside radius 1/2) = 1/4 — the volume formula computing an area ratio.
  - id: rayleigh
    name: Worked example — two Gaussians and the Rayleigh distance
    importance: highlight
    one_liner: Independent zero-mean Gaussians give Pr(R <= s) = 1 - e^{-s^2/(2 sigma^2)} in polar coordinates, so the radius R has the Rayleigh density (s/sigma^2) e^{-s^2/(2 sigma^2)}.
estimated_runtime_sec: 300
---

# Joint Continuous Distributions — Concept Map

This video covers Section 11.1 of book chapter 11 (Joint Cumulative
Distributions) and opens the continuous mirror of the discrete arc: video 21
organized two discrete variables into a joint PMF *table*; this video
replaces the table with a density *surface*. Video 38 slices that surface
into conditionals, exactly as video 22 sliced the table.

## What
Two random variables on the same experiment are described together by the
**joint CDF** `F_{X,Y}(x,y) = Pr(X <= x, Y <= y)` — the probability of the
quadrant below-left of (x, y). Its limits recover the pieces: `y -> inf`
gives the marginal `F_X(x)`, either argument to `-inf` gives 0. When
F_{X,Y} is totally differentiable, the **joint PDF**
`f_{X,Y} = d^2 F_{X,Y} / dx dy` exists and the pair is called *jointly
continuous*: probability becomes volume, `Pr((X,Y) in S)` is the double
integral of f_{X,Y} over S, and marginal densities fall out by integrating
the other variable away. Two worked examples run the machine: the uniform
disk (an area ratio) and two independent Gaussians, whose distance from the
origin turns out to be Rayleigh.

## Why it matters
Almost nothing in engineering involves one random quantity in isolation —
signal and noise, position in two coordinates, two arrival times. Chapter 7
built this vocabulary for discrete pairs; measurements live on a continuum,
so the whole kit must cross the bridge that videos 26–27 built for single
variables. The joint CDF is again the universal object, the density again
its derivative — but now probability is volume under a surface, and every
later move of the chapter (conditioning in 38, independence in 39, sums in
40) is a manipulation of this one object.

## Key ideas (in dependency order)
1. **The joint CDF.** `F_{X,Y}(x,y) = Pr(X <= x, Y <= y)` — equivalently
   the probability of the outcome set
   `{omega : X(omega) <= x, Y(omega) <= y}`. Video 26's accumulation idea,
   now sweeping a quadrant corner across the plane instead of a point along
   a line.
2. **Its limits.** `lim_{y -> inf} F_{X,Y}(x,y) = F_X(x)` (the constraint
   on Y evaporates; the quadrant becomes a half-plane), symmetrically
   `lim_{x -> inf} F_{X,Y}(x,y) = F_Y(y)`, and both limits at `-inf` give
   0 — the two-variable version of video 26's 0-to-1 endpoints.
3. **The joint PDF.** When F_{X,Y} is totally differentiable,
   `f_{X,Y}(x,y) = d^2 F_{X,Y} / dx dy` (order of differentiation
   immaterial); the pair is *jointly continuous* when this density exists.
   Calculus runs it backwards:
   `F_{X,Y}(x,y) = int_{-inf}^{x} int_{-inf}^{y} f_{X,Y}(u,v) dv du`.
   Nonnegative, and its integral over the whole plane is 1.
4. **Probability = volume.** For an admissible region S,
   `Pr((X,Y) in S) = double-int_S f_{X,Y}(x,y) dy dx` (the indicator
   `\mathbf{1}_S` inside a full-plane integral, in the source's first
   form). When S is a rectangle `[a,b] x [c,d]` this is the familiar
   iterated integral `int_a^b int_c^d f_{X,Y} dy dx`.
5. **Marginals by integrating out.** `f_Y(y) = int f_{X,Y}(x,y) dx` —
   differentiate the marginal-CDF limit of idea 2, or read it as the
   continuous analog of video 21's row sums: in chapter 7 we summed a
   table's row; now we integrate a slice of the surface.
6. **Worked: the uniform disk.** `f_{X,Y} = 1/pi` on `x^2 + y^2 <= 1`,
   zero outside. `Pr((X,Y) inside radius 1/2) = 1/4` — the volume formula
   reduces to (area of small disk)/(area of unit disk); a flat density
   makes probability literally area.
7. **Worked: two Gaussians, one distance.** X, Y independent zero-mean
   Gaussians with variance sigma^2:
   `f_{X,Y}(x,y) = (1/(2 pi sigma^2)) e^{-(x^2+y^2)/(2 sigma^2)}` — the
   bell curve rotated into a bell *surface*. For `R = sqrt(X^2 + Y^2)`,
   polar coordinates give `Pr(R <= s) = 1 - e^{-s^2/(2 sigma^2)}`, hence
   `f_R(s) = (s/sigma^2) e^{-s^2/(2 sigma^2)}` — the **Rayleigh
   distribution** of video 30, now derived rather than cataloged.

## What else (connections, to seed callbacks in narration)
- Video 21's joint PMF table is the constant refrain: cell -> surface
  patch, row sum -> integrating out, "the joint determines the marginals
  but not conversely" carries over verbatim.
- Video 26's CDF properties (limits 0 and 1, accumulation) reappear with
  one more argument; video 27's derivative-of-CDF move is now a mixed
  partial.
- The Gaussian surface is video 28's bell curve squared into two
  dimensions; the Rayleigh answer lands on video 30's gallery entry and on
  chapter 9's derived-distribution theme (videos 31–32).
- The Gaussian example quietly *uses* independence-as-product one section
  early — video 39 makes that definition official.
- Slicing this surface at a fixed y is exactly where video 38 picks up.

## Conceptual progression (drives the storyboard)
Two variables, one experiment (recap 21's table in one breath) → the
continuum forces the CDF route (26's lesson) → a corner sweeping the plane
accumulates F_{X,Y} → push the corner to infinity: marginals appear →
differentiate twice: the density surface → probability as volume over a
region → rectangles as the easy case → integrate out a variable: marginal
density as a collapsed slice → the flat disk: volume = area ratio → the
Gaussian bell surface → carve a cylinder of radius s: the Rayleigh payoff.

## Visual opportunities
- **The sweeping corner**: a shaded quadrant with corner at (x, y) gliding
  across a scatter of sample points; a meter fills toward 1 as the corner
  moves up-right — video 26's sweep, upgraded to 2-D.
- **Table melts into surface**: video 21's joint PMF grid with bars on
  each cell, bars thinning and multiplying into a smooth density surface
  (the discrete-to-continuous bridge in one shot).
- **Volume over a region**: a region S highlighted on the floor plane, the
  column of density above it filling with color as the double integral is
  written.
- **Integrating out**: the surface sliced at a fixed y, the slice's area
  collapsing onto a 1-D axis to build f_Y point by point — row sums made
  continuous.
- **Disk example**: the 1/pi cylinder over the unit disk; the inner
  radius-1/2 disk lifts its quarter of the volume out.
- **Rayleigh climax**: the Gaussian bell surface; a growing circle of
  radius s carves out the central volume while `1 - e^{-s^2/(2 sigma^2)}`
  counts up; the captured volume re-plots as the Rayleigh density.

## Notation (per project.yaml)
- Joint CDF `F_{X,Y}(x,y)`, joint PDF `f_{X,Y}(x,y)`, marginals `F_X`,
  `f_Y`; probabilities via `\Pr`; indicator `\mathbf{1}_S`; commas inside
  `\Pr(X \leq x, Y \leq y)` for joint events.

## Deliberately out of scope
- Conditional CDFs/PDFs and anything of the form f_{X|Y} — video 38.
- The formal definition and consequences of independence (the Gaussian
  example simply *states* its factored density) — video 39.
- Sums, convolution, and MGFs — video 40.
- Covariance, correlation, and general jointly-Gaussian vectors — the
  scratch notes list them, but this video stays within Section 11.1.

## Cut first (if the script runs over budget)
The disk example compresses to a single picture with the 1/4 answer spoken
over it (its area-ratio logic is one sentence); the marginal-PDF beat can
fold into the limits beat, with the integrate-out formula shown once and
the row-sum callback carrying the intuition.
