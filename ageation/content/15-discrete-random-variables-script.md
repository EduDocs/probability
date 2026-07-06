---
slug: 15-discrete-random-variables
title: Discrete Random Variables and the PMF
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 15-discrete-random-variables.md
derived_from_sha256: 8d5aa57522e36f42770bbf68940f324f8365de98fe172c0d1989dbedc31cf86e
provenance_stamped: 2026-07-06
target_scene_file: scenes/discrete_random_variables.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Turn the outcomes of an experiment into numbers, and describe those numbers with a probability mass function."
  recap: "Last chapter: independence -- when knowing one event tells you nothing about another."
  key_idea: "A discrete random variable is completely described by its probability mass function, p_X(x) = Pr(X = x)."
  bridge: "Next: the named distributions -- Bernoulli, binomial, Poisson, geometric, and uniform."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 480
tolerance_sec: 45

estimated_runtime_sec: 470
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 92
    est_sec: 37
    measured_sec: null
    sync_points: []
  - id: rv-mapping
    scene_class: RandomVariableMapping
    narration_words: 120
    est_sec: 48
    measured_sec: null
    sync_points: [show-omega, fire-arrows, many-to-one, definition]
  - id: discrete-rv
    scene_class: DiscreteRandomVariable
    narration_words: 95
    est_sec: 38
    measured_sec: null
    sync_points: [finite, countable]
  - id: pmf-definition
    scene_class: PMFDefinition
    narration_words: 180
    est_sec: 72
    measured_sec: null
    sync_points: [define, preimage, normalize, set-formula]
  - id: urn-example
    scene_class: UrnExample
    narration_words: 150
    est_sec: 60
    measured_sec: null
    sync_points: [setup, pmf, odd, outro]
---

# Video Script — Discrete Random Variables and the PMF

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last chapter we studied independence — when learning one event tells you
> nothing about another. Now the whole subject takes a turn. So far outcomes
> have been abstract things: a face of a die, a point in a sample space. In this
> chapter we attach a number to every outcome, and that single move unlocks
> sums, averages, and limits. We'll define a random variable as a function, focus
> on the discrete case, and describe it completely with one object — its
> probability mass function. Then we'll put a PMF to work on a small example.

**Animation cue:** title card + recap line (independence), then the objective and
a four-item outline (function, discrete, PMF, example).

---

## Beat: rv-mapping  (scene: RandomVariableMapping)

> Here is a sample space <bookmark mark="show-omega"/> Omega, with a handful of
> outcomes. A random variable is nothing mysterious: <bookmark mark="fire-arrows"/>
> it is simply a function that sends each outcome to a point on the real line.
> Roll a die, and the natural random variable is the number of dots on the top
> face — outcome to number. <bookmark mark="many-to-one"/> Notice that different
> outcomes are allowed to land on the same number; the map need not be
> one-to-one. Formally, <bookmark mark="definition"/> we write X maps Omega to
> the real numbers. That real number attached to an outcome is called the value
> of the random variable.

**Cues**
- `show-omega`: fade in the Omega box with colored outcomes.
- `fire-arrows`: lag-animate curved arrows to a number line.
- `many-to-one`: highlight two outcomes hitting the same target.
- `definition`: write `X : \Omega \to \mathbb{R}` along the bottom.

---

## Beat: discrete-rv  (scene: DiscreteRandomVariable)

> The random variables we study first are the discrete ones. <bookmark mark="finite"/>
> A random variable is discrete when its range — the set of values it can take —
> is finite or countable. A die gives a finite range, one through six.
> <bookmark mark="countable"/> But discrete does not mean finite. Toss a coin
> repeatedly until the first head, and record how many tosses it took. That count
> can be one, two, three, and on forever — a countably infinite range. Both are
> discrete; what they share is that we can list their values one by one.

**Cues**
- `finite`: show `X(\Omega) = \{1,\dots,6\}` next to a die.
- `countable`: show `\{1, 2, 3, \dots\}` for coin-until-heads; arrow off to the right.

---

## Beat: pmf-definition  (scene: PMFDefinition)

> To describe a discrete random variable completely, we only need to say how much
> probability sits on each value. <bookmark mark="define"/> That is the
> probability mass function. The mass of x, written little-p sub-X of x, is just
> the probability that X equals x. <bookmark mark="preimage"/> And "X equals x"
> is really an event back in the sample space: the set of all outcomes that X
> maps to x. That set is the preimage of x, and its probability is the mass. So
> the PMF simply pushes the probability law forward, from the sample space onto
> the number line. <bookmark mark="normalize"/> As x ranges over all the values,
> these preimages are disjoint and cover the whole sample space — they partition
> it — so the masses must add up to exactly one. <bookmark mark="set-formula"/>
> And once we have the PMF, the probability that X lands anywhere in a set S is
> just the sum of the masses over S. The PMF is the whole story.

**Cues**
- `define`: `p_X(x) = \Pr(X = x)` in accent.
- `preimage`: shade `\{\omega : X(\omega) = x\}` inside Omega; `= \Pr(X^{-1}(x))`.
- `normalize`: `\sum_{x \in X(\Omega)} p_X(x) = 1`; bars over the axis.
- `set-formula`: `\Pr(X \in S) = \sum_{x \in S} p_X(x)`.

---

## Beat: urn-example  (scene: UrnExample)

> Let's make it concrete. <bookmark mark="setup"/> An urn holds three balls,
> numbered one, two, and three. We draw two of them without replacement, and we
> record the order — so there are six equally likely outcomes. Let the random
> variable X be the sum of the two numbers drawn. <bookmark mark="pmf"/> Work out
> the sums: they can only be three, four, or five, and each occurs for exactly two
> of the six outcomes. So the PMF is one-third on three, one-third on four,
> one-third on five. <bookmark mark="odd"/> Now suppose we want the probability
> that the sum is odd. The odd values are three and five, so we just add their
> masses: one-third plus one-third is two-thirds. <bookmark mark="outro"/> That is
> the pattern for the whole chapter — build the PMF, then sum the mass over the
> values you care about. A discrete random variable is completely described by its
> probability mass function. Next, we meet named distributions.

**Cues**
- `setup`: list the six ordered pairs; note equiprobable.
- `pmf`: three bars at 3, 4, 5, each `1/3`.
- `odd`: shade bars 3 and 5; `\Pr(\text{odd}) = 1/3 + 1/3 = 2/3`.
- `outro`: key-idea card + bridge to the named distributions.

---

## Cut list (if over budget)
1. Trim the die aside in `rv-mapping` to the arrows only.
2. Drop the countably-infinite half of `discrete-rv` (keep the finite case).
3. Compress `pmf-definition` by folding `set-formula` into the urn example.
