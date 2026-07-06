---
slug: 14-independence
title: Independence
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/14-independence.tex
source_sha256: 06a6b3017505d1b38097fa3b77de3dccd518a7f4fa89e43e1bda8552febd7727
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/conditional_probability.tex
companion_upstream: ../chapters/conditional_probability.md
companion: sources/14-independence.md
companion_sha256: 0e811c327b6ab7615027fd584a481db08ff072be3f16ceeff7969f130a2aac2d
prereqs:
  - 13-bayes-monty-hall
audience: undergraduate engineering, first probability course
concepts:
  - id: independence-two-events
    name: Independence of two events
    importance: core
    one_liner: A and B are independent when Pr(A ∩ B) = Pr(A) Pr(B); equivalently Pr(A | B) = Pr(A) — knowing B carries no information about A. Independence is symmetric and is NOT the same as mutual exclusivity.
  - id: independence-multiple-events
    name: Independence of multiple events
    importance: core
    one_liner: A_1, ..., A_n are independent when Pr(∩_{i∈S} A_i) = ∏_{i∈S} Pr(A_i) for EVERY subset S; pairwise independence (all pairs factor) does not imply the full joint factorization, and vice versa.
  - id: conditional-independence
    name: Conditional independence
    importance: core
    one_liner: A_1, A_2 are conditionally independent given B when Pr(A_1 ∩ A_2 | B) = Pr(A_1 | B) Pr(A_2 | B); it neither implies nor is implied by unconditional independence — conditioning can create or destroy independence.
estimated_runtime_sec: 420        # ~7 min
---

# Independence — Concept Map

# What
Section 4.4 with its two subsections. Two events are **independent** when
`Pr(A ∩ B) = Pr(A) Pr(B)`, equivalently `Pr(A | B) = Pr(A)` — learning `B` tells
you nothing about `A`. The video sharpens the intuition (independence is *not*
mutual exclusivity; independent trials have no memory — the gambler's fallacy),
extends the definition to **multiple events** (where *pairwise* independence and
*mutual* independence genuinely differ), and introduces **conditional
independence**, which can appear or vanish when we condition on a third event.

# Why it matters
Independence is the assumption that makes joint probabilities tractable — it is
what lets us multiply, and it underlies i.i.d. sampling, reliability, and nearly
every tractable model in the subject. The subtleties matter too: conflating
independence with disjointness, or assuming pairwise independence is enough, are
real modeling errors, and conditional independence is the backbone of graphical
models and naive-Bayes classifiers downstream.

# Key ideas (in dependency order)
1. **Definition.** A, B independent ⇔ Pr(A ∩ B) = Pr(A) Pr(B). When Pr(B) > 0
   this is equivalent to Pr(A | B) = Pr(A): the posterior equals the prior.
   Symmetric in A and B.
2. **Two dice.** {r = 4} and {b = 6} are independent (Pr = 1/36 = (1/6)(1/6));
   but {r = 4} and {r + b = 11} are dependent (Pr(r=4 | sum=11) = 0 ≠ 1/6).
3. **Disjoint ≠ independent.** If Pr(A), Pr(B) > 0 and A ∩ B = ∅, then
   Pr(A ∩ B) = 0 < Pr(A) Pr(B) — disjoint nontrivial events cannot be
   independent.
4. **Gambler's fallacy.** Independent trials carry no memory; ten heads in a row
   does not make tails "due." Long-run frequency balancing is not a corrective
   force on individual trials.
5. **Multiple events.** A_1, …, A_n independent ⇔ Pr(∩_{i∈S} A_i)
   = ∏_{i∈S} Pr(A_i) for *every* subset S. For three events: three pairwise
   equalities *plus* the triple product. Pairwise ⇏ mutual: fair coin twice,
   A = H first, B = H second, C = tosses differ — pairwise independent yet
   Pr(A ∩ B ∩ C) = 0 ≠ 1/8. The triple can factor without the pairs: dice with
   A = r odd, B = r ∈ {2,3,4}, C = product 12.
6. **Conditional independence.** A_1, A_2 conditionally independent given B ⇔
   Pr(A_1 ∩ A_2 | B) = Pr(A_1 | B) Pr(A_2 | B). Coin-until-heads: A_1 even,
   A_2 < 6 are conditionally independent given B = "more than one toss" but not
   unconditionally. Conversely {r=2}, {b=6} are independent but *not* given that
   the sum is odd. Conditioning can create or destroy independence.

# Visual plan (beats)
- **overview** — recap (Bayes' rule updates beliefs), then the question: when does
  evidence change nothing? Outline: two events, multiple events, conditional.
- **independence** — the definition Pr(A ∩ B) = Pr(A) Pr(B) and its Pr(A | B) =
  Pr(A) face; the two-dice contrast (independent vs dependent); the
  disjoint-≠-independent Venn; name the gambler's fallacy.
- **multiple-events** — the full subset-factorization condition; the coin-twice
  A/B/C example showing pairwise-but-not-mutual (a 2×2 outcome grid); a one-line
  note that the triple can factor without the pairs.
- **conditional-independence** — the definition; the coin-until-heads example
  (independent only after conditioning); the dice sum-odd counterexample
  (independence destroyed by conditioning); the symmetric takeaway.

# Notation (per project.yaml)
- Pr(·) for probability, written \Pr (never blackboard-bold P).
- Conditioning bar \mid; intersection \cap; product \prod; complement A^{\mathrm{c}}.

# Out of scope / cut first
- The n-event conditional-independence definition (state the two-event case; note
  it extends by the same subset condition).
- A formal proof that conditional independence is symmetric (assert it).
