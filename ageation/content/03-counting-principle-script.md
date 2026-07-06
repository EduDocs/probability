---
slug: 03-counting-principle
title: The Counting Principle
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 03-counting-principle.md
derived_from_sha256: 26831818b4edff26308cd64484bdfd8effc818c127c6384bd1149d60196a93cc
provenance_stamped: 2026-07-06
target_scene_file: scenes/counting_principle.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Turn probability into counting, and count Cartesian products."
  recap: "In Chapter 1 we built sets and functions -- the language of outcomes."
  key_idea: "When outcomes are equally likely, probability is counting; the counting principle multiplies choices."
  bridge: "Next: permutations and combinations -- counting ordered and unordered selections."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 420
tolerance_sec: 45

estimated_runtime_sec: 430
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 82
    est_sec: 33
    measured_sec: null
    sync_points: []
  - id: equally-likely
    scene_class: EquallyLikely
    narration_words: 150
    est_sec: 60
    measured_sec: null
    sync_points: [die, event, ratio]
  - id: counting-principle
    scene_class: CountingPrinciple
    narration_words: 196
    est_sec: 78
    measured_sec: null
    sync_points: [grid, product, coin-die, independence]
  - id: multistage
    scene_class: MultiStageSampling
    narration_words: 168
    est_sec: 67
    measured_sec: null
    sync_points: [r-sets, urn, n-to-k]
  - id: power-set
    scene_class: PowerSet
    narration_words: 188
    est_sec: 75
    measured_sec: null
    sync_points: [toggles, enumerate, two-to-n, outro]
---

# Video Script — The Counting Principle

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> In Chapter one we built the language of sets and functions — the vocabulary of
> outcomes. Now we start computing with it. This chapter is about counting,
> because in the simplest model, finding the probability reduces to
> counting. In this video we meet the equally-likely model, the counting
> principle, multi-stage experiments, and a quick way to count all the subsets
> of a set.

**Animation cue:** title card with a recap of Chapter 1, then the outline.

---

## Beat: equally-likely  (scene: EquallyLikely)

> Here is the simplest probabilistic scenario: finitely many outcomes, all
> equally likely. <bookmark mark="die"/> Take a fair die — six faces, each just
> as likely as any other. The probability of any single face is one over six.
> <bookmark mark="event"/> An event is just a subset of the outcomes. Consider
> the event "roll a prime": the faces two, three, and five. <bookmark
> mark="ratio"/> To find its probability, we count. Three favorable outcomes out
> of six total, so the probability is three over six, or one half. That is the
> whole model: probability is the number of favorable outcomes divided by the
> total. The catch is that the counting is often the hard part — and that is
> what combinatorics is for.

**Cues**
- `die`: show six die faces in a row.
- `event`: highlight faces 2, 3, 5.
- `ratio`: write P(prime) = 3/6 = 1/2.

---

## Beat: counting-principle  (scene: CountingPrinciple)

> The first tool is the counting principle, and it is about the Cartesian
> product from Chapter one. <bookmark mark="grid"/> Take a set S with three
> elements and a set T with two. Pair every element of S with every element of T,
> and you fill a grid. <bookmark mark="product"/> The number of pairs is just
> three times two — six. In general, if S has m elements and T has n, their
> Cartesian product has m times n elements. To count a product, multiply the sizes.
> <bookmark mark="coin-die"/> Flip a coin and roll a die. Two outcomes for the
> coin, six for the die — so two times six, twelve joint outcomes in all.
> <bookmark mark="independence"/> And because the outcomes are equally likely,
> the probability of any one is one over twelve, which factors as one-half times
> one-sixth. Combining unrelated experiments multiplies their probabilities — an
> informal first taste of independence, which we will make precise later.

**Cues**
- `grid`: build the 3 x 2 grid of paired balls (reuse the Sets-video style).
- `product`: write |S x T| = |S| |T| = 3 x 2 = 6.
- `coin-die`: coin (2) x die (6) = 12.
- `independence`: 1/12 = 1/2 x 1/6.

---

## Beat: multistage  (scene: MultiStageSampling)

> The principle extends to any number of stages. <bookmark mark="r-sets"/> With r
> sets of sizes n-one, n-two, up to n-r, the number of ordered tuples is the
> product n-one times n-two, all the way to n-r. Each independent choice just
> multiplies the running total. <bookmark mark="urn"/> Here is the classic case:
> an urn with n numbered balls. Draw one, record its number, and put it back.
> Repeat k times. <bookmark mark="n-to-k"/> Each of the k draws has the same n
> possibilities, so the number of ordered sequences is n multiplied by itself k
> times — n to the power k. This is sampling with replacement, with order kept,
> and it is the first of four sampling schemes we will assemble by the end of the
> chapter.

**Cues**
- `r-sets`: write n_1 n_2 ... n_r.
- `urn`: an urn with numbered balls and k draw-slots.
- `n-to-k`: write n^k.

---

## Beat: power-set  (scene: PowerSet)

> Here is a neat application: how many subsets does a set have? <bookmark
> mark="toggles"/> Take the set one, two, three. To build a subset, go through
> the elements one at a time and make a single yes-or-no choice: is this element
> in, or out? <bookmark mark="enumerate"/> That is one binary choice per element
> — exactly the indicator function from the last video. Three elements, two
> choices each, so by the counting principle there are two times two times two —
> eight subsets, from the empty set all the way up to the whole set. <bookmark
> mark="two-to-n"/> In general, a set with n elements has two to the n subsets.
> One indicator bit per element, multiplied together. <bookmark mark="outro"/>
> So the whole of this video rests on one idea: when outcomes are equally likely,
> probability is counting, and to count choices made in stages, you multiply.
> Next, we sharpen the toolkit with permutations and combinations — counting
> selections when order does, and does not, matter.

**Cues**
- `toggles`: three elements with in/out toggles.
- `enumerate`: list the 8 subsets of {1,2,3}.
- `two-to-n`: write 2^n (and 2^3 = 8).
- `outro`: key-idea card + bridge to Permutations and Combinations.

---

## Cut list (if over budget)
1. Trim the independence aside in `counting-principle` to one sentence.
2. Drop the explicit r-sets generalization in `multistage`, keep the n^k urn.
3. Shorten the subset enumeration in `power-set` (show 4 of the 8, say "and so on").
