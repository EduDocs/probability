---
slug: 10-continuity-measure
title: Continuity of Probability and a Measure-Theory View
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 10-continuity-measure.md
derived_from_sha256: be36bd250706e9c255d58dc01ebc6e7ea0feccd0fd9aeda5edc8c1cf365bceff
provenance_stamped: 2026-07-06
target_scene_file: scenes/continuity_measure.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "See how probability respects limits of monotone event sequences, and why an honest theory restricts attention to a sigma-field of admissible events."
  recap: "Last video: the three families of models -- finite, countably infinite, and uncountably infinite sample spaces."
  key_idea: "Probability is continuous along monotone sequences of events -- Pr(A) = lim Pr(A_n) -- and on uncountable spaces it lives on a sigma-field of admissible events, the domain of measure theory."
  bridge: "That completes the probabilistic model: a sample space and a probability law. Everything ahead builds on this foundation."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 300
tolerance_sec: 45

estimated_runtime_sec: 300
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 95
    est_sec: 38
    measured_sec: null
    sync_points: []
  - id: continuity-below
    scene_class: ContinuityFromBelow
    narration_words: 195
    est_sec: 78
    measured_sec: null
    sync_points: [increasing, statement, shells, proof]
  - id: continuity-above
    scene_class: ContinuityFromAbove
    narration_words: 140
    est_sec: 56
    measured_sec: null
    sync_points: [decreasing, complement, name]
  - id: measure-theory
    scene_class: MeasureTheory
    narration_words: 235
    est_sec: 94
    measured_sec: null
    sync_points: [ladder, everysubset, sigmafield, unify, outro]
---

# Video Script — Continuity of Probability and a Measure-Theory View

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> In the last video we sorted sample spaces into three families — finite,
> countably infinite, and uncountably infinite. This short coda ties off two
> topics that complete the picture. First, the continuity of
> probability: the fact that probability behaves well under limits, when a
> sequence of events steadily grows or steadily shrinks. And second, a glimpse
> of measure theory — the honest answer to a question the continuous case forces
> on us: can we really assign a probability to every subset of the sample space?

**Animation cue:** title card recapping the three families, then a two-item
outline — continuity of probability, and a measure-theory view.

---

## Beat: continuity-below  (scene: ContinuityFromBelow)

> Start with a sequence of events that only grows. <bookmark mark="increasing"/>
> A-one sits inside A-two, which sits inside A-three, and so on — an increasing
> sequence — and we write A for their union, the limit they fill out. Picture
> nested regions, each containing the last, expanding toward A. <bookmark
> mark="statement"/> Continuity from below says exactly what you would hope: the
> probability of the limit is the limit of the probabilities. Pr of A equals the
> limit, as n goes to infinity, of Pr of A-n. <bookmark mark="shells"/> Why is it
> true? The trick is to disjointify. Let B-one be A-one, and each later B-k be
> the new ring that A-k adds to A-k-minus-one. These shells are disjoint, the
> first n of them union to exactly A-n, and all of them together union to A.
> <bookmark mark="proof"/> Now apply the third axiom — countable additivity. Pr
> of A is the infinite sum of the shell probabilities, which is the limit of the
> partial sums, which is just the limit of Pr of A-n. The axiom of countable
> additivity is doing all the work.

**Cues**
- `increasing`: nested growing regions A_1 ⊂ A_2 ⊂ A_3 ⊂ ... inside Omega; union A.
- `statement`: write Pr(A) = lim_{n→∞} Pr(A_n).
- `shells`: recolor the rings B_1 = A_1, B_k = A_k − A_{k−1}; note they are disjoint.
- `proof`: Pr(A) = Σ Pr(B_k) = lim Σ_{k≤n} Pr(B_k) = lim Pr(A_n).

---

## Beat: continuity-above  (scene: ContinuityFromAbove)

> The mirror image holds for a sequence that only shrinks. <bookmark
> mark="decreasing"/> Now A-one contains A-two contains A-three, and so on — a
> decreasing sequence — closing down onto their intersection A, the part common
> to all of them. <bookmark mark="complement"/> We do not need a new proof. Flip
> to complements: as the A-k shrink, their complements grow, an increasing
> sequence we already understand. Apply continuity from below to the complements,
> then use the complement rule to flip back, and out comes the same conclusion:
> Pr of A equals the limit of Pr of A-n. <bookmark mark="name"/> Continuity from
> below, for growing events, and continuity from above, for shrinking ones,
> together go by one name: the continuity of probability. It is what lets us pass
> to the limit — to talk about what happens eventually, not just at every finite
> stage.

**Cues**
- `decreasing`: nested shrinking regions A_1 ⊃ A_2 ⊃ A_3 ⊃ ...; intersection A.
- `complement`: show A_k^c increasing; "apply continuity from below to complements."
- `name`: write Pr(A) = lim Pr(A_n); banner "the continuity of probability."

---

## Beat: measure-theory  (scene: MeasureTheory)

> One last honesty. <bookmark mark="ladder"/> Our intuition for the infinite
> climbs a ladder. The finite we grasp directly. The countably infinite — the
> integers, the rationals — we can at least list, one element after another. The
> uncountable — the real numbers — cannot be listed at all; there are strictly
> more of them. We use the finite to understand the countable, and the countable
> to reach for the uncountable. <bookmark mark="everysubset"/> Now the catch. It
> is tempting to assign a probability to every single subset of the sample space.
> For a finite or countable Omega, fine. But for an uncountable Omega, this leads
> to genuine contradictions that cannot be patched. You simply cannot weigh every
> subset at once. <bookmark mark="sigmafield"/> The resolution is to step back and
> only assign probabilities to a well-behaved sub-collection of events — closed
> under complements and countable unions. Such a collection is called a
> sigma-field, and the events in it are the admissible ones. <bookmark
> mark="unify"/> Studying sigma-fields and the measures defined on them is the
> subject of measure theory, and measure-theoretic probability gives one unified
> framework for the discrete and the continuous alike. We are only pointing at the
> door here, not walking through it. <bookmark mark="outro"/> And that completes
> the probabilistic model: a sample space of outcomes, and a probability law that
> obeys the axioms and respects limits. Everything in the rest of the subject is
> built on this foundation.

**Cues**
- `ladder`: three rungs finite ⊂ countable ⊂ uncountable; arrows climbing.
- `everysubset`: "assign Pr to every subset?" — green check for finite/countable, red cross for uncountable.
- `sigmafield`: a box of "admissible events" closed under complement and countable union; label sigma-field.
- `unify`: "measure theory: one framework for discrete + continuous."
- `outro`: key-idea card + chapter-closing bridge.

---

## Cut list (if over budget)
1. Drop the partial-sum middle step in `continuity-below`'s `proof` (keep the endpoints).
2. Trim the cardinality ladder in `measure-theory` to one sentence.
3. Drop the "passing to the limit / eventually" remark in `continuity-above`'s `name`.
