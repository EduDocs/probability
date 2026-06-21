# Meeting Expectations — scratch

> Scratch/ideas only. The shipped prose lives in `discrete_expectations.tex`. Not part of the LaTeX build.

## Purpose
Introduce expectation as the canonical summary of a discrete distribution, then build out the surrounding machinery: expectations of functions, mean, variance, moments, and generating functions.

## Key points / outline
- Expected value of a discrete RV: weighted sum E[X] = sum x p_X(x); existence requires absolute summability.
- Expectations of functions: E[g(X)] computed directly from p_X (law of the unconscious statistician).
- The mean as the first moment; centering interpretation.
- The variance: E[(X - E[X])^2]; spread of the distribution; standard deviation.
- Affine functions: E[aX + b] = aE[X] + b; Var(aX + b) = a^2 Var(X).
- Moments E[X^k] and central moments; their role in summarizing a distribution.
- Ordinary generating functions (OGF) for nonneg integer-valued RVs: encode the PMF as a power series; derivatives at 1 recover moments; products correspond to convolutions / sums of independent RVs.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
