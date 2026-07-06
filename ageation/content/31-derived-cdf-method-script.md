---
slug: 31-derived-cdf-method
title: Derived Distributions — the CDF Method
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # human pre-approved via chat 2026-07-03 (batch instruction)
derived_from: 31-derived-cdf-method.md
derived_from_sha256: 0b164d408d7b33f88a8b137479d8def3c55a0b059e785f9bc591db4256cd161b
provenance_stamped: 2026-07-06
target_scene_file: scenes/derived_cdf_method.py

# --- Narrative glue (links this video to its neighbours) ----------
linking:
  objective: "Find the distribution of Y = g(X): describe the event g(X) <= y, and integrate the density of X over it."
  recap: "The gallery closed chapter 8 - each density a record of a construction. Now we transform them."
  key_idea: "Describe the event g(X) <= y as a set of x values, and integrate the density of X over it."
  bridge: "Next: differentiate this answer, and the change-of-variables formula falls out."

# --- Voice + timing config ----------------------------------------
voice:
  provider: openai   # scenes read this via _style.speech_service()
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150     # used only for the pre-TTS estimate
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 310
tolerance_sec: 45

# --- Estimates vs measured ------------------------------------------
# est_sec: narration_words / 2.6 (cheap, pre-render).
# measured_sec: written back by assemble / make measure (ffprobe).
estimated_runtime_sec: 371
measured_runtime_sec: 315.7

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 105
    est_sec: 40
    measured_sec: 36.5
    sync_points: [pipeline, rayleigh, monotone]
  - id: cdf-method
    scene_class: CDFMethod
    narration_words: 251
    est_sec: 97
    measured_sec: 81.8
    sync_points: [scaled, general-g, two-hop, no-masses, preimage,
                  specialize, recipe]
  - id: rayleigh-squared
    scene_class: RayleighSquared
    narration_words: 210
    est_sec: 81
    measured_sec: 69.3
    sync_points: [setup, event, shade, integrate, recognize]
  - id: monotone-sup
    scene_class: MonotoneFunctions
    narration_words: 248
    est_sec: 95
    measured_sec: 77.2
    sync_points: [shape-cont, shape-disc, shape-mixed, friendliest, define,
                  halfline, sup, slide, uniform, stretch]
  - id: decreasing-mirror
    scene_class: DecreasingMirror
    narration_words: 150
    est_sec: 58
    measured_sec: 50.9
    sync_points: [flip, formula, outro]
---

# Video Script — Derived Distributions — the CDF Method

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is
an authoring marker: the generated scene splits the narration into
*sequential* voiceover blocks at each marker (bookmark-free timing; no
Whisper).

Beat coverage of the concept ledger: `cdf-method` folds in
`function-of-continuous-rv` and `preimage-probability`; `monotone-sup` folds
in `uniform-doubled` and carries `shape-not-guaranteed` as its one-sentence
opening; `decreasing-mirror` closes.

---

## Beat: overview  (scene: ChapterOverview)

> The gallery closed chapter eight, each density a record of a construction.
> Chapter nine puts those densities to work: pass a random variable through a
> function, and ask what distribution comes out. The answer must be derived,
> and deriving it is this video's whole business. <bookmark mark="pipeline"/>
> In this video we meet the master tool, the CDF method: describe the event
> that g of X lands at or below y, and integrate the density over it.
> <bookmark mark="rayleigh"/> We use it to pay a debt from last video: the
> square of a Rayleigh really is exponential. <bookmark mark="monotone"/>
> And when g is monotone, the whole method collapses to a single formula.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 9  ·  Functions and Derived
  Distributions", title "Derived Distributions - the CDF Method", two-line
  objective; card rises to the top edge; `progress_tag(1, 3)` in the DR
  corner. `self.wait(0.5)` before the outline.
- `pipeline`: outline line "1.  The CDF method" fades in.
- `rayleigh`: outline line "2.  A Rayleigh, squared" fades in.
- `monotone`: outline line "3.  Monotone functions" fades in.

---

## Beat: cdf-method  (scene: CDFMethod)

> Engineering transforms signals frequently: amplitudes get squared into
> energies, <bookmark mark="scaled"/> voltages get scaled and shifted.
> <bookmark mark="general-g"/> Each transform drags a
> distribution along, so take a continuous random variable X and a
> real-valued function g. <bookmark mark="two-hop"/> The picture is the one
> from chapter five: an outcome omega lands on the first real line at X of
> omega, and g carries it to a second line. The composite arrow is a new
> random variable, Y equals g of X. <bookmark mark="no-masses"/> For discrete
> X we derived the PMF of Y by regrouping masses over each preimage. A
> continuum has no masses to regroup, so events must do the work.
> <bookmark mark="preimage"/> The probability that Y lands in a set S is the
> probability that X lands in the preimage of S, the set of inputs u where g
> of u falls in S. That is the set-theoretic preimage from the video on
> functions, back after a long wait and finally load-bearing. And a
> probability about X we know how to compute: integrate the density of X
> over the preimage.
> <bookmark mark="specialize"/> Now specialize. Take S to be the half-line at
> or below y. Then the event Y in S is the event g of X at most y, and its
> probability is, by definition, the CDF of Y at y.
> <bookmark mark="recipe"/> So the recipe has two lines. First, describe the
> event g of X at most y as a set of x values. Second, integrate the density
> of X over that set. Every derived distribution in this chapter starts from
> these two lines.

**Cues** (per-phrase sub-blocks so each element lands on its sentence)
- opening: section title "The CDF Method" written, then docked up; the
  amplitude example `A \longmapsto A^2` fades in with its muted caption
  "amplitude, squared into energy" (2026-07-05 draft review, 0:40 - the
  opening motivation played over a bare title).
- `scaled`: the second example `V \longmapsto aV + b`, muted caption
  "voltage, scaled and shifted" (2026-07-05 draft review, 0:40).
- `general-g`: the general pipeline `X \xrightarrow{g} g(X)` written in
  accent under the examples; all three fade as the two-hop diagram begins
  (2026-07-05 draft review, 0:40).
- `two-hop`: the two-hop diagram animates - `\Omega` blob (omega_box) at the
  left, arrow to an X number line, second arrow to a Y number line; a sample
  dot hops blob to line to line; composite arrow drawn straight through,
  labelled `Y = g(X)` in accent. The whole diagram rides 0.5 higher so it
  balances the band under the title (2026-07-04 draft review, 1:20).
- `no-masses`: caption "no masses to regroup: events do the work" (MUTED)
  under the diagram; the accent moves off `Y = g(X)`.
- `preimage`: diagram fades; the preimage identity is written line by line:
  `\Pr(Y \in S) = \Pr(X \in g^{-1}(S)) = \int_{g^{-1}(S)} f_X(u)\,du`, with
  `g^{-1}(S) = \{u \mid g(u) \in S\}` as a MUTED side note. Narration now
  cites "the video on functions" by content - the video-number reference
  ("video two's", "twenty-nine videos") is removed (2026-07-04 draft
  review, 1:47).
- `specialize`: `S = (-\infty, y]` accented; the identity transforms to
  `F_Y(y) = \Pr(g(X) \leq y)`.
- `recipe`: the two-line recipe card appears - "1. describe
  `\{x \mid g(x) \leq y\}`", "2. integrate `f_X` over it" - boxed, accent on
  the box only. The card sits 0.4 lower (buff 0.55 -> 0.95) so it does not
  crowd the identity stack (2026-07-04 draft review, 2:20).

---

## Beat: rayleigh-squared  (scene: RayleighSquared)

> Let the method earn its keep. <bookmark mark="setup"/> Last video
> introduced the Rayleigh density as the amplitude of a fading channel, and
> stated, without proof, that its square is exponential. Take X Rayleigh with
> sigma squared equal to one, so the density is u times e to the minus u
> squared over two, for u at least zero. Let Y be X squared, the energy of
> the fade. <bookmark mark="event"/> Fix y positive, and run the recipe. The
> event Y at most y is the event X squared at most y, which puts X between
> minus root y and root y. <bookmark mark="shade"/> But a Rayleigh variable
> is never negative, so the lower limit rises to zero: the integral runs from
> zero to root y, the shaded area under the density.
> <bookmark mark="integrate"/> Substitute v equals u squared. The
> differential v is twice u, exactly the factor sitting in the integrand, and
> the integral collapses: F of Y at y equals one minus e to the minus y over
> two. <bookmark mark="recognize"/> Look at that function. It is the exponential
> CDF from chapter eight, with parameter one half. The square of a Rayleigh
> random variable is exponential; the promise is kept, in four lines. And
> notice what the method needed from g: nothing beyond the ability to
> describe one event.

**Cues**
- opening: section title "A Rayleigh, Squared", docked up.
- `setup`: the Rayleigh density `f_X(u) = u\,e^{-u^2/2}`, `u \geq 0` plotted
  on axes (chart keeps a >= 0.8 bottom margin); card `Y = X^2` beside it.
  The left plot rides 0.4 higher for visual harmony (2026-07-04 draft
  review, 3:30).
- `event`: derivation line 1 at the right:
  `F_Y(y) = \Pr(X^2 \leq y) = \Pr(-\sqrt{y} \leq X \leq \sqrt{y})`.
- `shade`: the region from zero to `\sqrt{y}` under the curve fills; a tick
  labelled `\sqrt{y}` marks the boundary; line 2:
  `= \int_0^{\sqrt{y}} u\,e^{-u^2/2}\,du`.
- `integrate`: line 3 lands in accent: `F_Y(y) = 1 - e^{-y/2}` (the previous
  accents demote to INK).
- `recognize`: caption "the exponential CDF, parameter one half" (MUTED)
  under the result; `Indicate` on the boxed result. Spoken "Look at that
  curve" becomes "Look at that function" (2026-07-04 draft review, 3:38).

---

## Beat: monotone-sup  (scene: MonotoneFunctions)

> One caution before we go on: continuity of X promises nothing about Y.
> <bookmark mark="shape-cont"/> A
> function of a continuous random variable can be continuous,
> <bookmark mark="shape-disc"/> discrete, <bookmark mark="shape-mixed"/> or
> neither, so we study structured cases,
> <bookmark mark="friendliest"/> and the friendliest structure is
> monotonicity. <bookmark mark="define"/> A function is monotone increasing
> when larger inputs never produce smaller outputs: x one at most x two
> forces g of x one at most g of x two. <bookmark mark="halfline"/> For such
> a g, the event g of X at most y is everything to the left of a boundary:
> the preimage of a half-line is a half-line. <bookmark mark="sup"/> The
> boundary is the supremum of that preimage, and the CDF of Y is the CDF of X
> evaluated there. Why a supremum? Because a flat stretch of g sends many
> inputs to the same output, and a jump of g can leave the preimage of a
> point empty. Taking the largest point of the half-line's preimage handles
> both at once. <bookmark mark="slide"/> Watch the threshold climb: as y
> rises, the boundary glides to the right, and F of Y grows with it.
> <bookmark mark="uniform"/> The gentlest instance: X uniform on zero one,
> and Y twice X. For y between zero and two, Y at most y means X at most y
> over two, so F of Y at y is y over two. <bookmark mark="stretch"/> The
> density of Y is one half on zero two: the rectangle stretches to double
> width and half height, and the area stays one. An affine function of a
> uniform random variable is uniform.

**Cues**
- opening: section title "Monotone Functions", docked up; `Y = g(X)` with
  muted caption "continuity of X promises nothing about Y" anchors the
  caution (2026-07-05 draft review, 4:02 - the caution played over a bare
  title; the `shape-not-guaranteed` ledger item now gets glyphs).
- `shape-cont`: mini-glyph on a muted baseline - a small smooth density
  bump, muted label "continuous" (2026-07-05 draft review, 4:02).
- `shape-disc`: second mini-glyph - three PMF stems with dots, muted label
  "discrete" (2026-07-05 draft review, 4:02).
- `shape-mixed`: third mini-glyph - a rising CDF piece with a jump to a
  dot, muted label "neither" (2026-07-05 draft review, 4:02).
- `friendliest`: the three shape glyphs fade; a single small rising curve
  in accent, muted label "monotone", takes the center; it fades (with the
  caution line) as the definition arrives (2026-07-05 draft review, 4:02).
- `define`: the definition line `x_1 \leq x_2 \;\Rightarrow\; g(x_1) \leq
  g(x_2)` (SMALL, INK).
- `halfline`: a rising curve g (with one flat plateau) on axes, left column;
  a horizontal dashed threshold at height y; the x-axis segment where the
  curve sits at or below it lights up.
- `sup`: the formula, right column, on two left-aligned lines:
  `F_Y(y) = F_X\left(\sup\{g^{-1}((-\infty, y])\}\right)` in accent (the lit
  segment's dot demotes); spoken flat/jump justification over an `Indicate`
  of the plateau.
- `slide`: the threshold line animates upward; the boundary point slides
  right along the x-axis (racing across the plateau's preimage).
- `uniform`: the g-plot clears; the uniform example takes the stage:
  `F_Y(y) = \Pr(X \leq y/2) = y/2`, `y \in [0, 2]`.
- `stretch`: the height-1 density rectangle on [0,1] morphs to height 1/2 on
  [0,2]; caption "area stays one" (MUTED).

---

## Beat: decreasing-mirror  (scene: DecreasingMirror)

> What if g is monotone decreasing, so larger inputs produce smaller outputs?
> <bookmark mark="flip"/> The same argument runs in a mirror. A high
> threshold on the output is now cleared by small inputs, so the event g of X
> at most y collects everything to the right of a boundary.
> <bookmark mark="formula"/> That boundary is an infimum, and the probability
> of landing at or beyond it is one minus the CDF of X there. The infimum
> plays the same guardian role the supremum played, absorbing the flats and
> the jumps of g. Swap supremum for infimum, and F for one minus F; nothing else
> changes. <bookmark mark="outro"/> The key idea of this video: to find the
> distribution of g of X, describe the event g of X at most y as a set of x
> values, and integrate the density of X over it. Next video, we
> differentiate this answer, and the change-of-variables formula falls out.

**Cues**
- opening: section title "The Decreasing Mirror", docked up.
- `flip`: a falling curve g on axes, left column; the dashed threshold at y;
  now the x-axis lights up to the *right* of the crossing. The left plot
  rides 0.4 higher for visual harmony (2026-07-04 draft review, 6:00).
- `formula`: right column, two left-aligned lines:
  `F_Y(y) = 1 - F_X\left(\inf\{g^{-1}((-\infty, y])\}\right)` in accent;
  MUTED caption "sup becomes inf, F becomes 1 - F". Spoken "Swap sup for
  inf" becomes "Swap supremum for infimum" (2026-07-04 draft review, 6:20).
- `outro`: stage clears; shared outro card - "Key idea" (accent) + two-line
  takeaway + "Coming up:  The Change-of-Variables Formula".

---

## Cut list (if over budget)

1. The `shape-not-guaranteed` aside (the one caution sentence opening
   `monotone-sup`) - saves ~35 words.
2. The flat/jump justification of the supremum ("Why a supremum? ... both at
   once.") compresses to "the supremum absorbs flats and jumps" - saves ~40
   words.
3. The closing sentence of `rayleigh-squared` ("And notice what the method
   needed...") - saves ~20 words.
4. The `slide` sweep in `monotone-sup` ("Watch the threshold climb...") -
   saves ~25 words and one animation.
