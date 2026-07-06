---
slug: 20-moments
title: Moments
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the 480p draft for finals 2026-07-03
derived_from: 20-moments.md
derived_from_sha256: b86b0caaa75ca7413509090f133d090afb724b301a5845e6445a56fd779cd405
provenance_stamped: 2026-07-06
target_scene_file: scenes/moments.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Climb the ladder of moments E[X^n] and compute variances the easy way, from the first two moments."
  recap: "Last video: E[g(X)] from the PMF, the mean as a balance point, the variance as spread."
  key_idea: "Var(X) = E[X^2] - (E[X])^2 -- the variance from the first two moments, usually the easiest route."
  bridge: "Next chapter: several random variables at once."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Timing contract set at approval (2026-07-03) from the series calibration:
# nova at 1.0 measures ~0.80x the gTTS draft (ch18: 262.7 -> 210.8 s;
# ch19: 404.8 -> 320.2 s). Approved draft: 281.3 s -> expected final ~225 s.
target_runtime_sec: 225
tolerance_sec: 45

estimated_runtime_sec: 290
measured_runtime_sec: 225.1

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 90
    est_sec: 36
    measured_sec: 31.1
    sync_points: [ladder, identity, central]
  - id: moments
    scene_class: MomentsDefinition
    narration_words: 130
    est_sec: 52
    measured_sec: 32.1
    sync_points: [ladder, first-moment]
  - id: variance-formula
    scene_class: VarianceFromMoments
    narration_words: 170
    est_sec: 68
    measured_sec: 52.7
    sync_points: [expand, collapse, poisson-callback]
  - id: uniform
    scene_class: UniformExample
    narration_words: 165
    est_sec: 66
    measured_sec: 49.0
    sync_points: [flat-pmf, two-sums, result]
  - id: central
    scene_class: CentralMoments
    narration_words: 165
    est_sec: 66
    measured_sec: 60.2
    sync_points: [centering, skewness, kurtosis, takeaway, outro]
---

# Video Script — Moments

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> We now have two summaries of a random variable: the mean, where its PMF
> balances, and the variance, how far it spreads. This video completes the
> family. <bookmark mark="ladder"/> The moments of a random variable are the
> expectations of its powers, and they come with the most useful computational
> identity in the chapter: the variance from the first two moments.
> <bookmark mark="identity"/> We'll prove it in three lines, put it to work on
> a uniform random variable, <bookmark mark="central"/> and close with the
> central moments — the quantities behind skewness and kurtosis.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 6 · Meeting Expectations",
  recap line, objective; card rises to the top edge.
- `ladder`: outline line "1. The ladder of moments" fades in.
- `identity`: outline line "2. The identity at work" fades in.
- `central`: outline line "3. Central moments" fades in.

---

## Beat: moments  (scene: MomentsDefinition)

> The definition is last video's formula with the simplest possible family of
> functions. <bookmark mark="ladder"/> Take g of x equals x to the n. The n-th
> moment of X is the expectation of X to the n: sum x to the n times p sub X of
> x. One PMF, a whole ladder of numbers — first moment, second moment, third,
> and so on, each extracting a different feature from the same bars.
> <bookmark mark="first-moment"/> The first rung is an old friend: the first
> moment is exactly the mean. The higher rungs are new, and the second one is
> about to earn its keep.

**Cues**
- `ladder`: one house PMF chart at left; a column of chips at right filling
  in: `\mathrm{E}[X]`, `\mathrm{E}[X^2]`, `\mathrm{E}[X^3]`, with
  `\mathrm{E}[X^n] = \sum_{x \in X(\Omega)} x^n p_X(x)` in accent above.
- `first-moment`: the top chip glows; caption "the mean is the first moment."

---

## Beat: variance-formula  (scene: VarianceFromMoments)

> Here is the payoff. Start from the definition of the variance: the expected
> squared deviation from the mean. <bookmark mark="expand"/> Expand the square
> inside: x squared, minus two x times the mean, plus the mean squared. Now use
> linearity — last video's rule — to split the sum into three pieces.
> <bookmark mark="collapse"/> The first piece is the second moment. The middle
> piece is minus two times the mean, times the mean again. The last piece is
> the mean squared, times masses that sum to one. Minus two mean-squared plus
> mean-squared: the cross terms collapse, and what survives is clean — the
> variance is the second moment minus the square of the first.
> <bookmark mark="poisson-callback"/> A quick dividend: last video the Poisson
> had mean lambda and variance lambda. Read the identity backwards and its
> second moment comes free — lambda squared plus lambda. No new sum required.

**Cues**
- `expand`: `\mathrm{Var}(X) = \mathrm{E}\left[(X - \mathrm{E}[X])^2\right]`
  expands via TransformMatchingTex into the three-term sum.
- `collapse`: the cross terms highlight and cancel; the surviving
  `\mathrm{Var}(X) = \mathrm{E}[X^2] - (\mathrm{E}[X])^2` lands in accent —
  the one thing on screen.
- `poisson-callback`: compact card:
  `\mathrm{E}[X^2] = \lambda^2 + \lambda` for Poisson(`\lambda`).

---

## Beat: uniform  (scene: UniformExample)

> Let's see the identity save real work. <bookmark mark="flat-pmf"/> Take X
> uniform on one through n: a flat PMF, mass one over n everywhere. Its mean
> is the midpoint, n plus one over two. Computing the variance from the
> definition would mean summing squared deviations from that midpoint — messy.
> <bookmark mark="two-sums"/> The identity asks for something easier: the
> second moment is one over n times the sum of the first n squares, and that
> sum is a calculus classic — n times n plus one times two n plus one, over
> six. Subtract the square of the mean. <bookmark mark="result"/> The algebra
> telescopes to n squared minus one, over twelve. Sanity check it on the fair
> die, n equals six: thirty-five over twelve, just under three — matching the
> spread you'd eyeball on its flat PMF. Two standard sums, no centered mess.

**Cues**
- `flat-pmf`: the uniform house chart on 1..n (render with n = 6);
  `\mathrm{E}[X] = \tfrac{n+1}{2}` beneath.
- `two-sums`: `\mathrm{E}[X^2] = \tfrac{1}{n}\sum_{k=1}^{n} k^2 =
  \tfrac{(n+1)(2n+1)}{6}` builds; then the subtraction line.
- `result`: `\mathrm{Var}(X) = \tfrac{n^2 - 1}{12}` in accent; card
  "n = 6: 35/12" beside the die-face glyph.

---

## Beat: central  (scene: CentralMoments)

> One refinement completes the picture. <bookmark mark="centering"/> Instead
> of powers of X, take powers of X minus its mean — center first, then raise.
> These are the central moments, and we already know the second one: it is the
> variance itself. <bookmark mark="skewness"/> The higher central moments
> each capture a different trait. The third, standardized, is the skewness: it
> is zero for a symmetric PMF and picks up sign when one tail stretches
> farther than the other. <bookmark mark="kurtosis"/> The fourth is behind
> the kurtosis, which asks whether the spread comes from rare, extreme
> deviations or from frequent modest ones. <bookmark mark="takeaway"/> We
> won't compute these here — they belong to statistics — but you will meet
> them, and now you know what they measure.
> <bookmark mark="outro"/> The key idea of this video — and the tool to keep:
> the variance is the second moment minus the square of the first. That
> closes our summary toolkit for a single random variable. Coming up next:
> what changes when we watch several random variables at once.

**Cues** (each portrait is on screen exactly while it is spoken; 2026-07-03
draft review, 3:50)
- `centering`: the PMF slides left so its fulcrum sits at zero (the affine
  shift, replayed); `\mathrm{E}\left[(X - \mathrm{E}[X])^k\right]` above.
- `skewness`: the right-skewed PMF, captioned "skewness: asymmetry".
- `kurtosis`: swap to the heavy-tailed PMF, captioned "kurtosis: tail weight".
- `takeaway`: hold the kurtosis still; no new elements.
- `outro`: shared outro card — key idea + "Coming up: Multiple Random
  Variables".

---

## Cut list (if over budget)

1. Drop the `poisson-callback` card to one spoken sentence.
2. Skip the n = 6 sanity check in `uniform` (keep the general result).
3. Compress `portraits` to a single split-second still with two captions
   shown sequentially.
