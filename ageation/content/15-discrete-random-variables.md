---
slug: 15-discrete-random-variables
title: Discrete Random Variables and the PMF
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed             # draft | reviewed | approved  (human gate)
source: sources/15-discrete-random-variables.tex
source_sha256: 5015c13f03c72bce580e69e1b93d862bf8356315ac5ed52a76e3e64986556556
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_random_variables.tex
companion: sources/15-discrete-random-variables.md
companion_sha256: b5c87cf6e9842e326bd11d2344f531af394339de4087ab9155f583285430a248
companion_upstream: ../chapters/discrete_random_variables.md
prereqs:
  - 14-independence
audience: undergraduate engineering, first probability course
concepts:
  - id: rv-as-function
    name: Random variable as a function
    importance: core
    one_liner: A random variable X is a real-valued function of the outcome, X : Omega -> R; it assigns a number to every outcome, and several outcomes may map to the same number.
  - id: discrete-rv
    name: Discrete random variable
    importance: core
    one_liner: X is discrete when its range X(Omega) is finite or countably infinite (e.g. a die face, or the number of tosses until the first head).
  - id: pmf
    name: Probability mass function
    importance: core
    one_liner: The PMF p_X(x) = Pr(X = x) = Pr(X^{-1}(x)) gives the probability sitting on each value; it is nonnegative and sums to 1 over X(Omega).
  - id: pmf-of-a-set
    name: Probability of a set of values
    importance: highlight
    one_liner: For S subset of X(Omega), Pr(X in S) = sum_{x in S} p_X(x); the preimages partition Omega, which is why the PMF sums to 1.
estimated_runtime_sec: 480        # ~8 min
---

# Discrete Random Variables and the PMF — Concept Map

## What
This is the chapter opener plus Section 5.1. A **random variable** is a
real-valued function of the outcome of an experiment: `X : Omega -> R`. It
promotes the abstract outcomes of a probability space into *numbers* we can
compute with. A random variable is **discrete** when its range is finite or
countable, and such a variable is completely described by its **probability
mass function (PMF)** `p_X(x) = Pr(X = x)`.

## Why it matters
Probability spaces tell us how likely events are, but they don't hand us
numbers to add, average, or take limits of. The instant we attach a number to
each outcome, the entire machinery of sums, expectations, and convergence
becomes available. This chapter is the bridge from *events* to *quantities*,
and it underpins everything downstream — expectation, variance, random vectors.

## Key ideas (in dependency order)
1. **RV as a function.** `X` assigns a real number to every outcome. Different
   outcomes may land on the same value — the map need not be one-to-one. Die
   example: the six faces map to 1..6.
2. **Discrete range.** `X(Omega)` is the set of values `X` can take. Discrete
   means finite or countable. Coin-tossed-until-heads: the range is
   `{1, 2, 3, ...}`, countably infinite.
3. **The PMF via preimages.** `p_X(x) = Pr(X = x) = Pr(X^{-1}(x))`, the
   probability of the set of outcomes `{omega : X(omega) = x}`. This preimage is
   an *event*; the PMF just pushes the probability law forward onto the number
   line. `X^{-1}(x)` is a preimage, not a bijection inverse.
4. **Normalization.** The preimages, as `x` ranges over `X(Omega)`, are
   disjoint and partition `Omega`; so `sum_{x in X(Omega)} p_X(x) = 1` follows
   from countable additivity + normalization.
5. **Probability of a set.** For `S subset of X(Omega)`,
   `Pr(X in S) = sum_{x in S} p_X(x)` — an explicit formula for the probability
   of any set of values.

## Worked example (the payoff beat)
Urn with balls 1, 2, 3; draw two without replacement. Ordered outcomes
`Omega = {(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)}`, all equiprobable. Let `X` be
the sum. Then `p_X(3) = p_X(4) = p_X(5) = 1/3`. The event "sum is odd" is
`S = {3, 5}`, so `Pr(X in S) = p_X(3) + p_X(5) = 2/3`. This exercises the whole
pipeline: build a PMF from a sample space, then compute a set probability by
summing the mass.

## Visual plan (beats)
- **overview** — recap independence (last chapter), state the objective (turn
  outcomes into numbers, describe with a PMF), and a four-item outline.
- **rv-mapping** — an Omega box of colored outcomes, curved arrows to a number
  line; the die picture; emphasize many-to-one.
- **discrete-rv** — the finite-vs-countable distinction; coin-until-heads range
  `{1, 2, ...}` as the countably-infinite case.
- **pmf-definition** — `p_X(x) = Pr(X = x)`, the preimage highlighted inside
  Omega, the normalization `sum p_X = 1`, and the set formula
  `Pr(X in S) = sum_{x in S} p_X(x)` shown as bars.
- **urn-example** — build the three-value PMF, then shade `{3, 5}` and add the
  masses to `2/3`.

## Notation (per project.yaml)
- `Pr(...)` written `\Pr` (never blackboard-bold P).
- Preimage `X^{-1}(x) = \{\omega \in \Omega : X(\omega) = x\}`.
- Range `X(\Omega)`; sum `\sum_{x \in X(\Omega)} p_X(x) = 1`.

## Out of scope / cut first
- Any named distribution (that is the next video, 5.2).
- Expectation / variance (Chapter 6) — this video is purely the PMF.
- Continuous random variables (Chapter 8).
