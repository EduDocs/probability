---
slug: 18-expected-values
title: Expected Values
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03 ("Proceed")
source: sources/18-expected-values.tex
source_sha256: 7d9dd7a05900c28f44df3fc44020688a88d369c496d80b458771ff4f674a8d25
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_expectations.tex
companion: sources/18-expected-values.md
companion_sha256: b99ba1690b46f38674b6e913054edefe24cd3d73c2dae1d2e1702b69fed80027
prereqs:
  - 17-functions-of-random-variables
audience: undergraduate engineering, first probability course
concepts:
  - id: why-summarize
    name: Summarizing a PMF
    importance: core
    one_liner: A PMF describes a random variable completely, but often one number — an average — is what we actually want; the expectation operator produces it.
  - id: expectation-def
    name: Expected value of a discrete RV
    importance: core
    one_liner: E[X] = sum over x in X(Omega) of x p_X(x), whenever the sum converges absolutely; also called the mean of X.
  - id: function-of-pmf
    name: E[X] is a function of the PMF, not of X
    importance: highlight
    one_liner: The expected value is computed from the distribution alone; two different random variables with the same PMF have the same mean.
  - id: die-example
    name: Worked example — a fair die
    importance: core
    one_liner: The roll of a fair die has mean sum_{k=1}^{6} k/6 = 3.5 — a value the die can never show.
  - id: geometric-example
    name: Worked example — waiting for heads
    importance: core
    one_liner: Tossing a fair coin until heads, p_X(k) = 2^{-k} on {1, 2, ...}, gives E[X] = sum k/2^k = 2 — an infinite sum collapsing to a simple answer.
  - id: existence
    name: Existence requires absolute convergence
    importance: optional        # cut first if over budget
    one_liner: When the defining sum is not absolutely convergent, X simply has no expected value.
estimated_runtime_sec: 480      # ~8 min (five beats in project.yaml)
---

# Expected Values — Concept Map

This video covers the chapter opener plus Section 6.1 of "Meeting
Expectations" (book chapter 6). Videos 19 (Functions and Expectations)
and 20 (Moments) cover 6.2 and 6.3.

## What
The **expected value** (or **mean**) of a discrete random variable X is the
probability-weighted sum of its values:
`E[X] = sum_{x in X(Omega)} x p_X(x)`, defined whenever the sum converges
absolutely. It condenses the complete description carried by the PMF into a
single meaningful scalar.

## Why it matters
With large collections of data we rarely care about every individual point —
we ask for the average. Random variables deserve the same treatment: the PMF
answers *every* question about X, but that is usually more detail than we
need. The expectation operator is the standard way to distill the PMF into a
descriptive quantity, and it is the gateway to the whole summary toolkit
(variance, moments) built in the rest of the chapter.

## Key ideas (in dependency order)
1. **From full description to summary.** The PMF specifies the probability
   of every value X can take (last video's machinery). Often we want one
   number instead of a full table.
2. **The definition.** `E[X] = sum_{x in X(Omega)} x p_X(x)` — each value,
   weighted by its probability. The sum must converge absolutely; otherwise
   X has no expected value.
3. **A property of the PMF.** `E[X]` is not a function of the random
   variable's realized values; it is a functional of the *distribution*.
   Same PMF, same mean — regardless of the underlying experiment.
4. **Fair die.** `sum_{k=1}^{6} k/6 = 3.5`. Note the mean need not be a
   value the variable can actually take.
5. **Coin until heads (geometric, p = 1/2).** Range `{1, 2, ...}`,
   `p_X(k) = 2^{-k}`, and `E[X] = sum_{k>=1} k 2^{-k} = 2`: on average two
   tosses to see heads. A countably infinite sum yielding a crisp answer.
6. **Input/output view.** Expectation takes a detailed object (the PMF) and
   returns a scalar attribute — a concise summary of overall behavior.

## What else (connections, to seed callbacks in narration)
- The die and the coin-until-heads experiments are running examples from
  videos 15–16 (PMF, geometric RV) — reuse them, don't reintroduce them.
- The geometric sum echoes the geometric PMF from video 16.5.
- "Mean" here is exactly the first of the summary quantities; the variance
  and higher moments (videos 19–20) reuse this same weighted-sum pattern.

## Conceptual progression (drives the storyboard)
PMF bar chart (full detail) → "what one number summarizes this?" →
weighted-sum definition assembled term by term on the bars → die example
computed on its flat PMF → geometric example with its halving bars →
the funnel picture: PMF in, single scalar out.

## Visual opportunities
- A PMF bar chart where each bar contributes `x * p_X(x)`: values on the
  axis light up, get multiplied by their bar heights, accumulate into a sum.
- The die PMF (six equal bars) collapsing to a marker at 3.5 on the number
  line — visibly *between* the achievable values.
- The geometric PMF's halving bars (reuse the video-16 look) with partial
  sums of `k/2^k` marching to 2.
- The funnel: a detailed PMF entering, the scalar `E[X]` leaving —
  "a concise summary of overall behavior."

## Notation (per project.yaml)
- Expectation `\mathrm{E}[X]` (never the blackboard-bold or operator forms).
- PMF `p_X(x)`; range `X(\Omega)`; sums `\sum_{x \in X(\Omega)}`.

## Deliberately out of scope
- Expectations of functions `E[g(X)]` — next video (6.2).
- Variance, standard deviation, moments — videos 19 and 20.
- The center-of-mass interpretation — saved for video 19 (The Mean), where
  the book develops it.
- A general treatment of when sums fail to converge — one sentence only.
