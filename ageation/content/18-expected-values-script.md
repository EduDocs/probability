---
slug: 18-expected-values
title: Expected Values
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the 480p draft for finals 2026-07-03
derived_from: 18-expected-values.md
derived_from_sha256: 6820ac8b007110ae10ef691f1198927019481fdc38c3265f85cba1324e910fbf
provenance_stamped: 2026-07-06
target_scene_file: scenes/expected_values.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Collapse a whole PMF into one meaningful number: the expected value."
  recap: "Last video: functions of random variables -- Y = g(X) is itself a random variable."
  key_idea: "The expected value E[X] is the probability-weighted sum of the values of X -- a one-number summary of its PMF."
  bridge: "Next: expectations of functions -- the mean and the variance."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Timing contract set from the published final (2026-07-03): the 1080p nova
# render measured 210.8 s. Empirical series calibration: nova at 1.0 runs
# ~0.80x the gTTS draft duration (draft 262.7 s -> final 210.8 s), i.e. nova
# is FASTER than gTTS, not slower.
target_runtime_sec: 210
tolerance_sec: 45

estimated_runtime_sec: 300
measured_runtime_sec: 210.0

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 105
    est_sec: 42
    measured_sec: 35.6
    sync_points: [define, examples, object]
  - id: definition
    scene_class: ExpectedValueDefinition
    narration_words: 175
    est_sec: 70
    measured_sec: 58.5
    sync_points: [full-pmf, weighted-sum, converge, of-the-pmf]
  - id: die
    scene_class: FairDieExample
    narration_words: 130
    est_sec: 52
    measured_sec: 31.7
    sync_points: [flat-pmf, compute, between]
  - id: heads
    scene_class: WaitingForHeads
    narration_words: 150
    est_sec: 60
    measured_sec: 43.1
    sync_points: [halving-pmf, series, partial-sums]
  - id: summary
    scene_class: PMFToScalar
    narration_words: 135
    est_sec: 54
    measured_sec: 41.1
    sync_points: [pmf-in, scalar-out, trade, outro]
---

# Video Script — Expected Values

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> We now know that applying a function to a random variable gives another
> random variable, with its own PMF. So by now, a PMF is something we can build
> and transform. But a PMF is a lot of information — a whole table of values and
> probabilities. Very often, all we really want is one number: an average. This
> chapter is about the operator that produces such numbers — expectation.
> <bookmark mark="define"/> In this video we define the expected value of a
> discrete random variable, <bookmark mark="examples"/> compute it for a die
> roll and for a coin tossed until heads, <bookmark mark="object"/> and see
> what kind of object it really is.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 6 · Meeting Expectations",
  recap line, objective; card rises to the top edge.
- `define`: outline line "1. The definition" fades in.
- `examples`: outline line "2. Two worked examples" fades in.
- `object`: outline line "3. What E[X] really is" fades in.

---

## Beat: definition  (scene: ExpectedValueDefinition)

> Here is a PMF. <bookmark mark="full-pmf"/> It answers every question about
> its random variable: the probability of each value, of any set of values.
> Complete — but detailed. Suppose we want a single number that summarizes
> where this distribution sits. <bookmark mark="weighted-sum"/> The natural
> candidate is a weighted average: take each value x, weight it by its mass
> p sub X of x, and add everything up. That sum is the expected value of X,
> written E of X, and it is also called the mean. Each value contributes in
> proportion to how likely it is. <bookmark mark="converge"/> One caveat: for
> ranges with infinitely many values, the sum must converge absolutely;
> otherwise we simply say the expected value does not exist.
> <bookmark mark="of-the-pmf"/> And notice what kind of object this is. The
> expected value is not a function of the outcomes; it is computed from the
> PMF alone. Two random variables with the same PMF have exactly the same
> mean, no matter how different their experiments are.

**Cues**
- `full-pmf`: a PMF bar chart (reuse the house chart) at center.
- `weighted-sum`: `\mathrm{E}[X] = \sum_{x \in X(\Omega)} x \, p_X(x)` in
  accent; each bar briefly lights as its term `x \cdot p_X(x)` appears.
- `converge`: caption lane note, one line: "defined when the sum converges
  absolutely."
- `of-the-pmf`: the formula's inputs highlighted — only `p_X` appears.

---

## Beat: die  (scene: FairDieExample)

> Let's compute one. Roll a fair die once, and let X be the number of dots on
> the top face. <bookmark mark="flat-pmf"/> The PMF is flat: each of the six
> values carries mass one sixth. <bookmark mark="compute"/> So the expected
> value is one times one sixth, plus two times one sixth, and so on up to six —
> that is twenty-one over six, which is three and a half.
> <bookmark mark="between"/> Three and a half. Notice the die can never show
> that value. The mean is a balance point of the distribution, not necessarily
> a value the random variable can take.

**Cues**
- `flat-pmf`: six equal bars at 1..6 (house chart), a small die face beside
  the title (reuse `die_face`).
- `compute`: the sum builds term by term, collapses to `21/6 = 3.5`.
- `between`: a marker drops onto 3.5 on the axis, visibly between the bars;
  one caption line beneath.

---

## Beat: heads  (scene: WaitingForHeads)

> Now an infinite one. Toss a fair coin until the first head appears, and let
> X count the tosses. <bookmark mark="halving-pmf"/> We met this random
> variable before: its range is one, two, three, and on forever, and its PMF
> halves at every step — the probability of needing k tosses is one over two
> to the k. <bookmark mark="series"/> The expected value is the sum of k over
> two to the k, for k from one to infinity. Infinitely many terms — yet the
> series converges, and it converges to exactly two.
> <bookmark mark="partial-sums"/> Watch the partial sums: one half, then one
> and a half... creeping up and settling at two. On average, it takes two
> tosses to see the first head. An infinite amount of detail, condensed into
> one clean number.

**Cues**
- `halving-pmf`: the geometric PMF's halving bars (reuse the video-16 look),
  a coin glyph beside the title (reuse `coin`).
- `series`: `\mathrm{E}[X] = \sum_{k=1}^{\infty} k \, 2^{-k} = 2` in accent.
- `partial-sums`: a marker slides along the axis through the partial sums
  and settles on 2.

---

## Beat: summary  (scene: PMFToScalar)

> Step back and look at what expectation does. <bookmark mark="pmf-in"/> In
> goes a PMF — a complete, detailed description of a random variable.
> <bookmark mark="scalar-out"/> Out comes a single scalar: its mean.
> <bookmark mark="trade"/> That is the trade: we give up detail and gain a
> concise, meaningful summary of overall behavior. And this trade is the
> template for everything in this chapter. <bookmark mark="outro"/> The
> key idea to carry forward: the expected value is the probability-weighted
> sum of the values — one number that summarizes the whole PMF. Coming up
> next: we push functions through the expectation and meet the two summaries
> that dominate practice, the mean and the variance.

**Cues** (the pour is deliberately held back to `scalar-out`, ~15 s into the
beat, per the 2026-07-03 draft review)
- opening block: the PMF chart fades in above the (not yet drawn) funnel.
- `pmf-in`: the funnel is drawn beneath the chart.
- `scalar-out`: the chart pours into the funnel; `\mathrm{E}[X]` emerges
  below as a single glowing scalar.
- `trade`: hold the picture; no new elements.
- `outro`: shared outro card — key idea + "Coming up: Functions and
  Expectations".

---

## Cut list (if over budget)

1. Drop the `between` remark in `die` to one spoken sentence (no marker
   animation).
2. Compress `partial-sums` in `heads` to the settled marker only.
3. Fold the `converge` caveat into a caption with no narration pause.
