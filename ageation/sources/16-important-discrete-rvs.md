<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/discrete_random_variables.md -->
<!-- upstream_sha256: 2c7257876ac6ea7d87f2206b8d2b9ef297e3de8fa0694354b42c8e5f49b35dcb -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 847f2be7933a06400eb022957fbcf3deca9c3169 -->
<!-- git_tag: pdf-9-g847f2be -->
<!-- vendored_at: 2026-07-02 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [random-variable, pmf, function-of-rv, bernoulli, iid, binomial, poisson, geometric, discrete-uniform]
requires:   [sample-space, event, probability-law, function, preimage, independence-of-events]
---

# Discrete Random Variables — scratch

> Scratch/ideas only. The shipped prose lives in `discrete_random_variables.tex`. Not part of the LaTeX build.

## Purpose
Promote random variables from events to functions on the sample space, focus on the discrete case, and catalog the canonical discrete distributions that recur throughout the notes.

## Key points / outline
- Random variable as a function X: Omega -> R; discrete RV takes countably many values.
- Probability mass function (PMF) p_X(x) = Pr(X = x); axioms (nonneg, sums to 1).
- Events on X are pulled back to events on Omega via preimages.
- Bernoulli RV: single trial, parameter p; the atomic building block.
- Independent and identically distributed (iid) trials: repeated trials that are mutually independent (via independence of events) and share one distribution; the standard building block for the binomial and geometric models, and reused later for sums and limit theorems.
- Binomial RV: number of successes in n iid Bernoulli trials.
- Poisson RV: limit of binomial under rare-events scaling; counts of occurrences in an interval.
- Geometric RV: trial index of the first success in iid Bernoulli trials.
- Discrete uniform RV: equally-likely values over a finite range.
- Functions of a random variable: Y = g(X) yields a discrete RV with PMF obtained by summing p_X over preimages.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
