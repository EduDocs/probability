---
slug: 10-continuity-measure
title: Continuity of Probability and a Measure-Theory View
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/10-continuity-measure.tex
source_sha256: 0390aee133c064796b1e43553c5d8a427df530f6fb48a0e2403d86c11a61bcfa
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/probability_models.tex
companion: sources/10-continuity-measure.md
companion_sha256: a85a1f30cd74d5e583096067e8b704a4e5d8a0b8b2984f995a05e92b1e62c533
companion_upstream: ../chapters/probability_models.md
prereqs:
  - 09-model-categories
audience: undergraduate engineering, first probability course
concepts:
  - id: continuity-from-below
    name: Continuity from below
    importance: core
    one_liner: For an increasing sequence A_1 ⊂ A_2 ⊂ ... with union A, Pr(A) = lim Pr(A_n); proved by slicing into disjoint shells B_k = A_k - A_{k-1} and applying countable additivity.
  - id: continuity-from-above
    name: Continuity from above
    importance: core
    one_liner: For a decreasing sequence A_1 ⊃ A_2 ⊃ ... with intersection A, Pr(A) = lim Pr(A_n); obtained from continuity-from-below applied to the complements. Together the two are the continuity of probability.
  - id: measure-theory
    name: Probability and measure theory
    importance: supporting
    one_liner: On an uncountable Omega you cannot assign a probability to *every* subset; probability is defined on a sigma-field of admissible events, the subject of measure theory, which unifies the discrete and the continuous.
estimated_runtime_sec: 300        # ~5 min (starred coda)
---

# Continuity of Probability and a Measure-Theory View — Concept Map

# What
Sections 3.2.4 and 3.2.5 of Chapter 3 — the two **starred** sections that round
out the probabilistic model. **Continuity of probability** is the statement that
probability respects limits of monotone sequences of events: if the events grow
(an increasing sequence) up to a limit set, or shrink (a decreasing sequence)
down to one, the probabilities converge to the probability of the limit. The
**measure-theory** section is a candid, non-rigorous signpost: on an uncountable
sample space it is *impossible* to consistently assign a probability to every
subset, so probability is really defined on a restricted collection of "nice"
events — a sigma-field — and the machinery that makes this precise is measure
theory.

# Why it matters
These two sections are where the axioms stop being bookkeeping rules and start
behaving like analysis. Continuity from below/above is the workhorse that lets
us pass to limits — it is exactly what justifies statements like "the
probability that the process *eventually* succeeds is the limit of the
finite-horizon probabilities." The measure-theory aside is honest about the
ceiling of the elementary theory: it tells the student *why* a more advanced
treatment exists and what it buys (a single framework for discrete and
continuous models) without demanding the student learn it now.

# Key ideas (in dependency order)
1. **Monotone sequences of events.** Increasing: A_1 ⊂ A_2 ⊂ ... with limit
   A = ∪ A_k. Decreasing: A_1 ⊃ A_2 ⊃ ... with limit A = ∩ A_k.
2. **Continuity from below.** Pr(A) = lim_{n→∞} Pr(A_n) for an increasing
   sequence. Proof: disjointify — B_1 = A_1, B_k = A_k − A_{k−1}; the B_k are
   disjoint, ∪_{k≤n} B_k = A_n and ∪_k B_k = A, so countable additivity gives
   Pr(A) = Σ Pr(B_k) = lim Σ_{k≤n} Pr(B_k) = lim Pr(A_n).
3. **Continuity from above.** Pr(A) = lim Pr(A_n) for a decreasing sequence;
   apply continuity from below to the complements A_k^c (which increase) and use
   the complement rule. The pair is *the continuity of probability*.
4. **The cardinality ladder.** finite → countably infinite (listable as
   s_1, s_2, ...; integers, rationals) → uncountable (the reals; cannot be
   listed). Intuition climbs the ladder one rung at a time.
5. **Why not every subset?** Trying to assign a probability to *every* subset of
   an uncountable Omega leads to unresolvable contradictions. One must restrict
   to a subclass of "admissible" events — a field / sigma-field.
6. **Measure-theoretic probability.** sigma-fields and measures are the subject
   of measure theory; measure-theoretic probability gives a unified treatment of
   the discrete and the continuous. (Stated, not developed.)

# Visual plan (beats)
- **overview** — recap (three families of models), then the two-item outline:
  continuity of probability, and a measure-theory view. Mark both as starred.
- **continuity-from-below** — nested growing regions A_1 ⊂ A_2 ⊂ ... filling a
  limit A; the disjoint-shell decomposition B_k = A_k − A_{k−1}; the statement
  Pr(A) = lim Pr(A_n) with the one-line proof.
- **continuity-from-above** — nested shrinking regions A_1 ⊃ A_2 ⊃ ... closing
  down to A = ∩ A_k; "take complements" to reuse the previous result; name the
  pair the continuity of probability.
- **measure-theory** — the finite/countable/uncountable cardinality ladder; the
  "can we weigh every subset?" question answered *no* for the continuum; the
  sigma-field of admissible events; closing key idea + chapter close.

# Notation (per project.yaml)
- Pr(·) for probability, written \Pr in LaTeX (never blackboard-bold P).
- Unions/intersections \bigcup, \bigcap; complement A^{\mathrm{c}}.
- Limits \lim_{n \to \infty}.

# Out of scope / cut first
- Any actual construction of a sigma-field or a measure (signposted only).
- The Vitali / non-measurable-set construction (mentioned only as "contradictions").
- Continuity stated for general (non-monotone) sequences.
