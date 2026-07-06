---
slug: 09-model-categories
title: Categories of Probability Models
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 09-model-categories.md
derived_from_sha256: 533b63470ce11547e3bcd71aeeb72a3486cb928941ef331e85f7fed5b11593b1
provenance_stamped: 2026-07-06
target_scene_file: scenes/model_categories.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Classify probabilistic models by the size of their sample space, and see how a probability law is specified in each."
  recap: "Last video: the three axioms of probability -- nonnegativity, normalization, and additivity."
  key_idea: "How you specify a probability law depends on the size of the sample space: finite and countable models weight individual outcomes, while uncountable (continuous) models assign probability by integration -- length being the uniform special case."
  bridge: "Next: two starred topics -- continuity of probability, and the measure-theory underpinning."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 300  # recalibrated 2026-07-06: published nova final ~0.8x gtts draft; original target was a pre-render word-count guess never reconciled
tolerance_sec: 45

estimated_runtime_sec: 480
measured_runtime_sec: 375.8

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 100
    est_sec: 40
    measured_sec: 41.7
    sync_points: []
  - id: finite
    scene_class: FiniteModels
    narration_words: 185
    est_sec: 74
    measured_sec: 96.3
    sync_points: [equally, die, count, caution]
  - id: countable
    scene_class: CountablyInfiniteModels
    narration_words: 230
    est_sec: 92
    measured_sec: 97.8
    sync_points: [listable, coin, weights, sum, even]
  - id: uncountable
    scene_class: UncountableModels
    narration_words: 280
    est_sec: 112
    measured_sec: 139.9
    sync_points: [interval, length, point, wheel, arc, outro]
---

# Video Script — Categories of Probability Models

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Probability now rests on three axioms — nonnegativity,
> normalization, and additivity. Those axioms work on any sample space. But how
> you actually pin down a probability law depends on how big that sample space
> is. In this video we sort probabilistic models into three families: finite
> sample spaces, countably infinite ones, and uncountably infinite sample spaces.
> For the first two we can weight the individual outcomes; for the third, as we
> will see, that approach breaks down, and we measure probability by integration
> instead.

**Animation cue:** title card recapping the three axioms, then the three-item
outline (finite / countably infinite / uncountably infinite).

---

## Beat: finite  (scene: FiniteModels)

> Start with the simplest family: a finite sample space. <bookmark mark="general"/>
> When Omega has finitely many outcomes, a probability law is completely
> determined by the probabilities of those individual outcomes: the probability
> of an event A is just the sum of the probabilities of the outcomes it contains.
> <bookmark mark="equally"/> There is one especially clean case — the
> equally-likely model. For equally likely outcomes, each of the n outcomes
> carries probability one over n, and the probability of an event A is just the
> size of A divided by the size of Omega. <bookmark mark="die"/> Take
> a fair die. Six faces, each with probability one-sixth. <bookmark mark="count"/>
> To find the probability of an event, we count. The event "roll a prime" is the
> faces two, three, and five — three favorable outcomes out of six — so its
> probability is three over six, one half. Favorable over total, exactly the
> counting model from Chapter two, now named. <bookmark mark="caution"/> One
> warning. Equal likelihood is a modeling assumption, not a law of nature. A
> loaded die, a biased coin, the sum of two dice — none of these have equally
> likely outcomes. Assuming they do is a common misconception called the outcome
> approach. Use the equally-likely model only when a genuine symmetry of the
> experiment earns it.

**Cues**
- `general`: write Pr(A) = Σ Pr(x_i) where A = {x_1, ..., x_k}.
- `equally`: pause, then "For equally likely outcomes," + Pr(A) = |A| / |Omega| (accent); on transition the general line fades and this formula rises to the top slot.
- `die`: six die faces, each one-sixth.
- `count`: highlight {2,3,5}; write Pr({2,3,5}) = 3/6 = 1/2.
- `caution`: one-line caution that equal likelihood is an assumption.

---

## Beat: countable  (scene: CountablyInfiniteModels)

> Now let the sample space be infinite — but countably so. <bookmark
> mark="listable"/> A set is countable when its elements can be lined up in a
> sequence, s-one, s-two, s-three, and on; formally, it has the same cardinality
> as some subset of the natural numbers. Even though there are infinitely many
> outcomes, we can still specify the law one outcome at a time, by assigning each
> a weight — as long as those weights sum to one. <bookmark mark="coin"/> The
> classic example: toss a fair coin repeatedly until the first heads, and record
> how many tosses it took. The sample space is the positive integers, one, two,
> three, and so on — a countably infinite set. <bookmark mark="weights"/> The
> probability that the first heads lands on toss k is two to the minus k: a half,
> a quarter, an eighth, a sixteenth, each bar half the height of the one before.
> <bookmark mark="sum"/> Add up that whole infinite sequence of weights and it
> comes to exactly one, just as the axioms demand — the masses fill the bar.
> <bookmark mark="even"/> And we can ask real questions. What is the probability
> that the number of tosses is even? Add the even-indexed weights: one quarter,
> plus one sixteenth, plus one sixty-fourth, and on — a geometric series that sums
> to one third. An infinite computation, made finite by the structure of the
> model.

**Cues**
- `listable`: write Omega = {1, 2, 3, ...}; a countable set is listable.
- `coin`: coin-until-first-heads setup; the first head on toss k.
- `weights`: a row of decaying bars Pr(k) = 2^-k.
- `sum`: brace the bars; write sum of 2^-k = 1.
- `even`: highlight the even bars; write Pr(even) = 1/4 + 1/16 + ... = 1/3.

---

## Beat: uncountable  (scene: UncountableModels)

> The third family is the strange one: an uncountably infinite sample space.
> <bookmark mark="interval"/> Take the unit interval — every real number between
> zero and one. There are so many outcomes here that most subsets cannot be
> written as a finite or even countable list, so the trick of summing individual
> outcome-probabilities simply fails. <bookmark mark="point"/> In fact, on a
> continuum almost every single point carries probability zero — there are far
> too many of them for each to hold positive mass. A mixed law can place a lump
> on a few isolated points, but a purely continuous law spreads its mass out,
> leaving every single point with none. <bookmark mark="length"/> So we specify
> the law a different way. For the uniform law on this interval, the probability
> of landing between a and b is just its length, b minus a. A general continuous
> law replaces length with the area under a density — an integral — and length is
> simply the flat-density case. From there the third axiom extends this to any
> countable union of disjoint intervals by adding their probabilities. <bookmark
> mark="wheel"/> Here is
> the idea in action: the wheel of serendipity. Spin a pointer on a circle; the
> outcome is the angle where it stops, uniform on zero to two pi — an uncountable
> sample space. <bookmark mark="arc"/> The probability of landing in any arc is
> the length of that arc divided by two pi. Land in the first quadrant, an arc of
> length pi over two? That is one quarter. Probability has become geometry: an arc
> over the whole circumference. <bookmark mark="outro"/> So the family of a model
> is set by the size of its sample space: finite and countable models weight
> individual outcomes, while uncountable models assign probability by integration
> — by length, in the uniform case. That closes the core of Chapter three. Two
> starred topics remain — the
> continuity of probability, and the measure-theory that puts all of this on a
> rigorous footing.

**Cues**
- `interval`: number line segment [0,1]; outcomes are a continuum.
- `point`: a lone point; for a continuous law Pr({x}) = 0 (a mixed law may place mass on isolated points).
- `length`: shade [a,b]; the uniform law Pr((a,b)) = b - a and the general law Pr((a,b)) = ∫_a^b f(x) dx.
- `wheel`: a circle with a pointer; angle uniform on [0, 2pi).
- `arc`: highlight an arc; write Pr(arc) = (arc length)/(2pi); first quadrant = 1/4.
- `outro`: key-idea card + bridge to the two starred topics.

---

## Cut list (if over budget)
1. Trim the loaded-die / biased-coin list in `finite` to one example.
2. Drop the "first quadrant = 1/4" sentence in `uncountable`.
3. Shorten the listable-set definition in `countable` to one sentence.
