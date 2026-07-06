---
slug: 38-conditioning-densities
title: Conditioning with Densities
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 38-conditioning-densities.md
derived_from_sha256: 92493176a08a61f0dee0a00727b760f020d05aaa7ab44e9040fd0d73c6357f0a
provenance_stamped: 2026-07-06
target_scene_file: scenes/conditioning_densities.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Slice the joint density and renormalize - condition on events, on exact values, and estimate through noise."
  recap: "Last video: the joint density as a surface over the plane, marginals by integrating one variable out."
  key_idea: "Conditioning a density is slicing and renormalizing - and every slice has a mean, the conditional expectation."
  bridge: "Next: independence -- when every slice of the surface looks the same."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word --
# the target budgets the FINAL.
target_runtime_sec: 320
tolerance_sec: 45

estimated_runtime_sec: 367
measured_runtime_sec: 347.5

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 105
    est_sec: 40
    measured_sec: 40.5
    sync_points: [event, values, average, transform]
  - id: on-event
    scene_class: ConditionOnEvent
    narration_words: 208
    est_sec: 80
    measured_sec: 74.6
    sync_points: [ratio, derivative, interval, lifetime, truncate, rescale,
                  rises, echo, region, arrivals, any-region]
  - id: on-values
    scene_class: ConditionOnValues
    narration_words: 228
    est_sec: 88
    measured_sec: 78.9
    sync_points: [prob-zero, box, window, honest, cancel, formula,
                  definition, integrate, slice, profile, disk, chord,
                  marginal, uniform, flat]
  - id: cond-expectation
    scene_class: ConditionalExpectation
    narration_words: 198
    est_sec: 76
    measured_sec: 72.0
    sync_points: [integral, event-version, h-of-x, random-h, channel,
                  transmit, noise, guess, slice-gauss, collapse, mmse,
                  workhorse]
  - id: jacobian
    scene_class: JacobianDerived
    narration_words: 214
    est_sec: 83
    measured_sec: 81.5
    sync_points: [recall, setup, invertible, patch, carries, determinant,
                  formula, dimension-echo, gauss, gauss-form, survive, outro]
---

# Video Script — Conditioning with Densities

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> We have just built the joint density: a surface over the plane whose volume
> above a region is probability, with marginals found by integrating one
> variable out. This video slices that surface, because that is how
> observation works in the continuous world: you learn something, and the
> whole model updates. <bookmark mark="event"/> We
> condition a density on an event, and truncate-and-rescale returns in smooth
> form, <bookmark mark="values"/> then condition on an exact value — an event
> of probability zero — and make honest sense of it,
> <bookmark mark="average"/> average the slices to get conditional
> expectation, and let it estimate a signal through noise,
> <bookmark mark="transform"/> and close by transforming pairs with the
> Jacobian formula.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 11  ·  Multiple Continuous
  Random Variables", objective; card rises to the top edge;
  `progress_tag(2, 4)` in the DR corner. Then `self.wait(0.5)` before the
  outline.
- `event`: outline line "1. Conditioning on an event" fades in.
- `values`: outline line "2. Conditioning on a value" fades in.
- `average`: outline line "3. Conditional expectation" fades in.
- `transform`: outline line "4. Derived distributions" fades in.

---

## Beat: on-event  (scene: ConditionOnEvent)

> Chapter four's ratio has served every kind of conditioning so far, and it
> crosses into the continuous world untouched. <bookmark mark="ratio"/> Given
> an event A with positive probability, the conditional CDF of X is the
> probability that X is at most x and A happens, over the probability of A.
> <bookmark mark="derivative"/> Differentiate, and the slope is a genuine
> density: the conditional PDF of X given A. Nothing new is postulated here —
> the ratio we trust meets the CDF we trust. <bookmark mark="interval"/> The
> case to internalize is conditioning on an interval.
> <bookmark mark="lifetime"/> Suppose a component's lifetime is exponential,
> and we learn it failed within the first two years.
> <bookmark mark="truncate"/> Outside the interval the density dies: those
> lifetimes are ruled out. <bookmark mark="rescale"/> Inside, the shape is
> untouched — every value divides by the same number, the probability of
> landing in the interval — <bookmark mark="rises"/> and the curve rises just
> enough to enclose area one. <bookmark mark="echo"/> Truncate and rescale:
> the move we ran on the geometric bars in chapter seven, now on a smooth
> curve. <bookmark mark="region"/> And the event need not involve X alone.
> <bookmark mark="arrivals"/> Condition two exponential arrivals on Y at most
> X, and integrating the joint density over a triangle hands back a clean
> conditional density for X. <bookmark mark="any-region"/> Any region of the
> plane can play the role of A.

**Cues** (per-phrase sub-blocks so each animation lands on its sentence)
- opening: section title "Conditioning on an Event" written, docked up.
- `ratio`: `F_{X \mid A}(x) = \Pr(X \le x \mid A) = \Pr(\{X \le x\} \cap A)
  / \Pr(A)` in accent.
- `derivative`: `f_{X \mid A}(x) = dF_{X \mid A}/dx` beneath it; ratio
  demotes to INK.
- `interval`: the formulas clear and the bare axes arrive (2026-07-05 draft
  review: split so the curve lands on its own sentence).
- `lifetime` (2026-07-05 draft review): the exponential density curve, the
  interval [0, 2] marker, and the caption "lifetime, given failure within
  two years" land on this sentence (no em-dash on screen).
- `truncate`: the curve beyond x = 2 fades to a ghost; the region under the
  kept piece shaded.
- `rescale`: `f_{X \mid A}(x) = f_X(x) / \Pr(X \in I)` written; the
  denominator takes the accent.
- `rises` (2026-07-05 draft review): the kept piece stretches vertically to
  area one exactly as "the curve rises" is spoken.
- `echo` (2026-07-05 draft review): the muted "0 outside I" caption lands on
  the truncate-and-rescale echo.
- `region`: the triangle `\{y \le x\}` glyph and event label arrive — one
  breath, no derivation shown.
- `arrivals` (2026-07-05 draft review): joint density
  `\lambda^2 e^{-\lambda(x+y)}` and the result
  `f_{X \mid A}(x) = 2\lambda e^{-\lambda x}(1 - e^{-\lambda x})` written on
  this sentence.
- `any-region` (2026-07-05 draft review): the result line takes the accent
  on the closing sentence.

---

## Beat: on-values  (scene: ConditionOnValues)

> Now the harder question, and the one observation actually asks. A receiver
> reads Y equals exactly one point three — <bookmark mark="prob-zero"/> but
> for a continuous Y, that event has probability zero, and dividing by zero
> is not conditioning.
> <bookmark mark="box"/> Escape by a limit. <bookmark mark="window"/> Ask
> instead that X land within a small window delta x, given that Y landed
> within a small window delta y. <bookmark mark="honest"/> That ratio is
> honest — both windows have positive probability. <bookmark mark="cancel"/>
> The joint density times both widths, over the marginal times delta y: the
> delta y cancels. <bookmark mark="formula"/> What survives is the
> definition. <bookmark mark="definition"/> The conditional density of X
> given Y equals y is the joint density along the slice, divided by the
> marginal of Y at y — defined wherever that marginal is positive.
> <bookmark mark="integrate"/> Integrate it over a set, and you have the
> conditional probability that X lands there. <bookmark mark="slice"/>
> Picture it on last video's surface: cut across the support at height y,
> <bookmark mark="profile"/> and the profile of the cut, renormalized to
> area one, is the conditional density.
> <bookmark mark="disk"/> Try it on the uniform disk.
> <bookmark mark="chord"/> Given Y equals one half, the slice is a chord
> running from minus root three over two to plus root three over two,
> <bookmark mark="marginal"/> and the marginal there is root three over pi.
> <bookmark mark="uniform"/> Dividing leaves a constant: one over root three
> along the chord. <bookmark mark="flat"/> A flat surface conditions to a
> flat slice — uniform in, uniform out.

**Cues**
- opening: section title "Conditioning on a Value".
- `prob-zero` (2026-07-05 draft review): the card `\Pr(Y = y) = 0` and its
  muted caption "cannot divide by this" land as "probability zero" is
  spoken, not at the beat's start.
- `box`: the card clears; the shaded support region in the (x, y) plane
  arrives.
- `window` (2026-07-05 draft review): the small
  `\Delta_x \times \Delta_y` box pops in and the window ratio line is
  written on this sentence.
- `honest` (2026-07-05 draft review): the ratio's density form
  `f_{X,Y}(x,y)\Delta_x\Delta_y / (f_Y(y)\Delta_y)` written.
- `cancel` (2026-07-05 draft review): the box flattens onto the line y and
  the `\Delta_y` terms cancel exactly as "the delta y cancels" is spoken.
- `formula`: the limit lines clear.
- `definition` (2026-07-05 draft review):
  `f_{X \mid Y}(x \mid y) = f_{X,Y}(x,y) / f_Y(y)` in accent; muted caption
  "defined when f_Y(y) > 0".
- `integrate` (2026-07-05 draft review):
  `\Pr(X \in S \mid Y = y) = \int_S f_{X \mid Y}(x \mid y)\,dx` written on
  its own sentence.
- `slice`: the box picture yields to a slice strip across the support at
  height y.
- `profile` (2026-07-05 draft review): the profile curve lifts out and
  inflates to area one as renormalization is spoken.
- `disk`: the picture clears; the unit disk arrives.
- `chord` (2026-07-05 draft review): the horizontal chord at y = one half
  with endpoints marked at `\pm\sqrt{3}/2`.
- `marginal` (2026-07-05 draft review): `f_Y(0.5) = \sqrt{3}/\pi` written on
  this clause.
- `uniform`: the flat conditional `f_{X \mid Y}(x \mid 0.5) = 1/\sqrt{3}`
  drawn as a level segment above the chord, in accent.
- `flat` (2026-07-05 draft review): the level segment holds through the
  closing "uniform in, uniform out" breath.

---

## Beat: cond-expectation  (scene: ConditionalExpectation)

> Each observation hands us a fresh density — and any density has a mean.
> <bookmark mark="integral"/> The conditional expectation of g of Y, given X
> equals x, is an integral now: g of y, weighted by the conditional density
> of the slice. <bookmark mark="event-version"/> Given an event, the same
> formula runs with the event-conditioned density. <bookmark mark="h-of-x"/>
> Chapter seven's discovery returns intact: sweep the observation, and the
> slice means trace a function, h of x. <bookmark mark="random-h"/> Feed the
> random X in, and the conditional expectation of Y given X is itself a
> random variable. <bookmark mark="channel"/> Here is that machine doing
> engineering. <bookmark mark="transmit"/> A transmitter sends a standard
> Gaussian signal X. <bookmark mark="noise"/> The channel adds independent
> standard Gaussian noise N, and the receiver reads Y equals X plus N.
> <bookmark mark="guess"/> Given the value received, what should it guess
> for X?
> <bookmark mark="slice-gauss"/> Slice the joint Gaussian surface at the
> received y. <bookmark mark="collapse"/> The algebra collapses to a
> Gaussian in x, with mean y over two and variance one half.
> <bookmark mark="mmse"/> The minimum mean square error estimate is the mean
> of that slice: the estimate of X is y over two — split the difference
> between the received value and the zero-mean prior.
> <bookmark mark="workhorse"/> That estimator, a conditional expectation, is
> the workhorse of communication and control.

**Cues**
- opening: section title "Conditional Expectation". Both stacked equations
  render at BODY size — the event version matches the first equation's size
  (2026-07-05 draft review) — and the stack is distributed with even gaps.
- `integral`: `\mathrm{E}[g(Y) \mid X = x] = \int g(y)\, f_{Y \mid X}(y \mid
  x)\, dy` in accent.
- `event-version` (2026-07-05 draft review): the event version
  `\mathrm{E}[g(Y) \mid S] = \int g(y)\, f_{Y \mid S}(y)\, dy` beneath,
  muted, landing on "Given an event".
- `h-of-x`: `h(x) = \mathrm{E}[Y \mid X = x]` written (video 23's card,
  integrals in place of sums).
- `random-h` (2026-07-05 draft review): the morph to
  `h(X) = \mathrm{E}[Y \mid X]` and the caption "a random variable" land on
  "Feed the random X in".
- `channel`: the equation stack clears.
- `transmit` (2026-07-05 draft review): the X box, its arrow, and the plus
  node arrive with "a transmitter sends".
- `noise` (2026-07-05 draft review): the N arrow drops in, the Y output box
  arrives, and `Y = X + N` is written as the receiver line is spoken.
- `guess` (2026-07-05 draft review): the diagram holds for the question.
- `slice-gauss`: the axes and the sliced Gaussian profile drawn.
- `collapse` (2026-07-05 draft review): the conditional density
  `f_{X \mid Y}(x \mid y) = \frac{1}{\sqrt{\pi}} e^{-(4x^2 - 4xy + y^2)/4}`
  compresses to "Gaussian, m = y/2, sigma^2 = 1/2" on this sentence.
- `mmse`: `\mathrm{E}[X \mid Y = y] = y/2` in accent; the peak of the curve
  projects down to x = y/2.
- `workhorse` (2026-07-05 draft review): the estimate holds through the
  closing sentence.

---

## Beat: jacobian  (scene: JacobianDerived)

> One tool remains: transforming pairs. <bookmark mark="recall"/> Chapter
> nine turned the density of X into the density of g of X, paying with the
> derivative of g.
> <bookmark mark="setup"/> Now map two variables to two. Y one and Y two are
> functions of X one and X two — differentiable,
> <bookmark mark="invertible"/> and invertible, so every output point comes
> from exactly one input point. <bookmark mark="patch"/>
> Watch a small square of probability. <bookmark mark="carries"/> The map
> carries it to a parallelogram, <bookmark mark="determinant"/> and the
> factor by which its area stretches is the Jacobian determinant, the
> determinant of the two-by-two matrix of partial derivatives.
> <bookmark mark="formula"/> Probability itself cannot stretch, so the
> density must compensate: the joint density of the new pair is the old
> density at the pre-image, divided by the absolute Jacobian.
> <bookmark mark="dimension-echo"/> One dimension paid with the absolute
> derivative of g. Two dimensions pay with a determinant.
> <bookmark mark="gauss"/> The star application takes one breath: push a
> jointly Gaussian vector through any invertible affine map, A X plus b,
> <bookmark mark="gauss-form"/> and the Jacobian formula returns the
> Gaussian form — mean A m plus b, covariance A Sigma A transpose.
> <bookmark mark="survive"/> Gaussians survive every affine map, in any
> dimension, which partly explains why they dominate engineering.
> <bookmark mark="outro"/> The key idea of this video: conditioning a density
> is slicing and renormalizing — and every slice has a mean, which is the
> conditional expectation.

**Cues**
- opening: section title "Derived Distributions".
- `recall` (2026-07-05 draft review): the recall card
  `f_Y(y) = f_X(x)/|g'(x)|` muted (chapter nine's formula) lands on its
  sentence, not at the beat's start.
- `setup`: `Y_1 = g_1(X_1, X_2),\; Y_2 = g_2(X_1, X_2)` written.
- `invertible` (2026-07-05 draft review): the "invertible" caption fades in
  as the word is spoken.
- `patch`: two small planes side by side, shifted left to free a right-hand
  math column (2026-07-05 draft review): the square patch appears in the
  (x1, x2) plane.
- `carries` (2026-07-05 draft review): the map arrow and the parallelogram
  image land on this clause.
- `determinant` (2026-07-05 draft review): the area factor
  `|J(x_1, x_2)| = \det[\partial g_i / \partial x_j]` written in the right
  column.
- `formula`: `f_{Y_1,Y_2}(y_1,y_2) = f_{X_1,X_2}(x_1,x_2) / |J(x_1,x_2)|`
  in accent, placed directly below the Jacobian expression (2026-07-05
  draft review) so the beat reads as one balanced composition.
- `dimension-echo` (2026-07-05 draft review): the formula holds through the
  one-dimension/two-dimensions echo.
- `gauss`: the frame clears; `\mathbf{Y} = A\mathbf{X} + \mathbf{b}`
  written.
- `gauss-form` (2026-07-05 draft review): mean `A\mathbf{m} + \mathbf{b}`,
  covariance `A \Sigma A^{\mathrm{T}}` written as they are spoken.
- `survive` (2026-07-05 draft review): the Gaussian-form line takes the
  accent; "Gaussian in, Gaussian out" caption fades in.
- `outro`: shared outro card — key idea + "Coming up: Independent
  Continuous Variables". Card line matches the spoken close: "every slice
  has a mean: the conditional expectation." (2026-07-05 draft review).

---

## Cut list (if over budget)

1. Drop the `region` breath in `on-event` (the exp-race card) — the
   interval picture already carries event conditioning. Saves ~45 words.
2. Compress `gauss` in `jacobian` to the formulas with a single spoken
   clause ("and Gaussians survive every affine map"). Saves ~40 words.
3. Trim the closing sentence of `on-values` ("A flat surface...").
