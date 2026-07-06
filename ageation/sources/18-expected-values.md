<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/discrete_expectations.md -->
<!-- upstream_sha256: 416d800da682382b43789de57a09552e90a45766379dd6d6b3a446ebaaaf28fc -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [expectation, lotus, variance, moment, ogf]
requires:   [random-variable, pmf, function-of-rv, independence-of-rvs, convolution]
---

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
