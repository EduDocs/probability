# derived_from: content/24-independence-rvs-script.md
# derived_from_sha256: 28ab422ad7f0fd1cb790a579c154b0a906af04d82025e97aa852671034c69c3e
"""Chapter 7, Video 4 -- Independent Random Variables.

Source notes : discrete_vectors.tex (Section 7.5) -- independence as
               factorization, products of expectations, the variance of a
               sum, independence from events, and iid.
Script        : content/24-independence-rvs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/independence_rvs.py ChapterOverview
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
    variance,
    expectation,
    section_title,
    make_pmf_chart,
    mass_table,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    die_face,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


def result_card(tex: str, label: str | None = None) -> VGroup:
    """A compact result card: a rounded frame around one formula."""
    body = MathTex(tex, font_size=SMALL, color=INK)
    frame = RoundedRectangle(
        corner_radius=0.15,
        width=body.width + 0.6, height=body.height + 0.5,
        color=MUTED,
    ).set_stroke(MUTED, 2)
    body.move_to(frame)
    parts = VGroup(frame, body)
    if label:
        tag = Text(label, font_size=CAPTION, color=MUTED)
        tag.next_to(frame, UP, buff=0.12)
        parts.add(tag)
    return parts


WITH_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["2", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["3", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
]
WITHOUT_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", "0", r"\tfrac{1}{6}", r"\tfrac{1}{6}"],
    ["2", r"\tfrac{1}{6}", "0", r"\tfrac{1}{6}"],
    ["3", r"\tfrac{1}{6}", r"\tfrac{1}{6}", "0"],
]


def style_headers(table):
    for j in range(4):
        if table.cells[0][j] is not None:
            table.cells[0][j].set_color(MUTED)
    for i in range(1, 4):
        table.cells[i][0].set_color(MUTED)
        for j in range(1, 4):
            if table.cells[i][j].get_tex_string() == "0":
                table.cells[i][j].set_color(MUTED)
    return table


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Independent Random Variables",
            ["The joint PMF factors into its marginals - and",
             "products, variances, and iid follow."],
            kicker="Chapter 7  ·  Multiple Random Variables",
        )
        tag = progress_tag(4, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The joint PMF factors", font_size=BODY, color=INK),
            Text("2.  Products of expectations", font_size=BODY, color=INK),
            Text("3.  Variances add", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Two videos ago we saw that margins never determine a "
                 "joint table — except in one special case, and it "
                 "is the most important special case in probability."
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
            text="In this video we define independence for random variables "
                 "— the joint PMF factoring into its marginals —"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="watch expectations of products split cleanly in two,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and collect the payoff that powers the rest of this "
                 "course: for independent variables, the variance of a sum "
                 "is the sum of the variances."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class FactoringJointPMF(VoiceoverScene):
    """Beat: factoring -- the definition, the outer product, cell events."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Factoring the Joint PMF")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        definition = MathTex(
            r"p_{X,Y}(x, y)", "=", r"p_X(x)\; p_Y(y)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(definition)

        with self.voiceover(
            text="Random variables X and Y are independent when the joint "
                 "mass at every pair is the product of the marginal masses."
        ):
            self.wait(0.2)

        with self.voiceover(
            text="One equation, checked at every cell of the table: joint "
                 "equals marginal times marginal."
        ):
            self.play(Write(definition), run_time=1.2)
            self.play(definition[0].animate.set_color(ACCENT), run_time=0.5)

        table = style_headers(mass_table(WITH_TABLE))
        table.scale(0.85).move_to(DOWN * 1.5)
        col_margins = VGroup(*[
            MathTex(r"\tfrac{1}{3}", font_size=CAPTION, color=ACCENT)
            .next_to(table.cells[0][j], UP, buff=0.4)
            for j in range(1, 4)
        ])
        row_margins = VGroup(*[
            MathTex(r"\tfrac{1}{3}", font_size=CAPTION, color=ACCENT)
            .next_to(table.cells[i][3], RIGHT, buff=0.6)
            for i in range(1, 4)
        ])

        with self.voiceover(
            text="We have already met an independent pair without naming "
                 "it. Draw two balls with replacement, and the all-ninths "
                 "table is exactly one third times one third in every cell "
                 "— sweep the margins across the table and they rebuild it "
                 "perfectly."
        ):
            self.play(Create(table[0]), FadeIn(table[1]), run_time=1.0)
            self.play(FadeIn(col_margins), FadeIn(row_margins),
                      run_time=0.7)
            # A row third and a column third converge onto one cell and
            # rebuild its ninth — the factorization made visible
            # (2026-07-04 draft review, 1:00 + "better visual" note).
            cell = table.cells[2][2]
            c_copy = col_margins[1].copy()
            r_copy = row_margins[1].copy()
            mark_intended_overlap(
                c_copy, r_copy, table,
                reason="marginal thirds converge onto the cell they rebuild",
            )
            self.add(c_copy, r_copy)
            self.play(c_copy.animate.move_to(cell),
                      r_copy.animate.move_to(cell), run_time=0.9)
            self.play(FadeOut(c_copy), FadeOut(r_copy),
                      Indicate(cell, color=ACCENT), run_time=0.7)
            cells = [table.cells[i][j] for i in range(1, 4)
                     for j in range(1, 4)]
            self.play(LaggedStart(*[Indicate(c, color=ACCENT)
                                    for c in cells], lag_ratio=0.06),
                      run_time=1.6)

        # Split from the block above so the failing table lands exactly
        # with its own narration (2026-07-04 draft review, 1:00).
        without = style_headers(mass_table(WITHOUT_TABLE))
        without.scale(0.85).move_to(table)

        with self.voiceover(
            text="The without-replacement table fails immediately: a "
                 "product of positive margins can never manufacture the "
                 "zeros on its diagonal."
        ):
            self.play(FadeOut(col_margins), FadeOut(row_margins),
                      run_time=0.3)
            self.play(Transform(table, without), run_time=0.9)
            zeros = [table.cells[i][i] for i in range(1, 4)]
            self.play(LaggedStart(*[Indicate(z, color=ACCENT)
                                    for z in zeros], lag_ratio=0.25),
                      run_time=1.0)

        # Card keeps only the formula: the "chapter 4's ..." label line is
        # deleted and the table rises clear of the card
        # (2026-07-04 draft review, 1:21).
        cell_events = result_card(
            r"\{X = x\} \perp \{Y = y\}\ \text{for every pair}\ (x, y)",
        )
        cell_events.to_edge(DOWN, buff=0.8)
        fit_to_frame(cell_events)

        # While the narration discusses independence, show the table that
        # genuinely factors — back to with-replacement
        # (2026-07-04 draft review, "better visual" note).
        with_back = style_headers(mass_table(WITH_TABLE))
        with_back.scale(0.85 * 0.85)
        with_back.move_to(table.get_center() + UP * 0.9)

        with self.voiceover(
            text="And the connection to chapter four is exact: X and Y are "
                 "independent precisely when the events \"X equals x\" and "
                 "\"Y equals y\" are independent for every single pair. "
                 "Independence of variables is independence of events, "
                 "enforced across the whole table at once."
        ):
            self.play(Transform(table, with_back), run_time=0.7)
            self.play(FadeIn(cell_events, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ProductExpectation(VoiceoverScene):
    """Beat: products -- E[XY] factors; the dice; the general rule."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Expectations of Products")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        line1 = MathTex(
            expectation("XY"), "=",
            r"\sum_{x}\sum_{y} x\, y\; p_X(x)\, p_Y(y)",
            font_size=SMALL,
        )
        line2 = MathTex(
            r"= \left( \sum_{x} x\, p_X(x) \right)"
            r"\left( \sum_{y} y\, p_Y(y) \right)",
            font_size=SMALL,
        )
        line3 = MathTex(
            expectation("XY"), "=", expectation("X"), r"\,", expectation("Y"),
            font_size=BODY,
        )
        derivation = VGroup(line1, line2, line3).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35)
        derivation.next_to(title, DOWN, buff=0.5)
        fit_to_frame(derivation)

        with self.voiceover(
            text="Factored joints make expectations easy. Take the "
                 "expectation of the product X times Y: a double sum "
                 "against the joint. Substitute the factorization, and the "
                 "double sum separates — x terms with the marginal of X, y "
                 "terms with the marginal of Y. The expectation of a "
                 "product of independent variables is the product of the "
                 "expectations."
        ):
            self.play(Write(line1), run_time=1.2)
            self.play(FadeIn(line2), run_time=1.0)
            self.play(Write(line3), run_time=1.0)
            self.play(line3.animate.set_color(ACCENT), run_time=0.5)

        dice = VGroup(die_face(3, size=0.6), die_face(5, size=0.6))
        dice.arrange(RIGHT, buff=0.35)
        dice_val = MathTex(r"\mathrm{E}[XY] = 3.5 \times 3.5 = 12.25",
                           font_size=SMALL, color=INK)
        dice_row = VGroup(dice, dice_val).arrange(RIGHT, buff=0.7)
        dice_row.next_to(derivation, DOWN, buff=0.5)
        fit_to_frame(dice_row)

        with self.voiceover(
            text="Roll the two dice again: each has mean three and a half, "
                 "the rolls are independent, so the expected product is "
                 "three and a half squared — twelve and a quarter. No table "
                 "required."
        ):
            self.play(line3.animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(dice_row), run_time=0.9)

        general = MathTex(
            expectation("g(X)\\, h(Y)"), "=",
            expectation("g(X)"), r"\,", expectation("h(Y)"),
            font_size=SMALL, color=MUTED,
        ).next_to(dice_row, DOWN, buff=0.4)
        fit_to_frame(general)
        any_gh = Text("any g, any h", font_size=CAPTION, color=MUTED)
        any_gh.next_to(general, DOWN, buff=0.2)

        with self.voiceover(
            text="And nothing was special about the identity function: for "
                 "independent X and Y, the expectation of g of X times h of "
                 "Y splits the same way, for any functions g and h. Keep "
                 "that one — it does quiet work everywhere. "
        ):
            self.play(FadeIn(general), FadeIn(any_gh), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class VarianceOfSum(VoiceoverScene):
    """Beat: variance -- the cross term appears, and dies."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Variance of a Sum")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        expand1 = MathTex(
            variance("X + Y"), "=",
            variance("X"), "+", variance("Y"), "+",
            r"2\, \mathrm{E}\left[(X - \mathrm{E}[X])(Y - \mathrm{E}[Y])\right]",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.55)
        fit_to_frame(expand1)

        with self.voiceover(
            text="Now the identity this chapter has been building toward. "
                 "Means of sums always add — that was linearity, no "
                 "assumptions asked. What about variances? Expand the "
                 "variance of X plus Y around its mean, and the square "
                 "produces three pieces: the variance of X, the variance of "
                 "Y, and twice a cross term — the expectation of the two "
                 "deviations multiplied together."
        ):
            self.play(Write(expand1), run_time=1.8)

        cross_note = Text("how the variables move together",
                          font_size=CAPTION, color=MUTED)
        cross_note.next_to(expand1, DOWN, buff=0.5)

        with self.voiceover(
            text="That cross term measures how the variables move "
                 "together; it will later earn the name covariance."
        ):
            self.play(expand1[6].animate.set_color(ACCENT),
                      FadeIn(cross_note), run_time=0.9)

        # Accent flag for the independence assumption before the equation
        # that equals zero; stack re-spaced evenly down the frame
        # (2026-07-04 draft review, 3:45).
        indep_tag = Text("under independence", font_size=CAPTION,
                         color=ACCENT)
        indep_tag.next_to(cross_note, DOWN, buff=0.65)
        dies = MathTex(
            r"\mathrm{E}\left[X - \mathrm{E}[X]\right]"
            r"\ \mathrm{E}\left[Y - \mathrm{E}[Y]\right]"
            r"= 0 \cdot 0 = 0",
            font_size=SMALL, color=MUTED,
        ).next_to(indep_tag, DOWN, buff=0.3)
        fit_to_frame(dies)
        identity = MathTex(
            variance("X + Y"), "=", variance("X"), "+", variance("Y"),
            font_size=BODY,
        ).next_to(dies, DOWN, buff=0.75)
        fit_to_frame(identity)

        with self.voiceover(
            text="But let X and Y be independent. The cross term becomes an "
                 "expectation of a product of independent quantities — so "
                 "it factors, by the rule we just proved. And each factor "
                 "is a deviation from its own mean, whose expectation is "
                 "zero. Zero times zero: the cross term vanishes. For "
                 "independent random variables, the variance of the sum is "
                 "the sum of the variances."
        ):
            self.play(expand1[6].animate.set_color(MUTED),
                      FadeIn(indep_tag, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(dies), run_time=1.0)
            self.play(Write(identity), run_time=1.1)
            self.play(identity.animate.set_color(ACCENT),
                      indep_tag.animate.set_color(MUTED), run_time=0.5)

        contrast = VGroup(
            Text("means: always add", font_size=SMALL, color=INK),
            Text("variances: add when independent", font_size=SMALL,
                 color=ACCENT),
        ).arrange(DOWN, buff=0.2)
        contrast.to_edge(DOWN, buff=0.9)

        with self.voiceover(
            text="Hold the contrast: means add always; variances add under "
                 "independence. That asymmetry is why independent noise "
                 "averages out — and it is the engine inside every limit "
                 "theorem still to come."
        ):
            self.play(identity.animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(contrast, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class IndependenceAndIID(VoiceoverScene):
    """Beat: iid -- independence from an event, and the iid workhorse."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Independence from Events, and iid")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        event_card = result_card(
            r"p_{X \mid S}(x) = p_X(x)\ \text{for all}\ x",
            "conditioning that changes nothing",
        )
        event_card.next_to(title, DOWN, buff=0.5)
        # Box a touch lower, opening space under the "conditioning ..."
        # caption line (2026-07-04 draft review, 4:06).
        VGroup(event_card[0], event_card[1]).shift(DOWN * 0.12)
        fit_to_frame(event_card)

        with self.voiceover(
            text="Two small pieces complete the picture. A random variable "
                 "can be independent of an event: conditioning on S then "
                 "changes nothing — the sliced PMF equals the marginal, "
                 "every bar untouched."
        ):
            self.play(FadeIn(event_card, shift=DOWN * 0.2), run_time=0.9)

        # Four identical mini PMF cards: the iid workhorse.
        mini_vals = [0.0, 0.2, 0.5, 0.3]
        proto, _bars = make_pmf_chart(mini_vals, x_label="", y_label="",
                                      y_max=0.7)
        proto.scale(0.22)
        minis = VGroup(*[proto.copy() for _ in range(4)])
        minis.arrange(RIGHT, buff=0.55)
        # Charts a touch higher for vertical balance
        # (2026-07-04 draft review, 4:21).
        minis.move_to(DOWN * 0.85)
        fit_to_frame(minis)
        product = MathTex(
            r"p_{\mathbf{X}}(\mathbf{x}) = \prod_{k=1}^{n} p_X(x_k)",
            font_size=SMALL, color=INK,
        ).next_to(minis, DOWN, buff=0.45)
        iid_note = Text("independent and identically distributed",
                        font_size=CAPTION, color=MUTED)
        iid_note.next_to(product, DOWN, buff=0.22)

        with self.voiceover(
            text="And the workhorse configuration of all of probability: "
                 "draws that are independent and identically distributed — "
                 "iid. One PMF, copied across n draws, with the joint "
                 "factoring into n identical terms. Every sample, every "
                 "repeated experiment, many data set we model from here on "
                 "starts with those three letters."
        ):
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2)
                                    for m in minis], lag_ratio=0.2),
                      run_time=1.2)
            self.play(Write(product), FadeIn(iid_note), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Independence factors the joint into its marginals -",
             "products split, and variances of sums add."],
            next_title="Sums and Many Variables",
        )

        with self.voiceover(
            text="The key idea of this video: independence factors the "
                 "joint into its marginals — so products of expectations "
                 "split, and variances of sums add."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
