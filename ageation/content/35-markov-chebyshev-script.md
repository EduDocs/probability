---
slug: 35-markov-chebyshev
title: The Markov and Chebyshev Inequalities
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 35-markov-chebyshev.md
derived_from_sha256: f2d06cb6286919804a4fc4e495a01c69004adb09ed76127c6bc55087fe08aef2
provenance_stamped: 2026-07-06
target_scene_file: scenes/markov_chebyshev.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Turn one moment into a tail bound: dominate an indicator, then take expectations."
  recap: "Last video: the MGF packaged every moment of a random variable into one function."
  key_idea: "Probabilities are expectations of indicators; dominating an indicator turns one moment into a tail bound."
  bridge: "Next: the Chernoff bound, an exponential family of dominations optimized with the MGF."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word
# — the target budgets the FINAL.
target_runtime_sec: 310
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / 2.6 (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 379
measured_runtime_sec: 426.1

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 94
    est_sec: 36
    measured_sec: 43.7
    sync_points: [dominate, markov, chebyshev, cantelli]
  - id: why-bounds
    scene_class: WhyBounds
    narration_words: 198
    est_sec: 76
    measured_sec: 87.3
    sync_points: [unknown, claim, domination, weighted, indicator, strategy]
  - id: markov
    scene_class: MarkovInequality
    narration_words: 219
    est_sec: 84
    measured_sec: 90.6
    sync_points: [step, line, expect, markov, use, slack]
  - id: chebyshev
    scene_class: ChebyshevInequality
    narration_words: 245
    est_sec: 94
    measured_sec: 99.4
    sync_points: [setup, chain, template, square, variance, lln]
  - id: cantelli
    scene_class: CantelliBound
    narration_words: 230
    est_sec: 88
    measured_sec: 105.1
    sync_points: [center, family, optimize, cantelli, rehearse, outro]
---

# Video Script — The Markov and Chebyshev Inequalities

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Recently, the moment generating function packaged every moment of a
> random variable into one function. This video puts those moments to work:
> when a probability cannot be computed exactly, a single moment can still
> fence it in. <bookmark mark="dominate"/> First, the engine behind every
> bound in this chapter: a function that dominates another has the larger
> expectation. <bookmark mark="markov"/> Then the Markov inequality, which
> turns one mean into a tail bound, <bookmark mark="chebyshev"/> the
> Chebyshev inequality, a template that mints a whole family of bounds,
> <bookmark mark="cantelli"/> and the Cantelli inequality, where we choose
> the best bound from an entire family.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 10 · Expectations and
  Bounds", title, objective; `progress_tag(2, 3)` in the DR corner; card
  rises to the top edge; `self.wait(0.5)` before the outline.
- `dominate`: outline line "1. Dominating functions" fades in.
- `markov`: outline line "2. The Markov inequality" fades in.
- `chebyshev`: outline line "3. The Chebyshev inequality" fades in.
- `cantelli`: outline line "4. The Cantelli inequality" fades in.

---

## Beat: why-bounds  (scene: WhyBounds)

> Here is a common predicament. We need a tail probability, the chance that
> some quantity exceeds a threshold, <bookmark mark="unknown"/> and the
> exact value is out of reach: the distribution is unknown, or the integral
> is intractable. But suppose we do know one number, the mean.
> <bookmark mark="claim"/> Remarkably, that one number can fence in the
> probability, and the engine is a simple picture.
> <bookmark mark="domination"/> Take two nonnegative functions, g below and
> h above, so that g of x is at most h of x for every x.
> <bookmark mark="weighted"/> Now weight both by the density of X. The
> density is nonnegative, so at every point the weighted g still sits under
> the weighted h, and integrating preserves the order: the expectation of g
> of X is at most the expectation of h of X. Pointwise domination survives
> the integral. <bookmark mark="indicator"/> One more ingredient, remembered
> from earlier chapters: a probability is itself an expectation. The
> probability that X lands in a set S is the expectation of the indicator of
> S, the function that is one on S and zero elsewhere.
> <bookmark mark="strategy"/> The strategy is now visible. To bound a
> probability, sit a computable function on top of an indicator step, and
> take expectations of both sides.

**Cues** (per-phrase sub-blocks; the signature dominating-function picture)
- opening: section title "Bounds from Expectations" docks up; the target
  `\Pr(X \geq a) = ?` appears in INK.
- `unknown`: a muted "distribution unknown" caption; the target stays.
- `claim`: `\mathrm{E}[X]` card in accent, the one number we do have.
- `domination`: axes with two curves, g (solid INK) under h (dashed BLUE);
  labels g(x), h(x). g(x) label sits right of the descending h curve so
  the curves never cross it (2026-07-05 draft review, 1:29).
- `weighted`: the region under g shaded inside the region under h;
  `\mathrm{E}[g(X)] \leq \mathrm{E}[h(X)]` written beside the chart.
- `indicator`: chart clears; `\Pr(X \in S) = \mathrm{E}[\mathbf{1}_S(X)]`
  in accent.
- `strategy`: caption "dominate an indicator, then take expectations"
  (muted).

---

## Beat: markov  (scene: MarkovInequality)

> Run the strategy on the right tail. X is nonnegative, a is positive, and
> the target is the probability that X is at least a.
> <bookmark mark="step"/> Draw the indicator of the interval from a to
> infinity: zero at first, then a step up to one at a.
> <bookmark mark="line"/> Now lay the straight line x over a on top of it.
> Below a, the line is nonnegative while the step is zero; at a, the line
> reaches exactly one; beyond a, it keeps climbing while the step stays
> flat. Everywhere on the nonnegative axis, the line dominates the step.
> <bookmark mark="expect"/> Take expectations of both sides. The
> expectation of the step is the tail probability itself; the expectation
> of the line is the mean of X divided by a. <bookmark mark="markov"/> That
> is the Markov inequality: for a nonnegative random variable, the
> probability that X is at least a is at most the expectation of X over a.
> One mean, one tail bound. <bookmark mark="use"/> Put a number on it. A
> queue holds ten customers on average. The chance of finding fifty or more
> is at most ten over fifty, one fifth, no matter how the queue length is
> distributed. <bookmark mark="slack"/> The gap between the line and the
> step is the price of that generality: the bound is often loose, and
> everything that follows works to close the gap.

**Cues** (the Markov picture: line over step, pivot at (a, 1))
- opening: section title "The Markov Inequality"; the target
  `\Pr(X \geq a)` with "X nonnegative, a > 0" caption.
- `step`: axes; the indicator step `\mathbf{1}_{[a,\infty)}(x)` drawn flat
  at zero, then jumping to one at x = a; dashed riser at a.
- `line`: the line x/a drawn over it, passing through (a, 1); label x/a in
  BLUE; a dot marks the pivot (a, 1).
- `expect`: `\mathrm{E}[\mathbf{1}_{[a,\infty)}(X)] = \Pr(X \geq a)` and
  `\mathrm{E}[X/a] = \mathrm{E}[X]/a` written on the right.
- `markov`: `\Pr(X \geq a) \leq \mathrm{E}[X]/a` lands in accent.
- `use`: worked line `\mathrm{E}[X] = 10:\ \Pr(X \geq 50) \leq 1/5`.
- `slack`: the region between line and step flashes; caption "the gap is
  the slack in the bound" (muted).

---

## Beat: chebyshev  (scene: ChebyshevInequality)

> Nothing in that argument was special about the line. Any dominating
> function works, and that observation is worth a theorem.
> <bookmark mark="setup"/> Let h be any nonnegative function and S any set
> of interest, and write i sub S for the infimum of h over S, the lowest h
> ever gets on that set. <bookmark mark="chain"/> Then i sub S times the
> indicator of S sits under h times the indicator, which sits under h
> itself, at every point. <bookmark mark="template"/> Take expectations and
> the Chebyshev inequality appears: i sub S times the probability that X is
> in S is at most the expectation of h of X. When the infimum is positive,
> divide through, and the template mints a bound for every choice of h and
> S. <bookmark mark="square"/> The most famous instance takes h of x equal
> to x squared, and S the set where x squared is at least b squared. The
> infimum is b squared, so the probability that the magnitude of X is at
> least b is at most the second moment over b squared.
> <bookmark mark="variance"/> Apply that to the centered variable, X minus
> its mean, and the second moment becomes the variance: the probability
> that X strays from its mean by b or more is at most the variance over b
> squared. This is the form everyone calls Chebyshev, and it is what
> variance is for. <bookmark mark="lln"/> Hold on to it: run this bound on
> an empirical average, and out comes the Law of Large Numbers, coming
> soon.

**Cues** (the template picture: h over S, the infimum pressing up)
- opening: section title "The Chebyshev Inequality".
- `setup`: axes; a nonnegative curve h(x); the set S highlighted on the
  x-axis; a dashed horizontal line at height `i_S` under h over S;
  `i_S = \inf_{x \in S} h(x)` beside it.
- `chain`: the pointwise chain
  `i_S \mathbf{1}_S(x) \leq h(x)\mathbf{1}_S(x) \leq h(x)` written.
- `template`: `i_S \Pr(X \in S) \leq \mathrm{E}[h(X)]` lands in accent;
  caption "one template, a family of bounds" (muted).
- `square`: chart clears; instance line `h(x) = x^2`,
  `\Pr(|X| \geq b) \leq \mathrm{E}[X^2]/b^2`.
- `variance`: `\Pr(|X - m| \geq b) \leq \mathrm{Var}(X)/b^2` in accent;
  the previous line demotes to INK.
- `lln`: flag caption "Chebyshev on an empirical average: → the Law of
  Large Numbers" (muted). (2026-07-04 register pass: episode-number
  callback replaced by topic anchor, spoken and on screen.)

---

## Beat: cantelli  (scene: CantelliBound)

> One worked bound to finish, and a preview of a powerful move. Suppose we
> know the mean m and the variance sigma squared, and we want a one-sided
> tail: the probability that X exceeds its mean by at least a.
> <bookmark mark="center"/> Center the variable: Y equals X minus m has
> mean zero and the same variance. <bookmark mark="family"/> Now dominate
> with a whole family of parabolas: h of y equals y plus b, squared, one
> function for every positive b. Over the set where y is at least a, the
> infimum is a plus b, squared; and the expectation of Y plus b, squared,
> is sigma squared plus b squared. Chebyshev hands us a bound for every b.
> <bookmark mark="optimize"/> A family of bounds means a choice: take the
> best one. Slide b along the curve of bounds; it dips, bottoms out, and
> rises again. Calculus finds the minimum at b equal to sigma squared over
> a. <bookmark mark="cantelli"/> Substitute back, and the algebra collapses
> to the Cantelli inequality: the one-sided tail is at most sigma squared
> over a squared plus sigma squared. <bookmark mark="rehearse"/> Remember
> the move: dominate with a family, then optimize over it. Next video, the
> family is exponential, the pocket tool is the moment generating function,
> and the result is the Chernoff bound. <bookmark mark="outro"/> The key
> idea of this video: probabilities are expectations of indicators, so
> dominating an indicator turns one moment into a tail bound.

**Cues** (Cantelli's dial: the bound as a curve in b, marker slides to the
minimum)
- opening: section title "The Cantelli Inequality"; target
  `\Pr(X - m \geq a)` with "known: m and sigma squared" caption.
- `center`: `Y = X - m`, `\mathrm{E}[Y] = 0` written.
- `family`: `h(y) = (y + b)^2`, `i_S = (a+b)^2, a > 0`, and the family
  bound `\Pr(Y \geq a) \leq (\sigma^2 + b^2)/(a+b)^2` stacked on the left.
  The `a > 0` condition is explicit on the i_S line — the infimum step and
  the optimum `b^* = \sigma^2/a` both require it, matching the notes'
  derivation (2026-07-05 draft review, 6:50).
- `optimize`: axes on the right: the bound plotted against b (hardcoded
  sigma = 1, a = 1: (1 + b^2)/(1+b)^2); a marker dot slides along the
  curve to the minimum at b = 1; dashed drop line;
  `b^\ast = \sigma^2/a` in accent.
- `cantelli`: `\Pr(X - m \geq a) \leq \sigma^2/(a^2 + \sigma^2)` lands in
  accent; previous accent demotes.
- `rehearse`: caption "next: an exponential family, optimized with the
  MGF" (muted), centered in its own bottom lane with the 0.8 bottom
  margin respected; the left column rides slightly high to leave the lane
  clear (2026-07-05 draft review, 6:50); stage clears.
- `outro`: shared outro card, key idea + "Coming up: The Chernoff Bound
  and Jensen's Inequality"; `self.wait(0.5)` before the final fade.

---

## Cut list (if over budget)

1. The tightness example (starred in the concept map) is already cut: the
   two-point PMF meeting Chebyshev with equality never made the script.
2. Next: trim the Markov worked example (`use`) to one sentence, saving
   ~20 words.
3. Next: compress Cantelli's `optimize` narration to "calculus finds b
   equals sigma squared over a" over the sliding-marker animation,
   saving ~25 words.
