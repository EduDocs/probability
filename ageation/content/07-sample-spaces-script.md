---
slug: 07-sample-spaces
title: Sample Spaces and Events
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 07-sample-spaces.md
derived_from_sha256: 9827451b0f47a0984704aa31f928462701acca51b9e25321c3f8e0812e1a8d22
provenance_stamped: 2026-07-06
target_scene_file: scenes/sample_spaces.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Build the first half of a probabilistic model: the sample space of outcomes and the events we ask about."
  recap: "We spent Chapter 2 counting outcomes; now we build the framework that gives those counts meaning."
  key_idea: "A probabilistic model starts with a sample space -- all possible outcomes -- and events are its admissible subsets; a valid sample space is distinct, mutually exclusive, and exhaustive."
  bridge: "Next: the rules a probability law must obey -- the axioms of probability."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 360
tolerance_sec: 45

estimated_runtime_sec: 365
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 92
    est_sec: 37
    measured_sec: null
    sync_points: []
  - id: experiment-sample-space
    scene_class: ExperimentAndSampleSpace
    narration_words: 250
    est_sec: 100
    measured_sec: null
    sync_points: [omega, outcome, event, die]
  - id: choosing
    scene_class: ChoosingASampleSpace
    narration_words: 195
    est_sec: 78
    measured_sec: null
    sync_points: [heads, histories, choice]
  - id: rules
    scene_class: RulesForASampleSpace
    narration_words: 268
    est_sec: 107
    measured_sec: null
    sync_points: [rule1, rule2, bad, good, outro]
---

# Video Script — Sample Spaces and Events

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> We spent Chapter two counting outcomes; now we build the framework that gives
> those counts meaning. A probabilistic model has two parts — a sample space and
> a probability law — and this video builds the first. In it, we meet the
> experiment, its outcomes, and the sample space; we define an event; we see why
> one experiment can have many sample spaces; and we lay down the two rules a
> sample space must obey.

**Animation cue:** title card recapping Chapter 2, then the four-item outline.

---

## Beat: experiment-sample-space  (scene: ExperimentAndSampleSpace)

> In probability, an experiment is a random occurrence that produces one of
> several outcomes. <bookmark mark="omega"/> Collect every possible outcome into
> a single set, and you have the sample space, written capital Omega — the same
> universal set from Chapter one, now wearing its probability name. Picture it as
> a box holding one ball for each possible outcome. <bookmark mark="outcome"/>
> When you actually run the experiment, exactly one of these balls is realized:
> that is the outcome. <bookmark mark="event"/> An event is an admissible subset
> of the sample space — any collection of outcomes we might want to ask a
> question about. Here it is a dashed loop drawn around some of the balls.
> <bookmark mark="die"/> Make it concrete with the rolling of a die. The sample
> space is the six faces, Omega equals one through six. The set of primes less
> than or equal to six — two, three, and five — is one event among many. And the
> number you actually read off the die is the outcome. Sample space, event,
> outcome: the whole vocabulary, on one picture.

**Cues**
- `omega`: draw the Omega box with colored outcome balls.
- `outcome`: tag a single ball as the realized outcome.
- `event`: dashed loop around a few balls, labelled "event".
- `die`: relabel to Omega = {1,...,6}, loop around {2,3,5}.

---

## Beat: choosing  (scene: ChoosingASampleSpace)

> There is essentially no restriction on what counts as an experiment, and — this
> is the subtle part — the same experiment can have more than one sample space.
> Take n tosses of a coin. <bookmark mark="heads"/> If all you care about is how
> many heads come up, the natural sample space is just the counts: zero, one,
> two, all the way to n. That is only n plus one outcomes. <bookmark
> mark="histories"/> But if you want the complete history — which toss was heads
> and which was tails, in order — then each outcome is a full sequence, and there
> are two to the n of them. Same coins, same tosses, but a far larger sample
> space. <bookmark mark="choice"/> Neither is more correct than the other. The
> choice of sample space depends on the property you wish to analyze: rich enough
> to distinguish every outcome you care about, but no more detailed than the
> question demands.

**Cues**
- `heads`: show Omega = {0, 1, ..., n}.
- `histories`: show a column of HHT... sequences, 2^n of them.
- `choice`: the takeaway line about matching the model to the question.

---

## Beat: rules  (scene: RulesForASampleSpace)

> Some freedom, then — but not total freedom. A sample space must obey two rules.
> <bookmark mark="rule1"/> First, its elements must be distinct and mutually
> exclusive. No two outcomes can occur at once, so that the outcome of the
> experiment is always unique. <bookmark mark="rule2"/> Second, the sample space
> must be collectively exhaustive: every possible outcome has to be accounted for,
> with nothing left out. <bookmark mark="bad"/> Here is a tempting candidate for
> the die that breaks the first rule: the odd numbers, the even numbers, and the
> primes. These overlap — three and five are both odd and prime, and two is both
> prime and even — so a single roll can land in two categories at once. The
> outcome is not unique, so this is not an admissible sample space. <bookmark
> mark="good"/> Fix it by dropping the primes. The odd numbers and the even
> numbers are disjoint — no integer is both — and together they cover one through
> six completely. Distinct, mutually exclusive, and exhaustive: a partition of
> the outcomes, and a perfectly valid sample space. <bookmark mark="outro"/> So
> that is half of a probabilistic model: a sample space of all the outcomes, with
> events as its admissible subsets. Next, we give those events numbers — the rules
> a probability law must obey, the axioms of probability.

**Cues**
- `rule1`: rule 1 — distinct and mutually exclusive (unique outcome).
- `rule2`: rule 2 — collectively exhaustive (nothing left out).
- `bad`: overlapping odd / even / prime blobs; 2, 3, 5 caught in two.
- `good`: two disjoint odd / even regions tiling {1,...,6}.
- `outro`: key-idea card + bridge to the axioms of probability.

---

## Cut list (if over budget)
1. In `choosing`, name the 2^n histories without enumerating any sequences.
2. In `rules`, state the bad example verbally and only animate the good partition.
3. Trim the closing recap in `rules` to a single sentence before the bridge.
