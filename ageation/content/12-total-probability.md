---
slug: 12-total-probability
title: The Total Probability Theorem
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/12-total-probability.tex
source_sha256: 06a6b3017505d1b38097fa3b77de3dccd518a7f4fa89e43e1bda8552febd7727
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/conditional_probability.tex
companion_upstream: ../chapters/conditional_probability.md
companion: sources/12-total-probability.md
companion_sha256: 0e811c327b6ab7615027fd584a481db08ff072be3f16ceeff7969f130a2aac2d
prereqs:
  - 11-conditioning-events
audience: undergraduate engineering, first probability course
concepts:
  - id: partition-recap
    name: Partition of the sample space
    importance: supporting
    one_liner: A collection A_1, ..., A_n is a partition of Omega when the sets are disjoint and their union is all of Omega — the scaffolding the theorem stands on.
  - id: total-probability-theorem
    name: Total probability theorem
    importance: core
    one_liner: For a partition {A_k} with Pr(A_k) > 0, Pr(B) = Σ Pr(A_k) Pr(B | A_k) — the unconditional probability of B is the weighted average of its conditional probabilities across the partition.
estimated_runtime_sec: 360        # ~6 min
---

# The Total Probability Theorem — Concept Map

# What
Section 4.2. Starting from the two-event product rule
`Pr(A ∩ B) = Pr(B | A) Pr(A)`, the **total probability theorem** computes the
unconditional probability of an event `B` by splitting the sample space into a
**partition** `A_1, …, A_n` (disjoint pieces whose union is Ω) and summing the
contributions: `Pr(B) = Σ Pr(A_k) Pr(B | A_k)`. It is the "divide and conquer"
law — break a hard probability into easy conditional cases, weight each by how
likely its case is, and add.

# Why it matters
This is the workhorse for any problem with natural *scenarios* or *causes* — pick
an urn then draw, choose a channel then transmit, select a machine then sample
its output. It is also the engine that makes Bayes' rule computable: the
denominator in Bayes' rule is exactly a total-probability sum. Conceptually it
teaches the student to *set up* a problem by conditioning on the right partition.

# Key ideas (in dependency order)
1. **Two-event product rule.** Pr(A ∩ B) = Pr(B | A) Pr(A) — a one-line
   rearrangement of the definition of conditional probability, and the special
   case n = 1 of the chain rule.
2. **Partition of Omega.** A_1, …, A_n disjoint with ∪ A_k = Ω. Every outcome
   lands in exactly one piece.
3. **Decomposition of B.** B = B ∩ Ω = ∪_k (B ∩ A_k), a *disjoint* union, so by
   the third axiom Pr(B) = Σ Pr(B ∩ A_k).
4. **Conditional form.** Rewrite each slice with the product rule:
   Pr(B ∩ A_k) = Pr(A_k) Pr(B | A_k), giving
   Pr(B) = Σ Pr(A_k) Pr(B | A_k) — a weighted average of conditionals.
5. **Application (divide and conquer).** Urn 1 has 5 green / 3 red, urn 2 has
   3 green / 9 red; pick an urn at random then draw. Pr(green)
   = (5/8)(1/2) + (3/12)(1/2) = 7/16.

# Visual plan (beats)
- **overview** — recap (conditional probability + chain rule), then the goal:
  compute an unconditional probability by conditioning on cases.
- **partition** — a rectangle Omega sliced into disjoint colored pieces
  A_1, A_2, A_3 tiling it exactly; the definition (disjoint + union = Omega).
- **theorem** — overlay an event B across the pieces; decompose into the disjoint
  slices B ∩ A_k; the sum Pr(B) = Σ Pr(A_k) Pr(B | A_k), and the one-line proof
  chain (B = ∪ (B ∩ A_k) → axiom 3 → product rule).
- **example** — the two-urn tree: branch on the urn (1/2 each), then the green
  probability in each (5/8, 3/12); combine to 7/16.

# Notation (per project.yaml)
- Pr(·) for probability, written \Pr (never blackboard-bold P).
- Conditioning bar \mid; intersection \cap; union \bigcup; sum \sum.

# Out of scope / cut first
- The countably-infinite partition case (state for finite n; the sum extends).
- A second worked example — one clean urn problem carries the idea.
