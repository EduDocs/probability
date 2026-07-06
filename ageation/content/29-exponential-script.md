---
slug: 29-exponential
title: The Exponential Distribution
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 29-exponential.md
derived_from_sha256: 6ba67e0eabd92f0014aae162feda196a20b80e939690ed25b5aa8d15c4a45889
provenance_stamped: 2026-07-06
target_scene_file: scenes/exponential.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "The continuous model for waiting: density, rate, and a distribution that never remembers."
  recap: "Last video: the uniform and the Gaussian opened the catalog of continuous models."
  key_idea: "The exponential is the continuous geometric: memoryless, the model for waiting."
  bridge: "Next: a gallery of densities - gamma, Rayleigh, and friends, with the exponential at the root."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~930 words -> ~290 s.
target_runtime_sec: 290
tolerance_sec: 45

estimated_runtime_sec: 353
measured_runtime_sec: 331.1

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 98
    est_sec: 38
    measured_sec: 36.0
    sync_points: [definition, limit, memoryless, halflife]
  - id: definition
    scene_class: ExponentialDefinition
    narration_words: 229
    est_sec: 88
    measured_sec: 82.1
    sync_points: [density, cdf, rate, rate2, server, answer]
  - id: limit
    scene_class: GeometricLimit
    narration_words: 202
    est_sec: 78
    measured_sec: 68.0
    sync_points: [setup, scaled, staircase, melt, arrival]
  - id: memoryless
    scene_class: Memoryless
    narration_words: 177
    est_sec: 68
    measured_sec: 63.7
    sync_points: [statement, proof, restart, restart2, restart3, unique]
  - id: halflife
    scene_class: HalfLifeExample
    narration_words: 211
    est_sec: 81
    measured_sec: 81.4
    sync_points: [setup, split, solve, stream, outro]
---

# Video Script — The Exponential Distribution

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> The catalog of continuous models opened with the uniform and
> the Gaussian. Today we add the third leg of the triad: the exponential
> distribution, the model for waiting. <bookmark mark="definition"/> We meet
> its density and its CDF, and put them straight to work on a server,
> <bookmark mark="limit"/> then watch the geometric distribution squeeze
> into it as coin flips run on a finer and finer clock,
> <bookmark mark="memoryless"/> then meet the strange property the limit
> carries over: an exponential wait never remembers how long you have
> already waited, <bookmark mark="halflife"/> and finish by letting that
> property crack a half-life problem with almost no algebra.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 8 · Continuous Random
  Variables", objective; card rises to the top edge; progress tag 4 / 5 in
  the DR corner.
- `definition`: outline line "1. Density, CDF, and the rate" fades in.
- `limit`: outline line "2. The geometric, squeezed" fades in.
- `memoryless`: outline line "3. The memoryless property" fades in.
- `halflife`: outline line "4. Half-lives" fades in.

---

## Beat: definition  (scene: ExponentialDefinition)

> Last chapter's bus made waiting uniform: a bus was coming, on schedule,
> within thirty minutes. Real arrivals are not so polite. Requests hit a
> server, parts fail, calls arrive whenever they please. For waits like
> these, the workhorse model is the exponential distribution.
> <bookmark mark="density"/> An exponential random variable with parameter
> lambda has density lambda times e to the minus lambda x, for x at least
> zero. It starts at its highest value and decays, so short waits are
> always the most likely. <bookmark mark="cdf"/> Integrate once and the CDF
> comes out in closed form: the probability that X is at most x equals one
> minus e to the minus lambda x. You may recognize this curve; it made a
> cameo three videos ago as our first continuous CDF. Now it has a name.
> <bookmark mark="rate"/> The parameter lambda is a rate. With lambda one
> half, the density starts low and stretches out. <bookmark mark="rate2"/>
> Raise lambda to one, then to two, and the curve starts higher and dives
> faster. More events per unit time means shorter waits.
> <bookmark mark="server"/> Put it to work. Connection requests at an
> internet server have exponential inter-arrival times with lambda equal to
> one half. A request just arrived. What is the chance the next one lands
> within two minutes? <bookmark mark="answer"/> The CDF at two gives it
> directly: one minus e to the minus one, about zero point six three two.
> One integral, one answer.

**Cues** (two-column: chart left, formulas right; one curve in focus at a
time)
- opening block: section title written, docked up.
- `density`: `f_X(x) = \lambda e^{-\lambda x}, x \geq 0` in accent, upper
  right; axes grow at lower left, shifted further left for breathing room
  (2026-07-04 draft review, 1:15); the lambda = 1 density curve drawn.
  Chart raised and eased slightly right so the left and bottom margins
  breathe, tick numbers one size smaller at TICK (2026-07-05 draft review,
  1:50).
- `cdf`: density formula demotes; `F_X(x) = 1 - e^{-\lambda x}` in accent
  below it; the CDF curve drawn on the same axes in a second diagram color.
- `rate`: CDF formula demotes and its curve fades; the density morphs to
  lambda = 1/2 with an accent `\lambda = \tfrac{1}{2}` tag by the curve, at
  BODY size so it reads at a glance (2026-07-04 draft review, 1:15).
- `rate2`: the curve morphs to lambda = 1, then lambda = 2, the tag
  updating each time - steeper start, faster decay.
- `server`: curve morphs back to lambda = 1/2 (the server's rate); the
  area under the density from 0 to 2 fills in BAR blue.
- `answer`: `\Pr(T < 2) = 1 - e^{-1} \approx 0.632` written in accent in
  the right column; the shaded area indicated.

---

## Beat: limit  (scene: GeometricLimit)

> Where does this curve come from? From a distribution you already know.
> <bookmark mark="setup"/> Fix a rate lambda, and flip a coin on every tick
> of a clock that ticks n times per second, with success probability lambda
> over n. The number of flips until the first success is geometric; call it
> Y n. <bookmark mark="scaled"/> But measure the wait in seconds, not in
> ticks: divide by n. The scaled wait X n equals Y n over n.
> <bookmark mark="staircase"/> Its CDF is a staircase. The probability that
> X n is at most x is one minus, one minus lambda over n, raised to the
> floor of n x: a step at every tick of the clock. <bookmark mark="melt"/>
> Now speed up the clock. With n equal to four, the steps are chunky. At
> twelve, they tighten. At forty eight, the staircase is nearly smooth. Let
> n grow without bound, and the familiar limit for e takes over: the
> staircase melts into one minus e to the minus lambda x, exactly the
> exponential CDF. <bookmark mark="arrival"/> This is the sense in which
> the exponential is the continuous geometric: waiting in discrete ticks
> becomes waiting in continuous time. The same engine that squeezed the
> binomial into the Poisson runs here a second time.

**Cues** (the melting staircase is the video's centerpiece; chart left,
formulas right)
- opening block: section title written, docked up.
- `setup`: `Y_n \sim` geometric with `p_n = \lambda / n`; the PMF
  `p_{Y_n}(k) = (1 - \lambda/n)^{k-1} \lambda/n, k = 1, 2, \ldots` in the
  right column.
- `scaled`: `X_n = Y_n / n` in accent below it.
- `staircase`: `\Pr(X_n \leq x) = 1 - (1 - \lambda/n)^{\lfloor nx \rfloor}`
  written; axes grow at lower left, raised off the bottom edge to balance
  the right column (2026-07-04 draft review, 3:30); the n = 4 staircase CDF
  drawn (lambda = 1), accent tag "n = 4" inside the chart. Axes narrowed
  (x_length 6.2 -> 5.6) and tick numbers one size smaller at TICK
  (2026-07-05 draft review, 3:10).
- `melt`: the staircase Transforms through n = 12 and n = 48 into the
  smooth `1 - e^{-\lambda x}` curve, the tag updating and ending at
  `n \to \infty`; the limit `1 - e^{-\lambda x}` lands in accent in the
  right column.
- `arrival`: caption "discrete ticks become continuous time" muted beneath
  the right column; the limit formula indicated.

---

## Beat: memoryless  (scene: Memoryless)

> The geometric carried a famous quirk with it through the limit. Suppose
> you have already waited t seconds. What is the chance you wait at least u
> seconds more? <bookmark mark="statement"/> For an exponential, the answer
> is the memoryless property: the probability that X exceeds t plus u,
> given that X exceeds t, equals the probability that X exceeds u, the same
> as if you had just started. <bookmark mark="proof"/> The proof takes two
> lines. The conditional probability is a ratio of tails: e to the minus
> lambda times t plus u, over e to the minus lambda t. The factor with t
> cancels, leaving e to the minus lambda u. <bookmark mark="restart"/>
> Watch what that means. Cut the density at t, keep the tail,
> <bookmark mark="restart2"/> and renormalize: the same move we used on the
> truncated geometric. <bookmark mark="restart3"/> The rescaled tail lands
> exactly on the original curve. The process restarts.
> <bookmark mark="unique"/> A used component is as good as new. That is a
> modeling superpower, and a warning label, because real parts do wear out.
> Among continuous distributions, the exponential is the only one with this
> property.

**Cues**
- opening block: section title written, docked up.
- `statement`: `\Pr(X > t + u \mid X > t) = \Pr(X > u)` in accent under
  the title.
- `proof`: two derivation lines - the ratio of tails
  `e^{-\lambda(t+u)} / e^{-\lambda t}`, then `= e^{-\lambda u} =
  \Pr(X > u)`; the statement demotes, the final line takes the accent.
- `restart`: the density curve (muted) at lower left with a dashed cut at
  t; the tail beyond t lifts in accent and the region below it shades in
  accent at low opacity - the kept probability made visible (2026-07-04
  draft review, 4:43). Tick numbers one size smaller at TICK, uniform with
  every chart in the video (2026-07-05 draft review, 5:00).
- `restart2`: the tail rescales and lands exactly on the original curve
  from zero - the restart made visible; the shaded region stays behind as
  the ghost of where the tail was (2026-07-04 draft review, 4:43).
- `restart3`: the shading fades out, leaving the landed curve alone on the
  original density (2026-07-04 draft review, 4:43).
- `unique`: right of the chart, "as good as new" in ink with "the only
  continuous distribution with this property" muted beneath.

---

## Beat: halflife  (scene: HalfLifeExample)

> The memoryless property is not just a curiosity; it computes.
> <bookmark mark="setup"/> Hard drives at a server farm have a half-life of
> two years: the probability that a disk survives past year two is exactly
> one half. What is the chance a disk needs repair within its first year?
> We are not told lambda, and we will not need it. <bookmark mark="split"/>
> Split the two-year survival at year one. Surviving two years means
> surviving the first year, then surviving one more year given that first
> year. By memorylessness, that second factor equals the plain one-year
> survival. So the probability of surviving two years is the one-year
> survival, squared. <bookmark mark="solve"/> Take the square root:
> surviving one year has probability one over root two. The chance of
> failure within the first year is one minus one over root two, about zero
> point two nine three. Lambda never appeared. <bookmark mark="stream"/>
> One last debt to settle. Back when we split the Poisson stream, its
> bits were drawn with ragged gaps between the dots. That drawing was
> honest: when arrivals are random in time, the gaps between them are
> exponential. <bookmark mark="outro"/> The key idea of this video: the
> exponential is essentially the continuous version of the geometric
> random variable, memoryless, the model for waiting. Next video opens a
> whole gallery of densities, with the exponential at its root.

**Cues**
- opening block: section title written, docked up.
- `setup`: survival curve `\Pr(T > t)` at lower left, dots marking years
  one and two (ticks already say the values - no duplicate labels);
  `\Pr(T > 2) = \tfrac{1}{2}` in accent in the right column, the question
  `\Pr(T < 1) = ?` muted beneath. Tick numbers one size smaller at TICK,
  uniform with every chart in the video (2026-07-05 draft review, 5:00).
- `split`: the factorization written line by line -
  `\Pr(T > 2) = \Pr(T > 1) \cdot \Pr(T > 2 \mid T > 1) = \Pr(T > 1)^2`;
  the two markers indicated as the two equal factors.
- `solve`: `\Pr(T > 1) = 1/\sqrt{2}`, then
  `\Pr(T < 1) = 1 - 1/\sqrt{2} \approx 0.293` landing in accent.
- `stream`: stage clears; the Poisson-splitting dot stream returns (12
  dots, exponential-looking gaps), the gaps bracketed with an
  `\text{Exponential}(\lambda)` label - the callback paid off. Narration
  refers to the concept, never the video number (2026-07-04 draft review,
  6:20).
- `outro`: shared outro card - key idea + "Coming up: A Gallery of
  Densities". Spoken key idea reworded to "essentially the continuous
  version of the geometric random variable"; the card visual is unchanged
  (2026-07-04 draft review, 6:45).

---

## Cut list (if over budget)

1. Compress the limit algebra to its first and last lines (the melting
   staircase carries the argument); saves ~15 s.
2. Shrink the server example to a caption under the CDF formula; saves
   ~25 s.
3. Drop the Poisson-splitting stream callback in `halflife` (keep the
   outro); saves ~15 s.
