# derived_from: content/39-independence-continuous-script.md
# derived_from_sha256: 0e6165a107b4d7314a99db4aabb92a3007b66a8e3a12c8e8aa8da641e647791e
"""Chapter 11, Video 3 -- Independent Continuous Variables.

Source notes : random_vectors.tex (Section Independence, excluding the sums
               subsection) -- the factoring joint CDF, the product density,
               conditional = marginal, events factor, and the unit-square
               example with W = X + Y as the dependence counterexample.
Script        : content/39-independence-continuous-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/independence_continuous.py ChapterOverview
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
    section_title,
    mass_table,
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


# Halfway rule (2026-07-05 draft review round 2, stated at 2:41, 3:20, 5:30,
# 5:40, 5:50, 6:28): a beat's main content — figure column and equation
# column alike — sits centered HALFWAY between the bottom of the docked
# title and the bottom of the frame. Computed from a real docked
# section_title (the video-37 pattern), not eyeballed; both scene titles
# bottom out at the same y, so one module constant serves every beat.
_DOCKED_TITLE = section_title("The Density Factors").to_edge(UP)
CONTENT_MID_Y = zone_center_y(_DOCKED_TITLE)


def clamp_to_frame(m, margin=0.6, bottom=0.8):
    """Shift a placed mobject back inside the safe frame area (never scales).

    Layout guard: right/left/top use `margin`; the bottom lane keeps the
    house >= 0.8 clearance. Returns the mobject for chaining.
    """
    half_w = config.frame_width / 2
    half_h = config.frame_height / 2
    r = m.get_right()[0]
    if r > half_w - margin:
        m.shift(LEFT * (r - (half_w - margin)))
    l = m.get_left()[0]
    if l < -(half_w - margin):
        m.shift(RIGHT * (-(half_w - margin) - l))
    b = m.get_bottom()[1]
    if b < -(half_h - bottom):
        m.shift(UP * (-(half_h - bottom) - b))
    t = m.get_top()[1]
    if t > half_h - margin:
        m.shift(DOWN * (t - (half_h - margin)))
    return m


def bell(t, sigma2=0.03):
    """A [0,1]-parametrized bell profile peaking at t = 1/2 (hardcoded)."""
    return float(np.exp(-((t - 0.5) ** 2) / sigma2))


def product_patch(color=BAR, width=3.0, n=480, peak=0.85, dip=None):
    """The smooth product density f_X(x) f_Y(y), seen from above.

    One deterministic numpy intensity map (the ``density_patch`` technique
    from the joint-density video), shown as an ImageMobject with the height
    in the alpha channel so it blends into the background with no outline.
    Both factors are the SAME bell profile drawn along the square's edges,
    so the interior is their product by construction — a smooth surface,
    not a table of cells (2026-07-05 draft review, 2:42).

    ``dip=(center, sigma2, depth)`` thins the horizontal marginal around
    ``center`` (in [0,1] coordinates); the whole column above it thins with
    it, which is the factoring story told by one image swap.

    ImageMobject is NOT a VMobject: never put it in a VGroup, size it by
    assigning .width, and animate it only with FadeIn/FadeOut/.animate.
    """
    ts = np.linspace(0.0, 1.0, n)
    fx = np.exp(-((ts - 0.5) ** 2) / 0.03)
    if dip is not None:
        c0, s2, depth = dip
        fx = fx * (1.0 - depth * np.exp(-((ts - c0) ** 2) / s2))
    fy = np.exp(-((ts - 0.5) ** 2) / 0.03)
    z = np.outer(fy[::-1], fx)  # image rows run top -> bottom
    rgb = ManimColor(color).to_int_rgb()
    rgba = np.zeros((n, n, 4), dtype=np.uint8)
    rgba[..., 0] = rgb[0]
    rgba[..., 1] = rgb[1]
    rgba[..., 2] = rgb[2]
    rgba[..., 3] = np.rint(z * peak * 255.0).astype(np.uint8)
    img = ImageMobject(rgba)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bicubic"])
    img.width = width
    return img


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Independent Continuous Variables",
            ["Certify independence with one factoring equation:",
             "joint CDF, density, and every event pair split into products."],
            kicker="Chapter 11  ·  Multiple Continuous Random Variables",
        )
        tag = progress_tag(3, 4).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The definition: a factoring CDF",
                 font_size=BODY, color=INK),
            Text("2.  Densities, slices, and events factor too",
                 font_size=BODY, color=INK),
            Text("3.  The unit square: one pass, one fail",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video, conditioning with densities: observe one "
                 "variable, and the density of the other responds, slice by "
                 "slice. This video is about the opposite situation, the one "
                 "where nothing responds at all."
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
            text="We define independence for continuous variables with a "
                 "single factoring equation,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="watch it cascade down to densities, to conditional "
                 "slices, and to every pair of events,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and then put the definition to work on the unit square, "
                 "where the two coordinates pass the test and a third "
                 "variable, built from the first two, fails it."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class IndependenceDefinition(VoiceoverScene):
    """Beat: indep-cdf-def -- the factoring joint CDF, at every point."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Independence")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The video-24 callback: a small muted lattice + the discrete
        # product, gone once the continuous story starts.
        glyph = mass_table([[None] * 3] * 3, cell_w=0.8, cell_h=0.55)
        disc_eq = MathTex(r"p_{X,Y}(x,y) = p_X(x)\, p_Y(y)",
                          font_size=SMALL, color=MUTED)
        disc = VGroup(glyph, disc_eq).arrange(DOWN, buff=0.45)
        disc.move_to(DOWN * 0.9)
        fit_to_frame(disc)

        with self.voiceover(
            text="When does knowing X tell you nothing about Y? Chapter "
                 "seven answered for discrete variables with a table: "
                 "independence meant every cell of the joint PMF was the "
                 "product of its row margin and its column margin."
        ):
            self.play(FadeIn(glyph), run_time=0.8)
            self.play(Write(disc_eq), run_time=1.0)

        # The accumulation quadrant on the plane (left column).
        axes = Axes(
            x_range=[0, 4, 4], y_range=[0, 3, 3],
            x_length=4.4, y_length=3.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        ).set_color(MUTED)
        axes.move_to(LEFT * 3.3 + DOWN * 1.0)
        origin = axes.c2p(0, 0)
        p1 = axes.c2p(2.6, 2.1)
        p2 = axes.c2p(1.2, 2.5)

        def quadrant(p):
            q = Rectangle(
                width=p[0] - origin[0], height=p[1] - origin[1],
                fill_color=BAR, fill_opacity=0.22,
                stroke_color=BAR, stroke_width=1.5,
            )
            q.move_to(origin, aligned_edge=DL)
            return q

        quad = quadrant(p1)
        dot = Dot(p1, radius=0.06, color=INK)
        corner_lab = MathTex(r"(x, y)", font_size=CAPTION, color=INK)
        corner_lab.move_to(p1 + UP * 0.28 + RIGHT * 0.38)
        f_lab = MathTex(r"F_{X,Y}(x,y)", font_size=SMALL, color=MUTED)
        f_lab.next_to(axes, DOWN, buff=0.3)
        clamp_to_frame(f_lab)
        mark_intended_overlap(
            axes, quad, dot, corner_lab,
            reason="accumulation quadrant shades the plane from the origin")

        with self.voiceover(
            text="Continuous variables have no table. But every pair of "
                 "random variables has a joint CDF: the probability of the "
                 "quadrant where X stays at or below little x and Y stays "
                 "at or below little y."
        ):
            self.play(FadeOut(disc), run_time=0.5)
            self.play(Create(axes), run_time=0.7)
            self.play(FadeIn(quad), FadeIn(dot), FadeIn(corner_lab),
                      run_time=0.8)
            self.play(Write(f_lab), run_time=0.7)

        eq = MathTex(
            r"F_{X,Y}(x,y)", "=", r"F_X(x)\, F_Y(y)",
            font_size=BODY,
        ).move_to(RIGHT * 3.2 + UP * 1.0)
        clamp_to_frame(eq)

        with self.voiceover(
            text="That is where the definition lives. X and Y are "
                 "independent when the joint CDF factors: F of X and Y, at "
                 "x and y, equals F of X at x, times F of Y at y."
        ):
            self.play(Write(eq), run_time=1.4)
            self.play(eq[2].animate.set_color(ACCENT), run_time=0.5)

        all_cap = MathTex(r"\text{for all } x, y \in \mathbb{R}",
                          font_size=SMALL, color=MUTED)
        all_cap.next_to(eq, DOWN, buff=0.35)

        with self.voiceover(
            text="And the equality must hold at every point of the plane. "
                 "Pick any corner; the probability of its quadrant splits "
                 "into a product. One quadrant that refuses to split is "
                 "enough to destroy independence."
        ):
            self.play(FadeIn(all_cap, shift=UP * 0.2), run_time=0.6)
            self.play(
                Transform(quad, quadrant(p2)),
                dot.animate.move_to(p2),
                corner_lab.animate.move_to(p2 + UP * 0.28 + RIGHT * 0.38),
                run_time=1.2,
            )

        u_cap = Text("one definition for every kind of random variable",
                     font_size=CAPTION, color=MUTED)
        u_cap.next_to(all_cap, DOWN, buff=0.5)
        clamp_to_frame(u_cap)

        with self.voiceover(
            text="Because the CDF exists for every random variable, "
                 "discrete, continuous, or mixed, this one equation is the "
                 "master definition. The rest of this video is what it "
                 "becomes once densities enter the picture."
        ):
            self.play(FadeIn(u_cap, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class PDFFactorizes(VoiceoverScene):
    """Beat: pdf-factorizes -- differentiate; the product-surface picture."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Density Factors")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        d1 = MathTex(
            r"f_{X,Y}(x,y) = \frac{\partial^2 F_{X,Y}}"
            r"{\partial x\, \partial y}(x,y)",
            font_size=SMALL, color=INK)
        d2 = MathTex(r"= \frac{dF_X}{dx}(x)\, \frac{dF_Y}{dy}(y)",
                     font_size=SMALL, color=INK)
        res = MathTex(r"f_{X,Y}(x,y)", "=", r"f_X(x)\, f_Y(y)",
                      font_size=BODY)
        eqs = VGroup(d1, d2, res).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # The Gaussian-callback caption: two stacked lines at SMALL, broken
        # at the ":" (2026-07-05 draft review round 2, 3:12). The register
        # is unchanged — MUTED, de-numbered — only shape and size moved.
        g_cap = VGroup(
            MathTex(r"\text{the joint density's two Gaussians:}",
                    font_size=SMALL, color=MUTED),
            MathTex(r"f_X \times f_Y \text{ by construction}",
                    font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.22)
        g_cap.next_to(eqs, DOWN, buff=0.6)

        # The right column ENDS the beat centered on the halfway anchor
        # (2026-07-05 draft review round 2, 3:20): place equations +
        # caption so their combined block sits at CONTENT_MID_Y.
        _right = VGroup(eqs, g_cap)
        _right.move_to(RIGHT * 3.2 + UP * CONTENT_MID_Y)
        clamp_to_frame(_right)

        with self.voiceover(
            text="Now let the pair be jointly continuous, and "
                 "differentiate. The joint density is the mixed partial "
                 "derivative of the joint CDF, once in x and once in y."
        ):
            self.play(Write(d1), run_time=1.2)

        with self.voiceover(
            text="On a factored CDF, each derivative acts on its own "
                 "factor: the derivative of F of X in x, times the "
                 "derivative of F of Y in y."
        ):
            self.play(Write(d2), run_time=1.2)

        with self.voiceover(
            text="Those are the marginal densities. The joint density "
                 "factors too: f of X and Y, at x and y, equals f of X at "
                 "x, times f of Y at y."
        ):
            self.play(Write(res), run_time=1.2)
            self.play(res[2].animate.set_color(ACCENT),
                      d1.animate.set_color(MUTED),
                      d2.animate.set_color(MUTED), run_time=0.5)

        # The smooth product surface: two marginal profiles weaving the
        # square. The old 7x7 cell grid read as a discrete table; the
        # interior is now the density_patch gradient — a single smooth
        # ImageMobject whose intensity is f_X(x) f_Y(y)
        # (2026-07-05 draft review, 2:42).
        side = 3.0
        dip = (0.65, 0.006, 0.85)
        sq = Square(side_length=side).set_stroke(MUTED, 2)
        sq.move_to(LEFT * 3.2 + DOWN * 0.7)
        left_x = sq.get_left()[0]
        bot_y = sq.get_bottom()[1]

        patch = product_patch(width=side).move_to(sq.get_center())
        thinned = product_patch(width=side, dip=dip)
        thinned.move_to(sq.get_center())

        def fx_point(t, d=None):
            v = bell(t)
            if d is not None:
                c0, s2, depth = d
                v *= 1.0 - depth * float(np.exp(-((t - c0) ** 2) / s2))
            return np.array([left_x + t * side,
                             bot_y - 0.85 + 0.6 * v, 0])

        prof_x = ParametricFunction(
            lambda t: fx_point(t), t_range=[0, 1]).set_stroke(INK, 2)
        prof_x_dip = ParametricFunction(
            lambda t: fx_point(t, dip), t_range=[0, 1]).set_stroke(INK, 2)
        prof_x_back = ParametricFunction(
            lambda t: fx_point(t), t_range=[0, 1]).set_stroke(INK, 2)
        # The y-axis Gaussian rides closer to the square: baseline gap
        # 0.85 -> 0.55 (2026-07-05 draft review round 2, 2:41).
        prof_y = ParametricFunction(
            lambda t: np.array([left_x - 0.55 - 0.6 * bell(t),
                                bot_y + t * side, 0]),
            t_range=[0, 1]).set_stroke(INK, 2)
        fx_lab = MathTex(r"f_X(x)", font_size=CAPTION, color=MUTED)
        fx_lab.next_to(prof_x, RIGHT, buff=0.2)
        fy_lab = MathTex(r"f_Y(y)", font_size=CAPTION, color=MUTED)
        fy_lab.next_to(prof_y, UP, buff=0.2)
        # The whole left figure — square, gradient, both edge profiles and
        # their labels — centers on the halfway anchor (2026-07-05 draft
        # review round 2, 2:41). Group (not VGroup): patch/thinned are
        # ImageMobjects; a plain y-shift is all that's needed.
        _fig = Group(sq, patch, thinned, prof_x, prof_x_dip, prof_x_back,
                     prof_y, fx_lab, fy_lab)
        _fig.shift(UP * (CONTENT_MID_Y - _fig.get_center()[1]))
        mark_intended_overlap(
            sq, patch, thinned,
            reason="the smooth product gradient fills the square region")

        with self.voiceover(
            text="Here is the picture to keep. Lay the density of X along "
                 "the horizontal edge, and the density of Y along the "
                 "vertical edge. The joint density over the square is woven "
                 "from their product: the shade over any point is its "
                 "column profile times its row profile. The table that "
                 "factored for discrete variables has become a factoring "
                 "density."
        ):
            self.play(Create(sq), run_time=0.6)
            self.play(Create(prof_x), FadeIn(fx_lab), run_time=0.8)
            self.play(Create(prof_y), FadeIn(fy_lab), run_time=0.8)
            self.play(FadeIn(patch), run_time=1.6)

        with self.voiceover(
            text="Wherever X is likely and Y is likely, the joint is at "
                 "its darkest; thin either margin, and its whole row or "
                 "column thins with it."
        ):
            self.play(res[2].animate.set_color(INK), run_time=0.3)
            self.play(Flash(sq.get_center(), color=ACCENT,
                            flash_radius=0.45), run_time=0.8)
            self.play(FadeOut(patch), FadeIn(thinned),
                      Transform(prof_x, prof_x_dip), run_time=0.8)
            self.play(FadeOut(thinned), FadeIn(patch),
                      Transform(prof_x, prof_x_back), run_time=0.8)

        with self.voiceover(
            text="The two independent Gaussians from when we met the joint "
                 "density were built exactly this way. There we wrote the "
                 "product on faith; this equation is the license."
        ):
            self.play(FadeIn(g_cap, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionalIsMarginal(VoiceoverScene):
    """Beat: conditional-is-marginal -- frozen slices, and events factor."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning Learns Nothing")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Recall preview: last video's responsive slice, drawn live so the
        # opening narration has something to land on — the frame is no
        # longer dark while the recap is spoken (2026-07-05 draft review,
        # 3:30). Verbatim re-split of the original block into three
        # phrases; the picture is the DEPENDENT case, so the profile
        # changes shape when the slice slides.
        r_side = 2.9
        r_sq = Square(side_length=r_side).set_stroke(MUTED, 2)
        r_sq.move_to([0.0, zone_center_y(title), 0])
        r_left = r_sq.get_left()[0]
        r_bot = r_sq.get_bottom()[1]

        def recall_slice(frac, sigma2, height):
            x0 = r_left + frac * r_side
            line = DashedLine(
                [x0, r_bot, 0], [x0, r_bot + r_side, 0],
                color=MUTED, stroke_width=2, dash_length=0.10)
            curve = ParametricFunction(
                lambda t: np.array([x0 + height * bell(t, sigma2),
                                    r_bot + t * r_side, 0]),
                t_range=[0, 1]).set_stroke(ACCENT, 2.5)
            return line, curve

        r_line, r_curve = recall_slice(0.30, 0.020, 0.55)
        line2, curve2 = recall_slice(0.68, 0.055, 0.38)
        r_xlab = MathTex(r"X = x", font_size=CAPTION, color=MUTED)
        r_xlab.next_to(r_line, DOWN, buff=0.2)
        xlab2 = MathTex(r"X = x", font_size=CAPTION, color=MUTED)
        xlab2.next_to(line2, DOWN, buff=0.2)
        mark_intended_overlap(
            r_sq, r_line, r_curve, line2, curve2,
            reason="the recalled slice line and its profile live inside "
                   "the preview square")

        with self.voiceover(
            text="Last video made dependence visible: condition on X "
                 "equals x,"
        ):
            self.play(Create(r_sq), run_time=0.6)
            self.play(Create(r_line), FadeIn(r_xlab), run_time=0.7)

        with self.voiceover(
            text="and the slice of the joint density at x, renormalized, "
                 "becomes the conditional density of Y."
        ):
            self.play(Create(r_curve), run_time=1.0)

        with self.voiceover(
            text="Slide the observation, and the slice responds."
        ):
            self.play(
                Transform(r_line, line2),
                Transform(r_curve, curve2),
                Transform(r_xlab, xlab2),
                run_time=1.2,
            )

        eq = MathTex(
            r"f_{Y \mid X}(y \mid x)", "=",
            r"\frac{f_{X,Y}(x,y)}{f_X(x)}", "=",
            r"\frac{f_X(x)\, f_Y(y)}{f_X(x)}", "=",
            r"f_Y(y)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(eq)

        with self.voiceover(
            text="Watch what independence does to that machinery. The "
                 "conditional density is the joint over the marginal. But "
                 "the joint is now a product, so the factor f of X at x "
                 "cancels top and bottom,"
        ):
            self.play(FadeOut(VGroup(r_sq, r_line, r_curve, r_xlab)),
                      run_time=0.5)
            self.play(Write(eq[:3]), run_time=1.2)
            self.play(Write(eq[3:5]), run_time=1.0)

        def_cap = MathTex(r"\text{wherever } f_X(x) \neq 0",
                          font_size=SMALL, color=MUTED)
        def_cap.next_to(eq, DOWN, buff=0.35)

        with self.voiceover(
            text="and what remains is the marginal density of Y, alone, "
                 "wherever f of X at x is not zero. Observing X changes "
                 "nothing about Y."
        ):
            self.play(Write(eq[5:7]), run_time=0.8)
            self.play(eq[6].animate.set_color(ACCENT),
                      FadeIn(def_cap), run_time=0.6)

        # The frozen slice family (video 38's sweep, switched off).
        side = 2.9
        sq = Square(side_length=side).set_stroke(MUTED, 2)
        sq.move_to(LEFT * 3.4 + DOWN * 1.2)
        s_left = sq.get_left()[0]
        s_bot = sq.get_bottom()[1]

        slice_lines = VGroup()
        slice_curves = VGroup()
        for frac in (0.25, 0.5, 0.75):
            x0 = s_left + frac * side
            slice_lines.add(DashedLine(
                [x0, s_bot, 0], [x0, s_bot + side, 0],
                color=MUTED, stroke_width=2, dash_length=0.10))
            slice_curves.add(ParametricFunction(
                lambda t, x0=x0: np.array(
                    [x0 + 0.45 * bell(t, 0.02), s_bot + t * side, 0]),
                t_range=[0, 1]).set_stroke(INK, 2))
        same_cap = Text("every slice, the same profile",
                        font_size=CAPTION, color=MUTED)
        same_cap.next_to(sq, DOWN, buff=0.3)
        clamp_to_frame(same_cap, bottom=0.8)
        mark_intended_overlap(
            sq, slice_lines, slice_curves,
            reason="slice lines and their profiles live inside the square")

        with self.voiceover(
            text="Every slice, at every x you might observe, renormalizes "
                 "to the same curve. The responsiveness we called "
                 "dependence has been switched off. This is the discrete "
                 "lesson that all the table's rows were proportional, now "
                 "said with densities."
        ):
            self.play(Create(sq), run_time=0.6)
            self.play(LaggedStart(*[Create(l) for l in slice_lines],
                                  lag_ratio=0.25), run_time=0.9)
            self.play(LaggedStart(*[Create(c) for c in slice_curves],
                                  lag_ratio=0.25), run_time=1.1)
            self.play(FadeIn(same_cap), run_time=0.5)

        # Events factor: a vertical strip times a horizontal strip.
        frame = Square(side_length=side).set_stroke(MUTED, 2)
        frame.move_to(sq)
        v_strip = Rectangle(width=0.75, height=side,
                            fill_color=BAR, fill_opacity=0.25,
                            stroke_width=0)
        v_strip.move_to(frame.get_center() + LEFT * 0.5)
        h_strip = Rectangle(width=side, height=0.65,
                            fill_color=TEAL, fill_opacity=0.25,
                            stroke_width=0)
        h_strip.move_to(frame.get_center() + DOWN * 0.45)
        s_lab = MathTex(r"X \in S", font_size=CAPTION, color=INK)
        s_lab.next_to(v_strip, DOWN, buff=0.18)
        t_lab = MathTex(r"Y \in T", font_size=CAPTION, color=INK)
        t_lab.next_to(h_strip, LEFT, buff=0.18)
        ev_rect = Rectangle(width=0.75, height=0.65,
                            stroke_color=INK, stroke_width=2.5)
        ev_rect.move_to([v_strip.get_center()[0],
                         h_strip.get_center()[1], 0])
        mark_intended_overlap(
            frame, v_strip, h_strip, ev_rect, s_lab, t_lab,
            reason="the event strips cross inside the plane by design")

        ev_lines = VGroup(
            MathTex(pr(r"X \in S,\, Y \in T") +
                    r"= \int_S \int_T f_{X,Y}(x,y)\, dy\, dx",
                    font_size=SMALL, color=INK),
            MathTex(r"= \int_S f_X(x)\, dx \int_T f_Y(y)\, dy",
                    font_size=SMALL, color=INK),
            MathTex("=" + pr(r"X \in S") + pr(r"Y \in T"),
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ev_lines.move_to(RIGHT * 3.1 + DOWN * 1.6)
        clamp_to_frame(ev_lines)

        with self.voiceover(
            text="And the product climbs back up to events. Take any set S "
                 "of values for X, and any set T for Y. The probability "
                 "that both happen at once is a double integral of the "
                 "joint density over the rectangle S cross T."
        ):
            self.play(FadeOut(VGroup(sq, slice_lines, slice_curves,
                                     same_cap)),
                      eq[6].animate.set_color(INK), run_time=0.6)
            self.play(Create(frame), run_time=0.5)
            self.play(FadeIn(v_strip), Write(s_lab), run_time=0.7)
            self.play(FadeIn(h_strip), Write(t_lab), run_time=0.7)
            self.play(Create(ev_rect), run_time=0.6)
            self.play(Write(ev_lines[0]), run_time=1.0)

        with self.voiceover(
            text="Factor the integrand, and the double integral splits "
                 "into two ordinary ones: the probability that X lands in "
                 "S, times the probability that Y lands in T. Independent "
                 "variables manufacture independent events, every pair of "
                 "them at once, exactly the notion chapter four defined "
                 "one pair at a time."
        ):
            self.play(Write(ev_lines[1]), run_time=1.0)
            self.play(Write(ev_lines[2]), run_time=0.9)
            self.play(ev_lines[2].animate.set_color(ACCENT),
                      ev_rect.animate.set_stroke(INK, 4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UnitSquareExample(VoiceoverScene):
    """Beat: unit-square -- X vs Y pass; X vs W = X + Y fail at one point."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Unit Square, Both Verdicts")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # All the square-internal geometry, built up front and marked once.
        side = 3.2
        sq = Square(side_length=side)
        sq.set_stroke(MUTED, 2).set_fill(BAR, opacity=0.10)
        sq.move_to(LEFT * 3.6 + DOWN * 0.9)

        def sqp(u, v):
            """Unit-square coordinates -> scene point."""
            c = sq.get_corner(DL)
            return c + RIGHT * (u * side) + UP * (v * side)

        zero_lab = MathTex("0", font_size=CAPTION, color=MUTED)
        zero_lab.next_to(sq.get_corner(DL), DL, buff=0.12)
        one_x = MathTex("1", font_size=CAPTION, color=MUTED)
        one_x.next_to(sq.get_corner(DR), DOWN, buff=0.15)
        one_y = MathTex("1", font_size=CAPTION, color=MUTED)
        one_y.next_to(sq.get_corner(UL), LEFT, buff=0.15)

        # The left figure — square plus its 0/1 edge labels — centers on
        # the halfway anchor for the whole beat, covering both the
        # pass-verdict view and the later W = X + Y view of the same
        # square (2026-07-05 draft review round 2, 5:30 and 5:50). All
        # interior geometry below derives from sq's corners AFTER this
        # shift, so it follows automatically.
        _fig = VGroup(sq, zero_lab, one_x, one_y)
        _fig.shift(UP * (CONTENT_MID_Y - _fig.get_center()[1]))

        corner_rect = Rectangle(
            width=0.7 * side, height=0.55 * side,
            fill_color=GREEN, fill_opacity=0.30,
            stroke_color=GREEN, stroke_width=1.5)
        corner_rect.move_to(sq.get_corner(DL), aligned_edge=DL)
        pt = Dot(sqp(0.7, 0.55), radius=0.06, color=INK)
        pt_lab = MathTex(r"(x, y)", font_size=CAPTION, color=INK)
        pt_lab.move_to(sqp(0.7, 0.55) + UP * 0.25 + RIGHT * 0.35)

        diag = Line(sqp(0, 1), sqp(1, 0)).set_stroke(INK, 2)
        diag_lab = MathTex(r"x + y = 1", font_size=CAPTION, color=MUTED)
        diag_lab.move_to(sqp(0.72, 0.72))

        trap = Polygon(sqp(0, 0), sqp(0.5, 0), sqp(0.5, 0.5), sqp(0, 1),
                       fill_color=MAROON, fill_opacity=0.35,
                       stroke_color=MAROON, stroke_width=1.5)

        mark_intended_overlap(
            sq, corner_rect, pt, pt_lab, diag, diag_lab, trap,
            reason="example regions and labels layer inside the unit square")

        # Coordinates read x, y on screen — not omega_1, omega_2
        # (2026-07-05 draft review, 5:19; vendored source normalized to
        # match).
        setup = VGroup(
            MathTex(r"X = x, \quad Y = y",
                    font_size=SMALL, color=INK),
            MathTex(r"(x, y) \text{ uniform on } [0,1]^2",
                    font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.25)
        setup.move_to(RIGHT * 3.2 + UP * 1.9)

        # The pass-verdict column is built up front so its FINAL stack
        # (setup + both equations + indicator caption) can end the portion
        # centered on the halfway anchor (2026-07-05 draft review round 2,
        # 5:40); the reveals below are unchanged.
        eq1 = MathTex(r"F_{X,Y}(x,y)", "=", r"x\, y", font_size=BODY)
        eq1.next_to(setup, DOWN, buff=0.55)
        eq2 = MathTex("=", r"F_X(x)\, F_Y(y)", font_size=BODY, color=ACCENT)
        eq2.next_to(eq1, DOWN, buff=0.3)
        ind_cap = MathTex(
            r"F_{X,Y}(x,y) = \int_{-\infty}^{x}\! \mathbf{1}_{[0,1]}(u)\, du"
            r"\int_{-\infty}^{y}\! \mathbf{1}_{[0,1]}(v)\, dv",
            font_size=CAPTION, color=MUTED)
        ind_cap.next_to(eq2, DOWN, buff=0.4)
        _col1 = VGroup(setup, eq1, eq2, ind_cap)
        _col1.shift(UP * (CONTENT_MID_Y - _col1.get_center()[1]))
        clamp_to_frame(_col1)

        with self.voiceover(
            text="Time to run the test honestly. Pick a point uniformly at "
                 "random from the unit square, and let X and Y be its two "
                 "coordinates."
        ):
            self.play(Create(sq), run_time=0.7)
            self.play(FadeIn(zero_lab), FadeIn(one_x), FadeIn(one_y),
                      run_time=0.5)
            self.play(Write(setup[0]), run_time=0.8)
            self.play(FadeIn(setup[1]), run_time=0.6)

        with self.voiceover(
            text="For x and y between zero and one, the joint CDF is the "
                 "area of the corner rectangle: x times y."
        ):
            self.play(FadeIn(corner_rect), FadeIn(pt), FadeIn(pt_lab),
                      run_time=0.9)
            self.play(Write(eq1), run_time=1.0)

        with self.voiceover(
            text="But x is exactly F of X at x, and y is F of Y at y. The "
                 "joint is the product at every such point, and writing "
                 "the CDF as a product of two indicator integrals extends "
                 "the check to the whole plane. The coordinates are "
                 "independent."
        ):
            self.play(Write(eq2), run_time=0.9)
            self.play(FadeIn(ind_cap, shift=UP * 0.2), run_time=0.8)

        # The fail-verdict column is likewise built up front so its FINAL
        # stack (W definition + point evaluations + trapezoid CDF +
        # verdict) ends the beat centered on the halfway anchor
        # (2026-07-05 draft review round 2, 6:28).
        w_eq = MathTex(r"W = X + Y", font_size=BODY, color=INK)
        nums = VGroup(
            MathTex(r"F_W(1) = \tfrac{1}{2}", font_size=SMALL, color=INK),
            MathTex(r"F_X(0.5) = \tfrac{1}{2}", font_size=SMALL, color=INK),
            MathTex(r"F_X(0.5)\, F_W(1) = \tfrac{1}{4}",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        nums.next_to(w_eq, DOWN, buff=0.4)
        reg_eq = MathTex(
            r"F_{X,W}(0.5, 1) = \int_0^{1/2} (1 - x)\, dx = \tfrac{3}{8}",
            font_size=SMALL, color=INK)
        reg_eq.next_to(nums, DOWN, buff=0.4)
        verdict = MathTex(r"\tfrac{3}{8}", r"\neq", r"\tfrac{1}{4}",
                          font_size=BODY, color=ACCENT)
        verdict.next_to(reg_eq, DOWN, buff=0.35)
        _col2 = VGroup(w_eq, nums, reg_eq, verdict)
        _col2.move_to(RIGHT * 3.2 + UP * CONTENT_MID_Y)
        clamp_to_frame(_col2)

        with self.voiceover(
            text="Now build a third variable from the same two "
                 "coordinates: W, the sum of X and Y. A variable assembled "
                 "out of X should remember X. Independence needs every "
                 "point of the plane to factor, so a single failure "
                 "convicts."
        ):
            self.play(FadeOut(VGroup(corner_rect, pt, pt_lab, eq1, eq2,
                                     ind_cap, setup)), run_time=0.6)
            self.play(Write(w_eq), run_time=0.8)
            self.play(Create(diag), FadeIn(diag_lab), run_time=0.9)

        with self.voiceover(
            text="Evaluate at the point x equals one half, w equals one. F "
                 "of W at one is one half, and F of X at one half is one "
                 "half, so the product is one quarter."
        ):
            self.play(Write(nums[0]), run_time=0.7)
            self.play(Write(nums[1]), run_time=0.7)
            self.play(Write(nums[2]), run_time=0.8)

        with self.voiceover(
            text="The joint CDF is the probability of landing left of one "
                 "half and below the diagonal line: a trapezoid of area "
                 "three eighths."
        ):
            self.play(FadeIn(trap), run_time=0.9)
            self.play(Write(reg_eq), run_time=1.0)

        with self.voiceover(
            text="Three eighths is not one quarter. X and W are "
                 "dependent, not through anything exotic, but simply "
                 "because one variable was built from the other."
        ):
            self.play(Write(verdict), run_time=0.8)
            self.play(Indicate(verdict, color=ACCENT, scale_factor=1.06),
                      run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Independence is a factoring joint: CDF, density, events -",
             "and conditioning learns nothing new."],
            next_title="Sums of Continuous Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video: independence is a factoring "
                 "joint. The CDF, the density, and every pair of events "
                 "split into products, and conditioning learns nothing "
                 "new. As for the sum W, its distribution is precisely "
                 "where the next video begins."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
