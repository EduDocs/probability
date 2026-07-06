# derived_from: content/29-exponential-script.md
# derived_from_sha256: 8de43e28e092845aeacc4c52c9c60198ef68bf0f1e6948540220b8ea80ca056d
"""Chapter 8, Video 4 -- The Exponential Distribution.

Source notes : continuous_random_variables.tex (Section 8.4.3) -- PDF/CDF,
               the server example, the geometric-limit construction, the
               memoryless property, and the half-life example.
Script       : content/29-exponential-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/exponential.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np

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
    pr,
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


def cap_width(mobj, max_w):
    """Scale a single mobject down (never up) to a column width."""
    if mobj.width > max_w:
        mobj.scale(max_w / mobj.width)
    return mobj


def waiting_axes(x_max=4.0, y_max=2.2, y_step=0.5,
                 x_length=6.0, y_length=3.4, x_name="x"):
    """The chapter's shared time-axis chart: axes + an x-name at the tip."""
    # (2026-07-05 draft review, 5:00) tick numbers at TICK -- "one size
    # smaller everywhere moving forward" -- on every chart in the video.
    axes = Axes(
        x_range=[0, x_max, 1],
        y_range=[0, y_max, y_step],
        x_length=x_length,
        y_length=y_length,
        axis_config={"include_numbers": True, "font_size": TICK},
        tips=False,
    )
    x_lab = axes.get_x_axis_label(
        MathTex(x_name, font_size=BODY), edge=RIGHT,
        direction=DOWN + RIGHT, buff=0.25)
    return VGroup(axes, x_lab), axes


def staircase_cdf(axes, lam, n, x_max=4.0):
    """The scaled-geometric CDF 1 - (1 - lam/n)^floor(nx) as one VMobject."""
    p = lam / n
    pts = [axes.c2p(0, 0)]
    y = 0.0
    k_max = int(n * x_max)
    for k in range(1, k_max + 1):
        x = k / n
        pts.append(axes.c2p(x, y))          # run to the next tick
        y = 1.0 - (1.0 - p) ** k
        pts.append(axes.c2p(x, y))          # rise at the tick
    pts.append(axes.c2p(x_max, y))
    vm = VMobject(stroke_color=BAR, stroke_width=3)
    vm.set_points_as_corners(pts)
    return vm


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Exponential Distribution",
            ["The continuous model for waiting: density, rate,",
             "and a distribution that never remembers."],
            kicker="Chapter 8  ·  Continuous Random Variables",
        )
        tag = progress_tag(4, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Density, CDF, and the rate", font_size=BODY, color=INK),
            Text("2.  The geometric, squeezed", font_size=BODY, color=INK),
            Text("3.  The memoryless property", font_size=BODY, color=INK),
            Text("4.  Half-lives", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="The catalog of continuous models opened with "
                 "the uniform and the Gaussian. Today we add the third leg "
                 "of the triad: the exponential distribution, the model for "
                 "waiting."
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
            text="We meet its density and its CDF, and put them straight to "
                 "work on a server,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then watch the geometric distribution squeeze into it as "
                 "coin flips run on a finer and finer clock,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then meet the strange property the limit carries over: an "
                 "exponential wait never remembers how long you have already "
                 "waited,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and finish by letting that property crack a half-life "
                 "problem with almost no algebra."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExponentialDefinition(VoiceoverScene):
    """Beat: definition -- density, CDF, the rate family, the server."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Exponential Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # (2026-07-04 draft review, 1:15) chart shifted further left for
        # breathing room between the curve and the formula column.
        # (2026-07-05 draft review, 1:50) graph sat low with margins jammed
        # left and below: raised (buff 0.8 -> 1.15, still >= the 0.8 floor)
        # and eased slightly right (-3.3 -> -3.0) so the left and bottom
        # margins breathe; tick numbers now at TICK via waiting_axes.
        chart, axes = waiting_axes(x_max=4.0, y_max=2.2, y_step=0.5)
        chart.to_edge(DOWN, buff=1.15).set_x(-3.0)

        def dens(lam):
            return axes.plot(lambda x: lam * np.exp(-lam * x),
                             x_range=[0.0, 4.0], color=BAR, stroke_width=3)

        f_eq = MathTex(
            r"f_X(x)", "=", r"\lambda\, e^{-\lambda x}", r",\;\; x \geq 0",
            font_size=BODY, color=ACCENT,
        ).move_to(RIGHT * 3.5 + UP * 2.1)
        F_eq = MathTex(
            r"F_X(x)", "=", r"1 - e^{-\lambda x}",
            font_size=BODY, color=ACCENT,
        ).next_to(f_eq, DOWN, buff=0.5)

        with self.voiceover(
            text="Last chapter's bus made waiting uniform: a bus was coming, "
                 "on schedule, within thirty minutes. Real arrivals are not "
                 "so polite. Requests hit a server, parts fail, calls arrive "
                 "whenever they please. For waits like these, the workhorse "
                 "model is the exponential distribution."
        ):
            self.wait(0.3)

        curve = dens(1.0)
        with self.voiceover(
            text="An exponential random variable with parameter lambda has "
                 "density lambda times e to the minus lambda x, for x at "
                 "least zero. It starts at its highest value and decays, so "
                 "short waits are always the most likely."
        ):
            self.play(Write(f_eq), run_time=1.2)
            self.play(Create(chart[0]), Write(chart[1]), run_time=0.9)
            self.play(Create(curve), run_time=1.0)

        cdf_curve = axes.plot(lambda x: 1 - np.exp(-x),
                              x_range=[0.0, 4.0], color=TEAL, stroke_width=3)
        with self.voiceover(
            text="Integrate once and the CDF comes out in closed form: the "
                 "probability that X is at most x equals one minus e to the "
                 "minus lambda x. You may recognize this curve; it made a "
                 "cameo three videos ago as our first continuous CDF. Now it "
                 "has a name."
        ):
            self.play(f_eq.animate.set_color(INK), Write(F_eq), run_time=1.2)
            self.play(Create(cdf_curve), run_time=1.0)

        # (2026-07-04 draft review, 1:15) lambda tag at BODY size so it
        # reads at a glance next to the curve.
        rate_tag = MathTex(r"\lambda = \tfrac{1}{2}",
                           font_size=BODY, color=ACCENT)
        rate_tag.move_to(axes.c2p(3.1, 1.7))
        with self.voiceover(
            text="The parameter lambda is a rate. With lambda one half, the "
                 "density starts low and stretches out."
        ):
            self.play(F_eq.animate.set_color(INK), FadeOut(cdf_curve),
                      run_time=0.6)
            self.play(Transform(curve, dens(0.5)), FadeIn(rate_tag),
                      run_time=0.9)

        with self.voiceover(
            text="Raise lambda to one, then to two, and the curve starts "
                 "higher and dives faster. More events per unit time means "
                 "shorter waits."
        ):
            tag_1 = MathTex(r"\lambda = 1", font_size=BODY,
                            color=ACCENT).move_to(rate_tag)
            self.play(Transform(curve, dens(1.0)),
                      Transform(rate_tag, tag_1), run_time=0.9)
            tag_2 = MathTex(r"\lambda = 2", font_size=BODY,
                            color=ACCENT).move_to(rate_tag)
            self.play(Transform(curve, dens(2.0)),
                      Transform(rate_tag, tag_2), run_time=0.9)

        area = axes.get_area(dens(0.5), x_range=[0, 2],
                             color=BAR, opacity=0.45)
        with self.voiceover(
            text="Put it to work. Connection requests at an internet server "
                 "have exponential inter-arrival times with lambda equal to "
                 "one half. A request just arrived. What is the chance the "
                 "next one lands within two minutes?"
        ):
            tag_h = MathTex(r"\lambda = \tfrac{1}{2}", font_size=BODY,
                            color=MUTED).move_to(rate_tag)
            self.play(Transform(curve, dens(0.5)),
                      Transform(rate_tag, tag_h), run_time=0.9)
            self.play(FadeIn(area), run_time=0.9)

        ans = MathTex(
            pr("T < 2"), "=", r"1 - e^{-1}", r"\approx 0.632",
            font_size=BODY, color=ACCENT,
        ).next_to(F_eq, DOWN, buff=0.6)
        cap_width(ans, 5.0)
        with self.voiceover(
            text="The CDF at two gives it directly: one minus e to the "
                 "minus one, about zero point six three two. One integral, "
                 "one answer."
        ):
            self.play(Write(ans), run_time=1.1)
            self.play(Indicate(area, color=ACCENT, scale_factor=1.02),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GeometricLimit(VoiceoverScene):
    """Beat: limit -- the staircase CDF melting into the exponential."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Geometric, Squeezed")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        yn = MathTex(r"Y_n \sim \text{Geometric}\!\left(\lambda / n\right)",
                     font_size=SMALL, color=INK)
        pmf = MathTex(
            r"p_{Y_n}(k) = \left(1 - \tfrac{\lambda}{n}\right)^{k-1}"
            r"\tfrac{\lambda}{n},\;\; k = 1, 2, \ldots",
            font_size=SMALL, color=INK)
        xn = MathTex(r"X_n = \frac{Y_n}{n}", font_size=SMALL, color=ACCENT)
        cdfl = MathTex(
            pr(r"X_n \leq x"), "=",
            r"1 - \left(1 - \tfrac{\lambda}{n}\right)^{\lfloor nx \rfloor}",
            font_size=SMALL, color=INK)
        lim = MathTex(r"\longrightarrow\;\; 1 - e^{-\lambda x}",
                      font_size=BODY, color=ACCENT)
        for m in (yn, pmf, cdfl):
            cap_width(m, 5.2)
        col = VGroup(yn, pmf, xn, cdfl, lim)
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        col.move_to(RIGHT * 3.5 + UP * 0.7)
        fit_to_frame(col)

        # (2026-07-04 draft review, 3:30) chart raised off the bottom edge
        # so the left column balances the right-hand formula stack.
        # (2026-07-05 draft review, 3:10) chart was a bit wide: x_length
        # 6.2 -> 5.6 so the staircase no longer crowds the left border or
        # the formula column; tick numbers now at TICK via waiting_axes.
        chart, axes = waiting_axes(x_max=4.0, y_max=1.25, y_step=0.25,
                                   x_length=5.6, y_length=3.2)
        chart.to_edge(DOWN, buff=1.25).set_x(-3.1)

        with self.voiceover(
            text="Where does this curve come from? From a distribution you "
                 "already know."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="Fix a rate lambda, and flip a coin on every tick of a "
                 "clock that ticks n times per second, with success "
                 "probability lambda over n. The number of flips until the "
                 "first success is geometric; call it Y n."
        ):
            self.play(Write(yn), run_time=0.9)
            self.play(Write(pmf), run_time=1.1)

        with self.voiceover(
            text="But measure the wait in seconds, not in ticks: divide by "
                 "n. The scaled wait X n equals Y n over n."
        ):
            self.play(Write(xn), run_time=0.9)

        st = staircase_cdf(axes, 1.0, 4)
        n_tag = MathTex("n = 4", font_size=SMALL, color=INK)
        n_tag.move_to(axes.c2p(3.0, 0.4))
        with self.voiceover(
            text="Its CDF is a staircase. The probability that X n is at "
                 "most x is one minus, one minus lambda over n, raised to "
                 "the floor of n x: a step at every tick of the clock."
        ):
            self.play(xn.animate.set_color(INK), Write(cdfl), run_time=1.2)
            self.play(cdfl.animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(chart[0]), Write(chart[1]), run_time=0.9)
            self.play(Create(st), FadeIn(n_tag), run_time=1.0)

        smooth = axes.plot(lambda x: 1 - np.exp(-x),
                           x_range=[0.0, 4.0], color=BAR, stroke_width=3)
        mark_intended_overlap(
            st, smooth, reason="the staircase melts onto the smooth CDF")
        with self.voiceover(
            text="Now speed up the clock. With n equal to four, the steps "
                 "are chunky. At twelve, they tighten. At forty eight, the "
                 "staircase is nearly smooth. Let n grow without bound, and "
                 "the familiar limit for e takes over: the staircase melts "
                 "into one minus e to the minus lambda x, exactly the "
                 "exponential CDF."
        ):
            self.play(cdfl.animate.set_color(INK),
                      n_tag.animate.set_color(ACCENT), run_time=0.5)
            tag_12 = MathTex("n = 12", font_size=SMALL,
                             color=ACCENT).move_to(n_tag)
            self.play(Transform(st, staircase_cdf(axes, 1.0, 12)),
                      Transform(n_tag, tag_12), run_time=1.1)
            tag_48 = MathTex("n = 48", font_size=SMALL,
                             color=ACCENT).move_to(n_tag)
            self.play(Transform(st, staircase_cdf(axes, 1.0, 48)),
                      Transform(n_tag, tag_48), run_time=1.1)
            tag_inf = MathTex(r"n \to \infty", font_size=SMALL,
                              color=MUTED).move_to(n_tag)
            self.play(Transform(st, smooth),
                      Transform(n_tag, tag_inf), run_time=1.3)
            self.play(Write(lim), run_time=1.0)

        arrival = Text("discrete ticks become continuous time",
                       font_size=CAPTION, color=MUTED)
        arrival.next_to(col, DOWN, buff=0.5)
        with self.voiceover(
            text="This is the sense in which the exponential is the "
                 "continuous geometric: waiting in discrete ticks becomes "
                 "waiting in continuous time. The same engine that squeezed "
                 "the binomial into the Poisson runs here a second time."
        ):
            self.play(FadeIn(arrival, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(lim, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Memoryless(VoiceoverScene):
    """Beat: memoryless -- the statement, the two-line proof, the restart."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Memoryless Property")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        statement = MathTex(
            pr(r"X > t + u \mid X > t"), "=", pr("X > u"),
            font_size=BODY, color=ACCENT,
        ).move_to(UP * 2.2)
        fit_to_frame(statement)

        with self.voiceover(
            text="The geometric carried a famous quirk with it through the "
                 "limit. Suppose you have already waited t seconds. What is "
                 "the chance you wait at least u seconds more?"
        ):
            self.wait(0.3)

        with self.voiceover(
            text="For an exponential, the answer is the memoryless "
                 "property: the probability that X exceeds t plus u, given "
                 "that X exceeds t, equals the probability that X exceeds "
                 "u, the same as if you had just started."
        ):
            self.play(Write(statement), run_time=1.4)

        line1 = MathTex(
            pr(r"X > t + u \mid X > t"), "=",
            r"\frac{e^{-\lambda (t + u)}}{e^{-\lambda t}}",
            font_size=SMALL, color=INK)
        line2 = MathTex(
            "=", r"e^{-\lambda u}", "=", pr("X > u"),
            font_size=SMALL, color=INK)
        proof = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT,
                                             buff=0.3)
        # Align the second line's "=" under the first line's "=".
        line2.shift(RIGHT * (line1[1].get_left()[0]
                             - line2[0].get_left()[0]))
        proof.next_to(statement, DOWN, buff=0.45)
        fit_to_frame(proof)

        with self.voiceover(
            text="The proof takes two lines. The conditional probability is "
                 "a ratio of tails: e to the minus lambda times t plus u, "
                 "over e to the minus lambda t. The factor with t cancels, "
                 "leaving e to the minus lambda u."
        ):
            self.play(statement.animate.set_color(INK),
                      Write(line1), run_time=1.2)
            self.play(Write(line2), run_time=0.9)
            self.play(line2[1].animate.set_color(ACCENT), run_time=0.5)

        chart, axes = waiting_axes(x_max=4.0, y_max=1.2, y_step=0.5,
                                   x_length=5.6, y_length=2.6)
        chart.to_edge(DOWN, buff=0.8).set_x(-3.2)
        original = axes.plot(lambda x: np.exp(-x), x_range=[0.0, 4.0],
                             color=MUTED, stroke_width=3)
        cut = DashedLine(axes.c2p(1, 0), axes.c2p(1, 0.95),
                         color=INK, stroke_width=2.5, dash_length=0.1)
        t_lab = MathTex("t", font_size=CAPTION, color=INK)
        t_lab.move_to(axes.c2p(1, 1.06))
        tail = axes.plot(lambda x: np.exp(-x), x_range=[1.0, 4.0],
                         color=ACCENT, stroke_width=3.5)
        landed = axes.plot(lambda x: np.exp(-x), x_range=[0.0, 3.0],
                           color=ACCENT, stroke_width=3.5)
        mark_intended_overlap(
            original, tail, landed,
            reason="the rescaled tail lands exactly on the original density")
        # (2026-07-04 draft review, 4:43) shade the kept probability under
        # the tail before the move, then fade it once the tail has landed;
        # the shading + tail curve are one composed accent moment.
        tail_shade = axes.get_area(tail, x_range=[1.0, 4.0],
                                   color=ACCENT, opacity=0.3)
        mark_intended_overlap(
            tail_shade, original, tail, landed, cut, chart,
            reason="the shaded region composes with the tail it sits under")

        with self.voiceover(
            text="Watch what that means. Cut the density at t, keep the "
                 "tail,"
        ):
            self.play(line2[1].animate.set_color(INK),
                      Create(chart[0]), Write(chart[1]), run_time=0.9)
            self.play(Create(original), run_time=0.7)
            self.play(Create(cut), FadeIn(t_lab), run_time=0.6)
            self.play(Create(tail), run_time=0.7)
            self.play(FadeIn(tail_shade), run_time=0.7)

        with self.voiceover(
            text="and renormalize: the same move we used on the truncated "
                 "geometric."
        ):
            self.play(Transform(tail, landed), run_time=1.2)

        with self.voiceover(
            text="The rescaled tail lands exactly on the original curve. "
                 "The process restarts."
        ):
            self.play(FadeOut(tail_shade), run_time=0.9)

        note1 = Text("A used component is as good as new.",
                     font_size=SMALL, color=INK)
        note2 = Text("the only continuous distribution",
                     font_size=CAPTION, color=MUTED)
        note3 = Text("with this property", font_size=CAPTION, color=MUTED)
        notes = VGroup(note1, note2, note3).arrange(DOWN, buff=0.22)
        notes.move_to(RIGHT * 3.5 + DOWN * 2.0)
        fit_to_frame(notes)

        with self.voiceover(
            text="A used component is as good as new. That is a modeling "
                 "superpower, and a warning label, because real parts do "
                 "wear out. Among continuous distributions, the exponential "
                 "is the only one with this property."
        ):
            self.play(tail.animate.set_color(BAR),
                      FadeIn(note1, shift=RIGHT * 0.3), run_time=0.8)
            self.play(FadeIn(note2, shift=RIGHT * 0.3),
                      FadeIn(note3, shift=RIGHT * 0.3), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class HalfLifeExample(VoiceoverScene):
    """Beat: halflife -- survival factorized, the stream callback, outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Half-Lives")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="The memoryless property is not just a curiosity; it "
                 "computes."
        ):
            self.wait(0.3)

        chart, axes = waiting_axes(x_max=5.0, y_max=1.2, y_step=0.5,
                                   x_length=5.8, y_length=3.0, x_name="t")
        chart.to_edge(DOWN, buff=0.8).set_x(-3.1)
        y_lab = MathTex(r"\Pr\left(T > t\right)",
                        font_size=CAPTION, color=MUTED)
        y_lab.next_to(axes.y_axis.get_top(), UP, buff=0.18)
        lam = np.log(2.0) / 2.0
        survival = axes.plot(lambda x: np.exp(-lam * x), x_range=[0.0, 5.0],
                             color=BAR, stroke_width=3)
        d1 = Dot(axes.c2p(1, 2 ** -0.5), radius=0.07, color=INK)
        d2 = Dot(axes.c2p(2, 0.5), radius=0.07, color=INK)

        given = MathTex(
            pr("T > 2"), "=", r"\tfrac{1}{2}",
            font_size=BODY, color=ACCENT,
        ).move_to(RIGHT * 3.5 + UP * 2.15)
        question = MathTex(
            pr("T < 1"), "=", "?",
            font_size=SMALL, color=MUTED,
        ).next_to(given, DOWN, buff=0.35)

        with self.voiceover(
            text="Hard drives at a server farm have a half-life of two "
                 "years: the probability that a disk survives past year two "
                 "is exactly one half. What is the chance a disk needs "
                 "repair within its first year? We are not told lambda, and "
                 "we will not need it."
        ):
            self.play(Create(chart[0]), Write(chart[1]), FadeIn(y_lab),
                      run_time=0.9)
            self.play(Create(survival), run_time=0.9)
            self.play(FadeIn(d1, scale=1.6), FadeIn(d2, scale=1.6),
                      run_time=0.6)
            self.play(Write(given), run_time=0.9)
            self.play(FadeIn(question), run_time=0.6)

        l1 = MathTex(
            pr("T > 2"), "=", pr("T > 1"), pr(r"T > 2 \mid T > 1"),
            font_size=SMALL, color=INK)
        cap_width(l1, 5.2)
        l2 = MathTex(r"= \Pr\left(T > 1\right)^2",
                     font_size=SMALL, color=INK)
        split = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        l2.shift(RIGHT * (l1[1].get_left()[0] - l2.get_left()[0]))
        split.next_to(question, DOWN, buff=0.45)
        split.set_x(3.5)
        fit_to_frame(split)

        with self.voiceover(
            text="Split the two-year survival at year one. Surviving two "
                 "years means surviving the first year, then surviving one "
                 "more year given that first year. By memorylessness, that "
                 "second factor equals the plain one-year survival. So the "
                 "probability of surviving two years is the one-year "
                 "survival, squared."
        ):
            self.play(given.animate.set_color(INK), Write(l1), run_time=1.3)
            self.play(Indicate(d1, color=ACCENT, scale_factor=1.4),
                      Indicate(d2, color=ACCENT, scale_factor=1.4),
                      run_time=0.8)
            self.play(Write(l2), run_time=0.9)
            self.play(l2.animate.set_color(ACCENT), run_time=0.4)

        s1 = MathTex(r"\Pr\left(T > 1\right) = \tfrac{1}{\sqrt{2}}",
                     font_size=SMALL, color=INK)
        s2 = MathTex(
            r"\Pr\left(T < 1\right) = 1 - \tfrac{1}{\sqrt{2}}"
            r"\approx 0.293",
            font_size=BODY, color=ACCENT)
        cap_width(s2, 5.2)
        solve = VGroup(s1, s2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        solve.next_to(split, DOWN, buff=0.45)
        solve.set_x(3.5)
        fit_to_frame(solve)

        with self.voiceover(
            text="Take the square root: surviving one year has probability "
                 "one over root two. The chance of failure within the first "
                 "year is one minus one over root two, about zero point two "
                 "nine three. Lambda never appeared."
        ):
            self.play(l2.animate.set_color(INK), Write(s1), run_time=0.9)
            self.play(Write(s2), run_time=1.1)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])

        gaps = [0.55, 0.3, 1.45, 0.5, 1.0, 0.35, 1.9, 0.6, 1.2, 0.45, 0.9]
        xs = [-4.9]
        for g in gaps:
            xs.append(xs[-1] + g)
        stream_y = 0.4
        dots = VGroup(*[
            Dot(radius=0.11, color=INK).move_to([x, stream_y, 0])
            for x in xs
        ])
        braces = VGroup()
        for x0, x1 in zip(xs[:-1], xs[1:]):
            seg = Line([x0 + 0.08, stream_y - 0.22, 0],
                       [x1 - 0.08, stream_y - 0.22, 0])
            braces.add(Brace(seg, DOWN, buff=0.05, color=MUTED))
        gap_lab = MathTex(r"\text{gaps} \sim \text{Exponential}(\lambda)",
                          font_size=SMALL, color=ACCENT)
        gap_lab.next_to(braces, DOWN, buff=0.5)

        # (2026-07-04 draft review, 6:20) refer to the callback by concept
        # ("when we split the Poisson stream"), never by video number.
        with self.voiceover(
            text="One last debt to settle. Back when we split the Poisson "
                 "stream, its bits were drawn with ragged gaps between "
                 "the dots. That drawing was honest: when arrivals are "
                 "random in time, the gaps between them are exponential."
        ):
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots],
                                  lag_ratio=0.06), run_time=1.2)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15)
                                    for b in braces],
                                  lag_ratio=0.08), run_time=1.0)
            self.play(Write(gap_lab), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The exponential is the continuous geometric:",
             "memoryless, the model for waiting."],
            next_title="A Gallery of Densities",
        )

        # (2026-07-04 draft review, 6:45) narration reworded per review;
        # the outro card visual is unchanged.
        with self.voiceover(
            text="The key idea of this video: the exponential is "
                 "essentially the continuous version of the geometric "
                 "random variable, memoryless, the model for waiting. "
                 "Next video opens a whole gallery of densities, with the "
                 "exponential at its root."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
