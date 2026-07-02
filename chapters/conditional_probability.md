---
introduces: [conditional-probability, chain-rule, total-probability, bayes-rule, prior-posterior-likelihood, independence-of-events, conditional-independence]
requires:   [sample-space, event, probability-law, partition, axioms-of-probability]
---

# Conditional Probability — scratch

> Scratch/ideas only. The shipped prose lives in `conditional_probability.tex`. Not part of the LaTeX build.

## Purpose
Develop conditioning as the mechanism for updating probabilities given partial information, then use it to derive the chain rule, the total probability theorem, Bayes' rule, and independence.

## Key points / outline
- Conditioning on an event B with Pr(B) > 0: definition of Pr(A | B) and how it re-normalizes the law to B.
- Two motivations precede the definition: the equally-likely die (re-normalize over the surviving outcomes) and a frequentist N-trials argument (Pr(A | B) ≈ N_AB / N_B).
- The conditional law {Pr(A | B)} is itself a valid probability law on Omega (verifies the three axioms).
- Chain rule (multiplication rule) for the probability of a chain of events intersecting.
- Total probability theorem: decompose Pr(B) over a partition {A_k} using conditionals; relies on revisiting the partition notion.
- Bayes' rule: invert conditioning to compute Pr(A_i | B) from Pr(B | A_i) and priors; denominator expanded by total probability.
- Vocabulary of inference: prior Pr(A_i), posterior Pr(A_i | B), likelihood Pr(B | A_i).
- Independence of two events: Pr(A ∩ B) = Pr(A) Pr(B); equivalent to Pr(A | B) = Pr(A) when defined; symmetric relation.
- Independence of multiple events: pairwise vs. mutual; the full factorization condition over every subset.
- Conditional independence: independence under a conditioning event need not match marginal independence, and vice versa.
- Equivalent notations (comma for intersection) used in the rest of the notes.

## Worked examples (as shipped in the .tex)
- Fair die given an odd face — re-normalization over {1,3,5}, Pr(3 | odd) = 1/3. Anchors §Conditioning on Events.
- Frequentist N trials — N_AB / N_B → Pr(A ∩ B) / Pr(B), motivating the definition as a limit of relative frequencies.
- Coin tossed until heads, Pr(2 | even) = 3/4 — uses Pr(even) = 1/3 from the earlier coin example. Confirms the conditional law in action.
- Urn 8 blue / 4 green, three draws without replacement, Pr(bbb) = (8/12)(7/11)(6/10) = 14/55. Anchors the chain rule (Balls figure).
- Two urns (5g/3r and 3g/9r), pick a urn then draw, Pr(green) = 7/16. Anchors the total probability theorem (divide and conquer).
- Disease test (95% accurate, 1% prevalence), Pr(D | P) ≈ 0.161. Anchors Bayes' rule, and now also the base-rate fallacy and confusion of the inverse.
- Two dice — Pr(r=4 | b=6) = Pr(r=4) (independent) vs. Pr(r=4 | r+b=11) = 0 ≠ Pr(r=4) (dependent). Anchors §Independence.
- Fair coin twice, A/B/C pairwise independent but Pr(A∩B∩C) = 0 ≠ 1/8 — pairwise does not imply mutual.
- Two dice, A odd / B ∈ {2,3,4} / C product = 12 — not pairwise independent yet the triple product factorizes; the n-fold condition stands apart from the pairwise ones.
- Coin until heads, A1 even / A2 < 6 conditionally independent given B (tossed more than once) but not unconditionally.
- Two dice, {r=2} and {b=6} independent unconditionally but not given that the sum is odd — independence can be destroyed by conditioning.

## Resolved (realized in the .tex)
- **Bayes vocabulary pointer**: a paragraph after the Bayes proof names the *prior* Pr(A_i), the *posterior* Pr(A_i | B), and the *likelihood* Pr(B | A_i), framing the rule as turning priors into posteriors in the light of evidence.
- **Confusion of the inverse / prosecutor's fallacy**: named right after the Bayes proof — Pr(A | B) and Pr(B | A) answer different questions and are generally unequal; the courtroom form is called out by name. Sets up the disease example.
- **Base-rate fallacy**: named immediately after the disease example, where the surprising 16% is exactly the base rate (1% prevalence) being neglected; ties the lesson back to the prior Pr(D).
- **Disjoint ≠ independent** promoted to a named, indexed misconception (conflating independence with mutual exclusivity), where the chapter previously stated it only as unnamed prose.
- **Gambler's fallacy**: named at the close of the two-event independence discussion — independent trials carry no memory; the long-run balancing of frequencies is not a corrective force on individual trials.

## Open questions
- **Monty Hall is absent.** The chapter has no iconic conditioning *puzzle* — the one problem that most sharply exposes the gap between intuition and the conditional law. It would sit naturally as a capstone example to the Bayes' rule section (or as a starred aside), and it reuses the total-probability/Bayes machinery already developed. Deferred (future possibility, not committed): decide whether it earns a full worked example or a Further-Reading pointer; the disease test already carries the base-rate lesson, so Monty Hall would be additive, not load-bearing.
- **Simpson's paradox** is a candidate under total probability / conditional independence — aggregated and stratified conditionals can point opposite ways. Stronger fit once random variables and joint distributions are available downstream; likely better placed later than here. Left as a pointer for now.

## Notes & references
- Ross, *A First Course in Probability*, Chapter 3.
- Bertsekas & Tsitsiklis, *Introduction to Probability*, Sections 1.3–1.5.
- Miller & Childers, *Probability and Random Processes*, Sections 2.4–2.6.
- Gubner, Sections 1.5–1.6.
