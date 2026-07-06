---
slug: 05-partitions
title: Partitions and Stars and Bars
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/05-partitions.tex
source_sha256: 89f6242bfc55652aff4bf045a23070d126be93b694263a7d7bb064b96d39be88
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/combinatorics.tex
companion: sources/05-partitions.md
companion_sha256: 3975ab2c65c197a52bc419a814356b63159df0f57ebee864f5bb421fea0f2cc8
companion_upstream: ../chapters/combinatorics.md
prereqs:
  - 04-permutations-combinations
audience: undergraduate engineering, first probability course
concepts:
  - id: set-partition
    name: Set partitions and the multinomial coefficient
    importance: core
    one_liner: Splitting n distinct items into r labeled groups of fixed sizes n_1,...,n_r is counted by n!/(n_1! n_2! ... n_r!).
  - id: counting-argument
    name: Arrange-then-divide counting argument
    importance: core
    one_liner: Line up all n items (n! ways), then divide out the orderings within each group that do not matter.
  - id: stars-and-bars
    name: Stars and bars
    importance: highlight
    one_liner: Nonnegative integer solutions of x_1+...+x_r = k correspond to arrangements of k stars and r-1 bars, so there are C(k+r-1, r-1) of them.
  - id: with-replacement-unordered
    name: Sampling with replacement, without ordering
    importance: core
    one_liner: Drawing k times with replacement from r items and ignoring order gives C(n+k-1, k) outcomes -- the last cell of the sampling table.
estimated_runtime_sec: 390         # ~6.5 min
---

# Partitions and Stars and Bars — Concept Map

## What
Two ways to split a set, and the counts they produce. First, a set partition:
divide n distinct items into r labeled groups of fixed sizes n_1, ..., n_r. The
count is the multinomial coefficient n!/(n_1! n_2! ... n_r!) -- a direct
generalization of the binomial coefficient (the r = 2 case). Second, stars and
bars: when the group sizes are free and only the totals matter, count the
nonnegative integer solutions of x_1 + ... + x_r = k by drawing k stars and r-1
bars in a row. There are C(k+r-1, r-1) = C(k+r-1, k) of them. This delivers the
final cell of the sampling table -- with replacement, without order.

## Why (motivation for the viewer)
The binomial coefficient split a set in two; many real problems split it into
several groups at once -- dealing hands, assigning roles, tallying repeated
draws. The multinomial coefficient is the natural count, and it is the
normalizer of the multinomial distribution later in the course. Stars and bars
is the trick that resolves the one remaining sampling scheme (with replacement,
unordered), the cell that completes the 2x2 table the next video assembles.

## How (the spine of the video)
1. Set partition: line up n items in n! ways; the order inside each group of
   size n_i does not matter, so divide by n_i!. The result is the multinomial
   coefficient n!/(n_1! ... n_r!).
2. Concrete split: 6 distinct items into groups of sizes 3, 2, 1 gives
   6!/(3! 2! 1!) = 60.
3. Stars and bars: k identical stars and r-1 bars in a row of k+r-1 positions;
   the bars cut the stars into r groups, mapping an arrangement to a solution
   tuple (x_1, ..., x_r). Choose the bar (or star) positions: C(k+r-1, r-1).
4. Sampling tie-in: drawing k times with replacement from r items, order
   ignored, is exactly this count -- C(n+k-1, k) -- the last sampling cell.

## What else (connections, to seed callbacks in narration)
- The multinomial coefficient with r = 2 is the binomial coefficient C(n,k)
  from the last video -- partitioning into "the k chosen" and "the n-k left".
- Stars and bars answers a different question from the multinomial: there the
  group sizes were fixed; here we count how the sizes themselves can be chosen.
- With-replacement-unordered is the fourth and final cell of the sampling
  table; the next video lays all four schemes side by side.
- The multinomial coefficient returns as the multinomial distribution's
  normalizer (forward link).

## Conceptual progression (drives the storyboard)
recap C(n,k) as a two-way split  ->  split n into r groups: arrange n!, divide
by each n_i!, giving the multinomial coefficient  ->  6 items into 3,2,1 = 60
->  stars and bars: a concrete row of stars and bars mapping to a tuple, count
C(k+r-1, r-1)  ->  the with-replacement-unordered cell C(n+k-1, k) + bridge.

## Visual opportunities
- A row of 6 numbered balls dealt into three labeled boxes of sizes 3, 2, 1;
  the multinomial fraction written out to 60.
- A concrete stars-and-bars row, e.g. star star bar star bar bar star, with the
  bars cutting the stars into groups and a tuple (x_1,...,x_4) read off below.
- The k+r-1 positions braced, with "choose the r-1 bar slots" highlighted.
- The 2x2 sampling table with the with-replacement/unordered cell filled in.

## Deliberately out of scope
- The full multinomial distribution (later chapter) -- only foreshadowed.
- Compositions vs partitions of an integer (number-theoretic sense) -- the
  notes count labeled tuples, which is all the sampling table needs.
- The complete side-by-side sampling table -- that is the next video's job.
