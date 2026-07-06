---
slug: 24-independence-rvs
title: Independent Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the script 2026-07-03
derived_from: 24-independence-rvs.md
derived_from_sha256: 5470e54dec0b0f02799c07bf5838c801abf6dc93a94bc679b138f524b4aaf5a2
provenance_stamped: 2026-07-06
target_scene_file: scenes/independence_rvs.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Independence for random variables: the joint PMF factors - and products, variances, and iid follow."
  recap: "Last video: E[Y given X] is a random variable, and the tower property averages it back to E[Y]."
  key_idea: "Independence factors the joint into its marginals; expectations of products split, and variances of sums add."
  bridge: "Next: sums of independent variables -- convolution, and a transform that turns sums into products."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~850 words -> ~265 s.
target_runtime_sec: 265
tolerance_sec: 45

estimated_runtime_sec: 340
measured_runtime_sec: 241.0

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 90
    est_sec: 36
    measured_sec: 28.6
    sync_points: [factor, products, variance-out]
  - id: factoring
    scene_class: FactoringJointPMF
    narration_words: 200
    est_sec: 80
    measured_sec: 54.4
    sync_points: [definition, outer-product, fails, cell-events]
  - id: products
    scene_class: ProductExpectation
    narration_words: 175
    est_sec: 70
    measured_sec: 48.0
    sync_points: [split-sum, dice, general]
  - id: variance
    scene_class: VarianceOfSum
    narration_words: 220
    est_sec: 88
    measured_sec: 65.6
    sync_points: [expand, cross-term, dies, contrast]
  - id: iid
    scene_class: IndependenceAndIID
    narration_words: 165
    est_sec: 66
    measured_sec: 44.4
    sync_points: [event-version, iid-cards, outro]
---

# Video Script — Independent Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Two videos ago we saw that margins never determine a joint table — except
> in one special case, and it is the most important special case in
> probability. <bookmark mark="factor"/> In this video we define
> independence for random variables — the joint PMF factoring into its
> marginals — <bookmark mark="products"/> watch expectations of products
> split cleanly in two, <bookmark mark="variance-out"/> and collect the
> payoff that powers the rest of this course: for independent variables,
> the variance of a sum is the sum of the variances.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 7 · Multiple Random
  Variables", recap line, objective; card rises to the top edge.
- `factor`: outline line "1. The joint PMF factors" fades in.
- `products`: outline line "2. Products of expectations" fades in.
- `variance-out`: outline line "3. Variances add" fades in.

---

## Beat: factoring  (scene: FactoringJointPMF)

> Random variables X and Y are independent when the joint mass at every
> pair is the product of the marginal masses. <bookmark mark="definition"/>
> One equation, checked at every cell of the table: joint equals marginal
> times marginal. <bookmark mark="outer-product"/> We have already met an
> independent pair without naming it. Draw two balls with replacement, and
> the all-ninths table is exactly one third times one third in every cell —
> sweep the margins across the table and they rebuild it perfectly.
> <bookmark mark="fails"/> The
> without-replacement table fails immediately: a product of positive margins
> can never manufacture the zeros on its diagonal.
> <bookmark mark="cell-events"/> And the connection to chapter four is
> exact: X and Y are independent precisely when the events "X equals x" and
> "Y equals y" are independent for every single pair. Independence of
> variables is independence of events, enforced across the whole table at
> once.

**Cues**
- `definition`: `p_{X,Y}(x, y) = p_X(x)\, p_Y(y)` in accent, alone.
- `outer-product`: the with-replacement table with its one-third margins;
  a row third and a column third converge onto a cell and rebuild its
  one-ninth visually, then the sweep tints every cell (2026-07-04 draft
  review, 1:00 + "better visual" note — factorization shown on the table
  that genuinely factors).
- `fails`: only now does the without-replacement table appear (Transform),
  diagonal zeros highlighted — "no product does this." Split from
  `outer-product` so the second table lands exactly with its narration
  (2026-07-04 draft review, 1:00).
- `cell-events`: the table returns to the with-replacement (independent)
  one and rises clear of the caption card (2026-07-04 draft review, 1:21 +
  "better visual" note); caption card: `\{X = x\}` and `\{Y = y\}`
  independent for every pair — card keeps only the formula, the
  "chapter 4's ..." label line is deleted (2026-07-04 draft review, 1:21).

---

## Beat: products  (scene: ProductExpectation)

> Factored joints make expectations easy. <bookmark mark="split-sum"/> Take
> the expectation of the product X times Y: a double sum against the joint.
> Substitute the factorization, and the double sum separates — x terms with
> the marginal of X, y terms with the marginal of Y. The expectation of a
> product of independent variables is the product of the expectations.
> <bookmark mark="dice"/> Roll the two dice again: each has mean three and a
> half, the rolls are independent, so the expected product is three and a
> half squared — twelve and a quarter. No table required.
> <bookmark mark="general"/> And nothing was special about the identity
> function: for independent X and Y, the expectation of g of X times h of Y
> splits the same way, for any functions g and h. Keep that one — it does
> quiet work everywhere.

**Cues**
- `split-sum`: `\mathrm{E}[XY] = \sum_x \sum_y xy\, p_X(x) p_Y(y)`
  separating into `\left(\sum_x x\, p_X(x)\right)\left(\sum_y y\,
  p_Y(y)\right)`; result `\mathrm{E}[XY] = \mathrm{E}[X]\,\mathrm{E}[Y]` in
  accent.
- `dice`: two die_face glyphs; card `\mathrm{E}[XY] = 3.5 \times 3.5 =
  12.25`.
- `general`: `\mathrm{E}[g(X)\, h(Y)] = \mathrm{E}[g(X)]\,
  \mathrm{E}[h(Y)]`, CAPTION note "any g, h."

---

## Beat: variance  (scene: VarianceOfSum)

> Now the identity this chapter has been building toward. Means of sums
> always add — that was linearity, no assumptions asked. What about
> variances? <bookmark mark="expand"/> Expand the variance of X plus Y
> around its mean, and the square produces three pieces: the variance of X,
> the variance of Y, and twice a cross term — the expectation of the two
> deviations multiplied together. <bookmark mark="cross-term"/> That cross
> term measures how the variables move together; it will later earn the
> name covariance. <bookmark mark="dies"/> But let X and Y be independent.
> The cross term becomes an expectation of a product of independent quantities —
> so it factors, by the rule we just proved. And each factor is a deviation
> from its own mean, whose expectation is zero. Zero times zero: the cross
> term vanishes. For independent random variables, the variance of the sum is
> the sum of the variances. <bookmark mark="contrast"/> Hold the contrast:
> means add always; variances add under independence. That asymmetry is why
> independent noise averages out — and it is the engine inside every limit
> theorem still to come.

**Cues**
- `expand`: `\mathrm{Var}(X + Y)` expanding into
  `\mathrm{Var}(X) + \mathrm{Var}(Y) + 2\,\mathrm{E}[(X - \mathrm{E}[X])
  (Y - \mathrm{E}[Y])]` — TransformMatchingTex-style build, cross term
  last.
- `cross-term`: the cross term alone in accent; caption "how they move
  together."
- `dies`: an accent line "under independence" precedes the zero equation,
  and the beat's stack is re-spaced evenly down the frame (2026-07-04 draft
  review, 3:45); the cross term factoring into
  `\mathrm{E}[X - \mathrm{E}[X]]\,\mathrm{E}[Y - \mathrm{E}[Y]]`, each
  factor collapsing to 0; the surviving identity
  `\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y)` in accent (the
  "under independence" line reverts to muted as the identity takes the
  accent).
- `contrast`: two-line card — "means: always add" (INK) / "variances: add
  when independent" (accent).

---

## Beat: iid  (scene: IndependenceAndIID)

> Two small pieces complete the picture. <bookmark mark="event-version"/> A
> random variable can be independent of an event: conditioning on S then
> changes nothing — the sliced PMF equals the marginal, every bar
> untouched. <bookmark mark="iid-cards"/> And the workhorse configuration of
> all of probability: draws that are independent and identically distributed
> — iid. One PMF, copied across n draws, with the joint factoring into n
> identical terms. Every sample, every repeated experiment, many data set
> we model from here on starts with those three letters.
> <bookmark mark="outro"/> The key idea of this video: independence factors
> the joint into its marginals — so products of expectations split, and
> variances of sums add.

**Cues**
- `event-version`: video 22's slice animation replayed on a factorable
  table — the lifted row matches the marginal exactly; caption
  `p_{X \mid S} = p_X`; the boxed card sits a touch lower, clear of its
  "conditioning ..." caption line (2026-07-04 draft review, 4:06).
- `iid-cards`: a row of four identical mini PMF cards, raised a touch for
  vertical balance (2026-07-04 draft review, 4:21);
  `p_{\mathbf{X}}(\mathbf{x}) = \prod_k p_X(x_k)` beneath.
- `outro`: shared outro card — key idea + "Coming up: Sums and Many
  Variables".

---

## Cut list (if over budget)

1. Compress `event-version` to a caption with one spoken sentence.
2. Drop the `general` block's narration to an aside over the formula.
3. Trim the closing flourish of `variance` ("engine inside every limit
   theorem").
