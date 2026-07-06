# derived_from: content/27-pdfs-expectation-script.md
# derived_from_sha256: 26c22a93f50545ae3136eca7edc067c60db8407e4e7c6bccede8f0311b943f12
"""Chapter 8, Video 2 -- Densities and Expectation.

Source notes : 27-pdfs-expectation.tex (Sections 8.2-8.3) -- the probability
               density function, probabilities as areas, the density axioms,
               expectation as an integral, the tail formula, and the
               dartboard example.
Script        : content/27-pdfs-expectation-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/pdfs_expectation.py ChapterOverview
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
    pr,
    expectation,
    variance,
    section_title,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    make_pmf_chart,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


# The running example pair: a smooth progression CDF and its bump of a density
# (the book's own Section 8.1 figure -- F(x) = 1 - e^{-x^2/4}).
def F_ramp(x):
    return 1.0 - np.exp(-x * x / 4.0)


def f_bump(x):
    return (x / 2.0) * np.exp(-x * x / 4.0)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Densities and Expectation",
            ["Differentiate the CDF into the density, read probabilities",
             "as areas, and rebuild expectation as an integral."],
            kicker="Chapter 8  ·  Continuous Random Variables",
        )
        tag = progress_tag(2, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The probability density function",
                 font_size=BODY, color=INK),
            Text("2.  Probabilities as areas", font_size=BODY, color=INK),
            Text("3.  Expectation and the tail formula",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="The bridge is in place: the cumulative distribution "
                 "function, one function that describes any random variable "
                 "— staircases for the discrete, smooth progressions for the "
                 "continuous."
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
            text="In this video we differentiate that smooth function and meet the "
                 "density, the working object of the continuous world for "
                 "the rest of the course,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="read the probabilities of intervals as areas under it, "
                 "and see why single exact points carry no probability at "
                 "all,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then rebuild expectation on integrals, where the mean and "
                 "the variance survive word for word, and finish with a "
                 "trick that computes a mean from tail probabilities alone."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DensityDefinition(VoiceoverScene):
    """Beat: density -- CDF above, density below, slope-to-area duality."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Probability Density Function")
        fit_to_frame(title)

        # Left column: the CDF stacked over its derivative, sharing an
        # x-scale (concept map: slope-to-area duality).
        ax_F = Axes(
            x_range=[0, 4, 1], y_range=[0, 1.1, 1],
            x_length=5.4, y_length=1.9,
            axis_config={"include_numbers": False}, tips=False,
        ).move_to(LEFT * 3.3 + UP * 1.45)
        F_curve = ax_F.plot(F_ramp, x_range=[0, 4], color=INK)
        F_lab = MathTex(r"F_X(x)", font_size=SMALL, color=MUTED)
        F_lab.next_to(ax_F.c2p(4, 1), RIGHT, buff=0.18)

        ax_f = Axes(
            x_range=[0, 4, 1], y_range=[0, 0.55, 1],
            x_length=5.4, y_length=1.9,
            axis_config={"include_numbers": False}, tips=False,
        ).move_to(LEFT * 3.3 + DOWN * 1.35)
        f_curve = ax_f.plot(f_bump, x_range=[0, 4], color=INK)
        f_lab = MathTex(r"f_X(x)", font_size=SMALL, color=MUTED)
        f_lab.next_to(ax_f.c2p(1.5, 0.46), UP, buff=0.15)

        with self.voiceover(
            text="Take a continuous random variable, one whose CDF is a "
                 "smooth function, differentiable almost everywhere."
        ):
            self.play(Write(title), run_time=0.8)
            self.play(title.animate.to_edge(UP), run_time=0.6)
            self.play(Create(ax_F), run_time=0.7)
            self.play(Create(F_curve), FadeIn(F_lab), run_time=1.0)

        def_eq = MathTex(
            r"f_X(x)", "=", r"\frac{dF_X}{dx}(x)",
            font_size=BODY, color=ACCENT,
        ).move_to(RIGHT * 3.4 + UP * 1.8)
        fit_to_frame(def_eq)

        with self.voiceover(
            text="Its derivative gets a name: the probability density "
                 "function, f of x, the slope of the CDF at each point. "
                 "Where the function climbs steeply, the density stands "
                 "tall; where the function flattens out, the density falls "
                 "back toward zero."
        ):
            self.play(Write(def_eq), run_time=1.2)

        ftc_eq = MathTex(
            r"F_X(x)", "=", r"\int_{-\infty}^{x} f_X(u)\,du",
            font_size=BODY, color=ACCENT,
        ).next_to(def_eq, DOWN, buff=0.5)
        fit_to_frame(ftc_eq)

        with self.voiceover(
            text="And the fundamental theorem of calculus runs the "
                 "definition backwards: integrate the density from minus "
                 "infinity up to x, and the CDF reappears. Differentiate to "
                 "go one way, integrate to come back."
        ):
            self.play(def_eq.animate.set_color(INK), run_time=0.4)
            self.play(Write(ftc_eq), run_time=1.2)

        with self.voiceover(
            text="Watch the two functions together: the CDF above, its "
                 "density below."
        ):
            self.play(ftc_eq.animate.set_color(INK), run_time=0.4)
            self.play(Create(ax_f), run_time=0.7)
            self.play(Create(f_curve), FadeIn(f_lab), run_time=0.9)

        # The moving x: shaded area under f up to x tracks the CDF height.
        x_t = ValueTracker(0.6)
        area = always_redraw(lambda: ax_f.get_area(
            f_curve, x_range=(0, x_t.get_value()),
            color=BAR, opacity=0.45, stroke_width=0))
        marker = always_redraw(lambda: DashedLine(
            ax_F.c2p(x_t.get_value(), 0),
            ax_F.c2p(x_t.get_value(), F_ramp(x_t.get_value())),
            color=ACCENT, stroke_width=2.5, dash_length=0.1))
        cdf_dot = always_redraw(lambda: Dot(
            ax_F.c2p(x_t.get_value(), F_ramp(x_t.get_value())),
            radius=0.06, color=ACCENT))

        with self.voiceover(
            text="Slide a point x along the axis, and the shaded area under "
                 "the density, up to x, always matches the height of the "
                 "CDF. Height above, area below — the same information, "
                 "stored two ways."
        ) as tracker:
            self.add(area, marker, cdf_dot)
            self.play(x_t.animate.set_value(3.3), rate_func=linear,
                      run_time=max(tracker.duration - 1.5, 2.5))

        iv1 = MathTex(
            pr(r"x_1 < X \le x_2"), "=", r"F_X(x_2) - F_X(x_1)",
            font_size=SMALL, color=INK,
        )
        iv2 = MathTex(
            r"= \int_{x_1}^{x_2} f_X(u)\,du",
            font_size=SMALL, color=ACCENT,
        )
        iv_group = VGroup(iv1, iv2).arrange(DOWN, aligned_edge=LEFT,
                                            buff=0.28)
        iv2.shift(RIGHT * 0.7)
        iv_group.next_to(ftc_eq, DOWN, buff=0.7)
        fit_to_frame(iv_group)

        with self.voiceover(
            text="That reading turns last video's interval formula into a "
                 "picture. The probability that X lands between x one and x "
                 "two is the CDF difference,"
        ):
            for m in (area, marker, cdf_dot):
                m.clear_updaters()
            self.play(FadeOut(area), FadeOut(marker), FadeOut(cdf_dot),
                      run_time=0.5)
            self.play(Write(iv1), run_time=1.2)

        x1, x2 = 1.2, 2.4
        strip = ax_f.get_area(f_curve, x_range=(x1, x2),
                              color=BAR, opacity=0.55, stroke_width=0)
        e1 = DashedLine(ax_f.c2p(x1, 0), ax_f.c2p(x1, f_bump(x1)),
                        color=MUTED, stroke_width=2, dash_length=0.08)
        e2 = DashedLine(ax_f.c2p(x2, 0), ax_f.c2p(x2, f_bump(x2)),
                        color=MUTED, stroke_width=2, dash_length=0.08)
        l1 = MathTex("x_1", font_size=CAPTION, color=MUTED)
        l1.next_to(ax_f.c2p(x1, 0), DOWN, buff=0.22)
        l2 = MathTex("x_2", font_size=CAPTION, color=MUTED)
        l2.next_to(ax_f.c2p(x2, 0), DOWN, buff=0.22)

        with self.voiceover(
            text="which is exactly the integral of the density across the "
                 "interval. Probabilities of intervals are areas under the "
                 "density curve. Where the density runs tall, the variable "
                 "lands there often; where it hugs zero, it almost never "
                 "does. The density spreads probability along the line the "
                 "way the mass function once stacked it on points."
        ):
            self.play(FadeIn(strip), Create(e1), Create(e2),
                      FadeIn(l1), FadeIn(l2), run_time=0.9)
            self.play(Write(iv2), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DensityProperties(VoiceoverScene):
    """Beat: properties -- massless points, density-not-probability, axioms."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("What a Density Must Satisfy")
        fit_to_frame(title)

        ax = Axes(
            x_range=[0, 6, 1], y_range=[0, 2.6, 1],
            x_length=6.2, y_length=3.2,
            axis_config={"include_numbers": False}, tips=False,
        ).move_to(LEFT * 3.0 + DOWN * 0.55)

        def f_wide(x):
            return 0.85 * np.exp(-((x - 2.6) ** 2) / (2 * 1.1 ** 2))

        def f_spike(x):
            return 2.3 * np.exp(-((x - 2.6) ** 2) / (2 * 0.16 ** 2))

        curve = ax.plot(f_wide, x_range=[0, 6], color=INK)

        with self.voiceover(
            text="The area picture answers a natural question with a "
                 "surprise. What is the probability that X hits one exact "
                 "value?"
        ):
            self.play(Write(title), run_time=0.8)
            self.play(title.animate.to_edge(UP), run_time=0.6)
            self.play(Create(ax), run_time=0.6)
            self.play(Create(curve), run_time=0.9)

        x1, x2 = 3.1, 3.9
        strip = ax.get_area(curve, x_range=(x1, x2),
                            color=BAR, opacity=0.55, stroke_width=0)
        l1 = MathTex("x_1", font_size=CAPTION, color=MUTED)
        l1.next_to(ax.c2p(x1, 0), DOWN, buff=0.22)
        l2 = MathTex("x_2", font_size=CAPTION, color=MUTED)
        l2.next_to(ax.c2p(x2, 0), DOWN, buff=0.22)

        with self.voiceover(
            text="Take a strip under the density, from x one up to x two,"
        ):
            self.play(FadeIn(strip), FadeIn(l1), FadeIn(l2), run_time=0.8)

        sliver = ax.get_area(curve, x_range=(3.78, x2),
                             color=BAR, opacity=0.55, stroke_width=0)

        with self.voiceover(
            text="and slide x one upward. The strip narrows, its area "
                 "drains away,"
        ):
            self.play(Transform(strip, sliver), FadeOut(l1), run_time=1.2)

        zero_eq = MathTex(pr("X = x"), "=", "0",
                          font_size=BODY, color=ACCENT)
        zero_eq.move_to(RIGHT * 3.4 + UP * 1.7)
        fit_to_frame(zero_eq)

        with self.voiceover(
            text="and in the limit nothing is left: for a continuous random "
                 "variable, the probability that X equals any single point "
                 "is exactly zero."
        ):
            self.play(FadeOut(strip), FadeOut(l2), run_time=0.7)
            self.play(Write(zero_eq), run_time=1.0)

        ends = VGroup(
            MathTex(pr(r"x_1 < X < x_2"), "=", pr(r"x_1 \le X < x_2"),
                    font_size=CAPTION, color=MUTED),
            MathTex("=", pr(r"x_1 < X \le x_2"), "=",
                    pr(r"x_1 \le X \le x_2"),
                    font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.22)
        cap = Text("endpoints never matter", font_size=CAPTION, color=MUTED)
        ends_block = VGroup(ends, cap).arrange(DOWN, buff=0.3)
        ends_block.next_to(zero_eq, DOWN, buff=0.55)
        fit_to_frame(ends_block)

        with self.voiceover(
            text="A useful corollary follows at once: open or closed, "
                 "endpoints never matter — all four interval probabilities "
                 "agree."
        ):
            self.play(zero_eq.animate.set_color(INK), run_time=0.4)
            self.play(FadeIn(ends[0], shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(ends[1], shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(cap), run_time=0.5)

        warn = MathTex(r"f_X(x)", r"\neq", pr("X = x"),
                       font_size=BODY, color=ACCENT)
        warn.move_to(RIGHT * 3.4 + UP * 1.5)
        fit_to_frame(warn)
        warn_cap = Text("probability per unit length",
                        font_size=CAPTION, color=MUTED)
        warn_cap.next_to(warn, DOWN, buff=0.3)

        with self.voiceover(
            text="And a warning worth its own frame: f of x is not the "
                 "probability that X equals x. It is a density, probability "
                 "per unit length."
        ):
            self.play(FadeOut(zero_eq), FadeOut(ends_block), run_time=0.5)
            self.play(Write(warn), run_time=1.0)
            self.play(FadeIn(warn_cap), run_time=0.5)

        spike = ax.plot(f_spike, x_range=[0, 6], color=INK)
        one_line = DashedLine(ax.c2p(0, 1), ax.c2p(6, 1),
                              color=MUTED, stroke_width=2, dash_length=0.1)
        one_lab = MathTex("1", font_size=CAPTION, color=MUTED)
        one_lab.next_to(ax.c2p(0, 1), LEFT, buff=0.18)
        tall_cap = Text("a density can exceed one",
                        font_size=CAPTION, color=MUTED)
        tall_cap.next_to(ax.c2p(3, 0), DOWN, buff=0.55)

        with self.voiceover(
            text="A tall, narrow density can rise far above one: squeeze "
                 "the same unit of area onto a thinner base, and the height "
                 "must grow. Only areas are probabilities, never heights."
        ):
            self.play(warn.animate.set_color(INK), run_time=0.4)
            self.play(Create(one_line), FadeIn(one_lab), run_time=0.6)
            self.play(Transform(curve, spike), run_time=1.2)
            self.play(FadeIn(tall_cap), run_time=0.5)

        ax1_eq = MathTex(r"\int_{-\infty}^{\infty} f_X(u)\,du", "=", "1",
                         font_size=SMALL, color=INK)
        ax1_eq.move_to(RIGHT * 3.4 + UP * 1.5)
        area_full = ax.get_area(spike, x_range=(0.5, 4.7),
                                color=BAR, opacity=0.35, stroke_width=0)

        with self.voiceover(
            text="The axioms survive the translation. The variable lands "
                 "somewhere, so the total area under the density is one — "
                 "normalization, in its new clothes."
        ):
            self.play(FadeOut(warn), FadeOut(warn_cap), run_time=0.5)
            self.play(FadeIn(area_full), run_time=0.7)
            self.play(Write(ax1_eq), run_time=0.9)

        ax2_eq = MathTex(r"f_X(x)", r"\ge", "0",
                         font_size=SMALL, color=INK)
        ax2_eq.next_to(ax1_eq, DOWN, buff=0.5)

        with self.voiceover(
            text="Probabilities are nonnegative, so the density never dips "
                 "below zero."
        ):
            self.play(Write(ax2_eq), run_time=0.8)

        ax3_eq = MathTex(pr(r"X \in S"), "=", r"\int_S f_X(u)\,du",
                         font_size=SMALL, color=ACCENT)
        ax3_eq.next_to(ax2_eq, DOWN, buff=0.5)
        fit_to_frame(ax3_eq)

        with self.voiceover(
            text="And for any admissible set S, the probability that X "
                 "falls in S is the integral of the density over S. Two "
                 "conditions, nonnegative and total area one, and a "
                 "function essentially qualifies as a density — that is all it takes to "
                 "specify a continuous model."
        ):
            self.play(Write(ax3_eq), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExpectationIntegral(VoiceoverScene):
    """Beat: expectation -- sum morphs to integral, then the tail formula."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Expectation as an Integral")
        fit_to_frame(title)

        with self.voiceover(
            text="Expectation crosses the bridge the same way."
        ):
            self.play(Write(title), run_time=0.8)
            self.play(title.animate.to_edge(UP), run_time=0.6)

        eq_d = MathTex(
            expectation("g(X)"), "=", r"\sum_{x} g(x)\, p_X(x)",
            font_size=BODY, color=INK,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(eq_d)

        values = [0.10, 0.20, 0.30, 0.25, 0.15]
        chart, bars = make_pmf_chart(values, x_label="x",
                                     y_label=r"p_X(x)")
        axes_c = chart[0]
        # Review 2026-07-04, 4:09: a "0" tick label on the x-axis (Axes
        # suppresses the origin number by default), created pre-scale so it
        # rides along with the chart's transforms.
        zero_tick = axes_c.x_axis.get_number_mobject(0)
        # Review 2026-07-04, 4:14: the y-axis name will morph p_X -> f_X
        # when the bars melt into a density; build the target pre-scale too.
        f_ylab = axes_c.get_y_axis_label(MathTex(r"f_X(x)", font_size=BODY))
        chart.add(zero_tick, f_ylab)
        chart.scale(0.55)
        # Review 2026-07-04, 4:09: ride higher on the left side of the frame.
        chart.to_edge(DOWN, buff=1.2)
        chart.move_to([-3.0, chart.get_center()[1], 0])
        y_tick_first = axes_c.y_axis.numbers[0]  # the "0.09" label

        with self.voiceover(
            text="In chapter six, the expected value of g of X weighed each "
                 "value by its probability mass and summed."
        ):
            self.play(Write(eq_d), run_time=1.1)
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            # Review 2026-07-04, 4:09: as the bars land, fade the first
            # y-tick label (the k=0 bar overlapped it) and add the "0" tick.
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.12),
                      y_tick_first.animate.set_opacity(0),
                      FadeIn(zero_tick), run_time=0.9)

        eq_i = MathTex(
            expectation("g(X)"), "=",
            r"\int_{-\infty}^{\infty} g(u)\, f_X(u)\,du",
            font_size=BODY, color=INK,
        ).move_to(eq_d)
        fit_to_frame(eq_i)

        # Review 2026-07-04, 4:14: the density extends LEFT past 0 — the
        # viewer must not conclude densities live only on the positive axis.
        smooth = axes_c.plot(
            lambda x: 0.30 * np.exp(-((x - 2.2) ** 2) / 2.2),
            x_range=[-1, 5], color=INK)
        melt = axes_c.get_area(smooth, x_range=(-1, 5),
                               color=BAR, opacity=0.5, stroke_width=0)

        with self.voiceover(
            text="Replace the sum by an integral and the mass by density "
                 "times length, and the sentence survives word for word: "
                 "the expectation of g of X is the integral of g times the "
                 "density. Every tool from that chapter rides along for "
                 "free."
        ):
            self.play(TransformMatchingTex(eq_d, eq_i), run_time=1.2)
            self.play(eq_i.animate.set_color(ACCENT), run_time=0.4)
            # Review 2026-07-04, 4:14: y-axis name morphs p_X(x) -> f_X(x)
            # at the same moment the bars melt into the curve.
            self.play(ReplacementTransform(bars, melt), Create(smooth),
                      Transform(chart[2], f_ylab),
                      run_time=1.2)

        mean_eq = MathTex(
            expectation("X"), "=", r"\int_{-\infty}^{\infty} u\, f_X(u)\,du",
            font_size=SMALL, color=INK,
        ).move_to(RIGHT * 3.4 + DOWN * 0.3)
        fit_to_frame(mean_eq)

        with self.voiceover(
            text="Set g to the identity and the mean appears: the integral "
                 "of u times f of u."
        ):
            self.play(eq_i.animate.set_color(INK), run_time=0.4)
            self.play(Write(mean_eq), run_time=1.0)

        var_eq = MathTex(
            variance("X"), "=",
            expectation(r"(X - " + expectation("X") + r")^2"),
            font_size=SMALL, color=INK,
        ).next_to(mean_eq, DOWN, buff=0.45)
        fit_to_frame(var_eq)

        with self.voiceover(
            text="The variance is the expected squared distance from the "
                 "mean, exactly as before,"
        ):
            self.play(Write(var_eq), run_time=1.0)

        short_eq = MathTex(
            variance("X"), "=",
            expectation("X^2") + r" - \left(" + expectation("X")
            + r"\right)^2",
            font_size=SMALL, color=ACCENT,
        ).next_to(var_eq, DOWN, buff=0.45)
        fit_to_frame(short_eq)

        with self.voiceover(
            text="and the shortcut still holds: the mean of the square, "
                 "minus the square of the mean."
        ):
            self.play(Write(short_eq), run_time=1.0)

        tail_eq = MathTex(
            expectation("X"), "=", r"\int_0^{\infty} " + pr("X > x")
            + r"\,dx",
            font_size=BODY, color=ACCENT,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(tail_eq)

        with self.voiceover(
            text="But the continuous world offers one genuinely new tool. "
                 "For a nonnegative random variable with finite mean, the "
                 "mean is the integral of the tail: integrate the "
                 "probability that X exceeds x, from zero to infinity — a "
                 "mean computed without ever touching the density."
        ):
            self.play(*[FadeOut(m) for m in self.mobjects
                        if m is not title], run_time=0.6)
            self.play(Write(tail_eq), run_time=1.3)

        # The order-swap picture: the region 0 < x < u swept two ways.
        axr = Axes(
            x_range=[0, 4.4, 1], y_range=[0, 4.4, 1],
            x_length=3.6, y_length=3.6,
            axis_config={"include_numbers": False}, tips=False,
        ).move_to(LEFT * 3.4 + DOWN * 1.0)
        xl = MathTex("x", font_size=CAPTION, color=MUTED)
        xl.next_to(axr.c2p(4.4, 0), DOWN + RIGHT, buff=0.12)
        ul = MathTex("u", font_size=CAPTION, color=MUTED)
        ul.next_to(axr.c2p(0, 4.4), LEFT, buff=0.18)
        region = Polygon(axr.c2p(0, 0), axr.c2p(4.2, 4.2), axr.c2p(0, 4.2),
                         stroke_color=MUTED, stroke_width=1.5,
                         fill_color=BAR, fill_opacity=0.12)
        diag = Line(axr.c2p(0, 0), axr.c2p(4.2, 4.2),
                    color=MUTED, stroke_width=2)
        diag_lab = MathTex("u = x", font_size=CAPTION, color=MUTED)
        diag_lab.next_to(axr.c2p(3.3, 3.3), DOWN + RIGHT, buff=0.12)

        starts = [0.2 + 0.57 * i for i in range(7)]
        w = 0.40
        vstrips = VGroup(*[
            Polygon(axr.c2p(s, s), axr.c2p(s + w, s + w),
                    axr.c2p(s + w, 4.2), axr.c2p(s, 4.2),
                    stroke_color=INK, stroke_width=1,
                    fill_color=BAR, fill_opacity=0.45)
            for s in starts
        ])
        hstrips = VGroup(*[
            Polygon(axr.c2p(0, s), axr.c2p(s, s),
                    axr.c2p(s + w, s + w), axr.c2p(0, s + w),
                    stroke_color=INK, stroke_width=1,
                    fill_color=BAR, fill_opacity=0.45)
            for s in starts
        ])
        mark_intended_overlap(axr, region, diag, diag_lab, vstrips, hstrips,
                              xl, ul,
                              reason="order-swap region shaded by strips")

        with self.voiceover(
            text="The proof is a change of perspective. The tail integral "
                 "is a double integral over the region where u exceeds x, "
                 "swept in vertical strips, one for each x."
        ):
            self.play(tail_eq.animate.set_color(INK), run_time=0.4)
            self.play(Create(axr), FadeIn(xl), FadeIn(ul), run_time=0.7)
            self.play(FadeIn(region), Create(diag), FadeIn(diag_lab),
                      run_time=0.7)
            self.play(LaggedStart(*[FadeIn(s) for s in vstrips],
                                  lag_ratio=0.12), run_time=1.1)

        rows_eq = VGroup(
            MathTex(r"\int_0^{\infty} " + pr("X > x") + r"\,dx",
                    font_size=SMALL, color=INK),
            MathTex(r"= \int_0^{\infty} u\, f_X(u)\,du \;=\; "
                    + expectation("X"),
                    font_size=SMALL, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows_eq[1].shift(RIGHT * 0.5)
        rows_eq.move_to(RIGHT * 3.4 + DOWN * 1.0)
        fit_to_frame(rows_eq)

        with self.voiceover(
            text="Sweep the same region in horizontal strips instead, and "
                 "each strip runs from zero up to u, so it contributes u "
                 "times f of u — the integrand of the mean. Same region, "
                 "two ways to sweep it: tails on one side, the mean on the "
                 "other."
        ):
            self.play(ReplacementTransform(vstrips, hstrips), run_time=1.2)
            self.play(Write(rows_eq[0]), run_time=0.8)
            self.play(Write(rows_eq[1]), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DartboardExample(VoiceoverScene):
    """Beat: darts -- the tail formula pays off with no density in sight."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Darts and the Tail Formula")
        fit_to_frame(title)

        with self.voiceover(
            text="Let the tail formula show off."
        ):
            self.play(Write(title), run_time=0.8)
            self.play(title.animate.to_edge(UP), run_time=0.6)

        center = LEFT * 3.5 + DOWN * 0.55
        R_SCENE = 1.85
        disk = Circle(radius=R_SCENE, color=INK, stroke_width=2.5)
        disk.set_fill(BAR, opacity=0.15).move_to(center)
        dart_pts = [
            (0.30, 0.50), (-0.90, 0.20), (1.20, -0.60), (-0.40, -1.10),
            (0.10, -0.30), (0.80, 1.00), (-1.30, -0.60), (1.40, 0.40),
            (-0.20, 1.30), (0.60, -1.30),
        ]
        darts = VGroup(*[
            Dot(center + RIGHT * x + UP * y, radius=0.05, color=INK)
            for x, y in dart_pts
        ])

        r_frac = 0.6
        ring = Circle(radius=r_frac * R_SCENE, color=ACCENT,
                      stroke_width=2.5).move_to(center)
        annulus = Annulus(inner_radius=r_frac * R_SCENE,
                          outer_radius=R_SCENE,
                          fill_color=MAROON, fill_opacity=0.25,
                          stroke_width=0).move_to(center)
        r_dir = np.array([np.cos(0.7), np.sin(0.7), 0.0])
        r_line = Line(center, center + r_frac * R_SCENE * r_dir,
                      color=ACCENT, stroke_width=2.5)
        r_lab = MathTex("r", font_size=CAPTION, color=ACCENT)
        r_lab.move_to(center + 0.55 * r_frac * R_SCENE * r_dir
                      + 0.22 * (UP + LEFT))
        big_lab = MathTex("R > r", font_size=SMALL, color=INK)
        big_lab.move_to(center + UP * (R_SCENE + r_frac * R_SCENE) / 2)
        mark_intended_overlap(disk, darts, ring, annulus, r_line, r_lab,
                              big_lab,
                              reason="dartboard composition: ring, darts, "
                                     "and annulus share the disk")

        q_eq = MathTex(expectation("R"), "=", "?",
                       font_size=BODY, color=INK)
        # Review 2026-07-04, 6:30: the whole equation column (everything is
        # chained below q_eq via next_to) sits a bit further left for
        # balance against the dartboard.
        q_eq.move_to(RIGHT * 2.9 + UP * 1.8)

        with self.voiceover(
            text="A player throws darts at a circular target of unit "
                 "radius, and every dart lands uniformly over the disk — "
                 "probability proportional to area, the geometric models "
                 "from early in the course. How far from the center should "
                 "we expect a dart to land?"
        ):
            self.play(Create(disk), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in darts],
                                  lag_ratio=0.08), run_time=1.2)
            self.play(Write(q_eq), run_time=0.8)

        with self.voiceover(
            text="Call the distance R, and pick a radius r. The dart lands "
                 "beyond r exactly when it falls outside the inner disk of "
                 "radius r, and for a uniform dart, probability is area "
                 "ratio."
        ):
            self.play(Create(ring), run_time=0.7)
            self.play(Create(r_line), FadeIn(r_lab), run_time=0.6)
            self.play(FadeIn(annulus), FadeIn(big_lab), run_time=0.8)

        tail_eq = MathTex(
            pr("R > r"), "=", r"1 - \frac{\pi r^2}{\pi}", "=", r"1 - r^2",
            font_size=SMALL, color=INK,
        ).next_to(q_eq, DOWN, buff=0.6)
        fit_to_frame(tail_eq)

        with self.voiceover(
            text="The inner disk has area pi r squared out of pi, so the "
                 "tail is one minus r squared."
        ):
            self.play(ring.animate.set_color(INK),
                      r_line.animate.set_color(INK),
                      r_lab.animate.set_color(MUTED), run_time=0.4)
            self.play(Write(tail_eq), run_time=1.1)
            self.play(tail_eq[4].animate.set_color(ACCENT), run_time=0.4)

        int_eq = MathTex(
            expectation("R"), "=", r"\int_0^1 \left(1 - r^2\right) dr",
            font_size=SMALL, color=INK,
        ).next_to(tail_eq, DOWN, buff=0.5)
        fit_to_frame(int_eq)

        with self.voiceover(
            text="That is everything the tail formula needs. The expected "
                 "distance is the integral, from zero to one, of one minus "
                 "r squared,"
        ):
            self.play(tail_eq[4].animate.set_color(INK), run_time=0.4)
            self.play(Write(int_eq), run_time=1.0)

        res_eq = MathTex(
            r"= \left. r - \frac{r^3}{3} \right|_0^1", "=", r"\frac{2}{3}",
            font_size=SMALL, color=INK,
        ).next_to(int_eq, DOWN, buff=0.4)
        res_eq.shift(RIGHT * 0.5)
        fit_to_frame(res_eq)
        no_pdf = Text("no density ever written",
                      font_size=CAPTION, color=MUTED)
        no_pdf.next_to(res_eq, DOWN, buff=0.35)

        with self.voiceover(
            text="which is r minus r cubed over three, evaluated at one: "
                 "two thirds. Notice what never appeared: the density of R. "
                 "The tail was pure geometry, and the tail formula turned "
                 "geometry straight into a mean."
        ):
            self.play(Write(res_eq), run_time=1.0)
            self.play(res_eq[2].animate.set_color(ACCENT),
                      FadeIn(no_pdf), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The density is the CDF's slope, probabilities are areas",
             "under it, and expectation rides the same integral."],
            next_title="The Uniform and Gaussian Distributions",
        )

        with self.voiceover(
            text="The key idea of this video: the density is the CDF's "
                 "slope, probabilities are areas under it, and expectation "
                 "rides the same integral. Next up: the distributions "
                 "everyone uses — the uniform and the Gaussian."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
