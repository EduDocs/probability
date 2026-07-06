# derived_from: content/42-law-large-numbers-script.md
# derived_from_sha256: ab233e8a1659bfe5f92fb204d46cb2a6761843c3440f55531f4fa4808aa92de0
"""Chapter 12, Video 2 -- The Law of Large Numbers.

Source notes : 42-law-large-numbers.tex (\\section{The Law of Large
               Numbers} + \\subsection{Heavy-Tailed Distributions*};
               contour mechanics quoted headline-plus-result only).
Script        : content/42-law-large-numbers-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark
segment -- the same pattern as the earlier videos in the series.

Signature visuals: the shrinking variance bars (Var[X]/n on display), the
die-frequency trace hugging one sixth inside an epsilon band, and the
Cauchy running mean that refuses to settle (both traces HARDCODED --
no runtime randomness).

Draft render:
    uv run manim -pql scenes/law_large_numbers.py ChapterOverview
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
    die_face,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    speech_service,
    zone_center_y,
    even_stack,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice); AGEATION_TTS
    is the draft/final switch (render.py sets gtts for -ql)."""
    return speech_service()


# (2026-07-05 draft review, 5:00) Hardcoded running relative frequency of
# sixes -- the TRUE partial means of a fixed 120-roll die sequence, so the
# fluctuations damp honestly like 1/n (|x_n - x_{n-1}| <= 1/n at every
# step, verified offline on these rounded literals). The rolls come from a
# Lehmer LCG computed offline: x <- 48271 * x mod (2^31 - 1), seed 15,
# roll = 1 + x mod 6; 20 sixes in 120 rolls, so the trace ends exactly on
# 1/6. Deterministic by design -- no runtime randomness.
SIX_FREQS = [
    0.0, 0.5, 0.3333, 0.25, 0.2, 0.1667, 0.1429, 0.125, 0.1111, 0.1,
    0.0909, 0.0833, 0.0769, 0.0714, 0.0667, 0.0625, 0.0588, 0.0556, 0.1053,
    0.1, 0.0952, 0.0909, 0.1304, 0.125, 0.12, 0.1154, 0.1111, 0.1071,
    0.1034, 0.1333, 0.129, 0.125, 0.1515, 0.1765, 0.1714, 0.1667, 0.1622,
    0.1579, 0.1538, 0.15, 0.1463, 0.1429, 0.1395, 0.1364, 0.1556, 0.1522,
    0.1489, 0.1458, 0.1429, 0.14, 0.1373, 0.1346, 0.1321, 0.1296, 0.1273,
    0.1429, 0.1404, 0.1379, 0.1356, 0.1333, 0.1311, 0.129, 0.1429, 0.1406,
    0.1385, 0.1364, 0.1493, 0.1471, 0.1449, 0.1429, 0.1549, 0.1667, 0.1644,
    0.1757, 0.1733, 0.1842, 0.1818, 0.1795, 0.1772, 0.175, 0.1728, 0.1707,
    0.1687, 0.1786, 0.1765, 0.1744, 0.1724, 0.1705, 0.1685, 0.1667, 0.1648,
    0.163, 0.172, 0.1702, 0.1684, 0.1771, 0.1753, 0.1837, 0.1818, 0.18,
    0.1782, 0.1765, 0.1748, 0.1731, 0.1714, 0.1698, 0.1682, 0.1667, 0.1743,
    0.1727, 0.1712, 0.1696, 0.1681, 0.1667, 0.1652, 0.1638, 0.1624, 0.1695,
    0.1681, 0.1667,
]

# Hardcoded Cauchy running means: a plausible jittering partial-mean
# sequence -- violent excursions that never settle (no runtime randomness).
# (2026-07-05 draft review) Left as is on purpose: this trace is SUPPOSED
# to refuse to settle; only its position changed.
CAUCHY_MEANS = [1.8, 0.4, 6.1, 3.2, 2.7, -4.5, -2.1, -1.4, 5.3, 3.9, 3.1, 2.6]

# (2026-07-05 draft review, 5:00/5:55/6:30) The reviewer's vertical rule
# (the chapter 37-41 module-constant pattern): a beat's left figure sits
# centered on the halfway anchor below the docked title, and the right
# equation block ends the beat centered on the same anchor.
_DOCKED_TITLE = section_title("Counting Sixes").to_edge(UP)
CONTENT_MID_Y = zone_center_y(_DOCKED_TITLE)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Law of Large Numbers",
            ["Prove that empirical averages converge in probability",
             "to the mean, and see why finite variance is load-bearing."],
            kicker="Chapter 12  ·  Limit Theorems",
        )
        tag = progress_tag(2, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The statement", font_size=BODY, color=INK),
            Text("2.  A three-move proof", font_size=BODY, color=INK),
            Text("3.  Counting sixes", font_size=BODY, color=INK),
            Text("4.  The average that never settles",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="Averages settle. Flip enough coins, roll enough dice, and "
                 "the running average calms down toward one number, almost "
                 "as if chance were wearing off. Last video built the "
                 "vocabulary for that feeling: convergence in probability, "
                 "in mean square, and in distribution."
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
            text="In this video the feeling becomes a theorem, the law of "
                 "large numbers: the empirical average of independent, "
                 "identically distributed random variables converges in "
                 "probability to the mean."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        # (2026-07-05 draft review, 0:36 / 0:42) "already covered" +
        # "completes the proof" -- verbatim lockstep with the script.
        with self.voiceover(
            text="The proof takes three short moves we have already "
                 "covered, and the Chebyshev inequality completes the "
                 "proof."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Then a die makes it concrete: the relative frequency of a "
                 "six converges to the probability of a six."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="And finally a warning label: one famous heavy-tailed "
                 "density refuses to settle at all."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class LLNStatement(VoiceoverScene):
    """Beat: lln-statement -- the setting, the average, the weak law."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Law of Large Numbers")
        fit_to_frame(title)

        with self.voiceover(text="Here is the setting."):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        hyp = MathTex(
            r"X_1, X_2, \ldots \ \text{ i.i.d.}, \quad \text{mean }"
            + expectation("X") + r", \quad " + variance("X") + r" < \infty",
            font_size=BODY,
        ).move_to(UP * 2.1)
        fit_to_frame(hyp)

        with self.voiceover(
            text="Take a sequence of independent, identically distributed "
                 "random variables, X one, X two, and so on, each with mean "
                 "E of X and finite variance."
        ):
            self.play(Write(hyp), run_time=1.2)

        emp_sum = MathTex(r"S_n = \sum_{i=1}^{n} X_i", font_size=BODY)
        emp_sum.move_to(UP * 1.0)
        fit_to_frame(emp_sum)

        with self.voiceover(
            text="Add the first n of them and call the total S n, the "
                 "empirical sum."
        ):
            self.play(Write(emp_sum), run_time=1.0)

        avg = MathTex(
            r"\frac{S_n}{n} = \frac{X_1 + \cdots + X_n}{n}",
            font_size=BODY, color=ACCENT,
        ).move_to(DOWN * 0.25)
        fit_to_frame(avg)

        with self.voiceover(
            text="Divide by n, and you get the empirical average, S n over "
                 "n. This is the quantity every experimenter actually "
                 "computes: measure n times, add, divide. Signal averaging, "
                 "opinion polls, Monte Carlo estimates: they all live here."
        ):
            self.play(Write(avg), run_time=1.2)

        thm = MathTex(
            r"\lim_{n \to \infty}\,"
            + pr(r"\left| \frac{S_n}{n} - " + expectation("X")
                 + r" \right| \geq \epsilon")
            + r" = 0",
            font_size=BODY, color=ACCENT,
        ).move_to(DOWN * 1.75)
        fit_to_frame(thm)
        eps_note = MathTex(r"\text{for every } \epsilon > 0",
                           font_size=SMALL, color=MUTED)
        eps_note.next_to(thm, DOWN, buff=0.3)

        with self.voiceover(
            text="The law of large numbers asserts that the empirical "
                 "average converges in probability to the mean. For every "
                 "positive epsilon, the probability that S n over n misses "
                 "E of X by epsilon or more goes to zero as n grows."
        ):
            self.play(avg.animate.set_color(INK), run_time=0.4)
            self.play(Write(thm), run_time=1.4)
            self.play(FadeIn(eps_note, shift=UP * 0.2), run_time=0.6)

        # (2026-07-05 draft review, video-wide) "dies out" -> "vanishes"
        # for terms going to zero, narration + on-screen text in lockstep.
        reading = Text("the chance of a noticeable deviation vanishes",
                       font_size=CAPTION, color=MUTED)
        reading.to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="Read the statement slowly. The average is still a random "
                 "variable, but the probability of a noticeable deviation, "
                 "however tight you set the bar, vanishes as the sample "
                 "grows. There are many versions of this law; this is the "
                 "simplest one, and after last video its proof costs almost "
                 "nothing."
        ):
            self.play(FadeIn(reading, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(thm, color=ACCENT, scale_factor=1.03),
                      run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChebyshevCloses(VoiceoverScene):
    """Beat: chebyshev-closes -- unbiased mean, vanishing variance, and the
    Chebyshev finish (mean-and-variance + chebyshev-closes ledger)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Proof in Three Moves")
        fit_to_frame(title)

        with self.voiceover(
            text="The proof takes three moves, and we own every one of them."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        # (2026-07-05 draft review, 3:29) The right column ran out of room:
        # every equation now sits on ONE LINE, the whole column is
        # distributed with even_stack, and the left chart is drawn slightly
        # smaller so the column has the width it needs.
        col_x = 3.3

        mean_eq = MathTex(
            expectation(r"\frac{S_n}{n}"), "=",
            r"\frac{" + expectation("X_1") + r" + \cdots + "
            + expectation("X_n") + r"}{n}",
            "=", expectation("X"),
            font_size=SMALL,
        )
        fit_to_frame(mean_eq)
        var_eq = MathTex(
            variance(r"\frac{S_n}{n}"), "=",
            r"\frac{" + variance("X_1") + r" + \cdots + "
            + variance("X_n") + r"}{n^2}",
            "=", r"\frac{" + variance("X") + r"}{n}",
            font_size=SMALL,
        )
        fit_to_frame(var_eq)
        ms = MathTex(
            expectation(r"\left| \tfrac{S_n}{n} - " + expectation("X")
                        + r" \right|^2")
            + r" = " + variance(r"\tfrac{S_n}{n}")
            + r" \;\longrightarrow\; 0",
            font_size=SMALL,
        )
        fit_to_frame(ms)
        cheb_eq = MathTex(
            pr(r"\left| \tfrac{S_n}{n} - " + expectation("X")
               + r" \right| \geq \epsilon"),
            r"\leq",
            r"\frac{" + variance(r"\tfrac{S_n}{n}") + r"}{\epsilon^2}",
            "=", r"\frac{" + variance("X") + r"}{n\,\epsilon^2}",
            font_size=SMALL,
        )
        fit_to_frame(cheb_eq)
        qed = Text("convergence in probability", font_size=CAPTION,
                   color=MUTED)
        even_stack(mean_eq, var_eq, ms, cheb_eq, qed,
                   top=2.35, bottom=-2.9, x=col_x)

        with self.voiceover(
            text="First, the mean. Expectation is linear, so the "
                 "expectation of S n over n is the sum of the individual "
                 "means divided by n, and that is exactly E of X. The "
                 "average is unbiased: it points at the right target for "
                 "every sample size, and independence played no part yet."
        ):
            self.play(Write(mean_eq), run_time=1.9)
            self.play(mean_eq[4].animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="Second, the spread. The variables are independent, so "
                 "their variances add. The variance of S n over n is the "
                 "sum of the variances divided by n squared, which "
                 "collapses to Var of X over n."
        ):
            self.play(mean_eq[4].animate.set_color(INK), run_time=0.3)
            self.play(Write(var_eq), run_time=1.9)
            self.play(var_eq[4].animate.set_color(ACCENT), run_time=0.4)

        # The shrinking-variance chart (left column, riding high).
        unit, bar_w, gap = 2.2, 0.55, 0.95
        ns = [1, 2, 4, 8, 16]
        baseline = Line(LEFT * 2.4, RIGHT * 2.4, color=MUTED, stroke_width=2)
        bars, n_labels = VGroup(), VGroup()
        for i, n_val in enumerate(ns):
            cx = -gap * (len(ns) - 1) / 2 + gap * i
            h = unit / n_val
            bar = Rectangle(width=bar_w, height=h, fill_color=BAR,
                            fill_opacity=0.85, stroke_color=INK,
                            stroke_width=1)
            bar.move_to([cx, h / 2, 0])
            bars.add(bar)
            n_labels.add(MathTex(str(n_val), font_size=CAPTION, color=MUTED)
                         .next_to([cx, 0, 0], DOWN, buff=0.2))
        y_name = MathTex(r"\frac{" + variance("X") + r"}{n}",
                         font_size=BODY, color=INK)
        y_name.next_to(bars[0], UP, buff=0.3)
        x_name = MathTex("n", font_size=BODY, color=MUTED)
        x_name.next_to(n_labels, RIGHT, buff=0.45)
        chart = VGroup(baseline, bars, n_labels, y_name, x_name)
        mark_intended_overlap(
            chart, reason="variance bars stand on the chart baseline")
        fit_to_frame(chart)
        # (2026-07-05 draft review, 3:29) Slightly smaller chart; the
        # reclaimed width goes to the one-line equations on the right.
        chart.scale(0.85)
        chart.set_x(-4.0).to_edge(DOWN, buff=1.7)

        with self.voiceover(
            text="Watch that denominator work: quadruple the sample and the "
                 "variance of the average drops to a quarter. More data "
                 "buys proportionally more certainty. As n grows, the "
                 "variance vanishes."
        ):
            self.play(Create(baseline), FadeIn(n_labels), FadeIn(x_name),
                      run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.2),
                      Write(y_name), run_time=1.4)

        ms_cap = Text("convergence in mean square, for free",
                      font_size=CAPTION, color=MUTED)
        ms_cap.to_edge(DOWN, buff=0.8).match_x(chart)

        with self.voiceover(
            text="And since the expected squared deviation of the average "
                 "from E of X is exactly this variance, vanishing variance "
                 "already delivers convergence in mean square."
        ):
            self.play(var_eq[4].animate.set_color(INK), run_time=0.3)
            self.play(Write(ms), run_time=1.1)
            self.play(FadeIn(ms_cap, shift=UP * 0.2), run_time=0.6)

        # Move 3: Chebyshev closes -- the one-line finish.
        with self.voiceover(
            text="Third, the finish. The Chebyshev inequality from the "
                 "bounds video converts variance into a tail bound: the "
                 "probability that the average misses the mean by epsilon "
                 "or more is at most Var of X over n epsilon squared."
        ):
            self.play(Write(cheb_eq), run_time=2.1)
            self.play(cheb_eq[4].animate.set_color(ACCENT), run_time=0.4)

        with self.voiceover(
            text="The right side marches to zero, so the trapped left side "
                 "must follow. That is convergence in probability, and the "
                 "theorem is proved."
        ):
            self.play(Indicate(cheb_eq[4], color=ACCENT, scale_factor=1.05),
                      run_time=0.8)
            self.play(FadeIn(qed, shift=UP * 0.2), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class DieFrequency(VoiceoverScene):
    """Beat: die-frequency -- the fraction of sixes hugging one sixth."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Counting Sixes")
        fit_to_frame(title)

        with self.voiceover(text="Now make the theorem physical."):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        die = die_face(6, size=0.95, fill=BAR)
        die.move_to(LEFT * 5.6 + UP * 2.2)

        with self.voiceover(
            text="Roll a die over and over, and ask how often a six shows "
                 "up as the number of throws becomes very large."
        ):
            self.play(Create(die[0]), FadeIn(die[1]), run_time=1.0)

        col_x = 3.4
        ind1 = MathTex(r"X_n = \mathbf{1}_{\{D_n = 6\}}", font_size=BODY)
        ind1.move_to([col_x, 2.1, 0])
        fit_to_frame(ind1)
        ind2 = MathTex(r"X_n \sim \text{Bernoulli}\!\left(\tfrac{1}{6}"
                       r"\right)", font_size=BODY)
        ind2.next_to(ind1, DOWN, buff=0.4)
        ind2.set_x(col_x)
        bridge = MathTex(
            expectation("X_n") + r" = " + pr(r"D_n = 6")
            + r" = \tfrac{1}{6}",
            font_size=SMALL, color=MUTED,
        )
        bridge.next_to(ind2, DOWN, buff=0.4)
        bridge.set_x(col_x)
        fit_to_frame(bridge)

        frac = MathTex(
            r"\frac{S_n}{n} = \frac{\text{number of sixes}}{n}",
            font_size=BODY,
        )
        frac.next_to(bridge, DOWN, buff=0.5)
        frac.set_x(col_x)
        fit_to_frame(frac)
        inst = MathTex(
            r"\lim_{n \to \infty}\,"
            + pr(r"\left| \tfrac{S_n}{n} - \tfrac{1}{6} \right| \geq "
                 r"\epsilon")
            + r" = 0",
            font_size=SMALL, color=ACCENT,
        )
        inst.next_to(frac, DOWN, buff=0.55)
        inst.set_x(col_x)
        fit_to_frame(inst)
        # (2026-07-05 draft review, 5:00) The right equation block ends the
        # beat centered on the halfway anchor.
        rcol = VGroup(ind1, ind2, bridge, frac, inst)
        rcol.shift(UP * (CONTENT_MID_Y - rcol.get_center()[1]))

        with self.voiceover(
            text="Let D n be the number on the nth roll, and let X n be "
                 "the indicator that D n equals six: one when the roll is "
                 "a six, zero otherwise. Each X n is a Bernoulli random "
                 "variable with parameter one sixth, independent across "
                 "rolls and with finite variance, so the theorem applies. "
                 "Indicators bridge events and averages: the expectation "
                 "of an indicator is the probability of its event."
        ):
            self.play(Write(ind1), run_time=1.0)
            self.play(Write(ind2), run_time=1.0)
            self.play(FadeIn(bridge, shift=UP * 0.2), run_time=0.8)

        with self.voiceover(
            text="The empirical average S n over n is then the number of "
                 "sixes divided by the number of rolls: the relative "
                 "frequency of a six."
        ):
            self.play(Write(frac), run_time=1.1)

        # The settling trace: the true running relative frequency of sixes
        # in the fixed 120-roll LCG sequence (hardcoded literals above --
        # fluctuations damp like 1/n; 2026-07-05 draft review, 5:00).
        n_max = len(SIX_FREQS)
        freqs = SIX_FREQS

        axes = Axes(
            x_range=[0, n_max, 20],
            y_range=[0, 0.6, 0.6],
            x_length=5.4,
            y_length=3.0,
            tips=False,
            axis_config={"include_numbers": False},
        )
        p16 = 1.0 / 6.0
        eps = 0.08
        ref_line = DashedLine(axes.c2p(0, p16), axes.c2p(n_max, p16),
                              color=INK, stroke_width=2.5, dash_length=0.1)
        ref_lab = MathTex(r"\tfrac{1}{6}", font_size=SMALL, color=INK)
        ref_lab.next_to(axes.c2p(0, p16), LEFT, buff=0.2)
        band_bl = axes.c2p(0, p16 - eps)
        band_tr = axes.c2p(n_max, p16 + eps)
        band = Rectangle(
            width=band_tr[0] - band_bl[0], height=band_tr[1] - band_bl[1],
            stroke_width=0, fill_color=TEAL, fill_opacity=0.30,
        ).move_to((band_bl + band_tr) / 2)
        band_lab = MathTex(r"\pm\,\epsilon", font_size=SMALL, color=TEAL)
        band_lab.next_to(axes.c2p(n_max, p16), RIGHT, buff=0.2)
        trace = VMobject(stroke_color=BAR, stroke_width=3)
        trace.set_points_as_corners(
            [axes.c2p(n, f) for n, f in enumerate(freqs, start=1)])
        x_name = MathTex("n", font_size=BODY, color=MUTED)
        x_name.next_to(axes.c2p(n_max, 0), DOWN + RIGHT, buff=0.2)
        chart = VGroup(axes, ref_line, ref_lab, trace, x_name)
        mark_intended_overlap(
            chart, band, band_lab,
            reason="trace, one-sixth line, and epsilon band share the axes")
        fig = VGroup(chart, band, band_lab)
        fit_to_frame(fig)
        # (2026-07-05 draft review, 5:00) Left figure sits on the halfway
        # anchor below the docked title.
        fig.set_x(-3.2)
        fig.shift(UP * (CONTENT_MID_Y - fig.get_center()[1]))

        with self.voiceover(
            text="Watch it run. Early on the fraction lurches around, but "
                 "as rolls accumulate it hugs the level of one sixth, and "
                 "excursions outside an epsilon band become rare."
        ):
            self.play(Create(axes), FadeIn(x_name), run_time=0.7)
            self.play(Create(ref_line), Write(ref_lab), run_time=0.7)
            self.play(Create(trace), run_time=2.4)
            self.play(FadeIn(band), Write(band_lab), run_time=0.8)

        moral = Text("relative frequency converges to probability",
                     font_size=CAPTION, color=MUTED)
        moral.to_edge(DOWN, buff=0.75).match_x(fig)

        with self.voiceover(
            text="By the law of large numbers, the relative frequency of a "
                 "six converges in probability to one sixth, the "
                 "probability of a six. The long-run-frequency reading of "
                 "probability, the intuition this whole course has leaned "
                 "on, is now a theorem inside the axioms."
        ):
            self.play(Write(inst), run_time=1.3)
            self.play(FadeIn(moral, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CauchyRefusal(VoiceoverScene):
    """Beat: cauchy-refusal -- Cauchy sums stay Cauchy (headline plus
    result), so the average never settles (cauchy-stability +
    cauchy-refusal ledger; sequential section titles)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Sums of Cauchy Random Variables")
        fit_to_frame(title)

        with self.voiceover(
            text="One more scene, because the fine print earns its keep. "
                 "The theorem demanded finite variance, and a famous "
                 "member of our gallery of densities fails that condition: "
                 "the heavy-tailed Cauchy."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        # Left: the Cauchy density (gamma = 1).
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 0.4, 0.4],
            x_length=5.4,
            y_length=2.9,
            tips=False,
            axis_config={"include_numbers": False},
        )
        gamma = 1.0
        curve = axes.plot(
            lambda x: gamma / (PI * (gamma ** 2 + x ** 2)),
            x_range=[-6, 6], color=BAR, stroke_width=4)
        x_name = MathTex("x", font_size=BODY, color=MUTED)
        x_name.next_to(axes.c2p(6, 0), DOWN + RIGHT, buff=0.2)
        chart = VGroup(axes, curve, x_name)
        mark_intended_overlap(
            chart, reason="density curve and label share the axes")
        fit_to_frame(chart)
        # (2026-07-05 draft review, 5:55) Left figure sits on the halfway
        # anchor below the docked title.
        chart.set_x(-3.4)
        chart.shift(UP * (CONTENT_MID_Y - chart.get_center()[1]))

        col_x = 3.4
        fdef = MathTex(
            r"f_X(x) = \frac{\gamma}{\pi\left(\gamma^2 + x^2\right)}",
            font_size=BODY,
        ).move_to([col_x, 2.0, 0])
        fit_to_frame(fdef)
        no_moments = Text("no mean, no variance",
                          font_size=CAPTION, color=MUTED)
        no_moments.next_to(fdef, DOWN, buff=0.3)
        no_moments.set_x(col_x)
        conv = MathTex(
            r"f_S(x) = \int_{-\infty}^{\infty} f_{X_1}(u)\,"
            r"f_{X_2}(x - u)\, du",
            font_size=SMALL,
        )
        conv.next_to(no_moments, DOWN, buff=0.45)
        conv.set_x(col_x)
        fit_to_frame(conv)
        conv_tag = Text("contour integration: two simple poles",
                        font_size=CAPTION, color=MUTED)
        conv_tag.next_to(conv, DOWN, buff=0.25)
        conv_tag.set_x(col_x)
        stab = MathTex(
            r"f_S(x) = \frac{\gamma_1 + \gamma_2}"
            r"{\pi\left((\gamma_1 + \gamma_2)^2 + x^2\right)}",
            font_size=BODY, color=ACCENT,
        )
        stab.next_to(conv_tag, DOWN, buff=0.4)
        stab.set_x(col_x)
        fit_to_frame(stab)
        stab_cap = Text("Cauchy again: the parameters add",
                        font_size=CAPTION, color=MUTED)
        stab_cap.next_to(stab, DOWN, buff=0.25)
        stab_cap.set_x(col_x)
        # (2026-07-05 draft review, 5:55) The right equation block ends
        # this portion centered on the halfway anchor.
        rcol1 = VGroup(fdef, no_moments, conv, conv_tag, stab, stab_cap)
        rcol1.shift(UP * (CONTENT_MID_Y - rcol1.get_center()[1]))

        with self.voiceover(
            text="Its density is gamma over pi times gamma squared plus x "
                 "squared, and those tails decay so slowly that the Cauchy "
                 "has no mean and no variance."
        ):
            self.play(Create(axes), FadeIn(x_name), run_time=0.7)
            self.play(Create(curve), run_time=1.0)
            self.play(Write(fdef), run_time=1.0)
            self.play(FadeIn(no_moments, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="What do Cauchy sums do? The density of a sum of "
                 "independent continuous random variables is a "
                 "convolution, and contour integration, two simple poles "
                 "and their residues, evaluates this one in closed form."
        ):
            self.play(Write(conv), run_time=1.1)
            self.play(FadeIn(conv_tag, shift=UP * 0.2), run_time=0.6)

        with self.voiceover(
            text="Here is the headline: the sum of two independent Cauchy "
                 "random variables is Cauchy again, and the parameters "
                 "simply add."
        ):
            self.play(Write(stab), run_time=1.2)
            self.play(FadeIn(stab_cap, shift=UP * 0.2), run_time=0.6)

        title2 = section_title("The Average That Never Settles")
        fit_to_frame(title2)
        title2.to_edge(UP)
        induct = MathTex(r"S_n \sim \text{Cauchy}(n\gamma)",
                         font_size=BODY)
        induct.move_to([col_x, 1.6, 0])
        avg = MathTex(r"\frac{S_n}{n} \sim \text{Cauchy}(\gamma)",
                      font_size=BODY, color=ACCENT)
        avg.next_to(induct, DOWN, buff=0.5)
        avg.set_x(col_x)
        same_cap = Text("the same density, for every n",
                        font_size=CAPTION, color=MUTED)
        same_cap.next_to(avg, DOWN, buff=0.35)
        same_cap.set_x(col_x)
        # (2026-07-05 draft review, 6:30) The right equation block ends
        # this portion centered on the halfway anchor.
        rcol2 = VGroup(induct, avg, same_cap)
        rcol2.shift(UP * (CONTENT_MID_Y - rcol2.get_center()[1]))

        with self.voiceover(
            text="By induction, the empirical sum S n is Cauchy with "
                 "parameter n gamma. Now divide by n. The scaling rule for "
                 "derived densities compresses the picture right back, and "
                 "S n over n is Cauchy with parameter gamma. The very same "
                 "density, for every n."
        ):
            self.play(Transform(title, title2),
                      FadeOut(VGroup(fdef, no_moments, conv, conv_tag,
                                     stab, stab_cap)),
                      run_time=0.8)
            self.play(Write(induct), run_time=0.9)
            self.play(Write(avg), run_time=0.9)
            self.play(Indicate(curve, color=ACCENT, scale_factor=1.02),
                      FadeIn(same_cap, shift=UP * 0.2), run_time=0.8)

        # The wandering running mean (hardcoded partial means).
        w_axes = Axes(
            x_range=[0, 13, 1],
            y_range=[-5, 7, 6],
            x_length=5.4,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        )
        w_trace = VMobject(stroke_color=BAR, stroke_width=3)
        w_trace.set_points_as_corners(
            [w_axes.c2p(n, v) for n, v in enumerate(CAUCHY_MEANS, start=1)])
        w_dots = VGroup(*[
            Dot(w_axes.c2p(n, v), radius=0.05, color=BAR)
            for n, v in enumerate(CAUCHY_MEANS, start=1)
        ])
        w_xname = MathTex("n", font_size=BODY, color=MUTED)
        w_xname.next_to(w_axes.c2p(13, 0), DOWN + RIGHT, buff=0.2)
        w_yname = MathTex(r"\frac{S_n}{n}", font_size=BODY, color=MUTED)
        w_yname.next_to(w_axes.c2p(0, 7), UP + RIGHT, buff=0.2)
        w_chart = VGroup(w_axes, w_trace, w_dots, w_xname, w_yname)
        mark_intended_overlap(
            w_chart,
            reason="running-mean trace and its dots ride the axes")
        fit_to_frame(w_chart)
        # (2026-07-05 draft review, 6:30) Left figure sits on the halfway
        # anchor; the trace itself stays deliberately unsettled.
        w_chart.set_x(-3.4)
        w_chart.shift(UP * (CONTENT_MID_Y - w_chart.get_center()[1]))

        with self.voiceover(
            text="So the running average never settles. After a million "
                 "samples its distribution is exactly the distribution of "
                 "one observation, and the trace keeps taking violent "
                 "excursions. Averaging buys you nothing here."
        ):
            self.play(FadeOut(chart), run_time=0.5)
            self.play(Create(w_axes), FadeIn(w_xname), FadeIn(w_yname),
                      run_time=0.7)
            self.play(Create(w_trace), run_time=2.0)
            self.play(FadeIn(w_dots), run_time=0.5)

        moral = Text("no finite variance, no law of large numbers",
                     font_size=CAPTION, color=MUTED)
        moral.to_edge(DOWN, buff=0.75).match_x(w_chart)

        with self.voiceover(
            text="Nothing is broken. With no finite second moment, the "
                 "hypothesis of the law fails, so the conclusion is not "
                 "owed. Finite variance was load-bearing all along."
        ):
            self.play(avg.animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(moral, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # (2026-07-05 draft review, video-wide) "dies" -> "vanishes" for
        # the variance going to zero, card + narration in lockstep.
        outro = outro_bridge(
            ["Averages of independent samples converge in probability",
             "to the mean: their variance vanishes like one over n."],
            next_title="The Central Limit Theorem",
        )

        with self.voiceover(
            text="The key idea of this video: averages of independent "
                 "samples converge in probability to the mean, because "
                 "their variance vanishes like one over n. Next, the "
                 "companion masterpiece: the central limit theorem, where "
                 "the fluctuations around the mean take on a universal "
                 "shape."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
