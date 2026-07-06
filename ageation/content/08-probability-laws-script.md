---
slug: 08-probability-laws
title: Probability Laws
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 08-probability-laws.md
derived_from_sha256: 9882f44c56fa79e61bfb7511be2687954788c14a4b6cca9427f45be43801de46
provenance_stamped: 2026-07-06
target_scene_file: scenes/probability_laws.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Build probability from three axioms, and derive the rules for combining events."
  recap: "Last video: sample spaces and events -- the stage every experiment plays out on."
  key_idea: "Three axioms -- nonnegativity, normalization, additivity -- generate every rule for combining probabilities."
  bridge: "Next: three families of models -- finite, countably infinite, and uncountably infinite."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 570
tolerance_sec: 45

estimated_runtime_sec: 575
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 96
    est_sec: 38
    measured_sec: null
    sync_points: []
  - id: three-axioms
    scene_class: ThreeAxioms
    narration_words: 190
    est_sec: 78
    measured_sec: null
    sync_points: [assign, ax1, ax2, ax3]
  - id: additivity
    scene_class: Additivity
    narration_words: 200
    est_sec: 82
    measured_sec: null
    sync_points: [finite, countable, sum]
  - id: consequences
    scene_class: Consequences
    narration_words: 300
    est_sec: 120
    measured_sec: null
    sync_points: [complement, empty, mono, conjunction]
  - id: union-formula
    scene_class: UnionFormula
    narration_words: 150
    est_sec: 62
    measured_sec: null
    sync_points: [venn, subtract, inclusion]
  - id: union-bound
    scene_class: UnionBound
    narration_words: 285
    est_sec: 116
    measured_sec: null
    sync_points: [bound, urn, compute, exact, outro]
---

# Video Script — Probability Laws

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> In the last video we built sample spaces and events — the stage every
> experiment plays out on. Now we put numbers on those events. A probability law
> is the rule that assigns each event its likelihood, and remarkably, it rests on
> just three axioms. In this video we meet the three axioms themselves; the
> consequences they force, like the complement rule and monotonicity; the formula
> for the union of two events; and the union bound, a workhorse inequality. By the
> end, every rule you will ever use for combining probabilities will trace back to
> these three axioms.

**Animation cue:** title card recapping sample spaces, then the four-item outline.

---

## Beat: three-axioms  (scene: ThreeAxioms)

> Start with the central object. <bookmark mark="assign"/> A probability law
> assigns to every event A a single number, written Pr of A, that measures how
> likely A is. Picture the sample space Omega as a region, and an event A as a
> patch inside it; the probability of A is the amount of mass sitting on that
> patch. In other branches of mathematics the very same object is called a
> probability measure — a name we will follow up when we reach measure theory.
> <bookmark mark="ax1"/> The first axiom is nonnegativity: every event gets a
> probability that is at least zero. Weights are never negative. <bookmark
> mark="ax2"/> The second is normalization: the whole sample space carries
> probability exactly one. Something in Omega is certain to happen, and certainty
> is one. <bookmark mark="ax3"/> The third is additivity. If two events A and B
> are disjoint — they share no outcomes — then the probability of their union is
> just the sum of their probabilities. Non-overlapping masses simply add. That
> third axiom is the engine of the whole theory, so let us spend some time with it.

**Cues**
- `assign`: Omega box with a shaded event A; the three-axiom list to the side.
- `ax1`: reveal nonnegativity; indicate the shaded mass.
- `ax2`: reveal normalization; indicate the whole Omega box.
- `ax3`: reveal additivity (for disjoint A, B).

---

## Beat: additivity  (scene: Additivity)

> Here are two disjoint events, A on the left and B on the right, with no overlap
> between them. <bookmark mark="finite"/> Because they are disjoint, the
> probability of A-or-B is exactly the probability of A plus the probability of B.
> Nothing is double counted, because there is no shared region to count twice.
> <bookmark mark="countable"/> But the axiom says more. Additivity holds not just
> for two disjoint events, but for a whole infinite sequence of them. Take
> disjoint events A-one, A-two, A-three, and so on, tiling the sample space with
> no overlaps. <bookmark mark="sum"/> The probability of their union — the chance
> that some one of them occurs — equals the infinite sum of the individual
> probabilities. Picture the pieces as a half, then a quarter, then an eighth, and
> on forever: the masses add up to the whole. This is countable additivity, and it
> is the property that lets probability handle limits and genuinely infinite
> experiments, not just finite ones.

**Cues**
- `finite`: two disjoint shaded blobs; write Pr(A union B) = Pr(A) + Pr(B).
- `countable`: a unit bar split into shrinking disjoint pieces A_1, A_2, ...
- `sum`: write Pr(union A_k) = sum Pr(A_k).

---

## Beat: consequences  (scene: Consequences)

> The axioms immediately force a string of useful rules. <bookmark
> mark="complement"/> Take any event A and its complement A-c — everything in
> Omega outside A. They are disjoint, and together they fill the whole sample
> space, so by normalization and additivity their probabilities add to one.
> Rearranging, the probability of the complement is one minus the probability of
> A. <bookmark mark="empty"/> As a special case, let A be all of Omega: its
> complement is the empty set, so the impossible event carries probability zero.
> <bookmark mark="mono"/> Next, monotonicity. Suppose A sits inside B. Then we
> split B into A together with the part of B outside A — two disjoint pieces.
> Additivity says Pr of B equals Pr of A plus the probability of that leftover,
> and since probabilities are never negative, Pr of A is at most Pr of B. A bigger
> event is at least as likely. <bookmark mark="conjunction"/> This has a
> consequence human intuition routinely violates. Because A-and-B sits inside A,
> the probability of a conjunction can never exceed the probability of A alone —
> adding detail to a description can only lower its probability, never raise it.
> Yet people reliably get this backwards. In a classic experiment, respondents
> were told that someone is politically active and outspoken, then asked which is
> more likely: that the person is a bank teller who is also active in a social
> movement, or simply a bank teller. Most people chose the former — even though it
> is a special case of the latter, and so can only be less probable. The richer,
> more representative story simply feels more likely. Ranking the more specific
> scenario above one of its own constituents is the conjunction fallacy.

**Cues**
- `complement`: shade A, then shade its complement; write Pr(A^c) = 1 - Pr(A).
- `empty`: write Pr(empty) = 0.
- `mono`: nested circles A subset B; shade the ring B - A; write the inequality.
- `conjunction`: write Pr(A intersect B) <= Pr(A); the bank-teller experiment (three lines), then "the conjunction fallacy" in accent at the bottom, appearing last.

---

## Beat: union-formula  (scene: UnionFormula)

> What if the two events do overlap? <bookmark mark="venn"/> Here are A and B with
> a shared lens in the middle. If we simply add Pr of A and Pr of B, we count that
> overlapping lens twice — once for each circle. <bookmark mark="subtract"/> So we
> subtract it back out once. In general, the probability of A-union-B equals Pr of
> A, plus Pr of B, minus the probability of their intersection. Add the parts, then correct
> for the double counting — and notice that when A and B are disjoint the
> intersection is empty, and we recover plain additivity. <bookmark
> mark="inclusion"/> The same bookkeeping extends to any number of events,
> alternately adding and subtracting the overlaps of overlaps; that general
> pattern is the inclusion–exclusion principle. We state it and move on.

**Cues**
- `venn`: two overlapping circles A, B; highlight the intersection lens.
- `subtract`: write Pr(A union B) = Pr(A) + Pr(B) - Pr(A intersect B).
- `inclusion`: one-line inclusion-exclusion for n events.

---

## Beat: union-bound  (scene: UnionBound)

> Sometimes the intersections are hopelessly hard to compute. Then we settle for
> a bound. <bookmark mark="bound"/> Drop the subtracted overlap terms from the
> union formula and the right side can only grow, so the probability of a union of
> events is at most the sum of their probabilities. Applied repeatedly — a quick
> induction — this gives the union bound, also called Boole's inequality, for any
> number of events. <bookmark mark="urn"/> Here it earns its keep. An urn holds
> nine hundred ninety blue balls and ten red ones. Five people each draw a ball,
> without replacement, and we want the probability that at least one of them draws
> red — the union of the five events "person k draws red". <bookmark
> mark="compute"/> Each person, on their own, has a one-in-a-hundred chance of
> red. The union bound just adds those up: five times one-hundredth is
> one-twentieth, or zero point zero five. That is an upper bound, and it took
> almost no work. <bookmark mark="exact"/> The exact answer needs the probability
> that nobody draws red — a ratio of binomial coefficients — which comes to about
> zero point zero four nine. Remarkably close to the bound, and far harder to
> reach. That is exactly when the union bound shines: when the individual
> probabilities are simple but the joint event is not. As a second application,
> suppose each of the five people draws two balls and we ask for the probability
> that someone draws two reds. The same union bound applies with almost no extra
> work — five times the chance of a single person drawing two reds, which totals
> one in two thousand two hundred and twenty — yet the exact value here is
> genuinely hard to compute. That is exactly the situation the union bound was
> made for. <bookmark mark="outro"/> So
> the whole of this video rests on three axioms — nonnegativity, normalization,
> and additivity — and everything else, the complement rule, monotonicity, the
> union formula, and the union bound, follows from them. Next, we meet three
> families of probability models: finite, countably infinite, and uncountably
> infinite sample spaces.

**Cues**
- `bound`: write Pr(union A_k) <= sum Pr(A_k); name induction / Boole.
- `urn`: an urn of 990 blue + 10 red and 5 draw slots.
- `compute`: Pr(B_k) = 1/100; bound = 5/100 = 1/20.
- `exact`: 1 - C(990,5)/C(1000,5) ~ 0.049.
- second application: two balls each; bound 5*C(10,2)/C(1000,2) = 1/2220; exact much harder.
- `outro`: key-idea card + bridge to the three families of models.

---

## Cut list (if over budget)
1. Trim the conjunction-fallacy aside in `consequences` to one sentence.
2. Shorten the countable-additivity narration in `additivity` (keep the bar).
3. Drop the second sentence of the `inclusion` block in `union-formula`.
