---
slug: 02-functions
title: Functions
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/02-functions.tex
source_sha256: 7480c23aa09d3ba02f274eb37b52e76b2b0eaeeea6537b6ea55b6570bf25c47e
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/sets_and_functions.tex
companion: sources/02-functions.md
companion_sha256: 7272dcb73f33386c9d37ec07e4682b0b2c1e536a1e11153dc8f8048710d7fdcf
companion_upstream: ../chapters/sets_and_functions.md
prereqs:
  - 01-sets
audience: undergraduate engineering, first probability course
concepts:
  - id: relation
    name: Relation
    importance: core
    one_liner: A relation between X and Y is any subset of the Cartesian product X x Y.
  - id: function
    name: Function as a single-valued relation
    importance: core
    one_liner: A function sends every element of X to exactly one element of Y.
  - id: domain-codomain
    name: Domain, codomain, and the rule of correspondence
    importance: core
    one_liner: f maps a domain X into a codomain Y; formally the triple (X, Y, f).
  - id: image-preimage
    name: Image, preimage, and level set
    importance: highlight
    one_liner: The preimage of a value can hold several arguments -- the seed of the random variable.
  - id: properties
    name: Injective, surjective, bijective
    importance: core
    one_liner: One-to-one, onto, and both -- the last giving an inverse function.
  - id: indicator
    name: The indicator function
    importance: core
    one_liner: 1_S maps Omega to {0,1}, reporting membership -- the seed of the Bernoulli random variable.
  - id: set-theory-and-probability
    name: Set theory and probability
    importance: highlight
    one_liner: Omega is the sample space, a partition gives total probability, a preimage gives a random variable.
estimated_runtime_sec: 600         # ~10 min target
---

# Functions — Concept Map

## What
The second half of Chapter 1: functions, built on the Cartesian product from the
Sets video. A relation between two sets is any subset of their Cartesian
product; a function is the special relation that is *single-valued* -- it sends
each input to exactly one output. From there: domain and codomain, image and
preimage (and the level set), the injective / surjective / bijective
properties, the indicator function, and a closing map of which set construct
underwrites which probability idea.

## Why (motivation for the viewer)
Functions are the bridge from "sets of outcomes" to "numbers we can compute
with." The single most important payoff is the *preimage*: because the preimage
of a value can contain many arguments, a function lets us pull a question about
numbers back to a question about the sample space -- which is exactly what a
random variable does. The indicator function is the first concrete instance, and
the seed of the Bernoulli random variable. So this video is where the
set-theoretic language of Chapter 1 starts turning into probability.

## How (the spine of the video)
1. Recall the Cartesian product; define a relation as a subset of X x Y.
2. Specialize to a function: the single-valued property, f(x) = y.
3. Domain, codomain, the notation f: X -> Y, and the formal triple (X, Y, f);
   the example f(x) = x^2.
4. Image f(X) and preimage f^{-1}(T); the level set f^{-1}({y}); show that a
   preimage of one value may hold several arguments (the x^2 picture).
5. Injective, surjective, bijective; the inverse function of a bijection.
6. The indicator function 1_S : Omega -> {0,1}.
7. Tie-back: Omega -> sample space, partition -> total probability, preimage ->
   random variable, Cartesian product -> joint distribution.

## What else (connections, to seed callbacks in narration)
- A relation is built from the Cartesian product introduced in the Sets video.
- The complement / universal set Omega from the Sets video reappears as the
  domain of the indicator function.
- The preimage is the mechanism behind random variables (Chapter 5).
- The indicator is the seed of the Bernoulli random variable.
- Bijection <=> the inverse relation is itself a function.

## Conceptual progression (drives the storyboard)
arrows from X to Y (a relation)  ->  prune to single-valued (a function)  ->
label domain / codomain  ->  the x^2 graph, a horizontal line cutting it twice
(preimage of a value = two arguments)  ->  arrow diagrams for injective /
surjective / bijective  ->  the two-valued indicator on Omega  ->  a closing
table mapping set constructs to probability ideas.

## Visual opportunities
- Two ovals X and Y with arrows; first a messy relation, then the single-valued
  function (each x has exactly one outgoing arrow).
- The parabola f(x) = x^2 with a horizontal line at height c meeting it at
  -sqrt(c) and +sqrt(c): the preimage (level set) of c has two elements.
- Side-by-side arrow diagrams contrasting injective vs not, surjective vs not.
- The indicator step function on Omega, or an Omega box with S shaded and the
  value 1 inside S, 0 outside.

## Deliberately out of scope
- The full machinery of random variables (Chapter 5) -- only previewed here via
  the preimage and the indicator.
- Continuity, limits, calculus on functions -- not needed at this level.
- Composition of functions and detailed inverse algebra beyond the bijection
  statement.
