---
slug: 40-continuous-sums
title: Sums of Continuous Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 40-continuous-sums.md
derived_from_sha256: 9f030c074161a49b3d2547384cbccf8b951c03618a424f9950d4536c26f498d4
provenance_stamped: 2026-07-06
target_scene_file: scenes/continuous_sums.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Find the density of a sum of independent variables: convolve the densities, or let the MGF turn sums into products."
  recap: "Last video: independence factors the joint density into the product of its marginals."
  key_idea: "For independent variables, densities convolve, and transforms multiply."
  bridge: "Coming up: Types of Convergence -- the final chapter opens with sums of many variables."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 310
tolerance_sec: 45

estimated_runtime_sec: 373
measured_runtime_sec: 337.3

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 92
    est_sec: 35
    measured_sec: 34.9
    sync_points: [convolve, examples, shortcut]
  - id: convolution-def
    scene_class: ConvolutionDefinition
    narration_words: 254
    est_sec: 98
    measured_sec: 82.8
    sync_points: [claim, star, cdf, factor, differentiate]
  - id: uniform-sum
    scene_class: UniformSum
    narration_words: 187
    est_sec: 72
    measured_sec: 66.2
    sync_points: [flip, grow, shrink, triangle, dice]
  - id: exp-gauss-sums
    scene_class: ExponentialGaussianSums
    narration_words: 230
    est_sec: 88
    # ledger entries exponential-sum + gaussian-sum share this beat
    measured_sec: 82.7
    sync_points: [product, erlang, gauss, stable]
  - id: mgf-product
    scene_class: MGFProduct
    narration_words: 202
    est_sec: 80
    measured_sec: 70.8
    sync_points: [title, rule, redo, add, outro]
---

# Video Script — Sums of Continuous Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

This video (4 of 4) closes book chapter 11. The concept ledger's convolution-def
and cdf-proof entries share the ConvolutionDefinition beat; exponential-sum and
gaussian-sum share the ExponentialGaussianSums beat.

---

## Beat: overview  (scene: ChapterOverview)

> This chapter closes with the question the whole course keeps returning to:
> add two independent continuous random variables, and what is the density of
> the sum? <bookmark mark="convolve"/> In this video the discrete convolution
> of chapter seven ripens into an integral: for independent variables, the
> density of a sum is the convolution of the densities.
> <bookmark mark="examples"/> We run that integral three times — two uniforms
> fold into a triangle, two exponentials into an Erlang, two Gaussians into
> another Gaussian — <bookmark mark="shortcut"/> and then we skip the integral
> entirely: under the moment generating function, sums become products.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 11 · Multiple Continuous
  Random Variables", title, objective; card rises to the top edge;
  progress_tag(4, 4) in the DR corner.
- `convolve`: outline line "1. The convolution of densities" fades in.
- `examples`: outline line "2. Three sums, worked" fades in.
- `shortcut`: outline line "3. Sums become products" fades in.

---

## Beat: convolution-def  (scene: ConvolutionDefinition)

> Last video left us with a factored joint: for independent X and Y, the
> joint density is the product of the marginals. Here is what that purchase
> buys. Form the sum, W equals X plus Y — a new random variable. What is its
> density? <bookmark mark="claim"/> The claim: the density of W is the
> convolution of the two marginal densities. For each target value w,
> integrate f X of u, times f Y of w minus u, over every u — every way of
> splitting w into two pieces gets weighed, and the roles of X and Y can be
> swapped without changing the answer. <bookmark mark="star"/> When we
> convolved PMFs, we did exactly this with masses: the PMF of a sum collected
> p X of m times p Y of k minus m over all m. Replace masses by densities and the
> sum by an integral, and it is the same sliding machine, gone continuous.
> <bookmark mark="cdf"/> To prove it, go through the CDF. The probability
> that W is at most w is the probability that the pair X, Y lands in the half
> plane below the line u plus v equals w. <bookmark mark="factor"/>
> Independence factors the joint density, so the inner integral runs the
> density of Y up to w minus u — and that is a value of the CDF of Y.
> <bookmark mark="differentiate"/> Now differentiate with respect to w,
> sliding the derivative under the integral. Each CDF of Y becomes a density
> of Y, and what remains is exactly the convolution. Claim proved — the
> fundamental theorem of calculus, used judiciously.

**Cues** (per-phrase sub-blocks so each element lands on its sentence)
- opening: `f_{X,Y}(x, y) = f_X(x)\, f_Y(y)` recalled (muted), then
  `W = X + Y` beneath it.
- `claim`: `f_W(w) = (f_X \ast f_Y)(w) = \int_{-\infty}^{\infty}
  f_X(u)\, f_Y(w - u)\, du` in accent; caption "symmetric in the two
  factors."
- `star`: video 25's discrete card
  `p_{X+Y}(k) = \sum_m p_X(m)\, p_Y(k - m)` (muted) beside the integral;
  the sum-to-integral correspondence indicated. (2026-07-04 register pass:
  narration "Video twenty-five did exactly this" is now "When we convolved
  PMFs, we did exactly this" — topic anchor, not a number.)
- `cdf`: left column: the (u, v) plane with the line u + v = w and the
  half-plane below it shaded; right column:
  `F_W(w) = \Pr\left(X + Y \leq w\right)` and the double integral.
- `factor`: the joint factors; inner integral becomes `F_Y(w - u)`, giving
  `F_W(w) = \int F_Y(w - u)\, f_X(u)\, du`.
- `differentiate`: derivative slides under the integral;
  `f_W(w) = \int f_Y(w - u)\, f_X(u)\, du` lands in accent.

---

## Beat: uniform-sum  (scene: UniformSum)

> Now run the integral once — and watch it happen. Draw two numbers
> independently from the unit interval, each uniform: two flat rectangles of
> height one. What is the density of their sum? <bookmark mark="flip"/>
> Convolution has a picture: mirror one rectangle, then slide it across the
> other. At each position w, the density of the sum is the area where the two
> windows overlap. <bookmark mark="grow"/> For w between zero and one, the
> windows overlap on an interval of length exactly w. The overlap grows, and
> the density rises linearly: f of w equals w. <bookmark mark="shrink"/>
> Past one, the sliding window begins to leave the other side. The overlap
> shrinks at the same rate it grew, and the density falls: two minus w,
> hitting zero at two. <bookmark mark="triangle"/> Flat plus flat equals
> triangle. Sums near one can be assembled in the most ways; sums near zero
> or two in almost none. <bookmark mark="dice"/> And you have met this shape
> before. The total of two dice climbed bar by bar to seven, then fell away
> symmetrically. That staircase was this triangle, sampled at the integers —
> the discrete twin, resolved into a continuum.

**Cues** (the video's signature visual: flip-and-slide with the traced curve
building point by point — discrete slider positions, no ValueTracker)
- opening: one axes; the fixed rectangle f_X (BLUE fill) on [0, 1].
- `flip`: the mirrored window f_Y(w - u) (TEAL fill) slides in from the
  left; caption "slide the mirror across."
- `grow`: slider stops at w = 0.5, then w = 1: overlap region shaded in
  accent, its width visibly growing; on a second small axes to the right,
  traced dots land at (0.5, 0.5), (1, 1). (2026-07-04 register pass:
  narration "traces a rising ramp" is now "rises linearly" — "ramp" is
  banned; the triangle sentence carries the climb-and-fall image.)
  (2026-07-05 draft review, 2:58: the slide is the key visualization —
  slow it down and smooth it out; long run_times, smooth ease into the
  first stop, linear glide between checkpoints, breathing waits at each
  stop.)
- `shrink`: slider stops at w = 1.5: the overlap window shrinks; traced dot
  at (1.5, 0.5). (Same 2026-07-05 pacing note applies.)
- `triangle`: the full tent function drawn through the dots;
  `f_W(w) = w` on [0,1], `2 - w` on (1,2] in accent beside it; slide stage
  cleared first (one chart at a time). (2026-07-05 draft review, 3:33:
  the edges are grouped only AFTER their Create animations play —
  pre-adding them to the on-screen trace group made both pop in fully and
  then redraw, the right edge twice.)
- `dice`: the triangle result shifts left; a miniature two-dice total bar
  chart (values 2..12, peak at 7) appears at the right for the twin moment;
  caption centered under the pair's midpoint.

---

## Beat: exp-gauss-sums  (scene: ExponentialGaussianSums)

> Two more sums from the notes, each carrying its own lesson. First, add two
> independent exponential waiting times, rate lambda each.
> <bookmark mark="product"/> For w at least zero, the convolution runs u from
> zero to w — and something pleasant happens inside: e to the minus lambda
> times w minus u, times e to the minus lambda u, multiplies to e to the
> minus lambda w. The integration variable cancels; the integrand is flat.
> <bookmark mark="erlang"/> So the integral simply measures the length of the
> interval, and the density is lambda squared, times w, times e to the minus
> lambda w. That is the Erlang distribution with parameter two, straight out
> of the gallery of densities — now derived, and it reads naturally: the sum
> of two exponential waits is the wait for the second arrival.
> <bookmark mark="gauss"/> Second, add two independent standard Gaussians.
> The convolution multiplies two bells; complete the square in the exponent,
> and the integrand splits into e to the minus w squared over four, times a
> Gaussian density centered at w over two. A Gaussian density integrates to
> one — the same trick that tamed the bell curve's integral.
> <bookmark mark="stable"/> What survives is one over the square root of four
> pi, times e to the minus w squared over four: a Gaussian with mean zero and
> variance two. Gaussian plus Gaussian stays Gaussian — in general, the means
> add and the variances add.

**Cues** (two worked sums; one chart on screen at a time; sequential
section titles — "Exponentials" for the first sum, Transformed to
"Gaussians" at the hand-off; 2026-07-05 draft review, 4:10 + 5:02)
- opening: section title "Exponentials"; exponential density curve
  `\lambda e^{-\lambda u}` on an axes (lambda = 1 drawn), `X, Y \sim`
  exponential card above. The density chart rides centered on the halfway
  anchor (`zone_center_y(title)`), not resting low (2026-07-05 draft
  review, 4:10).
- `product`: derivation line
  `f_W(w) = \int_0^w \lambda e^{-\lambda(w-u)}\, \lambda e^{-\lambda u}\, du
  = \int_0^w \lambda^2 e^{-\lambda w}\, du`; caption "the integrand does not
  depend on u."
- `erlang`: `f_W(w) = \lambda^2 w\, e^{-\lambda w}` in accent; the Erlang
  ramp-and-decay curve replaces the exponential on the axes; caption
  "Erlang, m = 2: the wait for the second arrival." The derivation stack
  ends centered on the halfway anchor (2026-07-05 draft review, 4:50).
- `gauss`: title Transforms to "Gaussians"; exponential chart cleared; two
  standard bells drawn centered on the halfway anchor (2026-07-05 draft
  review, 5:02 + 5:05); the complete-the-square line:
  `f_W(w) = \frac{1}{2\pi} e^{-w^2/4} \int_{-\infty}^{\infty}
  e^{-(u - w/2)^2}\, du`, the leftover integral boxed as "a Gaussian
  density, integrates to one."
- `stable`: `f_W(w) = \frac{1}{\sqrt{4\pi}}\, e^{-w^2/4}` in accent; a
  lower, wider bell (variance 2) drawn over the two standard bells fading
  to muted; caption "means add, variances add." The Gaussian equation
  stack ends centered on the halfway anchor (2026-07-05 draft review,
  5:44).

---

## Beat: mgf-product  (scene: MGFProduct)

> Each of those answers cost one integral. <bookmark mark="title"/> This
> chapter closes with the shortcut. Sums become products — the same banner
> the discrete chapter flew, and the same trick underneath.
> <bookmark mark="rule"/> Take the moment generating function of
> the sum. e to the s W splits into e to the s X, times e to the s Y — and
> independence factors the expectation of the product. The MGF of a sum is
> the product of the MGFs. We built this transform when we introduced moment
> generating functions; this is the moment it earns its keep. <bookmark mark="redo"/> Rerun the Gaussian
> sum, now with arbitrary parameters: the MGF of each Gaussian is an
> exponential in s, with its mean on the linear term and its variance on the
> square. <bookmark mark="add"/> Multiply the two, and the exponents simply
> add: m one plus m two on s, sigma one squared plus sigma two squared on s
> squared over two. That is a Gaussian MGF with the summed mean and the
> summed variance — the general fact, in two lines, no convolution in sight.
> <bookmark mark="outro"/> The key idea of this video: for independent
> variables, densities convolve, and transforms multiply. Next up is the
> final chapter: sums of many variables, and the types of convergence that
> govern them.

**Cues**
- `title`: section title "Sums Become Products" — video 25's title card
  returning verbatim, written centered then docked up. (2026-07-05 draft
  review, 5:47 + 5:50: "and honest work it was" cut from the narration, and
  the bookmark moved so the title's Write starts exactly with "This chapter
  closes with the shortcut"; the dock-up rides the "Sums become products"
  sentence.)
- `rule`: `M_W(s) = \mathrm{E}\left[e^{sW}\right]
  = \mathrm{E}\left[e^{sX}\right] \mathrm{E}\left[e^{sY}\right]
  = M_X(s)\, M_Y(s)` building term by term; result in accent. (2026-07-04
  register pass: narration "Video thirty-four built this transform" is now
  "We built this transform when we introduced moment generating functions"
  — topic anchor, not a number.)
- `redo`: the two Gaussian MGF cards side by side:
  `M_X(s) = e^{m_1 s + \sigma_1^2 s^2 / 2}`,
  `M_Y(s) = e^{m_2 s + \sigma_2^2 s^2 / 2}`.
- `add`: the exponents combine:
  `M_W(s) = \exp\left((m_1 + m_2)s +
  \frac{(\sigma_1^2 + \sigma_2^2) s^2}{2}\right)` in accent; caption
  "Gaussian again: mean m1 + m2, variance sigma1 squared + sigma2 squared."
- `outro`: shared outro card — key idea ("For independent variables,
  densities convolve," / "and transforms multiply.") + "Coming up: Types of
  Convergence".

---

## Cut list (if over budget)

1. Compress the `cdf`/`factor` derivation in convolution-def to the
   half-plane picture plus the first and last algebra lines (saves ~60
   words).
2. Trim the exponential example to its flat-integrand line plus the boxed
   Erlang answer (saves ~40 words).
3. Drop the closing sentence of uniform-sum ("the discrete twin, resolved
   into a continuum") and the dice mini-chart (saves ~35 words).
