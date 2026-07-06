# derived_from: content/04-permutations-combinations-script.md
# derived_from_sha256: ee0061c3a0a4c7dfa8072ecdcc34470173d4c0bf76fdcddfe50b603346cbe70e
"""Chapter 2, Video 2 -- Permutations and Combinations (manim-voiceover).

Source notes : ../chapters/combinatorics.tex  (2.2 Permutations, 2.2.1
               k-Permutations, 2.3 Combinations, 2.3.1 Binomial Theorem)
Script        : content/04-permutations-combinations-script.md

Bookmark-free timing (sequential voiceover blocks), same as the Chapter 1
videos. Draft uses gTTS; switch make_speech_service() to OpenAIService(nova)
for the final.
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


BALL_COLORS = [RED, BLUE, GREEN, GRAY_B]


def slot(side=0.8):
    return Square(side_length=side, color=INK).set_stroke(INK, 2)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap, title, outline by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Permutations & Combinations",
            "Count ordered arrangements, unordered selections, and the factor between them.",
            kicker="Chapter 2  ·  Combinatorics",
        )
        fit_to_frame(intro)
        tag = progress_tag(2, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="Last video, we saw that, in simple scenarios, probability "
                 "reduces to counting, and that to count choices made in stages, "
                 "you multiply. Now we build the two counts you will reach for "
                 "again and again."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Permutations  —  ordered arrangements", font_size=BODY),
            Text("2.  k-permutations  —  ordered selections", font_size=BODY),
            Text("3.  Combinations  —  unordered selections", font_size=BODY),
            Text("4.  Pascal's rule and the binomial theorem", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this video: permutations, the ordered arrangements;",
            "k-permutations, ordered selections of part of a set;",
            "combinations, the unordered selections;",
            "and the binomial theorem that ties them together.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="The whole video turns on one question — does order matter?"
        ):
            self.play(Indicate(items, color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Permutations(VoiceoverScene):
    """Beat: permutations -- fill n slots, n! arrangements; list the 6 of {1,2,3}."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Permutations")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        pool = VGroup(ball("1", RED), ball("2", BLUE), ball("3", GREEN))
        pool.arrange(RIGHT, buff=0.4).move_to(UP * 1.6)
        slots = VGroup(*[slot() for _ in range(3)]).arrange(RIGHT, buff=0.5)
        slots.next_to(pool, DOWN, buff=1.0)

        with self.voiceover(
            text="A permutation is an ordered arrangement of distinct objects — a "
                 "list with no repeats. Count them by filling slots. Take the set "
                 "one, two, three, and three slots to fill."
        ):
            self.play(LaggedStartMap(FadeIn, pool, lag_ratio=0.2))
            self.play(LaggedStartMap(Create, slots, lag_ratio=0.2))

        counts = VGroup(*[MathTex(str(c), font_size=BODY, color=ACCENT)
                          for c in (3, 2, 1)])
        for c, s in zip(counts, slots):
            c.next_to(s, DOWN, buff=0.25)
        with self.voiceover(
            text="The first slot has three choices. Once it is taken, the second "
                 "has only two left. The last has just one. By the counting "
                 "principle, multiply: three times two times one."
        ):
            for c in counts:
                self.play(FadeIn(c, shift=DOWN * 0.1), run_time=0.4)

        fact = MathTex(r"3! = 3 \times 2 \times 1 = 6", font_size=BODY, color=ACCENT)
        ngen = MathTex(r"n! = n\,(n-1)\cdots 1", font_size=SMALL, color=MUTED)
        VGroup(fact, ngen).arrange(DOWN, buff=0.35).next_to(slots, DOWN, buff=1.0)
        with self.voiceover(
            text="That product is three factorial, which is six. In general, "
                 "arranging n distinct objects gives n factorial — n times n minus "
                 "one, all the way down to one."
        ):
            self.play(Write(fact))
            self.play(FadeIn(ngen))

        self.play(FadeOut(pool), FadeOut(slots), FadeOut(counts),
                  fact.animate.to_edge(UP, buff=1.4), FadeOut(ngen))

        perms = VGroup(*[MathTex(p, font_size=BODY, color=INK) for p in
                         (r"1\,2\,3", r"1\,3\,2", r"2\,1\,3",
                          r"2\,3\,1", r"3\,1\,2", r"3\,2\,1")])
        perms.arrange_in_grid(rows=2, cols=3, buff=(1.1, 0.7)).move_to(DOWN * 0.6)
        with self.voiceover(
            text="Here are all six arrangements of one, two, three. Same three "
                 "objects every time; only the order changes."
        ):
            self.play(LaggedStartMap(FadeIn, perms, lag_ratio=0.15), run_time=2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class KPermutations(VoiceoverScene):
    """Beat: k-permutations -- k of n slots, n!/(n-k)!; the songs example."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("k-Permutations")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Pool lowered so it clears the n!/(n-k)! formula written near the top.
        pool = VGroup(*[ball(str(i + 1), BALL_COLORS[i]) for i in range(4)])
        pool.arrange(RIGHT, buff=0.4).move_to(UP * 0.6)
        slots = VGroup(slot(), slot()).arrange(RIGHT, buff=0.5)
        slots.next_to(pool, DOWN, buff=0.9)

        with self.voiceover(
            text="Often we arrange only part of the set. Suppose we rank k of the "
                 "n objects. The first slot still has n choices, the second n minus "
                 "one, and so on — but now we stop after k slots."
        ):
            self.play(LaggedStartMap(FadeIn, pool, lag_ratio=0.15))
            self.play(LaggedStartMap(Create, slots, lag_ratio=0.2))
            counts = VGroup(
                MathTex("4", font_size=BODY, color=ACCENT).next_to(slots[0], DOWN, buff=0.25),
                MathTex("3", font_size=BODY, color=ACCENT).next_to(slots[1], DOWN, buff=0.25),
            )
            self.play(FadeIn(counts[0]), FadeIn(counts[1]))

        formula = MathTex(r"\frac{n!}{(n-k)!} = n\,(n-1)\cdots(n-k+1)",
                          font_size=BODY, color=ACCENT).next_to(title, DOWN, buff=0.6)
        fit_to_frame(formula)
        with self.voiceover(
            text="The count is n times n minus one, down to n minus k plus one, "
                 "which we write compactly as n factorial over n minus k factorial."
        ):
            self.play(Write(formula))

        songs = MathTex(r"\text{4 songs, choose 2 in order:}\quad "
                        r"\frac{4!}{2!} = 4 \times 3 = 12",
                        font_size=SMALL, color=INK).to_edge(DOWN, buff=1.0)
        fit_to_frame(songs)
        with self.voiceover(
            text="For example, a band with four songs wants to play two, in order. "
                 "That is the number of 2-permutations of four: four times three, "
                 "twelve arrangements. This is sampling without replacement, "
                 "keeping order."
        ):
            self.play(Write(songs))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Combinations(VoiceoverScene):
    """Beat: combinations -- 12 ordered pairs collapse k! at a time into 6 subsets."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Combinations")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Six subsets of {1,2,3,4}, each shown with its two orderings inside a loop.
        pairs = [("1", "2"), ("1", "3"), ("1", "4"),
                 ("2", "3"), ("2", "4"), ("3", "4")]
        groups = VGroup()
        for a, b in pairs:
            two = VGroup(
                MathTex(rf"{a}\,{b}", font_size=SMALL, color=INK),
                MathTex(rf"{b}\,{a}", font_size=SMALL, color=INK),
            ).arrange(DOWN, buff=0.18)
            loop = SurroundingRectangle(two, color=MUTED, corner_radius=0.18, buff=0.18)
            groups.add(VGroup(loop, two))
        groups.arrange_in_grid(rows=2, cols=3, buff=(0.7, 0.6)).move_to(DOWN * 0.4)
        fit_to_frame(groups)
        loops = VGroup(*[g[0] for g in groups])
        twos = VGroup(*[g[1] for g in groups])

        with self.voiceover(
            text="Now drop the order. A combination is just a subset — which "
                 "objects, not in what arrangement. Here are the twelve "
                 "2-permutations of one, two, three, four — all ordered pairs."
        ):
            self.play(LaggedStartMap(FadeIn, twos, lag_ratio=0.08), run_time=2.0)

        with self.voiceover(
            text="But one, two and two, one are the same subset. Group the pairs "
                 "that use the same two elements, and the twelve collapse into six "
                 "groups. Each group holds exactly two orderings — that is two "
                 "factorial."
        ):
            self.play(LaggedStartMap(Create, loops, lag_ratio=0.1), run_time=1.8)

        factor = MathTex(r"\frac{12 \text{ ordered}}{2! \text{ orderings}} = 6"
                         r"\ \text{subsets}", font_size=SMALL, color=ACCENT)
        factor.next_to(title, DOWN, buff=0.4)
        fit_to_frame(factor)
        with self.voiceover(
            text="So the number of subsets is the number of pairs divided by two, "
                 "which is equal to six."
        ):
            self.play(Write(factor))

        self.play(FadeOut(groups), FadeOut(factor))

        formula = MathTex(r"\binom{n}{k} = \frac{n!}{k!\,(n-k)!}",
                          font_size=TITLE, color=ACCENT).move_to(UP * 0.6)
        with self.voiceover(
            text="In general, the number of k-element subsets is n factorial over "
                 "k factorial times n minus k factorial — the binomial "
                 "coefficient, n choose k. The ordered count, divided by the k "
                 "factorial orderings."
        ):
            self.play(Write(formula))

        symm = MathTex(r"\binom{n}{k} = \binom{n}{n-k}",
                       font_size=BODY, color=INK).next_to(formula, DOWN, buff=0.8)
        with self.voiceover(
            text="And notice: choosing the k elements to keep is the same as "
                 "choosing the n minus k to leave out. So n choose k equals n "
                 "choose n minus k."
        ):
            self.play(Write(symm))

        self.play(*[FadeOut(m) for m in self.mobjects])


class BinomialTheorem(VoiceoverScene):
    """Beat: binomial-theorem -- Pascal's rule + triangle, the theorem, 2^n; outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Pascal's Rule and the Binomial Theorem")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        pascal_rule = MathTex(r"\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}",
                              font_size=BODY, color=ACCENT).next_to(title, DOWN, buff=0.5)
        fit_to_frame(pascal_rule)
        with self.voiceover(
            text="Binomial coefficients fit together beautifully. Pascal's rule "
                 "says n choose k equals n minus one choose k minus one, plus n "
                 "minus one choose k. For a k-subset, ask whether element n is in "
                 "it: if yes, choose the rest from the others; if no, choose all k "
                 "from the others."
        ):
            self.play(Write(pascal_rule))

        # Pascal's triangle, rows 0..4.
        rows_vals = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        tri = VGroup()
        for vals in rows_vals:
            row = VGroup(*[MathTex(str(v), font_size=SMALL, color=INK) for v in vals])
            row.arrange(RIGHT, buff=0.5)
            tri.add(row)
        tri.arrange(DOWN, buff=0.32).next_to(pascal_rule, DOWN, buff=0.6)
        fit_to_frame(tri)
        with self.voiceover(
            text="Stack the coefficients by row and you get Pascal's triangle, "
                 "where every entry is the sum of the two above it."
        ):
            self.play(LaggedStartMap(FadeIn, tri, lag_ratio=0.2), run_time=2.0)
            # Highlight row 4's middle 6 = 3 + 3 above it.
            self.play(tri[4][2].animate.set_color(ACCENT),
                      tri[3][1].animate.set_color(ACCENT),
                      tri[3][2].animate.set_color(ACCENT))

        self.play(FadeOut(tri), pascal_rule.animate.set_opacity(0.0))

        theorem = MathTex(r"(x + y)^n = \sum_{k=0}^{n} \binom{n}{k}\, x^k y^{n-k}",
                          font_size=BODY, color=ACCENT).next_to(title, DOWN, buff=0.7)
        fit_to_frame(theorem)
        with self.voiceover(
            text="They are called binomial coefficients because of the binomial "
                 "theorem: x plus y to the n is the sum over k of n choose k, x to "
                 "the k, y to the n minus k. The coefficient of x-to-the-k counts "
                 "the ways to pick x from k of the factors — that is n choose k."
        ):
            self.play(Write(theorem))

        corollary = MathTex(r"x = y = 1:\quad \sum_{k=0}^{n} \binom{n}{k} = 2^n",
                            font_size=BODY, color=INK).next_to(theorem, DOWN, buff=0.8)
        fit_to_frame(corollary)
        with self.voiceover(
            text="Set x and y both to one, and the theorem gives the sum of all "
                 "the binomial coefficients equals two to the n — the same count "
                 "of subsets we found before, now split by size."
        ):
            self.play(Write(corollary))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing key idea + bridge (centred two-line key idea, Chapter-1 style).
        key_idea = VGroup(
            Text("Order kept gives n! / (n-k)!;", font_size=BODY, color=INK),
            Text("order dropped divides by k!, giving n choose k.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Partitions and Stars and Bars",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So everything here hangs on a single hinge: order kept gives n "
                 "factorial over n minus k factorial; order dropped divides by k "
                 "factorial, giving n choose k. Next, we split a set into several "
                 "groups at once — partitions, and the stars-and-bars trick."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
