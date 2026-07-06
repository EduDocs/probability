---
introduces: [convergence-in-probability, convergence-in-distribution, convergence-in-mean-square, lln, clt]
requires:   [random-variable, expectation, variance, iid, gaussian]
videos:
  - title: Random Sequences and Convergence
    url: https://www.youtube.com/watch?v=azNGCqYRBwE
  - title: The Law of Large Numbers
    url: https://www.youtube.com/watch?v=dBxxZhCPZX8
  - title: The Central Limit Theorem
    url: https://www.youtube.com/watch?v=6f6TSaBL-FM
---

# Sequences, Convergence and Limit Theorems — scratch

> Scratch/ideas only. The shipped prose lives in `empirical_sums.tex`. Not part of the LaTeX build.

## Purpose
Make precise what it means for a sequence of random variables to converge, and use that vocabulary to state and motivate the two headline limit theorems: the law of large numbers and the central limit theorem.

## Key points / outline
- Setup: a sequence X_1, X_2, ... and a limit X, all on a common probability space.
- Types of convergence: convergence in probability, mean-square convergence, convergence in distribution; implications between them.
- Convergence relationships (e.g., mean-square implies in-probability implies in-distribution); examples showing the converses fail.
- Law of large numbers: the empirical mean of iid RVs converges to E[X]; engineering payoff is concentration / "economy of scale."
- Heavy-tailed distributions as a cautionary case where LLN-style intuition breaks (starred).
- Central limit theorem: the standardized sum of iid finite-variance RVs converges in distribution to a standard Gaussian.
- Normal approximation as the everyday application of the CLT.

## Open questions
-

## Notes & references
- Ross, *A First Course in Probability*, Chapter 8.
- Bertsekas & Tsitsiklis, *Introduction to Probability*, Sections 7.2–7.4.
- Miller & Childers, *Probability and Random Processes*, Chapter 7.
