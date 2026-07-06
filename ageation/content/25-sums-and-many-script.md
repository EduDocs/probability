---
slug: 25-sums-and-many
title: Sums and Many Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human approved the script 2026-07-03
derived_from: 25-sums-and-many.md
derived_from_sha256: bf316d9eb9872305a5f31c53d8e0d744e5593548289d006dfe6e3e91144f29ec
provenance_stamped: 2026-07-06
target_scene_file: scenes/sums_and_many.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Find the distribution of a sum: convolve the PMFs - or transform, and let sums become products."
  recap: "Last video: independence factors the joint; products split, and variances of sums add."
  key_idea: "For independent variables the PMF of a sum is a convolution, and the generating function turns that convolution into a product."
  bridge: "Next chapter: random variables that take a continuum of values."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# Series calibration: nova finals measure ~0.31 s/word. ~1000 words -> ~310 s.
target_runtime_sec: 310
tolerance_sec: 45

estimated_runtime_sec: 400
measured_runtime_sec: 283.9

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 95
    est_sec: 38
    measured_sec: 29.6
    sync_points: [convolve, transform, scale-up]
  - id: convolution
    scene_class: Convolution
    narration_words: 185
    est_sec: 74
    measured_sec: 52.1
    sync_points: [diagonals, factor, formula]
  - id: ogf
    scene_class: GeneratingFunction
    narration_words: 220
    est_sec: 88
    measured_sec: 58.5
    sync_points: [pack, examples, moments]
  - id: products
    scene_class: SumsBecomeProducts
    narration_words: 200
    est_sec: 80
    measured_sec: 57.6
    sync_points: [one-line, poisson-merge, mirror]
  - id: many
    scene_class: ManyVariables
    narration_words: 250
    est_sec: 100
    measured_sec: 86.1
    sync_points: [vector, sn, bernoulli-build, n2, n3, n4, pascal, closes,
                  outro]
---

# Video Script — Sums and Many Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> This chapter ends where the rest of probability begins: with sums of
> independent random variables. Sample totals, accumulated noise, repeated
> trials — they are all sums. <bookmark mark="convolve"/> In this video we
> compute the distribution of a sum directly, by convolving PMFs,
> <bookmark mark="transform"/> then meet the generating function — a
> transform under which sums of variables become products of functions —
> <bookmark mark="scale-up"/> and scale everything to n variables, watching
> Bernoulli trials assemble themselves into the binomial.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 7 · Multiple Random
  Variables", recap line, objective; card rises to the top edge.
- `convolve`: outline line "1. Convolution" fades in.
- `transform`: outline line "2. The generating function" fades in.
- `scale-up`: outline line "3. Empirical sums" fades in. (2026-07-04 draft
  review, 0:34: on-screen text shortened — dropped the "n variables and "
  prefix; narration unchanged.)

---

## Beat: convolution  (scene: Convolution)

> What is the PMF of a sum? We answered this once by brute force.
> <bookmark mark="diagonals"/> For the two dice, the pairs producing each
> total lie on an anti-diagonal of the joint table — the sum's mass collects
> along those diagonals. <bookmark mark="factor"/> Now add last video's
> assumption: X and Y independent, integer-valued. Every joint mass on the
> diagonal factors into marginals, and the diagonal sum becomes: the mass
> that X is m, times the mass that Y makes up the rest, k minus m, summed
> over m. <bookmark mark="formula"/> That operation has a name — the
> discrete convolution of the two PMFs — and a symbol, the star. It is
> commutative, it is associative, and it answers the question completely:
> for independent variables, the PMF of the sum is the convolution of the
> PMFs. It is also, frankly, work — a fresh sum for every value of k. Which
> is exactly why the next idea exists.

**Cues**
- `diagonals`: the 6×6 dice table from video 21, one anti-diagonal lit in
  accent; the triangular sum PMF recalled in miniature.
- `factor`: cells on the diagonal annotated `p_X(m)\, p_Y(k - m)`.
- `formula`: two lines — `p_{X+Y}(k) = (p_X * p_Y)(k)` with
  `= \sum_m p_X(m)\, p_Y(k - m)` beneath it (the sum on the second line,
  its `=` aligned under the first line's first `=`); star term in accent;
  caption "commutative, associative." (2026-07-04 draft review, 1:18.)
- layout: the title stays at the top edge; the dice table (left) and the
  annotation/formula column (right) both ride higher and balance each
  other to use the vertical space. (2026-07-04 draft review, 0:40.)

---

## Beat: ogf  (scene: GeneratingFunction)

> Here is one of mathematics' favorite tricks: change representation until
> the hard operation becomes easy. <bookmark mark="pack"/> Take a random
> variable on the non-negative integers and pack its whole PMF into one
> function: G of z equals the expectation of z to the X — each mass becomes
> a coefficient of a power of z. This is the ordinary generating function,
> and engineers will recognize its silhouette: it is essentially the z-transform of the
> PMF. Nothing is lost — differentiate at zero and the coefficients come
> back out. <bookmark mark="examples"/> Three generating functions carry
> this course. A Bernoulli: one minus p plus p z. A binomial: that same
> expression, raised to the n — remember that shape. A Poisson: e to the
> lambda times z minus one. <bookmark mark="moments"/> And as a bonus, the
> function knows its moments: differentiate at one and the mean falls out;
> differentiate twice for the second moment. One object, the whole
> distribution, all its summaries.

**Cues**
- `pack`: a small PMF chart whose bars slide into the coefficients of
  `p_0 + p_1 z + p_2 z^2 + \cdots`;
  `G_X(z) = \mathrm{E}\left[z^X\right]` in accent above.
- `examples`: three result cards, one at a time — Bernoulli `1 - p + pz`;
  binomial `(1 - p + pz)^n` (its exponent briefly indicated); Poisson
  `e^{\lambda(z - 1)}`.
- `moments`: caption card `\mathrm{E}[X] = G_X'(1)`.

---

## Beat: products  (scene: SumsBecomeProducts)

> Now watch the trick pay off. <bookmark mark="one-line"/> Take independent
> X and Y and ask for the generating function of their sum. z to the X plus
> Y is z to the X times z to the Y — and the expectation of a product of
> independent quantities factors, by last video's rule. One line: the
> generating function of a sum is the product of the generating functions.
> The convolution — all those diagonal sums — has become a multiplication.
> <bookmark mark="poisson-merge"/> Try it on two independent Poisson
> streams, with rates alpha and beta. Multiply their generating functions:
> the exponents add, giving e to the alpha plus beta, z minus one. That is
> itself a Poisson generating function — so the merged stream is Poisson
> with rate alpha plus beta. Two lines, no convolution in sight.
> <bookmark mark="mirror"/> And notice the symmetry: when we split a
> Poisson stream, it stayed Poisson, and merging Poisson streams does too.
> Thin or combine — the family is closed.

**Cues**
- `one-line`: two lines — `G_{X+Y}(z) = \mathrm{E}[z^X z^Y] =
  \mathrm{E}[z^X]\, \mathrm{E}[z^Y]` with `= G_X(z)\, G_Y(z)` beneath it,
  the second line's `=` aligned under the first line's first `=`; the
  result line in accent. (2026-07-04 draft review, 3:02.) The `*` →
  `\times` morph beneath the equation is removed — it did nothing.
  (2026-07-04 draft review, 3:05.)
- `poisson-merge`: `e^{\alpha(z-1)} \cdot e^{\beta(z-1)} =
  e^{(\alpha+\beta)(z-1)}` with the exponents visibly combining; card
  "Poisson(α) + Poisson(β) = Poisson(α+β)." The whole element sits
  centered vertically, halfway between the equation above and the mirror
  lines below. (2026-07-04 draft review, 3:22.)
- `mirror`: two-line caption — "split: Poisson stays Poisson" /
  "merge: Poisson stays Poisson." (2026-07-04 draft review, 4:02: video-
  number reference removed on screen and in narration; refer to the
  concept — splitting the Poisson stream — instead.)

---

## Beat: many  (scene: ManyVariables)

> Everything extends past pairs. <bookmark mark="vector"/> For n random
> variables, the joint PMF is the probability that all n coordinates hit
> their values at once — and when the variables are independent, it factors
> into n marginal terms, just as pairs did. <bookmark mark="sn"/> The
> object to care about is the empirical sum: S n, the total of n
> independent draws from one PMF. Build it one variable at a time — each
> step convolves in one more copy — so the PMF of S n is an n-fold
> convolution. Or transform: the generating function of S n is G to the
> power n. One exponent instead of n minus one convolutions.
> <bookmark mark="bernoulli-build"/> Watch it happen. Start from a single
> Bernoulli trial: two bars. <bookmark mark="n2"/> Convolve in a second
> trial, <bookmark mark="n3"/> a third, <bookmark mark="n4"/> a fourth
> — the bars spread and hump, <bookmark mark="pascal"/> and the recursion
> driving each step is Pascal's rule from the combinatorics chapter.
> <bookmark mark="closes"/> By induction, the sum of n
> Bernoulli trials is exactly the binomial — and on the transform side,
> G of z to the n is one minus p plus p z to the n, the binomial generating
> function we met one beat ago. The loop closes from both directions.
> <bookmark mark="outro"/> The key idea of this video — and of this
> section: independence turns joints into products — of probability mass
> functions, of expectations, of generating functions — and that is what
> makes sums of many variables tractable. Coming up next: random variables
> that take a continuum of values.

**Cues**
- `vector`: `p_{\mathbf{X}}(\mathbf{x}) = \prod_{k=1}^{n} p_{X_k}(x_k)`
  card (independent case), video 24's iid mini-cards recalled.
- `sn`: `S_n = \sum_{k=1}^{n} X_k`; twin cards
  `p_{S_n} = p_X * \cdots * p_X` (n-fold) and
  `G_{S_n}(z) = G_X(z)^n` in accent.
- section title reads "Multiple Variables and Empirical Sums". (2026-07-04
  draft review, 4:16: on-screen title only; voice unchanged.)
- `bernoulli-build`: the two Bernoulli bars convolved repeatedly — n = 1,
  2, 3, 4 (one chart at a time, morphing) — settling into the binomial
  silhouette; caption "Pascal's rule, one convolution at a time."
  (2026-07-04 draft review, 5:00: block re-split per phrase — marks `n2`,
  `n3`, `n4`, `pascal`, `closes` — so each chart morph and the caption
  land on their own sentence; narration verbatim.)
- `outro`: shared outro card — key idea + "Coming up: Continuous Random
  Variables". (2026-07-04 draft review, 5:45: card reads "of PMFs" and the
  voice spells out "probability mass functions".)

---

## Cut list (if over budget)

1. Drop the `moments` bonus from `ogf` (keep the caption card only).
2. Compress `mirror` to one spoken sentence.
3. Trim the Pascal's-rule aside in `bernoulli-build` to a caption.
