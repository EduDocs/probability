---
slug: 17-functions-of-random-variables
title: Functions of Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed             # draft | reviewed | approved  (human gate)
source: sources/17-functions-of-random-variables.tex
source_sha256: 5015c13f03c72bce580e69e1b93d862bf8356315ac5ed52a76e3e64986556556
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/discrete_random_variables.tex
companion: sources/17-functions-of-random-variables.md
companion_sha256: b5c87cf6e9842e326bd11d2344f531af394339de4087ab9155f583285430a248
companion_upstream: ../chapters/discrete_random_variables.md
prereqs:
  - 16-important-discrete-rvs
audience: undergraduate engineering, first probability course
concepts:
  - id: function-of-rv
    name: A function of a random variable is a random variable
    importance: core
    one_liner: If X is a random variable and g is real-valued, then Y = g(X) is also a random variable; it assigns g(X(omega)) to each outcome, and Y is discrete when X is.
  - id: pmf-of-y
    name: PMF of Y = g(X)
    importance: core
    one_liner: p_Y(y) = sum over {x in X(Omega) : g(x) = y} of p_X(x); collect the mass of every X-value that g sends to y.
  - id: affine
    name: Affine functions
    importance: highlight
    one_liner: For Y = aX + b with a != 0, g is invertible, so p_Y(y) = p_X((y - b)/a); the mass moves without merging.
  - id: taxi-example
    name: Worked example — taxi fares
    importance: core
    one_liner: Ride length X uniform on {1..10} miles, fare Y = 2.5 + 2X; p_Y(2.5 + 2k) = 1/10, a relabeled uniform.
estimated_runtime_sec: 480        # ~8 min
---

# Functions of Random Variables — Concept Map

## What
Section 5.3. Given a random variable `X` and a real-valued function `g`, the
composition `Y = g(X)` is itself a random variable. This video shows why, how to
get the PMF of `Y` from the PMF of `X` (sum the mass over preimages), and works
one clean example end to end — the taxi fare — as the user asked.

## Why it matters
We rarely observe the quantity we ultimately care about directly; we observe
something and then transform it. Fares from distances, energy from voltage,
cost from counts — all are functions of a random variable. The rule "sum the
mass over the preimage" is the discrete ancestor of the change-of-variables
machinery for derived distributions (Chapter 9), so it is worth seeing cleanly
in the discrete case first. It also reuses the preimage idea from video 1: the
PMF of `Y` is just the PMF law pushed forward one more step.

## Key ideas (in dependency order)
1. **Y = g(X) is a random variable.** For outcome `omega`, `X` takes value
   `x = X(omega)` and `Y` takes value `g(x)`. It attaches a number to every
   outcome, so it is a random variable; if `X` is discrete so is `Y`, and
   `|g(X(Omega))| <= |X(Omega)|` (g can merge values, never split them).
2. **PMF of Y.** For `y in g(X(Omega))`,
   `p_Y(y) = sum_{x : g(x) = y} p_X(x)` — collect the mass of every `x` that
   maps to `y`; otherwise `p_Y(y) = 0`. When `g` is many-to-one, several bars of
   `X` merge into one bar of `Y`.
3. **Affine case.** `Y = aX + b`, `a != 0`. Here `g` is one-to-one, so no bars
   merge: `p_Y(y) = p_X((y - b)/a)`. The mass is just relabeled and rescaled —
   the shape of the PMF is preserved. Linear/affine maps are everywhere in
   applied probability and engineering.
4. **Taxi example (the centerpiece).** Ride length `X` is discrete uniform on
   `{1, ..., 10}` miles. Fare rule: $2.50 on entry, $0.40 per one-fifth mile, so
   $2.00 per mile, giving `Y = 2.5 + 2X`. This is affine with `a = 2, b = 2.5`,
   so `p_Y(2.5 + 2k) = 1/10` for `k = 1..10` and zero elsewhere — a uniform PMF
   relabeled onto the fare values {4.5, 6.5, ..., 22.5}.

## Visual plan (beats)
- **overview** — recap video 2 (the named distributions), state the objective
  (transform a random variable and track its PMF), outline.
- **function-of-rv** — the two-number-line mapping picture from the notes: Omega
  -> R via X, then R -> R via g, so outcomes reach Y = g(X); note many-to-one.
- **pmf-of-y** — the preimage-sum formula; a small X-PMF whose bars merge into a
  Y-PMF under a many-to-one g (e.g. Y = X^2 or |X|).
- **affine** — Y = aX + b; show the invertible case where bars only shift/scale;
  the formula p_Y(y) = p_X((y-b)/a).
- **taxi** — the worked example: uniform X on {1..10} -> fares {4.5..22.5}, each
  with mass 1/10; then the key-idea outro + bridge to Chapter 6 (expectation).

## Notation (per project.yaml)
- `Pr(...)` as `\Pr`; PMFs `p_X`, `p_Y`.
- Preimage-sum: `p_Y(y) = \sum_{\{x \in X(\Omega) : g(x) = y\}} p_X(x)`.

## Out of scope / cut first
- Non-invertible worked examples beyond the merge illustration.
- Continuous change of variables / derived distributions (Chapter 9) — named as
  the sequel only.
- Expectation of g(X) via the "law of the unconscious statistician" (Chapter 6).
