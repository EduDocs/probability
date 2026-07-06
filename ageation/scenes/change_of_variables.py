# derived_from: content/32-change-of-variables-script.md
# derived_from_sha256: ced9f17c32e04605072d0c1b06bb7ee331f6e7be411524971065f6344215ef53
"""Chapter 9, Video 2 -- The Change-of-Variables Formula.

Source notes : derived_distributions.tex (Section 9.2, "Differentiable
               Functions") -- the f_Y(y) = f_X(x)/|g'(x)| formula, the
               sum over roots, and its worked examples.
Script        : content/32-change-of-variables-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/change_of_variables.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import math
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
    section_title,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


# --- The notes' monotone cubic (Figure: DifferentiablePDF) --------------------

def cubic(x):
    """g(x) = 0.25 (x - 1.75)^3 + 2 -- strictly increasing, one flat stretch."""
    return 0.25 * (x - 1.75) ** 3 + 2.0


def cubic_inv(y):
    t = 4.0 * (y - 2.0)
    return 1.75 + math.copysign(abs(t) ** (1.0 / 3.0), t)


def wavy(x):
    """The notes' piecewise-monotone g for the sum-over-roots figure."""
    return 2.5 + 2.0 * np.sin(2 * np.pi * np.sqrt(x + 0.5)) + 0.4 * x


def delta_strip(axes, y_lo, y_hi):
    """The delta-strip pair: a thin band on the y axis, its pullback interval
    on the x axis, and the dashed guides connecting them through the curve.

    Returns VGroup(y_rect, x_rect, guides).
    """
    x_lo, x_hi = cubic_inv(y_lo), cubic_inv(y_hi)
    a_lo, a_hi = axes.c2p(0, y_lo), axes.c2p(0, y_hi)
    b_lo, b_hi = axes.c2p(x_lo, 0), axes.c2p(x_hi, 0)

    y_rect = Rectangle(
        width=0.14, height=a_hi[1] - a_lo[1],
        fill_color=MAROON, fill_opacity=0.9, stroke_width=0,
    ).move_to([a_lo[0] + 0.09, (a_lo[1] + a_hi[1]) / 2, 0])
    x_rect = Rectangle(
        width=max(b_hi[0] - b_lo[0], 0.08), height=0.14,
        fill_color=MAROON, fill_opacity=0.9, stroke_width=0,
    ).move_to([(b_lo[0] + b_hi[0]) / 2, b_lo[1] + 0.09, 0])

    guides = VGroup(
        DashedLine(a_lo, axes.c2p(x_lo, y_lo), color=MUTED, stroke_width=1.5),
        DashedLine(axes.c2p(x_lo, y_lo), b_lo, color=MUTED, stroke_width=1.5),
        DashedLine(a_hi, axes.c2p(x_hi, y_hi), color=MUTED, stroke_width=1.5),
        DashedLine(axes.c2p(x_hi, y_hi), b_hi, color=MUTED, stroke_width=1.5),
    )
    return VGroup(y_rect, x_rect, guides)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Change-of-Variables Formula",
            ["Skip the integral: a differentiable map takes",
             "the density of X straight to the density of Y."],
            kicker="Chapter 9  ·  Functions and Derived Distributions",
        )
        tag = progress_tag(2, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The formula: density in, density out",
                 font_size=BODY, color=INK),
            Text("2.  An affine Gaussian stays Gaussian",
                 font_size=BODY, color=INK),
            Text("3.  Non-monotone maps: sum over the roots",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video we derived distributions the long way: chase "
                 "the event, integrate to a CDF, then differentiate. This "
                 "video adds a single assumption, differentiability, and "
                 "the integral disappears entirely."
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
            text="First we build the change-of-variables formula, which "
                 "takes the density of X straight to the density of Y, and "
                 "see why the slope of g is the exchange rate between the "
                 "two axes."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Then we let it work: an affine map of a Gaussian stays "
                 "Gaussian,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and when g folds the axis onto itself, every root of g of "
                 "x equals y pays its own share."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class SlopeRescales(VoiceoverScene):
    """Beat: slope-rescales -- invert, differentiate, and the delta strip."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Slope Rescales the Density")
        fit_to_frame(title)

        # Body-size assumption caption + concept reference, not a video
        # number (2026-07-04 draft review, 0:48).
        assume = MathTex(r"g\ \text{differentiable, strictly increasing}",
                         font_size=BODY, color=MUTED)
        assume.move_to(RIGHT * 3.3 + UP * 2.35)
        fit_to_frame(assume)

        with self.voiceover(
            text="Start where last video left off, with one new "
                 "assumption: g is differentiable and strictly increasing."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)
            self.play(FadeIn(assume, shift=RIGHT * 0.3), run_time=0.6)

        inv_line = MathTex(
            r"F_Y(y)", "=", r"F_X\left(g^{-1}(y)\right)",
            font_size=BODY,
        ).move_to(RIGHT * 3.3 + UP * 1.45)
        fit_to_frame(inv_line)

        with self.voiceover(
            text="That buys invertibility. Every y now comes from exactly "
                 "one x, so x equals g inverse of y is a genuine function, "
                 "and last video's formula loses its sup: the CDF of Y at y "
                 "is simply the CDF of X at g inverse of y."
        ):
            self.play(Write(inv_line), run_time=1.2)

        chain = MathTex(
            r"f_Y(y)", "=", r"f_X\left(g^{-1}(y)\right)", r"\frac{dx}{dy}",
            font_size=BODY,
        ).move_to(RIGHT * 3.3 + UP * 0.25)
        fit_to_frame(chain)

        with self.voiceover(
            text="Now differentiate both sides with respect to y. The chain "
                 "rule hands us the density of Y: the density of X at g "
                 "inverse of y, times the derivative of the inverse, the "
                 "rate dx by dy."
        ):
            self.play(Write(chain), run_time=1.2)
            self.play(chain[3].animate.set_color(ACCENT), run_time=0.5)

        # The notes' figure: the monotone cubic and its delta strips.
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 2],
            x_length=5.4,
            y_length=4.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).move_to(LEFT * 3.3 + DOWN * 0.3)  # raised (2026-07-04 review, 1:56)
        curve = axes.plot(cubic, x_range=[0, 4.6, 0.02], color=BAR)
        x_name = axes.get_x_axis_label(
            MathTex("x", font_size=SMALL, color=MUTED),
            edge=RIGHT, direction=DOWN + RIGHT, buff=0.25)
        y_name = axes.get_y_axis_label(
            MathTex(r"y = g(x)", font_size=SMALL, color=MUTED))

        shallow = delta_strip(axes, 1.75, 2.25)
        steep = delta_strip(axes, 5.75, 6.25)
        delta_lab = MathTex(r"\delta", font_size=CAPTION, color=MAROON)
        delta_lab.next_to(shallow[0], LEFT, buff=0.12)
        delta_lab_steep = MathTex(r"\delta", font_size=CAPTION, color=MAROON)
        delta_lab_steep.next_to(steep[0], LEFT, buff=0.12)

        mark_intended_overlap(
            axes, curve, x_name, y_name, shallow, steep,
            delta_lab, delta_lab_steep,
            reason="delta strips and dashed guides ride the curve's axes")

        with self.voiceover(
            text="That derivative is not a technicality; it is the whole "
                 "story. Take a thin strip of width delta on the y axis and "
                 "pull it back through the curve."
        ):
            self.play(Create(axes), FadeIn(x_name), FadeIn(y_name),
                      run_time=0.8)
            self.play(Create(curve), run_time=0.9)
            self.play(FadeIn(shallow[0]), FadeIn(delta_lab), run_time=0.6)

        with self.voiceover(
            text="Where the slope is shallow, the strip pulls back to a "
                 "wide interval of x values, so plenty of probability "
                 "funnels into that band of y."
        ):
            self.play(Create(shallow[2]), run_time=0.8)
            self.play(FadeIn(shallow[1]), run_time=0.6)

        with self.voiceover(
            text="Where the slope is steep, the same strip pulls back to a "
                 "narrow interval, and hardly any probability lands there."
        ):
            self.play(Transform(shallow, steep),
                      Transform(delta_lab, delta_lab_steep), run_time=1.2)

        exchange = Text("the slope is the exchange rate between the axes",
                        font_size=CAPTION, color=MUTED)
        # Centered under the chart it describes (2026-07-04 review, 1:56).
        exchange.move_to(axes.get_center() * RIGHT + DOWN * 2.9)
        fit_to_frame(exchange)

        with self.voiceover(
            text="The derivative is the exchange rate between the two axes. "
                 "Probability is conserved, so the density must be rescaled "
                 "by exactly how much the map stretches the axis."
        ):
            self.play(FadeIn(exchange, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(chain[3], color=ACCENT, scale_factor=1.03),
                      run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChangeOfVariables(VoiceoverScene):
    """Beat: change-of-variables -- both cases, one absolute value."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Change-of-Variables Formula")
        fit_to_frame(title)

        # Body size, matching the equation stack it heads; the stack below
        # is rebalanced around it (2026-07-04 draft review, 2:20).
        sub = MathTex(r"x = g^{-1}(y)", font_size=BODY, color=MUTED)
        sub.move_to(UP * 2.55)

        with self.voiceover(
            text="Substitute x for g inverse of y and the result reads "
                 "cleanly."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)
            self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.6)

        inc = MathTex(
            r"f_Y(y) = \frac{f_X(x)}{\frac{dg}{dx}(x)}",
            font_size=BODY,
        ).move_to(UP * 1.6 + LEFT * 1.4)
        inc_cap = MathTex(r"\text{increasing: slope positive}",
                          font_size=CAPTION, color=MUTED)
        inc_cap.next_to(inc, RIGHT, buff=0.6)

        with self.voiceover(
            text="For a strictly increasing g, the density of Y is the "
                 "density of X divided by the slope of g at x, and the "
                 "slope is positive, so the density stays positive."
        ):
            self.play(Write(inc), run_time=1.1)
            self.play(FadeIn(inc_cap), run_time=0.5)

        dec = VGroup(
            MathTex(r"F_Y(y) = 1 - F_X\left(g^{-1}(y)\right)",
                    font_size=SMALL, color=MUTED),
            MathTex(r"f_Y(y) = \frac{f_X(x)}{-\frac{dg}{dx}(x)}",
                    font_size=SMALL, color=MUTED),
        ).arrange(RIGHT, buff=0.9).move_to(UP * 0.45)
        fit_to_frame(dec)

        with self.voiceover(
            text="What if g is strictly decreasing? Then g of X at most y "
                 "means X at least g inverse of y, so the CDF picks up a "
                 "one minus, and differentiating produces a minus sign, "
                 "exactly cancelling the sign of the now negative slope."
        ):
            self.play(Write(dec[0]), run_time=0.9)
            self.play(Write(dec[1]), run_time=0.9)

        combined = MathTex(
            r"f_Y(y) = f_X\left(g^{-1}(y)\right)\left|\frac{dx}{dy}\right|"
            r" = \frac{f_X(x)}{\left|\frac{dg}{dx}(x)\right|}",
            font_size=BODY, color=ACCENT,
        ).move_to(DOWN * 0.85)
        fit_to_frame(combined)

        with self.voiceover(
            text="One absolute value absorbs both cases. When g is "
                 "differentiable and strictly monotone, the density of Y at "
                 "y is the density of X at x, divided by the absolute value "
                 "of the derivative of g, with x equal to g inverse of y. "
                 "This is the change-of-variables formula, the workhorse of "
                 "derived distributions."
        ):
            self.play(inc.animate.set_color(MUTED),
                      inc_cap.animate.set_opacity(0.6), run_time=0.5)
            self.play(Write(combined), run_time=1.4)

        recipe = Text("invert, differentiate, divide",
                      font_size=CAPTION, color=MUTED)
        recipe.next_to(combined, DOWN, buff=0.3)

        with self.voiceover(
            text="The recipe now has just three moves: invert, "
                 "differentiate, and divide."
        ):
            self.play(FadeIn(recipe, shift=UP * 0.2), run_time=0.6)

        ray = MathTex(
            r"f_Y(y) = \frac{f_X(\sqrt{y})}"
            r"{\left|\frac{dg}{dx}(\sqrt{y})\right|}"
            r" = \frac{\sqrt{y}}{2\sqrt{y}}\, e^{-y/2}",
            r"= \frac{1}{2}\, e^{-y/2}",
            font_size=SMALL,
        ).move_to(DOWN * 2.25)
        fit_to_frame(ray)
        # Concept reference, not a video number (2026-07-04 review, 3:24).
        ray_cap = Text("last video's Rayleigh energy: one line, same exponential",
                       font_size=CAPTION, color=MUTED)
        ray_cap.next_to(ray, DOWN, buff=0.25)
        fit_to_frame(ray_cap)

        with self.voiceover(
            text="It even collapses last video's channel fading example. "
                 "The Rayleigh amplitude squared took an integral there; "
                 "here it takes one line, and the algebra folds down to one "
                 "half e to the minus y over two. Same exponential, no "
                 "integral."
        ):
            # The recipe caption's moment has passed; it was overlapping
            # the Rayleigh line (2026-07-04 draft review, 3:24).
            self.play(combined.animate.set_color(INK),
                      FadeOut(recipe), run_time=0.4)
            self.play(Write(ray), run_time=1.2)
            self.play(ray[1].animate.set_color(ACCENT),
                      FadeIn(ray_cap), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GaussianAffine(VoiceoverScene):
    """Beat: gaussian-affine -- an affine map never leaves the family."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("An Affine Gaussian Stays Gaussian")
        fit_to_frame(title)

        with self.voiceover(
            text="Time to let the formula work."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        r1 = VGroup(
            MathTex(r"f_X(x) = \frac{e^{-x^2/2}}{\sqrt{2\pi}}",
                    font_size=SMALL),
            MathTex(r"Y = aX + b,\quad a \neq 0", font_size=SMALL),
        ).arrange(RIGHT, buff=1.1).move_to(UP * 2.35)
        fit_to_frame(r1)

        axes = Axes(
            x_range=[-4, 6, 1],
            y_range=[0, 0.5, 0.25],
            x_length=7.2,
            y_length=2.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).to_edge(DOWN, buff=0.85)
        bell0 = axes.plot(
            lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi),
            x_range=[-4, 4], color=BAR)
        bell1 = axes.plot(
            lambda x: math.exp(-(x - 2) ** 2 / 4.5) / (math.sqrt(2 * math.pi) * 1.5),
            x_range=[-3, 6], color=BAR)
        lab0 = MathTex(r"\mu = 0,\ \sigma = 1",
                       font_size=CAPTION, color=MUTED)
        lab0.move_to(axes.c2p(-2.6, 0.42))
        # No bare "bell" on screen (2026-07-04 draft review, 4:20).
        lab1 = MathTex(r"\text{still Gaussian: } \mu = b,\ \sigma = \left|a\right|",
                       font_size=CAPTION, color=MUTED)
        lab1.move_to(axes.c2p(-2.45, 0.42))  # clear of the y axis line
        mean_line = DashedLine(axes.c2p(2, 0), axes.c2p(2, 0.26),
                               color=MUTED, stroke_width=1.5)
        mark_intended_overlap(
            axes, bell0, bell1, lab0, lab1, mean_line,
            reason="bell curve, its labels, and the mean line share the axes")

        with self.voiceover(
            text="Let X be a standard Gaussian, the bell curve with density "
                 "e to the minus x squared over two, divided by the square "
                 "root of two pi. Let Y equal a X plus b, an amplification "
                 "and an offset, with a nonzero."
        ):
            self.play(Write(r1[0]), run_time=0.9)
            self.play(Write(r1[1]), run_time=0.8)
            self.play(Create(axes), run_time=0.6)
            self.play(Create(bell0), FadeIn(lab0), run_time=1.0)

        r2 = MathTex(
            r"g^{-1}(y) = \frac{y - b}{a},\qquad \frac{dx}{dy} = \frac{1}{a}",
            font_size=SMALL,
        ).move_to(UP * 1.5)
        fit_to_frame(r2)

        with self.voiceover(
            text="The map is affine, so inverting it is arithmetic: x "
                 "equals y minus b, over a, and dx by dy is one over a."
        ):
            self.play(Write(r2), run_time=1.0)

        r3 = MathTex(
            r"f_Y(y) = f_X\!\left(\frac{y-b}{a}\right)"
            r"\frac{1}{\left|a\right|}",
            font_size=SMALL,
        ).move_to(UP * 0.7)
        fit_to_frame(r3)

        with self.voiceover(
            text="Feed both into the formula. The density of Y is the "
                 "standard density evaluated at y minus b over a, divided by "
                 "the absolute value of a."
        ):
            self.play(Write(r3), run_time=1.0)

        r4 = MathTex(
            r"f_Y(y) = \frac{1}{\sqrt{2\pi}\,\left|a\right|}\,"
            r" e^{-\frac{(y-b)^2}{2a^2}}",
            font_size=BODY, color=ACCENT,
        ).move_to(DOWN * 0.35)
        fit_to_frame(r4)

        with self.voiceover(
            text="Simplify, and look at what came out: a Gaussian with mean "
                 "b and standard deviation the absolute value of a."
        ):
            self.play(Write(r4), run_time=1.2)

        with self.voiceover(
            text="The density shifts by b and stretches by a, but the "
                 "silhouette never changes. Only the labels move. The same "
                 "progression works for any Gaussian input: an affine "
                 "function of a Gaussian random variable remains Gaussian. "
                 "Amplify a noisy channel, add an offset, and the noise "
                 "keeps its distribution."
        ):
            self.play(Transform(bell0, bell1),
                      Transform(lab0, lab1), run_time=1.4)
            self.play(Create(mean_line), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class SumOverRoots(VoiceoverScene):
    """Beat: sum-over-roots -- piecewise monotone g and the cosine pile-up."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Sum over the Roots")
        fit_to_frame(title)

        with self.voiceover(
            text="Monotone maps are the friendly case."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        axes_w = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 2],
            x_length=5.2,
            y_length=4.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).move_to(LEFT * 3.3 + DOWN * 0.55)
        wcurve = axes_w.plot(wavy, x_range=[0, 5, 0.02], color=BAR)
        wx_name = axes_w.get_x_axis_label(
            MathTex("x", font_size=SMALL, color=MUTED),
            edge=RIGHT, direction=DOWN + RIGHT, buff=0.25)
        wy_name = axes_w.get_y_axis_label(
            MathTex(r"g(x)", font_size=SMALL, color=MUTED))

        with self.voiceover(
            text="A real g can wander: rise, fall, rise again. As long as "
                 "it is differentiable with finitely many local extrema, it "
                 "is monotone piece by piece."
        ):
            self.play(Create(axes_w), FadeIn(wx_name), FadeIn(wy_name),
                      run_time=0.8)
            self.play(Create(wcurve), run_time=1.1)

        level_y = 4.0
        roots_x = [0.71, 1.54, 3.52]
        level = DashedLine(axes_w.c2p(0, level_y), axes_w.c2p(5, level_y),
                           color=MUTED, stroke_width=1.5)
        level_lab = MathTex("y", font_size=CAPTION, color=MUTED)
        level_lab.next_to(axes_w.c2p(0, level_y), LEFT, buff=0.18)
        root_dots = VGroup(*[
            Dot(axes_w.c2p(rx, level_y), radius=0.07, color=MAROON)
            for rx in roots_x
        ])
        drops = VGroup(*[
            DashedLine(axes_w.c2p(rx, level_y), axes_w.c2p(rx, 0),
                       color=MUTED, stroke_width=1.5)
            for rx in roots_x
        ])
        mark_intended_overlap(
            axes_w, wcurve, wx_name, wy_name, level, level_lab,
            root_dots, drops,
            reason="the level line and root drops ride the wavy curve")

        with self.voiceover(
            text="So pick a level y and collect every x where g of x "
                 "equals y. Each root sits on its own monotone piece, and "
                 "each piece obeys the formula we just built."
        ):
            self.play(Create(level), FadeIn(level_lab), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in root_dots],
                                  lag_ratio=0.25), run_time=0.8)
            self.play(LaggedStart(*[Create(d) for d in drops],
                                  lag_ratio=0.25), run_time=0.9)

        fsum = MathTex(
            r"f_Y(y)", "=",
            r"\sum_{\{x \,\mid\, g(x) = y\}}"
            r" \frac{f_X(x)}{\left|\frac{dg}{dx}(x)\right|}",
            font_size=BODY, color=ACCENT,
        ).move_to(RIGHT * 3.4 + UP * 1.5)
        fit_to_frame(fsum)

        with self.voiceover(
            text="Add the contributions: the density of Y at y is the sum, "
                 "over all roots, of the density of X at that root divided "
                 "by the absolute value of the slope there. The discrete "
                 "world summed masses over the same preimage; densities do "
                 "the same, with the stretch factor that masses never "
                 "needed."
        ):
            self.play(Write(fsum), run_time=1.4)

        # --- the cosine example: two roots per level ---------------------
        self.play(FadeOut(VGroup(axes_w, wcurve, wx_name, wy_name, level,
                                 level_lab, root_dots, drops)),
                  fsum.animate.set_color(MUTED), run_time=0.6)

        two_pi = 2 * math.pi
        axes_c = Axes(
            x_range=[0, 6.6, 1],
            y_range=[-1.4, 1.4, 1],
            x_length=5.6,
            y_length=3.2,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).move_to(LEFT * 3.3 + DOWN * 0.9)
        ccurve = axes_c.plot(np.cos, x_range=[0, two_pi, 0.02], color=BAR)
        pi_labels = VGroup(
            MathTex("0", font_size=CAPTION, color=MUTED)
            .move_to(axes_c.c2p(0.12, -0.28)),
            MathTex(r"\pi", font_size=CAPTION, color=MUTED)
            .move_to(axes_c.c2p(math.pi, -0.28)),
            MathTex(r"2\pi", font_size=CAPTION, color=MUTED)
            .move_to(axes_c.c2p(two_pi - 0.18, -0.32)),
        )
        phase_dots = VGroup(*[
            Dot(axes_c.c2p((k + 0.5) * two_pi / 12, 0),
                radius=0.05, color=TEAL)
            for k in range(12)
        ])

        y0 = 0.4
        rts = [math.acos(y0), two_pi - math.acos(y0)]
        level_c = DashedLine(axes_c.c2p(0, y0), axes_c.c2p(two_pi, y0),
                             color=MUTED, stroke_width=1.5)
        root_dots_c = VGroup(*[
            Dot(axes_c.c2p(rx, y0), radius=0.07, color=MAROON)
            for rx in rts
        ])
        drops_c = VGroup(*[
            DashedLine(axes_c.c2p(rx, y0), axes_c.c2p(rx, -1.4),
                       color=MUTED, stroke_width=1.5)
            for rx in rts
        ])
        root_labels = VGroup(
            MathTex(r"\arccos(y)", font_size=CAPTION, color=MUTED),
            MathTex(r"2\pi - \arccos(y)", font_size=CAPTION, color=MUTED),
        )
        for lab, rx in zip(root_labels, rts):
            lab.next_to(axes_c.c2p(rx, -1.4), DOWN, buff=0.22)
        mark_intended_overlap(
            axes_c, ccurve, pi_labels, phase_dots, level_c, root_dots_c,
            drops_c, root_labels,
            reason="the level line and root drops ride the cosine")

        with self.voiceover(
            text="Watch it in action. Sample a sinusoid at a random phase: "
                 "X is uniform between zero and two pi, and Y equals the "
                 "cosine of X."
        ):
            self.play(Create(axes_c), FadeIn(pi_labels), run_time=0.7)
            self.play(Create(ccurve), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in phase_dots],
                                  lag_ratio=0.05), run_time=0.9)

        with self.voiceover(
            text="For y strictly between minus one and one, the level line "
                 "cuts the cosine twice: once at arc cosine of y, and once "
                 "at two pi minus arc cosine of y."
        ):
            self.play(Create(level_c), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, scale=1.6)
                                    for d in root_dots_c],
                                  lag_ratio=0.3), run_time=0.7)
            self.play(LaggedStart(*[Create(d) for d in drops_c],
                                  lag_ratio=0.3),
                      FadeIn(root_labels), run_time=0.9)

        deriv = MathTex(r"\frac{d}{dx}\cos(x) = -\sin(x)",
                        font_size=SMALL).move_to(RIGHT * 3.4 + UP * 0.1)
        fit_to_frame(deriv)
        result = MathTex(
            r"f_Y(y)", "=", r"\frac{1}{\pi \sqrt{1 - y^2}}",
            font_size=BODY, color=ACCENT,
        ).move_to(RIGHT * 3.4 + DOWN * 1.1)
        fit_to_frame(result)

        with self.voiceover(
            text="The derivative of cosine is minus sine, and at both roots "
                 "its magnitude is the square root of one minus y squared. "
                 "Each root contributes one over two pi times that root; "
                 "together they give one over pi square root of one minus y "
                 "squared."
        ):
            self.play(Write(deriv), run_time=0.9)
            self.play(Write(result), run_time=1.2)

        # --- the U-shaped arcsine density --------------------------------
        self.play(FadeOut(VGroup(axes_c, ccurve, pi_labels, phase_dots,
                                 level_c, root_dots_c, drops_c,
                                 root_labels)),
                  run_time=0.6)

        axes_u = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[0, 2.2, 1],
            x_length=5.4,
            y_length=3.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).move_to(LEFT * 3.3 + DOWN * 0.55)  # raised (2026-07-04 review, 6:25)
        # The arcsine density blows up at y = +-1: clip the plot range
        # slightly inside the singular endpoints, and sample FINELY -- a
        # 2-element x_range inherits the axes' step (1.0 here), which is
        # what made the steep arms jagged (2026-07-05 review, 6:19).
        ucurve = axes_u.plot(
            lambda y: 1.0 / (math.pi * math.sqrt(1.0 - y * y)),
            x_range=[-0.985, 0.985, 0.005], color=BAR)
        walls = VGroup(
            DashedLine(axes_u.c2p(-1, 0), axes_u.c2p(-1, 2.0),
                       color=MUTED, stroke_width=1.5),
            DashedLine(axes_u.c2p(1, 0), axes_u.c2p(1, 2.0),
                       color=MUTED, stroke_width=1.5),
        )
        u_labels = VGroup(
            MathTex("-1", font_size=CAPTION, color=MUTED),
            MathTex("1", font_size=CAPTION, color=MUTED),
        )
        u_labels[0].next_to(axes_u.c2p(-1, 0), DOWN, buff=0.22)
        u_labels[1].next_to(axes_u.c2p(1, 0), DOWN, buff=0.22)
        uy_name = axes_u.get_y_axis_label(
            MathTex(r"f_Y(y)", font_size=SMALL, color=MUTED))
        mark_intended_overlap(
            axes_u, ucurve, walls, u_labels, uy_name,
            reason="the density walls and endpoint labels ride the axes")

        with self.voiceover(
            text="Plot it and the shape is striking: a U. The density piles "
                 "up near plus and minus one, because the cosine lingers "
                 "near its peaks. Shallow slope, wide pullback, heaped "
                 "probability: the exchange rate at work."
        ):
            self.play(Create(axes_u), FadeIn(uy_name), FadeIn(u_labels),
                      run_time=0.7)
            self.play(Create(ucurve), run_time=1.0)
            self.play(LaggedStart(*[Create(w) for w in walls],
                                  lag_ratio=0.3), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["A differentiable map turns densities into densities:",
             "divide by the slope, and sum over the roots."],
            next_title="Generating Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video: a differentiable map turns "
                 "densities into densities. Divide by the slope, and sum "
                 "over the roots. Next we aim this machinery at the CDF "
                 "itself and turn it into a recipe for generating random "
                 "variables."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
