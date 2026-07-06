---
slug: 30-additional-distributions
title: A Gallery of Densities
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 30-additional-distributions.md
derived_from_sha256: f69fcea359f8580a97b7de5948dce1d2589e80aeb9bbef4fb2605dc8a10a2aba
provenance_stamped: 2026-07-06
target_scene_file: scenes/additional_distributions.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Four more named densities, each one a record of a construction built from distributions you already know."
  recap: "Last video: the exponential completed the triad - waiting times, the squeezed geometric, and memorylessness."
  key_idea: "A named density is a record of a construction - know how a curve is built, and you know when to reach for it."
  bridge: "Next chapter: derived distributions - what happens when a continuous random variable is pushed through a function."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# Series calibration: nova finals measure ~0.31 s/word. ~920 words -> ~285 s.
target_runtime_sec: 310
tolerance_sec: 45         # check_status fails rendered+ chapters outside this

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / wpm (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 359
measured_runtime_sec: 339.4

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 101
    est_sec: 39
    measured_sec: 37.8
    sync_points: [family, settings, gaussian, warning]
  - id: gamma
    scene_class: GammaDistribution
    narration_words: 221
    est_sec: 85
    measured_sec: 77.7
    sync_points: [def, recursion, factorial, half, density, dial]
  - id: special-cases
    scene_class: GammaSpecialCases
    narration_words: 187
    est_sec: 72
    measured_sec: 69.7
    sync_points: [exponential, chi-square, erlang, stream, one-family]
  - id: rayleigh
    scene_class: RayleighDistribution
    narration_words: 155
    est_sec: 60
    measured_sec: 57.9
    sync_points: [scatter, radius, density, trap, square]
  - id: laplace-cauchy
    scene_class: LaplaceCauchy
    narration_words: 267
    est_sec: 103
    measured_sec: 96.3
    sync_points: [splice, laplace, cauchy, average, gallery, outro]
---

# Video Script — A Gallery of Densities

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> The uniform, the Gaussian, the exponential — three densities carried this
> chapter. But engineering keeps a wider gallery, and every curve in it is a
> record of a construction. <bookmark mark="family"/> In this video we extend
> the factorial into the gamma function and unlock a two parameter family,
> the gamma distribution, <bookmark mark="settings"/> then read three of its
> settings: the exponential, the kai square, and the Erlang.
> <bookmark mark="gaussian"/> We take the length of a Gaussian vector and
> meet the Rayleigh, then splice two exponentials into the Laplace,
> <bookmark mark="warning"/> and we close with a warning called the Cauchy —
> a density so heavy tailed that averaging accomplishes nothing.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 8  ·  Continuous Random
  Variables", objective; card rises to the top edge; `progress_tag(5, 5)` in
  the DR corner.
- `family`: outline line "1. The gamma function and the gamma family" fades in.
- `settings`: outline line "2. Exponential, chi-square, Erlang" fades in.
  (2026-07-05 draft review: "kai" phonetic respelling for TTS — the Greek
  letter chi is pronounced "kai"; narration only, on-screen text keeps
  "chi-square".)
- `gaussian`: outline line "3. Rayleigh and Laplace" fades in.
- `warning`: outline line "4. The Cauchy warning" fades in.

---

## Beat: gamma  (scene: GammaDistribution)

> Start with a function, not a density. <bookmark mark="def"/> The gamma
> function assigns to each positive number z an integral: u to the z minus
> one, times e to the minus u, integrated over the positive axis.
> <bookmark mark="recursion"/> Integrate by parts once and a recursion falls
> out: gamma of z plus one equals z times gamma of z.
> <bookmark mark="factorial"/> Chain that recursion down the integers, and
> gamma of k plus one is exactly k factorial. The gamma function is the
> factorial, extended off the integers into a smooth curve.
> <bookmark mark="half"/> Its most famous value at a non integer argument is
> gamma of one half, which equals the square root of pi. The proof squares
> the integral and switches to polar coordinates — the same trick that
> integrated the bell curve two videos ago, back for a second encore.
> <bookmark mark="density"/> Now build the density. Take lambda, times
> lambda x to the alpha minus one, times e to the minus lambda x, and divide
> by gamma of alpha so the total area is one. This is the gamma
> distribution, with a shape parameter alpha and a rate parameter lambda.
> <bookmark mark="dial"/> Together they form a dial. Turn it, and the curve
> sweeps from a steep decay at small alpha to a rounded hump that drifts
> rightward as alpha grows. Two knobs are enough to fit a remarkable range
> of measured data.

**Cues**
- section title "The Gamma Distribution", docked up.
- `def`: `\Gamma(z) = \int_0^\infty u^{z-1} e^{-u}\, du` in accent.
- `recursion`: `\Gamma(z+1) = z\, \Gamma(z)` written beneath; accent moves to
  it, the definition demotes to INK.
- `factorial`: `\Gamma(k+1) = k!` lands beside the recursion; caption
  "the factorial, extended" in muted.
- `half`: `\Gamma(1/2) = \sqrt{\pi}`; muted caption "the polar trick, second
  encore" (callback to video 28).
- `density`: formulas clear; the gamma PDF
  `f_X(x) = \lambda (\lambda x)^{\alpha-1} e^{-\lambda x} / \Gamma(\alpha)`
  in accent with "x > 0" alongside.
- `dial`: axes rise; one gamma curve morphs through (alpha, lambda)
  settings — steep decay to rounded, right-drifting humps — with a muted
  parameter label updating at each pause. (2026-07-05 draft review: axis
  tick numbers at `TICK` (26), one size smaller series-wide — applied in
  the shared `density_axes` helper, so every chart in this video.)

---

## Beat: special-cases  (scene: GammaSpecialCases)

> One family, three famous settings. <bookmark mark="exponential"/> Set
> alpha to one, and the powers of x vanish: what remains is lambda e to the
> minus lambda x — the exponential distribution, last video's star, sitting
> at the very first notch of the dial. <bookmark mark="chi-square"/> Set
> lambda to one half and alpha to k over two, and the family becomes the kai
> square distribution with k degrees of freedom. Its construction comes from
> the Gaussian density: square k independent standard normal variables and add
> them, and the sum is kai square. That construction makes it a workhorse of
> statistical inference. <bookmark mark="erlang"/> Set alpha to a positive
> integer m, and the family is called Erlang. Here the construction is a sum
> of waits: add m independent exponential waiting times, each with rate
> lambda. <bookmark mark="stream"/> Picture the arrival stream from last
> video. The wait to the first arrival is exponential. The wait to the
> second stacks two of them. Keep going, and the time of the m-th arrival is
> Erlang — its density humps and drifts rightward as m grows.
> <bookmark mark="one-family"/> Three names, one formula. The label on the
> curve tells you which construction produced it.

**Cues**
- section title "Chi-Square and Erlang", docked up.
- `exponential`: the gamma curve at alpha = 1 with label "Exponential" and
  `f_X(x) = \lambda e^{-\lambda x}`; the curve is the one accent object.
- `chi-square`: curve morphs to the chi-square setting (lambda = 1/2,
  alpha = k/2); label swaps; construction line
  `X = Z_1^2 + \cdots + Z_k^2` with muted "k degrees of freedom".
  (2026-07-04 draft review, 2:50: narration says "the Gaussian density",
  not "the bell curve" — no bare "bell"; the gamma beat's single "bell
  curve" mention stays as this video's one allowed use.)
  (2026-07-05 draft review: "kai" phonetic respelling for TTS — spoken
  form only; the card, formulas, and section title keep "chi-square" /
  `\chi^2`.)
- `erlang`: curve morphs to an integer-alpha hump; label swaps to "Erlang";
  `S_m = X_1 + \cdots + X_m` with the Erlang PDF (the (m-1)! form).
- `stream`: the dot stream returns; brackets under the waits to the 1st,
  2nd, then m-th dot, summed into one long bracket labelled `S_m`.
- `one-family`: the three parameter tags shown together beneath the curve,
  muted, as a mini recap row.

---

## Beat: rayleigh  (scene: RayleighDistribution)

> Now build sideways from the Gaussian. <bookmark mark="scatter"/> Scatter a
> cloud of points on a plane, with each coordinate an independent zero mean
> Gaussian. <bookmark mark="radius"/> Then ask a geometric question: how far
> does a point land from the center? That length, the square root of X
> squared plus Y squared, is a new random variable.
> <bookmark mark="density"/> Its density is the Rayleigh distribution: r
> over sigma squared, times e to the minus r squared over two sigma squared.
> It rises from zero, peaks, and decays — the shape of amplitude fading in
> urban radio, where reflected signals add like Gaussian coordinates.
> <bookmark mark="trap"/> One naming trap deserves a clear sentence. The
> sigma squared in the formula honors the Gaussians inside the construction.
> It is not the Rayleigh's own variance, which works out to four minus pi
> over two, times sigma squared. <bookmark mark="square"/> And one bonus
> connection: square a Rayleigh variable and you get an exponential — the
> gallery keeps looping back on itself.

**Cues**
- section title "The Rayleigh Distribution", docked up.
- `scatter`: small centered axes (left column) with 40 pre-computed
  Gaussian points fading in (no runtime randomness). (2026-07-05 draft
  review: the old handpicked cloud read as uniform; each marginal is now
  exactly the standard-normal quantiles Phi^{-1}((i+0.5)/40), paired in a
  fixed order — dense center, sparse tails.)
- `radius`: one point turns accent; a line is drawn from the origin to it;
  `R = \sqrt{X^2 + Y^2}` beside the cloud.
- `density`: right column, the Rayleigh PDF
  `f_R(r) = (r/\sigma^2)\, e^{-r^2/(2\sigma^2)}`, r >= 0, plus a small
  Rayleigh curve. (2026-07-04 draft review, 4:10: the muted "wireless
  fading" caption is removed — on-screen only; narration unchanged.)
- `trap`: `\mathrm{Var}(R) = \frac{4-\pi}{2}\,\sigma^2` with muted caption
  "sigma squared names the Gaussians inside".
- `square`: muted line `R^2 \sim \text{exponential}`.

---

## Beat: laplace-cauchy  (scene: LaplaceCauchy)

> Two curves remain, and they bracket the gallery.
> <bookmark mark="splice"/> Take last video's exponential density, flip a
> copy across zero, glue the halves at the peak, and renormalize — the
> factor of one half keeps the area at one.
> <bookmark mark="laplace"/> The result is the Laplace distribution: e to
> the minus absolute value of x over b, divided by two b. It is symmetric
> like a Gaussian, but sharper at the peak and heavier in the tails — and it
> records its own construction: the difference of two independent
> exponential waits is Laplace. <bookmark mark="cauchy"/> The final curve
> looks tame: gamma over pi times gamma squared plus x squared. This is the
> Cauchy distribution, and its tails decay so slowly that the mean is
> undefined. No mean, no variance, no higher moments.
> <bookmark mark="average"/> It gets worse. Average n independent Cauchy
> variables, and the sample mean is Cauchy with the same parameter. Watch a
> running mean: it jumps, drifts, and refuses to settle, no matter how many
> samples arrive. Averaging is not a universal cure.
> <bookmark mark="gallery"/> Step back and read the gallery: the gamma from
> the extended factorial, the kai square from squared normals, the Erlang
> from summed waits, the Rayleigh from a vector's length, the Laplace from a
> difference of waits, and the Cauchy from tails too heavy to tame. Every
> curve is a construction. <bookmark mark="outro"/> The key idea
> of this video: a named density is a record of a construction — know how a
> curve is built, and you know when to reach for it. That closes chapter
> eight. Next chapter: derived distributions — what happens when a
> continuous random variable is pushed through a function.

**Cues**
- section title "Laplace", docked up. (2026-07-04 draft review, 5:10: the
  two densities are treated in sequence, each under its own title — the
  beat used to open on a shared "Laplace and Cauchy" title. The spoken
  opener "Two curves remain..." is the cue that two densities are coming.)
- `splice`: an exponential curve on the positive axis; a mirrored copy
  flips across zero; the two halves glue at the seam (declared overlap:
  the splice composition). (2026-07-04 draft review, 5:10: narration now
  says the spliced result is renormalized — the factor of one half keeps
  the area at one — matching the on-screen `e^{-|x|/b}/(2b)`.)
- `laplace`: `f_X(x) = \frac{1}{2b} e^{-|x|/b}` in accent; muted line
  `X_1 - X_2 \sim \text{Laplace}` for the difference construction.
- `cauchy`: the section title Transforms from "Laplace" to "Cauchy"
  (2026-07-04 draft review, 5:10); the Laplace clears; the Cauchy curve
  appears with
  `f_X(x) = \frac{\gamma}{\pi(\gamma^2 + x^2)}`; a Gaussian ghost is shown
  in sequence and the Cauchy's fat tails get the accent; muted caption
  "no mean, no variance".
- `average`: a jittering running-mean polyline over sample count, from a
  hardcoded sequence of partial means; it visibly refuses to settle.
- `gallery`: closing gallery card, six small labelled curves, each tagged
  by its construction (declared overlap: the gallery composition).
  (2026-07-04 draft review, 6:30: the closing line reads "Every curve is a
  construction." — "remembered" dropped; nothing on screen mirrored it.)
  (2026-07-05 draft review: "kai" phonetic respelling for TTS — spoken
  form only; the gallery panel keeps "Chi-Square".)
- `outro`: shared outro card - key idea + "Coming up: Derived
  Distributions"; kicker context "Chapter 8  ·  Continuous Random
  Variables" closes with `progress_tag(5, 5)`.

---

## Cut list (if over budget)

1. Compress the Laplace segment to one sentence plus the splice picture
   (saves ~20 s): drop the difference-construction sentence.
2. Drop the Rayleigh mean/variance numbers, keep the construction and the
   naming trap (saves ~10 s).
3. Trim the `one-family` recap sentence at the end of special-cases
   (saves ~8 s).
