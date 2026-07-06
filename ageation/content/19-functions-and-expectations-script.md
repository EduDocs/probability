---
slug: 19-functions-and-expectations
title: Functions and Expectations
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the 480p draft for finals 2026-07-03
derived_from: 19-functions-and-expectations.md
derived_from_sha256: 7ac86c8404ea2238b1720c43c339f4aad3065ccde2c61e9c14b9a2a9077978e3
provenance_stamped: 2026-07-06
target_scene_file: scenes/functions_and_expectations.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Average any function of a random variable straight from its PMF, and meet the mean and the variance."
  recap: "Last video: the expected value E[X] -- one number summarizing a whole PMF."
  key_idea: "Average g(X) straight from the PMF -- the mean and the variance."
  bridge: "Next: moments -- the ladder E[X^n] and the two-moment shortcut for the variance."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Timing contract set at approval (2026-07-03) from the series calibration:
# nova at 1.0 measures ~0.80x the gTTS draft (chapter 18: 262.7 -> 210.8 s).
# Approved draft: 404.8 s -> expected final ~325 s.
target_runtime_sec: 325
tolerance_sec: 60

estimated_runtime_sec: 390
measured_runtime_sec: 320.2

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 100
    est_sec: 40
    measured_sec: 32.1
    sync_points: [formula, contest, summaries, algebra]
  - id: lotus
    scene_class: ExpectationOfFunction
    narration_words: 175
    est_sec: 70
    measured_sec: 53.9
    sync_points: [question, formula, subsumes, indicator]
  - id: two-ways
    scene_class: ExtremeTrio
    narration_words: 195
    est_sec: 78
    measured_sec: 69.5
    sync_points: [setup, route-one, route-two, agree]
  - id: mean
    scene_class: CenterOfMass
    narration_words: 160
    est_sec: 64
    measured_sec: 48.2
    sync_points: [particles, balance, named-means]
  - id: variance
    scene_class: VarianceDefinition
    narration_words: 165
    est_sec: 66
    measured_sec: 51.9
    sync_points: [same-mean, definition, sigma, named-variances]
  - id: affine
    scene_class: AffineRules
    narration_words: 180
    est_sec: 72
    measured_sec: 64.5
    sync_points: [shift, scale, linearity, outro]
---

# Video Script — Functions and Expectations

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video we defined the expected value: one number that summarizes a whole
> PMF. This video, that idea grows into a toolkit. <bookmark mark="formula"/>
> We'll learn to average any function of a random variable directly from its
> PMF — no derived distribution needed — <bookmark mark="contest"/> check the
> recipe on a radio contest, <bookmark mark="summaries"/> and then meet the
> two summaries that dominate all of probability: the mean, which is a center
> of mass, and the variance, which measures spread. <bookmark mark="algebra"/>
> We finish with the algebra that ties them together — what happens to both
> under shifting and scaling.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 6 · Meeting Expectations",
  recap line, objective; card rises to the top edge.
- `formula`: outline line "1. The expectation of g(X)" fades in.
- `contest`: outline line "2. Two ways to the same answer" fades in.
- `summaries`: outline line "3. The mean and the variance" fades in.
- `algebra`: outline line "4. Affine functions" fades in.

---

## Beat: lotus  (scene: ExpectationOfFunction)

> Suppose Y equals g of X, and we want its mean. <bookmark mark="question"/>
> We know one route already: build the PMF of Y from preimages, like last
> chapter, then apply the definition. That works — but there is a shortcut.
> <bookmark mark="formula"/> The expectation of g of X can be computed
> straight from the PMF of X: sum g of x times p sub X of x over the range of
> X. Evaluate g on each value, weight by the original masses, add.
> <bookmark mark="subsumes"/> Two quick checks. If g is the identity, this is
> just the mean from last video — the definition subsumes it. And if g is a
> constant c, the masses sum to one and the expectation is c itself.
> <bookmark mark="indicator"/> One more, with real content: let g be the
> indicator of a set S — one inside S, zero outside. Then the expectation of
> the indicator of X in S is exactly the probability that X lands in S.
> Probabilities are expectations. Keep that; it pays off across the course.

**Cues**
- `question`: `Y = g(X)` with the video-17 two-space picture faded in at
  left; "route one" arrow through `p_Y`.
- `formula`: `\mathrm{E}[g(X)] = \sum_{x \in X(\Omega)} g(x)\, p_X(x)` in
  accent — the "route two" arrow going direct.
- `subsumes`: `g(x) = x` and `g(x) = c` reductions, one line each.
- `indicator`: `\mathrm{E}[\mathbf{1}_S(X)] = \Pr(X \in S)`.

---

## Beat: two-ways  (scene: ExtremeTrio)

> Let's test both routes on the same problem. <bookmark mark="setup"/> A radio
> station runs a contest: one hundred cards in a drum, three drawn, each
> winner gets a thousand dollars — but each person can win only once. David
> mailed in fifty of those hundred cards. Let X be how many of the three drawn
> cards are his. Its PMF comes from counting: choose k of his fifty, and three
> minus k of the other fifty. His winnings are g of X: a thousand times the
> minimum of X and one. <bookmark mark="route-one"/> Route one, the direct
> formula: sum g of k times the mass of k over k equals zero to three. The
> zero term drops out, the rest collapse — a thousand times twenty-nine over
> thirty-three. <bookmark mark="route-two"/> Route two, through Y itself: Y is
> either zero or a thousand. The chance of zero is the chance none of the
> three cards is David's — four over thirty-three. So Y equals a thousand with
> probability twenty-nine over thirty-three. Same product.
> <bookmark mark="agree"/> Both routes, one answer: about eight hundred and
> seventy-nine dollars. That agreement is a theorem, not luck — group the
> values of X by where g sends them, and the two sums rearrange into each
> other.

**Cues**
- `setup`: card drum sketch at left; `p_X(k) = \binom{50}{k}\binom{50}{3-k} /
  \binom{100}{3}` and `g(k) = 1000\min\{k,1\}` stacked at right.
- `route-one`: the four terms appear over the PMF bars, sum to
  `1000 \cdot \tfrac{29}{33}`.
- `route-two`: the two-point PMF of Y; `p_Y(0) = 4/33` highlighted.
- `agree`: both columns' results slide together; caption "the same answer,
  provably, always."

---

## Beat: mean  (scene: CenterOfMass)

> The simplest expectation deserves a picture. <bookmark mark="particles"/>
> Take the PMF of X and build it physically: at each value x, place a
> particle whose mass is p sub X of x. Here is a Bernoulli with mass
> one-quarter at zero and three-quarters at one. <bookmark mark="balance"/>
> Ask a mechanics question: where does this system balance? The center of
> mass is the mass-weighted average of the positions — and that is, symbol
> for symbol, the formula for the mean. This system balances at
> three-quarters: the mean of the Bernoulli. The mean is where the PMF
> balances. <bookmark mark="named-means"/> The named distributions each come
> with a mean worth remembering: a geometric with parameter p balances at one
> over p, and a binomial with n trials balances at n times p — results we'll
> lean on constantly.

**Cues**
- `particles`: the book's two-ball figure recreated with `ball` glyphs on a
  rod; masses labelled 1/4 and 3/4.
- `balance`: a fulcrum slides under the rod and settles at 0.75; the
  center-of-mass formula morphs into `\mathrm{E}[X]`.
- `named-means`: two compact cards: `\mathrm{E}[X] = 1/p` (geometric),
  `\mathrm{E}[X] = np` (binomial). One chart at a time — cards, not charts.

---

## Beat: variance  (scene: VarianceDefinition)

> The mean says where a distribution sits. It says nothing about how widely
> it spreads. <bookmark mark="same-mean"/> These two PMFs balance at exactly
> the same point — but one hugs its mean and the other scatters. We need a
> second number. <bookmark mark="definition"/> Measure each value's deviation
> from the mean, square it so that left and right count alike, and take the
> expectation. That is the variance: the expected squared deviation from the
> mean. It is never negative, and it is large exactly when mass sits far from
> the balance point. <bookmark mark="sigma"/> Its square root is the standard
> deviation, sigma — the spread in the same units as X itself.
> <bookmark mark="named-variances"/> For a Bernoulli with parameter p, the
> variance works out to p times one minus p — largest at one half, where the
> outcome is most uncertain. And the Poisson is famous for this: its variance
> equals its mean; both are lambda.

**Cues**
- `same-mean`: two house charts shown in sequence (one at a time), same
  fulcrum position marked; captions "same mean," "different spread."
- `definition`: `\mathrm{Var}(X) = \mathrm{E}\left[(X - \mathrm{E}[X])^2\right]`
  in accent; squared-deviation whiskers light up on the wide chart.
- `sigma`: `\sigma = \sqrt{\mathrm{Var}(X)}`, one caption line.
- `named-variances`: compact cards: Bernoulli `p(1-p)`; Poisson "mean =
  variance = lambda".

---

## Beat: affine  (scene: AffineRules)

> Finally, the algebra. Take Y equals a X plus b — an affine function: scale
> by a, shift by b. What happens to the mean and the variance?
> <bookmark mark="shift"/> Shift first. Slide the whole PMF right by b, and
> the balance point slides with it: the mean of X plus b picks up exactly b.
> The spread doesn't change at all — shifting moves a distribution, it does
> not widen it. <bookmark mark="scale"/> Now scale by a. The balance point
> scales to a times the mean. But deviations from the mean scale by a too,
> and the variance squares them — so the variance picks up a squared. The
> mean of a X plus b is a times the mean plus b; the variance of a X plus b
> is a squared times the variance. The shift b is gone entirely.
> <bookmark mark="linearity"/> Behind the first rule is something more
> general: expectation is linear. The expectation of a sum of functions of X
> is the sum of their expectations, constants slide out — no independence, no
> fine print. <bookmark mark="outro"/> The key idea of this video: average a
> function through the PMF directly — and its two star cases, the mean and
> the variance.

**Cues** (narration ends at "the mean and the variance", mirroring the card;
the affine response and the moments tease live on screen only; 2026-07-03
draft review)
- `shift`: the PMF translates right by b (fulcrum rides along); caption
  `\mathrm{E}[X + b] = \mathrm{E}[X] + b`, spread whiskers unchanged.
- `scale`: the PMF stretches horizontally by a; whiskers stretch;
  `\mathrm{E}[aX + b] = a\,\mathrm{E}[X] + b` and
  `\mathrm{Var}(aX + b) = a^2\,\mathrm{Var}(X)` stacked in accent.
- `linearity`: `\mathrm{E}[a\,g(X) + h(X)] = a\,\mathrm{E}[g(X)] +
  \mathrm{E}[h(X)]`, one line.
- `outro`: shared outro card — key idea + "Coming up: Moments".

---

## Cut list (if over budget)

1. Compress `agree` in `two-ways` to one spoken sentence over the final
   frame (drop the rearrangement remark).
2. Drop the geometric/binomial `named-means` cards to a single spoken aside.
3. Fold `linearity` into the `scale` block's caption with one sentence.
4. Trim `sigma` to a caption with no dedicated narration.
