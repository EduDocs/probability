---
slug: 06-sampling
title: A Unified View of Sampling
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 06-sampling.md
derived_from_sha256: eb830877f66b7a166d4ac217d9e05f6c3453c4de5912f106fb049c17d95affd3
provenance_stamped: 2026-07-06
target_scene_file: scenes/sampling.py

linking:
  objective: "Classify any draw of k from n by replacement and order, read off its count from one 2x2 table, and apply it."
  recap: "Last video: partitions and the stars-and-bars count."
  key_idea: "Every sampling problem is two yes/no questions -- replacement? order? -- and one 2x2 table of counts; the without-replacement column divides by k!."
  bridge: "Next chapter: the axioms of probability that make all this rigorous."

voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 300
tolerance_sec: 45

estimated_runtime_sec: 290
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 85
    est_sec: 34
    measured_sec: null
    sync_points: []
  - id: sampling-table
    scene_class: SamplingTable
    narration_words: 240
    est_sec: 96
    measured_sec: null
    sync_points: [grid, ordered, unordered, kfactor]
  - id: birthday-setup
    scene_class: BirthdayProblem
    narration_words: 210
    est_sec: 84
    measured_sec: null
    sync_points: [setup, denominator, numerator, formula]
  - id: birthday-punchline
    scene_class: BirthdayPunchline
    narration_words: 150
    est_sec: 60
    measured_sec: null
    sync_points: [curve, callout, outro]
---

# Video Script — A Unified View of Sampling

---

## Beat: overview  (scene: ChapterOverview)

> Last video, we split a set into several groups at once — partitions, and the
> stars-and-bars count. That was the last piece. In this video we step back and
> see that everything in this chapter has been one question all along: drawing k
> items from n, asked four different ways. We assemble those four into a single
> table, and then put it to work on a famous puzzle — the Birthday Problem.

**Animation cue:** title card with a recap, then a two-item outline.

---

## Beat: sampling-table  (scene: SamplingTable)

> Every urn example in this chapter draws k items from a set of n. <bookmark
> mark="grid"/> Two yes-or-no questions tell them apart. First: do we put each
> item back before the next draw — with replacement, or without? Second: do we
> record the order of the draws, or only which items came out? Two binary
> choices make a two-by-two table, and each cell holds a count. <bookmark
> mark="ordered"/> The ordered column comes straight from the counting
> principle. With replacement, every one of the k draws has all n items
> available, so there are n to the k ordered sequences. Without replacement the
> pool shrinks each time — n, then n minus one, down to n minus k plus one —
> which is n factorial over n minus k factorial. <bookmark mark="unordered"/> The
> unordered column drops the order. <bookmark mark="kfactor"/> Look along the
> without-replacement row: any selection of k distinct items can be arranged
> in k factorial ways, so the unordered count is the ordered one divided by k
> factorial — that is n choose k. The with-replacement row is subtler, because
> a repeated item cannot be reordered into distinct sequences; the stars-and-bars
> argument from last video handles it and gives n plus k minus one, choose k.
> Four cells, two questions. Recognizing which cell a problem lives in is usually
> the whole battle.

**Cues**
- `grid`: draw the 2x2 grid with row labels (with / without replacement) and column labels (ordered / unordered).
- `ordered`: fill the ordered column — n^k (top), n!/(n-k)! (bottom).
- `unordered`: fill the unordered column — C(n+k-1,k) (top), C(n,k) (bottom).
- `kfactor`: right-arrow across the without-replacement row labeled "÷ k!" linking n!/(n-k)! to C(n,k).

---

## Beat: birthday-setup  (scene: BirthdayProblem)

> Now one example that uses two cells of that table. <bookmark mark="setup"/> A
> room holds k people. Each person's birthday is equally likely to be any of the
> three hundred sixty-five days of the year, with different people unrelated. What
> is the probability that at least two of them share a birthday? <bookmark
> mark="denominator"/> It is easier to count the opposite — that all k birthdays
> are distinct — and subtract from one. List the birthdays in order. That is a
> sequence of k days drawn from three hundred sixty-five, with repeats allowed:
> sampling with replacement, ordered. So there are three hundred sixty-five to
> the k equally likely outcomes in total — the denominator. <bookmark
> mark="numerator"/> The outcomes with all distinct birthdays are exactly those
> drawn without replacement, ordered — a k-permutation of three hundred
> sixty-five: three sixty-five times three sixty-four, down to three hundred
> sixty-five minus k plus one. <bookmark mark="formula"/> The probability all are
> distinct is the ratio of those two counts. So the probability of at least one
> shared birthday is one minus three hundred sixty-five factorial, over three
> hundred sixty-five minus k factorial, times three sixty-five to the k.

**Cues**
- `setup`: k small figures and a strip labeled "365 days".
- `denominator`: 365^k, tagged "with replacement, ordered".
- `numerator`: 365!/(365-k)!, tagged "without replacement, ordered".
- `formula`: P(shared) = 1 - 365!/((365-k)! · 365^k).

---

## Beat: birthday-punchline  (scene: BirthdayPunchline)

> Now evaluate it. <bookmark mark="curve"/> As the room fills, the probability of
> a shared birthday climbs — slowly at first, then steeply. <bookmark
> mark="callout"/> It first passes one half at just k equals twenty-three, where
> it is about zero point five oh seven. In a room of only twenty-three people, it
> is already more likely than not that some pair shares a birthday — even with
> three hundred sixty-five days to go around. The surprise comes from a swap:
> people imagine the chance that someone shares *their* particular birthday, which
> grows far more slowly, instead of the chance that *any* pair matches. <bookmark
> mark="outro"/> And that is the chapter. Every sampling problem is two
> questions: sampling with or without replacement? And sampling with or without
> order? The answers dictate which cell of the sampling table should be used.
> Next chapter, we make probability models rigorous, with the axioms of
> probability.

**Cues**
- `curve`: a rising curve of P(shared) vs k.
- `callout`: a dashed line at 1/2, the point k = 23 highlighted (~0.507).
- `outro`: key-idea card + bridge to the next chapter (axioms of probability).
