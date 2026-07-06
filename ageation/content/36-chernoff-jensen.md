---
slug: 36-chernoff-jensen
title: The Chernoff Bound and Jensen's Inequality
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/36-chernoff-jensen.tex
source_sha256: ed51482cf6eb97cf3db7069cb4b2b7be472baea9b4a953de39f301327a986252
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/expectations_and_bounds.tex
companion: sources/36-chernoff-jensen.md
companion_sha256: e034200c86458961206f714159e3abfba75bddd45e4e1c74f4980f14a60bd496
prereqs:
  - 35-markov-chebyshev
audience: undergraduate engineering, first probability course
concepts:
  - id: chernoff-construction
    name: The exponential dominating function
    importance: core
    one_liner: Run Chebyshev with h(x) = e^{sx} over S = [a, inf) - i_S = e^{sa}, so Pr(X >= a) <= e^{-sa} M_X(s); video 34's MGF becomes a tail bound.
  - id: chernoff-optimize
    name: The Chernoff bound — optimizing the family
    importance: highlight
    one_liner: Every s > 0 gives a valid bound, so take the best - Pr(X >= a) <= inf_{s>0} e^{-sa} M_X(s), the celebrated Chernoff bound.
  - id: log-mgf-legendre
    name: The log-MGF and the Legendre transform
    importance: optional        # named, not developed; cut first
    one_liner: With Lambda(s) = log M_X(s), the bound reads log Pr(X >= a) <= -sup_{s>0} {sa - Lambda(s)} — the right side is the Legendre transformation of Lambda.
  - id: convexity-tangent
    name: Convex functions sit above their tangents
    importance: core
    one_liner: If g'' >= 0 then g' is increasing, and the fundamental theorem of calculus gives g(x) >= g(a) + (x - a) g'(a) — every tangent line under-estimates a convex curve.
  - id: jensen
    name: Jensen's inequality
    importance: core
    one_liner: Put a = E[X] in the tangent bound and take expectations - the linear term dies, leaving E[g(X)] >= g(E[X]) for convex g.
estimated_runtime_sec: 300
---

# The Chernoff Bound and Jensen's Inequality — Concept Map

This video covers the last two subsections of book chapter 10 (Expectations
and Bounds), closing the chapter. Video 35 built the Chebyshev template
this video pushes to its exponential extreme, and video 34 forged the MGF
it runs on; book chapter 11 (continuous random vectors, videos 37–40)
follows.

## What
Two capstone inequalities. The **Chernoff bound** is the Chebyshev
template run with the dominating function `h(x) = e^{sx}`: over
`S = [a, inf)` the infimum is `e^{sa}`, so
`Pr(X >= a) <= e^{-sa} M_X(s)` — one bound for *every* s > 0. Optimizing
over the whole family gives
`Pr(X >= a) <= inf_{s>0} e^{-sa} M_X(s)`, sometimes written through the
log-MGF `Lambda(s) = log M_X(s)` as
`log Pr(X >= a) <= -sup_{s>0} {sa - Lambda(s)}` — a Legendre
transformation. **Jensen's inequality** comes from a different source
entirely: not domination but *convexity*. A twice-differentiable convex
function sits above each of its tangent lines,
`g(x) >= g(a) + (x - a) g'(a)`; choosing the tangent point `a = E[X]` and
taking expectations kills the linear term, leaving
`E[g(X)] >= g(E[X])`.

## Why it matters
Chernoff is the chapter's payoff: Markov spent one moment, Chebyshev
spent two, and Chernoff spends the *entire* MGF — the whole catalog of
moments at once — which is why it has "a central role in many application
domains" (coding, communications, large deviations). It is also the purest
example of a course-long theme: don't settle for one bound when you hold a
family — optimize. Jensen is the other kind of inequality, flowing from
the shape of a single function rather than from domination; `E[g(X)] >=
g(E[X])` is the one-line reason averages and nonlinear functions never
commute, a fact used everywhere from estimation to information theory.

## Key ideas (in dependency order)
1. **The exponential dominator.** To bound `Pr(X >= a)`, apply video 35's
   Chebyshev inequality with `h(x) = e^{sx}`, s > 0, and `S = [a, inf)`:
   `i_S = inf_{x >= a} e^{sx} = e^{sa}`.
2. **One bound per s.** Immediately,
   `Pr(X >= a) <= e^{-sa} E[e^{sX}] = e^{-sa} M_X(s)` — video 34's MGF,
   evaluated, is a tail bound. Every curve `e^{s(x - a)}` dominates the
   indicator `1_{[a,inf)}(x)`, so each s > 0 certifies its own bound
   (the notes' figure: a fan of exponentials over one step).
3. **Optimize the family.** The best exponential depends on the
   distribution of X and on a — so search:
   `Pr(X >= a) <= inf_{s>0} e^{-sa} M_X(s)`. This is the Chernoff bound.
4. **Log form (optional).** With `Lambda(s) = log M_X(s)`, taking logs
   turns the product into a difference:
   `log Pr(X >= a) <= -sup_{s>0} {sa - Lambda(s)}`; the right-hand side
   is the *Legendre transformation* of Lambda — a name to recognize, not
   a tool to develop.
5. **Convexity and tangents.** Let g be convex and twice differentiable,
   `g''(x) >= 0`. The fundamental theorem of calculus writes
   `g(x) = g(a) + \int_a^x g'(u) du`; since g' is monotone increasing,
   replacing g'(u) by g'(a) inside the integral only shrinks it:
   `g(x) >= g(a) + (x - a) g'(a)`. A convex curve lies above every
   tangent line.
6. **Jensen's inequality.** The tangent bound holds pointwise, so
   `g(X) >= g(a) + (X - a) g'(a)` as random variables. Choose
   `a = E[X]` and take expectations: `E[X] - E[X] = 0` wipes out the
   slope term, and `E[g(X)] >= g(E[X])` remains — provided both
   expectations exist. (True for general convex g too; the smooth proof
   is the honest one at this level.)

## What else (connections, to seed callbacks in narration)
- The whole video is video 35's machinery running hotter: Cantelli
  optimized over a quadratic family (one dial b); Chernoff optimizes over
  an exponential family (one dial s) — same move, sharper weapon.
- `e^{-sa} M_X(s)` is the promised payoff of video 34: "keep this
  function in your pocket" gets cashed here.
- Jensen explains an old sighting: video 19/20's fact
  `E[X^2] >= (E[X])^2` (variance is nonnegative) is Jensen with
  `g(x) = x^2` — the callback that makes the new inequality feel
  inevitable.
- The scratch notes flag Chernoff's home turf: exponentially sharp tail
  bounds for sums of independent variables — the independence story for
  continuous variables is completed in book chapter 11, and the
  concentration story in chapter 12 (videos 41–43).
- Convexity's tangent picture recalls the center-of-mass view of the mean
  (video 19): E[X] is where the tangent gets anchored.

## Conceptual progression (drives the storyboard)
The bounds ledger so far: Markov cost one moment, Chebyshev two → what if
we spend them all? → e^{sx} as the dominating function, i_S = e^{sa} →
one bound per s: the fan of exponentials over the indicator step → tighten
the fan: the infimum over s > 0 — the Chernoff bound → (a glance at the
log form and its Legendre name) → change of key: inequalities from a
function's own shape → convex means curving upward, above every tangent →
anchor the tangent at E[X], average both sides → E[g(X)] >= g(E[X]) →
the chapter closes: expectation as a bounding tool, from one moment to
all of them to none but convexity.

## Visual opportunities
- **The fan**: the indicator step 1_{[a,inf)} with the family
  e^{s(x-a)} drawn for several s values (the notes' own figure,
  animated) — each curve pinned to the point (a, 1), steepening as s
  grows.
- **Tightening**: the corresponding bound values e^{-sa} M_X(s) plotted
  against s beside the fan; a marker slides to the minimum — video 35's
  Cantelli-dial animation, reprised deliberately.
- **Bounds ledger**: a three-row table building up — Markov / E[X],
  Chebyshev / E[X^2], Chernoff / M_X(s) — "what you pay, what you get."
- **Tangent test**: a convex curve with a tangent line sweeping along it,
  the curve never dipping below — convexity as a single animated
  invariant.
- **Jensen's collapse**: the inequality g(X) >= g(a) + (X - a) g'(a)
  on screen; a = E[X] substituted, the (E[X] - E[X]) term literally
  fading to zero, leaving E[g(X)] >= g(E[X]) boxed as the chapter's
  final card.

## Notation (per project.yaml)
- Probability `\Pr`, expectation `\mathrm{E}`; indicator `\mathbf{1}_S`.
- MGF `M_X(s)`; log-MGF `\Lambda(s) = \log M_X(s)`; infimum/supremum
  `\inf_{s > 0}`, `\sup_{s > 0}`; derivatives `\frac{dg}{dx}`.

## Deliberately out of scope
- Markov and Chebyshev themselves — video 35; here they are one recap
  breath and a template invocation.
- Computing M_X for specific distributions — video 34's job; Chernoff is
  stated for a generic MGF, no worked distribution is plugged in (the
  notes plug none in).
- Large-deviations theory behind the Legendre transformation — named
  only, as in the notes.
- Jensen for non-differentiable convex g — the notes state it holds and
  call the proof much harder; we do the same in one sentence.
- Sums of iid variables and concentration — chapters 11–12 (videos
  37–43).

## Cut first (if the script runs over budget)
The log-MGF / Legendre beat drops entirely (it is a rebranding, not a new
bound); next, the tangent-line derivation compresses to the sweeping
tangent animation with the algebra reduced to its first and last lines.
