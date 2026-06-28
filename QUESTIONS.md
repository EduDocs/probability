# Conceptual Audit — Questions and Suggested Improvements

> Generated audit of the chapter sidecars under `chapters/`. Findings,
> questions, and proposed improvements grounded in canonical probability
> references and empirically supported pedagogical principles. Companion
> document to `TODO.md` (structural progression findings, not duplicated here)
> and `CONCEPT_MAP.md` (the DAG this audit examines).

The audit reads the 13 in-scope chapter sidecars (`preface` through
`empirical_sums`) plus the two parked appendix sidecars (`appendix`,
`appendix_background`). It treats `TODO.md` as already known: the OGF/MGF
forward references, the orphaned "iid" concept, the indicator-function
orphan, the conditional-notation promise, and the unfinished `appendix.md`
are recorded there and are not re-litigated here.

The audit is conceptual: it reads the `.md` spines, not the `.tex` prose.
A couple of `.tex` peeks (`discrete_expectations.tex`,
`conditional_probability.tex`, `random_vectors.tex`) were used only to confirm
that the sidecar reflects what the prose actually does — the audit is of the
sidecar's design log, not the shipped chapter.

## Per-chapter findings

### `preface.md`

- Coverage: thin but appropriate. The spine declares audience (calculus,
  some programming), scope (introductory), course length (45 hours), and the
  role of computing. What is missing relative to canonical engineering-text
  prefaces (Bertsekas–Tsitsiklis, Stark–Woods, Gubner) is any statement of
  the book's *philosophy*: frequentist vs. Bayesian framing, the role of
  measure theory ("starred" only), and the intended use of examples. The
  reader is told the prerequisites but not the contract.
- Granularity / ordering: bullets are at roughly the right level. The
  "computing" theme is repeated across three bullets that could be one.
- Pedagogical observation: a one-line statement of *what a student will be
  able to do* after finishing — a learning-outcome sentence in the style of
  Bertsekas–Tsitsiklis's preface — would help instructors calibrate. The
  preface currently describes the artifact, not the transformation.
- Pedagogical observation: no mention of how the book treats
  *misconceptions*. The Konold "outcome approach" and Kahneman–Tversky
  representativeness work strongly suggest that engineering students arrive
  with stable wrong intuitions; the preface is the natural place to signal
  that the book will surface and refute them (whether it does or not is a
  separate question, see Pedagogical observations §misconceptions).

### `mathematical_review.md`

- Coverage: comprehensive for naive set theory. Good move to declare
  "rigorous axiomatic treatment is set aside" up front. The frontmatter
  introduces `indicator-function`, which (as TODO.md notes) is then orphaned
  downstream.
- Granularity / ordering: ordering is sound (sets → operations → algebra →
  products → functions → indicator → tie-back). Bullets read at the right
  level of grain.
- Coverage gap: the book is sold as engineering-oriented with calculus
  prerequisites, yet the math review chapter is purely set-theoretic. There
  is no calculus review of series convergence, geometric series, Taylor
  expansions, multivariable integration, or polar coordinates — all of
  which the later chapters use heavily. The new `appendix_background.md`
  partially fills this, but the spine of `mathematical_review.md` does not
  signal the split or point readers to the appendix.
- Pedagogical observation: the chapter sidesteps cardinality except in
  `basic_concepts.md`, where countability is then quietly invoked. The
  natural home for the countable/uncountable distinction is here (Ross
  Ch. 1 Appendix, Bertsekas–Tsitsiklis §1.1) as part of the set toolkit, not
  next to the axioms.
- Pedagogical observation: the closing tie-back is good — it satisfies the
  "advance organizer" pattern (Ausubel, 1968): readers know why they sat
  through set theory. Consider one bullet on *which* probability constructs
  each chunk supports (preimage → RV, partition → total probability,
  product → joint distributions).

### `combinatorics.md`

- Coverage: complete for the finite equally-likely model. Stirling is
  flagged starred (also in TODO.md).
- Sequencing: a defensible ordering. One small issue — the
  counting-principle bullet is general (Cartesian-product cardinality),
  then permutations, then Stirling, then k-permutations. Most canonical
  texts (Ross Ch. 1, Bertsekas–Tsitsiklis §1.6) defer Stirling until after
  all the basic counts are established, because it is an *asymptotic
  result* not a counting tool.
- Frontmatter mismatch (already in TODO.md / CONCEPT_MAP.md): chapter
  `requires: event`, but `event` is introduced in `basic_concepts`. The
  spine handles this by speaking of "events" intuitively while deferring
  the formal definition; the sidecar should make that pedagogical choice
  explicit rather than relying on the reader to fail gracefully.
- Coverage gap: classical worked problems that texts at this level use to
  build intuition — the birthday problem, the matching/derangement problem,
  the hat-check problem, hypergeometric / urn problems with replacement vs.
  without — are not on the spine at all. Birthday and derangement are in
  almost every undergraduate text (Ross §2.5; Pitman §1.5; Grimmett–Stirzaker
  §1.4) precisely because they elicit and refute the "outcome approach"
  misconception (Konold, 1989). Worth adding at minimum a "canonical examples"
  bullet that names the ones the chapter will work through.
- Pedagogical observation: variation theory (Marton, 2015) is highly
  relevant here. Permutation vs. combination is the single most over-confused
  pair in undergraduate probability. A "contrast" bullet on the spine —
  *one* worked problem framed both ways with explicit contrast — would
  pay for itself.

### `basic_concepts.md`

- Coverage: solid axiomatic spine. Sample space, events, axioms, finite /
  countably infinite / uncountably infinite models, sigma-field preview.
  Cardinality bullet is appropriately late.
- Sequencing: defensible. Most canonical texts (Bertsekas–Tsitsiklis §1.2,
  Ross Ch. 2) introduce the axioms first, then derive the consequences
  (monotonicity, union bound, inclusion–exclusion). The spine does this.
- Coverage gap: continuity of probability (the "limit of a monotone sequence
  of events" property — sometimes called continuity from below / above)
  is missing. Most engineering texts at least state it (Bertsekas–Tsitsiklis
  §1.2 Problem 14, Stark–Woods §1.4) because it is used implicitly in any
  derivation involving a countable sequence of events.
- Pedagogical observation: the chapter is the spine's first encounter with
  the abstract machinery. Cognitive Load Theory (Sweller, 1988; van
  Merriënboer–Sweller, 2005) flags this kind of chapter as high
  intrinsic load: many new abstractions interleaved with implications.
  The spine should either name a *running example* that threads through the
  chapter (Bertsekas–Tsitsiklis use Bernoulli trials and the dart on a square)
  or signal that worked examples accompany each abstract definition.
- Pedagogical observation: "probability law" is the book's name for what
  most texts call the *probability measure*. The spine could note this
  vocabulary choice and tie it back to functions on a sigma-field — a small
  but valuable pointer for students who consult other texts.

### `conditional_probability.md`

- Coverage: standard sequence — definition, multiplication rule, total
  probability, Bayes, independence (events), conditional independence. All
  necessary pieces are present.
- Sequencing: textbook-canonical and well organized. Independence comes
  after Bayes; this is the Bertsekas–Tsitsiklis order (§1.3, §1.5) and
  Pitman's order.
- Coverage gap: no spine bullet for the *Bayes-rule worked example* (the
  diagnostic test, the Monty Hall problem, the two-children problem).
  These are the canonical conditional-probability examples that
  Falk & Bar-Hillel (1983) identify as the loci of student misconception;
  every undergraduate text uses at least one. The spine does not commit to
  any.
- Coverage gap: the spine treats independence and conditional independence
  but does not flag the *Simpson's-paradox / confounding* counterexample
  that contrasts marginal vs. conditional independence. Bertsekas–Tsitsiklis
  §1.5 use exactly this contrast.
- Closing "notations" bullet is the orphaned promise already noted in TODO.md.
- Pedagogical observation: this chapter is *the* spiral-curriculum hinge
  (Bruner, 1960). Conditioning recurs at progressively higher abstraction
  later — conditional PMF, conditional expectation as a random variable,
  conditional density, conditional expectation as a projection. The
  current spine reads as a single-level treatment with no signal that the
  concept will return. A closing bullet pointing forward — "conditioning
  recurs in `discrete_vectors.md` (`E[X|Y]` as an RV), `random_vectors.md`
  (conditional density), and the tower property" — would set up the spiral.

### `discrete_random_variables.md`

- Coverage: defensible catalog. Bernoulli, binomial, Poisson, geometric,
  discrete uniform. Hypergeometric is missing — present in Ross §4.8.3,
  Pitman §3.6, Stark–Woods §2.5 — and it is the natural payoff for the
  partition / combination work done in `combinatorics.md`.
- Sequencing: sound. Bernoulli first as the atom, then binomial as the sum,
  then Poisson via rare-events scaling, then geometric, then discrete uniform.
- Coverage gap: negative binomial / Pascal distribution is missing. It is
  the natural sibling of the geometric (sum-of-geometrics framing) and is
  on the spine in Ross §4.8.2 and Pitman §3.4. The spine could mention it
  in passing as "negative binomial extends the geometric to k successes".
- Coverage gap: the connection between Bernoulli and the *indicator function*
  introduced in `mathematical_review.md` is not made (the orphan flagged in
  TODO.md). This is not just a tie-back; it is the *one place* where the
  abstract set machinery from Ch. 1 visibly turns into probability machinery.
- Coverage gap: the chapter lists distributions but does not introduce
  *moments / variance / mean* until `discrete_expectations.md`. Most texts
  (Bertsekas–Tsitsiklis §2.4, Pitman §3) state the mean and variance of each
  named distribution at the point of introduction so the catalog is
  self-contained. The current spine punts on that, which means the catalog
  is incomplete information for any student who flips back to look up
  "what's the variance of a Poisson?". Worth a decision either way.
- Pedagogical observation: variation theory again. PMF axioms parallel the
  probability-law axioms one chapter earlier; an explicit bullet flagging
  "PMF satisfies axioms analogous to a probability law on the integers" would
  make the structural parallel obvious instead of latent.
- Frontmatter `requires: iid` — `iid` is undefined upstream (TODO.md). Spine
  uses "iid Bernoulli trials" without ever defining the term.

### `discrete_expectations.md`

- Coverage: standard. Expectation, LOTUS, mean, variance, moments, OGF.
- Sequencing: reasonable; LOTUS appears very early (second bullet), before
  the spine has established what other expectations one might want. Most
  texts (Pitman §3, Bertsekas–Tsitsiklis §2.4) introduce the mean as the
  motivating example, then variance, *then* generalize to LOTUS. The
  current spine inverts that.
- Coverage gap: *linearity of expectation* is introduced one chapter later
  in `discrete_vectors.md`, which is the natural home for the multi-variable
  statement, but the single-variable form `E[aX + b] = aE[X] + b` *is* in
  this chapter (the "affine functions" bullet). The spine treats this as a
  consequence rather than naming it linearity. Worth tightening: name the
  property here and reuse it in `discrete_vectors.md`.
- Coverage gap: no spine bullet for *conditional expectation given an event*
  in the single-RV setting. The full `E[X|Y]` machinery lives in
  `discrete_vectors.md`, but `E[X | A]` for an event `A` is a one-line
  extension of the expectation definition and is a common worked example
  (Bertsekas–Tsitsiklis §2.4, total-expectation theorem).
- Coverage gap: no spine mention of the variance computation shortcut
  `Var(X) = E[X^2] - (E[X])^2`. This is on every comparable text's spine
  and is the most-used identity in homework problems.
- OGF forward-reference (independence-of-RVs / convolution) already in
  TODO.md.
- Pedagogical observation: this chapter is a strong candidate for the
  *worked-example effect* (Sweller & Cooper, 1985; Renkl, 2014): expectation
  of a Bernoulli, binomial, geometric, Poisson. The spine has no bullet
  committing to those four canonical computations; whether the prose
  delivers them is then invisible from the design layer.

### `discrete_vectors.md`

- Coverage: joint PMF, marginals, conditional PMF, conditional expectation,
  tower, linearity, independence, OGFs, convolution. Strong coverage.
- Sequencing: defensible. Conditional expectation is introduced before
  independence — this is the Bertsekas–Tsitsiklis ordering (§2.5–2.7).
  Pitman and Ross go independence-first.
- Coverage gap: *covariance and correlation* are missing from the spine. In
  every comparable text (Ross §7.4, Bertsekas–Tsitsiklis §4.2, Pitman §6.4,
  Grimmett–Stirzaker §3.3) covariance is introduced immediately after joint
  PMF / marginal / independence, because (a) `Var(X+Y) = Var(X) + Var(Y) +
  2 Cov(X,Y)` is the only honest way to talk about variance of sums, and
  (b) correlation is the first multivariate descriptor that students need.
  Their absence here propagates downstream: `random_vectors.md` and
  `empirical_sums.md` both rely on `Var(X_1 + ... + X_n)` arguments that
  silently require independence to drop the covariance.
- Coverage gap: *law of total variance* (`Var(X) = E[Var(X|Y)] + Var(E[X|Y])`)
  is missing. The tower property is on the spine, but its variance analog
  — heavily used in engineering (signal-plus-noise decomposition,
  bias-variance) — is absent.
- Coverage gap: the spine introduces `E[X|Y]` as an RV and states the tower
  property, but does not flag the *smoother / projection* interpretation
  (Bertsekas–Tsitsiklis §4.6, Grimmett–Stirzaker §3.7). That framing is
  what makes the construct useful in any later inference course; even a
  one-line bullet would set the stage.
- Pedagogical observation: this chapter introduces an unusually high number
  of new constructs for one week of a 45-hour course (eight on the spine,
  plus the missing covariance / total variance / smoother bullets above).
  Cognitive Load Theory (Sweller, 1988) flags this as germane-overload
  territory. A natural split: §A joint distributions + marginals +
  independence; §B conditional PMF / expectation / tower / total variance;
  §C linearity / covariance / sums-of-RVs / convolution / OGF. The spine
  could signal this internal grouping even if the chapter ships as one.

### `continuous_random_variables.md`

- Coverage: CDF, PDF, expectation, uniform, Gaussian, exponential, plus
  Gamma, Rayleigh, Laplace, Cauchy. The auxiliary catalog (Gamma, Rayleigh,
  Laplace, Cauchy) is broader than many engineering texts at this point in
  the curriculum.
- Sequencing: CDF first, then PDF as derivative. This is the engineering
  ordering (Stark–Woods §3.2, Gubner §4.1) and supports the discrete-revisit
  bullet that follows. Bertsekas–Tsitsiklis and Pitman go PDF-first and
  define CDF as the integral; either is defensible, but the CDF-first
  ordering pairs better with this book's later treatment of derived
  distributions.
- Coverage gap: no spine bullet for the *one fundamental warning* about
  continuous RVs — that `Pr(X = x) = 0`, and that the PDF is not a
  probability. The "f_X is not itself a probability" half-sentence in the
  PDF bullet is the only mention; this is the canonical misconception
  (Konold; Garfield & Ben-Zvi, 2007) and warrants its own bullet.
- Coverage gap: tail-probability / survival-function `Pr(X > x)` framing
  — used implicitly in Markov / Chebyshev / Chernoff later — is not on
  the spine here. A one-line bullet would set up the bounds chapter.
- Gamma / Rayleigh forward-reference already in TODO.md. Cauchy bullet's
  "mean undefined" is exactly the kind of misconception-naming bullet the
  rest of the spine could use more of (good as-is).
- Pedagogical observation: discrete-revisit bullet is excellent variation-
  theory practice (Marton, 2015): contrast PMF vs. PDF via the CDF as the
  unifying object. Worth strengthening into an explicit "what's the same /
  what's different" pair of sub-bullets.
- Pedagogical observation: at this point in the course the student has met
  most of the standard distributions. A bullet on *which distribution
  models what* (Bernoulli/binomial = counts; Poisson = rare events; Gaussian
  = sums; exponential = waiting times) — a *table of correspondences* —
  would do real cognitive-load work (intrinsic-load reduction via schema
  formation; van Merriënboer–Sweller, 2005).

### `derived_distributions.md`

- Coverage: monotone case, non-monotone case (partition into monotone
  pieces), inverse-CDF method. Compact, clean spine.
- Sequencing: textbook-standard.
- Coverage gap: the spine treats only `g: R -> R`. The *bivariate* change
  of variables (`g: R^2 -> R^2`, with the Jacobian determinant) is deferred
  to `random_vectors.md` — defensible, but worth noting on the spine so a
  reader doesn't expect it here. The frontmatter introduces `jacobian`
  here, which is fine for the univariate `|dg^{-1}/dy|` factor, but the
  full *matrix* Jacobian is then a forward reference.
- Coverage gap: *order statistics* (CDF and PDF of `max`, `min`, the
  k-th order statistic) is missing. This is in every comparable text
  (Ross §6.6, Pitman §4.6, Bertsekas–Tsitsiklis §3.6 exercises,
  Stark–Woods §6.4) and is one of the only places where the change-of-
  variables / derived-distribution machinery does real engineering work
  (reliability, parallel systems, ML on `max`).
- Coverage gap: no bullet on the canonical worked examples — `Y = X^2`
  for `X ~ N(0,1)` (chi-square), `Y = aX + b` linear, `Y = e^X` (lognormal).
  Worked examples are exactly where the change-of-variables formula
  becomes operative for students; the spine should at least name the
  canonical set.
- Pedagogical observation: the chapter is short on the spine but does heavy
  conceptual lifting (derived distributions are reportedly one of the harder
  topics in engineering probability — Stark–Woods devote a full chapter).
  Sweller & Cooper (1985) — worked-example effect — predict that this is
  the chapter where the *number* and *quality* of worked examples matters
  most. The spine does not commit to any.

### `expectations_and_bounds.md`

- Coverage: MGF, Markov, Chebyshev, Chernoff, Jensen. Standard set.
- Sequencing: MGF first, then the three classical inequalities, then
  Jensen. Defensible; matches Grimmett–Stirzaker §5.7. Some texts
  (Bertsekas–Tsitsiklis §5.1–5.2) lead with Markov/Chebyshev *before*
  the MGF, motivating concentration first and then sharpening it with the
  MGF / Chernoff. Either is fine; the spine should note the choice.
- Coverage gap: *characteristic function* (`E[e^{itX}]`) is not on the
  spine. The MGF does not exist for the Cauchy (introduced one chapter
  earlier!) or for any heavy-tailed RV; the characteristic function does.
  Grimmett–Stirzaker §5.7 and Pitman §4.4 both make this contrast. At
  the undergrad-engineering level the characteristic function can be a
  starred bullet, but its absence — given that Cauchy is already on the
  spine — leaves a real inconsistency.
- Coverage gap: *Cauchy–Schwarz / Hölder inequalities* are missing. These
  are the natural companions of Jensen — together they cover the
  inequality toolkit used in any later probability/statistics course
  (Ross §8.2, Grimmett–Stirzaker §5.7). At minimum Cauchy–Schwarz
  warrants a starred bullet.
- Coverage gap: no bullet stating *when each inequality should be reached
  for*. Markov needs only `E[X]`; Chebyshev needs variance; Chernoff needs
  the MGF. This is the kind of "schema for tool selection" bullet that
  variation theory (Marton, 2015) and worked-example research (Renkl, 2014)
  identify as high-leverage.
- MGF forward-reference (independence of *continuous* RVs) already in
  TODO.md.
- Pedagogical observation: the chapter sits at a curricular hinge — the
  payoff is the LLN/CLT in `empirical_sums.md`. The spine could close with
  a one-line forward bullet ("Chebyshev → weak LLN, MGF/CLT → CLT proof
  sketch") to signal the spiral.

### `random_vectors.md`

- Coverage: joint CDF, joint PDF, conditional PDF, conditional expectation,
  derived distributions, independence, convolution. Strong coverage.
- Sequencing: textbook-canonical.
- Coverage gap: *multivariate Gaussian* is not on the spine. This is the
  single most important continuous joint distribution and is in every
  comparable text at this point (Ross §6.5, Bertsekas–Tsitsiklis §4.7,
  Stark–Woods §6.2, Pitman §5.3). It is the natural payoff of the joint-PDF
  + linear-algebra + independence machinery this chapter assembles. Its
  absence is the single biggest coverage gap in the book.
- Coverage gap: *covariance matrix* (and, jointly, correlation matrix /
  correlation coefficient) is not on the spine — see the parallel gap in
  `discrete_vectors.md`. For an engineering-oriented book this is the
  workhorse multivariate descriptor.
- Coverage gap: no joint-distribution unifying bullet across `discrete_vectors`
  and `random_vectors` (already noted in TODO.md as a "joint distribution"
  bridging bullet). Worth restating from the pedagogy angle:
  spiral-curriculum (Bruner, 1960) and Marton's variation theory both flag
  this kind of unifying retrospective as high-leverage when the same
  construct is met in two registers.
- Pedagogical observation: this is a high-load chapter (six new spine
  bullets, each of which is a continuous analog of a discrete construct).
  The spine does not lean on the parallel — e.g., "everything in
  `discrete_vectors.md` carries over with sums → integrals, PMF → PDF."
  Stating that parallel explicitly is exactly the kind of "advance
  organizer" Ausubel (1968) and Mayer (2001) flag as reducing extraneous
  load.
- Coverage gap: *bivariate normal* — even as a starred standalone bullet
  with the standard density formula and the correlation parameter — is
  worth flagging. Engineering applications (estimation, regression,
  Kalman filtering) lean on it heavily.

### `empirical_sums.md`

- Coverage: convergence modes, LLN, CLT, heavy-tailed cautionary case.
  Clean spine.
- Sequencing: standard. Define convergence vocabulary, then LLN, then CLT.
- Coverage gap: *almost-sure convergence* is missing. The spine names
  in-probability, in-mean-square, in-distribution; almost-sure is the
  fourth standard mode (Grimmett–Stirzaker §7.2, Ross §8.4, Pitman §5.4).
  At an undergraduate level it can be starred — the strong LLN is the
  payoff — but its omission is unusual.
- Coverage gap: no distinction between *weak* and *strong* LLN, and no
  mention of *Slutsky's theorem* or the *continuous mapping theorem* —
  both used implicitly whenever one says "the sample variance also
  converges." These can be starred, but the spine currently elides them
  entirely.
- Coverage gap: no bullet on the *normal approximation to the binomial*
  (de Moivre–Laplace), which is the historical and pedagogical bridge
  between the discrete catalog (Ch. 6) and the CLT. Every comparable
  text (Ross §8.3, Pitman §3.5, Bertsekas–Tsitsiklis §5.4) uses it.
- Coverage gap: *confidence intervals* / *normal approximation in practice*
  (computing `z`-style intervals) — the everyday engineering payoff of the
  CLT — is not on the spine. Stark–Woods and Gubner both treat this as the
  motivating example for the CLT.
- Pedagogical observation: this chapter is the spine's first encounter with
  *limits of random objects*. Cognitive Load Theory (Sweller; van
  Merriënboer–Sweller 2005) and the "contrastive examples" tradition
  (Marton, 2015) both predict that students confuse the four convergence
  modes without explicit contrast. The spine has one bullet on
  "implications between them" — that bullet should commit to *which*
  contrastive counterexamples the chapter will use (the canonical pair:
  `1/n` constant for in-probability-but-not-in-mean-square; "moving bump"
  for in-distribution-but-not-in-probability).
- Pedagogical observation: heavy-tailed cautionary bullet is excellent —
  it explicitly names a misconception ("LLN-style intuition breaks"). This
  is the model the rest of the book should follow.

### `appendix.md` (parked)

- Already in TODO.md: title is "Sums," opens with an orphaned `E[Y]` display,
  only `sum k` has a proof, `sum k^2` / `sum k^3` are bare. `appendix_background.md`
  supersedes it.
- No fresh finding beyond what TODO.md and `appendix_background.md`'s
  Decisions section say.

### `appendix_background.md` (parked)

- Coverage: comprehensive reference appendix — series and sums, useful
  integrals, multivariable calculus, limits and asymptotics, counting
  identities. Frontmatter introduces 20 concepts; spine is well-grouped.
- Sequencing: lookup-oriented (decided explicitly), not pedagogical. Good
  call. Series → integrals → multivariable → limits → counting matches
  the order in which main chapters call back to each.
- Pedagogical observation: the Bishop / ESL "reference appendix" pattern is
  well-chosen and is one of the strongest design decisions in the project.
  The Decisions block already documents this; no change needed.
- Open question (the sidecar's own): linear-algebra primer for
  `random_vectors.md`. Answered indirectly above — multivariate Gaussian
  + covariance-matrix coverage in `random_vectors.md` will need at least
  inner-product and norm; adding a one-page linear-algebra section here
  is cheap and forward-compatible.
- Frontmatter scope: 20 concepts is a lot to introduce; consider whether
  some (`l-hopital`, `squeeze-theorem`, `monotone-convergence-of-sequences`)
  are actually called back to from any main chapter, or whether they are
  speculative inclusions. The sidecar's own open question raises this; the
  audit's recommendation is "include only what's actually cited."
- Relationship to `mathematical_review.md` (the sidecar's own open
  question): the current split — motivating front-matter vs. reference
  manual — is correct, but it is invisible from `mathematical_review.md`,
  which has no closing bullet pointing readers at the reference. Worth a
  one-line tie-in on `mathematical_review.md`.

## DAG vs. best-practice probability curricula

The book's reading order is:

> preface → mathematical_review → combinatorics → basic_concepts →
> conditional_probability → discrete_random_variables → discrete_expectations
> → discrete_vectors → continuous_random_variables → derived_distributions →
> expectations_and_bounds → random_vectors → empirical_sums

### Overall ordering vs. canonical references

This ordering is the *engineering-probability standard*. It matches:

- **Stark & Woods** (Ch. 1 set theory → Ch. 2 probability spaces → Ch. 3
  conditional → Ch. 4 RVs → Ch. 5–6 multivariate → Ch. 7 limit theorems).
- **Gubner** (math review → counting → probability axioms → conditional →
  discrete RVs → discrete pairs → continuous → continuous pairs → limit
  theorems).
- **Miller & Childers**, similar.

It diverges from:

- **Bertsekas & Tsitsiklis** (MIT 6.041): no separate combinatorics chapter
  (counting folded into examples in §1.6); discrete *and continuous* RVs
  treated in the same chapter pair (Ch. 2 discrete, Ch. 3 continuous, then
  Ch. 4 joint covering *both* together). The 6.041 syllabus deliberately
  *delays* combinatorics until the student has seen the axioms, partly
  because counting-for-its-own-sake is the easiest place to lose engineering
  students. Worth examining: in this book, combinatorics precedes axioms,
  and the `combinatorics.md` sidecar uses "events" intuitively before they
  are formalized (forward reference in CONCEPT_MAP.md). The fix is small
  (a half-line caveat in `combinatorics.md`) but the structural choice is
  worth re-examining.
- **Ross** (*A First Course in Probability*): same broad order, but Ross
  introduces *axioms before counting* (Ch. 1 combinatorics is brief; Ch. 2
  is axioms).
- **Pitman** (*Probability*): starts with axioms and Bayes (Ch. 1), then
  weaves combinatorics into the binomial chapter (Ch. 2). Counting is
  treated as a *tool for distributions* rather than a standalone topic.
- **Grimmett & Stirzaker**: axioms-first (Ch. 1), counting in §1.4, discrete
  and continuous treated separately (Ch. 2, Ch. 3, Ch. 4) with joint
  in Ch. 3, generating functions in Ch. 5, limit theorems in Ch. 7.

The book's discrete-then-continuous split (the "engineering ordering") is
defensible for a single-semester course but has a known pedagogical cost:
students develop two mental compartments and struggle when the convergence
theorems treat both at once. The CDF-revisit bullet in
`continuous_random_variables.md` mitigates this, but the spine could
do more.

### Coverage of standard topics

The audit's standard checklist:

| Topic | Status | Notes |
|---|---|---|
| Set theory preliminaries | Present (`mathematical_review`) | Solid |
| Counting / combinatorics | Present (`combinatorics`) | Missing birthday/derangement/hypergeometric framing |
| Axioms, sample space, events | Present (`basic_concepts`) | Continuity-of-probability missing |
| Inclusion–exclusion, union bound | Present | Good |
| Conditional probability, total probability, Bayes | Present | No canonical Bayes example named on spine |
| Independence (events) | Present | Good |
| Discrete distributions catalog | Present | Hypergeometric, negative binomial missing |
| Discrete expectation, LOTUS, variance, moments | Present | `Var = E[X^2] - (EX)^2` shortcut not named |
| OGFs | Present | Forward-ref issue (TODO.md) |
| Joint PMF, marginals, conditional PMF | Present | Good |
| Conditional expectation, tower property | Present | Smoother / projection interpretation missing |
| Linearity of expectation | Present | Could be named in discrete_expectations too |
| Independence of RVs (discrete) | Present | Good |
| Convolution | Present | Good |
| **Covariance / correlation** | **Missing** | Major gap; see discrete_vectors / random_vectors |
| **Law of total variance** | **Missing** | High-utility identity, standard at this level |
| **Conditional expectation as smoother / projection** | **Missing** | Pedagogically valuable, low cost |
| CDF, PDF, continuous distributions | Present | Cauchy-but-no-CF inconsistency |
| Change of variables (univariate) | Present | Good |
| **Order statistics** | **Missing** | Standard; natural payoff of CoV machinery |
| MGF | Present | Cauchy/non-existence not flagged |
| **Characteristic function** | **Missing** (or starred) | Needed once Cauchy is on the spine |
| Markov, Chebyshev, Chernoff, Jensen | Present | Good |
| **Cauchy–Schwarz** | **Missing** | Standard companion to Jensen |
| Joint CDF, joint PDF, conditional PDF | Present | Good |
| **Multivariate Gaussian** | **Missing** | **Biggest single coverage gap** |
| **Covariance matrix** | **Missing** | Companion to multivariate Gaussian |
| Change of variables (multivariate, Jacobian) | Present | Good |
| Convergence modes, LLN, CLT | Present | Almost-sure missing; weak/strong LLN not distinguished |
| **Normal approximation to binomial (de Moivre–Laplace)** | **Missing** | Standard CLT preview |
| **Confidence-interval / normal-table practice** | **Missing** | Standard engineering payoff |

Topics correctly *omitted* at undergraduate level (no action needed,
flagged for explicitness):

- Borel–Cantelli lemmas (rare at undergrad outside Grimmett–Stirzaker).
- Exchangeability (de Finetti) (rare outside Bayesian curricula).
- Markov chains, random walks (typically a separate course; the book is
  explicit about being a single semester).
- Measure-theoretic foundations (sigma-field preview is appropriately
  starred in `basic_concepts.md`).

### Pacing

The discrete-vs-continuous split is roughly balanced by sidecar count
(`discrete_random_variables`, `discrete_expectations`, `discrete_vectors`
vs. `continuous_random_variables`, `derived_distributions`,
`expectations_and_bounds`, `random_vectors`). By LaTeX line count
(`wc -l` on the `.tex` files), the continuous side is slightly heavier
(2677 lines vs. 2131 for the parallel discrete chapters). This matches the
Stark–Woods / Gubner pacing for an engineering audience and is appropriate
for the preface's stated 45-hour budget.

The limit theorems (`empirical_sums.md`) get a single chapter — 433 lines
of LaTeX — which is on the lighter end for engineering texts. Bertsekas
& Tsitsiklis give limit theorems a chapter with substantially more
worked examples and a chapter on statistical inference; Stark–Woods spread
limit theorems across two chapters. For a single-semester course this is
defensible, but the spine could acknowledge that *what is covered* is
deliberately a preview rather than a complete treatment.

## Pedagogical observations

### Cognitive Load Theory (Sweller, 1988; van Merriënboer & Sweller, 2005)

High-load chapters on the current spine:

- **`basic_concepts.md`** — five abstract constructs (sample space, event,
  probability law, sigma-field, the three axioms) plus four derived
  properties plus three sample-space cases plus the cardinality detour.
  This is a textbook-typical introduction but the spine does not signal a
  running example to anchor the load. Bertsekas–Tsitsiklis use Bernoulli
  trials and the dart-on-a-square throughout the chapter — the spine could
  commit to one explicitly.
- **`discrete_vectors.md`** — eight new spine concepts, several of which
  (conditional expectation as RV, tower property, OGF multiplicativity)
  are *meta-constructs* about earlier objects. This is the highest-load
  chapter in the book. The spine could split into "joint distributions,"
  "conditional machinery," and "sums and generating functions" subsections.
- **`random_vectors.md`** — six new spine concepts, all of which are
  *continuous analogs* of `discrete_vectors.md` constructs. CLT
  recommendation: lean explicitly on the discrete-analog parallel as an
  "advance organizer" (Ausubel, 1968) to reduce extraneous load. Currently
  the spine treats them as fresh introductions.

### Worked-example effect (Sweller & Cooper, 1985; Renkl, 2014)

The worked-example effect predicts that, for novices, *seeing a
fully-worked example reduces cognitive load and improves transfer relative
to "solve a problem" alone.* Chapters whose spines do not commit to
canonical worked examples — and thereby make it invisible whether the
prose delivers them — include:

- `combinatorics.md` (birthday, derangement, hypergeometric not named).
- `conditional_probability.md` (Bayes diagnostic-test, Monty Hall, two-
  children not named).
- `discrete_expectations.md` (Bernoulli/binomial/geometric/Poisson means
  not named).
- `derived_distributions.md` (chi-square, lognormal, linear transformation
  not named).
- `empirical_sums.md` (binomial-to-normal worked example not named).

Recommendation: a "Canonical worked examples" bullet on each of these
sidecars. This is a sidecar-level change, not a prose change — the goal
is design-log honesty.

### Variation theory / contrastive examples (Marton, 2015)

The book introduces several pairs of constructs that students are
documented to confuse. Where the spine names the contrast explicitly:

- `discrete_random_variables.md`: Bernoulli ⟶ binomial as sum — implicit
  ("number of successes in n iid Bernoulli trials"), could be stronger.
- `continuous_random_variables.md`: discrete vs. continuous via CDF —
  good, the spine names the contrast.
- `empirical_sums.md`: implications between convergence modes — good,
  needs counter-examples named.

Where the spine *does not* name the contrast and probably should:

- Permutation vs. combination (`combinatorics.md`).
- Independence of events vs. independence of RVs (across
  `conditional_probability.md` and `discrete_vectors.md`).
- PMF vs. PDF (`continuous_random_variables.md`).
- Events vs. random variables (`discrete_random_variables.md`, the
  preimage bullet partially does this).
- LLN vs. CLT (`empirical_sums.md` — one bullet each, no contrast bullet).
- Marginal vs. conditional independence (`conditional_probability.md` —
  acknowledged in the spine but no canonical contrast example named).

### Spaced practice and interleaving (Brown, Roediger & McDaniel, 2014; Rohrer & Pashler, 2010)

The book's structure *does* naturally revisit core concepts:

- Conditioning: events (Ch. 4) → discrete RVs (Ch. 7) → continuous RVs
  (Ch. 11). This is excellent spiral structure (Bruner, 1960).
- Independence: events → discrete RVs → continuous RVs.
- Expectation: discrete (Ch. 6) → continuous (Ch. 8) → bounds (Ch. 10) →
  limits (Ch. 12). Excellent.

Where the structure does *not* naturally revisit:

- Combinatorics is used heavily in `discrete_random_variables.md` (binomial,
  hypergeometric, multinomial) but no spine bullet ties the counting back
  to the catalog of distributions. The connection is left implicit.
- The indicator function (orphan in TODO.md) is the canonical example of
  a missed interleaving opportunity — it sits in Ch. 1 and could profitably
  be revisited at Bernoulli (Ch. 6), at expectation of an indicator (Ch. 7,
  `E[1_A] = Pr(A)` is the bridge identity), at total expectation, and at
  Markov's inequality.

### Concrete-to-abstract / motivating examples first

The `.tex` peek (preface, conditional_probability) shows that the prose
*does* lead with examples before abstractions. The sidecars often do not
make this visible: `conditional_probability.tex` opens with the die-roll
example and the frequentist motivation *before* the formal definition;
the sidecar lists only the formal sequence. This is a design-log honesty
issue, not a pedagogy failure.

Recommendation: a brief "motivating example" sub-bullet on each
introduces-a-new-construct sidecar so the spine reflects the prose's
actual concrete-to-abstract structure.

### Misconceptions in probability

Documented student misconceptions (Konold, 1989; Kahneman & Tversky;
Falk & Bar-Hillel, 1983; Garfield & Ben-Zvi, 2007):

| Misconception | Where it should be addressed | Spine status |
|---|---|---|
| Outcome approach (every outcome is equally likely) | `combinatorics`, `basic_concepts` | Not named |
| Gambler's fallacy / representativeness | `conditional_probability` / `discrete_random_variables` | Not named |
| Confusing `Pr(A|B)` with `Pr(B|A)` | `conditional_probability` | Not named (Bayes bullet does the math, not the contrast) |
| Conjunction fallacy | `basic_concepts` | Not named |
| `Pr(X = x) = 0` for continuous X means X cannot equal x | `continuous_random_variables` | Partially named ("f_X is not itself a probability") |
| Mean = "most likely value" | `discrete_expectations` | Not named |
| LLN means the next coin must be heads to "balance out" | `empirical_sums` | Not named |

Only the heavy-tailed cautionary bullet in `empirical_sums.md` explicitly
names a misconception. The Cauchy-mean-undefined bullet does too, weakly.
For an engineering audience trained to trust formulas, *explicitly naming
the misconception the formula is the cure for* is a high-leverage
pedagogical move — Garfield & Ben-Zvi's stats-ed research is consistent
on this point. Sidecar-level change: add a "common misconception" bullet
where each relevant chapter is the natural home.

### Spiral curriculum (Bruner, 1960)

Strong spiral structure in this book: conditioning, expectation, and
independence each recur at increasing sophistication. The spine *as it
stands* does not signal the spiral — each chapter introduces the next
level of the same concept as if fresh. Two-line forward bullets at the
end of each introducing chapter ("conditioning recurs in
`discrete_vectors`, `random_vectors`, and the tower property") would
make the spiral visible to readers reviewing the sidecar.

### Prior knowledge / preliminaries (Bishop, PRML; Hastie-Tibshirani-Friedman, ESL)

The Bishop / ESL pattern is: short motivating preliminaries up front
(notation, key facts), reference appendices for the heavy calculus. The
new `appendix_background.md` correctly adopts this split (the sidecar's
own Decisions block names it). What is missing is the *forward pointer*
from `mathematical_review.md` to the reference appendix; without it the
reader does not know the appendix exists until a chapter cites it.

## Open questions for the author

### On scope and coverage

1. Is the omission of covariance / correlation a deliberate scope choice,
   or an oversight? In an engineering book, this is the single most
   surprising absence — sums of non-independent RVs cannot be discussed
   honestly without it.
2. Is the multivariate Gaussian deliberately deferred (perhaps to a
   follow-up "Undergraduate Probability II" / random processes course)?
   If yes, the sidecar should state that scope boundary. If no, this is
   the second most surprising absence.
3. Should the Cauchy distribution remain in `continuous_random_variables.md`
   given that the bounds chapter has no characteristic function and
   therefore no analytical tool for it? Either drop Cauchy or add a
   starred characteristic-function bullet.
4. Does the book promise to *name* student misconceptions (heavy-tailed,
   Cauchy-mean-undefined are the only two examples currently), or only
   to *refute them by formal treatment*? The preface is the right place
   to declare the contract.

### On structure and sequencing

5. Why does combinatorics precede the axioms (against Ross, Bertsekas–
   Tsitsiklis, Pitman, Grimmett–Stirzaker)? The current order works but
   requires `combinatorics.md` to use "event" informally — what is the
   pedagogical argument for this choice?
6. Should `discrete_vectors.md` split into two chapters (or two explicitly-
   signposted halves)? Eight spine concepts plus the missing covariance /
   total-variance / smoother bullets put it well over typical
   cognitive-load budgets for a one-week unit.
7. The MGF appears before the bounds, the OGF appears at the end of
   `discrete_expectations.md`, and the characteristic function does not
   appear. Is this asymmetry intentional, or an artifact of the discrete-
   first organization?

### On audience and motivation

8. Will the chapters' worked examples be canonical (birthday, Monty Hall,
   diagnostic test, dart on a square, queue / waiting time) or
   engineering-specific (signal-plus-noise, channel capacity preview,
   reliability)? The preface signals engineering; the sidecars are
   silent on which examples will land.
9. Is the 45-hour budget consistent with the spine as written? Counting
   the new bullets implied by the suggestions below would not exceed
   typical pacing, but the *existing* spine is already dense for one
   semester.

### On the spine and the design log

10. Should each sidecar's spine commit to its canonical worked examples
    (as a "Canonical examples" sub-bullet), or are examples treated as
    purely a prose-layer concern? The current sidecar template does not
    distinguish — a project-level decision is worth making.
11. Are forward-pointer bullets (the spiral) part of the sidecar's
    register, or are they noise? If the answer is "part," several
    chapters need them; if "noise," the audit's spiral suggestions
    fall away.

### On the appendices

12. Should `appendix.md` ("Sums") be retired in favor of
    `appendix_background.md`'s *Series and sums* section, as
    `appendix_background.md` already proposes in its Decisions block?
13. Should the appendix grow a short linear-algebra primer to support
    multivariate Gaussian / covariance-matrix coverage in
    `random_vectors.md`?

## Suggested improvements (ranked by importance)

Each item gives: the change, the sidecars it touches, *why* (citing a
principle or canonical reference), and the cost / risk.

### 1. Add covariance, correlation, and law of total variance to the spine

- **What:** add covariance and correlation coefficient bullets to
  `discrete_vectors.md` (immediately after independence-of-RVs); add the
  law of total variance bullet after the tower property; restate both in
  continuous form in `random_vectors.md`.
- **Why:** every comparable engineering text (Ross §7.4,
  Bertsekas–Tsitsiklis §4.2, Stark–Woods §5.3, Pitman §6.4) treats
  covariance as a core construct, not an extension. Without it,
  `Var(X_1 + ... + X_n)` arguments in `empirical_sums.md` silently rely
  on independence. The law of total variance is the variance analog of
  the tower property and is heavily used in engineering decomposition
  arguments.
- **Cost / risk:** moderate spine growth in `discrete_vectors.md` and
  `random_vectors.md` (already high-load chapters). Mitigate by lifting
  the linearity-of-expectation bullet upstream to `discrete_expectations.md`.
- **Impact:** highest — closes the largest single curricular gap.

### 2. Add the multivariate (and bivariate) Gaussian to `random_vectors.md`

- **What:** spine bullet on the bivariate Gaussian (density formula,
  correlation parameter, marginal and conditional are still Gaussian);
  optional starred bullet on the multivariate Gaussian via the
  covariance matrix.
- **Why:** the canonical joint continuous distribution; appears in every
  reference (Ross §6.5, Bertsekas–Tsitsiklis §4.7, Stark–Woods §6.2,
  Pitman §5.3). Engineering applications (regression, Kalman filter,
  any inference course) start here. Its absence is the second largest
  curricular gap.
- **Cost / risk:** requires at minimum a covariance bullet earlier
  (item 1) and an inner-product/norm note in `appendix_background.md`.
  The bivariate case alone (without matrix notation) is cheap.
- **Impact:** very high; pairs with item 1.

### 3. Add canonical worked-example sub-bullets across the spine

- **What:** add a one-line "Canonical worked examples" sub-bullet to
  each chapter that introduces a major technique: `combinatorics.md`
  (birthday, derangement, hypergeometric framing), `conditional_probability.md`
  (Bayes diagnostic, Monty Hall, two-children), `discrete_expectations.md`
  (Bernoulli / binomial / geometric / Poisson means and variances),
  `derived_distributions.md` (linear, square, log), `empirical_sums.md`
  (de Moivre–Laplace).
- **Why:** worked-example effect (Sweller & Cooper, 1985; Renkl, 2014).
  Currently invisible from the design layer whether the prose delivers
  these. Sidecar honesty: if the chapter does deliver them, name them;
  if it doesn't, the audit has surfaced a gap.
- **Cost / risk:** zero — these are design-log clarifications.
- **Impact:** high; makes pedagogical commitments inspectable.

### 4. Name documented student misconceptions on the spine where each lives

- **What:** add a "Common misconception" sub-bullet to each chapter that
  is the natural home for a documented misconception: `basic_concepts.md`
  (outcome approach, conjunction fallacy), `conditional_probability.md`
  (`Pr(A|B)` vs. `Pr(B|A)`, base-rate neglect — Falk & Bar-Hillel, 1983),
  `discrete_expectations.md` (mean as "most likely"), `empirical_sums.md`
  (gambler's fallacy as inverted LLN), `continuous_random_variables.md`
  (already partially present — strengthen).
- **Why:** Konold's "outcome approach" (1989), Kahneman & Tversky's
  representativeness, Garfield & Ben-Zvi (2007). Documented evidence
  that *explicit naming + refutation* outperforms formal treatment alone
  for engineering audiences. The book already does this twice (heavy
  tails, Cauchy mean) — extend the pattern.
- **Cost / risk:** low; small spine additions.
- **Impact:** high; touches the chapters with the highest documented
  failure rates.

### 5. Add a multivariate-from-univariate "advance organizer" bullet to `random_vectors.md`

- **What:** opening bullet on the spine making the *parallel* with
  `discrete_vectors.md` explicit: "everything in Ch. 8 carries over with
  sums → integrals, PMF → PDF. The new work is the joint PDF, the
  Jacobian, and convolution."
- **Why:** Ausubel (1968) / Mayer (2001) advance-organizer effect;
  variation theory (Marton, 2015) explicit-contrast principle. The current
  spine treats six constructs as fresh; they are mostly analogs.
- **Cost / risk:** zero.
- **Impact:** moderate-high; reduces extraneous load on a heavy chapter.

### 6. Add a closing forward-pointer bullet (the spiral) to spiral-hinge chapters

- **What:** one-line "Recurs in:" closing bullet on `conditional_probability.md`,
  `discrete_expectations.md`, and `expectations_and_bounds.md`. Each lists
  the chapters where the construct returns at higher sophistication.
- **Why:** Bruner (1960) spiral curriculum is *only effective when the
  learner can see the spiral.* The current spine treats each level as
  fresh. Cheap, high-leverage.
- **Cost / risk:** zero — sidecar-only.
- **Impact:** moderate.

### 7. Add order statistics to `derived_distributions.md`

- **What:** spine bullets for `max`, `min`, k-th order statistic, joint
  density of order statistics.
- **Why:** standard at this level (Ross §6.6, Pitman §4.6, Stark–Woods
  §6.4). The natural payoff of the change-of-variables machinery and the
  primary engineering use (reliability, parallel systems, ML on `max`).
- **Cost / risk:** low spine growth; chapter is currently short.
- **Impact:** moderate-high.

### 8. Add a CDF-revisit / discrete-as-continuous bridge bullet

- **What:** strengthen the discrete-revisit bullet in
  `continuous_random_variables.md` into an explicit contrast: PMF vs. PDF
  (units, "PDF is not a probability"), summation vs. integration,
  step CDF vs. continuous CDF.
- **Why:** Marton (2015) variation theory: students who are not shown the
  contrast explicitly persistently confuse PMF and PDF (Garfield & Ben-Zvi,
  2007).
- **Cost / risk:** zero — restructures an existing bullet.
- **Impact:** moderate.

### 9. Add weak/strong LLN, almost-sure convergence, and de Moivre–Laplace to `empirical_sums.md`

- **What:** spine bullets for almost-sure convergence (starred), the
  distinction between weak LLN (in probability) and strong LLN (almost
  surely), and the de Moivre–Laplace bridge from binomial to normal as
  the CLT preview.
- **Why:** standard in Ross §8, Bertsekas–Tsitsiklis §5, Grimmett–Stirzaker
  §7. de Moivre–Laplace is the historical and pedagogical bridge.
- **Cost / risk:** low.
- **Impact:** moderate.

### 10. Resolve the Cauchy / characteristic-function inconsistency

- **What:** either drop Cauchy from `continuous_random_variables.md` (or
  star it as a "no-MGF" cautionary) *or* add a characteristic-function
  bullet (starred) to `expectations_and_bounds.md`.
- **Why:** internal coherence: a distribution introduced specifically as
  heavy-tailed and pathological should be discussable with the tools the
  book provides. Currently it is not.
- **Cost / risk:** low — a coherence fix.
- **Impact:** moderate.

### 11. Make the appendix relationship visible from `mathematical_review.md`

- **What:** closing tie-back bullet pointing at `appendix_background.md`,
  spelling out that calculus identities live there and the chapter is the
  motivating set-theoretic preliminaries.
- **Why:** Bishop / ESL pattern only works when readers know the
  reference manual exists. Currently invisible from the spine.
- **Cost / risk:** zero — a one-line bullet.
- **Impact:** moderate.

### 12. Make canonical-example commitments visible: standardize the sidecar template

- **What:** project-level decision (touches all sidecars): extend the
  sidecar skeleton with an explicit "Canonical examples" subsection (or
  sub-bullet pattern) so spine commitments to specific worked examples
  are inspectable.
- **Why:** addresses items 3 and 4 systematically. Without a template
  slot, example commitments stay implicit. With it, the sidecar is a
  pedagogical contract.
- **Cost / risk:** moderate — requires a project decision and a
  back-fill pass. Aligns with the existing skeleton.
- **Impact:** moderate; the structural enabler for items 3–4.
