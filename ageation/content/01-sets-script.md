---
slug: 01-sets
title: Sets
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 01-sets.md
derived_from_sha256: 9d1f44a4dfbab1c21626525b3cc691c264ae9e7dd37d5ea6f6efb8d8a525e6f6
provenance_stamped: 2026-07-06
target_scene_file: scenes/sets.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Build the language of sets that all of probability is written in."
  recap: "This is where the course begins -- no prerequisites."
  key_idea: "Sets, their operations, and the Cartesian product are the alphabet of probability."
  bridge: "Next: functions -- the single-valued relations that turn outcomes into numbers."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
target_runtime_sec: 600
tolerance_sec: 45         # build fails review if |actual - target| > tolerance

# --- Estimates vs measured -------------------------------------------------
estimated_runtime_sec: 567
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 78
    est_sec: 31
    measured_sec: null
    sync_points: []
  - id: what-is-a-set
    scene_class: WhatIsASet
    narration_words: 214
    est_sec: 86
    measured_sec: null
    sync_points: [show-omega, membership, subset, set-builder]
  - id: special-sets
    scene_class: SpecialSets
    narration_words: 150
    est_sec: 60
    measured_sec: null
    sync_points: [empty, universal, complement]
  - id: operations
    scene_class: SetOperations
    narration_words: 232
    est_sec: 93
    measured_sec: null
    sync_points: [union, intersection, disjoint, difference]
  - id: partition
    scene_class: Partition
    narration_words: 132
    est_sec: 53
    measured_sec: null
    sync_points: [slice, total-probability]
  - id: rules
    scene_class: AlgebraicRules
    narration_words: 226
    est_sec: 90
    measured_sec: null
    sync_points: [precedence, distributive, demorgan, indexed]
  - id: cartesian
    scene_class: CartesianProduct
    narration_words: 215
    est_sec: 86
    measured_sec: null
    sync_points: [pair, grid, outro]
---

# Video Script — Sets

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker: in the generated scene it becomes a *separate
sequential* `with self.voiceover(...)` block, and the corresponding animation is
played for that block's `tracker.duration`. No Whisper / word-level timing is
required.

---

## Beat: overview  (scene: ChapterOverview)

> Probability is built, from the ground up, on the language of sets. So that is
> where we begin. In this first video we meet sets and their elements, the two
> special sets that anchor everything, the operations that combine sets, the
> idea of a partition, the algebraic laws, and finally the Cartesian product.
> Get comfortable here, because every idea in this course casts a set-theoretic
> shadow.

**Animation cue:** title card in, then reveal the six outline items, one per
clause of the last two sentences.

---

## Beat: what-is-a-set  (scene: WhatIsASet)

> A set is simply a collection of objects, which we call its elements.
> <bookmark mark="show-omega"/> Picture a box holding a handful of distinct
> objects; each one is an element of the set. <bookmark mark="membership"/> If an
> object x belongs to a set S, we write x is in S. If it does not belong, we
> write x is not in S. Two sets are equal exactly when they contain precisely the
> same elements — equality of sets is equality of contents, nothing more.
> <bookmark mark="subset"/> Now suppose every element of S is also an element of
> T. Then we say S is a subset of T, written S is contained in T. Notice this
> allows S and T to be the same set. If S is contained in T but the two are
> genuinely different, we call S a proper subset. And here is a fact that will
> become useful: two sets are equal if and only if each is a subset of the other —
> that double inclusion is how you prove two sets are the same.
> <bookmark mark="set-builder"/> How do we actually specify a set? If it is
> small, we just list its elements inside braces. More often, we start from some
> collection and keep only the elements with a given property. For instance,
> starting from the integers, the even numbers are all x in the integers such
> that x is even. Read the braces as "the set of", and the bar as "such that".

**Cues**
- `show-omega`: fade in the box with colored, numbered balls.
- `membership`: highlight one ball as "in", flash an outside ball as "not in".
- `subset`: draw a smaller loop around some balls; show the containment symbol.
- `set-builder`: write the even-integers set-builder expression below.

---

## Beat: special-sets  (scene: SpecialSets)

> Two special sets deserve names. <bookmark mark="empty"/> The first is the empty
> set: the set with no elements at all, written as a slashed circle. It may look
> useless, but it is the natural answer whenever a condition is never met.
> <bookmark mark="universal"/> The second is the universal set, written 
> Omega — the collection of all objects of interest in the problem at hand. Once
> we fix Omega, every set we care about lives inside it. Remember the symbol
> Omega: in probability it has a special name, the sample space, the set of all
> possible outcomes of an experiment. <bookmark mark="complement"/> With a
> universal set in hand we can define the complement of a set S: everything in
> Omega that is not in S. We write it S with a small c. Picture Omega as the full
> frame and S as a region inside it; the complement is simply all the rest. As a
> sanity check, the complement of Omega itself is the empty set — outside of
> everything there is nothing.

**Cues**
- `empty`: write the empty-set symbol; brief "nothing here" beat.
- `universal`: draw the Omega frame; label it, then echo "sample space".
- `complement`: shade S, then shade the rest of Omega as the complement.

---

## Beat: operations  (scene: SetOperations)

> Now we combine sets. Throughout, picture two overlapping circles, S on the
> left and T on the right, sitting inside Omega. <bookmark mark="union"/> The
> union of S and T is everything that lies in S, or in T, or in both. On the
> picture, we shade both circles completely — the union holds anything caught by
> either one. <bookmark mark="intersection"/> The intersection is stricter: only
> the elements that lie in S and in T at the same time. That is the overlapping
> lens in the middle, and nothing else. <bookmark mark="disjoint"/> Sometimes
> two sets share no elements at all — their intersection is the empty set. We
> say such sets are disjoint, and we will lean on disjointness again and again,
> because for disjoint events probabilities simply add. <bookmark
> mark="difference"/> Finally, the difference S minus T is the set of elements
> that are in S but not in T. On the picture, take the left circle and carve away
> the overlap; what remains is S minus T. This is sometimes called the complement
> of T relative to S — the same idea as before, but measured inside S instead of
> inside all of Omega.

**Cues:** fixed pair of circles for all four; boolean-op shading per operation,
with the symbolic expression appearing above each.

---

## Beat: partition  (scene: Partition)

> Here is a structure worth singling out. <bookmark mark="slice"/> Take a set and
> break it into pieces so that no two pieces overlap, and together the pieces use
> up the whole set. A collection of nonempty, disjoint sets whose union is the
> whole thing is called a partition. Think of slicing a disk into wedges: every
> point of the disk lands in exactly one wedge — no gaps, no double counting.
> <bookmark mark="total-probability"/> Keep this picture in mind, because it is
> the backbone of one of the most useful results in the course. When the sample
> space is partitioned into cases, the probability of any event can be assembled,
> piece by piece, from its overlap with each case. That is the law of total
> probability, and a partition is exactly what makes it work.

**Cues**
- `slice`: a disk splits into three disjoint colored wedges, labelled S1, S2, S3.
- `total-probability`: overlay a faint event region crossing all wedges.

---

## Beat: rules  (scene: AlgebraicRules)

> Set operations obey an algebra, much like ordinary arithmetic.
> <bookmark mark="precedence"/> First, order matters, so we use parentheses to
> show precedence. R union, the quantity S intersect T, is generally a different
> set from the quantity R union S, all intersected with T. When in doubt,
> parenthesize. <bookmark mark="distributive"/> Two combinations, though, always
> agree — the distributive laws. Intersection distributes over union, and union
> distributes over intersection, exactly mirroring how multiplication
> distributes over addition. <bookmark mark="demorgan"/> The most useful
> identities are De Morgan's laws. They describe what happens when you take the
> complement of a combination. The complement of a union is the intersection of
> the complements; and the complement of an intersection is the union of the
> complements. In words: complement flips union into intersection, and back
> again. <bookmark mark="indexed"/> And this is not limited to two sets. Take the
> complement of a union over any index set, finite or infinite, and you get the
> intersection of all the complements. De Morgan scales to as many sets as you
> like — which is exactly why it is so heavily used later, when we manipulate
> whole families of events at once.

**Cues**
- `precedence`: two three-circle pictures, R∪(S∩T) vs (R∪S)∩T, shaded differently.
- `distributive`: write the two distributive identities.
- `demorgan`: shade the complement of a union, morph to the intersection of
  complements on the same circles.
- `indexed`: write the indexed De Morgan identity.

---

## Beat: cartesian  (scene: CartesianProduct)

> There is one more way to build a new set, and it is the one that lets
> probability talk about several things at once. <bookmark mark="pair"/> Start
> with an ordered pair: a first object and a second object, written in
> parentheses, where the order matters — the pair one comma a is not the pair a
> comma one. <bookmark mark="grid"/> The Cartesian product of S and T, written S
> cross T, is the set of all ordered pairs whose first entry comes from S and
> whose second entry comes from T. Take S to be one, two, three, and T to be a
> and b. Pair every element of S with every element of T, and you get a grid —
> here, six ordered pairs in all. That grid is the Cartesian product. When we
> reach random vectors later in the course, this is the construction that lets us
> describe two quantities jointly. <bookmark mark="outro"/> And that completes our
> tour of sets. We have the elements and subsets, the empty and universal sets
> and the complement, the operations and partitions, the algebraic laws, and the
> Cartesian product — the alphabet that the rest of probability is spelled with.
> In the next video we put this language to work and study functions: the special
> relations that send each input to exactly one output, and the bridge from
> outcomes to numbers.

**Cues**
- `pair`: show an ordered pair, emphasize order with a quick swap-and-reject.
- `grid`: build the 3x2 grid of paired balls from {1,2,3} x {a,b}.
- `outro`: fade to the key-idea card and the bridge to the Functions video.

---

## Cut list (if over budget)
1. Trim the `rules` beat to De Morgan only (drop the explicit distributive
   identities; mention them in one line).
2. Shorten `operations` by folding `difference` into a single sentence.
3. Drop the `total-probability` overlay in `partition` (keep the slicing).
