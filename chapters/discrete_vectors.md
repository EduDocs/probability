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
- OGFs as a multiplicative tool: OGF of a sum of independent integer-valued RVs is the product of OGFs.
- Sums of two independent RVs via convolution of PMFs.
- Numerous RVs: extending to n-tuples, joint independence, and structural shortcuts that scale.

## Open questions
-

## Notes & references
- Standard introductory probability texts (see chapter's Further Reading block at end of `.tex`).
