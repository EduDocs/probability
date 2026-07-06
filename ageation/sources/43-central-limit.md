<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/empirical_sums.md -->
<!-- upstream_sha256: 91972349f0c398cb963ac5b94fc7ab8218cdf25a1b104ebec184db16005dd773 -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [convergence-in-probability, convergence-in-distribution, convergence-in-mean-square, lln, clt]
requires:   [random-variable, expectation, variance, iid, gaussian]
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
