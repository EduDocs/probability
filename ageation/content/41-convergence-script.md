---
slug: 41-convergence
title: Types of Convergence
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved via chat 2026-07-04
derived_from: 41-convergence.md
derived_from_sha256: 2296831ad514b3c6c181d4432f4e5e488048d41e2ad7d4b3e7a1fc1c94bc37d6
provenance_stamped: 2026-07-06
target_scene_file: scenes/convergence.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Three ways a sequence of random variables can settle down - in probability, in mean square, in distribution."
  recap: "Last video: sums of continuous random variables - convolution stacked the densities, and the MGF turned sums into products."
  key_idea: "One sequence can settle in three senses - in probability, in mean square, in distribution - and the limit theorems demand you know which."
  bridge: "Next: The Law of Large Numbers - the concentrating sequence becomes a theorem."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova finals ~0.31 s/word; gTTS drafts ~0.44 s/word — the target budgets the FINAL
target_runtime_sec: 300
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / wpm (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 380
measured_runtime_sec: 339.0

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 110
    est_sec: 44
    measured_sec: 41.9
    sync_points: [ask, prob, ms, dist]
  - id: two-sequences
    scene_class: TwoSequences
    narration_words: 223
    est_sec: 89
    measured_sec: 78.7
    sync_points: [sum, squeeze, invariant, never-moves, two]
  - id: in-probability
    scene_class: ConvergenceInProbability
    narration_words: 187
    est_sec: 75
    measured_sec: 66.7
    sync_points: [band, gaussian, uniform, verdict]
  - id: mean-square
    scene_class: MeanSquareConvergence
    narration_words: 188
    est_sec: 75
    measured_sec: 67.7
    sync_points: [example, bridge, chebyshev, cap, moral]
  - id: in-distribution
    scene_class: ConvergenceInDistribution
    narration_words: 242
    est_sec: 97
    measured_sec: 83.9
    sync_points: [seen, uniform-cdf, continuity, verdict, outro]
---

# Video Script — Types of Convergence

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is
an authoring marker: the generated scene splits the narration into
*sequential* voiceover blocks at each marker (bookmark-free timing; no
Whisper). All cross-references are by concept, never by video number.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, we built the distribution of a sum of continuous random
> variables: convolution stacked the densities, and moment generating
> functions turned sums into products. <bookmark mark="ask"/> Now we ask what
> happens as the sequence of sums runs on forever. Random variables can
> settle down in more than one sense, and the finale of this course depends
> on telling those senses apart. In this video we meet three of them, each
> with its own picture. <bookmark mark="prob"/> First, convergence
> in probability: deviations of any fixed size become vanishingly rare.
> <bookmark mark="ms"/> Second, mean square convergence: the average squared
> error itself dies out. <bookmark mark="dist"/> Third, convergence in
> distribution: only the CDFs need to settle onto a limiting shape.

**Cues** (outline lines land clause by clause, one sub-block each)
- opening block: intro card with kicker "Chapter 12  ·  Limit Theorems"
  (title verified against the vendored chapter line), title, two-line
  objective; card rises to the top edge; `progress_tag(1, 3)` in DR corner.
- `self.wait(0.5)` after the framing block, before the outline.
- `ask`: outline heading forms.
- `prob`: outline line "1.  Convergence in probability" fades in.
- `ms`: outline line "2.  Mean square convergence" fades in.
- `dist`: outline line "3.  Convergence in distribution" fades in.

---

## Beat: two-sequences  (scene: TwoSequences)

> Everything starts with one experiment. A sequence of random variables X
> one, X two, and so on, together with a limiting random variable X, all
> defined on the same probability space — all functions of the outcome of a
> single experiment. Without that shared space, the difference between X n
> and X would mean nothing. <bookmark mark="sum"/> Take independent Gaussian
> variables, each with mean m and variance sigma squared, and form the
> partial sums S n. Sums of Gaussians stay Gaussian — that was the
> convolution result — so S n over n is Gaussian too, with mean m and
> variance sigma squared over n. <bookmark mark="squeeze"/> Watch that
> variance. As n grows, the density of S n over n squeezes onto m: taller,
> narrower at every step. The sequence of averages is becoming increasingly
> predictable. <bookmark mark="invariant"/> Now
> scale the same sums differently: subtract n times m, and divide by the
> square root of n. The mean is zero, and the variance works out to sigma
> squared — with no n left anywhere in it. <bookmark mark="never-moves"/>
> However large n gets, this sequence keeps the same Gaussian density: the
> distribution simply never moves. <bookmark mark="two"/> One recipe, two
> scalings, two utterly different behaviors — one collapses onto a point,
> the other holds its shape forever. Both patterns will return as theorems,
> so to say precisely what each is doing, we need vocabulary.

**Cues** (sequential section titles as the topic changes)
- opening: section title "One Experiment, One Sequence"; setup line
  `X_1, X_2, \ldots` and `X` on one probability space.
- `sum`: title transforms to "The Concentrating Sequence"; right column:
  `S_n = \sum X_i`, mean m, variance `\sigma^2/n` (BODY-size labels).
- `squeeze`: left chart (rides high, bottom buff ~1.3): Gaussian densities
  of `S_n/n` for n = 1, 4, 16 over a fixed mark at m; variance label counts
  down; caption centered on the chart (match_x).
- `invariant`: title transforms to "The Invariant Sequence"; formula
  `(S_n - nm)/\sqrt{n}`, mean 0, variance `\sigma^2`.
- `never-moves`: single Gaussian density redrawn identically while an
  n-counter (BODY size) ticks 1, 4, 16 — the curve never moves.
- `two`: side-by-side verdict captions "collapses onto m" / "never moves".

---

## Beat: in-probability  (scene: ConvergenceInProbability)

> Here is the first notion. A sequence X one, X two, and so on converges in
> probability to X if, for every positive epsilon, the probability that X n
> differs from X by epsilon or more tends to zero. <bookmark mark="band"/>
> Picture a band of half-width epsilon around the limit. Convergence in
> probability says the mass outside that band drains away — deviations of
> any visible size become vanishingly rare. <bookmark mark="gaussian"/> Our
> concentrating sequence does exactly this: S n over n converges in
> probability to m. The shaded tails outside the band carry less and less
> probability as the density squeezes in. <bookmark mark="uniform"/> A
> second example makes the definition almost trivial to check. Let X n be
> uniform on the interval from zero to one over n. The support itself
> shrinks toward zero, so once n exceeds one over epsilon, the whole
> distribution lives inside the band, and the deviation probability is not
> just small — it is exactly zero. <bookmark mark="verdict"/> So X n
> converges in probability to the constant zero. Keep this shrinking uniform
> family in mind: it returns at the end of the video wearing a different
> notion of convergence.

**Cues**
- opening: section title "Convergence in Probability"; the definition
  `\lim \Pr(|X_n - X| \geq \epsilon) = 0` in accent, "for every epsilon
  greater than zero" condition at BODY size.
- `band`: left chart: axis with m marked, epsilon band (two dashed lines
  starting AT the y-axis, never crossing tick labels) around m.
- `gaussian`: Gaussian density of `S_n/n` drawn over the band; tail areas
  outside the band SHADED (opacity 0.3, mark_intended_overlap) exactly on
  "shaded tails", then draining as the density narrows.
- `uniform`: swap to the uniform picture (one chart at a time): flat
  rectangular densities on [0, 1/n] for n = 1, 2, 5 shrinking inside the
  band; parameter tag "n = 1, 2, 5" at BODY size.
- `verdict`: accent line `X_n \to 0` in probability; caption "the deviation
  probability is exactly zero" centered under the chart.

---

## Beat: mean-square  (scene: MeanSquareConvergence)

> The second notion speaks the language of expectation. A sequence converges
> in mean square to X if the expected value of the squared difference
> between X n and X tends to zero. That is, the second moment of the error
> itself must vanish as n goes to infinity. <bookmark mark="example"/> For
> the Gaussian average, that expected squared error is exactly sigma squared
> over n — so the concentrating sequence converges in mean square to m, and
> we even see the rate: the error falls like one over n.
> <bookmark mark="bridge"/> Mean square convergence is the stronger claim:
> it implies convergence in probability, and the bridge is the Chebyshev
> bound from the inequalities video. <bookmark mark="chebyshev"/> Apply that
> bound to the variable X n minus X: the probability that the deviation
> reaches epsilon is at most the expected squared error divided by epsilon
> squared. <bookmark mark="cap"/> The hypothesis says the numerator tends to
> zero. Epsilon is fixed, so the whole bound collapses, and the deviation
> probability is squeezed to zero along with it. <bookmark mark="moral"/>
> One inequality converts one mode of convergence into the other — the same
> tool that once bounded tail probabilities now powers a limit statement.

**Cues**
- opening: section title "Mean Square Convergence"; definition
  `\lim \mathrm{E}[|X_n - X|^2] = 0` in accent.
- `example`: `\mathrm{E}[|S_n/n - m|^2] = \sigma^2/n \to 0` — long chain
  broken onto two lines, continuation built as ("=", rhs) with the "="
  x-aligned under the first line's "=".
- `bridge`: muted proposition card "mean square implies in probability"
  (arrow diagram, single accent moves to it).
- `chebyshev`: the Chebyshev line
  `\Pr(|X_n - X| \geq \epsilon) \leq \mathrm{E}[|X_n - X|^2]/\epsilon^2`.
- `cap`: numerator indicated; "\to 0" lands; bound collapses.
- `moral`: implication arrow accented once, everything else demoted to INK.

---

## Beat: in-distribution  (scene: ConvergenceInDistribution)

> The third notion asks for the least. A sequence converges in distribution
> to X if the CDF of X n converges to the CDF of X at every point where the
> limiting CDF is continuous. Only the distribution functions need to settle
> — this is also called weak convergence. <bookmark mark="seen"/> You have
> seen this pattern before: when the geometric staircase was squeezed into
> the exponential CDF, that was convergence in distribution, before it had a
> name. <bookmark mark="uniform-cdf"/> Now bring back the shrinking uniform
> family. The CDF of X n rises from zero to one across the interval from
> zero to one over n — and as n grows, these continuous CDFs steepen toward
> the unit step at zero. <bookmark mark="continuity"/> Here the fine print
> earns its keep. At every negative x the CDFs equal zero, and at every
> positive x they tend to one. But exactly at zero, each CDF of X n reads
> zero while the step reads one. No matter: zero is the one point where the
> limiting CDF jumps, so the definition simply exempts it.
> <bookmark mark="verdict"/> The sequence converges in distribution to the
> constant zero — a whole family of continuous random variables settling
> onto a deterministic limit. <bookmark mark="outro"/> The key idea of this
> video: one sequence can settle in three senses — in probability, in mean
> square, in distribution — and knowing which one you are claiming is
> exactly what the two great limit theorems ahead demand. Next up: the law
> of large numbers.

**Cues**
- opening: section title "Convergence in Distribution"; definition
  `\lim F_{X_n}(x) = F_X(x)` at continuity points, in accent; muted
  caption "also called weak convergence".
- `seen`: small echo panel: a staircase CDF over a smooth exponential CDF
  (concept callback, no video number anywhere on screen).
- `uniform-cdf`: main chart: CDFs of uniform [0, 1/n] for n = 1, 2, 5
  steepening toward the unit step at 0; one drawn per n with its label.
- `continuity`: the point (0, 0) vs (0, 1) flagged; open/closed dots; the
  x = 0 exemption caption at BODY size, clear of the axis ticks.
- `verdict`: accent line `X_n \to 0` in distribution.
- `outro`: full clear, then outro_bridge key-idea card ("One sequence,
  three senses of settling:" / "in probability, in mean square, in
  distribution.") + "Coming up: The Law of Large Numbers";
  `self.wait(0.5)` before the final fade.

---

## Cut list (if over budget)

1. ~~Drop "That is the whole definition..." from `in-probability`~~ —
   APPLIED 2026-07-04 (draft measured 439.9 s put the projected final
   ~7 s over budget; saved 13 words plus animation overhead).
2. Trim the `seen` geometric-to-exponential echo panel in `in-distribution`
   to the spoken sentence alone (saves ~8 s of visuals, no words).
3. Compress the uniform example in `in-probability` to one sentence
   ("the support shrinks inside any band, so the deviation probability
   is eventually zero") — saves ~35 words.
4. Drop the closing sentence of `two-sequences` ("Both patterns will
   return...") — saves ~10 words.
