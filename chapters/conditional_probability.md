# Conditional Probability — scratch

> Scratch/ideas only. The shipped prose lives in `conditional_probability.tex`. Not part of the LaTeX build.

## Purpose
Develop conditioning as the mechanism for updating probabilities given partial information, then use it to derive the total probability theorem, Bayes' rule, and independence.

## Key points / outline
- Conditioning on an event B with Pr(B) > 0: definition of Pr(A | B) and how it re-normalizes the law to B.
- The conditional law is itself a valid probability law on Omega (or on B).
- Multiplication rule for chains of events.
- Total probability theorem: decompose Pr(A) over a partition {B_i} using conditionals.
- Bayes' rule: invert conditioning to compute Pr(B_i | A) from Pr(A | B_i) and priors.
- Independence of two events: Pr(A intersect B) = Pr(A) Pr(B); equivalent to Pr(A | B) = Pr(A) when defined.
- Independence of multiple events: pairwise vs. mutual; the full factorization condition.
- Conditional independence: independence under a conditioning event need not match marginal independence.
- Equivalent notations conventions used in the rest of the notes.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
