# derived_from: content/30-additional-distributions-script.md
# derived_from_sha256: d7323a4dc9d163e4fd890f9632630ee0d1213d6f1277918750ead504c903b853
"""Chapter 8, Video 5 -- A Gallery of Densities.

Source notes : continuous_random_variables.tex (Section 8.5, Additional
               Distributions) -- the gamma function and gamma family,
               chi-square, Erlang, Rayleigh, Laplace, and Cauchy.
Script        : content/30-additional-distributions-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/additional_distributions.py ChapterOverview
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
    TICK,
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
    """Voice comes from project.yaml (project.voice); AGEATION_TTS
    is the draft/final switch (render.py sets gtts for -ql)."""
    return speech_service()


def gamma_pdf(alpha, lam):
    """The gamma density f(x) = lambda (lambda x)^(alpha-1) e^(-lambda x)
    / Gamma(alpha). Callers must start plot ranges slightly above 0 --
    the density is singular at 0 for alpha < 1."""
    g = math.gamma(alpha)

    def f(x):
        return lam * (lam * x) ** (alpha - 1) * math.exp(-lam * x) / g

    return f


def rayleigh_pdf(sigma=1.0):
    s2 = sigma * sigma

    def f(r):
        return (r / s2) * math.exp(-r * r / (2 * s2))

    return f


def laplace_pdf(b=1.0):
    def f(x):
        return math.exp(-abs(x) / b) / (2 * b)

    return f


def cauchy_pdf(gam=1.0):
    def f(x):
        return gam / (math.pi * (gam * gam + x * x))

    return f


def gauss_pdf(sigma=1.0):
    def f(x):
        return math.exp(-x * x / (2 * sigma * sigma)) / (
            math.sqrt(2 * math.pi) * sigma)

    return f


def density_axes(x_range, y_range, x_length=8.5, y_length=3.0,
                 x_name="x", numbers=True):
    """A density-plot chart in the house chart style: numbered x-axis,
    quiet y-axis, x name below-right of the tip. Returns (group, axes)."""
    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=x_length,
        y_length=y_length,
        axis_config={"include_numbers": False},
        # (2026-07-05 draft review) tick numbers one size smaller
        # series-wide: font_size TICK (26), was 30.
        x_axis_config={"include_numbers": numbers, "font_size": TICK},
        tips=False,
    )
    x_lab = axes.get_x_axis_label(
        MathTex(x_name, font_size=BODY), edge=RIGHT,
        direction=DOWN + RIGHT, buff=0.25)
    group = VGroup(axes, x_lab)
    fit_to_frame(group)
    return group, axes


# 40 pre-computed zero-mean Gaussian coordinate pairs (sigma = 1).
# (2026-07-05 draft review, 3:20) the old handpicked cloud read as
# uniform; each marginal is now exactly the 40 standard-normal
# quantiles Phi^{-1}((i + 0.5)/40), i = 0..39 -- dense near the center,
# sparse in the tails -- paired in a fixed authoring-time order.
# Hardcoded so nothing random happens at import or render time.
GAUSS_POINTS = [
    (-1.09, -0.64), (1.21, 0.56), (-0.49, -0.56), (-0.03, 0.64),
    (-0.29, 0.35), (-0.64, 1.53), (0.71, -1.21), (0.09, 0.03),
    (-0.8, 0.71), (-0.56, -0.71), (2.24, 1.09), (-2.24, 0.09),
    (0.56, -0.16), (-0.35, -0.49), (1.78, 1.78), (-0.09, 2.24),
    (0.16, -0.22), (0.8, 0.89), (0.49, -0.42), (0.29, -0.29),
    (-0.16, -1.53), (0.89, -1.36), (-0.89, 0.42), (0.42, 1.21),
    (1.53, 1.36), (-0.42, -0.89), (-1.53, -2.24), (-1.78, -0.35),
    (0.98, 0.8), (-0.22, -0.98), (0.64, 0.22), (1.36, -0.8),
    (0.22, 0.16), (-0.98, 0.98), (1.09, 0.29), (-1.21, 0.49),
    (-1.36, -0.03), (0.35, -1.78), (-0.71, -1.09), (0.03, -0.09),
]
RADIUS_POINT_INDEX = 10  # (2.24, 1.09) -- the point whose radius gets drawn

# Hardcoded running means of a Cauchy sample -- a plausible sequence of
# partial means that visibly refuses to settle (no randomness at import).
CAUCHY_RUNNING_MEANS = [
    1.8, 0.4, 6.1, 3.2, 2.7, -4.5, -2.1, -1.4, 5.3, 3.9, 3.1, 2.6,
]


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "A Gallery of Densities",
            ["Four more named densities, each one a record of a",
             "construction built from distributions you already know."],
            kicker="Chapter 8  ·  Continuous Random Variables",
        )
        tag = progress_tag(5, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The gamma function and the gamma family",
                 font_size=BODY, color=INK),
            Text("2.  Exponential, chi-square, Erlang",
                 font_size=BODY, color=INK),
            Text("3.  Rayleigh and Laplace", font_size=BODY, color=INK),
            Text("4.  The Cauchy warning", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="The uniform, the Gaussian, the exponential — three "
                 "densities carried this chapter. But engineering keeps a "
                 "wider gallery, and every curve in it is a record of a "
                 "construction."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.6)
        fit_to_frame(outline)

        with self.voiceover(
            text="In this video we extend the factorial into the gamma "
                 "function and unlock a two parameter family, the gamma "
                 "distribution,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        # (2026-07-05 draft review) "kai" phonetic respelling for TTS --
        # the Greek letter chi is pronounced "kai"; spoken form only,
        # on-screen text keeps "chi-square".
        with self.voiceover(
            text="then read three of its settings: the exponential, the "
                 "kai square, and the Erlang."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We take the length of a Gaussian vector and meet the "
                 "Rayleigh, then splice two exponentials into the Laplace,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and we close with a warning called the Cauchy — a "
                 "density so heavy tailed that averaging accomplishes "
                 "nothing."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GammaDistribution(VoiceoverScene):
    """Beat: gamma -- the gamma function, its values, and the density dial."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Gamma Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        g_def = MathTex(
            r"\Gamma(z)", "=", r"\int_0^{\infty} u^{z-1} e^{-u} \, du",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        g_rec = MathTex(
            r"\Gamma(z+1)", "=", r"z \, \Gamma(z)", font_size=BODY,
        ).next_to(g_def, DOWN, buff=0.45)
        g_fact = MathTex(
            r"\Gamma(k+1)", "=", r"k!", font_size=BODY,
        ).next_to(g_rec, DOWN, buff=0.45)
        fact_cap = Text("the factorial, extended",
                        font_size=CAPTION, color=MUTED)
        fact_cap.next_to(g_fact, DOWN, buff=0.25)
        g_half = MathTex(
            r"\Gamma\!\left(\tfrac{1}{2}\right)", "=", r"\sqrt{\pi}",
            font_size=BODY,
        ).next_to(fact_cap, DOWN, buff=0.4)
        half_cap = Text("the polar trick, second encore",
                        font_size=CAPTION, color=MUTED)
        half_cap.next_to(g_half, DOWN, buff=0.25)

        with self.voiceover(
            text="Start with a function, not a density."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="The gamma function assigns to each positive number z an "
                 "integral: u to the z minus one, times e to the minus u, "
                 "integrated over the positive axis."
        ):
            self.play(Write(g_def), run_time=1.2)
            self.play(g_def.animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="Integrate by parts once and a recursion falls out: gamma "
                 "of z plus one equals z times gamma of z."
        ):
            self.play(g_def.animate.set_color(INK),
                      Write(g_rec), run_time=1.0)
            self.play(g_rec.animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="Chain that recursion down the integers, and gamma of k "
                 "plus one is exactly k factorial. The gamma function is "
                 "the factorial, extended off the integers into a smooth "
                 "curve."
        ):
            self.play(g_rec.animate.set_color(INK),
                      Write(g_fact), run_time=0.9)
            self.play(g_fact.animate.set_color(ACCENT),
                      FadeIn(fact_cap, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="Its most famous value at a non integer argument is gamma "
                 "of one half, which equals the square root of pi. The "
                 "proof squares the integral and switches to polar "
                 "coordinates — the same trick that integrated the bell "
                 "curve two videos ago, back for a second encore."
        ):
            self.play(g_fact.animate.set_color(INK),
                      Write(g_half), run_time=0.9)
            self.play(g_half.animate.set_color(ACCENT),
                      FadeIn(half_cap, shift=UP * 0.2), run_time=0.6)

        self.wait(0.3)
        self.play(FadeOut(VGroup(g_def, g_rec, g_fact, fact_cap,
                                 g_half, half_cap)), run_time=0.5)

        pdf = MathTex(
            r"f_X(x)", "=",
            r"\frac{\lambda (\lambda x)^{\alpha - 1} e^{-\lambda x}}"
            r"{\Gamma(\alpha)}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        support = MathTex(r"x > 0", font_size=SMALL, color=MUTED)
        support.next_to(pdf, RIGHT, buff=0.7)
        fit_to_frame(VGroup(pdf, support))

        with self.voiceover(
            text="Now build the density. Take lambda, times lambda x to "
                 "the alpha minus one, times e to the minus lambda x, and "
                 "divide by gamma of alpha so the total area is one. This "
                 "is the gamma distribution, with a shape parameter alpha "
                 "and a rate parameter lambda."
        ):
            self.play(Write(pdf), run_time=1.4)
            self.play(pdf.animate.set_color(ACCENT),
                      FadeIn(support), run_time=0.6)

        chart, axes = density_axes([0, 8, 1], [0, 1.1, 0.25])
        chart.to_edge(DOWN, buff=0.8)

        settings = [(1, 1.0), (2, 1.0), (3, 1.5), (5, 2.0)]
        curves = [
            axes.plot(gamma_pdf(a, lam), x_range=[0.02, 8],
                      color=ACCENT, stroke_width=4)
            for a, lam in settings
        ]
        tags = [
            MathTex(r"\alpha = " + str(a)
                    + r",\ \lambda = " + f"{lam:g}",
                    font_size=SMALL, color=MUTED)
            .move_to(axes.c2p(6.2, 0.85))
            for a, lam in settings
        ]

        with self.voiceover(
            text="Together they form a dial. Turn it, and the curve sweeps "
                 "from a steep decay at small alpha to a rounded hump that "
                 "drifts rightward as alpha grows. Two knobs are enough to "
                 "fit a remarkable range of measured data."
        ):
            self.play(pdf.animate.set_color(INK),
                      Create(axes), Write(chart[1]), run_time=0.8)
            curve, tag = curves[0], tags[0]
            self.play(Create(curve), FadeIn(tag), run_time=0.9)
            for nxt_curve, nxt_tag in zip(curves[1:], tags[1:]):
                self.play(Transform(curve, nxt_curve),
                          Transform(tag, nxt_tag), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GammaSpecialCases(VoiceoverScene):
    """Beat: special-cases -- exponential, chi-square, Erlang, one family."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Chi-Square and Erlang")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        gen = MathTex(
            r"f_X(x) = \frac{\lambda (\lambda x)^{\alpha - 1} "
            r"e^{-\lambda x}}{\Gamma(\alpha)}",
            font_size=SMALL, color=MUTED,
        ).next_to(title, DOWN, buff=0.35)

        chart, axes = density_axes([0, 6, 1], [0, 0.6, 0.2])
        chart.to_edge(DOWN, buff=0.8)

        def card(name, formula, note):
            parts = VGroup(
                Text(name, font_size=SMALL, color=INK),
                MathTex(formula, font_size=SMALL, color=INK),
                MathTex(note, font_size=CAPTION, color=MUTED),
            ).arrange(DOWN, buff=0.22)
            parts.move_to(RIGHT * 3.4 + UP * 0.75)
            return fit_to_frame(parts)

        with self.voiceover(
            text="One family, three famous settings."
        ):
            self.play(FadeIn(gen), Create(axes), Write(chart[1]),
                      run_time=1.0)

        exp_curve = axes.plot(gamma_pdf(1, 0.5), x_range=[0.02, 6],
                              color=ACCENT, stroke_width=4)
        exp_card = card("Exponential",
                        r"f_X(x) = \lambda e^{-\lambda x}",
                        r"\alpha = 1")

        with self.voiceover(
            text="Set alpha to one, and the powers of x vanish: what "
                 "remains is lambda e to the minus lambda x — "
                 "the exponential distribution, last video's star, sitting at "
                 "the very first notch of the dial."
        ):
            self.play(Create(exp_curve), run_time=1.0)
            self.play(FadeIn(exp_card, shift=RIGHT * 0.3), run_time=0.7)

        chi_curve = axes.plot(gamma_pdf(2, 0.5), x_range=[0.02, 6],
                              color=ACCENT, stroke_width=4)
        chi_card = card("Chi-Square",
                        r"X = Z_1^2 + \cdots + Z_k^2",
                        r"\lambda = \tfrac{1}{2},\ \alpha = \tfrac{k}{2}")

        # (2026-07-04 draft review, 2:50) "the Gaussian density", not
        # "the bell curve" -- no bare "bell"; the gamma beat keeps this
        # video's single allowed "bell curve" mention.
        # (2026-07-05 draft review) "kai" phonetic respelling for TTS --
        # spoken form only; the card and formulas keep "Chi-Square".
        with self.voiceover(
            text="Set lambda to one half and alpha to k over two, and the "
                 "family becomes the kai square distribution with k "
                 "degrees of freedom. Its construction comes from the "
                 "Gaussian density: square k independent standard normal "
                 "variables and add them, and the sum is kai square. That "
                 "construction makes it a workhorse of statistical "
                 "inference."
        ):
            self.play(Transform(exp_curve, chi_curve),
                      Transform(exp_card, chi_card), run_time=1.1)

        erl_curve = axes.plot(gamma_pdf(4, 2.0), x_range=[0.02, 6],
                              color=ACCENT, stroke_width=4)
        erl_card = card("Erlang",
                        r"S_m = X_1 + \cdots + X_m",
                        r"\alpha = m")

        with self.voiceover(
            text="Set alpha to a positive integer m, and the family is "
                 "called Erlang. Here the construction is a sum of waits: "
                 "add m independent exponential waiting times, each with "
                 "rate lambda."
        ):
            self.play(Transform(exp_curve, erl_curve),
                      Transform(exp_card, erl_card), run_time=1.1)

        self.play(FadeOut(VGroup(gen, chart, exp_curve, exp_card)),
                  run_time=0.5)

        # The arrival stream from video 29, with the waits bracketed:
        # the m-th arrival time is the sum of m exponential waits.
        x0, y0 = -4.6, 0.6
        arrivals = [-3.4, -2.6, -1.0, 0.2, 1.8]
        timeline = Arrow([-5.0, y0, 0], [4.6, y0, 0],
                         color=MUTED, stroke_width=3, buff=0,
                         max_tip_length_to_length_ratio=0.03)
        t_lab = MathTex("t", font_size=CAPTION, color=MUTED)
        t_lab.next_to(timeline.get_end(), DOWN, buff=0.2)
        tick = Line([x0, y0 - 0.15, 0], [x0, y0 + 0.15, 0],
                    color=MUTED, stroke_width=3)
        zero_lab = MathTex("0", font_size=CAPTION, color=MUTED)
        zero_lab.next_to(tick, UP, buff=0.15)
        dots = VGroup(*[Dot(radius=0.09, color=INK).move_to([x, y0, 0])
                        for x in arrivals])

        def wait_brace(xa, xb, label_tex):
            seg = Line([xa, y0 - 0.12, 0], [xb, y0 - 0.12, 0],
                       stroke_opacity=0)
            brace = Brace(seg, DOWN, buff=0.1, color=MUTED)
            lab = MathTex(label_tex, font_size=CAPTION, color=INK)
            lab.next_to(brace, DOWN, buff=0.15)
            return VGroup(brace, lab)

        w1 = wait_brace(x0, arrivals[0], r"X_1")
        w2 = wait_brace(arrivals[0], arrivals[1], r"X_2")
        w3 = wait_brace(arrivals[1], arrivals[2], r"X_3")
        cdots = MathTex(r"\cdots", font_size=SMALL, color=MUTED)
        cdots.move_to([(arrivals[2] + arrivals[4]) / 2, y0 - 0.65, 0])

        long_seg = Line([x0, y0 - 1.55, 0], [arrivals[4], y0 - 1.55, 0],
                        stroke_opacity=0)
        long_brace = Brace(long_seg, DOWN, buff=0.0, color=MUTED)
        sm_lab = MathTex(r"S_m = X_1 + \cdots + X_m",
                         font_size=SMALL, color=ACCENT)
        sm_lab.next_to(long_brace, DOWN, buff=0.2)

        mark_intended_overlap(
            timeline, t_lab, tick, zero_lab, dots, w1, w2, w3, cdots,
            long_brace, sm_lab,
            reason="arrival stream with bracketed, summed waits")

        with self.voiceover(
            text="Picture the arrival stream from last video. The wait to "
                 "the first arrival is exponential. The wait to the second "
                 "stacks two of them. Keep going, and the time of the m-th "
                 "arrival is Erlang — its density humps and drifts "
                 "rightward as m grows."
        ):
            self.play(Create(timeline), FadeIn(t_lab), Create(tick),
                      FadeIn(zero_lab), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots],
                                  lag_ratio=0.15), run_time=0.9)
            self.play(FadeIn(w1), run_time=0.5)
            self.play(FadeIn(w2), run_time=0.5)
            self.play(FadeIn(w3), FadeIn(cdots), run_time=0.5)
            self.play(FadeIn(long_brace), Write(sm_lab),
                      dots[4].animate.set_color(ACCENT), run_time=0.9)

        recap = VGroup(
            MathTex(r"\text{Exponential: } \alpha = 1",
                    font_size=CAPTION, color=MUTED),
            MathTex(r"\text{Chi-square: } \lambda = \tfrac{1}{2},"
                    r"\ \alpha = \tfrac{k}{2}",
                    font_size=CAPTION, color=MUTED),
            MathTex(r"\text{Erlang: } \alpha = m",
                    font_size=CAPTION, color=MUTED),
        ).arrange(RIGHT, buff=0.9)
        recap.move_to(DOWN * 2.9)
        fit_to_frame(recap)

        with self.voiceover(
            text="Three names, one formula. The label on the curve tells "
                 "you which construction produced it."
        ):
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2)
                                    for r in recap],
                                  lag_ratio=0.25), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class RayleighDistribution(VoiceoverScene):
    """Beat: rayleigh -- a Gaussian vector's length, and the naming trap."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Rayleigh Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Now build sideways from the Gaussian."
        ):
            self.wait(0.3)

        plane = Axes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=4.2, y_length=4.2,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "color": MUTED},
            tips=False,
        ).move_to(LEFT * 3.4 + DOWN * 0.6)
        cloud = VGroup(*[
            Dot(radius=0.05, color=BAR).move_to(plane.c2p(x, y))
            for x, y in GAUSS_POINTS
        ])
        mark_intended_overlap(plane, cloud,
                              reason="Gaussian scatter across the plane")

        with self.voiceover(
            text="Scatter a cloud of points on a plane, with each "
                 "coordinate an independent zero mean Gaussian."
        ):
            self.play(Create(plane), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, scale=1.8) for d in cloud],
                                  lag_ratio=0.03), run_time=1.4)

        px, py = GAUSS_POINTS[RADIUS_POINT_INDEX]
        radius = Line(plane.c2p(0, 0), plane.c2p(px, py),
                      color=ACCENT, stroke_width=4)
        mark_intended_overlap(radius, plane, cloud,
                              reason="radius drawn across the scatter")
        r_form = MathTex(r"R = \sqrt{X^2 + Y^2}", font_size=BODY)
        r_form.move_to(RIGHT * 3.3 + UP * 1.9)

        with self.voiceover(
            text="Then ask a geometric question: how far does a point land "
                 "from the center? That length, the square root of X "
                 "squared plus Y squared, is a new random variable."
        ):
            self.play(cloud[RADIUS_POINT_INDEX].animate
                      .set_color(ACCENT).scale(1.6), run_time=0.5)
            self.play(Create(radius), run_time=0.7)
            self.play(Write(r_form), run_time=0.9)

        pdf = MathTex(
            r"f_R(r)", "=",
            r"\frac{r}{\sigma^2}\, e^{-r^2 / (2\sigma^2)}",
            font_size=SMALL,
        ).next_to(r_form, DOWN, buff=0.4)
        mini = Axes(
            x_range=[0, 4, 1], y_range=[0, 0.7, 0.35],
            x_length=3.4, y_length=1.6,
            axis_config={"include_numbers": False, "include_ticks": False,
                         "color": MUTED},
            tips=False,
        ).next_to(pdf, DOWN, buff=0.35)
        mini_curve = mini.plot(rayleigh_pdf(1.0), x_range=[0, 4],
                               color=INK, stroke_width=3)
        # (2026-07-04 draft review, 4:10) the muted "wireless fading"
        # caption is removed -- on-screen only; the narration still tells
        # the urban-radio story.

        with self.voiceover(
            text="Its density is the Rayleigh distribution: r over sigma "
                 "squared, times e to the minus r squared over two sigma "
                 "squared. It rises from zero, peaks, and decays — the "
                 "shape of amplitude fading in urban radio, where "
                 "reflected signals add like Gaussian coordinates."
        ):
            self.play(radius.animate.set_color(INK),
                      Write(pdf), run_time=1.0)
            self.play(pdf.animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(mini), Create(mini_curve), run_time=0.9)

        var_line = MathTex(
            variance("R"), "=", r"\frac{4 - \pi}{2}\, \sigma^2",
            font_size=SMALL,
        ).move_to(LEFT * 3.3 + UP * 0.4)
        trap_cap = MathTex(
            r"\sigma^2 \text{ names the Gaussians inside}",
            font_size=CAPTION, color=MUTED,
        ).next_to(var_line, DOWN, buff=0.3)

        with self.voiceover(
            text="One naming trap deserves a clear sentence. The sigma "
                 "squared in the formula honors the Gaussians inside the "
                 "construction. It is not the Rayleigh's own variance, "
                 "which works out to four minus pi over two, times sigma "
                 "squared."
        ):
            self.play(FadeOut(VGroup(plane, cloud, radius)), run_time=0.6)
            self.play(pdf.animate.set_color(INK),
                      Write(var_line), run_time=1.0)
            self.play(var_line.animate.set_color(ACCENT),
                      FadeIn(trap_cap, shift=UP * 0.2), run_time=0.6)

        sq_line = MathTex(r"R^2 \sim \text{exponential}",
                          font_size=SMALL, color=MUTED)
        sq_line.next_to(trap_cap, DOWN, buff=0.45)

        with self.voiceover(
            text="And one bonus connection: square a Rayleigh variable and "
                 "you get an exponential — the gallery keeps looping back "
                 "on itself."
        ):
            self.play(FadeIn(sq_line, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class LaplaceCauchy(VoiceoverScene):
    """Beat: laplace-cauchy -- the splice, the warning, and the gallery."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # (2026-07-04 draft review, 5:10) the two densities are treated in
        # sequence, each under its own title: the beat opens on "Laplace"
        # and the title Transforms to "Cauchy" when the narration moves on.
        # The spoken opener is the cue that two densities remain.
        title = section_title("Laplace")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Two curves remain, and they bracket the gallery."
        ):
            self.wait(0.3)

        chart, axes = density_axes([-4, 4, 1], [0, 0.6, 0.2])
        chart.to_edge(DOWN, buff=0.8)
        right_half = axes.plot(lambda x: 0.5 * math.exp(-x),
                               x_range=[0, 4], color=INK, stroke_width=4)
        left_half = axes.plot(lambda x: 0.5 * math.exp(x),
                              x_range=[-4, 0], color=ACCENT, stroke_width=4)
        seam = Dot(axes.c2p(0, 0.5), radius=0.07, color=ACCENT)

        # (2026-07-04 draft review, 5:10) the splice narration says the
        # result is renormalized -- the factor of one half keeps the area
        # at one -- matching the on-screen e^{-|x|/b}/(2b).
        with self.voiceover(
            text="Take last video's exponential density, flip a copy "
                 "across zero, glue the halves at the peak, and "
                 "renormalize — the factor of one half keeps the area at "
                 "one."
        ):
            self.play(Create(axes), Write(chart[1]), run_time=0.7)
            self.play(Create(right_half), run_time=0.8)
            self.play(TransformFromCopy(right_half, left_half),
                      run_time=1.0)
            self.play(FadeIn(seam, scale=2.0), run_time=0.4)

        lap = MathTex(
            r"f_X(x)", "=", r"\frac{1}{2b}\, e^{-|x|/b}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        diff = MathTex(r"X_1 - X_2 \sim \text{Laplace}",
                       font_size=SMALL, color=MUTED)
        diff.next_to(lap, DOWN, buff=0.3)

        with self.voiceover(
            text="The result is the Laplace distribution: e to the minus "
                 "absolute value of x over b, divided by two b. It is "
                 "symmetric like a Gaussian, but sharper at the peak and "
                 "heavier in the tails — and it records its own "
                 "construction: the difference of two independent "
                 "exponential waits is Laplace."
        ):
            self.play(FadeOut(seam),
                      left_half.animate.set_color(INK),
                      Write(lap), run_time=1.0)
            self.play(lap.animate.set_color(ACCENT),
                      FadeIn(diff, shift=UP * 0.2), run_time=0.6)

        cau = MathTex(
            r"f_X(x)", "=",
            r"\frac{\gamma}{\pi \left( \gamma^2 + x^2 \right)}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        nomean = Text("no mean, no variance", font_size=CAPTION,
                      color=MUTED)
        nomean.next_to(cau, DOWN, buff=0.25)
        ghost = axes.plot(gauss_pdf(1.0), x_range=[-4, 4],
                          color=MUTED, stroke_width=3)
        ghost_lab = Text("Gaussian", font_size=CAPTION, color=MUTED)
        ghost_lab.move_to(axes.c2p(-1.7, 0.45))
        cau_curve = axes.plot(cauchy_pdf(1.0), x_range=[-4, 4],
                              color=INK, stroke_width=4)
        cau_lab = Text("Cauchy", font_size=CAPTION, color=INK)
        cau_lab.move_to(axes.c2p(2.4, 0.17))
        tails = VGroup(
            axes.plot(cauchy_pdf(1.0), x_range=[1.8, 4],
                      color=ACCENT, stroke_width=6),
            axes.plot(cauchy_pdf(1.0), x_range=[-4, -1.8],
                      color=ACCENT, stroke_width=6),
        )
        cauchy_title = section_title("Cauchy").to_edge(UP)

        # (2026-07-04 draft review, 5:10) the section title Transforms
        # from "Laplace" to "Cauchy" as the narration moves on.
        with self.voiceover(
            text="The final curve looks tame: gamma over pi times gamma "
                 "squared plus x squared. This is the Cauchy distribution, "
                 "and its tails decay so slowly that the mean is "
                 "undefined. No mean, no variance, no higher moments."
        ):
            self.play(FadeOut(VGroup(lap, diff, right_half, left_half)),
                      Transform(title, cauchy_title),
                      run_time=0.5)
            self.play(Write(cau), run_time=0.9)
            self.play(FadeIn(ghost), FadeIn(ghost_lab), run_time=0.6)
            self.play(Create(cau_curve), FadeIn(cau_lab), run_time=0.9)
            self.play(LaggedStart(*[Create(t) for t in tails],
                                  lag_ratio=0.3),
                      FadeIn(nomean, shift=UP * 0.2), run_time=0.9)

        chart2, axes2 = density_axes([0, 13, 2], [-6, 8, 2],
                                     y_length=3.6, x_name="n")
        chart2.to_edge(DOWN, buff=0.8)
        run_mean = VMobject(color=ACCENT, stroke_width=4)
        run_mean.set_points_as_corners([
            axes2.c2p(n + 1, v)
            for n, v in enumerate(CAUCHY_RUNNING_MEANS)
        ])
        settle = Text("the running mean refuses to settle",
                      font_size=CAPTION, color=MUTED)
        settle.next_to(title, DOWN, buff=0.45)

        with self.voiceover(
            text="It gets worse. Average n independent Cauchy variables, "
                 "and the sample mean is Cauchy with the same parameter. "
                 "Watch a running mean: it jumps, drifts, and refuses to "
                 "settle, no matter how many samples arrive. Averaging is "
                 "not a universal cure."
        ):
            self.play(FadeOut(VGroup(cau, nomean, ghost, ghost_lab,
                                     cau_curve, cau_lab, tails, chart)),
                      run_time=0.6)
            self.play(Create(axes2), Write(chart2[1]),
                      FadeIn(settle), run_time=0.8)
            self.play(Create(run_mean), run_time=2.6, rate_func=linear)

        gallery_title = section_title("The Gallery").to_edge(UP)

        def panel(fn, x_range, y_max, name, tag):
            ax = Axes(
                x_range=[x_range[0], x_range[1]],
                y_range=[0, y_max],
                x_length=2.7, y_length=1.1,
                axis_config={"include_numbers": False,
                             "include_ticks": False, "color": MUTED},
                tips=False,
            )
            curve = ax.plot(fn, x_range=list(x_range),
                            color=BAR, stroke_width=3)
            name_t = Text(name, font_size=CAPTION, color=INK)
            tag_t = Text(tag, font_size=CAPTION, color=MUTED).scale(0.85)
            labels = VGroup(name_t, tag_t).arrange(DOWN, buff=0.1)
            labels.next_to(ax, DOWN, buff=0.15)
            return VGroup(ax, curve, labels)

        panels = VGroup(
            panel(gamma_pdf(3, 1.5), (0.02, 5), 0.5,
                  "Gamma", "the factorial, extended"),
            panel(gamma_pdf(2, 0.5), (0.02, 8), 0.25,
                  "Chi-Square", "squared normals, summed"),
            panel(gamma_pdf(4, 2.0), (0.02, 5), 0.55,
                  "Erlang", "exponential waits, summed"),
            panel(rayleigh_pdf(1.0), (0, 4), 0.7,
                  "Rayleigh", "a Gaussian vector's length"),
            panel(laplace_pdf(1.0), (-4, 4), 0.6,
                  "Laplace", "a difference of two waits"),
            panel(cauchy_pdf(1.0), (-4, 4), 0.4,
                  "Cauchy", "tails too heavy to tame"),
        )
        panels.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.55))
        panels.next_to(gallery_title, DOWN, buff=0.5)
        fit_to_frame(VGroup(gallery_title, panels))
        mark_intended_overlap(
            panels, reason="gallery composition of six labelled curves")

        # (2026-07-04 draft review, 6:30) the closing line is "Every curve
        # is a construction." -- "remembered" dropped.
        # (2026-07-05 draft review) "kai" phonetic respelling for TTS --
        # spoken form only; the gallery panel keeps "Chi-Square".
        with self.voiceover(
            text="Step back and read the gallery: the gamma from the "
                 "extended factorial, the kai square from squared normals, "
                 "the Erlang from summed waits, the Rayleigh from a "
                 "vector's length, the Laplace from a difference of waits, "
                 "and the Cauchy from tails too heavy to tame. Every curve "
                 "is a construction."
        ):
            self.play(FadeOut(VGroup(settle, chart2, run_mean)),
                      Transform(title, gallery_title), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2)
                                    for p in panels],
                                  lag_ratio=0.18), run_time=2.2)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["A named density is a record of a construction:",
             "know how a curve is built, and you know when to reach for it."],
            next_title="Derived Distributions",
        )
        tag = progress_tag(5, 5).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="The key idea of this video: a named density is a record "
                 "of a construction — know how a curve is built, and you "
                 "know when to reach for it. That closes chapter eight. "
                 "Next chapter: derived distributions — what happens when "
                 "a continuous random variable is pushed through a "
                 "function."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        self.wait(0.5)
        self.play(FadeOut(outro), FadeOut(tag))
