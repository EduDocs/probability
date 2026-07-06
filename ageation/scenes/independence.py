# derived_from: content/14-independence-script.md
# derived_from_sha256: 11a06a01acf8b2f4e433db8d9959610f31eb4b9464c79721fdc4b75929da56f0
"""Chapter 4, Video 4 -- Independence.

Source notes : ../chapters/conditional_probability.tex  (independence of two
               events, of several events, and conditional independence) -- the
               coda that closes the conditional-probability chapter.
Script        : content/14-independence-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, one per <bookmark> segment -- the same
pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/independence.py ChapterOverview
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
    the rest of the series; switch the lines below and add OPENAI_API_KEY.
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1", transcription_model=None)


# --- Shared visual helpers (mirroring the house style) -----------------------

def omega_box(width=8.5, height=4.6):
    """The sample-space frame: a rounded rectangle labelled Omega."""
    box = RoundedRectangle(
        corner_radius=0.25, width=width, height=height, color=MUTED
    ).set_stroke(MUTED, width=2)
    box.set_stroke(opacity=0.9)
    lab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    lab.next_to(box.get_corner(UL), DR, buff=0.22)
    return VGroup(box, lab)


def make_dice_grid(cell=0.46):
    """A 6x6 outcome grid: rows are the red die, columns the blue die.

    Returns (grid, cells) where cells[(r, b)] is the square for red=r, blue=b.
    """
    grid = VGroup()
    cells = {}
    for r in range(1, 7):        # red die -> row (top = 1)
        for b in range(1, 7):    # blue die -> column (left = 1)
            sq = Square(side_length=cell).set_stroke(MUTED, 1.2)
            sq.set_fill(INK, 0.03)
            sq.move_to(RIGHT * (b - 3.5) * cell + DOWN * (r - 3.5) * cell)
            cells[(r, b)] = sq
            grid.add(sq)
    return grid, cells


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap, the guiding question, and the three-part outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Independence",
            "When knowing one event tells you nothing "
            "about another.",
            kicker="Chapter 4  ·  Conditional Probability",
        )
        fit_to_frame(intro)
        tag = progress_tag(4, 4).to_corner(DR, buff=0.4)

        question = Text("When does evidence change nothing?",
                        font_size=BODY, color=ACCENT)
        outline = VGroup(
            Text("1.  Two events", font_size=SMALL, color=INK),
            Text("2.  Multiple events", font_size=SMALL, color=INK),
            Text("3.  Conditional independence", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        # Build the card, then reveal the question as it is asked.
        with self.voiceover(
            text="Bayes' rule showed how evidence reshapes our beliefs. This video "
                 "is about the opposite situation: when evidence changes nothing. "
                 "Two events are independent if learning one tells you nothing about "
                 "the other. It sounds simple, and for two events it nearly is — but "
                 "independence hides some genuine surprises. It is not the same as "
                 "events being incompatible; with three or more events it splinters "
                 "into pairwise and mutual versions that don't coincide; and it can "
                 "appear or vanish the instant we condition on something else."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

            block = VGroup(question, outline).arrange(DOWN, buff=0.7)
            block.next_to(intro, DOWN, buff=1.1)
            fit_to_frame(block)
            self.play(Write(question), run_time=0.9)

        # Reveal each outline item exactly as it is named.
        with self.voiceover(
            text="We'll take these in turn: two events, then many, then "
                 "independence under conditioning."
        ) as tracker:
            self.play(FadeIn(outline[0], shift=RIGHT * 0.3), run_time=0.5)
            self.wait(max(0.1, tracker.duration * 0.28))
            self.play(FadeIn(outline[1], shift=RIGHT * 0.3), run_time=0.5)
            self.wait(max(0.1, tracker.duration * 0.22))
            self.play(FadeIn(outline[2], shift=RIGHT * 0.3), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Independence(VoiceoverScene):
    """Beat: independence -- definition, dice, disjointness, the gambler's fallacy."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Independence of Two Events")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- define: the product rule and its conditional reading. ---
        main = MathTex(r"\Pr(A \cap B) = \Pr(A)\,\Pr(B)",
                       font_size=SECTION, color=ACCENT)
        cond = MathTex(r"\Pr(A \mid B) = \Pr(A)", font_size=BODY, color=INK)
        note = Text("symmetric — B carries no information about A",
                    font_size=CAPTION, color=MUTED)
        define = VGroup(main, cond, note).arrange(DOWN, buff=0.5)
        define.move_to(DOWN * 0.3)
        fit_to_frame(define)

        with self.voiceover(
            text="Start with the definition. Two events A and B are independent when "
                 "the probability of both is the product of their probabilities — Pr "
                 "of A-and-B equals Pr of A times Pr of B. When B has positive "
                 "probability that's the same as saying Pr of A given B equals Pr of "
                 "A: conditioning on B leaves A's probability untouched. The "
                 "posterior equals the prior — B carries no information about A. And "
                 "it's symmetric: if A is independent of B, then B is independent of A."
        ):
            self.play(Write(main))
            self.play(FadeIn(cond, shift=UP * 0.15))
            self.play(FadeIn(note, shift=UP * 0.1))

        self.play(FadeOut(define))

        # --- dice: a 6x6 outcome grid with numbered axes. ---
        grid, cells = make_dice_grid()
        # Numeric axis labels: blue die 1..6 along the top, red die 1..6 down
        # the left, so every cell can be read off by its coordinates.
        col_nums = VGroup(*[
            MathTex(str(b), font_size=CAPTION, color=MUTED).next_to(
                cells[(1, b)], UP, buff=0.12) for b in range(1, 7)])
        row_nums = VGroup(*[
            MathTex(str(r), font_size=CAPTION, color=MUTED).next_to(
                cells[(r, 1)], LEFT, buff=0.12) for r in range(1, 7)])
        blue_lab = Text("blue", font_size=CAPTION, color=MUTED).next_to(
            col_nums, UP, buff=0.2)
        red_lab = Text("red", font_size=CAPTION, color=MUTED).rotate(PI / 2).next_to(
            row_nums, LEFT, buff=0.2)
        axes_labs = VGroup(col_nums, row_nums, blue_lab, red_lab)
        grid_group = VGroup(grid, axes_labs).move_to(LEFT * 3.3)
        fit_to_frame(grid_group)

        indep = VGroup(
            MathTex(r"\Pr(\{r=4\}\cap\{b=6\})", font_size=SMALL, color=INK),
            MathTex(r"= \tfrac{1}{36} = \tfrac16\cdot\tfrac16",
                    font_size=SMALL, color=ACCENT),
            Text("independent", font_size=CAPTION, color=ACCENT),
        ).arrange(DOWN, buff=0.22)
        dep = VGroup(
            MathTex(r"\Pr(\{r=4\}\cap\{r+b=11\})", font_size=SMALL, color=INK),
            MathTex(r"= 0 \neq \tfrac16\cdot\Pr(r+b=11)",
                    font_size=SMALL, color=MUTED),
            Text("dependent", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.22)
        eqs = VGroup(indep, dep).arrange(DOWN, buff=0.7).move_to(RIGHT * 3.3)
        fit_to_frame(eqs)

        # Independent case: the event {r=4} is a blue row, {b=6} a yellow column,
        # and their single overlap cell — the joint — glows green.
        with self.voiceover(
            text="Two dice, one red, one blue — thirty-six equally likely outcomes. "
                 "A four on the red die and a six on the blue: the probability of "
                 "both is one thirty-sixth, which is one-sixth times one-sixth. "
                 "The events are independent."
        ):
            self.play(Create(grid, lag_ratio=0.01), run_time=1.4)
            self.play(FadeIn(axes_labs))
            self.play(
                *[cells[(4, b)].animate.set_fill(BAR, 0.5)
                  for b in range(1, 7) if b != 6],
                *[cells[(r, 6)].animate.set_fill(ACCENT, 0.5)
                  for r in range(1, 7) if r != 4],
            )
            self.play(cells[(4, 6)].animate.set_fill(GREEN, 0.85))
            self.play(FadeIn(indep, shift=UP * 0.1))

        indep_lit = {cells[(4, b)] for b in range(1, 7)}
        indep_lit |= {cells[(r, 6)] for r in range(1, 7)}

        # Dependent case: clear the independent lighting first, then show {r=4}
        # (blue) and {sum=11} (red) never sharing a cell.
        with self.voiceover(
            text="But a four on the red die and a sum of eleven? A red four makes "
                 "a sum of eleven impossible — eleven needs a five and a six — so "
                 "the joint probability is zero, nowhere near one-sixth times the "
                 "probability of the sum. The events are dependent."
        ):
            self.play(*[c.animate.set_fill(INK, 0.03) for c in indep_lit])
            self.play(*[cells[(4, b)].animate.set_fill(BAR, 0.5)
                        for b in range(1, 7)])
            self.play(cells[(5, 6)].animate.set_fill(MAROON, 0.7),
                      cells[(6, 5)].animate.set_fill(MAROON, 0.7))
            self.play(FadeIn(dep, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in [grid_group, eqs]])

        # --- disjoint: two disjoint blobs inside Omega. ---
        frame = omega_box(width=6.0, height=4.2).move_to(LEFT * 3.2)
        blobA = Circle(radius=0.85, color=INK).set_stroke(INK, 2)
        blobA.set_fill(BAR, 0.5).move_to(LEFT * 4.4 + UP * 0.2)
        blobB = Circle(radius=0.85, color=INK).set_stroke(INK, 2)
        blobB.set_fill(ACCENT, 0.5).move_to(LEFT * 1.9 + DOWN * 0.4)
        labA = MathTex("A", font_size=SMALL, color=INK).move_to(blobA)
        labB = MathTex("B", font_size=SMALL, color=INK).move_to(blobB)
        disjoint_pic = VGroup(frame, blobA, blobB, labA, labB)
        fit_to_frame(disjoint_pic)

        disjoint_eq = VGroup(
            MathTex(r"A \cap B = \varnothing", font_size=BODY, color=INK),
            MathTex(r"\Pr(A \cap B) = 0 < \Pr(A)\,\Pr(B)",
                    font_size=SMALL, color=ACCENT),
            Text("disjoint ≠ independent", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.3)
        fit_to_frame(disjoint_eq)
        # Balance the outer gaps: nudge the box group right so its left margin
        # equals the equation column's right margin.
        disjoint_pic.shift(
            RIGHT * (-disjoint_eq.get_right()[0] - disjoint_pic.get_left()[0]))

        with self.voiceover(
            text="And beware one seductive error: independence is not disjointness. "
                 "In fact, disjoint events with positive probability are the opposite "
                 "of independent — if they can't co-occur, then learning one happened "
                 "tells you the other definitely did not. Their joint probability is "
                 "zero, while the product of their probabilities is positive."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(blobA), FadeIn(labA), FadeIn(blobB), FadeIn(labB))
            self.play(Write(disjoint_eq[0]))
            self.play(FadeIn(disjoint_eq[1], shift=UP * 0.1))
            self.play(FadeIn(disjoint_eq[2], shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in [disjoint_pic, disjoint_eq]])

        # --- gambler: a run of heads then a next toss still at 1/2. ---
        run = VGroup()
        for _ in range(5):
            c = Circle(radius=0.34, color=INK).set_stroke(INK, 2).set_fill(BAR, 0.25)
            lab = MathTex("H", font_size=SMALL, color=INK).move_to(c)
            run.add(VGroup(c, lab))
        run.arrange(RIGHT, buff=0.3)
        nxt = Circle(radius=0.34, color=ACCENT).set_stroke(ACCENT, 2.5)
        nxt.set_fill(ACCENT, 0.12)
        qmark = MathTex("?", font_size=BODY, color=ACCENT).move_to(nxt)
        next_toss = VGroup(nxt, qmark).next_to(run, RIGHT, buff=0.55)
        coins = VGroup(run, next_toss).move_to(UP * 1.0)
        fit_to_frame(coins)

        still = MathTex(r"\Pr(\text{tails next}) = \tfrac12",
                        font_size=BODY, color=INK)
        still.next_to(coins, DOWN, buff=0.7)
        caption = Text("the gambler's fallacy", font_size=SMALL, color=ACCENT)
        caption.next_to(still, DOWN, buff=0.5)
        gambler = VGroup(coins, still, caption)
        fit_to_frame(gambler)

        with self.voiceover(
            text="Independence also means trials have no memory. A fair coin that "
                 "just landed heads five times running is exactly as likely to show "
                 "tails next toss as it ever was — one-half. Believing a tail is "
                 "somehow \"due\" is the gambler's fallacy: the long run balances out "
                 "by swamping the past with fresh trials, never by correcting it."
        ):
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in run],
                                  lag_ratio=0.25), run_time=1.2)
            self.play(FadeIn(next_toss, scale=1.2))
            self.play(Write(still))
            self.play(FadeIn(caption, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class MultipleEvents(VoiceoverScene):
    """Beat: multiple-events -- the full condition, pairwise counterexample, failure."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Independence of Several Events")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- define: every subset factors. ---
        cond = MathTex(
            r"\Pr\!\left(\bigcap_{i \in S} A_i\right) = \prod_{i \in S} \Pr(A_i)",
            font_size=SECTION, color=ACCENT,
        )
        forevery = Text("for every subset S", font_size=SMALL, color=INK)
        note = Text("3 events:  3 pairs  +  the triple", font_size=SMALL, color=MUTED)
        define = VGroup(cond, forevery, note).arrange(DOWN, buff=0.5)
        define.move_to(DOWN * 0.2)
        fit_to_frame(define)

        with self.voiceover(
            text="With more than two events, independence gets subtle. Events A-one "
                 "through A-n are independent only if every subset of them factors — "
                 "the probability of any bunch occurring together equals the product "
                 "of their individual probabilities. For three events A, B, C that's "
                 "four conditions: the three pairs, and the triple all at once."
        ):
            self.play(Write(cond))
            self.play(FadeIn(forevery, shift=UP * 0.1))
            self.play(FadeIn(note, shift=UP * 0.1))

        self.play(FadeOut(define))

        # --- pairwise: the coin-twice counterexample. ---
        outcomes = ["HH", "HT", "TH", "TT"]
        cell_sq = 0.9
        space = VGroup()
        space_cells = {}
        for i, o in enumerate(outcomes):
            row, col = divmod(i, 2)
            sq = Square(side_length=cell_sq).set_stroke(MUTED, 1.5)
            sq.set_fill(INK, 0.04)
            sq.move_to(RIGHT * (col - 0.5) * cell_sq + DOWN * (row - 0.5) * cell_sq)
            txt = MathTex(o, font_size=SMALL, color=INK).move_to(sq)
            space_cells[o] = sq
            space.add(VGroup(sq, txt))
        space_group = space.move_to(LEFT * 3.4)
        fit_to_frame(space_group)

        events = VGroup(
            MathTex(r"A:\ \text{heads first}", font_size=SMALL, color=INK),
            MathTex(r"B:\ \text{heads second}", font_size=SMALL, color=INK),
            MathTex(r"C:\ \text{tosses differ}", font_size=SMALL, color=INK),
            MathTex(r"\Pr(A)=\Pr(B)=\Pr(C)=\tfrac12", font_size=SMALL, color=MUTED),
            MathTex(r"\text{each pair} = \tfrac14", font_size=SMALL, color=ACCENT),
            Text("pairwise independent", font_size=CAPTION, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(RIGHT * 3.1)
        fit_to_frame(events)

        with self.voiceover(
            text="Why insist on all of them? Because the pairwise conditions don't "
                 "force the triple. Flip a fair coin twice."
        ):
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in space],
                                  lag_ratio=0.2), run_time=1.2)

        # Each event line appears as it is named.
        with self.voiceover(text="Let A be heads on the first toss,"):
            self.play(FadeIn(events[0], shift=RIGHT * 0.2))
        with self.voiceover(text="B heads on the second,"):
            self.play(FadeIn(events[1], shift=RIGHT * 0.2))
        with self.voiceover(text="and C the event that the two tosses differ."):
            self.play(FadeIn(events[2], shift=RIGHT * 0.2))

        with self.voiceover(
            text="Each has probability one-half, and any two are independent — "
                 "every pair multiplies correctly to one quarter."
        ):
            self.play(FadeIn(events[3], shift=UP * 0.1))
            self.play(FadeIn(events[4], shift=UP * 0.1),
                      FadeIn(events[5], shift=UP * 0.1))

        # --- fail: the triple collapses. ---
        fail_eq = MathTex(
            r"\Pr(A \cap B \cap C) = 0 \neq \tfrac18 = \Pr(A)\,\Pr(B)\,\Pr(C)",
            font_size=SMALL, color=INK,
        )
        fail_cap = MathTex(r"\text{pairwise} \;\not\Rightarrow\; \text{mutual}",
                           font_size=BODY, color=ACCENT)
        fail = VGroup(fail_eq, fail_cap).arrange(DOWN, buff=0.4)
        fail.to_edge(DOWN, buff=0.8)
        fit_to_frame(fail)

        with self.voiceover(
            text="But all three together? A and B means two heads, which rules C out "
                 "entirely — so the triple probability is zero, while the product of "
                 "the three is one-eighth. Pairwise independent, yet not independent. "
                 "The triple condition is genuinely needed: it neither follows from "
                 "the pairs nor implies them."
        ):
            self.play(space_cells["HH"].animate.set_fill(MAROON, 0.55))
            self.play(Write(fail_eq))
            self.play(FadeIn(fail_cap, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionalIndependence(VoiceoverScene):
    """Beat: conditional-independence -- definition, create, destroy, and close."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditional Independence")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- define: factoring under the conditional law. ---
        cond = MathTex(
            r"\Pr(A_1 \cap A_2 \mid B) = \Pr(A_1 \mid B)\,\Pr(A_2 \mid B)",
            font_size=SECTION, color=ACCENT,
        )
        note = Text("ordinary independence, measured in the world where B is known",
                    font_size=CAPTION, color=MUTED)
        define = VGroup(cond, note).arrange(DOWN, buff=0.5).move_to(DOWN * 0.2)
        fit_to_frame(define)

        with self.voiceover(
            text="Finally, independence can live inside a condition. Two events are "
                 "conditionally independent given B if they factor under the "
                 "conditional law: Pr of A-one-and-A-two given B equals Pr of A-one "
                 "given B times Pr of A-two given B. Because the conditional law is "
                 "itself a genuine probability law, this is just ordinary "
                 "independence — measured in the world where B is known."
        ):
            self.play(Write(cond))
            self.play(FadeIn(note, shift=UP * 0.1))

        self.play(FadeOut(define))

        # --- create: conditioning can create independence. ---
        create_label = Text("conditioning CREATES independence",
                            font_size=BODY, color=GREEN).to_edge(UP, buff=1.3)

        # Left visual: the toss-count outcomes 1..6 (then ...), with a row of
        # membership dots under each cell for B (>1), A_1 (even), A_2 (<6).
        kstrip = VGroup()
        for k in range(1, 7):
            sq = Square(side_length=0.55).set_stroke(MUTED, 1.2).set_fill(INK, 0.05)
            sq.add(MathTex(str(k), font_size=SMALL, color=INK).move_to(sq))
            kstrip.add(sq)
        kstrip.arrange(RIGHT, buff=0.1)
        kell = MathTex(r"\cdots", font_size=SMALL, color=MUTED).next_to(
            kstrip, RIGHT, buff=0.15)

        def mrow(members, col, dy, label_tex):
            dots = VGroup(*[
                Dot(radius=0.08, color=col).move_to(
                    kstrip[k - 1].get_center() + DOWN * dy)
                for k in members])
            lab = MathTex(label_tex, font_size=CAPTION, color=col).move_to(
                [kstrip.get_left()[0] - 1.15,
                 kstrip[0].get_center()[1] - dy, 0])
            return VGroup(dots, lab)

        rowB = mrow(range(2, 7), TEAL, 0.7, r"B:\ k>1")
        rowA1 = mrow((2, 4, 6), BAR, 1.15, r"A_1:\ \text{even}")
        rowA2 = mrow(range(1, 6), ACCENT, 1.6, r"A_2:\ k<6")
        strip_vis = VGroup(kstrip, kell, rowB, rowA1, rowA2)
        strip_vis.move_to(LEFT * 2.6 + DOWN * 0.4)
        fit_to_frame(strip_vis)

        # Right: the clean factorization under B.
        head = MathTex(r"\Pr(A_1 \cap A_2 \mid B)", font_size=SMALL, color=INK)
        factor = MathTex(r"\tfrac58 = \tfrac23 \cdot \tfrac{15}{16}",
                         font_size=BODY, color=ACCENT)
        unc = Text("not independent unconditionally", font_size=CAPTION, color=MUTED)
        rightcol = VGroup(head, factor, unc).arrange(DOWN, buff=0.35)
        rightcol.move_to(RIGHT * 3.7 + DOWN * 0.4)
        fit_to_frame(rightcol)

        with self.voiceover(
            text="Conditioning can create independence. Toss a coin until heads is seen "
                 "for the first time; let B be the event that it took more than one toss, "
                 "A-one be the event that the count is even, and A-two be the event that "
                 "the count remains under six. Unconditionally, A-one and A-two are not "
                 "independent: their joint probability is five-sixteenths, which does not "
                 "match the product of their separate probabilities. But given B they "
                 "factor cleanly: the conditional probability of A-one is two-thirds, the "
                 "conditional probability of A-two is fifteen-sixteenths, and their joint conditional probability "
                 "is five-eighths — exactly two-thirds times fifteen-sixteenths. "
                 "Conditioning made them independent."
        ):
            self.play(FadeIn(create_label, shift=DOWN * 0.1))
            self.play(LaggedStart(*[FadeIn(m) for m in kstrip], lag_ratio=0.1),
                      FadeIn(kell))
            self.play(FadeIn(rowB, shift=UP * 0.1))
            self.play(FadeIn(rowA1, shift=UP * 0.1), FadeIn(rowA2, shift=UP * 0.1))
            self.play(Write(head))
            self.play(Write(factor))
            self.play(FadeIn(unc, shift=UP * 0.1))

        self.play(FadeOut(create_label), FadeOut(strip_vis), FadeOut(rightcol))

        # --- destroy: conditioning can destroy independence. ---
        destroy_label = Text("conditioning DESTROYS independence",
                            font_size=BODY, color=MAROON).to_edge(UP, buff=1.3)

        # Left visual: the dice grid -- {r=2} (blue) and {b=6} (yellow) meet in
        # one green cell (independent), but that cell has sum 8, so conditioning
        # on an odd sum crosses it out.
        dgrid, dcells = make_dice_grid(cell=0.4)
        dcol = VGroup(*[MathTex(str(b), font_size=CAPTION, color=MUTED).next_to(
            dcells[(1, b)], UP, buff=0.1) for b in range(1, 7)])
        drow = VGroup(*[MathTex(str(r), font_size=CAPTION, color=MUTED).next_to(
            dcells[(r, 1)], LEFT, buff=0.1) for r in range(1, 7)])
        dgrid_group = VGroup(dgrid, dcol, drow).move_to(LEFT * 3.4 + DOWN * 0.2)
        fit_to_frame(dgrid_group)
        cross = VGroup(
            Line(dcells[(2, 6)].get_corner(UL), dcells[(2, 6)].get_corner(DR)),
            Line(dcells[(2, 6)].get_corner(UR), dcells[(2, 6)].get_corner(DL)),
        ).set_stroke(MAROON, 5)

        outright = MathTex(r"\Pr(\{r=2\}\cap\{b=6\}) = \tfrac{1}{36}",
                           font_size=SMALL, color=INK)
        given = MathTex(r"\Pr(\cdot \mid \text{sum odd}) = 0",
                        font_size=SMALL, color=ACCENT)
        why = Text("2 + 6 = 8 is even → excluded", font_size=CAPTION, color=MUTED)
        drightcol = VGroup(outright, given, why).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.4 + DOWN * 0.2)
        fit_to_frame(drightcol)

        with self.voiceover(text="Conditioning can destroy independence."):
            self.play(FadeIn(destroy_label, shift=DOWN * 0.1))
            self.play(Create(dgrid, lag_ratio=0.01), FadeIn(dcol), FadeIn(drow))

        with self.voiceover(text="A red-die two"):
            self.play(*[dcells[(2, b)].animate.set_fill(BAR, 0.5)
                        for b in range(1, 7) if b != 6])

        with self.voiceover(
            text="and a blue-die six are independent outright — one thirty-sixth."
        ):
            self.play(*[dcells[(r, 6)].animate.set_fill(ACCENT, 0.5)
                        for r in range(1, 7) if r != 2])
            self.play(dcells[(2, 6)].animate.set_fill(GREEN, 0.85), Write(outright))

        with self.voiceover(
            text="But condition on the sum being odd: two plus six is eight, which "
                 "is even, so the joint conditional probability is zero,"
        ):
            self.play(Create(cross), FadeIn(given, shift=UP * 0.1))

        with self.voiceover(
            text="while each event alone still has conditional probability "
                 "one-sixth. The condition broke their independence."
        ):
            self.play(FadeIn(why, shift=UP * 0.1))

        self.play(FadeOut(destroy_label), FadeOut(dgrid_group), FadeOut(cross),
                  FadeOut(drightcol))

        # --- outro: key idea + bridge to the next chapter. ---
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            MathTex(r"A \perp B \iff \Pr(A \cap B) = \Pr(A)\,\Pr(B)",
                    font_size=BODY, color=INK),
            VGroup(
                Text("For multiple events, pairwise independence is weaker than "
                     "independence;", font_size=SMALL, color=MUTED),
                Text("conditioning can create or destroy it.",
                     font_size=SMALL, color=MUTED),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45)
        fit_to_frame(outro)

        with self.voiceover(
            text="So independence is not one idea but a family of them — sensitive to "
                 "how many events you weigh, and to what you already know. That "
                 "completes conditional probability. "
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.15), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
