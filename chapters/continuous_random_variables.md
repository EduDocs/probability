---
introduces: [cdf, pdf, uniform-continuous, gaussian, exponential, gamma, rayleigh, laplace, cauchy]
requires:   [random-variable, pmf, expectation, lotus, function-of-rv, independence-of-rvs, joint-pdf]
videos:
  - title: Cumulative Distribution Functions
    url: https://www.youtube.com/watch?v=efruBDxXoC8
  - title: Probability Density Functions and Expectation
    url: https://www.youtube.com/watch?v=wph-ZYmhQ-I
  - title: Uniform and Gaussian Random Variables
    url: https://www.youtube.com/watch?v=o0UZHYtonXI
  - title: Exponential Random Variable
    url: https://www.youtube.com/watch?v=FIhvj1yAC3s
  - title: Additional Continuous Distributions
    url: https://www.youtube.com/watch?v=8ij5BX4G0iE
---

# Continuous Random Variables — scratch

> Scratch/ideas only. The shipped prose lives in `continuous_random_variables.tex`. Not part of the LaTeX build.

## Purpose
Extend the random-variable machinery from the discrete to the continuous case via CDFs and PDFs, then catalog the canonical continuous distributions used throughout the notes.

## Key points / outline
- CDF F_X(x) = Pr(X <= x) as the unifying object: right-continuous, nondecreasing, limits 0 and 1.
- Discrete RVs revisited through their step-CDFs; continuous RVs as those with continuous CDFs; mixed RVs as the hybrid case (starred).
- Probability density function (PDF) f_X as the derivative of F_X for absolutely continuous RVs; probabilities as integrals over intervals; f_X is not itself a probability.
- Expectation revisited: E[g(X)] = integral g(x) f_X(x) dx; same identity language as the discrete case but with sums replaced by integrals.
- Uniform distribution on an interval as the simplest continuous model.
- Gaussian (normal) distribution: parameterization by mean and variance; standardization; central role to come.
- Exponential distribution: memoryless property, link to Poisson processes.
- Additional named families: Gamma (sums of independent exponentials), Rayleigh (norm of 2D Gaussian), Laplace (double-exponential), Cauchy (heavy tails, mean undefined).

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
