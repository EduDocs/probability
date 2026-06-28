---
introduces: [mgf, markov-inequality, chebyshev-inequality, chernoff-bound, jensen-inequality]
requires:   [expectation, variance, moment, ogf, random-variable, independence-of-rvs]
---

# Expectations and Bounds — scratch

> Scratch/ideas only. The shipped prose lives in `expectations_and_bounds.tex`. Not part of the LaTeX build.

## Purpose
Promote expectation from a summary statistic to a tool for bounding probabilities, via moment generating functions and the classical concentration / tail inequalities.

## Key points / outline
- Moment generating function (MGF) M_X(s) = E[e^{sX}]; recovers moments by repeated differentiation at s = 0; uniqueness when finite on a neighborhood of 0.
- MGFs convert sums of independent RVs into products — same multiplicative structure as OGFs, generalized.
- Markov inequality: a one-sided tail bound for nonneg RVs in terms of E[X].
- Chebyshev inequality: a two-sided tail bound for deviations from the mean in terms of the variance.
- Chernoff bound: exponentially sharper tail bound obtained by optimizing a Markov bound on e^{sX} using the MGF.
- Jensen's inequality: convexity-based bound, E[phi(X)] >= phi(E[X]) for convex phi; flipped for concave phi.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
