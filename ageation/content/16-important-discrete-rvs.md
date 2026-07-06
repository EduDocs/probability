---
slug: 16-important-discrete-rvs
title: Important Discrete Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed             # draft | reviewed | approved  (human gate)
source: sources/16-important-discrete-rvs.tex
source_sha256: 5015c13f03c72bce580e69e1b93d862bf8356315ac5ed52a76e3e64986556556
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_random_variables.tex
companion: sources/16-important-discrete-rvs.md
companion_sha256: b5c87cf6e9842e326bd11d2344f531af394339de4087ab9155f583285430a248
companion_upstream: ../chapters/discrete_random_variables.md
prereqs:
  - 15-discrete-random-variables
audience: undergraduate engineering, first probability course
concepts:
  - id: bernoulli
    name: Bernoulli random variable
    importance: core
    one_liner: The atomic building block; X in {0, 1} with Pr(X = 1) = p. Every Bernoulli RV is equivalent to one (biased) coin flip.
  - id: binomial
    name: Binomial random variable
    importance: core
    one_liner: The number of successes in n i.i.d. Bernoulli trials; p_X(k) = C(n,k) p^k (1-p)^{n-k}, which sums to 1 by the binomial theorem.
  - id: poisson
    name: Poisson random variable
    importance: core
    one_liner: Counts occurrences in an interval; p_X(k) = lambda^k / k! e^{-lambda}, normalized by the Taylor series for e^{lambda}.
  - id: binomial-to-poisson
    name: Binomial-to-Poisson limit
    importance: highlight        # the visual climax
    one_liner: With p = lambda/n, Binomial(n, lambda/n) converges to Poisson(lambda) as n grows; the Poisson approximates a binomial with large n and small p.
  - id: geometric
    name: Geometric random variable
    importance: core
    one_liner: The trial index of the first success; p_X(k) = (1-p)^{k-1} p, a geometrically decaying PMF, and the only discrete RV with the memoryless property.
  - id: discrete-uniform
    name: Discrete uniform random variable
    importance: core
    one_liner: All n values equally likely; p_X(k) = 1/n. The fair die and fair coin are special cases.
estimated_runtime_sec: 660        # ~11 min
---

# Important Discrete Random Variables — Concept Map

## What
Section 5.2: a guided tour of the discrete distributions an engineer meets over
and over. Each is tied to a concrete counting story, each has a PMF that
normalizes for a clean reason, and each gets a bar chart on a shared axis so the
shapes are comparable. The visual climax is the **binomial-to-Poisson limit**.

## Why it matters
Discrete random variables arise almost anywhere counting is involved. Knowing
this handful of named PMFs — and the stories that generate them — lets you
recognize a model on sight instead of deriving it from scratch: a single trial
(Bernoulli), a fixed number of trials (binomial), rare events over time
(Poisson), waiting for a first success (geometric), and pure symmetry
(uniform). The binomial→Poisson limit ties two of them together and justifies
the Poisson approximation used throughout applications.

## Key ideas (in dependency order)
1. **Bernoulli(p).** `X(Omega) = {0, 1}`, `Pr(X = 1) = p`, `Pr(X = 0) = 1 - p`.
   Equivalent to one biased coin flip; the atom the others are built from.
2. **Binomial(n, p).** Sum of `n` i.i.d. Bernoulli trials.
   `p_X(k) = C(n,k) p^k (1-p)^{n-k}`, `k = 0..n`. Sums to 1 by the binomial
   theorem: `(p + (1-p))^n = 1`. *Story:* Brazos Soda — win $1 with prob 1/4
   under a cap, 8 bottles; `Pr(X > 4) = sum_{k=5}^{8} C(8,k) 3^{8-k}/4^8`.
3. **Poisson(lambda).** `p_X(k) = lambda^k / k! e^{-lambda}`, `k = 0, 1, ...`.
   Normalizes via `sum lambda^k/k! = e^{lambda}`. *Story:* server requests at
   rate lambda per second; `Pr(no request) = p_N(0) = e^{-lambda}`. Fundamental
   for counting occurrences (networking, queues, inventory).
4. **Binomial → Poisson (the climax).** Fix lambda, set `p_n = lambda/n`. Then
   `lim_{n->inf} C(n,k) (lambda/n)^k (1 - lambda/n)^{n-k} = lambda^k/k! e^{-lambda}`.
   So a binomial with large `n` and small `p` is well approximated by a Poisson
   with `lambda = np`. *Story:* 1000 bits, bit-error prob 1e-2; `Pr(>= 4 errors)
   ~ 0.9897` via Poisson(10) vs exact 0.9899.
5. **Geometric(p).** Number of trials to the first success:
   `p_X(k) = (1-p)^{k-1} p`, `k = 1, 2, ...` — the probability of `k-1` failures
   then a success, a decaying PMF. *Memoryless:*
   `Pr(X = k + j | X > k) = Pr(X = j)`; past failures don't matter, and the
   geometric is the *only* discrete RV with this property.
6. **Discrete uniform on {1..n}.** `p_X(k) = 1/n` — all values equally likely;
   fair coin and fair die are instances.

## Visual plan (beats)
- **overview** — recap video 1 (RV + PMF), preview the gallery, note the
  binomial→Poisson punchline.
- **bernoulli** — two bars at 0 and 1; the coin-flip equivalence.
- **binomial** — grow the `n=8, p=0.25` bars; the formula + normalization; the
  Brazos-Soda story.
- **poisson** — the `lambda=2` bars; the Taylor-series normalization; the server
  story.
- **binomial-to-poisson** — a faint fixed Poisson(10) reference; binomial bars
  redrawn for `n = 5, 15, 25, 35` settling onto it (Transform + n label).
- **geometric** — decaying `p=0.25` bars; the memoryless identity as the aside.
- **uniform** — flat `n=8` bars; fair die/coin; then the video's key-idea outro.

## Notation (per project.yaml)
- `Pr(...)` as `\Pr`; PMF `p_X(k)`; binomial coeff `\binom{n}{k}`.
- Memoryless: `\Pr(X = k + j \mid X > k) = \Pr(X = j)`.

## Out of scope / cut first
- A full derivation of the binomial→Poisson limit (shown as a result, the
  algebra summarized on one line).
- Expectations/variances of these RVs (Chapter 6).
- The uniform beat can be trimmed to a single bar chart if over budget.
