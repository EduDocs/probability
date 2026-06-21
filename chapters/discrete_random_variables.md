# Discrete Random Variables — scratch

> Scratch/ideas only. The shipped prose lives in `discrete_random_variables.tex`. Not part of the LaTeX build.

## Purpose
Promote random variables from events to functions on the sample space, focus on the discrete case, and catalog the canonical discrete distributions that recur throughout the notes.

## Key points / outline
- Random variable as a function X: Omega -> R; discrete RV takes countably many values.
- Probability mass function (PMF) p_X(x) = Pr(X = x); axioms (nonneg, sums to 1).
- Events on X are pulled back to events on Omega via preimages.
- Bernoulli RV: single trial, parameter p; the atomic building block.
- Binomial RV: number of successes in n iid Bernoulli trials.
- Poisson RV: limit of binomial under rare-events scaling; counts of occurrences in an interval.
- Geometric RV: trial index of the first success in iid Bernoulli trials.
- Discrete uniform RV: equally-likely values over a finite range.
- Functions of a random variable: Y = g(X) yields a discrete RV with PMF obtained by summing p_X over preimages.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
