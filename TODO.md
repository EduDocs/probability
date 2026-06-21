# TODO

Open items from the `/progression` audit of the chapter sidecars (run on
bootstrapped `.md` files in `chapters/`). Each item is a sidecar-level fix —
surgical and additive — unless flagged otherwise.

## Blockers (story does not hold as ordered)

- [ ] **OGF forward-reference in `chapters/discrete_expectations.md`.**
  The OGF bullet invokes "sums of independent RVs" via convolution, but
  independence of RVs is only introduced one chapter later in
  `chapters/discrete_vectors.md`. Upstream, `conditional_probability.md` only
  defines independence of *events*.
  - Option A: split the OGF bullet. Keep "OGF encodes the PMF; derivatives at 1
    recover moments" in `discrete_expectations.md`; move the
    convolution/independent-sums half to `discrete_vectors.md`.
  - Option B: add an "independence of two RVs" bullet to
    `discrete_expectations.md` as a brief setup before the OGF bullet.

- [ ] **MGF forward-reference in `chapters/expectations_and_bounds.md`.**
  The MGF multiplicativity bullet and the Chernoff bound assume independence of
  RVs (in particular, continuous RVs). Independence of continuous RVs is only
  introduced one chapter later in `chapters/random_vectors.md`.
  - Option A: add an "independence of RVs" bullet to
    `continuous_random_variables.md` so the construct is in place before
    `expectations_and_bounds.md` uses it.
  - Option B: reorder so `random_vectors` precedes `expectations_and_bounds`.
  - Option C: add an upstream-pointer bullet to `expectations_and_bounds.md`
    that explicitly leans on `discrete_vectors.md`.

## Warnings (coherent but fraying)

- [ ] **Late-defined constructs in `chapters/continuous_random_variables.md`.**
  Gamma is described as "sums of independent exponentials" and Rayleigh as
  "norm of 2D Gaussian," but sums of independent continuous RVs and the 2D
  joint Gaussian are not formalized until `random_vectors.md`.
  Fix: mark these bullets as forward-pointers ("formalized in
  `random_vectors.md`"), or trim to a parametric definition.

- [ ] **Orphaned promise in `chapters/conditional_probability.md`.**
  The closing bullet promises "equivalent notations conventions used in the
  rest of the notes" but no downstream sidecar delivers on it.
  Fix: replace with the explicit conventions actually used (`Pr(A|B)`,
  `p_{X|Y}(x|y)`, `E[X|Y]` as a random variable vs. `E[X|Y=y]` as a value), or
  drop the bullet.

- [ ] **Orphaned indicator-function setup in `chapters/mathematical_review.md`.**
  The indicator function is introduced but no later sidecar names it again
  (Bernoulli is implicitly one).
  Fix: drop from `mathematical_review.md`, or add a tie-back bullet in
  `discrete_random_variables.md` ("Bernoulli RV = indicator of an event").

- [ ] **"iid" used but never defined as a spine concept.**
  `discrete_random_variables.md` ("iid Bernoulli trials") and
  `empirical_sums.md` (LLN/CLT) both use "iid" without any sidecar
  introducing it.
  Fix: add an "iid" bullet to `chapters/discrete_vectors.md` right after the
  independence-of-RVs bullet so it has a canonical home before
  `empirical_sums` invokes it.

## Notes (optional polish)

- [ ] **Missing unifying "joint distribution" concept.**
  Joint PMF (`discrete_vectors.md`) and joint PDF / joint CDF
  (`random_vectors.md`) are introduced cleanly, but nothing bridges them.
  Fix: a one-line bullet in `random_vectors.md` — "joint CDF / joint PDF
  generalize the joint PMF (`discrete_vectors.md`) and the univariate CDF
  (`continuous_random_variables.md`)."

- [ ] **Starred / orphaned setups (acceptable, just confirm).**
  Stirling's formula (starred, in `combinatorics.md`) and mixed RVs (starred,
  in `continuous_random_variables.md`) are not used downstream. Fine for
  starred topics; flagged for completeness.

## Out-of-scope chapter (separate issue, not a progression finding)

- [ ] **`chapters/appendix.tex` looks unfinished and mis-titled.**
  - `\chapter{Sums}` — the title is "Sums," not "Appendix."
  - Opens with an unmotivated `E[Y] = sum y p_Y(y)` derivation block that reads
    like a fragment imported from another chapter.
  - Only `sum k` has a proof; `sum k^2` and `sum k^3` are stated bare.
  - Currently commented out of `UndergraduateProbabilityI.tex` (`%\include{chapters/appendix}`).
  Decide: finish the appendix, fold its content into another chapter, or
  delete it.

## Process

- The progression audit is naturally convergent — re-running `/progression`
  after applying any of the above will surface fewer findings. Fixes are
  ask-first and additive; never delete a sidecar's scratch / open-questions /
  rationale to "clean up."
- A `.md` fix that implies prose work is a follow-up `/md2tex` pass on the
  same chapter; don't touch the `.tex` from the progression audit.
