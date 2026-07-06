---
slug: 03-counting-principle
title: The Counting Principle
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/03-counting-principle.tex
source_sha256: 89f6242bfc55652aff4bf045a23070d126be93b694263a7d7bb064b96d39be88
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/combinatorics.tex
companion: sources/03-counting-principle.md
companion_sha256: 3975ab2c65c197a52bc419a814356b63159df0f57ebee864f5bb421fea0f2cc8
companion_upstream: ../chapters/combinatorics.md
prereqs:
  - 01-sets
  - 02-functions
audience: undergraduate engineering, first probability course
concepts:
  - id: equally-likely
    name: The finite equally-likely model
    importance: core
    one_liner: When outcomes are finite and equally likely, probability is favorable over total.
  - id: counting-principle
    name: The counting principle
    importance: core
    one_liner: The Cartesian product of an m-set and an n-set has m times n elements.
  - id: independence-teaser
    name: Joint experiments and independence (informal)
    importance: optional
    one_liner: Combining unrelated experiments multiplies their probabilities -- a first, informal taste of independence.
  - id: multistage
    name: Multi-stage experiments and sampling with replacement
    importance: core
    one_liner: r stages with n_i choices each give n_1 n_2 ... n_r outcomes; drawing k times from n with replacement gives n^k.
  - id: power-set
    name: Counting subsets (the power set)
    importance: highlight
    one_liner: A set with n elements has 2^n subsets -- one yes/no choice per element.
estimated_runtime_sec: 420         # ~7 min target (the shortest of the four)
---

# The Counting Principle — Concept Map

# What
The opening of Chapter 2 (Combinatorics): the simplest probability model and the
first counting tool. When a sample space is finite and its outcomes are equally
likely, the probability of an event is just the count of favorable outcomes over
the total count. So probability reduces to counting -- and the counting
principle is the foundational rule: the number of elements in a Cartesian
product is the product of the sizes. From there: multi-stage experiments
(n_1 n_2 ... n_r), sampling with replacement (n^k), and counting subsets (2^n).

## Why (motivation for the viewer)
This is where probability becomes computable for the first time. The equally-
likely model turns "what is the chance" into "count two things and divide" -- but
the counting is often the hard part, which is exactly what combinatorics is for.
The counting principle is the engine behind every later count in the chapter, and
it rests directly on the Cartesian product from the Sets video, so this is a
natural next step that pays its setup forward.

## How (the spine of the video)
1. The finite equally-likely model: P(event) = favorable / total; the fair die.
2. The counting principle: |S x T| = |S| |T|, read off the product grid; coin
   and die give 2 x 6 = 12.
3. (Light) joint experiments: combining unrelated experiments multiplies the
   per-experiment probabilities -- an informal first look at independence.
4. Multi-stage: r sets give n_1 n_2 ... n_r; sampling k times with replacement
   from n balls gives n^k.
5. Counting subsets: a set with n elements has 2^n subsets (one yes/no per
   element) -- a callback to the indicator function from the Functions video.

## What else (connections, to seed callbacks in narration)
- The counting principle is the Cartesian product of the Sets video, now counted.
- The 2^n subsets count is exactly "one indicator bit per element" -- the
  indicator function from the Functions video.
- n^k (sampling with replacement, ordered) is the first cell of the sampling
  table that the fourth video assembles.
- Independence is named only informally here; the precise definition is deferred
  to the conditional-probability chapter (do not over-claim).

## Conceptual progression (drives the storyboard)
a die with a highlighted event (3 of 6 faces)  ->  the {1,2,3} x {a,b} grid
counted as 3 x 2 = 6  ->  coin x die = 2 x 6 = 12  ->  an urn drawn k times,
n^k sequences  ->  three elements each flipped in/out, 2^3 = 8 subsets.

## Visual opportunities
- A die face grid with the prime outcomes {2,3,5} highlighted; P = 3/6.
- The Cartesian product grid (reuse the Sets-video grid style): 3 x 2 = 6.
- A small tree / product for coin x die -> 12.
- An urn with numbered balls; k draw-slots; n^k.
- Three elements with yes/no toggles enumerating the 8 subsets of {1,2,3}.

## Deliberately out of scope
- Permutations, combinations, the binomial theorem (next video).
- The formal probability axioms and inclusion-exclusion (later chapter).
- A precise definition of independence (conditional-probability chapter) -- only
  an informal multiplicative teaser here.
