# derived_from: content/18-expected-values-script.md
# derived_from_sha256: 0dd0614eb16e14c9407a8041c009990f611c7abc3d5a7b69e8426094c156242a
"""Chapter 6, Video 1 -- Expected Values.

Source notes : discrete_expectations.tex (chapter intro + Section 6.1) --
               the definition of E[X], the fair-die and coin-until-heads
               examples, and expectation as a summary of the PMF.
Script        : content/18-expected-values-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/expected_values.py ChapterOverview
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
    expectation,
    section_title,
    make_pmf_chart,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    die_face,
    coin,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card, recap of g(X), and the outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Expected Values",
            ["Collapse a whole PMF into one meaningful number:",
             "the expected value."],
            kicker="Chapter 6  ·  Meeting Expectations",
        )
        tag = progress_tag(1, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The definition", font_size=BODY, color=INK),
            Text("2.  Two worked examples", font_size=BODY, color=INK),
            Text("3.  What E[X] really is", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last time we saw that applying a function to a random "
                 "variable gives another random variable, with its own PMF. "
                 "So by now, a PMF is something we can build and transform. "
                 "But a PMF is a lot of information — a whole table of values "
                 "and probabilities. Very often, all we really want is one "
                 "number: an average. This chapter is about the operator that "
                 "produces such numbers — expectation."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        # Breathing room between the chapter framing and the outline --
        # sequential voiceover blocks otherwise join gaplessly (2026-07-03
        # hi-res review, 0:24).
        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(outline)

        # Each outline line lands with its clause (per-phrase sub-blocks;
        # 2026-07-03 draft review).
        with self.voiceover(
            text="In this video we define the expected value of a discrete "
                 "random variable,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="compute it for a die roll and for a coin tossed until "
                 "heads,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and see what kind of object it really is."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExpectedValueDefinition(VoiceoverScene):
    """Beat: definition -- the weighted sum, convergence, a PMF property."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Expected Value")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # A generic, mildly skewed PMF -- not one of the named families, so
        # the definition reads as general.
        values = [0.0, 0.10, 0.20, 0.30, 0.25, 0.15]
        chart, bars = make_pmf_chart(values, x_label="x", y_label=r"p_X(x)")
        chart.scale(0.75).to_edge(DOWN, buff=0.55)

        formula = MathTex(
            expectation("X"), "=",
            r"\sum_{x \in X(\Omega)} x \, p_X(x)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(formula)

        caveat = Text("defined when the sum converges absolutely",
                      font_size=CAPTION, color=MUTED)
        caveat.next_to(formula, DOWN, buff=0.25)

        with self.voiceover(text="Here is a PMF."):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.9)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=1.0)

        with self.voiceover(
            text="It answers every question about its random variable: the "
                 "probability of each value, of any set of values. Complete — "
                 "but detailed. Suppose we want a single number that "
                 "summarizes where this distribution sits."
        ):
            self.play(LaggedStart(*[Indicate(b, scale_factor=1.06)
                                    for b in bars], lag_ratio=0.12),
                      run_time=2.0)

        with self.voiceover(
            text="The natural candidate is a weighted average: take each "
                 "value x, weight it by its mass p sub X of x, and add "
                 "everything up. That sum is the expected value of X, written "
                 "E of X, and it is also called the mean. Each value "
                 "contributes in proportion to how likely it is."
        ) as tracker:
            self.play(Write(formula), run_time=1.4)
            self.play(formula[0].animate.set_color(ACCENT), run_time=0.5)
            self.play(LaggedStart(*[Indicate(b, color=ACCENT,
                                             scale_factor=1.08)
                                    for b in bars], lag_ratio=0.15),
                      run_time=2.2)

        with self.voiceover(
            text="One caveat: for ranges with infinitely many values, the sum "
                 "must converge absolutely; otherwise we simply say the "
                 "expected value does not exist."
        ):
            self.play(FadeIn(caveat), run_time=0.6)

        with self.voiceover(
            text="And notice what kind of object this is. The expected value "
                 "is not a function of the outcomes; it is computed from the "
                 "PMF alone. Two random variables with the same PMF have "
                 "exactly the same mean, no matter how different their "
                 "experiments are."
        ):
            self.play(formula[0].animate.set_color(INK),
                      formula[2].animate.set_color(ACCENT), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class FairDieExample(VoiceoverScene):
    """Beat: die -- flat PMF, the sum, and a mean the die cannot show."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Fair Die")
        glyph = die_face(5, size=0.7).next_to(title, LEFT, buff=0.5)
        header = VGroup(title, glyph)
        fit_to_frame(header)
        self.play(Write(title), FadeIn(glyph))
        self.play(header.animate.to_edge(UP))

        values = [0.0] + [1 / 6] * 6
        chart, bars = make_pmf_chart(values, x_label="x", y_label=r"p_X(x)",
                                     y_max=0.3)
        chart.scale(0.72).to_edge(DOWN, buff=0.55)

        line1 = MathTex(
            expectation("X"), "=",
            r"\tfrac{1}{6}\left(1 + 2 + 3 + 4 + 5 + 6\right)",
            font_size=BODY,
        )
        line2 = MathTex(r"= \tfrac{21}{6} = 3.5", font_size=BODY,
                        color=ACCENT)
        calc = VGroup(line1, line2).arrange(DOWN, buff=0.25)
        calc.next_to(header, DOWN, buff=0.45)
        fit_to_frame(calc)

        with self.voiceover(
            text="Let's compute one. Roll a fair die once, and let X be the "
                 "number of dots on the top face."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.9)

        with self.voiceover(
            text="The PMF is flat: each of the six values carries mass one "
                 "sixth."
        ):
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=1.2)

        with self.voiceover(
            text="So the expected value is one times one sixth, plus two "
                 "times one sixth, and so on up to six — that is twenty-one "
                 "over six, which is three and a half."
        ):
            self.play(Write(line1), run_time=1.4)
            self.play(Write(line2), run_time=0.9)

        marker = Dot(color=ACCENT, radius=0.09)
        axes = chart[0]
        marker.move_to(axes.c2p(3.5, 0))
        marker_label = MathTex("3.5", font_size=SMALL, color=ACCENT)
        marker_label.next_to(marker, DOWN, buff=0.35)
        note = Text("the mean need not be a value the die can show",
                    font_size=CAPTION, color=MUTED)
        note.next_to(calc, DOWN, buff=0.3)

        with self.voiceover(
            text="Three and a half. Notice the die can never show that "
                 "value. The mean is a balance point of the distribution, "
                 "not necessarily a value the random variable can take."
        ):
            self.play(line2.animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(marker, scale=2.0), FadeIn(marker_label),
                      run_time=0.8)
            self.play(FadeIn(note), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class WaitingForHeads(VoiceoverScene):
    """Beat: heads -- the geometric halving PMF and its convergent mean."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Waiting for Heads")
        glyph = coin("H", ACCENT, radius=0.36).next_to(title, LEFT, buff=0.5)
        header = VGroup(title, glyph)
        fit_to_frame(header)
        self.play(Write(title), FadeIn(glyph))
        self.play(header.animate.to_edge(UP))

        kmax = 8
        values = [0.0] + [2.0 ** (-k) for k in range(1, kmax + 1)]
        chart, bars = make_pmf_chart(values, x_label="k", y_label=r"p_X(k)")
        chart.scale(0.72).to_edge(DOWN, buff=0.55)

        series = MathTex(
            expectation("X"), "=",
            r"\sum_{k=1}^{\infty} \frac{k}{2^k}", "=", "2",
            font_size=BODY,
        ).next_to(header, DOWN, buff=0.45)
        fit_to_frame(series)

        with self.voiceover(
            text="Now an infinite one. Toss a fair coin until the first head "
                 "appears, and let X count the tosses."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.9)

        with self.voiceover(
            text="We met this random variable before: its range is one, two, "
                 "three, and on forever, and its PMF halves at every step — "
                 "the probability of needing k tosses is one over two to "
                 "the k."
        ):
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.12), run_time=1.6)

        with self.voiceover(
            text="The expected value is the sum of k over two to the k, for "
                 "k from one to infinity. Infinitely many terms — yet the "
                 "series converges, and it converges to exactly two."
        ):
            self.play(Write(series), run_time=1.6)
            self.play(series[4].animate.set_color(ACCENT), run_time=0.4)

        # Partial sums of k/2^k: 0.5, 1.0, 1.375, 1.625, 1.78125, ...
        # No "2" label at the settle point: the axis tick already says 2 and
        # the pair collided (2026-07-03 hi-res review, 2:39). The dot alone
        # marks the limit; a final Indicate stands in for the label.
        partials = [0.5, 1.0, 1.375, 1.625, 1.78125, 1.875]
        axes = chart[0]
        marker = Dot(color=ACCENT, radius=0.09).move_to(axes.c2p(partials[0], 0))

        with self.voiceover(
            text="Watch the partial sums: one half, then one and a half... "
                 "creeping up and settling at two. On average, it takes two "
                 "tosses to see the first head. An infinite amount of detail, "
                 "condensed into one clean number."
        ):
            self.play(FadeIn(marker, scale=2.0), run_time=0.4)
            for p in partials[1:]:
                self.play(marker.animate.move_to(axes.c2p(p, 0)),
                          run_time=0.45)
            self.play(marker.animate.move_to(axes.c2p(2, 0)), run_time=0.6)
            self.play(Indicate(marker, scale_factor=1.6), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class PMFToScalar(VoiceoverScene):
    """Beat: summary -- the funnel picture, then the shared outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("From a PMF to a Single Number")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        values = [0.0, 0.10, 0.20, 0.30, 0.25, 0.15]
        chart, _bars = make_pmf_chart(values, x_label="x", y_label=r"p_X(x)")
        chart.scale(0.5)
        chart.next_to(title, DOWN, buff=0.5)

        funnel = Polygon(
            [-2.2, 0.0, 0], [2.2, 0.0, 0], [0.55, -1.5, 0], [-0.55, -1.5, 0],
            color=MUTED, stroke_width=3,
        )
        funnel.next_to(chart, DOWN, buff=0.25)
        scalar = MathTex(expectation("X"), font_size=SECTION, color=ACCENT)
        scalar.next_to(funnel, DOWN, buff=0.4)
        group = VGroup(chart, funnel, scalar)
        fit_to_frame(group)

        # The chart deliberately slides into the funnel's mouth.
        mark_intended_overlap(chart, funnel,
                              reason="the PMF pours into the funnel")

        # The pour is held back to the "Out comes a single scalar" clause
        # (~15 s into the beat) per the 2026-07-03 draft review.
        with self.voiceover(
            text="Step back and look at what expectation does."
        ):
            self.play(FadeIn(chart), run_time=0.8)

        with self.voiceover(
            text="In goes a PMF — a complete, detailed description of a "
                 "random variable."
        ):
            self.play(Create(funnel), run_time=0.8)

        with self.voiceover(
            text="Out comes a single scalar: its mean."
        ):
            self.play(chart.animate.scale(0.25).move_to(funnel.get_center()),
                      run_time=1.4)
            self.play(FadeOut(chart), FadeIn(scalar, shift=DOWN * 0.3),
                      run_time=1.0)

        with self.voiceover(
            text="That is the trade: we give up detail and gain a concise, "
                 "meaningful summary of overall behavior. And this trade is "
                 "the template for everything in this chapter."
        ):
            self.play(Indicate(scalar, scale_factor=1.08), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The expected value is the probability-weighted sum",
             "of the values — one number for a whole PMF."],
            next_title="Functions and Expectations",
        )

        with self.voiceover(
            text="The key idea to carry forward: the expected value is the "
                 "probability-weighted sum of the values — one number that "
                 "summarizes the whole PMF. Coming up next: we push functions "
                 "through the expectation and meet the two summaries that "
                 "dominate practice, the mean and the variance."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
