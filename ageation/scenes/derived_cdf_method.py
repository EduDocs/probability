# derived_from: content/31-derived-cdf-method-script.md
# derived_from_sha256: 3d05b3811fc061f342066c37cf29405f60066b2e9e6edcf2bf9e561712271053
"""Chapter 9, Video 1 -- Derived Distributions: the CDF Method.

Source notes : derived_distributions.tex (chapter opening + Section 9.1,
               Monotone Functions) -- Y = g(X), preimage probabilities,
               the CDF method, Rayleigh squared, the sup/inf formulas.
Script        : content/31-derived-cdf-method-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark
segment -- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/derived_cdf_method.py ChapterOverview
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
    caption_under,
    omega_box,
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


# --- Shared geometry for the monotone / decreasing plots ---------------------

def g_plateau(x):
    """The notes' monotone-increasing g with a flat stretch on [1.75, 3.25]."""
    if x < 1.75:
        return 0.5 * (x - 1.75) ** 3 + 4
    if x <= 3.25:
        return 4.0
    return 0.5 * (x - 3.25) ** 3 + 4


def g_plateau_sup(y):
    """sup{ g^{-1}((-inf, y]) } for g_plateau (clamped to [0, 5])."""
    if y < 4:
        x = 1.75 - (2 * (4 - y)) ** (1 / 3)
    elif y == 4:
        x = 3.25
    else:
        x = 3.25 + (2 * (y - 4)) ** (1 / 3)
    return min(max(x, 0.0), 5.0)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            ["Derived Distributions:", "The CDF Method"],
            ["Pass X through a function g, and derive",
             "the distribution of Y = g(X) from one event."],
            kicker="Chapter 9  ·  Functions and Derived Distributions",
        )
        tag = progress_tag(1, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The CDF method", font_size=BODY, color=INK),
            Text("2.  A Rayleigh, squared", font_size=BODY, color=INK),
            Text("3.  Monotone functions", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="The gallery closed chapter eight, each density a record of "
                 "a construction. Chapter nine puts those densities to work: "
                 "pass a random variable through a function, and ask what "
                 "distribution comes out. The answer must be derived, and "
                 "deriving it is this video's whole business."
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
            text="In this video we meet the master tool, the CDF method: "
                 "describe the event that g of X lands at or below y, and "
                 "integrate the density over it."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We use it to pay a debt from last video: the square of a "
                 "Rayleigh really is exponential."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="And when g is monotone, the whole method collapses to a "
                 "single formula."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CDFMethod(VoiceoverScene):
    """Beat: cdf-method -- the two-hop picture, preimages, the recipe."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The CDF Method")
        fit_to_frame(title)

        # 2026-07-05 draft review (0:40): the opening motivation was spoken
        # over a bare title -- each example transform now lands on its phrase,
        # then the general pipeline, all fading before the two-hop diagram.
        ex_amp = VGroup(
            MathTex(r"A \;\longmapsto\; A^2", font_size=BODY, color=INK),
            Text("amplitude, squared into energy",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.22)
        ex_volt = VGroup(
            MathTex(r"V \;\longmapsto\; aV + b", font_size=BODY, color=INK),
            Text("voltage, scaled and shifted",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.22)
        pipe = MathTex(r"X \;\xrightarrow{\;\;g\;\;}\; g(X)",
                       font_size=BODY, color=ACCENT)
        opening = VGroup(ex_amp, ex_volt, pipe).arrange(DOWN, buff=0.55)
        opening.move_to(DOWN * 0.5)
        fit_to_frame(opening)

        with self.voiceover(
            text="Engineering transforms signals frequently: amplitudes get "
                 "squared into energies,"
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))
            self.play(FadeIn(ex_amp, shift=RIGHT * 0.4), run_time=0.7)

        with self.voiceover(
            text="voltages get scaled and shifted."
        ):
            self.play(FadeIn(ex_volt, shift=RIGHT * 0.4), run_time=0.7)

        with self.voiceover(
            text="Each transform drags a distribution along, so take a "
                 "continuous random variable X and a real-valued function g."
        ):
            self.play(Write(pipe), run_time=1.0)

        # The two-hop diagram: Omega blob -> X line -> Y line, then the
        # composite arrow drawn straight through (the notes' figure).
        omega = omega_box(2.4, 2.6).move_to(LEFT * 4.8 + DOWN * 0.9)
        w_dot = Dot(omega.get_center() + UP * 0.35, radius=0.07, color=INK)
        w_lab = MathTex(r"\omega", font_size=CAPTION, color=MUTED)
        w_lab.next_to(w_dot, UP, buff=0.15)

        x_line = NumberLine(x_range=[-2, 2, 1], length=3.2,
                            color=MUTED).move_to(LEFT * 0.6 + DOWN * 2.1)
        y_line = NumberLine(x_range=[-2, 2, 1], length=3.2,
                            color=MUTED).move_to(RIGHT * 4.6 + DOWN * 2.1)
        x_name = MathTex("X", font_size=SMALL, color=MUTED)
        x_name.next_to(x_line, DOWN, buff=0.25)
        y_name = MathTex("Y", font_size=SMALL, color=MUTED)
        y_name.next_to(y_line, DOWN, buff=0.25)

        x_dot = Dot(x_line.n2p(0.5), radius=0.07, color=INK)
        y_dot = Dot(y_line.n2p(-0.5), radius=0.07, color=INK)
        hop1 = CurvedArrow(w_dot.get_center() + DOWN * 0.15 + RIGHT * 0.15,
                           x_dot.get_center() + UP * 0.12 + LEFT * 0.1,
                           angle=-0.6, color=MUTED, stroke_width=3,
                           tip_length=0.18)
        hop2 = CurvedArrow(x_dot.get_center() + UP * 0.12 + RIGHT * 0.1,
                           y_dot.get_center() + UP * 0.12 + LEFT * 0.1,
                           angle=-0.7, color=MUTED, stroke_width=3,
                           tip_length=0.18)
        g_lab = MathTex("g", font_size=SMALL, color=INK)
        g_lab.move_to(hop2.point_from_proportion(0.5) + UP * 0.35)
        composite = CurvedArrow(w_dot.get_center() + UP * 0.18 + RIGHT * 0.12,
                                y_dot.get_center() + UP * 0.18,
                                angle=-1.1, color=ACCENT, stroke_width=4,
                                tip_length=0.2)
        comp_lab = MathTex(r"Y = g(X)", font_size=BODY, color=ACCENT)
        comp_lab.move_to(composite.point_from_proportion(0.5) + UP * 0.45)

        diagram = VGroup(omega, w_dot, w_lab, x_line, y_line, x_name, y_name,
                         x_dot, y_dot, hop1, hop2, g_lab, composite, comp_lab)
        mark_intended_overlap(
            *diagram,
            reason="two-hop diagram: arrows thread the sample space "
                   "and the number lines by design")
        # 2026-07-04 draft review (1:20): ride 0.5 higher for visual harmony.
        diagram.shift(UP * 0.5)
        fit_to_frame(diagram)

        with self.voiceover(
            text="The picture is the one from chapter five: an outcome omega "
                 "lands on the first real line at X of omega, and g carries "
                 "it to a second line. The composite arrow is a new random "
                 "variable, Y equals g of X."
        ):
            self.play(FadeOut(opening), run_time=0.5)
            self.play(Create(omega[0]), Write(omega[1]),
                      FadeIn(w_dot), Write(w_lab), run_time=0.8)
            self.play(Create(x_line), Write(x_name), run_time=0.6)
            self.play(Create(hop1), FadeIn(x_dot), run_time=0.7)
            self.play(Create(y_line), Write(y_name), run_time=0.6)
            self.play(Create(hop2), Write(g_lab), FadeIn(y_dot), run_time=0.7)
            self.play(Create(composite), Write(comp_lab), run_time=1.0)

        caption = Text("no masses to regroup: events do the work",
                       font_size=CAPTION, color=MUTED)
        caption.to_edge(DOWN, buff=0.9).shift(RIGHT * 1.8)

        with self.voiceover(
            text="For discrete X we derived the PMF of Y by regrouping "
                 "masses over each preimage. A continuum has no masses to "
                 "regroup, so events must do the work."
        ):
            self.play(comp_lab.animate.set_color(INK),
                      composite.animate.set_color(INK), run_time=0.5)
            self.play(FadeIn(caption, shift=UP * 0.2), run_time=0.7)

        self.play(FadeOut(diagram), FadeOut(caption), run_time=0.6)

        ident = MathTex(
            pr(r"Y \in S"), "=", pr(r"X \in g^{-1}(S)"), "=",
            r"\int_{g^{-1}(S)} f_X(u)\, du",
            font_size=BODY,
        )
        ident.next_to(title, DOWN, buff=0.55)
        fit_to_frame(ident)
        note = MathTex(r"g^{-1}(S) = \{\, u \mid g(u) \in S \,\}",
                       font_size=SMALL, color=MUTED)
        note.next_to(ident, DOWN, buff=0.4)

        with self.voiceover(
            text="The probability that Y lands in a set S is the probability "
                 "that X lands in the preimage of S, the set of inputs u "
                 "where g of u falls in S. That is the set-theoretic "
                 "preimage from the video on functions, back after a long "
                 "wait and finally load-bearing. And a probability about X "
                 "we know how to compute: integrate the density of X over "
                 "the preimage."
        ):
            self.play(Write(ident[0]), Write(ident[1]), Write(ident[2]),
                      run_time=1.2)
            self.play(FadeIn(note, shift=RIGHT * 0.3), run_time=0.7)
            self.play(Write(ident[3]), Write(ident[4]), run_time=1.0)

        s_line = MathTex(r"S = (-\infty,\, y]", font_size=BODY, color=ACCENT)
        s_line.next_to(note, DOWN, buff=0.5)
        cdf_line = MathTex(r"F_Y(y)", "=", pr(r"g(X) \leq y"),
                           font_size=BODY)
        cdf_line.next_to(s_line, DOWN, buff=0.4)

        with self.voiceover(
            text="Now specialize. Take S to be the half-line at or below y. "
                 "Then the event Y in S is the event g of X at most y, and "
                 "its probability is, by definition, the CDF of Y at y."
        ):
            self.play(Write(s_line), run_time=0.8)
            self.play(s_line.animate.set_color(INK), Write(cdf_line),
                      run_time=1.0)
            self.play(cdf_line[0].animate.set_color(ACCENT), run_time=0.5)

        recipe_lines = VGroup(
            MathTex(r"\text{1. describe the set }\ "
                    r"\{\, x \mid g(x) \leq y \,\}",
                    font_size=SMALL, color=INK),
            MathTex(r"\text{2. integrate }\ f_X\ \text{ over it}",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # 2026-07-04 draft review (2:20): the accent box sits 0.4 lower.
        recipe_lines.next_to(cdf_line, DOWN, buff=0.95)
        box = SurroundingRectangle(recipe_lines, color=ACCENT,
                                   buff=0.25, corner_radius=0.1)
        mark_intended_overlap(box, recipe_lines,
                              reason="recipe card frames its two lines")

        with self.voiceover(
            text="So the recipe has two lines. First, describe the event g "
                 "of X at most y as a set of x values. Second, integrate the "
                 "density of X over that set. Every derived distribution in "
                 "this chapter starts from these two lines."
        ):
            self.play(cdf_line[0].animate.set_color(INK),
                      Write(recipe_lines[0]), run_time=0.9)
            self.play(Write(recipe_lines[1]), run_time=0.9)
            self.play(Create(box), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class RayleighSquared(VoiceoverScene):
    """Beat: rayleigh-squared -- the worked highlight, R^2 is exponential."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Rayleigh, Squared")
        fit_to_frame(title)

        with self.voiceover(
            text="Let the method earn its keep."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[0, 0.7, 0.35],
            x_length=5.2,
            y_length=3.0,
            tips=False,
            axis_config={"include_numbers": False},
        ).move_to(LEFT * 3.5 + DOWN * 0.9)  # 2026-07-04 review (3:30): +0.4
        curve = axes.plot(lambda u: u * math.exp(-u * u / 2),
                          x_range=[0, 3.4], color=BAR)
        u_name = axes.get_x_axis_label(
            MathTex("u", font_size=SMALL, color=MUTED), edge=RIGHT,
            direction=DOWN + RIGHT, buff=0.25)
        dens_lab = MathTex(r"f_X(u) = u\, e^{-u^2/2}, \quad u \geq 0",
                           font_size=SMALL, color=INK)
        dens_lab.next_to(axes, UP, buff=0.35)
        y_card = MathTex(r"Y = X^2", font_size=BODY, color=ACCENT)
        y_card.move_to(RIGHT * 3.4 + UP * 1.9)

        sqrt_y = 1.5  # the boundary sqrt(y) for the shaded event
        area = axes.get_area(curve, x_range=[0, sqrt_y],
                             color=BAR, opacity=0.35)
        bound = DashedLine(axes.c2p(sqrt_y, 0),
                           axes.c2p(sqrt_y, 0.55),
                           color=MUTED, stroke_width=2.5, dash_length=0.1)
        bound_lab = MathTex(r"\sqrt{y}", font_size=CAPTION, color=INK)
        bound_lab.next_to(axes.c2p(sqrt_y, 0), DOWN, buff=0.25)
        mark_intended_overlap(
            axes, curve, area, bound, u_name,
            reason="density curve, shaded event, and boundary live "
                   "on the axes by design")

        with self.voiceover(
            text="Last video introduced the Rayleigh density as the "
                 "amplitude of a fading channel, and stated, without proof, "
                 "that its square is exponential. Take X Rayleigh with sigma "
                 "squared equal to one, so the density is u times e to the "
                 "minus u squared over two, for u at least zero. Let Y be X "
                 "squared, the energy of the fade."
        ):
            self.play(Create(axes), FadeIn(u_name), run_time=0.8)
            self.play(Create(curve), run_time=1.0)
            self.play(Write(dens_lab), run_time=1.0)
            self.play(Write(y_card), run_time=0.8)

        lines = VGroup(
            MathTex(r"F_Y(y) = " + pr(r"X^2 \leq y"), font_size=SMALL),
            MathTex(r"= " + pr(r"-\sqrt{y} \leq X \leq \sqrt{y}"),
                    font_size=SMALL),
            MathTex(r"= \int_0^{\sqrt{y}} u\, e^{-u^2/2}\, du",
                    font_size=SMALL),
            MathTex(r"F_Y(y) = 1 - e^{-y/2}", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        lines.move_to(RIGHT * 3.4 + DOWN * 0.9)
        fit_to_frame(lines)

        with self.voiceover(
            text="Fix y positive, and run the recipe. The event Y at most y "
                 "is the event X squared at most y, which puts X between "
                 "minus root y and root y."
        ):
            self.play(y_card.animate.set_color(INK), Write(lines[0]),
                      run_time=0.9)
            self.play(Write(lines[1]), run_time=0.9)

        with self.voiceover(
            text="But a Rayleigh variable is never negative, so the lower "
                 "limit rises to zero: the integral runs from zero to root "
                 "y, the shaded area under the density."
        ):
            self.play(Create(bound), FadeIn(bound_lab), run_time=0.7)
            self.play(FadeIn(area), run_time=0.8)
            self.play(Write(lines[2]), run_time=0.9)

        with self.voiceover(
            text="Substitute v equals u squared. The differential v is twice "
                 "u, exactly the factor sitting in the integrand, and the "
                 "integral collapses: F of Y at y equals one minus e to the "
                 "minus y over two."
        ):
            self.play(Write(lines[3]), run_time=1.0)
            self.play(lines[3].animate.set_color(ACCENT), run_time=0.5)

        expo = Text("the exponential CDF, parameter one half",
                    font_size=CAPTION, color=MUTED)
        expo.next_to(lines[3], DOWN, buff=0.35)

        with self.voiceover(
            text="Look at that function. It is the exponential CDF from chapter "
                 "eight, with parameter one half. The square of a Rayleigh "
                 "random variable is exponential; the promise is kept, in "
                 "four lines. And notice what the method needed from g: "
                 "nothing beyond the ability to describe one event."
        ):
            self.play(FadeIn(expo, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(lines[3], color=ACCENT, scale_factor=1.03),
                      run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MonotoneFunctions(VoiceoverScene):
    """Beat: monotone-sup -- increasing g, the sup formula, uniform doubled."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Monotone Functions")
        fit_to_frame(title)

        # 2026-07-05 draft review (4:02): the caution was spoken over a bare
        # title -- Y = g(X) anchors it, and each possible shape of Y gets a
        # mini-glyph landing as it is named; all fade before the definition.
        caution = MathTex(r"Y = g(X)", font_size=BODY, color=INK)
        caution.move_to(UP * 1.8)
        caution_cap = caption_under(
            caution, "continuity of X promises nothing about Y")

        def _mini_axes():
            return Axes(x_range=[0, 4, 4], y_range=[0, 1.4, 1.4],
                        x_length=2.0, y_length=1.1, tips=False)

        def _mini(ax, body, label):
            base = Line(ax.c2p(0, 0), ax.c2p(4, 0),
                        color=MUTED, stroke_width=2)
            lab = Text(label, font_size=CAPTION, color=MUTED)
            lab.next_to(base, DOWN, buff=0.25)
            mark_intended_overlap(
                base, *body,
                reason="mini shape glyph sits on its baseline by design")
            return VGroup(base, VGroup(*body), lab)

        ax_c = _mini_axes()
        mini_cont = _mini(
            ax_c,
            [ax_c.plot(lambda u: 1.25 * math.exp(-((u - 2) ** 2)),
                       x_range=[0.2, 3.8], color=BAR)],
            "continuous")
        ax_d = _mini_axes()
        mini_disc = _mini(
            ax_d,
            [VGroup(Line(ax_d.c2p(x, 0), ax_d.c2p(x, h),
                         color=BAR, stroke_width=3),
                    Dot(ax_d.c2p(x, h), radius=0.05, color=BAR))
             for x, h in [(1, 0.8), (2, 1.25), (3, 0.55)]],
            "discrete")
        ax_m = _mini_axes()
        mini_mix = _mini(
            ax_m,
            [ax_m.plot(lambda u: 0.35 * u, x_range=[0.2, 1.8], color=BAR),
             Dot(ax_m.c2p(1.8, 1.0), radius=0.05, color=BAR),
             ax_m.plot(lambda u: 1.0 + 0.12 * (u - 1.8),
                       x_range=[1.8, 3.8], color=BAR)],
            "neither")
        minis = VGroup(mini_cont, mini_disc, mini_mix)
        minis.arrange(RIGHT, buff=0.9).move_to(DOWN * 1.0)
        fit_to_frame(minis)

        ax_g = _mini_axes()
        mono_mini = _mini(
            ax_g,
            [ax_g.plot(lambda u: 0.1 + 1.2 / (1 + math.exp(-2.2 * (u - 2))),
                       x_range=[0.2, 3.8], color=ACCENT)],
            "monotone")
        mono_mini.move_to(DOWN * 1.0)

        with self.voiceover(
            text="One caution before we go on: continuity of X promises "
                 "nothing about Y."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))
            self.play(Write(caution), run_time=0.7)
            self.play(FadeIn(caution_cap, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="A function of a continuous random variable can be "
                 "continuous,"
        ):
            self.play(FadeIn(mini_cont, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="discrete,"
        ):
            self.play(FadeIn(mini_disc, shift=UP * 0.2), run_time=0.5)

        with self.voiceover(
            text="or neither, so we study structured cases,"
        ):
            self.play(FadeIn(mini_mix, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="and the friendliest structure is monotonicity."
        ):
            self.play(FadeOut(minis), run_time=0.5)
            self.play(FadeIn(mono_mini, shift=UP * 0.2), run_time=0.7)

        defline = MathTex(
            r"x_1 \leq x_2 \;\Rightarrow\; g(x_1) \leq g(x_2)",
            font_size=SMALL, color=INK)
        defline.next_to(title, DOWN, buff=0.45)

        with self.voiceover(
            text="A function is monotone increasing when larger inputs "
                 "never produce smaller outputs: x one at most x two forces "
                 "g of x one at most g of x two."
        ):
            self.play(FadeOut(caution), FadeOut(caution_cap),
                      FadeOut(mono_mini), run_time=0.5)
            self.play(Write(defline), run_time=1.0)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 7.5, 2.5],
            x_length=4.8,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        ).move_to(LEFT * 3.6 + DOWN * 1.5)
        curve = axes.plot(g_plateau, x_range=[0, 5], color=BAR)
        g_name = MathTex(r"y = g(x)", font_size=CAPTION, color=MUTED)
        g_name.next_to(axes.c2p(4.4, 7.0), LEFT, buff=0.15)

        # Threshold snapshots (y0 low, y1 just past the plateau, y2 high);
        # the slide is realized as Transforms between the snapshots.
        y0, y1, y2 = 3.6, 4.3, 6.0

        def snapshot(y):
            xb = g_plateau_sup(y)
            thr = DashedLine(axes.c2p(0, y), axes.c2p(5, y),
                             color=MUTED, stroke_width=2.5, dash_length=0.1)
            seg = Line(axes.c2p(0, 0), axes.c2p(xb, 0),
                       color=ACCENT, stroke_width=6)
            dot = Dot(axes.c2p(xb, 0), radius=0.07, color=ACCENT)
            return thr, seg, dot

        thr, seg, bdot = snapshot(y0)
        thr1, seg1, bdot1 = snapshot(y1)
        thr2, seg2, bdot2 = snapshot(y2)
        thr_lab = MathTex("y", font_size=CAPTION, color=MUTED)
        thr_lab.next_to(axes.c2p(0.3, y0), UP, buff=0.15)
        plat = Line(axes.c2p(1.75, 4), axes.c2p(3.25, 4),
                    color=BAR, stroke_width=6)
        mark_intended_overlap(
            axes, curve, g_name, thr, seg, bdot, thr1, seg1, bdot1,
            thr2, seg2, bdot2, thr_lab, plat,
            reason="threshold, plateau, and preimage segment live on "
                   "the g plot by design")

        with self.voiceover(
            text="For such a g, the event g of X at most y is everything to "
                 "the left of a boundary: the preimage of a half-line is a "
                 "half-line."
        ):
            self.play(Create(axes), Create(curve), FadeIn(g_name),
                      run_time=1.0)
            self.play(Create(thr), FadeIn(thr_lab), run_time=0.7)
            self.play(Create(seg), FadeIn(bdot), run_time=0.8)

        formula = VGroup(
            MathTex(r"F_Y(y) = " + pr(r"g(X) \leq y"), font_size=SMALL),
            MathTex(r"= F_X\!\left(\sup\left\{\, g^{-1}\!\left("
                    r"(-\infty, y]\right) \,\right\}\right)",
                    font_size=SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        formula.move_to(RIGHT * 3.4 + UP * 0.6)
        fit_to_frame(formula)

        with self.voiceover(
            text="The boundary is the supremum of that preimage, and the "
                 "CDF of Y is the CDF of X evaluated there. Why a supremum? "
                 "Because a flat stretch of g sends many inputs to the same "
                 "output, and a jump of g can leave the preimage of a point "
                 "empty. Taking the largest point of the half-line's "
                 "preimage handles both at once."
        ):
            self.play(Write(formula[0]), run_time=0.9)
            self.play(Write(formula[1]), run_time=1.1)
            self.play(seg.animate.set_color(BAR),
                      bdot.animate.set_color(BAR), run_time=0.4)
            self.play(formula[1].animate.set_color(ACCENT), run_time=0.5)
            self.play(Indicate(plat, color=INK, scale_factor=1.05),
                      run_time=0.9)

        with self.voiceover(
            text="Watch the threshold climb: as y rises, the boundary "
                 "glides to the right, and F of Y grows with it."
        ):
            self.play(formula[1].animate.set_color(INK),
                      seg.animate.set_color(ACCENT),
                      bdot.animate.set_color(ACCENT),
                      FadeOut(thr_lab), run_time=0.5)
            self.play(Transform(thr, thr1), Transform(seg, seg1),
                      Transform(bdot, bdot1), run_time=1.3)
            self.play(Transform(thr, thr2), Transform(seg, seg2),
                      Transform(bdot, bdot2), run_time=1.3)

        # plat entered the scene via Indicate (playing an animation on an
        # un-added mobject adds it), so it must leave with the plot.
        plot_group = VGroup(axes, curve, g_name, thr, seg, bdot, plat)
        self.play(FadeOut(plot_group), FadeOut(formula), FadeOut(defline),
                  run_time=0.6)

        unif1 = MathTex(r"X \sim \mathrm{Uniform}[0, 1], \qquad Y = 2X",
                        font_size=SMALL, color=INK)
        unif1.next_to(title, DOWN, buff=0.5)
        unif2 = MathTex(
            r"F_Y(y) = " + pr(r"X \leq \tfrac{y}{2}")
            + r" = \tfrac{y}{2}, \qquad y \in [0, 2]",
            font_size=BODY, color=INK)
        unif2.next_to(unif1, DOWN, buff=0.45)
        fit_to_frame(unif2)

        with self.voiceover(
            text="The gentlest instance: X uniform on zero one, and Y twice "
                 "X. For y between zero and two, Y at most y means X at "
                 "most y over two, so F of Y at y is y over two."
        ):
            self.play(Write(unif1), run_time=0.9)
            self.play(Write(unif2), run_time=1.1)

        ax2 = Axes(
            x_range=[0, 2.3, 1],
            y_range=[0, 1.3, 0.5],
            x_length=5.0,
            y_length=2.0,
            tips=False,
            axis_config={"include_numbers": True, "font_size": 30},
        ).to_edge(DOWN, buff=0.9)
        ux = (ax2.c2p(1, 0) - ax2.c2p(0, 0))[0]
        uy = (ax2.c2p(0, 1) - ax2.c2p(0, 0))[1]
        r1 = Rectangle(width=ux, height=uy,
                       fill_color=BAR, fill_opacity=0.5,
                       stroke_color=BAR, stroke_width=2)
        r1.move_to(ax2.c2p(0, 0), aligned_edge=DL)
        r2 = Rectangle(width=2 * ux, height=uy / 2,
                       fill_color=BAR, fill_opacity=0.5,
                       stroke_color=BAR, stroke_width=2)
        r2.move_to(ax2.c2p(0, 0), aligned_edge=DL)
        mark_intended_overlap(
            ax2, r1, r2,
            reason="the density rectangle stands on the axes by design")
        area_note = Text("area stays one", font_size=CAPTION, color=MUTED)
        area_note.next_to(ax2, RIGHT, buff=0.45)

        with self.voiceover(
            text="The density of Y is one half on zero two: the rectangle "
                 "stretches to double width and half height, and the area "
                 "stays one. An affine function of a uniform random "
                 "variable is uniform."
        ):
            self.play(Create(ax2), run_time=0.7)
            self.play(FadeIn(r1), run_time=0.6)
            self.play(Transform(r1, r2), run_time=1.1)
            self.play(FadeIn(area_note, shift=UP * 0.2), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DecreasingMirror(VoiceoverScene):
    """Beat: decreasing-mirror -- the inf formula, then the outro card."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Decreasing Mirror")
        fit_to_frame(title)

        with self.voiceover(
            text="What if g is monotone decreasing, so larger inputs "
                 "produce smaller outputs?"
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 2],
            x_length=4.8,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        ).move_to(LEFT * 3.6 + DOWN * 1.0)  # 2026-07-04 review (6:00): +0.4
        curve = axes.plot(lambda x: 5 * math.exp(-0.5 * x),
                          x_range=[0, 5], color=BAR)
        g_name = MathTex(r"y = g(x)", font_size=CAPTION, color=MUTED)
        g_name.next_to(axes.c2p(4.3, 5.4), RIGHT, buff=0.15)

        y0 = 2.0
        xb = 2 * math.log(5 / y0)  # g(xb) = y0
        thr = DashedLine(axes.c2p(0, y0), axes.c2p(5, y0),
                         color=MUTED, stroke_width=2.5, dash_length=0.1)
        thr_lab = MathTex("y", font_size=CAPTION, color=MUTED)
        thr_lab.next_to(axes.c2p(4.6, y0), UP, buff=0.15)
        seg = Line(axes.c2p(xb, 0), axes.c2p(5, 0),
                   color=ACCENT, stroke_width=6)
        bdot = Dot(axes.c2p(xb, 0), radius=0.07, color=ACCENT)
        mark_intended_overlap(
            axes, curve, g_name, thr, thr_lab, seg, bdot,
            reason="threshold and preimage segment live on the g plot "
                   "by design")

        with self.voiceover(
            text="The same argument runs in a mirror. A high threshold on "
                 "the output is now cleared by small inputs, so the event g "
                 "of X at most y collects everything to the right of a "
                 "boundary."
        ):
            self.play(Create(axes), Create(curve), FadeIn(g_name),
                      run_time=1.0)
            self.play(Create(thr), FadeIn(thr_lab), run_time=0.7)
            self.play(Create(seg), FadeIn(bdot), run_time=0.8)

        formula = VGroup(
            MathTex(r"F_Y(y) = " + pr(
                r"X \geq \inf\left\{\, g^{-1}\!\left((-\infty, y]\right) "
                r"\,\right\}"), font_size=SMALL),
            MathTex(r"= 1 - F_X\!\left(\inf\left\{\, g^{-1}\!\left("
                    r"(-\infty, y]\right) \,\right\}\right)",
                    font_size=SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        formula.move_to(RIGHT * 3.3 + UP * 0.6)
        fit_to_frame(formula)
        mirror_note = Text("sup becomes inf, F becomes 1 - F",
                           font_size=CAPTION, color=MUTED)
        mirror_note.next_to(formula, DOWN, buff=0.4)

        with self.voiceover(
            text="That boundary is an infimum, and the probability of "
                 "landing at or beyond it is one minus the CDF of X there. "
                 "The infimum plays the same guardian role the supremum "
                 "played, absorbing the flats and the jumps of g. Swap "
                 "supremum for infimum, and F for one minus F; nothing else "
                 "changes."
        ):
            self.play(Write(formula[0]), run_time=1.0)
            self.play(seg.animate.set_color(BAR),
                      bdot.animate.set_color(BAR),
                      Write(formula[1]), run_time=1.1)
            self.play(formula[1].animate.set_color(ACCENT), run_time=0.5)
            self.play(FadeIn(mirror_note, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Describe the event that g(X) is at most y,",
             "then integrate the density of X over it."],
            next_title="The Change-of-Variables Formula",
        )

        with self.voiceover(
            text="The key idea of this video: to find the distribution of g "
                 "of X, describe the event g of X at most y as a set of x "
                 "values, and integrate the density of X over it. Next "
                 "video, we differentiate this answer, and the "
                 "change-of-variables formula falls out."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
