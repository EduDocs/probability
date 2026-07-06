<!-- --- provenance (auto-added by tools/vendor_sources.py) --- -->
<!-- upstream: ../chapters/combinatorics.md -->
<!-- upstream_sha256: 1b3b1f70fc6bd7b1e040700502b741fbb58dc4ccd655d68710478c9fa07ef7e3 -->
<!-- git_origin: git@github.com:EduDocs/probability.git -->
<!-- git_commit: 5abd463a5f8a9a8dc94fb064ec671ec1451bd61b -->
<!-- git_tag: 5abd463 -->
<!-- vendored_at: 2026-06-29 -->
<!-- EDITABLE working copy. Normalize notation here; the parent stays read-only. -->
<!-- ---------------------------------------------------------------- -->
---
introduces: [finite-equally-likely-model, counting-principle, permutation, combination, binomial-coefficient, binomial-theorem, pascals-rule, multinomial-coefficient]
requires:   [set, cartesian-product]
---

# Intuitive Probability and Combinatorics — scratch

> Scratch/ideas only. The shipped prose lives in `combinatorics.tex`. Not part of the LaTeX build.

## Purpose
Build intuition for probability in the simplest case — finite, equally-likely outcomes — by developing the counting tools needed to compute event probabilities as ratios of cardinalities.

## Pedagogical stance
- Intentionally informal: "event" is used loosely (a subset of outcomes) and the equally-likely model is computed directly, *before* the axioms are introduced in `probability_models`. The formal treatment can technically come next; locally, the intuitive approach lands better. Frontmatter therefore deliberately does **not** `require: event` — the spine commits to using it pre-formally.
- Ordering constraint: this chapter precedes `probability_models`, so inclusion–exclusion and the axioms are **not** yet available. Examples that need inclusion–exclusion (derangement / hat-check) are out of scope here; the birthday problem (counting + complement only) is in scope.

## Key points / outline
- Finite equally-likely model: probability of an event = (favorable outcomes) / (total outcomes).
- Counting outcomes is often the real difficulty; combinatorics gives the toolkit.
- Counting principle: cardinality of a Cartesian product as a product of cardinalities; iterated for multi-stage experiments.
- Joint experiments via Cartesian products: a light, intuitive touch only — the equally-likely product construction previews independence, but the formal product rule and the definition of independence are deferred to `conditional_probability`. Do not assert the "iff independent" characterization here (it reads as circular before independence is defined).
- Permutations: ordered arrangements of n distinct objects; factorial n!.
- k-permutations: ordered selections of k from n, n!/(n-k)!.
- Combinations: unordered selections; binomial coefficient.
- Permutation-vs-combination contrast (variation theory): one concrete scenario counted *both* ways, with the k! ordering factor named as the single difference. This is the most-confused pair in the chapter.
- Binomial identities: symmetry C(n,k)=C(n,n-k); Pascal's rule C(n,k)=C(n-1,k-1)+C(n-1,k) via the "does element n get picked?" argument; binomial theorem (x+y)^n = sum C(n,k) x^k y^{n-k}, recovering sum C(n,k)=2^n by setting x=y=1 (a second derivation alongside the power-set one), and the alternating sum sum (-1)^k C(n,k)=0 by setting x=-1,y=1. Binomial theorem is needed downstream so the binomial PMF in `discrete_random_variables` sums to one.
- Stirling's formula as an asymptotic approximation to n! (optional/starred). Placed *after* the basic counts (combinations), not mid-permutations — it is an asymptotic result, not a counting tool.
- Partitions of a set / multinomial coefficient for splitting n items into labeled groups.
- Integer solutions to linear equations as a stars-and-bars partition problem (starred).
- The four sampling schemes (replacement × ordering) assembled into one explicit 2×2 summary table — the chapter's organizing schema, latent across four scattered examples. Shipped as its own section "A Unified View of Sampling", with each unordered count derived by quotienting the matching ordered count by k!. Uses the unified "draw k from n" convention:
  - with replacement, ordered: n^k
  - without replacement, ordered: n!/(n-k)!
  - without replacement, unordered: C(n,k)
  - with replacement, unordered: C(n+k-1, k)  (stars-and-bars, relabeled from the n-balls-into-r-subsets derivation)
- Combinatorial examples that tie counting back to probability calculations.

## Canonical worked examples
- Birthday problem — first intuition-busting example; needs only the counting principle and a complement; refutes the "outcome approach" misconception (Konold, 1989).
- Sampling-scheme urns (the four cases above) — keep, and label each with its cell in the 2×2 table.
- Hypergeometric framing: the without-replacement/unordered urn is the seed of the hypergeometric distribution in `discrete_random_variables`; flag the forward link.
- Lottery (Pick 3, Mega Millions) — keep the counting, trim the operational flavour text (security seals, mixing paddles) that adds extraneous load.
- Sinking-boat partition example — keep.

## Decisions
- Stars and bars: named the technique explicitly at the integer-solutions argument (was unnamed "balls and markers"). Figures + prose now use literal stars (\bigstar) and bars (|), renaming balls -> stars and markers -> bars. The name had to be anchored where the argument lives, because the downstream sampling table refers back to "the stars-and-bars count".
- Independence kept informal in the worked examples too, not just the counting-principle section. Birthday setup says "no relation to one another"; Pick 3 says "with replacement, repetitions possible" — neither uses the word "independent". The joint model is carried by the equally-likely-over-the-product statement. Formal independence stays deferred to `conditional_probability`.
- Sampling table uses the unified "draw k from n" convention -> with-replacement/unordered cell is C(n+k-1,k). The chapter's own stars-and-bars derivation counts n balls into r subsets, so the table caption flags the relabeling (n item types <-> subsets, k draws <-> stars).

## Open questions
-

## Notes & references
- Standard combinatorics references (see chapter's Further Reading block at end of `.tex`).
