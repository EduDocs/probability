---
slug: 02-functions
title: Functions
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 02-functions.md
derived_from_sha256: 7ec838e33f1185d443e1d5b8e87a0fac8020b3bcdd2058b4257df3981f27498c
provenance_stamped: 2026-07-06
target_scene_file: scenes/functions.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "See how a function -- a single-valued relation -- turns sets of outcomes into numbers."
  recap: "Last video we built the language of sets: operations, partitions, and the Cartesian product."
  key_idea: "A function sends each input to exactly one output; its preimage is the seed of the random variable."
  bridge: "Next: combinatorics -- counting the outcomes themselves."

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
estimated_runtime_sec: 562
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 84
    est_sec: 34
    measured_sec: null
    sync_points: []
  - id: relations-to-functions
    scene_class: RelationsToFunctions
    narration_words: 210
    est_sec: 84
    measured_sec: null
    sync_points: [relation, single-valued, notation]
  - id: domain-codomain
    scene_class: DomainCodomain
    narration_words: 188
    est_sec: 75
    measured_sec: null
    sync_points: [map, triple, example]
  - id: image-preimage
    scene_class: ImagePreimage
    narration_words: 246
    est_sec: 98
    measured_sec: null
    sync_points: [image, preimage, level-set, two-points]
  - id: properties
    scene_class: InjSurjBij
    narration_words: 220
    est_sec: 88
    measured_sec: null
    sync_points: [injective, surjective, bijective, inverse]
  - id: indicator
    scene_class: IndicatorFunction
    narration_words: 168
    est_sec: 67
    measured_sec: null
    sync_points: [define, evaluate, bernoulli]
  - id: tie-back
    scene_class: SetTheoryAndProbability
    narration_words: 182
    est_sec: 73
    measured_sec: null
    sync_points: [omega, partition, preimage, outro]
---

# Video Script — Functions

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker: in the generated scene it becomes a *separate
sequential* `with self.voiceover(...)` block, and the corresponding animation is
played for that block's `tracker.duration`. No Whisper / word-level timing is
required.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, we built the language of sets — operations, partitions, and the
> Cartesian product. Now we put that language to work. A function is a special
> kind of relation, and it is the bridge from sets of outcomes to numbers we can
> compute with. In this video we define relations and functions, meet the
> domain, codomain, image, and preimage, sort functions into one-to-one and
> onto, and finish with the indicator function — our first real taste of
> probability.

**Animation cue:** title card with a one-line recap of Sets, then reveal the
outline items one per clause.

---

## Beat: relations-to-functions  (scene: RelationsToFunctions)

> Recall the Cartesian product: all ordered pairs with a first entry from X and
> a second from Y. <bookmark mark="relation"/> A relation between X and Y is
> simply any subset of that product. When a pair x comma y belongs to the
> relation, we say x is related to y. Think of it as a bundle of arrows from X
> to Y — any arrows at all. <bookmark mark="single-valued"/> A function is a
> relation with one extra rule: it is single-valued. For every element of X
> there is one, and only one, element of Y that it points to. No element of the
> domain is left without an arrow, and none has two. That unique partner is
> written f of x. <bookmark mark="notation"/> So a function is exactly a relation
> that passes the single-valued test: from each x in X, exactly one arrow leaves.
> The rule that produces f of x from x is called the rule of correspondence.

**Cues**
- `relation`: draw ovals X and Y with several arrows (a messy relation).
- `single-valued`: prune to exactly one outgoing arrow per element of X.
- `notation`: write f(x) = y beside the surviving arrows.

---

## Beat: domain-codomain  (scene: DomainCodomain)

> Two sets come with every function. <bookmark mark="map"/> The domain is the set
> it is defined on — the inputs that are allowed. The codomain is the set the
> outputs are constrained to lie in. We capture both with the notation f maps X
> to Y, where X is the domain and Y the codomain. <bookmark mark="triple"/>
> Strictly speaking, a function is a triple: the domain, the codomain, and the
> graph — that single-valued subset of the Cartesian product. The intuitive
> picture and the formal triple say the same thing. <bookmark mark="example"/>
> Here is a concrete example: f maps the real numbers to the real numbers, with
> f of x equal to x squared. The domain and codomain are both the real line, and
> the rule of correspondence is x maps to x squared.

**Cues**
- `map`: write `f : X -> Y`, label domain under X, codomain under Y.
- `triple`: show the triple `(X, Y, f)` with the graph as a subset of `X x Y`.
- `example`: write `f(x) = x^2` and the map `x |-> x^2`.

---

## Beat: image-preimage  (scene: ImagePreimage)

> Two more sets are attached to every function. <bookmark mark="image"/> The image
> is the set of values the function actually attains — all the f of x as x ranges
> over the domain. It is a subset of the codomain, and need not fill it.
> <bookmark mark="preimage"/> Going the other way: the preimage of a set T is the
> collection of all inputs that land in T — every x whose output f of x lies in
> T. <bookmark mark="level-set"/> The most useful case is the preimage of a
> single value, called its level set: all the x that map to that one value.
> <bookmark mark="two-points"/> And here is the crucial fact. The preimage of a
> single value can contain many arguments. Take f of x equal to x squared, and
> draw the horizontal line at height c. It meets the parabola at minus root c and
> plus root c — so the preimage of c is two points. One output, several inputs.
> Hold on to this picture: pulling a value back to the set of inputs that produce
> it is exactly how a random variable will work.

**Cues**
- `image`: shade the image as a subset of the codomain.
- `preimage`: highlight the inputs mapping into a target set T.
- `level-set`: draw the parabola `f(x) = x^2`.
- `two-points`: horizontal line at `c`, mark `-sqrt(c)` and `+sqrt(c)`.

---

## Beat: properties  (scene: InjSurjBij)

> Functions come in useful flavors. <bookmark mark="injective"/> A function is
> injective, or one-to-one, if it never sends two different inputs to the same
> output. Distinct inputs, distinct outputs — no collisions. <bookmark
> mark="surjective"/> A function is surjective, or onto, if its image is the
> whole codomain. Every target value is hit by at least one input; nothing in the
> codomain is missed. <bookmark mark="bijective"/> A function that is both
> one-to-one and onto is called a bijection. Every output is hit exactly once.
> <bookmark mark="inverse"/> And that is precisely the condition for an inverse
> to exist: a function has an inverse exactly when it is a bijection. Then the
> preimage of every single value is itself a single point, and the inverse maps
> Y back to X, undoing the original.

**Cues**
- `injective`: arrow diagram with distinct inputs to distinct outputs.
- `surjective`: arrow diagram covering every element of the codomain.
- `bijective`: a perfect pairing, every output hit exactly once.
- `inverse`: reverse the arrows to show `f^{-1} : Y -> X`.

---

## Beat: indicator  (scene: IndicatorFunction)

> Here is the function that opens the door to probability: the indicator
> function. <bookmark mark="define"/> Fix a subset S of the universal set Omega.
> The indicator of S maps Omega to just two values, zero and one. <bookmark
> mark="evaluate"/> For an outcome omega, the indicator is one when omega is in
> S, and zero when it is not. In words, it simply reports whether its input
> belongs to S — one for yes, zero for no. <bookmark mark="bernoulli"/> When
> Omega is a sample space, the indicator of S reports whether an observed outcome
> fell in S. That single zero-or-one readout is the seed of the Bernoulli random
> variable, which we will meet in full later in the course.

**Cues**
- `define`: `1_S : Omega -> {0, 1}` with the Omega box and S shaded.
- `evaluate`: show the two-case definition; 1 inside S, 0 outside.
- `bernoulli`: tag the indicator as the seed of the Bernoulli random variable.

---

## Beat: tie-back  (scene: SetTheoryAndProbability)

> Step back and look at what Chapter one has assembled, because every piece
> reappears in a probabilistic guise. <bookmark mark="omega"/> The universal set
> Omega becomes the sample space of an experiment. <bookmark mark="partition"/> A
> partition of it underlies the law of total probability — breaking a question
> into disjoint cases. <bookmark mark="preimage"/> The preimage of a function is
> the mechanism behind random variables, and the Cartesian product lets us
> describe several quantities jointly. <bookmark mark="outro"/> So the set theory
> was never a detour. It is the scaffolding the whole subject is built on. With
> sets and functions in hand, we are ready to start counting — which is exactly
> what the next chapter, combinatorics, is about.

**Cues**
- `omega`: `Omega -> sample space`.
- `partition`: `partition -> law of total probability`.
- `preimage`: `preimage -> random variable`, `Cartesian product -> joint`.
- `outro`: key-idea card + bridge to Combinatorics.

---

## Cut list (if over budget)
1. Trim `properties` to injective + surjective + the one-line bijection (drop
   the explicit inverse-arrow animation).
2. Shorten `image-preimage` by stating the image in one sentence and spending
   the time on the preimage / level-set picture (the payoff).
3. Compress the `tie-back` table to three rows (Omega, partition, preimage).
