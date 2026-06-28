---
introduces: [joint-cdf, joint-pdf, conditional-pdf]
requires:   [cdf, pdf, marginal, conditional-expectation, tower-property, change-of-variables, jacobian, independence-of-rvs, convolution]
---

# Multiple Continuous Random Variables — scratch

> Scratch/ideas only. The shipped prose lives in `random_vectors.tex`. Not part of the LaTeX build.

## Purpose
Generalize the continuous-RV machinery to jointly distributed continuous random vectors: joint distributions, conditional densities, derived distributions, independence, and sums.

## Key points / outline
- Joint CDF and joint PDF for continuous random vectors; marginals by integration.
- Conditional probability distributions: conditioning on values (the conditional PDF f_{X|Y}) vs. conditioning on events.
- Conditional expectation E[X | Y] in the continuous case; tower property still holds.
- Derived distributions of g(X,Y): change-of-variables with the Jacobian determinant; handling non-invertible maps.
- Independence: joint PDF factors as product of marginals; conditional density equals marginal.
- Sums of independent continuous RVs: convolution of PDFs as the continuous analog of PMF convolution.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
