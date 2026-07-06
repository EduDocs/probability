---
slug: 27-pdfs-expectation
title: Densities and Expectation
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 27-pdfs-expectation.md
derived_from_sha256: 8ae214e6421bc32f31a59484118191c54097a311a89a231811ea62249ebd662a
provenance_stamped: 2026-07-06
target_scene_file: scenes/pdfs_expectation.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Differentiate the CDF into the density, read probabilities as areas, and rebuild expectation as an integral."
  recap: "Last video: the CDF bridge - staircases for discrete variables, smooth progressions for continuous ones."
  key_idea: "The density is the CDF's slope, probabilities are areas under it, and expectation rides the same integral."
  bridge: "Next: the distributions everyone uses - the uniform and the Gaussian."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# Series calibration: nova finals measure ~0.31 s/word. ~950 words -> ~295 s.
target_runtime_sec: 300
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / 2.6 (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 371
measured_runtime_sec: 339.2

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 98
    est_sec: 38
    measured_sec: 39.1
    sync_points: [density, area, expectation]
  - id: density
    scene_class: DensityDefinition
    narration_words: 213
    est_sec: 82
    measured_sec: 77.9
    sync_points: [slope, ftc, duality, drag, interval, area]
  - id: properties
    scene_class: DensityProperties
    narration_words: 222
    est_sec: 85
    measured_sec: 76.2
    sync_points: [strip, shrink, zero, endpoints, not-prob, tall, axiom-one, axiom-two, admissible]
  - id: expectation
    scene_class: ExpectationIntegral
    narration_words: 236
    est_sec: 91
    measured_sec: 78.0
    sync_points: [discrete, morph, mean, variance, shortcut, tail, columns, rows]
  - id: darts
    scene_class: DartboardExample
    narration_words: 196
    est_sec: 75
    measured_sec: 68.0
    sync_points: [setup, ring, tail, integrate, result, outro]
---

# Video Script — Densities and Expectation

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video built the bridge: the cumulative distribution function, one
> function that describes any random variable — staircases for the
> discrete, smooth progressions for the continuous. <bookmark mark="density"/> In
> this video we differentiate that smooth function and meet the density, the working
> object of the continuous world for the rest of the course,
> <bookmark mark="area"/> read the probabilities of intervals as areas
> under it, and see why single exact points carry no probability at all,
> <bookmark mark="expectation"/> then rebuild expectation on integrals,
> where the mean and the variance survive word for word, and finish with a
> trick that computes a mean from tail probabilities alone.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 8 · Continuous Random
  Variables", objective; card rises to the top edge; progress_tag(2, 5)
  in the DR corner.
- `density`: outline line "1. The probability density function" fades in.
- `area`: outline line "2. Probabilities as areas" fades in.
- `expectation`: outline line "3. Expectation and the tail formula" fades
  in.

---

## Beat: density  (scene: DensityDefinition)

> Take a continuous random variable, one whose CDF is a smooth function,
> differentiable almost everywhere. <bookmark mark="slope"/> Its derivative
> gets a name: the probability density function, f of x, the slope of the
> CDF at each point. Where the function climbs steeply, the density stands
> tall; where the function flattens out, the density falls back toward zero.
> <bookmark mark="ftc"/> And the fundamental theorem of
> calculus runs the definition backwards: integrate the density from minus
> infinity up to x, and the CDF reappears. Differentiate to go one way,
> integrate to come back. <bookmark mark="duality"/> Watch the two
> functions together: the CDF above, its density below.
> <bookmark mark="drag"/> Slide a point x along the axis, and the shaded
> area under the density, up to x, always matches the height of the CDF.
> Height above, area below — the same information, stored two ways.
> <bookmark mark="interval"/> That reading turns last video's interval
> formula into a picture. The probability that X lands between x one and
> x two is the CDF difference, <bookmark mark="area"/> which is exactly
> the integral of the density across the interval. Probabilities of
> intervals are areas under the density curve. Where the density runs
> tall, the variable lands there often; where it hugs zero, it almost
> never does. The density spreads probability along the line the way the
> mass function once stacked it on points.

**Cues** (CDF above, density below; one moving x drags a shaded area)
- opening: section title "The Probability Density Function" docks up.
- `slope`: `f_X(x) = dF_X/dx (x)` written in accent beside the stacked
  axes.
- `ftc`: `F_X(x) = \int_{-\infty}^x f_X(u)\,du` written beneath it; the
  definition demotes to ink.
- `duality`: the two stacked plots drawn — CDF function on top, its bell-ish
  derivative below, sharing an x-scale.
- `drag`: a dot slides along x; the area under f up to x fills while a
  vertical marker on the CDF tracks the matching height.
- `interval`: `Pr(x_1 < X <= x_2) = F_X(x_2) - F_X(x_1)` recalled.
- `area`: the strip between x one and x two shades under the density; the
  formula extends with `= \int_{x_1}^{x_2} f_X(u)\,du` in accent.

---

## Beat: properties  (scene: DensityProperties)

> The area picture answers a natural question with a surprise. What is
> the probability that X hits one exact value? <bookmark mark="strip"/>
> Take a strip under the density, from x one up to x two,
> <bookmark mark="shrink"/> and slide x one upward. The strip narrows, its
> area drains away, <bookmark mark="zero"/> and in the limit nothing is
> left: for a continuous random variable, the probability that X equals
> any single point is exactly zero. <bookmark mark="endpoints"/> A useful
> corollary follows at once: open or closed, endpoints never matter — all
> four interval probabilities agree. <bookmark mark="not-prob"/> And a
> warning worth its own frame: f of x is not the probability that X equals
> x. It is a density, probability per unit length.
> <bookmark mark="tall"/> A tall, narrow density can rise far above one:
> squeeze the same unit of area onto a thinner base, and the height must
> grow. Only areas are probabilities, never heights.
> <bookmark mark="axiom-one"/> The axioms survive the translation. The
> variable lands somewhere, so the total area under the density is one —
> normalization, in its new clothes. <bookmark mark="axiom-two"/>
> Probabilities are nonnegative, so the density never dips below zero.
> <bookmark mark="admissible"/> And for any admissible set S, the
> probability that X falls in S is the integral of the density over S.
> Two conditions, nonnegative and total area one, and a function essentially qualifies
> as a density — that is all it takes to specify a continuous model.

**Cues** (one density curve reused across the whole beat)
- opening: section title "What a Density Must Satisfy" docks up.
- `strip`: the density curve with a shaded strip between x one and x two.
- `shrink`: the strip's left edge slides right toward x two; the sliver
  narrows.
- `zero`: `Pr(X = x) = 0` lands in accent as the sliver vanishes.
- `endpoints`: caption line "endpoints never matter" with the four
  interval forms shown equal (muted).
- `not-prob`: `f_X(x) \ne Pr(X = x)` — the warning card.
- `tall`: the curve morphs into a tall narrow spike crossing the dashed
  line y = 1; caption "a density can exceed one."
- `axiom-one`: `\int_{-\infty}^{\infty} f_X(u)\,du = 1` written; total
  area flashes.
- `axiom-two`: `f_X(x) \ge 0` written beside it.
- `admissible`: `Pr(X \in S) = \int_S f_X(u)\,du` in accent.

---

## Beat: expectation  (scene: ExpectationIntegral)

> Expectation crosses the bridge the same way. <bookmark mark="discrete"/>
> In chapter six, the expected value of g of X weighed each value by its
> probability mass and summed. <bookmark mark="morph"/> Replace the sum by
> an integral and the mass by density times length, and the sentence
> survives word for word: the expectation of g of X is the integral of g
> times the density. Every tool from that chapter rides along for free.
> <bookmark mark="mean"/> Set g to the identity and the
> mean appears: the integral of u times f of u. <bookmark mark="variance"/>
> The variance is the expected squared distance from the mean, exactly as
> before, <bookmark mark="shortcut"/> and the shortcut still holds: the
> mean of the square, minus the square of the mean.
> <bookmark mark="tail"/> But the continuous world offers one genuinely
> new tool. For a nonnegative random variable with finite mean, the mean
> is the integral of the tail: integrate the probability that X exceeds x,
> from zero to infinity — a mean computed without ever touching the
> density. <bookmark mark="columns"/> The proof is a change of
> perspective. The tail integral is a double integral over the region
> where u exceeds x, swept in vertical strips, one for each x.
> <bookmark mark="rows"/> Sweep the same region in horizontal strips
> instead, and each strip runs from zero up to u, so it contributes u
> times f of u — the integrand of the mean. Same region, two ways to
> sweep it: tails on one side, the mean on the other.

**Cues** (the sum-to-integral morph, then the order-swap picture)
- opening: section title "Expectation as an Integral" docks up.
- `discrete`: chapter six's `E[g(X)] = \sum_x g(x) p_X(x)` with a few PMF
  bars beneath it. The chart rides higher on the left half of the frame
  (bottom buff 1.2, not 0.8); as the bars grow in, the first y-tick label
  ("0.09") fades out so no bar overlaps it, and a "0" tick label appears
  on the x-axis. (2026-07-04 draft review, 4:09)
- `morph`: the sigma transforms into an integral sign and `p_X(x)` into
  `f_X(u)\,du` (TransformMatchingTex); the bars melt into a smooth curve
  that extends LEFT past 0 (densities are not confined to the positive
  axis), and at the same moment the chart's y-axis label transforms from
  `p_X(x)` to `f_X(x)`. (2026-07-04 draft review, 4:14)
- `mean`: `E[X] = \int u f_X(u)\,du` written.
- `variance`: `Var(X) = E[(X - E[X])^2]` written beneath.
- `shortcut`: `Var(X) = E[X^2] - (E[X])^2` in accent.
- `tail`: the tail formula `E[X] = \int_0^\infty Pr(X > x)\,dx` in accent
  on a cleared stage.
- `columns`: the triangular region 0 < x < u shaded by vertical strips.
- `rows`: the same region re-shaded by horizontal strips; the two
  integrals shown equal.

---

## Beat: darts  (scene: DartboardExample)

> Let the tail formula show off. <bookmark mark="setup"/> A player throws
> darts at a circular target of unit radius, and every dart lands
> uniformly over the disk — probability proportional to area, the
> geometric models from early in the course. How far from the center
> should we expect a dart to land? <bookmark mark="ring"/> Call the
> distance R, and pick a
> radius r. The dart lands beyond r exactly when it falls outside the
> inner disk of radius r, and for a uniform dart, probability is area
> ratio. <bookmark mark="tail"/> The inner disk has area pi r squared out
> of pi, so the tail is one minus r squared.
> <bookmark mark="integrate"/> That is everything the tail formula needs.
> The expected distance is the integral, from zero to one, of one minus r
> squared, <bookmark mark="result"/> which is r minus r cubed over three,
> evaluated at one: two thirds. Notice what never appeared: the density of
> R. The tail was pure geometry, and the tail formula turned geometry
> straight into a mean. <bookmark mark="outro"/> The key idea of this
> video: the density is the CDF's slope, probabilities are areas under it,
> and expectation rides the same integral. Next up: the distributions
> everyone uses — the uniform and the Gaussian.

**Cues** (the dartboard left, the tail computation right)
- opening: section title "Darts and the Tail Formula" docks up.
- `setup`: a unit disk with a few dart dots scattered uniformly; the
  question `E[R] = ?` beside it.
- `ring`: a circle of radius r inside the disk; the outside annulus
  highlights; `R > r` label.
- `tail`: `Pr(R > r) = 1 - \pi r^2 / \pi = 1 - r^2` written, area ratio
  emphasized. The whole right-hand equation column (question, tail,
  integral, result) sits at x ≈ +2.9 rather than +3.4 for better balance
  against the dartboard. (2026-07-04 draft review, 6:30)
- `integrate`: `E[R] = \int_0^1 (1 - r^2)\,dr` from the tail formula.
- `result`: `= 2/3` lands in accent; caption "no density ever written"
  (muted).
- `outro`: shared outro card — key idea + "Coming up: The Uniform and
  Gaussian Distributions."

---

## Cut list (if over budget)

1. Compress the order-swap proof in `expectation` to one sentence over the
   picture (keep the tail formula statement) — saves ~25 s.
2. Drop the four-forms endpoint display in `properties` (keep the spoken
   "endpoints never matter") — saves ~10 s.
3. Trim the closing flourish of `density` ("Where the density runs
   tall...") — saves ~8 s.
