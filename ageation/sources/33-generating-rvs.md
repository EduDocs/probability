<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/derived_distributions.md -->
<!-- upstream_sha256: 7c6821f86e119370ecffc7a7cb100cedaf473c6d6c699c8ed491c324dd5da68f -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [change-of-variables, jacobian, probability-integral-transform]
requires:   [random-variable, pmf, pdf, cdf, function-of-rv, uniform-continuous]
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
