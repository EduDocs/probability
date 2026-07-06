---
slug: 26-cdfs
title: Cumulative Distribution Functions
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 26-cdfs.md
derived_from_sha256: 6b2535ac3ce488d159ec075b018401cf7a188d3f3f68b79d473d1dbb6b76f307
provenance_stamped: 2026-07-06
target_scene_file: scenes/cdfs.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "One function for every random variable: interval probabilities as differences of heights."
  recap: "Last video: Sums and Many Variables closed the discrete chapter - PMFs answered every question we asked."
  key_idea: "Every random variable - discrete, continuous, or mixed - has a CDF, and interval probabilities are differences of heights."
  bridge: "Next: Densities and Expectation - differentiate the ramp and meet the PDF."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# Series calibration: nova finals measure ~0.31 s/word. ~940 words -> ~290 s.
target_runtime_sec: 300
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / wpm (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 277
measured_runtime_sec: 262.5

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 99
    est_sec: 38
    measured_sec: 40.5
    sync_points: [define, staircases, ramps]
  - id: definition
    scene_class: CDFDefinition
    narration_words: 212
    est_sec: 82
    measured_sec: 72.2
    sync_points: [new-object, definition, event, limits, split, interval]
  - id: discrete
    scene_class: DiscreteCDF
    narration_words: 207
    est_sec: 80
    measured_sec: 69.0
    sync_points: [sum, sweep, jump, recover, geometric, difference]
  - id: continuous
    scene_class: ContinuousCDF
    narration_words: 143
    est_sec: 57
    measured_sec: 54.5
    sync_points: [ramp, name, no-mass, derivative]
  - id: mixed
    scene_class: MixedRVs
    narration_words: 50
    est_sec: 20
    measured_sec: 26.3
    sync_points: []
---

# Video Script — Cumulative Distribution Functions

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, sums of discrete random variables closed our story of the discrete world:
> PMFs answered every question we asked. This video opens a new chapter,
> because the discrete world is not enough. Noise voltages, waiting times,
> and signal amplitudes range over a continuum, and no list of values can
> hold them. <bookmark mark="define"/> The bridge is the cumulative
> distribution function: one object defined for every random variable, with
> three properties it must obey. <bookmark mark="staircases"/> We watch
> discrete variables draw staircases whose jumps are exactly their PMFs,
> <bookmark mark="ramps"/> and meet the new citizens: smoothly climbing
> CDFs, the continuous random variables, plus the hybrids in between.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 8  ·  Continuous Random
  Variables", objective; progress_tag(1, 5) in the DR corner; card rises to
  the top edge.
- `define`: outline line "1.  The CDF and its properties" fades in.
- `staircases`: outline line "2.  Staircases: discrete random variables"
  fades in.
- `ramps`: outline line "3.  Smooth and hybrids: continuous and mixed"
  fades in. (2026-07-04 draft review, 0:30: the word "ramp" is banned from
  on-screen text in this video; narration wording unchanged.)
  (2026-07-04 register pass: narration reworded too — "smooth ramps" is
  now "smoothly climbing CDFs".)

---

## Beat: definition  (scene: CDFDefinition)

> Why does the machinery of the PMF run out? A spinner can stop at any
> angle, uncountably many outcomes, and the third axiom adds probabilities
> over countably many disjoint events only. <bookmark mark="new-object"/>
> We need a new object.
> <bookmark mark="definition"/> Here it is. The cumulative distribution
> function of X at x is the probability that X is less than or equal to x.
> <bookmark mark="event"/> In terms of the sample space, it measures every
> outcome that X sends at or to the left of x. It exists for every random
> variable, discrete or not: that is what makes it a bridge.
> <bookmark mark="limits"/> Its shape is constrained three ways. Toward
> minus infinity the event empties, so the CDF falls to zero; toward plus
> infinity it captures everything, so the CDF climbs to one.
> <bookmark mark="split"/> Now take two points, x one below x two. The
> event that X is at most x two splits into two disjoint pieces: X at most
> x one, and X strictly between x one and x two. Probabilities add, so the
> CDF can never decrease. <bookmark mark="interval"/> Rearrange the same
> equation and you get the workhorse of the whole chapter: the probability
> that X lands in the interval from x one to x two is a difference of two
> heights, F at x two minus F at x one.

**Cues** (per-phrase sub-blocks so each element lands as it is named)
- opening block: the third axiom `\Pr(\bigcup_k A_k) = \sum_k \Pr(A_k)`
  centered with caption "countably many only", written BEFORE the narration
  starts and held on screen through the whole axiom sentence.
  (2026-07-04 draft review, 0:54: the card faded too fast; appear earlier,
  stay longer.)
- `new-object`: the axiom card and caption fade out on "We need a new
  object."
- `definition`: `F_X(x) = \Pr(X \leq x)` in accent, docked under the title.
- `event`: a number line with the ray at or left of x shaded; the
  sample-space form `F_X(x) = \Pr(X^{-1}((-\infty, x]))` beneath the
  definition (definition demotes to ink).
- `limits`: the two limits, `F_X \to 0` at minus infinity and `F_X \to 1`
  at plus infinity, side by side; the shaded ray shrinks empty then grows
  to cover the whole line.
- `split`: number line with x one and x two marked; the split
  `\{X \leq x_2\} = \{X \leq x_1\} \cup \{x_1 < X \leq x_2\}` and the
  conclusion "never decreases."
- `interval`: `\Pr(x_1 < X \leq x_2) = F_X(x_2) - F_X(x_1)` in accent.

---

## Beat: discrete  (scene: DiscreteCDF)

> Now let a discrete random variable meet its CDF. <bookmark mark="sum"/>
> If X takes listed values, its CDF at x just sums the PMF over every value
> at or below x. <bookmark mark="sweep"/> Watch the accumulation happen for
> an old friend: the geometric, with parameter p equal to one half. Sweep
> from left to right across its bars. Between values nothing accrues, so
> the running total stays flat; each time the sweep crosses a bar, the
> total hops up by that bar's mass. The result is a staircase climbing
> toward one. <bookmark mark="jump"/> Look at one step: its jump height is
> exactly the mass sitting at that value.
> <bookmark mark="recover"/> So the PMF can be recovered from the CDF, as
> the value at x minus the limit from the left. Two descriptions, one
> random variable. <bookmark mark="geometric"/> Let us work the geometric
> in both directions. Its masses are one minus p to the k minus one, times
> p. Summing the first floor of x of them telescopes into a clean closed
> form: the CDF is one minus, one minus p to the floor of x.
> <bookmark mark="difference"/> And differencing hands the masses back: the
> CDF at k minus the CDF at k minus one collapses to one minus p to the k
> minus one, times p. The PMF, exactly.

**Cues**
- `sum`: `F_X(x) = \sum_{u \leq x} p_X(u)` docked under the title.
- `sweep`: the geometric PMF bars (p = 1/2) on one set of axes scaled to
  probability one; a vertical accent sweep line moves left to right while
  the staircase CDF draws segment by segment over the same axes. The
  vertical connectors (risers) of the step function are DASHED, the same
  dashed treatment as the MixedRVs jump connectors; the flat treads stay
  solid. The dashed level at height one stops AT the y-axis.
  (2026-07-04 draft review, 2:42: dashed risers; uniform y-label fix.)
- `jump`: the riser at k = 2 highlighted in accent; label `p_X(2)` beside
  the jump height (the sweep line has faded).
- `recover`: `p_X(x) = F_X(x) - \lim_{u \uparrow x} F_X(u)` replaces the
  sum formula.
- `geometric`: chart clears; the geometric card
  `p_X(k) = (1-p)^{k-1} p, \; k = 1, 2, \ldots` (index range shown), then
  `F_X(x) = 1 - (1-p)^{\lfloor x \rfloor}` in accent beneath it.
- `difference`: the differencing derivation trimmed to setup and final
  line `(1-p)^{k-1} p`; the final line takes the accent (CDF formula
  demotes).

---

## Beat: continuous  (scene: ContinuousCDF)

> Not every accumulation climbs in jumps. <bookmark mark="ramp"/> Here is a
> CDF that rises in a smooth progression: zero for negative x, then one
> minus e to the minus x. It satisfies everything we asked: it starts at zero, never
> decreases, and climbs to one.
> <bookmark mark="name"/> When the CDF of X is continuous like this, and
> differentiable almost everywhere, we call X a continuous random variable.
> <bookmark mark="no-mass"/> And continuity has a striking consequence:
> with no jumps, no single point carries mass on its own. Probability now
> lives on intervals: mark two points on the axis, and the chance of
> landing between them is the vertical gap between their two heights.
> <bookmark mark="derivative"/> One more glance at our smooth curve: it is
> differentiable, with derivative e to the minus x, for x positive,
> measuring how fast probability accumulates. Hold that thought, because
> that derivative is the star of the next video.

**Cues**
- `ramp`: axes with the curve `F_X(x) = 1 - e^{-x}` for x at least zero
  (flat at zero to its left); the formula beside the curve; a dashed level
  at height one that stops AT the y-axis so it never overlaps the "1.0"
  y-axis label. (2026-07-04 draft review, 4:18.) (2026-07-04 register
  pass: narration "rises as a smooth ramp" is now "rises in a smooth
  progression".)
- `name`: caption "continuous CDF, differentiable almost everywhere" and
  the accent label "continuous random variable."
- `no-mass`: two dashed verticals at x one and x two on the ramp; the
  vertical gap between the two heights braced and labelled
  `F_X(x_2) - F_X(x_1)`.
- `derivative`: `\frac{dF_X}{dx}(x) = e^{-x}, \; x > 0` in accent, the
  qualifier on screen; caption "how fast probability accumulates."
  (2026-07-04 draft review, 4:52: the derivative statement holds for
  x > 0 only; narration gains ", for x positive".) (2026-07-04 register
  pass: narration "our ramp" is now "our smooth curve".)

---

## Beat: mixed  (scene: MixedRVs)

> One family remains: mixed random variables, whose CDFs climb smoothly
> in places and jump in others, like this one. They have no PMF and they can be discontinuous at
> multiple points, yet the
> CDF still answers every interval question, as differences of heights.
> Next video, we differentiate the continuous CDF and meet the probability
> density function.

**Cues**
- single block: axes with the hybrid CDF drawn left to right: ramp, jump,
  ramp, jump, ramp to one; dashed connectors at the jumps. The chart is
  the only visual; everything fades at the block's end.
  (2026-07-04 draft review, 5:18: narration phrase "and no derivative
  everywhere" replaced with "and they can be discontinuous at multiple
  points"; no on-screen text mirrors the phrase.) (2026-07-04 register
  pass: narration "CDFs ramp and jump" is now "CDFs climb smoothly in
  places and jump in others"; "differentiate the ramp" is now
  "differentiate the continuous CDF".)

---

## Cut list (if over budget)

All three cuts APPLIED 2026-07-03 (draft measured 430.3 s vs 345 s ceiling),
plus line-level tightening in `definition`, `discrete`, and `continuous`.

1. Drop the `mixed` beat to a single sentence over the hybrid picture
   (the subsection is starred in the notes) - saves ~45 s. [applied]
2. Compress the `spinner`/`axiom` opening of `definition` to one sentence
   over the axiom card - saves ~20 s. [applied]
3. Trim the two-line differencing derivation in `discrete` to its final
   line - saves ~10 s. [applied]
