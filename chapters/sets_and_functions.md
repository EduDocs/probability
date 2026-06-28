---
introduces: [set, partition, cartesian-product, relation, function, preimage, indicator-function]
requires:   []
---

# Sets and Functions — scratch

> Scratch/ideas only. The shipped prose lives in `sets_and_functions.tex`. Not part of the LaTeX build.

## Purpose
Establish the set-theoretic language and notation that the rest of the notes depend on, at the naive-set-theory level — enough to support the probability axioms without going into measure theory.

## Key points / outline
- Naive set theory as the working foundation; rigorous axiomatic treatment is set aside.
- Sets and elements: membership, equality, subset vs. proper subset.
- Ways to specify a set: listing, enumeration, set-builder notation.
- Special sets: empty set, universal set (called the sample space in probability), complement.
- Elementary operations: union, intersection, disjointness, partition, set difference.
- Arbitrary unions and intersections over an index set.
- Algebraic rules: precedence, distributive laws, De Morgan's laws (two-set and indexed forms).
- Cartesian products and ordered pairs as a way to build new sets.
- Relations as subsets of a Cartesian product; a function is the special single-valued relation (formal triple = the two sets plus a graph obeying the single-value property).
- Functions: domain, codomain, image, preimage, level set.
- Function properties: injective, surjective, bijective; inverse functions.
- The indicator function, defined on the universal set Ω, as a probability-relevant example; teaser tie to the sample space and the Bernoulli random variable.
- Closing tie-back: name which set construct underwrites which probability idea (Ω → sample space, partition → law of total probability, preimage → random variable, Cartesian product → joint distribution).

## Open questions
-

## Notes & references
- Bertsekas & Tsitsiklis, *Introduction to Probability*, Section 1.1.
- Gubner, *Probability and Random Processes for Electrical and Computer Engineers*, Section 1.2.

## Decisions
- Renamed from "Mathematical Review" to **Sets and Functions** (files `sets_and_functions.{tex,md}`). The old title oversold the scope — the chapter is set theory and functions, not a general math review — and collided with the reference appendix `appendix_background` ("Mathematical Background"). The front-matter (motivating) vs. reference-manual (lookup) split is discussed in `appendix_background.md`.
- Introduced **relations** (a subset of a Cartesian product) so that *function* can be defined precisely as a single-valued relation, replacing the vague "structured subset" phrasing. It lands right after Cartesian products, which supply the prerequisite.
- Enlarged the **indicator function** from a subset of ℝ to a subset of the universal set Ω, with a one-line teaser to the sample space and the Bernoulli RV. This also begins to address the orphaned-indicator finding in `TODO.md`.
- **Countable / uncountable stays in `basic_concepts`,** not here: that chapter already develops it where it is motivated (finite → countable → uncountable → measure-theory preview). This chapter only de-jargoned its single loose use of "countable" in the set-specification paragraph.
