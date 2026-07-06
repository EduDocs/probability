# derived_from: content/21-joint-pmfs-script.md
# derived_from_sha256: 76cf1332bbf310d86e7e510ae630d6a247f4c560fbb89de906c017015bf90540
"""Chapter 7, Video 1 -- Joint PMFs and Expectations.

Source notes : discrete_vectors.tex (chapter intro + Sections 7.1-7.2) --
               the joint PMF, marginals by summing out, the with/without
               replacement contrast, functions of a pair, and linearity.
Script        : content/21-joint-pmfs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/joint_pmfs.py ChapterOverview
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
    section_title,
    make_pmf_chart,
    mass_table,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    omega_box,
    ball,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


# The urn joint tables (headers in row 0 / column 0).
WITHOUT_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", "0", r"\tfrac{1}{6}", r"\tfrac{1}{6}"],
    ["2", r"\tfrac{1}{6}", "0", r"\tfrac{1}{6}"],
    ["3", r"\tfrac{1}{6}", r"\tfrac{1}{6}", "0"],
]
WITH_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["2", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
    ["3", r"\tfrac{1}{9}", r"\tfrac{1}{9}", r"\tfrac{1}{9}"],
]


def margin_marks(table):
    """Marginal labels placed on the table's grid geometry.

    Anchoring to cell glyphs drifts ("0" and "1/6" have different sizes),
    so every mark takes its row y / column x from the header digits and a
    fixed offset from the table edge: the p_X column is one vertical line,
    the p_Y row is one horizontal line (2026-07-03 draft review round 4,
    2:06/2:27). Returns (col_head, margin_col, row_head, margin_row).
    """
    mx = table.get_right()[0] + 0.95
    my = table.get_bottom()[1] - 0.55
    row_y = [table.cells[i][0].get_center()[1] for i in range(4)]
    col_x = [table.cells[0][j].get_center()[0] for j in range(4)]
    col_head = MathTex("p_X", font_size=CAPTION, color=MUTED)
    col_head.move_to([mx, row_y[0], 0])
    margin_col = VGroup(*[
        MathTex(r"\tfrac{1}{3}", font_size=SMALL, color=ACCENT)
        .move_to([mx, row_y[i], 0])
        for i in range(1, 4)
    ])
    row_head = MathTex("p_Y", font_size=CAPTION, color=MUTED)
    row_head.move_to([col_x[0], my, 0])
    margin_row = VGroup(*[
        MathTex(r"\tfrac{1}{3}", font_size=SMALL, color=ACCENT)
        .move_to([col_x[j], my, 0])
        for j in range(1, 4)
    ])
    return col_head, margin_col, row_head, margin_row


def style_headers(table):
    """Headers (row 0 and column 0) in MUTED; zeros de-emphasized."""
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
            "Joint PMFs and Expectations",
            ["Describe two random variables at once - and read",
             "marginals, functions, and expectations off one table."],
            kicker="Chapter 7  ·  Multiple Random Variables",
        )
        tag = progress_tag(1, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The joint PMF", font_size=BODY, color=INK),
            Text("2.  Marginals — and their limits", font_size=BODY, color=INK),
            Text("3.  Functions and linearity", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="So far the course has watched one random variable at a "
                 "time. Real models rarely have that luxury: a signal comes "
                 "with its noise, a first draw with a second. This chapter "
                 "puts several random variables on screen at once."
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
            text="In this video we meet the object that describes a pair "
                 "completely — the joint probability mass function, best "
                 "pictured as a table of masses —"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="learn to recover each variable's own PMF by summing the "
                 "table out, and see why the margins alone can never tell "
                 "the whole story,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and then push functions and expectations through the "
                 "pair, ending at one of the most useful facts in "
                 "probability."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JointPMFDefinition(VoiceoverScene):
    """Beat: joint-pmf -- the pair as a map, the definition, set sums."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Joint PMF")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Left: the sample space with three outcomes. Right: a small plane.
        box = omega_box(width=3.6, height=3.4)
        box.move_to(LEFT * 4.1 + DOWN * 0.7)
        balls = VGroup(
            ball("1", "#c0504d", radius=0.26),
            ball("2", BAR, radius=0.26),
            ball("3", "#6aa84f", radius=0.26),
        )
        balls[0].move_to(box.get_center() + UP * 0.9 + LEFT * 0.7)
        balls[1].move_to(box.get_center() + DOWN * 0.2 + RIGHT * 0.8)
        balls[2].move_to(box.get_center() + DOWN * 1.0 + LEFT * 0.5)

        plane = Axes(
            x_range=[0, 4, 1], y_range=[0, 4, 1],
            x_length=3.4, y_length=3.0,
            axis_config={"include_numbers": False}, tips=False,
        ).move_to(RIGHT * 3.4 + DOWN * 0.7)
        x_name = MathTex("X", font_size=SMALL, color=MUTED)
        x_name.next_to(plane.c2p(4, 0), DOWN + RIGHT, buff=0.2)
        y_name = MathTex("Y", font_size=SMALL, color=MUTED)
        y_name.next_to(plane.c2p(0, 4), LEFT, buff=0.25)

        targets = [(1, 3), (3, 1), (2, 2)]
        dots = VGroup(*[
            Dot(plane.c2p(x, y), radius=0.08, color=ACCENT)
            for (x, y) in targets
        ])
        arrows = VGroup(*[
            CurvedArrow(b.get_center() + RIGHT * 0.3, d.get_center(),
                        angle=-PI / 7, color=MUTED, stroke_width=2.5,
                        tip_length=0.16)
            for b, d in zip(balls, dots)
        ])
        # The mapping figure is one composition: arrows sweep from the box
        # into the plane, dots ride the axes.
        mark_intended_overlap(box, balls, plane, dots, arrows,
                              reason="outcome-to-plane mapping figure")

        with self.voiceover(
            text="Take two random variables riding the same experiment."
        ):
            self.play(Create(box[0]), Write(box[1]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(b) for b in balls],
                                  lag_ratio=0.2), run_time=0.8)

        with self.voiceover(
            text="Together they form a pair: each outcome in the sample "
                 "space now lands on a point in the plane — an x-coordinate "
                 "from X, a y-coordinate from Y."
        ):
            self.play(Create(plane), FadeIn(x_name), FadeIn(y_name),
                      run_time=0.9)
            self.play(LaggedStart(*[Create(a) for a in arrows],
                                  lag_ratio=0.25), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(d, scale=2.0) for d in dots],
                                  lag_ratio=0.25), run_time=0.8)

        definition = MathTex(
            r"p_{X,Y}(x, y)", "=", pr(r"X = x,\, Y = y"),
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(definition)

        with self.voiceover(
            text="The pair is described by one function: the joint "
                 "probability mass function. p sub X comma Y of x and y is "
                 "the probability that X equals x and, at the same time, Y "
                 "equals y. It is the one-variable definition with the event "
                 "replaced by an intersection."
        ):
            self.play(Write(definition), run_time=1.4)
            self.play(definition[0].animate.set_color(ACCENT), run_time=0.5)

        # Side by side, not stacked: the stacked pair dipped into the
        # mapping arrows and the Y label (2026-07-03 draft review, 1:30).
        set_sum = VGroup(
            MathTex(r"\Pr(S) = \sum_{(x,y) \in S} p_{X,Y}(x, y)",
                    font_size=SMALL, color=INK),
            MathTex(r"\sum_{x}\sum_{y} p_{X,Y}(x, y) = 1",
                    font_size=SMALL, color=INK),
        ).arrange(RIGHT, buff=1.1)
        set_sum.next_to(definition, DOWN, buff=0.3)
        fit_to_frame(set_sum)

        with self.voiceover(
            text="And the familiar rules carry over: the probability that "
                 "the pair lands in any set of points is the sum of the "
                 "joint masses over that set, and summing over every pair of "
                 "values gives exactly one."
        ):
            self.play(FadeIn(set_sum[0]), run_time=0.7)
            self.play(FadeIn(set_sum[1]), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MarginalPMFs(VoiceoverScene):
    """Beat: marginals -- the urn table, row sums, column sums."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Marginals by Summing Out")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        balls = VGroup(
            ball("1", "#c0504d", radius=0.24),
            ball("2", BAR, radius=0.24),
            ball("3", "#6aa84f", radius=0.24),
        ).arrange(RIGHT, buff=0.3)
        balls.next_to(title, DOWN, buff=0.4)

        # The table sits centered and stays put; the marginals are written
        # into its margins in place (2026-07-03 draft review round 3, 2:06).
        table = style_headers(mass_table(WITHOUT_TABLE))
        table.move_to(DOWN * 1.1)
        fit_to_frame(table)

        with self.voiceover(
            text="Here is a joint PMF worth staring at. An urn holds balls "
                 "numbered one, two, and three; we draw two without "
                 "replacement. X is the first number, Y the second. The "
                 "table shows every mass: zeros on the diagonal — the same "
                 "ball cannot appear twice — and one sixth in every other "
                 "cell."
        ):
            self.play(LaggedStart(*[FadeIn(b) for b in balls],
                                  lag_ratio=0.2), run_time=0.7)
            self.play(Create(table[0]), run_time=0.9)
            self.play(FadeIn(table[1]), run_time=0.9)

        margin_col_head, margin_col, margin_row_head, margin_row = \
            margin_marks(table)

        with self.voiceover(
            text="What is the PMF of X alone? Fix a row and add across it: "
                 "one sixth plus one sixth is one third, for every row. That "
                 "operation — summing out the variable you don't care about "
                 "— is called marginalization, and the result is the "
                 "marginal PMF of X."
        ):
            row = VGroup(*[table.cells[1][j] for j in range(1, 4)])
            self.play(LaggedStart(*[Indicate(c, color=ACCENT)
                                    for c in row], lag_ratio=0.2),
                      run_time=1.2)
            self.play(FadeIn(margin_col_head),
                      FadeIn(margin_col[0], shift=LEFT * 0.3), run_time=0.7)
            self.play(FadeIn(margin_col[1], shift=LEFT * 0.3),
                      FadeIn(margin_col[2], shift=LEFT * 0.3), run_time=0.8)

        # The caption lives in the gap between the balls and the table --
        # at the bottom edge it collided with the p_Y margin row
        # (2026-07-03 draft review, 2:29).
        caption = Text("the marginal PMFs live in the margins",
                       font_size=CAPTION, color=MUTED)
        caption.move_to((balls.get_bottom() + table.get_top()) / 2)

        with self.voiceover(
            text="Columns work the same way, and Y's marginal is also "
                 "uniform: one third, one third, one third. The margins of "
                 "the table — literally, the sums written in its margins — "
                 "are the individual distributions."
        ):
            col = VGroup(*[table.cells[i][1] for i in range(1, 4)])
            self.play(LaggedStart(*[Indicate(c, color=ACCENT)
                                    for c in col], lag_ratio=0.2),
                      run_time=1.0)
            self.play(FadeIn(margin_row_head),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.3)
                                    for m in margin_row], lag_ratio=0.2),
                      run_time=1.0)
            self.play(FadeIn(caption), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MarginalsNotEnough(VoiceoverScene):
    """Beat: not-enough -- same margins, different joints."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Marginals Are Not Enough")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Table (and its margins) sit exactly where the previous beat's
        # table sat (2026-07-03 draft review round 4, 2:58).
        table = style_headers(mass_table(WITHOUT_TABLE))
        table.move_to(DOWN * 1.1)
        fit_to_frame(table)
        tag_without = Text("without replacement", font_size=CAPTION,
                           color=MUTED)
        tag_without.next_to(title, DOWN, buff=0.35)

        with self.voiceover(
            text="Now change one word in the experiment: draw the two balls "
                 "with replacement."
        ):
            self.play(FadeIn(tag_without), Create(table[0]),
                      FadeIn(table[1]), run_time=1.0)

        with_table = style_headers(mass_table(WITH_TABLE))
        with_table.move_to(table)
        tag_with = Text("with replacement", font_size=CAPTION, color=INK)
        tag_with.move_to(tag_without)

        # Both margins reappear: row sums stream right, column sums stream
        # down — matching the narration "sum the rows and columns"
        # (2026-07-03 draft review round 2, 3:00), placed on the same grid
        # geometry as the previous beat (round 4, 2:58).
        margin_col_head, margin_col, margin_row_head, margins = \
            margin_marks(with_table)

        with self.voiceover(
            text="The table transforms — every cell becomes one ninth, "
                 "diagonal included, because the first ball goes back before "
                 "the second draw. Sum the rows and columns: one third "
                 "everywhere. The marginals are exactly the same as before."
        ):
            # A smooth morph, not a cut (2026-07-03 draft review, 2:50).
            self.play(Transform(tag_without, tag_with), run_time=0.8)
            self.play(Transform(table, with_table), run_time=1.4)
            row = VGroup(*[table.cells[1][j] for j in range(1, 4)])
            self.play(LaggedStart(*[Indicate(c, color=ACCENT)
                                    for c in row], lag_ratio=0.15),
                      run_time=0.8)
            self.play(FadeIn(margin_col_head),
                      LaggedStart(*[FadeIn(m, shift=LEFT * 0.3)
                                    for m in margin_col], lag_ratio=0.2),
                      run_time=0.9)
            self.play(FadeIn(margin_row_head),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.3)
                                    for m in margins], lag_ratio=0.2),
                      run_time=0.9)

        # The lesson sits halfway between the tag and the table's top edge.
        verdict = Text("same margins - different joints",
                       font_size=SMALL, color=ACCENT)
        verdict.move_to((tag_without.get_bottom() + table.get_top()) / 2)

        with self.voiceover(
            text="Same margins — different tables. And that is the lesson: "
                 "the marginal PMFs do not determine the joint PMF. Whether "
                 "the two draws can collide, whether they push each other "
                 "around — dependence lives inside the table, in information "
                 "the margins simply do not carry. To describe a pair, you "
                 "need the joint."
        ):
            self.play(FadeIn(verdict, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class JointExpectation(VoiceoverScene):
    """Beat: expectations -- the dice sum, the double sum, linearity."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Functions and Linearity")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # A 6x6 lattice of small squares standing in for the dice table,
        # with the die values labelled in the dice colors: rows = blue die
        # (X), columns = red die (Y) (2026-07-03 draft review, 3:44).
        BLUE_DIE, RED_DIE = BAR, "#c0504d"
        n = 6
        cell = 0.52
        squares = VGroup()
        lattice = [[None] * n for _ in range(n)]
        for i in range(n):        # i ~ blue die (rows, y downward)
            for j in range(n):    # j ~ red die (columns)
                sq = Square(side_length=cell, stroke_width=1.2,
                            stroke_color=MUTED, fill_color=BAR,
                            fill_opacity=0.12)
                sq.move_to([(j - (n - 1) / 2) * cell,
                            ((n - 1) / 2 - i) * cell, 0])
                lattice[i][j] = sq
                squares.add(sq)
        col_vals = VGroup(*[
            MathTex(str(j + 1), font_size=CAPTION, color=RED_DIE)
            .next_to(lattice[0][j], UP, buff=0.18)
            for j in range(n)
        ])
        row_vals = VGroup(*[
            MathTex(str(i + 1), font_size=CAPTION, color=BLUE_DIE)
            .next_to(lattice[i][0], LEFT, buff=0.25)
            for i in range(n)
        ])
        grid = VGroup(squares, col_vals, row_vals)
        grid.move_to(DOWN * 1.25)
        u_def = MathTex("U = X + Y", font_size=SMALL, color=INK)
        u_def.next_to(title, DOWN, buff=0.35)
        dice_note = Text("rolling a blue die and a red die",
                         font_size=CAPTION, color=MUTED)
        dice_note.move_to((u_def.get_bottom() + grid.get_top()) / 2)
        k_label = MathTex("x + y = 2", font_size=SMALL, color=ACCENT)
        k_label.next_to(grid, RIGHT, buff=0.6)
        fit_to_frame(VGroup(grid, k_label))

        with self.voiceover(
            text="Functions ride along, exactly as they did for one "
                 "variable."
        ):
            self.play(Write(u_def), run_time=0.7)

        def light(k, label_tex, hold=1.4):
            cells = [lattice[i][j] for i in range(n) for j in range(n)
                     if (i + 1) + (j + 1) == k]
            new_label = MathTex(label_tex, font_size=SMALL, color=ACCENT)
            new_label.move_to(k_label)
            self.play(*[sq.animate.set_fill(ACCENT, opacity=0.6)
                        for sq in cells],
                      Transform(k_label, new_label), run_time=hold)
            self.play(*[sq.animate.set_fill(BAR, opacity=0.12)
                        for sq in cells], run_time=0.5)

        with self.voiceover(
            text="Roll a blue die and a red die, and let U be their sum. U "
                 "is a random variable, and its PMF sums the joint over the "
                 "pairs that produce each value — the diagonals of the "
                 "six-by-six table."
        ):
            self.play(FadeIn(grid), FadeIn(dice_note), run_time=0.9)

        # Each diagonal lights exactly while its value is spoken.
        with self.voiceover(text="Two comes from one pair,"):
            self.play(FadeIn(k_label), run_time=0.2)
            light(2, "x + y = 2")

        with self.voiceover(text="seven from six pairs,"):
            light(7, "x + y = 7")

        # Twelve is named explicitly, not skipped over (2026-07-03 draft
        # review round 4, 3:58).
        with self.voiceover(text="and twelve, again, from a single pair:"):
            light(12, "x + y = 12")

        # The triangular PMF of the sum (one chart at a time: grid leaves).
        tri = [0.0] * 2 + [k / 36 for k in (1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1)]
        chart, bars = make_pmf_chart(tri, x_label="u", y_label=r"p_U(u)",
                                     y_max=0.2)
        chart.scale(0.6).to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="the familiar triangle of the two-dice sum, straight from "
                 "the joint."
        ):
            self.play(FadeOut(grid), FadeOut(k_label), FadeOut(dice_note),
                      run_time=0.5)
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.06), run_time=1.0)

        double_sum = MathTex(
            expectation("g(X, Y)"), "=",
            r"\sum_{x}\sum_{y} g(x, y)\, p_{X,Y}(x, y)",
            font_size=SMALL,
        ).next_to(u_def, DOWN, buff=0.3)
        fit_to_frame(double_sum)

        with self.voiceover(
            text="Expectations follow the same pattern one dimension up: "
                 "the expected value of g of X and Y is a double sum — g of "
                 "each pair, weighted by the joint mass of that pair."
        ):
            self.play(Write(double_sum), run_time=1.2)

        linearity = MathTex(
            expectation("X + Y"), "=",
            expectation("X"), "+", expectation("Y"),
            font_size=BODY,
        )
        linearity.next_to(double_sum, DOWN, buff=0.35)
        fit_to_frame(linearity)
        no_indep = Text("no independence required", font_size=CAPTION,
                        color=MUTED)
        no_indep.next_to(linearity, DOWN, buff=0.22)

        with self.voiceover(
            text="Now take the simplest g: the sum. Split x plus y inside "
                 "the double sum, and it falls apart into two single sums — "
                 "each one a marginal mean. The expectation of X plus Y is "
                 "the expectation of X plus the expectation of Y. Look at "
                 "what we did not assume: nothing. No independence, no "
                 "special structure — linearity of expectation holds for "
                 "every pair, always."
        ):
            self.play(FadeOut(VGroup(chart, *bars)), run_time=0.4)
            self.play(Write(linearity), run_time=1.2)
            self.play(linearity.animate.set_color(ACCENT),
                      FadeIn(no_indep), run_time=0.7)

        # The urn callback gets its picture (2026-07-03 draft review
        # round 2, 4:45): the three-ball urn beside the arithmetic.
        urn_body = RoundedRectangle(corner_radius=0.25, width=1.7,
                                    height=1.9, color=MUTED)
        urn_body.set_stroke(MUTED, 2)
        urn_balls = VGroup(
            ball("1", "#c0504d", radius=0.24),
            ball("2", BAR, radius=0.24),
            ball("3", "#6aa84f", radius=0.24),
        )
        urn_balls[0].move_to(urn_body.get_center() + LEFT * 0.35 + DOWN * 0.45)
        urn_balls[1].move_to(urn_body.get_center() + RIGHT * 0.35 + DOWN * 0.45)
        urn_balls[2].move_to(urn_body.get_center() + UP * 0.15)
        urn = VGroup(urn_body, urn_balls)
        mark_intended_overlap(urn_body, urn_balls,
                              reason="balls sit inside the urn")
        urn_math = MathTex(
            expectation("X + Y"), "=", "2 + 2", "=", "4",
            font_size=SMALL, color=INK,
        )
        urn_group = VGroup(urn, urn_math).arrange(RIGHT, buff=0.8)
        urn_group.move_to(DOWN * 1.9)
        fit_to_frame(urn_group)

        with self.voiceover(
            text="For instance, in an urn with three balls, the expectation "
                 "for a pair of drawings is two plus two — four — with and "
                 "without replacement."
        ):
            self.play(Create(urn_body), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, scale=1.4) for b in urn_balls],
                                  lag_ratio=0.2), run_time=0.8)
            self.play(Write(urn_math), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["The joint PMF is the whole story of a pair -",
             "and E[X + Y] = E[X] + E[Y]."],
            next_title="Conditioning Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video: the joint PMF is the whole "
                 "story of a pair — marginals sum it out, and expectations "
                 "of sums split with no questions asked."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
