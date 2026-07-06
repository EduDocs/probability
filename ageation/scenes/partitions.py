# derived_from: content/05-partitions-script.md
# derived_from_sha256: 8044f9e2bca2f49ca40d975692fbdd88abe778a872e5aaaebb92d94159c50974
"""Chapter 2, Video 3 -- Partitions and Stars and Bars (manim-voiceover).

Source notes : ../chapters/combinatorics.tex  (2.4 Partitions, 2.4.1 Integer
               Solutions to Linear Equations)
Script        : content/05-partitions-script.md

Bookmark-free timing (sequential voiceover blocks), same as the earlier
Chapter 2 videos. Draft uses gTTS; switch make_speech_service() to
OpenAIService(nova) for the final.
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
    section_title,
    intro_card,
    progress_tag,
    fit_to_frame,
    configure_openai_client,
)


def make_speech_service():
    """Draft -> GTTSService (free). Final -> OpenAIService(voice="nova")."""
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


def ball(label, color, radius=0.32, font_size=22):
    """A colored disk with a dark centered label (Chapter 1 house style)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


BALL_COLORS = [RED, BLUE, GREEN, GRAY_B, ORANGE, PURPLE]


def star(font_size=BODY):
    return MathTex(r"\bigstar", font_size=font_size, color=ACCENT)


def bar(font_size=BODY):
    return MathTex(r"\mid", font_size=font_size, color=INK)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap, title, outline by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Partitions & Stars and Bars",
            "Split a set into several labeled groups, and share a total among r bins.",
            kicker="Chapter 2  ·  Combinatorics",
        )
        fit_to_frame(intro)
        tag = progress_tag(3, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="Last video, we counted permutations and combinations — ordered "
                 "arrangements versus unordered selections. A combination split a "
                 "set in two: the chosen and the rest."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)

        self.wait(0.7)  # a longer beat before pivoting to this video

        with self.voiceover(
            text="In this video, we split a set into several groups at once."
        ):
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Partitions  —  the multinomial coefficient", font_size=BODY),
            Text("2.  Stars and bars  —  sharing a total among bins", font_size=BODY),
            Text("3.  One more sampling count:  with replacement, unordered",
                 font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.8)
        fit_to_frame(items)

        clauses = [
            "We start with partitions and the multinomial coefficient;",
            "then stars and bars, a picture for counting how a total can be "
            "shared among several bins;",
            "and one more sampling count, drawing with replacement but ignoring "
            "order.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Partitions(VoiceoverScene):
    """Beat: partitions -- arrange n!, divide by group orderings; 6 -> 3,2,1 = 60."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Partitions")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        two_way = MathTex(
            r"\binom{n}{k}:\quad n \;=\; \underbrace{k}_{\text{chosen}}"
            r" \;+\; \underbrace{n-k}_{\text{left}}",
            font_size=BODY, color=MUTED,
        ).next_to(title, DOWN, buff=0.7)
        fit_to_frame(two_way)
        with self.voiceover(
            text="A combination splits a set into two parts — the k chosen and the "
                 "n minus k left behind. But often we want more parts at once."
        ):
            self.play(Write(two_way))

        self.play(FadeOut(two_way))

        # Six numbered balls -> a row.
        balls = VGroup(*[ball(str(i + 1), BALL_COLORS[i], radius=0.3, font_size=20)
                         for i in range(6)])
        balls.arrange(RIGHT, buff=0.35).move_to(UP * 1.4)
        fit_to_frame(balls)
        prompt = Text("Split 6 items into groups of sizes  3, 2, 1",
                      font_size=SMALL, color=INK).next_to(balls, DOWN, buff=0.8)
        with self.voiceover(
            text="Take six distinct items and split them into three labeled groups "
                 "of sizes three, two, and one. How many ways are there to "
                 "accomplish this task?"
        ):
            self.play(LaggedStartMap(FadeIn, balls, lag_ratio=0.12), run_time=1.6)
            self.play(FadeIn(prompt, shift=UP * 0.2))

        self.play(FadeOut(prompt))

        arrange_lab = MathTex(r"6! \text{ orderings of the row}",
                              font_size=SMALL, color=ACCENT)
        arrange_lab.next_to(balls, DOWN, buff=0.6)
        with self.voiceover(
            text="Here is the trick: first line up all six items in a row. There "
                 "are six factorial orderings. Now read the groups off the row — "
                 "the first three items, then the next two, then the last one."
        ):
            self.play(Write(arrange_lab))

        # Braces marking the 3 / 2 / 1 groups.
        g1 = VGroup(*balls[0:3])
        g2 = VGroup(*balls[3:5])
        g3 = VGroup(*balls[5:6])
        br1 = Brace(g1, UP, color=MUTED)
        br2 = Brace(g2, UP, color=MUTED)
        br3 = Brace(g3, UP, color=MUTED)
        l1 = br1.get_tex(r"3!").set_color(MUTED).scale(0.8)
        l2 = br2.get_tex(r"2!").set_color(MUTED).scale(0.8)
        l3 = br3.get_tex(r"1!").set_color(MUTED).scale(0.8)
        braces = VGroup(br1, br2, br3, l1, l2, l3)
        with self.voiceover(
            text="But the order inside a group does not matter: any of the three "
                 "factorial shuffles of the first group gives the same group, and "
                 "likewise two factorial for the second. So divide out those "
                 "internal orderings."
        ):
            self.play(GrowFromCenter(br1), FadeIn(l1),
                      GrowFromCenter(br2), FadeIn(l2),
                      GrowFromCenter(br3), FadeIn(l3))

        concrete = MathTex(
            r"\frac{6!}{3!\,2!\,1!} = 60",
            font_size=BODY, color=ACCENT,
        )
        general = MathTex(
            r"\binom{n}{n_1, n_2, \ldots, n_r}"
            r" = \frac{n!}{n_1!\, n_2! \cdots n_r!}",
            font_size=BODY, color=INK,
        )
        stack = VGroup(concrete, general).arrange(DOWN, buff=0.5)
        stack.next_to(arrange_lab, DOWN, buff=0.7)
        fit_to_frame(stack)
        with self.voiceover(
            text="Six factorial over three factorial, two factorial, one factorial "
                 "— that is sixty. In general, splitting n items into r groups of "
                 "sizes n-one through n-r gives the multinomial coefficient: n "
                 "factorial divided by the product of the n-i factorials."
        ):
            self.play(Write(concrete))
            self.play(Write(general))

        self.play(*[FadeOut(m) for m in self.mobjects])


class StarsAndBars(VoiceoverScene):
    """Beat: stars-and-bars -- k stars + r-1 bars, map to a tuple, C(k+r-1, r-1)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Stars and Bars")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        eqn = MathTex(
            r"x_1 + x_2 + \cdots + x_r = k,"
            r"\qquad x_i \ge 0 \ \text{integers}",
            font_size=BODY, color=ACCENT,
        ).next_to(title, DOWN, buff=0.6)
        fit_to_frame(eqn)

        # Bottom (yellow) equation, anchored low; written later. The stars-and-
        # bars row is then centred vertically between eqn (top) and count (bottom).
        count = MathTex(
            r"\binom{k + r - 1}{r - 1} = \binom{k + r - 1}{k}",
            font_size=BODY, color=ACCENT,
        ).to_edge(DOWN, buff=1.0)
        fit_to_frame(count)

        with self.voiceover(
            text="Now change the question. Instead of fixing the group sizes, we "
                 "ask: in how many ways can the sizes themselves be chosen? Count "
                 "the nonnegative integer solutions of x-one plus x-two, up to x-r, "
                 "equals k."
        ):
            self.play(Write(eqn))

        # Concrete row: ★ ★ | ★ | | ★ ★   (k = 5 stars, r = 4 groups, 3 bars).
        kinds = ["s", "s", "b", "s", "b", "b", "s", "s"]
        tokens = VGroup()
        stars_only = VGroup()
        bars_only = VGroup()
        for kind in kinds:
            t = star() if kind == "s" else bar()
            tokens.add(t)
            (stars_only if kind == "s" else bars_only).add(t)
        tokens.arrange(RIGHT, buff=0.38)
        mid_y = (eqn.get_bottom()[1] + count.get_top()[1]) / 2
        tokens.move_to([0, mid_y, 0])
        fit_to_frame(tokens)
        with self.voiceover(
            text="Here is the picture, called stars and bars. Draw k identical "
                 "stars in a row, and drop in r minus one bars."
        ):
            self.play(LaggedStartMap(FadeIn, stars_only, lag_ratio=0.15),
                      run_time=1.4)
            self.play(LaggedStartMap(GrowFromCenter, bars_only, lag_ratio=0.2),
                      run_time=1.2)

        with self.voiceover(
            text="The bars cut the stars into r groups: the stars before the first "
                 "bar, between consecutive bars, and after the last bar."
        ):
            self.play(*[t.animate.set_color(MUTED) for t in bars_only],
                      run_time=0.6)
            self.play(Indicate(stars_only, color=ACCENT, scale_factor=1.08))

        # Tuple read-out sits ABOVE the row, leaving the space below for the
        # positions brace and the count equation.
        tuple_lab = MathTex(
            r"(x_1, x_2, x_3, x_4) = (2,\, 1,\, 0,\, 2)",
            font_size=SMALL, color=INK,
        ).next_to(tokens, UP, buff=0.55)
        fit_to_frame(tuple_lab)
        with self.voiceover(
            text="Each arrangement reads off as a solution. This row — two stars, a "
                 "bar, one star, a bar, then nothing, a bar, two stars — gives the "
                 "tuple two, one, zero, two. Two consecutive bars just mean an "
                 "empty group."
        ):
            self.play(Write(tuple_lab))

        self.play(FadeOut(tuple_lab))

        positions = Brace(tokens, DOWN, color=MUTED)
        pos_lab = positions.get_tex(r"k + r - 1 \text{ positions}")
        pos_lab.set_color(MUTED).scale(0.85)
        with self.voiceover(
            text="So every solution is one arrangement of k stars and r minus one "
                 "bars in a row of k plus r minus one positions. Counting them is "
                 "counting which positions hold the bars: k plus r minus one, "
                 "choose r minus one. Equivalently, choose the star positions — "
                 "k plus r minus one, choose k."
        ):
            self.play(GrowFromCenter(positions), FadeIn(pos_lab))
            self.play(Write(count))

        self.play(*[FadeOut(m) for m in self.mobjects])


class SamplingTieIn(VoiceoverScene):
    """Beat: sampling -- with replacement, unordered = C(n+k-1, k); table; outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("With Replacement, without Ordering")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Urn of n balls + a tally (not a sequence).
        urn_balls = VGroup(
            ball("1", RED, radius=0.28, font_size=18),
            ball("2", BLUE, radius=0.28, font_size=18),
            MathTex(r"\cdots", font_size=SMALL, color=INK),
            ball("n", GRAY_B, radius=0.28, font_size=18),
        ).arrange(RIGHT, buff=0.26)
        urn_box = SurroundingRectangle(urn_balls, color=MUTED, corner_radius=0.18,
                                       buff=0.4)
        urn = VGroup(urn_box, urn_balls)
        urn_lab = Text("urn of n balls", font_size=CAPTION, color=MUTED)
        urn_lab.next_to(urn_box, UP, buff=0.2)
        urn_grp = VGroup(urn, urn_lab).move_to(UP * 0.9)
        fit_to_frame(urn_grp)

        with self.voiceover(
            text="Stars and bars settles a sampling question we left open. An urn "
                 "holds n numbered balls. Draw one, record its number, put it back, "
                 "and repeat k times — but this time we ignore the order, keeping "
                 "only a tally of how many times each ball appeared."
        ):
            self.play(FadeIn(urn), FadeIn(urn_lab))

        tally = MathTex(
            r"x_1 + x_2 + \cdots + x_n = k",
            font_size=BODY, color=INK,
        ).next_to(urn_grp, DOWN, buff=0.7)
        formula = MathTex(
            r"\binom{n + k - 1}{k}",
            font_size=TITLE, color=ACCENT,
        ).next_to(tally, DOWN, buff=0.6)
        fit_to_frame(VGroup(tally, formula))
        with self.voiceover(
            text="A tally has one count per ball: nonnegative numbers x-one through "
                 "x-n that add up to k draws. That is a stars-and-bars problem with "
                 "n bins and k stars, so the number of outcomes is n plus k minus "
                 "one, choose k."
        ):
            self.play(Write(tally))
            self.play(Write(formula))

        with self.voiceover(
            text="So drawing k times from n with replacement, but ignoring order, "
                 "gives n plus k minus one, choose k. That is the fourth and last "
                 "way to sample — and in the next video we will line up all four "
                 "side by side."
        ):
            self.play(Indicate(formula, color=ACCENT, scale_factor=1.1))

        # Clear everything (title included) before the closing card.
        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing key idea + bridge (centred two-line key idea, house style).
        key_idea = VGroup(
            MathTex(r"\text{fixed sizes:}\ \ \frac{n!}{n_1!\cdots n_r!}"
                    r"\qquad\quad\text{free sizes:}\ \ \binom{k+r-1}{r-1}",
                    font_size=BODY, color=INK),
        )
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  A Unified View of Sampling",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So the whole story is two counts. Fixed group sizes give the "
                 "multinomial coefficient, n factorial over the product of the n-i "
                 "factorials. Free sizes give stars and bars, k plus r minus one "
                 "choose r minus one. Next, we lay all four sampling schemes side "
                 "by side, and put them to work on the birthday problem."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
