---
slug: 07-sample-spaces
title: Sample Spaces and Events
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/07-sample-spaces.tex
source_sha256: 0390aee133c064796b1e43553c5d8a427df530f6fb48a0e2403d86c11a61bcfa
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/probability_models.tex
companion: sources/07-sample-spaces.md
companion_sha256: a85a1f30cd74d5e583096067e8b704a4e5d8a0b8b2984f995a05e92b1e62c533
companion_upstream: ../chapters/probability_models.md
prereqs:
  - 06-sampling
audience: undergraduate engineering, first probability course
concepts:
  - id: experiment-outcome
    name: Experiment, outcome, and the sample space
    importance: core
    one_liner: An experiment is a random occurrence with one of several outcomes; the set of all outcomes is the sample space Omega.
  - id: event
    name: Events as admissible subsets
    importance: core
    one_liner: An event is an admissible subset of the sample space; for a die, Omega = {1,...,6} and {2,3,5} (the primes) is one event.
  - id: choosing-sample-space
    name: One experiment, many sample spaces
    importance: core
    one_liner: The same experiment admits different sample spaces -- n coin tosses can be modelled as {0,...,n} heads or as 2^n full histories; the choice depends on what you analyze.
  - id: sample-space-rules
    name: The two rules a sample space must obey
    importance: highlight
    one_liner: Outcomes must be distinct and mutually exclusive (so the outcome is unique) and collectively exhaustive (every outcome accounted for); {odd, even, prime} fails, {odd, even} works.
estimated_runtime_sec: 360         # ~6 min (the chapter opener)
---

# Sample Spaces and Events — Concept Map

## What
The opening of Chapter 3 (Probability Models): the first half of the framework
on which all of probability rests. A probabilistic model has two components, a
sample space and a probability law; this video builds the sample space. An
*experiment* is a random occurrence that produces one of several *outcomes*. The
set of all possible outcomes is the *sample space*, written Omega. An *event* is
an *admissible subset* of Omega. The same experiment can be modelled by different
sample spaces, and a valid sample space must satisfy two rules: its outcomes are
distinct and mutually exclusive, and collectively exhaustive.

## Why (motivation for the viewer)
We spent Chapter 2 counting outcomes; now we name the objects those counts live
on. Before any probability can be assigned, you have to pin down *what can
happen* -- the sample space -- and *which collections of happenings you want to
ask about* -- the events. Getting this scaffolding right (no overlaps, no gaps)
is exactly what makes the probability law in the next video well-defined.

## How (the spine of the video)
1. Experiment -> outcomes -> sample space Omega; an event is an admissible
   subset. The book's ball-in-box figure: a box of colored outcomes, one tagged
   as the observed outcome, a dashed loop tagging an event.
2. The die instance: Omega = {1,...,6}; the event {2,3,5} (the primes); the
   number actually rolled is the outcome.
3. One experiment, many sample spaces: n coin tosses as {0,...,n} (number of
   heads) versus 2^n full head/tail histories. The choice depends on the
   property you wish to analyze.
4. The two rules: (1) distinct and mutually exclusive -> the outcome is unique;
   (2) collectively exhaustive -> every outcome accounted for. Contrast
   {odd, even, prime} (overlaps: 3,5 odd and prime; 2 prime and even -> not
   admissible) with {odd, even} (disjoint and exhaustive -> admissible).

## What else (connections, to seed callbacks in narration)
- Omega is the universal set from the Sets video, now wearing its probability
  name (the sample space, glossed back in Chapter 1).
- An event is a subset of Omega -- the subset idea from the Sets video.
- "Distinct, mutually exclusive, exhaustive" is exactly a *partition* of Omega
  (Chapter 1 / Chapter 5) when the outcomes are lumped into groups.
- This is half of a probabilistic model; the probability law (the axioms) is the
  next video.

## Conceptual progression (drives the storyboard)
a box of colored outcome-balls with one tagged "outcome" and a dashed-loop
"event"  ->  the die: Omega = {1,...,6} with the loop around {2,3,5}  ->  the
same n-coin experiment under two sample spaces, {0,...,n} vs 2^n histories  ->
the {odd, even, prime} overlap (not admissible) beside the {odd, even} partition
(admissible).

## Visual opportunities
- The Omega-box with scattered colored balls; an arrow tagging one "outcome" and
  a dashed ellipse tagging an "event" (reuse the Sets-video Omega-box + loop).
- The die: six numbered balls in Omega, a dashed loop around 2, 3, 5.
- Two stacked sample spaces for the same coin experiment: {0,...,n} on one side,
  a column of HHT... sequences (2^n) on the other.
- A two-panel contrast: overlapping odd/even/prime blobs (with 2, 3, 5 caught in
  two blobs) versus two clean disjoint odd/even regions tiling {1,...,6}.

## Deliberately out of scope
- The probability law and the axioms of probability (next video).
- Conditional probability, independence, and any numerical probabilities beyond
  the equally-likely teaser already seen in Chapter 2.
- Sigma-algebras / measurability ("admissible" is kept informal at this level).
