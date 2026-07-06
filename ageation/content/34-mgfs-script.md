---
slug: 34-mgfs
title: Moment Generating Functions
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 34-mgfs.md
derived_from_sha256: 58dfc2dada5eb190bed3077fa095e17d4ddb6c780abc9aaa0ef77056206486ee
provenance_stamped: 2026-07-06
target_scene_file: scenes/mgfs.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Package every moment into one function: compute one transform, then differentiate."
  recap: "Last video closed chapter nine with the inverse-CDF sampler: uniform numbers in, any distribution out."
  key_idea: "One transform holds every moment: differentiate at zero and they fall out."
  bridge: "Next: The Markov and Chebyshev Inequalities, where expectations start bounding probabilities."

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

estimated_runtime_sec: 367
measured_runtime_sec: 329.5

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 92
    est_sec: 35
    measured_sec: 34.6
    sync_points: [definition, moments, examples]
  - id: mgf-definition
    scene_class: MGFDefinition
    narration_words: 249
    est_sec: 93
    measured_sec: 87.0
    sync_points: [dial, integral, laplace, ogf]
  - id: moments-by-differentiation
    scene_class: MomentsFromDerivatives
    narration_words: 147
    est_sec: 57
    measured_sec: 54.7
    sync_points: [swap, cascade, zero, readout]
  - id: exponential-mgf
    scene_class: ExponentialMGF
    narration_words: 171
    est_sec: 66
    measured_sec: 60.3
    sync_points: [integral, fraction, mean, nth, variance]
  - id: gaussian-mgf
    scene_class: GaussianMGF
    narration_words: 284
    est_sec: 116
    measured_sec: 92.8
    sync_points: [setup, square, slide, result, affine, general, check, outro]
---

# Video Script — Moment Generating Functions

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video closed the chapter on derived distributions with a sampler:
> push uniform numbers through the inverse CDF and any distribution you
> want comes out. This chapter puts expectations to a new use, turning
> them into bounds on probabilities — and it opens by forging the tool
> the sharpest bound will run on. <bookmark mark="definition"/> In this
> video we meet the moment generating function: one expectation with a
> dial. <bookmark mark="moments"/> We differentiate it and watch every
> moment fall out, <bookmark mark="examples"/> and we work the transform
> for two densities we know well: the exponential and the Gaussian.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 10  ·  Expectations and
  Bounds", two-line objective; progress_tag(1, 3) in the DR corner; card
  rises to the top edge. No on-screen recap line (spoken only).
- `definition`: outline line "1. The definition: one expectation, one dial"
  fades in.
- `moments`: outline line "2. Moments by differentiation" fades in.
- `examples`: outline line "3. Two worked transforms: exponential, Gaussian"
  fades in.

---

## Beat: mgf-definition  (scene: MGFDefinition)

> Here is the definition. The moment generating function of a random
> variable X is the expected value of e to the s X.
> <bookmark mark="dial"/> Read it as a probe. The number s is a dial: fix
> a setting, and the expectation returns a single number. Sweep the dial,
> and you trace out an entire function of s that encodes the distribution
> of X. <bookmark mark="integral"/> For a continuous random variable, the
> expectation is an integral: the density of X, weighted by e to the s x,
> integrated over the whole line. At s equals zero the weight is flat and
> the integral is exactly one. Tilt s positive, and the weight favors the
> large values of x — the transform feels the right tail.
> <bookmark mark="laplace"/> If you have met the Laplace transform in a
> circuits or signals course, you have seen this integral before. The
> moment generating function is a variant of it, and it strikes the same
> bargain: hard operations in one domain become easy operations in the
> transform domain. <bookmark mark="ogf"/> The definition covers discrete
> random variables too. For an integer-valued X, the expectation is a
> sum: e to the s k, times the mass at k, over all values k. That is
> exactly the ordinary generating function from when sums became
> products for discrete variables, evaluated at z equals e to the s.
> Same machine, new coordinates — and as a party
> trick, it grinds out the mean of a discrete uniform with two rounds of
> l'Hopital's rule and no special sums.

**Cues**
- opening: section title docks up; `M_X(s) = \mathrm{E}[e^{sX}]` written,
  left-hand side in accent.
- `dial`: caption "one number per dial setting" (muted) beneath the
  definition; accent demotes to ink when focus moves.
- `integral`: `M_X(s) = \int_{-\infty}^{\infty} f_X(x)\, e^{sx}\, dx`
  written below; small chart at the bottom: a bell density (BAR) with the
  weight curve `e^{sx}` overlaid, tilting up to the right (accent while
  named, then fades with the chart).
- `laplace`: muted caption "a variant of the Laplace transform".
- `ogf`: chart cleared first; `M_X(s) = \sum_k e^{sk}\, p_X(k) = G_X(e^s)`
  written, the `G_X(e^s)` term in accent — the generating-function video's
  card returning; muted note "the ordinary generating function, in new
  coordinates" (no video number on screen or in voice — refer to the
  concept; 2026-07-04 draft review, 2:00). The discrete-uniform party
  trick is spoken only, no formula (concept map marks it optional; kept
  to one breath).

---

## Beat: moments-by-differentiation  (scene: MomentsFromDerivatives)

> Now the name earns itself. Suppose the transform exists on an open
> interval around s equals zero, and differentiate it n times.
> <bookmark mark="swap"/> The derivative slips inside the expectation, so
> we are differentiating e to the s X with respect to s, n times over.
> <bookmark mark="cascade"/> Watch what each pass does: differentiating
> once pulls one factor of X down in front of the exponential. Twice, X
> squared. After n passes, X to the n stands in front.
> <bookmark mark="zero"/> Now set s to zero. The exponential collapses to
> one, and what remains is the expected value of X to the n — the n-th
> moment, read off on demand. <bookmark mark="readout"/> In particular,
> the first derivative at zero is the mean, and the second derivative at
> zero is the second moment: the two numbers every variance computation
> needs, now delivered by one function. Compute the transform
> once, and differentiation replaces integration forever after.

**Cues**
- opening: section title; the differentiation claim
  `\frac{d^n}{ds^n} M_X(s)\big|_{s=0}` written.
- `swap`: `= \mathrm{E}\big[\frac{d^n}{ds^n} e^{sX}\big]\big|_{s=0}`
  continues the line (derivative slips inside).
- `cascade`: the derivative cascade, one line per pass:
  `X e^{sX}`, `X^2 e^{sX}`, `X^n e^{sX}` — each factor landing as it is
  spoken, the accumulating power in accent.
- `zero`: the exponential term fades to muted; `= \mathrm{E}[X^n]` lands
  in accent.
- `readout`: the two read-outs `M_X'(0) = \mathrm{E}[X]`,
  `M_X''(0) = \mathrm{E}[X^2]` written side by side; caption
  "differentiate, do not integrate" (muted). Narration refers to the
  variance concept, not a video number (2026-07-04 draft review, 3:28).

---

## Beat: exponential-mgf  (scene: ExponentialMGF)

> Time to work one end to end. Let X be exponential with parameter
> lambda. <bookmark mark="integral"/> The transform is a single easy
> integral. From zero to infinity, lambda e to the minus lambda x, times
> the probe e to the s x. The two exponentials merge into e to the minus
> lambda minus s, times x — and for s below lambda, the integral
> evaluates to lambda over lambda minus s. <bookmark mark="fraction"/>
> That compact fraction now holds every moment of X.
> <bookmark mark="mean"/> Differentiate once: lambda over lambda minus s
> squared. Set s to zero, and the mean appears: one over lambda — no
> integration by parts required. <bookmark mark="nth"/> Keep
> differentiating and a factorial builds up: the n-th derivative is n
> factorial lambda over lambda minus s to the n plus one, which at zero
> is n factorial over lambda to the n. Every moment of the exponential,
> from one integral. <bookmark mark="variance"/> The variance rides along
> for free: the second moment is two over lambda squared; subtract the
> square of the mean, and one over lambda squared remains.

**Cues**
- opening: section title; `X \sim \text{Exponential}(\lambda)` card.
- `integral`: the chain
  `M_X(s) = \int_0^\infty \lambda e^{-\lambda x} e^{sx} dx
  = \int_0^\infty \lambda e^{-(\lambda - s)x} dx
  = \frac{\lambda}{\lambda - s}` revealed step by step; condition
  `s < \lambda` as a muted caption.
- `fraction`: the fraction indicated in accent; the derivation demotes.
- `mean`: `\mathrm{E}[X] = \frac{\lambda}{(\lambda-s)^2}\big|_{s=0}
  = \frac{1}{\lambda}` written.
- `nth`: `\mathrm{E}[X^n] = \frac{n!\,\lambda}{(\lambda-s)^{n+1}}
  \big|_{s=0} = \frac{n!}{\lambda^n}` written, the result in accent.
- `variance`: `\mathrm{Var}(X) = \frac{2}{\lambda^2} -
  \frac{1}{\lambda^2} = \frac{1}{\lambda^2}` closes the beat.

---

## Beat: gaussian-mgf  (scene: GaussianMGF)

> The jewel of the catalog is the standard normal.
> <bookmark mark="setup"/> Its density is e to the minus x squared over
> two, scaled by the square root of two pi. Multiply by the probe, and
> the two exponents merge into minus x squared minus two s x, over two.
> <bookmark mark="square"/> Now complete the square: add and subtract s
> squared inside, and the exponent splits into minus x minus s squared
> over two, plus s squared over two. The clean factor, e to the s squared
> over two, steps outside the integral. <bookmark mark="slide"/> Look at
> what stays inside: a Gaussian density whose center has slid from zero
> to s. Sliding a bell curve does not change its area — it still
> integrates to exactly one. <bookmark mark="result"/> So the integral
> vanishes, and the factor out front is the whole answer: the moment
> generating function of the standard normal is e to the s squared over
> two — the simplest transform in the catalog.
> <bookmark mark="affine"/> One more rule lifts this to every Gaussian.
> For Y equals a X plus b, the transform of Y is e to the s b, times the
> transform of X at a s: the shift walks out of the expectation, and the
> scale folds into the dial. <bookmark mark="general"/> Apply it to Y
> equals sigma X plus m — an affine function of a Gaussian is Gaussian —
> and the general answer appears: e to the s m plus s squared sigma
> squared over two. <bookmark mark="check"/> Differentiate at zero: the
> mean is m; the second moment is sigma squared plus m squared; so the
> variance is sigma squared, exactly as anticipated.
> <bookmark mark="outro"/> The key idea of this video: one transform
> packages every moment — compute it once, and differentiate instead of
> integrating.

**Cues**
- opening: section title; the standard normal density
  `f_X(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}` written.
- `setup`: `M_X(s) = \int \frac{1}{\sqrt{2\pi}}
  e^{-(x^2 - 2sx)/2} dx` — the merged exponent.
- `square`: the completed square
  `= e^{s^2/2} \int \frac{1}{\sqrt{2\pi}} e^{-(x-s)^2/2} dx`, the freed
  factor in accent.
- `slide`: chart at the bottom: the standard bell (BAR) slides its center
  from zero to s; as the narration notes the area is unchanged, the area
  under the slid curve shades in (BAR fill, 0.3 opacity, declared via
  mark_intended_overlap) together with the caption "area stays one"
  (muted; word spelled out) (2026-07-04 draft review, 5:35). One chart
  at a time; cleared before the affine block.
- `result`: `M_X(s) = e^{s^2/2}` lands in accent; derivation demotes.
- `affine`: `M_{aX+b}(s) = e^{sb}\, M_X(as)` written (accent moves here).
- `general`: `M_Y(s) = e^{sm + s^2\sigma^2/2}` for `Y = \sigma X + m`.
- `check`: read-outs `\mathrm{E}[Y] = m`,
  `\mathrm{E}[Y^2] = \sigma^2 + m^2`, `\mathrm{Var}(Y) = \sigma^2`.
- `outro`: everything clears; shared outro card — "Key idea" + two-line
  takeaway + "Coming up: The Markov and Chebyshev Inequalities". The
  spoken close ends at "…differentiate instead of integrating." — the
  "Keep it in your pocket…" sentence is deleted; the card holds briefly
  so the visuals fit the shorter audio (2026-07-04 draft review, 6:54).

---

## Cut list (if over budget)

1. Drop the discrete-uniform party-trick sentence in `mgf-definition`
   (the concept map's starred optional entry; saves ~30 words).
2. Compress `nth` in `exponential-mgf` to the boxed result, skipping the
   factorial-buildup sentence (~25 words).
3. Trim the Laplace paragraph to its first sentence (~25 words).
