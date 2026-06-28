---
introduces: [sample-space, event, probability-law, axioms-of-probability, inclusion-exclusion, union-bound, sigma-field]
requires:   [set, partition, finite-equally-likely-model, counting-principle]
---

# Basic Concepts of Probability — scratch

> Scratch/ideas only. The shipped prose lives in `basic_concepts.tex`. Not part of the LaTeX build.

## Purpose
Introduce the axiomatic framework of probability: sample spaces, events, and probability laws, then specialize the framework to finite, countably infinite, and uncountably infinite models.

## Key points / outline
- Experiment, outcome, sample space (Omega), event as an admissible subset of Omega.
- Requirements on a sample space: outcomes distinct, mutually exclusive, collectively exhaustive.
- Probability law assigns Pr(A) to each event A, subject to axioms (non-negativity, normalization, countable additivity).
- Consequences: probability of complements, monotonicity, union bounds.
- Inclusion–exclusion principle as the general formula for the probability of a union.
- Boole inequality (union bound) as a one-sided weakening.
- Finite sample spaces: equally likely model as a special case; counting reduction.
- Countably infinite models: probabilities built from a discrete distribution over a countable Omega.
- Uncountably infinite models: probabilities defined on intervals via density/length, with care about which subsets are admissible.
- Cardinality and countability (natural numbers as the benchmark); power sets push beyond countable.
- Starred preview of measure theory: fields and sigma-fields as the technically correct event class.

## Open questions
-

## Notes & references
- Ross, *A First Course in Probability*, Chapter 2.
- Bertsekas & Tsitsiklis, *Introduction to Probability*, Section 1.2.
- Miller & Childers, *Probability and Random Processes*, Sections 2.1–2.3.
- Gubner, Sections 1.1, 1.3–1.4.
