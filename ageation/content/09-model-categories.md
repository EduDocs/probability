---
slug: 09-model-categories
title: Categories of Probability Models
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/09-model-categories.tex
source_sha256: 0390aee133c064796b1e43553c5d8a427df530f6fb48a0e2403d86c11a61bcfa
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/probability_models.tex
companion: sources/09-model-categories.md
companion_sha256: a85a1f30cd74d5e583096067e8b704a4e5d8a0b8b2984f995a05e92b1e62c533
companion_upstream: ../chapters/probability_models.md
prereqs:
  - 08-probability-laws
audience: undergraduate engineering, first probability course
concepts:
  - id: finite-models
    name: Finite sample spaces and the equally-likely model
    importance: core
    one_liner: When Omega is finite and every outcome is equally likely, Pr(A) = |A| / |Omega| -- count favorable over total.
  - id: countably-infinite-models
    name: Countably infinite models
    importance: core
    one_liner: A countable Omega can be listed s_1, s_2, ...; assign weights that sum to 1 (coin-until-first-heads, Pr(k) = 2^-k).
  - id: uncountably-infinite-models
    name: Uncountably infinite models
    importance: core
    one_liner: For an uncountable Omega, a continuous law gives single points probability 0 and assigns probability by integrating a density; length, Pr((a,b)) = b - a on [0,1], is the uniform special case (mixed laws may also place mass on isolated points).
estimated_runtime_sec: 480        # ~8 min
---

# Categories of Probability Models — Concept Map

# What
Sections 3.2.1–3.2.3 of Chapter 3 (Probability Models): the three families a
sample space can fall into, and how a probability law is actually *specified* in
each. **Finite** spaces are pinned down by the probabilities of single outcomes,
and the equally-likely model is the clean special case where Pr(A) = |A| /
|Omega|. **Countably infinite** spaces (those listable as s_1, s_2, ...) are
still specified outcome-by-outcome, by weights that sum to one. **Uncountably
infinite** spaces (the unit interval, a continuum of angles) break that pattern:
individual outcomes carry probability zero, and the law is given instead by
*length* — Pr((a,b)) = b − a — extended to unions of disjoint intervals by the
third axiom.

## Why (motivation for the viewer)
Having just built the axioms, the natural next question is: what does a
probability law look like in practice? The answer depends entirely on the *size*
of the sample space. This video is the classification that organizes every model
the rest of the course will use, and it delivers the single most
counter-intuitive fact in elementary probability — that on a continuum, every
exact outcome has probability zero, yet intervals have positive probability.

## How (the spine of the video)
1. **Finite (3.2.1):** outcomes determine the law; the equally-likely special
   case Pr(A) = |A| / |Omega|. Fair die: Pr({2,3,5}) = 3/6 = 1/2. Caution: equal
   likelihood is a *modeling assumption* traceable to a symmetry, not automatic
   — the outcome approach / equiprobability bias (loaded die, biased coin, sum of
   two dice).
2. **Countably infinite (3.2.2):** a countable set is one listable in sequence
   (same cardinality as a subset of the naturals). The law assigns weights
   summing to 1. Coin tossed until first heads: Omega = {1, 2, 3, ...}, Pr(k) =
   2^-k. The weights sum to 1; Pr(even) = 1/4 + 1/16 + ... = 1/3.
3. **Uncountably infinite (3.2.3):** the law generally cannot be given by
   single-outcome probabilities (each point gets 0). Model on [0,1]: probability
   = length, Pr((a,b)) = b − a, extended to countable disjoint unions by the
   third axiom. Wheel of serendipity: angle uniform on [0, 2pi), Pr(arc) = (arc
   length) / (2pi).

## What else (connections, to seed callbacks in narration)
- The finite equally-likely model is exactly the "favorable over total" counting
  model from Chapter 2 — now named and placed in a taxonomy.
- Countable additivity (last video) is precisely what makes the infinite coin
  sum and the disjoint-interval rule legitimate.
- The length-as-probability idea is the seed of the density / integral picture;
  Pr(A) = integral over A of dx is named but its machinery is deferred.

## Conceptual progression (drives the storyboard)
finite die with primes highlighted, |A|/|Omega|  ->  caution that equal
likelihood is assumed  ->  a listable Omega = {1,2,3,...}  ->  coin-until-heads
with decaying 2^-k bars summing to 1, Pr(even) = 1/3  ->  the unit interval with
a shaded sub-interval [a,b] of length b-a, single points = 0  ->  the wheel of
serendipity, arc length over 2pi.

## Visual opportunities
- Six die faces with {2,3,5} highlighted; Pr({2,3,5}) = 3/6 = 1/2.
- A row of decaying geometric bars 2^-k (PMF-bar look), braced to sum to 1; the
  even-indexed bars highlighted summing to 1/3.
- A number-line segment [0,1] with a shaded band [a,b]; a lone point labelled
  probability 0.
- A circle (the wheel) with a highlighted arc and a pointer; Pr(arc) = arc/2pi.

## Deliberately out of scope
- The integral / density formulation beyond naming Pr(A) = integral_A dx.
- Continuity of probability and the measure-theory underpinning (the two starred
  sections that follow — named only as the bridge).
- Any treatment of the sigma-algebra of admissible events.
