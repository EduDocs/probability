---
slug: 14-independence
title: Independence
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 14-independence.md
derived_from_sha256: 3290402aaadfff486a1138184ad77a1ccdc82735f39b14ba6abf1ea062a2d8d6
provenance_stamped: 2026-07-06
target_scene_file: scenes/independence.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Pin down independence -- when knowing one event tells you nothing about another -- and its subtleties across several events and under conditioning."
  recap: "Last video: Bayes' rule, updating a prior to a posterior in light of evidence."
  key_idea: "A and B are independent when Pr(A ∩ B) = Pr(A) Pr(B); with several events pairwise independence is weaker than mutual, and conditioning can create or destroy independence."
  bridge: "Next chapter: random variables -- attaching numbers to the outcomes of an experiment."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 450
tolerance_sec: 45

estimated_runtime_sec: 450
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 105
    est_sec: 42
    measured_sec: null
    sync_points: []
  - id: independence
    scene_class: Independence
    narration_words: 285
    est_sec: 114
    measured_sec: null
    sync_points: [define, dice, disjoint, gambler]
  - id: multiple-events
    scene_class: MultipleEvents
    narration_words: 210
    est_sec: 84
    measured_sec: null
    sync_points: [define, pairwise, fail]
  - id: conditional-independence
    scene_class: ConditionalIndependence
    narration_words: 260
    est_sec: 104
    measured_sec: null
    sync_points: [define, create, destroy, outro]
---

# Video Script — Independence

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Bayes' rule showed how evidence reshapes our beliefs. This video is about the
> opposite situation: when evidence changes nothing. Two events are independent if
> learning one tells you nothing about the other. It sounds simple, and for two
> events it nearly is — but independence hides some genuine surprises. It is not
> the same as events being incompatible; with three or more events it splinters
> into pairwise and mutual versions that don't coincide; and it can appear or
> vanish the instant we condition on something else. We'll take these in turn: two
> events, then many, then independence under conditioning.

**Animation cue:** title card, recap line (Bayes' rule), then the question — when
does evidence change nothing? — and a three-item outline.

---

## Beat: independence  (scene: Independence)

> Start with the definition. <bookmark mark="define"/> Two events A and B are
> independent when the probability of both is the product of their probabilities —
> Pr of A-and-B equals Pr of A times Pr of B. When B has positive probability
> that's the same as saying Pr of A given B equals Pr of A: conditioning on B
> leaves A's probability untouched. The posterior equals the prior — B carries no
> information about A. And it's symmetric: if A is independent of B, then B is
> independent of A. <bookmark mark="dice"/> Two dice, one red, one blue —
> thirty-six equally likely outcomes. A four on the red die and a six on the blue:
> the probability of both is one thirty-sixth, which is one-sixth times one-sixth.
> The events are independent. But a four on the red die and a sum of eleven? A red
> four makes a sum of eleven impossible — eleven needs a five and a six — so the
> joint probability is zero, nowhere near one-sixth times the probability of the
> sum. The events are dependent. <bookmark mark="disjoint"/> And beware one
> seductive error:
> independence is not disjointness. In fact, disjoint events with positive
> probability are the opposite of independent — if they can't co-occur, then
> learning one happened tells you the other definitely did not. Their joint
> probability is zero, while the product of their probabilities is positive.
> <bookmark mark="gambler"/> Independence also means trials have no memory. A fair
> coin that just landed heads five times running is exactly as likely to show tails
> next toss as it ever was — one-half. Believing a tail is somehow "due" is the
> gambler's fallacy: the long run balances out by swamping the past with fresh
> trials, never by correcting it.

**Cues**
- `define`: Pr(A ∩ B) = Pr(A) Pr(B) ⇔ Pr(A \mid B) = Pr(A); note the symmetry.
- `dice`: a 6×6 outcome grid; highlight {r=4} ∩ {b=6} (independent) vs {r=4} ∩ {r+b=11} (empty → dependent).
- `disjoint`: two disjoint blobs in Omega; Pr(A ∩ B) = 0 < Pr(A) Pr(B).
- `gambler`: a run H H H H … then a next toss still at 1/2; name the gambler's fallacy in accent.

---

## Beat: multiple-events  (scene: MultipleEvents)

> With more than two events, independence gets subtle. <bookmark mark="define"/>
> Events A-one through A-n are independent only if every subset of them factors —
> the probability of any bunch occurring together equals the product of their
> individual probabilities. For three events A, B, C that's four conditions: the
> three pairs, and the triple all at once. <bookmark mark="pairwise"/> Why insist
> on all of them? Because the pairwise conditions don't force the triple. Flip a
> fair coin twice. Let A be heads on the first toss, B heads on the second, and C
> the event that the two tosses differ. Each has probability one-half, and any two
> are independent — every pair multiplies correctly to one quarter.
> <bookmark mark="fail"/> But all three together? A and B means two heads, which
> rules C out entirely — so the triple probability is zero, while the product of
> the three is one-eighth. Pairwise independent, yet not independent. The triple
> condition is genuinely extra: it neither follows from the pairs nor implies
> them.

**Cues**
- `define`: the full condition Pr(∩_{i∈S} A_i) = ∏_{i∈S} Pr(A_i) for every subset S; for three events, 3 pairs + the triple.
- `pairwise`: coin-twice sample space {HH, HT, TH, TT}; A = H first, B = H second, C = differ; each 1/2, each pair = 1/4.
- `fail`: Pr(A ∩ B ∩ C) = 0 ≠ 1/8 = Pr(A)Pr(B)Pr(C); "pairwise ⇏ mutual" in accent.

---

## Beat: conditional-independence  (scene: ConditionalIndependence)

> Finally, independence can live inside a condition. <bookmark mark="define"/> Two
> events are conditionally independent given B if they factor under the
> conditional law: Pr of A-one-and-A-two given B equals Pr of A-one given B times
> Pr of A-two given B. Because the conditional law is itself a genuine probability
> law, this is just ordinary independence — measured in the world where B is
> known. <bookmark mark="create"/> Conditioning can create independence. Toss a
> coin until heads is seen for the first time; let B be the event that it took more
> than one toss, A-one be the event that the count is even, and A-two be the event
> that the count remains under six. Unconditionally, A-one and A-two are not
> independent: their joint probability is five-sixteenths, which does not match the
> product of their separate probabilities. But given B they factor cleanly: the
> conditional probability of A-one is two-thirds, the conditional probability of
> A-two is fifteen-sixteenths, and their joint conditional probability is
> five-eighths — exactly two-thirds times fifteen-sixteenths. Conditioning made
> them independent. <bookmark mark="destroy"/> Conditioning can destroy
> independence. A red-die two and a blue-die six are
> independent outright — one thirty-sixth. But condition on the sum being odd: two
> plus six is eight, which is even, so the joint conditional probability is zero,
> while each event alone still has conditional probability one-sixth. The condition
> broke their independence. <bookmark mark="outro"/> So independence is not one idea
> but a family of them — sensitive to how many events you weigh, and to what you
> already know. That completes conditional probability.

**Cues**
- `define`: Pr(A_1 ∩ A_2 \mid B) = Pr(A_1 \mid B) Pr(A_2 \mid B).
- `create`: coin-until-heads; A_1 even, A_2 < 6, given B = "more than one toss"; 5/8 = (2/3)(15/16); note not independent unconditionally.
- `destroy`: {r=2}, {b=6} independent (1/36) but Pr(· \mid \text{sum odd}) = 0 ≠ (1/6)(1/6).
- `outro`: key-idea card + bridge to random variables (next chapter).

---

## Cut list (if over budget)
1. Drop the gambler's-fallacy aside in `independence` (keep disjoint ≠ independent).
2. Trim the two-dice detail in `independence` to the independent case only.
3. Compress the coin-until-heads arithmetic in `conditional-independence` to the factorization line.
