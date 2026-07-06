# derived_from: content/06-sampling-script.md
# derived_from_sha256: d1128433f505480f198f4f89a82a8b09f21cec3d2e42b97548a9e85bd6df9dec
"""Chapter 2, Video 4 (finale) -- A Unified View of Sampling (manim-voiceover).

Source notes : ../chapters/combinatorics.tex  (2.5 A Unified View of Sampling
               + the Birthday Problem from 2.6 Combinatorial Examples)
Script        : content/06-sampling-script.md

Bookmark-free timing (sequential voiceover blocks), same as the rest of the
series. Draft uses gTTS; switch make_speech_service() to OpenAIService(nova)
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


def p_match(k):
    """Probability that at least two of k people share a birthday (365 days)."""
    p_distinct = 1.0
    for i in range(k):
        p_distinct *= (365 - i) / 365
    return 1 - p_distinct


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of V3, title, and a two-item outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "A Unified View of Sampling",
            "Classify any draw of k from n by replacement and order, then read off its count.",
            kicker="Chapter 2  ·  Combinatorics",
        )
        fit_to_frame(intro)
        tag = progress_tag(4, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="Last video, we split a set into several groups at once — "
                 "partitions, and the stars-and-bars count. That was the last "
                 "piece. In this video we step back and see that everything in this "
                 "chapter has been one question all along: drawing k items from n, "
                 "asked four different ways."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  The 2x2 sampling table", font_size=BODY),
            Text("2.  The Birthday Problem", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.next_to(intro, DOWN, buff=0.9)
        fit_to_frame(items)

        clauses = [
            "We assemble the four counts into a single table,",
            "and then put it to work on a famous puzzle — the Birthday Problem.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class SamplingTable(VoiceoverScene):
    """Beat: sampling-table -- the 2x2 grid, the four counts, the k! link."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Sampling Table")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- 2x2 grid of equal cells (row-major: 0 TL, 1 TR, 2 BL, 3 BR) -----
        cell_w, cell_h = 3.5, 1.45
        cells = VGroup(*[
            Rectangle(width=cell_w, height=cell_h).set_stroke(MUTED, 2.5)
            for _ in range(4)
        ])
        cells.arrange_in_grid(rows=2, cols=2, buff=0)

        # Counts, one per cell (with replacement on top row).
        counts = [
            MathTex(r"n^{k}", font_size=BODY, color=INK),                 # TL: with, ordered
            MathTex(r"\binom{n+k-1}{k}", font_size=BODY, color=INK),      # TR: with, unordered
            MathTex(r"\dfrac{n!}{(n-k)!}", font_size=BODY, color=INK),    # BL: without, ordered
            MathTex(r"\binom{n}{k}", font_size=BODY, color=INK),          # BR: without, unordered
        ]
        for m, box in zip(counts, cells):
            m.move_to(box.get_center())

        # Column headers (above the top row) and row headers (left of each row).
        col_ord = Text("ordered", font_size=SMALL, color=ACCENT).next_to(cells[0], UP, buff=0.3)
        col_uno = Text("unordered", font_size=SMALL, color=ACCENT).next_to(cells[1], UP, buff=0.3)
        row_with = Text("with replacement", font_size=CAPTION, color=ACCENT)
        row_with.next_to(cells[0], LEFT, buff=0.4)
        row_wout = Text("without replacement", font_size=CAPTION, color=ACCENT)
        row_wout.next_to(cells[2], LEFT, buff=0.4)

        headers = VGroup(col_ord, col_uno, row_with, row_wout)

        # The "divide by k!" link as a CURVED arrow from the bottom-LEFT cell to
        # the bottom-RIGHT cell -- emphasising a BL->BR progression, not a plain
        # left-to-right relation.
        karrow = CurvedArrow(
            cells[2].get_bottom() + DOWN * 0.2,
            cells[3].get_bottom() + DOWN * 0.2,
            angle=TAU / 6, color=ACCENT, stroke_width=5, tip_length=0.22,
        )
        klabel = MathTex(r"\div\, k!", font_size=SMALL, color=ACCENT)
        klabel.next_to(karrow, DOWN, buff=0.12)
        karrow_grp = VGroup(karrow, klabel)

        table = VGroup(cells, headers, VGroup(*counts), karrow_grp)
        table.next_to(title, DOWN, buff=1.5)
        fit_to_frame(table)

        # Caption naming the unified convention, just above the (lowered) table.
        draw_lab = MathTex(r"\text{draw } k \text{ from } n",
                           font_size=SMALL, color=MUTED)
        draw_lab.next_to(title, DOWN, buff=0.5)

        with self.voiceover(
            text="Every urn example in this chapter draws k items from a set of n. "
                 "Two yes-or-no questions tell them apart. First: do we put each "
                 "item back before the next draw — with replacement, or without? "
                 "Second: do we record the order of the draws, or only which items "
                 "came out? Two binary choices make a two-by-two table, and each "
                 "cell holds a count."
        ):
            self.play(FadeIn(draw_lab, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(cells), run_time=1.4)
            self.play(FadeIn(col_ord), FadeIn(col_uno),
                      FadeIn(row_with), FadeIn(row_wout), run_time=1.0)

        with self.voiceover(
            text="The ordered column comes straight from the counting principle. "
                 "With replacement, every one of the k draws has all n items "
                 "available, so there are n to the k ordered sequences. Without "
                 "replacement the pool shrinks each time — n, then n minus one, "
                 "down to n minus k plus one — which is n factorial over n minus k "
                 "factorial."
        ):
            self.play(Write(counts[0]))   # n^k
            self.play(Write(counts[2]))   # n!/(n-k)!

        with self.voiceover(
            text="The unordered column drops the order, recording only which items "
                 "came out."
        ):
            self.play(Write(counts[3]))   # C(n,k)
            self.play(Write(counts[1]))   # C(n+k-1,k)

        with self.voiceover(
            text="Look along the without-replacement row: any selection of k "
                 "distinct items can be arranged in k factorial ways, so the "
                 "unordered count is the ordered one divided by k factorial — that "
                 "is n choose k."
        ):
            self.play(Create(karrow), FadeIn(klabel))
            self.play(Indicate(counts[2], color=ACCENT, scale_factor=1.12),
                      Indicate(counts[3], color=ACCENT, scale_factor=1.12))

        with self.voiceover(
            text="The with-replacement row is subtler, because a repeated item "
                 "cannot be reordered into distinct sequences; the stars-and-bars "
                 "argument from last video handles it and gives n plus k minus one, "
                 "choose k."
        ):
            self.play(FadeOut(karrow_grp))   # the BL->BR arrow vanishes here
            self.play(Indicate(counts[1], color=ACCENT, scale_factor=1.12))

        with self.voiceover(
            text="Four cells, two questions. Recognizing which cell a problem "
                 "lives in is usually the whole battle."
        ):
            self.play(Indicate(cells, color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class BirthdayProblem(VoiceoverScene):
    """Beat: birthday-setup -- two table cells become the birthday formula."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Birthday Problem")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # A small crowd (k people) above a strip of 365 days; larger tokens and
        # BODY labels, centred to use the vertical space.
        people = VGroup(*[ball("", BAR, radius=0.34) for _ in range(6)])
        people.arrange(RIGHT, buff=0.3)
        dots = MathTex(r"\cdots", font_size=BODY, color=INK)
        crowd = VGroup(people, dots).arrange(RIGHT, buff=0.35)
        crowd_lab = Text("k people", font_size=BODY, color=MUTED)
        crowd_lab.next_to(crowd, DOWN, buff=0.4)
        crowd_grp = VGroup(crowd, crowd_lab)
        days_lab = MathTex(r"365 \text{ equally likely days}",
                           font_size=BODY, color=MUTED)
        days_lab.next_to(crowd_grp, DOWN, buff=1.0)
        block = VGroup(crowd_grp, days_lab).move_to(DOWN * 0.3)
        fit_to_frame(block)

        with self.voiceover(
            text="Now one example that uses two cells of that table. A room holds k "
                 "people. Each person's birthday is equally likely to be any of the "
                 "three hundred sixty-five days of the year, with different people "
                 "unrelated. What is the probability that at least two of them share "
                 "a birthday?"
        ):
            self.play(LaggedStartMap(FadeIn, people, lag_ratio=0.12), Write(dots))
            self.play(FadeIn(crowd_lab), FadeIn(days_lab))

        self.play(FadeOut(crowd_grp), FadeOut(days_lab))

        # Denominator: total ordered sequences (with replacement).
        denom = MathTex(r"\text{total} \;=\; 365^{k}",
                        font_size=BODY, color=INK)
        denom_tag = Text("with replacement, ordered", font_size=BODY, color=MUTED)
        denom_tag.next_to(denom, DOWN, buff=0.3)
        denom_grp = VGroup(denom, denom_tag).move_to(UP * 1.1)
        fit_to_frame(denom_grp)

        with self.voiceover(
            text="It is easier to count the opposite — that all k birthdays are "
                 "distinct — and subtract from one. List the birthdays in order. "
                 "That is a sequence of k days drawn from three hundred sixty-five, "
                 "with repeats allowed: sampling with replacement, ordered. So there "
                 "are three hundred sixty-five to the k equally likely outcomes in "
                 "total."
        ):
            self.play(Write(denom))
            self.play(FadeIn(denom_tag))

        # Numerator: distinct birthdays (without replacement, ordered).
        numer = MathTex(r"\text{distinct} \;=\; \frac{365!}{(365-k)!}",
                        font_size=BODY, color=INK)
        numer_tag = Text("without replacement, ordered", font_size=BODY, color=MUTED)
        numer_tag.next_to(numer, DOWN, buff=0.3)
        numer_grp = VGroup(numer, numer_tag).next_to(denom_grp, DOWN, buff=1.0)
        fit_to_frame(VGroup(denom_grp, numer_grp))

        with self.voiceover(
            text="The outcomes with all distinct birthdays are exactly those drawn "
                 "without replacement, ordered — a k-permutation of three hundred "
                 "sixty-five: three sixty-five times three sixty-four, down to three "
                 "hundred sixty-five minus k plus one."
        ):
            self.play(Write(numer))
            self.play(FadeIn(numer_tag))

        self.play(FadeOut(denom_grp), FadeOut(numer_grp))

        formula = MathTex(
            r"\Pr(\text{shared})",
            r"=",
            r"1 - \frac{365!}{(365-k)!\,\cdot\,365^{k}}",
            font_size=BODY, color=ACCENT,
        ).move_to(ORIGIN)
        fit_to_frame(formula)

        with self.voiceover(
            text="The probability all are distinct is the ratio of those two "
                 "counts. So the probability of at least one shared birthday is one "
                 "minus three hundred sixty-five factorial, over three hundred "
                 "sixty-five minus k factorial, times three sixty-five to the k."
        ):
            self.play(Write(formula))
            self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class BirthdayPunchline(VoiceoverScene):
    """Beat: birthday-punchline -- the rising curve, the 23 callout, the outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Surprise at 23")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0, 1, 0.25],
            x_length=8.5,
            y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 22},
            tips=False,
        )
        x_lab = Text("k  (people)", font_size=CAPTION, color=MUTED)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.4)
        y_lab = MathTex(r"\Pr(\text{shared})", font_size=SMALL, color=MUTED)
        y_lab.next_to(axes.y_axis, UP, buff=0.25)
        chart = VGroup(axes, x_lab, y_lab)
        chart.next_to(title, DOWN, buff=0.5)
        fit_to_frame(chart)

        ks = list(range(1, 51))
        pts = [axes.c2p(k, p_match(k)) for k in ks]
        curve = VMobject(color=ACCENT).set_points_as_corners(pts)
        curve.set_stroke(ACCENT, 4)

        with self.voiceover(
            text="Now evaluate it. As the room fills, the probability of a shared "
                 "birthday climbs — slowly at first, then steeply."
        ):
            self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab), run_time=1.4)
            self.play(Create(curve), run_time=2.0)

        half_line = DashedLine(
            axes.c2p(0, 0.5), axes.c2p(50, 0.5),
            color=MUTED, stroke_width=2,
        )
        dot23 = Dot(axes.c2p(23, p_match(23)), color=INK, radius=0.07)
        call23 = MathTex(r"k = 23:\ \approx 0.507", font_size=SMALL, color=INK)
        # To the right (and a touch down) so it sits clear of the rising curve.
        call23.next_to(dot23, RIGHT, buff=0.5).shift(DOWN * 0.25)
        fit_to_frame(VGroup(chart, call23))

        with self.voiceover(
            text="It first passes one half at just k equals twenty-three, where it "
                 "is about zero point five oh seven. In a room of only twenty-three "
                 "people, it is already more likely than not that some pair shares a "
                 "birthday — even with three hundred sixty-five days to go around."
        ):
            self.play(Create(half_line))
            self.play(FadeIn(dot23, scale=1.5), Write(call23))

        with self.voiceover(
            text="The surprise comes from a swap: people imagine the chance that "
                 "someone shares their particular birthday, which grows far more "
                 "slowly, instead of the chance that any pair matches."
        ):
            self.play(Indicate(dot23, color=ACCENT, scale_factor=2.0))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing key idea + bridge (centred two-line key idea, house style).
        key_idea = VGroup(
            Text("Two questions — With or without replacement? With or without order?",
                 font_size=SMALL, color=INK),
            Text("The answers point to one cell of a 2x2 table.",
                 font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Next chapter:  The Axioms of Probability",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="And that is the chapter. Every sampling problem is two "
                 "questions: sampling with or without replacement? And sampling "
                 "with or without order? The answers dictate which cell of the "
                 "sampling table should be used. Next chapter, we make probability "
                 "models rigorous, with the axioms of probability."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
