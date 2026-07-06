---
slug: 29-exponential
title: The Exponential Distribution
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved          # human approved via chat 2026-07-03
source: sources/29-exponential.tex
source_sha256: 97aed752ea5c0b160dea541368e4cd64a021b6399ffd9be0c700af4b14c4bb41
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/continuous_random_variables.tex
companion: sources/29-exponential.md
companion_sha256: 03278c8dbecd26d8dca205580ba51bc9f97be65ef64ad47c706c28ed082efb4c
prereqs:
  - 28-uniform-gaussian
audience: undergraduate engineering, first probability course
concepts:
  - id: exp-definition
    name: The exponential distribution
    importance: core
    one_liner: f_X = lambda e^{-lambda x}, F_X = 1 - e^{-lambda x} for x >= 0 — the model for lifetimes and inter-arrival times, with rate lambda.
  - id: server-example
    name: Worked example — inter-arrival times
    importance: core
    one_liner: Requests with exponential(1/2) gaps - Pr(next within 2 min) = 1 - e^{-1}, about 0.632 — one integral, one answer.
  - id: geometric-limit
    name: The geometric, squeezed
    importance: core
    one_liner: Scale a geometric(lambda/n) by 1/n and let n grow - the staircase CDF converges to 1 - e^{-lambda x}; the exponential IS the continuous geometric.
  - id: memoryless
    name: The memoryless property
    importance: core
    one_liner: Pr(X > t + u | X > t) = Pr(X > u) — a used component is as good as new; the exponential is the ONLY continuous distribution with this property.
  - id: half-life
    name: Worked example — half-lives
    importance: core
    one_liner: A disk with a two-year half-life - memorylessness factorizes Pr(T > 2) = Pr(T > 1)^2, so Pr(T < 1) = 1 - 1/sqrt(2), about 0.293 — no lambda needed.
estimated_runtime_sec: 290
---

# The Exponential Distribution — Concept Map

This video covers Section 8.4.3 of book chapter 8. It is the exponential's
own video: videos 26–27 built the CDF/PDF machinery, video 28 opened the
catalog, and video 30 will place the exponential inside the gamma family.

## What
The **exponential distribution** — density `lambda e^{-lambda x}`, CDF
`1 - e^{-lambda x}` on x >= 0 — is the continuous model for waiting:
lifetimes of devices, gaps between arrivals. Two facts give it its
character. It is the *limit of the geometric*: scale a geometric with
success probability lambda/n by 1/n, let n grow, and the staircase CDF
smooths into `1 - e^{-lambda x}`. And it is *memoryless* —
`Pr(X > t + u | X > t) = Pr(X > u)` — the only continuous distribution
with that property, which is exactly what makes half-life reasoning work.

## Why it matters
The exponential is the third leg of the great modeling triad
(uniform / Gaussian / exponential) and the backbone of queueing and
reliability: whenever arrivals are "random in time" (video 22's Poisson
stream), the gaps between them are exponential — the video 22 dot-stream
callback made precise. Memorylessness is both a modeling superpower
(no aging) and a warning label (real parts wear out); the half-life
example shows it computing something concrete with almost no algebra.

## Key ideas (in dependency order)
1. **Definition.** `f_X(x) = lambda e^{-lambda x}`, `F_X(x) =
   1 - e^{-lambda x}` for x >= 0; lambda is a *rate* — bigger lambda,
   shorter waits (three curves, one at a time). This is video 26's cameo
   CDF, now with its name.
2. **Worked: the server.** Inter-arrival time exponential with
   lambda = 1/2; `Pr(T < 2) = 1 - e^{-1} ≈ 0.632` by one integral.
3. **The geometric, squeezed.** Y_n geometric(lambda/n), X_n = Y_n / n:
   `Pr(X_n <= x) = 1 - (1 - lambda/n)^{floor(nx)} -> 1 - e^{-lambda x}`.
   Trials every 1/n of a second, success rate lambda per second — waiting
   in discrete ticks becomes waiting in continuous time.
4. **Memoryless.** `Pr(X > t + u | X > t) = e^{-lambda u} = Pr(X > u)` —
   two lines from the definition of conditional probability. Inherited
   from the geometric through the limit; and among continuous
   distributions, the exponential is the only one.
5. **Worked: half-lives.** Disk half-life two years:
   `Pr(T > 2) = Pr(T > 1)^2` by memorylessness, so
   `Pr(T > 1) = 1/sqrt(2)` and `Pr(T < 1) ≈ 0.293` — lambda never
   computed.

## What else (connections, to seed callbacks in narration)
- Video 22's Poisson-splitting stream drew its dots with exponential
  gaps — this video explains that drawing.
- The geometric's memorylessness appeared in video 23's shopping spree
  (`E[N | N >= 5] = 4 + E[N]`); the exponential inherits the property in
  the limit.
- The limit construction parallels how the Poisson arose from binomials
  (video 16) — same n-to-infinity engine, second time on screen.
- Gamma/Erlang (video 30) will SUM independent exponentials; worth one
  forward-looking breath.

## Conceptual progression (drives the storyboard)
Waiting as the theme (bus was uniform; real arrivals are not) → the
exponential curves, rate on display → server example: one integral →
"where does it come from?" — geometric trials on a finer and finer clock,
staircase melting into the smooth CDF → what the geometric bequeaths:
memorylessness, proved in two lines → used-is-as-good-as-new, said
honestly → half-life: the property doing real work → the triad complete.

## Visual opportunities
- **Rate family**: exponential densities for lambda in {0.5, 1, 2} in
  sequence — steeper start, faster decay.
- **Staircase melts**: the scaled-geometric CDF staircase for n = 4, 12,
  48 morphing into the smooth exponential CDF — the limit as an
  animation, the video's centerpiece.
- **Memoryless**: the density beyond t rescaled (video 22's
  truncate-and-renormalize move, run on a smooth curve) landing exactly
  on the original density — the "restart" made visible.
- **Half-life**: a survival curve with markers at years 1 and 2;
  Pr(T > 2) split into two equal Pr(T > 1) factors.
- **Poisson-stream callback**: video 22's dot stream returns; the gaps
  highlighted and labelled exponential(lambda).

## Notation (per project.yaml)
- Rate `\lambda`; density `f_X`, CDF `F_X`; conditionals with `\mid`;
  floor `\lfloor nx \rfloor` in the limit computation.

## Deliberately out of scope
- The full uniqueness proof that only the exponential is memoryless — the
  fact is stated, not proved.
- Erlang / gamma as sums of exponentials — video 30.
- Poisson-process formalism; the stream stays a picture, not a
  definition.

## Cut first (if the script runs over budget)
The limit derivation compresses to the staircase-melting animation with
the algebra reduced to its first and last lines; the server example can
shrink to a caption under the definition beat.
