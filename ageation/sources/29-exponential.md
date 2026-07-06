<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/continuous_random_variables.md -->
<!-- upstream_sha256: 9165b919c522599d616f05bd0db8179aeeb1e0866f8d01b7e08dfec8ea780f7c -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [cdf, pdf, uniform-continuous, gaussian, exponential, gamma, rayleigh, laplace, cauchy]
requires:   [random-variable, pmf, expectation, lotus, function-of-rv, independence-of-rvs, joint-pdf]
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
