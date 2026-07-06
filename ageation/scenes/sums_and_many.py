# derived_from: content/25-sums-and-many-script.md
# derived_from_sha256: 93340fb2a180584440c41f56ebf716edc5afb530e8c94fe9778815e89afd38c8
"""Chapter 7, Video 5 -- Sums of Variables.

Source notes : discrete_vectors.tex (Sections 7.6-7.7) -- convolution, the
               ordinary generating function, sums-become-products, and
               empirical sums of n variables.
Script        : content/25-sums-and-many-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/sums_and_many.py ChapterOverview
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


def bernoulli_convolutions(n: int, p: float = 0.5) -> list:
    """PMF of the sum of n Bernoulli(p) draws (index = value)."""
    pmf = [1.0]
    for _ in range(n):
        nxt = [0.0] * (len(pmf) + 1)
        for k, mass in enumerate(pmf):
            nxt[k] += mass * (1 - p)
            nxt[k + 1] += mass * p
        pmf = nxt
    return pmf


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Sums of Variables",
            ["Find the distribution of a sum: convolve the PMFs",
             "or transform, and let sums become products."],
            kicker="Chapter 7  ·  Multiple Random Variables",
        )
        tag = progress_tag(5, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Convolution", font_size=BODY, color=INK),
            Text("2.  The generating function", font_size=BODY, color=INK),
            # 2026-07-04 draft review, 0:34: on-screen text shortened
            # (narration unchanged).
            Text("3.  Empirical sums", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="This chapter ends where the rest of probability begins: "
                 "with sums of independent random variables. Sample totals, "
                 "accumulated noise, repeated trials — they are all sums."
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
            text="In this video we compute the distribution of a sum "
                 "directly, by convolving PMFs,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then meet the generating function — a transform under "
                 "which sums of variables become products of functions —"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and scale everything to n variables, watching Bernoulli "
                 "trials assemble themselves into the binomial."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Convolution(VoiceoverScene):
    """Beat: convolution -- diagonals of the dice table, factored."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The PMF of a Sum")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The 6x6 dice lattice with one anti-diagonal lit.
        n, cell = 6, 0.5
        squares = VGroup()
        lattice = [[None] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell, stroke_width=1.2,
                            stroke_color=MUTED, fill_color=BAR,
                            fill_opacity=0.12)
                sq.move_to([(j - (n - 1) / 2) * cell,
                            ((n - 1) / 2 - i) * cell, 0])
                lattice[i][j] = sq
                squares.add(sq)
        grid = VGroup(squares)
        # 2026-07-04 draft review, 0:40: both columns ride higher (title
        # stays at the top edge) to balance the vertical space.
        grid.move_to(LEFT * 3.4 + DOWN * 0.5)
        diag_label = MathTex("x + y = 7", font_size=SMALL, color=ACCENT)
        diag_label.next_to(grid, DOWN, buff=0.4)

        with self.voiceover(
            text="What is the PMF of a sum? We answered this once by brute "
                 "force. For the two dice, the pairs producing each total "
                 "lie on an anti-diagonal of the joint table — the sum's "
                 "mass collects along those diagonals."
        ):
            self.play(FadeIn(grid), run_time=0.8)
            diag = [lattice[i][j] for i in range(n) for j in range(n)
                    if (i + 1) + (j + 1) == 7]
            self.play(*[sq.animate.set_fill(ACCENT, opacity=0.6)
                        for sq in diag], FadeIn(diag_label), run_time=0.9)

        annot = MathTex(r"p_X(m)\; p_Y(k - m)", font_size=SMALL,
                        color=INK)
        annot.move_to(RIGHT * 3.2 + UP * 0.9)

        with self.voiceover(
            text="Now add last video's assumption: X and Y independent, "
                 "integer-valued. Every joint mass on the diagonal factors "
                 "into marginals, and the diagonal sum becomes: the mass "
                 "that X is m, times the mass that Y makes up the rest, k "
                 "minus m, summed over m."
        ):
            self.play(Write(annot), run_time=1.0)

        # 2026-07-04 draft review, 1:18: the convolution equation goes on
        # two lines, the sum on the second line, its "=" aligned under the
        # first line's first "=".
        formula_l1 = MathTex(
            r"p_{X+Y}(k)", "=", r"(p_X * p_Y)(k)",
            font_size=SMALL,
        )
        formula_l2 = MathTex(
            "=", r"\sum_{m} p_X(m)\, p_Y(k - m)",
            font_size=SMALL,
        )
        formula_l2.next_to(formula_l1, DOWN, buff=0.3)
        formula_l2.shift(RIGHT * (formula_l1[1].get_center()[0]
                                  - formula_l2[0].get_center()[0]))
        formula = VGroup(formula_l1, formula_l2)
        formula.move_to(RIGHT * 3.2 + DOWN * 0.9)
        fit_to_frame(formula)
        props = Text("commutative, associative", font_size=CAPTION,
                     color=MUTED)
        props.next_to(formula, DOWN, buff=0.25)

        with self.voiceover(
            text="That operation has a name — the discrete convolution of "
                 "the two PMFs — and a symbol, the star. It is commutative, "
                 "it is associative, and it answers the question "
                 "completely: for independent variables, the PMF of the sum "
                 "is the convolution of the PMFs. It is also, frankly, work "
                 "— a fresh sum for every value of k. Which is exactly why "
                 "the next idea exists."
        ):
            self.play(Write(formula), run_time=1.4)
            self.play(formula_l1[2].animate.set_color(ACCENT),
                      FadeIn(props), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GeneratingFunction(VoiceoverScene):
    """Beat: ogf -- pack the PMF into a power series; the three examples."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Generating Function")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        gdef = MathTex(
            r"G_X(z)", "=", expectation("z^X"), "=",
            r"\sum_{k=0}^{\infty} z^k\, p_X(k)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(gdef)

        values = [0.15, 0.35, 0.3, 0.2]
        chart, bars = make_pmf_chart(values, x_label="k", y_label="",
                                     y_max=0.5)
        # Chart + series ride high, level with each other (2026-07-05
        # draft review, 1:55).
        chart.scale(0.5).move_to(LEFT * 3.4 + DOWN * 1.35)
        series = MathTex(
            r"p_0 + p_1 z + p_2 z^2 + p_3 z^3",
            font_size=SMALL, color=INK,
        ).move_to(RIGHT * 3.2 + DOWN * 1.35)

        with self.voiceover(
            text="Here is one of mathematics' favorite tricks: change "
                 "representation until the hard operation becomes easy. "
                 "Take a random variable on the non-negative integers and "
                 "pack its whole PMF into one function: G of z equals the "
                 "expectation of z to the X — each mass becomes a "
                 "coefficient of a power of z. This is the ordinary "
                 "generating function, and engineers will recognize its "
                 "silhouette: it is essentially the z-transform of the PMF. Nothing is "
                 "lost — differentiate at zero and the coefficients come "
                 "back out."
        ):
            self.play(Write(gdef), run_time=1.4)
            self.play(gdef[0].animate.set_color(ACCENT), run_time=0.4)
            self.play(Create(chart[0]), Write(chart[1]),
                      run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.12), run_time=0.8)
            self.play(Write(series), run_time=1.0)

        cards = VGroup(
            result_card(r"G_X(z) = 1 - p + pz", "Bernoulli(p)"),
            result_card(r"G_S(z) = (1 - p + pz)^n", "binomial(n, p)"),
            result_card(r"G_X(z) = e^{\lambda(z - 1)}",
                        r"Poisson"),
        )

        with self.voiceover(
            text="Three generating functions carry this course. A "
                 "Bernoulli: one minus p plus p z. A binomial: that same "
                 "expression, raised to the n — remember that shape. A "
                 "Poisson: e to the lambda times z minus one."
        ):
            self.play(FadeOut(VGroup(chart, series)), run_time=0.4)
            cards.arrange(RIGHT, buff=0.55)
            cards.move_to(DOWN * 1.6)
            fit_to_frame(cards)
            for card in cards:
                self.play(FadeIn(card, shift=UP * 0.2), run_time=0.6)

        moments = MathTex(r"\mathrm{E}[X] = G_X'(1)",
                          font_size=SMALL, color=MUTED)
        moments.next_to(cards, UP, buff=0.5)

        with self.voiceover(
            text="And as a bonus, the function knows its moments: "
                 "differentiate at one and the mean falls out; "
                 "differentiate twice for the second moment. One object, "
                 "the whole distribution, all its summaries."
        ):
            self.play(FadeIn(moments), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class SumsBecomeProducts(VoiceoverScene):
    """Beat: products -- the one-line rule; Poissons merge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Sums Become Products")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # 2026-07-04 draft review, 3:02: the equation goes on two lines,
        # the second line's "=" aligned under the first line's first "=".
        # (MathTex drops empty leading parts, so the continuation line is
        # built as ("=", rhs) and aligned on part [0].)
        # 3:05: the "*" -> "\times" morph beneath it did nothing — removed.
        line1 = MathTex(
            r"G_{X+Y}(z)", "=", r"\mathrm{E}[z^X z^Y]", "=",
            r"\mathrm{E}[z^X]\, \mathrm{E}[z^Y]",
            font_size=BODY,
        )
        line2 = MathTex(
            "=", r"G_X(z)\, G_Y(z)",
            font_size=BODY,
        )
        line1.next_to(title, DOWN, buff=0.5)
        line2.next_to(line1, DOWN, buff=0.3)
        line2.shift(RIGHT * (line1[1].get_center()[0]
                             - line2[0].get_center()[0]))
        one_line = VGroup(line1, line2)
        fit_to_frame(one_line)

        with self.voiceover(
            text="Now watch the trick pay off. Take independent X and Y "
                 "and ask for the generating function of their sum. z to "
                 "the X plus Y is z to the X times z to the Y — and the "
                 "expectation of a product of independent quantities "
                 "factors, by last video's rule. One line: the generating "
                 "function of a sum is the product of the generating "
                 "functions. The convolution — all those diagonal sums — "
                 "has become a multiplication."
        ):
            self.play(Write(line1), run_time=1.4)
            self.play(Write(line2), run_time=0.8)
            self.play(line2[1].animate.set_color(ACCENT), run_time=0.5)

        # The mirror caption's final position anchors the vertical
        # centering of the Poisson element below.
        mirror = VGroup(
            # 2026-07-04 draft review, 4:02: no video-number references
            # on screen — refer to the concept instead.
            Text("split: Poisson stays Poisson",
                 font_size=CAPTION, color=MUTED),
            Text("merge: Poisson stays Poisson", font_size=CAPTION,
                 color=MUTED),
        ).arrange(DOWN, buff=0.15)
        mirror.to_edge(DOWN, buff=0.8)

        merge = MathTex(
            r"e^{\alpha(z-1)} \cdot e^{\beta(z-1)}",
            "=", r"e^{(\alpha + \beta)(z-1)}",
            font_size=SMALL,
        )
        merge_card = result_card(
            r"\text{Poisson}(\alpha) + \text{Poisson}(\beta)"
            r"= \text{Poisson}(\alpha + \beta)",
        )
        merge_card.next_to(merge, DOWN, buff=0.35)
        poisson = VGroup(merge, merge_card)
        # 2026-07-04 draft review, 3:22: the Poisson element sits halfway
        # between the equation above and the mirror lines below.
        mid_y = (one_line.get_bottom()[1] + mirror.get_top()[1]) / 2
        poisson.move_to([0, mid_y, 0])
        fit_to_frame(poisson)

        with self.voiceover(
            text="Try it on two independent Poisson streams, with rates "
                 "alpha and beta. Multiply their generating functions: the "
                 "exponents add, giving e to the alpha plus beta, z minus "
                 "one. That is itself a Poisson generating function — so "
                 "the merged stream is Poisson with rate alpha plus beta. "
                 "Two lines, no convolution in sight."
        ):
            self.play(Write(merge), run_time=1.2)
            self.play(merge[2].animate.set_color(ACCENT), run_time=0.4)
            self.play(FadeIn(merge_card, shift=UP * 0.2), run_time=0.7)

        with self.voiceover(
            # 2026-07-04 draft review, 4:02: video-number reference removed
            # from the narration — refer to the concept instead.
            text="And notice the symmetry: when we split a Poisson stream, "
                 "it stayed Poisson, and merging Poisson streams does too. "
                 "Thin or combine — the family is closed."
        ):
            self.play(FadeIn(mirror), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ManyVariables(VoiceoverScene):
    """Beat: many -- n variables, empirical sums, the Bernoulli build."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # 2026-07-04 draft review, 4:16: on-screen title only; voice
        # unchanged.
        title = section_title("Multiple Variables and Empirical Sums")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        vector = MathTex(
            r"p_{\mathbf{X}}(\mathbf{x})",
            "=", r"\prod_{k=1}^{n} p_{X_k}(x_k)",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(vector)
        indep_note = Text("independent case", font_size=CAPTION,
                          color=MUTED)
        indep_note.next_to(vector, DOWN, buff=0.2)

        with self.voiceover(
            text="Everything extends past pairs. For n random variables, "
                 "the joint PMF is the probability that all n coordinates "
                 "hit their values at once — and when the variables are "
                 "independent, it factors into n marginal terms, just as "
                 "pairs did."
        ):
            self.play(Write(vector), FadeIn(indep_note), run_time=1.2)

        sn_cards = VGroup(
            result_card(r"p_{S_n} = p_X * p_X * \cdots * p_X",
                        "n-fold convolution"),
            result_card(r"G_{S_n}(z) = G_X(z)^n", "one exponent"),
        ).arrange(RIGHT, buff=0.7)
        sn_def = MathTex(r"S_n = \sum_{k=1}^{n} X_k",
                         font_size=SMALL, color=INK)
        block = VGroup(sn_def, sn_cards).arrange(DOWN, buff=0.4)
        block.next_to(indep_note, DOWN, buff=0.45)
        fit_to_frame(block)

        with self.voiceover(
            text="The object to care about is the empirical sum: S n, the "
                 "total of n independent draws from one PMF. Build it one "
                 "variable at a time — each step convolves in one more "
                 "copy — so the PMF of S n is an n-fold convolution. Or "
                 "transform: the generating function of S n is G to the "
                 "power n. One exponent instead of n minus one "
                 "convolutions."
        ):
            self.play(Write(sn_def), run_time=0.7)
            self.play(FadeIn(sn_cards[0], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(sn_cards[1], shift=UP * 0.2), run_time=0.7)
            self.play(sn_cards[1][1].animate.set_color(ACCENT),
                      run_time=0.5)

        # 2026-07-04 draft review, 5:00: this block is re-split into
        # per-phrase sub-blocks (marks n2/n3/n4/pascal/closes) so each
        # chart morph and the caption land on their own sentence. The
        # sub-block texts concatenate verbatim to the script narration.
        def build_chart(step):
            vals = bernoulli_convolutions(step)
            new_chart, _ = make_pmf_chart(
                vals, x_label="k", y_label=r"p_{S_n}", y_max=0.6)
            new_chart.scale(0.62).to_edge(DOWN, buff=0.8)
            n_tag = MathTex(f"n = {step}", font_size=SMALL, color=INK)
            n_tag.next_to(title, DOWN, buff=0.4)
            return new_chart, n_tag

        with self.voiceover(
            text="Watch it happen. Start from a single Bernoulli trial: "
                 "two bars."
        ):
            self.play(FadeOut(VGroup(vector, indep_note, block)),
                      run_time=0.5)
            chart, tag = build_chart(1)
            self.play(Create(chart), FadeIn(tag), run_time=0.9)

        for step, phrase in (
            (2, "Convolve in a second trial,"),
            (3, "a third,"),
            (4, "a fourth — the bars spread and hump,"),
        ):
            with self.voiceover(text=phrase):
                new_chart, n_tag = build_chart(step)
                self.play(Transform(chart, new_chart),
                          Transform(tag, n_tag), run_time=1.0)

        pascal = Text("Pascal's rule, one convolution at a time",
                      font_size=CAPTION, color=MUTED)
        pascal.next_to(tag, DOWN, buff=0.3)

        with self.voiceover(
            text="and the recursion driving each step is Pascal's rule "
                 "from the combinatorics chapter."
        ):
            self.play(FadeIn(pascal), run_time=0.6)

        with self.voiceover(
            text="By induction, the sum of n Bernoulli trials is exactly "
                 "the binomial — and on the transform side, G of z to the "
                 "n is one minus p plus p z to the n, the binomial "
                 "generating function we met one beat ago. The loop closes "
                 "from both directions."
        ):
            self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # 2026-07-04 draft review, 5:45: card reads "of PMFs"; the voice
        # spells out "probability mass functions".
        outro = outro_bridge(
            ["Independence turns joints into products:",
             "PMFs, expectations, generating functions."],
            next_title="Continuous Random Variables",
        )

        with self.voiceover(
            text="The key idea of this video — and of this section: "
                 "independence turns joints into products — of probability "
                 "mass functions, of expectations, of generating functions "
                 "— and that is what makes sums of many variables "
                 "tractable. Coming up next: random variables that take a "
                 "continuum of values."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
