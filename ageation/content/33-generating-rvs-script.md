---
slug: 33-generating-rvs
title: Generating Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 33-generating-rvs.md
derived_from_sha256: cc31793a15f51729f2e0a4b0f47e91f1caaa9bddcc5bf499640f7c342a7e379b
provenance_stamped: 2026-07-06
target_scene_file: scenes/generating_rvs.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Turn one Uniform(0,1) routine into a generator for any distribution - invert the CDF, or bin it."
  recap: "Last video: the change-of-variables formula - a monotone map transforms a density by its slope."
  key_idea: "The CDF is a two-way bridge: run it forward to derive distributions, backward to generate them from a single uniform routine."
  bridge: "Coming up: Moment Generating Functions"

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word
# — the target budgets the FINAL.
target_runtime_sec: 300
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / wpm (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 359
measured_runtime_sec: 324.8

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 99
    est_sec: 38
    measured_sec: 38.7
    sync_points: [flatten, backwards, worked, discrete]
  - id: uniform-from-cdf
    scene_class: UniformFromCDF
    narration_words: 200
    est_sec: 77
    measured_sec: 71.5
    sync_points: [setup, apply, flat, uniform]
  - id: inverse-cdf-method
    scene_class: InverseCDFMethod
    narration_words: 206
    est_sec: 79
    measured_sec: 69.8
    sync_points: [identity, derive, rain, dense, method]
  - id: exponential-recipe
    scene_class: ExponentialRecipe
    narration_words: 174
    est_sec: 67
    measured_sec: 59.3
    sync_points: [cdf, invert, recipe, draws, check]
  - id: discrete-binning
    scene_class: DiscreteBinning
    narration_words: 256
    est_sec: 98
    measured_sec: 85.5
    sync_points: [pmf, bins, rule, drops, why, caveat, outro]
---

# Video Script — Generating Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video gave us the change-of-variables formula: pass a continuous
> random variable through a smooth monotone function, and the density
> transforms by the slope. This video points that formula at one special
> function, the CDF itself, and theory becomes an algorithm.
> <bookmark mark="flatten"/> First, feeding any continuous random variable
> through its own CDF flattens it to a uniform.
> <bookmark mark="backwards"/> Then we run the map backwards: the inverse
> CDF turns uniform draws into any distribution we want,
> <bookmark mark="worked"/> we work the recipe end to end for the
> exponential, <bookmark mark="discrete"/> and a binning trick handles
> discrete targets too. That closes chapter nine: derive forward, generate
> backward.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 9 · Functions and Derived
  Distributions", objective; card rises to the top edge; progress_tag(3, 3)
  in the DR corner.
- `flatten`: outline line "1. Any X, through its own CDF, is uniform".
- `backwards`: outline line "2. The inverse-CDF method".
- `worked`: outline line "3. A worked recipe: the exponential".
- `discrete`: outline line "4. Discrete targets: bins".

---

## Beat: uniform-from-cdf  (scene: UniformFromCDF)

> Start with the engineering problem. Simulations need random variables of
> every shape: exponential arrival times, Gaussian noise, discrete packet
> counts. But the computer offers exactly one primitive, a routine that
> returns a value uniformly distributed between zero and one. The goal of
> this video is to manufacture everything else from that single routine.
> <bookmark mark="setup"/> Here is the observation that unlocks it. Take any
> continuous random variable X with an invertible CDF, and feed X into its
> own CDF: define Y equals F of X. <bookmark mark="apply"/> On the support
> of X, the CDF is differentiable and strictly increasing, and its
> derivative is the density itself. So last video's formula applies: the
> density of Y is the density of X divided by the absolute derivative of
> the CDF, and that is f of x over f of x, which is one.
> <bookmark mark="flat"/> One, for every y between zero and one, and zero
> outside, because a CDF never leaves the unit interval. The bumps cancel
> perfectly. Wherever X is likely, the CDF climbs fast and spreads those
> values out; wherever X is rare, the CDF barely moves and packs them
> together. <bookmark mark="uniform"/> Every continuous random variable,
> passed through its own CDF, becomes uniform on the unit interval.

**Cues** (per-phrase sub-blocks so each animation lands on its sentence)
- opening block: "the problem" as three muted want-lines (exponential,
  Gaussian, discrete) against the one available primitive, `Y \sim
  \text{Uniform}(0,1)` in accent.
- `setup`: problem lines clear; the CDF curve `F_X` rises on axes (left
  column); `Y = F_X(X)` written in accent (right column).
- `apply`: the change-of-variables chain
  `f_Y(y) = f_X(x)/\lvert \frac{dF_X}{dx}(x)\rvert = f_X(x)/f_X(x) = 1`
  written line by line; the `= 1` lands in accent.
- `flat`: the flat density `f_Y = 1` on (0,1) drawn as a unit-height slab;
  caption "0 outside, since 0 <= F <= 1" muted.
- `uniform`: boxed takeaway `F_X(X) \sim \text{Uniform}(0,1)` indicated.

---

## Beat: inverse-cdf-method  (scene: InverseCDFMethod)

> If the CDF is a bridge from any distribution to the uniform, cross it in
> the other direction. <bookmark mark="identity"/> When F is invertible,
> applying the inverse CDF to F of X returns X itself. So take Y uniform on
> the unit interval and define V equals F inverse of Y.
> <bookmark mark="derive"/> Derived distributions once more: the density of
> V is the density of Y divided by the derivative of the inverse map, which
> is the density of Y times the derivative of F at v. The uniform density
> is one, so what remains is exactly the density of X at v. The variable V
> has precisely the distribution we wanted. <bookmark mark="rain"/> Watch
> it work. Uniform draws rain down the vertical axis. Each one slides
> across to the CDF curve and drops to the horizontal axis. As draws
> accumulate, their histogram grows into the density of X.
> <bookmark mark="dense"/> Where the curve is steep, a wide band of uniform
> values funnels into a narrow interval, so the samples land densely,
> exactly where the density is high. Where the curve is shallow, the
> samples spread thin. <bookmark mark="method"/> This is the inverse-CDF
> method: to generate a random variable with CDF F, apply F inverse to a
> uniform draw. One uniform routine generates any continuous distribution.

**Cues** (the uniform rain is the centerpiece)
- opening block: the CDF curve reappears; an arrow along it flips
  direction (forward crossing demoted, backward crossing in accent).
- `identity`: `F_X^{-1}(F_X(X)) = X`, then `V = F_X^{-1}(Y)` in accent.
- `derive`: the two-step density chain
  `f_V(v) = f_Y(y)/\lvert \frac{dF_X^{-1}}{dy}(y)\rvert = f_Y(y)\,
  \frac{dF_X}{dv}(v) = f_X(v)` on two left-aligned lines; `f_X(v)` accent.
- `rain`: hardcoded uniform dots [0.13, 0.42, 0.58, 0.77, 0.31, 0.91,
  0.24, 0.66] fall down the y-axis of the CDF plot, slide horizontally to
  the curve, then drop to the x-axis.
- `dense`: the landed dots cluster where the curve is steep; a muted brace
  "steep = dense" under the crowded zone; thin zone noted.
- `method`: boxed recipe `X = F_X^{-1}(Y),\; Y \sim \text{Uniform}[0,1]`
  indicated once.

---

## Beat: exponential-recipe  (scene: ExponentialRecipe)

> The recipe deserves one full workout. Target: an exponential random
> variable with parameter lambda. <bookmark mark="cdf"/> Its CDF is one
> minus e to the minus lambda x, for x at least zero.
> <bookmark mark="invert"/> Inverting is algebra: set y equal to the CDF,
> solve for x, and out comes F inverse of y equals minus one over lambda,
> times the log of one minus y. <bookmark mark="recipe"/> So the generator
> is one line: X equals minus one over lambda, times the log of one minus
> Y. Take lambda equal to one to keep the numbers visible.
> <bookmark mark="draws"/> Feed it actual uniform draws. Point one three
> becomes a short wait. Point four two, a moderate one. Point nine one,
> where the logarithm climbs steeply, becomes a long one. Small uniforms map
> to short waits, and draws near one stretch deep into the tail.
> <bookmark mark="check"/> The change-of-variables formula confirms it:
> differentiating pushes the uniform density to lambda times e to the
> minus lambda x, exactly the exponential density. This is how a simulator
> makes arrivals: draw a uniform, take a logarithm, done.

**Cues** (worked example with the hardcoded draws)
- opening block: section title; target card `X \sim
  \text{Exponential}(\lambda)` muted.
- `cdf`: `F_X(x) = 1 - e^{-\lambda x}, \; x \geq 0` written.
- `invert`: two algebra lines: `y = 1 - e^{-\lambda x}` then
  `F_X^{-1}(y) = -\tfrac{1}{\lambda}\log(1 - y)`; second line accent.
- `recipe`: the generator `X = -\tfrac{1}{\lambda}\log(1 - Y)` boxed in
  accent; the earlier lines demote to ink; caption `\lambda = 1` muted.
- `draws`: a small table of draws animates: 0.13 -> 0.14, 0.42 -> 0.54,
  0.91 -> 2.41 (values of -log(1-y) at lambda 1); each row lands as
  spoken, with a short/moderate/long tick on a number line. (2026-07-04
  register pass: "far up the ramp of the logarithm" -> "where the
  logarithm climbs steeply".)
- `check`: verification line `f_X(x) = f_Y(y) \big/ \tfrac{1}{\lambda(1-y)}
  = \lambda e^{-\lambda x}` written; closing caption "draw a uniform, take
  a logarithm" muted.

---

## Beat: discrete-binning  (scene: DiscreteBinning)

> Discrete targets need one twist, because a staircase CDF has no inverse.
> Bins do the job instead. <bookmark mark="pmf"/> Take a PMF on values x
> one, x two, x three, with masses point two, point five, and point three.
> Its CDF climbs in jumps: point two, then point seven, then one.
> <bookmark mark="bins"/> Now slice the unit interval at exactly those
> heights. The first bin runs from zero to point two, the second from
> point two to point seven, the third from point seven to one. Each bin's
> length is exactly the mass of its value. <bookmark mark="rule"/> The
> generator is a case statement: draw Y uniform, and output x i when Y
> lands in bin i. <bookmark mark="drops"/> Watch the draws fall. Point one
> three lands in the first bin: output x one. Point four two, second bin:
> x two. Point seven seven, third bin: x three. <bookmark mark="why"/> The
> probability of outputting x i is the probability that a uniform draw
> lands in its bin, and that is the bin's length, F at x i minus F at x i
> minus one, which is exactly the PMF at x i. The video that introduced
> CDFs proved that a discrete CDF's jump heights are the probabilities;
> here the risers become sampling bins. <bookmark mark="caveat"/> One caveat: a naive case
> statement can be slow, and many discrete distributions have far more
> efficient generators. <bookmark mark="outro"/> That closes chapter nine.
> The key idea: the CDF is a two-way bridge. Run it forward to derive
> distributions; run it backward to generate them from a single uniform
> routine. Coming up: moment generating functions.

**Cues** (the [0,1] interval cut into PMF-sized bins)
- opening block: section title; staircase idea named.
- `pmf`: a small three-bar PMF (0.2, 0.5, 0.3) at left; its staircase CDF
  heights 0.2 / 0.7 / 1 as a header line snug above the chart, centred on
  the bars. (2026-07-04 draft review, 6:30: the `F_X: ...` line had been
  floating between the chart and the formula column — it now hugs the
  chart and the formula column rides higher, leaving a clear lane.)
- `bins`: a vertical unit interval at right partitioned at 0.2 and 0.7;
  the three bins tinted BLUE/TEAL/GREEN and labeled `p_X(x_1)`,
  `p_X(x_2)`, `p_X(x_3)`; boundary tick labels 0 / 0.2 / 0.7 / 1 sit left
  of the stack. (2026-07-04 draft review, 5:43: the stack moved right so
  the tick labels clear the rectangles — labels anchor to the rectangles'
  left edge with daylight, never under a bin.)
- `rule`: the case function `g(y) = x_i \;\text{ if }\; F_X(x_{i-1}) < y
  \leq F_X(x_i)` written; accent.
- `drops`: hardcoded dots 0.13, 0.42, 0.77 fall onto the interval one per
  spoken clause; each lights its bin and its output value `x_i` flashes by
  the matching PMF bar.
- `why`: `\Pr(X = x_i) = F_X(x_i) - F_X(x_{i-1}) = p_X(x_i)` written
  beneath; accent on the final equality. (2026-07-04 draft review, 6:30:
  the callback names the concept — "the video that introduced CDFs" —
  never a video number.)
- `caveat`: muted caption "case statements can be slow; better generators
  exist" over the final frame; nothing new drawn.
- `outro`: everything clears; shared outro card, key idea on two lines +
  "Coming up:  Moment Generating Functions".

---

## Cut list (if over budget)

1. The efficiency caveat (optional concept): drop the `caveat` sentence and
   its caption entirely (saves ~18 words / ~7 s).
2. Compress the exponential verification (`check`) to "and the formula
   confirms it" (saves ~20 words / ~8 s).
3. Trim the callback to the CDF-introduction video in `why` (saves
   ~18 words / ~7 s).
