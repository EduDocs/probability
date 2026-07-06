---
slug: 42-law-large-numbers
title: The Law of Large Numbers
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-04
source: sources/42-law-large-numbers.tex
source_sha256: c13bf4618eb4bbe38d3a7468994a46bd69e62bf1753311394259509f2466e2c5
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/empirical_sums.tex
companion: sources/42-law-large-numbers.md
companion_sha256: 51341fb22e74140f95766dd58eb5134122f48455900bc4f5c1726b03d683b956
prereqs:
  - 41-convergence
audience: undergraduate engineering, first probability course
concepts:                 # one entry per idea worth a beat
  - id: lln-statement
    name: The law of large numbers
    importance: core
    one_liner: For iid X_i with finite variance, Pr(|S_n/n - E[X]| >= epsilon) -> 0 — the empirical average converges in probability to the mean.
  - id: mean-and-variance
    name: The average's mean and variance
    importance: core
    one_liner: E[S_n/n] = E[X] and, by independence, Var[S_n/n] = Var[X]/n — the average is unbiased and its spread dies like 1/n.
  - id: chebyshev-closes
    name: Chebyshev finishes the proof
    importance: highlight
    one_liner: Vanishing variance gives mean square convergence, and Pr(|S_n/n - E[X]| >= epsilon) <= Var[X]/(n epsilon^2) — video 35's inequality is the engine of the whole theorem.
  - id: die-frequency
    name: Worked example — counting sixes
    importance: core
    one_liner: X_n = 1_{D_n = 6} is Bernoulli(1/6), so the fraction of sixes converges in probability to 1/6 — relative frequency converges to probability.
  - id: cauchy-stability
    name: Sums of Cauchy random variables (starred)
    importance: optional        # starred subsection; first in the cut list
    one_liner: Convolving two independent Cauchy densities (contour integration, two residues) gives another Cauchy with parameter gamma_1 + gamma_2.
  - id: cauchy-refusal
    name: The average that never settles (starred)
    importance: optional        # starred subsection; first in the cut list
    one_liner: S_n is Cauchy(n gamma), so S_n/n is Cauchy(gamma) — the SAME density for every n; no finite second moment, no law of large numbers.
estimated_runtime_sec: 310
---

# The Law of Large Numbers — Concept Map

This video covers Section 12.2 of book chapter 12, including the starred
subsection on heavy-tailed distributions. Video 41 supplied the
convergence vocabulary this theorem is stated in; video 43 closes the
course with the companion result, the central limit theorem.

## What
The **law of large numbers**: for independent and identically distributed
`X_1, X_2, ...` with mean `E[X]` and finite variance, the empirical
average `S_n/n = (X_1 + ... + X_n)/n` converges in probability to `E[X]`
— `Pr(|S_n/n - E[X]| >= epsilon) -> 0` for every `epsilon > 0`. The proof
is three lines the course has already paid for: the average has mean
`E[X]`, independence makes its variance `Var[X]/n`, and Chebyshev's
inequality converts vanishing variance into vanishing deviation
probability. The starred coda shows the hypothesis is not decoration:
Cauchy averages have the *same* Cauchy density for every n — with no
finite second moment, the law simply does not apply.

## Why it matters
This is the theorem that makes probability empirical: the fraction of
sixes in a long run of die rolls converges to `Pr(six) = 1/6`, so the
"long-run frequency" reading of probability — the intuition the whole
course has leaned on since chapter 1 — is now a *theorem* inside the
axioms. It is also the engineering charter of the chapter's opening:
concentration is what permits designing large systems around expected
behavior. And the Cauchy coda settles an old score: video 30 showed
sample means that refused to settle; this video explains exactly why.

## Key ideas (in dependency order)
1. **The statement.** For iid `X_1, X_2, ...` with mean `E[X]` and
   finite variance, for every `epsilon > 0`:
   `lim_{n -> inf} Pr(|S_n/n - E[X]| >= epsilon) = 0` — convergence in
   probability of the empirical average to the mean (the simplest of the
   law's many versions).
2. **The average is unbiased.** `E[S_n/n] = (E[X_1] + ... + E[X_n])/n =
   E[X]` — linearity, no independence needed.
3. **Its variance dies.** By independence,
   `Var[S_n/n] = (Var[X_1] + ... + Var[X_n])/n^2 = Var[X]/n` — video
   24's variance-of-a-sum rule doing the heavy lifting. Since
   `E[|S_n/n - E[X]|^2] = Var[S_n/n] -> 0`, the average converges to
   `E[X]` in mean square.
4. **Chebyshev closes.** `Pr(|S_n/n - E[X]| >= epsilon) <=
   Var[X]/(n epsilon^2)`, which goes to zero — the same move as video
   41's Proposition, now proving a named theorem. Video 35's inequality
   is the engine of the weak law.
5. **Worked: counting sixes.** Roll a die repeatedly; let
   `X_n = 1_{D_n = 6}`, a Bernoulli(1/6) indicator. Then `S_n/n` is the
   fraction of sixes, and
   `Pr(|S_n/n - 1/6| >= epsilon) -> 0`: relative frequency converges to
   probability.
6. **Starred: Cauchy sums stay Cauchy.** For independent Cauchy
   `X_1, X_2` with parameters `gamma_1, gamma_2`, the convolution
   integral — evaluated by contour integration, two simple poles —
   yields `f_S(x) = (gamma_1 + gamma_2) / (pi((gamma_1 + gamma_2)^2 +
   x^2))`: Cauchy again, parameters adding.
7. **Starred: the average that never settles.** By induction `S_n` is
   Cauchy(`n gamma`), and the derived-distribution scaling (chapter 9)
   gives `S_n/n` the density `gamma / (pi(gamma^2 + x^2))` — identical
   for every n. No concentration, ever; the finite-second-moment
   hypothesis is violated, and the law of large numbers does not apply.

## What else (connections, to seed callbacks in narration)
- Chebyshev's inequality (video 35, book chapter 10) was proved as a
  bound; here it becomes an engine — the explicit payoff of that video.
- Video 30 introduced the Cauchy and its refusal to average out; the
  starred coda is that scene explained, not just observed.
- The convolution-of-densities move is video 40's; the scaling of
  `S_n/n` is chapter 9's derived-distribution methodology (video 32).
- The indicator trick `X_n = 1_{D_n = 6}` is video 19's
  `E[1_S] = Pr(S)` bridge, now run in the limit.
- The empirical sums `S_n` were named in video 25; this is the theorem
  they were named for.

## Conceptual progression (drives the storyboard)
The claim, in words: averages settle → the statement, quantified with
epsilon → the proof in three known moves: unbiased mean → variance
`Var[X]/n` (independence) → mean square convergence for free →
Chebyshev converts it to convergence in probability → the die: fraction
of sixes hugging 1/6 — frequency-as-probability becomes a theorem → but
the fine print matters: the Cauchy → sums of Cauchys stay Cauchy
(parameters add) → so `S_n/n` is Cauchy(`gamma`) for every n — the
distribution that never narrows → finite variance was load-bearing all
along.

## Visual opportunities
- **The settling trace**: a running empirical average of die-roll
  indicators plotted against n, jittering early and hugging the 1/6
  line late; the epsilon band from video 41 overlaid, exits becoming
  rare.
- **Variance bar**: a bar of height `Var[X]/n` shrinking as the n
  counter ticks — the 1/n decay on display next to the Chebyshev bound
  `Var[X]/(n epsilon^2)`.
- **Proof as three dominoes**: mean line, variance line, Chebyshev line
  appearing in sequence, each tagged with the video that paid for it
  (24, 35, 41).
- **Cauchy contrast**: the Gaussian-average PDFs squeezing (video 41's
  animation recalled), then the Cauchy-average PDF redrawn for n = 1,
  10, 100 — landing on itself every time (shown in sequence, one curve
  at a time per house rule).
- **The wandering mean**: a Cauchy running-average trace that keeps
  taking violent excursions no matter how large n gets — video 30's
  mystery, replayed as explanation.

## Notation (per project.yaml)
- Probabilities `\Pr`, expectation `\mathrm{E}`, variance `\mathrm{Var}`,
  indicator `\mathbf{1}_{\{D_n = 6\}}`; empirical sum
  `S_n = \sum_{i=1}^n X_i`; Cauchy parameter `\gamma`.

## Deliberately out of scope
- The strong law and almost-sure convergence — the notes state only the
  weak law's "simplest form"; so do we.
- The central limit theorem and the `sqrt(n)` scaling — video 43.
- The full contour-integration mechanics (residue computations shown as
  headline plus result, not derived step by step on screen).
- Convergence in distribution plays no role here — it belongs to videos
  41 and 43.

## Cut first (if the script runs over budget)
The starred heavy-tailed coda goes first: cauchy-stability drops to one
spoken sentence ("sums of Cauchys are Cauchy — parameters add") over a
single density picture, and cauchy-refusal keeps only the n = 1, 10,
100 overlay with its moral. If still over, the die example compresses
to the settling-trace animation with one line of narration.
