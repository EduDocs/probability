# TODO

Open items from the `/progression` audit of the chapter sidecars (run on
bootstrapped `.md` files in `chapters/`). Each item is a sidecar-level fix —
surgical and additive — unless flagged otherwise.

Reconciled against a re-run of `/progression` on 2026-06-28. That pass
reframed the two blocker pairs as **2-cycles** (each chapter requires a concept
the other introduces), confirmed the regenerated concept map now flags
`continuous_random_variables → joint-pdf` mechanically, and closed the `iid`
item below.

## Blockers (story does not hold as ordered)

- [ ] **OGF forward-reference in `chapters/discrete_expectations.md`.**
  The OGF bullet invokes "sums of independent RVs" via convolution, but
  independence of RVs is only introduced one chapter later in
  `chapters/discrete_vectors.md`. Upstream, `conditional_probability.md` only
  defines independence of *events*.
  This is one half of a **2-cycle**: `discrete_expectations` requires
  `independence-of-rvs` / `convolution` from `discrete_vectors`, while
  `discrete_vectors` requires `expectation` / `ogf` back from
  `discrete_expectations`.
  - Option A: split the OGF bullet. Keep "OGF encodes the PMF; derivatives at 1
    recover moments" in `discrete_expectations.md`; move the
    convolution/independent-sums half to `discrete_vectors.md`.
  - Option B: add an "independence of two RVs" bullet to
    `discrete_expectations.md` as a brief setup before the OGF bullet.
  - Option C (recommended — mirrors the `event`/`iid` precedent): treat the
    convolution/independence link as a *preview*. Drop `independence-of-rvs`
    and `convolution` from this sidecar's `requires`, and annotate the OGF
    bullet that the property is previewed here and formalized in
    `discrete_vectors.md`. This breaks the cycle at the frontmatter level, the
    way `combinatorics` defers `event` and `discrete_vectors` re-grounds `iid`.

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
  - **`joint-pdf` 2-cycle (now mechanically flagged).** The sidecar's
    `requires` lists `joint-pdf`, introduced later in `random_vectors.md`
    (which depends back on `cdf`/`pdf`/`gaussian`), so the regenerated concept
    map reports it as a forward reference. But **nothing in the
    continuous-RV spine actually uses `joint-pdf`** — the outline is
    single-variable throughout. Likely a *stale `requires` entry*. The one
    possible genuine use is deriving Rayleigh as the norm of a 2-D Gaussian;
    check `continuous_random_variables.tex`. If unused, remove `joint-pdf` from
    `requires` (clears the cycle); if used, keep it and add the forward-pointer
    above.

- [ ] **Orphaned promise in `chapters/conditional_probability.md`.**
  The closing bullet promises "equivalent notations conventions used in the
  rest of the notes" but no downstream sidecar delivers on it.
  Fix: replace with the explicit conventions actually used (`Pr(A|B)`,
  `p_{X|Y}(x|y)`, `E[X|Y]` as a random variable vs. `E[X|Y=y]` as a value), or
  drop the bullet.

- [ ] **Orphaned indicator-function setup in `chapters/sets_and_functions.md`.**
  The indicator function is introduced but no later sidecar names it again
  (Bernoulli is implicitly one).
  Fix: drop from `sets_and_functions.md`, or add a tie-back bullet in
  `discrete_random_variables.md` ("Bernoulli RV = indicator of an event").

- [x] **"iid" used but never defined as a spine concept.** *(Resolved.)*
  `discrete_random_variables.md` now `introduces: iid` with a spine bullet
  (informal, via independence of events), and `discrete_vectors.md` re-grounds
  it ("made rigorous at the RV level here once independence of random variables
  is defined") right after the independence-of-RVs bullet — the canonical home
  the fix called for. The 2026-06-28 re-run treats this as a well-handled
  spiral, not a defect.

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

- [ ] **Orphaned `conditional-independence` in `chapters/conditional_probability.md`.**
  Introduced but never consumed by a later sidecar. Standard topic, defensible
  to keep, but it is a dangling setup. Confirm it stays, or add a downstream
  tie-back (e.g. naive-Bayes-style factoring) if one fits.

- [ ] **`binomial-theorem` introduced twice.**
  Both `combinatorics.md` and the parked `appendix_background.md` introduce it
  (flagged under "Aliasing / redundancy" in the concept map). Harmless while
  the appendix stays parked; if it is ever `\include`d, make one the canonical
  introduction and the other a back-reference.

## Out-of-scope chapter (separate issue, not a progression finding)

- [ ] **`chapters/appendix.tex` looks unfinished and mis-titled.**
  - `\chapter{Sums}` — the title is "Sums," not "Appendix."
  - Opens with an unmotivated `E[Y] = sum y p_Y(y)` derivation block that reads
    like a fragment imported from another chapter.
  - Only `sum k` has a proof; `sum k^2` and `sum k^3` are stated bare.
  - Currently commented out of `probability.tex` (`%\include{chapters/appendix}`).
  Decide: finish the appendix, fold its content into another chapter, or
  delete it.

## Outside the structural audit (graph-resolution limits)

`just concept md` reads the YAML frontmatter and surfaces forward references
as a set-membership check. Two findings above are **deliberately invisible to
that mechanical audit** and live only in this document:

- **MGF blocker in `expectations_and_bounds.md`** (above). At the frontmatter
  level, `independence-of-rvs` *is* introduced upstream (in
  `discrete_vectors.md`), so the graph treats this as satisfied. The actual
  defect is that the discrete introduction does not extend to continuous RVs
  without the construction in `random_vectors.md`. The sidecars do not split
  the concept into `independence-of-rvs-discrete` / `-continuous`, so the gap
  shows up only in prose.
- **Gamma / Rayleigh warning in `continuous_random_variables.md`** (above).
  Two distinct cases, now separated: `independence-of-rvs` *is* introduced
  upstream (in `discrete_vectors.md`), so the graph treats it as satisfied even
  though the *continuous* formalization only lands in `random_vectors.md` — that
  discrete-vs-continuous gap is the part invisible to the graph. By contrast
  `joint-pdf` is introduced **downstream** in `random_vectors.md`, so the graph
  *does* flag it as a forward reference (see the `joint-pdf` 2-cycle item
  above); it is not invisible.

If we ever want these flagged mechanically, the fix is to split the concept
in the sidecars' frontmatter (`independence-of-rvs-discrete`,
`independence-of-rvs-continuous`) and update the chapters that introduce /
require each variant. For now, leave the graph at its current resolution and
track these via this TODO.

## Process

- The progression audit is naturally convergent — re-running `/progression`
  after applying any of the above will surface fewer findings. Fixes are
  ask-first and additive; never delete a sidecar's scratch / open-questions /
  rationale to "clean up."
- A `.md` fix that implies prose work is a follow-up `/md2tex` pass on the
  same chapter; don't touch the `.tex` from the progression audit.
