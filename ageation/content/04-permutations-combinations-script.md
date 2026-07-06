---
slug: 04-permutations-combinations
title: Permutations and Combinations
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 04-permutations-combinations.md
derived_from_sha256: c7d7d036f28b04fb94e6fa3e1b60e9501db11c2e95e059637fbe902dce96a54e
provenance_stamped: 2026-07-06
target_scene_file: scenes/permutations_combinations.py

linking:
  objective: "Count ordered arrangements and unordered selections -- and the one factor between them."
  recap: "Last video: probability is counting, and to count choices in stages you multiply."
  key_idea: "A k-permutation is a combination times k! orderings: order kept gives n!/(n-k)!, order dropped gives C(n,k)."
  bridge: "Next: partitions into several groups, and the stars-and-bars trick."

voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 540
tolerance_sec: 45

estimated_runtime_sec: 545
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 80
    est_sec: 32
    measured_sec: null
    sync_points: []
  - id: permutations
    scene_class: Permutations
    narration_words: 185
    est_sec: 74
    measured_sec: null
    sync_points: [slots, factorial, list]
  - id: k-permutations
    scene_class: KPermutations
    narration_words: 170
    est_sec: 68
    measured_sec: null
    sync_points: [slots, formula, songs]
  - id: combinations
    scene_class: Combinations
    narration_words: 220
    est_sec: 88
    measured_sec: null
    sync_points: [ordered, group, factor, formula, symmetry]
  - id: binomial-theorem
    scene_class: BinomialTheorem
    narration_words: 215
    est_sec: 86
    measured_sec: null
    sync_points: [pascal-rule, triangle, theorem, corollary, outro]
---

# Video Script — Permutations and Combinations

---

## Beat: overview  (scene: ChapterOverview)

> Last video, we saw that, in simple scenarios, probability reduces to counting,
> and that to count choices made in stages, you multiply. Now we build the two
> counts you will reach for again and again. In this
> video: permutations, the ordered arrangements; k-permutations, ordered
> selections of part of a set; combinations, the unordered selections; and the
> binomial theorem that ties them together. The whole video turns on one
> question — does order matter?

**Animation cue:** title card with a recap, then the outline.

---

## Beat: permutations  (scene: Permutations)

> A permutation is an ordered arrangement of distinct objects — a list with no
> repeats. <bookmark mark="slots"/> Count them by filling slots. Take the set one,
> two, three, and three slots to fill. The first slot has three choices. Once it
> is taken, the second slot has only two left. The last slot has just one. By the
> counting principle, multiply: three times two times one. <bookmark
> mark="factorial"/> That product is three factorial, which is six. In general,
> arranging n distinct objects gives n factorial — n times n minus one, all the
> way down to one. <bookmark mark="list"/> Here are all six arrangements of one,
> two, three. Same three objects every time; only the order changes.

**Cues**
- `slots`: three slots; pool shrinks 3 -> 2 -> 1 as each is filled.
- `factorial`: write 3! = 3 x 2 x 1 = 6, then n!.
- `list`: list the 6 permutations of {1,2,3}.

---

## Beat: k-permutations  (scene: KPermutations)

> Often we arrange only part of the set. <bookmark mark="slots"/> Suppose we rank
> k of the n objects. The first slot still has n choices, the second n minus one,
> and so on — but now we stop after k slots. <bookmark mark="formula"/> The count
> is n times n minus one, down to n minus k plus one, which we write compactly as
> n factorial over n minus k factorial. <bookmark mark="songs"/> For example, a
> band with four songs wants to play two, in order. That is the number of
> 2-permutations of four: four times three, twelve arrangements. This is sampling
> without replacement, keeping order — once a ball is drawn it is gone, but the
> sequence is recorded.

**Cues**
- `slots`: n balls, only k slots; n then n-1 choices.
- `formula`: n!/(n-k)! = n(n-1)...(n-k+1).
- `songs`: 4 songs, 2 slots -> 4 x 3 = 12.

---

## Beat: combinations  (scene: Combinations)

> Now drop the order. A combination is just a subset — which objects, not in
> what arrangement. This is the distinction that trips people up most, so let's
> see it directly. <bookmark mark="ordered"/> Here are the twelve 2-permutations
> of one, two, three, four — all ordered pairs. <bookmark mark="group"/> But one,
> two and two, one are the same subset. Group the pairs that use the same two
> elements, and the twelve collapse into six groups. <bookmark mark="factor"/>
> Each group holds exactly two orderings — that is two factorial. So the number
> of subsets is the number of pairs divided by two, which is equal to six. <bookmark
> mark="formula"/> In general, the number of k-element subsets is n factorial
> over k factorial times n minus k factorial — the binomial coefficient, n choose
> k. The ordered count, divided by the k factorial orderings. <bookmark
> mark="symmetry"/> And notice: choosing the k elements to keep is the same as
> choosing the n minus k to leave out. So n choose k equals n choose n minus k.

**Cues**
- `ordered`: the 12 ordered pairs of {1,2,3,4}.
- `group`: collapse into 6 dashed loops of 2.
- `factor`: label the k! = 2 ordering factor; 12 / 2 = 6.
- `formula`: C(n,k) = n!/(k!(n-k)!).
- `symmetry`: C(n,k) = C(n,n-k).

---

## Beat: binomial-theorem  (scene: BinomialTheorem)

> Binomial coefficients fit together beautifully. <bookmark mark="pascal-rule"/>
> Pascal's rule says n choose k equals n minus one choose k minus one, plus n
> minus one choose k. The reason is simple: for a k-subset, ask whether element n
> is in it. If yes, choose the other k minus one from the rest; if no, choose all
> k from the rest. <bookmark mark="triangle"/> Stack the coefficients by row and
> you get Pascal's triangle, where every entry is the sum of the two above it.
> <bookmark mark="theorem"/> They are called binomial coefficients because of the
> binomial theorem: x plus y to the n is the sum over k of n choose k, x to the k,
> y to the n minus k. Expanding the product, the coefficient of x-to-the-k counts
> the ways to pick x from k of the factors — that is n choose k. <bookmark
> mark="corollary"/> Set x and y both to one, and the theorem gives the sum of
> all the binomial coefficients equals two to the n — the same count of subsets
> we found before, now split by size. <bookmark mark="outro"/> So everything here
> hangs on a single hinge: order kept gives n factorial over n minus k factorial;
> order dropped divides by k factorial, giving n choose k. Next, we go further and
> split a set into several groups at once — partitions, and the stars-and-bars
> trick.

**Cues**
- `pascal-rule`: C(n,k) = C(n-1,k-1) + C(n-1,k).
- `triangle`: build Pascal's triangle, highlight one entry = sum of two above.
- `theorem`: (x+y)^n = sum C(n,k) x^k y^{n-k}.
- `corollary`: x=y=1 -> sum C(n,k) = 2^n.
- `outro`: key-idea card + bridge to Partitions.

---

## Cut list (if over budget)
1. Drop the alternating-sum corollary (keep only 2^n).
2. Shorten the Pascal's-triangle build to four rows.
3. Trim the songs example in k-permutations to one sentence.
