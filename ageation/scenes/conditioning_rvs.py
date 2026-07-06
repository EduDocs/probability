# derived_from: content/22-conditioning-rvs-script.md
# derived_from_sha256: bf900ba31935dcaad0e19a05d07047181ebfe2ac0666449bf8d8ec6e6daf5c55
"""Chapter 7, Video 2 -- Conditioning Random Variables.

Source notes : discrete_vectors.tex (Section 7.3, both subsections) --
               conditioning on events and on random variables, the product
               rule, and the Poisson-splitting example.
Script        : content/22-conditioning-rvs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/conditioning_rvs.py ChapterOverview
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
    make_pmf_chart,
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


WITHOUT_TABLE = [
    [r"p_{X,Y}", "1", "2", "3"],
    ["1", "0", r"\tfrac{1}{6}", r"\tfrac{1}{6}"],
    ["2", r"\tfrac{1}{6}", "0", r"\tfrac{1}{6}"],
    ["3", r"\tfrac{1}{6}", r"\tfrac{1}{6}", "0"],
]
# Conditional rows p_{Y|X}(.|x) for the without-replacement urn.
COND_ROWS = {
    1: ["0", r"\tfrac{1}{2}", r"\tfrac{1}{2}"],
    2: [r"\tfrac{1}{2}", "0", r"\tfrac{1}{2}"],
    3: [r"\tfrac{1}{2}", r"\tfrac{1}{2}", "0"],
}


def x_tiling(width=4.6, height=2.7):
    """Omega sliced into the disjoint {X = x} tiles.

    The Total Probability figure (chapter 4 video), relabelled: returns
    VGroup(outer, olab, tiles, labels) so callers can animate the border,
    the Omega label, the coloured tiles, and the X = x labels apart.
    """
    outer = Rectangle(width=width, height=height, color=MUTED)
    outer.set_stroke(MUTED, 2)
    olab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    olab.next_to(outer.get_corner(UL), UP, buff=0.15)

    cols = [BLUE, TEAL, GREEN]
    names = [r"X{=}1", r"X{=}2", r"X{=}3"]
    tw = width / 3.0
    left = outer.get_left()[0]
    cy = outer.get_center()[1]

    tiles = VGroup()
    labels = VGroup()
    for i, (col, nm) in enumerate(zip(cols, names)):
        cx = left + tw * (i + 0.5)
        tile = Rectangle(
            width=tw, height=height,
            fill_color=col, fill_opacity=0.25,
            stroke_color=INK, stroke_width=1.5,
        ).move_to([cx, cy, 0])
        tiles.add(tile)
        labels.add(MathTex(nm, font_size=CAPTION, color=INK)
                   .move_to([cx, cy + height * 0.36, 0]))

    return VGroup(outer, olab, tiles, labels)


def cond_chart(probs, labels, x_label_texs=("1", "2", "3"),
               unit=2.4, bar_w=0.55, gap=1.1):
    """A small conditional-PMF bar chart: baseline, bars, mass labels.

    Returns VGroup(baseline, bars, mass_labels, x_labels); zero-mass values
    keep a ghost sliver so Transform stays structurally aligned.
    """
    n = len(probs)
    span = gap * (n - 1) + bar_w + 0.8
    baseline = Line(LEFT * span / 2, RIGHT * span / 2,
                    color=MUTED, stroke_width=2)
    bars, mlabels, xlabels = VGroup(), VGroup(), VGroup()
    for i, (p_val, lab) in enumerate(zip(probs, labels)):
        cx = -gap * (n - 1) / 2 + gap * i
        h = max(unit * p_val, 0.02)
        bar = Rectangle(width=bar_w, height=h,
                        fill_color=BAR, stroke_color=BAR, stroke_width=1.5,
                        fill_opacity=0.85 if p_val > 0 else 0.15)
        if p_val == 0:
            bar.set_stroke(opacity=0.3)
        bar.move_to([cx, h / 2, 0])
        bars.add(bar)
        mlab = MathTex(lab, font_size=CAPTION, color=INK)
        mlab.next_to(bar, UP, buff=0.15)
        mlabels.add(mlab)
        xlab = MathTex(x_label_texs[i], font_size=CAPTION, color=MUTED)
        xlab.next_to([cx, 0, 0], DOWN, buff=0.2)
        xlabels.add(xlab)
    chart = VGroup(baseline, bars, mlabels, xlabels)
    mark_intended_overlap(baseline, bars,
                          reason="bars stand on the chart baseline")
    return chart


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
            "Conditioning Random Variables",
            ["Update a random variable's PMF by what you observe -",
             "slice the joint table and renormalize."],
            kicker="Chapter 7  ·  Multiple Random Variables",
        )
        tag = progress_tag(2, 5).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Conditioning on an event", font_size=BODY, color=INK),
            Text("2.  Conditioning on a random variable",
                 font_size=BODY, color=INK),
            Text("3.  Splitting a Poisson", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Dependence is why we build joint models — and conditioning "
                 "is how we use it: observe something, update everything "
                 "else."
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
            text="In this video we condition a random variable on an event, "
                 "and watch a familiar ratio produce a genuine PMF,"
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="then condition on another random variable — which turns "
                 "out to be a slice of last video's table, renormalized —"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and put the machinery to work on a result that deserves "
                 "to be famous: thinning a Poisson stream leaves it Poisson."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionOnEvent(VoiceoverScene):
    """Beat: on-events -- the ratio, validity, and the truncated geometric."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning on an Event")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        ratio = MathTex(
            r"p_{X \mid S}(x)", "=",
            r"\frac{\Pr\left(\{X = x\} \cap S\right)}{\Pr\left(S\right)}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.45)
        fit_to_frame(ratio)

        with self.voiceover(
            text="Chapter four defined the conditional probability of one "
                 "event given another. Random variables inherit it directly."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="The conditional PMF of X given an event S weighs each "
                 "value by the same ratio: the probability that X equals x "
                 "and S happens, over the probability of S."
        ):
            self.play(Write(ratio), run_time=1.4)
            self.play(ratio[0].animate.set_color(ACCENT), run_time=0.5)

        # Validity: the Total Probability tiling — {X = x} tiles crossed
        # by a translucent S (2026-07-03 draft review, 1:04).
        tiling = x_tiling(width=4.6, height=2.7)
        tiling.move_to(LEFT * 3.3 + DOWN * 1.4)
        outer, olab, tiles, tlabels = tiling
        s_event = Ellipse(
            width=outer.width * 0.84, height=outer.height * 0.52,
            fill_color=MAROON, fill_opacity=0.30,
            stroke_color=MAROON, stroke_width=1.5,
        ).move_to(outer.get_center() + DOWN * 0.25)
        s_label = MathTex("S", font_size=SMALL, color=MAROON)
        s_label.move_to(s_event.get_center() + RIGHT * 1.45)
        pieces = VGroup(*[
            Intersection(s_event, tile).set_stroke(ACCENT, 2.5)
            .set_fill(opacity=0.0)
            for tile in tiles
        ])
        mark_intended_overlap(tiling, s_event, s_label, pieces,
                              reason="partition tiles crossed by S")
        valid = MathTex(r"\sum_{x} p_{X \mid S}(x)", "=", "1",
                        font_size=BODY, color=INK)
        valid.move_to(RIGHT * 3.3 + DOWN * 1.4)

        with self.voiceover(
            text="Is this still a PMF? Yes — and the reason is elegant. The "
                 "events \"X equals x\" partition the sample space, so by "
                 "the total probability theorem their intersections with S "
                 "add up to the probability of S itself. Divide, and the "
                 "conditional masses sum to exactly one."
        ):
            self.play(Create(outer), Write(olab), run_time=0.7)
            self.play(FadeIn(tiles), FadeIn(tlabels), run_time=0.8)
            self.play(FadeIn(s_event), Write(s_label), run_time=0.7)
            self.play(LaggedStart(*[Create(p) for p in pieces],
                                  lag_ratio=0.3), run_time=1.0)
            self.play(Write(valid), run_time=0.8)

        self.play(FadeOut(VGroup(tiling, s_event, s_label, pieces, valid)),
                  run_time=0.5)

        # The truncated geometric: bars beyond n fade, the rest renormalize.
        p, n_cut = 0.5, 4
        values = [0.0] + [(1 - p) ** (k - 1) * p for k in range(1, 9)]
        chart, bars = make_pmf_chart(values, x_label="k", y_label=r"p(k)")
        chart.scale(0.62).to_edge(DOWN, buff=0.8)

        # Per-phrase sub-blocks so each animation lands on its sentence
        # (2026-07-03 draft review, 1:40).
        with self.voiceover(
            text="Here is the picture to keep. A packet is retransmitted "
                 "until it gets through, so the number of trials is "
                 "geometric."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                                  lag_ratio=0.1), run_time=1.0)

        axes = chart[0]
        cut_x = (bars[n_cut - 1].get_right()[0]
                 + bars[n_cut].get_left()[0]) / 2
        cut_line = DashedLine(
            [cut_x, axes.c2p(0, 0)[1], 0],
            [cut_x, axes.c2p(0, 0.58)[1], 0],
            color=ACCENT, stroke_width=2.5, dash_length=0.12,
        )
        cut_label = MathTex("n", font_size=SMALL, color=ACCENT)
        cut_label.next_to(cut_line, UP, buff=0.12)
        mark_intended_overlap(cut_line, chart,
                              reason="cutoff line rises from the x-axis")

        with self.voiceover(
            text="But this system gives up after n failures. Given that "
                 "the packet made it, what does the trial count look like?"
        ):
            self.play(Create(cut_line), FadeIn(cut_label), run_time=0.8)

        with self.voiceover(
            text="Only the first n bars survive."
        ):
            self.play(*[b.animate.set_fill(opacity=0.12)
                        for b in bars[n_cut:]], run_time=0.9)

        scale = 1.0 / (1.0 - (1.0 - p) ** n_cut)
        formula = MathTex(
            r"p_{Y \mid S}(k)", "=",
            r"\frac{(1-p)^{k-1} p}{1 - (1-p)^n}",
            font_size=SMALL,
        ).next_to(ratio, DOWN, buff=0.35)
        fit_to_frame(formula)

        with self.voiceover(
            text="Their shape is untouched — each one is divided by the "
                 "same number, the probability of success, one minus one "
                 "minus p to the n."
        ):
            self.play(ratio[0].animate.set_color(INK),
                      Write(formula), run_time=1.0)
            self.play(formula[2].animate.set_color(ACCENT), run_time=0.5)

        with self.voiceover(
            text="Conditioning kept the geometry and rescaled the mass: "
                 "the bars beyond n vanish, the rest grow just enough to "
                 "carry mass one."
        ):
            self.play(*[b.animate.stretch(scale, 1,
                                          about_point=b.get_bottom())
                        for b in bars[:n_cut]], run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionOnRV(VoiceoverScene):
    """Beat: on-rvs -- slice the table, the formula, the family."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning on a Random Variable")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Table and formula raised; the conditional slice is a small bar
        # chart, not a number row (2026-07-03 draft review, 2:33).
        table = style_headers(mass_table(WITHOUT_TABLE))
        table.scale(0.9).move_to(LEFT * 3.1 + UP * 0.35)

        with self.voiceover(
            text="Now condition on information of a richer kind: the "
                 "observed value of another random variable."
        ):
            self.play(Create(table[0]), FadeIn(table[1]), run_time=1.0)

        # Lift row X=1 out beneath as raw masses, then renormalize.
        # Charts align on the baseline (chart[0]) so Transforms don't
        # drift; the chart sits right of the table's column so its mass
        # labels never touch the table frame (2026-07-03 draft review
        # round 2, 2:34/2:51).
        baseline_at = DOWN * 2.5 + RIGHT * 0.9

        def place(chart):
            return chart.shift(baseline_at - chart[0].get_center())

        raw = place(cond_chart([0, 1 / 6, 1 / 6],
                               ["0", r"\tfrac{1}{6}", r"\tfrac{1}{6}"]))
        cond = place(cond_chart([0, 1 / 2, 1 / 2], COND_ROWS[1]))
        lifted_head = MathTex(r"p_{Y \mid X}(\cdot \mid 1)",
                              font_size=SMALL, color=ACCENT)
        lifted_head.next_to(raw, LEFT, buff=0.7)

        # Per-phrase sub-blocks so each step lands on its sentence
        # (2026-07-03 draft review round 2, 2:34).
        with self.voiceover(
            text="Go back to the joint table. Observing X equals x means "
                 "the experiment landed somewhere in one row."
        ):
            row = VGroup(*[table.cells[1][j] for j in range(1, 4)])
            self.play(LaggedStart(*[Indicate(c, color=ACCENT) for c in row],
                                  lag_ratio=0.2), run_time=1.2)

        with self.voiceover(
            text="So keep that row — and forget the rest."
        ):
            others = VGroup(*[table.cells[i][j]
                              for i in (2, 3) for j in range(1, 4)])
            self.play(others.animate.set_opacity(0.25), run_time=0.6)

        with self.voiceover(
            text="The row's masses don't sum to one,"
        ):
            self.play(FadeIn(lifted_head), Create(raw[0]),
                      FadeIn(raw[3]), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in raw[1]],
                                  lag_ratio=0.2),
                      FadeIn(raw[2]), run_time=0.9)

        with self.voiceover(
            text="but we know the fix: divide by the row total, which is "
                 "exactly the marginal of X at x."
        ):
            self.play(Transform(raw, cond), run_time=1.0)

        formula = MathTex(
            r"p_{Y \mid X}(y \mid x)", "=",
            r"\frac{p_{X,Y}(x, y)}{p_X(x)}",
            font_size=BODY,
        ).move_to(RIGHT * 3.4 + UP * 0.5)
        fit_to_frame(formula)
        defined = Text("defined when p(x) > 0", font_size=CAPTION,
                       color=MUTED)
        defined.next_to(formula, DOWN, buff=0.25)

        with self.voiceover(
            text="That is the whole definition. The conditional PMF of Y "
                 "given X equals x is the joint mass over the marginal mass "
                 "— defined whenever the marginal is positive, because "
                 "conditioning on something that cannot happen means "
                 "nothing."
        ):
            self.play(Write(formula), run_time=1.4)
            self.play(formula[0].animate.set_color(ACCENT),
                      FadeIn(defined), run_time=0.7)

        with self.voiceover(
            text="And notice the plural: every value of x carves its own "
                 "row and its own conditional PMF. Conditioning on a random "
                 "variable hands you a whole family of distributions, "
                 "indexed by what you might observe. Slide the observation, "
                 "and the distribution of Y responds — that responsiveness "
                 "is dependence, made visible."
        ):
            for x in (2, 3):
                new_head = MathTex(
                    r"p_{Y \mid X}(\cdot \mid " + str(x) + ")",
                    font_size=SMALL, color=ACCENT).move_to(lifted_head)
                probs = [0 if s == "0" else 1 / 2 for s in COND_ROWS[x]]
                new_chart = place(cond_chart(probs, COND_ROWS[x]))
                self.play(
                    table[1].animate.set_opacity(1.0), run_time=0.3)
                others = VGroup(*[table.cells[i][j]
                                  for i in range(1, 4) if i != x
                                  for j in range(1, 4)])
                self.play(others.animate.set_opacity(0.25),
                          Transform(lifted_head, new_head),
                          Transform(raw, new_chart), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])


class EventVsRV(VoiceoverScene):
    """Beat: two-views -- the indicator bridge and the product rule."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Two Views, One Idea")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        indicator = MathTex(
            r"p_{X \mid S}(x)", "=",
            r"p_{X \mid \mathbf{1}_S}(x \mid 1)",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.55)
        fit_to_frame(indicator)
        ind_note = MathTex(
            r"\mathbf{1}_S(\omega) = \begin{cases} 1, & \omega \in S \\"
            r" 0, & \omega \notin S \end{cases}",
            font_size=SMALL, color=MUTED,
        ).next_to(indicator, DOWN, buff=0.35)

        with self.voiceover(
            text="Two kinds of conditioning, then — on events and on random "
                 "variables. They are the same idea in two dresses."
        ):
            self.wait(0.3)

        with self.voiceover(
            text="Any event S has an indicator variable: one when S "
                 "happens, zero when it doesn't. Conditioning on S is "
                 "precisely conditioning on that variable taking the value "
                 "one. And conditioning on X equals x is just conditioning "
                 "on an event. Each view contains the other."
        ):
            self.play(Write(indicator), run_time=1.2)
            self.play(FadeIn(ind_note), run_time=0.7)

        product = MathTex(
            r"p_{X,Y}(x, y)", "=",
            r"p_{Y \mid X}(y \mid x)\; p_X(x)",
            font_size=BODY,
        ).next_to(ind_note, DOWN, buff=0.6)
        fit_to_frame(product)
        seq_note = Text("build joints the way experiments unfold",
                        font_size=CAPTION, color=MUTED)
        seq_note.next_to(product, DOWN, buff=0.25)

        with self.voiceover(
            text="One more gift before the payoff: read the slice formula "
                 "backwards. The joint mass equals the conditional times "
                 "the marginal. That is the product rule — and it means "
                 "joint distributions can be built the way experiments "
                 "actually unfold: first draw, then second draw given the "
                 "first."
        ):
            self.play(Write(product), run_time=1.2)
            self.play(product[0].animate.set_color(ACCENT),
                      FadeIn(seq_note), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class PoissonSplitting(VoiceoverScene):
    """Beat: splitting -- thinning a Poisson stream leaves it Poisson."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Splitting a Poisson")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # A stream of bits: exponential-looking inter-arrival gaps (Poisson
        # process feel), sitting halfway between the K card and the binomial
        # PMF (2026-07-03 draft review, 4:35).
        k_card = MathTex(r"K \sim \text{Poisson}(\lambda)",
                         font_size=SMALL, color=INK)
        k_card.next_to(title, DOWN, buff=0.4)
        given = MathTex(
            r"p_{M \mid K}(m \mid k)", "=",
            r"\binom{k}{m} p^m (1-p)^{k-m}",
            font_size=SMALL,
        ).next_to(k_card, DOWN, buff=1.4)
        fit_to_frame(given)

        rng_ones = {1, 3, 4, 7, 10}
        gaps = [0.55, 0.3, 1.45, 0.5, 1.0, 0.35, 1.9, 0.6, 1.2, 0.45, 0.9]
        xs = [-4.9]
        for g in gaps:
            xs.append(xs[-1] + g)
        stream_y = (k_card.get_bottom()[1] + given.get_top()[1]) / 2
        dots = VGroup(*[
            Dot(radius=0.11, color=INK).move_to([x, stream_y, 0])
            for x in xs
        ])

        with self.voiceover(
            text="Now let the machinery earn its keep. A transmitter sends "
                 "bits: each is a one with probability p, a zero otherwise, "
                 "independently — and the number of bits sent in an "
                 "interval is Poisson with parameter lambda. Question: what "
                 "is the distribution of the number of ones?"
        ):
            self.play(FadeIn(k_card), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots],
                                  lag_ratio=0.06), run_time=1.2)
            self.play(*[d.animate.set_color(
                        ACCENT if i in rng_ones else MUTED)
                        for i, d in enumerate(dots)], run_time=1.0)

        with self.voiceover(
            text="Condition on the total. Given that k bits were sent, each "
                 "independently a one with probability p, the count of ones "
                 "is binomial with parameters k and p — that much we have "
                 "known since chapter five."
        ):
            self.play(Write(given), run_time=1.2)

        lines = VGroup(
            MathTex(r"p_M(m) = \sum_{k} p_{M \mid K}(m \mid k)\, p_K(k)",
                    font_size=SMALL, color=INK),
            MathTex(r"= \frac{(\lambda p)^m}{m!} e^{-\lambda}"
                    r"\sum_{u=0}^{\infty} \frac{((1-p)\lambda)^u}{u!}",
                    font_size=SMALL, color=MUTED),
            MathTex(r"p_M(m) = \frac{(\lambda p)^m}{m!}\, e^{-\lambda p}",
                    font_size=BODY, color=ACCENT),
        ).arrange(DOWN, buff=0.3)
        lines.next_to(given, DOWN, buff=0.4)
        fit_to_frame(lines)

        with self.voiceover(
            text="Now un-condition with the product rule: the mass of m "
                 "ones sums the binomial times the Poisson over all totals "
                 "k. Shift the index, and the sum telescopes into the "
                 "series for an exponential. What remains is unmistakable: "
                 "lambda p to the m over m factorial, times e to the minus "
                 "lambda p. The number of ones is Poisson with parameter p "
                 "times lambda. Thin a Poisson stream at random, and it "
                 "stays Poisson — just slower."
        ):
            self.play(Write(lines[0]), run_time=1.0)
            self.play(FadeIn(lines[1]), run_time=0.9)
            self.play(Write(lines[2]), run_time=1.1)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Conditioning slices the joint and renormalizes -",
             "run backwards, it builds joints one stage at a time."],
            next_title="Conditional Expectation",
        )

        with self.voiceover(
            text="The key idea of this video: conditioning is slicing the "
                 "joint and renormalizing — and run backwards, it builds "
                 "joint models one stage at a time."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
