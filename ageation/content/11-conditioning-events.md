---
slug: 11-conditioning-events
title: Conditioning on Events
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/11-conditioning-events.tex
source_sha256: 06a6b3017505d1b38097fa3b77de3dccd518a7f4fa89e43e1bda8552febd7727
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/conditional_probability.tex
companion_upstream: ../chapters/conditional_probability.md
companion: sources/11-conditioning-events.md
companion_sha256: 0e811c327b6ab7615027fd584a481db08ff072be3f16ceeff7969f130a2aac2d
prereqs:
  - 10-continuity-measure
audience: undergraduate engineering, first probability course
concepts:
  - id: conditional-probability
    name: Conditional probability
    importance: core
    one_liner: For an event B with Pr(B) > 0, the conditional probability Pr(A | B) = Pr(A ∩ B) / Pr(B) re-normalizes the law to the world where B is known to have happened.
  - id: valid-conditional-law
    name: The conditional law is a probability law
    importance: supporting
    one_liner: The collection {Pr(A | B)} satisfies the three axioms (nonnegativity, Pr(Ω | B) = 1, countable additivity), so conditioning yields a bona fide probability law on Omega.
  - id: chain-rule
    name: The chain rule (multiplication rule)
    importance: core
    one_liner: Pr(A_1 ∩ ... ∩ A_n) = Pr(A_1) Pr(A_2 | A_1) ... Pr(A_n | A_1 ∩ ... ∩ A_{n-1}) — the probability of a sequence of events built one conditioning step at a time.
estimated_runtime_sec: 420        # ~7 min
---

# Conditioning on Events — Concept Map

# What
The chapter introduction and Section 4.1. **Conditional probability** is the
mechanism for updating a probability when partial information arrives: once we
learn that the outcome lies in an event `B`, the likelihood of any event `A`
becomes `Pr(A | B) = Pr(A ∩ B) / Pr(B)` (defined whenever `Pr(B) > 0`).
Geometrically, conditioning *zooms in* on `B` and re-normalizes so that `B`
carries all the probability. Two motivations precede the definition — the
equally-likely die and a frequentist counting argument — and then we show the
conditional law is itself a valid probability law and derive the **chain rule**
for the probability of several events occurring together.

# Why it matters
Conditioning is the single most important computational move in the subject:
every later result in the chapter — total probability, Bayes' rule, independence
— is built on it. It is also the formal model of *learning from evidence*, which
is why it reaches so far into engineering, inference, and decision-making. The
chain rule is the everyday tool for sequential experiments (draws without
replacement, multi-stage processes) where each step's probability depends on
what came before.

# Key ideas (in dependency order)
1. **Motivation 1 — the fair die.** Six equally likely faces; told the face is
   odd, only {1, 3, 5} survive and stay equally likely, so Pr(3 | odd) = 1/3.
   Conditioning re-normalizes over the surviving outcomes.
2. **Motivation 2 — frequentist counting.** Over N trials,
   Pr(A | B) ≈ N_AB / N_B = (N_AB / N) / (N_B / N) → Pr(A ∩ B) / Pr(B) as N → ∞.
   The ratio of relative frequencies is the definition in the limit.
3. **Definition.** For Pr(B) > 0, Pr(A | B) = Pr(A ∩ B) / Pr(B).
4. **The conditional law is valid.** {Pr(A | B)} obeys the three axioms:
   nonnegativity (a ratio of nonnegatives), Pr(Ω | B) = Pr(B)/Pr(B) = 1, and
   countable additivity (disjoint A_k give disjoint A_k ∩ B). A worked check:
   coin tossed until first heads, Pr(2 | even) = (1/4)/(1/3) = 3/4.
5. **Chain rule.** Pr(A_1 ∩ ... ∩ A_n) = Pr(A_1) Pr(A_2 | A_1) ...
   Pr(A_n | A_1 ∩ ... ∩ A_{n-1}); telescoping ratios cancel to prove it.
6. **Application.** Urn with 8 green and 4 gray balls, three draws without
   replacement, Pr(ggg) = (8/12)(7/11)(6/10) = 14/55.

# Visual plan (beats)
- **overview** — recap (the probabilistic model: sample space + law), then the
  chapter outline: conditioning, total probability, Bayes' rule, independence.
- **conditioning** — the fair-die re-normalization ({1,…,6} collapsing to
  {1,3,5}); the frequentist N-trials ratio; land the definition
  Pr(A | B) = Pr(A ∩ B) / Pr(B) as the accent equation.
- **valid-law** — the three axioms re-checked for the conditional law (Ω | B = 1
  is the memorable one); the coin-until-heads Pr(2 | even) = 3/4 example.
- **chain-rule** — the telescoping product; the urn-draw tree
  (8/12 → 7/11 → 6/10) giving Pr(ggg) = 14/55.

# Notation (per project.yaml)
- Pr(·) for probability, written \Pr (never blackboard-bold P).
- Conditioning bar \mid; intersection \cap; union \bigcup.
- Complement A^{\mathrm{c}}.

# Out of scope / cut first
- The full epsilon-level proof that the conditional law is countably additive
  (state the axiom check, show Ω | B = 1, gesture at the rest).
- The "equivalent notations" section (comma-for-intersection) — deferred; used
  silently later.
