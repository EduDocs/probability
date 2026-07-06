# derived_from: content/40-continuous-sums-script.md
# derived_from_sha256: 0865d3300d5f59e40623df19af28a1502b0f89319fb78ae2c1867e78e8c38d80
"""Chapter 11, Video 4 -- Sums of Continuous Random Variables.

Source notes : random_vectors.tex (Independence section, "Sums of
               Continuous Random Variables" subsection) -- the convolution
               of densities, the CDF proof, the uniform/exponential/
               Gaussian worked sums, and the MGF product rule.
Script        : content/40-continuous-sums-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/continuous_sums.py ChapterOverview
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
    zone_center_y,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


# Halfway rule (2026-07-05 draft review round 2, 1:52 / 2:27): a beat's main
# content — figure column and equation column alike — centers HALFWAY between
# the docked title's bottom and the frame bottom. Computed from a real docked
# section_title (the video-39 pattern), not eyeballed; the section titles in
# this file bottom out at the same y, so one module constant serves.
_DOCKED_TITLE = section_title("The Convolution of Densities").to_edge(UP)
CONTENT_MID_Y = zone_center_y(_DOCKED_TITLE)


def dice_total_chart(unit=5.4, bar_w=0.22, gap=0.32):
    """A miniature two-dice total bar chart (totals 2..12, peak at 7).

    The triangle silhouette from the discrete chapter, recalled for the
    twin moment. Returns VGroup(baseline, bars, x_labels).
    """
    heights = [(6 - abs(k - 7)) / 36 for k in range(2, 13)]
    n = len(heights)
    span = gap * (n - 1) + bar_w + 0.5
    baseline = Line(LEFT * span / 2, RIGHT * span / 2,
                    color=MUTED, stroke_width=2)
    bars = VGroup()
    for i, h in enumerate(heights):
        cx = -gap * (n - 1) / 2 + gap * i
        bar = Rectangle(width=bar_w, height=unit * h,
                        fill_color=BAR, fill_opacity=0.85,
                        stroke_color=INK, stroke_width=1)
        bar.move_to([cx, unit * h / 2, 0])
        bars.add(bar)
    xlabels = VGroup()
    for i, txt in ((0, "2"), (5, "7"), (10, "12")):
        cx = -gap * (n - 1) / 2 + gap * i
        # Tick numbers read at TICK (2026-07-05 review round 2, type-scale
        # audit) — these play the role of axis ticks on the mini chart.
        xlabels.add(MathTex(txt, font_size=TICK, color=MUTED)
                    .next_to([cx, 0, 0], DOWN, buff=0.18))
    chart = VGroup(baseline, bars, xlabels)
    mark_intended_overlap(baseline, bars,
                          reason="bars stand on the chart baseline")
    return chart


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            ["Sums of Continuous", "Random Variables"],
            ["Find the density of a sum of independent variables:",
             "convolve the densities, or let the MGF turn sums into products."],
            kicker="Chapter 11  ·  Multiple Continuous Random Variables",
        )
        tag = progress_tag(4, 4).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The convolution of densities", font_size=BODY,
                 color=INK),
            Text("2.  Three sums, worked", font_size=BODY, color=INK),
            Text("3.  Sums become products", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="This chapter closes with the question the whole course "
                 "keeps returning to: add two independent continuous random "
                 "variables, and what is the density of the sum?"
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
            text="In this video the discrete convolution of chapter seven "
                 "ripens into an integral: for independent variables, the "
                 "density of a sum is the convolution of the densities."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We run that integral three times — two uniforms fold into "
                 "a triangle, two exponentials into an Erlang, two Gaussians "
                 "into another Gaussian —"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and then we skip the integral entirely: under the moment "
                 "generating function, sums become products."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConvolutionDefinition(VoiceoverScene):
    """Beat: convolution-def -- the claim, the discrete twin, the CDF proof."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Convolution of Densities")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        recall = MathTex(r"f_{X,Y}(x, y) = f_X(x)\, f_Y(y)",
                         font_size=SMALL, color=MUTED)
        recall.next_to(title, DOWN, buff=0.45)
        wsum = MathTex(r"W = X + Y", font_size=BODY, color=INK)
        wsum.next_to(recall, DOWN, buff=0.35)

        with self.voiceover(
            text="Last video left us with a factored joint: for independent "
                 "X and Y, the joint density is the product of the "
                 "marginals. Here is what that purchase buys. Form the sum, "
                 "W equals X plus Y — a new random variable. What is its "
                 "density?"
        ):
            self.play(Write(recall), run_time=1.0)
            self.play(Write(wsum), run_time=0.8)

        claim = MathTex(
            r"f_W(w)", "=", r"(f_X \ast f_Y)(w)", "=",
            r"\int_{-\infty}^{\infty} f_X(u)\, f_Y(w - u)\, du",
            font_size=BODY,
        ).next_to(wsum, DOWN, buff=0.5)
        fit_to_frame(claim)
        sym = Text("symmetric in the two factors", font_size=CAPTION,
                   color=MUTED)
        sym.next_to(claim, DOWN, buff=0.3)

        with self.voiceover(
            text="The claim: the density of W is the convolution of the two "
                 "marginal densities. For each target value w, integrate f X "
                 "of u, times f Y of w minus u, over every u — every way of "
                 "splitting w into two pieces gets weighed, and the roles of "
                 "X and Y can be swapped without changing the answer."
        ):
            self.play(Write(claim), run_time=1.6)
            self.play(claim[0].animate.set_color(ACCENT),
                      FadeIn(sym), run_time=0.6)

        discrete = MathTex(
            r"p_{X+Y}(k) = \sum_{m} p_X(m)\, p_Y(k - m)",
            font_size=SMALL, color=MUTED,
        ).next_to(sym, DOWN, buff=0.45)

        with self.voiceover(
            text="When we convolved PMFs, we did exactly this with masses: "
                 "the PMF of a sum collected p X of m times p Y of k minus "
                 "m over all m. Replace masses by densities and the sum by "
                 "an integral, and it is the same sliding machine, gone "
                 "continuous."
        ):
            self.play(Write(discrete), run_time=1.2)

        # The CDF proof: half-plane picture left, derivation right.
        plane = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=3.6, y_length=3.6, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        ).move_to([-3.6, CONTENT_MID_Y, 0])
        # Axis names at BODY (2026-07-05 review round 2, type-scale audit;
        # STYLE_BOOK 12: tick numbers TICK, axis names BODY).
        ulabel = MathTex("u", font_size=BODY, color=MUTED)
        ulabel.next_to(plane.x_axis.get_end(), DOWN, buff=0.18)
        vlabel = MathTex("v", font_size=BODY, color=MUTED)
        vlabel.next_to(plane.y_axis.get_end(), LEFT, buff=0.18)
        wline = plane.plot(lambda u: 1.0 - u, x_range=[-1.4, 2.4])
        wline.set_stroke(INK, 2.5)
        region = Polygon(
            plane.c2p(-2.4, -2.4), plane.c2p(2.4, -2.4),
            plane.c2p(2.4, -1.4), plane.c2p(-1.4, 2.4),
            plane.c2p(-2.4, 2.4),
            stroke_width=0, fill_color=TEAL, fill_opacity=0.25,
        )
        # Line tag at BODY (2026-07-05 review round 2, type-scale audit —
        # the chart_tag rule: SMALL/CAPTION tags on charts read too small).
        line_label = MathTex(r"u + v = w", font_size=BODY, color=INK)
        line_label.next_to(plane.c2p(2.4, -1.4), RIGHT, buff=0.2)
        mark_intended_overlap(
            plane, wline, region, ulabel, vlabel, line_label,
            reason="half-plane below the line u + v = w, shaded on the plane")
        # 2026-07-05 draft review round 2 (1:52): the LEFT figure's center
        # sits ON the halfway anchor — center the visible group (axes +
        # labels + line + region), not just the axes.
        figure = VGroup(plane, ulabel, vlabel, wline, region, line_label)
        figure.shift(UP * (CONTENT_MID_Y - figure.get_center()[1]))

        lines = VGroup(
            MathTex(r"F_W(w) = " + pr(r"X + Y \leq w"),
                    font_size=SMALL, color=INK),
            MathTex(r"= \int_{-\infty}^{\infty} \int_{-\infty}^{w-u} "
                    r"f_X(u)\, f_Y(v)\, dv\, du",
                    font_size=SMALL, color=INK),
            MathTex(r"= \int_{-\infty}^{\infty} F_Y(w - u)\, f_X(u)\, du",
                    font_size=SMALL, color=INK),
            MathTex(r"f_W(w) = \int_{-\infty}^{\infty} "
                    r"f_Y(w - u)\, f_X(u)\, du",
                    font_size=BODY, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        # 2026-07-05 draft review round 2 (2:27): the RIGHT equation block
        # ENDS the beat vertically centered on the halfway anchor.
        lines.move_to([3.4, CONTENT_MID_Y, 0])
        fit_to_frame(lines)

        with self.voiceover(
            text="To prove it, go through the CDF. The probability that W "
                 "is at most w is the probability that the pair X, Y lands "
                 "in the half plane below the line u plus v equals w."
        ):
            # Dock the recap at exactly SMALL, not an off-scale 0.8 x BODY
            # (2026-07-05 review round 2, type-scale audit).
            self.play(FadeOut(recall), FadeOut(wsum), FadeOut(sym),
                      FadeOut(discrete),
                      claim.animate.scale(SMALL / BODY)
                           .next_to(title, DOWN, buff=0.3)
                           .set_color(INK),
                      run_time=0.8)
            self.play(Create(plane), Write(ulabel), Write(vlabel),
                      run_time=0.8)
            self.play(Create(wline), Write(line_label), run_time=0.7)
            self.play(FadeIn(region), run_time=0.6)
            self.play(Write(lines[0]), run_time=0.8)
            self.play(Write(lines[1]), run_time=0.9)

        with self.voiceover(
            text="Independence factors the joint density, so the inner "
                 "integral runs the density of Y up to w minus u — and that "
                 "is a value of the CDF of Y."
        ):
            self.play(Write(lines[2]), run_time=1.0)

        with self.voiceover(
            text="Now differentiate with respect to w, sliding the "
                 "derivative under the integral. Each CDF of Y becomes a "
                 "density of Y, and what remains is exactly the convolution. "
                 "Claim proved — the fundamental theorem of calculus, used "
                 "judiciously."
        ):
            self.play(Write(lines[3]), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UniformSum(VoiceoverScene):
    """Beat: uniform-sum -- flip-and-slide traces the triangle."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Sum of Two Uniforms")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Slide stage (left): the fixed rectangle and the sliding mirror.
        # Ticks at TICK, axis names at BODY (2026-07-05 review round 2,
        # type-scale audit; STYLE_BOOK 12).
        sax = Axes(
            x_range=[-1.5, 3, 1], y_range=[0, 1.4, 1],
            x_length=6.0, y_length=2.6, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": True, "font_size": TICK,
                           "numbers_to_include": [0, 1, 2]},
        ).move_to(LEFT * 3.2 + DOWN * 0.4)
        sxlab = axis_label_x(sax, MathTex("u", font_size=BODY,
                                          color=MUTED), buff=0.25)

        unit_x = (sax.c2p(1, 0) - sax.c2p(0, 0))[0]
        unit_y = (sax.c2p(0, 1) - sax.c2p(0, 0))[1]

        fx_rect = Rectangle(width=unit_x, height=unit_y,
                            fill_color=BLUE, fill_opacity=0.35,
                            stroke_color=BLUE, stroke_width=2)
        fx_rect.move_to(sax.c2p(0.5, 0.5))
        # Chart tags at BODY (2026-07-05 review round 2, type-scale audit).
        fx_lab = MathTex(r"f_X", font_size=BODY, color=BLUE)
        fx_lab.next_to(fx_rect, UP, buff=0.12)

        fy_rect = Rectangle(width=unit_x, height=unit_y,
                            fill_color=TEAL, fill_opacity=0.35,
                            stroke_color=TEAL, stroke_width=2)
        fy_lab = MathTex(r"f_Y", font_size=BODY, color=TEAL)
        window = VGroup(fy_rect, fy_lab)

        def place_window(w):
            fy_rect.move_to(sax.c2p(w - 0.5, 0.5))
            fy_lab.next_to(fy_rect, UP, buff=0.12)
            return window

        def ov_rect(w):
            a, b = max(0.0, w - 1.0), min(1.0, w)
            r = Rectangle(width=(b - a) * unit_x, height=unit_y,
                          fill_color=ACCENT, fill_opacity=0.45,
                          stroke_width=0)
            r.move_to(sax.c2p((a + b) / 2, 0.5))
            return r

        mark_intended_overlap(
            sax, fx_rect, fx_lab, fy_rect, fy_lab,
            reason="the mirrored window slides across the fixed density")

        # Result stage (right): f_W traced point by point.
        rax = Axes(
            x_range=[0, 2.2, 1], y_range=[0, 1.2, 1],
            x_length=4.2, y_length=2.6, tips=False,
            axis_config={"include_numbers": True, "font_size": TICK,
                         "stroke_color": MUTED},
        ).move_to(RIGHT * 3.6 + DOWN * 0.4)
        rxlab = axis_label_x(rax, MathTex("w", font_size=BODY,
                                          color=MUTED), buff=0.25)
        rylab = rax.get_y_axis_label(
            MathTex(r"f_W(w)", font_size=BODY, color=MUTED),
            edge=LEFT, direction=LEFT, buff=0.3)
        result_group = VGroup(rax, rxlab, rylab)

        with self.voiceover(
            text="Now run the integral once — and watch it happen. Draw two "
                 "numbers independently from the unit interval, each "
                 "uniform: two flat rectangles of height one. What is the "
                 "density of their sum?"
        ):
            self.play(Create(sax), Write(sxlab), run_time=0.8)
            self.play(FadeIn(fx_rect), Write(fx_lab), run_time=0.7)
            self.play(Create(rax), Write(rxlab), Write(rylab), run_time=0.8)

        cap = Text("slide the mirror across", font_size=CAPTION, color=MUTED)
        cap.to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="Convolution has a picture: mirror one rectangle, then "
                 "slide it across the other. At each position w, the "
                 "density of the sum is the area where the two windows "
                 "overlap."
        ):
            place_window(-0.4)
            self.play(FadeIn(window, shift=RIGHT * 0.4), run_time=0.8)
            self.play(FadeIn(cap), run_time=0.5)

        self.wait(0.5)

        dots = VGroup(
            Dot(rax.c2p(0.5, 0.5), radius=0.06, color=INK),
            Dot(rax.c2p(1.0, 1.0), radius=0.06, color=INK),
            Dot(rax.c2p(1.5, 0.5), radius=0.06, color=INK),
        )
        ov = ov_rect(0.5)
        mark_intended_overlap(
            ov, sax, fx_rect, fy_rect,
            reason="the overlap area is the value of the convolution")

        with self.voiceover(
            text="For w between zero and one, the windows overlap on an "
                 "interval of length exactly w. The overlap grows, and the "
                 "density rises linearly: f of w equals w."
        ):
            # 2026-07-05 review (2:58): the slide is the key visualization —
            # long, smooth glides between checkpoint stops (ease into the
            # first stop, linear glide while the overlap grows/shrinks),
            # with breathing room at each stop.
            self.play(window.animate.shift(
                sax.c2p(0.0, 0.5) - fy_rect.get_center()),
                run_time=2.0, rate_func=smooth)
            self.play(FadeIn(ov), FadeIn(dots[0]), run_time=0.8)
            self.wait(0.4)
            self.play(window.animate.shift(
                sax.c2p(0.5, 0.5) - fy_rect.get_center()),
                Transform(ov, ov_rect(1.0)),
                run_time=2.5, rate_func=linear)
            self.play(FadeIn(dots[1]), run_time=0.6)

        self.wait(0.5)

        with self.voiceover(
            text="Past one, the sliding window begins to leave the other "
                 "side. The overlap shrinks at the same rate it grew, and "
                 "the density falls: two minus w, hitting zero at two."
        ):
            self.play(window.animate.shift(
                sax.c2p(1.0, 0.5) - fy_rect.get_center()),
                Transform(ov, ov_rect(1.5)),
                run_time=2.5, rate_func=linear)
            self.play(FadeIn(dots[2]), run_time=0.6)

        self.wait(0.5)

        result_group.add(dots)
        # Primary accent result reads at BODY, like every other beat's
        # (2026-07-05 review round 2, type-scale audit).
        tent_formula = MathTex(
            r"f_W(w) = \begin{cases} w & 0 \leq w \leq 1 \\"
            r" 2 - w & 1 < w \leq 2 \end{cases}",
            font_size=BODY, color=ACCENT,
        )

        with self.voiceover(
            text="Flat plus flat equals triangle. Sums near one can be "
                 "assembled in the most ways; sums near zero or two in "
                 "almost none."
        ):
            # One chart at a time: clear the slide stage, recentre the trace.
            self.play(FadeOut(sax), FadeOut(sxlab), FadeOut(fx_rect),
                      FadeOut(fx_lab), FadeOut(window), FadeOut(ov),
                      FadeOut(cap), run_time=0.6)
            self.play(result_group.animate.move_to(LEFT * 3.2 + DOWN * 0.6),
                      run_time=0.8)
            seg1 = rax.plot(lambda w: w, x_range=[0, 1]).set_stroke(INK, 3)
            seg2 = rax.plot(lambda w: 2 - w,
                            x_range=[1, 2]).set_stroke(INK, 3)
            # 2026-07-05 review (3:33): group the edges only AFTER their
            # Create animations. Adding them to the on-screen result_group
            # first made both pop in fully rendered, and each Create then
            # reset-and-redrew its edge (the right edge flashed twice).
            self.play(Create(seg1), run_time=0.7)
            self.play(Create(seg2), run_time=0.7)
            result_group.add(seg1, seg2)
            tent_formula.move_to(RIGHT * 3.3 + UP * 0.6)
            fit_to_frame(tent_formula)
            self.play(Write(tent_formula), run_time=1.0)

        dice = dice_total_chart()
        dice.move_to(RIGHT * 3.3 + DOWN * 1.9)
        dice_cap = Text("the two-dice total, sampled",
                        font_size=CAPTION, color=MUTED)
        dice_cap.next_to(dice, DOWN, buff=0.3)

        with self.voiceover(
            text="And you have met this shape before. The total of two dice "
                 "climbed bar by bar to seven, then fell away symmetrically. "
                 "That staircase was this triangle, sampled at the integers "
                 "— the discrete twin, resolved into a continuum."
        ):
            self.play(FadeIn(dice[0]), FadeIn(dice[2]), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in dice[1]],
                                  lag_ratio=0.08), run_time=1.2)
            self.play(FadeIn(dice_cap), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExponentialGaussianSums(VoiceoverScene):
    """Beat: exp-gauss-sums -- Erlang from exponentials, Gaussian stability."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # 2026-07-05 review (4:10 / 5:02): sequential section titles — the
        # frame reads "Exponentials" while the exponential sum is on screen,
        # then Transforms to "Gaussians" at the hand-off.
        title = section_title("Exponentials")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The reviewer's halfway anchor: content centered between the docked
        # title's bottom and the frame bottom (2026-07-05 review, 4:10-5:44).
        zone_y = zone_center_y(title)

        # 2026-07-05 draft review round 2 (4:20 / 5:20): the beat's fonts
        # read SMALL — the primary setup statement moves to BODY, axis
        # names to BODY, curve tags to BODY (STYLE_BOOK 12 / chart_tag
        # rule). Vertical anchors are good and stay untouched.
        setup = MathTex(
            r"f_X(u) = f_Y(u) = \lambda e^{-\lambda u}, \quad u \geq 0",
            font_size=BODY, color=INK,
        ).next_to(title, DOWN, buff=0.4)

        eax = Axes(
            x_range=[0, 5, 1], y_range=[0, 1.1, 0.5],
            x_length=4.8, y_length=2.4, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        ).move_to([-3.7, zone_y, 0])
        exlab = axis_label_x(eax, MathTex("u", font_size=BODY,
                                          color=MUTED), buff=0.25)
        ecurve = eax.plot(lambda u: math.exp(-u),
                          x_range=[0, 5]).set_stroke(BLUE, 3)
        eclab = MathTex(r"\lambda e^{-\lambda u}", font_size=BODY,
                        color=BLUE)
        eclab.move_to(eax.c2p(2.6, 0.55))
        # Center the visible chart (axes + curve + labels) on the anchor.
        echart = VGroup(eax, exlab, ecurve, eclab)
        echart.shift(UP * (zone_y - echart.get_center()[1]))

        with self.voiceover(
            text="Two more sums from the notes, each carrying its own "
                 "lesson. First, add two independent exponential waiting "
                 "times, rate lambda each."
        ):
            self.play(Write(setup), run_time=1.0)
            self.play(Create(eax), Write(exlab), run_time=0.7)
            self.play(Create(ecurve), Write(eclab), run_time=0.9)

        deriv = VGroup(
            MathTex(r"f_W(w) = \int_0^w \lambda e^{-\lambda(w-u)}\,"
                    r" \lambda e^{-\lambda u}\, du",
                    font_size=SMALL, color=INK),
            MathTex(r"= \int_0^w \lambda^2 e^{-\lambda w}\, du",
                    font_size=SMALL, color=INK),
            MathTex(r"\text{the integrand does not depend on } u",
                    font_size=CAPTION, color=MUTED),
            MathTex(r"f_W(w) = \lambda^2 w\, e^{-\lambda w}",
                    font_size=BODY, color=ACCENT),
            MathTex(r"\text{Erlang, } m = 2\text{: the wait for the "
                    r"second arrival}",
                    font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # Ends centered on the halfway anchor (2026-07-05 review, 4:50).
        deriv.move_to([3.4, zone_y, 0])
        fit_to_frame(deriv)

        with self.voiceover(
            text="For w at least zero, the convolution runs u from zero to "
                 "w — and something pleasant happens inside: e to the minus "
                 "lambda times w minus u, times e to the minus lambda u, "
                 "multiplies to e to the minus lambda w. The integration "
                 "variable cancels; the integrand is flat."
        ):
            self.play(Write(deriv[0]), run_time=1.1)
            self.play(Write(deriv[1]), run_time=0.9)
            self.play(FadeIn(deriv[2]), run_time=0.6)

        erl_curve = eax.plot(lambda w: w * math.exp(-w),
                             x_range=[0, 5]).set_stroke(BLUE, 3)
        erl_lab = MathTex(r"\lambda^2 w\, e^{-\lambda w}",
                          font_size=BODY, color=BLUE)
        erl_lab.move_to(eax.c2p(3.0, 0.55))
        new_xlab = MathTex("w", font_size=BODY,
                           color=MUTED).move_to(exlab)

        with self.voiceover(
            text="So the integral simply measures the length of the "
                 "interval, and the density is lambda squared, times w, "
                 "times e to the minus lambda w. That is the Erlang "
                 "distribution with parameter two, straight out of the "
                 "gallery of densities — now derived, and it reads "
                 "naturally: the sum of two exponential waits is the wait "
                 "for the second arrival."
        ):
            self.play(Write(deriv[3]), run_time=1.0)
            self.play(Transform(ecurve, erl_curve),
                      Transform(eclab, erl_lab),
                      Transform(exlab, new_xlab), run_time=1.0)
            self.play(FadeIn(deriv[4]), run_time=0.6)

        # Gaussians: one chart at a time -- clear the exponential stage.
        # Sequential title hand-off (2026-07-05 review, 5:02).
        gauss_title = section_title("Gaussians")
        fit_to_frame(gauss_title)
        gauss_title.to_edge(UP)
        gzone_y = zone_center_y(gauss_title)

        gax = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.5, 0.25],
            x_length=6.0, y_length=2.4, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        ).move_to([-3.4, gzone_y, 0])
        gxlab = axis_label_x(gax, MathTex("w", font_size=BODY,
                                          color=MUTED), buff=0.25)
        bell = gax.plot(
            lambda u: math.exp(-u * u / 2) / math.sqrt(2 * math.pi),
            x_range=[-4, 4]).set_stroke(BLUE, 3)
        bell_lab = MathTex(r"f_X = f_Y", font_size=BODY, color=BLUE)
        bell_lab.move_to(gax.c2p(2.3, 0.33))
        # Center the visible chart on the anchor (2026-07-05 review, 5:05).
        gchart = VGroup(gax, gxlab, bell, bell_lab)
        gchart.shift(UP * (gzone_y - gchart.get_center()[1]))

        glines = VGroup(
            MathTex(r"f_W(w) = \frac{1}{2\pi}\, e^{-w^2/4}"
                    r" \int_{-\infty}^{\infty} e^{-(u - w/2)^2}\, du",
                    font_size=SMALL, color=INK),
            Text("a Gaussian density: integrates to one",
                 font_size=CAPTION, color=MUTED),
            MathTex(r"f_W(w) = \frac{1}{\sqrt{4\pi}}\, e^{-w^2/4}",
                    font_size=BODY, color=ACCENT),
            Text("means add, variances add", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        # Ends centered on the halfway anchor (2026-07-05 review, 5:44).
        glines.move_to([3.4, gzone_y, 0])
        fit_to_frame(glines)

        with self.voiceover(
            text="Second, add two independent standard Gaussians. The "
                 "convolution multiplies two bells; complete the square in "
                 "the exponent, and the integrand splits into e to the "
                 "minus w squared over four, times a Gaussian density "
                 "centered at w over two. A Gaussian density integrates to "
                 "one — the same trick that tamed the bell curve's integral."
        ):
            self.play(FadeOut(setup), FadeOut(eax), FadeOut(exlab),
                      FadeOut(ecurve), FadeOut(eclab), FadeOut(deriv),
                      Transform(title, gauss_title),
                      run_time=0.6)
            self.play(Create(gax), Write(gxlab), run_time=0.7)
            self.play(Create(bell), Write(bell_lab), run_time=0.9)
            self.play(Write(glines[0]), run_time=1.2)
            self.play(FadeIn(glines[1]), run_time=0.6)

        wide_bell = gax.plot(
            lambda w: math.exp(-w * w / 4) / math.sqrt(4 * math.pi),
            x_range=[-4, 4]).set_stroke(INK, 3)
        wide_lab = MathTex(r"f_W", font_size=BODY, color=INK)
        wide_lab.move_to(gax.c2p(2.9, 0.14))

        with self.voiceover(
            text="What survives is one over the square root of four pi, "
                 "times e to the minus w squared over four: a Gaussian with "
                 "mean zero and variance two. Gaussian plus Gaussian stays "
                 "Gaussian — in general, the means add and the variances "
                 "add."
        ):
            self.play(Write(glines[2]), run_time=1.0)
            self.play(bell.animate.set_stroke(MUTED, 2),
                      bell_lab.animate.set_color(MUTED), run_time=0.5)
            self.play(Create(wide_bell), Write(wide_lab), run_time=0.9)
            self.play(FadeIn(glines[3]), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MGFProduct(VoiceoverScene):
    """Beat: mgf-product -- sums become products, one more time."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # Video 25's title card, returning verbatim.
        title = section_title("Sums Become Products")
        fit_to_frame(title)

        # 2026-07-05 review (5:47): "and honest work it was" cut.
        with self.voiceover(
            text="Each of those answers cost one integral."
        ):
            self.wait(0.3)

        # 2026-07-05 review (5:50): the title animation starts exactly with
        # the words "This chapter closes with the shortcut."
        with self.voiceover(
            text="This chapter closes with the shortcut."
        ):
            self.play(Write(title), run_time=1.2)

        with self.voiceover(
            text="Sums become products — the same banner the discrete "
                 "chapter flew, and the same trick underneath."
        ):
            self.play(title.animate.to_edge(UP))

        rule = VGroup(
            MathTex(r"M_W(s) = " + expectation(r"e^{sW}") + " = "
                    + expectation(r"e^{sX} e^{sY}"),
                    font_size=BODY, color=INK),
            MathTex("= " + expectation(r"e^{sX}") + r"\,"
                    + expectation(r"e^{sY}") + " = ",
                    r"M_X(s)\, M_Y(s)",
                    font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.next_to(title, DOWN, buff=0.55)
        fit_to_frame(rule)

        with self.voiceover(
            text="Take the moment generating function of the sum. e to the "
                 "s W splits into e to the s X, times e to the s Y — and "
                 "independence factors the expectation of the product. The "
                 "MGF of a sum is the product of the MGFs. We built this "
                 "transform when we introduced moment generating "
                 "functions; this is the moment it earns its keep."
        ):
            self.play(Write(rule[0]), run_time=1.2)
            self.play(Write(rule[1]), run_time=1.2)
            self.play(rule[1][1].animate.set_color(ACCENT), run_time=0.5)

        cards = VGroup(
            MathTex(r"M_X(s) = e^{m_1 s + \sigma_1^2 s^2 / 2}",
                    font_size=SMALL, color=INK),
            MathTex(r"M_Y(s) = e^{m_2 s + \sigma_2^2 s^2 / 2}",
                    font_size=SMALL, color=INK),
        ).arrange(RIGHT, buff=0.9)
        cards.next_to(rule, DOWN, buff=0.55)
        fit_to_frame(cards)

        with self.voiceover(
            text="Rerun the Gaussian sum, now with arbitrary parameters: "
                 "the MGF of each Gaussian is an exponential in s, with its "
                 "mean on the linear term and its variance on the square."
        ):
            self.play(rule[1][1].animate.set_color(INK), run_time=0.4)
            self.play(Write(cards[0]), run_time=0.9)
            self.play(Write(cards[1]), run_time=0.9)

        prod = MathTex(
            r"M_W(s) = \exp\left( (m_1 + m_2)\, s"
            r" + \frac{(\sigma_1^2 + \sigma_2^2)\, s^2}{2} \right)",
            font_size=BODY, color=ACCENT,
        ).next_to(cards, DOWN, buff=0.5)
        fit_to_frame(prod)
        pcap = MathTex(
            r"\text{Gaussian again: mean } m_1 + m_2,"
            r" \ \text{variance } \sigma_1^2 + \sigma_2^2",
            font_size=CAPTION, color=MUTED,
        ).next_to(prod, DOWN, buff=0.3)

        with self.voiceover(
            text="Multiply the two, and the exponents simply add: m one "
                 "plus m two on s, sigma one squared plus sigma two squared "
                 "on s squared over two. That is a Gaussian MGF with the "
                 "summed mean and the summed variance — the general fact, "
                 "in two lines, no convolution in sight."
        ):
            self.play(Write(prod), run_time=1.3)
            self.play(FadeIn(pcap), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["For independent variables, densities convolve,",
             "and transforms multiply."],
            next_title="Types of Convergence",
        )

        with self.voiceover(
            text="The key idea of this video: for independent variables, "
                 "densities convolve, and transforms multiply. Next up is "
                 "the final chapter: sums of many variables, and the types "
                 "of convergence that govern them."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
