# derived_from: content/43-central-limit-script.md
# derived_from_sha256: c145db5c2b98baa8f369431d31d3d8a3c7a780702cd851e5ed2dee6f44b8ae26
"""Chapter 12, Video 3 -- The Central Limit Theorem (series finale).

Source notes : empirical_sums.tex (Section "The Central Limit Theorem" +
               "Normal Approximation" subsection) -- the theorem, the
               log-MGF proof (E[X]=0, sigma^2=1, MGF exists; pointwise MGF
               convergence -> convergence in distribution quoted without
               proof), and the Phi approximation of large-sum CDFs.
Script        : content/43-central-limit-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Series finale: the outro closes the arc (no "coming up" line); the course's
one deliberate "bell curve" is spent on the closing card.

Draft render:
    uv run manim -pql scenes/central_limit.py ChapterOverview
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
    expectation,
    variance,
    section_title,
    axis_label_x,
    intro_card,
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


def gauss(u):
    """The standard Gaussian density."""
    return math.exp(-u * u / 2) / math.sqrt(2 * math.pi)


def eq_chain(first, *rest, eq_index=1, buff=0.30):
    """Stack continuation ("=", rhs) lines under `first`.

    Each continuation line's leading part (its "=" or "approx" sign) is
    x-aligned with part [eq_index] of the first line, so the chain reads as
    one derivation (the two-line-equation house rule). Returns the VGroup.
    """
    group = VGroup(first)
    anchor_x = first[eq_index].get_x()
    prev = first
    for line in rest:
        line.next_to(prev, DOWN, buff=buff)
        line.shift(RIGHT * (anchor_x - line[0].get_x()))
        group.add(line)
        prev = line
    return group


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Central Limit Theorem",
            ["Standardize a large iid sum, and every finite-variance",
             "distribution flows to the standard normal."],
            kicker="Chapter 12  ·  Limit Theorems",
        )
        tag = progress_tag(3, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The theorem", font_size=BODY, color=INK),
            # (2026-07-05 draft review round 2, honest framing) the video
            # builds the intuition; it does not prove the CLT.
            Text("2.  The intuition: sums become products",
                 font_size=BODY, color=INK),
            Text("3.  The normal approximation", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # (2026-07-05 draft review round 3) register: vanish, not die.
        with self.voiceover(
            text="Last video, the law of large numbers: divide a sum of "
                 "independent, identically distributed variables by n, and "
                 "the empirical average settles onto the mean. The "
                 "fluctuations vanish."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)

        # (2026-07-05 draft review, 0:20) production-finality claim removed:
        # the human may make more videos later.
        with self.voiceover(
            text="This video zooms in. Divide "
                 "by the square root of n instead, and the fluctuations do "
                 "not vanish — they stabilize into a definite shape."
        ):
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(outline)

        with self.voiceover(
            text="First, the central limit theorem: what that shape is, and "
                 "why the starting distribution does not matter."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        # (2026-07-05 draft review round 2, honest framing) "the proof" ->
        # "the intuition": the key MGF-convergence step is quoted, not proved.
        with self.voiceover(
            text="Then the intuition, built through the moment-generating "
                 "function, where sums become products."
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="And finally the payoff: the normal approximation, which "
                 "estimates any large sum with a single table. When we first "
                 "met the Gaussian, we promised that many small independent "
                 "effects would explain it. This is where the promise is "
                 "kept."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CLTStatement(VoiceoverScene):
    """Beat: clt-statement -- the standardized sum, the theorem, any start."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Central Limit Theorem")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        setup = MathTex(r"S_n = X_1 + \cdots + X_n", font_size=BODY)
        setup.next_to(title, DOWN, buff=0.5)
        conds = MathTex(
            expectation("X_i") + r"= \mathrm{E}[X],\qquad "
            + variance("X_i") + r"= \sigma^2",
            font_size=BODY,
        ).next_to(setup, DOWN, buff=0.3)

        with self.voiceover(
            text="Here is the statement. Take independent, identically "
                 "distributed random variables with mean E of X and variance "
                 "sigma squared, and form the sum S n."
        ):
            self.play(Write(setup), run_time=0.9)
            self.play(Write(conds), run_time=1.0)

        zdef = MathTex(r"\frac{S_n - n\,\mathrm{E}[X]}{\sigma\sqrt{n}}",
                       font_size=BODY)
        zdef.next_to(conds, DOWN, buff=0.5)
        znote = MathTex(
            r"\text{mean } 0, \ \text{variance } 1, \ \text{for every } n",
            font_size=SMALL, color=MUTED,
        ).next_to(zdef, DOWN, buff=0.3)

        with self.voiceover(
            text="Center the sum by subtracting n times the mean, and scale "
                 "it by sigma times the square root of n. This standardized "
                 "sum has mean zero and variance one, for every n. The "
                 "centering removes the drift; the root n scaling holds the "
                 "spread steady."
        ):
            self.play(Write(zdef), run_time=1.1)
            self.play(zdef.animate.set_color(ACCENT), run_time=0.4)
            self.play(FadeIn(znote), run_time=0.6)

        th1 = MathTex(
            r"\lim_{n \to \infty}",
            pr(r"\frac{S_n - n\,\mathrm{E}[X]}{\sigma\sqrt{n}} \le x"),
            font_size=BODY,
        )
        th2 = MathTex(
            "=", r"\int_{-\infty}^{x} \frac{1}{\sqrt{2\pi}}\, e^{-u^2/2}\, du",
            font_size=BODY,
        )
        # (2026-07-05 draft review, 1:35) the continuation line is CENTERED
        # under the first, a balanced two-line group (the eq_chain anchor
        # pushed it far right); the same form rides into the docked column.
        th2.next_to(th1, DOWN, buff=0.32)
        th2.match_x(th1)
        theorem = VGroup(th1, th2)
        theorem.next_to(znote, DOWN, buff=0.45)
        fit_to_frame(theorem)

        with self.voiceover(
            text="The central limit theorem says: as n grows, the "
                 "probability that the standardized sum lands at or below "
                 "any x converges to the integral of the standard Gaussian "
                 "density up to x. The standardized sum converges in "
                 "distribution — the very notion we defined for CDFs — to a "
                 "standard normal random variable."
        ):
            self.play(zdef.animate.set_color(INK), run_time=0.4)
            self.play(Write(th1), run_time=1.2)
            self.play(Write(th2), run_time=1.1)
            self.play(th2[1].animate.set_color(ACCENT), run_time=0.5)

        # Any starting shape: chart left, formulas dock right — both columns
        # centered on the halfway anchor (2026-07-05 draft review, 2:00).
        zc = zone_center_y(title)
        axes = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[0, 0.6, 0.3],
            x_length=5.6, y_length=2.8, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        )
        xlab = axis_label_x(axes, MathTex("u", font_size=CAPTION,
                                          color=MUTED), buff=0.25)
        chart = VGroup(axes, xlab)
        chart.move_to([-3.4, 0.0, 0.0])
        cap = Text("start anywhere", font_size=CAPTION, color=MUTED)
        cap.next_to(chart, DOWN, buff=0.35)
        cap.match_x(axes)
        # Figure + caption travel as one block to the halfway anchor.
        block = VGroup(chart, cap)
        block.shift(UP * (zc - block.get_center()[1]))
        cap2 = Text("the same limit, every time",
                    font_size=CAPTION, color=MUTED)
        cap2.move_to(cap)
        cap2.match_x(axes)

        flat = axes.plot(lambda u: 0.2887,
                         x_range=[-1.732, 1.732]).set_stroke(BAR, 3)
        # (2026-07-05 draft review, 2:00) the uniform density is visibly
        # zero outside its support: zero-level segments on the x-axis and
        # dashed vertical lines at the support's edges.
        flat_zero = VGroup(
            axes.plot(lambda u: 0.0,
                      x_range=[-3.5, -1.732]).set_stroke(BAR, 3),
            axes.plot(lambda u: 0.0,
                      x_range=[1.732, 3.5]).set_stroke(BAR, 3),
        )
        flat_edges = VGroup(*[
            DashedLine(axes.c2p(u, 0), axes.c2p(u, 0.2887),
                       color=BAR, stroke_width=2.5, dash_length=0.1)
            for u in (-1.732, 1.732)
        ])
        # A lopsided mean-0, variance-1 shape (shifted Gamma(2, 1/sqrt 2)).
        skew = axes.plot(
            lambda u: 2.0 * (u + 1.414)
            * math.exp(-(u + 1.414) / 0.707),
            x_range=[-1.414, 3.5]).set_stroke(BAR, 3)
        normal = axes.plot(gauss, x_range=[-3.5, 3.5]).set_stroke(ACCENT, 3)
        mark_intended_overlap(
            axes, flat, flat_zero, flat_edges, skew, normal,
            reason="the densities are drawn on their shared axes")

        formulas = VGroup(zdef, theorem)

        with self.voiceover(
            text="Now hear what the theorem does not ask. It does not ask "
                 "where you start. Begin with a flat distribution,"
        ):
            self.play(FadeOut(setup), FadeOut(conds), FadeOut(znote),
                      th2[1].animate.set_color(INK), run_time=0.5)
            self.play(formulas.animate.scale(0.8)
                      .move_to([3.4, zc, 0.0]), run_time=0.8)
            self.play(Create(axes), Write(xlab), run_time=0.7)
            curve = flat
            self.play(Create(curve), Create(flat_zero),
                      Create(flat_edges), FadeIn(cap), run_time=0.8)

        with self.voiceover(
            text="or a lopsided one,"
        ):
            self.play(Transform(curve, skew), FadeOut(flat_zero),
                      FadeOut(flat_edges), run_time=0.9)

        with self.voiceover(
            text="standardize the sum, and the limit is the same standard "
                 "normal, every time. Only the mean and the variance "
                 "survive; every other detail of the starting distribution "
                 "is forgotten in the limit. That is why the Gaussian is "
                 "everywhere: it is the shape large sums cannot avoid."
        ):
            self.play(Transform(curve, normal),
                      Transform(cap, cap2), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GaussianExact(VoiceoverScene):
    """Beat: gaussian-exact -- for Gaussian inputs the scaling is exact."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Gaussian Case Is Exact")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        setup = MathTex(
            r"X_i \ \text{Gaussian:}\quad "
            + expectation("X_i") + r"= m,\quad "
            + variance("X_i") + r"= \sigma^2",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)

        # (2026-07-05 draft review, 2:30-2:55) the destination shape is on
        # screen while it is discussed: the Gaussian density sits at the
        # bottom CENTER through the setup, then slides LEFT into the
        # invariant chart's placement when the mean/variance need the room
        # (2:58) — the n-tag waits until the count becomes needed.
        axes = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 0.25],
            x_length=5.4, y_length=2.6, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        )
        xlab = axis_label_x(axes, MathTex("u", font_size=CAPTION,
                                          color=MUTED), buff=0.25)
        chart = VGroup(axes, xlab)
        chart.move_to(LEFT * 3.4)
        chart.to_edge(DOWN, buff=1.35)
        curve = axes.plot(gauss, x_range=[-3.5, 3.5]).set_stroke(BAR, 3)
        nlab_pos = axes.c2p(2.4, 0.40)  # saved at the FINAL placement
        cap = Text("the curve never moves", font_size=CAPTION, color=MUTED)
        cap.next_to(chart, DOWN, buff=0.35)
        cap.match_x(axes)
        gblock = VGroup(chart, curve)
        gblock.shift(RIGHT * 3.4)  # bottom center first; slides left later

        with self.voiceover(
            text="One case we can check completely. Suppose every X i is "
                 "itself Gaussian, with mean m and variance sigma squared, "
                 "drawn fresh and independent every time. No limits yet — "
                 "just bookkeeping we already own."
        ):
            self.play(Write(setup), run_time=1.2)
            self.play(Create(axes), Write(xlab), run_time=0.6)
            self.play(Create(curve), run_time=0.8)

        stmt = MathTex(
            r"\frac{S_n - nm}{\sqrt{n}}",
            r"\ \text{ is Gaussian for every } n",
            font_size=BODY,
        ).next_to(setup, DOWN, buff=0.5)
        fit_to_frame(stmt)

        with self.voiceover(
            text="When we convolved densities, we learned that sums of "
                 "independent Gaussians stay Gaussian — so S n minus n m, "
                 "over the square root of n, is Gaussian for every n."
        ):
            self.play(Write(stmt), run_time=1.2)
            self.play(stmt[0].animate.set_color(ACCENT), run_time=0.4)

        # (2026-07-05 draft review, 2:58) the mean and the variance each on
        # ONE LINE — the vertical space reclaimed — and the right block ends
        # the frame centered on the halfway anchor.
        zc = zone_center_y(title)
        m1 = MathTex(
            r"\mathrm{E}\!\left[ \frac{S_n - nm}{\sqrt{n}} \right]", "=",
            r"\frac{\mathrm{E}\!\left[ S_n - nm \right]}{\sqrt{n}} = 0",
            font_size=SMALL,
        )
        v1 = MathTex(
            r"\mathrm{Var}\!\left( \frac{S_n - nm}{\sqrt{n}} \right)", "=",
            r"\frac{\mathrm{Var}\!\left( S_n \right)}{n}"
            r" = \frac{n \sigma^2}{n} =", r"\sigma^2",
            font_size=SMALL,
        )
        chains = VGroup(m1, v1)
        chains.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        if chains.width > 6.0:
            chains.scale(6.0 / chains.width)
        chains.move_to([3.4, zc, 0.0])
        fit_to_frame(chains)

        with self.voiceover(
            text="Compute its mean: the centering makes it zero. Compute "
                 "its variance: the n independent variances add to n sigma "
                 "squared, and dividing by root n divides the variance by "
                 "n. What remains is sigma squared, with no n anywhere in "
                 "sight."
        ):
            self.play(stmt[0].animate.set_color(INK), run_time=0.4)
            self.play(gblock.animate.shift(LEFT * 3.4), run_time=0.8)
            self.play(Write(m1), run_time=1.2)
            self.play(Write(v1), run_time=1.3)
            self.play(v1[3].animate.set_color(ACCENT), run_time=0.4)

        # The invariant curve: the chart is already in place; the n-label
        # (BODY) arrives only now, when the count becomes needed.
        nlab = MathTex(r"n = 1", font_size=BODY, color=INK)
        nlab.move_to(nlab_pos)
        mark_intended_overlap(
            axes, curve, nlab,
            reason="the invariant density and its n-label share the axes")

        with self.voiceover(
            text="So for Gaussian inputs the scaled sum does not merely "
                 "converge — it is the same distribution at every single n. "
                 "The curve never moves. This is the invariant sequence we "
                 "met when we defined convergence in distribution, and the "
                 "central limit theorem is the claim that every "
                 "finite-variance input flows to the shape the Gaussian "
                 "already occupies."
        ):
            self.play(v1[3].animate.set_color(INK),
                      curve.animate.set_stroke(ACCENT, 3), run_time=0.4)
            self.play(Write(nlab), run_time=0.7)
            self.play(FadeIn(cap), run_time=0.5)
            for n_txt in ("n = 2", "n = 8", "n = 32"):
                new_lab = MathTex(n_txt, font_size=BODY, color=INK)
                new_lab.move_to(nlab)
                mark_intended_overlap(
                    new_lab, axes, curve,
                    reason="the invariant density and its n-label share "
                           "the axes")
                self.play(Transform(nlab, new_lab), run_time=0.5)
            self.play(Indicate(curve, color=ACCENT, scale_factor=1.03),
                      run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MGFProof(VoiceoverScene):
    """Beat: mgf-proof -- log-MGF, sums become products, the s^2/2 limit."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Log-MGF")
        fit_to_frame(title)

        # (2026-07-05 draft review round 2, honest framing) "prove" ->
        # "build the intuition": this beat sketches the argument; the
        # MGF-to-distribution step stays unproved (stated below).
        with self.voiceover(
            text="How do you build the intuition that every distribution "
                 "flows to the same limit? Not through the density — "
                 "through the transform."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        assume = VGroup(
            MathTex(expectation("X") + r"= 0,\qquad "
                    + variance("X") + r"= 1",
                    font_size=BODY, color=INK),
            MathTex(r"M_X(s)\ \text{exists and is finite}",
                    font_size=BODY, color=MUTED),
        ).arrange(DOWN, buff=0.3)
        assume.next_to(title, DOWN, buff=0.45)

        with self.voiceover(
            text="Assume the mean is zero and the variance is one; proper "
                 "scaling recovers the general case. Assume too that the "
                 "moment-generating function of X exists and is finite."
        ):
            self.play(Write(assume[0]), run_time=1.0)
            self.play(FadeIn(assume[1]), run_time=0.7)

        lam = MathTex(
            r"\Lambda_X(s)", "=", r"\log M_X(s)", "=",
            r"\log " + expectation(r"e^{sX}"),
            font_size=BODY,
        ).next_to(assume, DOWN, buff=0.5)
        fit_to_frame(lam)

        with self.voiceover(
            text="Our tool is its logarithm: capital Lambda of s, the log "
                 "of the expectation of e to the s X."
        ):
            self.play(Write(lam), run_time=1.2)
            self.play(lam[0].animate.set_color(ACCENT), run_time=0.4)

        vals = VGroup(
            MathTex(r"\Lambda_X(0) = 0", font_size=SMALL),
            MathTex(r"\Lambda_X'(0) = \mathrm{E}[X] = 0", font_size=SMALL),
            MathTex(r"\Lambda_X''(0) = \mathrm{E}\!\left[ X^2 \right] = 1",
                    font_size=SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        vals.next_to(lam, DOWN, buff=0.45)
        # (2026-07-05 draft review, 4:26) the takeaway line: the label
        # "Near the origin:" + the equation, at the SAME size and spacing
        # as the Lambda_X(s) line above the three conditions, equation in
        # ACCENT (lam's accent was demoted above, so it stands alone).
        near = MathTex(
            r"\text{Near the origin:}",
            r"\quad \Lambda_X(s) \approx \tfrac{s^2}{2}",
            font_size=BODY,
        ).next_to(vals, DOWN, buff=0.45)
        near[0].set_color(INK)
        near[1].set_color(ACCENT)
        fit_to_frame(near)

        # (2026-07-05 draft review, 4:26) spoken "Zero, zero, one:" recap
        # removed — the three values were each just said once above.
        with self.voiceover(
            text="Three numbers pin this curve near the origin. At zero, "
                 "Lambda is the log of one: zero. Its first derivative at "
                 "zero is the mean: zero. Its second derivative at zero is "
                 "the second moment: one. Near the origin, "
                 "Lambda hugs the parabola s squared over two, and that is "
                 "the whole secret."
        ):
            self.play(lam[0].animate.set_color(INK), run_time=0.4)
            self.play(Write(vals[0]), run_time=0.7)
            self.play(Write(vals[1]), run_time=0.7)
            self.play(Write(vals[2]), run_time=0.7)
            self.play(FadeIn(near), run_time=0.7)

        # --- Sums become products (sequential section title) -------------
        p1 = MathTex(
            r"\log \mathrm{E}\!\left[ e^{s S_n/\sqrt{n}} \right]", "=",
            r"\log\!\left( M_X\!\left( \tfrac{s}{\sqrt{n}} \right)"
            r" \cdots M_X\!\left( \tfrac{s}{\sqrt{n}} \right) \right)",
            font_size=BODY,
        )
        p2 = MathTex("=", r"n\, \Lambda_X\!\left( s\, n^{-1/2} \right)",
                     font_size=BODY)
        pchain = eq_chain(p1, p2, eq_index=1, buff=0.32)
        fit_to_frame(pchain)
        pcap = MathTex(
            r"\text{one function of one variable, } n \text{ copies}",
            font_size=CAPTION, color=MUTED,
        )

        with self.voiceover(
            text="Now bring in the sum. Independence means the expectation "
                 "of a product factors — the generating-function move we "
                 "have used twice before. The log-MGF of S n over root n "
                 "collapses into n identical factors: n times Lambda of s "
                 "over root n. One function of one variable controls the "
                 "entire sum."
        ):
            new_title = section_title("Sums Become Products").to_edge(UP)
            self.play(Transform(title, new_title),
                      FadeOut(assume), FadeOut(lam), FadeOut(vals),
                      FadeOut(near), run_time=0.7)
            pchain.next_to(title, DOWN, buff=0.7)
            pcap.next_to(pchain, DOWN, buff=0.4)
            self.play(Write(p1), run_time=1.4)
            self.play(Write(p2), run_time=0.9)
            self.play(p2[1].animate.set_color(ACCENT),
                      FadeIn(pcap), run_time=0.6)

        # --- The limit (sequential section title) -------------------------
        c1 = MathTex(
            r"\lim_{n \to \infty}"
            r" \frac{\Lambda_X\!\left( s\, n^{-1/2} \right)}{n^{-1}}", "=",
            r"\frac{s}{2} \lim_{n \to \infty}"
            r" \frac{\Lambda_X'\!\left( s\, n^{-1/2} \right)}{n^{-1/2}}",
            font_size=SMALL,
        )
        # (2026-07-05 draft review, 5:00) the cascade on TWO lines: the
        # second line carries the s^2/2 term and is CENTERED under the
        # first, so the derivation reads as one balanced group.
        c2 = MathTex(
            "=", r"\frac{s^2}{2} \lim_{n \to \infty}"
            r" \Lambda_X''\!\left( s\, n^{-1/2} \right) =", r"\frac{s^2}{2}",
            font_size=SMALL,
        )
        c2.next_to(c1, DOWN, buff=0.26)
        c2.match_x(c1)
        cascade = VGroup(c1, c2)
        if cascade.width > 6.0:
            cascade.scale(6.0 / cascade.width)
        cascade.move_to(RIGHT * 3.2 + DOWN * 0.8)

        with self.voiceover(
            text="What happens as n grows? Write it as Lambda over one "
                 "over n, and apply L'Hopital's rule — twice. Each pass "
                 "peels one derivative off Lambda, until the second "
                 "derivative at zero, which is one, stands exposed. The "
                 "limit is s squared over two."
        ):
            new_title = section_title("The Limit Is the Gaussian's")
            fit_to_frame(new_title)
            new_title.to_edge(UP)
            self.play(Transform(title, new_title),
                      FadeOut(pchain), FadeOut(pcap), run_time=0.7)
            self.play(Write(c1), run_time=1.3)
            self.play(Write(c2), run_time=1.2)
            self.play(c2[2].animate.set_color(ACCENT), run_time=0.4)

        # Transform-space picture: n Lambda(s/sqrt n) settling on s^2/2.
        axes = Axes(
            x_range=[-2, 2, 1], y_range=[0, 2.2, 1],
            x_length=5.0, y_length=2.7, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
        )
        xlab = axis_label_x(axes, MathTex("s", font_size=CAPTION,
                                          color=MUTED), buff=0.25)
        chart = VGroup(axes, xlab)
        chart.move_to(LEFT * 3.5)
        chart.to_edge(DOWN, buff=1.35)

        parab = axes.plot(lambda s: s * s / 2,
                          x_range=[-2, 2]).set_stroke(ACCENT, 3)
        plab = MathTex(r"\tfrac{s^2}{2}", font_size=SMALL, color=ACCENT)
        plab.move_to(axes.c2p(1.55, 1.95))
        ncurves = VGroup(*[
            axes.plot(lambda s, nn=n: nn * math.log(
                math.cosh(s / math.sqrt(nn))),
                x_range=[-2, 2]).set_stroke(MUTED, 2.5)
            for n in (1, 4, 16)
        ])
        legend = MathTex(r"n = 1,\ 4,\ 16", font_size=SMALL, color=MUTED)
        legend.move_to(axes.c2p(-1.15, 1.9))
        mark_intended_overlap(
            axes, parab, plab, ncurves, legend,
            reason="the n-curves settle onto the parabola on shared axes")
        pcap2 = Text("the curves settle onto the parabola",
                     font_size=CAPTION, color=MUTED)
        pcap2.next_to(chart, DOWN, buff=0.35)
        pcap2.match_x(axes)
        # (2026-07-05 draft review, 5:19) figure + caption move as ONE
        # block to the halfway anchor of the content zone.
        pblock = VGroup(chart, parab, plab, ncurves, legend, pcap2)
        pblock.shift(UP * (zone_center_y(title) - pblock.get_center()[1]))

        with self.voiceover(
            text="Watch it happen: as n grows, the curves settle onto the "
                 "parabola."
        ):
            self.play(c2[2].animate.set_color(INK), run_time=0.3)
            self.play(Create(axes), Write(xlab), run_time=0.6)
            self.play(Create(parab), Write(plab), run_time=0.7)
            self.play(LaggedStart(*[Create(c) for c in ncurves],
                                  lag_ratio=0.35),
                      FadeIn(legend), run_time=1.4)
            self.play(FadeIn(pcap2), run_time=0.4)

        result = MathTex(
            r"M_{S_n/\sqrt{n}}(s)", r"\ \longrightarrow\ ", r"e^{s^2/2}",
            font_size=BODY,
        ).move_to(RIGHT * 3.2 + UP * 0.3)
        # (2026-07-05 draft review, 5:39) the ": quoted without proof" tail
        # is gone from the caption; the narration states it once, plainly.
        quote = VGroup(
            Text("pointwise MGF convergence implies",
                 font_size=CAPTION, color=MUTED),
            Text("convergence in distribution",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.15)
        quote.next_to(result, DOWN, buff=0.45)
        fit_to_frame(VGroup(result, quote))

        with self.voiceover(
            text="So the MGF of the scaled sum converges pointwise to e to "
                 "the s squared over two — precisely the moment-generating "
                 "function of a standard normal. That pointwise convergence "
                 "of MGFs forces convergence in distribution: a "
                 "sophisticated result we state without proof."
        ):
            self.play(FadeOut(cascade),
                      parab.animate.set_stroke(INK, 3),
                      plab.animate.set_color(INK), run_time=0.5)
            self.play(Write(result), run_time=1.0)
            self.play(result[2].animate.set_color(ACCENT), run_time=0.4)
            self.play(FadeIn(quote), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class NormalApproximation(VoiceoverScene):
    """Beat: normal-approximation -- Phi as the everyday tool + finale."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Normal Approximation")
        fit_to_frame(title)

        with self.voiceover(
            text="The theorem earns its keep as a calculator."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        setup = MathTex(
            r"S_n = X_1 + \cdots + X_n,\qquad "
            + expectation("X") + r"\ \text{and}\ \sigma^2\ \text{known},"
            r"\qquad n\ \text{large}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(setup)

        with self.voiceover(
            text="Take any large iid sum — n is large, and the mean and "
                 "variance are known."
        ):
            self.play(Write(setup), run_time=1.1)

        f1 = MathTex(r"F_{S_n}(x)", "=", pr(r"S_n \le x"), font_size=BODY)
        f2 = MathTex(
            "=",
            pr(r"\frac{S_n - n\,\mathrm{E}[X]}{\sigma\sqrt{n}}"
               r" \le \frac{x - n\,\mathrm{E}[X]}{\sigma\sqrt{n}}"),
            font_size=BODY,
        )
        f3 = MathTex(
            r"\approx",
            r"\Phi\!\left( \frac{x - n\,\mathrm{E}[X]}{\sigma\sqrt{n}}"
            r" \right)",
            font_size=BODY,
        )
        chain = eq_chain(f1, f2, f3, eq_index=1, buff=0.34)
        chain.next_to(setup, DOWN, buff=0.5)
        fit_to_frame(chain)

        with self.voiceover(
            text="The CDF of S n at x is the probability that S n is at "
                 "most x. Standardize both sides of the inequality, and the "
                 "left side is, by the theorem, approximately a standard "
                 "normal."
        ):
            self.play(Write(f1), run_time=0.9)
            self.play(Write(f2), run_time=1.2)

        tablecap = MathTex(
            r"\text{one table of } \Phi \text{ serves every large sum}",
            font_size=CAPTION, color=MUTED,
        ).next_to(chain, DOWN, buff=0.4)

        with self.voiceover(
            text="So the CDF of the sum is approximately capital Phi, the "
                 "standard normal CDF, evaluated at x minus n times the "
                 "mean, over sigma root n. One table of Phi serves every "
                 "large sum with finite variance."
        ):
            self.play(Write(f3), run_time=1.0)
            self.play(f3[1].animate.set_color(ACCENT),
                      FadeIn(tablecap), run_time=0.6)

        # Worked run: 100 fair bits, at most 55 ones.
        e1 = MathTex(r"n = 100,\qquad " + pr(r"X_i = 1") + r"= \tfrac{1}{2}",
                     font_size=BODY)
        e2 = MathTex(r"n\,\mathrm{E}[X] = 50,\qquad \sigma\sqrt{n} = 5",
                     font_size=BODY)
        g1 = MathTex(pr(r"S_{100} \le 55"), r"\approx",
                     r"\Phi\!\left( \tfrac{55 - 50}{5} \right)",
                     font_size=SMALL)
        g2 = MathTex("=", r"\Phi(1)", font_size=SMALL)
        g3 = MathTex(r"\approx", r"0.84", font_size=SMALL)
        gchain = eq_chain(g1, g2, g3, eq_index=1, buff=0.26)
        column = VGroup(VGroup(e1, e2).arrange(DOWN, aligned_edge=LEFT,
                                               buff=0.3),
                        gchain).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        column.move_to(RIGHT * 3.3 + DOWN * 0.4)
        fit_to_frame(column)

        with self.voiceover(
            text="A concrete run. A transmitter sends one hundred bits, "
                 "each equally likely to be zero or one, independently. "
                 "What is the probability that at most fifty-five are ones? "
                 "The mean count is fifty; sigma root n is five. "
                 "Standardize: fifty-five minus fifty, over five, is one."
        ):
            self.play(FadeOut(setup), FadeOut(chain), FadeOut(tablecap),
                      run_time=0.5)
            self.play(Write(e1), run_time=1.0)
            self.play(Write(e2), run_time=0.9)
            self.play(Write(g1), run_time=1.0)
            self.play(Write(g2), run_time=0.6)

        # The probability, seen: shade the area exactly as it is spoken.
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.45, 0.2],
            x_length=5.4, y_length=2.6, tips=False,
            axis_config={"include_numbers": False, "stroke_color": MUTED},
            x_axis_config={"include_numbers": True, "font_size": 30,
                           "numbers_to_include": [-2, 0, 1, 2]},
        )
        xlab = axis_label_x(axes, MathTex("u", font_size=CAPTION,
                                          color=MUTED), buff=0.25)
        chart = VGroup(axes, xlab)
        chart.move_to(LEFT * 3.4)
        chart.to_edge(DOWN, buff=1.35)

        curve = axes.plot(gauss, x_range=[-4, 4]).set_stroke(INK, 3)
        area = axes.get_area(curve, x_range=[-4, 1],
                             color=ACCENT, opacity=0.3)
        vline = DashedLine(axes.c2p(1, 0), axes.c2p(1, gauss(1)),
                           color=INK, stroke_width=2.5, dash_length=0.1)
        mark_intended_overlap(
            axes, curve, area, vline,
            reason="the probability is the shaded area under the density")
        acap = Text("the shaded area up to one: about 0.84",
                    font_size=CAPTION, color=MUTED)
        acap.next_to(chart, DOWN, buff=0.35)
        acap.match_x(axes)
        # (2026-07-05 draft review round 2, 6:43) figure + caption move as
        # ONE BLOCK, its center on the halfway anchor of the content zone.
        ablock = VGroup(chart, curve, area, vline, acap)
        ablock.shift(UP * (zone_center_y(title) - ablock.get_center()[1]))

        with self.voiceover(
            text="The answer is approximately Phi of one — the area under "
                 "the standard Gaussian density up to one — about zero "
                 "point eight four."
        ):
            self.play(Create(axes), Write(xlab), run_time=0.7)
            self.play(Create(curve), run_time=0.7)
            self.play(FadeIn(area), Create(vline), run_time=0.8)
            self.play(Write(g3), FadeIn(acap), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Series finale: key idea + a closing line, no next-video tease.
        # (2026-07-05 draft review round 2, ending) the closing message
        # LANDS: the landing sentence gets its own voiceover moment, alone
        # at center in ACCENT, then demotes to INK as the key card's first
        # line (the single ACCENT hands off to the "Key idea" kicker).
        land = MathTex(
            r"\text{A large sum, scaled by } 1/\sqrt{n}"
            r"\text{, forgets its distribution.}",
            font_size=BODY, color=INK,
        )
        # (2026-07-05 draft review round 3) both card lines render through
        # MathTex \text so LaTeX and Pango sizing cannot disagree.
        key = VGroup(
            land,
            MathTex(r"\text{Standardized, it flows to the standard normal.}",
                    font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.24)
        closing = VGroup(
            Text("We opened with sets; we close with the bell curve.",
                 font_size=SMALL, color=MUTED),
            Text("Probability, end to end.", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.18)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key,
            closing,
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)

        land_solo = land.copy().set_color(ACCENT).move_to(ORIGIN)

        with self.voiceover(
            text="The key idea of this video: a large sum, scaled by one "
                 "over root n, forgets its distribution."
        ):
            self.play(Write(land_solo), run_time=1.4)

        with self.voiceover(
            text="Standardized, it flows to the standard normal."
        ):
            self.play(Transform(land_solo, land),
                      FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.8)
            self.play(Write(key[1]), run_time=1.0)

        # (2026-07-05 draft review, 0:20 sweep) "final video" softened —
        # no claim that the series ends here; the arc language stays.
        with self.voiceover(
            text="We opened with sets; we close with the bell curve. "
                 "Probability, end to end."
        ):
            self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.8)

        self.wait(0.5)
        self.play(FadeOut(land_solo), FadeOut(outro[0]),
                  FadeOut(key[1]), FadeOut(closing))
