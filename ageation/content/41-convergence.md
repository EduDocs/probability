---
slug: 41-convergence
title: Types of Convergence
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-04
source: sources/41-convergence.tex
source_sha256: c13bf4618eb4bbe38d3a7468994a46bd69e62bf1753311394259509f2466e2c5
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/empirical_sums.tex
companion: sources/41-convergence.md
companion_sha256: 51341fb22e74140f95766dd58eb5134122f48455900bc4f5c1726b03d683b956
prereqs:
  - 40-continuous-sums
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: common-experiment
    name: A sequence of random variables on one experiment
    importance: core
    one_liner: X_1, X_2, ... and a limit X, all functions of the SAME outcome — the shared probability space is what makes convergence statements meaningful.
  - id: two-gaussian-sequences
    name: Two sequences, two behaviors
    importance: highlight
    one_liner: For iid Gaussians, S_n/n is Gaussian with variance sigma^2/n — it concentrates at m; (S_n - nm)/sqrt(n) is Gaussian with variance sigma^2 forever — its shape never moves. Two patterns, needing two vocabularies.
  - id: convergence-in-probability
    name: Convergence in probability
    importance: core
    one_liner: For every epsilon > 0, Pr(|X_n - X| >= epsilon) -> 0 — the chance of a visible deviation dies out; S_n/n converges in probability to m.
  - id: mean-square-convergence
    name: Mean square convergence
    importance: core
    one_liner: E[|X_n - X|^2] -> 0 — the second moment of the error vanishes; a stronger, expectation-flavored notion.
  - id: ms-implies-prob
    name: Mean square implies in probability
    importance: core
    one_liner: Chebyshev applied to X_n - X gives Pr(|X_n - X| >= epsilon) <= E[|X_n - X|^2]/epsilon^2 — video 35's inequality turns one convergence into the other.
  - id: convergence-in-distribution
    name: Convergence in distribution
    importance: core
    one_liner: F_{X_n}(x) -> F_X(x) at every continuity point of F_X — the CDFs settle onto a limiting shape; also called weak convergence.
  - id: uniform-shrinking
    name: Worked example — uniform on [0, 1/n]
    importance: core
    one_liner: X_n uniform on [0, 1/n] converges in distribution to the constant 0 — the ramp CDFs steepen into a unit step, skipping the jump point itself.
estimated_runtime_sec: 300
---

# Types of Convergence — Concept Map

This video covers the opening of Section 12.1 of book chapter 12 plus its
three subsections (convergence in probability, mean square convergence,
convergence in distribution). It opens the course's final act: video 40
built sums of continuous random variables; videos 42 and 43 will spend
this vocabulary on the two headline limit theorems.

## What
A sequence of random variables `X_1, X_2, ...` and a limiting random
variable `X`, all defined on the *same* probability space, can approach
each other in more than one sense. The chapter's motivating pair: for iid
Gaussians with mean m and variance `sigma^2`, the empirical average
`S_n/n` is Gaussian with mean m and variance `sigma^2/n` — its PDF
squeezes onto m — while `(S_n - nm)/sqrt(n)` is Gaussian with mean 0 and
variance `sigma^2` *for every n* — its distribution never moves. Three
definitions organize such patterns: **convergence in probability**
(`Pr(|X_n - X| >= epsilon) -> 0`), **mean square convergence**
(`E[|X_n - X|^2] -> 0`), and **convergence in distribution**
(`F_{X_n}(x) -> F_X(x)` at continuity points). Mean square convergence
implies convergence in probability — Chebyshev's inequality is the bridge.

## Why it matters
These are the definitions that let the next two videos say something
precise. "The average settles down" and "the histogram looks Gaussian"
are different claims, and conflating them is the classic error;
concentration behavior is also the engineering payoff — it is what lets
complex systems be designed with tiny failure probabilities and true
economies of scale. The two Gaussian sequences preview the entire finale:
the concentrating one *is* the law of large numbers (video 42), and the
shape-invariant one *is* the central limit theorem (video 43), both seen
here in the one case we can compute exactly.

## Key ideas (in dependency order)
1. **The setup.** A sequence `X_1, X_2, ...` and a limit `X`, all random
   variables on one probability space — all functions of the outcome of
   the *same* experiment. Without that, `|X_n - X|` means nothing.
2. **Worked: the concentrating sequence.** For iid Gaussian `X_i` with
   mean m and variance `sigma^2`, `S_n = X_1 + ... + X_n` is Gaussian
   (sums and affine maps of Gaussians stay Gaussian — video 40), with
   `E[S_n/n] = m` and `Var[S_n/n] = sigma^2/n`. The PDF of `S_n/n`
   concentrates around m: the sequence becomes increasingly predictable.
3. **Worked: the invariant sequence.** Same ingredients, different
   scaling: `(S_n - nm)/sqrt(n)` has mean 0 and variance `sigma^2` — a
   Gaussian whose distribution is the same for every n. One sequence
   collapses, the other holds its shape.
4. **Convergence in probability.** For every `epsilon > 0`,
   `lim_{n -> inf} Pr(|X_n - X| >= epsilon) = 0` — deviations of any
   fixed size become vanishingly rare. In the first example, `S_n/n`
   converges in probability to m.
5. **Mean square convergence.** `lim_{n -> inf} E[|X_n - X|^2] = 0` —
   the mean squared error itself dies.
6. **Mean square implies in probability.** Chebyshev applied to
   `X_n - X`: `Pr(|X_n - X| >= epsilon) <= E[|X_n - X|^2] / epsilon^2`,
   and the right side can be made arbitrarily small — video 35's
   inequality converting one mode of convergence into another.
7. **Convergence in distribution.** `lim_{n -> inf} F_{X_n}(x) = F_X(x)`
   at every x where `F_X` is continuous — the weakest notion, also
   called weak convergence: only the CDFs need to settle.
8. **Worked: uniform on [0, 1/n].** `X_n` uniform on `[0, 1/n]`
   converges in distribution to 0: `F_X(x)` is the unit step at 0,
   `F_{X_n}(x) = 0` for x < 0, and `F_{X_n}(x) -> 1` for every x > 0.
   The continuity-point clause earns its keep at x = 0.

## What else (connections, to seed callbacks in narration)
- Chebyshev's inequality (video 35) reappears as the *engine* of a
  limit statement — and video 42 will run the same move on `S_n/n`.
- The sums `S_n` are video 25's empirical sums, now with video 40's
  convolution machinery behind them (Gaussian + Gaussian = Gaussian).
- Convergence in distribution has been on screen twice already: the
  geometric staircase melting into the exponential CDF (video 29), and
  the binomial converging to the Poisson (video 16) — now the pattern
  gets its name.
- The unit-step limit CDF is video 26's staircase language: a constant
  is a random variable whose CDF is one jump.

## Conceptual progression (drives the storyboard)
One experiment, a whole sequence of functions on it → the Gaussian
average: variance sigma^2/n, the PDF squeezing onto m → the standardized
sum: the shape that refuses to move → two behaviors need two (three)
vocabularies → convergence in probability: the epsilon-band picture →
mean square convergence: the error's second moment dies → Chebyshev
bridges the two (video 35 returns) → convergence in distribution: only
the CDFs must settle → uniform on [0, 1/n]: ramps steepening into a
step, with the continuity fine print visible → the stage is set for two
theorems.

## Visual opportunities
- **The squeeze**: Gaussian PDFs of `S_n/n` for n = 1, 4, 16, 64 drawn
  in sequence over a fixed mark at m — each narrower and taller, the
  variance label counting down sigma^2/n.
- **The invariant bell**: the PDF of `(S_n - nm)/sqrt(n)` redrawn for
  the same n values — identical every time; only the n counter changes.
- **Epsilon band**: a horizontal band of half-width epsilon around m;
  the shaded tail mass of `S_n/n` outside the band visibly draining to
  zero as n grows — convergence in probability made literal.
- **The bridge**: Chebyshev's inequality from video 35 slides in,
  `X_n - X` substituted, and the mean-square hypothesis caps the bound.
- **Ramp to step**: the CDFs of uniform [0, 1/n] for n = 1, 2, 5, 20 —
  ever-steeper ramps converging onto the unit step at 0, with the
  single point x = 0 flagged as exempt.

## Notation (per project.yaml)
- Probabilities `\Pr`, expectation `\mathrm{E}`, variance `\mathrm{Var}`;
  sums `S_n = \sum_{i=1}^n X_i`; CDFs `F_{X_n}(x)`; deviations
  `\left| X_n - X \right| \geq \epsilon`.

## Deliberately out of scope
- The law of large numbers as a theorem — video 42 states and proves it;
  here the Gaussian average is only an observed pattern.
- The central limit theorem — video 43; the invariant bell is left as a
  mystery to be resolved.
- Almost-sure convergence and the full hierarchy of implications beyond
  "mean square implies in probability" — the notes state only that one.
- Heavy-tailed counterexamples — video 42's starred coda.

## Cut first (if the script runs over budget)
The uniform-[0, 1/n] example compresses to the ramp-to-step animation
with the algebra reduced to one spoken sentence; the proof of
"mean square implies in probability" compresses to the Chebyshev line
alone (the delta bookkeeping dropped).
