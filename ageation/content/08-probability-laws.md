---
slug: 08-probability-laws
title: Probability Laws
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/08-probability-laws.tex
source_sha256: 0390aee133c064796b1e43553c5d8a427df530f6fb48a0e2403d86c11a61bcfa
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/probability_models.tex
companion: sources/08-probability-laws.md
companion_sha256: a85a1f30cd74d5e583096067e8b704a4e5d8a0b8b2984f995a05e92b1e62c533
companion_upstream: ../chapters/probability_models.md
prereqs:
  - 07-sample-spaces
audience: undergraduate engineering, first probability course
concepts:
  - id: three-axioms
    name: The three axioms of probability
    importance: core
    one_liner: A probability law assigns each event a number satisfying nonnegativity, normalization, and (countable) additivity.
  - id: complement-monotonicity
    name: Complement rule and monotonicity
    importance: core
    one_liner: Pr(A^c) = 1 - Pr(A), Pr(empty) = 0, and A subset B implies Pr(A) <= Pr(B) -- all forced by the axioms.
  - id: union-formula
    name: The union of two events
    importance: core
    one_liner: Pr(A union B) = Pr(A) + Pr(B) - Pr(A intersect B); generalizes to inclusion-exclusion.
  - id: union-bound
    name: The union bound (Boole's inequality)
    importance: highlight
    one_liner: Pr(union A_k) <= sum Pr(A_k) -- the workhorse bound when joints are hard but individuals are easy.
estimated_runtime_sec: 570        # ~9.5 min target (the chapter's heavyweight)
---

# Probability Laws — Concept Map

# What
Section 3.2 of Chapter 3 (Probability Models): the axiomatic core of the whole
course. A *probability law* (also called a *probability measure*) is the rule
that assigns every event A a number Pr(A) obeying just three axioms —
**nonnegativity** (Pr(A) >= 0), **normalization** (Pr(Omega) = 1), and
**additivity** (disjoint events' probabilities add, finitely and then
countably). From those three, everything else follows by short deductions: the
complement rule, the impossible event having probability zero, monotonicity,
the two-event union formula, and the union bound.

## Why (motivation for the viewer)
This is the moment probability stops being "favorable over total" and becomes a
deductive theory that works on any sample space — finite, countably infinite, or
uncountable. The three axioms are the entire foundation; every manipulation a
student will ever do with probabilities is licensed by one of them. Showing the
consequences *derived* (rather than asserted) is the point: it teaches that the
rules are not arbitrary, they are forced.

## How (the spine of the video)
1. The three axioms: Pr assigns a number to each event; nonnegativity,
   normalization, additivity. Dwell on finite disjoint additivity, then
   generalize to countable additivity (an infinite disjoint sequence whose
   masses sum to the whole). Aside: "probability law" = "probability measure".
2. Consequences: the complement rule Pr(A^c) = 1 - Pr(A) (A and A^c disjoint,
   exhaust Omega); corollary Pr(empty) = 0; monotonicity A subset B => Pr(A) <=
   Pr(B) via B = A union (B - A). Aside: the conjunction fallacy.
3. The union of two events: Pr(A union B) = Pr(A) + Pr(B) - Pr(A intersect B)
   (Venn; subtract the double-counted lens); one line on inclusion-exclusion.
4. The union bound: Pr(union A_k) <= sum Pr(A_k) (induction idea), with the
   990-blue / 10-red urn worked example: bound 1/20 vs exact ~0.049.

## What else (connections, to seed callbacks in narration)
- Disjointness and partitions come straight from the Sets video; additivity is
  why disjointness mattered.
- "Probability measure" is a forward pointer to the starred measure-theory
  section at the end of the chapter.
- The union bound is the first genuinely useful *inequality* of the course; it
  recurs throughout (concentration, reliability, the probabilistic method).

## Conceptual progression (drives the storyboard)
an event shaded as mass inside Omega, Pr(Omega)=1  ->  two disjoint blobs whose
masses add  ->  an infinite shrinking partition summing to 1  ->  A and its
complement filling Omega  ->  nested A subset B  ->  two overlapping circles with
the lens subtracted  ->  an urn of 990 blue + 10 red, bound vs exact.

## Visual opportunities
- Omega box with a shaded event "mass"; the three axioms listed alongside.
- Two disjoint shaded regions; then a unit bar split into 1/2, 1/4, 1/8, ...
- Complement region shaded; nested circles with the ring B - A shaded.
- Two overlapping circles, the intersection lens highlighted then subtracted.
- An urn (mostly blue, a few red) with 5 draw slots; bound 1/20 vs exact 0.049.

## Deliberately out of scope
- Conditional probability and independence (later chapter).
- The formal measure-theoretic construction of admissible events / sigma-algebra
  (the starred section; only named here).
- The full inclusion-exclusion formula for n events (stated in one line, not
  derived).
