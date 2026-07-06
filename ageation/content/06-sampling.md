---
slug: 06-sampling
title: A Unified View of Sampling
stage: concept            # tex -> [concept] -> script -> scene -> render
status: approved             # draft | reviewed | approved  (human gate)
source: sources/06-sampling.tex
source_sha256: 89f6242bfc55652aff4bf045a23070d126be93b694263a7d7bb064b96d39be88
provenance_stamped: 2026-07-06
framework_commit: a64a018
upstream: ../chapters/combinatorics.tex
companion: sources/06-sampling.md
companion_sha256: 3975ab2c65c197a52bc419a814356b63159df0f57ebee864f5bb421fea0f2cc8
companion_upstream: ../chapters/combinatorics.md
prereqs:
  - 05-partitions
audience: undergraduate engineering, first probability course
concepts:
  - id: sampling-table
    name: The 2x2 sampling table
    importance: core
    one_liner: Drawing k items from n is classified by replacement (yes/no) and order (kept/dropped); the four counts are n^k, n!/(n-k)!, C(n+k-1,k), and C(n,k).
  - id: ordered-counts
    name: The ordered counts from the counting principle
    importance: core
    one_liner: With replacement each draw has n choices (n^k); without replacement the pool shrinks (n!/(n-k)!).
  - id: k-factorial-link
    name: The k! link down the without-replacement column
    importance: highlight
    one_liner: Dropping order divides the without-replacement ordered count n!/(n-k)! by k! orderings, giving C(n,k).
  - id: stars-and-bars-cell
    name: The with-replacement, unordered cell
    importance: core
    one_liner: Order ignored with repeats allowed is the stars-and-bars count C(n+k-1,k) -- the subtler fourth cell.
  - id: birthday-problem
    name: The Birthday Problem
    importance: highlight
    one_liner: With k people and 365 days, P(shared) = 1 - [365!/(365-k)!]/365^k, which first exceeds 1/2 at just 23 people.
estimated_runtime_sec: 300         # ~5 min (one table + one worked example)
---

# A Unified View of Sampling — Concept Map

## What
The organizing schema of the whole chapter, drawn together at last. Every urn
problem in combinatorics is a question of drawing k items from n distinguishable
items, classified by two binary choices: are draws made *with* or *without
replacement*, and is their *order* recorded or not? Those two yes/no choices
make a 2x2 table with four counts:

|                       | ordered          | unordered      |
|-----------------------|------------------|----------------|
| with replacement      | n^k              | C(n+k-1, k)    |
| without replacement   | n!/(n-k)!        | C(n, k)        |

The ordered column comes straight from the counting principle; each unordered
count is the ordered one with the orderings quotiented out. The video then
applies the table to the Birthday Problem.

## Why (motivation for the viewer)
The four counts were each derived separately across the chapter, but the real
skill is recognizing *which* of the four a problem calls for -- that is usually
the crux. Laying them in one grid turns four formulas into one decision: ask the
two questions, read off the cell. The Birthday Problem then shows the payoff: a
single ratio of two table cells produces a famously counterintuitive answer.

## How (the spine of the video)
1. Recap V3 (partitions + stars and bars) and pose the two binary questions.
2. Build the 2x2 table: rows = with / without replacement, columns = ordered /
   unordered. Fill the ordered column first (n^k, n!/(n-k)!) from the counting
   principle, then the unordered column (C(n+k-1,k), C(n,k)).
3. Emphasize the k! link down the without-replacement column: C(n,k) is
   n!/(n-k)! divided by k!. Note the with-replacement column is subtler --
   repeats cannot be reordered -- so its unordered cell needs stars and bars.
4. Birthday Problem: k people, 365 days. Denominator 365^k is sampling with
   replacement, ordered; numerator 365!/(365-k)! is without replacement,
   ordered. P(all distinct) is their ratio; P(shared) = 1 minus that.
5. The punchline: the probability first exceeds 1/2 at just k = 23.

## What else (connections, to seed callbacks in narration)
- The ordered, with-replacement cell n^k is the multi-stage sampling count from
  Video 1 (the counting principle).
- The without-replacement column -- n!/(n-k)! and C(n,k) -- is exactly the
  k-permutation and combination from Video 2, with the same k! factor between.
- The with-replacement, unordered cell C(n+k-1,k) is the stars-and-bars count
  from Video 3 (n item types as subsets, k draws as stars).
- The Birthday Problem uses only the counting principle and a k-permutation --
  two cells of the very table just assembled.
- This finale closes the chapter; the next chapter makes the equally-likely
  model rigorous with the axioms of probability.

## Conceptual progression (drives the storyboard)
two binary questions -> a 2x2 grid with row/column headers -> fill the ordered
column (n^k, n!/(n-k)!) -> fill the unordered column, dividing the
without-replacement entry by k! to get C(n,k), and naming stars-and-bars for the
with-replacement cell C(n+k-1,k) -> apply two cells to the Birthday Problem ->
the surprising 23 -> >1/2 punchline + bridge to the next chapter.

## Visual opportunities
- A clean 2x2 grid: gridlines, "with replacement"/"without replacement" row
  labels, "ordered"/"unordered" column labels, each cell a MathTex count.
- A rightward arrow across the without-replacement row labeled "÷ k!" linking
  n!/(n-k)! to C(n,k).
- Birthday Problem: k figures and a strip of 365 days; numerator/denominator
  written as table cells; the "23" callout where the curve crosses 1/2.

## Deliberately out of scope
- The lottery and sinking-boat examples in 2.6 -- one worked example (the
  Birthday Problem) is enough to demonstrate reading the table.
- A formal treatment of independence -- kept informal, as in the notes.
- Re-deriving each count from scratch -- the chapter already did that; this
  video only assembles and applies them.
