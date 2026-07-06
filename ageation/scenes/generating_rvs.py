# derived_from: content/33-generating-rvs-script.md
# derived_from_sha256: 05c7c7b25ad17dd34aeece65a768e9a5d758de48e889bcd819c49b3865727ce1
"""Chapter 9, Video 3 -- Generating Random Variables.

Source notes : derived_distributions.tex (Section 9.3, both subsections) --
               the probability integral transform, the inverse-CDF method,
               the exponential recipe, and discrete binning.
Script        : content/33-generating-rvs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/generating_rvs.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import math
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
    section_title,
    make_pmf_chart,
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


# Hardcoded uniform draws -- NO runtime randomness (STYLE_BOOK / lint).
Y_DRAWS = [0.13, 0.42, 0.58, 0.77, 0.31, 0.91, 0.24, 0.66]
# Their images under the exponential(1) inverse CDF, x = -log(1 - y).
X_DRAWS = [-math.log(1.0 - y) for y in Y_DRAWS]


def cdf_plot(x_len=5.2, y_len=3.2):
    """The exponential(1) CDF on labelled axes -- the shared figure of the
    continuous half of this video.

    Returns (group, axes, curve); the group is (axes, x_lab, y_lab, curve).
    """
    axes = Axes(
        x_range=[0, 4.4, 1],
        y_range=[0, 1.1, 0.5],
        x_length=x_len,
        y_length=y_len,
        axis_config={"include_numbers": True, "font_size": 30},
        tips=False,
    )
    curve = axes.plot(lambda x: 1 - math.exp(-x), x_range=[0, 4.4],
                      color=BAR, stroke_width=3.5)
    x_lab = axes.get_x_axis_label(
        MathTex("x", font_size=BODY), edge=RIGHT,
        direction=DOWN + RIGHT, buff=0.25)
    y_lab = axes.get_y_axis_label(MathTex(r"F_X(x)", font_size=BODY))
    group = VGroup(axes, x_lab, y_lab, curve)
    mark_intended_overlap(axes, curve,
                          reason="the CDF curve is drawn on its own axes")
    fit_to_frame(group)
    return group, axes, curve


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Generating Random Variables",
            ["Turn one Uniform(0,1) routine into a generator for",
             "any distribution - invert the CDF, or bin it."],
            kicker="Chapter 9  ·  Functions and Derived Distributions",
        )
        tag = progress_tag(3, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Any X, through its own CDF, is uniform",
                 font_size=BODY, color=INK),
            Text("2.  The inverse-CDF method", font_size=BODY, color=INK),
            Text("3.  A worked recipe: the exponential",
                 font_size=BODY, color=INK),
            Text("4.  Discrete targets: bins", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="Our newest tool is the change-of-variables formula: pass "
                 "a continuous random variable through a smooth monotone "
                 "function, and the density transforms by the slope. This "
                 "video points that formula at one special function, the "
                 "CDF itself, and theory becomes an algorithm."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.55)
        fit_to_frame(outline)

        with self.voiceover(
            text="First, feeding any continuous random variable through "
                 "its own CDF flattens it to a uniform."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Then we run the map backwards: the inverse CDF turns "
                 "uniform draws into any distribution we want,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="we work the recipe end to end for the exponential,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and a binning trick handles discrete targets too. That "
                 "closes chapter nine: derive forward, generate backward."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UniformFromCDF(VoiceoverScene):
    """Beat: uniform-from-cdf -- F_X(X) is Uniform(0,1)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Uniform from Anything")
        fit_to_frame(title)

        # The engineering problem: three wants vs the one primitive.
        wants = VGroup(
            Text("exponential arrival times", font_size=SMALL, color=MUTED),
            Text("Gaussian noise", font_size=SMALL, color=MUTED),
            Text("discrete packet counts", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.3)
        primitive_note = Text("the only primitive:",
                              font_size=CAPTION, color=MUTED)
        primitive = MathTex(r"Y \sim \text{Uniform}(0, 1)",
                            font_size=BODY, color=ACCENT)
        problem = VGroup(wants, primitive_note, primitive)
        problem.arrange(DOWN, buff=0.45)

        with self.voiceover(
            text="Start with the engineering problem. Simulations need "
                 "random variables of every shape: exponential arrival "
                 "times, Gaussian noise, discrete packet counts. But the "
                 "computer offers exactly one primitive, a routine that "
                 "returns a value uniformly distributed between zero and "
                 "one. The goal of this video is to manufacture everything "
                 "else from that single routine."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.7)
            problem.next_to(title, DOWN, buff=0.6)
            fit_to_frame(problem)
            self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.3)
                                    for w in wants],
                                  lag_ratio=0.3), run_time=1.5)
            self.play(FadeIn(primitive_note), run_time=0.5)
            self.play(Write(primitive), run_time=0.9)

        self.wait(0.3)

        # Two-column layout: the CDF figure left, the derivation right.
        plot, axes, curve = cdf_plot()
        plot.move_to(LEFT * 3.3 + DOWN * 0.9)

        y_def = MathTex(r"Y = F_X(X)", font_size=BODY)
        chain1 = MathTex(
            r"f_Y(y) = \frac{f_X(x)}"
            r"{\left| \frac{dF_X}{dx}(x) \right|}",
            font_size=SMALL,
        )
        chain2 = MathTex(r"= \frac{f_X(x)}{f_X(x)}", "=", "1",
                         font_size=SMALL)
        chain = VGroup(chain1, chain2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)

        slab_line = Line(LEFT * 1.3, RIGHT * 1.3, color=MUTED,
                         stroke_width=2)
        slab_rect = Rectangle(width=2.6, height=0.7, fill_color=BAR,
                              fill_opacity=0.35, stroke_color=BAR,
                              stroke_width=2)
        slab_rect.next_to(slab_line.get_center(), UP, buff=0)
        slab_label = MathTex(r"f_Y(y) = 1", font_size=SMALL, color=INK)
        slab_label.move_to(slab_rect)
        tick0 = MathTex("0", font_size=CAPTION, color=MUTED)
        tick0.next_to(slab_line.get_start(), DOWN, buff=0.15)
        tick1 = MathTex("1", font_size=CAPTION, color=MUTED)
        tick1.next_to(slab_line.get_end(), DOWN, buff=0.15)
        slab = VGroup(slab_line, slab_rect, slab_label, tick0, tick1)
        mark_intended_overlap(slab_line, slab_rect, slab_label,
                              reason="the flat density slab stands on its "
                                     "baseline with its label inside")
        outside = MathTex(r"0 \leq F_X(x) \leq 1",
                          font_size=CAPTION, color=MUTED)

        takeaway = MathTex(r"F_X(X) \sim \text{Uniform}(0, 1)",
                           font_size=BODY, color=INK)

        column = VGroup(y_def, chain, VGroup(slab, outside).arrange(
            DOWN, buff=0.25), takeaway)
        column.arrange(DOWN, buff=0.4)
        column.move_to(RIGHT * 3.5 + DOWN * 0.35)
        fit_to_frame(column)

        with self.voiceover(
            text="Here is the observation that unlocks it. Take any "
                 "continuous random variable X with an invertible CDF, and "
                 "feed X into its own CDF: define Y equals F of X."
        ):
            self.play(FadeOut(problem), run_time=0.5)
            self.play(Create(axes), Write(plot[1]), Write(plot[2]),
                      run_time=1.0)
            self.play(Create(curve), run_time=1.0)
            self.play(Write(y_def), run_time=0.8)
            self.play(y_def.animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="On the support of X, the CDF is differentiable and "
                 "strictly increasing, and its derivative is the density "
                 "itself. So last video's formula applies: the density of "
                 "Y is the density of X divided by the absolute derivative "
                 "of the CDF, and that is f of x over f of x, which is one."
        ):
            self.play(y_def.animate.set_color(INK), run_time=0.4)
            self.play(Write(chain1), run_time=1.2)
            self.play(Write(chain2), run_time=1.0)
            self.play(chain2[2].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text="One, for every y between zero and one, and zero outside, "
                 "because a CDF never leaves the unit interval. The bumps "
                 "cancel perfectly. Wherever X is likely, the CDF climbs "
                 "fast and spreads those values out; wherever X is rare, "
                 "the CDF barely moves and packs them together."
        ):
            self.play(chain2[2].animate.set_color(INK), run_time=0.4)
            self.play(Create(slab_line), FadeIn(tick0), FadeIn(tick1),
                      run_time=0.6)
            self.play(GrowFromEdge(slab_rect, DOWN),
                      FadeIn(slab_label), run_time=0.8)
            self.play(FadeIn(outside), run_time=0.5)

        box = SurroundingRectangle(takeaway, color=ACCENT, buff=0.18)

        with self.voiceover(
            text="Every continuous random variable, passed through its own "
                 "CDF, becomes uniform on the unit interval."
        ):
            self.play(Write(takeaway), run_time=0.9)
            self.play(Create(box), run_time=0.5)
            self.play(Indicate(takeaway, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class InverseCDFMethod(VoiceoverScene):
    """Beat: inverse-cdf-method -- the uniform rain."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Inverse-CDF Method")
        fit_to_frame(title)

        plot, axes, curve = cdf_plot()
        plot.move_to(LEFT * 3.3 + DOWN * 0.9)

        with self.voiceover(
            text="If the CDF is a bridge from any distribution to the "
                 "uniform, cross it in the other direction."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.7)
            self.play(Create(axes), Write(plot[1]), Write(plot[2]),
                      run_time=1.0)
            self.play(Create(curve), run_time=1.0)

        # Right column: identity, definition, density chain, boxed recipe.
        id_line = MathTex(r"F_X^{-1}\!\left( F_X(X) \right) = X",
                          font_size=SMALL)
        v_def = MathTex(r"V = F_X^{-1}(Y)", font_size=BODY)
        v_note = MathTex(r"Y \sim \text{Uniform}[0, 1]",
                         font_size=CAPTION, color=MUTED)
        chain1 = MathTex(
            r"f_V(v) = \frac{f_Y(y)}"
            r"{\left| \frac{dF_X^{-1}}{dy}(y) \right|}",
            font_size=SMALL,
        )
        chain2 = MathTex(r"= f_Y(y)\, \frac{dF_X}{dv}(v)", "=", r"f_X(v)",
                         font_size=SMALL)
        chain = VGroup(chain1, chain2).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)
        recipe = MathTex(r"X = F_X^{-1}(Y)", font_size=BODY, color=INK)

        column = VGroup(id_line, VGroup(v_def, v_note).arrange(
            DOWN, buff=0.2), chain, recipe)
        column.arrange(DOWN, buff=0.42)
        column.move_to(RIGHT * 3.5 + DOWN * 0.3)
        fit_to_frame(column)

        with self.voiceover(
            text="When F is invertible, applying the inverse CDF to F of X "
                 "returns X itself. So take Y uniform on the unit interval "
                 "and define V equals F inverse of Y."
        ):
            self.play(Write(id_line), run_time=0.9)
            self.play(Write(v_def), FadeIn(v_note), run_time=1.0)
            self.play(v_def.animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="Derived distributions once more: the density of V is the "
                 "density of Y divided by the derivative of the inverse "
                 "map, which is the density of Y times the derivative of F "
                 "at v. The uniform density is one, so what remains is "
                 "exactly the density of X at v. The variable V has "
                 "precisely the distribution we wanted."
        ):
            self.play(v_def.animate.set_color(INK), run_time=0.4)
            self.play(Write(chain1), run_time=1.2)
            self.play(Write(chain2), run_time=1.0)
            self.play(chain2[2].animate.set_color(ACCENT), run_time=0.5)

        # The uniform rain: hardcoded draws fall down the y-axis, slide to
        # the curve, and drop to the x-axis (the sampler made visible).
        dots = VGroup()
        paths = []
        for y_val, x_val in zip(Y_DRAWS, X_DRAWS):
            dot = Dot(radius=0.07, color=TEAL)
            start = axes.c2p(0, 1.05)
            dot.move_to(start)
            path = VMobject()
            path.set_points_as_corners([
                start,
                axes.c2p(0, y_val),
                axes.c2p(x_val, y_val),
                axes.c2p(x_val, 0),
            ])
            dots.add(dot)
            paths.append(path)

        # Histogram of the landed draws (bins of width 0.5, height per
        # count in axes units) -- grows into the density's shape.
        bin_w = 0.5
        counts = {}
        for x_val in X_DRAWS:
            idx = int(x_val / bin_w)
            counts[idx] = counts.get(idx, 0) + 1
        hist = VGroup()
        for idx, count in sorted(counts.items()):
            left = axes.c2p(idx * bin_w, 0)
            right = axes.c2p((idx + 1) * bin_w, 0)
            top = axes.c2p(0, 0.12 * count)
            rect = Rectangle(
                width=right[0] - left[0],
                height=top[1] - axes.c2p(0, 0)[1],
                fill_color=TEAL, fill_opacity=0.30,
                stroke_color=TEAL, stroke_width=1.5,
            )
            rect.move_to([(left[0] + right[0]) / 2, axes.c2p(0, 0)[1], 0],
                         aligned_edge=DOWN)
            hist.add(rect)
        mark_intended_overlap(
            dots, hist, axes, curve,
            reason="rain dots travel along the axes and curve; the sample "
                   "histogram stands on the x-axis beneath them")

        with self.voiceover(
            text="Watch it work. Uniform draws rain down the vertical "
                 "axis. Each one slides across to the CDF curve and drops "
                 "to the horizontal axis. As draws accumulate, their "
                 "histogram grows into the density of X."
        ):
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots],
                                  lag_ratio=0.08), run_time=0.8)
            self.play(LaggedStart(*[MoveAlongPath(d, p)
                                    for d, p in zip(dots, paths)],
                                  lag_ratio=0.12), run_time=3.6)
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in hist],
                                  lag_ratio=0.15), run_time=1.0)

        steep = Text("steep: dense", font_size=CAPTION, color=MUTED)
        steep.move_to(axes.c2p(2.0, 0.55))
        sparse = Text("shallow: sparse", font_size=CAPTION, color=MUTED)
        sparse.move_to(axes.c2p(3.3, 0.35))

        with self.voiceover(
            text="Where the curve is steep, a wide band of uniform values "
                 "funnels into a narrow interval, so the samples land "
                 "densely, exactly where the density is high. Where the "
                 "curve is shallow, the samples spread thin."
        ) as tracker:
            self.play(FadeIn(steep, shift=UP * 0.2), run_time=0.6)
            self.wait(max(tracker.duration * 0.55 - 0.6, 0.3))
            self.play(FadeIn(sparse, shift=UP * 0.2), run_time=0.6)

        box = SurroundingRectangle(recipe, color=ACCENT, buff=0.18)

        with self.voiceover(
            text="This is the inverse-CDF method: to generate a random "
                 "variable with CDF F, apply F inverse to a uniform draw. "
                 "One uniform routine generates any continuous "
                 "distribution."
        ):
            self.play(chain2[2].animate.set_color(INK), run_time=0.4)
            self.play(Write(recipe), run_time=0.8)
            self.play(Create(box), run_time=0.5)
            self.play(Indicate(recipe, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExponentialRecipe(VoiceoverScene):
    """Beat: exponential-recipe -- X = -log(1 - Y) / lambda, worked."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Worked Recipe: the Exponential")
        fit_to_frame(title)

        target = MathTex(r"X \sim \text{Exponential}(\lambda)",
                         font_size=SMALL, color=MUTED)

        with self.voiceover(
            text="The recipe deserves one full workout. Target: an "
                 "exponential random variable with parameter lambda."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.7)
            target.next_to(title, DOWN, buff=0.5)
            self.play(FadeIn(target, shift=DOWN * 0.2), run_time=0.7)

        cdf_eq = MathTex(r"F_X(x) = 1 - e^{-\lambda x}, \quad x \geq 0",
                         font_size=BODY)
        cdf_eq.next_to(target, DOWN, buff=0.5)

        with self.voiceover(
            text="Its CDF is one minus e to the minus lambda x, for x at "
                 "least zero."
        ):
            self.play(Write(cdf_eq), run_time=1.0)

        inv1 = MathTex(r"y = 1 - e^{-\lambda x}", font_size=SMALL)
        inv2 = MathTex(
            r"F_X^{-1}(y) = -\tfrac{1}{\lambda}\, \log(1 - y)",
            font_size=BODY,
        )
        inv = VGroup(inv1, inv2).arrange(DOWN, buff=0.3)
        inv.next_to(cdf_eq, DOWN, buff=0.5)
        fit_to_frame(inv)

        with self.voiceover(
            text="Inverting is algebra: set y equal to the CDF, solve for "
                 "x, and out comes F inverse of y equals minus one over "
                 "lambda, times the log of one minus y."
        ):
            self.play(Write(inv1), run_time=0.8)
            self.play(Write(inv2), run_time=1.0)
            self.play(inv2.animate.set_color(ACCENT), run_time=0.4)

        recipe = MathTex(r"X = -\tfrac{1}{\lambda}\, \log(1 - Y)",
                         font_size=BODY, color=INK)
        recipe.next_to(title, DOWN, buff=0.55)
        box = SurroundingRectangle(recipe, color=ACCENT, buff=0.18)
        lam_note = MathTex(r"\lambda = 1", font_size=CAPTION, color=MUTED)
        lam_note.next_to(box, RIGHT, buff=0.45)

        with self.voiceover(
            text="So the generator is one line: X equals minus one over "
                 "lambda, times the log of one minus Y. Take lambda equal "
                 "to one to keep the numbers visible."
        ):
            self.play(inv2.animate.set_color(INK), run_time=0.4)
            self.play(FadeOut(target), FadeOut(cdf_eq), FadeOut(inv),
                      run_time=0.6)
            self.play(Write(recipe), run_time=0.9)
            self.play(Create(box), run_time=0.5)
            self.play(FadeIn(lam_note), run_time=0.5)

        # Three of the hardcoded draws animate through the formula onto a
        # waiting-time number line: short, moderate, long.
        rows = VGroup(
            MathTex(r"0.13 \;\to\; 0.14", font_size=SMALL, color=INK),
            MathTex(r"0.42 \;\to\; 0.54", font_size=SMALL, color=INK),
            MathTex(r"0.91 \;\to\; 2.41", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.move_to(LEFT * 3.6 + DOWN * 0.5)
        rows_head = MathTex(r"y \;\to\; -\log(1 - y)",
                            font_size=CAPTION, color=MUTED)
        rows_head.next_to(rows, UP, buff=0.35)

        nline = NumberLine(
            x_range=[0, 3, 1], length=6.4,
            include_numbers=True, font_size=30, color=MUTED,
        )
        nline.move_to(DOWN * 2.4)
        wait_dots = VGroup(*[
            Dot(radius=0.09, color=TEAL).move_to(nline.number_to_point(v))
            for v in (0.14, 0.54, 2.41)
        ])
        mark_intended_overlap(nline, wait_dots,
                              reason="waiting-time markers sit on the "
                                     "number line by design")

        with self.voiceover(
            text="Feed it actual uniform draws. Point one three becomes a "
                 "short wait. Point four two, a moderate one. Point nine "
                 "one, where the logarithm climbs steeply, becomes a long "
                 "one. Small uniforms map to short waits, and draws near "
                 "one stretch deep into the tail."
        ) as tracker:
            self.play(FadeIn(rows_head), Create(nline), run_time=0.8)
            step = max((tracker.duration - 3.2) / 3, 0.4)
            for row, dot in zip(rows, wait_dots):
                self.play(FadeIn(row, shift=RIGHT * 0.3),
                          FadeIn(dot, scale=1.6), run_time=0.7)
                self.wait(step)

        check = MathTex(
            r"f_X(x) = f_Y(y) \Big/ \tfrac{1}{\lambda (1 - y)}", "=",
            r"\lambda e^{-\lambda x}",
            font_size=SMALL,
        )
        check.move_to(RIGHT * 3.3 + DOWN * 0.5)
        fit_to_frame(check)
        closing = Text("draw a uniform, take a logarithm",
                       font_size=CAPTION, color=MUTED)
        closing.next_to(check, DOWN, buff=0.45)

        with self.voiceover(
            text="The change-of-variables formula confirms it: "
                 "differentiating pushes the uniform density to lambda "
                 "times e to the minus lambda x, exactly the exponential "
                 "density. This is how a simulator makes arrivals: draw a "
                 "uniform, take a logarithm, done."
        ):
            self.play(box.animate.set_color(MUTED), run_time=0.4)
            self.play(Write(check), run_time=1.2)
            self.play(check[2].animate.set_color(ACCENT), run_time=0.5)
            self.play(FadeIn(closing), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DiscreteBinning(VoiceoverScene):
    """Beat: discrete-binning -- PMF-sized bins on [0,1], plus the outro."""

    # The worked PMF: masses at x_1, x_2, x_3.
    MASSES = [0.2, 0.5, 0.3]
    BOUNDS = [0.0, 0.2, 0.7, 1.0]  # CDF plateau heights
    BIN_COLORS = [BLUE, TEAL, GREEN]

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Discrete Targets: Bins")
        fit_to_frame(title)

        with self.voiceover(
            text="Discrete targets need one twist, because a staircase CDF "
                 "has no inverse. Bins do the job instead."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.7)

        # Left: the PMF chart. Its bar index k doubles as the value x_k.
        chart, bars = make_pmf_chart(
            [0] + self.MASSES, x_label="x", y_label=r"p_X(x)")
        chart.scale(0.55).move_to(LEFT * 3.5 + DOWN * 1.3)
        heights = MathTex(r"F_X:\;\; 0.2,\;\; 0.7,\;\; 1",
                          font_size=SMALL, color=MUTED)
        # (2026-07-04 draft review, 6:30) snug above the chart and centred
        # on the bars, so the line reads as the chart's header instead of
        # floating between the chart and the formula column.
        heights.next_to(chart, UP, buff=0.3)
        heights.match_x(bars)

        with self.voiceover(
            text="Take a PMF on values x one, x two, x three, with masses "
                 "point two, point five, and point three. Its CDF climbs "
                 "in jumps: point two, then point seven, then one."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.9)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.2), run_time=1.0)
            self.play(Write(heights), run_time=0.9)

        # Right: the unit interval, sliced at the CDF plateau heights.
        # (2026-07-04 draft review, 5:43) the stack sits a bit further
        # right so its boundary tick labels get daylight instead of
        # running under the rectangles.
        base = RIGHT * 3.3 + DOWN * 2.2
        unit_h = 4.0
        bin_rects = VGroup()
        bin_labels = VGroup()
        for i in range(3):
            lo, hi = self.BOUNDS[i], self.BOUNDS[i + 1]
            rect = Rectangle(
                width=0.7, height=(hi - lo) * unit_h,
                fill_color=self.BIN_COLORS[i], fill_opacity=0.35,
                stroke_color=INK, stroke_width=1.5,
            )
            rect.move_to(base + UP * ((lo + hi) / 2 * unit_h))
            bin_rects.add(rect)
            lab = MathTex(r"p_X(x_{" + str(i + 1) + r"})",
                          font_size=CAPTION, color=INK)
            lab.next_to(rect, RIGHT, buff=0.3)
            bin_labels.add(lab)
        # (2026-07-04 draft review, 5:43) anchor the tick labels to the
        # rectangles' LEFT EDGE (base is the stack's centre line, so a
        # buff measured from it landed the numbers under the bins).
        tick_labels = VGroup(*[
            MathTex(s, font_size=CAPTION, color=MUTED)
            .next_to(base + LEFT * 0.35 + UP * (v * unit_h), LEFT,
                     buff=0.25)
            for s, v in zip(("0", "0.2", "0.7", "1"), self.BOUNDS)
        ])
        mark_intended_overlap(
            bin_rects, reason="adjacent bins share their boundary edges")

        with self.voiceover(
            text="Now slice the unit interval at exactly those heights. "
                 "The first bin runs from zero to point two, the second "
                 "from point two to point seven, the third from point "
                 "seven to one. Each bin's length is exactly the mass of "
                 "its value."
        ):
            self.play(LaggedStart(*[GrowFromEdge(r, DOWN)
                                    for r in bin_rects],
                                  lag_ratio=0.3), run_time=1.4)
            self.play(FadeIn(tick_labels), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2)
                                    for l in bin_labels],
                                  lag_ratio=0.25), run_time=1.0)

        rule = MathTex(
            r"g(y) = x_i", r"\;\;\text{if}\;\;",
            r"F_X(x_{i-1}) < y \leq F_X(x_i)",
            font_size=SMALL,
        )
        # (2026-07-04 draft review, 6:30) the formula column rides higher
        # so the chart's F_X header below keeps a clear lane.
        rule.move_to(LEFT * 0.6 + UP * 2.2)
        fit_to_frame(rule)

        with self.voiceover(
            text="The generator is a case statement: draw Y uniform, and "
                 "output x i when Y lands in bin i."
        ):
            self.play(Write(rule), run_time=1.0)
            self.play(rule.animate.set_color(ACCENT), run_time=0.4)

        # Hardcoded draws fall onto the interval; each lights its bin and
        # its output bar.
        drop_specs = [(0.13, 0), (0.42, 1), (0.77, 2)]
        drop_dots = VGroup(*[Dot(radius=0.08, color=INK)
                             for _ in drop_specs])
        mark_intended_overlap(
            drop_dots, bin_rects,
            reason="uniform draws land inside their bins by design")

        with self.voiceover(
            text="Watch the draws fall. Point one three lands in the "
                 "first bin: output x one. Point four two, second bin: x "
                 "two. Point seven seven, third bin: x three."
        ) as tracker:
            self.play(rule.animate.set_color(INK), run_time=0.4)
            step = max((tracker.duration - 4.6) / 3, 0.2)
            for dot, (y_val, i) in zip(drop_dots, drop_specs):
                dot.move_to(base + UP * (unit_h + 0.55))
                self.play(FadeIn(dot, scale=1.4), run_time=0.3)
                self.play(dot.animate.move_to(base + UP * (y_val * unit_h)),
                          run_time=0.5)
                self.play(Indicate(bin_rects[i], color=ACCENT,
                                   scale_factor=1.02),
                          Indicate(bars[i], color=ACCENT,
                                   scale_factor=1.03),
                          run_time=0.7)
                self.wait(step)

        why = MathTex(
            pr(r"X = x_i"), "=",
            r"F_X(x_i) - F_X(x_{i-1})", "=", r"p_X(x_i)",
            font_size=SMALL,
        )
        why.next_to(rule, DOWN, buff=0.45)
        fit_to_frame(why)

        with self.voiceover(
            text="The probability of outputting x i is the probability "
                 "that a uniform draw lands in its bin, and that is the "
                 "bin's length, F at x i minus F at x i minus one, which "
                 "is exactly the PMF at x i. The video that introduced "
                 "CDFs proved that a discrete CDF's jump heights are the "
                 "probabilities; here the risers become sampling bins."
        ):
            self.play(Write(why), run_time=1.4)
            self.play(why[4].animate.set_color(ACCENT), run_time=0.5)

        caveat = Text("case statements can be slow; better generators exist",
                      font_size=CAPTION, color=MUTED)
        caveat.move_to(DOWN * 3.0)
        fit_to_frame(caveat)

        with self.voiceover(
            text="One caveat: a naive case statement can be slow, and many "
                 "discrete distributions have far more efficient "
                 "generators."
        ):
            self.play(why[4].animate.set_color(INK), run_time=0.4)
            self.play(FadeIn(caveat), run_time=0.7)

        outro = outro_bridge(
            ["The CDF is a two-way bridge: run it forward to derive,",
             "backward to generate from a single uniform routine."],
            next_title="Moment Generating Functions",
        )

        with self.voiceover(
            text="That closes chapter nine. The key idea: the CDF is a "
                 "two-way bridge. Run it forward to derive distributions; "
                 "run it backward to generate them from a single uniform "
                 "routine. Coming up: moment generating functions."
        ):
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
