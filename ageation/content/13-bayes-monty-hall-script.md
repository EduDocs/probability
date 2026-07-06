---
slug: 13-bayes-monty-hall
title: Bayes' Rule and the Monty Hall Problem
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 13-bayes-monty-hall.md
derived_from_sha256: d58a62ad6e5a46e8e3a5f53342d6e7060b67969a188c9407c8ae86e0ea5b278c
provenance_stamped: 2026-07-06
target_scene_file: scenes/bayes_monty_hall.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Reverse conditioning with Bayes' rule to update beliefs from evidence -- and see why an accurate test can still mislead."
  recap: "Last video: the total probability theorem, Pr(B) = Σ Pr(A_k) Pr(B | A_k)."
  key_idea: "Bayes' rule turns priors into posteriors through the likelihoods: Pr(A_i | B) = Pr(A_i) Pr(B | A_i) / Σ_k Pr(A_k) Pr(B | A_k); the prior is never optional."
  bridge: "Next: independence -- when conditioning on new information changes nothing at all."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 490
tolerance_sec: 45

estimated_runtime_sec: 490
measured_runtime_sec: null

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 100
    est_sec: 40
    measured_sec: null
    sync_points: []
  - id: bayes-rule
    scene_class: BayesRule
    narration_words: 200
    est_sec: 80
    measured_sec: null
    sync_points: [invert, expand, name]
  - id: pitfalls
    scene_class: BaseRateFallacy
    narration_words: 250
    est_sec: 100
    measured_sec: null
    sync_points: [inverse, test, compute, why]
  - id: monty-hall
    scene_class: MontyHall
    narration_words: 300
    est_sec: 120
    measured_sec: null
    sync_points: [setup, likelihood, bayes, switch, outro]
---

# Video Script — Bayes' Rule and the Monty Hall Problem

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> The total probability theorem let us compute the probability of an effect from
> its causes. Bayes' rule runs the arrow backwards: given that the effect
> happened, how likely was each cause? This is the mathematics of inference — of
> evidence, of learning from data. In this video we derive Bayes' rule, name its
> three ingredients — prior, likelihood, and posterior — confront a famous trap
> in probabilistic reasoning, and finish with the puzzle that has started many
> arguments in probability: the Monty Hall problem.

**Animation cue:** title card, recap line (total probability theorem), then the
goal — invert conditioning to update beliefs (the disease example is saved for
the base-rate beat, not teased here); then Monty Hall.

---

## Beat: bayes-rule  (scene: BayesRule)

> The derivation is short. <bookmark mark="invert"/> The probability of A-i and B
> can be written two ways with the product rule — as Pr of A-i given B times Pr of
> B, or as Pr of B given A-i times Pr of A-i. Set the two equal and divide by Pr
> of B, and you have Bayes' rule: Pr of A-i given B is Pr of A-i, times Pr of B
> given A-i, over Pr of B. <bookmark mark="expand"/> And that denominator is
> exactly a total-probability sum over the partition of causes, so we can write
> the whole thing in terms of priors and likelihoods alone. <bookmark mark="name"/>
> Each piece carries a name. The prior, Pr of A-i, is what we believed before the
> evidence. The likelihood, Pr of B given A-i, is how well each cause explains the
> evidence. And the posterior, Pr of A-i given B, is the updated belief afterward.
> Bayes' rule is the machine that turns priors into posteriors in the light of
> what we observe.

**Cues**
- `invert`: Pr(A_i ∩ B) = Pr(A_i \mid B) Pr(B) = Pr(B \mid A_i) Pr(A_i); rearrange to the first Bayes form.
- `expand`: replace Pr(B) with Σ_k Pr(A_k) Pr(B \mid A_k) — the full Bayes formula.
- `name`: label the three terms — prior Pr(A_i), likelihood Pr(B \mid A_i), posterior Pr(A_i \mid B) — in accent.

---

## Beat: pitfalls  (scene: BaseRateFallacy)

> Bayes' rule also guards against a stubborn confusion. <bookmark mark="inverse"/>
> The probability of A given B and the probability of B given A are different
> questions with different answers — swapping them is called confusion of the
> inverse, and in a courtroom, the prosecutor's fallacy. <bookmark mark="test"/>
> Here is how much it matters. A disease affects one percent of the population. A
> test is ninety-five percent accurate both ways: it catches the disease
> ninety-five times in a hundred, and correctly clears the healthy ninety-five
> times in a hundred. You test positive. What is the probability you're actually
> sick? <bookmark mark="compute"/> Bayes' rule: the prior times the likelihood —
> one percent times ninety-five percent — over the total probability of a positive
> test. Work it through and the answer is about sixteen percent. Not ninety-five —
> sixteen. <bookmark mark="why"/> The reason is the base rate. Ninety-nine percent
> of people are healthy, and five percent of that huge group test positive by
> mistake — and those false positives far outnumber the true positives drawn from
> the tiny one percent who are ill. Ignore the prior and a positive result looks
> damning; keep it, and the truth is far milder. Neglecting the base rate this way
> is the base-rate fallacy.

**Cues**
- `inverse`: show Pr(A \mid B) ≠ Pr(B \mid A) as two distinct questions.
- `test`: state the setup — 1% prevalence, 95% accurate both ways; "you test positive."
- `compute`: Pr(D \mid P) = (0.01·0.95) / (0.01·0.95 + 0.99·0.05) ≈ 0.161 (accent).
- `why`: a 100-square population grid — 1 true positive vs the false positives from the healthy 99; name the base-rate fallacy.

---

## Beat: monty-hall  (scene: MontyHall)

> Now the classic. <bookmark mark="setup"/> Three doors. Behind one, a car; behind
> each of the others, a goat — the car equally likely anywhere. You pick door one.
> The host, who knows where the car is, opens a different door — say door three —
> always revealing a goat, and offers you the chance to switch. Should you take
> it? <bookmark mark="likelihood"/> Everything hinges on the host's options. If the
> car is behind your door, door one, the host may open two or three freely — so
> opening three has probability one-half. If the car is behind door two, the host
> is forced: he can open neither your door nor the car's, so he must open three —
> probability one. If the car is behind door three, he would never open it —
> probability zero. <bookmark mark="bayes"/> By total probability, the host opens
> door three with probability one-half. Now apply Bayes. The posterior that the
> car is behind door one — staying — works out to one-third. The posterior that
> it's behind door two — switching — is two-thirds. <bookmark mark="switch"/>
> Switching doubles your chances, from one-third to two-thirds. The opened door
> was never neutral: because the host is constrained to dodge both your door and
> the car, his choice pours door three's share of probability onto door two, not
> back onto your original pick. <bookmark mark="outro"/> Bayes' rule turned an
> argument into arithmetic. Next video: independence — the special case where the
> evidence, however carefully weighed, tells us nothing new.

**Cues**
- `setup`: three closed doors; contestant marker on door 1; host opens door 3 revealing a goat.
- `likelihood`: the likelihood table Pr(H \mid C_1) = 1/2, Pr(H \mid C_2) = 1, Pr(H \mid C_3) = 0.
- `bayes`: Pr(H) = 1/2; then Pr(C_1 \mid H) = 1/3 (stay), Pr(C_2 \mid H) = 2/3 (switch), in accent.
- `switch`: highlight the 1/3 → 2/3 jump; a small mass-transfer diagram (door 3's share moves to door 2).
- `outro`: key-idea card + bridge to independence.

---

## Cut list (if over budget)
1. Trim the confusion-of-the-inverse aside in `pitfalls` to one sentence.
2. Drop the population-grid visual; keep the arithmetic in `pitfalls`.
3. Shorten the mass-transfer explanation in `monty-hall` to one line.
