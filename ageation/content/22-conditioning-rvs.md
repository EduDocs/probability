---
slug: 22-conditioning-rvs
title: Conditioning Random Variables
stage: concept            # tex -> [concept] -> script -> scene -> render
status: reviewed          # human approved via chat 2026-07-03
source: sources/22-conditioning-rvs.tex
source_sha256: 720b9deaf084fab02fbf89e2487f4ad3594bbd53458a78dc1975eca3293c6b7b
provenance_stamped: 2026-07-06
framework_commit: 9ec97cb-dirty
upstream: ../chapters/discrete_vectors.tex
companion: sources/22-conditioning-rvs.md
companion_sha256: 24365e9d6b861b146df44bdc5fd758e3aedc15ae905f595e143aacdc613a4a68
prereqs:
  - 21-joint-pmfs
audience: undergraduate engineering, first probability course
concepts:
  - id: cond-on-event
    name: Conditioning a random variable on an event
    importance: core
    one_liner: p_{X|S}(x) = Pr(X = x | S) — the PMF re-weighted by what we know; total probability shows it sums to one, so it is a genuine PMF.
  - id: cond-on-rv
    name: Conditioning on a random variable
    importance: core
    one_liner: p_{Y|X}(y|x) = p_{X,Y}(x,y) / p_X(x) — slice the joint table at X = x and renormalize; one conditional PMF for every value of x.
  - id: two-views
    name: Events and random variables — one conditioning idea
    importance: highlight
    one_liner: Conditioning on S is conditioning on its indicator variable at 1, and conditioning on X = x is conditioning on an event — the two definitions are one.
  - id: product-rule
    name: The product rule for joint PMFs
    importance: core
    one_liner: p_{X,Y}(x,y) = p_{Y|X}(y|x) p_X(x) — build a joint distribution sequentially, one draw at a time.
  - id: truncated-geometric
    name: Worked example — packets with a retry limit
    importance: core
    one_liner: Given that a packet with at most n retries succeeds, its trial count has the geometric PMF truncated and renormalized by 1 - (1-p)^n.
  - id: poisson-splitting
    name: Worked example — splitting a Poisson
    importance: highlight
    one_liner: Poisson(lambda) transmissions, each a one with probability p independently — the count of ones is Poisson(p*lambda); conditioning plus the product rule prove it.
  - id: hypergeometric
    name: Erasures in a packet header
    importance: optional        # cut first if over budget
    one_liner: Conditioned on c corrupted bits total, the number in the n-bit header is hypergeometric — counting, not chance, once the total is known.
estimated_runtime_sec: 480      # ~8 min (five beats in project.yaml)
---

# Conditioning Random Variables — Concept Map

This video covers Section 7.3 of book chapter 7 (both subsections:
conditioning on events, conditioning on random variables). Video 21 built
the joint PMF this video slices; video 23 averages the slices.

## What
Conditioning, met in chapter 4 for events, extends to random variables in
two steps. Given an event S, the **conditional PMF**
`p_{X|S}(x) = Pr(X = x | S)` re-weights the distribution by what is known —
and total probability guarantees it still sums to one. Given another random
variable, `p_{Y|X}(y|x) = p_{X,Y}(x,y) / p_X(x)` slices the joint table at
`X = x` and renormalizes — a whole *family* of PMFs, one per value of x.
Rearranged, this is the **product rule** `p_{X,Y} = p_{Y|X} p_X`: joint
distributions can be built sequentially.

## Why it matters
Dependence is the whole point of joint models, and conditioning is how
dependence is *used*: observe one variable, update the other. The
slice-and-renormalize picture makes the definition mechanical rather than
mysterious, and the product rule runs it in reverse — most real models are
*specified* conditionally (first this draw, then that one given it). The
Poisson-splitting example shows the machinery earning its keep on a
genuinely surprising result.

## Key ideas (in dependency order)
1. **Conditioning on an event.** `p_{X|S}(x) = Pr({X = x} ∩ S) / Pr(S)` —
   chapter 4's definition applied to the events `{X = x}`. Because those
   events partition Ω, total probability gives `sum_x p_{X|S}(x) = 1`: a
   valid PMF, not just a ratio.
2. **Worked: the retry limit.** Transmissions succeed with probability p;
   a system drops the packet after n failures. Given success S,
   `Pr(S) = 1 - (1-p)^n` and `p_{Y|S}(k) = (1-p)^{k-1} p / (1 - (1-p)^n)`
   for k = 1..n — the geometric PMF truncated and renormalized. The bars
   keep their shape; only the scale changes.
3. **Conditioning on a random variable.** `p_{Y|X}(y|x) = p_{X,Y}(x,y) /
   p_X(x)` (defined when `p_X(x) > 0`): fix a row of the joint table,
   divide by its row sum. Each x yields its own conditional PMF — a family
   indexed by the observation.
4. **One idea, two dresses.** Conditioning on S equals conditioning on the
   indicator variable `1_S` at value 1, and `p_{X|Y}(x|y)` is just
   conditioning on the event `{Y = y}` — the two definitions coincide
   (video 19's indicator returns).
5. **The product rule.** `p_{X,Y}(x,y) = p_{Y|X}(y|x) p_X(x) =
   p_{X|Y}(x|y) p_Y(y)` — read the slice formula backwards to *construct*
   joints sequentially.
6. **Worked: Poisson splitting.** Bits arrive Poisson(λ); each is a one
   with probability p, independently. Conditioned on K = k total, the ones
   are binomial(k, p); un-condition with the product rule and the sum
   telescopes: M is Poisson(pλ). Thinning a Poisson stream leaves a
   Poisson stream.

## What else (connections, to seed callbacks in narration)
- Chapter 4's conditional probability (videos 11–14) is the foundation —
  same ratio, now organized per value of a random variable.
- The geometric PMF's halving bars (videos 16, 18) return truncated.
- The indicator bridge is video 19's `E[1_S(X)] = Pr(X ∈ S)` in a new role.
- Poisson splitting foreshadows video 25, where the OGF product rule gives
  the mirror result (merging independent Poisson streams adds parameters).
- The hypergeometric example shares its binomial-ratio form with the
  Extreme Trio contest PMF (video 19).

## Conceptual progression (drives the storyboard)
Chapter-4 ratio recalled → applied to {X = x} events → a PMF survives
(total probability) → truncated geometric as re-scaling bars → the joint
table sliced at a row, renormalized to a conditional PMF → slide the slice:
a family of PMFs → the formula reversed into the product rule → Poisson
splitting as the payoff derivation.

## Visual opportunities
- **Truncation**: the geometric bars beyond n fade out; the surviving bars
  grow uniformly to re-fill mass one (a single scale animation).
- **The slice**: video 21's joint table with one row highlighted, lifted
  out, and renormalized into a bar chart; then the highlight sweeps to
  other rows, morphing the conditional PMF as x changes — the "family."
- **Product rule**: the slice animation played backwards — a marginal bar
  times a conditional row rebuilds the joint cell by cell.
- **Poisson splitting**: a stream of dots (bits), each colored one/zero by
  a coin flip; the ones sub-stream visibly thinner; the telescoping sum
  compressed to its first and last lines.

## Notation (per project.yaml)
- Conditional PMFs `p_{X|S}(x)`, `p_{Y|X}(y|x)`; conditionals written with
  `\mid`, never a bare bar.
- Indicator `\mathbf{1}_S`.

## Deliberately out of scope
- Conditional expectation — that is video 23 in its entirety.
- Independence (`p_{Y|X} = p_Y`) — named in one breath at most; video 24.
- The starred hypergeometric example is optional from the start.

## Cut first (if the script runs over budget)
The hypergeometric example drops entirely; the two-views bridge (idea 4)
compresses to one spoken sentence over the indicator symbol.
