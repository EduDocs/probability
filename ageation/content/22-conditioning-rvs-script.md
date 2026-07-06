---
slug: 22-conditioning-rvs
title: Conditioning Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the script 2026-07-03
derived_from: 22-conditioning-rvs.md
derived_from_sha256: 5bbdb34dfa0b644b08d8480d8f8826a4cf13c99bddeaba7d7f45fd72d40dcfd1
provenance_stamped: 2026-07-06
target_scene_file: scenes/conditioning_rvs.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Update a random variable's PMF by what you observe - slice the joint table and renormalize."
  recap: "Last video: the joint PMF as a table, marginals in its margins, linearity of expectation."
  key_idea: "Conditioning slices the joint table and renormalizes; run it backwards and the product rule builds joints sequentially."
  bridge: "Next: conditional expectation -- the mean of every slice, and a random variable made of means."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~940 words -> ~290 s.
target_runtime_sec: 290
tolerance_sec: 45

estimated_runtime_sec: 375
measured_runtime_sec: 268.5

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 95
    est_sec: 38
    measured_sec: 29.3
    sync_points: [events, rvs, payoff]
  - id: on-events
    scene_class: ConditionOnEvent
    narration_words: 220
    est_sec: 88
    measured_sec: 68.3
    sync_points: [ratio, valid, truncate, cutoff, survive, renormalize, rescale]
  - id: on-rvs
    scene_class: ConditionOnRV
    narration_words: 200
    est_sec: 80
    measured_sec: 58.7
    sync_points: [slice, keep, raw-masses, renorm, formula, family]
  - id: two-views
    scene_class: EventVsRV
    narration_words: 145
    est_sec: 58
    measured_sec: 43.3
    sync_points: [indicator, product-rule]
  - id: splitting
    scene_class: PoissonSplitting
    narration_words: 220
    est_sec: 88
    measured_sec: 68.8
    sync_points: [setup, binomial-given, telescope, outro]
---

# Video Script — Conditioning Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Dependence is why we build joint models — and conditioning is how we use
> it: observe something, update everything else. <bookmark mark="events"/>
> In this video we condition a random variable on an event, and watch a
> familiar ratio produce a genuine PMF, <bookmark mark="rvs"/> then condition
> on another random variable — which turns out to be a slice of last video's
> table, renormalized — <bookmark mark="payoff"/> and put the machinery to
> work on a result that deserves to be famous: thinning a Poisson stream
> leaves it Poisson.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 7 · Multiple Random
  Variables", recap line, objective; card rises to the top edge.
- `events`: outline line "1. Conditioning on an event" fades in.
- `rvs`: outline line "2. Conditioning on a random variable" fades in.
- `payoff`: outline line "3. Splitting a Poisson" fades in.

---

## Beat: on-events  (scene: ConditionOnEvent)

> Chapter four defined the conditional probability of one event given
> another. Random variables inherit it directly. <bookmark mark="ratio"/>
> The conditional PMF of X given an event S weighs each value by the same
> ratio: the probability that X equals x and S happens, over the probability
> of S. <bookmark mark="valid"/> Is this still a PMF? Yes — and the reason
> is elegant. The events "X equals x" partition the sample space, so by the
> total probability theorem their intersections with S add up to the
> probability of S itself. Divide, and the conditional masses sum to exactly
> one. <bookmark mark="truncate"/> Here is the picture to keep. A packet is
> retransmitted until it gets through, so the number of trials is geometric.
> <bookmark mark="cutoff"/> But this system gives up after n failures. Given
> that the packet made it, what does the trial count look like?
> <bookmark mark="survive"/> Only the first n bars survive.
> <bookmark mark="renormalize"/> Their shape is untouched — each one is
> divided by the same number, the probability of success, one minus one
> minus p to the n. <bookmark mark="rescale"/> Conditioning kept the
> geometry and rescaled the mass: the bars beyond n vanish, the rest grow
> just enough to carry mass one.

**Cues** (per-phrase sub-blocks so each animation lands on its sentence;
2026-07-03 draft review, 1:40)
- `ratio`: `p_{X \mid S}(x) = \Pr(X = x \mid S) = \Pr(\{X = x\} \cap S) /
  \Pr(S)` in accent.
- `valid`: the Total Probability tiling reused — Omega sliced into
  coloured {X = x} tiles, a translucent S ellipse across them, the
  intersection pieces outlined; `\sum_x p_{X \mid S}(x) = 1` at its right,
  both raised for balance (2026-07-03 draft review, 1:04).
- `truncate`: the geometric PMF (halving bars) grows in.
- `cutoff`: a dashed cutoff line appears after bar n.
- `survive`: bars beyond the cutoff fade to ghosts — exactly on "only the
  first n bars survive."
- `renormalize`: `p_{Y \mid S}(k) = (1-p)^{k-1} p / (1 - (1-p)^n)` written.
- `rescale`: surviving bars stretch uniformly to mass one.

---

## Beat: on-rvs  (scene: ConditionOnRV)

> Now condition on information of a richer kind: the observed value of
> another random variable. <bookmark mark="slice"/> Go back to the joint
> table. Observing X equals x means the experiment landed somewhere in one
> row. <bookmark mark="keep"/> So keep that row — and forget the rest.
> <bookmark mark="raw-masses"/> The row's masses don't sum to one,
> <bookmark mark="renorm"/> but we know the fix: divide by the row total,
> which is exactly the marginal of X at x. <bookmark mark="formula"/> That
> is the whole
> definition. The conditional PMF of Y given X equals x is the joint mass
> over the marginal mass — defined whenever the marginal is positive,
> because conditioning on something that cannot happen means nothing.
> <bookmark mark="family"/> And notice the plural: every value of x carves
> its own row and its own conditional PMF. Conditioning on a random variable
> hands you a whole family of distributions, indexed by what you might
> observe. Slide the observation, and the distribution of Y responds — that
> responsiveness is dependence, made visible.

**Cues** (table and formula raised; conditional slice shown as a small bar
chart, not a number row, per-phrase sub-blocks, chart placed right of the
table's column so its labels clear the frame; 2026-07-03 draft review,
2:33 + round 2, 2:34/2:51)
- `slice`: video 21's 3×3 urn table, upper left; row X=1 lights in accent.
- `keep`: the other rows dim.
- `raw-masses`: a small bar chart grows beneath-right with the raw row
  masses (1/6, 1/6).
- `renorm`: the bars stretch to mass one (1/2, 1/2) exactly on "divide by
  the row total."
- `formula`: `p_{Y \mid X}(y \mid x) = p_{X,Y}(x, y) / p_X(x)` in accent,
  upper right; caption "defined when p_X(x) > 0."
- `family`: the highlight sweeps to the other rows; the bar chart morphs
  row by row — one conditional PMF per x.

---

## Beat: two-views  (scene: EventVsRV)

> Two kinds of conditioning, then — on events and on random variables. They
> are the same idea in two dresses. <bookmark mark="indicator"/> Any event S
> has an indicator variable: one when S happens, zero when it doesn't.
> Conditioning on S is precisely conditioning on that variable taking the
> value one. And conditioning on X equals x is just conditioning on an
> event. Each view contains the other. <bookmark mark="product-rule"/> One
> more gift before the payoff: read the slice formula backwards. The joint
> mass equals the conditional times the marginal. That is the product rule —
> and it means joint distributions can be built the way experiments actually
> unfold: first draw, then second draw given the first.

**Cues**
- `indicator`: `p_{X \mid S}(x) = p_{X \mid \mathbf{1}_S}(x \mid 1)` with the
  indicator card from video 19 beside it.
- `product-rule`: `p_{X,Y}(x,y) = p_{Y \mid X}(y \mid x)\, p_X(x)` in
  accent; the slice animation replayed backwards in miniature — marginal
  bar times conditional row rebuilding a joint cell.

---

## Beat: splitting  (scene: PoissonSplitting)

> Now let the machinery earn its keep. <bookmark mark="setup"/> A
> transmitter sends bits: each is a one with probability p, a zero
> otherwise, independently — and the number of bits sent in an interval is
> Poisson with parameter lambda. Question: what is the distribution of the
> number of ones? <bookmark mark="binomial-given"/> Condition on the total.
> Given that k bits were sent, each independently a one with probability p,
> the count of ones is binomial with parameters k and p — that much we have
> known since chapter five. <bookmark mark="telescope"/> Now un-condition
> with the product rule: the mass of m ones sums the binomial times the
> Poisson over all totals k. Shift the index, and the sum telescopes into
> the series for an exponential. What remains is unmistakable: lambda p to
> the m over m factorial, times e to the minus lambda p. The number of ones
> is Poisson with parameter p times lambda. Thin a Poisson stream at random,
> and it stays Poisson — just slower. <bookmark mark="outro"/> The key idea
> of this video: conditioning is slicing the joint and renormalizing — and
> run backwards, it builds joint models one stage at a time.

**Cues**
- `setup`: a horizontal stream of dots (bits) with exponential-looking
  inter-arrival gaps (Poisson process feel), placed halfway between the
  `K \sim` Poisson(`\lambda`) card above and the binomial PMF below; each
  dot flips to accent (one) or muted (zero). (2026-07-03 draft review,
  4:35)
- `binomial-given`: `p_{M \mid K}(m \mid k) = \binom{k}{m} p^m (1-p)^{k-m}`
  — the video-16 binomial card look.
- `telescope`: the derivation compressed to three lines — the full sum, the
  index shift, and `p_M(m) = (\lambda p)^m e^{-\lambda p} / m!` landing in
  accent; middle steps indicated, not lingered on.
- `outro`: shared outro card — key idea + "Coming up: Conditional
  Expectation".

---

## Cut list (if over budget)

1. Drop the backwards-replay miniature in `two-views` (keep the formula).
2. Compress `valid` to a caption ("total probability makes it a PMF").
3. Trim the closing sentence of `on-rvs` ("that responsiveness...").
