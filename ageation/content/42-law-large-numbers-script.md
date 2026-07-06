---
slug: 42-law-large-numbers
title: The Law of Large Numbers
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved via chat 2026-07-04
derived_from: 42-law-large-numbers.md
derived_from_sha256: 2707f990913c8e6726281a937dc32b25684cb68e52521c4afa74614d09cd6d80
provenance_stamped: 2026-07-06
target_scene_file: scenes/law_large_numbers.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Prove that empirical averages converge in probability to the mean - and see why finite variance is load-bearing."
  recap: "The types-of-convergence video: convergence in probability, in mean square, in distribution - the vocabulary this theorem is stated in."
  key_idea: "Averages of independent samples converge in probability to the mean because their variance vanishes like one over n."
  bridge: "Next: The Central Limit Theorem - the fluctuations around the mean take on a universal shape."

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
estimated_runtime_sec: 383
measured_runtime_sec: 342.7

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 123
    est_sec: 49
    measured_sec: 46.3
    sync_points: [statement, proof, die, cauchy]
  - id: lln-statement
    scene_class: LLNStatement
    narration_words: 173
    est_sec: 69
    measured_sec: 61.0
    sync_points: [iid, sum, average, theorem, reading]
  - id: chebyshev-closes
    scene_class: ChebyshevCloses
    narration_words: 214
    est_sec: 86
    measured_sec: 73.4
    sync_points: [mean, variance, shrink, ms, cheby, closes]
  - id: die-frequency
    scene_class: DieFrequency
    narration_words: 193
    est_sec: 77
    measured_sec: 65.7
    sync_points: [die, indicator, fraction, trace, moral]
  - id: cauchy-refusal
    scene_class: CauchyRefusal
    narration_words: 255
    est_sec: 102
    measured_sec: 96.3
    sync_points: [density, conv, stable, induction, wander, moral, outro]
---

# Video Script — The Law of Large Numbers

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an authoring marker: the generated scene splits the narration into *sequential* voiceover blocks at each marker (bookmark-free timing; no Whisper).

Ledger mapping: `lln-statement` -> LLNStatement; `mean-and-variance` +
`chebyshev-closes` -> ChebyshevCloses; `die-frequency` -> DieFrequency;
`cauchy-stability` (headline plus result only) + `cauchy-refusal` ->
CauchyRefusal. Cross-references are by concept, never by video number.

---

## Beat: overview  (scene: ChapterOverview)

> Averages settle. Flip enough coins, roll enough dice, and the running
> average calms down toward one number, almost as if chance were wearing
> off. Last video built the vocabulary for
> that feeling: convergence in probability, in mean square, and in
> distribution. <bookmark mark="statement"/> In this video the feeling
> becomes a theorem, the law of large numbers: the empirical average of
> independent, identically distributed random variables converges in
> probability to the mean. <bookmark mark="proof"/> The proof takes three
> short moves we have already covered, and the Chebyshev inequality
> completes the proof. <bookmark mark="die"/> Then a die makes it
> concrete: the relative frequency of a six converges to the probability of
> a six. <bookmark mark="cauchy"/> And finally a warning label: one famous
> heavy-tailed density refuses to settle at all.

**Cues** (outline lines land clause by clause, one sub-block each;
"already covered" + "completes the proof" wording per 2026-07-05 draft
review, 0:36 / 0:42)
- opening block: intro_card with kicker "Chapter 12  ·  Limit Theorems"
  (the vendored chapter prints "Sequences, Convergence and Limit
  Theorems"; the bracketed short title fits the kicker lane), title, the
  two-line objective; progress_tag(2, 3) in DR; card docks to the top.
  `self.wait(0.5)` after the card docks.
- `statement`: outline line "1.  The statement" fades in.
- `proof`: outline line "2.  A three-move proof" fades in.
- `die`: outline line "3.  Counting sixes" fades in.
- `cauchy`: outline line "4.  The average that never settles" fades in.

---

## Beat: lln-statement  (scene: LLNStatement)

> Here is the setting. <bookmark mark="iid"/> Take a sequence of
> independent, identically distributed random variables, X one, X two, and
> so on, each with mean E of X and finite variance. <bookmark mark="sum"/>
> Add the first n of them and call the total S n, the empirical sum.
> <bookmark mark="average"/> Divide by n, and you get the empirical
> average, S n over n. This is the quantity every experimenter actually
> computes: measure n times, add, divide. Signal averaging, opinion polls,
> Monte Carlo estimates: they all live here. <bookmark mark="theorem"/> The
> law of large numbers asserts that the empirical average converges in
> probability to the mean. For every positive epsilon, the probability that
> S n over n misses E of X by epsilon or more goes to zero as n grows.
> <bookmark mark="reading"/> Read the statement slowly. The average is
> still a random variable, but the probability of a noticeable deviation,
> however tight you set the bar, vanishes as the sample grows. There are
> many versions of this law; this is the simplest one, and after last video
> its proof costs almost nothing.

**Cues**
- section title "The Law of Large Numbers", written centered then docked up.
- `iid`: hypothesis line `X_1, X_2, \ldots` iid, mean E[X], finite Var, in INK.
- `sum`: `S_n = \sum_{i=1}^n X_i` written beneath.
- `average`: `S_n/n = (X_1 + \cdots + X_n)/n` in ACCENT (the object of the
  video); previous accent demotes.
- `theorem`: the theorem box: `\lim_{n\to\infty} \Pr(|S_n/n - E[X]| \ge
  \epsilon) = 0` for every `\epsilon > 0`, in ACCENT (average demotes).
- `reading`: muted caption, centered, spelled-out prose: "the chance of a
  noticeable deviation vanishes" (no symbols in the Text; caption in its
  own lane, clear of the bottom edge; "vanishes" per the 2026-07-05 draft
  review's video-wide dies-to-vanishes note).

---

## Beat: chebyshev-closes  (scene: ChebyshevCloses)

> The proof takes three moves, and we own every one of them.
> <bookmark mark="mean"/> First, the mean. Expectation is linear, so the
> expectation of S n over n is the sum of the individual means divided by
> n, and that is exactly E of X. The average is unbiased: it points at the
> right target for every sample size, and independence played no part yet.
> <bookmark mark="variance"/> Second, the spread. The variables are
> independent, so their variances add. The variance of S n over n is the
> sum of the variances divided by n squared, which collapses to Var of X
> over n. <bookmark mark="shrink"/> Watch that denominator work: quadruple
> the sample and the variance of the average drops to a quarter. More data
> buys proportionally more certainty. As n grows, the variance vanishes. <bookmark mark="ms"/> And since the expected squared
> deviation of the average from E of X is exactly this variance, vanishing
> variance already delivers convergence in mean square.
> <bookmark mark="cheby"/> Third, the finish. The Chebyshev inequality from
> the bounds video converts variance into a tail bound: the probability
> that the average misses the mean by epsilon or more is at most Var of X
> over n epsilon squared. <bookmark mark="closes"/> The right side marches
> to zero, so the trapped left side must follow. That is convergence in
> probability, and the theorem is proved.

**Cues** (side-by-side: left shrinking-variance chart rides HIGH and is
drawn slightly SMALLER (0.85 scale) so the right column has room; every
right-column equation sits on ONE LINE, distributed with `even_stack`;
captions centered on the chart with `match_x`; 2026-07-05 draft review,
3:29)
- section title "A Proof in Three Moves".
- `mean`: one-line chain `E[S_n/n] = (E[X_1] + \cdots + E[X_n])/n = E[X]`;
  chain visibly closes on `E[X]`.
- `variance`: second one-line chain: `Var(S_n/n) = (Var(X_1) + \cdots +
  Var(X_n))/n^2 = Var(X)/n`, the closing term in ACCENT.
- `shrink`: left chart appears: bars of height Var[X]/n at n = 1, 2, 4, 8,
  16 shrinking; the n label at BODY size; no tick labels under the bars
  colliding (bar positions clear of drawn ticks).
- `ms`: `E[|S_n/n - E[X]|^2] = Var(S_n/n) -> 0` — mean square convergence,
  muted caption "convergence in mean square, for free" centered on the
  chart.
- `cheby`: the one-line Chebyshev finish: `\Pr(|S_n/n - E[X]| \ge \epsilon)
  \le Var(S_n/n)/\epsilon^2 = Var(X)/(n\epsilon^2)`, closing term in ACCENT.
- `closes`: `\to 0` indicated; QED-style muted line "convergence in
  probability" beneath.

---

## Beat: die-frequency  (scene: DieFrequency)

> Now make the theorem physical. <bookmark mark="die"/> Roll a die over and
> over, and ask how often a six shows up as the number of throws becomes
> very large. <bookmark mark="indicator"/> Let D n be the number on the nth
> roll, and let X n be the indicator that D n equals six: one when the roll
> is a six, zero otherwise. Each X n is a Bernoulli random variable with
> parameter one sixth, independent across rolls and with finite variance,
> so the theorem applies. Indicators bridge events and averages: the
> expectation of an indicator is the probability of its event.
> <bookmark mark="fraction"/> The empirical average
> S n over n is then the number of sixes divided by the number of rolls:
> the relative frequency of a six. <bookmark mark="trace"/> Watch it run.
> Early on the fraction lurches around, but as rolls accumulate it hugs the
> level of one sixth, and excursions outside an epsilon band become rare.
> <bookmark mark="moral"/> By the law of large numbers, the relative
> frequency of a six converges in probability to one sixth, the probability
> of a six. The long-run-frequency reading of probability, the intuition
> this whole course has leaned on, is now a theorem inside the axioms.

**Cues** (left chart centered on the halfway anchor below the docked title
(`zone_center_y` / CONTENT_MID_Y), caption lane beneath; the right formula
column ends the beat centered on the same anchor; 2026-07-05 draft review,
5:00)
- section title "Counting Sixes".
- `die`: the house `die_face(6)` glyph appears upper left.
- `indicator`: `X_n = \mathbf{1}_{\{D_n = 6\}}` and `X_n \sim
  \text{Bernoulli}(1/6)` in the right column; the parameter label at BODY.
- `fraction`: `S_n/n = (\text{number of sixes})/n` beneath.
- `trace`: running relative-frequency trace against n — HARDCODED literal
  values (no runtime randomness) of the TRUE running relative frequency of
  sixes in a fixed 120-roll Lehmer-LCG die sequence (x <- 48271 x mod
  2^31-1, seed 15, roll = 1 + x mod 6; 20 sixes), so fluctuations damp
  honestly like 1/n — |change per step| <= 1/n, early swings, late calm
  (2026-07-05 draft review, 5:00); dashed reference line at y = 1/6 STARTS
  AT the y-axis; epsilon band shaded at the moment the narration says
  "epsilon band" (opacity ~0.3, mark_intended_overlap with the trace).
- `moral`: theorem instance `\lim \Pr(|S_n/n - 1/6| \ge \epsilon) = 0`
  in ACCENT; muted caption "relative frequency converges to probability"
  centered on the chart (`match_x`), in the caption lane.

---

## Beat: cauchy-refusal  (scene: CauchyRefusal)

> One more scene, because the fine print earns its keep. The theorem
> demanded finite variance, and a famous member of our gallery of densities
> fails that condition: the heavy-tailed Cauchy. <bookmark mark="density"/>
> Its density is gamma over pi times gamma squared plus x squared, and
> those tails decay so slowly that the Cauchy has no mean and no variance.
> <bookmark mark="conv"/> What do Cauchy sums do? The density of a sum of
> independent continuous random variables is a convolution, and contour
> integration, two simple poles and their residues, evaluates this one in
> closed form. <bookmark mark="stable"/> Here is the headline: the sum of
> two independent Cauchy random variables is Cauchy again, and the
> parameters simply add. <bookmark mark="induction"/> By induction, the
> empirical sum S n is Cauchy with parameter n gamma. Now divide by n. The
> scaling rule for derived densities compresses the picture right back, and
> S n over n is Cauchy with parameter gamma. The very same density, for
> every n. <bookmark mark="wander"/> So the running average never settles.
> After a million samples its distribution is exactly the distribution of
> one observation, and the trace keeps taking violent excursions.
> Averaging buys you nothing here.
> <bookmark mark="moral"/> Nothing is broken. With no finite second moment,
> the hypothesis of the law fails, so the conclusion is not owed. Finite
> variance was load-bearing all along. <bookmark mark="outro"/> The key
> idea of this video: averages of independent samples converge in
> probability to the mean, because their variance vanishes like one over n.
> Next, the companion masterpiece: the central limit theorem, where the
> fluctuations around the mean take on a universal shape.

**Cues** (multi-topic beat: SEQUENTIAL section titles — "Sums of Cauchy
Random Variables" Transforms to "The Average That Never Settles" at
`induction`; contour mechanics stay headline plus result per the concept's
cut order; both portions place the left figure on the halfway anchor
(`zone_center_y` / CONTENT_MID_Y) and end with the right equation block
centered on that anchor; 2026-07-05 draft review, 5:55 / 6:30)
- opening: section title "Sums of Cauchy Random Variables".
- `density`: the Cauchy density curve on left axes (one chart at a time);
  `f_X(x) = \gamma / (\pi(\gamma^2 + x^2))` at right.
- `conv`: convolution headline `f_S(x) = \int f_{X_1}(u) f_{X_2}(x-u)\,du`
  with muted tag "contour integration, two simple poles" — result quoted,
  not derived.
- `stable`: `f_S(x) = (\gamma_1 + \gamma_2) / (\pi((\gamma_1+\gamma_2)^2 +
  x^2))` in ACCENT; muted caption "Cauchy again - parameters add".
- `induction`: title Transforms to "The Average That Never Settles";
  `S_n \sim \text{Cauchy}(n\gamma)` then `S_n/n \sim \text{Cauchy}(\gamma)`
  in ACCENT — the same density for every n.
- `wander`: the never-settling running mean: HARDCODED jittering
  partial-mean sequence [1.8, 0.4, 6.1, 3.2, 2.7, -4.5, -2.1, -1.4, 5.3,
  3.9, 3.1, 2.6] traced against n; dashed zero line starting at the
  y-axis; the trace replaces the density chart (one chart at a time).
- `moral`: muted line "no finite variance, no law of large numbers"
  centered on the chart.
- `outro`: everything fades; outro_bridge with the key idea split on two
  lines + "Coming up: The Central Limit Theorem"; `self.wait(0.5)` before
  the final fade.

---

## Cut list (if over budget)

1. The `conv` + `stable` sub-blocks of `cauchy-refusal` compress to one
   spoken sentence ("sums of independent Cauchys are Cauchy - the
   parameters add") over the density picture (~-30 s).
2. Drop the `wander` trace, keep the `induction` identity and the moral
   (~-20 s).
3. Compress `die-frequency` to the settling trace with one line of
   narration (~-35 s).
