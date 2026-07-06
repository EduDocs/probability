---
slug: 37-joint-continuous
title: Joint Continuous Distributions
stage: script             # tex -> concept -> [script] -> scene -> render
status: approved          # approved via scheduled batch instruction 2026-07-03
derived_from: 37-joint-continuous.md
derived_from_sha256: e38021b89e5ff48afd01e32c9930f7dc160380e04f89f2f807c3de561730cd62
provenance_stamped: 2026-07-06
target_scene_file: scenes/joint_continuous.py

# --- Narrative glue (links this video to its neighbours) -------------------
linking:
  objective: "Describe two continuous random variables with one joint CDF - and turn probability into volume under a density surface."
  recap: "Last video: Chernoff and Jensen closed the chapter on bounds - the single-variable toolkit is complete."
  key_idea: "One joint CDF carries the pair; differentiate twice, and probability is volume under a density surface."
  bridge: "Next: conditioning with densities - slicing the surface at a value we observe."

# --- Voice + timing config -------------------------------------------------
voice:
  provider: openai        # final voice (needs OPENAI_API_KEY in .env)
  model: tts-1
  name: nova
  rate: 1.0
words_per_minute: 150
# nova finals measure ~0.31 s/word; drafts render with gTTS at ~0.44 s/word —
# the target budgets the FINAL.
target_runtime_sec: 300
tolerance_sec: 45

estimated_runtime_sec: 366
measured_runtime_sec: 352.5

beats:
  - id: overview
    scene_class: ChapterOverview
    narration_words: 112
    est_sec: 43
    measured_sec: 41.8
    sync_points: [cdf, pdf, marginals, examples]
  - id: joint-cdf
    scene_class: JointCDF
    narration_words: 241
    est_sec: 93
    measured_sec: 84.7
    sync_points: [pmf-table, no-mass, definition, outcome-set, quadrant,
                  region, slide, limit-y, half-plane, limit-y-formula,
                  limit-x, limit-zero, one-function]
  - id: joint-pdf
    scene_class: JointPDF
    narration_words: 198
    est_sec: 76
    measured_sec: 72.9
    sync_points: [mixed, rebuild, surface, volume, rectangle]
  - id: marginal-pdfs
    scene_class: MarginalPDFs
    narration_words: 165
    est_sec: 63
    measured_sec: 63.2
    sync_points: [slice, integrate, both]
  - id: unit-circle
    scene_class: UnitCircleExample
    narration_words: 237
    est_sec: 91
    measured_sec: 89.8
    sync_points: [disk, quarter, gauss, polar, rayleigh, outro]
---

# Video Script — Joint Continuous Distributions

Narration is the source of truth for timing. Each `<bookmark mark="id"/>` is an
authoring synchronization marker realized as a separate sequential
`with self.voiceover(...)` block in the scene.

---

## Beat: overview  (scene: ChapterOverview)

> Last video, Chernoff and Jensen closed the chapter on bounds, and with it
> the single-variable story. But measurements come in pairs — a signal and
> its noise, a position in two coordinates — and they live on a continuum.
> This chapter describes two continuous random variables together.
> <bookmark mark="cdf"/> In this video we meet the joint CDF, one function
> on the plane that records the probability of a whole quadrant,
> <bookmark mark="pdf"/> then differentiate it twice into a density surface,
> where probability becomes volume over a region,
> <bookmark mark="marginals"/> recover each variable's own density by
> integrating the other away, <bookmark mark="examples"/> and run the
> machine on a flat disk and on two Gaussians — where a famous distribution
> falls out.

**Cues** (outline lines appear in sequence with the voice)
- opening block: title card with kicker "Chapter 11  ·  Multiple Continuous
  Random Variables", objective; progress_tag(1, 4) in the DR corner; card
  rises to the top edge.
- `cdf`: outline line "1. The joint CDF" fades in.
- `pdf`: outline line "2. The density surface and volume" fades in.
- `marginals`: outline line "3. Marginal densities" fades in.
- `examples`: outline line "4. Two worked examples" fades in.

---

## Beat: joint-cdf  (scene: JointCDF)

> Two random variables, one experiment. <bookmark mark="pmf-table"/> Chapter
> seven described a discrete pair with a joint PMF — a table of masses.
> <bookmark mark="no-mass"/> On a continuum single points
> carry no mass, so we lean on the tool that carried single variables across
> this bridge: accumulate. <bookmark mark="definition"/> The joint
> cumulative distribution function of X and Y is the probability that X is
> at most x and, at the same time, Y is at most y.
> <bookmark mark="outcome-set"/> Keeping in mind that X
> and Y are functions on one sample space, this is the probability of the
> set of outcomes where both coordinates come in under their thresholds.
> <bookmark mark="quadrant"/> Picture it on the plane. Fix a corner point.
> <bookmark mark="region"/> The event collects every outcome landing at or
> below it and at or to its left — the whole southwest quadrant.
> <bookmark mark="slide"/> Slide the corner up and to the right,
> and the function accumulates probability, the one-variable sweep upgraded
> to two dimensions. <bookmark mark="limit-y"/> Limits recover the pieces.
> <bookmark mark="half-plane"/> Push y to infinity: the constraint on Y
> evaporates, the quadrant grows into a half-plane,
> <bookmark mark="limit-y-formula"/> and the joint CDF becomes the marginal
> CDF of X alone.
> <bookmark mark="limit-x"/> Push x to infinity instead, and the marginal
> CDF of Y comes out. <bookmark mark="limit-zero"/> And push either argument
> down to minus infinity: the quadrant slides off the plane, and the
> function falls to zero — the two-variable version of the CDF endpoints we
> met for a single variable. <bookmark mark="one-function"/> One function
> carries both variables — and both marginals live inside it as limits.

**Cues** (two-column: plane diagram lower-left, formulas at right; the
diagram rides up and to the right of the first draft's spot for balance —
2026-07-05 draft review, 13:14. The shaded quadrant always overflows the
drawn axes past the origin: the event runs to minus infinity both ways.)
- opening block: the definition's left-hand side `F_{X,Y}(x, y)` is written
  (skeleton, INK) as the pair is named — the stage is no longer empty
  through the opening sentences. (2026-07-05 draft review round 3, 0:50)
- `pmf-table`: a small lump-of-mass grid fades in lower-left — the discrete
  joint PMF as a table of masses. (2026-07-05 draft review round 3, 0:50)
- `no-mass`: the grid fades out — single points carry no mass on the
  continuum. (2026-07-05 draft review round 3, 0:50)
- `definition`: the skeleton completes to
  `F_{X,Y}(x,y) = \Pr(X \leq x, Y \leq y)`, accent on the left-hand side.
  (2026-07-05 draft review, 13:14: per-phrase sub-blocks so each
  element lands on its sentence; round 3, 0:50: the LHS now pre-exists.)
- `outcome-set`: the outcome-set form beneath in MUTED, SMALL.
  (2026-07-05 draft review, 13:14)
- `quadrant`: small axes lower-left; the corner dot at (x, y) fades in.
- `region`: the southwest quadrant shades in BLUE at low opacity,
  spilling past both axes. (2026-07-05 draft review, 13:14)
- `slide`: the corner slides up-right and the shaded region grows with it.
  (2026-07-05 draft review, 13:14)
- `limit-y`: the definition demotes to INK.
- `half-plane`: the region stretches past the top of the y-axis
  (half-plane). (2026-07-05 draft review, 13:14)
- `limit-y-formula`: `\lim_{y \to \infty} F_{X,Y}(x,y) = F_X(x)` at right,
  accent moves here. (2026-07-05 draft review, 13:14)
- `limit-x`: symmetric formula `\lim_{x \to \infty} F_{X,Y}(x,y) = F_Y(y)`
  beneath; region stretches rightward instead, past the x-axis tip.
- `limit-zero`: the region shrinks off the lower-left and fades;
  `\lim_{x \to -\infty} F_{X,Y}(x,y) = 0` completes the list.
- `one-function`: the definition is Indicated in accent.
  (2026-07-05 draft review, 13:14)

---

## Beat: joint-pdf  (scene: JointPDF)

> For a single variable, one derivative turned the CDF into a density. Here
> there are two directions, so differentiate twice — once in x, once in y.
> <bookmark mark="mixed"/> When the joint CDF is totally differentiable,
> this mixed partial derivative is the joint probability density function,
> and the order of differentiation does not matter. When the density exists,
> we call the pair jointly continuous. <bookmark mark="rebuild"/> Calculus
> runs backwards too: integrating the density over the quadrant rebuilds the
> CDF. And the density behaves as a density should — never negative, and
> integrating to one over the whole plane. <bookmark mark="surface"/> Now
> the picture to keep. When we built the joint PMF table, it stacked a
> lump of mass on each cell. Let the cells shrink and multiply, and the
> table melts into a
> surface: a height above every point of the plane, tall where the pair is
> likely, flat where it is not. <bookmark mark="volume"/> And probability
> becomes volume. The probability that the pair lands in a region S is the
> double integral of the density over S — the volume trapped under the
> surface, directly above the region. <bookmark mark="rectangle"/> When S is
> a rectangle, the volume is the familiar iterated integral: x from a to b,
> y from c to d.

**Cues**
- opening block: the mixed-partial definition
  `f_{X,Y}(x,y) = \partial^2 F_{X,Y} / \partial x \partial y` is written
  while "differentiate twice" is spoken, so the stage is never empty at the
  beat boundary. (2026-07-05 draft review round 2, 2:12)
- `mixed`: the already-written definition takes the accent; caption
  "jointly continuous when this exists" in MUTED.
  (2026-07-05 draft review round 2, 2:12)
- `rebuild`: `F_{X,Y}(x,y) = \int_{-\infty}^{x}\int_{-\infty}^{y}
  f_{X,Y}(u,v)\,dv\,du` plus the nonnegativity/normalization line, SMALL.
- `surface`: formulas clear; a 4x4 grid of cells with varying opacity (the
  discrete table's lumps) morphs into a smooth heat disk of concentric
  rings — the table-becomes-surface shot; caption "the table becomes a
  surface" in MUTED. (2026-07-04 register pass: narration callback
  re-anchored on the joint PMF table, not a video number.)
- `volume`: a blob region S outlined on the heat map;
  `\Pr((X,Y) \in S) = \iint_S f_{X,Y}(x,y)\,dy\,dx` at right; caption "the
  volume under the surface, above S" in MUTED.
- `rectangle`: S morphs into a rectangle; the iterated integral
  `\int_a^b \int_c^d f_{X,Y}(x,y)\,dy\,dx` written beneath.

---

## Beat: marginal-pdfs  (scene: MarginalPDFs)

> One variable at a time, again. The joint object answers every question,
> but often we want one variable's own distribution. In the discrete
> chapter, marginalizing meant summing a table's row; here the row is a
> slice of the surface. <bookmark mark="slice"/> Fix a value of y and cut
> the surface along it. The slice's profile shows how the mass along that
> line is spread across x. <bookmark mark="integrate"/> Integrate the slice
> over all of x, and the total is the marginal density of Y at that value.
> The row sum from the discrete joint-table video has become an integral:
> the marginal
> density of Y is the integral, over x, of the joint density. No new
> principle here — just the discrete recipe with the sum promoted to an
> integral. <bookmark mark="both"/> Symmetrically, integrating out y leaves
> the marginal density of X. And the old warning carries over word for
> word: the joint determines the marginals, but not conversely. Just as two
> different tables shared identical margins, two different surfaces can
> cast identical shadows.

**Cues**
- opening block: a small 3x3 joint table at left with one row lit in
  accent — the video-21 mirror on screen while it is named.
- `slice`: table demotes; the heat disk appears at left with a horizontal
  slice line at the fixed y, in accent.
- `integrate`: `f_Y(y) = \int_{-\infty}^{\infty} f_{X,Y}(x,y)\,dx` at
  right in accent; the slice line's role spoken as the formula lands.
  (2026-07-04 register pass: row-sum callback re-anchored on the discrete
  joint-table video, not a video number.)
- `both`: `f_X(x) = \int_{-\infty}^{\infty} f_{X,Y}(x,y)\,dy` beneath in
  INK; caption "the joint determines the marginals, not conversely" in
  MUTED.

---

## Beat: unit-circle  (scene: UnitCircleExample)

> Time to run the machine, twice. First, the flattest surface there is.
> <bookmark mark="disk"/> Let the pair be uniform on the unit circle: the
> density is one over pi inside the disk and zero outside — constant
> height, total volume one. <bookmark mark="quarter"/> What is the
> probability of landing within radius one half? Volume above the small
> disk: a constant height times its area. The small disk holds one quarter
> of the area, so the probability is one quarter. Under a flat density,
> probability is literally area. <bookmark mark="gauss"/> Now a curved
> surface. Take two independent zero-mean Gaussians with the same variance
> sigma squared. Their joint density is the bell curve spun into a
> two-dimensional Gaussian density — tallest at the origin, falling with
> the squared distance from
> it. <bookmark mark="polar"/> Ask for the probability that the point lands
> within distance s of the origin. Switch the double integral to polar
> coordinates and it collapses, leaving one minus e to the minus s squared
> over two sigma squared. <bookmark mark="rayleigh"/> Look at what that is:
> the CDF of the distance R itself. Differentiate once, and R has the
> Rayleigh density — s over sigma squared, times e to the minus s squared
> over two sigma squared. The Rayleigh entered the course as a catalog
> entry; the joint density just derived it. <bookmark mark="outro"/> The
> key idea of this video: one joint CDF carries a pair of continuous
> variables — differentiate it twice, and probability becomes volume under
> a density surface.

**Cues** (halfway rule, 2026-07-05 draft review round 3: the disk, the
Gaussian patch, and the Rayleigh plot all center on CONTENT_MID_Y)
- `disk`: the unit disk at left, centered on CONTENT_MID_Y, with a SHARP
  boundary — the uniform density drops off discontinuously at the circle's
  edge, so the flat patch gets a hard-cutoff mask (~1.5 px anti-aliasing,
  no soft fade); the cases-form density `f_{X,Y} = 1/\pi` on the disk, `0`
  otherwise, at right. (2026-07-05 draft review round 3, 5:41)
- `quarter`: the inner radius-1/2 disk outlined in accent;
  `\Pr((X,Y) \in S) = \frac{1}{\pi}\cdot\pi\left(\frac{1}{2}\right)^2
  = \frac{1}{4}` lands with "one quarter."
- `gauss`: disk clears; the soft Gaussian gradient patch (TEAL) at left,
  centered on CONTENT_MID_Y (2026-07-05 draft review round 3, 6:05);
  `f_{X,Y}(x,y) = \frac{1}{2\pi\sigma^2}
  e^{-(x^2+y^2)/(2\sigma^2)}` at right. (2026-07-04 register pass: bare
  "bell surface" became "two-dimensional Gaussian density"; the single
  "bell curve" stays.)
- `polar`: a circle of radius s grows over the heat disk in accent;
  `\Pr(R \leq s) = 1 - e^{-s^2/(2\sigma^2)}` written as it grows.
- `rayleigh`: heat disk leaves; a small plot of the Rayleigh density curve
  appears, centered on CONTENT_MID_Y (2026-07-05 draft review round 3,
  6:38); `f_R(s) = \frac{s}{\sigma^2} e^{-s^2/(2\sigma^2)}` in accent.
- `outro`: shared outro card — key idea + "Coming up: Conditioning with
  Densities".

---

## Cut list (if over budget)

1. Compress the disk example to one picture with the one-quarter answer
   spoken over it (drop the `quarter` area-ratio formula walk).
2. Drop the closing shadows sentence of `marginal-pdfs` ("Just as two
   different tables...").

Applied 2026-07-04: trimmed the rectangle sentence in `joint-pdf` ("Nothing
about the recipe is new...") to bring the projected final inside tolerance.

Applied 2026-07-05 (draft review round 2): the `joint-pdf` mixed-partial
definition now lands during the opening sentence (cue moved, narration
verbatim — no re-split); the shared density-patch center, the lump grid /
ninths table, and the volume equation stack were lifted onto the
halfway-between-title-and-frame-bottom rule.
