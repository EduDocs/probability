# derived_from: content/03-counting-principle-script.md
# derived_from_sha256: f885c1948576f0a93d67a06aab218a204bc22a992a55ca40c997751b557f0db1
"""Chapter 2, Video 1 -- The Counting Principle (narrated with manim-voiceover).

Source notes : ../chapters/combinatorics.tex  (chapter intro + 2.1 Counting
               Principle)
Script        : content/03-counting-principle-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, timed by ``tracker.duration`` -- the
same pattern as the Chapter 1 videos.

Draft render:
    uv run manim -pql scenes/counting_principle.py ChapterOverview
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
    section_title,
    intro_card,
    progress_tag,
    fit_to_frame,
    configure_openai_client,
)


def make_speech_service():
    """Voice (mirrors voice: in the script YAML).

    Draft  -> GTTSService (free). Final -> OpenAIService(voice="nova"), matching
    the Chapter 1 series; switch the lines below and add OPENAI_API_KEY.
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


# --- Shared visual helpers (mirroring the Chapter 1 house style) -------------

def ball(label, color, radius=0.32, font_size=22):
    """A colored disk with a dark centered label (see Chapter 1 contrast note)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


def die_face(n, size=0.95, color=INK, fill=None):
    """A rounded square die face showing n pips in the standard layout."""
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
    """Beat: overview -- recap of Chapter 1, title, and outline by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Counting",
            "Turn probability into counting, and count Cartesian products.",
            kicker="Chapter 2  ·  Combinatorics",
        )
        tag = progress_tag(1, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="In Chapter one we built the language of sets and functions — "
                 "the vocabulary of outcomes. Now we start computing with it."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(tag), run_time=0.4)

        with self.voiceover(
            text="This chapter is about counting, because in the simplest model, "
                 "finding the probability reduces to counting."
        ):
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  The equally-likely model", font_size=BODY),
            Text("2.  The counting principle", font_size=BODY),
            Text("3.  Multi-stage experiments and sampling", font_size=BODY),
            Text("4.  Counting all the subsets of a set", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this video we meet the equally-likely model,",
            "the counting principle,",
            "multi-stage experiments,",
            "and a quick way to count all the subsets of a set.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class EquallyLikely(VoiceoverScene):
    """Beat: equally-likely -- the fair die, an event, favorable over total."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Equally Likely Outcomes")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        primes = {2, 3, 5}
        faces = VGroup(*[die_face(n) for n in range(1, 7)])
        faces.arrange(RIGHT, buff=0.4).move_to(UP * 0.4)
        fit_to_frame(faces)

        with self.voiceover(
            text="Here is the simplest probabilistic scenario: finitely many "
                 "outcomes, all equally likely. Take a fair die — six faces, each "
                 "just as likely as any other. The probability of any single face "
                 "is one over six."
        ):
            self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.12), run_time=2.0)
            one_sixth = MathTex(r"\Pr(\text{a face}) = \tfrac{1}{6}",
                                font_size=BODY, color=INK).next_to(faces, DOWN, buff=0.7)
            self.play(Write(one_sixth))

        with self.voiceover(
            text="An event is just a subset of the outcomes. Consider the event "
                 "roll a prime: the faces two, three, and five."
        ):
            ev = MathTex(r"E = \{\, 2, 3, 5 \,\}", font_size=BODY, color=ACCENT)
            ev.move_to(one_sixth)
            self.play(ReplacementTransform(one_sixth, ev))
            self.play(*[faces[n - 1][0].animate.set_fill(ACCENT, opacity=0.3)
                        for n in primes])

        with self.voiceover(
            text="To find its probability, we count. Three favorable outcomes out "
                 "of six total — so the probability is three over six, one half. "
                 "That is the whole model: favorable outcomes divided by the total. "
                 "The catch is that the counting is often the hard part, and that "
                 "is what combinatorics is for."
        ):
            ratio = MathTex(
                r"\Pr(E) = \frac{\text{favorable}}{\text{total}}"
                r" = \frac{3}{6} = \frac{1}{2}",
                font_size=BODY, color=INK,
            ).next_to(ev, DOWN, buff=0.6)
            fit_to_frame(ratio)
            self.play(Write(ratio))

        self.play(*[FadeOut(m) for m in self.mobjects])


class CountingPrinciple(VoiceoverScene):
    """Beat: counting-principle -- |S x T| = |S||T|, coin x die, independence."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Counting Principle")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # S = {1,2,3}, T = {a,b}; build the product grid (Chapter-1 style).
        s_cols = [("1", RED), ("2", BLUE), ("3", GREEN)]
        t_rows = [("a", YELLOW), ("b", PINK)]
        s_group = VGroup(*[ball(l, c) for l, c in s_cols])
        s_group.arrange(DOWN, buff=0.4).to_edge(LEFT, buff=1.5).shift(DOWN * 0.5)
        s_lab = MathTex("S", font_size=SMALL, color=MUTED).next_to(s_group, UP, buff=0.25)
        t_group = VGroup(*[ball(l, c) for l, c in t_rows])
        t_group.arrange(DOWN, buff=0.4).next_to(s_group, RIGHT, buff=0.7)
        t_lab = MathTex("T", font_size=SMALL, color=MUTED).next_to(t_group, UP, buff=0.25)

        grid = VGroup()
        for tl, tc in t_rows:
            for sl, sc in s_cols:
                grid.add(VGroup(ball(sl, sc, radius=0.26, font_size=18),
                                ball(tl, tc, radius=0.26, font_size=18)
                                ).arrange(RIGHT, buff=0.08))
        grid.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.55))
        grid.to_edge(RIGHT, buff=1.1).shift(DOWN * 0.5)
        arrow = Arrow(t_group.get_right(), grid.get_left(), color=ACCENT,
                      buff=0.4, stroke_width=4)

        with self.voiceover(
            text="The first tool is the counting principle, and it is about the "
                 "Cartesian product from Chapter one. Take a set S with three "
                 "elements and a set T with two. Pair every element of S with "
                 "every element of T, and you fill a grid."
        ):
            self.play(LaggedStartMap(FadeIn, s_group, lag_ratio=0.2), FadeIn(s_lab))
            self.play(LaggedStartMap(FadeIn, t_group, lag_ratio=0.2), FadeIn(t_lab))
            self.play(GrowArrow(arrow))
            self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.1), run_time=1.8)

        prod = MathTex(r"|S \times T| = |S|\,|T| = 3 \times 2 = 6",
                       font_size=BODY, color=ACCENT).next_to(title, DOWN, buff=0.5)
        fit_to_frame(prod)
        with self.voiceover(
            text="The number of pairs is just three times two — six. In general, "
                 "if S has m elements and T has n elements, their Cartesian product has m "
                 "times n elements. To count a product, multiply the sizes."
        ):
            self.play(Write(prod))

        self.play(FadeOut(grid), FadeOut(arrow), FadeOut(s_group), FadeOut(t_group),
                  FadeOut(s_lab), FadeOut(t_lab), FadeOut(prod))

        coin_die = MathTex(r"\underbrace{2}_{\text{coin}} \times "
                           r"\underbrace{6}_{\text{die}} = 12",
                           font_size=TITLE, color=INK).move_to(UP * 0.6)
        with self.voiceover(
            text="Flip a coin and roll a die. Two outcomes for the coin, six for "
                 "the die — so two times six, twelve joint outcomes in all."
        ):
            self.play(Write(coin_die))

        indep = MathTex(r"\Pr \{ (c,d) \} = \tfrac{1}{12} = \tfrac{1}{2} \times \tfrac{1}{6}",
                        font_size=BODY, color=ACCENT).next_to(coin_die, DOWN, buff=0.8)
        with self.voiceover(
            text="And because the outcomes are equally likely, the probability of "
                 "any one is one over twelve, which factors as one-half times "
                 "one-sixth. Combining unrelated experiments multiplies their "
                 "probabilities — an informal first taste of independence, which "
                 "we will make precise later."
        ):
            self.play(Write(indep))

        self.play(*[FadeOut(m) for m in self.mobjects])


class MultiStageSampling(VoiceoverScene):
    """Beat: multistage -- n_1...n_r, then sampling with replacement gives n^k."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Multi-Stage Experiments")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        rsets = MathTex(r"|S_1 \times S_2 \times \cdots \times S_r|"
                        r" = n_1 \, n_2 \cdots n_r",
                        font_size=BODY, color=ACCENT).next_to(title, DOWN, buff=0.7)
        fit_to_frame(rsets)
        with self.voiceover(
            text="The principle extends to any number of stages. With r sets of "
                 "sizes n-one, n-two, up to n-r, the number of ordered tuples is "
                 "the product n-one times n-two, all the way to n-r. Each "
                 "independent choice just multiplies the running total."
        ):
            self.play(Write(rsets))

        # Urn (1 2 3 ... n) and k draw-slots, laid out as ONE horizontal row that
        # is vertically aligned (box, balls, squares share a centre line) and
        # centred on screen.
        urn_balls = VGroup(
            ball("1", RED, radius=0.3, font_size=20),
            ball("2", BLUE, radius=0.3, font_size=20),
            ball("3", GREEN, radius=0.3, font_size=20),
            MathTex(r"\cdots", font_size=BODY, color=INK),
            ball("n", GRAY_B, radius=0.3, font_size=20),
        ).arrange(RIGHT, buff=0.28)
        urn_box = SurroundingRectangle(urn_balls, color=MUTED, corner_radius=0.18, buff=0.45)
        urn = VGroup(urn_box, urn_balls)

        slots = VGroup(*[Square(side_length=0.8, color=INK).set_stroke(INK, 2)
                         for _ in range(3)])
        slots.arrange(RIGHT, buff=0.28)
        dots3 = MathTex(r"\cdots", font_size=BODY, color=INK).next_to(slots, RIGHT, buff=0.3)
        slot_grp = VGroup(slots, dots3)

        # Slots to the right of the urn at the SAME height (next_to keeps y),
        # with a gap for the arrow; then centre the whole row horizontally.
        slot_grp.next_to(urn, RIGHT, buff=2.0)
        draw_arrow = Arrow(urn.get_right(), slots.get_left(), color=ACCENT,
                           buff=0.3, stroke_width=4)
        main = VGroup(urn, draw_arrow, slot_grp).move_to(DOWN * 0.4)
        fit_to_frame(main)

        urn_lab = Text("urn of n balls", font_size=CAPTION, color=MUTED).next_to(urn_box, UP, buff=0.2)
        kbrace = Brace(slots, DOWN)
        kbrace_lab = kbrace.get_tex(r"k \text{ draws}")

        with self.voiceover(
            text="Here is the classic case: an urn with n numbered balls. Draw "
                 "one, record its number, and put it back. Repeat k times."
        ):
            self.play(FadeIn(urn), FadeIn(urn_lab))
            self.play(GrowArrow(draw_arrow))
            self.play(Create(slots), Write(dots3), GrowFromCenter(kbrace),
                      Write(kbrace_lab))

        nk = MathTex(r"n \times n \times \cdots \times n = n^k",
                     font_size=BODY, color=ACCENT).to_edge(DOWN, buff=0.7)
        fit_to_frame(nk)
        with self.voiceover(
            text="Each of the k draws has the same n possibilities, so the number "
                 "of ordered sequences is n multiplied by itself k times — n to "
                 "the power k. This is sampling with replacement, with order kept, "
                 "the first of four schemes we assemble by the end of the chapter."
        ):
            self.play(Write(nk))

        self.play(*[FadeOut(m) for m in self.mobjects])


class PowerSet(VoiceoverScene):
    """Beat: power-set -- 2^n subsets via one yes/no per element; outro/bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Counting Subsets")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        elems = VGroup(ball("1", RED), ball("2", BLUE), ball("3", GREEN))
        elems.arrange(RIGHT, buff=1.0).move_to(UP * 1.5)
        toggles = VGroup(*[
            VGroup(MathTex(r"\text{in?}", font_size=SMALL, color=ACCENT),
                   MathTex(r"0/1", font_size=SMALL, color=MUTED)
                   ).arrange(DOWN, buff=0.1).next_to(b, DOWN, buff=0.25)
            for b in elems
        ])

        with self.voiceover(
            text="Here is a neat application: how many subsets does a set have? "
                 "Take the set one, two, three. To build a subset, go through the "
                 "elements one at a time and make a single yes-or-no choice: is "
                 "this element in, or out?"
        ):
            self.play(LaggedStartMap(FadeIn, elems, lag_ratio=0.2))
            self.play(LaggedStartMap(FadeIn, toggles, lag_ratio=0.2))

        subsets = VGroup(
            MathTex(r"\varnothing"), MathTex(r"\{1\}"), MathTex(r"\{2\}"),
            MathTex(r"\{3\}"), MathTex(r"\{1,2\}"), MathTex(r"\{1,3\}"),
            MathTex(r"\{2,3\}"), MathTex(r"\{1,2,3\}"),
        )
        for s in subsets:
            s.set_color(INK).scale(0.9)
        subsets.arrange_in_grid(rows=2, cols=4, buff=(0.7, 0.5)).move_to(DOWN * 1.2)
        fit_to_frame(subsets)
        with self.voiceover(
            text="That is one binary choice per element — exactly the indicator "
                 "function from the last video. Three elements, two choices each, "
                 "so by the counting principle there are two times two times two: "
                 "eight subsets, from the empty set up to the whole set."
        ):
            self.play(LaggedStartMap(FadeIn, subsets, lag_ratio=0.12), run_time=2.2)

        two_n = MathTex(r"2 \times 2 \times 2 = 2^3 = 8 \qquad\Rightarrow\qquad 2^n",
                        font_size=BODY, color=ACCENT)
        two_n.next_to(subsets, DOWN, buff=0.6)
        fit_to_frame(two_n)
        with self.voiceover(
            text="In general, a set with n elements has two to the n subsets. One "
                 "indicator bit per element, multiplied together."
        ):
            self.play(Write(two_n))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing key idea + bridge (centred two-line key idea, Chapter-1 style).
        key_idea = VGroup(
            Text("When outcomes are equally likely, probability is counting;",
                 font_size=BODY, color=INK),
            Text("to count choices made in stages, you multiply.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Permutations and Combinations",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So the whole of this video rests on one idea: when outcomes are "
                 "equally likely, probability is counting, and to count choices "
                 "made in stages, you multiply. Next, we sharpen the toolkit with "
                 "permutations and combinations — counting selections when order "
                 "does, and does not, matter."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
