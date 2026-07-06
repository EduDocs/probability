# derived_from: content/15-discrete-random-variables-script.md
# derived_from_sha256: 68dbb694b59a716a3fa3973456d221a31251729fbde217137c9bd9047bd6d1da
"""Chapter 5 -- Discrete Random Variables and the PMF (narrated with manim-voiceover).

Source notes : ../chapters/discrete_random_variables.tex
Script        : content/15-discrete-random-variables-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, one per <bookmark> segment -- the same
pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/discrete_random_variables.py ChapterOverview
Final: switch make_speech_service() to OpenAIService (needs OPENAI_API_KEY).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from manim import *  # noqa: F401,F403
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.openai import OpenAIService  # final voice

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
    intro_card,
    progress_tag,
    fit_to_frame,
    configure_openai_client,
)


def make_speech_service():
    """Voice (mirrors voice: in the script YAML).

    Draft  -> GTTSService (free). Final -> OpenAIService(voice="nova"), matching
    the rest of the series; switch the lines below and add OPENAI_API_KEY.
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1", transcription_model=None)


# --- Shared visual helpers (mirroring the house style) -----------------------

def omega_box(width=4.2, height=4.2):
    """The sample-space frame: a rounded rectangle labelled Omega."""
    box = RoundedRectangle(
        corner_radius=0.2, width=width, height=height, color=MUTED
    ).set_stroke(MUTED, width=2)
    lab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    lab.next_to(box.get_corner(UL), DR, buff=0.22)
    return VGroup(box, lab)


def ball(label, color, radius=0.30, font_size=22):
    """A colored disk with a dark centered label (Chapter 2 house style)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


def die_face(n, size=0.8, color=INK, fill=None):
    """A rounded-square die face showing n pips in the standard layout (Ch 3)."""
    sq = RoundedRectangle(corner_radius=0.12, width=size, height=size)
    sq.set_stroke(color, 2.5)
    if fill is not None:
        sq.set_fill(fill, opacity=0.30)
    o = size * 0.26
    P = {
        "c": [0, 0, 0],
        "tl": [-o, o, 0], "tr": [o, o, 0],
        "bl": [-o, -o, 0], "br": [o, -o, 0],
        "ml": [-o, 0, 0], "mr": [o, 0, 0],
    }
    layout = {
        1: ["c"], 2: ["tl", "br"], 3: ["tl", "c", "br"],
        4: ["tl", "tr", "bl", "br"], 5: ["tl", "tr", "c", "bl", "br"],
        6: ["tl", "tr", "ml", "mr", "bl", "br"],
    }
    pips = VGroup(*[Dot(point=P[k], radius=size * 0.07, color=color)
                    for k in layout[n]])
    return VGroup(sq, pips)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card, recap of independence, and the outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # Manual intro card so the title reads "…and PMFs" and the objective
        # sits on two centred lines.
        intro = VGroup(
            Text("Chapter 5  ·  Discrete Random Variables",
                 font_size=SMALL, color=ACCENT),
            Text("Discrete Random Variables and PMFs", font_size=TITLE, color=INK),
            VGroup(
                Text("Turn the outcomes of an experiment into numbers,",
                     font_size=SMALL, color=MUTED),
                Text("and describe those numbers with a probability mass function.",
                     font_size=SMALL, color=MUTED),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(intro)
        tag = progress_tag(1, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Random variables as functions", font_size=SMALL, color=INK),
            Text("2.  The discrete case", font_size=SMALL, color=INK),
            Text("3.  The probability mass function", font_size=SMALL, color=INK),
            Text("4.  A worked example", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="Last chapter we studied independence — when learning one event "
                 "tells you nothing about another. Now the whole subject takes a "
                 "turn. So far outcomes have been abstract things: a face of a die, "
                 "a point in a sample space. In this chapter we attach a number to "
                 "every outcome, and that single move unlocks sums, averages, and "
                 "limits. We'll define a random variable as a function, focus on the "
                 "discrete case, and describe it completely with one object — its "
                 "probability mass function. Then we'll put a PMF to work on a small "
                 "example."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

            outline.next_to(intro, DOWN, buff=1.0)
            fit_to_frame(outline)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in outline],
                                  lag_ratio=0.3), run_time=1.4)

        self.play(*[FadeOut(m) for m in self.mobjects])


class RandomVariableMapping(VoiceoverScene):
    """Beat: rv-mapping -- X as a function from outcomes to the real line."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Random Variable is a Function")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        box_group = omega_box().shift(LEFT * 3.5 + DOWN * 0.3)
        box = box_group[0]

        # Six numbered balls (Chapter 2 style: coloured disks, dark numbers).
        colors = [RED, ORANGE, GREEN, TEAL, BLUE, PURPLE]
        offsets = [
            [-0.95, 1.0, 0], [0.75, 0.95, 0], [-0.75, -0.15, 0],
            [0.9, -0.25, 0], [-0.15, 0.25, 0], [0.25, -1.05, 0],
        ]
        outcomes = VGroup(*[
            ball(str(i + 1), colors[i], radius=0.26).move_to(
                box.get_center() + np.array(off))
            for i, off in enumerate(offsets)
        ])

        line = NumberLine(
            x_range=[0, 6, 1], length=4.5, include_numbers=True, font_size=22,
        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        rlabel = MathTex(r"\mathbb{R}", font_size=BODY).next_to(line, UP, buff=0.3)

        # Two outcomes deliberately share the target 4 (many-to-one).
        targets = [1, 4, 2, 4, 3, 5]
        arrows = VGroup()
        for grp, t in zip(outcomes, targets):
            arrows.add(CurvedArrow(
                grp.get_center() + RIGHT * 0.45,
                line.number_to_point(t),
                angle=-PI / 6, color=ACCENT, stroke_width=3, tip_length=0.18,
            ))

        # A small die aside: rolling a die maps an outcome to a number of dots.
        # Uses the Chapter 3 pip die instead of a boxed numeral.
        die = die_face(5, size=0.8)
        die_map = MathTex(r"\mapsto", font_size=SMALL, color=MUTED)
        die_val = MathTex(r"5", font_size=SMALL, color=ACCENT)
        die_row = VGroup(die, die_map, die_val).arrange(RIGHT, buff=0.25)
        die_cap = Text("roll a die: outcome to dots", font_size=CAPTION, color=MUTED)
        die_aside = VGroup(die_row, die_cap).arrange(DOWN, buff=0.2)
        die_aside.shift(RIGHT * 3.0 + UP * 2.0)
        fit_to_frame(die_aside)

        target_dot = Dot(line.number_to_point(4), radius=0.12, color=ACCENT)

        # The yellow definition sits centred below the real-number axis.
        defn = MathTex(r"X : \Omega \to \mathbb{R}", font_size=BODY, color=ACCENT)
        defn.next_to(line, DOWN, buff=0.6)

        with self.voiceover(
            text="Here is a sample space Omega, with a handful of outcomes."
        ):
            self.play(Create(box), Write(box_group[1]))
            self.play(LaggedStartMap(FadeIn, outcomes, lag_ratio=0.2))

        with self.voiceover(
            text="A random variable is nothing mysterious: it is simply a function "
                 "that sends each outcome to a point on the real line. Roll a die, "
                 "and the natural random variable is the number of dots on the top "
                 "face — outcome to number."
        ):
            self.play(Create(line), Write(rlabel))
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.25),
                      run_time=2)
            self.play(FadeIn(die_aside, shift=UP * 0.1))

        with self.voiceover(
            text="Notice that different outcomes are allowed to land on the same "
                 "number; the map need not be one-to-one."
        ):
            self.play(Indicate(VGroup(arrows[1], arrows[3]), color=ACCENT))
            self.play(FadeIn(target_dot, scale=1.5), Indicate(target_dot, color=ACCENT))

        with self.voiceover(
            text="Formally, we write X maps Omega to the real numbers. That real "
                 "number attached to an outcome is called the value of the random "
                 "variable."
        ):
            self.play(Write(defn))

        self.play(*[FadeOut(m) for m in self.mobjects])


class DiscreteRandomVariable(VoiceoverScene):
    """Beat: discrete-rv -- finite vs countably-infinite ranges."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Discrete Case")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        finite_group = VGroup(
            MathTex(r"X(\Omega) = \{1, \dots, 6\}", font_size=SECTION, color=ACCENT),
            Text("finite range - a die", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.3)

        countable_group = VGroup(
            MathTex(r"X(\Omega) = \{1, 2, 3, \dots\}", font_size=SECTION,
                    color=ACCENT),
            Text("countably infinite - toss a coin until the first head",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.3)

        both = VGroup(finite_group, countable_group).arrange(DOWN, buff=1.1)
        both.next_to(title, DOWN, buff=0.8)
        fit_to_frame(both)

        with self.voiceover(
            text="The random variables we study first are the discrete ones. A "
                 "random variable is discrete when its range — the set of values it "
                 "can take — is finite or countable. A die gives a finite range, one "
                 "through six."
        ):
            self.play(Write(finite_group[0]))
            self.play(FadeIn(finite_group[1], shift=UP * 0.1))

        with self.voiceover(
            text="But discrete does not mean finite. Toss a coin repeatedly until the "
                 "first head, and record how many tosses it took. That count can be "
                 "one, two, three, and on forever — a countably infinite range. Both "
                 "are discrete; what they share is that we can list their values one "
                 "by one."
        ):
            self.play(Write(countable_group[0]))
            self.play(FadeIn(countable_group[1], shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class PMFDefinition(VoiceoverScene):
    """Beat: pmf-definition -- mass, preimage, normalization, and set probability."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Probability Mass Function")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        define = MathTex(
            r"p_X(x)", r"=", pr("X = x"),
            font_size=SECTION, color=ACCENT,
        )
        define.move_to(UP * 0.5)
        fit_to_frame(define)

        with self.voiceover(
            text="To describe a discrete random variable completely, we only need to "
                 "say how much probability sits on each value. That is the "
                 "probability mass function. The mass of x, written little-p sub-X of "
                 "x, is just the probability that X equals x."
        ):
            self.play(Write(define))

        self.play(define.animate.next_to(title, DOWN, buff=0.35).scale(0.8))

        # Omega box on the left with a shaded preimage; formulas stack on the right.
        box_group = omega_box(width=3.6, height=3.4).shift(LEFT * 3.6 + DOWN * 0.6)
        box = box_group[0]
        c = box.get_center()
        # Three clustered outcomes make up the preimage of x; three sit apart.
        cluster = [c + np.array(p) for p in
                   [[-0.55, 0.5, 0], [-0.8, -0.2, 0], [-0.3, -0.1, 0]]]
        others = [c + np.array(p) for p in
                  [[0.7, 0.6, 0], [0.85, -0.55, 0], [0.35, -1.0, 0]]]
        pal = [RED, ORANGE, GREEN, TEAL, BLUE, PURPLE]
        dot_positions = cluster + others
        dots = VGroup(*[
            ball(str(i + 1), pal[i], radius=0.19).move_to(p)
            for i, p in enumerate(dot_positions)])
        # The preimage of x: the three outcomes X sends to x, fully enclosed.
        pre_center = (cluster[0] + cluster[1] + cluster[2]) / 3
        preimage = Ellipse(width=1.7, height=1.75, color=ACCENT)
        preimage.set_stroke(ACCENT, 3).set_fill(ACCENT, 0.18)
        preimage.move_to(pre_center).set_z_index(-1)
        pre_lab = MathTex(r"\{\omega : X(\omega) = x\}", font_size=CAPTION,
                          color=ACCENT)
        pre_lab.next_to(box, DOWN, buff=0.2)
        pre_pic = VGroup(box_group, dots, preimage, pre_lab)
        fit_to_frame(pre_pic)

        pre_tex = MathTex(r"\Pr(X = x) = \Pr\!\left(X^{-1}(x)\right)",
                          font_size=SMALL, color=INK)
        norm_tex = MathTex(r"\sum_{x \in X(\Omega)} p_X(x) = 1",
                           font_size=SMALL, color=INK)
        set_tex = MathTex(r"\Pr(X \in S) = \sum_{x \in S} p_X(x)",
                          font_size=SMALL, color=ACCENT)
        formulas = VGroup(pre_tex, norm_tex, set_tex).arrange(
            DOWN, aligned_edge=LEFT, buff=0.7
        )
        formulas.shift(RIGHT * 3.0 + DOWN * 0.6)
        fit_to_frame(formulas)

        with self.voiceover(
            text="And \"X equals x\" is really an event back in the sample space: the "
                 "set of all outcomes that X maps to x. That set is the preimage of "
                 "x, and its probability is the mass. So the PMF simply pushes the "
                 "probability law forward, from the sample space onto the number line."
        ):
            self.play(Create(box), Write(box_group[1]))
            self.play(LaggedStartMap(FadeIn, dots, lag_ratio=0.1))
            self.play(Create(preimage), Write(pre_lab))
            self.play(Write(pre_tex))

        with self.voiceover(
            text="As x ranges over all the values, these preimages are disjoint and "
                 "cover the whole sample space — they partition it — so the masses "
                 "must add up to exactly one."
        ):
            self.play(Write(norm_tex))

        with self.voiceover(
            text="And once we have the PMF, the probability that X lands anywhere in "
                 "a set S is just the sum of the masses over S. The PMF is the whole "
                 "story."
        ):
            self.play(Write(set_tex))

        self.play(*[FadeOut(m) for m in self.mobjects])


class UrnExample(VoiceoverScene):
    """Beat: urn-example -- draw two of three balls, PMF of the sum, then close."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Worked Example")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # The six equally likely ordered draws and their sums.
        pairs = [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
        rows = VGroup(*[
            MathTex(rf"({a},{b}) \to {a + b}", font_size=SMALL, color=INK)
            for a, b in pairs
        ]).arrange_in_grid(rows=3, cols=2, buff=(0.6, 0.3))
        setup_cap = VGroup(
            Text("draw 2 of 3 without replacement,", font_size=CAPTION, color=MUTED),
            Text("keep the order", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.15)
        setup_cap.next_to(rows, DOWN, buff=0.35)
        xdef = MathTex(r"X = \text{sum of the two draws}", font_size=SMALL,
                       color=ACCENT)
        xdef.next_to(setup_cap, DOWN, buff=0.3)
        setup = VGroup(rows, setup_cap, xdef).move_to(LEFT * 3.3 + DOWN * 0.4)
        fit_to_frame(setup)

        with self.voiceover(
            text="Let's make it concrete. An urn holds three balls, numbered one, "
                 "two, and three. We draw two of them without replacement, and we "
                 "record the order — so there are six equally likely outcomes. Let "
                 "the random variable X be the sum of the two numbers drawn."
        ):
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in rows],
                                  lag_ratio=0.15), run_time=1.6)
            self.play(FadeIn(setup_cap, shift=UP * 0.1))
            self.play(Write(xdef))

        # PMF: mass 1/3 on each of 3, 4, 5. Leading zeros put bars at x = 3, 4, 5.
        chart, bars = make_pmf_chart(
            [0, 0, 0, 1 / 3, 1 / 3, 1 / 3], x_label="x", y_label=r"p_X(x)",
        )
        chart.scale(0.72).move_to(RIGHT * 3.2 + DOWN * 0.3)
        fit_to_frame(chart)

        with self.voiceover(
            text="Work out the sums: they can only be three, four, or five, and each "
                 "occurs for exactly two of the six outcomes. So the PMF is one-third "
                 "on three, one-third on four, one-third on five."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=1.0)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.15), run_time=1.2)

        odd_tex = MathTex(
            r"\Pr(\text{odd}) = \tfrac13 + \tfrac13 = \tfrac23",
            font_size=BODY, color=ACCENT,
        )
        odd_tex.next_to(chart, DOWN, buff=0.3)
        fit_to_frame(odd_tex)

        with self.voiceover(
            text="Now suppose we want the probability that the sum is odd. The odd "
                 "values are three and five, so we just add their masses: one-third "
                 "plus one-third is two-thirds."
        ):
            # bars[0] is x=3, bars[1] is x=4, bars[2] is x=5.
            self.play(bars[0].animate.set_fill(ACCENT, 0.9),
                      bars[2].animate.set_fill(ACCENT, 0.9))
            self.play(Write(odd_tex))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- outro: key idea + bridge to the named distributions. ---
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            MathTex(r"p_X(x) = \Pr(X = x)", font_size=BODY, color=INK),
            Text("A discrete random variable is completely described by its PMF.",
                 font_size=SMALL, color=MUTED),
            Text("Coming up:  named distributions", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.45)
        fit_to_frame(outro)

        with self.voiceover(
            text="That is the pattern for the whole chapter — build the PMF, then sum "
                 "the mass over the values you care about. A discrete random variable "
                 "is completely described by its probability mass function. Next, we "
                 "meet named distributions."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(outro[3], shift=UP * 0.15), run_time=0.6)

        self.wait(0.5)
        self.play(FadeOut(outro))
