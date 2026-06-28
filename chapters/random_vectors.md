---
introduces: [joint-cdf, joint-pdf, conditional-pdf, covariance, correlation, gaussian-vector]
requires:   [cdf, pdf, expectation, variance, marginal, conditional-expectation, tower-property, change-of-variables, jacobian, independence-of-rvs, convolution, gaussian]
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
- Covariance and the covariance matrix: Cov(X,Y) = E[(X − E[X])(Y − E[Y])] = E[XY] − E[X]E[Y]; for a random vector, the covariance matrix Σ collects variances on its diagonal and covariances off it.
- Pearson correlation coefficient ρ_{X,Y} = Cov(X,Y) / (σ_X σ_Y); the Cauchy–Schwarz inequality gives |ρ_{X,Y}| ≤ 1, with equality iff Y is an affine function of X; uncorrelated (Cov = 0) is weaker than independent in general.
- Jointly Gaussian vectors: the joint PDF is set by the mean vector m and covariance matrix Σ; affine maps preserve Gaussianity (Y = AX + b is Gaussian with mean Am + b and covariance AΣAᵀ), generalizing to n dimensions. (Captures the worked Gaussian-vector example already in `random_vectors.tex`.)
- Bivariate normal in scalar form: the two-dimensional jointly Gaussian PDF written explicitly with five parameters (μ_X, μ_Y, σ_X, σ_Y, ρ) — the scalar expansion of the matrix form (m, Σ).
- A special property of the Gaussian family: jointly Gaussian RVs that are uncorrelated (ρ = 0) are independent — which fails for general RVs, where uncorrelated does not imply independence.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
