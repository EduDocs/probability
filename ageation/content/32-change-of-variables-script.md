---
slug: 32-change-of-variables
title: The Change-of-Variables Formula
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 32-change-of-variables.md
derived_from_sha256: 0296efa1f6b727917a7875ebb875c1fd9b411ba1f66978b93a5395999e15efcf
provenance_stamped: 2026-07-06
target_scene_file: scenes/change_of_variables.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Skip the integral - a differentiable map takes the density of X straight to the density of Y."
  recap: "Last video: the CDF method - chase the event g(X) <= y, integrate, then differentiate."
  key_idea: "A differentiable map turns densities into densities - divide by the slope, and sum over the roots."
  bridge: "Next: aim the formula at the CDF itself and turn it into a recipe for generating random variables."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 320
tolerance_sec: 45

estimated_runtime_sec: 367
measured_runtime_sec: 318.2

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 95
    est_sec: 37
    measured_sec: 33.8
    sync_points: [formula, gaussian, roots]
  - id: slope-rescales
    scene_class: SlopeRescales
    narration_words: 202
    est_sec: 78
    measured_sec: 64.6
    sync_points: [invert, differentiate, strip, shallow, steep, exchange]
  - id: change-of-variables
    scene_class: ChangeOfVariables
    narration_words: 193
    est_sec: 74
    measured_sec: 64.7
    sync_points: [increasing, decreasing, formula, recipe, rayleigh]
  - id: gaussian-affine
    scene_class: GaussianAffine
    narration_words: 168
    est_sec: 65
    measured_sec: 55.5
    sync_points: [setup, invert, apply, still-gaussian, closed]
  - id: sum-over-roots
    scene_class: SumOverRoots
    narration_words: 296
    est_sec: 114
    measured_sec: 99.7
    sync_points: [wavy, roots, sum, cosine, two-roots, contributions, pileup, outro]
---

# Video Script — The Change-of-Variables Formula

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video we derived distributions the long way: chase the event,
> integrate to a CDF, then differentiate. This video adds a single
> assumption, differentiability, and the integral disappears entirely.
> <bookmark mark="formula"/> First we build the change-of-variables formula,
> which takes the density of X straight to the density of Y, and see why the
> slope of g is the exchange rate between the two axes.
> <bookmark mark="gaussian"/> Then we let it work: an affine map of a
> Gaussian stays Gaussian, <bookmark mark="roots"/> and when g folds the
> axis onto itself, every root of g of x equals y pays its own share.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 9 · Functions and Derived
  Distributions", objective; card rises to the top edge; progress tag 2 / 3
  in the DR corner.
- `formula`: outline line "1. The formula: density in, density out" fades in.
- `gaussian`: outline line "2. An affine Gaussian stays Gaussian" fades in.
- `roots`: outline line "3. Non-monotone maps: sum over the roots" fades in.

---

## Beat: slope-rescales  (scene: SlopeRescales)

> Start where last video left off, with one new assumption: g is
> differentiable and strictly increasing. <bookmark mark="invert"/> That
> buys invertibility. Every y now comes from exactly one x, so x equals g
> inverse of y is a genuine function, and last video's formula loses its
> sup: the CDF of Y at y is simply the CDF of X at g inverse of y.
> <bookmark mark="differentiate"/> Now differentiate both sides with
> respect to y. The chain rule hands us the density of Y: the density of X
> at g inverse of y, times the derivative of the inverse, the rate dx by
> dy. <bookmark mark="strip"/> That derivative is not a technicality; it is
> the whole story. Take a thin strip of width delta on the y axis and pull
> it back through the curve. <bookmark mark="shallow"/> Where the slope is
> shallow, the strip pulls back to a wide interval of x values, so plenty
> of probability funnels into that band of y. <bookmark mark="steep"/>
> Where the slope is steep, the same strip pulls back to a narrow interval,
> and hardly any probability lands there. <bookmark mark="exchange"/> The
> derivative is the exchange rate between the two axes. Probability is
> conserved, so the density must be rescaled by exactly how much the map
> stretches the axis.

**Cues** (two-column: the monotone-curve chart left, the derivation right)
- opening block: section title docks up; the assumption caption
  "g differentiable, strictly increasing" appears muted, at body size
  (raised from caption size; no number reference in the narration —
  "last video", not "video thirty-one") (2026-07-04 draft review, 0:48).
- `invert`: `F_Y(y) = F_X(g^{-1}(y))` written on the right, its left side
  briefly in accent.
- `differentiate`: the chain-rule line
  `f_Y(y) = f_X(g^{-1}(y)) \frac{dx}{dy}` written beneath it; the
  `\frac{dx}{dy}` factor is the accent.
- `strip`: the monotone cubic curve (the notes' figure) grows in on the
  left, riding slightly higher off the bottom edge (2026-07-04 draft
  review, 1:56); a thin delta-strip appears on the y axis.
- `shallow`: the strip sits on the shallow stretch; its pullback interval
  on the x axis is wide (both intervals in accent-ish red per the notes;
  here the strip pair carries the accent).
- `steep`: the strip slides up to the steep stretch; the pullback pinches
  narrow.
- `exchange`: caption under the chart, "the slope is the exchange rate
  between the axes" (muted), centered on the chart (2026-07-04 draft
  review, 1:56); the `\frac{dx}{dy}` factor indicated once.

---

## Beat: change-of-variables  (scene: ChangeOfVariables)

> Substitute x for g inverse of y and the result reads cleanly.
> <bookmark mark="increasing"/> For a strictly increasing g, the density of
> Y is the density of X divided by the slope of g at x, and the slope is
> positive, so the density stays positive. <bookmark mark="decreasing"/>
> What if g is strictly decreasing? Then g of X at most y means X at least
> g inverse of y, so the CDF picks up a one minus, and differentiating
> produces a minus sign, exactly cancelling the sign of the now negative
> slope. <bookmark mark="formula"/> One absolute value absorbs both cases.
> When g is differentiable and strictly monotone, the density of Y at y is
> the density of X at x, divided by the absolute value of the derivative of
> g, with x equal to g inverse of y. This is the change-of-variables
> formula, the workhorse of derived distributions.
> <bookmark mark="recipe"/> The recipe now has just three moves: invert,
> differentiate, and divide. <bookmark mark="rayleigh"/> It even collapses last
> video's channel fading example. The Rayleigh amplitude squared took an
> integral there; here it takes one line, and the algebra folds down to one
> half e to the minus y over two. Same exponential, no integral.

**Cues**
- opening block: section title; `x = g^{-1}(y)` substitution card, muted,
  at body size — the same size as the equation stack it heads — and the
  stack rebalanced beneath it (2026-07-04 draft review, 2:20).
- `increasing`: `f_Y(y) = f_X(x) / \frac{dg}{dx}(x)` with the caption
  "increasing: slope positive" (muted).
- `decreasing`: the decreasing case beneath, muted:
  `F_Y(y) = 1 - F_X(g^{-1}(y))` then `f_Y(y) = f_X(x) / (-\frac{dg}{dx}(x))`.
- `formula`: the combined boxed formula lands in accent:
  `f_Y(y) = f_X(g^{-1}(y)) |dx/dy| = f_X(x) / |\frac{dg}{dx}(x)|`, with
  `x = g^{-1}(y)`; the two cases above demote to muted.
- `recipe`: caption "invert, differentiate, divide" (muted).
- `rayleigh`: the recipe caption fades out as the Rayleigh line arrives —
  it was overlapping the fraction (2026-07-04 draft review, 3:24). One
  line under the box, small:
  `f_Y(y) = f_X(\sqrt{y}) / |\frac{dg}{dx}(\sqrt{y})| = \tfrac{1}{2} e^{-y/2}`
  with caption "last video's Rayleigh energy: one line, same exponential"
  (concept reference, no video number; 2026-07-04 draft review, 3:24).

---

## Beat: gaussian-affine  (scene: GaussianAffine)

> Time to let the formula work. <bookmark mark="setup"/> Let X be a
> standard Gaussian, the bell curve with density e to the minus x squared
> over two, divided by the square root of two pi. Let Y equal a X plus b,
> an amplification and an offset, with a nonzero. <bookmark mark="invert"/>
> The map is affine, so inverting it is arithmetic: x equals y minus b,
> over a, and dx by dy is one over a. <bookmark mark="apply"/> Feed both
> into the formula. The density of Y is the standard density evaluated at y
> minus b over a, divided by the absolute value of a.
> <bookmark mark="still-gaussian"/> Simplify, and look at what came out: a
> Gaussian with mean b and standard deviation the absolute value of a.
> <bookmark mark="closed"/> The density shifts by b and stretches by a, but
> the silhouette never changes. Only the labels move. The same progression
> works for any Gaussian
> input: an affine function of a Gaussian random variable remains Gaussian.
> Amplify a noisy channel, add an offset, and the noise keeps its
> distribution.

**Cues**
- opening block: section title docks up.
- `setup`: `f_X(x) = e^{-x^2/2} / \sqrt{2\pi}` and `Y = aX + b, a \neq 0`
  written; the standard bell grows on the axes below.
- `invert`: `g^{-1}(y) = (y-b)/a`, `dx/dy = 1/a` (small line).
- `apply`: `f_Y(y) = f_X((y-b)/a) \cdot 1/|a|` written.
- `still-gaussian`: the simplified
  `f_Y(y) = e^{-(y-b)^2/(2a^2)} / (\sqrt{2\pi}\,|a|)` lands in accent.
- `closed`: the curve slides right by b and stretches by a (a = 1.5, b = 2
  for the picture) while the parameter label updates; caption "still
  Gaussian: mean b, standard deviation |a|" (muted) — no bare "bell",
  spoken or on screen (2026-07-04 draft review, 4:20).

---

## Beat: sum-over-roots  (scene: SumOverRoots)

> Monotone maps are the friendly case. <bookmark mark="wavy"/> A real g
> can wander: rise, fall, rise again. As long as it is differentiable with
> finitely many local extrema, it is monotone piece by piece.
> <bookmark mark="roots"/> So pick a level y and collect every x where g of
> x equals y. Each root sits on its own monotone piece, and each piece
> obeys the formula we just built. <bookmark mark="sum"/> Add the
> contributions: the density of Y at y is the sum, over all roots, of the
> density of X at that root divided by the absolute value of the slope
> there. The discrete world summed masses over the same preimage; densities
> do the same, with the stretch factor that masses never needed.
> <bookmark mark="cosine"/> Watch it in action. Sample a sinusoid at a
> random phase: X is uniform between zero and two pi, and Y equals the
> cosine of X. <bookmark mark="two-roots"/> For y strictly between minus
> one and one, the level line cuts the cosine twice: once at arc cosine of
> y, and once at two pi minus arc cosine of y.
> <bookmark mark="contributions"/> The derivative of cosine is minus sine,
> and at both roots its magnitude is the square root of one minus y
> squared. Each root contributes one over two pi times that root; together
> they give one over pi square root of one minus y squared.
> <bookmark mark="pileup"/> Plot it and the shape is striking: a U. The
> density piles up near plus and minus one, because the cosine lingers near
> its peaks. Shallow slope, wide pullback, heaped probability: the exchange
> rate at work. <bookmark mark="outro"/> The key idea of this video: a
> differentiable map turns densities into densities. Divide by the slope,
> and sum over the roots. Next we aim this machinery at the CDF itself and
> turn it into a recipe for generating random variables.

**Cues**
- opening block: section title.
- `wavy`: the notes' wavy g grows in on the left.
- `roots`: a horizontal level line at y cuts the curve three times; a dot
  at each intersection, dashed drops to the x axis.
- `sum`: the sum-over-roots formula lands in accent on the right:
  `f_Y(y) = \sum_{\{x \mid g(x) = y\}} f_X(x) / |\frac{dg}{dx}(x)|`.
- `cosine`: the wavy chart clears; the cosine on `[0, 2\pi]` grows in with
  uniform phase dots along the x axis; formula demotes to muted.
- `two-roots`: level line at y, two root dots, `\arccos(y)` and
  `2\pi - \arccos(y)` marked.
- `contributions`: `f_Y(y) = 1 / (\pi \sqrt{1 - y^2})` builds on the right,
  landing in accent.
- `pileup`: the cosine chart clears; the U-shaped arcsine density plots on
  `(-1, 1)` (range clipped inside the singular endpoints), dashed walls at
  plus and minus one; the chart rides slightly higher for balance with the
  right column (2026-07-04 draft review, 6:25).
- `outro`: shared outro card — key idea + "Coming up: Generating Random
  Variables".

---

## Cut list (if over budget)

1. Drop the Rayleigh one-line redo in `change-of-variables` (the optional
   ledger entry; saves ~40 words / ~15 s).
2. Compress the `decreasing` derivation to "the minus sign the absolute
   value absorbs," shown over the combined formula only (~30 words).
3. Trim the closing sentence of `gaussian-affine` ("Amplify a noisy
   channel...").
