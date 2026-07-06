---
slug: 21-joint-pmfs
title: Joint PMFs and Expectations
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the script 2026-07-03
derived_from: 21-joint-pmfs.md
derived_from_sha256: 7fb3f0287fbc4c0464a4fd33865a9ce9cd11d5937fc81887703f0cbc40a45479
provenance_stamped: 2026-07-06
target_scene_file: scenes/joint_pmfs.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Describe two random variables at once with one joint PMF - and read marginals, functions, and expectations off it."
  recap: "Last video: moments -- the variance from the first two moments closed the single-variable toolkit."
  key_idea: "The joint PMF is the whole story of a pair; marginals sum it out, and E[X + Y] = E[X] + E[Y] with no independence needed."
  bridge: "Next: conditioning -- slicing the joint table by what we observe."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word (ch. 6 across three
# videos). ~950 words -> ~295 s.
target_runtime_sec: 250   # recalibrated at final (0.8 x 310s draft, STYLE_BOOK 12)
tolerance_sec: 45

estimated_runtime_sec: 380
measured_runtime_sec: 248.3

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 110
    est_sec: 44
    measured_sec: 39.1
    sync_points: [table, marginals-out, functions-out]
  - id: joint-pmf
    scene_class: JointPMFDefinition
    narration_words: 175
    est_sec: 70
    measured_sec: 42.1
    sync_points: [pair-map, definition, set-sum]
  - id: marginals
    scene_class: MarginalPMFs
    narration_words: 190
    est_sec: 76
    measured_sec: 48.1
    sync_points: [urn-table, row-sums, col-sums]
  - id: not-enough
    scene_class: MarginalsNotEnough
    narration_words: 165
    est_sec: 66
    measured_sec: 40.5
    sync_points: [with-replacement, compare]
  - id: expectations
    scene_class: JointExpectation
    narration_words: 235
    est_sec: 94
    measured_sec: 78.4
    sync_points: [dice-sum, two-pair, seven-pair, twelve-pair, triangle, double-sum, split, urn, outro]
---

# Video Script — Joint PMFs and Expectations

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> So far the course has watched one random variable at a time. Real models
> rarely have that luxury: a signal comes with its noise, a first draw with a
> second. This chapter puts several random variables on screen at once.
> <bookmark mark="table"/> In this video we meet the object that describes a
> pair completely — the joint probability mass function, best pictured as a
> table of masses — <bookmark mark="marginals-out"/> learn to recover each
> variable's own PMF by summing the table out, and see why the margins alone
> can never tell the whole story, <bookmark mark="functions-out"/> and then
> push functions and expectations through the pair, ending at one of the most
> useful facts in probability.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 7 · Multiple Random
  Variables", recap line, objective; card rises to the top edge.
- `table`: outline line "1. The joint PMF" fades in.
- `marginals-out`: outline line "2. Marginals — and their limits" fades in.
- `functions-out`: outline line "3. Functions and linearity" fades in.

---

## Beat: joint-pmf  (scene: JointPMFDefinition)

> Take two random variables riding the same experiment. <bookmark mark="pair-map"/>
> Together they form a pair: each outcome in the sample space now lands on a
> point in the plane — an x-coordinate from X, a y-coordinate from Y.
> <bookmark mark="definition"/> The pair is described by one function: the
> joint probability mass function. p sub X comma Y of x and y is the
> probability that X equals x and, at the same time, Y equals y. It is the
> one-variable definition with the event replaced by an intersection.
> <bookmark mark="set-sum"/> And the familiar rules carry over: the
> probability that the pair lands in any set of points is the sum of the
> joint masses over that set, and summing over every pair of values gives
> exactly one.

**Cues**
- `pair-map`: the omega box with outcome balls; two arrows per outcome land
  on a small pair of axes at right (the book's Ω-to-plane figure,
  simplified to three outcomes).
- `definition`: `p_{X,Y}(x, y) = \Pr(X = x, Y = y)` in accent.
- `set-sum`: `\Pr(S) = \sum_{(x,y) \in S} p_{X,Y}(x,y)` and the
  normalization line beneath, CAPTION-size.

---

## Beat: marginals  (scene: MarginalPMFs)

> Here is a joint PMF worth staring at. <bookmark mark="urn-table"/> An urn
> holds balls numbered one, two, and three; we draw two without replacement.
> X is the first number, Y the second. The table shows every mass: zeros on
> the diagonal — the same ball cannot appear twice — and one sixth in every
> other cell. <bookmark mark="row-sums"/> What is the PMF of X alone? Fix a
> row and add across it: one sixth plus one sixth is one third, for every
> row. That operation — summing out the variable you don't care about — is
> called marginalization, and the result is the marginal PMF of X.
> <bookmark mark="col-sums"/> Columns work the same way, and Y's marginal is
> also uniform: one third, one third, one third. The margins of the table —
> literally, the sums written in its margins — are the individual
> distributions.

**Cues**
- `urn-table`: three `ball` glyphs beside a 3×3 joint table, centered
  horizontally; diagonal zeros in MUTED, off-diagonal `1/6` cells in INK.
- `row-sums`: the table stays in place (2026-07-03 draft review round 3,
  2:06); cells of one row light in accent and stream right into a margin
  column of `1/3`s written into the margin; repeat compressed for the
  other rows. Margin marks sit on the grid geometry — the p_X column is
  one vertical line, the p_Y row one horizontal line (round 4, 2:06/2:27).
- `col-sums`: same downward, margin row appears beneath; caption "the
  marginal PMFs live in the margins."

---

## Beat: not-enough  (scene: MarginalsNotEnough)

> Now change one word in the experiment: draw the two balls with
> replacement. <bookmark mark="with-replacement"/> The table transforms —
> every cell becomes one ninth, diagonal included, because the first ball
> goes back before the second draw. Sum the rows and columns: one third
> everywhere. The marginals are exactly the same as before.
> <bookmark mark="compare"/> Same margins — different tables. And that is
> the lesson: the marginal PMFs do not determine the joint PMF. Whether the
> two draws can collide, whether they push each other around — dependence
> lives inside the table, in information the margins simply do not carry.
> To describe a pair, you need the joint.

**Cues**
- `with-replacement`: the without-replacement table transforms cell by cell
  into the all-ninths table; then both margins are re-summed with the
  narration — row sums stream right, column sums stream down — visibly
  unchanged (2026-07-03 draft review round 2, 3:00). Table, p_X, and p_Y
  sit exactly where the previous beat's did (round 4, 2:58).
- `compare`: both tables shown in sequence (one at a time, house rule) with
  margins highlighted identical; caption "marginals are not enough."

---

## Beat: expectations  (scene: JointExpectation)

> Functions ride along, exactly as they did for one variable.
> <bookmark mark="dice-sum"/> Roll a blue die and a red die, and let U be
> their sum. U is a random variable, and its PMF sums the joint over the
> pairs that produce each value — the diagonals of the six-by-six table.
> <bookmark mark="two-pair"/> Two comes from one pair,
> <bookmark mark="seven-pair"/> seven from six pairs,
> <bookmark mark="twelve-pair"/> and twelve, again, from a single pair:
> <bookmark mark="triangle"/> the familiar triangle of the two-dice sum,
> straight from the joint. <bookmark mark="double-sum"/>
> Expectations follow the same pattern one dimension up: the expected value
> of g of X and Y is a double sum — g of each pair, weighted by the joint
> mass of that pair. <bookmark mark="split"/> Now take the simplest g: the
> sum. Split x plus y inside the double sum, and it falls apart into two
> single sums — each one a marginal mean. The expectation of X plus Y is the
> expectation of X plus the expectation of Y. Look at what we did not
> assume: nothing. No independence, no special structure — linearity of
> expectation holds for every pair, always. <bookmark mark="urn"/> For
> instance, in an urn with three balls, the expectation for a pair of
> drawings is two plus two — four — with and without replacement.
> <bookmark mark="outro"/> The key
> idea of this video: the joint PMF is the whole story of a pair —
> marginals sum it out, and expectations of sums split with no questions
> asked.

**Cues** (each diagonal lights exactly while its value is spoken; die
values labelled above and left of the grid in the dice colors; 2026-07-03
draft review, 3:44)
- `dice-sum`: the 6×6 grid with column values 1–6 above (red die) and row
  values 1–6 at left (blue die); caption "rolling a blue die and a red
  die" between the grid and U = X + Y.
- `two-pair`: the x + y = 2 diagonal (one cell) lights, unhurried.
- `seven-pair`: the x + y = 7 diagonal (six cells) lights.
- `twelve-pair`: the x + y = 12 diagonal lights while twelve is named
  explicitly (2026-07-03 draft review round 4, 3:58).
- `triangle`: the triangular PMF of U appears on its sentence (grid leaves
  first — one chart at a time).
- `double-sum`: `\mathrm{E}[g(X,Y)] = \sum_x \sum_y g(x,y)\, p_{X,Y}(x,y)`
  in accent.
- `split`: the double sum with `g = x + y` visibly separating into
  `\sum_x x\, p_X(x) + \sum_y y\, p_Y(y)`; caption "no independence
  required".
- `urn`: the three-ball urn image appears beside `E[X+Y] = 2 + 2 = 4`
  while the example is spoken (2026-07-03 draft review round 2, 4:45).
- `outro`: shared outro card (no ", always" on the card) + "Coming up:
  Conditioning Random Variables".

---

## Cut list (if over budget)

1. Compress the `set-sum` block to a caption with one spoken sentence.
2. Drop the row-by-row repeat in `marginals` (light one row, state the rest).
3. Trim the urn callback ("two plus two is four") from `expectations`.
