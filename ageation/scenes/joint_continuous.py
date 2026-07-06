# derived_from: content/37-joint-continuous-script.md
# derived_from_sha256: 0cb95a9dc094a4356482cd762eb88b686f33be16a28e7163fa50565d390fed61
"""Chapter 11, Video 1 -- Joint Continuous Distributions.

Source notes : 37-joint-continuous.tex (Section 11.1, Joint Cumulative
               Distributions) -- the joint CDF, its limits, the joint PDF,
               probability as volume, marginal densities, and the two worked
               examples (uniform disk, Gaussian pair -> Rayleigh).
Script        : content/37-joint-continuous-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

The pipeline renders with plain Scene, so every three-dimensional idea gets a
two-dimensional stand-in: the joint CDF is a shaded quadrant of the plane
(overflowing the drawn axes -- the event runs to minus infinity both ways),
the density surface is a smooth gradient patch (a deterministic numpy
intensity image, opacity for height), and "volume" is spoken over a
highlighted region.

Draft render:
    uv run manim -pql scenes/joint_continuous.py ChapterOverview
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
    section_title,
    mass_table,
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


# Shared geometry for the density-surface patches (2026-07-05 draft review):
# JointPDF and MarginalPDFs show the SAME surface, so they share one center
# and one size.
#
# Halfway rule (2026-07-05 draft review round 2): body content sits HALFWAY
# between the bottom of the docked title and the bottom of the frame --
# computed from a real docked section_title, not eyeballed. Both beats'
# titles bottom out at y ~ 2.949, so the midline is ~ -0.525.
_TITLE_BOTTOM_Y = section_title("The Density Surface").to_edge(UP).get_bottom()[1]
CONTENT_MID_Y = (_TITLE_BOTTOM_Y - config.frame_height / 2) / 2
PATCH_CENTER = LEFT * 3.2 + UP * CONTENT_MID_Y
PATCH_WIDTH = 3.2


def density_patch(color=BLUE, width=PATCH_WIDTH, kind="gauss",
                  n=480, sigma=0.34, peak=0.92):
    """A density surface seen from above: one smooth deterministic gradient.

    A numpy-evaluated intensity map (no runtime randomness -- it is a plain
    function evaluation) shown as an ImageMobject with the height in the
    alpha channel, so the patch blends into the background with no outline.
    ``kind="gauss"`` is a 2-D Gaussian; ``kind="flat"`` is uniform on the
    disk inscribed in the image, with a SHARP boundary: the uniform density
    drops off discontinuously at the circle's edge, so the mask is a hard
    cutoff with ~1.5 px of anti-aliasing only -- no gradual fade
    (2026-07-05 draft review round 3, 5:41). The Gaussian patches stay soft.

    ImageMobject is NOT a VMobject: group it with Group(...), size it by
    assigning .width, and animate it only with FadeIn/FadeOut/.animate.
    """
    xs = np.linspace(-1.0, 1.0, n)
    gx, gy = np.meshgrid(xs, xs)
    if kind == "gauss":
        z = np.exp(-(gx ** 2 + gy ** 2) / (2.0 * sigma ** 2))
    else:
        r = np.sqrt(gx ** 2 + gy ** 2)
        aa = 1.5 * (2.0 / n)  # ~1.5 pixels, in r units -- crisp edge
        z = np.clip((1.0 - r) / aa, 0.0, 1.0)
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


def bell_profile(color=BLUE, width=PATCH_WIDTH, height=1.05, sigma=0.34):
    """The Gaussian patch's 1-D side profile (for the squash-down shot)."""
    half = width / 2.0
    s = sigma * half
    pts = [
        np.array([x, height * np.exp(-x * x / (2.0 * s * s)), 0.0])
        for x in np.linspace(-half, half, 81)
    ]
    curve = VMobject(stroke_color=color, stroke_width=3.5)
    curve.set_points_smoothly(pts)
    return curve


def lump_grid(cell=0.55):
    """Video 21's table as lumps of mass: a 4x4 grid, opacity = mass."""
    ops = [
        [0.10, 0.18, 0.14, 0.06],
        [0.18, 0.45, 0.34, 0.12],
        [0.14, 0.34, 0.26, 0.10],
        [0.06, 0.12, 0.10, 0.05],
    ]
    grid = VGroup()
    for i, row in enumerate(ops):
        for j, op in enumerate(row):
            sq = Square(side_length=cell)
            sq.set_stroke(MUTED, 1.2).set_fill(BAR, opacity=op)
            sq.move_to([(j - 1.5) * cell, (1.5 - i) * cell, 0])
            grid.add(sq)
    mark_intended_overlap(grid, reason="table cells share grid edges")
    return grid


# The video-21 mirror shown in the marginal beat: with-replacement urn table.
NINTHS_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["2", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["3", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
]


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Joint Continuous Distributions",
            ["Describe two continuous random variables with one joint CDF -",
             "and turn probability into volume under a density surface."],
            kicker="Chapter 11  ·  Multiple Continuous Random Variables",
        )
        tag = progress_tag(1, 4).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The joint CDF", font_size=BODY, color=INK),
            Text("2.  The density surface and volume",
                 font_size=BODY, color=INK),
            Text("3.  Marginal densities", font_size=BODY, color=INK),
            Text("4.  Two worked examples", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text='Chernoff and Jensen closed the chapter on bounds, and with it the single-variable story. But measurements come in pairs — a signal and its noise, a position in two coordinates — and they live on a continuum. This chapter describes two continuous random variables together.'
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
            text='In this video we meet the joint CDF, one function on the plane that records the probability of a whole quadrant,'
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text='then differentiate it twice into a density surface, where probability becomes volume over a region,'
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="recover each variable's own density by integrating the other away,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text='and run the machine on a flat disk and on two Gaussians — where a famous distribution falls out.'
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JointCDF(VoiceoverScene):
    """Beat: joint-cdf -- definition, the sweeping quadrant, the limits."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Joint CDF")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        defn = MathTex(
            r"F_{X,Y}(x, y)", "=", pr(r"X \leq x,\; Y \leq y"),
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(defn)
        outcome = MathTex(
            r"= \Pr\left(\{\omega \in \Omega \mid X(\omega) \leq x,\;"
            r" Y(\omega) \leq y\}\right)",
            font_size=SMALL, color=MUTED,
        ).next_to(defn, DOWN, buff=0.28)

        # Per-phrase re-split (2026-07-05 draft review round 3, 0:50): the
        # beat used to open on an empty stage for the whole first block.
        # The definition's left-hand side (the F_{X,Y} skeleton) now lands
        # on the first sentence, and the "table of masses" gets a compact
        # preview element that dissolves when mass vanishes on the continuum.
        pmf_preview = lump_grid(cell=0.5).move_to(LEFT * 3.4 + DOWN * 0.9)

        with self.voiceover(
            text='Two random variables, one experiment.'
        ):
            self.play(Write(defn[0]), run_time=1.0)

        with self.voiceover(
            text='Chapter seven described a discrete pair with a joint PMF — a table of masses.'
        ):
            self.play(FadeIn(pmf_preview, shift=UP * 0.2), run_time=0.9)

        with self.voiceover(
            text='On a continuum single points carry no mass, so we lean on the tool that carried single variables across this bridge: accumulate.'
        ):
            self.play(FadeOut(pmf_preview), run_time=0.9)

        with self.voiceover(
            text='The joint cumulative distribution function of X and Y is the probability that X is at most x and, at the same time, Y is at most y.'
        ):
            self.play(Write(defn[1]), Write(defn[2]), run_time=1.4)
            self.play(defn[0].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text='Keeping in mind that X and Y are functions on one sample space, this is the probability of the set of outcomes where both coordinates come in under their thresholds.'
        ):
            self.play(FadeIn(outcome, shift=DOWN * 0.2), run_time=0.8)

        # The plane, lower-left (raised and pushed right for balance,
        # 2026-07-05 draft review): a corner point and its SW quadrant.
        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=4.6, y_length=3.0,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        )
        axes.to_edge(DOWN, buff=1.25).to_edge(LEFT, buff=1.4)

        def quadrant(cx, cy):
            # The event {X <= x, Y <= y} runs to minus infinity in both
            # coordinates: anchor the shading PAST the drawn axes so nobody
            # reads it as stopping at zero.
            o = axes.c2p(-0.5, -0.45)
            c = axes.c2p(cx, cy)
            return Polygon(
                o, [c[0], o[1], 0], c, [o[0], c[1], 0],
                fill_color=BAR, fill_opacity=0.35,
                stroke_color=INK, stroke_width=1.5,
            )

        region = quadrant(2.2, 1.6)
        corner = Dot(axes.c2p(2.2, 1.6), radius=0.07, color=INK)
        clabel = MathTex(r"(x, y)", font_size=CAPTION, color=INK)
        clabel.next_to(corner, UR, buff=0.12)
        mark_intended_overlap(axes, region, corner, clabel,
                              reason="quadrant region shades the plane past "
                                     "both axes (the event runs to minus "
                                     "infinity); corner dot and label sit "
                                     "on its edge")

        with self.voiceover(
            text='Picture it on the plane. Fix a corner point.'
        ):
            self.play(Create(axes), run_time=0.7)
            self.play(FadeIn(corner, scale=1.6), FadeIn(clabel), run_time=0.6)

        with self.voiceover(
            text='The event collects every outcome landing at or below it and at or to its left — the whole southwest quadrant.'
        ):
            self.play(FadeIn(region), run_time=0.8)

        with self.voiceover(
            text='Slide the corner up and to the right, and the function accumulates probability, the one-variable sweep upgraded to two dimensions.'
        ):
            self.play(
                Transform(region, quadrant(3.1, 2.3)),
                corner.animate.move_to(axes.c2p(3.1, 2.3)),
                clabel.animate.next_to(axes.c2p(3.1, 2.3), UR, buff=0.12),
                run_time=1.4,
            )

        limy = MathTex(
            r"\lim_{y \to \infty} F_{X,Y}(x, y)", "=", r"F_X(x)",
            font_size=SMALL,
        ).move_to(RIGHT * 3.4 + DOWN * 0.6)
        fit_to_frame(limy)

        with self.voiceover(
            text='Limits recover the pieces.'
        ):
            self.play(defn[0].animate.set_color(INK), run_time=0.4)

        with self.voiceover(
            text='Push y to infinity: the constraint on Y evaporates, the quadrant grows into a half-plane,'
        ):
            self.play(
                Transform(region, quadrant(3.1, 3.35)),
                corner.animate.move_to(axes.c2p(3.1, 3.35)),
                clabel.animate.next_to(axes.c2p(3.1, 3.35), UR, buff=0.12),
                run_time=1.2,
            )

        with self.voiceover(
            text='and the joint CDF becomes the marginal CDF of X alone.'
        ):
            self.play(Write(limy), run_time=0.9)
            self.play(limy[2].animate.set_color(ACCENT), run_time=0.5)

        limx = MathTex(
            r"\lim_{x \to \infty} F_{X,Y}(x, y)", "=", r"F_Y(y)",
            font_size=SMALL,
        ).next_to(limy, DOWN, buff=0.35, aligned_edge=LEFT)

        with self.voiceover(
            text='Push x to infinity instead, and the marginal CDF of Y comes out.'
        ):
            self.play(limy[2].animate.set_color(INK), run_time=0.3)
            self.play(
                Transform(region, quadrant(4.4, 2.3)),
                corner.animate.move_to(axes.c2p(4.4, 2.3)),
                clabel.animate.next_to(axes.c2p(4.4, 2.3), UR, buff=0.12),
                run_time=1.0,
            )
            self.play(Write(limx), run_time=0.9)
            self.play(limx[2].animate.set_color(ACCENT), run_time=0.5)

        limzero = MathTex(
            r"\lim_{x \to -\infty} F_{X,Y}(x, y)", "=", r"0",
            font_size=SMALL,
        ).next_to(limx, DOWN, buff=0.35, aligned_edge=LEFT)

        with self.voiceover(
            text='And push either argument down to minus infinity: the quadrant slides off the plane, and the function falls to zero — the two-variable version of the CDF endpoints we met for a single variable.'
        ):
            self.play(limx[2].animate.set_color(INK), run_time=0.3)
            self.play(
                Transform(region, quadrant(0.25, 0.2)),
                corner.animate.move_to(axes.c2p(0.25, 0.2)),
                clabel.animate.next_to(axes.c2p(0.25, 0.2), UR, buff=0.12),
                run_time=1.0,
            )
            self.play(FadeOut(region), FadeOut(corner), FadeOut(clabel),
                      run_time=0.5)
            self.play(Write(limzero), run_time=0.9)

        with self.voiceover(
            text='One function carries both variables — and both marginals live inside it as limits.'
        ):
            self.play(Indicate(defn, color=ACCENT, scale_factor=1.03),
                      run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JointPDF(VoiceoverScene):
    """Beat: joint-pdf -- the mixed partial, and probability as volume."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Density Surface")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        mixed = MathTex(
            r"f_{X,Y}(x, y)", "=",
            r"\frac{\partial^2 F_{X,Y}}{\partial x\, \partial y}(x, y)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(mixed)
        jc_note = Text("jointly continuous when this density exists",
                       font_size=CAPTION, color=MUTED)
        jc_note.next_to(mixed, DOWN, buff=0.3)

        # The definition is written DURING the opening sentence (2026-07-05
        # draft review round 2, 2:12): the old cut left the stage empty for
        # the whole first block.
        with self.voiceover(
            text='For a single variable, one derivative turned the CDF into a density. Here there are two directions, so differentiate twice — once in x, once in y.'
        ):
            self.wait(0.3)
            self.play(Write(mixed), run_time=1.4)

        with self.voiceover(
            text='When the joint CDF is totally differentiable, this mixed partial derivative is the joint probability density function, and the order of differentiation does not matter. When the density exists, we call the pair jointly continuous.'
        ):
            self.play(mixed[0].animate.set_color(ACCENT), run_time=0.5)
            self.play(FadeIn(jc_note, shift=DOWN * 0.2), run_time=0.7)

        rebuild = MathTex(
            r"F_{X,Y}(x, y) = \int_{-\infty}^{x} \int_{-\infty}^{y}"
            r" f_{X,Y}(u, v)\, dv\, du",
            font_size=SMALL,
        ).next_to(jc_note, DOWN, buff=0.45)
        props = MathTex(
            r"f_{X,Y} \geq 0, \qquad \iint_{\mathbb{R}^2}"
            r" f_{X,Y}(u, v)\, dv\, du = 1",
            font_size=SMALL, color=MUTED,
        ).next_to(rebuild, DOWN, buff=0.3)

        with self.voiceover(
            text='Calculus runs backwards too: integrating the density over the quadrant rebuilds the CDF. And the density behaves as a density should — never negative, and integrating to one over the whole plane.'
        ):
            self.play(mixed[0].animate.set_color(INK), run_time=0.4)
            self.play(Write(rebuild), run_time=1.2)
            self.play(FadeIn(props, shift=DOWN * 0.2), run_time=0.8)

        # The discrete-to-continuous bridge: the joint table's lumps melt
        # into a smooth gradient patch (height above every point of the
        # plane). A brief pseudo-3D moment sells the surface: the Gaussian's
        # 1-D bell profile appears above (the surface seen from the side),
        # then squashes down onto the top-view gradient.
        grid = lump_grid().move_to(PATCH_CENTER)
        patch = density_patch(color=BLUE).move_to(PATCH_CENTER)
        profile = bell_profile(color=BLUE)
        profile.next_to(patch, UP, buff=0.1)
        squashed = Line(
            PATCH_CENTER + LEFT * (PATCH_WIDTH / 2),
            PATCH_CENTER + RIGHT * (PATCH_WIDTH / 2),
            stroke_color=BLUE, stroke_width=1.0,
        ).set_opacity(0.0)
        mark_intended_overlap(grid, patch, profile, squashed,
                              reason="the lump grid melts into the gradient "
                                     "patch; the side-view bell profile "
                                     "squashes down onto it")
        # With the patch on the halfway rule the profile's bbox corner grazes
        # the mixed-partial formula's bbox corner; the actual ink is the
        # near-zero right tail hugging its baseline, ~0.5 units below the
        # formula (2026-07-05 draft review round 2).
        mark_intended_overlap(profile, mixed,
                              reason="bbox-only: the bell profile's flat "
                                     "right tail crosses the formula's bbox "
                                     "corner with no ink collision")
        bridge_cap = Text("the table becomes a surface",
                          font_size=CAPTION, color=MUTED)
        bridge_cap.next_to(patch, DOWN, buff=0.3)

        with self.voiceover(
            text="Now the picture to keep. When we built the joint PMF table, it stacked a lump of mass on each cell. Let the cells shrink and multiply, and the table melts into a surface: a height above every point of the plane, tall where the pair is likely, flat where it is not."
        ):
            self.play(FadeOut(rebuild), FadeOut(props), FadeOut(jc_note),
                      run_time=0.5)
            self.play(FadeIn(grid, shift=UP * 0.2), run_time=0.9)
            self.wait(0.6)
            self.play(Create(profile), run_time=0.8)
            self.play(
                FadeOut(grid),
                Transform(profile, squashed),
                FadeIn(patch),
                run_time=1.5,
            )
            self.remove(profile)
            self.play(FadeIn(bridge_cap), run_time=0.6)

        blob = Ellipse(width=1.5, height=0.95)
        blob.set_stroke(ACCENT, 3).set_fill(opacity=0.0)
        blob.rotate(0.5).move_to(patch.get_center() + RIGHT * 0.35 + UP * 0.25)
        s_lab = MathTex("S", font_size=SMALL, color=ACCENT)
        s_lab.move_to(blob.get_center())
        mark_intended_overlap(patch, blob, s_lab,
                              reason="the region S is outlined on the "
                                     "gradient density patch")
        # The full right-hand stack is laid out up front and centered on the
        # halfway rule, so the FINAL frame (with the rectangle integral in)
        # is what balances against the patch (2026-07-05 draft review
        # round 2, 3:38).
        vol = MathTex(
            pr(r"(X, Y) \in S"), "=",
            r"\iint_{S} f_{X,Y}(x, y)\, dy\, dx",
            font_size=SMALL,
        )
        vol_cap = Text("the volume under the surface, above S",
                       font_size=CAPTION, color=MUTED)
        vol_cap.next_to(vol, DOWN, buff=0.3)
        rect_int = MathTex(
            r"= \int_{a}^{b} \int_{c}^{d} f_{X,Y}(x, y)\, dy\, dx",
            font_size=SMALL,
        ).next_to(vol_cap, DOWN, buff=0.35)
        vol_stack = VGroup(vol, vol_cap, rect_int)
        fit_to_frame(vol_stack)
        vol_stack.move_to(RIGHT * 3.3 + UP * CONTENT_MID_Y)

        with self.voiceover(
            text='And probability becomes volume. The probability that the pair lands in a region S is the double integral of the density over S — the volume trapped under the surface, directly above the region.'
        ):
            self.play(Create(blob), FadeIn(s_lab), run_time=0.9)
            self.play(Write(vol), run_time=1.2)
            self.play(FadeIn(vol_cap), run_time=0.6)

        rect = Rectangle(width=1.6, height=1.0)
        rect.set_stroke(ACCENT, 3).set_fill(opacity=0.0)
        rect.move_to(blob.get_center())
        mark_intended_overlap(patch, rect,
                              reason="the rectangle S is outlined on the "
                                     "gradient density patch")

        with self.voiceover(
            text='When S is a rectangle, the volume is the familiar iterated integral: x from a to b, y from c to d.'
        ):
            self.play(Transform(blob, rect), run_time=0.8)
            self.play(Write(rect_int), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MarginalPDFs(VoiceoverScene):
    """Beat: marginal-pdfs -- row sums become integrals."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Marginal Densities")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The video-21 mirror: a joint table with one row lit, on screen
        # exactly while the discrete recipe is named.
        table = mass_table(NINTHS_TABLE)
        table.scale(0.85).move_to(PATCH_CENTER)
        for j in range(4):
            if table.cells[0][j] is not None:
                table.cells[0][j].set_color(MUTED)
        for i in range(1, 4):
            table.cells[i][0].set_color(MUTED)

        with self.voiceover(
            text="One variable at a time, again. The joint object answers every question, but often we want one variable's own distribution. In the discrete chapter, marginalizing meant summing a table's row; here the row is a slice of the surface."
        ):
            self.play(Create(table[0]), FadeIn(table[1]), run_time=1.0)
            row = VGroup(*[table.cells[2][j] for j in range(1, 4)])
            self.play(row.animate.set_color(ACCENT), run_time=0.7)

        # The SAME gradient patch as the previous beat -- same center, same
        # size -- so the two beats read as one object. The slice line runs
        # past the patch on both sides: the integral is over the whole line.
        patch = density_patch(color=BLUE).move_to(PATCH_CENTER)
        reach = PATCH_WIDTH / 2 + 0.7
        slice_line = Line(
            PATCH_CENTER + LEFT * reach + UP * 0.4,
            PATCH_CENTER + RIGHT * reach + UP * 0.4,
            color=ACCENT, stroke_width=3.5,
        )
        y_lab = MathTex("y", font_size=CAPTION, color=ACCENT)
        y_lab.next_to(slice_line.get_end(), RIGHT, buff=0.15)
        mark_intended_overlap(patch, slice_line, y_lab,
                              reason="the fixed-y slice line cuts across "
                                     "the gradient patch and extends past "
                                     "it on both sides")

        with self.voiceover(
            text="Fix a value of y and cut the surface along it. The slice's profile shows how the mass along that line is spread across x."
        ):
            self.play(FadeOut(table), run_time=0.5)
            self.play(FadeIn(patch, shift=UP * 0.2), run_time=0.8)
            self.play(Create(slice_line), FadeIn(y_lab), run_time=0.9)

        fy = MathTex(
            r"f_Y(y)", "=", r"\int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dx",
            font_size=BODY,
        ).move_to(RIGHT * 3.3 + DOWN * 0.4)
        fit_to_frame(fy)

        with self.voiceover(
            text='Integrate the slice over all of x, and the total is the marginal density of Y at that value. The row sum from the discrete joint-table video has become an integral: the marginal density of Y is the integral, over x, of the joint density. No new principle here — just the discrete recipe with the sum promoted to an integral.'
        ):
            self.play(slice_line.animate.set_color(INK),
                      y_lab.animate.set_color(INK), run_time=0.4)
            self.play(Write(fy), run_time=1.3)
            self.play(fy[0].animate.set_color(ACCENT), run_time=0.5)

        fx = MathTex(
            r"f_X(x)", "=", r"\int_{-\infty}^{\infty} f_{X,Y}(x, y)\, dy",
            font_size=SMALL,
        ).next_to(fy, DOWN, buff=0.45)
        warn = Text("the joint determines the marginals, not conversely",
                    font_size=CAPTION, color=MUTED)
        warn.next_to(fx, DOWN, buff=0.4)

        with self.voiceover(
            text='Symmetrically, integrating out y leaves the marginal density of X. And the old warning carries over word for word: the joint determines the marginals, but not conversely. Just as two different tables shared identical margins, two different surfaces can cast identical shadows.'
        ):
            self.play(fy[0].animate.set_color(INK), run_time=0.3)
            self.play(Write(fx), run_time=1.0)
            self.play(FadeIn(warn, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class UnitCircleExample(VoiceoverScene):
    """Beat: unit-circle -- the flat disk, then the Gaussian pair and Rayleigh."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Two Worked Examples")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text='Time to run the machine, twice. First, the flattest surface there is.'
        ):
            self.wait(0.3)

        # Halfway rule (2026-07-05 draft review round 3, 5:41 + 6:05): both
        # density images center on CONTENT_MID_Y, like the earlier beats.
        disk_center = LEFT * 3.4 + UP * CONTENT_MID_Y
        # Uniform on the disk: a FLAT image with a SHARP boundary -- constant
        # intensity inside the support, hard cutoff at the circle's edge
        # (the uniform density is discontinuous there; 2026-07-05 draft
        # review round 3, 5:41), no outline.
        unit_disk = density_patch(color=BAR, width=3.0, kind="flat",
                                  peak=0.55).move_to(disk_center)
        f_disk = MathTex(
            r"f_{X,Y}(x, y) = \begin{cases} \frac{1}{\pi} &"
            r" x^2 + y^2 \leq 1 \\[2pt] 0 & \text{otherwise} \end{cases}",
            font_size=SMALL,
        ).move_to(RIGHT * 3.3 + UP * 0.7)
        fit_to_frame(f_disk)

        with self.voiceover(
            text='Let the pair be uniform on the unit circle: the density is one over pi inside the disk and zero outside — constant height, total volume one.'
        ):
            self.play(FadeIn(unit_disk), run_time=0.8)
            self.play(Write(f_disk), run_time=1.2)

        inner = Circle(radius=0.75, color=ACCENT, stroke_width=3)
        inner.set_fill(ACCENT, opacity=0.15).move_to(disk_center)
        inner_lab = MathTex("S", font_size=SMALL, color=ACCENT)
        inner_lab.move_to(disk_center)
        mark_intended_overlap(unit_disk, inner, inner_lab,
                              reason="the radius-one-half disk sits inside "
                                     "the unit disk")
        quarter = MathTex(
            pr(r"(X, Y) \in S"), "=",
            r"\frac{1}{\pi} \cdot \pi \left(\tfrac{1}{2}\right)^{2}",
            "=", r"\tfrac{1}{4}",
            font_size=SMALL,
        ).next_to(f_disk, DOWN, buff=0.55)
        fit_to_frame(quarter)

        with self.voiceover(
            text='What is the probability of landing within radius one half? Volume above the small disk: a constant height times its area. The small disk holds one quarter of the area, so the probability is one quarter. Under a flat density, probability is literally area.'
        ):
            self.play(Create(inner), FadeIn(inner_lab), run_time=0.9)
            self.play(Write(quarter), run_time=1.3)

        self.play(FadeOut(unit_disk), FadeOut(inner), FadeOut(inner_lab),
                  FadeOut(f_disk), FadeOut(quarter), run_time=0.6)

        # The Gaussian pair: the same smooth-gradient treatment, in TEAL.
        bell = density_patch(color=TEAL).move_to(disk_center)
        f_gauss = MathTex(
            r"f_{X,Y}(x, y) = \frac{1}{2\pi\sigma^2}\,"
            r" e^{-\frac{x^2 + y^2}{2\sigma^2}}",
            font_size=SMALL,
        ).move_to(RIGHT * 3.3 + UP * 0.8)
        fit_to_frame(f_gauss)

        with self.voiceover(
            text='Now a curved surface. Take two independent zero-mean Gaussians with the same variance sigma squared. Their joint density is the bell curve spun into a two-dimensional Gaussian density — tallest at the origin, falling with the squared distance from it.'
        ):
            self.play(FadeIn(bell, shift=UP * 0.2), run_time=0.9)
            self.play(Write(f_gauss), run_time=1.2)

        s_circle = Circle(radius=0.5, color=ACCENT, stroke_width=3)
        s_circle.move_to(disk_center)
        mark_intended_overlap(bell, s_circle,
                              reason="the radius-s circle grows over the "
                                     "Gaussian gradient patch")
        r_def = MathTex(r"R = \sqrt{X^2 + Y^2}",
                        font_size=SMALL, color=MUTED)
        r_def.next_to(f_gauss, DOWN, buff=0.45)
        pr_s = MathTex(
            pr(r"R \leq s"), "=", r"1 - e^{-\frac{s^2}{2\sigma^2}}",
            font_size=SMALL,
        ).next_to(r_def, DOWN, buff=0.35)
        fit_to_frame(pr_s)

        with self.voiceover(
            text='Ask for the probability that the point lands within distance s of the origin. Switch the double integral to polar coordinates and it collapses, leaving one minus e to the minus s squared over two sigma squared.'
        ):
            self.play(Create(s_circle), FadeIn(r_def), run_time=0.8)
            self.play(s_circle.animate.scale(2.3), run_time=1.2)
            self.play(Write(pr_s), run_time=1.1)

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 0.7, 0.35],
            x_length=4.6, y_length=2.3,
            axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        )
        # Halfway rule (2026-07-05 draft review round 3, 6:38): the Rayleigh
        # plot centers on CONTENT_MID_Y like the density images before it.
        axes.move_to(LEFT * 3.3 + UP * CONTENT_MID_Y)
        curve = axes.plot(lambda s: s * np.exp(-s * s / 2.0),
                          x_range=[0, 4], color=BAR)
        mark_intended_overlap(axes, curve,
                              reason="the density curve rises from the axis")
        curve_cap = Text("the Rayleigh density", font_size=CAPTION,
                         color=MUTED)
        curve_cap.next_to(axes, DOWN, buff=0.25)
        f_r = MathTex(
            r"f_R(s)", "=", r"\frac{s}{\sigma^2}\, e^{-\frac{s^2}{2\sigma^2}}",
            font_size=BODY,
        ).next_to(pr_s, DOWN, buff=0.5)
        fit_to_frame(f_r)

        with self.voiceover(
            text='Look at what that is: the CDF of the distance R itself. Differentiate once, and R has the Rayleigh density — s over sigma squared, times e to the minus s squared over two sigma squared. The Rayleigh entered the course as a catalog entry; the joint density just derived it.'
        ):
            self.play(FadeOut(bell), FadeOut(s_circle), run_time=0.5)
            self.play(Create(axes), run_time=0.6)
            self.play(Create(curve), FadeIn(curve_cap), run_time=1.0)
            self.play(Write(f_r), run_time=1.2)
            self.play(f_r[0].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["One joint CDF carries the pair; differentiate twice,",
             "and probability is volume under a density surface."],
            next_title="Conditioning with Densities",
        )

        with self.voiceover(
            text='The key idea of this video: one joint CDF carries a pair of continuous variables — differentiate it twice, and probability becomes volume under a density surface.'
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
