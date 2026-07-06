# derived_from: content/19-functions-and-expectations-script.md
# derived_from_sha256: 288b25036b8dae85c325ef0f7193152fef2501a1f4cef45ad84d33446ea55436
"""Chapter 6, Video 2 -- Functions and Expectations.

Source notes : discrete_expectations.tex (Section 6.2 + subsections 6.2.1
               The Mean, 6.2.2 The Variance, 6.2.3 Affine Functions).
Script        : content/19-functions-and-expectations-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/functions_and_expectations.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from manim import *  # noqa: F401,F403
from manim_voiceover import VoiceoverScene

from _style import (
    ACCENT,
    MUTED,
    BAR,
    INK,
    TITLE,
    SECTION,
    BODY,
    SMALL,
    CAPTION,
    expectation,
    variance,
    pr,
    section_title,
    make_pmf_chart,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    ball,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


def card(tex: str, label: str | None = None) -> VGroup:
    """A compact result card: a rounded frame around one formula."""
    body = MathTex(tex, font_size=SMALL, color=INK)
    frame = RoundedRectangle(
        corner_radius=0.15,
        width=body.width + 0.6, height=body.height + 0.5,
        color=MUTED,
    ).set_stroke(MUTED, 2)
    body.move_to(frame)
    parts = VGroup(frame, body)
    if label:
        tag = Text(label, font_size=CAPTION, color=MUTED)
        tag.next_to(frame, UP, buff=0.12)
        parts.add(tag)
    return parts


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Functions and Expectations",
            ["Average any function of a random variable straight",
             "from its PMF - and meet the mean and the variance."],
            kicker="Chapter 6  ·  Meeting Expectations",
        )
        tag = progress_tag(2, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The expectation of g(X)", font_size=BODY, color=INK),
            Text("2.  Two ways to the same answer", font_size=BODY, color=INK),
            Text("3.  The mean and the variance", font_size=BODY, color=INK),
            Text("4.  Affine functions", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="Last video we defined the expected value: one number that "
                 "summarizes a whole PMF. This video, that idea grows into a "
                 "toolkit."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        outline.next_to(intro, DOWN, buff=0.6)
        fit_to_frame(outline)

        with self.voiceover(
            text="We'll learn to average any function of a random variable "
                 "directly from its PMF — no derived distribution needed —"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(text="check the recipe on a radio contest,"):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and then meet the two summaries that dominate all of "
                 "probability: the mean, which is a center of mass, and the "
                 "variance, which measures spread."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We finish with the algebra that ties them together — what "
                 "happens to both under shifting and scaling."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExpectationOfFunction(VoiceoverScene):
    """Beat: lotus -- the direct formula, its reductions, the indicator."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Expectation of g(X)")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Route one: through the derived PMF of Y (last chapter's machinery).
        y_def = MathTex("Y = g(X)", font_size=BODY, color=INK)
        y_def.next_to(title, DOWN, buff=0.5)
        route1 = VGroup(
            MathTex("p_X", font_size=SMALL, color=MUTED),
            MathTex(r"\rightarrow", font_size=SMALL, color=MUTED),
            MathTex("p_Y", font_size=SMALL, color=MUTED),
            MathTex(r"\rightarrow", font_size=SMALL, color=MUTED),
            MathTex(expectation("Y"), font_size=SMALL, color=MUTED),
        ).arrange(RIGHT, buff=0.3)
        route1_tag = Text("route one: derive the PMF of Y",
                          font_size=CAPTION, color=MUTED)
        route1_block = VGroup(route1, route1_tag).arrange(DOWN, buff=0.2)
        route1_block.next_to(y_def, DOWN, buff=0.5)

        with self.voiceover(
            text="Suppose Y equals g of X, and we want its mean."
        ):
            self.play(Write(y_def), run_time=0.8)

        with self.voiceover(
            text="We know one route already: build the PMF of Y from "
                 "preimages, like last chapter, then apply the definition. "
                 "That works — but there is a shortcut."
        ):
            self.play(FadeIn(route1_block), run_time=1.0)

        formula = MathTex(
            expectation("g(X)"), "=",
            r"\sum_{x \in X(\Omega)} g(x) \, p_X(x)",
            font_size=BODY,
        )
        formula.next_to(route1_block, DOWN, buff=0.55)
        fit_to_frame(formula)
        route2_tag = Text("route two: straight from the PMF of X",
                          font_size=CAPTION, color=MUTED)
        route2_tag.next_to(formula, DOWN, buff=0.22)

        with self.voiceover(
            text="The expectation of g of X can be computed straight from "
                 "the PMF of X: sum g of x times p sub X of x over the range "
                 "of X. Evaluate g on each value, weight by the original "
                 "masses, add."
        ):
            self.play(Write(formula), run_time=1.4)
            self.play(formula[0].animate.set_color(ACCENT),
                      FadeIn(route2_tag), run_time=0.7)

        reductions = VGroup(
            MathTex(r"g(x) = x:\quad", expectation("X"),
                    font_size=SMALL, color=INK),
            MathTex(r"g(x) = c:\quad", expectation("c"), "= c",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        reductions.next_to(route2_tag, DOWN, buff=0.4)

        with self.voiceover(
            text="Two quick checks. If g is the identity, this is just the "
                 "mean from last video — the definition subsumes it. And if "
                 "g is a constant c, the masses sum to one and the "
                 "expectation is c itself."
        ):
            self.play(FadeIn(reductions[0], shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(reductions[1], shift=RIGHT * 0.3), run_time=0.6)

        indicator = MathTex(
            expectation(r"\mathbf{1}_S(X)"), "=", pr(r"X \in S"),
            font_size=BODY,
        )
        indicator.move_to(reductions.get_center())
        fit_to_frame(indicator)

        with self.voiceover(
            text="One more, with real content: let g be the indicator of a "
                 "set S — one inside S, zero outside. Then the expectation of "
                 "the indicator of X in S is exactly the probability that X "
                 "lands in S. Probabilities are expectations. Keep that; it "
                 "pays off across the course."
        ):
            self.play(FadeOut(reductions), run_time=0.4)
            self.play(Write(indicator), run_time=1.0)
            self.play(formula[0].animate.set_color(INK),
                      indicator[2].animate.set_color(ACCENT), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExtremeTrio(VoiceoverScene):
    """Beat: two-ways -- both routes on the radio contest, same answer."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Two Ways to the Same Answer")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Left column: the setup (drum of cards + the two formulas).
        drum = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.2,
                                color=MUTED).set_stroke(MUTED, 2)
        drum_label = Text("100 cards", font_size=CAPTION, color=INK)
        david = Text("50 are David's", font_size=CAPTION, color=ACCENT)
        VGroup(drum_label, david).arrange(DOWN, buff=0.18).move_to(drum)
        drum_grp = VGroup(drum, drum_label, david)

        pmf = MathTex(
            r"p_X(k) = \frac{\binom{50}{k}\binom{50}{3-k}}{\binom{100}{3}}",
            font_size=SMALL,
        )
        gdef = MathTex(r"g(k) = 1000 \min\{k, 1\}", font_size=SMALL)
        # Both columns sit high from the start so the two closing lines get
        # a clear lane at the bottom and the final frame reads balanced
        # (2026-07-03 draft review, 3:17).
        left = VGroup(drum_grp, pmf, gdef).arrange(DOWN, buff=0.35)
        left.move_to(LEFT * 3.6 + UP * 0.35)
        fit_to_frame(left)

        with self.voiceover(
            text="Let's test both routes on the same problem. A radio "
                 "station runs a contest: one hundred cards in a drum, three "
                 "drawn, each winner gets a thousand dollars — but each "
                 "person can win only once. David mailed in fifty of those "
                 "hundred cards. Let X be how many of the three drawn cards "
                 "are his. Its PMF comes from counting: choose k of his "
                 "fifty, and three minus k of the other fifty. His winnings "
                 "are g of X: a thousand times the minimum of X and one."
        ):
            self.play(Create(drum), FadeIn(drum_label), run_time=0.9)
            self.play(FadeIn(david), run_time=0.6)
            self.play(Write(pmf), run_time=1.2)
            self.play(Write(gdef), run_time=0.9)

        # Right column: the two routes, stacked.
        r1_head = Text("route one: sum g(k) p(k)", font_size=CAPTION,
                       color=MUTED)
        r1 = MathTex(
            r"\sum_{k=0}^{3} g(k)\, p_X(k) = 1000 \cdot \tfrac{29}{33}",
            font_size=SMALL,
        )
        r2_head = Text("route two: through the PMF of Y", font_size=CAPTION,
                       color=MUTED)
        r2 = MathTex(
            r"p_Y(0) = \tfrac{4}{33},\quad "
            r"p_Y(1000) = \tfrac{29}{33}",
            font_size=SMALL,
        )
        r2b = MathTex(r"0 \cdot \tfrac{4}{33} + 1000 \cdot \tfrac{29}{33}"
                      r"= 1000 \cdot \tfrac{29}{33}",
                      font_size=SMALL)
        right = VGroup(r1_head, r1, r2_head, r2, r2b).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28)
        right.move_to(RIGHT * 3.3 + UP * 0.35)
        fit_to_frame(right)

        with self.voiceover(
            text="Route one, the direct formula: sum g of k times the mass "
                 "of k over k equals zero to three. The zero term drops out, "
                 "the rest collapse — a thousand times twenty-nine over "
                 "thirty-three."
        ):
            self.play(FadeIn(r1_head), Write(r1), run_time=1.4)

        with self.voiceover(
            text="Route two, through Y itself: Y is either zero or a "
                 "thousand. The chance of zero is the chance none of the "
                 "three cards is David's — four over thirty-three. So Y "
                 "equals a thousand with probability twenty-nine over "
                 "thirty-three. Same product."
        ):
            self.play(FadeIn(r2_head), Write(r2), run_time=1.4)
            self.play(Write(r2b), run_time=1.0)

        payoff = MathTex(expectation("g(X)"), r"\approx \$878.79",
                         font_size=BODY, color=ACCENT)
        payoff.to_edge(DOWN, buff=0.7)
        agree = Text("the same answer, provably, always",
                     font_size=CAPTION, color=MUTED)
        agree.next_to(payoff, UP, buff=0.3)

        with self.voiceover(
            text="Both routes, one answer: about eight hundred and "
                 "seventy-nine dollars. That agreement is a theorem, not "
                 "luck — group the values of X by where g sends them, and "
                 "the two sums rearrange into each other."
        ):
            self.play(FadeIn(agree), Write(payoff), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CenterOfMass(VoiceoverScene):
    """Beat: mean -- the Bernoulli balance beam and the named means."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Mean as a Center of Mass")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The rod: a number line from -0.5 to 1.5 with the two mass points.
        rod = NumberLine(x_range=[-0.5, 1.5, 0.5], length=8,
                         include_numbers=True, font_size=30)
        rod.shift(DOWN * 0.8)
        b0 = ball("0.25", MUTED, radius=0.28, font_size=22)
        b0.move_to(rod.number_to_point(0) + UP * 0.45)
        b1 = ball("0.75", BAR, radius=0.42, font_size=26)
        b1.move_to(rod.number_to_point(1) + UP * 0.6)

        fulcrum = Triangle(color=ACCENT, fill_opacity=1).scale(0.18)
        fulcrum.next_to(rod.number_to_point(0.5), DOWN, buff=0.05)

        # The balance figure is one composition: balls sit on the rod and
        # the fulcrum tucks under it.
        mark_intended_overlap(rod, b0, b1, fulcrum,
                              reason="balance-beam figure by construction")

        pmf_line = MathTex(r"p_X(0) = 0.25,\quad p_X(1) = 0.75",
                           font_size=SMALL)
        pmf_line.next_to(title, DOWN, buff=0.45)

        with self.voiceover(
            text="The simplest expectation deserves a picture. Take the PMF "
                 "of X and build it physically: at each value x, place a "
                 "particle whose mass is p sub X of x. Here is a Bernoulli "
                 "with mass one-quarter at zero and three-quarters at one."
        ):
            self.play(Write(pmf_line), run_time=1.0)
            self.play(Create(rod), run_time=0.8)
            self.play(FadeIn(b0, shift=DOWN * 0.3),
                      FadeIn(b1, shift=DOWN * 0.3), run_time=0.9)

        com = MathTex(
            r"\frac{m_1 x_1 + m_2 x_2}{m_1 + m_2}", "=", "0.75",
            font_size=BODY,
        )
        com.next_to(pmf_line, DOWN, buff=0.4)
        mean_eq = MathTex(expectation("X"), "=", "0.75",
                          font_size=BODY, color=ACCENT)
        mean_eq.move_to(com)

        with self.voiceover(
            text="Ask a mechanics question: where does this system balance? "
                 "The center of mass is the mass-weighted average of the "
                 "positions — and that is, symbol for symbol, the formula "
                 "for the mean. This system balances at three-quarters: the "
                 "mean of the Bernoulli. The mean is where the PMF balances."
        ):
            self.play(FadeIn(fulcrum, shift=UP * 0.2), run_time=0.6)
            self.play(Write(com), run_time=1.2)
            self.play(fulcrum.animate.next_to(rod.number_to_point(0.75),
                                              DOWN, buff=0.05),
                      run_time=1.2)
            self.play(TransformMatchingShapes(com, mean_eq), run_time=1.0)

        cards = VGroup(
            card(expectation("X") + r"= \tfrac{1}{p}", "geometric(p)"),
            card(expectation("X") + r"= np", "binomial(n, p)"),
        ).arrange(RIGHT, buff=0.8)
        cards.to_edge(DOWN, buff=0.5)
        fit_to_frame(cards)

        with self.voiceover(
            text="The named distributions each come with a mean worth "
                 "remembering: a geometric with parameter p balances at one "
                 "over p, and a binomial with n trials balances at n times "
                 "p — results we'll lean on constantly."
        ):
            self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class VarianceDefinition(VoiceoverScene):
    """Beat: variance -- same mean, different spread; the definition."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Variance")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Two PMFs with the same mean (3): tight vs wide. Shown one at a
        # time (house rule), same fulcrum position marked on each.
        tight = [0.0, 0.0, 0.15, 0.70, 0.15]
        wide = [0.0, 0.25, 0.15, 0.20, 0.15, 0.25]
        # means: tight -> 2*.15 + 3*.7 + 4*.15 = 3.0
        #        wide  -> 1*.25 + 2*.15 + 3*.2 + 4*.15 + 5*.25 = 3.0

        chart_t, bars_t = make_pmf_chart(tight, x_label="x",
                                         y_label=r"p_X(x)", y_max=0.8)
        chart_t.scale(0.62).to_edge(DOWN, buff=0.5)
        chart_w, bars_w = make_pmf_chart(wide, x_label="x",
                                         y_label=r"p_X(x)", y_max=0.8)
        chart_w.scale(0.62).to_edge(DOWN, buff=0.5)

        def mean_marker(chart):
            axes = chart[0]
            tri = Triangle(color=ACCENT, fill_opacity=1).scale(0.12)
            tri.next_to(axes.c2p(3, 0), DOWN, buff=0.03)
            return tri

        tri_t = mean_marker(chart_t)
        tri_w = mean_marker(chart_w)
        mark_intended_overlap(chart_t, tri_t, reason="fulcrum under the axis")
        mark_intended_overlap(chart_w, tri_w, reason="fulcrum under the axis")

        cap_same = Text("same mean", font_size=CAPTION, color=MUTED)
        cap_diff = Text("different spread", font_size=CAPTION, color=MUTED)

        with self.voiceover(
            text="The mean says where a distribution sits. It says nothing "
                 "about how widely it spreads. These two PMFs balance at "
                 "exactly the same point — but one hugs its mean and the "
                 "other scatters. We need a second number."
        ):
            self.play(Create(chart_t[0]), Write(chart_t[1]),
                      Write(chart_t[2]), run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_t],
                                  lag_ratio=0.1), FadeIn(tri_t),
                      run_time=0.9)
            cap_same.next_to(title, DOWN, buff=0.35)
            self.play(FadeIn(cap_same), run_time=0.5)
            self.play(FadeOut(VGroup(chart_t, tri_t)), run_time=0.5)
            self.play(Create(chart_w[0]), Write(chart_w[1]),
                      Write(chart_w[2]), run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_w],
                                  lag_ratio=0.1), FadeIn(tri_w),
                      run_time=0.9)
            cap_diff.next_to(cap_same, DOWN, buff=0.2)
            self.play(FadeIn(cap_diff), run_time=0.5)

        defn = MathTex(
            variance("X"), "=",
            expectation(r"\left( X - \mathrm{E}[X] \right)^2"),
            font_size=BODY,
        )
        defn.next_to(cap_diff, DOWN, buff=0.35)
        fit_to_frame(defn)

        with self.voiceover(
            text="Measure each value's deviation from the mean, square it so "
                 "that left and right count alike, and take the expectation. "
                 "That is the variance: the expected squared deviation from "
                 "the mean. It is never negative, and it is large exactly "
                 "when mass sits far from the balance point."
        ):
            self.play(FadeOut(cap_same), run_time=0.3)
            self.play(Write(defn), run_time=1.4)
            self.play(defn[0].animate.set_color(ACCENT), run_time=0.5)
            self.play(LaggedStart(*[Indicate(b, scale_factor=1.06)
                                    for b in (bars_w[0], bars_w[-1])],
                                  lag_ratio=0.3), run_time=1.2)

        sigma = MathTex(r"\sigma = \sqrt{" + variance("X") + "}",
                        font_size=SMALL, color=MUTED)
        sigma.next_to(defn, DOWN, buff=0.25)

        with self.voiceover(
            text="Its square root is the standard deviation, sigma — the "
                 "spread in the same units as X itself."
        ):
            self.play(FadeIn(sigma), run_time=0.6)

        with self.voiceover(
            text="For a Bernoulli with parameter p, the variance works out "
                 "to p times one minus p — largest at one half, where the "
                 "outcome is most uncertain. And the Poisson is famous for "
                 "this: its variance equals its mean; both are lambda."
        ):
            self.play(FadeOut(VGroup(chart_w, tri_w, cap_diff)),
                      run_time=0.5)
            cards = VGroup(
                card(variance("X") + r"= p(1-p)", "Bernoulli(p)"),
                card(expectation("X") + "=" + variance("X")
                     + r"= \lambda", "Poisson"),
            ).arrange(RIGHT, buff=0.8)
            cards.to_edge(DOWN, buff=0.55)
            fit_to_frame(cards)
            self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class AffineRules(VoiceoverScene):
    """Beat: affine -- shift, scale, linearity, and the outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Affine Functions")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # One axes, three incarnations of the same distribution:
        # base X on {1..4}, shifted X+2 on {3..6}, scaled 2X on {2,4,6,8}.
        base = [0.0, 0.20, 0.40, 0.30, 0.10]           # mean 2.3
        shifted = [0.0] * 3 + [0.20, 0.40, 0.30, 0.10]  # mean 4.3
        scaled = [0.0, 0.0, 0.20, 0.0, 0.40, 0.0, 0.30, 0.0, 0.10]  # mean 4.6

        chart, bars = make_pmf_chart(base, x_max=9, x_label="x",
                                     y_label=r"p_X(x)", y_max=0.55)
        chart.scale(0.62).to_edge(DOWN, buff=0.5)
        axes = chart[0]

        def bars_for(values):
            # Unit width via c2p, NOT axes.x_axis.unit_size: unit_size is
            # frozen at construction, so after chart.scale() it is ~1.6x too
            # large and every transformed bar fattened -- a conservation-of-
            # mass violation on screen (2026-07-03 draft review, 5:52).
            unit_w = (axes.c2p(1, 0) - axes.c2p(0, 0))[0]
            grp = VGroup()
            for k, p in enumerate(values):
                if p <= 0:
                    continue
                height = axes.c2p(0, p)[1] - axes.c2p(0, 0)[1]
                rect = Rectangle(width=unit_w * 0.7, height=height,
                                 fill_color=BAR, fill_opacity=0.85,
                                 stroke_width=1, stroke_color=INK)
                rect.move_to(axes.c2p(k, 0), aligned_edge=DOWN)
                grp.add(rect)
            return grp

        def fulcrum_at(x):
            tri = Triangle(color=ACCENT, fill_opacity=1).scale(0.12)
            tri.next_to(axes.c2p(x, 0), DOWN, buff=0.03)
            return tri

        fulcrum = fulcrum_at(2.3)
        mark_intended_overlap(chart, fulcrum,
                              reason="fulcrum under the axis")

        y_def = MathTex("Y = aX + b", font_size=BODY, color=INK)
        y_def.next_to(title, DOWN, buff=0.4)

        with self.voiceover(
            text="Finally, the algebra. Take Y equals a X plus b — an affine "
                 "function: scale by a, shift by b. What happens to the mean "
                 "and the variance?"
        ):
            self.play(Write(y_def), run_time=0.9)
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), FadeIn(fulcrum),
                      run_time=0.9)

        rule_shift = MathTex(expectation("X + b"), "=",
                             expectation("X"), "+ b",
                             font_size=SMALL)
        rule_shift.next_to(y_def, DOWN, buff=0.35)

        with self.voiceover(
            text="Shift first. Slide the whole PMF right by b, and the "
                 "balance point slides with it: the mean of X plus b picks "
                 "up exactly b. The spread doesn't change at all — shifting "
                 "moves a distribution, it does not widen it."
        ):
            new_bars = bars_for(shifted)
            mark_intended_overlap(chart, new_bars,
                                  reason="bars ride the shared axes")
            self.play(Transform(bars, new_bars),
                      fulcrum.animate.next_to(axes.c2p(4.3, 0), DOWN,
                                              buff=0.03),
                      run_time=1.4)
            self.play(FadeIn(rule_shift), run_time=0.7)

        rules = MathTex(
            expectation("aX + b"), "=", "a\\,", expectation("X"), "+ b,",
            r"\quad", variance("aX + b"), "=", "a^2\\,", variance("X"),
            font_size=SMALL,
        )
        rules.move_to(rule_shift)
        fit_to_frame(rules)

        with self.voiceover(
            text="Now scale by a. The balance point scales to a times the "
                 "mean. But deviations from the mean scale by a too, and the "
                 "variance squares them — so the variance picks up a "
                 "squared. The mean of a X plus b is a times the mean plus "
                 "b; the variance of a X plus b is a squared times the "
                 "variance. The shift b is gone entirely."
        ):
            back_bars = bars_for(base)
            mark_intended_overlap(chart, back_bars,
                                  reason="bars ride the shared axes")
            self.play(Transform(bars, back_bars),
                      fulcrum.animate.next_to(axes.c2p(2.3, 0), DOWN,
                                              buff=0.03),
                      run_time=0.8)
            scaled_bars = bars_for(scaled)
            mark_intended_overlap(chart, scaled_bars,
                                  reason="bars ride the shared axes")
            self.play(Transform(bars, scaled_bars),
                      fulcrum.animate.next_to(axes.c2p(4.6, 0), DOWN,
                                              buff=0.03),
                      run_time=1.4)
            self.play(FadeOut(rule_shift), run_time=0.3)
            self.play(Write(rules), run_time=1.4)
            self.play(rules[6].animate.set_color(ACCENT), run_time=0.5)

        linearity = MathTex(
            expectation("a\\,g(X) + h(X)"), "=",
            "a\\,", expectation("g(X)"), "+", expectation("h(X)"),
            font_size=SMALL, color=MUTED,
        )
        linearity.next_to(rules, DOWN, buff=0.3)
        fit_to_frame(linearity)

        with self.voiceover(
            text="Behind the first rule is something more general: "
                 "expectation is linear. The expectation of a sum of "
                 "functions of X is the sum of their expectations, constants "
                 "slide out — no independence, no fine print."
        ):
            self.play(FadeIn(linearity), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Average g(X) straight from the PMF",
             "the mean and the variance"],
            next_title="Moments",
        )

        # Narration mirrors the card and stops at "the mean and the
        # variance"; the affine response and the moments tease live on
        # screen only (2026-07-03 draft review).
        with self.voiceover(
            text="The key idea of this video: average a function through the "
                 "PMF directly — and its two star cases, the mean and the "
                 "variance."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
