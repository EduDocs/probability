<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/expectations_and_bounds.md -->
<!-- upstream_sha256: 7c1122b67bf05b97e96935ecf3ae2e1c3fe888db9cc1b2a94b0189f5ffbbe436 -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [mgf, markov-inequality, chebyshev-inequality, chernoff-bound, jensen-inequality, confidence-interval]
requires:   [expectation, variance, moment, ogf, random-variable, independence-of-rvs, iid]
---

# Expectations and Bounds — scratch

> Scratch/ideas only. The shipped prose lives in `expectations_and_bounds.tex`. Not part of the LaTeX build.

## Purpose
Promote expectation from a summary statistic to a tool for bounding probabilities, via moment generating functions and the classical concentration / tail inequalities.

## Key points / outline
- Moment generating function (MGF) M_X(s) = E[e^{sX}]; recovers moments by repeated differentiation at s = 0; uniqueness when finite on a neighborhood of 0.
- MGFs convert sums of independent RVs into products — same multiplicative structure as OGFs, generalized.
- Dependency note: this multiplicative property — and the Chernoff bound for sums below — lean on independence of random variables (introduced for the discrete case in `discrete_vectors`); the continuous-RV formalization, via factoring of joint densities, is completed in `random_vectors`.
- Markov inequality: a one-sided tail bound for nonneg RVs in terms of E[X].
- Chebyshev inequality: a two-sided tail bound for deviations from the mean in terms of the variance.
- Chebyshev in action — confidence intervals: for the empirical proportion p̂ = (X₁ + … + Xₙ)/n of n iid Bernoulli(p) trials, Chebyshev gives Pr(|p̂ − p| < a/(2√n)) ≥ 1 − 1/a², turning the abstract bound into an interval estimate for p — a first bridge to statistics, and a concrete preview of the law of large numbers in `empirical_sums`.
- Chernoff bound: exponentially sharper tail bound obtained by optimizing a Markov bound on e^{sX} using the MGF.
- Jensen's inequality: convexity-based bound, E[phi(X)] >= phi(E[X]) for convex phi; flipped for concave phi.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
