---
slug: 05-partitions
title: Partitions and Stars and Bars
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 05-partitions.md
derived_from_sha256: 8f7342b3fcbadd22a09dd61868a6909e04c8ead38686a789e65ee9e8af8ad539
provenance_stamped: 2026-07-06
target_scene_file: scenes/partitions.py

linking:
  objective: "Split a set into several labeled groups, and count the ways to share a total among r bins."
  recap: "Last video: permutations and combinations -- ordered vs unordered selections."
  key_idea: "Fixed group sizes give the multinomial coefficient n!/(n_1!...n_r!); free sizes give stars and bars, C(k+r-1, r-1)."
  bridge: "Next: a unified view of all four sampling schemes, and the birthday problem."

voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 390
tolerance_sec: 45

estimated_runtime_sec: 390
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 80
    est_sec: 32
    measured_sec: null
    sync_points: []
  - id: partitions
    scene_class: Partitions
    narration_words: 200
    est_sec: 80
    measured_sec: null
    sync_points: [split, arrange, divide, formula]
  - id: stars-and-bars
    scene_class: StarsAndBars
    narration_words: 215
    est_sec: 86
    measured_sec: null
    sync_points: [row, cut, tuple, count]
  - id: sampling
    scene_class: SamplingTieIn
    narration_words: 175
    est_sec: 70
    measured_sec: null
    sync_points: [urn, formula, emphasize, outro]
---

# Video Script — Partitions and Stars and Bars

---

## Beat: overview  (scene: ChapterOverview)

> Last video, we counted permutations and combinations — ordered arrangements
> versus unordered selections. A combination split a set in two: the chosen and
> the rest. In this video, we split a set into several groups at once. We start
> with partitions and the multinomial coefficient; then stars and bars, a picture
> for counting how a total can be shared among several bins; and one more
> sampling count, drawing with replacement but ignoring order.

**Animation cue:** title card with a recap, then the outline.

---

## Beat: partitions  (scene: Partitions)

> A combination splits a set into two parts — the k chosen and the n minus k
> left behind. <bookmark mark="split"/> But often we want more parts at once.
> Take six distinct items and split them into three labeled groups of sizes
> three, two, and one. How many ways are there to accomplish this task?
> <bookmark mark="arrange"/> Here is the
> trick: first line up all six items in a row. There are six factorial orderings.
> Now read the groups off the row — the first three items, then the next two,
> then the last one. <bookmark mark="divide"/> But the order inside a group does
> not matter: any of the three factorial shuffles of the first group gives the
> same group, and likewise two factorial for the second. So divide out those
> internal orderings. <bookmark mark="formula"/> Six factorial over three
> factorial, two factorial, one factorial — that is sixty. In general, splitting
> n items into r groups of sizes n-one through n-r gives the multinomial
> coefficient: n factorial divided by the product of the n-i factorials.

**Cues**
- `split`: recall C(n,k) as a two-way split, then show 6 balls -> boxes 3,2,1.
- `arrange`: line the 6 balls in a row; label 6! orderings.
- `divide`: highlight that within-group order is redundant; divide by 3! 2! 1!.
- `formula`: 6!/(3!2!1!) = 60, then the general multinomial coefficient.

---

## Beat: stars-and-bars  (scene: StarsAndBars)

> Now change the question. Instead of fixing the group sizes, we ask: in how
> many ways can the sizes themselves be chosen? Count the nonnegative integer
> solutions of x-one plus x-two, up to x-r, equals k. <bookmark mark="row"/>
> Here is the picture, called stars and bars. Draw k identical stars in a row,
> and drop in r minus one bars. <bookmark mark="cut"/> The bars cut the stars
> into r groups: the stars before the first bar, between consecutive bars, and
> after the last bar. <bookmark mark="tuple"/> Each arrangement reads off as a
> solution. This row — two stars, a bar, one star, a bar, then nothing, a bar,
> two stars — gives the tuple two, one, zero, two. Two consecutive bars just
> mean an empty group. <bookmark mark="count"/> So every solution is one
> arrangement of k stars and r minus one bars in a row of k plus r minus one
> positions. Counting them is counting which positions hold the bars: k plus r
> minus one, choose r minus one. Equivalently, choose the star positions —
> k plus r minus one, choose k.

**Cues**
- `row`: state x_1+...+x_r = k; draw k stars in a row.
- `cut`: insert r-1 bars, splitting the stars into r groups.
- `tuple`: read off the concrete arrangement as a solution tuple, note empty group.
- `count`: brace the k+r-1 positions; C(k+r-1, r-1) = C(k+r-1, k).

---

## Beat: sampling  (scene: SamplingTieIn)

> Stars and bars settles a sampling question we left open. <bookmark
> mark="urn"/> An urn holds n numbered balls. Draw one, record its number, put
> it back, and repeat k times — but this time we ignore the order, keeping only
> a tally of how many times each ball appeared. <bookmark mark="formula"/> A
> tally has one count per ball: nonnegative numbers x-one through x-n that add
> up to k draws. That is a stars-and-bars problem with n bins and k stars, so
> the number of outcomes is n plus k minus one, choose k. <bookmark
> mark="emphasize"/> So drawing k times from n with replacement, but ignoring
> order, gives n plus k minus one, choose k — the fourth and last way to sample,
> which we will line up with the others in the next video. <bookmark
> mark="outro"/> So the whole story is two
> counts. Fixed group sizes give the multinomial coefficient, n factorial over
> the product of the n-i factorials. Free sizes give stars and bars, k plus r
> minus one choose r minus one. Next, we lay all four sampling schemes side by
> side, and put them to work on the birthday problem.

**Cues**
- `urn`: urn of n balls, k draws with replacement, keep a tally not a sequence.
- `formula`: tally = solution of sum x_i = k over n bins -> C(n+k-1, k).
- `table`: 2x2 sampling table, fill the with-replacement/unordered cell.
- `outro`: key-idea card + bridge to A Unified View of Sampling.

---

## Cut list (if over budget)
1. Trim the sampling-table recap to naming only the new cell.
2. Shorten the partitions arrange-then-divide narration to one pass.
3. Drop the "two consecutive bars = empty group" aside in stars and bars.
