---
slug: 04-permutations-combinations
title: Permutations and Combinations
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/04-permutations-combinations.tex
source_sha256: 89f6242bfc55652aff4bf045a23070d126be93b694263a7d7bb064b96d39be88
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/combinatorics.tex
companion: sources/04-permutations-combinations.md
companion_sha256: 3975ab2c65c197a52bc419a814356b63159df0f57ebee864f5bb421fea0f2cc8
companion_upstream: ../chapters/combinatorics.md
prereqs:
  - 03-counting-principle
audience: undergraduate engineering, first probability course
concepts:
  - id: permutation
    name: Permutations and the factorial
    importance: core
    one_liner: An ordered arrangement of n distinct objects; there are n! of them.
  - id: k-permutation
    name: k-permutations
    importance: core
    one_liner: Ordered selections of k from n number n!/(n-k)! = n(n-1)...(n-k+1).
  - id: combination
    name: Combinations and the binomial coefficient
    importance: highlight
    one_liner: Unordered selections of k from n number C(n,k); a k-permutation is a combination times k! orderings.
  - id: symmetry
    name: Symmetry of the binomial coefficient
    importance: core
    one_liner: Choosing k to keep is choosing n-k to drop, so C(n,k) = C(n,n-k).
  - id: binomial-theorem
    name: Pascal's rule and the binomial theorem
    importance: core
    one_liner: C(n,k)=C(n-1,k-1)+C(n-1,k); (x+y)^n = sum C(n,k) x^k y^{n-k}.
estimated_runtime_sec: 540         # ~9 min (the densest of the four)
---

# Permutations and Combinations — Concept Map

## What
The core counting toolkit. A permutation is an ordered arrangement of n distinct
objects -- there are n factorial of them. A k-permutation is an ordered
selection of k from n, counted by n!/(n-k)!. A combination is an unordered
selection -- a subset -- counted by the binomial coefficient C(n,k). The single
most important relationship: a k-permutation is a combination followed by an
ordering, so the ordered count is the unordered count times k!. The video closes
with Pascal's rule, Pascal's triangle, and the binomial theorem.

## Why (motivation for the viewer)
Almost every finite probability calculation reduces to one question: are we
counting ordered sequences or unordered subsets? Getting that distinction right
-- and knowing the single k! factor that separates them -- is the most common
make-or-break step in counting problems. The binomial coefficient that comes out
is also the backbone of the binomial distribution later in the course, and the
binomial theorem is what makes that distribution's probabilities sum to one.

## How (the spine of the video)
1. Permutations: fill n slots, n choices then n-1 ... down to 1, giving n!.
2. k-permutations: stop after k slots, giving n!/(n-k)! = n(n-1)...(n-k+1).
3. Combinations: the same selection, but order ignored. Count the 2-subsets vs
   the 2-permutations of {1,2,3,4} -- 6 vs 12 -- and name the k! ordering factor.
   This gives C(n,k) = n!/(k!(n-k)!).
4. Symmetry: choosing k to keep = choosing n-k to drop, so C(n,k)=C(n,n-k).
5. Pascal's rule (does element n get picked?) and the binomial theorem, with the
   x=y=1 corollary recovering sum C(n,k)=2^n.

## What else (connections, to seed callbacks in narration)
- k-permutations are sampling without replacement, with ordering; combinations
  are sampling without replacement, without ordering -- two cells of the
  sampling table the fourth video assembles.
- The unordered-without-replacement count is the engine of the hypergeometric
  distribution (forward link to discrete random variables).
- sum_k C(n,k) = 2^n connects back to the 2^n subsets from the Counting video
  (now split by subset size), recovered again from the binomial theorem.
- The binomial coefficient returns as the binomial distribution's normalizer.

## Conceptual progression (drives the storyboard)
fill three slots 3x2x1 = 6, list the 6 permutations  ->  fill only k of n slots,
n!/(n-k)!  ->  the 12 ordered pairs of {1,2,3,4} collapse, k! at a time, into 6
unordered subsets  ->  C(n,k) formula + the C(n,k)=C(n,n-k) mirror  ->  Pascal's
triangle building row by row, then (x+y)^n.

## Visual opportunities
- Three slots filled left to right with a shrinking pool (3, then 2, then 1);
  the 6 permutations of {1,2,3} listed (reuse the ball style).
- k-permutation: 4 balls, 2 slots, 4 x 3 = 12.
- The perm-vs-combination contrast: 12 ordered pairs grouped into 6 dashed
  loops of 2, the k!=2 factor labeled (the chapter's key visual).
- C(n,k) = C(n,n-k) shown as "pick k in" vs "pick n-k out".
- Pascal's triangle with one entry highlighted as the sum of the two above it.

## Deliberately out of scope
- Stirling's formula (starred in the notes) -- skipped.
- Multinomial coefficients / set partitions (next video).
- The full binomial distribution (later chapter) -- only foreshadowed.
