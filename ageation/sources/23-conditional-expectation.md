<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/discrete_vectors.md -->
<!-- upstream_sha256: 3a21e907411559bda5461edf5d37446c4062a4a698849d38d1976d4868e2cd79 -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 3e1b5679ffcc0830fd342fa30695e369798e9352 -->
<!-- git_tag: pdf-14-g3e1b567 -->
<!-- vendored_at: 2026-07-03 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [joint-pmf, marginal, conditional-pmf, conditional-expectation, tower-property, linearity-of-expectation, independence-of-rvs, convolution]
requires:   [random-variable, pmf, expectation, ogf, independence-of-events]
---

# Multiple Discrete Random Variables — scratch

> Scratch/ideas only. The shipped prose lives in `discrete_vectors.tex`. Not part of the LaTeX build.

## Purpose
Extend the discrete RV machinery to jointly distributed collections — joint PMFs, conditionals, independence, and the algebra that supports sums and products of many RVs.

## Key points / outline
- Joint PMF p_{X,Y}(x,y); marginals recovered by summing out.
- Functions of joint RVs and expectations: E[g(X,Y)] as a double sum; linearity of expectation.
- Conditional RVs: conditioning on an event, then on a random variable (a family of conditional PMFs indexed by the conditioning value).
- Conditional expectation E[X | Y]: itself a random variable; tower property E[E[X|Y]] = E[X].
- Independence: joint PMF factors as product of marginals; equivalent formulations.
- iid random variables: the independent-and-identically-distributed notion from `discrete_random_variables`, made rigorous at the RV level here once independence of random variables is defined; the standing assumption for sums and the later limit theorems.
- OGFs as a multiplicative tool: OGF of a sum of independent integer-valued RVs is the product of OGFs.
- Sums of two independent RVs via convolution of PMFs.
- Numerous RVs: extending to n-tuples, joint independence, and structural shortcuts that scale.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
