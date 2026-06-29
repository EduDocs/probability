---
introduces: [sample-space, event, probability-law, axioms-of-probability, inclusion-exclusion, union-bound, sigma-field]
requires:   [set, partition, finite-equally-likely-model, counting-principle]
---

# Probability Models — scratch

> Scratch/ideas only. The shipped prose lives in `probability_models.tex`. Not part of the LaTeX build.

## Purpose
Introduce the axiomatic framework of probability: sample spaces, events, and probability laws, then specialize the framework to finite, countably infinite, and uncountably infinite models.

## Key points / outline
- Experiment, outcome, sample space (Omega), event as an admissible subset of Omega.
- Requirements on a sample space: outcomes distinct, mutually exclusive, collectively exhaustive.
- Probability law assigns Pr(A) to each event A, subject to axioms (non-negativity, normalization, countable additivity).
- Consequences derived: complement rule Pr(Aᶜ) = 1 − Pr(A) (with Pr(∅) = 0), monotonicity (A ⊂ B ⇒ Pr(A) ≤ Pr(B)), and the two-event union formula Pr(A ∪ B) = Pr(A) + Pr(B) − Pr(A ∩ B).
- Continuity of probability (continuity from below/above) as a starred consequence of countable additivity.
- Inclusion–exclusion principle as the general formula for the probability of a union.
- Boole inequality (union bound) as a one-sided weakening, proved by induction.
- Finite sample spaces: equally likely model as a special case; counting reduction.
- Countably infinite models: probabilities built from a discrete distribution over a countable Omega.
- Uncountably infinite models: probabilities defined on intervals via density/length, with care about which subsets are admissible.
- Cardinality and countability (natural numbers as the benchmark); power sets push beyond countable.
- Starred preview of measure theory: fields and sigma-fields as the technically correct event class.

## Worked examples (as shipped in the .tex)
- Rolling a die — sample-space/event vocabulary, then the equally-likely model (Pr({2,3,5}) = 3/6). Anchors §Sample Spaces and Events and §§Finite Sample Spaces.
- Even/odd/prime vs. odd/even — non-admissible (overlapping) vs. admissible (disjoint, exhaustive) sample space. Anchors the sample-space rules.
- Urn with 990 blue / 10 red balls, five draws — union bound vs. exact (1 − C(990,5)/C(1000,5)); second part (two reds each) where the exact computation is hard. Anchors the union bound.
- Fair coin tossed until heads — countably infinite Omega = {1,2,…}, geometric weights 2⁻ᵏ summing to 1; Pr(even) = 1/3. Anchors §§Countably Infinite Models.
- Wheel of serendipity (uniform on [0,2π)) — Pr by length/integral. Anchors §§Uncountably Infinite Models.

## Open questions
- **No single running example** threads the chapter. The prose uses four separate vignettes (die, urn, coin, wheel); Cognitive Load Theory flags this introductory chapter as high intrinsic load and favors one anchoring example carried throughout (Bertsekas–Tsitsiklis thread Bernoulli trials + dart-on-a-square). Decide: adopt one anchor or keep the vignette-per-section structure deliberately.

## Resolved (realized in the .tex)
- **Complement rule** Pr(Aᶜ) = 1 − Pr(A), with Pr(∅) = 0 as an immediate corollary, added as the lead consequence right after the axioms.
- **Continuity of probability** added as a starred subsection (*Continuity of Probability\**): continuity from below with a disjointification proof, plus the decreasing-sequence case derived via the complement rule.
- **Vocabulary pointer**: a sentence at the definition notes that "probability law" is elsewhere called a *probability measure*, with a forward pointer to the starred measure-theory section.
- **Misconceptions named**: the *conjunction fallacy* (Pr(A∩B) ≤ Pr(A), via monotonicity) is refuted right after the monotonicity proposition; the *outcome approach* (equiprobability bias) is cautioned at the equally-likely model in §§Finite Sample Spaces.

## Notes & references
- Ross, *A First Course in Probability*, Chapter 2.
- Bertsekas & Tsitsiklis, *Introduction to Probability*, Section 1.2.
- Miller & Childers, *Probability and Random Processes*, Sections 2.1–2.3.
- Gubner, Sections 1.1, 1.3–1.4.
