# derived_from: content/20-moments-script.md
# derived_from_sha256: fcb18452629631d69435ccc09d271098519c950c2de74af4fef6e94847ecb1d7
"""Chapter 6, Video 3 -- Moments.

Source notes : discrete_expectations.tex (Section 6.3) -- the ladder of
               moments E[X^n], the two-moment variance identity, the uniform
               worked example, and central moments.
Script        : content/20-moments-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/moments.py ChapterOverview
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
    section_title,
    make_pmf_chart,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    die_face,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


def result_card(tex: str, label: str | None = None) -> VGroup:
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
            "Moments",
            ["Climb the ladder of moments - and compute variances",
             "the easy way, from the first two moments."],
            kicker="Chapter 6  ·  Meeting Expectations",
        )
        tag = progress_tag(3, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The ladder of moments", font_size=BODY, color=INK),
            Text("2.  The identity at work", font_size=BODY, color=INK),
            Text("3.  Central moments", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="We now have two summaries of a random variable: the mean, "
                 "where its PMF balances, and the variance, how far it "
                 "spreads. This video completes the family."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(outline)

        with self.voiceover(
            text="The moments of a random variable are the expectations of "
                 "its powers, and they come with the most useful "
                 "computational identity in the chapter: the variance from "
                 "the first two moments."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We'll prove it in three lines, put it to work on a uniform "
                 "random variable,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and close with the central moments — the quantities behind "
                 "skewness and kurtosis."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MomentsDefinition(VoiceoverScene):
    """Beat: moments -- the ladder E[X^n], with the mean as its first rung."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The nth Moment")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        formula = MathTex(
            expectation("X^n"), "=",
            r"\sum_{x \in X(\Omega)} x^n \, p_X(x)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(formula)

        # Both columns ride slightly high so the composition breathes and a
        # margin stays clear beneath the chart (2026-07-03 draft review,
        # 1:17).
        values = [0.0, 0.10, 0.20, 0.30, 0.25, 0.15]
        chart, bars = make_pmf_chart(values, x_label="x", y_label=r"p_X(x)")
        chart.scale(0.6)
        chart.move_to(LEFT * 3.2 + DOWN * 1.1)

        chips = VGroup(
            MathTex(expectation("X"), font_size=SMALL, color=INK),
            MathTex(expectation("X^2"), font_size=SMALL, color=INK),
            MathTex(expectation("X^3"), font_size=SMALL, color=INK),
            MathTex(r"\vdots", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.35)
        chips.move_to(RIGHT * 3.4 + DOWN * 1.1)

        with self.voiceover(
            text="The definition is last video's formula with the simplest "
                 "possible family of functions."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=0.9)

        with self.voiceover(
            text="Take g of x equals x to the n. The n-th moment of X is the "
                 "expectation of X to the n: sum x to the n times p sub X of "
                 "x. One PMF, a whole ladder of numbers — first moment, "
                 "second moment, third, and so on, each extracting a "
                 "different feature from the same bars."
        ):
            self.play(Write(formula), run_time=1.4)
            self.play(formula[0].animate.set_color(ACCENT), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.3)
                                    for c in chips], lag_ratio=0.25),
                      run_time=1.6)

        first_note = Text("the mean is the first moment",
                          font_size=CAPTION, color=MUTED)
        first_note.next_to(chips, DOWN, buff=0.35)

        with self.voiceover(
            text="The first rung is an old friend: the first moment is "
                 "exactly the mean. The higher rungs are new, and the second "
                 "one is about to earn its keep."
        ):
            self.play(formula[0].animate.set_color(INK), run_time=0.3)
            self.play(Indicate(chips[0], color=ACCENT, scale_factor=1.15),
                      run_time=0.9)
            self.play(FadeIn(first_note), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class VarianceFromMoments(VoiceoverScene):
    """Beat: variance-formula -- the three-line derivation of the identity."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Variance from Two Moments")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        line1 = MathTex(
            variance("X"), "=",
            expectation(r"\left( X - \mathrm{E}[X] \right)^2"),
            font_size=BODY,
        )
        line2 = MathTex(
            "=", expectation("X^2"),
            "-", r"2\,\mathrm{E}[X]\cdot\mathrm{E}[X]",
            "+", r"\left(\mathrm{E}[X]\right)^2",
            font_size=BODY,
        )
        derivation = VGroup(line1, line2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35)
        derivation.next_to(title, DOWN, buff=0.5)
        fit_to_frame(derivation)

        with self.voiceover(
            text="Here is the payoff. Start from the definition of the "
                 "variance: the expected squared deviation from the mean."
        ):
            self.play(Write(line1), run_time=1.2)

        with self.voiceover(
            text="Expand the square inside: x squared, minus two x times the "
                 "mean, plus the mean squared. Now use linearity — last "
                 "video's rule — to split the sum into three pieces."
        ):
            self.play(Write(line2), run_time=1.6)

        combine_note = MathTex(
            r"-2\left(\mathrm{E}[X]\right)^2 + \left(\mathrm{E}[X]\right)^2"
            r"= -\left(\mathrm{E}[X]\right)^2",
            font_size=SMALL, color=MUTED,
        )
        combine_note.next_to(derivation, DOWN, buff=0.4)

        identity = MathTex(
            variance("X"), "=", expectation("X^2"), "-",
            r"\left(\mathrm{E}[X]\right)^2",
            font_size=SECTION,
        )
        identity.next_to(combine_note, DOWN, buff=0.5)
        fit_to_frame(identity)

        with self.voiceover(
            text="The first piece is the second moment. The middle piece is "
                 "minus two times the mean, times the mean again. The last "
                 "piece is the mean squared, times masses that sum to one. "
                 "Minus two mean-squared plus mean-squared: the cross terms "
                 "collapse, and what survives is clean — the variance is the "
                 "second moment minus the square of the first."
        ):
            self.play(Indicate(line2[3], scale_factor=1.08),
                      Indicate(line2[5], scale_factor=1.08), run_time=1.2)
            self.play(FadeIn(combine_note), run_time=0.8)
            self.play(Write(identity), run_time=1.4)
            self.play(identity.animate.set_color(ACCENT), run_time=0.5)

        callback = result_card(
            expectation("X^2") + r"= \lambda^2 + \lambda",
            "Poisson: read the identity backwards",
        )
        callback.to_edge(DOWN, buff=0.8)
        fit_to_frame(callback)

        with self.voiceover(
            text="A quick dividend: last video the Poisson had mean lambda "
                 "and variance lambda. Read the identity backwards and its "
                 "second moment comes free — lambda squared plus lambda. No "
                 "new sum required."
        ):
            self.play(FadeIn(callback, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UniformExample(VoiceoverScene):
    """Beat: uniform -- the identity saving real work on a flat PMF."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Worked Example: the Uniform PMF")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        values = [0.0] + [1 / 6] * 6
        chart, bars = make_pmf_chart(values, x_label="k", y_label=r"p_X(k)",
                                     y_max=0.3)
        chart.scale(0.62).to_edge(DOWN, buff=0.8)

        mean_line = MathTex(
            r"p_X(k) = \tfrac{1}{n},\quad", expectation("X"),
            r"= \tfrac{n+1}{2}",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(mean_line)

        with self.voiceover(
            text="Let's see the identity save real work. Take X uniform on "
                 "one through n: a flat PMF, mass one over n everywhere. Its "
                 "mean is the midpoint, n plus one over two. Computing the "
                 "variance from the definition would mean summing squared "
                 "deviations from that midpoint — messy."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=0.9)
            self.play(Write(mean_line), run_time=1.2)

        second = MathTex(
            expectation("X^2"),
            r"= \frac{1}{n}\sum_{k=1}^{n} k^2 = \frac{(n+1)(2n+1)}{6}",
            font_size=SMALL,
        ).next_to(mean_line, DOWN, buff=0.3)
        fit_to_frame(second)

        with self.voiceover(
            text="The identity asks for something easier: the second moment "
                 "is one over n times the sum of the first n squares, and "
                 "that sum is a calculus classic — n times n plus one times "
                 "two n plus one, over six. Subtract the square of the mean."
        ):
            self.play(Write(second), run_time=1.6)

        result = MathTex(
            variance("X"), r"= \frac{n^2 - 1}{12}",
            font_size=BODY, color=ACCENT,
        )
        die_card = VGroup(
            die_face(6, size=0.55),
            MathTex(r"n = 6:\ \tfrac{35}{12}", font_size=SMALL, color=MUTED),
        ).arrange(RIGHT, buff=0.35)
        # Result and the die sanity check share one row so nothing dips into
        # the chart's lane below.
        result_row = VGroup(result, die_card).arrange(RIGHT, buff=0.8)
        result_row.next_to(second, DOWN, buff=0.35)
        fit_to_frame(result_row)

        with self.voiceover(
            text="The algebra telescopes to n squared minus one, over "
                 "twelve. Sanity check it on the fair die, n equals six: "
                 "thirty-five over twelve, just under three — matching the "
                 "spread you'd eyeball on its flat PMF. Two standard sums, "
                 "no centered mess."
        ):
            self.play(Write(result), run_time=1.0)
            self.play(FadeIn(die_card, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CentralMoments(VoiceoverScene):
    """Beat: central -- centering, the portrait gallery, and the outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Central Moments")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        centering = MathTex(
            expectation(r"\left( X - \mathrm{E}[X] \right)^k"),
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        center_note = Text("center first, then raise to the power",
                           font_size=CAPTION, color=MUTED)
        center_note.next_to(centering, DOWN, buff=0.22)

        # Centering picture: bars slide so the balance point lands on zero.
        # No y-axis numbers: the centered PMF peaks at x = 0, exactly where
        # the y-axis lives, so tick labels would hide behind the center bar
        # -- and the y-scale carries no information in this illustration.
        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[0, 0.4, 0.1],
            x_length=9.0,
            y_length=2.6,
            axis_config={"include_numbers": True, "font_size": 30},
            y_axis_config={"include_numbers": False},
            tips=False,
        ).to_edge(DOWN, buff=0.8)
        fit_to_frame(axes)

        def bars_at(positions_masses):
            unit_w = (axes.c2p(1, 0) - axes.c2p(0, 0))[0]
            grp = VGroup()
            for k, p in positions_masses:
                height = axes.c2p(0, p)[1] - axes.c2p(0, 0)[1]
                rect = Rectangle(width=unit_w * 0.7, height=height,
                                 fill_color=BAR, fill_opacity=0.85,
                                 stroke_width=1, stroke_color=INK)
                rect.move_to(axes.c2p(k, 0), aligned_edge=DOWN)
                grp.add(rect)
            return grp

        # Mean 3 by construction: .15+.4+.9+.8+.75 = 3.0
        base = [(1, 0.15), (2, 0.20), (3, 0.30), (4, 0.20), (5, 0.15)]
        centered = [(k - 3, p) for k, p in base]
        bars = bars_at(base)

        def fulcrum_at(x):
            tri = Triangle(color=ACCENT, fill_opacity=1).scale(0.12)
            tri.next_to(axes.c2p(x, 0), DOWN, buff=0.03)
            return tri

        fulcrum = fulcrum_at(3)
        mark_intended_overlap(axes, bars, fulcrum,
                              reason="bars and fulcrum ride the shared axes")

        with self.voiceover(
            text="One refinement completes the picture. Instead of powers of "
                 "X, take powers of X minus its mean — center first, then "
                 "raise. These are the central moments, and we already know "
                 "the second one: it is the variance itself."
        ):
            self.play(Write(centering), FadeIn(center_note), run_time=1.2)
            self.play(Create(axes), run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), FadeIn(fulcrum),
                      run_time=0.9)
            new_bars = bars_at(centered)
            mark_intended_overlap(axes, new_bars,
                                  reason="bars and fulcrum ride the shared axes")
            self.play(Transform(bars, new_bars),
                      fulcrum.animate.next_to(axes.c2p(0, 0), DOWN,
                                              buff=0.03),
                      run_time=1.4)

        # Portraits: one at a time (house rule), captions in the same slot.
        # Each portrait is a separate voiceover block so the picture on
        # screen is the one being spoken about (2026-07-03 draft review,
        # 3:50).
        skew_vals = [0.0, 0.32, 0.26, 0.18, 0.12, 0.07, 0.05]
        skew_chart, skew_bars = make_pmf_chart(skew_vals, x_label="x",
                                               y_label=r"p_X(x)", y_max=0.4)
        skew_chart.scale(0.55).to_edge(DOWN, buff=0.8)
        skew_cap = Text("skewness: asymmetry", font_size=CAPTION, color=MUTED)

        kurt_vals = [0.0, 0.05, 0.06, 0.10, 0.58, 0.10, 0.06, 0.05]
        kurt_chart, kurt_bars = make_pmf_chart(kurt_vals, x_label="x",
                                               y_label=r"p_X(x)", y_max=0.7)
        kurt_chart.scale(0.55).to_edge(DOWN, buff=0.8)
        kurt_cap = Text("kurtosis: tail weight", font_size=CAPTION,
                        color=MUTED)

        with self.voiceover(
            text="The higher central moments each capture a different trait. "
                 "The third, standardized, is the skewness: it is zero for a "
                 "symmetric PMF and picks up sign when one tail stretches "
                 "farther than the other."
        ):
            self.play(FadeOut(VGroup(bars, fulcrum, axes)), run_time=0.5)
            skew_cap.next_to(center_note, DOWN, buff=0.3)
            self.play(FadeIn(skew_chart), FadeIn(skew_cap), run_time=0.9)

        with self.voiceover(
            text="The fourth is behind the kurtosis, which asks whether the "
                 "spread comes from rare, extreme deviations or from "
                 "frequent modest ones."
        ):
            self.play(FadeOut(skew_chart), FadeOut(skew_cap), run_time=0.5)
            kurt_cap.next_to(center_note, DOWN, buff=0.3)
            self.play(FadeIn(kurt_chart), FadeIn(kurt_cap), run_time=0.9)

        with self.voiceover(
            text="We won't compute these here — they belong to statistics — "
                 "but you will meet them, and now you know what they measure."
        ):
            self.wait(0.3)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The variance is the second moment",
             "minus the square of the first."],
            next_title="Multiple Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video — and the tool to keep: the "
                 "variance is the second moment minus the square of the "
                 "first. That closes our summary toolkit for a single random "
                 "variable. Coming up next: what changes when we watch "
                 "several random variables at once."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
