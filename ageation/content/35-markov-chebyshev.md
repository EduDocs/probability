---
slug: 35-markov-chebyshev
title: The Markov and Chebyshev Inequalities
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
source: sources/35-markov-chebyshev.tex
source_sha256: ed51482cf6eb97cf3db7069cb4b2b7be472baea9b4a953de39f301327a986252
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/expectations_and_bounds.tex
companion: sources/35-markov-chebyshev.md
companion_sha256: e034200c86458961206f714159e3abfba75bddd45e4e1c74f4980f14a60bd496
prereqs:
  - 34-mgfs
audience: undergraduate engineering, first probability course
concepts:
  - id: why-bounds
    name: When exact probabilities are out of reach
    importance: core
    one_liner: Computing a probability exactly is often impossible or impractical; a good bound is the engineer's answer, and expectation is the tool that produces it.
  - id: dominating-functions
    name: Dominating functions
    importance: core
    one_liner: If 0 <= g(x) <= h(x) everywhere, then E[g(X)] <= E[h(X)] — the density weights both sides the same way, so pointwise domination survives the integral.
  - id: markov
    name: The Markov inequality
    importance: core
    one_liner: Pr(X >= a) = E[1_{[a,inf)}(X)] and the line x/a sits above that indicator step, so Pr(X >= a) <= E[X]/a for nonnegative X.
  - id: chebyshev
    name: The Chebyshev inequality
    importance: core
    one_liner: For nonnegative h and any set S, i_S Pr(X in S) <= E[h(X)] where i_S = inf_{x in S} h(x) — one template that mints a whole family of bounds.
  - id: second-moment-bound
    name: The second-moment instance
    importance: core
    one_liner: "Take h(x) = x^2 and S = {x^2 >= b^2}: Pr(|X| >= b) <= E[X^2]/b^2 — applied to X - m this is the classical variance form that video 42 will feed the Law of Large Numbers."
  - id: cantelli
    name: Worked example — the Cantelli inequality
    importance: highlight
    one_liner: Dominate with h(y) = (y+b)^2, get (sigma^2 + b^2)/(a+b)^2 for every b, then minimize at b = sigma^2/a — the one-sided bound sigma^2/(a^2 + sigma^2).
  - id: tightness
    name: A bound met with equality
    importance: optional        # cut first if over budget
    one_liner: A two-point PMF with mass b^2/a^2 at x = a makes Pr(X in S) exactly E[X^2]/a^2 — Chebyshev cannot be improved without more information.
estimated_runtime_sec: 310
---

# The Markov and Chebyshev Inequalities — Concept Map

This video covers the Important Inequalities introduction plus the Markov
and Chebyshev subsections of book chapter 10. Video 34 built the MGF;
video 36 will push today's dominating-function template to its exponential
extreme (Chernoff) and meet convexity (Jensen).

## What
When a probability is impossible or impractical to compute exactly, an
*upper bound* may be answer enough — and expectations are the way to get
one. The engine is the **dominating function** principle: if
`0 <= g(x) <= h(x)` for all x, then `E[g(X)] <= E[h(X)]`. Since any
probability is itself an expectation — `Pr(X in S) = E[1_S(X)]` (video
19's indicator trick) — bounding a probability reduces to finding a
computable function that sits above an indicator step. The line `x/a`
above `1_{[a,inf)}` gives the **Markov inequality**
`Pr(X >= a) <= E[X]/a`; the general template — the **Chebyshev
inequality** `i_S Pr(X in S) <= E[h(X)]` with `i_S = inf_{x in S} h(x)` —
mints the second-moment bound `Pr(|X| >= b) <= E[X^2]/b^2`, the one-sided
Cantelli bound `sigma^2/(a^2 + sigma^2)`, and more.

## Why it matters
This is where expectation is promoted from a summary statistic to a
*working tool*: one number (a mean, a variance) fences in probabilities
about which we know almost nothing else. That leverage is the seed of the
Law of Large Numbers — video 42 will run the variance form of Chebyshev on
an empirical average and watch the tail probability collapse as n grows —
and of every concentration argument after it. The tightness example
delivers the honest counterpart: without more information, these bounds
cannot be improved, which is exactly why video 36 will pay for sharper
ones with the whole MGF.

## Key ideas (in dependency order)
1. **Why bounds.** Exact values are often unreachable; a pertinent bound
   is acceptable — and expectation is "most important" in finding one.
2. **Dominating functions.** For nonnegative g, h with `g(x) <= h(x)`
   everywhere: `E[g(X)] = \int g(x) f_X(x) dx <= \int h(x) f_X(x) dx =
   E[h(X)]` — the density acts as a common weighting, so the pointwise
   inequality integrates. (The notes' Figure: two curves, one under the
   other.)
3. **Probability as expectation.** `Pr(X in S) = E[1_S(X)]` — so to bound
   a probability, dominate an indicator with something whose expectation
   we can compute.
4. **Markov.** X nonnegative, a > 0, S = [a, inf): the line `h(x) = x/a`
   satisfies `h(x) >= 1_S(x)` for all x >= 0, hence
   `Pr(X >= a) = E[1_S(X)] <= E[X]/a`. One mean, one tail bound.
5. **Chebyshev.** For nonnegative h and admissible S, let
   `i_S = inf_{x in S} h(x)`. Then `i_S 1_S(x) <= h(x) 1_S(x) <= h(x)`
   pointwise, and integrating gives `i_S Pr(X in S) <= E[h(X)]`; when
   `i_S > 0`, `Pr(X in S) <= E[h(X)]/i_S`. Proved for densities, valid
   for PMFs alike.
6. **The second-moment instance.** `h(x) = x^2`, `S = {x : x^2 >= b^2}`:
   `i_S = b^2`, so `Pr(|X| >= b) <= E[X^2]/b^2`. Applied to the centered
   variable X - m this reads `Pr(|X - m| >= b) <= Var[X]/b^2` — the form
   everyone calls "Chebyshev," and the one the Law of Large Numbers runs
   on.
7. **Worked: Cantelli.** For Y = X - m (so E[Y] = 0), dominate with
   `h(y) = (y + b)^2` over S = {y >= a}: `i_S = (a+b)^2` and
   `Pr(Y >= a) <= (sigma^2 + b^2)/(a+b)^2` for every b > 0. Minimize over
   b: the derivative vanishes at `b = sigma^2/a`, giving
   `Pr(X - m >= a) <= sigma^2/(a^2 + sigma^2)` — a first taste of
   *optimizing over a family of bounds*, video 36's main move.
8. **Tightness (optional).** With `p_X(0) = 1 - b^2/a^2`,
   `p_X(a) = b^2/a^2`: `E[X^2] = b^2` and `Pr(X in S) = b^2/a^2` — the
   Chebyshev bound `b^2/a^2` is met with equality.

## What else (connections, to seed callbacks in narration)
- `Pr(X in S) = E[1_S(X)]` is video 19's indicator identity (born in
  video 2-5), now load-bearing.
- The union bound (video 8) was the course's first inequality; these are
  its expectation-powered descendants.
- Video 20's variance — "the spread in one number" — finally shows what it
  is *for*: fencing tail probabilities.
- Plant the flag: Chebyshev on an empirical average is the entire proof of
  the (weak) Law of Large Numbers — book chapter 12, video 42. The
  companion notes preview it as confidence intervals for an empirical
  proportion.
- Cantelli's optimize-the-family move is rehearsal for the Chernoff bound
  (video 36), where the family is exponential and the pocket tool is
  video 34's MGF.

## Conceptual progression (drives the storyboard)
A tail probability we cannot compute → probabilities ARE expectations
(indicator recalled) → domination: one curve under another, weighted by
the density → the integral preserves the ordering → Markov: a straight
line over a step, E[X]/a → generalize: any nonnegative h, any set S, the
infimum i_S → Chebyshev as a template → instance h = x^2: the variance
bound → Cantelli: a family of bounds indexed by b, pick the best one →
equality is possible: the two-point PMF → what one moment buys, and what
it costs — sharper bounds need more (next video).

## Visual opportunities
- **Domination**: g(x) under h(x) (the notes' own figure), both then
  multiplied by a density f_X — the two weighted areas shaded in
  sequence, one visibly inside the other.
- **Markov's line**: the indicator step 1_{[a,inf)} drawn, then the line
  x/a laid over it, pivoting at the point (a, 1); the gap between line
  and step IS the slack in the bound.
- **Chebyshev template**: the set S highlighted on the x-axis, h(x)
  plotted, a horizontal dashed line at height i_S pressing up under h
  over S.
- **Cantelli's dial**: the bound (sigma^2 + b^2)/(a+b)^2 plotted against
  b; a marker slides along the curve to the minimum at b = sigma^2/a —
  optimization as literal descent.
- **Tightness**: the two-point PMF's bars, with E[X^2] and Pr(X >= a)
  computed beside them; the bound and the truth snapping to the same
  number.

## Notation (per project.yaml)
- Probability `\Pr`, expectation `\mathrm{E}`, variance `\mathrm{Var}`;
  indicator `\mathbf{1}_S`.
- Infimum `i_S = \inf_{x \in S} h(x)`; mean `m`, variance `\sigma^2`.

## Deliberately out of scope
- The Chernoff bound and Jensen's inequality — video 36 in its entirety
  (the exponential dominating family is only foreshadowed).
- The MGF plays no role here beyond a one-breath forward flag.
- The Law of Large Numbers / confidence-interval application — planted as
  a promise for video 42, not derived.

## Cut first (if the script runs over budget)
The tightness example drops entirely; next, Cantelli keeps its setup and
its punchline `sigma^2/(a^2 + sigma^2)` but the minimization shrinks to
"calculus finds b = sigma^2/a" over the sliding-marker animation.
