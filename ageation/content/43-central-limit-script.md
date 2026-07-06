---
slug: 43-central-limit
title: The Central Limit Theorem
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved via chat 2026-07-04
derived_from: 43-central-limit.md
derived_from_sha256: caf9e333e1bbf44675c56c9a25c7e32caa8176790d04a0b32afe367e81cf84a2
provenance_stamped: 2026-07-06
target_scene_file: scenes/central_limit.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Standardize a large iid sum, and every finite-variance distribution flows to the standard normal."
  recap: "Last video: the empirical average settles onto the mean. Now zoom in on the fluctuations."
  key_idea: "A large sum forgets its distribution: standardized, it flows to the standard normal."
  bridge: null            # series finale -- no forward tease; the outro closes the arc

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova ~0.31 s/word; gTTS drafts ~0.44 -- target budgets the FINAL
target_runtime_sec: 310
tolerance_sec: 45         # check_status fails rendered+ chapters outside this

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / wpm (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 380
measured_runtime_sec: 342.8

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 121
    est_sec: 48
    measured_sec: 46.7
    sync_points: [zoom, theorem, intuition, payoff]
  - id: clt-statement
    scene_class: CLTStatement
    narration_words: 194
    est_sec: 78
    measured_sec: 70.3
    sync_points: [standardize, theorem, astonish, skew, limit]
  - id: gaussian-exact
    scene_class: GaussianExact
    narration_words: 165
    est_sec: 66
    measured_sec: 61.4
    sync_points: [sum-gaussian, mean-var, invariant]
  - id: mgf-proof
    scene_class: MGFProof
    narration_words: 273
    est_sec: 109
    measured_sec: 94.6
    sync_points: [assume, lambda, three, products, lhopital, parabola, normal-mgf]
  - id: normal-approximation
    scene_class: NormalApproximation
    narration_words: 206
    est_sec: 82
    measured_sec: 69.8
    sync_points: [setup, standardize, phi, example, area, outro, flows, close]
---

# Video Script — The Central Limit Theorem

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring marker: the generated scene splits the narration into *sequential*
voiceover blocks at each marker (bookmark-free timing; no Whisper).

Series finale: there is no bridge and no "coming up" line. The outro is the
key-idea card plus a closing line that lands the whole course. The single
permitted "bell curve" (the classic name is the point of this video) is spent
there, deliberately, and nowhere else.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, the law of large numbers: divide a sum of independent,
> identically distributed variables by n, and the empirical average settles
> onto the mean. The fluctuations vanish. <bookmark mark="zoom"/> This video
> zooms in. Divide by the square root of n
> instead, and the fluctuations do not vanish — they stabilize into a definite
> shape. <bookmark mark="theorem"/> First, the central limit theorem: what
> that shape is, and why the starting distribution does not matter.
> <bookmark mark="intuition"/> Then the intuition, built through the
> moment-generating function, where sums become products.
> <bookmark mark="payoff"/> And finally the payoff: the normal
> approximation, which estimates any large sum with a single table. When we
> first met the Gaussian, we promised that many small independent effects
> would explain it. This is where the promise is kept.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 12  ·  Limit Theorems"
  (per the vendored `\chapter[Limit Theorems]{...}` line), objective; card
  rises to the top edge; progress_tag(3, 3) in the DR corner.
- `zoom`: `self.wait(0.5)` after the card docks, then nothing new — the
  spoken pivot carries it.
- `theorem`: outline line "1.  The theorem" fades in.
- `intuition`: outline line "2.  The intuition: sums become products" fades
  in (2026-07-05 draft review round 2, honest framing: the video builds the
  intuition, it does not prove the CLT — the key MGF-convergence step is
  quoted without proof).
- `payoff`: outline line "3.  The normal approximation" fades in; the
  promise sentence plays over the finished outline.

---

## Beat: clt-statement  (scene: CLTStatement)

> Here is the statement. Take independent, identically distributed random
> variables with mean E of X and variance sigma squared, and form the sum
> S n. <bookmark mark="standardize"/> Center the sum by subtracting n times
> the mean, and scale it by sigma times the square root of n. This
> standardized sum has mean zero and variance one, for every n. The
> centering removes the drift; the root n scaling holds the spread steady.
> <bookmark mark="theorem"/> The central limit theorem says: as n grows, the
> probability that the standardized sum lands at or below any x converges to
> the integral of the standard Gaussian density up to x. The standardized
> sum converges in distribution — the very notion we defined for CDFs — to a
> standard normal random variable. <bookmark mark="astonish"/> Now hear what
> the theorem does not ask. It does not ask where you start. Begin with a
> flat distribution, <bookmark mark="skew"/> or a lopsided one,
> <bookmark mark="limit"/> standardize the sum, and the limit is the same
> standard normal, every time. Only the mean and the variance survive; every
> other detail of the starting distribution is forgotten in the limit. That
> is why the Gaussian is everywhere: it is the shape large sums cannot
> avoid.

**Cues** (formula column first, then it docks right and the chart lands left,
riding high with its caption lane centered beneath it)
- open: section title "The Central Limit Theorem"; setup line
  `S_n = X_1 + \cdots + X_n` with mean/variance conditions at BODY size.
- `standardize`: the standardized sum `\frac{S_n - n E[X]}{\sigma\sqrt{n}}`
  written in accent.
- `theorem`: the limit statement on two lines, the continuation line
  ("=", rhs) CENTERED under the first line as a balanced two-line group
  (2026-07-05 draft review, 1:35; the same balanced form carries into the
  docked right column later in the beat):
  `\lim_n \Pr(\ldots \le x)` / `= \int_{-\infty}^x \frac{1}{\sqrt{2\pi}}
  e^{-u^2/2} du`.
- `astonish`: formulas dock to the right column, ending the beat centered
  on the halfway anchor (`zone_center_y`); the density chart + caption land
  left as one block, also centered on the anchor (2026-07-05 draft review,
  2:00): a flat uniform density with DASHED vertical lines at the support's
  edges and zero-level segments on the x-axis outside the support (the
  function is visibly zero out of bounds), caption "start anywhere"
  centered on the chart (match_x).
- `skew`: the flat density transforms into a lopsided one.
- `limit`: the density transforms into the standard normal curve, stroke to
  accent; caption becomes "the same limit, every time".

---

## Beat: gaussian-exact  (scene: GaussianExact)

> One case we can check completely. Suppose every X i is itself Gaussian,
> with mean m and variance sigma squared, drawn fresh and independent every
> time. No limits yet — just bookkeeping we already own.
> <bookmark mark="sum-gaussian"/>
> When we convolved densities, we learned that sums of independent Gaussians
> stay Gaussian — so S n minus n m, over the square root of n, is Gaussian
> for every n. <bookmark mark="mean-var"/> Compute its mean: the centering
> makes it zero. Compute its variance: the n independent variances add to n
> sigma squared, and dividing by root n divides the variance by n. What
> remains is sigma squared, with no n anywhere in sight.
> <bookmark mark="invariant"/> So for Gaussian inputs the scaled sum does
> not merely converge — it is the same distribution at every single n. The
> curve never moves. This is the invariant sequence we met when we defined
> convergence in distribution, and the central limit theorem is the claim
> that every finite-variance input flows to the shape the Gaussian already
> occupies.

**Cues** (left chart rides high; derivation column right; the n-label at
BODY size — parameter labels never shrink to CAPTION)
- open: section title "The Gaussian Case Is Exact"; setup line: each `X_i`
  Gaussian with `E[X_i] = m`, `Var(X_i) = \sigma^2` at BODY; the Gaussian
  density chart appears at the BOTTOM CENTER while the destination shape is
  discussed (2026-07-05 draft review, 2:30-2:55) — no n-tag yet.
- `sum-gaussian`: `\frac{S_n - nm}{\sqrt{n}}` labelled "Gaussian for every
  n" (BODY); the bottom-center Gaussian stays on screen.
- `mean-var`: the chart SLIDES LEFT to the invariant placement (the same
  position it holds at `invariant`), still without the n-tag; the mean and
  variance derivations land in the right column as ONE LINE each (the
  vertical space reclaimed), the block ending the frame centered on the
  halfway anchor (2026-07-05 draft review, 2:58): mean line ending 0,
  variance line ending `\sigma^2`.
- `invariant`: the left chart (already in place): a BODY-size label
  stepping n = 1, 2, 8, 32 while the curve holds still (Indicate on the
  last step); caption "the curve never moves" centered on the chart.

---

## Beat: mgf-proof  (scene: MGFProof)

> How do you build the intuition that every distribution flows to the same
> limit? Not through the density — through the transform.
> <bookmark mark="assume"/>
> Assume the mean is zero and the variance is one; proper scaling recovers
> the general case. Assume too that the moment-generating function of X
> exists and is finite. <bookmark mark="lambda"/> Our tool is its logarithm:
> capital Lambda of s, the log of the expectation of e to the s X.
> <bookmark mark="three"/> Three numbers pin this curve near the origin. At
> zero, Lambda is the log of one: zero. Its first derivative at zero is the
> mean: zero. Its second derivative at zero is the second moment: one.
> Near the origin, Lambda hugs the parabola s squared over
> two, and that is the whole secret. <bookmark mark="products"/> Now bring in the sum. Independence means the
> expectation of a product factors — the generating-function move we have
> used twice before. The log-MGF of S n over root n collapses into n
> identical factors: n times Lambda of s over root n. One function of one
> variable controls the entire sum. <bookmark mark="lhopital"/> What happens
> as n grows? Write it as Lambda over one over n, and apply L'Hopital's rule
> — twice. Each pass peels one derivative off Lambda, until the second
> derivative at zero, which is one, stands exposed. The limit is s squared
> over two. <bookmark mark="parabola"/> Watch it happen: as n grows, the
> curves settle onto the parabola. <bookmark mark="normal-mgf"/> So the MGF
> of the scaled sum converges pointwise to e to the s squared over two —
> precisely the moment-generating function of a standard normal. That
> pointwise convergence of MGFs forces convergence in distribution: a
> sophisticated result we state without proof.

**Cues** (multi-topic beat: SEQUENTIAL section titles — "The Log-MGF", then
"Sums Become Products", then "The Limit Is the Gaussian's"; none of the
on-screen titles claims a proof, and the narration says "build the
intuition" — 2026-07-05 draft review round 2, honest framing. The one kept
"without proof" is the accurate "a sophisticated result we state without
proof." The beat id `mgf-proof` and class `MGFProof` are frozen names.)
- open: section title "The Log-MGF".
- `assume`: assumption labels at BODY: `E[X] = 0, Var(X) = 1` and
  "M_X exists and is finite".
- `lambda`: `\Lambda_X(s) = \log M_X(s) = \log E[e^{sX}]` in accent.
- `three`: the three values, one line each:
  `\Lambda_X(0) = 0`, `\Lambda_X'(0) = E[X] = 0`,
  `\Lambda_X''(0) = E[X^2] = 1`; then the label "Near the origin:" followed
  by `\Lambda_X(s) \approx s^2/2` in ACCENT, at the same BODY size and
  spacing as the `\Lambda_X(s) = ...` line above the three conditions
  (2026-07-05 draft review, 4:26).
- `products`: title swaps to "Sums Become Products"; the chain on two
  lines, "=" x-aligned:
  `\log E[e^{s S_n/\sqrt{n}}] = \log(M_X(s/\sqrt{n}) \cdots M_X(s/\sqrt{n}))`
  / `= n \Lambda_X(s n^{-1/2})` (accent lands on the last).
- `lhopital`: title swaps to "The Limit Is the Gaussian's"; the cascade on
  TWO LINES, the second line (carrying the `s^2/2` term) centered under the
  first (2026-07-05 draft review, 5:00):
  `\lim \Lambda_X(s n^{-1/2}) / n^{-1} = (s/2) \lim \Lambda_X'(s n^{-1/2})
  / n^{-1/2}` /
  `= (s^2/2) \lim \Lambda_X''(s n^{-1/2}) = s^2/2`.
- `parabola`: left chart + caption moved as ONE BLOCK to the halfway anchor
  (`zone_center_y`; 2026-07-05 draft review, 5:19): the parabola `s^2/2` in
  accent with the curves `n \Lambda_X(s n^{-1/2})` for a fair ±1 coin
  (`\Lambda = \log\cosh`) at n = 1, 4, 16 in muted ink settling onto it;
  hardcoded functions, no randomness; caption centered on the chart.
- `normal-mgf`: `M_{S_n/\sqrt{n}}(s) \to e^{s^2/2}` in accent; muted
  caption "pointwise MGF convergence implies convergence in distribution"
  (the ": quoted without proof" tail removed — 2026-07-05 draft review,
  5:39).

---

## Beat: normal-approximation  (scene: NormalApproximation)

> The theorem earns its keep as a calculator. <bookmark mark="setup"/> Take
> any large iid sum — n is large, and the mean and variance are known.
> <bookmark mark="standardize"/> The CDF of S n at x is the probability that
> S n is at most x. Standardize both sides of the inequality, and the left
> side is, by the theorem, approximately a standard normal.
> <bookmark mark="phi"/> So the CDF of the sum is approximately capital Phi,
> the standard normal CDF, evaluated at x minus n times the mean, over sigma
> root n. One table of Phi serves every large sum with finite variance.
> <bookmark mark="example"/> A concrete run. A transmitter sends one hundred
> bits, each equally likely to be zero or one, independently. What is the
> probability that at most fifty-five are ones? The mean count is fifty;
> sigma root n is five. Standardize: fifty-five minus fifty, over five, is
> one. <bookmark mark="area"/> The answer is approximately Phi of one — the
> area under the standard Gaussian density up to one — about zero point
> eight four. <bookmark mark="outro"/> The key idea of this video: a large
> sum, scaled by one over root n, forgets its distribution.
> <bookmark mark="flows"/> Standardized, it flows to the standard normal.
> <bookmark mark="close"/> We opened with sets; we close with the bell
> curve. Probability, end to end.

**Cues**
- open: section title "The Normal Approximation".
- `setup`: `S_n = X_1 + \cdots + X_n`, mean/variance conditions at BODY.
- `standardize`: the chain on aligned lines:
  `F_{S_n}(x) = \Pr(S_n \le x)` /
  `= \Pr((S_n - nE[X])/(\sigma\sqrt{n}) \le (x - nE[X])/(\sigma\sqrt{n}))`.
- `phi`: continuation line `\approx \Phi((x - nE[X])/(\sigma\sqrt{n}))` in
  accent, aligned with the chain.
- `example`: the chain docks; worked numbers in the right column: n = 100,
  `nE[X] = 50`, `\sigma\sqrt{n} = 5`,
  `\Pr(S_{100} \le 55) \approx \Phi(1) \approx 0.84`.
- `area`: left chart: the standard normal density with the region up to
  u = 1 SHADED (fill opacity ~0.3, mark_intended_overlap) exactly as the
  narration says "area"; caption "the shaded area up to one: about 0.84"
  centered on the chart ("one" spelled out in the prose caption). The
  figure AND its caption move as ONE BLOCK whose center sits on the
  halfway anchor (`zone_center_y`), level with the docked right column
  (2026-07-05 draft review round 2, 6:43).
- `outro`: stage clears; the landing sentence gets its OWN voiceover moment
  and stands ALONE at center in ACCENT (2026-07-05 draft review round 2,
  ending: the closing message must land): the MathTex line
  "A large sum, scaled by $1/\sqrt{n}$, forgets its distribution."
  (the scaling typeset, never prose).
- `flows`: the landing line demotes to INK and takes its place as the key
  card's first line; "Key idea" kicker fades in above it in accent (the
  single ACCENT hands off); the second INK line writes: "Standardized, it
  flows to the standard normal." Spoken words = card words.
- `close`: the closing lines in muted ink ("We opened with sets; we close
  with the bell curve." / "Probability, end to end.") — the series-finale
  close, no next_title.

---

## Cut list (if over budget)

1. Drop the `parabola` chart phrase in mgf-proof ("Watch it happen ...")
   and its chart — the cascade already lands the limit (saves ~12 words +
   the chart time).
2. Compress the L'Hopital cascade to its first and last lines; speak the
   two-rule cascade, don't write the middle line (saves ~10 s of Writes).
3. Trim the closing sentence of gaussian-exact ("This is the invariant
   sequence ... already occupies.") to "The theorem claims every
   finite-variance input flows to this same shape." (saves ~20 words).
4. In clt-statement, cut the final sentence ("That is why the Gaussian is
   everywhere ...") — the overview already made the promise point.
