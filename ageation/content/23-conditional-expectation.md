---
slug: 23-conditional-expectation
title: Conditional Expectation
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03
source: sources/23-conditional-expectation.tex
source_sha256: 720b9deaf084fab02fbf89e2487f4ad3594bbd53458a78dc1975eca3293c6b7b
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_vectors.tex
companion: sources/23-conditional-expectation.md
companion_sha256: 24365e9d6b861b146df44bdc5fd758e3aedc15ae905f595e143aacdc613a4a68
prereqs:
  - 22-conditioning-rvs
audience: undergraduate engineering, first probability course
concepts:
  - id: cond-exp-given-value
    name: E[Y | X = x]
    importance: core
    one_liner: The mean of the conditional PMF p_{Y|X}(·|x) — one number per observed value x, i.e. a function h(x).
  - id: cond-exp-as-rv
    name: E[Y | X] is a random variable
    importance: core
    one_liner: Feed the random X into h — before the experiment resolves, the conditional expectation h(X) = E[Y|X] is itself random; the soda shop gives E[C|B] = pB.
  - id: tower-property
    name: The tower property
    importance: highlight       # the conceptual climax
    one_liner: E[E[Y|X]] = E[X]-average of the per-slice means = E[Y]; averaging the conditional answers recovers the unconditional one.
  - id: cond-exp-given-event
    name: Conditional expectation given an event
    importance: core
    one_liner: E[X | S] is the mean of p_{X|S}; the same idea with the chapter's other conditioning.
  - id: random-sum
    name: Worked example — the shopping spree
    importance: core
    one_liner: T = sum of N iid shirt costs with N geometric(1/2) — nested conditioning gives E[T] = 21 E[N] = $42, and E[T | N >= 5] = $126 via memorylessness.
estimated_runtime_sec: 480      # ~8 min (five beats in project.yaml)
---

# Conditional Expectation — Concept Map

This video covers Section 7.4 of book chapter 7. Video 22 built the family
of conditional PMFs; this video takes each slice's mean — and discovers the
chapter's deepest object.

## What
The **conditional expectation** `E[Y | X = x]` is simply the mean of the
conditional PMF `p_{Y|X}(·|x)` — one number for each observed x, so it is a
function `h(x)`. The decisive move: feed the *random* X back in. Then
`h(X) = E[Y | X]` is **itself a random variable**, and the **tower
property** `E[E[Y|X]] = E[Y]` says that averaging the per-observation
answers recovers the overall answer. Conditioning on an event works the
same way, and together they crack problems — like a random sum of random
costs — that direct computation cannot easily touch.

## Why it matters
`E[Y|X]` is the best summary of Y available to someone who will observe X —
it is the mathematical backbone of prediction and estimation, and the tower
property is the everyday tool for computing expectations in stages:
condition on what makes the problem easy, average the answers. The shopping
spree shows the full pattern (condition on N, use linearity inside, tower
out) in miniature; the same pattern powers everything from queueing to
machine learning.

## Key ideas (in dependency order)
1. **Per-slice means.** `E[Y | X = x] = sum_y y p_{Y|X}(y|x)` — video 22's
   sliced-and-renormalized PMF, collapsed to its balance point (video 19's
   fulcrum, once per slice).
2. **A function of x.** Collect the per-slice means: `h(x) = E[Y | X = x]`
   is an ordinary function on the values of X.
3. **The decisive move.** Before the experiment, X is random — so `h(X) =
   E[Y | X]` is a random variable. Soda shop: bottles sold B is
   Poisson(10), each cherry with probability p; `E[C | B = 10] = 10p`, and
   in general `E[C | B] = pB` — visibly random because B is.
4. **The tower property.** `E[E[Y|X]] = sum_x E[Y|X=x] p_X(x)`; expand,
   swap the sums, and the joint re-marginalizes: `= E[Y]`. Same for
   `E[E[g(Y)|X]] = E[g(Y)]`.
5. **Given an event.** `E[X | S] = sum_x x p_{X|S}(x)` — the event version,
   with `E[g(X)|S]` alike.
6. **Worked: the shopping spree.** N shirts, N geometric(1/2); each costs
   $10/$20/$50 with probabilities .5/.3/.2 (mean $21), independently.
   `T = sum_{i=1}^N C_i`. Tower on N: `E[T] = E[E[T|N]] = E[21 N] =
   21 E[N] = 42`. Then `E[T | N >= 5] = 21 E[N | N >= 5] = 21 (4 + E[N]) =
   126` — the memoryless property of the geometric doing the last step.

## What else (connections, to seed callbacks in narration)
- The balance-point fulcrum from video 19 returns, planted once per slice
  of video 22's table.
- The soda shop reuses Poisson splitting's setup from video 22 — same
  store, now asking for means instead of PMFs.
- Memorylessness of the geometric was video 16's aside; here it closes a
  real computation.
- The random sum `T = sum C_i` foreshadows Wald-style arguments and the
  empirical sums of the later chapters.
- The tower property is the discrete ancestor of every "condition and
  average" argument to come (total expectation, limit theorems).

## Conceptual progression (drives the storyboard)
One slice of the table → its fulcrum → fulcrums on every slice → connect
them: a function h(x) → feed X in: the function jumps with the observation
(a random variable) → average the fulcrums with the marginal weights: the
tower collapses to E[Y] → event version in one card → the shopping spree
as the grand application.

## Visual opportunities
- **Fulcrums per slice**: video 22's family of conditional PMFs, each with
  its accent fulcrum; the fulcrums trace out h(x) as the slice sweeps.
- **h(X) as a random variable**: the soda-shop card `E[C | B] = pB` with B
  jittering through values and the conditional mean jumping with it.
- **The tower**: per-slice fulcrums, each weighted by its marginal bar,
  merging into one grand fulcrum at E[Y] — the derivation compressed to
  first and last lines beside it.
- **Shopping spree**: a two-level cartoon — a geometric N picks how many
  shirt cards flip over, each card revealing a price; the nested
  expectation written as two shells collapsing inward, 21·E[N] = 42, then
  the N ≥ 5 rerun landing on 126.

## Notation (per project.yaml)
- `\mathrm{E}[Y \mid X = x]`, `\mathrm{E}[Y \mid X]`, `\mathrm{E}[X \mid S]`
  — conditionals with `\mid`; expectation via the helper.

## Deliberately out of scope
- Independence (video 24) — no factoring here.
- Variance decomposition / law of total variance — not in this chapter.
- Formal treatment of E[Y|X] as an estimator (later courses); we show the
  object, not optimality.

## Cut first (if the script runs over budget)
The event-conditioned expectation (idea 5) compresses to a single card; the
N ≥ 5 rerun of the shopping spree drops to a spoken aside with the answer.
