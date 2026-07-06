---
slug: 23-conditional-expectation
title: Conditional Expectation
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the script 2026-07-03
derived_from: 23-conditional-expectation.md
derived_from_sha256: 133a81be52e92da0afb0e6ea7c0189f23dfe34f080aa8aa6225e18a38311570e
provenance_stamped: 2026-07-06
target_scene_file: scenes/conditional_expectation.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Average a random variable slice by slice - and meet E[Y | X], a random variable made of means."
  recap: "Last video: conditioning slices the joint table and renormalizes; the product rule builds joints."
  key_idea: "E[Y | X] is itself a random variable, and averaging it recovers E[Y] -- the tower property."
  bridge: "Next: independence -- when the slices all look alike."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~930 words -> ~290 s.
target_runtime_sec: 290
tolerance_sec: 45

estimated_runtime_sec: 370
measured_runtime_sec: 260.7

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 90
    est_sec: 36
    measured_sec: 27.8
    sync_points: [per-slice, as-rv, tower-out]
  - id: definition
    scene_class: CondExpDefinition
    narration_words: 175
    est_sec: 70
    measured_sec: 45.8
    sync_points: [slice-mean, function-h, event-version]
  - id: as-rv
    scene_class: CondExpAsRV
    narration_words: 200
    est_sec: 80
    measured_sec: 57.9
    sync_points: [feed-x, soda-setup, pB]
  - id: tower
    scene_class: TowerProperty
    narration_words: 190
    est_sec: 76
    measured_sec: 48.6
    sync_points: [statement, derivation, meaning]
  - id: shirts
    scene_class: ShoppingSpree
    narration_words: 235
    est_sec: 94
    measured_sec: 80.6
    sync_points: [setup, prices, mean-ci, total, condition-n, tower-out2, at-least-five, outro]
---

# Video Script — Conditional Expectation

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, every observation of X handed us a fresh distribution for Y —
> a whole family of sliced, renormalized PMFs. This video compresses each
> slice to a single number. <bookmark mark="per-slice"/> We define the
> conditional expectation — the mean of Y given an observation —
> <bookmark mark="as-rv"/> discover that, taken together, those means form a
> random variable of their own, <bookmark mark="tower-out"/> and prove the
> tower property, the rule that lets us compute hard expectations one easy
> stage at a time.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 7 · Multiple Random
  Variables", recap line, objective; card rises to the top edge.
- `per-slice`: outline line "1. The mean of a slice" fades in.
- `as-rv`: outline line "2. A random variable made of means" fades in.
- `tower-out`: outline line "3. The tower property" fades in.

---

## Beat: definition  (scene: CondExpDefinition)

> Start from one slice. <bookmark mark="slice-mean"/> Given that X equals
> value lower case x, the variable Y has a conditional PMF — and any PMF
> has a mean. The
> conditional expectation of Y given X equals x weighs each value of y by
> its conditional mass. On the picture, it is the balance point of that
> slice: one fulcrum for the row we observed. <bookmark mark="function-h"/>
> Do this for every possible observation and collect the answers. The
> conditional expectation becomes a function — call it h — that maps each
> value x to the mean of its slice. <bookmark mark="event-version"/> And
> events work the same way: the expectation of X given an event S is the
> mean of the event based on the conditional PMF from last video — one
> balance point for the re-weighted bars.

**Cues**
- `slice-mean`: video 22's lifted, renormalized slice with an accent
  fulcrum settling under it;
  `\mathrm{E}[Y \mid X = x] = \sum_y y\, p_{Y \mid X}(y \mid x)` in accent.
- `function-h`: the slice sweeps across x values; fulcrums accumulate,
  tracing dots of `h(x) = \mathrm{E}[Y \mid X = x]`.
- `event-version`: compact card:
  `\mathrm{E}[X \mid S] = \sum_x x\, p_{X \mid S}(x)`; the bottom-left
  chart and the bottom-right card sit level, raised toward mid-frame
  (2026-07-03 draft review, 1:25).

---

## Beat: as-rv  (scene: CondExpAsRV)

> Here is the move that gives this chapter its depth. <bookmark mark="feed-x"/>
> Before the experiment runs, we don't know which value X will take — X is
> random. Feed that random X into the function h, and h of X becomes a random
> variable: the conditional expectation of Y given X, written with no
> particular value in sight. The experiment resolves X, and X resolves the
> mean. <bookmark mark="soda-setup"/> Make it concrete. A shop sells cherry
> soda and lemonade; the number of bottles sold in an hour is Poisson with
> mean ten, and each customer independently picks cherry with probability p.
> Given that exactly ten bottles were sold, the cherry count is binomial,
> and its conditional mean is ten p. <bookmark mark="pB"/> But the bottle
> count B is random — so the conditional mean of the cherry count is p times
> B: a random variable that scales with the crowd. Sell more bottles, expect
> more cherry sodas — the conditional expectation tracks the information.

**Cues**
- `feed-x`: `h(x) = \mathrm{E}[Y \mid X = x]` morphing into
  `h(X) = \mathrm{E}[Y \mid X]` in accent; caption "a random variable."
- `soda-setup`: two bottle glyphs (accent / muted), `B \sim` Poisson(10)
  card, `\mathrm{E}[C \mid B = 10] = 10p`.
- `pB`: `\mathrm{E}[C \mid B] = pB` in accent; a small B counter ticks
  through values while the mean updates with it.

---

## Beat: tower  (scene: TowerProperty)

> A random variable made of means should itself have a mean — and it is
> exactly the one you hope for. <bookmark mark="statement"/> The expectation
> of the conditional expectation of Y given X equals the expectation of Y.
> This is the tower property. <bookmark mark="derivation"/> The proof is
> three moves we already own. Write the outer expectation as a sum over x,
> weighted by the marginal. Substitute each slice's mean. The conditional
> mass times the marginal is the joint — the product rule — and summing the
> joint over x re-marginalizes it to the PMF of Y. What is left is the plain
> mean of Y. <bookmark mark="meaning"/> Read it as strategy, not just
> algebra: to find a hard expectation, condition on something that makes it
> easy, then average the easy answers over what you conditioned on. Compute
> in stages.

**Cues**
- `statement`: `\mathrm{E}\left[\mathrm{E}[Y \mid X]\right] = \mathrm{E}[Y]`
  in accent, alone at center.
- `derivation`: three compact lines with their equals signs aligned
  vertically — the weighted sum of slice means, the joint appearing via
  the product rule, the collapse to `\sum_y y\, p_Y(y)`
  (2026-07-03 draft review, 3:31).
- `meaning`: caption "condition on what makes it easy - average the
  answers" in accent, like the other scenes' closing lines
  (2026-07-03 draft review, 3:31).

---

## Beat: shirts  (scene: ShoppingSpree)

> Watch the strategy crack a problem that direct computation would fumble.
> <bookmark mark="setup"/> A student buys shirts. How many? Random: N is
> geometric with parameter one half. <bookmark mark="prices"/> What does
> each cost? Also random: ten, twenty, or fifty dollars with probabilities
> point five, point three, point two — <bookmark mark="mean-ci"/> mean
> twenty-one dollars — <bookmark mark="total"/> independently of everything
> else. The total spent is a sum with a random number of terms. What is its
> mean?
> <bookmark mark="condition-n"/> Condition on N. Given that the student buys
> n shirts, the total is a sum of n costs, and linearity gives twenty-one
> times n. So the conditional expectation of the total given N is twenty-one
> N — a random variable, exactly as this video promised.
> <bookmark mark="tower-out2"/> Now the tower: average it. Twenty-one times
> the expectation of N, and a geometric with parameter one half has mean
> two. Forty-two dollars. <bookmark mark="at-least-five"/> One more twist:
> given that the student buys at least five shirts, the same tower gives
> twenty-one times the conditional mean of N — and the geometric is
> memoryless, so having reached five, the wait beyond four resets: four plus
> two is six. Six shirts expected, one hundred twenty-six dollars.
> <bookmark mark="outro"/> The key idea of this video: the conditional
> expectation is a random variable, and the tower property turns hard
> expectations into staged easy ones.

**Cues** ($ shown on every dollar amount; 2026-07-03 draft review)
- `setup`: `N \sim` geometric(1/2) card.
- `prices`: `C_i \in \{\$10, \$20, \$50\}` beneath it; the full mean
  computation `\mathrm{E}[C_i] = \$10 \times 0.5 + \$20 \times 0.3 +
  \$50 \times 0.2 = \$21` writes in while the prices and probabilities
  are enumerated — early, so it stays on screen longer (2026-07-03 draft
  review round 2, 4:07).
- `mean-ci`: the `\$21` term highlights in accent exactly on "mean
  twenty-one dollars" (2026-07-03 draft review, 3:51).
- `total`: the computation fades; only then the compact
  `\mathrm{E}[C_i] = \$21` block appears; the row of five face-down shirt
  cards and `T = \sum_{i=1}^{N} C_i`.
- `condition-n`: all five cards flip to prices ($20/$10/$50/$10/$20 —
  2026-07-03 draft review, 4:15); `\mathrm{E}[T \mid N] = \$21\,N` in
  accent.
- `tower-out2`: the cards, T definition, AND the accent
  `\mathrm{E}[T \mid N]` line all fade before the tower line lands
  (2026-07-03 draft review, 4:36);
  `\mathrm{E}[T] = \mathrm{E}[\mathrm{E}[T \mid N]] = \$21\,\mathrm{E}[N]
  = \$42`.
- `at-least-five`: card `\mathrm{E}[N \mid N \ge 5] = 4 + \mathrm{E}[N] = 6`
  (memoryless), then `\mathrm{E}[T \mid N \ge 5] = \$21 \times 6 = \$126`
  in accent.
- `outro`: shared outro card — key idea + "Coming up: Independent Random
  Variables".

---

## Cut list (if over budget)

1. Compress `event-version` to a caption card with no dedicated narration.
2. Drop the B-counter animation in `pB` (keep the formula).
3. Trim `at-least-five` to the stated result with one memoryless aside.
