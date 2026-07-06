# derived_from: content/13-bayes-monty-hall-script.md
# derived_from_sha256: 564b0e243c964bddaa92adc75691a5307e22dff6df355d0b8a033b821e7ea835
"""Chapter 4, Video 3 -- Bayes' Rule and the Monty Hall Problem.

Source notes : conditional-probability chapter (Bayes' rule, base-rate
               fallacy, and the Monty Hall problem).
Script        : content/13-bayes-monty-hall-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, one per ``<bookmark>`` mark in the
script -- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/bayes_monty_hall.py ChapterOverview
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
    outro_bridge,
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

def door(index, width=1.4, height=3.0):
    """A tall closed door labelled with its number."""
    panel = RoundedRectangle(
        corner_radius=0.12, width=width, height=height, color=MUTED
    ).set_stroke(MUTED, width=2).set_fill(BAR, opacity=0.12)
    knob = Dot(radius=0.06, color=MUTED).move_to(
        panel.get_right() + LEFT * 0.22
    )
    num = MathTex(str(index), font_size=BODY, color=INK).move_to(
        panel.get_center() + UP * 0.9
    )
    return VGroup(panel, knob, num)


def goat_icon(color="#C9C9C9"):
    """A small, stylized goat face (draft-quality) revealed behind a door."""
    head = Ellipse(width=0.62, height=0.82).set_fill(color, 1).set_stroke(WHITE, 2)
    horn_l = Line(head.get_top() + LEFT * 0.12,
                  head.get_top() + LEFT * 0.26 + UP * 0.26).set_stroke(WHITE, 3)
    horn_r = Line(head.get_top() + RIGHT * 0.12,
                  head.get_top() + RIGHT * 0.26 + UP * 0.26).set_stroke(WHITE, 3)
    ear_l = Ellipse(width=0.28, height=0.12).set_fill(color, 1).set_stroke(
        WHITE, 1.5).move_to(head.get_left() + LEFT * 0.02)
    ear_r = Ellipse(width=0.28, height=0.12).set_fill(color, 1).set_stroke(
        WHITE, 1.5).move_to(head.get_right() + RIGHT * 0.02)
    eye_l = Dot(radius=0.045, color=BLACK).move_to(
        head.get_center() + LEFT * 0.13 + UP * 0.12)
    eye_r = Dot(radius=0.045, color=BLACK).move_to(
        head.get_center() + RIGHT * 0.13 + UP * 0.12)
    snout = Ellipse(width=0.26, height=0.2).set_fill("#A8A8A8", 1).set_stroke(
        WHITE, 1).move_to(head.get_center() + DOWN * 0.22)
    beard = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.2).set_stroke(
        WHITE, 3)
    return VGroup(ear_l, ear_r, horn_l, horn_r, head, snout, eye_l, eye_r, beard)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card, recap, and the goal of the video."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Bayes' Rule",
            "Reverse conditioning with Bayes' rule to update beliefs from "
            "evidence.",
            kicker="Chapter 4  ·  Conditional Probability",
        )
        fit_to_frame(intro)
        tag = progress_tag(3, 4).to_corner(DR, buff=0.4)

        recap = MathTex(
            r"\Pr(A_i \mid B) = "
            r"\frac{\Pr(A_i)\,\Pr(B \mid A_i)}"
            r"{\sum_k \Pr(A_k)\,\Pr(B \mid A_k)}",
            font_size=BODY, color=MUTED,
        )
        goal = Text(
            "Bayes' rule runs the arrow backwards: from effect to cause.",
            font_size=SMALL, color=ACCENT,
        )
        panel = VGroup(recap, goal).arrange(DOWN, buff=0.5)

        with self.voiceover(
            text="The total probability theorem let us compute the probability "
                 "of an effect from its causes. Bayes' rule runs the arrow "
                 "backwards: given that the effect happened, how likely was each "
                 "cause? This is the mathematics of inference — of evidence, of "
                 "learning from data. In this video we derive Bayes' rule, name "
                 "its three ingredients — prior, likelihood, and posterior — "
                 "confront a famous trap in probabilistic reasoning, and finish "
                 "with the puzzle that has started many arguments in probability: "
                 "the Monty Hall problem."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)
            panel.next_to(intro, DOWN, buff=0.9)
            fit_to_frame(panel)
            self.play(Write(recap), run_time=1.2)
            self.play(FadeIn(goal, shift=UP * 0.15), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class BayesRule(VoiceoverScene):
    """Beat: bayes-rule -- invert with the product rule, expand, name the parts."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Bayes' Rule")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        product = MathTex(
            r"\Pr(A_i \cap B)", r"=", r"\Pr(A_i \mid B)\,\Pr(B)",
            r"=", r"\Pr(B \mid A_i)\,\Pr(A_i)",
            font_size=BODY, color=INK,
        )
        bayes1 = MathTex(
            r"\Pr(A_i \mid B)", r"=",
            r"\frac{\Pr(A_i)\,\Pr(B \mid A_i)}{\Pr(B)}",
            font_size=BODY, color=INK,
        )
        stack = VGroup(product, bayes1).arrange(DOWN, buff=0.7)
        stack.next_to(title, DOWN, buff=0.7)
        fit_to_frame(stack)
        cond = MathTex(r"\text{requires }\ \Pr(B) > 0",
                       font_size=CAPTION, color=MUTED)
        cond.next_to(bayes1, DOWN, buff=0.3)

        with self.voiceover(
            text="The derivation is short. The probability of A-i and B can be "
                 "written two ways with the product rule — as Pr of A-i given B "
                 "times Pr of B, or as Pr of B given A-i times Pr of A-i."
        ):
            self.play(Write(product), run_time=1.6)

        with self.voiceover(
            text="Set the two equal and divide by Pr of B, and you have Bayes' "
                 "rule: Pr of A-i given B is Pr of A-i, times Pr of B given A-i, "
                 "over Pr of B."
        ):
            self.play(Write(bayes1), run_time=1.4)
            self.play(FadeIn(cond, shift=UP * 0.1), run_time=0.6)

        bayes2 = MathTex(
            r"\Pr(A_i \mid B)", r"=",
            r"\frac{\Pr(A_i)\,\Pr(B \mid A_i)}"
            r"{\sum_k \Pr(A_k)\,\Pr(B \mid A_k)}",
            font_size=BODY, color=ACCENT,
        )
        bayes2.move_to(bayes1)

        with self.voiceover(
            text="And that denominator is exactly a total-probability sum over "
                 "the partition of causes, so we can write the whole thing in "
                 "terms of priors and likelihoods alone."
        ):
            self.play(FadeOut(product, shift=UP * 0.3),
                      FadeOut(cond, shift=DOWN * 0.2))
            self.play(FadeTransform(bayes1, bayes2))
            fit_to_frame(bayes2)
            self.play(bayes2.animate.next_to(title, DOWN, buff=0.7))

        def named(label, expr, col):
            t = Text(label, font_size=CAPTION, color=col)
            m = MathTex(expr, font_size=SMALL, color=col)
            return VGroup(t, m).arrange(DOWN, buff=0.18)

        names = VGroup(
            named("prior", r"\Pr(A_i)", ACCENT),
            named("likelihood", r"\Pr(B \mid A_i)", ACCENT),
            named("posterior", r"\Pr(A_i \mid B)", ACCENT),
        ).arrange(RIGHT, buff=1.0)
        names.next_to(bayes2, DOWN, buff=0.7)
        fit_to_frame(names)

        # A small "belief meter": the evidence slides the prior to the posterior.
        bl = Line(LEFT * 3.0, RIGHT * 3.0).set_stroke(MUTED, 2)
        z = MathTex("0", font_size=CAPTION, color=MUTED).next_to(
            bl.get_left(), DOWN, buff=0.15)
        o = MathTex("1", font_size=CAPTION, color=MUTED).next_to(
            bl.get_right(), DOWN, buff=0.15)
        pri = Dot(radius=0.09, color=MUTED).move_to(bl.point_from_proportion(0.18))
        pos = Dot(radius=0.09, color=ACCENT).move_to(bl.point_from_proportion(0.62))
        pril = Text("prior", font_size=CAPTION, color=MUTED).next_to(
            pri, DOWN, buff=0.2)
        posl = Text("posterior", font_size=CAPTION, color=ACCENT).next_to(
            pos, DOWN, buff=0.2)
        upd = CurvedArrow(pri.get_top(), pos.get_top(), angle=-PI / 3,
                          color=ACCENT)
        updl = Text("evidence updates the belief", font_size=CAPTION,
                    color=MUTED).next_to(upd, UP, buff=0.2)
        belief = VGroup(bl, z, o, pri, pos, pril, posl, upd, updl)
        belief.next_to(names, DOWN, buff=0.7)
        fit_to_frame(belief)

        with self.voiceover(
            text="Each piece carries a name. The prior, Pr of A-i, is what we "
                 "believed before the evidence. The likelihood, Pr of B given "
                 "A-i, is how well each cause explains the evidence. And the "
                 "posterior, Pr of A-i given B, is the updated belief afterward. "
                 "Bayes' rule is the machine that turns priors into posteriors in "
                 "the light of what we observe."
        ):
            self.play(FadeIn(names[0], shift=UP * 0.15))
            self.play(FadeIn(names[1], shift=UP * 0.15))
            self.play(FadeIn(names[2], shift=UP * 0.15))
            self.play(Create(bl), FadeIn(z), FadeIn(o),
                      FadeIn(pri, scale=1.3), FadeIn(pril))
            self.play(Create(upd), FadeIn(pos, scale=1.3),
                      FadeIn(posl), FadeIn(updl))

        self.play(*[FadeOut(m) for m in self.mobjects])


class BaseRateFallacy(VoiceoverScene):
    """Beat: pitfalls -- inverse confusion, the disease test, and the base rate."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Confusion of the Inverse")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        neq = MathTex(
            r"\Pr(A \mid B)", r"\neq", r"\Pr(B \mid A)",
            font_size=SECTION, color=ACCENT,
        )
        # Glosses stacked on their own lines (side-by-side captions collided).
        gloss = VGroup(
            VGroup(
                MathTex(r"\Pr(A \mid B)", font_size=SMALL, color=INK),
                Text("the cause, given the evidence", font_size=CAPTION,
                     color=MUTED),
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex(r"\Pr(B \mid A)", font_size=SMALL, color=INK),
                Text("the evidence, given the cause", font_size=CAPTION,
                     color=MUTED),
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        gloss.next_to(neq, DOWN, buff=0.6)
        inverse = VGroup(neq, gloss)
        inverse.next_to(title, DOWN, buff=1.0)
        fit_to_frame(inverse)

        with self.voiceover(
            text="Bayes' rule also guards against a stubborn confusion. The "
                 "probability of A given B and the probability of B given A are "
                 "different questions with different answers — swapping them is "
                 "called confusion of the inverse, and in a courtroom, the "
                 "prosecutor's fallacy."
        ):
            self.play(Write(neq))
            self.play(FadeIn(gloss[0], shift=UP * 0.1))
            self.play(FadeIn(gloss[1], shift=UP * 0.1))

        self.play(FadeOut(inverse))

        # A natural-frequency tree makes the notions concrete: split a
        # population by disease status (the 1% prior / base rate), then by test
        # result (the 95% and 5% likelihoods), reading off true vs false
        # positives at the leaves.
        def node(top, sub, subcol=MUTED):
            return VGroup(
                Text(top, font_size=CAPTION, color=INK),
                Text(sub, font_size=CAPTION, color=subcol),
            ).arrange(DOWN, buff=0.08)

        root = node("10,000", "people").move_to(LEFT * 5.0)
        sick = node("sick", "100").move_to(LEFT * 1.5 + UP * 1.5)
        healthy = node("healthy", "9,900").move_to(LEFT * 1.5 + DOWN * 1.7)
        tp = node("test +", "95", subcol=ACCENT).move_to(RIGHT * 2.7 + UP * 2.0)
        fp = node("test +", "495", subcol=RED).move_to(RIGHT * 2.7 + DOWN * 0.6)

        def branch(a, b, lbl, dy):
            # Generous end-buffs keep the line clear of the node labels
            # ("people", "healthy", ...), leaving air around each node.
            ln = Line(a.get_center(), b.get_center(), buff=0.6)
            ln.set_stroke(MUTED, 2)
            m = MathTex(lbl, font_size=CAPTION, color=MUTED).move_to(
                ln.point_from_proportion(0.5) + UP * dy)
            return VGroup(ln, m)

        br1 = branch(root, sick, r"0.01", 0.24)
        br2 = branch(root, healthy, r"0.99", -0.24)
        br3 = branch(sick, tp, r"0.95", 0.24)
        br4 = branch(healthy, fp, r"0.05", -0.24)
        tree = VGroup(root, br1, br2, br3, br4, sick, healthy, tp, fp)
        fit_to_frame(tree)

        # Build the tree in step with the narration: the prior split as the
        # "one percent of the population" is spoken, the likelihood split with
        # the "ninety-five percent accurate" line, the leaves on "test positive".
        with self.voiceover(
            text="Here is how much it matters. A disease affects one percent of "
                 "the population."
        ):
            self.play(FadeIn(root))
            self.play(Create(br1[0]), Create(br2[0]),
                      FadeIn(sick, shift=RIGHT * 0.2),
                      FadeIn(healthy, shift=RIGHT * 0.2))
            self.play(Write(br1[1]), Write(br2[1]))

        with self.voiceover(
            text="A test is ninety-five percent accurate both ways: it catches "
                 "the disease ninety-five times in a hundred, and correctly "
                 "clears the healthy ninety-five times in a hundred."
        ):
            self.play(Create(br3[0]), Create(br4[0]),
                      FadeIn(tp, shift=RIGHT * 0.2),
                      FadeIn(fp, shift=RIGHT * 0.2))
            self.play(Write(br3[1]), Write(br4[1]))

        with self.voiceover(
            text="You test positive. What is the probability you're actually "
                 "sick?"
        ):
            self.play(Indicate(tp, color=ACCENT, scale_factor=1.15),
                      Indicate(fp, color=RED, scale_factor=1.15))

        compute = MathTex(
            r"\Pr(D \mid P)", r"=",
            r"\frac{0.01 \cdot 0.95}{0.01 \cdot 0.95 + 0.99 \cdot 0.05}",
            r"\approx", r"0.16",
            font_size=BODY, color=ACCENT,
        )
        compute.move_to(ORIGIN)
        fit_to_frame(compute)

        with self.voiceover(
            text="Bayes' rule: the prior times the likelihood — one percent "
                 "times ninety-five percent — over the total probability of a "
                 "positive test. Work it through and the answer is about sixteen "
                 "percent. Not ninety-five — sixteen."
        ):
            self.play(FadeOut(tree))
            self.play(Write(compute), run_time=1.8)
            self.play(Indicate(compute[4], color=ACCENT, scale_factor=1.3))

        self.play(compute.animate.scale(0.75).next_to(title, DOWN, buff=0.5))

        # 10x10 population grid: 1 true positive, ~5 false positives, rest healthy.
        cells = VGroup()
        for i in range(100):
            sq = Square(side_length=0.36).set_stroke(MUTED, width=1)
            if i == 0:
                sq.set_fill(ACCENT, opacity=1.0)
            elif i <= 5:
                sq.set_fill(RED, opacity=0.9)
            else:
                sq.set_fill(MUTED, opacity=0.22)
            cells.add(sq)
        cells.arrange_in_grid(rows=10, cols=10, buff=0.05)

        def legend_row(col, label):
            swatch = Square(side_length=0.3).set_fill(col, opacity=0.9)
            swatch.set_stroke(MUTED, width=1)
            txt = Text(label, font_size=CAPTION, color=INK)
            return VGroup(swatch, txt).arrange(RIGHT, buff=0.25)

        legend = VGroup(
            legend_row(ACCENT, "1 true positive"),
            legend_row(RED, "~5 false positives"),
            legend_row(MUTED, "healthy, correctly cleared"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        name_cap = Text("base-rate fallacy", font_size=SMALL, color=ACCENT)
        right_col = VGroup(legend, name_cap).arrange(DOWN, aligned_edge=LEFT,
                                                     buff=0.7)
        board = VGroup(cells, right_col).arrange(RIGHT, buff=0.8)
        board.next_to(compute, DOWN, buff=0.5)
        fit_to_frame(board)

        with self.voiceover(
            text="The reason is the base rate. Ninety-nine percent of people are "
                 "healthy, and five percent of that huge group test positive by "
                 "mistake — and those false positives far outnumber the true "
                 "positives drawn from the tiny one percent who are ill. Ignore "
                 "the prior and a positive result looks damning; keep it, and the "
                 "truth is far milder. Neglecting the base rate this way is the "
                 "base-rate fallacy."
        ):
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01),
                      run_time=2.2)
            self.play(FadeIn(legend, shift=RIGHT * 0.2))
            self.play(FadeIn(name_cap, shift=UP * 0.15))

        self.play(*[FadeOut(m) for m in self.mobjects])


class MontyHall(VoiceoverScene):
    """Beat: monty-hall -- setup, likelihoods, Bayes, the switch, and the close."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Monty Hall Problem")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        doors = VGroup(door(1), door(2), door(3)).arrange(RIGHT, buff=1.3)
        doors.next_to(title, DOWN, buff=0.9)
        pick = Text("your pick", font_size=CAPTION, color=ACCENT)
        pick.next_to(doors[0], DOWN, buff=0.3)
        # The goat waits behind door 3, revealed only when the door swings open.
        g = goat_icon().move_to(doors[2][0].get_center())
        glab = Text("goat", font_size=CAPTION, color=MUTED).next_to(
            doors[2][0], DOWN, buff=0.3)
        stage = VGroup(doors, pick, g, glab)
        fit_to_frame(stage)

        with self.voiceover(
            text="Now the classic. Three doors. Behind one, a car; behind each "
                 "of the others, a goat — the car equally likely anywhere. You "
                 "pick door one."
        ):
            self.play(LaggedStart(*[FadeIn(d) for d in doors], lag_ratio=0.25),
                      run_time=1.4)
            self.play(FadeIn(pick, shift=UP * 0.1))

        with self.voiceover(
            text="The host, who knows where the car is, opens a different door — "
                 "say door three — always revealing a goat, and offers you the "
                 "chance to switch. Should you take it?"
        ) as tracker:
            self.wait(max(0.3, tracker.duration * 0.30))
            # Swing door 3 open about its left hinge to a thin edge, revealing
            # the goat that was behind it.
            self.play(
                doors[2][0].animate.stretch(
                    0.12, 0, about_point=doors[2][0].get_left()
                ).set_fill(GREY_BROWN, 0.5),
                FadeOut(doors[2][1]), FadeOut(doors[2][2]),
                run_time=0.9,
            )
            self.play(FadeIn(g, scale=1.2), FadeIn(glab, shift=UP * 0.1),
                      run_time=0.8)

        self.play(stage.animate.scale(0.8).to_edge(LEFT, buff=1.5))

        table = VGroup(
            MathTex(r"\Pr(H \mid C_1) = \tfrac{1}{2}", font_size=SMALL, color=INK),
            MathTex(r"\Pr(H \mid C_2) = 1", font_size=SMALL, color=INK),
            MathTex(r"\Pr(H \mid C_3) = 0", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        table.to_edge(RIGHT, buff=1.9)
        fit_to_frame(table)

        with self.voiceover(
            text="Everything hinges on the host's options. If the car is behind "
                 "your door, door one, the host may open two or three freely — so "
                 "opening three has probability one-half. If the car is behind "
                 "door two, the host is forced: he can open neither your door nor "
                 "the car's, so he must open three — probability one. If the car "
                 "is behind door three, he would never open it — probability "
                 "zero."
        ):
            self.play(FadeIn(table[0], shift=RIGHT * 0.2))
            self.play(FadeIn(table[1], shift=RIGHT * 0.2))
            self.play(FadeIn(table[2], shift=RIGHT * 0.2))

        posteriors = VGroup(
            MathTex(r"\Pr(H) = \tfrac{1}{2}", font_size=BODY, color=INK),
            MathTex(r"\Pr(C_1 \mid H) = \tfrac{1}{3}", font_size=BODY,
                    color=ACCENT),
            MathTex(r"\Pr(C_2 \mid H) = \tfrac{2}{3}", font_size=BODY,
                    color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        stay_lab = Text("stay", font_size=CAPTION, color=MUTED)
        stay_lab.next_to(posteriors[1], RIGHT, buff=0.4)
        switch_lab = Text("switch", font_size=CAPTION, color=MUTED)
        switch_lab.next_to(posteriors[2], RIGHT, buff=0.4)
        result = VGroup(posteriors, stay_lab, switch_lab)
        result.to_edge(RIGHT, buff=1.9)
        fit_to_frame(result)

        with self.voiceover(
            text="By total probability, the host opens door three with "
                 "probability one-half. Now apply Bayes. The posterior that the "
                 "car is behind door one — staying — works out to one-third. The "
                 "posterior that it's behind door two — switching — is "
                 "two-thirds."
        ):
            self.play(FadeOut(table))
            self.play(Write(posteriors[0]))
            self.play(FadeIn(posteriors[1], shift=RIGHT * 0.2),
                      FadeIn(stay_lab))
            self.play(FadeIn(posteriors[2], shift=RIGHT * 0.2),
                      FadeIn(switch_lab))

        self.play(FadeOut(stage), FadeOut(result))

        axis = Line(LEFT * 3.5, RIGHT * 3.5, color=MUTED).to_edge(DOWN, buff=1.4)
        stay_bar = Rectangle(width=1.6, height=1.0, color=MUTED,
                             fill_color=MUTED, fill_opacity=0.5)
        stay_bar.next_to(axis.get_center() + LEFT * 2.0, UP, buff=0)
        switch_bar = Rectangle(width=1.6, height=2.0, color=ACCENT,
                               fill_color=ACCENT, fill_opacity=0.8)
        switch_bar.next_to(axis.get_center() + RIGHT * 2.0, UP, buff=0)
        stay_txt = VGroup(
            Text("stay", font_size=CAPTION, color=MUTED),
            MathTex(r"\tfrac{1}{3}", font_size=BODY, color=MUTED),
        ).arrange(DOWN, buff=0.15).next_to(stay_bar, UP, buff=0.35)
        switch_txt = VGroup(
            Text("switch", font_size=CAPTION, color=ACCENT),
            MathTex(r"\tfrac{2}{3}", font_size=BODY, color=ACCENT),
        ).arrange(DOWN, buff=0.15).next_to(switch_bar, UP, buff=0.35)
        # Arc from the stay bar's top corner to just outside the switch bar's
        # top-left corner, so the arrowhead never lands on the yellow rectangle.
        arrow = Arrow(stay_bar.get_corner(UR) + UP * 0.25,
                      switch_bar.get_corner(UL) + UP * 0.25,
                      color=ACCENT, buff=0.15)
        # Caption sits below the axis, clear of the bars and their labels.
        arrow_lab = Text("door 3's share moves to door 2", font_size=CAPTION,
                         color=ACCENT).next_to(axis, DOWN, buff=0.35)
        bars = VGroup(axis, stay_bar, switch_bar, stay_txt, switch_txt,
                      arrow, arrow_lab)
        fit_to_frame(bars)

        with self.voiceover(
            text="Switching doubles your chances, from one-third to two-thirds. "
                 "The opened door was never neutral: because the host is "
                 "constrained to dodge both your door and the car, his choice "
                 "pours door three's share of probability onto door two, not back "
                 "onto your original pick."
        ):
            self.play(Create(axis))
            self.play(GrowFromEdge(stay_bar, DOWN), FadeIn(stay_txt))
            self.play(GrowFromEdge(switch_bar, DOWN), FadeIn(switch_txt))
            self.play(GrowArrow(arrow), FadeIn(arrow_lab, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            "Bayes' rule turns priors into posteriors through the likelihoods.",
            next_title="Independence",
        )
        fit_to_frame(outro)

        with self.voiceover(
            text="Bayes' rule turned an argument into arithmetic. Next video: "
                 "independence — the special case where the evidence, however "
                 "carefully weighed, tells us nothing new."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
