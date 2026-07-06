---
slug: 11-conditioning-events
title: Conditioning on Events
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 11-conditioning-events.md
derived_from_sha256: 83a2a1cb1285a4117c4f943e0b03290671b536ba40e335ffa2764f827d6f770c
provenance_stamped: 2026-07-06
target_scene_file: scenes/conditioning_events.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Update a probability when partial information is revealed: define conditional probability and use it to chain events together."
  recap: "Last chapter closed the probabilistic model -- a sample space of outcomes and a probability law obeying the axioms."
  key_idea: "Conditioning on B re-normalizes the law to B: Pr(A | B) = Pr(A ∩ B) / Pr(B); chaining these conditionals gives the probability of a whole sequence of events."
  bridge: "Next: the total probability theorem -- assembling an unconditional probability from conditional pieces across a partition."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 280  # recalibrated 2026-07-06: published nova final ~0.8x gtts draft; original target was a pre-render word-count guess never reconciled
tolerance_sec: 45

estimated_runtime_sec: 430
measured_runtime_sec: 349.9

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 110
    est_sec: 44
    measured_sec: 49.7
    sync_points: []
  - id: conditioning
    scene_class: ConditioningOnEvents
    narration_words: 240
    est_sec: 96
    measured_sec: 100.8
    sync_points: [reveal, ratio, frequency, define]
  - id: valid-law
    scene_class: ConditionalLaw
    narration_words: 220
    est_sec: 88
    measured_sec: 91.3
    sync_points: [nonneg, norm, add, coin]
  - id: chain-rule
    scene_class: ChainRule
    narration_words: 250
    est_sec: 100
    measured_sec: 108.1
    sync_points: [rule, urn, draws, outro]
---

# Video Script — Conditioning on Events

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> The probabilistic model is now complete — a sample
> space of possible outcomes, and a probability law that gives each event its
> likelihood. But probability is rarely frozen. The moment we learn something —
> a partial clue about how the experiment turned out — the odds should shift.
> This chapter is about exactly that: conditional probability, the mathematics of
> updating beliefs in the light of information. Across four videos we will define
> conditioning, assemble probabilities across a partition with the total
> probability theorem, invert them with Bayes' rule, and finally ask when
> information changes nothing at all — independence. We begin at the foundation:
> conditioning on an event.

**Animation cue:** title card ("Conditional Probability"), then a four-item
outline — conditioning, total probability, Bayes' rule, independence.

---

## Beat: conditioning  (scene: ConditioningOnEvents)

> Start with a fair die — six faces, each with probability one-sixth.
> <bookmark mark="reveal"/> Now someone tells you the face is odd. Three outcomes
> survive — one, three, and five; the even faces are gone. Before the clue those
> three were equally likely, and nothing about the clue breaks that symmetry, so
> each now carries probability one-third. Notice what happened: we discarded the
> impossible outcomes and re-normalized the rest so they sum to one again.
> <bookmark mark="ratio"/> So the probability of rolling a three, given that the
> face is odd, is one-third — which we can write as the probability of "three and
> odd" divided by the probability of "odd." <bookmark mark="frequency"/> Here is
> a second way to see the same formula. Imagine repeating the experiment a huge
> number of times, N. Count the trials where B happens, and among those, the ones
> where A happens too. The fraction of B-trials that are also A-trials is the
> conditional probability — N-A-B over N-B. Divide top and bottom by N and each
> count turns into a probability, so this ratio tends to the probability of
> A-and-B over the probability of B. <bookmark mark="define"/> That limit is the
> definition. For any event B with positive probability, the conditional
> probability of A given B is the probability of A-and-B, divided by the
> probability of B. It rescales the law so that B becomes the new certain event.

**Cues**
- `reveal`: die faces 1–6 in an Omega box; dim the even faces, keep {1,3,5}, relabel each 1/3.
- `ratio`: write Pr(3 \mid \text{odd}) = Pr(3 ∩ {1,3,5}) / Pr({1,3,5}) = 1/3.
- `frequency`: N trials; N_AB / N_B = (N_AB/N)/(N_B/N) → Pr(A∩B)/Pr(B).
- `define`: accent Pr(A \mid B) = Pr(A ∩ B) / Pr(B), with the side note Pr(B) > 0.

---

## Beat: valid-law  (scene: ConditionalLaw)

> Is this new object really a probability law? It is — it obeys the same three
> axioms. <bookmark mark="nonneg"/> First, nonnegativity: a ratio of two
> nonnegative numbers can't be negative. <bookmark mark="norm"/> Second,
> normalization. Condition the whole sample space on B: the probability of
> Omega-and-B is just the probability of B, so Pr of Omega given B is Pr of B over
> Pr of B — exactly one. Under the conditional law, B carries all the probability.
> <bookmark mark="add"/> And third, additivity: if events are disjoint,
> intersecting each with B keeps them disjoint, so their conditional
> probabilities add. All three axioms hold — conditioning yields a bona fide
> probability law, and every rule we proved last chapter still works inside B.
> <bookmark mark="coin"/> Let's use it. A fair coin is tossed until the first
> heads; the probability that this takes exactly k tosses is two-to-the-minus-k.
> We showed earlier that the number of tosses is even with probability one-third.
> What is the probability it took exactly two tosses, given that it was even?
> That's the probability of two — one quarter — over the probability of even — one
> third — which is three quarters. Knowing the count was even makes "two" quite
> likely.

**Cues**
- `nonneg`: Pr(A \mid B) = Pr(A ∩ B)/Pr(B) ≥ 0.
- `norm`: Pr(Ω \mid B) = Pr(Ω ∩ B)/Pr(B) = Pr(B)/Pr(B) = 1.
- `add`: disjoint A_k ⇒ A_k ∩ B disjoint ⇒ Pr(∪ A_k \mid B) = Σ Pr(A_k \mid B).
- `coin`: Pr(2 \mid \text{even}) = (1/4)/(1/3) = 3/4 (recall Pr(even) = 1/3).

---

## Beat: chain-rule  (scene: ChainRule)

> Conditioning also runs the other way — it lets us build up the probability of
> several events all happening together. <bookmark mark="rule"/> Rearrange the
> definition: the probability of A-and-B is the probability of A, times the
> probability of B given A. Now iterate. The probability that a whole list of
> events, A-one through A-n, all occur is the probability of the first, times the
> probability of the second given the first, times the third given the first two,
> and so on down the chain. This is the chain rule, and it falls out because the
> conditional probabilities telescope — each denominator cancels the previous
> numerator. <bookmark mark="urn"/> It is tailor-made for drawing without
> replacement. An urn holds eight green balls and four gray ones — twelve in all.
> We draw three, and ask: what is the probability all three are green?
> <bookmark mark="draws"/> The first draw is green with probability eight over
> twelve. Given that, eleven balls remain, seven green, so the second is green
> with probability seven over eleven. With two greens gone, six of the ten left
> are green — six over ten. Multiply along the chain: eight-twelfths times
> seven-elevenths times six-tenths is fourteen over fifty-five.
> <bookmark mark="outro"/> Conditioning re-normalizes the law to what you know,
> and chaining those conditionals gives the probability of a whole sequence of
> events. Next, we
> turn the idea around: instead of building intersections, we assemble the total
> probability of an event from a partition of cases.

**Cues**
- `rule`: Pr(A ∩ B) = Pr(A) Pr(B \mid A); then the full chain-rule product for A_1…A_n.
- `urn`: an urn of 8 green + 4 gray balls; three draws without replacement.
- `draws`: a left-to-right tree 8/12 → 7/11 → 6/10; write Pr(ggg) = (8/12)(7/11)(6/10) = 14/55.
- `outro`: key-idea card + bridge to the total probability theorem.

---

## Cut list (if over budget)
1. Drop the frequentist motivation in `conditioning` (keep the die + definition).
2. Compress the additivity check in `valid-law` to one line.
3. Trim the chain-rule general statement; go straight from the two-event rule to the urn.
