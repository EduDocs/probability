---
slug: 28-uniform-gaussian
title: The Uniform and Gaussian Distributions
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 28-uniform-gaussian.md
derived_from_sha256: d8cfdcc7c6e6e6c6f0d6529f5a93063ad45baac005c2a77ae74a7c3626cd0407
provenance_stamped: 2026-07-06
target_scene_file: scenes/uniform_gaussian.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Meet the two canonical densities - the flat uniform, where probability is a length ratio, and the Gaussian density, where one tabulated curve answers every question."
  recap: "Last video: densities under an integral sign, and expectation as an integral too."
  key_idea: "The uniform makes probability a length ratio; the Gaussian routes every question through one curve, Phi."
  bridge: "Next: the exponential distribution - the geometric gone continuous."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~950 words -> ~295 s.
target_runtime_sec: 320
tolerance_sec: 45

estimated_runtime_sec: 366
measured_runtime_sec: 322.3

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 100
    est_sec: 38
    measured_sec: 39.8
    sync_points: [uniform, gaussian, channel]
  - id: uniform
    scene_class: UniformDistribution
    narration_words: 204
    est_sec: 78
    measured_sec: 66.6
    sync_points: [definition, three-pdfs, cdf-ramp, length-ratio, bus-setup, shade, answer]
  - id: gaussian
    scene_class: GaussianDistribution
    narration_words: 233
    est_sec: 90
    measured_sec: 80.1
    sync_points: [bell, slide-m, widen-sigma, standard, no-closed-form, standardize, one-curve, renamings]
  - id: channel
    scene_class: NoisyChannel
    narration_words: 207
    est_sec: 80
    measured_sec: 66.8
    sync_points: [setup, decide, two-ways, tail, mirror, total, answer]
  - id: integral
    scene_class: GaussianIntegral
    narration_words: 198
    est_sec: 76
    measured_sec: 69.1
    sync_points: [question, square, polar, radial, collapse, area-one, moments, outro]
---

# Video Script — The Uniform and Gaussian Distributions

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video built the machinery of the continuous world: densities that we
> integrate for probability, and expectations that are integrals too. Now we
> start the catalog of distributions worth knowing by name.
> <bookmark mark="uniform"/> First, the flattest density of all, the uniform:
> equal lengths, equal probabilities, and a wait for the bus computed
> honestly. <bookmark mark="gaussian"/> Then the most important one, the
> Gaussian density, and the standardization trick that routes every question
> through a single tabulated curve. <bookmark mark="channel"/> Finally, two
> payoffs: a noisy channel whose error rate is a tail probability, and the
> classic polar trick that proves the Gaussian is a density at all.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 8  ·  Continuous Random
  Variables", objective; card rises to the top edge; `progress_tag(3, 5)`
  in the DR corner.
- `uniform`: outline line "1. The uniform distribution" fades in.
- `gaussian`: outline line "2. The Gaussian and standardization" fades in.
- `channel`: outline line "3. A noisy channel, and why the area is one"
  fades in.

---

## Beat: uniform  (scene: UniformDistribution)

> The uniform random variable is the fair spinner of the continuum: within
> its support, intervals of the same length are equally probable.
> <bookmark mark="definition"/> Its density is a flat shelf. Two parameters,
> a and b, mark the edges of the support, and the height is one over b minus
> a, whatever makes the total area equal one. <bookmark mark="three-pdfs"/>
> Watch the trade-off. On an interval of length one, the shelf has height
> one. Stretch the support to length two, and the shelf drops to one half.
> Stretch it to four, and it drops to one quarter. Wider means shorter, with
> the area pinned at one. <bookmark mark="cdf-ramp"/> The CDF is just as
> plain: zero before a, one after b, and in between a straight line climbing
> at a constant rate. <bookmark mark="length-ratio"/> For a uniform variable,
> then, probability is a length ratio: the length of the piece you care
> about, over the length of the whole support. <bookmark mark="bus-setup"/>
> Try it. A bus comes every thirty minutes, and David arrives at the stop at
> a uniformly random time, so his wait is uniform on zero to thirty minutes.
> <bookmark mark="shade"/> The chance he waits less than five minutes is the
> integral of one thirtieth over the first five minutes,
> <bookmark mark="answer"/> five parts out of thirty: one sixth.

**Cues** (per-phrase sub-blocks so each animation lands on its sentence)
- `definition`: `f_X(x) = 1/(b-a)` on `[a, b]` in accent, with the flat-shelf
  PDF drawn on axes.
- `three-pdfs`: three uniform PDFs in sequence on one set of axes — supports
  `[0,1]`, `[0,2]`, `[0,4]`; each replaces the last (taller means narrower,
  "area = 1" caption pinned at BODY size — larger per review
  (2026-07-04 draft review, 1:20)).
- `cdf-ramp`: the chart swaps to the ramp CDF (0, then linear, then 1).
  (2026-07-04 register pass: narration "a straight ramp climbing" is now
  "a straight line climbing".)
- `length-ratio`: caption "probability = length of piece / length of support"
  (muted, beneath the chart; the chart rides higher so a clear gap sits
  above this line (2026-07-04 draft review, 1:40)).
- `bus-setup`: the chart clears; a 30-minute strip (0 to 30) appears with
  `f_T(t) = 1/30` above it.
- `shade`: the first 5 minutes of the strip shade in accent;
  `Pr(T < 5) = \int_0^5 dt/30` written.
- `answer`: `= 5/30 = 1/6` lands in accent.

---

## Beat: gaussian  (scene: GaussianDistribution)

> From the flattest density to the most famous one. <bookmark mark="bell"/>
> The Gaussian, or normal, random variable is the default model for
> quantities shaped by many small independent effects, like thermal noise or
> measurement error. Its density is the bell curve: e to the minus x minus m
> squared over two sigma squared, scaled by one over root two pi sigma.
> <bookmark mark="slide-m"/> The two parameters are motions, not mysteries.
> Slide m, and the whole density slides with it: m is the center.
> <bookmark mark="widen-sigma"/> Increase sigma, and the density widens and
> flattens, area again pinned at one: sigma sets the spread.
> <bookmark mark="standard"/> The special case m equals zero, sigma equals
> one, is called the standard normal. Remember it, because it is about to do
> all the work. <bookmark mark="no-closed-form"/> Here is the catch: the CDF
> of a Gaussian is an integral with no closed form. No amount of calculus
> produces an antiderivative for the density. <bookmark mark="standardize"/>
> The rescue is a change of variables. Substitute v equals u minus m over
> sigma, and every Gaussian CDF collapses to F of x equals Phi of x minus m
> over sigma, <bookmark mark="one-curve"/> where Phi is the CDF of the
> standard normal: one tabulated curve, computed once, serving every m and
> every sigma there is. <bookmark mark="renamings"/> The same information
> wears other names. Statisticians use the error function, erf, and
> engineers use the tail, Q of x, which is simply one minus Phi of x:
> different fields, same curve.

**Cues** (one bell morphing — parameters as motions, not three stills)
- `bell`: axes with the standard bell drawn; the density formula
  `f_X(x) = (1/\sqrt{2\pi}\sigma) e^{-(x-m)^2/2\sigma^2}` in accent above.
- `slide-m`: the bell slides right (m: 0 to 1.5); caption "m centers it".
- `widen-sigma`: the bell widens and flattens (sigma: 1 to 2); caption
  "sigma sets the spread".
- `standard`: bell returns to m = 0, sigma = 1; label "standard normal"
  in accent.
- `no-closed-form`: the CDF integral written, then struck with "no closed
  form" (muted caption).
- `standardize`: `F_X(x) = \Phi((x - m)/\sigma)` in accent — the shaded area
  under an (m, sigma) bell slides and rescales onto the standard bell,
  same area.
- `one-curve`: caption "one curve serves all m, sigma".
- `renamings`: one line, muted: `Q(x) = 1 - \Phi(x)`, `\mathrm{erf}` named
  beside it — one breath, no derivation.

---

## Beat: channel  (scene: NoisyChannel)

> Let the tail earn its keep. <bookmark mark="setup"/> A binary message
> crosses a noisy wire. The input X is plus one or minus one with equal
> probability, and the output is Y equals X plus Z, where Z is Gaussian
> noise with mean zero and spread sigma. <bookmark mark="decide"/> The
> receiver does the natural thing: it decides by the sign of Y. Positive
> means a plus one was sent; negative means a minus one.
> <bookmark mark="two-ways"/> When does it fail? In two ways: a plus one was
> sent and the noise dragged Y below zero, or a minus one was sent and the
> noise pushed Y above zero. <bookmark mark="tail"/> Picture the two densities,
> one centered at plus one, one at minus one, with the threshold at zero.
> Given a plus one, an error means the noise beats the signal: Z below minus
> one, and by symmetry of the density that is the tail probability Q of one
> over sigma. <bookmark mark="mirror"/> The other error is its mirror image,
> the same tail reflected across the threshold. <bookmark mark="total"/> The
> total probability theorem averages the two conditional errors, a half of
> each, <bookmark mark="answer"/> and symmetry makes the average trivial:
> the probability of error is exactly Q of one over sigma. Noise level in,
> error rate out: reliability read off a tail.

**Cues**
- `setup`: `X \in \{-1, +1\}` equiprobable, `Y = X + Z`,
  `Z \sim` Gaussian(0, sigma^2) — the model card, top of frame.
- `decide`: axes with the threshold at 0 marked; "decide by sign" caption.
- `two-ways`: the two error clauses listed as two short lines.
- `tail`: two bells centered at -1 and +1 with the threshold at 0; the right
  bell's left tail (beyond 0) shades in accent;
  `\Pr(Y \le 0 \mid X = +1) = Q(1/\sigma)` written.
- `mirror`: the mirrored tail of the left bell shades; the symmetry equality
  written beneath.
- `total`: `\Pr(\text{error}) = \tfrac12 Q(1/\sigma) + \tfrac12 Q(1/\sigma)`.
- `answer`: `\Pr(\text{error}) = Q(1/\sigma)` lands in accent.

---

## Beat: integral  (scene: GaussianIntegral)

> One debt remains: is the Gaussian even a density? Its area must be one,
> yet the function refuses to be integrated directly.
> <bookmark mark="question"/> The classic trick is easy to follow and hard
> to discover. Call the integral I, and study I squared instead.
> <bookmark mark="square"/> Squaring turns one integral into two, and two
> integrals into a double integral over the whole plane, of e to the minus u
> squared plus v squared over two. <bookmark mark="polar"/> Now look at that
> surface from above. Its level sets are perfect circles, begging for polar
> coordinates. <bookmark mark="radial"/> The angle contributes a factor of
> two pi, and the radial integrand becomes r times e to the minus r squared
> over two: that extra r is exactly the derivative the exponential was
> missing. <bookmark mark="collapse"/> The radial integral evaluates in one
> line, and I squared equals one. <bookmark mark="area-one"/> Since I is
> nonnegative, the area under the curve is exactly one.
> <bookmark mark="moments"/> The same normalization identity, exploited once
> more, delivers the moments: the mean is m and the variance is sigma
> squared, so the parameters mean what we said they mean.
> <bookmark mark="outro"/> The key idea of this video: the uniform makes
> probability a length ratio, and the Gaussian routes every question through
> one curve, Phi.

**Cues** (section title reads "Why the Bell Curve Integrates to One"
(2026-07-04 draft review, 5:40); the `I^2` continuation lines are built as
`("=", rhs)` and hang beneath the first `I^2` equation with their equals
signs aligned, so the derivation reads as one chain
(2026-07-04 draft review, 6:20))
- `question`: `I = \int f_X(u)\, du` with "area = 1?" in accent.
- `square`: `I^2` expanded to the double integral.
- `polar`: top view of circular level sets — a few concentric circles
  (muted) with the radial arrow, landing on the "perfect circles" sentence
  (re-split so each element lands on its phrase
  (2026-07-04 draft review, 5:50)).
- `radial`: the polar rewrite
  `\int_0^{2\pi} \tfrac{1}{2\pi} d\theta \int_0^\infty r e^{-r^2/2}\, dr`
  lands on the "angle contributes a factor of two pi" sentence
  (2026-07-04 draft review, 5:50).
- `collapse`: `= (-e^{-r^2/2})\big|_0^\infty = 1` on "evaluates in one line"
  (2026-07-04 draft review, 5:50).
- `area-one`: `I^2 = 1 \Rightarrow I = 1` in accent as "the area under the
  curve is exactly one" is spoken (2026-07-04 draft review, 5:50).
- `moments`: one muted line: `\mathrm{E}[X] = m`, `\mathrm{Var}(X) = \sigma^2`
  "from the same normalization".
- `outro`: shared outro card — key idea + "Coming up: The Exponential
  Distribution". The next-up card line is visual-only; the spoken "Next
  up..." sentence was dropped (2026-07-04 draft review, 6:48).

---

## Cut list (if over budget)

1. Compress `renamings` to its caption only (drop the spoken erf sentence;
   keep `Q(x) = 1 - \Phi(x)` on screen) — saves ~10 s.
2. Drop the `moments` sentence in `integral` (keep the polar trick) —
   saves ~10 s.
3. Trim the closing clause of `channel` ("Noise level in, error rate out")
   — saves ~5 s.
