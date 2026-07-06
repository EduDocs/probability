---
slug: 17-functions-of-random-variables
title: Functions of Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 17-functions-of-random-variables.md
derived_from_sha256: a7672ebebad1350eeedfe40930d5229393f873559960312050d270fbfcc97da9
provenance_stamped: 2026-07-06
target_scene_file: scenes/functions_of_random_variables.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Transform a random variable into a new one, Y = g(X), and compute its PMF by summing mass over preimages."
  recap: "Last video: the named discrete distributions -- Bernoulli, binomial, Poisson, geometric, uniform."
  key_idea: "Y = g(X) is again a random variable, with p_Y(y) = sum of p_X(x) over all x that g maps to y."
  bridge: "Next chapter: expectation -- collapsing a whole PMF into a single number."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 480
tolerance_sec: 45

estimated_runtime_sec: 460
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 90
    est_sec: 36
    measured_sec: null
    sync_points: []
  - id: function-of-rv
    scene_class: FunctionOfRandomVariable
    narration_words: 130
    est_sec: 52
    measured_sec: null
    sync_points: [x-map, g-map, compose, discrete]
  - id: pmf-of-y
    scene_class: PMFofFunction
    narration_words: 140
    est_sec: 56
    measured_sec: null
    sync_points: [formula, merge, result]
  - id: affine
    scene_class: AffineExample
    narration_words: 100
    est_sec: 40
    measured_sec: null
    sync_points: [define, invert]
  - id: taxi
    scene_class: TaxiFare
    narration_words: 175
    est_sec: 70
    measured_sec: null
    sync_points: [setup, fare, pmf, outro]
---

# Video Script — Functions of Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video we collected the named discrete distributions. This time we do
> something with a random variable rather than just describe it. Very often the
> quantity we care about isn't what we measure directly — it's some function of
> it. A fare from a distance, a cost from a count, energy from a voltage. So the
> question is: if X is a random variable and we apply a function g to it, what is
> the new random variable Y equals g of X, and what is its PMF? We'll answer that,
> and then work the classic taxi-fare example end to end.

**Animation cue:** title card + recap (named distributions), objective, and a
short outline (Y = g(X), its PMF, affine case, worked example).

---

## Beat: function-of-rv  (scene: FunctionOfRandomVariable)

> Recall that a random variable is already a function of the outcome.
> <bookmark mark="x-map"/> X takes each outcome omega to a number x on the real
> line. <bookmark mark="g-map"/> Now apply a second function g to that number,
> sending x onward to a value y equals g of x. <bookmark mark="compose"/> Chain
> them together and you have a single map from outcomes straight to y — and since
> it assigns a number to every outcome, Y equals g of X is itself a random
> variable. <bookmark mark="discrete"/> And if X is discrete, so is Y. In fact g
> can only merge values, never split them, so Y takes no more values than X does.

**Cues**
- `x-map`: Omega box -> number line via `X` (arrows).
- `g-map`: a second number line; arrows `x \mapsto g(x)`.
- `compose`: direct arrows Omega -> `Y`; label `Y = g(X)`.
- `discrete`: note `|g(X(\Omega))| \le |X(\Omega)|`.

---

## Beat: pmf-of-y  (scene: PMFofFunction)

> How do we get the PMF of Y from the PMF of X? <bookmark mark="formula"/> For
> each value y, we collect the mass of every x that g sends to y. In symbols,
> p-sub-Y of y is the sum of p-sub-X of x over all x with g of x equal to y —
> exactly the preimage idea from the first video, applied one step further.
> <bookmark mark="merge"/> Picture it with a small example. Suppose g squares its
> input, and X takes the values minus-one, zero, and one. Then minus-one and one
> both map to one, so their two bars merge — their masses add — into a single bar
> of Y at the value one. <bookmark mark="result"/> Wherever g is many-to-one, bars
> of X pile up into taller bars of Y; and any y that g never produces simply gets
> zero.

**Cues**
- `formula`: `p_Y(y) = \sum_{\{x : g(x) = y\}} p_X(x)` in accent.
- `merge`: X-PMF at {-1,0,1} under `g(x)=x^2`; bars at -1 and 1 combine at y=1.
- `result`: resulting Y-PMF at {0, 1}.

---

## Beat: affine  (scene: AffineExample)

> One case is especially clean. <bookmark mark="define"/> Let Y equal a-X-plus-b,
> an affine function, with a not zero. Because that function is one-to-one, no two
> values of X ever collide — nothing merges. <bookmark mark="invert"/> Each value
> just gets relabeled: the mass that X put on x now sits on a-x-plus-b. So the PMF
> of Y is p-sub-X evaluated at y-minus-b over a. The shape of the distribution is
> untouched — it is only shifted and stretched along the axis.

**Cues**
- `define`: `Y = aX + b,\ a \neq 0`; note one-to-one.
- `invert`: `p_Y(y) = p_X\!\left(\frac{y - b}{a}\right)`; bars shift/scale, don't merge.

---

## Beat: taxi  (scene: TaxiFare)

> Let's finish with a worked example. <bookmark mark="setup"/> A taxi driver's
> ride length, in miles, is a discrete uniform random variable X on the whole
> numbers one through ten — each length equally likely, probability one-tenth. The
> meter charges two dollars fifty just to start, plus forty cents for every
> one-fifth of a mile — which is two dollars a mile. <bookmark mark="fare"/> So the
> fare is Y equals two-point-five plus two X — an affine function of the distance,
> exactly the case we just did. <bookmark mark="pmf"/> Since it's one-to-one, the
> uniform PMF just gets relabeled onto the fare values: a one-mile ride costs four
> dollars fifty, a two-mile ride six fifty, and so on up to twenty-two fifty for
> ten miles — each fare with probability one-tenth. A uniform distribution, moved
> onto a new set of values. <bookmark mark="outro"/> And that is the whole idea:
> a function of a random variable is a random variable, and its PMF comes from
> summing the mass over preimages.

**Cues**
- `setup`: uniform X on {1,...,10}, each `1/10`; the fare rule ($2.50 + $0.40 per fifth-mile).
- `fare`: `Y = 2.5 + 2X`; label affine (a = 2, b = 2.5).
- `pmf`: relabeled bars at fares {4.5, 6.5, ..., 22.5}, each `1/10`; `p_Y(2.5 + 2k) = 1/10`.
- `outro`: key-idea card + bridge to Chapter 6 (expectation).

---

## Cut list (if over budget)
1. Shorten `pmf-of-y` to the formula plus the merge picture (drop the zero-value aside).
2. Trim the affine derivation to the final formula.
3. Compress the taxi meter arithmetic to the `Y = 2.5 + 2X` line.
