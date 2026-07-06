---
slug: 01-sets
title: Sets
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/01-sets.tex
source_sha256: 59944a8561c362cc895bc69b53687751333071b8e0fbe589d0db2f09b215c17f
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/sets_and_functions.tex
companion: sources/01-sets.md
companion_sha256: 23e302453063904227fd401d8691d0806a24f8f20f633101e400b9b3fbc50f41
companion_upstream: ../chapters/sets_and_functions.md
audience: undergraduate engineering, first probability course
concepts:
  - id: set-membership
    name: Sets, elements, and subsets
    importance: core
    one_liner: A set is a collection of objects; membership, equality, and subset relate them.
  - id: set-builder
    name: Specifying a set
    importance: core
    one_liner: List the elements, or carve a subset with set-builder notation.
  - id: special-sets
    name: Empty set, universal set, complement
    importance: core
    one_liner: The empty set has nothing; the universal set Omega is everything in context; the complement is everything outside a set.
  - id: operations
    name: Union, intersection, difference, disjointness
    importance: core
    one_liner: The elementary operations that combine two sets, read off a Venn diagram.
  - id: partition
    name: Partition
    importance: highlight
    one_liner: Disjoint nonempty pieces whose union is the whole set -- the seed of total probability.
  - id: rules
    name: Precedence, distributive laws, De Morgan's laws
    importance: core
    one_liner: The algebra of sets, and how complement turns union into intersection.
  - id: cartesian-product
    name: Cartesian product
    importance: core
    one_liner: All ordered pairs (x, y) -- the way to build a new set from two existing ones.
estimated_runtime_sec: 600         # ~10 min target
---

# Sets — Concept Map

## What
The set-theoretic language that the whole probability course is built on, at the
naive-set-theory level. A set is a collection of objects; from membership we
build subsets, the special sets (empty, universal, complement), the elementary
operations (union, intersection, difference), partitions, the algebraic laws
(distributive, De Morgan), and finally the Cartesian product. This is the first
of two videos drawn from Chapter 1; the second covers functions.

## Why (motivation for the viewer)
Probability is an axiomatic theory written in the language of sets. Before we can
say what an event is, or what it means to condition on information, we need a
precise vocabulary for collections of outcomes. Every later idea has a
set-theoretic shadow: the universal set becomes the sample space, a partition
underlies the law of total probability, and the Cartesian product lets us talk
about several quantities at once. Getting fluent here pays off for the entire
course.

## How (the spine of the video)
1. A set as a collection of elements; membership, equality, subset, proper subset.
2. Two ways to specify a set: listing, and set-builder notation.
3. The special sets: empty set, universal set Omega (the sample space), complement.
4. The elementary operations on two sets, read off Venn diagrams: union,
   intersection, disjointness, difference.
5. Partition -- disjoint pieces tiling the whole set (teaser: total probability).
6. The algebra: precedence, the distributive laws, and De Morgan's laws
   (two-set and indexed forms).
7. The Cartesian product as ordered pairs -- a grid built from two small sets.

## What else (connections, to seed callbacks in narration)
- Omega is introduced here as the universal set and explicitly named the *sample
  space* -- the single most reused object in the course.
- A partition is exactly the structure behind the law of total probability
  (Chapter 4).
- The Cartesian product foreshadows joint distributions and random vectors.
- This video deliberately stops before functions; the preimage-as-random-variable
  payoff lands in the companion Functions video.

## Conceptual progression (drives the storyboard)
collection of balls in a box  ->  carve out subsets  ->  the complement fills
the rest of Omega  ->  two overlapping circles shade into union / intersection /
difference  ->  the circles tile into a partition  ->  De Morgan flips a shaded
region  ->  two little sets multiply into a grid of ordered pairs.

## Visual opportunities
- An Omega ellipse with colored, numbered balls (mirrors the book's opening
  figure).
- Venn diagrams with boolean-op shading for each operation, on a fixed pair of
  circles so the regions are directly comparable.
- A partition shown as a disk sliced into disjoint colored wedges.
- De Morgan animated: shade the complement of a union, then morph to the
  intersection of the complements over the *same* circles.
- A Cartesian product drawn as a 3x2 grid of paired balls from {1,2,3} x {a,b}.

## Deliberately out of scope
- Functions, relations, image/preimage, injective/surjective/bijective, and the
  indicator function -- all reserved for the second video (Functions).
- Countable vs. uncountable -- developed later, in Probability Models, where it
  is motivated.
- Any measure theory; this stays at the naive-set-theory level, by design.
