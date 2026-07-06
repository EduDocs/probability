# derived_from: content/28-uniform-gaussian-script.md
# derived_from_sha256: 44df9243b436e1eded0cb767af8600adcf678341a6770f55bc13b1481120c6b2
"""Chapter 8, Video 3 -- The Uniform and Gaussian Distributions.

Source notes : 28-uniform-gaussian.tex (Sections 8.4.1-8.4.2) -- the uniform
               density and ramp CDF, the Gaussian density, standardization and
               Phi, the noisy channel, and the polar normalization trick.
Script        : content/28-uniform-gaussian-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/uniform_gaussian.py ChapterOverview
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
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


def gauss(m, s):
    """The Gaussian density with parameters m and sigma, as a plottable."""
    return lambda x: np.exp(-((x - m) ** 2) / (2 * s * s)) / (
        np.sqrt(2 * np.pi) * s)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Uniform and Gaussian Distributions",
            ["The flat uniform, where probability is a length ratio, and the",
             "Gaussian density, where one tabulated curve answers every question."],
            kicker="Chapter 8  ·  Continuous Random Variables",
        )
        tag = progress_tag(3, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The uniform distribution", font_size=BODY, color=INK),
            Text("2.  The Gaussian and standardization",
                 font_size=BODY, color=INK),
            Text("3.  A noisy channel, and why the area is one",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video built the machinery of the continuous world: "
                 "densities that we integrate for probability, and "
                 "expectations that are integrals too. Now we start the "
                 "catalog of distributions worth knowing by name."
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
            text="First, the flattest density of all, the uniform: equal "
                 "lengths, equal probabilities, and a wait for the bus "
                 "computed honestly."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Then the most important one, the Gaussian density, and the "
                 "standardization trick that routes every question through "
                 "a single tabulated curve."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Finally, two payoffs: a noisy channel whose error rate is "
                 "a tail probability, and the classic polar trick that "
                 "proves the Gaussian is a density at all."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UniformDistribution(VoiceoverScene):
    """Beat: uniform -- flat shelf, ramp CDF, and the bus-stop wait."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Uniform Distribution")
        fit_to_frame(title)

        axes = Axes(
            x_range=[-0.5, 5, 1],
            y_range=[0, 1.25, 0.25],
            x_length=8.0,
            y_length=3.0,
            tips=False,
            axis_config={"include_numbers": False},
        )
        # Chart rides higher so the length-ratio caption gets a clear lane
        # beneath it (2026-07-04 draft review, 1:40).
        axes.to_edge(DOWN, buff=1.9)
        x_name = MathTex("x", font_size=BODY, color=MUTED)
        x_name.next_to(axes.x_axis.get_end(), DOWN + RIGHT, buff=0.25)

        def shelf(a, b, h):
            """Flat uniform PDF on [a, b] with its area shaded."""
            bl = axes.c2p(a, 0)
            tr = axes.c2p(b, h)
            area = Polygon(
                bl, [tr[0], bl[1], 0], tr, [bl[0], tr[1], 0],
                fill_color=BAR, fill_opacity=0.25, stroke_width=0,
            )
            top = Line(axes.c2p(a, h), axes.c2p(b, h),
                       color=INK, stroke_width=3.5)
            ld = DashedLine(axes.c2p(a, 0), axes.c2p(a, h),
                            color=MUTED, stroke_width=2)
            rd = DashedLine(axes.c2p(b, 0), axes.c2p(b, h),
                            color=MUTED, stroke_width=2)
            g = VGroup(area, top, ld, rd)
            mark_intended_overlap(axes, g,
                                  reason="the density sits on the axes")
            return g

        def stage_labels(right, h, h_tex):
            zero = MathTex("0", font_size=CAPTION, color=MUTED)
            zero.next_to(axes.c2p(0, 0), DOWN, buff=0.2)
            edge = MathTex(str(right), font_size=CAPTION, color=MUTED)
            edge.next_to(axes.c2p(right, 0), DOWN, buff=0.2)
            hgt = MathTex(h_tex, font_size=CAPTION, color=MUTED)
            hgt.next_to(axes.c2p(0, h), LEFT, buff=0.15)
            return VGroup(zero, edge, hgt)

        with self.voiceover(
            text="The uniform random variable is the fair spinner of the "
                 "continuum: within its support, intervals of the same "
                 "length are equally probable."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        f_formula = MathTex(
            r"f_X(x)", "=", r"\frac{1}{b - a}, \quad x \in [a, b]",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(f_formula)

        s_def = shelf(1, 4, 1 / 3)
        a_lab = MathTex("a", font_size=CAPTION, color=MUTED)
        a_lab.next_to(axes.c2p(1, 0), DOWN, buff=0.2)
        b_lab = MathTex("b", font_size=CAPTION, color=MUTED)
        b_lab.next_to(axes.c2p(4, 0), DOWN, buff=0.2)
        h_lab = MathTex(r"\tfrac{1}{b-a}", font_size=CAPTION, color=MUTED)
        h_lab.next_to(axes.c2p(0, 1 / 3), LEFT, buff=0.15)

        with self.voiceover(
            text="Its density is a flat shelf. Two parameters, a and b, "
                 "mark the edges of the support, and the height is one over "
                 "b minus a, whatever makes the total area equal one."
        ):
            self.play(Write(f_formula), run_time=1.2)
            self.play(f_formula[0].animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(axes), FadeIn(x_name), run_time=0.9)
            self.play(FadeIn(s_def), FadeIn(a_lab), FadeIn(b_lab),
                      FadeIn(h_lab), run_time=0.9)

        # BODY-sized: the invariant is the point of the whole sequence
        # (2026-07-04 draft review, 1:20).
        area_cap = MathTex(r"\text{area} = 1", font_size=BODY, color=MUTED)
        area_cap.move_to(axes.c2p(4.1, 1.1))
        stages = [
            (shelf(0, 1, 1.0), stage_labels(1, 1.0, "1")),
            (shelf(0, 2, 0.5), stage_labels(2, 0.5, r"\tfrac{1}{2}")),
            (shelf(0, 4, 0.25), stage_labels(4, 0.25, r"\tfrac{1}{4}")),
        ]

        with self.voiceover(
            text="Watch the trade-off. On an interval of length one, the "
                 "shelf has height one. Stretch the support to length two, "
                 "and the shelf drops to one half. Stretch it to four, and "
                 "it drops to one quarter. Wider means shorter, with the "
                 "area pinned at one."
        ):
            s1, l1 = stages[0]
            self.play(FadeOut(a_lab), FadeOut(b_lab), FadeOut(h_lab),
                      Transform(s_def, s1), FadeIn(l1), FadeIn(area_cap),
                      run_time=1.0)
            lbls = l1
            for s_next, l_next in stages[1:]:
                self.wait(0.6)
                self.play(Transform(s_def, s_next),
                          Transform(lbls, l_next), run_time=1.0)

        ramp = VGroup(
            Line(axes.c2p(0, 0), axes.c2p(4, 1), color=INK, stroke_width=3.5),
            Line(axes.c2p(4, 1), axes.c2p(5, 1), color=INK, stroke_width=3.5),
        )
        mark_intended_overlap(axes, ramp,
                              reason="the CDF ramp sits on the axes")
        cdf_lbls = stage_labels(4, 1.0, "1")
        F_formula = MathTex(
            r"F_X(x)", "=", r"\frac{x - a}{b - a}, \quad a \le x \le b",
            font_size=BODY,
        ).move_to(f_formula)
        fit_to_frame(F_formula)

        with self.voiceover(
            text="The CDF is just as plain: zero before a, one after b, and "
                 "in between a straight line climbing at a constant rate."
        ):
            self.play(FadeOut(s_def), FadeOut(area_cap),
                      Transform(lbls, cdf_lbls),
                      ReplacementTransform(f_formula, F_formula),
                      run_time=0.9)
            self.play(F_formula[0].animate.set_color(ACCENT),
                      Create(ramp), run_time=1.0)

        ratio_cap = Text("probability = length of piece / length of support",
                         font_size=CAPTION, color=MUTED)
        ratio_cap.next_to(axes, DOWN, buff=0.55)

        with self.voiceover(
            text="For a uniform variable, then, probability is a length "
                 "ratio: the length of the piece you care about, over the "
                 "length of the whole support."
        ):
            self.play(F_formula[0].animate.set_color(INK),
                      FadeIn(ratio_cap, shift=UP * 0.2), run_time=0.8)

        self.play(FadeOut(VGroup(axes, x_name, ramp, lbls,
                                 F_formula, ratio_cap)), run_time=0.6)

        # The bus stop: a 30-minute strip, the first 5 minutes shaded.
        fT = MathTex(r"f_T(t)", "=", r"\frac{1}{30}, \quad t \in [0, 30]",
                     font_size=BODY).next_to(title, DOWN, buff=0.45)
        fit_to_frame(fT)
        strip = Rectangle(width=8.0, height=0.7, color=MUTED, stroke_width=2)
        strip.move_to(DOWN * 0.3)
        t0 = MathTex("0", font_size=CAPTION, color=MUTED)
        t0.next_to(strip.get_corner(DL), DOWN, buff=0.2)
        t30 = MathTex("30", font_size=CAPTION, color=MUTED)
        t30.next_to(strip.get_corner(DR), DOWN, buff=0.2)
        mins = Text("minutes", font_size=CAPTION, color=MUTED)
        mins.next_to(t30, RIGHT, buff=0.3)

        with self.voiceover(
            text="Try it. A bus comes every thirty minutes, and David "
                 "arrives at the stop at a uniformly random time, so his "
                 "wait is uniform on zero to thirty minutes."
        ):
            self.play(Write(fT), run_time=1.0)
            self.play(Create(strip), FadeIn(t0), FadeIn(t30), FadeIn(mins),
                      run_time=1.0)

        shade = Rectangle(width=8.0 * 5 / 30, height=0.7,
                          fill_color=ACCENT, fill_opacity=0.45,
                          stroke_width=0)
        shade.move_to(strip.get_left(), aligned_edge=LEFT)
        t5 = MathTex("5", font_size=CAPTION, color=MUTED)
        t5.next_to(shade.get_corner(DR), DOWN, buff=0.2)
        mark_intended_overlap(strip, shade, t0,
                              reason="the first five minutes shade the strip")
        answer = MathTex(
            pr("T < 5"), "=", r"\int_0^5 \frac{1}{30}\, dt",
            "=", r"\frac{5}{30}", "=", r"\frac{1}{6}",
            font_size=BODY,
        ).next_to(strip, DOWN, buff=0.9)
        fit_to_frame(answer)
        mark_intended_overlap(
            answer[2],
            reason="TeX tucks the integral's limits against the slanted sign")

        with self.voiceover(
            text="The chance he waits less than five minutes is the "
                 "integral of one thirtieth over the first five minutes,"
        ):
            self.play(FadeIn(shade), FadeIn(t5), run_time=0.7)
            self.play(Write(answer[:3]), run_time=1.0)

        with self.voiceover(
            text="five parts out of thirty: one sixth."
        ):
            self.play(shade.animate.set_fill(BAR, opacity=0.45),
                      Write(answer[3:]), run_time=0.9)
            self.play(answer[6].animate.set_color(ACCENT), run_time=0.4)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GaussianDistribution(VoiceoverScene):
    """Beat: gaussian -- the bell, parameters as motions, Phi, and Q."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Gaussian Distribution")
        fit_to_frame(title)

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 0.5, 0.25],
            x_length=9.0,
            y_length=3.0,
            tips=False,
            axis_config={"include_numbers": False},
        )
        axes.to_edge(DOWN, buff=1.3)
        x_name = MathTex("x", font_size=BODY, color=MUTED)
        x_name.next_to(axes.x_axis.get_end(), DOWN + RIGHT, buff=0.25)

        bell = axes.plot(gauss(0, 1), x_range=[-5, 5], color=INK)
        b_ms = axes.plot(gauss(1.5, 1.3), x_range=[-5, 5], color=MUTED)
        b_std = axes.plot(gauss(0, 1), x_range=[-5, 5], color=INK)
        area_ms = axes.get_area(b_ms, x_range=[-5, 2.8],
                                color=BAR, opacity=0.4)
        area_std = axes.get_area(b_std, x_range=[-5, 1.0],
                                 color=BAR, opacity=0.4)
        mark_intended_overlap(
            axes, bell, b_ms, b_std, area_ms, area_std, x_name,
            reason="curves and their shaded areas live on the axes")

        with self.voiceover(
            text="From the flattest density to the most famous one."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        density = MathTex(
            r"f_X(x)", "=",
            r"\frac{1}{\sqrt{2\pi}\,\sigma}\,"
            r"e^{-\frac{(x - m)^2}{2\sigma^2}}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(density)

        with self.voiceover(
            text="The Gaussian, or normal, random variable is the default "
                 "model for quantities shaped by many small independent "
                 "effects, like thermal noise or measurement error. Its "
                 "density is the bell curve: e to the minus x minus m "
                 "squared over two sigma squared, scaled by one over root "
                 "two pi sigma."
        ):
            self.play(Write(density), run_time=1.4)
            self.play(density[0].animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(axes), FadeIn(x_name), run_time=0.9)
            self.play(Create(bell), run_time=1.2)

        cap = MathTex(r"m \text{ centers it}", font_size=CAPTION, color=MUTED)
        cap.next_to(axes, DOWN, buff=0.25)

        with self.voiceover(
            text="The two parameters are motions, not mysteries. Slide m, "
                 "and the whole density slides with it: m is the center."
        ):
            self.play(FadeIn(cap), run_time=0.4)
            self.play(Transform(bell, axes.plot(gauss(1.5, 1),
                                                x_range=[-5, 5], color=INK)),
                      run_time=1.6)

        cap2 = MathTex(r"\sigma \text{ sets the spread}",
                       font_size=CAPTION, color=MUTED).move_to(cap)

        with self.voiceover(
            text="Increase sigma, and the density widens and flattens, area "
                 "again pinned at one: sigma sets the spread."
        ):
            self.play(FadeOut(cap), FadeIn(cap2), run_time=0.4)
            self.play(Transform(bell, axes.plot(gauss(1.5, 2),
                                                x_range=[-5, 5], color=INK)),
                      run_time=1.6)
            cap = cap2

        cap2 = MathTex(r"m = 0,\ \sigma = 1:\ \text{the standard normal}",
                       font_size=CAPTION, color=ACCENT).move_to(cap)

        with self.voiceover(
            text="The special case m equals zero, sigma equals one, is "
                 "called the standard normal. Remember it, because it is "
                 "about to do all the work."
        ):
            self.play(density[0].animate.set_color(INK), run_time=0.3)
            self.play(Transform(bell, axes.plot(gauss(0, 1),
                                                x_range=[-5, 5], color=INK)),
                      FadeOut(cap), FadeIn(cap2), run_time=1.4)
            cap = cap2

        cdf_int = MathTex(
            r"F_X(x)", "=",
            r"\frac{1}{\sqrt{2\pi}\,\sigma} \int_{-\infty}^{x}"
            r" e^{-\frac{(u - m)^2}{2\sigma^2}}\, du",
            font_size=SMALL,
        ).move_to(density)
        fit_to_frame(cdf_int)
        cap2 = Text("no closed form", font_size=CAPTION,
                    color=MUTED).move_to(cap)

        with self.voiceover(
            text="Here is the catch: the CDF of a Gaussian is an integral "
                 "with no closed form. No amount of calculus produces an "
                 "antiderivative for the density."
        ):
            self.play(ReplacementTransform(density, cdf_int),
                      FadeOut(cap), FadeIn(cap2), run_time=1.0)
            cap = cap2

        phi = MathTex(
            r"F_X(x)", "=", r"\Phi\!\left(\frac{x - m}{\sigma}\right)",
            font_size=BODY,
        ).next_to(cdf_int, DOWN, buff=0.35)
        fit_to_frame(phi)

        with self.voiceover(
            text="The rescue is a change of variables. Substitute v equals "
                 "u minus m over sigma, and every Gaussian CDF collapses to "
                 "F of x equals Phi of x minus m over sigma,"
        ):
            self.play(Transform(bell, b_ms), FadeIn(area_ms), run_time=1.0)
            self.play(Write(phi), run_time=1.0)
            self.play(phi[2].animate.set_color(ACCENT), run_time=0.4)
            self.play(Transform(bell, b_std),
                      Transform(area_ms, area_std), run_time=1.4)

        cap2 = MathTex(
            r"\text{one curve serves every } m \text{ and } \sigma",
            font_size=CAPTION, color=MUTED,
        ).move_to(cap)

        with self.voiceover(
            text="where Phi is the CDF of the standard normal: one "
                 "tabulated curve, computed once, serving every m and every "
                 "sigma there is."
        ):
            self.play(FadeOut(cap), FadeIn(cap2), run_time=0.6)
            cap = cap2

        cap2 = MathTex(
            r"Q(x) = 1 - \Phi(x), \qquad"
            r" \Phi(x) = \tfrac{1}{2}\bigl(1 + \mathrm{erf}(x/\sqrt{2})\bigr)",
            font_size=CAPTION, color=MUTED,
        ).move_to(cap)
        fit_to_frame(cap2)

        with self.voiceover(
            text="The same information wears other names. Statisticians use "
                 "the error function, erf, and engineers use the tail, Q of "
                 "x, which is simply one minus Phi of x: different fields, "
                 "same curve."
        ):
            self.play(phi[2].animate.set_color(INK), run_time=0.3)
            self.play(FadeOut(cap), FadeIn(cap2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class NoisyChannel(VoiceoverScene):
    """Beat: channel -- plus or minus one through Gaussian noise."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Noisy Channel")
        fit_to_frame(title)

        with self.voiceover(
            text="Let the tail earn its keep."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        card = MathTex(
            r"X \in \{-1, +1\} \text{ equiprobable}", r",\qquad",
            r"Y = X + Z", r",\qquad",
            r"Z \text{ Gaussian: mean } 0 \text{, spread } \sigma",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(card)

        with self.voiceover(
            text="A binary message crosses a noisy wire. The input X is "
                 "plus one or minus one with equal probability, and the "
                 "output is Y equals X plus Z, where Z is Gaussian noise "
                 "with mean zero and spread sigma."
        ):
            self.play(Write(card), run_time=1.6)

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.25],
            x_length=9.0,
            y_length=2.6,
            tips=False,
            axis_config={"include_numbers": False},
        )
        axes.to_edge(DOWN, buff=1.0)
        thresh = DashedLine(axes.c2p(0, 0), axes.c2p(0, 0.48),
                            color=MUTED, stroke_width=2.5, dash_length=0.12)
        zero_lab = MathTex("0", font_size=CAPTION, color=MUTED)
        zero_lab.next_to(axes.c2p(0, 0), DOWN, buff=0.2)
        dec_cap = MathTex(r"\text{decide by the sign of } Y",
                          font_size=SMALL, color=MUTED)
        dec_cap.next_to(card, DOWN, buff=0.4)

        b_plus = axes.plot(gauss(1, 0.9), x_range=[-4, 4], color=INK)
        b_minus = axes.plot(gauss(-1, 0.9), x_range=[-4, 4], color=BAR)
        p_lab = MathTex("+1", font_size=CAPTION, color=MUTED)
        p_lab.next_to(axes.c2p(1, 0), DOWN, buff=0.2)
        m_lab = MathTex("-1", font_size=CAPTION, color=MUTED)
        m_lab.next_to(axes.c2p(-1, 0), DOWN, buff=0.2)
        tail_p = axes.get_area(b_plus, x_range=[-4, 0],
                               color=MAROON, opacity=0.7)
        tail_m = axes.get_area(b_minus, x_range=[0, 4],
                               color=MAROON, opacity=0.7)
        mark_intended_overlap(
            axes, thresh, b_plus, b_minus, tail_p, tail_m,
            zero_lab, p_lab, m_lab,
            reason="two bells cross at the shared decision threshold")

        with self.voiceover(
            text="The receiver does the natural thing: it decides by the "
                 "sign of Y. Positive means a plus one was sent; negative "
                 "means a minus one."
        ):
            self.play(Create(axes), Create(thresh), FadeIn(zero_lab),
                      run_time=1.0)
            self.play(FadeIn(dec_cap, shift=UP * 0.2), run_time=0.6)

        two_ways = MathTex(
            r"\text{sent } +1 \text{ and } Y \le 0",
            r"\quad\text{or}\quad",
            r"\text{sent } -1 \text{ and } Y \ge 0",
            font_size=SMALL,
        ).move_to(dec_cap)
        fit_to_frame(two_ways)

        with self.voiceover(
            text="When does it fail? In two ways: a plus one was sent and "
                 "the noise dragged Y below zero, or a minus one was sent "
                 "and the noise pushed Y above zero."
        ):
            self.play(FadeOut(dec_cap), run_time=0.3)
            self.play(Write(two_ways[0]), run_time=0.7)
            self.play(Write(two_ways[1]), Write(two_ways[2]), run_time=0.8)

        tail_f = MathTex(
            pr(r"Y \le 0 \mid X = +1"), "=", pr(r"Z < -1"),
            "=", r"Q\!\left(\tfrac{1}{\sigma}\right)",
            font_size=SMALL,
        ).move_to(two_ways)
        fit_to_frame(tail_f)

        with self.voiceover(
            text="Picture the two densities, one centered at plus one, one "
                 "at minus one, with the threshold at zero. Given a plus "
                 "one, an error means the noise beats the signal: Z below "
                 "minus one, and by symmetry of the density that is the "
                 "tail probability Q of one over sigma."
        ):
            self.play(Create(b_plus), FadeIn(p_lab), run_time=0.8)
            self.play(Create(b_minus), FadeIn(m_lab), run_time=0.8)
            self.play(FadeOut(two_ways), run_time=0.3)
            self.play(FadeIn(tail_p), run_time=0.7)
            self.play(Write(tail_f), run_time=1.2)

        sym = MathTex(
            pr(r"Y \ge 0 \mid X = -1"), "=", pr(r"Y \le 0 \mid X = +1"),
            font_size=CAPTION, color=MUTED,
        ).next_to(tail_f, DOWN, buff=0.3)
        fit_to_frame(sym)

        with self.voiceover(
            text="The other error is its mirror image, the same tail "
                 "reflected across the threshold."
        ):
            self.play(FadeIn(tail_m), run_time=0.7)
            self.play(Write(sym), run_time=0.8)

        total = MathTex(
            pr(r"\text{error}"), "=",
            r"\tfrac{1}{2}\, Q\!\left(\tfrac{1}{\sigma}\right)"
            r" + \tfrac{1}{2}\, Q\!\left(\tfrac{1}{\sigma}\right)",
            font_size=SMALL,
        ).move_to(tail_f)
        fit_to_frame(total)

        with self.voiceover(
            text="The total probability theorem averages the two "
                 "conditional errors, a half of each,"
        ):
            self.play(FadeOut(tail_f), FadeOut(sym), run_time=0.4)
            self.play(Write(total), run_time=1.0)

        ans = MathTex(
            pr(r"\text{error}"), "=", r"Q\!\left(\tfrac{1}{\sigma}\right)",
            font_size=BODY,
        ).move_to(total)

        with self.voiceover(
            text="and symmetry makes the average trivial: the probability "
                 "of error is exactly Q of one over sigma. Noise level in, "
                 "error rate out: reliability read off a tail."
        ):
            self.play(ReplacementTransform(total, ans), run_time=0.9)
            self.play(ans[2].animate.set_color(ACCENT), run_time=0.5)
            self.play(Indicate(ans, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GaussianIntegral(VoiceoverScene):
    """Beat: integral -- the polar trick, and the outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # "Bell Curve" in full, never bare "Bell" (2026-07-04 draft
        # review, 5:40).
        title = section_title("Why the Bell Curve Integrates to One")
        fit_to_frame(title)

        with self.voiceover(
            text="One debt remains: is the Gaussian even a density? Its "
                 "area must be one, yet the function refuses to be "
                 "integrated directly."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP), run_time=0.8)

        L1 = MathTex(
            r"I", "=",
            r"\int_{-\infty}^{\infty} \frac{1}{\sqrt{2\pi}}\,"
            r" e^{-u^2/2}\, du",
            r"\;\overset{?}{=}\; 1",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(L1)

        with self.voiceover(
            text="The classic trick is easy to follow and hard to "
                 "discover. Call the integral I, and study I squared "
                 "instead."
        ):
            self.play(Write(L1[:3]), run_time=1.2)
            self.play(Write(L1[3]), run_time=0.6)
            self.play(L1[3].animate.set_color(ACCENT), run_time=0.4)

        # The I^2 chain hangs together: continuation lines are built as
        # ("=", rhs) -- MathTex drops empty leading parts -- and their
        # equals signs align under L2's, so the derivation reads as one
        # chain, not scattered equations (2026-07-04 draft review, 6:20).
        L2 = MathTex(
            r"I^2", "=",
            r"\int_{-\infty}^{\infty} \int_{-\infty}^{\infty}"
            r" \frac{1}{2\pi}\, e^{-\frac{u^2 + v^2}{2}}\, du\, dv",
            font_size=SMALL,
        ).next_to(L1, DOWN, buff=0.35)
        fit_to_frame(L2)

        def chain_align(line, above, buff=0.28):
            """Hang `line` below `above` with its '=' under L2's '='."""
            line.next_to(above, DOWN, buff=buff)
            line.shift(
                RIGHT * (L2[1].get_center()[0] - line[0].get_center()[0]))
            return line

        with self.voiceover(
            text="Squaring turns one integral into two, and two integrals "
                 "into a double integral over the whole plane, of e to the "
                 "minus u squared plus v squared over two."
        ):
            self.play(Write(L2), run_time=1.4)

        # Top view of the surface: circular level sets, a radial arrow --
        # off to the left, clear of the equation chain.
        circles = VGroup(*[
            Circle(radius=r, color=MUTED, stroke_width=2)
            for r in (0.45, 0.85, 1.25)
        ]).move_to(LEFT * 4.6 + DOWN * 1.6)
        radial = Arrow(circles.get_center(),
                       circles.get_center() + np.array([1.05, 1.05, 0]),
                       buff=0, color=INK, stroke_width=3,
                       max_tip_length_to_length_ratio=0.12)
        r_lab = MathTex("r", font_size=CAPTION, color=INK)
        r_lab.next_to(radial.get_end(), UR, buff=0.1)
        mark_intended_overlap(circles, radial, r_lab,
                              reason="the radial arrow crosses the level sets")

        L3 = chain_align(MathTex(
            "=",
            r"\int_0^{2\pi} \frac{1}{2\pi}\, d\theta"
            r" \int_0^{\infty} r\, e^{-r^2/2}\, dr",
            font_size=SMALL,
        ), L2)

        # Re-split per review: circles land on the "perfect circles"
        # sentence, the polar rewrite lands on the "angle contributes"
        # sentence (2026-07-04 draft review, 5:50).
        with self.voiceover(
            text="Now look at that surface from above. Its level sets are "
                 "perfect circles, begging for polar coordinates."
        ):
            self.play(LaggedStart(*[Create(c) for c in circles],
                                  lag_ratio=0.3), run_time=1.0)
            self.play(Create(radial), FadeIn(r_lab), run_time=0.7)

        with self.voiceover(
            text="The angle contributes a factor of two pi, and the radial "
                 "integrand becomes r times e to the minus r squared over "
                 "two: that extra r is exactly the derivative the "
                 "exponential was missing."
        ):
            self.play(Write(L3), run_time=1.2)

        L4 = chain_align(MathTex(
            "=", r"\left(-\, e^{-r^2/2}\right)\Big|_0^{\infty} = 1",
            font_size=SMALL,
        ), L3)
        L5 = MathTex(
            r"I^2", "=", r"1 \;\Rightarrow\; I = 1",
            font_size=SMALL, color=ACCENT,
        )
        L5.next_to(L4, DOWN, buff=0.28)
        L5.shift(RIGHT * (L2[1].get_center()[0] - L5[1].get_center()[0]))

        with self.voiceover(
            text="The radial integral evaluates in one line, and I squared "
                 "equals one."
        ):
            self.play(Write(L4), run_time=0.9)

        with self.voiceover(
            text="Since I is nonnegative, the area under the curve is "
                 "exactly one."
        ):
            self.play(L1[3].animate.set_color(INK), Write(L5), run_time=0.9)

        L6 = MathTex(
            expectation("X") + "= m", r",\qquad",
            variance("X") + r"= \sigma^2",
            font_size=CAPTION, color=MUTED,
        ).next_to(L5, DOWN, buff=0.3)
        L6.set_x(0)

        with self.voiceover(
            text="The same normalization identity, exploited once more, "
                 "delivers the moments: the mean is m and the variance is "
                 "sigma squared, so the parameters mean what we said they "
                 "mean."
        ):
            self.play(FadeIn(L6, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The uniform makes probability a length ratio;",
             "the Gaussian routes every question through one curve."],
            next_title="The Exponential Distribution",
        )

        # The "Next up..." sentence is dropped from the narration; the
        # card's Coming-up line stays as a visual-only bridge (2026-07-04
        # draft review, 6:48).
        with self.voiceover(
            text="The key idea of this video: the uniform makes probability "
                 "a length ratio, and the Gaussian routes every question "
                 "through one curve, Phi."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
