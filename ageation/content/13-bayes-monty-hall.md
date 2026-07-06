---
slug: 13-bayes-monty-hall
title: Bayes' Rule and the Monty Hall Problem
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/13-bayes-monty-hall.tex
source_sha256: 06a6b3017505d1b38097fa3b77de3dccd518a7f4fa89e43e1bda8552febd7727
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/conditional_probability.tex
companion_upstream: ../chapters/conditional_probability.md
companion: sources/13-bayes-monty-hall.md
companion_sha256: 0e811c327b6ab7615027fd584a481db08ff072be3f16ceeff7969f130a2aac2d
prereqs:
  - 12-total-probability
audience: undergraduate engineering, first probability course
concepts:
  - id: bayes-rule
    name: Bayes' rule
    importance: core
    one_liner: For a partition {A_k}, Pr(A_i | B) = Pr(A_i) Pr(B | A_i) / Σ_k Pr(A_k) Pr(B | A_k) — it inverts the direction of conditioning, computing Pr(A_i | B) from the likelihoods Pr(B | A_i) and the priors.
  - id: prior-posterior-likelihood
    name: Prior, posterior, likelihood
    importance: core
    one_liner: Pr(A_i) is the prior (before evidence), Pr(A_i | B) the posterior (after evidence), Pr(B | A_i) the likelihood; Bayes' rule is the recipe for turning priors into posteriors in light of evidence.
  - id: base-rate-fallacy
    name: Base-rate fallacy & confusion of the inverse
    importance: supporting
    one_liner: Pr(A | B) and Pr(B | A) answer different questions and are generally unequal; neglecting the prior (the base rate) makes an accurate test look far more informative than it is — the disease test yields Pr(D | P) ≈ 0.16.
  - id: monty-hall
    name: The Monty Hall problem
    importance: core
    one_liner: Asymmetric likelihoods Pr(H | C_1) = 1/2, Pr(H | C_2) = 1, Pr(H | C_3) = 0 drive Bayes' rule to posteriors 1/3 (stay) vs 2/3 (switch); the host's constraint makes the opened door anything but neutral.
estimated_runtime_sec: 480        # ~8 min
---

# Bayes' Rule and the Monty Hall Problem — Concept Map

# What
Section 4.3. **Bayes' rule** runs conditioning *backwards*: it computes the
posterior `Pr(A_i | B)` from the likelihoods `Pr(B | A_i)` and the priors
`Pr(A_i)`, with the denominator supplied by the total probability theorem. The
video names the inference vocabulary (prior / posterior / likelihood), warns
against the two reasoning errors the rule exposes (**confusion of the inverse**
and the **base-rate fallacy**, dramatized by a highly accurate disease test that
still gives only a 16% posterior), and closes with the **Monty Hall problem** as
a capstone where Bayes' rule resolves a famously counterintuitive puzzle.

# Why it matters
Bayes' rule is the mathematical core of inference: diagnosis, spam filtering,
sensor fusion, and machine learning all rest on it. Just as important is the
*intuition repair* — the base-rate fallacy and confusion of the inverse are
among the most consequential reasoning errors in medicine and law (the
prosecutor's fallacy). Monty Hall is the canonical demonstration that careful
conditioning beats gut feeling.

# Key ideas (in dependency order)
1. **Inversion.** Pr(A_i ∩ B) = Pr(A_i | B) Pr(B) = Pr(B | A_i) Pr(A_i);
   rearrange to Pr(A_i | B) = Pr(A_i) Pr(B | A_i) / Pr(B).
2. **Bayes' rule.** Expand Pr(B) by total probability:
   Pr(A_i | B) = Pr(A_i) Pr(B | A_i) / Σ_k Pr(A_k) Pr(B | A_k).
3. **Vocabulary.** prior Pr(A_i); posterior Pr(A_i | B); likelihood Pr(B | A_i).
   Bayes turns priors into posteriors in light of evidence.
4. **Confusion of the inverse.** Pr(A | B) ≠ Pr(B | A) in general; swapping them
   is the courtroom "prosecutor's fallacy."
5. **Disease test / base-rate fallacy.** 95% accurate both ways, 1% prevalence.
   Pr(D | P) = (0.01·0.95) / (0.01·0.95 + 0.99·0.05) ≈ 0.161. The false positives
   from the healthy 99% swamp the true positives; the prior is decisive.
6. **Monty Hall.** Car uniform over 3 doors; pick door 1, host opens door 3
   (event H) always showing a goat. Likelihoods Pr(H | C_1) = 1/2,
   Pr(H | C_2) = 1, Pr(H | C_3) = 0; total probability Pr(H) = 1/2; Bayes gives
   Pr(C_1 | H) = 1/3 (stay), Pr(C_2 | H) = 2/3 (switch). Switching doubles the
   odds because the host's constraint transfers door 3's share onto door 2.

# Visual plan (beats)
- **overview** — recap (total probability), then the goal: invert conditioning to
  update beliefs from evidence; tease Monty Hall.
- **bayes-rule** — the two-line derivation from the product rule; the general
  formula with the total-probability denominator; label prior / posterior /
  likelihood in accent.
- **pitfalls** — Pr(A | B) ≠ Pr(B | A) (confusion of the inverse); the disease
  test computation landing on ≈ 0.16; a small population grid (1% ill) making the
  base-rate fallacy visible; name it.
- **monty-hall** — three doors; the pick and the host's reveal; the likelihood
  table; Bayes to 1/3 vs 2/3; the "switch" punchline with the probability-mass
  transfer.

# Notation (per project.yaml)
- Pr(·) for probability, written \Pr (never blackboard-bold P).
- Conditioning bar \mid; complement A^{\mathrm{c}}; sum \sum; product \prod.

# Out of scope / cut first
- The general n-hypothesis prosecutor's-fallacy discussion (name it, move on).
- A formal proof that switching is optimal for any host bias (fix the unbiased
  1/2 case).
