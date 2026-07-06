---
slug: 25-sums-and-many
title: Sums of Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03
source: sources/25-sums-and-many.tex
source_sha256: 720b9deaf084fab02fbf89e2487f4ad3594bbd53458a78dc1975eca3293c6b7b
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_vectors.tex
companion: sources/25-sums-and-many.md
companion_sha256: 24365e9d6b861b146df44bdc5fd758e3aedc15ae905f595e143aacdc613a4a68
prereqs:
  - 24-independence-rvs
audience: undergraduate engineering, first probability course
concepts:
  - id: convolution
    name: The PMF of a sum is a convolution
    importance: core
    one_liner: For independent integer X, Y - p_{X+Y}(k) = sum over m of p_X(m) p_Y(k-m) — the discrete convolution, read off the joint table's anti-diagonals.
  - id: ogf
    name: The ordinary generating function
    importance: core
    one_liner: G_X(z) = E[z^X] packs the whole PMF into one function; derivatives at zero recover probabilities, derivatives at one recover moments.
  - id: ogf-product
    name: Sums become products
    importance: highlight       # the chapter's slickest tool
    one_liner: For independent X, Y - G_{X+Y}(z) = G_X(z) G_Y(z); adding variables multiplies their generating functions.
  - id: poisson-merge
    name: Worked example — merging Poissons
    importance: core
    one_liner: Poisson(alpha) + Poisson(beta) has OGF e^{(alpha+beta)(z-1)} — Poisson with parameter alpha + beta, in two lines instead of a convolution.
  - id: many-variables
    name: Joint PMFs of n variables
    importance: core
    one_liner: p_{X_1..X_n}(x_1..x_n) = Pr of the intersection; under independence it is the product of the marginals — the vector form of everything so far.
  - id: empirical-sums
    name: Empirical sums S_n
    importance: core
    one_liner: S_n = X_1 + ... + X_n for iid draws — n-fold convolution, OGF G_X(z)^n; Bernoulli draws assemble into the binomial, closing a loop from video 16.
  - id: negative-binomial
    name: The negative binomial via OGFs
    importance: optional        # starred in the book; cut first
    one_liner: The waiting time for r successes has OGF (p / (1-(1-p)z))^r — a sum of r geometric-like waits, read off the generating function.
estimated_runtime_sec: 540      # ~9 min (five beats in project.yaml)
---

# Sums and Many Variables — Concept Map

This video covers Sections 7.6 and 7.7, closing book chapter 7. Everything
converges here: video 21's table, video 24's independence, and a new tool —
the generating function — that turns sums into products.

## What
For independent integer-valued variables, the PMF of a sum is the **discrete
convolution** of the summands' PMFs. The **ordinary generating function**
`G_X(z) = E[z^X]` packs a whole PMF into one function — and turns that
convolution into a product: `G_{X+Y} = G_X · G_Y`. The same ideas scale to
any number of variables: joint PMFs of vectors, products under
independence, and the **empirical sums** `S_n = X_1 + ... + X_n` of iid
draws, whose PMF is an n-fold convolution and whose OGF is `G_X(z)^n`.

## Why it matters
Sums of independent random variables are the central objects of the rest of
the course — sample means are sums. Convolution answers the distribution
question directly but gets heavy fast; the OGF product rule is the
transform trick (the probabilist's z-transform, as engineers will
recognize) that makes n-fold sums tractable in one line. Watching Bernoulli
draws assemble into the binomial closes a loop opened in video 16 — and
`G_X(z)^n` is the doorway to the limit theorems.

## Key ideas (in dependency order)
1. **Convolution.** `p_{X+Y}(k) = sum_m p_X(m) p_Y(k - m)` for independent
   X, Y: video 21's anti-diagonals, now with the joint factored so only
   marginals appear. Commutative, associative.
2. **The generating function.** `G_X(z) = E[z^X] = sum_k z^k p_X(k)` —
   video 19's E[g(X)] with `g(x) = z^x`. It *encodes* the PMF
   (`p_X(k) = G^{(k)}(0)/k!`) and its derivatives at one give moments
   (`E[X] = G'(1)`). Bernoulli: `1 - p + pz`. Binomial: `(1-p+pz)^n`.
   Poisson: `e^{λ(z-1)}` — with the moments falling out on cue.
3. **Sums become products.** `G_{X+Y}(z) = E[z^{X+Y}] = E[z^X z^Y] =
   G_X(z) G_Y(z)` — video 24's product rule for expectations doing the
   work in one line.
4. **Worked: merging Poissons.** `e^{α(z-1)} e^{β(z-1)} = e^{(α+β)(z-1)}`
   — the sum is Poisson(α + β), by uniqueness. Two lines against a page of
   convolution; also the mirror of video 22's splitting.
5. **Many variables.** `p_{X_1..X_n}(x_1..x_n) = Pr(∩ {X_k = x_k})`;
   independence makes it a product of marginals. The binomial-OGF hint from
   idea 2 becomes visible structure: `(1-p+pz)^n` is n Bernoulli factors.
6. **Empirical sums.** `S_n = S_{n-1} + X_n` gives the n-fold convolution
   recursively, and `G_{S_n}(z) = G_X(z)^n` in one line. Worked at the
   PMF level for Bernoulli: the convolution recursion *is* Pascal's rule,
   and induction assembles the binomial — closing video 16's loop.

## What else (connections, to seed callbacks in narration)
- The dice anti-diagonals of video 21 return as convolution's level sets.
- `E[z^X z^Y] = E[z^X] E[z^Y]` is exactly video 24's product rule — the
  proof is a callback, not new work.
- Poisson merging mirrors video 22's Poisson splitting (thin a stream /
  merge two streams).
- Pascal's rule appeared in video 4 (binomial theorem); here it re-emerges
  from a convolution.
- Bridge forward: with sums under control, the course turns to continuous
  random variables (book chapter 8) — and S_n returns for the limit
  theorems.

## Conceptual progression (drives the storyboard)
Dice table → anti-diagonal sums with the joint factored: convolution → "a
better way": the PMF packed into G_X(z) as a bar-chart-to-power-series
morph → the three named OGFs as cards → the one-line product rule →
Poissons merging → the vector form and iid products → S_n stacking up:
convolve, convolve, convolve vs raise G to the n → Bernoulli bars
assembling into the binomial silhouette.

## Visual opportunities
- **Convolution on the table**: the 6×6 dice table with one anti-diagonal
  lit; cells annotated `p_X(m) p_Y(k-m)`; sweep k from 2 to 12 while the
  sum PMF grows underneath.
- **Packing the PMF**: bars at k = 0, 1, 2, ... sliding into the
  coefficients of `1·z^0 + p_1 z^1 + p_2 z^2 + ...` — the PMF *becoming* a
  power series.
- **Sums become products**: `G_{X+Y} = G_X G_Y` in accent while two OGF
  cards physically multiply; the Poisson merge as exponents adding.
- **S_n assembling**: Bernoulli PMF (two bars) convolved with itself
  repeatedly — n = 1, 2, 3, 4 — bars morphing toward the binomial shape
  (reusing the video-16 chart look); beside it, `G_X(z)^n` just increments
  its exponent.

## Notation (per project.yaml)
- Convolution `(p_X * p_Y)(k) = \sum_{m} p_X(m)\, p_Y(k-m)`.
- OGF `G_X(z) = \mathrm{E}\left[z^X\right]`; expectations via the helper.
- Empirical sum `S_n = \sum_{k=1}^{n} X_k`.

## Deliberately out of scope
- The starred negative-binomial derivation (differential-equation route) —
  optional from the start; at most one card naming the result.
- Moment generating functions / characteristic functions — later chapters.
- Limit theorems — teased in the bridge only.

## Cut first (if the script runs over budget)
The negative binomial drops entirely; the moments-from-derivatives remark
in idea 2 compresses to one caption; the Pascal's-rule connection becomes
a spoken aside.
