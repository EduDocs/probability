# derived_from: content/38-conditioning-densities-script.md
# derived_from_sha256: 3308d37f861c78cbbf6ccbcfdb37b8cef220e70d8243612d77865cb9d9a571a6
"""Chapter 11, Video 2 -- Conditioning with Densities.

Source notes : random_vectors.tex (Section 11.2, preamble + all three
               subsections) -- conditional CDF/PDF given an event, interval
               renormalization, conditioning on values, conditional
               expectation with the MMSE channel, and the Jacobian formula.
Script        : content/38-conditioning-densities-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/conditioning_densities.py ChapterOverview
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
    pr,
    expectation,
    section_title,
    axis_label_x,
    axis_label_y,
    intro_card,
    outro_bridge,
    progress_tag,
    even_stack,
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


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + four outline lines, clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Conditioning with Densities",
            ["Slice the joint density and renormalize - condition on",
             "events, on exact values, and estimate through noise."],
            kicker="Chapter 11  ·  Multiple Continuous Random Variables",
        )
        tag = progress_tag(2, 4).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Conditioning on an event", font_size=BODY, color=INK),
            Text("2.  Conditioning on a value", font_size=BODY, color=INK),
            Text("3.  Conditional expectation", font_size=BODY, color=INK),
            Text("4.  Derived distributions", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="Last video built the joint density: a surface over the "
                 "plane whose volume above a region is probability, with "
                 "marginals found by integrating one variable out. This "
                 "video slices that surface, because that is how observation "
                 "works in the continuous world: you learn something, and "
                 "the whole model updates."
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
            text="We condition a density on an event, and "
                 "truncate-and-rescale returns in smooth form,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then condition on an exact value — an event of "
                 "probability zero — and make honest sense of it,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="average the slices to get conditional expectation, and "
                 "let it estimate a signal through noise,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and close by transforming pairs with the Jacobian formula."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionOnEvent(VoiceoverScene):
    """Beat: on-event -- the ratio, its derivative, truncate-and-rescale."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning on an Event")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        ratio = MathTex(
            r"F_{X \mid A}(x)", "=",
            r"\frac{\Pr\left(\{X \le x\} \cap A\right)}{\Pr\left(A\right)}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(ratio)
        deriv = MathTex(
            r"f_{X \mid A}(x)", "=",
            r"\frac{dF_{X \mid A}}{dx}(x)",
            font_size=BODY,
        ).next_to(ratio, DOWN, buff=0.45)
        fit_to_frame(deriv)

        with self.voiceover(
            text="Chapter four's ratio has served every kind of "
                 "conditioning so far, and it crosses into the continuous "
                 "world untouched."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="Given an event A with positive probability, the "
                 "conditional CDF of X is the probability that X is at most "
                 "x and A happens, over the probability of A."
        ):
            self.play(Write(ratio), run_time=1.4)
            self.play(ratio[0].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text="Differentiate, and the slope is a genuine density: the "
                 "conditional PDF of X given A. Nothing new is postulated "
                 "here — the ratio we trust meets the CDF we trust."
        ):
            self.play(ratio[0].animate.set_color(INK),
                      Write(deriv), run_time=1.0)
            self.play(deriv[0].animate.set_color(ACCENT), run_time=0.5)

        # The exponential lifetime, truncated to [0, 2] and rescaled --
        # video 22's geometric-bars move, run on a smooth curve.
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.3, 0.5],
            x_length=6.8,
            y_length=3.4,
            axis_config={"include_numbers": True, "font_size": 30},
            tips=False,
        )
        chart = VGroup(
            axes,
            axis_label_x(axes, MathTex("x", font_size=CAPTION, color=MUTED)),
            axis_label_y(axes, MathTex(r"f_X(x)", font_size=CAPTION,
                                       color=MUTED)),
        )
        fit_to_frame(chart)
        chart.to_edge(DOWN, buff=0.8).shift(LEFT * 2.6)

        piece1 = axes.plot(lambda x: np.exp(-x), x_range=[0, 2], color=INK)
        piece2 = axes.plot(lambda x: np.exp(-x), x_range=[2, 5], color=INK)
        area1 = axes.get_area(piece1, x_range=[0, 2], color=BAR, opacity=0.35)
        iseg = Line(axes.c2p(0, 0), axes.c2p(2, 0),
                    color=ACCENT, stroke_width=6)
        scale = 1.0 / (1.0 - np.exp(-2.0))
        target_curve = axes.plot(lambda x: scale * np.exp(-x),
                                 x_range=[0, 2], color=INK)
        target_area = axes.get_area(target_curve, x_range=[0, 2],
                                    color=BAR, opacity=0.35)
        mark_intended_overlap(
            chart, piece1, piece2, area1, iseg, target_curve, target_area,
            reason="density curve, shading, and interval marker sit on the axes")

        caption = Text("lifetime, given failure within two years",
                       font_size=CAPTION, color=MUTED)
        caption.move_to(RIGHT * 3.5 + UP * 1.0)

        # (2026-07-05 draft review) split so the curve and interval marker
        # land on their own sentence instead of front-loading the block.
        with self.voiceover(
            text="The case to internalize is conditioning on an interval."
        ):
            self.play(deriv[0].animate.set_color(INK),
                      FadeOut(ratio), FadeOut(deriv), run_time=0.5)
            self.play(Create(axes), FadeIn(chart[1]), FadeIn(chart[2]),
                      run_time=0.8)

        with self.voiceover(
            text="Suppose a component's lifetime is exponential, and we "
                 "learn it failed within the first two years."
        ):
            self.play(Create(piece1), Create(piece2), run_time=0.9)
            self.play(Create(iseg), FadeIn(caption), run_time=0.7)

        with self.voiceover(
            text="Outside the interval the density dies: those lifetimes "
                 "are ruled out."
        ):
            self.play(piece2.animate.set_stroke(opacity=0.2),
                      FadeIn(area1), run_time=0.9)

        formula = MathTex(
            r"f_{X \mid A}(x)", "=",
            r"\frac{f_X(x)}{" + pr(r"X \in I") + "}",
            font_size=BODY,
        ).move_to(RIGHT * 3.5 + DOWN * 0.1)
        fit_to_frame(formula)
        zero_cap = MathTex(r"\text{and } 0 \text{ outside } I",
                           font_size=CAPTION, color=MUTED)
        zero_cap.next_to(formula, DOWN, buff=0.3)

        # (2026-07-05 draft review) per-phrase sub-blocks: the rescale
        # transform lands exactly on "the curve rises".
        with self.voiceover(
            text="Inside, the shape is untouched — every value divides by "
                 "the same number, the probability of landing in the "
                 "interval —"
        ):
            self.play(Write(formula), run_time=1.0)
            self.play(formula[2].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text="and the curve rises just enough to enclose area one."
        ):
            self.play(Transform(piece1, target_curve),
                      Transform(area1, target_area), run_time=1.2)

        with self.voiceover(
            text="Truncate and rescale: the move we ran on the geometric "
                 "bars in chapter seven, now on a smooth curve."
        ):
            self.play(FadeIn(zero_cap), run_time=0.5)

        self.play(FadeOut(VGroup(chart, piece1, piece2, area1, iseg,
                                 caption, formula, zero_cap)),
                  run_time=0.5)

        # One breath: a region event, integrated over a triangle.
        tri = Polygon([0, 0, 0], [2.4, 0, 0], [2.4, 2.4, 0],
                      fill_color=TEAL, fill_opacity=0.25,
                      stroke_color=INK, stroke_width=2)
        tri.move_to(LEFT * 3.4 + DOWN * 1.1)
        tri_label = MathTex(r"y \le x", font_size=CAPTION, color=INK)
        tri_label.move_to(tri.get_center() + RIGHT * 0.5 + DOWN * 0.35)
        mark_intended_overlap(tri, tri_label,
                              reason="region label sits inside the triangle")
        event_lab = MathTex(r"A = \{Y \le X\}", font_size=SMALL, color=INK)
        event_lab.next_to(tri, UP, buff=0.4)
        joint = MathTex(r"f_{X,Y}(x, y) = \lambda^2 e^{-\lambda(x + y)}",
                        font_size=SMALL, color=INK)
        joint.move_to(RIGHT * 3.0 + UP * 0.2)
        result = MathTex(
            r"f_{X \mid A}(x)", "=",
            r"2\lambda e^{-\lambda x}\left(1 - e^{-\lambda x}\right)",
            font_size=BODY,
        ).move_to(RIGHT * 3.0 + DOWN * 1.1)
        fit_to_frame(result)

        # (2026-07-05 draft review) per-phrase sub-blocks: the triangle on
        # its opener, the math on the arrivals sentence, accent on the close.
        with self.voiceover(
            text="And the event need not involve X alone."
        ):
            self.play(Create(tri), FadeIn(tri_label), Write(event_lab),
                      run_time=0.9)

        with self.voiceover(
            text="Condition two exponential arrivals on Y at most X, and "
                 "integrating the joint density over a triangle hands back "
                 "a clean conditional density for X."
        ):
            self.play(Write(joint), run_time=0.8)
            self.play(Write(result), run_time=0.9)

        with self.voiceover(
            text="Any region of the plane can play the role of A."
        ):
            self.play(result[2].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionOnValues(VoiceoverScene):
    """Beat: on-values -- the shrinking box, the definition, the disk chord."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning on a Value")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        prob_card = MathTex(pr("Y = y") + "= 0", font_size=BODY, color=INK)
        prob_card.move_to(DOWN * 0.3)
        prob_cap = Text("cannot divide by this", font_size=CAPTION,
                        color=MUTED)
        prob_cap.next_to(prob_card, DOWN, buff=0.3)

        # (2026-07-05 draft review) the zero card lands on "probability
        # zero", not at the beat's start.
        with self.voiceover(
            text="Now the harder question, and the one observation "
                 "actually asks. A receiver reads Y equals exactly one "
                 "point three —"
        ):
            self.wait(0.3)

        with self.voiceover(
            text="but for a continuous Y, that event has probability zero, "
                 "and dividing by zero is not conditioning."
        ):
            self.play(Write(prob_card), run_time=0.9)
            self.play(FadeIn(prob_cap), run_time=0.6)

        # The shrinking box on the joint support; the delta-y cancels.
        region = RoundedRectangle(
            corner_radius=0.25, width=4.4, height=2.6,
            fill_color=BAR, fill_opacity=0.15,
            stroke_color=MUTED, stroke_width=2,
        ).move_to(LEFT * 3.2 + UP * 0.5)
        flab = MathTex(r"f_{X,Y} > 0", font_size=CAPTION, color=MUTED)
        flab.move_to(region.get_corner(UL) + RIGHT * 0.75 + DOWN * 0.35)
        box = Square(side_length=0.5, color=ACCENT)
        box.set_fill(ACCENT, opacity=0.35)
        box.move_to(region.get_center() + RIGHT * 0.4 + DOWN * 0.2)
        strip = Rectangle(
            width=region.width * 0.94, height=0.14,
            stroke_color=ACCENT, stroke_width=2,
            fill_color=ACCENT, fill_opacity=0.4,
        ).move_to(region.get_center() + DOWN * 0.2)
        mark_intended_overlap(
            region, flab, box, strip,
            reason="box, slice strip, and label live inside the support")

        line1 = MathTex(
            pr(r"x \le X \le x + \Delta_x \mid y \le Y \le y + \Delta_y"),
            font_size=SMALL, color=INK,
        )
        line2 = MathTex(
            r"\approx \frac{f_{X,Y}(x,y)\,\Delta_x\,\Delta_y}"
            r"{f_Y(y)\,\Delta_y}",
            font_size=SMALL, color=INK,
        )
        ratio = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT,
                                             buff=0.3)
        ratio.move_to(RIGHT * 3.3 + UP * 1.2)
        fit_to_frame(ratio)
        line2_target = MathTex(
            r"\approx \frac{f_{X,Y}(x,y)}{f_Y(y)}\;\Delta_x",
            font_size=SMALL, color=INK,
        ).move_to(line2, aligned_edge=LEFT)

        # (2026-07-05 draft review) per-phrase sub-blocks: the cancel move
        # lands exactly on "the delta y cancels".
        with self.voiceover(text="Escape by a limit."):
            self.play(FadeOut(prob_card), FadeOut(prob_cap), run_time=0.4)
            self.play(Create(region), FadeIn(flab), run_time=0.7)

        with self.voiceover(
            text="Ask instead that X land within a small window delta x, "
                 "given that Y landed within a small window delta y."
        ):
            self.play(FadeIn(box, scale=1.4), run_time=0.6)
            self.play(Write(line1), run_time=1.0)

        with self.voiceover(
            text="That ratio is honest — both windows have positive "
                 "probability."
        ):
            self.play(Write(line2), run_time=0.9)

        with self.voiceover(
            text="The joint density times both widths, over the marginal "
                 "times delta y: the delta y cancels."
        ):
            self.play(box.animate.stretch(0.25, 1), run_time=0.8)
            self.play(Transform(line2, line2_target), run_time=0.9)

        defn = MathTex(
            r"f_{X \mid Y}(x \mid y)", "=",
            r"\frac{f_{X,Y}(x, y)}{f_Y(y)}",
            font_size=BODY,
        ).move_to(RIGHT * 3.3 + UP * 1.5)
        fit_to_frame(defn)
        defn_cap = MathTex(r"\text{defined when } f_Y(y) > 0",
                           font_size=CAPTION, color=MUTED)
        defn_cap.next_to(defn, DOWN, buff=0.25)
        integral = MathTex(
            pr(r"X \in S \mid Y = y") +
            r"= \int_S f_{X \mid Y}(x \mid y)\, dx",
            font_size=SMALL, color=INK,
        )
        integral.next_to(defn_cap, DOWN, buff=0.35)
        fit_to_frame(integral)

        # (2026-07-05 draft review) per-phrase sub-blocks: the integral
        # lands on its own "Integrate it over a set" sentence.
        with self.voiceover(text="What survives is the definition."):
            self.play(FadeOut(line1), FadeOut(line2), run_time=0.4)

        with self.voiceover(
            text="The conditional density of X given Y equals y is the "
                 "joint density along the slice, divided by the marginal "
                 "of Y at y — defined wherever that marginal is positive."
        ):
            self.play(Write(defn), run_time=1.1)
            self.play(defn[0].animate.set_color(ACCENT),
                      FadeIn(defn_cap), run_time=0.6)

        with self.voiceover(
            text="Integrate it over a set, and you have the conditional "
                 "probability that X lands there."
        ):
            self.play(Write(integral), run_time=1.0)

        # The slice strip and its lifted, inflated profile.
        base_c = LEFT * 3.2 + DOWN * 2.5
        baseline = Line(base_c + LEFT * 1.8, base_c + RIGHT * 1.8,
                        color=MUTED, stroke_width=2)
        bump = FunctionGraph(
            lambda x: 0.5 * np.exp(-((x / 0.8) ** 2)),
            x_range=[-1.7, 1.7], color=INK,
        ).shift(base_c)
        area_lab = MathTex(r"\text{area} = 1", font_size=CAPTION,
                           color=MUTED)
        area_lab.next_to(baseline, RIGHT, buff=0.35)
        mark_intended_overlap(baseline, bump,
                              reason="profile curve stands on its baseline")

        # (2026-07-05 draft review) split: the strip on the cut clause, the
        # lifted profile on the renormalization clause.
        with self.voiceover(
            text="Picture it on last video's surface: cut across the "
                 "support at height y,"
        ):
            self.play(defn[0].animate.set_color(INK),
                      Transform(box, strip), run_time=0.8)

        with self.voiceover(
            text="and the profile of the cut, renormalized to area one, "
                 "is the conditional density."
        ):
            self.play(Create(baseline), Create(bump), run_time=0.9)
            self.play(bump.animate.stretch(1.5, 1,
                                           about_point=base_c[1] * UP
                                           + base_c[0] * RIGHT),
                      FadeIn(area_lab), run_time=0.9)

        # The uniform disk, sliced at Y = 0.5.
        disk_c = LEFT * 3.4 + DOWN * 0.9
        disk = Circle(radius=1.5, color=INK, stroke_width=2)
        disk.set_fill(BAR, opacity=0.2).move_to(disk_c)
        half = np.sqrt(3) / 2
        chord_y = disk_c[1] + 0.5 * 1.5
        chord = Line([disk_c[0] - half * 1.5, chord_y, 0],
                     [disk_c[0] + half * 1.5, chord_y, 0],
                     color=ACCENT, stroke_width=5)
        # (2026-07-05 draft review) endpoint labels sit symmetrically OUT
        # along the chord line, clear of the circle; y = 0.5 stays on the
        # chord's level but keeps its distance from the right endpoint.
        end_l = MathTex(r"-\tfrac{\sqrt{3}}{2}", font_size=CAPTION,
                        color=MUTED)
        end_l.next_to(chord.get_start(), LEFT, buff=0.45)
        end_r = MathTex(r"\tfrac{\sqrt{3}}{2}", font_size=CAPTION,
                        color=MUTED)
        end_r.next_to(chord.get_end(), RIGHT, buff=0.45)
        y_lab = MathTex(r"y = 0.5", font_size=CAPTION, color=MUTED)
        y_lab.next_to(end_r, UP, buff=0.35)
        mark_intended_overlap(
            disk, chord, end_l, end_r, y_lab,
            reason="chord and endpoint labels sit on the disk")
        marg = MathTex(
            r"f_Y(0.5) = \int f_{X,Y}(x, 0.5)\, dx = \frac{\sqrt{3}}{\pi}",
            font_size=SMALL, color=INK,
        ).move_to(RIGHT * 3.3 + DOWN * 1.0)
        fit_to_frame(marg)

        # (2026-07-05 draft review) per-phrase sub-blocks: chord on its
        # clause, marginal value on its clause.
        with self.voiceover(text="Try it on the uniform disk."):
            self.play(FadeOut(VGroup(region, flab, box, baseline, bump,
                                     area_lab)), run_time=0.5)
            self.play(Create(disk), run_time=0.7)

        with self.voiceover(
            text="Given Y equals one half, the slice is a chord running "
                 "from minus root three over two to plus root three over "
                 "two,"
        ):
            self.play(Create(chord), FadeIn(end_l), FadeIn(end_r),
                      FadeIn(y_lab), run_time=0.9)

        with self.voiceover(
            text="and the marginal there is root three over pi."
        ):
            self.play(Write(marg), run_time=1.0)

        level_y = disk_c[1] + 1.5 + 0.55
        level = Line([disk_c[0] - half * 1.5, level_y, 0],
                     [disk_c[0] + half * 1.5, level_y, 0],
                     color=INK, stroke_width=4)
        dash_l = DashedLine([disk_c[0] - half * 1.5, chord_y, 0],
                            [disk_c[0] - half * 1.5, level_y, 0],
                            color=MUTED, stroke_width=2, dash_length=0.1)
        dash_r = DashedLine([disk_c[0] + half * 1.5, chord_y, 0],
                            [disk_c[0] + half * 1.5, level_y, 0],
                            color=MUTED, stroke_width=2, dash_length=0.1)
        mark_intended_overlap(disk, dash_l, dash_r,
                              reason="risers connect the chord to its "
                                     "flat conditional density")
        flat = MathTex(
            r"f_{X \mid Y}(x \mid 0.5)", "=",
            r"\frac{1}{\sqrt{3}}, \quad |x| \le \frac{\sqrt{3}}{2}",
            font_size=BODY,
        ).move_to(RIGHT * 3.3 + DOWN * 2.4)
        fit_to_frame(flat)

        # (2026-07-05 draft review) split: the level segment on the
        # constant, a held frame for the closing breath.
        with self.voiceover(
            text="Dividing leaves a constant: one over root three along "
                 "the chord."
        ):
            self.play(chord.animate.set_color(INK),
                      Create(dash_l), Create(dash_r), run_time=0.6)
            self.play(Create(level), run_time=0.6)
            self.play(level.animate.set_color(ACCENT),
                      Write(flat), run_time=1.0)

        with self.voiceover(
            text="A flat surface conditions to a flat slice — uniform in, "
                 "uniform out."
        ):
            self.wait(0.3)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionalExpectation(VoiceoverScene):
    """Beat: cond-expectation -- slice means, h(X), and the MMSE channel."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditional Expectation")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Each observation hands us a fresh density — and any "
                 "density has a mean."
        ):
            self.wait(0.3)

        # (2026-07-05 draft review) the event version renders at the SAME
        # font size as the first equation (was SMALL); MUTED keeps it
        # secondary, and even_stack rebalances the taller stack.
        e1 = MathTex(
            expectation(r"g(Y) \mid X = x"), "=",
            r"\int g(y)\, f_{Y \mid X}(y \mid x)\, dy",
            font_size=BODY,
        )
        fit_to_frame(e1)
        e2 = MathTex(
            expectation(r"g(Y) \mid S") +
            r"= \int g(y)\, f_{Y \mid S}(y)\, dy",
            font_size=BODY, color=MUTED,
        )
        fit_to_frame(e2)
        h1 = MathTex(r"h(x) = " + expectation(r"Y \mid X = x"),
                     font_size=BODY, color=INK)
        h_cap = Text("a random variable", font_size=CAPTION, color=MUTED)
        h_block = VGroup(h1, h_cap).arrange(DOWN, buff=0.3)
        even_stack(e1, e2, h_block, top=2.0, bottom=-2.2)
        h2 = MathTex(r"h(X) = " + expectation(r"Y \mid X"),
                     font_size=BODY, color=ACCENT).move_to(h1)

        with self.voiceover(
            text="The conditional expectation of g of Y, given X equals x, "
                 "is an integral now: g of y, weighted by the conditional "
                 "density of the slice."
        ):
            self.play(Write(e1), run_time=1.2)
            self.play(e1[0].animate.set_color(ACCENT), run_time=0.5)

        # (2026-07-05 draft review) the event version lands on "Given an
        # event", not front-loaded with the first integral.
        with self.voiceover(
            text="Given an event, the same formula runs with the "
                 "event-conditioned density."
        ):
            self.play(FadeIn(e2), run_time=0.7)

        with self.voiceover(
            text="Chapter seven's discovery returns intact: sweep the "
                 "observation, and the slice means trace a function, h of "
                 "x."
        ):
            self.play(e1[0].animate.set_color(INK), Write(h1), run_time=0.9)

        # (2026-07-05 draft review) the morph to h(X) lands on "Feed the
        # random X in".
        with self.voiceover(
            text="Feed the random X in, and the conditional expectation "
                 "of Y given X is itself a random variable."
        ):
            self.play(Transform(h1, h2), FadeIn(h_cap), run_time=0.9)

        # The noisy channel: X in, Y = X + N out.
        def node(label):
            box = RoundedRectangle(corner_radius=0.12, width=1.0, height=0.8)
            box.set_stroke(INK, 2)
            lab = MathTex(label, font_size=BODY, color=INK)
            lab.move_to(box.get_center())
            g = VGroup(box, lab)
            mark_intended_overlap(g, reason="node label inside its box")
            return g

        x_node = node("X").move_to(LEFT * 2.8 + UP * 0.9)
        plus = VGroup(
            Circle(radius=0.32, color=INK, stroke_width=2),
            MathTex("+", font_size=BODY, color=INK),
        )
        plus[1].move_to(plus[0].get_center())
        mark_intended_overlap(plus, reason="plus sign inside the sum node")
        plus.move_to(UP * 0.9)
        y_node = node("Y").move_to(RIGHT * 2.8 + UP * 0.9)
        n_lab = MathTex("N", font_size=BODY, color=INK).move_to(UP * 2.3)
        a1 = Arrow(x_node.get_right(), plus.get_left(), buff=0.12,
                   color=MUTED, stroke_width=3)
        a2 = Arrow(plus.get_right(), y_node.get_left(), buff=0.12,
                   color=MUTED, stroke_width=3)
        a3 = Arrow(n_lab.get_bottom(), plus.get_top(), buff=0.12,
                   color=MUTED, stroke_width=3)
        diagram = VGroup(x_node, plus, y_node, n_lab, a1, a2, a3)
        eq = MathTex("Y = X + N", font_size=BODY, color=INK)
        eq.move_to(DOWN * 0.3)
        eq_cap = Text("X and N standard Gaussian, independent",
                      font_size=CAPTION, color=MUTED)
        eq_cap.next_to(eq, DOWN, buff=0.3)

        # (2026-07-05 draft review) per-phrase sub-blocks: each stage of
        # the diagram arrives as its part is narrated.
        with self.voiceover(
            text="Here is that machine doing engineering."
        ):
            self.play(FadeOut(VGroup(e1, e2, h1, h_cap)), run_time=0.4)

        with self.voiceover(
            text="A transmitter sends a standard Gaussian signal X."
        ):
            self.play(FadeIn(x_node), FadeIn(plus), run_time=0.6)
            self.play(Create(a1), run_time=0.5)

        with self.voiceover(
            text="The channel adds independent standard Gaussian noise N, "
                 "and the receiver reads Y equals X plus N."
        ):
            self.play(FadeIn(n_lab), Create(a3), run_time=0.6)
            self.play(FadeIn(y_node), Create(a2), run_time=0.6)
            self.play(Write(eq), FadeIn(eq_cap), run_time=0.9)

        with self.voiceover(
            text="Given the value received, what should it guess for X?"
        ):
            self.wait(0.3)

        # Slice the Gaussian surface at the received y: a bell at y/2.
        axes2 = Axes(
            x_range=[-2, 3, 1],
            y_range=[0, 1.0, 0.5],
            x_length=5.2,
            y_length=2.4,
            axis_config={"include_numbers": False},
            tips=False,
        )
        axes2.to_edge(DOWN, buff=0.8).shift(LEFT * 2.9)
        bell = axes2.plot(lambda x: 0.8 * np.exp(-((x - 1.0) ** 2)),
                          x_range=[-2, 3], color=INK)
        dashed = DashedLine(axes2.c2p(1.0, 0), axes2.c2p(1.0, 0.8),
                            color=MUTED, stroke_width=2, dash_length=0.1)
        peak_lab = MathTex(r"\tfrac{y}{2}", font_size=CAPTION, color=MUTED)
        peak_lab.next_to(axes2.c2p(1.0, 0), DOWN, buff=0.2)
        mark_intended_overlap(
            axes2, bell, dashed, peak_lab,
            reason="bell curve, peak riser, and its label sit on the axes")

        g1 = MathTex(
            r"f_{X \mid Y}(x \mid y) = \frac{1}{\sqrt{\pi}}\,"
            r"e^{-(4x^2 - 4xy + y^2)/4}",
            font_size=SMALL, color=INK,
        ).move_to(RIGHT * 3.4 + DOWN * 1.2)
        fit_to_frame(g1)
        params = MathTex(
            r"\text{Gaussian:}\quad m = \frac{y}{2}, \quad"
            r"\sigma^2 = \frac{1}{2}",
            font_size=SMALL, color=ACCENT,
        ).next_to(g1, DOWN, buff=0.35)

        # (2026-07-05 draft review) split: the sliced profile on its
        # sentence, the algebra on the collapse sentence.
        with self.voiceover(
            text="Slice the joint Gaussian surface at the received y."
        ):
            self.play(FadeOut(eq_cap), run_time=0.3)
            self.play(Create(axes2), run_time=0.6)
            self.play(Create(bell), run_time=0.8)

        with self.voiceover(
            text="The algebra collapses to a Gaussian in x, with mean y "
                 "over two and variance one half."
        ):
            self.play(Write(g1), run_time=1.0)
            self.play(Write(params), Create(dashed), FadeIn(peak_lab),
                      run_time=0.9)

        est = MathTex(
            expectation(r"X \mid Y = y"), "=", r"\frac{y}{2}",
            font_size=BODY,
        ).next_to(params, DOWN, buff=0.4)
        fit_to_frame(est)

        # (2026-07-05 draft review) split: the estimate on its sentence, a
        # held frame for the workhorse close.
        with self.voiceover(
            text="The minimum mean square error estimate is the mean of "
                 "that slice: the estimate of X is y over two — split the "
                 "difference between the received value and the zero-mean "
                 "prior."
        ):
            self.play(params.animate.set_color(INK), Write(est),
                      run_time=0.9)
            self.play(est[2].animate.set_color(ACCENT), run_time=0.5)
            self.play(Indicate(dashed, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        with self.voiceover(
            text="That estimator, a conditional expectation, is the "
                 "workhorse of communication and control."
        ):
            self.wait(0.3)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JacobianDerived(VoiceoverScene):
    """Beat: jacobian -- the two-dimensional change of variables + outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Derived Distributions")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        recall = MathTex(r"f_Y(y) = \frac{f_X(x)}{|g'(x)|}",
                         font_size=SMALL, color=MUTED)
        recall.next_to(title, DOWN, buff=0.4)

        # (2026-07-05 draft review) the recall card lands on its own
        # sentence, not the beat opener.
        with self.voiceover(
            text="One tool remains: transforming pairs."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="Chapter nine turned the density of X into the density of "
                 "g of X, paying with the derivative of g."
        ):
            self.play(FadeIn(recall), run_time=0.7)

        maps = MathTex(
            r"Y_1 = g_1(X_1, X_2), \quad Y_2 = g_2(X_1, X_2)",
            font_size=BODY, color=INK,
        ).next_to(recall, DOWN, buff=0.5)
        fit_to_frame(maps)
        inv_cap = Text("invertible: each output from exactly one input",
                       font_size=CAPTION, color=MUTED)
        inv_cap.next_to(maps, DOWN, buff=0.25)

        # (2026-07-05 draft review) the "invertible" caption fades in as
        # the word is spoken.
        with self.voiceover(
            text="Now map two variables to two. Y one and Y two are "
                 "functions of X one and X two — differentiable,"
        ):
            self.play(Write(maps), run_time=1.1)

        with self.voiceover(
            text="and invertible, so every output point comes from exactly "
                 "one input point."
        ):
            self.play(FadeIn(inv_cap), run_time=0.6)

        # A square patch maps to a parallelogram; area scales by |J|.
        # (2026-07-05 draft review) both planes ride further LEFT so the
        # right-hand column holds the Jacobian card with the final equation
        # directly below it -- one balanced two-column composition.
        lframe = Square(side_length=2.0, color=MUTED, stroke_width=2)
        lframe.move_to(LEFT * 4.5 + DOWN * 1.1)
        llab = MathTex(r"(x_1, x_2)", font_size=CAPTION, color=MUTED)
        llab.next_to(lframe, DOWN, buff=0.2)
        patch = Square(side_length=0.5, color=INK, stroke_width=1.5)
        patch.set_fill(BAR, opacity=0.5)
        patch.move_to(lframe.get_center() + RIGHT * 0.25 + UP * 0.2)
        rframe = Square(side_length=2.0, color=MUTED, stroke_width=2)
        rframe.move_to(LEFT * 1.1 + DOWN * 1.1)
        rlab = MathTex(r"(y_1, y_2)", font_size=CAPTION, color=MUTED)
        rlab.next_to(rframe, DOWN, buff=0.2)
        para = Polygon(
            [0, 0, 0], [0.72, 0.16, 0], [0.98, 0.72, 0], [0.26, 0.56, 0],
            color=INK, stroke_width=1.5,
        )
        para.set_fill(BAR, opacity=0.5)
        para.move_to(rframe.get_center() + RIGHT * 0.1 + UP * 0.1)
        g_arrow = Arrow(lframe.get_right(), rframe.get_left(), buff=0.15,
                        color=MUTED, stroke_width=3)
        g_lab = MathTex("g", font_size=CAPTION, color=MUTED)
        g_lab.next_to(g_arrow, UP, buff=0.15)
        mark_intended_overlap(lframe, patch,
                              reason="the patch lives inside its plane")
        mark_intended_overlap(rframe, para,
                              reason="the image patch lives inside its plane")
        jdet = MathTex(
            r"J(x_1, x_2) = \det \begin{bmatrix}"
            r"\frac{\partial g_1}{\partial x_1} &"
            r"\frac{\partial g_1}{\partial x_2} \\[2pt]"
            r"\frac{\partial g_2}{\partial x_1} &"
            r"\frac{\partial g_2}{\partial x_2}"
            r"\end{bmatrix} \neq 0",
            font_size=SMALL, color=INK,
        ).move_to(RIGHT * 3.4 + DOWN * 0.5)
        fit_to_frame(jdet)

        # (2026-07-05 draft review) per-phrase sub-blocks: the patch on its
        # opener, the mapped parallelogram on its clause, the determinant
        # card as it is named.
        with self.voiceover(
            text="Watch a small square of probability."
        ):
            self.play(Create(lframe), FadeIn(llab), Create(rframe),
                      FadeIn(rlab), run_time=0.8)
            self.play(FadeIn(patch), run_time=0.5)

        with self.voiceover(
            text="The map carries it to a parallelogram,"
        ):
            self.play(Create(g_arrow), FadeIn(g_lab), run_time=0.6)
            self.play(FadeIn(para, shift=RIGHT * 0.3), run_time=0.7)

        with self.voiceover(
            text="and the factor by which its area stretches is the "
                 "Jacobian determinant, the determinant of the two-by-two "
                 "matrix of partial derivatives."
        ):
            self.play(Write(jdet), run_time=1.2)

        # (2026-07-05 draft review) the final equation sits directly BELOW
        # the Jacobian expression, closing the right-hand column.
        fyy = MathTex(
            r"f_{Y_1, Y_2}(y_1, y_2)", "=",
            r"\frac{f_{X_1, X_2}(x_1, x_2)}{|J(x_1, x_2)|}",
            font_size=BODY,
        ).next_to(jdet, DOWN, buff=0.55)
        fit_to_frame(fyy)

        with self.voiceover(
            text="Probability itself cannot stretch, so the density must "
                 "compensate: the joint density of the new pair is the old "
                 "density at the pre-image, divided by the absolute "
                 "Jacobian."
        ):
            self.play(Write(fyy), run_time=1.2)
            self.play(fyy[2].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text="One dimension paid with the absolute derivative of g. "
                 "Two dimensions pay with a determinant."
        ):
            self.wait(0.3)

        gauss_lines = VGroup(
            MathTex(r"\mathbf{Y} = A\mathbf{X} + \mathbf{b}",
                    font_size=BODY, color=INK),
            MathTex(expectation(r"\mathbf{Y}") +
                    r"= A\mathbf{m} + \mathbf{b}, \qquad"
                    r"\Sigma_{\mathbf{Y}} = A \Sigma A^{\mathrm{T}}",
                    font_size=BODY, color=INK),
            Text("Gaussian in, Gaussian out", font_size=CAPTION,
                 color=MUTED),
        ).arrange(DOWN, buff=0.45)
        gauss_lines.move_to(DOWN * 0.4)
        fit_to_frame(gauss_lines)

        # (2026-07-05 draft review) per-phrase sub-blocks: each Gaussian
        # line is written as it is spoken; "which partly explains why they
        # dominate" per the review's wording note.
        with self.voiceover(
            text="The star application takes one breath: push a jointly "
                 "Gaussian vector through any invertible affine map, A X "
                 "plus b,"
        ):
            self.play(FadeOut(VGroup(recall, maps, inv_cap, lframe, llab,
                                     patch, rframe, rlab, para, g_arrow,
                                     g_lab, jdet, fyy)), run_time=0.5)
            self.play(Write(gauss_lines[0]), run_time=0.8)

        with self.voiceover(
            text="and the Jacobian formula returns the Gaussian form — "
                 "mean A m plus b, covariance A Sigma A transpose."
        ):
            self.play(Write(gauss_lines[1]), run_time=1.0)

        with self.voiceover(
            text="Gaussians survive every affine map, in any dimension, "
                 "which partly explains why they dominate engineering."
        ):
            self.play(gauss_lines[1].animate.set_color(ACCENT),
                      FadeIn(gauss_lines[2]), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # (2026-07-05 draft review) "the conditional expectation" replaces
        # "the estimate you should make" -- spoken line and card in harmony.
        outro = outro_bridge(
            ["Conditioning a density is slicing and renormalizing -",
             "every slice has a mean: the conditional expectation."],
            next_title="Independent Continuous Variables",
        )

        with self.voiceover(
            text="The key idea of this video: conditioning a density is "
                 "slicing and renormalizing — and every slice has a mean, "
                 "which is the conditional expectation."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
