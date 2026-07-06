# derived_from: content/23-conditional-expectation-script.md
# derived_from_sha256: 8b0fe422558cf93c40f964b5c81ecd516c881cb89bc5f86148f0a168b1a8a8ef
"""Chapter 7, Video 3 -- Conditional Expectation.

Source notes : discrete_vectors.tex (Section 7.4) -- E[Y | X = x], the
               conditional expectation as a random variable, the tower
               property, and the random-sum shopping spree.
Script        : content/23-conditional-expectation-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/conditional_expectation.py ChapterOverview
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


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Conditional Expectation",
            ["Average a random variable slice by slice - and meet",
             "E[Y | X], a random variable made of means."],
            kicker="Chapter 7  ·  Multiple Random Variables",
        )
        tag = progress_tag(3, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The mean of a slice", font_size=BODY, color=INK),
            Text("2.  A random variable made of means",
                 font_size=BODY, color=INK),
            Text("3.  The tower property", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video, every observation of X handed us a fresh "
                 "distribution for Y — a whole family of sliced, "
                 "renormalized PMFs. This video compresses each slice to a "
                 "single number."
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
            text="We define the conditional expectation — the mean of Y "
                 "given an observation —"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="discover that, taken together, those means form a random "
                 "variable of their own,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and prove the tower property, the rule that lets us "
                 "compute hard expectations one easy stage at a time."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CondExpDefinition(VoiceoverScene):
    """Beat: definition -- per-slice means, the function h, event version."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Conditional Expectation")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        formula = MathTex(
            r"\mathrm{E}[Y \mid X = x]", "=",
            r"\sum_{y} y\, p_{Y \mid X}(y \mid x)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(formula)

        # One conditional slice (from video 22's urn): p_{Y|X}(.|1).
        values = [0.0, 0.0, 0.5, 0.5]
        chart, bars = make_pmf_chart(values, x_label="y",
                                     y_label=r"p_{Y \mid X}", y_max=0.7)
        # Bottom row raised toward mid-frame for balance (2026-07-03 draft
        # review, 1:25).
        chart.scale(0.55).move_to(LEFT * 3.2 + DOWN * 1.25)
        axes = chart[0]
        fulcrum = Triangle(color=ACCENT, fill_opacity=1).scale(0.12)
        fulcrum.next_to(axes.c2p(2.5, 0), DOWN, buff=0.03)
        mark_intended_overlap(chart, fulcrum,
                              reason="fulcrum under the axis")

        with self.voiceover(
            text="Start from one slice. Given that X equals value lower "
                 "case x, the variable Y has a conditional PMF — and any "
                 "PMF has a mean. The "
                 "conditional expectation of Y given X equals x weighs each "
                 "value of y by its conditional mass. On the picture, it is "
                 "the balance point of that slice: one fulcrum for the row "
                 "we observed."
        ):
            self.play(Write(formula), run_time=1.4)
            self.play(formula[0].animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.15), FadeIn(fulcrum),
                      run_time=0.9)

        # h(x): fulcrum positions traced on a small side plot.
        hplot = Axes(
            x_range=[0, 4, 1], y_range=[0, 4, 1],
            x_length=3.2, y_length=2.6,
            axis_config={"include_numbers": True, "font_size": 26},
            tips=False,
        ).move_to(RIGHT * 3.4 + DOWN * 1.25)
        h_name = MathTex(r"h(x) = \mathrm{E}[Y \mid X = x]",
                         font_size=CAPTION, color=MUTED)
        h_name.next_to(hplot, UP, buff=0.3)
        hdots = VGroup(*[
            Dot(hplot.c2p(x, h), radius=0.07, color=ACCENT)
            for x, h in ((1, 2.5), (2, 2.0), (3, 1.5))
        ])
        mark_intended_overlap(hplot, hdots,
                              reason="sample points ride the axes")

        with self.voiceover(
            text="Do this for every possible observation and collect the "
                 "answers. The conditional expectation becomes a function — "
                 "call it h — that maps each value x to the mean of its "
                 "slice."
        ):
            self.play(Create(hplot), FadeIn(h_name), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(d, scale=2.0) for d in hdots],
                                  lag_ratio=0.3), run_time=1.0)

        event_card = result_card(
            r"\mathrm{E}[X \mid S] = \sum_{x} x\, p_{X \mid S}(x)",
            "conditioning on an event",
        )
        # The h-trace has made its point; clear it so the event card gets
        # the right half without crowding the side plot's axes.
        event_card.move_to(RIGHT * 3.4 + DOWN * 1.25)
        fit_to_frame(event_card)

        with self.voiceover(
            text="And events work the same way: the expectation of X given "
                 "an event S is the mean of the event based on the "
                 "conditional PMF from last video — one balance point for "
                 "the re-weighted bars."
        ):
            self.play(FadeOut(VGroup(hplot, h_name, hdots)), run_time=0.5)
            self.play(FadeIn(event_card, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CondExpAsRV(VoiceoverScene):
    """Beat: as-rv -- feed the random X into h; the soda shop."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Random Variable Made of Means")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        h_of_x = MathTex(r"h(x) = \mathrm{E}[Y \mid X = x]",
                         font_size=BODY, color=INK)
        h_of_x.next_to(title, DOWN, buff=0.5)
        h_of_X = MathTex(r"h(X) = \mathrm{E}[Y \mid X]",
                         font_size=BODY, color=ACCENT)
        h_of_X.move_to(h_of_x)
        rv_note = Text("a random variable", font_size=CAPTION, color=MUTED)
        rv_note.next_to(h_of_X, DOWN, buff=0.25)

        with self.voiceover(
            text="Here is the move that gives this chapter its depth. "
                 "Before the experiment runs, we don't know which value X "
                 "will take — X is random. Feed that random X into the "
                 "function h, and h of X becomes a random variable: the "
                 "conditional expectation of Y given X, written with no "
                 "particular value in sight. The experiment resolves X, and "
                 "X resolves the mean."
        ):
            self.play(Write(h_of_x), run_time=1.0)
            self.play(TransformMatchingShapes(h_of_x, h_of_X), run_time=1.1)
            self.play(FadeIn(rv_note), run_time=0.5)

        bottles = VGroup(
            ball(r"\text{c}", ACCENT, radius=0.26),
            ball(r"\text{l}", MUTED, radius=0.26),
        ).arrange(RIGHT, buff=0.5)
        b_card = MathTex(r"B \sim \text{Poisson}(10)",
                         font_size=SMALL, color=INK)
        setup = VGroup(bottles, b_card).arrange(RIGHT, buff=0.9)
        setup.next_to(rv_note, DOWN, buff=0.55)
        given_ten = MathTex(r"\mathrm{E}[C \mid B = 10] = 10p",
                            font_size=SMALL, color=INK)
        given_ten.next_to(setup, DOWN, buff=0.4)

        with self.voiceover(
            text="Make it concrete. A shop sells cherry soda and lemonade; "
                 "the number of bottles sold in an hour is Poisson with "
                 "mean ten, and each customer independently picks cherry "
                 "with probability p. Given that exactly ten bottles were "
                 "sold, the cherry count is binomial, and its conditional "
                 "mean is ten p."
        ):
            self.play(FadeIn(setup), run_time=0.8)
            self.play(Write(given_ten), run_time=0.9)

        pB = MathTex(r"\mathrm{E}[C \mid B] = pB",
                     font_size=BODY, color=ACCENT)
        pB.next_to(given_ten, DOWN, buff=0.45)
        scales = Text("sell more bottles, expect more cherry sodas",
                      font_size=CAPTION, color=MUTED)
        scales.next_to(pB, DOWN, buff=0.25)

        with self.voiceover(
            text="But the bottle count B is random — so the conditional "
                 "mean of the cherry count is p times B: a random variable "
                 "that scales with the crowd. Sell more bottles, expect "
                 "more cherry sodas — the conditional expectation tracks "
                 "the information."
        ):
            self.play(Write(pB), run_time=1.0)
            self.play(FadeIn(scales), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class TowerProperty(VoiceoverScene):
    """Beat: tower -- statement, three-line proof, and the strategy."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Tower Property")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        statement = MathTex(
            r"\mathrm{E}\left[\, \mathrm{E}[Y \mid X] \,\right]",
            "=", r"\mathrm{E}[Y]",
            font_size=SECTION,
        ).next_to(title, DOWN, buff=0.55)
        fit_to_frame(statement)

        with self.voiceover(
            text="A random variable made of means should itself have a "
                 "mean — and it is exactly the one you hope for. The "
                 "expectation of the conditional expectation of Y given X "
                 "equals the expectation of Y. This is the tower property."
        ):
            self.play(Write(statement), run_time=1.4)
            self.play(statement.animate.set_color(ACCENT), run_time=0.5)

        # The derivation lines up on the equals signs (2026-07-03 draft
        # review, 3:31): each line splits at its first "=".
        lines = VGroup(
            MathTex(r"\mathrm{E}\left[\mathrm{E}[Y \mid X]\right]", "=",
                    r"\sum_{x} \mathrm{E}[Y \mid X = x]\; p_X(x)",
                    font_size=SMALL, color=INK),
            MathTex("=",
                    r"\sum_{x} \sum_{y} y\; p_{Y \mid X}(y \mid x)\,"
                    r" p_X(x) = \sum_{y} y \sum_{x} p_{X,Y}(x, y)",
                    font_size=SMALL, color=MUTED),
            MathTex("=",
                    r"\sum_{y} y\; p_Y(y) = \mathrm{E}[Y]",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.3)
        lines.next_to(statement, DOWN, buff=0.5)
        # Continuation lines hang their "=" under line 1's "=" — parts are
        # (lhs, "=", rhs) on line 1 and ("=", rhs) below.
        for ln in lines[1:]:
            ln.shift(RIGHT * (lines[0][1].get_x() - ln[0].get_x()))
        lines.move_to([0.0, lines.get_center()[1], 0.0])
        fit_to_frame(lines)

        with self.voiceover(
            text="The proof is three moves we already own. Write the outer "
                 "expectation as a sum over x, weighted by the marginal. "
                 "Substitute each slice's mean. The conditional mass times "
                 "the marginal is the joint — the product rule — and "
                 "summing the joint over x re-marginalizes it to the PMF of "
                 "Y. What is left is the plain mean of Y."
        ):
            self.play(statement.animate.set_color(INK), run_time=0.3)
            self.play(Write(lines[0]), run_time=1.0)
            self.play(FadeIn(lines[1]), run_time=1.0)
            self.play(Write(lines[2]), run_time=0.9)

        # Closing line in accent, like the other scenes' lessons
        # (2026-07-03 draft review, 3:31).
        strategy = Text("condition on what makes it easy - average the answers",
                        font_size=CAPTION, color=ACCENT)
        strategy.to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="Read it as strategy, not just algebra: to find a hard "
                 "expectation, condition on something that makes it easy, "
                 "then average the easy answers over what you conditioned "
                 "on. Compute in stages."
        ):
            self.play(FadeIn(strategy, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ShoppingSpree(VoiceoverScene):
    """Beat: shirts -- the random sum cracked by nested conditioning."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Worked Example: the Shopping Spree")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # A row of shirt cards, face down. Dollar amounts carry the $ sign
        # throughout the example (2026-07-03 draft review).
        cards = VGroup(*[
            RoundedRectangle(corner_radius=0.1, width=1.0, height=1.35,
                             color=MUTED).set_stroke(MUTED, 2)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.35)
        cards.move_to(DOWN * 0.35)
        n_card = MathTex(r"N \sim \text{geometric}(\tfrac{1}{2})",
                         font_size=SMALL, color=INK)
        n_card.next_to(title, DOWN, buff=0.4)
        prices = MathTex(
            r"C_i \in \{\$10, \$20, \$50\}",
            font_size=SMALL, color=MUTED,
        ).next_to(n_card, DOWN, buff=0.25)
        t_def = MathTex(r"T = \sum_{i=1}^{N} C_i",
                        font_size=SMALL, color=INK)
        t_def.next_to(cards, DOWN, buff=0.45)
        fit_to_frame(VGroup(n_card, prices, cards, t_def))

        with self.voiceover(
            text="Watch the strategy crack a problem that direct "
                 "computation would fumble. A student buys shirts. How "
                 "many? Random: N is geometric with parameter one half."
        ):
            self.play(Write(n_card), run_time=1.0)

        # The mean computation writes in while the prices are enumerated
        # (its numbers are the ones being spoken) and lingers through
        # "mean twenty-one dollars" — appearing early so its duration is
        # comfortable (2026-07-03 draft review, 3:51 + round 2, 4:07).
        mean_ci = MathTex(
            r"\mathrm{E}[C_i]", "=",
            r"\$10 \times 0.5 + \$20 \times 0.3 + \$50 \times 0.2",
            "=", r"\$21",
            font_size=SMALL, color=INK,
        ).move_to(DOWN * 0.35)
        fit_to_frame(mean_ci)
        e_ci = MathTex(r"\mathrm{E}[C_i] = \$21",
                       font_size=SMALL, color=MUTED)
        e_ci.next_to(prices, DOWN, buff=0.25)

        with self.voiceover(
            text="What does each cost? Also random: ten, twenty, or fifty "
                 "dollars with probabilities point five, point three, point "
                 "two —"
        ):
            self.play(FadeIn(prices), run_time=0.8)
            self.play(Write(mean_ci), run_time=1.6)

        with self.voiceover(text="mean twenty-one dollars —"):
            self.play(mean_ci[4].animate.set_color(ACCENT), run_time=0.6)

        with self.voiceover(
            text="independently of everything else. The total spent is a "
                 "sum with a random number of terms. What is its mean?"
        ):
            self.play(FadeOut(mean_ci), run_time=0.5)
            self.play(FadeIn(e_ci), run_time=0.6)
            self.play(LaggedStart(*[Create(c) for c in cards],
                                  lag_ratio=0.15), run_time=1.0)
            self.play(Write(t_def), run_time=0.8)

        # All five cards flip (2026-07-03 draft review, 4:15).
        labels = ["$20", "$10", "$50", "$10", "$20"]
        flips = VGroup(*[
            Text(lbl, font_size=CAPTION, color=ACCENT).move_to(cards[i])
            for i, lbl in enumerate(labels)
        ])
        cond = MathTex(r"\mathrm{E}[T \mid N] = \$21\, N",
                       font_size=BODY, color=ACCENT)
        cond.next_to(t_def, DOWN, buff=0.4)

        with self.voiceover(
            text="Condition on N. Given that the student buys n shirts, the "
                 "total is a sum of n costs, and linearity gives twenty-one "
                 "times n. So the conditional expectation of the total "
                 "given N is twenty-one N — a random variable, exactly as "
                 "this video promised."
        ):
            self.play(LaggedStart(*[FadeIn(f) for f in flips],
                                  lag_ratio=0.25), run_time=1.0)
            self.play(Write(cond), run_time=1.0)

        tower = MathTex(
            r"\mathrm{E}[T] = \mathrm{E}\left[\mathrm{E}[T \mid N]\right]"
            r"= \$21\, \mathrm{E}[N] = \$42",
            font_size=SMALL, color=INK,
        )

        with self.voiceover(
            text="Now the tower: average it. Twenty-one times the "
                 "expectation of N, and a geometric with parameter one half "
                 "has mean two. Forty-two dollars."
        ):
            # The accent conditional line leaves with the cards so the
            # tower block gets a clear stage (2026-07-03 draft review,
            # 4:36).
            self.play(FadeOut(VGroup(cards, flips, t_def, cond)),
                      run_time=0.4)
            tower.move_to(DOWN * 0.35)
            fit_to_frame(tower)
            self.play(Write(tower), run_time=1.2)

        memoryless = result_card(
            r"\mathrm{E}[N \mid N \ge 5] = 4 + \mathrm{E}[N] = 6",
            "the geometric is memoryless",
        )
        at_least = MathTex(
            r"\mathrm{E}[T \mid N \ge 5] = \$21 \times 6 = \$126",
            font_size=SMALL, color=ACCENT)
        block = VGroup(memoryless, at_least).arrange(DOWN, buff=0.35)
        block.next_to(tower, DOWN, buff=0.5)
        fit_to_frame(block)

        with self.voiceover(
            text="One more twist: given that the student buys at least five "
                 "shirts, the same tower gives twenty-one times the "
                 "conditional mean of N — and the geometric is memoryless, "
                 "so having reached five, the wait beyond four resets: four "
                 "plus two is six. Six shirts expected, one hundred "
                 "twenty-six dollars."
        ):
            self.play(FadeIn(memoryless, shift=UP * 0.2), run_time=0.8)
            self.play(Write(at_least), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["E[Y | X] is a random variable - and the tower",
             "property computes hard expectations in easy stages."],
            next_title="Independent Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video: the conditional expectation "
                 "is a random variable, and the tower property turns hard "
                 "expectations into staged easy ones."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
