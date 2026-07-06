---
slug: 16-important-discrete-rvs
title: Important Discrete Random Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
derived_from: 16-important-discrete-rvs.md
derived_from_sha256: c893923538af95c48d2baf7a17b0f5bc5acab9fe114448e67bf2b970f2a3b7d7
provenance_stamped: 2026-07-06
target_scene_file: scenes/important_discrete_rvs.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Meet the discrete distributions that recur everywhere -- Bernoulli, binomial, Poisson, geometric, uniform -- and see the binomial converge to the Poisson."
  recap: "Last video: a discrete random variable is described by its PMF, p_X(x) = Pr(X = x)."
  key_idea: "A handful of named PMFs -- each tied to a counting story -- cover most discrete models, and the binomial becomes Poisson in the rare-event limit."
  bridge: "Next: functions of a random variable -- transform X and track its PMF."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
target_runtime_sec: 290  # recalibrated 2026-07-06: published nova final ~0.8x gtts draft; original target was a pre-render word-count guess never reconciled
tolerance_sec: 60

estimated_runtime_sec: 650
measured_runtime_sec: 293.1

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 95
    est_sec: 38
    measured_sec: 32.5
    sync_points: []
  - id: bernoulli
    scene_class: Bernoulli
    narration_words: 105
    est_sec: 42
    measured_sec: 35.3
    sync_points: [define, chart, coin]
  - id: binomial
    scene_class: Binomial
    narration_words: 150
    est_sec: 60
    measured_sec: 49.1
    sync_points: [define, chart, soda]
  - id: poisson
    scene_class: Poisson
    narration_words: 140
    est_sec: 56
    measured_sec: 44.1
    sync_points: [define, chart, server]
  - id: binomial-to-poisson
    scene_class: BinomialToPoisson
    narration_words: 130
    est_sec: 52
    measured_sec: 41.8
    sync_points: [setup, n5, n15, n35, settle]
  - id: geometric
    scene_class: Geometric
    narration_words: 140
    est_sec: 56
    measured_sec: 49.3
    sync_points: [define, chart, memoryless]
  - id: uniform
    scene_class: DiscreteUniform
    narration_words: 110
    est_sec: 44
    measured_sec: 41.1
    sync_points: [define, chart, outro]
---

# Video Script — Important Discrete Random Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Recall that a discrete random variable is captured entirely by
> its probability mass function. In practice, though, you rarely start from
> scratch. A small number of distributions show up frequently, and almost all of
> them come from counting. In this video we tour five of them — the
> Bernoulli, the binomial, the Poisson, the geometric, and the uniform — each
> with its own counting story and its own bar chart. And in the middle we'll see
> something surprising: the binomial, in a certain limit, turns into the Poisson.

**Animation cue:** title card + recap (PMF), objective, and a five-item outline;
tease the binomial-to-Poisson punchline.

---

## Beat: bernoulli  (scene: Bernoulli)

> Start with the simplest random variable there is. <bookmark mark="define"/> A
> Bernoulli random variable takes only two values, zero and one. It equals one
> with probability p, and zero with probability one minus p. That's the entire
> distribution. <bookmark mark="chart"/> As a bar chart it is just two bars:
> possibly a tall one and a short one, and here p is one-quarter. <bookmark mark="coin"/>
> Every Bernoulli is really a coin flip — a biased coin that comes up heads,
> which we call one, with probability p. It looks trivial, but it is the atom
> from which the next two distributions are built.

**Cues**
- `define`: `p_X(x) = \begin{cases}1-p & x=0\\ p & x=1\end{cases}` in accent.
- `chart`: two bars at 0 and 1 (p = 0.25).
- `coin`: a heads=1 / tails=0 coin note.

---

## Beat: binomial  (scene: Binomial)

> Now flip that coin n times, independently, and count the ones.
> <bookmark mark="define"/> The number of successes in n independent, identical
> Bernoulli trials is a binomial random variable. Its PMF is n-choose-k times p
> to the k times one-minus-p to the n-minus-k — the n-choose-k counts which
> trials succeeded, and the powers give the probability of any one such pattern.
> Sum over all k and the binomial theorem gives exactly one. <bookmark mark="chart"/>
> With n equal to eight and p a quarter, the bars rise to a peak near two and
> taper off. <bookmark mark="soda"/> Here's the story: a soda promotion pays a
> dollar under one cap in four. Buy eight bottles, and the number of winners is
> binomial with n eight, p one-quarter. The chance of winning more than four
> dollars is the sum of the PMF from five up to eight.

**Cues**
- `define`: `p_X(k) = \binom{n}{k} p^k (1-p)^{n-k}`; normalization `(p+(1-p))^n=1`.
- `chart`: binomial bars, n = 8, p = 0.25.
- `soda`: Brazos-Soda note; `\Pr(X > 4) = \sum_{k=5}^{8}\binom{8}{k}\tfrac{3^{8-k}}{4^8}`.

---

## Beat: poisson  (scene: Poisson)

> The next one counts occurrences over time. <bookmark mark="define"/> A Poisson
> random variable has PMF lambda-to-the-k over k-factorial, times e-to-the-minus-
> lambda, for k equals zero, one, two, and up. It normalizes beautifully: the sum
> of lambda-to-the-k over k-factorial is just the Taylor series for e-to-the-
> lambda, which cancels the e-to-the-minus-lambda to leave one.
> <bookmark mark="chart"/> With lambda equal to two, the mass peaks at one and
> two and decays. <bookmark mark="server"/> Poisson is the go-to model for counts
> — requests hitting a server, arrivals in a queue, calls in a minute. If
> requests arrive at rate lambda per second, the probability that none arrives in
> a given second is simply e-to-the-minus-lambda.

**Cues**
- `define`: `p_X(k) = \frac{\lambda^k}{k!}e^{-\lambda}`; Taylor-series normalization.
- `chart`: Poisson bars, lambda = 2.
- `server`: server-requests note; `p_N(0) = e^{-\lambda}`.

---

## Beat: binomial-to-poisson  (scene: BinomialToPoisson)

> Here's the payoff, and it connects the last two. <bookmark mark="setup"/> Fix a
> rate lambda, and let each of n trials succeed with probability lambda over n —
> so as n grows, each success gets rarer, but the expected count stays lambda.
> <bookmark mark="n5"/> With fifteen trials the shape is close, but still a little
> rough. <bookmark mark="n15"/> Twenty-five trials, and it sharpens. <bookmark mark="n35"/>
> Thirty-five trials, and the bars <bookmark mark="settle"/> settle right onto the
> Poisson curve drawn faintly behind them. In the limit, the binomial becomes the
> Poisson. This is why a Poisson with lambda equal to n-times-p is such a good
> approximation to a binomial when n is large and p is small.

**Cues**
- `setup`: `\lim_{n\to\infty}\binom{n}{k}(\tfrac{\lambda}{n})^k(1-\tfrac{\lambda}{n})^{n-k} = \frac{\lambda^k}{k!}e^{-\lambda}`; faint fixed Poisson(10) reference.
- `n5/n15/n35`: Transform the binomial bar group; update the `n =` label in lockstep.
- `settle`: pulse the Poisson reference so the match is unmistakable.

---

## Beat: geometric  (scene: Geometric)

> Instead of counting successes in a fixed number of trials, now wait for the
> first success. <bookmark mark="define"/> Keep running Bernoulli trials until you
> get a one; the number of trials that took is a geometric random variable. Its
> PMF is one-minus-p to the k-minus-one, times p — the probability of k-minus-one
> failures followed by a success. <bookmark mark="chart"/> Because each extra
> trial multiplies by one-minus-p, the bars decay by a constant factor: a
> steadily shrinking staircase. <bookmark mark="memoryless"/> And the geometric
> hides a remarkable property — it is memoryless. Given that you've already waited
> more than k trials, the probability you need j more is exactly the original
> probability of j. The process forgets its past completely, and the geometric is
> the only discrete random variable that does.

**Cues**
- `define`: `p_X(k) = (1-p)^{k-1}p,\ k=1,2,\dots`
- `chart`: geometric bars, p = 0.25 (decaying).
- `memoryless`: `\Pr(X = k+j \mid X > k) = \Pr(X = j)` in accent.

---

## Beat: uniform  (scene: DiscreteUniform)

> The last one is the picture of pure symmetry. <bookmark mark="define"/> A
> discrete uniform random variable takes n values, all equally likely — each with
> probability one over n. <bookmark mark="chart"/> Its bar chart is perfectly
> flat; here n is eight, so every bar sits at one-eighth. We've quietly met this
> one already: a fair die and a fair coin are both discrete uniforms.
> <bookmark mark="outro"/> So there is our gallery — Bernoulli, binomial, Poisson,
> geometric, uniform — five distributions, each tied to a counting story, and the
> binomial folding into the Poisson in the limit. Next, we'll take a random
> variable and transform it, and follow what happens to its PMF.

**Cues**
- `define`: `p_X(k) = 1/n`.
- `chart`: flat uniform bars, n = 8; note fair die / fair coin.
- `outro`: key-idea card + bridge to functions of random variables.

---

## Cut list (if over budget)
1. Trim the `uniform` beat to the flat chart and the one-line fair-die note.
2. Drop the memoryless aside in `geometric` (keep the decaying-bars picture).
3. Shorten the two soda/server stories to a single sentence each.
