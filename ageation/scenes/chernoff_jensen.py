# derived_from: content/36-chernoff-jensen-script.md
# derived_from_sha256: 20b750e1fdcb4af44af30f6f8a599668c41e1718a9907d278d7995681cd262bc
"""Chapter 10, Video 3 -- The Chernoff Bound and Jensen's Inequality.

Source notes : expectations_and_bounds.tex (subsections "The Chernoff
               Bound" and "Jensen's Inequality" only).
Script       : content/36-chernoff-jensen-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark
segment -- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/chernoff_jensen.py ChapterOverview
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
    section_title,
    axis_label_x,
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


# --- Shared tail-bound chart (the notes' Chernoff figure) --------------------
A_VAL = 2.0     # the threshold a
X_MAX = 4.0
Y_MAX = 3.5


def tail_axes():
    """Axes with the indicator step 1_{[a, inf)} drawn on them.

    Returns (axes, step_group, label_group); the caller positions `axes`
    BEFORE calling exp_curve so plotted curves land on the moved axes.
    """
    axes = Axes(
        x_range=[0, X_MAX, 1],
        y_range=[0, Y_MAX, 1],
        x_length=5.6,
        y_length=3.4,
        axis_config={"include_numbers": False, "include_ticks": False},
        tips=False,
    )
    return axes


def tail_step(axes):
    """The indicator step plus its labels, drawn on already-placed axes."""
    step_lo = Line(axes.c2p(0, 0), axes.c2p(A_VAL, 0),
                   color=INK, stroke_width=3.5)
    step_hi = Line(axes.c2p(A_VAL, 1), axes.c2p(X_MAX, 1),
                   color=INK, stroke_width=3.5)
    riser = DashedLine(axes.c2p(A_VAL, 0), axes.c2p(A_VAL, 1),
                       color=MUTED, stroke_width=2, dash_length=0.1)
    step = VGroup(step_lo, step_hi, riser)
    a_tick = MathTex("a", font_size=SMALL, color=MUTED)
    a_tick.next_to(axes.c2p(A_VAL, 0), DOWN, buff=0.25)
    one_tick = MathTex("1", font_size=CAPTION, color=MUTED)
    one_tick.next_to(axes.c2p(0, 1), LEFT, buff=0.15)
    ind_label = MathTex(r"\mathbf{1}_{[a,\infty)}(x)",
                        font_size=SMALL, color=INK)
    ind_label.next_to(axes.c2p(3.1, 1), DOWN, buff=0.35)
    labels = VGroup(a_tick, one_tick, ind_label)
    return step, labels


def exp_curve(axes, s, color=BAR, stroke_width=3):
    """The dominator e^{s(x - a)} clipped to the visible y-range."""
    x_hi = min(X_MAX, A_VAL + np.log(Y_MAX * 0.95) / s)
    return axes.plot(lambda x, s=s: np.exp(s * (x - A_VAL)),
                     x_range=[0, x_hi], color=color,
                     stroke_width=stroke_width)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + four-line outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            ["The Chernoff Bound", "and Jensen's Inequality"],
            ["Apply the MGF for a tail bound, then let",
             "a function's own convexity bound an expectation."],
            kicker="Chapter 10  ·  Expectations and Bounds",
        )
        tag = progress_tag(3, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The exponential dominator", font_size=BODY, color=INK),
            Text("2.  The Chernoff bound", font_size=BODY, color=INK),
            Text("3.  Convexity and tangent lines", font_size=BODY,
                 color=INK),
            Text("4.  Jensen's inequality", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text='Last video, Markov and Chebyshev bounded a tail using one moment, then two. This video spends everything.'
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
            text="First we run the Chebyshev template with an exponential dominating function, and the moment generating function we just built turns into a tail bound."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text='Then we notice we hold a whole family of bounds, one for every rate, and optimize to reach the celebrated Chernoff bound.'
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text='Next, a change of key: convex functions sit above their tangent lines,'
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and that single picture proves Jensen's inequality, the reason averages and curved functions never commute."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChernoffConstruction(VoiceoverScene):
    """Beat: chernoff-construction -- e^{s(x-a)} dominates the indicator."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Exponential Dominator")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        goal = MathTex(pr(r"X \geq a"), r"\;\leq\;", r"?",
                       font_size=BODY).move_to(RIGHT * 3.3 + UP * 1.7)
        fit_to_frame(goal)

        axes = tail_axes()
        axes.move_to(LEFT * 3.2 + DOWN * 1.0)
        step, labels = tail_step(axes)
        curve = exp_curve(axes, 0.6)
        pin = Dot(axes.c2p(A_VAL, 1), radius=0.07, color=ACCENT)
        clabel = MathTex(r"e^{s(x-a)}", font_size=SMALL, color=BAR)
        clabel.next_to(curve.get_end(), LEFT, buff=0.35)
        # Chart internals share the plot region by design: the dominator
        # fan, the step, the pin, and the in-plot labels all coexist.
        mark_intended_overlap(
            axes, step, labels, curve, pin, clabel,
            reason="dominator and labels share the indicator's plot region")

        with self.voiceover(
            text='We want the right tail: the probability that X is at least a. The last video taught the recipe: write the probability as the expectation of an indicator, then dominate that indicator by a function whose expectation you can compute.'
        ):
            self.play(Write(goal), run_time=0.9)

        with self.voiceover(
            text='Here is the indicator of the interval from a to infinity: zero on the left, then a step up to one at a.'
        ):
            self.play(Create(axes), run_time=0.7)
            self.play(Create(step[0]), Create(step[2]), Create(step[1]),
                      FadeIn(labels[0]), FadeIn(labels[1]), run_time=1.0)
            self.play(Write(labels[2]), run_time=0.7)

        with self.voiceover(
            text='This time, dominate it with an exponential: e to the s times x minus a, for some positive rate s. At x equals a the curve passes through one exactly, and it only grows from there, so it sits above the step everywhere.'
        ):
            self.play(Create(curve), run_time=1.2)
            self.play(Write(clabel), run_time=0.6)
            self.play(FadeIn(pin, scale=1.6), run_time=0.6)

        rhs = VGroup(
            MathTex(r"h(x) = e^{sx},\quad s > 0", font_size=SMALL,
                    color=INK),
            MathTex(r"S = [a, \infty)", font_size=SMALL, color=INK),
            MathTex(r"i_S = \inf_{x \geq a} e^{sx} = e^{sa}",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rhs.move_to(RIGHT * 3.3 + UP * 0.45)
        fit_to_frame(rhs)

        with self.voiceover(
            text='In the language of the Chebyshev inequality, the function h of x is e to the s x, the set S is the interval from a to infinity, and the infimum of h over S is e to the s a.'
        ):
            self.play(pin.animate.set_color(INK), run_time=0.4)
            self.play(Write(rhs[0]), run_time=0.8)
            self.play(Write(rhs[1]), run_time=0.7)
            self.play(Write(rhs[2]), run_time=0.9)

        bound = MathTex(pr(r"X \geq a"), r"\leq",
                        r"e^{-sa}\," + expectation("e^{sX}"),
                        font_size=BODY)
        bound.next_to(rhs, DOWN, buff=0.5)
        fit_to_frame(bound)

        with self.voiceover(
            text='Divide through, and the tail is at most e to the minus s a times the expectation of e to the s X.'
        ):
            self.play(Write(bound), run_time=1.1)
            self.play(bound[2].animate.set_color(ACCENT), run_time=0.5)

        mgf = MathTex(r"=\;", r"e^{-sa}\,", r"M_X(s)", font_size=BODY)
        mgf.next_to(bound, DOWN, buff=0.35).align_to(bound[2], LEFT)
        fit_to_frame(mgf)

        with self.voiceover(
            text='Look closely at that last factor. It is the moment generating function of X, evaluated at s, the function we built and told you to keep in your pocket. Markov spent one moment. Chebyshev spent two. This construction spends the entire catalog at once.'
        ):
            self.play(bound[2].animate.set_color(INK), Write(mgf),
                      run_time=1.0)
            self.play(mgf[2].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChernoffOptimize(VoiceoverScene):
    """Beat: chernoff-optimize -- the fan of bounds and the best of them."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Chernoff Bound")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text='Nothing forced our choice of rate.'
        ):
            self.wait(0.3)

        # The fan: one dominator per s, all pinned at (a, 1).
        axes = tail_axes()
        axes.move_to(LEFT * 3.2 + DOWN * 1.0)
        step, labels = tail_step(axes)
        fan_ss = [0.4, 0.7, 1.1, 1.7]
        fan = VGroup(*[exp_curve(axes, s) for s in fan_ss])
        pin = Dot(axes.c2p(A_VAL, 1), radius=0.07, color=INK)
        mark_intended_overlap(
            axes, step, labels, fan, pin,
            reason="the fan of dominators shares the indicator's plot region")

        fam = MathTex(r"e^{s(x-a)},\quad s > 0", font_size=BODY, color=BAR)
        fam.move_to(RIGHT * 3.4 + UP * 1.2)
        fit_to_frame(fam)
        bnd = MathTex(pr(r"X \geq a"), r"\leq", r"e^{-sa}\, M_X(s)",
                      font_size=SMALL, color=INK)
        bnd.next_to(fam, DOWN, buff=0.55)
        per_s = Text("one bound for every s", font_size=CAPTION, color=MUTED)
        per_s.next_to(bnd, DOWN, buff=0.3)

        with self.voiceover(
            text='Every positive s gives an exponential pinned to the point a comma one, and every one of them dominates the step: a shallow curve for small s, a steeper one hugging the corner as s grows. Each member of the family certifies its own bound, e to the minus s a times M X of s.'
        ):
            self.play(Create(axes), run_time=0.6)
            self.play(Create(step[0]), Create(step[2]), Create(step[1]),
                      FadeIn(labels), run_time=0.8)
            self.play(FadeIn(pin, scale=1.6), run_time=0.4)
            self.play(LaggedStart(*[Create(c) for c in fan],
                                  lag_ratio=0.45), run_time=2.4)
            self.play(Write(fam), run_time=0.7)
            self.play(Write(bnd), FadeIn(per_s), run_time=0.9)

        # The dial: bound value against s; slide to the minimum.
        self.play(FadeOut(VGroup(axes, step, labels, fan, pin, fam)),
                  run_time=0.5)

        daxes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=5.2,
            y_length=3.0,
            axis_config={"include_numbers": True, "font_size": 30},
            tips=False,
        )
        daxes.move_to(LEFT * 2.8 + DOWN * 1.0)
        s_lab = axis_label_x(daxes, MathTex("s", font_size=BODY,
                                            color=MUTED))
        b_lab = MathTex(r"e^{-sa} M_X(s)", font_size=SMALL, color=MUTED)
        b_lab.next_to(daxes.c2p(0, 1.2), UP, buff=0.25)

        def bound_val(s):
            return np.exp(s * s / 2 - 2 * s)

        dcurve = daxes.plot(bound_val, x_range=[0.05, 3.4],
                            color=BAR, stroke_width=3)
        path = daxes.plot(bound_val, x_range=[0.3, 2.0])
        marker = Dot(daxes.input_to_graph_point(0.3, dcurve),
                     radius=0.09, color=ACCENT)
        mark_intended_overlap(
            daxes, dcurve, marker,
            reason="the marker rides the bound-versus-s curve")

        with self.voiceover(
            text="So we hold not one bound but a dial's worth, and you have rehearsed this move: for the Cantelli inequality we tuned a quadratic's offset and kept the minimum. Same move, sharper weapon. As s varies, the bound value traces a curve, and we slide down to its lowest point."
        ):
            self.play(Create(daxes), FadeIn(s_lab), FadeIn(b_lab),
                      run_time=0.8)
            self.play(Create(dcurve), run_time=1.0)
            self.play(FadeIn(marker, scale=1.6), run_time=0.5)
            self.play(MoveAlongPath(marker, path), run_time=2.2,
                      rate_func=smooth)
            self.play(Indicate(marker, color=ACCENT, scale_factor=1.3),
                      run_time=0.6)

        self.play(FadeOut(VGroup(daxes, s_lab, b_lab, dcurve, marker, bnd,
                                 per_s)), run_time=0.5)

        chern = MathTex(pr(r"X \geq a"), r"\;\leq\;",
                        r"\inf_{s>0}\, e^{-sa}\, M_X(s)",
                        font_size=BODY).move_to(UP * 0.9)
        fit_to_frame(chern)
        chern_name = Text("the Chernoff bound", font_size=CAPTION,
                          color=MUTED)
        chern_name.next_to(chern, DOWN, buff=0.3)

        with self.voiceover(
            text='Taking the best member of the family gives the Chernoff bound: the probability that X is at least a is at most the infimum, over positive s, of e to the minus s a times M X of s. Which rate wins depends on the distribution of X and on a, and that is why the bound carries the search inside it.'
        ):
            self.play(Write(chern), run_time=1.4)
            self.play(chern[2].animate.set_color(ACCENT),
                      FadeIn(chern_name), run_time=0.7)

        ledger_rows = VGroup()
        entries = [
            ("Markov", expectation("X")),
            ("Chebyshev", expectation("X^2")),
            ("Chernoff", r"M_X(s)"),
        ]
        for i, (nm, tex) in enumerate(entries):
            y = -1.0 - 0.62 * i
            name = Text(nm, font_size=SMALL, color=MUTED)
            name.move_to([-2.9, y, 0], aligned_edge=LEFT)
            cost = MathTex(tex, font_size=SMALL, color=INK)
            cost.move_to([0.4, y, 0], aligned_edge=LEFT)
            ledger_rows.add(VGroup(name, cost))

        with self.voiceover(
            text="Read the chapter's ledger. Markov paid one moment, Chebyshev paid a second, and Chernoff pays the whole moment generating function, which is why it earns exponentially sharp tails and a central role in coding and communications."
        ):
            self.play(FadeIn(ledger_rows[0], shift=RIGHT * 0.3),
                      run_time=0.6)
            self.play(FadeIn(ledger_rows[1], shift=RIGHT * 0.3),
                      run_time=0.6)
            self.play(FadeIn(ledger_rows[2], shift=RIGHT * 0.3),
                      run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConvexityTangent(VoiceoverScene):
    """Beat: convexity-tangent -- a convex curve sits above its tangents."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Convexity and Tangent Lines")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        def g_val(x):
            return 0.4 * (x - 2.0) ** 2 + 0.6

        def g_slope(x):
            return 0.8 * (x - 2.0)

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=5.4,
            y_length=3.2,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        )
        axes.move_to(LEFT * 3.3 + DOWN * 1.0)
        curve = axes.plot(g_val, x_range=[0.15, 3.85],
                          color=BAR, stroke_width=3)
        glabel = MathTex("g(x)", font_size=SMALL, color=BAR)
        glabel.next_to(axes.input_to_graph_point(3.7, curve), UP, buff=0.25)

        tracker = ValueTracker(1.0)

        def tangent_maker():
            a = tracker.get_value()
            ga, sl = g_val(a), g_slope(a)
            xlo = max(a - 1.2, 0.15)
            xhi = min(a + 1.2, 3.85)
            return Line(axes.c2p(xlo, ga + sl * (xlo - a)),
                        axes.c2p(xhi, ga + sl * (xhi - a)),
                        color=ACCENT, stroke_width=3)

        def anchor_maker():
            a = tracker.get_value()
            return Dot(axes.c2p(a, g_val(a)), radius=0.08, color=ACCENT)

        tangent = always_redraw(tangent_maker)
        anchor = always_redraw(anchor_maker)
        mark_intended_overlap(
            axes, curve, glabel, tangent, anchor,
            reason="the tangent rides the convex curve by design")

        conv = MathTex(r"\frac{d^2 g}{dx^2}(x) \geq 0", font_size=BODY,
                       color=INK).move_to(RIGHT * 3.4 + UP * 1.6)
        fit_to_frame(conv)
        conv_cap = Text("g is convex", font_size=CAPTION, color=MUTED)
        conv_cap.next_to(conv, DOWN, buff=0.25)

        with self.voiceover(
            text="For the chapter's last inequality, change key entirely. No dominating functions this time; the bound flows from the shape of a single function."
        ):
            self.wait(0.3)

        with self.voiceover(
            text='Call g convex when its second derivative is nonnegative everywhere, so the curve bends upward, like a parabola or an exponential.'
        ):
            self.play(Create(axes), run_time=0.6)
            self.play(Create(curve), Write(glabel), run_time=1.0)
            self.play(Write(conv), FadeIn(conv_cap), run_time=0.9)

        with self.voiceover(
            text='Draw a tangent line anywhere on such a curve and watch: the curve never dips below it. Slide the anchor point along, and the picture holds everywhere. That is the claim to prove.'
        ):
            self.play(FadeIn(anchor, scale=1.4), Create(tangent),
                      run_time=0.8)
            self.play(tracker.animate.set_value(3.0), run_time=2.2,
                      rate_func=smooth)
            self.play(tracker.animate.set_value(1.4), run_time=1.6,
                      rate_func=smooth)

        tangent.clear_updaters()
        anchor.clear_updaters()

        ftc = MathTex(r"g(x) = g(a) + \int_a^x \frac{dg}{dx}(u)\, du",
                      font_size=SMALL, color=INK)
        ftc.move_to(RIGHT * 3.4 + UP * 0.2)
        fit_to_frame(ftc)

        with self.voiceover(
            text='The fundamental theorem of calculus writes g of x as g of a plus the integral of the derivative from a up to x.'
        ):
            self.play(tangent.animate.set_color(MUTED),
                      anchor.animate.set_color(MUTED), run_time=0.4)
            self.play(Write(ftc), run_time=1.1)

        mono = MathTex(r"\geq g(a) + \int_a^x \frac{dg}{dx}(a)\, du",
                       font_size=SMALL, color=INK)
        mono.next_to(ftc, DOWN, buff=0.32).align_to(ftc, LEFT)
        mono.shift(RIGHT * 0.9)
        fit_to_frame(mono)

        with self.voiceover(
            text='A nonnegative second derivative makes the first derivative monotone increasing, so replacing the derivative inside the integral by its value at a can only shrink the result.'
        ):
            self.play(Write(mono), run_time=1.1)

        result = MathTex(r"g(x) \geq g(a) + (x - a)\,\frac{dg}{dx}(a)",
                         font_size=BODY, color=INK)
        result.next_to(mono, DOWN, buff=0.5)
        result.set_x(3.3)
        fit_to_frame(result)

        with self.voiceover(
            text='What remains is the equation of a line: g of x is at least g of a plus x minus a times the slope at a. A convex curve lies above every one of its tangent lines, an inequality manufactured from curvature alone.'
        ):
            self.play(ftc.animate.set_color(MUTED),
                      mono.animate.set_color(MUTED), run_time=0.4)
            self.play(Write(result), run_time=1.1)
            self.play(result.animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JensenInequality(VoiceoverScene):
    """Beat: jensen -- anchor the tangent at the mean and average."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Jensen's Inequality")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        line1 = MathTex(r"g(X) \geq g(a) + (X - a)\,\frac{dg}{dx}(a)",
                        font_size=BODY, color=INK).move_to(UP * 1.7)
        fit_to_frame(line1)

        with self.voiceover(
            text='Now let a random variable ride the tangent.'
        ):
            self.wait(0.3)

        with self.voiceover(
            text='The tangent bound holds at every point x, so it holds with X plugged in: g of X is at least g of a plus X minus a times the slope at a. That is an inequality between random variables, true outcome by outcome.'
        ):
            self.play(Write(line1), run_time=1.2)

        line2 = MathTex(r"a = " + expectation("X"), font_size=BODY,
                        color=INK)
        line2.next_to(line1, DOWN, buff=0.4)

        with self.voiceover(
            text='We may pick the anchor, so pick the one point the whole chapter keeps returning to: anchor the tangent at the mean, a equals the expected value of X.'
        ):
            self.play(Write(line2), run_time=0.9)
            self.play(line2.animate.set_color(ACCENT), run_time=0.5)

        line3 = MathTex(
            expectation("g(X)"),
            r"\geq",
            r"g\left(" + expectation("X") + r"\right)",
            r"+",
            r"\left(" + expectation("X") + r" - " + expectation("X")
            + r"\right)\frac{dg}{dx}\left(" + expectation("X") + r"\right)",
            font_size=SMALL, color=INK,
        )
        line3.next_to(line2, DOWN, buff=0.45)
        fit_to_frame(line3)

        # (2026-07-05 draft review, 5:27) The cancelling term holds its
        # accent through its whole sentence, and the fade is slow, landing
        # exactly on "dies on the spot".
        with self.voiceover(
            text='Take expectations on both sides.'
        ):
            self.play(line2.animate.set_color(INK), Write(line3),
                      run_time=1.4)

        with self.voiceover(
            text='Expectation is linear, so the slope term carries the '
                 'expected value of X minus the expected value of X, and '
                 'that difference is exactly zero.'
        ):
            self.play(line3[4].animate.set_color(ACCENT), run_time=0.8)

        with self.voiceover(
            text='The linear term dies on the spot.'
        ):
            self.play(FadeOut(line3[3], run_time=2.2),
                      FadeOut(line3[4], run_time=2.2))

        jform = MathTex(expectation("g(X)"), r"\;\geq\;",
                        r"g\left(" + expectation("X") + r"\right)",
                        font_size=BODY, color=INK)
        jform.next_to(line3, DOWN, buff=0.65)
        fit_to_frame(jform)
        jbox = SurroundingRectangle(jform, color=ACCENT, buff=0.25)
        jcap = Text("for convex g", font_size=CAPTION, color=MUTED)
        jcap.next_to(jbox, DOWN, buff=0.25)
        jgroup = VGroup(jform, jbox, jcap)

        with self.voiceover(
            text="What survives is Jensen's inequality: for convex g, the expectation of g of X is at least g of the expectation of X, provided both expectations exist. Averages and curved functions do not commute, and convexity tells you which way the inequality tips."
        ):
            self.play(Write(jform), run_time=1.0)
            self.play(Create(jbox), FadeIn(jcap), run_time=0.8)

        cb = MathTex(expectation("X^2"), r"\;\geq\;",
                     r"\left(" + expectation("X") + r"\right)^2",
                     font_size=BODY, color=INK).move_to(DOWN * 1.0)
        cbg = MathTex(r"g(x) = x^2", font_size=SMALL, color=MUTED)
        cbg.next_to(cb, DOWN, buff=0.3)
        cbt = Text("variance is nonnegative", font_size=CAPTION,
                   color=MUTED)
        cbt.next_to(cbg, DOWN, buff=0.2)

        with self.voiceover(
            text='You met an instance long ago. Take g of x equals x squared: Jensen says the second moment is at least the square of the mean, which is precisely the fact that variance is nonnegative. The inequality holds even for convex functions with corners, though that proof is much harder; the smooth case is the honest one at this level.'
        ):
            self.play(FadeOut(line1), FadeOut(line2), FadeOut(line3),
                      jgroup.animate.shift(UP * 1.8), run_time=0.9)
            self.play(Write(cb), run_time=0.9)
            self.play(FadeIn(cbg), FadeIn(cbt), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Expectation is a bounding tool: one moment,",
             "two moments, and the MGF; or convexity."],
            next_title="Joint Continuous Distributions",
        )

        with self.voiceover(
            text='The key idea of this chapter: expectation is a bounding tool. One moment gave Markov, two gave Chebyshev, the whole generating function gave Chernoff, and Jensen needs nothing but curvature.'
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
