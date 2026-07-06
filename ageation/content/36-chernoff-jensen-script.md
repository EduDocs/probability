---
slug: 36-chernoff-jensen
title: The Chernoff Bound and Jensen's Inequality
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 36-chernoff-jensen.md
derived_from_sha256: cc798ad32dddcaf3c7bd4a039b069729065e6703d94007be25730d0bb59dd95f
provenance_stamped: 2026-07-06
target_scene_file: scenes/chernoff_jensen.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Spend the whole MGF on a tail bound, then let a function's own convexity bound an expectation."
  recap: "Last video: Markov and Chebyshev bounded tails with one and two moments."
  key_idea: "Expectation is a bounding tool: one moment, two moments, the whole MGF - or nothing but curvature."
  bridge: "Coming up: Joint Continuous Distributions"

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 300
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / 2.6 (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 360
measured_runtime_sec: 330.9

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 88
    est_sec: 34
    measured_sec: 34.7
    sync_points: [construct, optimize, convex, jensen]
  - id: chernoff-construction
    scene_class: ChernoffConstruction
    narration_words: 212
    est_sec: 82
    measured_sec: 69.9
    sync_points: [indicator, dominate, infimum, bound, mgf]
  - id: chernoff-optimize
    scene_class: ChernoffOptimize
    narration_words: 210
    est_sec: 81
    measured_sec: 73.3
    sync_points: [fan, dial, chernoff, ledger]
  - id: convexity-tangent
    scene_class: ConvexityTangent
    narration_words: 171
    est_sec: 66
    measured_sec: 62.3
    sync_points: [convex, tangent, ftc, monotone, result]
  - id: jensen
    scene_class: JensenInequality
    narration_words: 251
    est_sec: 97
    measured_sec: 90.8
    sync_points: [pointwise, anchor, average, linear, dies, jensen, callback, outro]
---

# Video Script — The Chernoff Bound and Jensen's Inequality

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene. This video closes book
chapter 10 (Expectations and Bounds); the log-MGF/Legendre aside from the
concept map is cut per its own "cut first" note (see Cut list).

---

## Beat: overview  (scene: ChapterOverview)

> Last video, Markov and Chebyshev bounded a tail using one moment, then
> two. This video spends everything. <bookmark mark="construct"/> First we
> run the Chebyshev template with an exponential dominating function, and
> the moment generating function we just built turns into a tail bound.
> <bookmark mark="optimize"/> Then we notice we hold a whole family of
> bounds, one for every rate, and optimize to reach the celebrated Chernoff
> bound. <bookmark mark="convex"/> Next, a change of key: convex functions
> sit above their tangent lines, <bookmark mark="jensen"/> and that single
> picture proves Jensen's inequality, the reason averages and curved
> functions never commute.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 10  ·  Expectations and
  Bounds", title, objective; progress_tag(3, 3) in the DR corner; card
  rises to the top edge.
- `construct`: outline line "1. The exponential dominator" fades in.
  (2026-07-04 register pass: narration callback re-anchored on the MGF
  topic, not a video number.)
- `optimize`: outline line "2. The Chernoff bound" fades in.
- `convex`: outline line "3. Convexity and tangent lines" fades in.
- `jensen`: outline line "4. Jensen's inequality" fades in.

---

## Beat: chernoff-construction  (scene: ChernoffConstruction)

> We want the right tail: the probability that X is at least a. The last
> video taught the recipe: write the probability as the expectation
> of an indicator, then dominate that indicator by a function whose
> expectation you can compute. <bookmark mark="indicator"/> Here is the
> indicator of the interval from a to infinity: zero on the left, then a
> step up to one at a. <bookmark mark="dominate"/> This time, dominate it
> with an exponential: e to the s times x minus a, for some positive rate
> s. At x equals a the curve passes through one exactly, and it only grows
> from there, so it sits above the step everywhere.
> <bookmark mark="infimum"/> In the language of the Chebyshev inequality,
> the function h of x is e to the s x, the set S is the interval from a to
> infinity, and the infimum of h over S is e to the s a.
> <bookmark mark="bound"/> Divide through, and the tail is at most e to
> the minus s a times the expectation of e to the s X.
> <bookmark mark="mgf"/> Look closely at that last factor. It is the
> moment generating function of X, evaluated at s, the function we built
> and told you to keep in your pocket. Markov spent one moment.
> Chebyshev spent two. This construction spends the entire catalog at
> once.

**Cues** (two-column: indicator/dominator chart left, derivation right)
- opening block: section title "The Exponential Dominator" docks up; the
  goal `\Pr(X \geq a) \leq \, ?` appears upper right. (2026-07-04 register
  pass: "Video thirty-five" became "The last video" — it is the immediate
  predecessor.)
- `indicator`: axes grow at the left; the step function
  `\mathbf{1}_{[a,\infty)}(x)` drawn with its dotted riser at a; the label
  sits over the flat zero stretch, clear of the curve fan.
- `dominate`: the exponential `e^{s(x-a)}` sweeps in above the step,
  pinned to the point (a, 1); a dot marks the pin.
- `infimum`: right column, line by line: `h(x) = e^{sx}`,
  `S = [a, \infty)`, `i_S = \inf_{x \geq a} e^{sx} = e^{sa}`.
- `bound`: `\Pr(X \geq a) \leq e^{-sa}\, \mathrm{E}[e^{sX}]` written, in
  accent.
- `mgf`: the expectation factor transforms into `e^{-sa} M_X(s)`; the
  `M_X(s)` part carries the accent; previous accent demotes to ink.
  (2026-07-04 register pass: pocket callback re-anchored on "the function
  we built", not a video number.)

---

## Beat: chernoff-optimize  (scene: ChernoffOptimize)

> Nothing forced our choice of rate. <bookmark mark="fan"/> Every positive
> s gives an exponential pinned to the point a comma one, and every one of
> them dominates the step: a shallow curve for small s, a steeper one
> hugging the corner as s grows. Each member of the family certifies its
> own bound, e to the minus s a times M X of s. <bookmark mark="dial"/> So
> we hold not one bound but a dial's worth, and you have rehearsed this
> move: for the Cantelli inequality we tuned a quadratic's offset and kept
> the minimum. Same move, sharper weapon. As s varies, the bound value
> traces a curve, and we slide down to its lowest point.
> <bookmark mark="chernoff"/> Taking the best member of the family gives
> the Chernoff bound: the probability that X is at least a is at most the
> infimum, over positive s, of e to the minus s a times M X of s. Which
> rate wins depends on the distribution of X and on a, and that is why the
> bound carries the search inside it. <bookmark mark="ledger"/> Read the
> chapter's ledger. Markov paid one moment, Chebyshev paid a second, and
> Chernoff pays the whole moment generating function, which is why it
> earns exponentially sharp tails and a central role in coding and
> communications.

**Cues** (one chart at a time: fan first, then the bound-vs-s dial, then
the ledger)
- opening block: section title "The Chernoff Bound" docks up.
- `fan`: the beat-2 axes return with the step; exponentials for
  increasing s appear one after another, each pinned at (a, 1) — the
  family label `e^{s(x-a)},\ s > 0` beside the fan; per-curve bound line
  `\Pr(X \geq a) \leq e^{-sa} M_X(s)` beneath.
- `dial`: the fan clears; a new small chart plots the bound value against
  s (generic dip shape); a marker dot slides along the curve to the
  minimum — the Cantelli-dial animation, reprised deliberately.
- `chernoff`: the chart clears;
  `\Pr(X \geq a) \leq \inf_{s>0} e^{-sa} M_X(s)` lands centered, in
  accent — the video's headline formula.
- `ledger`: three-row ledger builds beneath: Markov / `\mathrm{E}[X]`,
  Chebyshev / `\mathrm{E}[X^2]`, Chernoff / `M_X(s)` — "what you pay."

---

## Beat: convexity-tangent  (scene: ConvexityTangent)

> For the chapter's last inequality, change key entirely. No dominating
> functions this time; the bound flows from the shape of a single
> function. <bookmark mark="convex"/> Call g convex when its second
> derivative is nonnegative everywhere, so the curve bends upward, like a
> parabola or an exponential. <bookmark mark="tangent"/> Draw a tangent
> line anywhere on such a curve and watch: the curve never dips below it.
> Slide the anchor point along, and the picture holds everywhere. That is
> the claim to prove. <bookmark mark="ftc"/> The fundamental theorem of
> calculus writes g of x as g of a plus the integral of the derivative
> from a up to x. <bookmark mark="monotone"/> A nonnegative second
> derivative makes the first derivative monotone increasing, so replacing
> the derivative inside the integral by its value at a can only shrink the
> result. <bookmark mark="result"/> What remains is the equation of a
> line: g of x is at least g of a plus x minus a times the slope at a. A
> convex curve lies above every one of its tangent lines, an inequality
> manufactured from curvature alone.

**Cues** (two-column: convex curve left, derivation right)
- opening block: section title "Convexity and Tangent Lines" docks up.
- `convex`: axes with a convex bowl g(x) at the left;
  `\frac{d^2 g}{dx^2}(x) \geq 0` at the right.
- `tangent`: a tangent line with its anchor dot appears on the curve and
  sweeps along it (ValueTracker), the curve never dipping below.
- `ftc`: right column: `g(x) = g(a) + \int_a^x \frac{dg}{dx}(u)\, du`.
- `monotone`: beneath it: `\geq g(a) + \int_a^x \frac{dg}{dx}(a)\, du`.
- `result`: `g(x) \geq g(a) + (x - a) \frac{dg}{dx}(a)` in accent; the
  earlier lines demote to muted.

---

## Beat: jensen  (scene: JensenInequality)

> Now let a random variable ride the tangent. <bookmark mark="pointwise"/>
> The tangent bound holds at every point x, so it holds with X plugged in:
> g of X is at least g of a plus X minus a times the slope at a. That is
> an inequality between random variables, true outcome by outcome.
> <bookmark mark="anchor"/> We may pick the anchor, so pick the one point
> the whole chapter keeps returning to: anchor the tangent at the mean, a
> equals the expected value of X. <bookmark mark="average"/> Take
> expectations on both sides. <bookmark mark="linear"/> Expectation is
> linear, so the slope term carries the expected value of X minus the
> expected value of X, and that difference is exactly zero.
> <bookmark mark="dies"/> The linear term dies on the spot.
> <bookmark mark="jensen"/> What survives is Jensen's inequality: for
> convex g, the expectation of g of X is at least g of the expectation of
> X, provided both expectations exist. Averages and curved functions do
> not commute, and convexity tells you which way the inequality tips.
> <bookmark mark="callback"/> You met an instance long ago. Take g of x
> equals x squared: Jensen says the second moment is at least the square
> of the mean, which is precisely the fact that variance is nonnegative.
> The inequality holds even for convex functions with corners, though that
> proof is much harder; the smooth case is the honest one at this level.
> <bookmark mark="outro"/> The key idea of this chapter: expectation is a
> bounding tool. One moment gave Markov, two gave Chebyshev, the whole
> generating function gave Chernoff, and Jensen needs nothing but
> curvature.

**Cues** (formula-driven; Jensen's collapse animated literally)
- opening block: section title "Jensen's Inequality" docks up.
- `pointwise`: `g(X) \geq g(a) + (X - a) \frac{dg}{dx}(a)` written.
- `anchor`: `a = \mathrm{E}[X]` in accent beneath it.
- `average`: the averaged line
  `\mathrm{E}[g(X)] \geq g(\mathrm{E}[X]) + (\mathrm{E}[X] -
  \mathrm{E}[X]) \frac{dg}{dx}(\mathrm{E}[X])` written.
- `linear`: the zero difference takes the accent and HOLDS it through
  the sentence (2026-07-05 draft review, 5:27).
- `dies`: the slope term fades slowly (run_time 2.2), landing exactly on
  "dies on the spot".
- `jensen`: `\mathrm{E}[g(X)] \geq g(\mathrm{E}[X])` boxed, in accent —
  the chapter's final card; caption "for convex g" muted.
- `callback`: `\mathrm{E}[X^2] \geq (\mathrm{E}[X])^2` with the caption
  "g(x) = x squared: variance is nonnegative" — the video 19 callback.
- `outro`: stage clears; shared outro card — "Key idea" + takeaway +
  "Coming up:  Joint Continuous Distributions".

---

## Cut list (if over budget)

1. Already cut: the log-MGF / Legendre-transform aside (concept
   `log-mgf-legendre`, marked optional / cut-first) — a rebranding, not a
   new bound; saves a full beat.
2. Drop the `ledger` segment of chernoff-optimize (keep the spoken close
   one sentence long); saves ~36 words / ~11 s.
3. Compress the `callback` segment of jensen to its first sentence and
   the formula; saves ~35 words / ~11 s.
4. Trim `dial`'s Cantelli reminiscence to "we optimized Cantelli the same
   way"; saves ~20 words / ~6 s.
