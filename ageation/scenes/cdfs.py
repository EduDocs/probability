# derived_from: content/26-cdfs-script.md
# derived_from_sha256: 47b31f872736df3342a1778f3006768422118784e348416926d72c704c440211
"""Chapter 8, Video 1 -- Cumulative Distribution Functions.

Source notes : continuous_random_variables.tex (Section 8.1, all three
               subsections) -- why the PMF runs out, the CDF and its
               properties, discrete staircases, continuous ramps, mixed.
Script        : content/26-cdfs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/cdfs.py ChapterOverview
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
    section_title,
    intro_card,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    show_zero_tick,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


# Geometric parameters shared by the discrete beat.
GEO_P = 0.5
GEO_N = 8


def geo_cdf(k: int) -> float:
    """F_X(k) = 1 - (1-p)^k for the geometric with p = GEO_P."""
    return 1.0 - (1.0 - GEO_P) ** k


def cdf_axes(x_max, y_step=0.25, x_length=8.6, y_length=3.6, x_step=1):
    """Shared axes idiom for the CDF charts (x extended one unit left)."""
    axes = Axes(
        x_range=[-x_step, x_max, x_step],
        y_range=[0, 1.05, y_step],
        x_length=x_length,
        y_length=y_length,
        axis_config={"include_numbers": True, "font_size": 30},
        x_axis_config={"numbers_to_exclude": [-x_step]},
        tips=False,
    )
    # Manim hides the origin label (2026-07-05 draft review, 4:14/5:10).
    show_zero_tick(axes)
    return axes


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Cumulative Distribution Functions",
            ["One function for every random variable:",
             "interval probabilities as differences of heights."],
            kicker="Chapter 8  ·  Continuous Random Variables",
        )
        tag = progress_tag(1, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The CDF and its properties", font_size=BODY, color=INK),
            Text("2.  Staircases: discrete random variables",
                 font_size=BODY, color=INK),
            Text("3.  Smooth and hybrids: continuous and mixed",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video, sums of discrete random variables closed our story of "
                 "the discrete world: PMFs answered every question we asked. "
                 "This video opens a new chapter, because the discrete world "
                 "is not enough. Noise voltages, waiting times, and signal "
                 "amplitudes range over a continuum, and no list of values "
                 "can hold them."
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
            text="The bridge is the cumulative distribution function: one "
                 "object defined for every random variable, with three "
                 "properties it must obey."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We watch discrete variables draw staircases whose jumps "
                 "are exactly their PMFs,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and meet the new citizens: smoothly climbing CDFs, the "
                 "continuous random variables, plus the hybrids in between."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CDFDefinition(VoiceoverScene):
    """Beat: definition -- why the PMF runs out, the CDF, its properties."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The CDF and Its Properties")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        axiom = MathTex(
            pr(r"\bigcup_{k} A_k"), "=", r"\sum_{k}" + pr(r"A_k"),
            font_size=SMALL,
        ).move_to(DOWN * 0.75)
        fit_to_frame(axiom)
        axiom_cap = Text("countably many only", font_size=CAPTION,
                         color=MUTED)
        axiom_cap.next_to(axiom, DOWN, buff=0.35)

        # (2026-07-04 draft review, 0:54) The axiom card appears BEFORE the
        # narration begins and stays on screen through its whole sentence;
        # it fades only on "We need a new object."
        self.play(Write(axiom), run_time=1.0)
        self.play(FadeIn(axiom_cap, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="Why does the machinery of the PMF run out? A spinner can "
                 "stop at any angle, uncountably many outcomes, and the "
                 "third axiom adds probabilities over countably many "
                 "disjoint events only."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="We need a new object."
        ):
            self.play(FadeOut(VGroup(axiom, axiom_cap)), run_time=0.6)

        defn = MathTex(
            r"F_X(x)", "=", pr(r"X \leq x"),
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(defn)

        with self.voiceover(
            text="Here it is. The cumulative distribution function of X at "
                 "x is the probability that X is less than or equal to x."
        ):
            self.play(Write(defn), run_time=1.2)
            self.play(defn[0].animate.set_color(ACCENT), run_time=0.5)

        ev_form = MathTex(
            r"F_X(x) = " + pr(r"X^{-1}\left((-\infty, x]\right)"),
            font_size=SMALL, color=MUTED,
        ).next_to(defn, DOWN, buff=0.35)
        fit_to_frame(ev_form)

        nline = NumberLine(x_range=[-4, 4, 1], length=8.5,
                           color=MUTED, include_ticks=True)
        nline.move_to(DOWN * 1.9)
        x_pt = 1.5
        x_dot = Dot(nline.number_to_point(x_pt), radius=0.07, color=INK)
        x_lab = MathTex("x", font_size=SMALL, color=INK)
        x_lab.next_to(x_dot, DOWN, buff=0.3)
        ray = Line(nline.number_to_point(-4), nline.number_to_point(x_pt),
                   color=ACCENT, stroke_width=6)
        mark_intended_overlap(
            nline, x_dot, ray,
            reason="the event ray shades the number line up to x")

        with self.voiceover(
            text="In terms of the sample space, it measures every outcome "
                 "that X sends at or to the left of x. It exists for every "
                 "random variable, discrete or not: that is what makes it a "
                 "bridge."
        ):
            self.play(defn[0].animate.set_color(INK),
                      Create(nline), run_time=0.7)
            self.play(FadeIn(x_dot), Write(x_lab), run_time=0.5)
            self.play(Create(ray), run_time=0.9)
            self.play(FadeIn(ev_form, shift=DOWN * 0.2), run_time=0.7)

        limits = VGroup(
            MathTex(r"\lim_{x \downarrow -\infty} F_X(x) = 0",
                    font_size=SMALL, color=INK),
            MathTex(r"\lim_{x \uparrow \infty} F_X(x) = 1",
                    font_size=SMALL, color=INK),
        ).arrange(RIGHT, buff=1.1).move_to(UP * 0.35)
        fit_to_frame(limits)

        with self.voiceover(
            text="Its shape is constrained three ways. Toward minus "
                 "infinity the event empties, so the CDF falls to zero; "
                 "toward plus infinity it captures everything, so the CDF "
                 "climbs to one."
        ):
            self.play(Write(limits[0]), run_time=0.8)
            self.play(ray.animate.put_start_and_end_on(
                nline.number_to_point(-4),
                nline.number_to_point(-3.98)), run_time=0.9)
            self.play(Write(limits[1]), run_time=0.8)
            self.play(ray.animate.put_start_and_end_on(
                nline.number_to_point(-4),
                nline.number_to_point(4)), run_time=1.0)

        x1, x2 = -1.0, 2.0
        seg_left = Line(nline.number_to_point(-4), nline.number_to_point(x1),
                        color=BLUE, stroke_width=6)
        seg_mid = Line(nline.number_to_point(x1), nline.number_to_point(x2),
                       color=GREEN, stroke_width=6)
        x1_lab = MathTex("x_1", font_size=SMALL, color=BLUE)
        x1_lab.next_to(nline.number_to_point(x1), DOWN, buff=0.3)
        x2_lab = MathTex("x_2", font_size=SMALL, color=GREEN)
        x2_lab.next_to(nline.number_to_point(x2), DOWN, buff=0.3)
        mark_intended_overlap(
            nline, seg_left, seg_mid,
            reason="the split event segments shade the number line")

        split_eq = MathTex(
            r"\{X \leq x_2\}", "=", r"\{X \leq x_1\}", r"\cup",
            r"\{x_1 < X \leq x_2\}",
            font_size=SMALL,
        ).move_to(UP * 0.45)
        fit_to_frame(split_eq)
        split_eq[2].set_color(BLUE)
        split_eq[4].set_color(GREEN)
        nondec = MathTex(r"F_X(x_1) \leq F_X(x_2)",
                         font_size=SMALL, color=MUTED)
        nondec.next_to(split_eq, DOWN, buff=0.3)

        with self.voiceover(
            text="Now take two points, x one below x two. The event that X "
                 "is at most x two splits into two disjoint pieces: X at "
                 "most x one, and X strictly between x one and x two. "
                 "Probabilities add, so the CDF can never decrease."
        ):
            self.play(FadeOut(limits), FadeOut(x_dot), FadeOut(x_lab),
                      run_time=0.5)
            self.play(ray.animate.put_start_and_end_on(
                nline.number_to_point(-4),
                nline.number_to_point(x2)), run_time=0.5)
            self.play(FadeOut(ray), FadeIn(seg_left), FadeIn(seg_mid),
                      Write(x1_lab), Write(x2_lab), run_time=0.8)
            self.play(Write(split_eq), run_time=1.1)
            self.play(FadeIn(nondec, shift=DOWN * 0.2), run_time=0.6)

        interval = MathTex(
            pr(r"x_1 < X \leq x_2"), "=", r"F_X(x_2) - F_X(x_1)",
            font_size=BODY, color=ACCENT,
        )
        interval.move_to(nondec.get_center() + DOWN * 0.15)
        fit_to_frame(interval)

        with self.voiceover(
            text="Rearrange the same equation and you get the workhorse of "
                 "the whole chapter: the probability that X lands in the "
                 "interval from x one to x two is a difference of two "
                 "heights, F at x two minus F at x one."
        ):
            self.play(FadeOut(nondec), run_time=0.4)
            self.play(Write(interval), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DiscreteCDF(VoiceoverScene):
    """Beat: discrete -- the sweep, the staircase, the geometric both ways."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Staircases: Discrete Random Variables")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Now let a discrete random variable meet its CDF."
        ):
            self.wait(0.3)

        sum_f = MathTex(
            r"F_X(x)", "=", r"\sum_{u \leq x} p_X(u)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(sum_f)

        with self.voiceover(
            text="If X takes listed values, its CDF at x just sums the PMF "
                 "over every value at or below x."
        ):
            self.play(Write(sum_f), run_time=1.2)

        # One chart: the geometric PMF bars with the CDF staircase accruing
        # over them (the tex figure, animated). Sweep line in accent.
        axes = cdf_axes(GEO_N + 1)
        x_axis_lab = axes.get_x_axis_label(
            MathTex("k", font_size=BODY), edge=RIGHT,
            direction=DOWN + RIGHT, buff=0.25)
        chart = VGroup(axes, x_axis_lab)
        fit_to_frame(chart)

        unit_w = (axes.c2p(1, 0) - axes.c2p(0, 0))[0]
        bars = VGroup()
        for k in range(1, GEO_N + 1):
            p_val = (1 - GEO_P) ** (k - 1) * GEO_P
            bottom = axes.c2p(k, 0)
            top = axes.c2p(k, p_val)
            bar = Rectangle(
                width=unit_w * 0.7, height=top[1] - bottom[1],
                fill_color=BAR, fill_opacity=0.85,
                stroke_width=1, stroke_color=INK,
            )
            bar.move_to(bottom, aligned_edge=DOWN)
            bars.add(bar)

        # (2026-07-04 draft review, 2:42) The vertical connectors of the
        # step function are dashed -- the same treatment as the MixedRVs
        # jump connectors; only the flat treads are the CDF proper.
        stair = VGroup()
        for k in range(1, GEO_N + 1):
            riser = DashedLine(axes.c2p(k, geo_cdf(k - 1)),
                               axes.c2p(k, geo_cdf(k)),
                               color=MUTED, stroke_width=2.5,
                               dash_length=0.06)
            flat_end = k + 1 if k < GEO_N else GEO_N + 0.8
            flat = Line(axes.c2p(k, geo_cdf(k)),
                        axes.c2p(flat_end, geo_cdf(k)),
                        color=INK, stroke_width=3.5)
            stair.add(riser, flat)

        # Dashed level starts AT the y-axis (uniform with the 4:18 fix in
        # ContinuousCDF) so it never overlaps the y-axis "1" label.
        level_one = DashedLine(axes.c2p(0, 1), axes.c2p(GEO_N + 1, 1),
                               color=MUTED, stroke_width=2, dash_length=0.12)
        sweep = DashedLine(axes.c2p(0.2, 0), axes.c2p(0.2, 1.0),
                           color=ACCENT, stroke_width=3, dash_length=0.12)
        chart.add(bars, stair, level_one)
        mark_intended_overlap(
            chart, sweep,
            reason="the CDF staircase accumulates over the PMF bars on one "
                   "set of axes; the sweep line crosses the chart")
        chart.add(sweep)
        chart.to_edge(DOWN, buff=0.8)
        sweep_end_center = (axes.c2p(GEO_N + 0.8, 0)
                            + axes.c2p(GEO_N + 0.8, 1.0)) / 2

        with self.voiceover(
            text="Watch the accumulation happen for an old friend: the "
                 "geometric, with parameter p equal to one half. Sweep from "
                 "left to right across its bars. Between values nothing "
                 "accrues, so the running total stays flat; each time the "
                 "sweep crosses a bar, the total hops up by that bar's "
                 "mass. The result is a staircase climbing toward one."
        ):
            self.play(Create(axes), Write(x_axis_lab),
                      Create(level_one), run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=1.0)
            self.play(Create(sweep), run_time=0.4)
            self.play(sweep.animate.move_to(sweep_end_center),
                      Create(stair, lag_ratio=0.0), run_time=4.0)

        # Solid accent highlight over the (dashed) riser at k = 2.
        jump_hi = Line(axes.c2p(2, geo_cdf(1)), axes.c2p(2, geo_cdf(2)),
                       color=ACCENT, stroke_width=6)
        jump_lab = MathTex(r"p_X(2)", font_size=SMALL, color=ACCENT)
        jump_lab.next_to(jump_hi, RIGHT, buff=0.18)
        mark_intended_overlap(
            chart, jump_hi, jump_lab,
            reason="the jump highlight sits on the staircase riser")

        with self.voiceover(
            text="Look at one step: its jump height is exactly the mass "
                 "sitting at that value."
        ):
            self.play(FadeOut(sweep), run_time=0.4)
            self.play(Create(jump_hi), Write(jump_lab), run_time=0.8)
            self.play(Indicate(bars[1], color=ACCENT, scale_factor=1.05),
                      run_time=0.8)

        recover = MathTex(
            r"p_X(x)", "=", r"F_X(x) - \lim_{u \uparrow x} F_X(u)",
            font_size=SMALL,
        ).move_to(sum_f.get_center())
        fit_to_frame(recover)

        with self.voiceover(
            text="So the PMF can be recovered from the CDF, as the value at "
                 "x minus the limit from the left. Two descriptions, one "
                 "random variable."
        ):
            self.play(FadeOut(jump_hi), FadeOut(jump_lab), run_time=0.4)
            self.play(FadeOut(sum_f), run_time=0.3)
            self.play(Write(recover), run_time=1.0)
            self.play(recover[0].animate.set_color(ACCENT), run_time=0.5)

        pmf_card = MathTex(
            r"p_X(k) = (1-p)^{k-1}\, p,", r"\quad k = 1, 2, \ldots",
            font_size=SMALL,
        ).move_to(UP * 1.1)
        cdf_card = MathTex(
            r"F_X(x) = 1 - (1-p)^{\lfloor x \rfloor}",
            font_size=BODY, color=ACCENT,
        ).next_to(pmf_card, DOWN, buff=0.5)
        fit_to_frame(VGroup(pmf_card, cdf_card))

        with self.voiceover(
            text="Let us work the geometric in both directions. Its masses "
                 "are one minus p to the k minus one, times p. Summing the "
                 "first floor of x of them telescopes into a clean closed "
                 "form: the CDF is one minus, one minus p to the floor of x."
        ):
            self.play(FadeOut(chart), recover[0].animate.set_color(INK),
                      run_time=0.6)
            self.play(Write(pmf_card), run_time=1.0)
            self.play(Write(cdf_card), run_time=1.0)

        diff_lines = VGroup(
            MathTex(r"p_X(k) = F_X(k) - F_X(k-1)",
                    font_size=SMALL, color=INK),
            MathTex(r"= (1-p)^{k-1}\, p",
                    font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.3)
        diff_lines.next_to(cdf_card, DOWN, buff=0.55)
        fit_to_frame(diff_lines)

        with self.voiceover(
            text="And differencing hands the masses back: the CDF at k "
                 "minus the CDF at k minus one collapses to one minus p to "
                 "the k minus one, times p. The PMF, exactly."
        ):
            self.play(cdf_card.animate.set_color(INK),
                      Write(diff_lines[0]), run_time=0.9)
            self.play(Write(diff_lines[1]), run_time=0.8)
            self.play(diff_lines[1].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ContinuousCDF(VoiceoverScene):
    """Beat: continuous -- the smooth ramp, no point mass, the derivative."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Continuous Random Variables")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Not every accumulation climbs in jumps."
        ):
            self.wait(0.3)

        axes = cdf_axes(4, y_step=0.5, x_length=8.0, y_length=3.2)
        x_axis_lab = axes.get_x_axis_label(
            MathTex("x", font_size=BODY), edge=RIGHT,
            direction=DOWN + RIGHT, buff=0.25)
        flat = axes.plot(lambda x: 0.0, x_range=[-1, 0],
                         color=INK, stroke_width=3.5)
        ramp = axes.plot(lambda x: 1 - np.exp(-x), x_range=[0, 4],
                         color=ACCENT, stroke_width=3.5)
        # (2026-07-04 draft review, 4:18) The dashed level starts AT the
        # y-axis so it never overlaps the "1.0" y-axis label.
        level_one = DashedLine(axes.c2p(0, 1), axes.c2p(4, 1),
                               color=MUTED, stroke_width=2, dash_length=0.12)
        chart = VGroup(axes, x_axis_lab, flat, ramp, level_one)
        mark_intended_overlap(
            chart, reason="the flat branch hugs the x-axis and the ramp "
                          "approaches the dashed level at one")
        fit_to_frame(chart)
        chart.to_edge(DOWN, buff=0.8)

        f_lab = MathTex(r"F_X(x) = 1 - e^{-x},\quad x \geq 0",
                        font_size=SMALL, color=INK)
        f_lab.next_to(title, DOWN, buff=0.4)
        fit_to_frame(f_lab)

        with self.voiceover(
            text="Here is a CDF that rises in a smooth progression: zero "
                 "for negative x, then one minus e to the minus x. It satisfies "
                 "everything we asked: it starts at zero, never decreases, "
                 "and climbs to one."
        ):
            self.play(Create(axes), Write(x_axis_lab),
                      Create(level_one), run_time=0.8)
            self.play(Write(f_lab), run_time=0.9)
            self.play(Create(flat), run_time=0.5)
            self.play(Create(ramp), run_time=2.0)

        cond_cap = Text("CDF continuous, differentiable almost everywhere",
                        font_size=CAPTION, color=MUTED)
        cond_cap.next_to(f_lab, DOWN, buff=0.3)
        name_lab = Text("a continuous random variable",
                        font_size=SMALL, color=ACCENT)
        name_lab.next_to(cond_cap, DOWN, buff=0.25)

        with self.voiceover(
            text="When the CDF of X is continuous like this, and "
                 "differentiable almost everywhere, we call X a continuous "
                 "random variable."
        ):
            self.play(ramp.animate.set_color(INK), run_time=0.4)
            self.play(FadeIn(cond_cap, shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(name_lab), run_time=0.8)

        x1, x2 = 0.5, 2.5
        f1, f2 = 1 - np.exp(-x1), 1 - np.exp(-x2)
        v1 = DashedLine(axes.c2p(x1, 0), axes.c2p(x1, f1),
                        color=MUTED, stroke_width=2, dash_length=0.1)
        v2 = DashedLine(axes.c2p(x2, 0), axes.c2p(x2, f2),
                        color=MUTED, stroke_width=2, dash_length=0.1)
        h1 = DashedLine(axes.c2p(x1, f1), axes.c2p(x2, f1),
                        color=MUTED, stroke_width=2, dash_length=0.1)
        d1 = Dot(axes.c2p(x1, f1), radius=0.06, color=INK)
        d2 = Dot(axes.c2p(x2, f2), radius=0.06, color=INK)
        x1_lab = MathTex("x_1", font_size=CAPTION, color=MUTED)
        x1_lab.next_to(axes.c2p(x1, 0), DOWN, buff=0.3)
        x2_lab = MathTex("x_2", font_size=CAPTION, color=MUTED)
        x2_lab.next_to(axes.c2p(x2, 0), DOWN, buff=0.3)
        gap = Line(axes.c2p(x2, f1), axes.c2p(x2, f2),
                   color=ACCENT, stroke_width=6)
        gap_lab = MathTex(r"F_X(x_2) - F_X(x_1)",
                          font_size=CAPTION, color=ACCENT)
        gap_lab.next_to(gap, RIGHT, buff=0.2)
        interval_marks = VGroup(v1, v2, h1, d1, d2, x1_lab, x2_lab,
                                gap, gap_lab)
        mark_intended_overlap(
            chart, interval_marks,
            reason="the interval construction is drawn on the ramp chart")

        with self.voiceover(
            text="And continuity has a striking consequence: with no jumps, "
                 "no single point carries mass on its own. Probability now "
                 "lives on intervals: mark two points on the axis, and the "
                 "chance of landing between them is the vertical gap "
                 "between their two heights."
        ):
            self.play(name_lab.animate.set_color(INK), run_time=0.4)
            self.play(Write(x1_lab), Write(x2_lab),
                      Create(v1), Create(v2), run_time=0.9)
            self.play(FadeIn(d1), FadeIn(d2), Create(h1), run_time=0.8)
            self.play(Create(gap), Write(gap_lab), run_time=1.0)

        # (2026-07-04 draft review, 4:52) The derivative statement carries
        # its domain qualifier: it holds for x > 0 only.
        deriv = MathTex(r"\frac{dF_X}{dx}(x) = e^{-x}, \; x > 0",
                        font_size=BODY, color=ACCENT)
        deriv.move_to((cond_cap.get_center() + name_lab.get_center()) / 2)
        fit_to_frame(deriv)
        deriv_cap = Text("how fast probability accumulates",
                         font_size=CAPTION, color=MUTED)
        deriv_cap.next_to(deriv, DOWN, buff=0.25)

        with self.voiceover(
            text="One more glance at our smooth curve: it is differentiable, "
                 "with derivative e to the minus x, for x positive, measuring "
                 "how fast probability accumulates. Hold that thought, "
                 "because that derivative is the star of the next video."
        ):
            self.play(FadeOut(interval_marks), run_time=0.5)
            self.play(FadeOut(cond_cap), FadeOut(name_lab), run_time=0.4)
            self.play(Write(deriv), run_time=1.0)
            self.play(FadeIn(deriv_cap, shift=UP * 0.2), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MixedRVs(VoiceoverScene):
    """Beat: mixed -- one block over the hybrid CDF (compressed per cut list)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Mixed Random Variables")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[-0.5, 2.2, 0.5],
            y_range=[0, 1.05, 0.25],
            x_length=7.5,
            y_length=3.4,
            axis_config={"include_numbers": True, "font_size": 30},
            x_axis_config={"numbers_to_exclude": [-0.5]},
            tips=False,
        )
        # Manim hides the origin label (2026-07-05 draft review, 5:10).
        show_zero_tick(axes)
        x_axis_lab = axes.get_x_axis_label(
            MathTex("x", font_size=BODY), edge=RIGHT,
            direction=DOWN + RIGHT, buff=0.25)

        # The book's hybrid CDF: four differentiable stretches, three jumps.
        seg1 = axes.plot(lambda x: 0.4 * x ** 2, x_range=[0, 0.6],
                         color=INK, stroke_width=3.5)
        seg2 = axes.plot(lambda x: 0.1 + 0.2 * x, x_range=[0.6, 1],
                         color=INK, stroke_width=3.5)
        seg3 = axes.plot(lambda x: 0.25 + 0.2 * (1 + (x - 0.5) ** 3),
                         x_range=[1, 1.5], color=INK, stroke_width=3.5)
        seg4 = axes.plot(lambda x: 1 - (x - 2) ** 2, x_range=[1.5, 2],
                         color=INK, stroke_width=3.5)
        jump1 = DashedLine(axes.c2p(0.6, 0.144), axes.c2p(0.6, 0.22),
                           color=MUTED, stroke_width=2.5, dash_length=0.06)
        jump2 = DashedLine(axes.c2p(1, 0.3), axes.c2p(1, 0.475),
                           color=MUTED, stroke_width=2.5, dash_length=0.06)
        jump3 = DashedLine(axes.c2p(1.5, 0.65), axes.c2p(1.5, 0.75),
                           color=MUTED, stroke_width=2.5, dash_length=0.06)
        chart = VGroup(axes, x_axis_lab, seg1, jump1, seg2, jump2,
                       seg3, jump3, seg4)
        mark_intended_overlap(
            chart, reason="the hybrid CDF and its jump connectors are one "
                          "composed figure on the axes")
        fit_to_frame(chart)
        chart.to_edge(DOWN, buff=1.4)

        with self.voiceover(
            text="One family remains: mixed random variables, whose CDFs "
                 "climb smoothly in places and jump in others, like this "
                 "one. They have no PMF and they can be discontinuous at "
                 "multiple points, yet the CDF still answers every interval "
                 "question, as differences of heights. Next video, we "
                 "differentiate the continuous CDF and meet the probability "
                 "density function."
        ):
            self.play(Create(axes), Write(x_axis_lab), run_time=0.7)
            self.play(Create(seg1), run_time=0.6)
            self.play(Create(jump1), run_time=0.3)
            self.play(Create(seg2), run_time=0.5)
            self.play(Create(jump2), run_time=0.3)
            self.play(Create(seg3), run_time=0.5)
            self.play(Create(jump3), run_time=0.3)
            self.play(Create(seg4), run_time=0.5)

        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
