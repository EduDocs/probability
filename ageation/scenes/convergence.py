# derived_from: content/41-convergence-script.md
# derived_from_sha256: c35470e4e219d73691323cbc0ae261ae290722ddff06477d08b0839286507b2e
"""Chapter 12, Video 1 -- Types of Convergence.

Source notes : empirical_sums.tex (Section 12.1 + its three subsections) --
               the two Gaussian sequences, convergence in probability,
               mean square convergence (and its Chebyshev bridge), and
               convergence in distribution with the uniform [0, 1/n] example.
Script        : content/41-convergence-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark
segment -- the same pattern as the earlier videos in the series.
All cross-references are by concept, never by video number.

Draft render:
    uv run manim -pql scenes/convergence.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import os
import sys

import numpy as np

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
    speech_service,
    zone_center_y,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice); AGEATION_TTS
    is the draft/final switch (render.py sets gtts for -ql)."""
    return speech_service()


# Fixed example parameters (hardcoded -- no runtime randomness).
M_VAL = 2.0          # the mean m of each Gaussian in the worked example
EPS_VAL = 0.8        # the epsilon band half-width (drawing scale only)

# (2026-07-05 draft review, 1:44/1:49) The reviewer's vertical rule: a
# beat's content blocks center on the halfway anchor below the docked
# title (the zone_center_y pattern from the other chapter-11/12 scenes).
_DOCKED_TITLE = section_title("The Concentrating Sequence").to_edge(UP)
CONTENT_MID_Y = zone_center_y(_DOCKED_TITLE)


def bare_axes(x_range, y_range, x_length, y_length):
    """Unnumbered axes for conceptual density/CDF sketches."""
    return Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={"include_numbers": False, "include_tip": False},
        tips=False,
    )


def gaussian_curve(axes, mean, sd, color, x_min, x_max):
    """A Gaussian density plotted on `axes` (increasing range, house rule)."""
    return axes.plot(
        lambda x: np.exp(-((x - mean) ** 2) / (2 * sd * sd))
        / (sd * np.sqrt(2 * np.pi)),
        x_range=[x_min, x_max],
        color=color,
        stroke_width=3,
    )


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + the three-notion outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Types of Convergence",
            ["Three ways a sequence of random variables can settle down:",
             "in probability, in mean square, in distribution."],
            kicker="Chapter 12  ·  Limit Theorems",
        )
        tag = progress_tag(1, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Convergence in probability", font_size=BODY, color=INK),
            Text("2.  Mean square convergence", font_size=BODY, color=INK),
            Text("3.  Convergence in distribution", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video, we built the distribution of a sum of "
                 "continuous random variables: convolution stacked the "
                 "densities, and moment generating functions turned sums "
                 "into products."
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
            text="Now we ask what happens as the sequence of sums runs on "
                 "forever. Random variables can settle down in more than "
                 "one sense, and the finale of this course depends on "
                 "telling those senses apart. In this video we meet three "
                 "of them, each with its own picture."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="First, convergence in probability: deviations of any "
                 "fixed size become vanishingly rare."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Second, mean square convergence: the average squared "
                 "error itself dies out."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Third, convergence in distribution: only the CDFs need "
                 "to settle onto a limiting shape."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


class TwoSequences(VoiceoverScene):
    """Beat: two-sequences -- the concentrating and the invariant Gaussians."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("One Experiment, One Sequence")
        fit_to_frame(title)
        self.play(Write(title), run_time=0.7)
        self.play(title.animate.to_edge(UP), run_time=0.5)

        seq_line = MathTex(
            r"X_1,\; X_2,\; X_3,\; \ldots \;\longrightarrow\; X",
            font_size=BODY, color=INK,
        ).move_to(UP * 0.8)
        seq_note = Text("all functions of the outcome of the same experiment",
                        font_size=SMALL, color=MUTED)
        seq_note.next_to(seq_line, DOWN, buff=0.5)
        fit_to_frame(VGroup(seq_line, seq_note))

        with self.voiceover(
            text="Everything starts with one experiment. A sequence of "
                 "random variables X one, X two, and so on, together with "
                 "a limiting random variable X, all defined on the same "
                 "probability space — all functions of the outcome of a "
                 "single experiment. Without that shared space, the "
                 "difference between X n and X would mean nothing."
        ):
            self.play(Write(seq_line), run_time=1.2)
            self.play(FadeIn(seq_note, shift=UP * 0.2), run_time=0.8)

        # --- The concentrating sequence -------------------------------
        title2 = section_title("The Concentrating Sequence").to_edge(UP)

        col = VGroup(
            MathTex(r"S_n = X_1 + \cdots + X_n", font_size=SMALL, color=INK),
            MathTex(expectation(r"\frac{S_n}{n}"), "=", "m",
                    font_size=SMALL, color=INK),
            MathTex(variance(r"\frac{S_n}{n}"), "=", r"\frac{\sigma^2}{n}",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        # (2026-07-05 draft review, 1:49) The equation block's end state
        # sits vertically centered on the halfway anchor, level with the
        # figure block on the left.
        col.move_to([3.6, CONTENT_MID_Y, 0])
        fit_to_frame(col)

        with self.voiceover(
            text="Take independent Gaussian variables, each with mean m "
                 "and variance sigma squared, and form the partial sums "
                 "S n. Sums of Gaussians stay Gaussian — that was the "
                 "convolution result — so S n over n is Gaussian too, with "
                 "mean m and variance sigma squared over n."
        ):
            self.play(FadeOut(seq_line), FadeOut(seq_note),
                      Transform(title, title2), run_time=0.7)
            self.play(Write(col[0]), run_time=0.8)
            self.play(Write(col[1]), run_time=0.8)
            self.play(Write(col[2]), run_time=0.8)

        # Left chart rides high so the caption gets its own lane.
        axes = bare_axes([-1, 5, 1], [0, 1.8, 0.6], 6.0, 3.2)
        m_line = DashedLine(axes.c2p(M_VAL, 0), axes.c2p(M_VAL, 1.7),
                            color=MUTED, stroke_width=2, dash_length=0.1)
        m_lab = MathTex("m", font_size=BODY, color=INK)
        m_lab.next_to(axes.c2p(M_VAL, 0), DOWN, buff=0.3)
        curves = VGroup(
            gaussian_curve(axes, M_VAL, 1.0, ACCENT, -1, 5),
            gaussian_curve(axes, M_VAL, 0.5, ACCENT, -1, 5),
            gaussian_curve(axes, M_VAL, 0.25, ACCENT, 0.5, 3.5),
        )
        n_tag = MathTex("n = 1", font_size=BODY, color=INK)
        chart = VGroup(axes, m_line, m_lab, curves, n_tag)
        chart.move_to(LEFT * 3.2)
        n_tag.move_to(axes.c2p(4.2, 1.5))
        mark_intended_overlap(
            axes, m_line, curves,
            reason="densities rise from the axis across the m line")
        caption = Text("the density squeezes onto m",
                       font_size=CAPTION, color=MUTED)
        caption.next_to(chart, DOWN, buff=0.3).match_x(axes)
        # (2026-07-05 draft review, 1:44) Figure + caption move as ONE
        # block whose center sits on the halfway anchor below the title.
        _left = VGroup(chart, caption)
        _left.shift(UP * (CONTENT_MID_Y - _left.get_center()[1]))

        with self.voiceover(
            text="Watch that variance. As n grows, the density of S n "
                 "over n squeezes onto m: taller, narrower at every step. "
                 "The sequence of averages is becoming increasingly "
                 "predictable."
        ):
            self.play(Create(axes), Create(m_line), Write(m_lab),
                      run_time=0.8)
            self.play(Create(curves[0]), FadeIn(n_tag), run_time=0.7)
            self.play(curves[0].animate.set_color(MUTED),
                      Create(curves[1]),
                      Transform(n_tag, MathTex("n = 4", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)
            self.play(curves[1].animate.set_color(MUTED),
                      Create(curves[2]),
                      Transform(n_tag, MathTex("n = 16", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)
            self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        # --- The invariant sequence -----------------------------------
        title3 = section_title("The Invariant Sequence").to_edge(UP)

        col2 = VGroup(
            MathTex(r"Z_n = \frac{S_n - n m}{\sqrt{n}}",
                    font_size=SMALL, color=INK),
            MathTex(expectation(r"Z_n"), "=", "0",
                    font_size=SMALL, color=INK),
            MathTex(variance(r"Z_n"), "=", r"\sigma^2",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        # (2026-07-05 draft review, 2:00/2:19) Harmonize with the anchor:
        # the right column's END state is equations + the verdict note, so
        # plan that combined block centered on the halfway anchor from the
        # start. The verdict is a secondary note -> SMALL, not BODY.
        verdict = VGroup(
            Text("one scaling collapses onto m,", font_size=SMALL,
                 color=INK),
            Text("the other never moves", font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.25)
        col2.move_to([3.6, 0, 0])
        verdict.next_to(col2, DOWN, buff=0.5)
        verdict.match_x(col2)
        _right = VGroup(col2, verdict)
        _right.shift(UP * (CONTENT_MID_Y - _right.get_center()[1]))
        fit_to_frame(_right)

        with self.voiceover(
            text="Now scale the same sums differently: subtract n times m, "
                 "and divide by the square root of n. The mean is zero, "
                 "and the variance works out to sigma squared — with no n "
                 "left anywhere in it."
        ):
            self.play(FadeOut(VGroup(chart, caption)),
                      Transform(title, title3), run_time=0.7)
            self.play(Transform(col[0], col2[0]), run_time=0.8)
            self.play(Transform(col[1], col2[1]), run_time=0.7)
            self.play(Transform(col[2], col2[2]), run_time=0.7)

        axes2 = bare_axes([-4, 4, 1], [0, 0.6, 0.2], 6.0, 3.0)
        zero_lab = MathTex("0", font_size=BODY, color=INK)
        zero_lab.next_to(axes2.c2p(0, 0), DOWN, buff=0.3)
        inv_curve = gaussian_curve(axes2, 0.0, 1.0, ACCENT, -4, 4)
        n_tag2 = MathTex("n = 1", font_size=BODY, color=INK)
        chart2 = VGroup(axes2, zero_lab, inv_curve, n_tag2)
        chart2.move_to(LEFT * 3.2)
        n_tag2.move_to(axes2.c2p(2.9, 0.5))
        mark_intended_overlap(
            axes2, inv_curve,
            reason="density tails run along the axis")
        caption2 = Text("the same Gaussian density for every n",
                        font_size=CAPTION, color=MUTED)
        caption2.next_to(chart2, DOWN, buff=0.3).match_x(axes2)
        # (2026-07-05 draft review, 2:00) Same anchor treatment as the
        # concentrating figure: figure + caption centered as one block.
        _left2 = VGroup(chart2, caption2)
        _left2.shift(UP * (CONTENT_MID_Y - _left2.get_center()[1]))

        with self.voiceover(
            text="However large n gets, this sequence keeps the same "
                 "Gaussian density: the distribution simply never moves."
        ):
            self.play(Create(axes2), Write(zero_lab), run_time=0.7)
            self.play(Create(inv_curve), FadeIn(n_tag2), run_time=0.8)
            for label in ("n = 4", "n = 16"):
                self.play(
                    Transform(n_tag2, MathTex(label, font_size=BODY,
                                              color=INK).move_to(n_tag2)),
                    Indicate(inv_curve, color=ACCENT, scale_factor=1.0),
                    run_time=0.8)
            self.play(FadeIn(caption2, shift=UP * 0.2), run_time=0.5)

        with self.voiceover(
            text="One recipe, two scalings, two utterly different "
                 "behaviors — one collapses onto a point, the other holds "
                 "its shape forever. Both patterns will return as "
                 "theorems, so to say precisely what each is doing, we "
                 "need vocabulary."
        ):
            self.play(inv_curve.animate.set_color(MUTED), run_time=0.4)
            self.play(FadeIn(verdict[0], shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(verdict[1], shift=RIGHT * 0.3), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


class ConvergenceInProbability(VoiceoverScene):
    """Beat: in-probability -- the epsilon band, then the shrinking uniform."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Convergence in Probability")
        fit_to_frame(title)
        self.play(Write(title), run_time=0.7)
        self.play(title.animate.to_edge(UP), run_time=0.5)

        definition = MathTex(
            r"\lim_{n \to \infty}",
            pr(r"\left| X_n - X \right| \geq \epsilon"),
            r"= 0",
            font_size=BODY, color=ACCENT,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(definition)
        cond = MathTex(r"\text{for every } \epsilon > 0",
                       font_size=SMALL, color=MUTED)
        cond.next_to(definition, DOWN, buff=0.25)

        with self.voiceover(
            text="Here is the first notion. A sequence X one, X two, and "
                 "so on converges in probability to X if, for every "
                 "positive epsilon, the probability that X n differs from "
                 "X by epsilon or more tends to zero."
        ):
            self.play(Write(definition), run_time=1.4)
            self.play(FadeIn(cond, shift=UP * 0.2), run_time=0.6)

        # --- The epsilon band around m --------------------------------
        axes = bare_axes([-1, 5, 1], [0, 1.0, 0.5], 6.0, 3.0)
        band_l = DashedLine(axes.c2p(M_VAL - EPS_VAL, 0),
                            axes.c2p(M_VAL - EPS_VAL, 0.85),
                            color=ACCENT, stroke_width=2.5, dash_length=0.1)
        band_r = DashedLine(axes.c2p(M_VAL + EPS_VAL, 0),
                            axes.c2p(M_VAL + EPS_VAL, 0.85),
                            color=ACCENT, stroke_width=2.5, dash_length=0.1)
        band_l_lab = MathTex(r"m - \epsilon", font_size=SMALL, color=INK)
        band_r_lab = MathTex(r"m + \epsilon", font_size=SMALL, color=INK)
        m_lab = MathTex("m", font_size=BODY, color=INK)
        chart = VGroup(axes, band_l, band_r, band_l_lab, band_r_lab, m_lab)
        chart.move_to(LEFT * 3.1)
        chart.to_edge(DOWN, buff=1.4)
        band_l_lab.next_to(band_l.get_top(), UP, buff=0.15)
        band_r_lab.next_to(band_r.get_top(), UP, buff=0.15)
        m_lab.next_to(axes.c2p(M_VAL, 0), DOWN, buff=0.3)
        mark_intended_overlap(
            axes, band_l, band_r,
            reason="epsilon band lines rise from the x-axis")

        with self.voiceover(
            text="Picture a band of half-width epsilon around the limit. "
                 "Convergence in probability says the mass outside that "
                 "band drains away — deviations of any visible size become "
                 "vanishingly rare."
        ):
            self.play(definition.animate.set_color(INK), Create(axes),
                      Write(m_lab), run_time=0.8)
            self.play(Create(band_l), Create(band_r),
                      Write(band_l_lab), Write(band_r_lab), run_time=1.0)

        wide = gaussian_curve(axes, M_VAL, 0.9, INK, -1, 5)
        narrow = gaussian_curve(axes, M_VAL, 0.45, INK, -0.5, 4.5)
        tail_l = axes.get_area(wide, x_range=(-1, M_VAL - EPS_VAL),
                               color=ACCENT, opacity=0.3)
        tail_r = axes.get_area(wide, x_range=(M_VAL + EPS_VAL, 5),
                               color=ACCENT, opacity=0.3)
        tail_l2 = axes.get_area(narrow, x_range=(-0.5, M_VAL - EPS_VAL),
                                color=ACCENT, opacity=0.3)
        tail_r2 = axes.get_area(narrow, x_range=(M_VAL + EPS_VAL, 4.5),
                                color=ACCENT, opacity=0.3)
        mark_intended_overlap(
            axes, band_l, band_r, wide, narrow,
            tail_l, tail_r, tail_l2, tail_r2,
            reason="density and shaded tails sit on the axis and band")
        sn_line = MathTex(r"\frac{S_n}{n}", r"\;\longrightarrow\;", "m",
                          font_size=BODY, color=INK)
        sn_note = Text("in probability", font_size=SMALL, color=MUTED)
        sn_col = VGroup(sn_line, sn_note).arrange(DOWN, buff=0.25)
        sn_col.move_to(RIGHT * 3.9 + DOWN * 1.4)
        fit_to_frame(sn_col)

        with self.voiceover(
            text="Our concentrating sequence does exactly this: S n over n "
                 "converges in probability to m. The shaded tails outside "
                 "the band carry less and less probability as the density "
                 "squeezes in."
        ):
            self.play(band_l.animate.set_color(MUTED),
                      band_r.animate.set_color(MUTED),
                      Create(wide), run_time=0.8)
            self.play(Write(sn_line), FadeIn(sn_note), run_time=0.8)
            self.play(FadeIn(tail_l), FadeIn(tail_r), run_time=0.7)
            self.play(Transform(wide, narrow),
                      Transform(tail_l, tail_l2),
                      Transform(tail_r, tail_r2), run_time=1.2)

        # --- The shrinking uniform family -----------------------------
        self.play(FadeOut(VGroup(chart, wide, tail_l, tail_r, sn_col)),
                  run_time=0.5)

        axes2 = bare_axes([-0.5, 1.5, 0.5], [0, 5.5, 1], 6.0, 3.2)
        rects = VGroup()
        for n in (1, 2, 5):
            w = (axes2.c2p(1.0 / n, 0) - axes2.c2p(0, 0))[0]
            h = (axes2.c2p(0, float(n)) - axes2.c2p(0, 0))[1]
            rect = Rectangle(width=w, height=h,
                             fill_color=BAR, fill_opacity=0.35,
                             stroke_color=INK, stroke_width=2)
            rect.move_to(axes2.c2p(0, 0), aligned_edge=DL)
            rects.add(rect)
        eps_line = DashedLine(axes2.c2p(0.4, 0), axes2.c2p(0.4, 5.2),
                              color=ACCENT, stroke_width=2.5,
                              dash_length=0.1)
        eps_lab = MathTex(r"\epsilon", font_size=BODY, color=ACCENT)
        zero_lab = MathTex("0", font_size=CAPTION, color=MUTED)
        one_lab = MathTex("1", font_size=CAPTION, color=MUTED)
        n_tag = MathTex("n = 1", font_size=BODY, color=INK)
        chart2 = VGroup(axes2, rects, eps_line, eps_lab,
                        zero_lab, one_lab, n_tag)
        chart2.move_to(LEFT * 3.1)
        chart2.to_edge(DOWN, buff=1.4)
        eps_lab.next_to(eps_line.get_top(), UR, buff=0.12)
        zero_lab.next_to(axes2.c2p(0, 0), DOWN, buff=0.25)
        one_lab.next_to(axes2.c2p(1, 0), DOWN, buff=0.25)
        n_tag.move_to(axes2.c2p(1.2, 4.6))
        mark_intended_overlap(
            axes2, rects, eps_line,
            reason="uniform densities share the origin corner and "
                   "straddle the epsilon line")

        with self.voiceover(
            text="A second example makes the definition almost trivial to "
                 "check. Let X n be uniform on the interval from zero to "
                 "one over n. The support itself shrinks toward zero, so "
                 "once n exceeds one over epsilon, the whole distribution "
                 "lives inside the band, and the deviation probability is "
                 "not just small — it is exactly zero."
        ):
            self.play(Create(axes2), Write(zero_lab), Write(one_lab),
                      run_time=0.7)
            self.play(Create(eps_line), Write(eps_lab), run_time=0.6)
            self.play(FadeIn(rects[0]), FadeIn(n_tag), run_time=0.6)
            self.play(rects[0].animate.set_fill(opacity=0.12),
                      FadeIn(rects[1]),
                      Transform(n_tag, MathTex("n = 2", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)
            self.play(rects[1].animate.set_fill(opacity=0.12),
                      FadeIn(rects[2]),
                      Transform(n_tag, MathTex("n = 5", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)

        verdict = MathTex("X_n", r"\;\longrightarrow\;", "0",
                          font_size=BODY, color=ACCENT)
        verdict_note = Text("in probability", font_size=SMALL, color=MUTED)
        verdict_col = VGroup(verdict, verdict_note).arrange(DOWN, buff=0.25)
        verdict_col.move_to(RIGHT * 3.9 + DOWN * 1.4)
        fit_to_frame(verdict_col)
        caption = Text("the deviation probability is exactly zero",
                       font_size=CAPTION, color=MUTED)
        caption.next_to(chart2, DOWN, buff=0.3).match_x(axes2)

        with self.voiceover(
            text="So X n converges in probability to the constant zero. "
                 "Keep this shrinking uniform family in mind: it returns "
                 "at the end of the video wearing a different notion of "
                 "convergence."
        ):
            self.play(eps_line.animate.set_color(MUTED),
                      eps_lab.animate.set_color(MUTED), run_time=0.4)
            self.play(Write(verdict), FadeIn(verdict_note), run_time=0.8)
            self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


class MeanSquareConvergence(VoiceoverScene):
    """Beat: mean-square -- definition, the rate, and the Chebyshev bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Mean Square Convergence")
        fit_to_frame(title)
        self.play(Write(title), run_time=0.7)
        self.play(title.animate.to_edge(UP), run_time=0.5)

        definition = MathTex(
            r"\lim_{n \to \infty}",
            expectation(r"\left| X_n - X \right|^2"),
            r"= 0",
            font_size=BODY, color=ACCENT,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(definition)

        with self.voiceover(
            text="The second notion speaks the language of expectation. A "
                 "sequence converges in mean square to X if the expected "
                 "value of the squared difference between X n and X tends "
                 "to zero. That is, the second moment of the error itself "
                 "must vanish as n goes to infinity."
        ):
            self.play(Write(definition), run_time=1.4)

        # Long chain broken onto two lines; the continuation "=" x-aligns
        # under the first line's "=" so it reads as one derivation.
        line1 = MathTex(
            expectation(r"\left| \tfrac{S_n}{n} - m \right|^2"),
            "=",
            variance(r"\tfrac{S_n}{n}"),
            font_size=SMALL, color=INK,
        )
        line2 = MathTex(
            "=",
            r"\frac{\sigma^2}{n} \;\longrightarrow\; 0",
            font_size=SMALL, color=INK,
        )
        line1.next_to(definition, DOWN, buff=0.5)
        line2.next_to(line1, DOWN, buff=0.25)
        line2.shift(RIGHT * (line1[1].get_x() - line2[0].get_x()))
        chain = VGroup(line1, line2)
        fit_to_frame(chain)

        with self.voiceover(
            text="For the Gaussian average, that expected squared error is "
                 "exactly sigma squared over n — so the concentrating "
                 "sequence converges in mean square to m, and we even see "
                 "the rate: the error falls like one over n."
        ):
            self.play(definition.animate.set_color(INK), run_time=0.4)
            self.play(Write(line1), run_time=1.0)
            self.play(Write(line2), run_time=0.9)
            self.play(line2[1].animate.set_color(ACCENT), run_time=0.4)

        impl = MathTex(
            r"\text{mean square}",
            r"\;\Longrightarrow\;",
            r"\text{in probability}",
            font_size=BODY, color=INK,
        ).next_to(chain, DOWN, buff=0.5)
        fit_to_frame(impl)

        with self.voiceover(
            text="Mean square convergence is the stronger claim: it "
                 "implies convergence in probability, and the bridge is "
                 "the Chebyshev bound from the inequalities video."
        ):
            self.play(line2[1].animate.set_color(INK), run_time=0.3)
            self.play(Write(impl), run_time=1.0)

        cheb = MathTex(
            pr(r"\left| X_n - X \right| \geq \epsilon"),
            r"\;\leq\;",
            r"\frac{" + expectation(r"\left| X_n - X \right|^2")
            + r"}{\epsilon^2}",
            font_size=BODY, color=INK,
        ).next_to(impl, DOWN, buff=0.5)
        fit_to_frame(cheb)

        with self.voiceover(
            text="Apply that bound to the variable X n minus X: the "
                 "probability that the deviation reaches epsilon is at "
                 "most the expected squared error divided by epsilon "
                 "squared."
        ):
            self.play(Write(cheb), run_time=1.2)
            self.play(cheb[2].animate.set_color(ACCENT), run_time=0.5)

        to_zero = MathTex(r"\longrightarrow\; 0",
                          font_size=BODY, color=ACCENT)
        to_zero.next_to(cheb, RIGHT, buff=0.3)
        fit_to_frame(VGroup(cheb, to_zero))

        with self.voiceover(
            text="The hypothesis says the numerator tends to zero. Epsilon "
                 "is fixed, so the whole bound collapses, and the "
                 "deviation probability is squeezed to zero along with it."
        ):
            self.play(cheb[2].animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(to_zero, shift=RIGHT * 0.3), run_time=0.7)

        with self.voiceover(
            text="One inequality converts one mode of convergence into the "
                 "other — the same tool that once bounded tail "
                 "probabilities now powers a limit statement."
        ):
            self.play(to_zero.animate.set_color(INK),
                      impl[1].animate.set_color(ACCENT), run_time=0.6)
            self.play(Indicate(impl, color=ACCENT, scale_factor=1.03),
                      run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)


class ConvergenceInDistribution(VoiceoverScene):
    """Beat: in-distribution -- CDFs settle; the uniform family returns."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Convergence in Distribution")
        fit_to_frame(title)
        self.play(Write(title), run_time=0.7)
        self.play(title.animate.to_edge(UP), run_time=0.5)

        definition = MathTex(
            r"\lim_{n \to \infty} F_{X_n}(x) = F_X(x)",
            font_size=BODY, color=ACCENT,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(definition)
        cond = MathTex(
            r"\text{at every } x \text{ where } F_X \text{ is continuous}",
            font_size=SMALL, color=INK,
        ).next_to(definition, DOWN, buff=0.25)
        weak = Text("also called weak convergence",
                    font_size=CAPTION, color=MUTED)
        weak.next_to(cond, DOWN, buff=0.25)

        with self.voiceover(
            text="The third notion asks for the least."
        ):
            self.wait(0.3)

        # (2026-07-05 draft review, 5:24) Paragraph turn: sequential
        # voiceover blocks join gaplessly, so breathe before the
        # definition lands (STYLE_BOOK 12 paragraph-turn rule).
        self.wait(0.5)

        with self.voiceover(
            text="A sequence converges in distribution to X if the CDF of "
                 "X n converges to the CDF of X at every point where the "
                 "limiting CDF is continuous. Only the distribution "
                 "functions need to settle — this is also called weak "
                 "convergence."
        ):
            self.play(Write(definition), run_time=1.2)
            self.play(FadeIn(cond, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(weak), run_time=0.5)

        # --- Echo: the staircase that settled onto a smooth CDF --------
        e_axes = bare_axes([0, 4, 1], [0, 1.2, 0.5], 4.4, 2.2)
        smooth = e_axes.plot(lambda x: 1 - np.exp(-x), x_range=[0, 4],
                             color=ACCENT, stroke_width=3)
        steps = VGroup(*[
            Line(e_axes.c2p(0.5 * k, 1 - np.exp(-0.5 * k)),
                 e_axes.c2p(0.5 * (k + 1), 1 - np.exp(-0.5 * k)),
                 color=MUTED, stroke_width=3)
            for k in range(1, 8)
        ])
        # (2026-07-05 draft review, 5:50) Vertical dashed risers connect
        # consecutive treads -- the DiscreteCDF staircase treatment (only
        # the flat treads are the CDF proper; the jumps are dashed).
        risers = VGroup(*[
            DashedLine(e_axes.c2p(0.5 * (k + 1), 1 - np.exp(-0.5 * k)),
                       e_axes.c2p(0.5 * (k + 1), 1 - np.exp(-0.5 * (k + 1))),
                       color=MUTED, stroke_width=2, dash_length=0.06)
            for k in range(1, 7)
        ])
        echo = VGroup(e_axes, smooth, steps, risers)
        echo.move_to(LEFT * 3.3)
        echo.to_edge(DOWN, buff=1.5)
        mark_intended_overlap(
            e_axes, smooth, steps, risers,
            reason="staircase segments hug the smooth CDF they settle onto")
        echo_cap = Text("a staircase settling onto a smooth CDF",
                        font_size=CAPTION, color=MUTED)
        echo_cap.next_to(echo, DOWN, buff=0.3).match_x(e_axes)

        with self.voiceover(
            text="You have seen this pattern before: when the geometric "
                 "staircase was squeezed into the exponential CDF, that "
                 "was convergence in distribution, before it had a name."
        ):
            self.play(definition.animate.set_color(INK),
                      Create(e_axes), run_time=0.7)
            stair_anims = []
            for i, s in enumerate(steps):
                stair_anims.append(Create(s))
                if i < len(risers):
                    stair_anims.append(Create(risers[i]))
            self.play(LaggedStart(*stair_anims, lag_ratio=0.1),
                      run_time=0.9)
            self.play(Create(smooth), FadeIn(echo_cap, shift=UP * 0.2),
                      run_time=0.9)

        self.play(FadeOut(VGroup(echo, echo_cap)), run_time=0.5)

        # --- The uniform family's CDFs steepen into the unit step ------
        axes = bare_axes([-0.6, 1.4, 0.5], [0, 1.25, 0.5], 6.4, 3.0)

        def cdf_curve(n, color):
            return axes.plot(
                lambda x, n=n: min(max(n * x, 0.0), 1.0),
                x_range=[-0.6, 1.4],
                color=color, stroke_width=3, use_smoothing=False)

        curves = VGroup(cdf_curve(1, ACCENT), cdf_curve(2, ACCENT),
                        cdf_curve(5, ACCENT))
        zero_lab = MathTex("0", font_size=CAPTION, color=MUTED)
        one_lab = MathTex("1", font_size=CAPTION, color=MUTED)
        n_tag = MathTex("n = 1", font_size=BODY, color=INK)
        chart = VGroup(axes, curves, zero_lab, one_lab, n_tag)
        chart.move_to(LEFT * 2.9)
        chart.to_edge(DOWN, buff=1.4)
        zero_lab.next_to(axes.c2p(0, 0), DOWN, buff=0.25)
        # The 0 tick label sits at the origin corner; shift it left so it
        # cannot sit under the rising curves.
        zero_lab.shift(LEFT * 0.22)
        one_lab.next_to(axes.c2p(1, 0), DOWN, buff=0.25)
        n_tag.move_to(axes.c2p(-0.38, 1.13))
        mark_intended_overlap(
            axes, curves,
            reason="CDFs coincide along the axis and at height one")

        with self.voiceover(
            text="Now bring back the shrinking uniform family. The CDF of "
                 "X n rises from zero to one across the interval from zero "
                 "to one over n — and as n grows, these continuous CDFs "
                 "steepen toward the unit step at zero."
        ):
            self.play(Create(axes), Write(zero_lab), Write(one_lab),
                      run_time=0.7)
            self.play(Create(curves[0]), FadeIn(n_tag), run_time=0.7)
            self.play(curves[0].animate.set_color(MUTED),
                      Create(curves[1]),
                      Transform(n_tag, MathTex("n = 2", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)
            self.play(curves[1].animate.set_color(MUTED),
                      Create(curves[2]),
                      Transform(n_tag, MathTex("n = 5", font_size=BODY,
                                               color=INK).move_to(n_tag)),
                      run_time=0.8)

        # The limiting step CDF: 0 for x < 0, jump to 1 at x = 0.
        step_low = Line(axes.c2p(-0.6, 0), axes.c2p(0, 0),
                        color=ACCENT, stroke_width=4)
        step_jump = DashedLine(axes.c2p(0, 0), axes.c2p(0, 1),
                               color=MUTED, stroke_width=2, dash_length=0.08)
        step_high = Line(axes.c2p(0, 1), axes.c2p(1.4, 1),
                         color=ACCENT, stroke_width=4)
        dot_high = Dot(axes.c2p(0, 1), radius=0.07, color=ACCENT)
        dot_low = Circle(radius=0.07, color=ACCENT, stroke_width=3)
        dot_low.move_to(axes.c2p(0, 0))
        step = VGroup(step_low, step_jump, step_high, dot_high, dot_low)
        mark_intended_overlap(
            axes, curves, step,
            reason="the limit step coincides with the axis and the CDFs")
        exempt = MathTex(r"\text{the one exempt point: } x = 0",
                         font_size=SMALL, color=MUTED)
        exempt.next_to(chart, DOWN, buff=0.3).match_x(axes)

        with self.voiceover(
            text="Here the fine print earns its keep. At every negative x "
                 "the CDFs equal zero, and at every positive x they tend "
                 "to one. But exactly at zero, each CDF of X n reads zero "
                 "while the step reads one. No matter: zero is the one "
                 "point where the limiting CDF jumps, so the definition "
                 "simply exempts it."
        ):
            self.play(curves[2].animate.set_color(MUTED), run_time=0.3)
            self.play(Create(step_low), Create(step_jump),
                      Create(step_high), run_time=1.0)
            self.play(FadeIn(dot_high, scale=1.6),
                      Create(dot_low), run_time=0.7)
            self.play(FadeIn(exempt, shift=UP * 0.2), run_time=0.6)

        verdict = MathTex("X_n", r"\;\longrightarrow\;", "0",
                          font_size=BODY, color=ACCENT)
        verdict_note = Text("in distribution", font_size=SMALL, color=MUTED)
        verdict_col = VGroup(verdict, verdict_note).arrange(DOWN, buff=0.25)
        verdict_col.move_to(RIGHT * 4.0 + DOWN * 1.2)
        fit_to_frame(verdict_col)

        with self.voiceover(
            text="The sequence converges in distribution to the constant "
                 "zero — a whole family of continuous random variables "
                 "settling onto a deterministic limit."
        ):
            self.play(step.animate.set_color(INK), run_time=0.4)
            self.play(Write(verdict), FadeIn(verdict_note), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        outro = outro_bridge(
            ["One sequence, three senses of settling:",
             "in probability, in mean square, in distribution."],
            next_title="The Law of Large Numbers",
        )

        with self.voiceover(
            text="The key idea of this video: one sequence can settle in "
                 "three senses — in probability, in mean square, in "
                 "distribution — and knowing which one you are claiming is "
                 "exactly what the two great limit theorems ahead demand. "
                 "Next up: the law of large numbers."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro), run_time=0.5)
