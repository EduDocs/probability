---
slug: 39-independence-continuous
title: Independent Continuous Variables
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 39-independence-continuous.md
derived_from_sha256: 618554280c32b9bfd027b98cd175b96d48be7f43eb551866444be5e121060b9a
provenance_stamped: 2026-07-06
target_scene_file: scenes/independence_continuous.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Certify independence with one factoring equation - joint CDF, density, and every event pair split into products."
  recap: "Last video: conditioning with densities - slice the joint at the observed value, and the slice responds."
  key_idea: "Independence is a factoring joint: CDF, density, and every event pair split - and conditioning learns nothing new."
  bridge: "Next: sums of continuous random variables - the distribution of W = X + Y, with the summands independent."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 290
tolerance_sec: 45

estimated_runtime_sec: 362
measured_runtime_sec: 330.9

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 87
    est_sec: 33
    measured_sec: 33.8
    sync_points: [definition, faces, example]
  - id: indep-cdf-def
    scene_class: IndependenceDefinition
    narration_words: 177
    est_sec: 68
    measured_sec: 61.8
    sync_points: [cdf, def, all, universal]
  - id: pdf-factorizes
    scene_class: PDFFactorizes
    narration_words: 194
    est_sec: 75
    measured_sec: 67.4
    sync_points: [derive, product, picture, cells, gaussian]
  - id: conditional-is-marginal
    scene_class: ConditionalIsMarginal
    narration_words: 223
    est_sec: 86
    measured_sec: 80.7
    sync_points: [recall-slice, recall-responds, divide, marginal, slices,
                  events, split]
  - id: unit-square
    scene_class: UnitSquareExample
    narration_words: 259
    est_sec: 100
    measured_sec: 87.2
    sync_points: [joint, factors, w, point, region, verdict, outro]
---

# Video Script — Independent Continuous Variables

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

Note: the concept ledger's `events-factor` entry is folded into the
`conditional-is-marginal` beat (five beats total per the chapter directive);
it keeps its own sync points (`events`, `split`).

---

## Beat: overview  (scene: ChapterOverview)

> Last video, conditioning with densities: observe one variable, and the
> density of the other responds, slice by slice. This video is about the
> opposite situation, the one where nothing responds at all.
> <bookmark mark="definition"/> We define independence for continuous
> variables with a single factoring equation, <bookmark mark="faces"/> watch
> it cascade down to densities, to conditional slices, and to every pair of
> events, <bookmark mark="example"/> and then put the definition to work on
> the unit square, where the two coordinates pass the test and a third
> variable, built from the first two, fails it.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 11  ·  Multiple Continuous
  Random Variables", objective; card rises to the top edge;
  `progress_tag(3, 4)` in the DR corner; `self.wait(0.5)` after the block.
- `definition`: outline line "1. The definition: a factoring CDF" fades in.
- `faces`: outline line "2. Densities, slices, and events factor too"
  fades in.
- `example`: outline line "3. The unit square: one pass, one fail" fades in.

---

## Beat: indep-cdf-def  (scene: IndependenceDefinition)

> When does knowing X tell you nothing about Y? Chapter seven answered for
> discrete variables with a table: independence meant every cell of the
> joint PMF was the product of its row margin and its column margin.
> <bookmark mark="cdf"/> Continuous variables have no table. But every pair
> of random variables has a joint CDF: the probability of the quadrant where
> X stays at or below little x and Y stays at or below little y.
> <bookmark mark="def"/> That is where the definition lives. X and Y are
> independent when the joint CDF factors: F of X and Y, at x and y, equals
> F of X at x, times F of Y at y. <bookmark mark="all"/> And the equality
> must hold at every point of the plane. Pick any corner; the probability of
> its quadrant splits into a product. One quadrant that refuses to split is
> enough to destroy independence. <bookmark mark="universal"/> Because the
> CDF exists for every random variable, discrete, continuous, or mixed, this
> one equation is the master definition. The rest of this video is what it
> becomes once densities enter the picture.

**Cues**
- opening: section title "Independence" written, docked to the top; the
  video-24 callback spoken over a small factored-table glyph (three-by-three
  lattice, muted) that fades once the continuous story starts.
- `cdf`: a plane (axes, muted) on the left; a point (x, y) marked and the
  quadrant to its lower-left shaded in BLUE at low opacity; label
  `F_{X,Y}(x,y)` beneath the plane.
- `def`: `F_{X,Y}(x,y) = F_X(x)\, F_Y(y)` in accent, right column.
- `all`: caption `\text{for all } x, y \in \mathbb{R}` beneath it (muted);
  the marked corner point slides to a second position and the shaded
  quadrant follows — the product must survive the move.
- `universal`: muted caption "one definition for every kind of random
  variable" beneath the equation block.

---

## Beat: pdf-factorizes  (scene: PDFFactorizes)

> Now let the pair be jointly continuous, and differentiate. The joint
> density is the mixed partial derivative of the joint CDF, once in x and
> once in y. <bookmark mark="derive"/> On a factored CDF, each derivative
> acts on its own factor: the derivative of F of X in x, times the
> derivative of F of Y in y. <bookmark mark="product"/> Those are the
> marginal densities. The joint density factors too: f of X and Y, at x and
> y, equals f of X at x, times f of Y at y. <bookmark mark="picture"/> Here
> is the picture to keep. Lay the density of X along the horizontal edge,
> and the density of Y along the vertical edge. The joint density over the
> square is woven from their product: the shade over any point is its column
> profile times its row profile. The table that factored for discrete
> variables has become a factoring density. <bookmark mark="cells"/>
> Wherever X is likely and Y is likely, the joint is at its darkest; thin
> either margin, and its whole row or column thins with it.
> <bookmark mark="gaussian"/> The two independent Gaussians from when we
> met the joint density were built exactly this way. There we wrote the
> product on faith; this equation is the license.

**Cues**
- opening: section title "The Density Factors"; the mixed-partial
  definition `f_{X,Y}(x,y) = \partial^2 F_{X,Y} / \partial x \partial y`
  written (INK).
- `derive`: the factored derivative line
  `= (dF_X/dx)(x) \cdot (dF_Y/dy)(y)` appears beneath (INK, two-step
  reveal).
- `product`: `f_{X,Y}(x,y) = f_X(x)\, f_Y(y)` lands in accent; the
  derivation demotes to muted.
- `picture`: left column: a square region; a bell-shaped `f_X` profile
  along its bottom edge and a bell-shaped `f_Y` profile rotated along its
  left edge; inside, a smooth product-density gradient — the
  `density_patch` ImageMobject technique (deterministic numpy intensity
  `f_X(x) f_Y(y)`, alpha channel, bicubic, no outline) — replacing the
  earlier cell grid, which read as a discrete table (2026-07-05 draft
  review, 2:42). (2026-07-04 register
  pass: "Video twenty-four's factoring table" is now "The table that
  factored for discrete variables" — topic anchor, not a number.)
- `cells`: a flash at the gradient's darkest point; the `f_X` margin thins
  at one x and the whole column above it thins with it (a second
  precomputed dipped gradient cross-faded in, then restored)
  (2026-07-05 draft review, 2:42).
- `gaussian`: muted caption "the joint density's two Gaussians: f X times
  f Y by construction" beneath the picture. (2026-07-04 register pass:
  narration "of video thirty-seven" is now "from when we met the joint
  density"; the on-screen caption dropped its number too — it lived in a
  MathTex \text{} block, which the language lint now scans.)

---

## Beat: conditional-is-marginal  (scene: ConditionalIsMarginal)

> Last video made dependence visible: condition on X equals x,
> <bookmark mark="recall-slice"/> and the slice of the joint density at x,
> renormalized, becomes the conditional density of Y.
> <bookmark mark="recall-responds"/> Slide the observation, and the slice
> responds.
> <bookmark mark="divide"/> Watch what independence does to that machinery.
> The conditional density is the joint over the marginal. But the joint is
> now a product, so the factor f of X at x cancels top and bottom,
> <bookmark mark="marginal"/> and what remains is the marginal density of Y,
> alone, wherever f of X at x is not zero. Observing X changes nothing about
> Y. <bookmark mark="slices"/> Every slice, at every x you might observe,
> renormalizes to the same curve. The responsiveness we called dependence
> has been switched off. This is the discrete lesson that all the table's
> rows were proportional, now said with densities. <bookmark mark="events"/>
> And the product climbs back up to events. Take any set S of values for X,
> and any set T for Y. The probability that both happen at once is a double
> integral of the joint density over the rectangle S cross T.
> <bookmark mark="split"/> Factor the integrand, and the double integral
> splits into two ordinary ones: the probability that X lands in S, times
> the probability that Y lands in T. Independent variables manufacture
> independent events, every pair of them at once, exactly the notion chapter
> four defined one pair at a time.

**Cues**
- opening: section title "Conditioning Learns Nothing"; a preview square
  centered on the halfway anchor below the title, with a dashed slice line
  at one x and the muted label `X = x` — the recalled conditioning picture
  drawn live instead of a dark frame (2026-07-05 draft review, 3:30).
- `recall-slice`: the renormalized slice profile (accent) drawn along the
  line — the conditional density of Y (2026-07-05 draft review, 3:30).
- `recall-responds`: line, label, and profile slide to a new x and the
  profile changes shape — the dependent slice responds
  (2026-07-05 draft review, 3:30).
- `divide`: the preview square fades out;
  `f_{Y \mid X}(y \mid x) = f_{X,Y}(x,y) / f_X(x)
  = f_X(x) f_Y(y) / f_X(x)` written line by line.
- `marginal`: `= f_Y(y)` lands in accent; muted caption "wherever f X of x
  is not zero".
- `slices`: left column: a square region with three vertical slice lines at
  different x positions; above each, the identical small profile curve —
  the slice family frozen (video 38's sweep, switched off).
- `events`: the square replaced by a plane with a vertical strip (X in S,
  BLUE at low opacity) and a horizontal strip (Y in T, TEAL at low
  opacity); their intersection rectangle is the event, with
  `\Pr\left(X \in S, Y \in T\right) = \int_S \int_T f_{X,Y}(x,y)\,dy\,dx`
  at the right. (Strips deliberately overlap: `mark_intended_overlap`.)
- `split`: the equation continues
  `= \int_S f_X(x)\,dx \int_T f_Y(y)\,dy = \Pr\left(X \in S\right)
  \Pr\left(Y \in T\right)` in accent; the rectangle's edges flash with its
  two generating strips.

---

## Beat: unit-square  (scene: UnitSquareExample)

> Time to run the test honestly. Pick a point uniformly at random from the
> unit square, and let X and Y be its two coordinates.
> <bookmark mark="joint"/> For x and y between zero and one, the joint CDF
> is the area of the corner rectangle: x times y.
> <bookmark mark="factors"/> But x is exactly F of X at x, and y is F of Y
> at y. The joint is the product at every such point, and writing the CDF
> as a product of two indicator integrals extends the check to the whole
> plane. The coordinates are independent. <bookmark mark="w"/> Now build a
> third variable from the same two coordinates: W, the sum of X and Y. A
> variable assembled out of X should remember X. Independence needs every
> point of the plane to factor, so a single failure convicts.
> <bookmark mark="point"/> Evaluate at the point x equals one half, w
> equals one. F of W at one is one half, and F of X at one half is one
> half, so the product is one quarter. <bookmark mark="region"/> The joint
> CDF is the probability of landing left of one half and below the diagonal
> line: a trapezoid of area three eighths. <bookmark mark="verdict"/> Three
> eighths is not one quarter. X and W are dependent, not through anything
> exotic, but simply because one variable was built from the other.
> <bookmark mark="outro"/> The key idea of this video: independence is a
> factoring joint. The CDF, the density, and every pair of events split
> into products, and conditioning learns nothing new. As for the sum W, its
> distribution is precisely where the next video begins.

**Cues**
- opening: section title "The Unit Square, Both Verdicts"; the unit square
  drawn on the left (BLUE fill at low opacity), corner labels 0 and 1;
  the point `(x, y)` uniform on `[0,1]^2` with `X = x`, `Y = y` typeset at
  the right (2026-07-05 draft review, 5:19: the on-screen coordinates read
  x, y — not `\omega_1, \omega_2`; the vendored source normalized to
  match).
- `joint`: the corner rectangle `[0,x] \times [0,y]` shaded (GREEN, low
  opacity) inside the square at a fixed sample point (x, y) = (0.7, 0.55);
  `F_{X,Y}(x,y) = xy` written.
- `factors`: `= F_X(x)\, F_Y(y)` continues in accent; muted one-line
  caption for the indicator extension
  (`\mathbf{1}_{[0,1]}(u)`-integral form).
- `w`: shaded rectangle clears; `W = X + Y` typeset; the diagonal line
  `x + y = 1` drawn across the square.
- `point`: the three numbers written as a small stack: `F_W(1) = 1/2`,
  `F_X(0.5) = 1/2`, product `= 1/4`.
- `region`: the trapezoid `{x \le 1/2,\ x + y \le 1}` shaded (MAROON, low
  opacity); `F_{X,W}(0.5, 1) = \int_0^{1/2}(1-x)\,dx = 3/8` written.
- `verdict`: `3/8 \neq 1/4` in accent; `Indicate` on the inequality.
- `outro`: stage clears; `outro_bridge` key-idea card ("Independence is a
  factoring joint: CDF, density, events" / "and conditioning learns nothing
  new."), bridge line "Coming up: Sums of Continuous Random Variables";
  W's distribution is deliberately NOT derived here — video 40 opens with
  it.

---

## Cut list (if over budget)

1. Compress the indicator-function extension in `unit-square` (`factors`)
   to nothing — keep only the [0,1] computation (saves ~2 sentences, ~8 s).
2. Drop the `gaussian` callback sentence pair in `pdf-factorizes`
   (saves ~10 s).
3. Trim the `universal` closing sentences of `indep-cdf-def` to one
   sentence (saves ~8 s).
4. Shorten the `events`/`split` narration in `conditional-is-marginal` to
   the statement plus "the double integral splits" (saves ~12 s).
