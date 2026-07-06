---
introduces: [change-of-variables, jacobian, probability-integral-transform]
requires:   [random-variable, pmf, pdf, cdf, function-of-rv, uniform-continuous]
videos:
  - title: Derived Cumulative Distribution Functions
    url: https://www.youtube.com/watch?v=fqC4IaOhk9M
  - title: Derived Probability Density Functions
    url: https://www.youtube.com/watch?v=I8XkZuPKDQU
  - title: Generating Random Variables Algorithmically
    url: https://www.youtube.com/watch?v=-1sfh0p_8eI
---

# Functions and Derived Distributions — scratch

> Scratch/ideas only. The shipped prose lives in `derived_distributions.tex`. Not part of the LaTeX build.

## Purpose
Show how to obtain the distribution of Y = g(X) from the distribution of a continuous X, and use that machinery to generate random variables on a computer.

## Key points / outline
- Setup: g: R -> R applied to a continuous RV X yields a new RV Y whose distribution must be derived from f_X.
- Monotone g: invert g and use the CDF/PDF transformation formula directly; the derivative |dg^{-1}/dy| appears as the Jacobian factor.
- Differentiable (non-monotone) g: partition the domain into monotone pieces, sum over preimages; handle critical-point subtleties.
- Generating random variables: use the inverse-CDF (probability integral transform) method to map a Uniform(0,1) draw to any target continuous distribution.
- Discrete generation: invert the discrete CDF (or sample by binning a Uniform draw into PMF intervals) to produce a target discrete distribution.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
