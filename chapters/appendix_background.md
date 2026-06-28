---
introduces: [
  arithmetic-series,
  geometric-series,
  sum-of-powers,
  taylor-series,
  integration-by-parts,
  substitution-rule,
  partial-fractions,
  improper-integral,
  gaussian-integral,
  gamma-function,
  beta-function,
  partial-derivative,
  double-integral,
  polar-coordinates,
  squeeze-theorem,
  l-hopital,
  monotone-convergence-of-sequences,
  binomial-theorem,
  vandermonde-identity,
  pascal-identity
]
requires: []
---

# Mathematical Background — scratch

> Scratch/ideas only.
> The shipped prose lives in `appendix_background.tex`.
> Not part of the LaTeX build.

## Purpose

A reference appendix consolidating the calculus and discrete-math facts the
notes assume but that students routinely need to look up, together with a
summary table of the named distributions the notes introduce. Designed for
**lookup, not linear reading** — the main chapters call back to specific entries via
semantic labels (`\Cref{app:gaussian-integral}`, not `Appendix A.3`). The
preliminaries chapter (`mathematical_review.tex`) stays the *motivating*
front-matter; this appendix is the *reference manual*.

## Key points / outline

### Series and sums
- Arithmetic series and its closed form.
- Geometric series (finite and infinite); convergence condition `|r| < 1`.
- Sum of `k`, `k^2`, `k^3` over `k = 1..n`; proofs by induction or telescoping.
- Taylor / Maclaurin series for `exp`, `log(1+x)`, `(1+x)^a`, `sin`, `cos`.
- Ratio test (one-line statement; for power-series convergence in Ch. 7 OGF use).

### Useful integrals
- Integration by parts; substitution; partial fractions.
- Improper integrals (limits of definite integrals); tail bounds.
- The Gaussian integral `∫ exp(-x^2/2) dx = √(2π)`, via the polar-coordinates trick.
- The gamma function `Γ(α) = ∫_0^∞ x^{α-1} e^{-x} dx`; recursion `Γ(α+1) = α Γ(α)`; `Γ(1/2) = √π`.
- The beta function `B(α, β)`; relation to gamma.

### Multivariable calculus
- Partial derivatives; mixed partials (Clairaut).
- Double / iterated integrals; Fubini for switching order on rectangles.
- The Jacobian determinant and the multivariable change-of-variables formula
  (note: the *univariate* form is the prerequisite for Ch. 9 derived
  distributions; the multivariate form is the prerequisite for Ch. 12).
- Polar coordinates and the standard `r dr dθ` substitution.

### Limits and asymptotics
- Squeeze / sandwich theorem.
- L'Hôpital's rule.
- Monotone and bounded convergence of sequences of real numbers.
- Stirling's approximation `n! ≈ √(2π n) (n/e)^n` (used starred in Ch. 2; the
  derivation lives here so the chapter can stay focused on counting).

### Counting identities (deeper review)
- Binomial theorem and its derivative-trick corollaries.
- Vandermonde's identity.
- Pascal's identity / Pascal's triangle.
- Inclusion–exclusion in its general form (the two- and three-set forms are
  covered in `basic_concepts.tex`; the general statement and a short induction
  proof live here).

### Distribution reference table
- A compact lookup table of the named distributions introduced in the notes:
  name, parameters, PMF or PDF, mean, and variance — one row per distribution.
- Discrete rows: Bernoulli, binomial, Poisson, geometric, discrete uniform.
- Continuous rows: uniform, Gaussian, exponential, gamma, Rayleigh, Laplace,
  Cauchy (mean and variance undefined), plus the bivariate normal (mean vector
  and covariance matrix).
- A summary, not a source: each row back-references the chapter where the
  distribution is defined; the table only collects results already derived.

## Open questions

- **File naming.** Keep as a single `appendix_background.{tex,md}`, or split
  into `appendix_series.tex`, `appendix_integration.tex`, etc. for finer-grained
  inline pointers? A single file is simpler; a split gives shorter `\Cref`
  targets at the cost of more files.
- **Scope.** Include a linear-algebra primer (dot product, norms, eigenstructure)
  for Ch. 12 random vectors? Currently omitted — the chapter only assumes 2D
  vectors and norms — but covariance matrices come close to needing it.
- **Audience calibration.** How much is too much? The risk is the appendix
  inflating into a calculus textbook. Resolution: include only facts the main
  chapters actually call back to (or are likely to within one revision); do not
  speculatively add "things a probability student might need."
- **Relationship to `mathematical_review.tex`.** Is the boundary clear? Rough
  rule: Ch. 1 is for *probability-specific set/function setup* (sample space as
  universal set, indicator function, σ-field preview); this appendix is for
  *calculus and arithmetic identities the prose calls back to*. Re-check at
  next `/progression`.

## Notes & references

- Inline pointers from chapters should be **semantic labels**, not numeric
  ("see the appendix on Gaussian integrals" + `\Cref{app:gaussian-integral}`,
  not "see Appendix A.3"). See the earlier discussion in the project log.
- The `mathematical_review.tex` chapter remains the motivating preliminaries
  read up front. This appendix is purely a reference manual.
- `chapters/appendix.tex` (titled "Sums" and currently `\include`-commented)
  contains partial proofs of `Σ k`, `Σ k^2`, `Σ k^3`. Its content folds
  naturally into the *Series and sums* section above; treat the existing file
  as the seed material once this appendix is realized into `.tex`.

## Decisions

- Authored as `appendix_background.{md,tex}` (new) rather than overwriting the
  existing parked `appendix.{md,tex}` (the "Sums" chapter flagged as
  mistitled/unfinished in `TODO.md`). This keeps the broken file isolated; once
  this appendix is realized into `.tex`, the parked `appendix.tex` should be
  retired and its useful sum-formula content folded into *Series and sums*.
- Framed as a **reference appendix**, not a self-contained refresher.
  Pedagogical move: students read `mathematical_review.tex` up front
  (motivation, framed for this book's notation) and consult this appendix
  on-demand when a later chapter calls back. See the in-conversation
  discussion of the Bishop / ESL hybrid pattern.
- `requires: []` because the appendix should depend only on the calculus
  prerequisite, not on any book concept. If a later draft notices it leaning
  on a book concept, that is a signal the content belongs in a chapter, not
  the appendix.
- Added a *Distribution reference table* section (REVIEW4 D13). This is a
  deliberate exception to the `requires: []` rule above: the table tabulates
  the means, variances, and PMFs/PDFs already derived in the distribution
  chapters, so it back-references book concepts rather than re-deriving them.
  When this appendix is realized into `.tex`, update `requires:` to list the
  summarized distributions (bernoulli, binomial, poisson, geometric,
  discrete-uniform, uniform-continuous, gaussian, exponential, gamma, rayleigh,
  laplace, cauchy, gaussian-vector) plus `expectation` and `variance`.
