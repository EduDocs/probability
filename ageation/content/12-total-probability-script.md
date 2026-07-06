---
slug: 12-total-probability
title: The Total Probability Theorem
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 12-total-probability.md
derived_from_sha256: 22a2cfce7583a77f555429ef8724b2ad0f1ab8f71e608022c0193fd6b768aba2
provenance_stamped: 2026-07-06
target_scene_file: scenes/total_probability.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Compute the overall probability of an event by splitting the sample space into cases -- divide and conquer."
  recap: "Last video: conditional probability, Pr(A | B) = Pr(A ∩ B) / Pr(B), and the chain rule."
  key_idea: "If the events A_k partition the sample space, then Pr(B) = Σ Pr(A_k) Pr(B | A_k) -- the total probability of B is the weighted average of its conditional probabilities."
  bridge: "Next: Bayes' rule -- inverting these conditionals to update beliefs, with the Monty Hall problem."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 360
tolerance_sec: 45

estimated_runtime_sec: 360
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 105
    est_sec: 42
    measured_sec: null
    sync_points: []
  - id: partition
    scene_class: Partitioning
    narration_words: 110
    est_sec: 44
    measured_sec: null
    sync_points: [define, tile]
  - id: theorem
    scene_class: TotalProbability
    narration_words: 190
    est_sec: 76
    measured_sec: null
    sync_points: [slice, add, condition]
  - id: example
    scene_class: TwoUrns
    narration_words: 210
    est_sec: 84
    measured_sec: null
    sync_points: [setup, branch, combine, outro]
---

# Video Script — The Total Probability Theorem

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video we learned to condition — to update the probability of an event once
> we know another has occurred. Now we use conditioning for a different job:
> computing the plain, unconditional probability of an event that is hard to
> attack head-on. The trick is divide and conquer. Break the sample space into a
> handful of scenarios, work out the probability inside each one where it's easy,
> then stitch the pieces back together. That recipe is the total probability
> theorem, and it is the bridge to Bayes' rule in the next video. First we need
> the right way to carve up the sample space: a partition.

**Animation cue:** title card, recap line (conditional probability + chain rule),
then the goal — an unconditional probability computed by conditioning on cases.

---

## Beat: partition  (scene: Partitioning)

> Recall the idea of a partition. <bookmark mark="define"/> A collection of events
> A-one, A-two, up to A-n is a partition of the sample space when two things hold:
> the events are disjoint — no two overlap — and together they cover everything,
> their union is all of Omega. <bookmark mark="tile"/> Picture Omega as a
> rectangle sliced cleanly into colored tiles. Every outcome lands in exactly one
> tile — no gaps, no double-counting. That "exactly one" is the whole point: it is
> what will let us add probabilities without any fear of overlap.

**Cues**
- `define`: write the partition definition — disjoint (A_i ∩ A_j = ∅) and ∪ A_k = Ω.
- `tile`: an Omega rectangle sliced into disjoint colored tiles A_1, A_2, A_3 that exactly cover it.

---

## Beat: theorem  (scene: TotalProbability)

> Now drop an event B onto this partition. <bookmark mark="slice"/> Wherever B
> falls, the tiles cut it into pieces — the part of B inside A-one, the part
> inside A-two, and so on. Since the tiles are disjoint, these pieces are disjoint
> too, and together they reassemble all of B. <bookmark mark="add"/> By the third
> axiom, the probability of B is just the sum of the probabilities of those pieces
> — the probability of B-and-A-one, plus B-and-A-two, and so on across the
> partition. <bookmark mark="condition"/> Here is the key move. Each piece, by the
> product rule, is the probability of its tile times the conditional probability
> of B given that tile. Substitute, and out comes the total probability theorem:
> the probability of B equals the sum over k of the probability of A-k times the
> probability of B given A-k. Read it as a weighted average — the chance of B in
> each scenario, weighted by how likely that scenario is.

**Cues**
- `slice`: overlay event B (a shape) across the tiles; highlight the pieces B ∩ A_1, B ∩ A_2, B ∩ A_3.
- `add`: write Pr(B) = Pr(B ∩ A_1) + Pr(B ∩ A_2) + ⋯ + Pr(B ∩ A_n).
- `condition`: substitute Pr(B ∩ A_k) = Pr(A_k) Pr(B \mid A_k); land the accent theorem Pr(B) = Σ_k Pr(A_k) Pr(B \mid A_k).

---

## Beat: example  (scene: TwoUrns)

> Let's put it to work. <bookmark mark="setup"/> Two urns sit on a table. The
> first holds five green balls and three red; the second, three green and nine
> red. We flip a fair coin to pick an urn — each with probability one-half — then
> draw a single ball. What is the probability it's green? <bookmark mark="branch"/>
> Condition on the urn. If we picked urn one, green has probability five over
> eight. If urn two, green has probability three over twelve — one quarter.
> <bookmark mark="combine"/> Total probability stitches them together: one-half
> times five-eighths, plus one-half times three-twelfths, which comes to
> seven-sixteenths. Notice we never had to reason about both urns at once — we
> solved each easy case and let the theorem average them. <bookmark mark="outro"/>
> That is the power of conditioning as a computational tool: divide the world into
> cases, conquer each, and average. Next we run this machinery in reverse — given
> that the ball came out green, which urn did it most likely come from? That
> inversion is Bayes' rule.

**Cues**
- `setup`: two urns, U_1 = 5 green / 3 red, U_2 = 3 green / 9 red; a fair coin picks the urn (1/2 each).
- `branch`: a two-branch tree; Pr(g \mid U_1) = 5/8, Pr(g \mid U_2) = 3/12.
- `combine`: Pr(g) = (1/2)(5/8) + (1/2)(3/12) = 7/16 (accent).
- `outro`: key-idea card + bridge to Bayes' rule (inverting the tree).

---

## Cut list (if over budget)
1. Shorten the partition beat — fold the definition into the theorem's first line.
2. Drop the "weighted average" gloss in `theorem`.
3. Trim the closing bridge in `example` to one sentence.
