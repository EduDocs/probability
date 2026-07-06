# derived_from: content/11-conditioning-events-script.md
# derived_from_sha256: 0ce04f7a095ad35b72b0e426e18190c391d33bb6c6b972e6ce0fe4cf40343a67
"""Chapter 4, Video 1 -- Conditioning on Events.

Source notes : conditional probability -- the definition of Pr(A | B), the
               proof that the conditional law obeys the three axioms, and the
               chain (multiplication) rule.
Script        : content/11-conditioning-events-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/conditioning_events.py ChapterOverview
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
    INK,
    TITLE,
    BODY,
    SMALL,
    CAPTION,
    section_title,
    intro_card,
    progress_tag,
    fit_to_frame,
    configure_openai_client,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


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


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + the four-video outline for the chapter."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # Manual intro card so the objective sits on two centred lines.
        intro = VGroup(
            Text("Chapter 4  ·  Conditional Probability",
                 font_size=SMALL, color=ACCENT),
            Text("Conditional Probability", font_size=TITLE, color=INK),
            VGroup(
                Text("Update a probability when partial information is revealed —",
                     font_size=SMALL, color=MUTED),
                Text("define conditional probability and chain events together.",
                     font_size=SMALL, color=MUTED),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(intro)
        tag = progress_tag(1, 4).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Conditioning on events", font_size=BODY, color=INK),
            Text("2.  The total probability theorem", font_size=BODY, color=INK),
            Text("3.  Bayes' rule", font_size=BODY, color=INK),
            Text("4.  Independence", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="The probabilistic model is now complete "
                 "— a sample space of possible outcomes, and a probability "
                 "law that gives each event its likelihood. But probability is "
                 "rarely frozen. The moment we learn something — a partial clue "
                 "about how the experiment turned out — the odds should shift. "
                 "This chapter is about exactly that: conditional probability, "
                 "the mathematics of updating beliefs in the light of "
                 "information. Across four videos we will define conditioning, "
                 "assemble probabilities across a partition with the total "
                 "probability theorem, invert them with Bayes' rule, and finally "
                 "ask when information changes nothing at all — independence. We "
                 "begin at the foundation: conditioning on an event."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)

            self.play(intro.animate.to_edge(UP), run_time=0.8)
            outline.next_to(intro, DOWN, buff=0.7)
            fit_to_frame(outline)
            self.play(
                LaggedStartMap(FadeIn, outline, shift=RIGHT * 0.4, lag_ratio=0.35),
                run_time=2.4,
            )

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditioningOnEvents(VoiceoverScene):
    """Beat: conditioning -- the die, the ratio, the frequency view, the def."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Conditioning on an Event")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- Left column: a fair die (drawn faces) inside an Omega box. ------
        # Pip layout on a unit 3x3 grid (x right, y up), scaled to the face.
        PIP = {
            1: [(0, 0)],
            2: [(-1, 1), (1, -1)],
            3: [(-1, 1), (0, 0), (1, -1)],
            4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
            5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
            6: [(-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)],
        }

        def die_face(n):
            sq = RoundedRectangle(
                corner_radius=0.12, width=1.3, height=1.3
            ).set_stroke(INK, 2)
            d = 0.30
            pips = VGroup(*[
                Dot(radius=0.078, color=INK).set_fill(INK, 1).move_to(
                    sq.get_center() + RIGHT * cx * d + UP * cy * d)
                for (cx, cy) in PIP[n]
            ])
            return VGroup(sq, pips)

        box = omega_box(width=5.9, height=4.9)
        faces = VGroup(*[die_face(n) for n in range(1, 7)])
        faces.arrange_in_grid(rows=2, cols=3, buff=0.5)
        faces.move_to(box[0]).shift(DOWN * 0.05)

        # The 1/6 label rides ABOVE each first-row face, BELOW each second-row
        # face, so the pips are never crowded.
        sixths = []
        for i, f in enumerate(faces):
            p = MathTex(r"1/6", font_size=CAPTION, color=MUTED)
            p.next_to(f, UP if i < 3 else DOWN, buff=0.14)
            sixths.append(p)
        sixths_group = VGroup(*sixths)

        # 1/3 relabels for the surviving odd faces {1,3,5}, in the same slots.
        thirds = VGroup()
        odd_thirds = {}
        for i in (0, 2, 4):
            t = MathTex(r"1/3", font_size=CAPTION, color=INK)
            t.move_to(sixths[i])
            thirds.add(t)
            odd_thirds[i] = t

        left = VGroup(box, faces, sixths_group, thirds)
        fit_to_frame(left)
        left.move_to(LEFT * 3.5 + DOWN * 0.15)

        # --- Right column: the ratio, the frequency view, the definition. ----
        ratio = VGroup(
            MathTex(r"\Pr(3 \mid \text{odd})", font_size=SMALL, color=INK),
            MathTex(r"= \frac{\Pr(3 \cap \{1,3,5\})}{\Pr(\{1,3,5\})} = \frac{1}{3}",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        freq = MathTex(
            r"\Pr(A \mid B) \approx \frac{N_{AB}}{N_B} = \frac{N_{AB}/N}{N_B/N}",
            font_size=SMALL, color=INK,
        )
        define = MathTex(
            r"\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)}",
            font_size=BODY, color=ACCENT,
        )
        note = MathTex(r"\Pr(B) > 0", font_size=CAPTION, color=MUTED)
        define_group = VGroup(define, note).arrange(DOWN, buff=0.25)

        right = VGroup(ratio, freq, define_group).arrange(DOWN, buff=0.55)
        fit_to_frame(right)
        right.move_to(RIGHT * 3.4 + DOWN * 0.1)
        dbox = SurroundingRectangle(
            define_group, color=ACCENT, buff=0.28, corner_radius=0.12
        ).set_stroke(ACCENT, 2)

        # Balance the outer black margins at the scene's end: nudge the die
        # group rightwards until its left gap equals the right column's right
        # gap (right_edge includes the accent box around the definition).
        right_edge = max(right.get_right()[0], dbox.get_right()[0])
        left.shift(RIGHT * (-right_edge - left.get_left()[0]))

        # Block 1 (lead-in): build the die.
        with self.voiceover(
            text="Start with a fair die — six faces, each with probability "
                 "one-sixth."
        ):
            self.play(Create(box[0]), Write(box[1]))
            self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.15), run_time=1.8)
            self.play(LaggedStartMap(FadeIn, sixths_group, lag_ratio=0.12),
                      run_time=1.2)

        # Block 2 (reveal): the clue removes the even faces, {1,3,5} re-normalize.
        with self.voiceover(
            text="Now someone tells you the face is odd. Three outcomes survive "
                 "— one, three, and five; the even faces are gone. Before the "
                 "clue those three were equally likely, and nothing about the "
                 "clue breaks that symmetry, so each now carries probability "
                 "one-third. Notice what happened: we discarded the impossible "
                 "outcomes and re-normalized the rest so they sum to one again."
        ):
            # Even faces dim and their 1/6 labels vanish; odd faces keep their
            # slot but the probability rescales 1/6 -> 1/3.
            self.play(
                *[faces[i].animate.set_opacity(0.15) for i in (1, 3, 5)],
                *[FadeOut(sixths[i]) for i in (1, 3, 5)],
                run_time=2.4,
            )
            self.play(
                *[FadeOut(sixths[i]) for i in (0, 2, 4)],
                *[FadeIn(odd_thirds[i]) for i in (0, 2, 4)],
            )

        # Block 3 (ratio).
        with self.voiceover(
            text="So the probability of rolling a three, given that the face is "
                 "odd, is one-third — which we can write as the probability of "
                 "\"three and odd\" divided by the probability of \"odd.\""
        ):
            self.play(Write(ratio))

        # Block 4 (frequency).
        with self.voiceover(
            text="Here is a second way to see the same formula. Imagine "
                 "repeating the experiment a huge number of times, N. Count the "
                 "trials where B happens, and among those, the ones where A "
                 "happens too. The fraction of B-trials that are also A-trials "
                 "is the conditional probability — N-A-B over N-B. Divide top "
                 "and bottom by N and each count turns into a probability, so "
                 "this ratio tends to the probability of A-and-B over the "
                 "probability of B."
        ):
            self.play(Write(freq))

        # Block 5 (define): the accented definition.
        with self.voiceover(
            text="That limit is the definition. For any event B with positive "
                 "probability, the conditional probability of A given B is the "
                 "probability of A-and-B, divided by the probability of B. It "
                 "rescales the law so that B becomes the new certain event."
        ):
            self.play(Write(define))
            self.play(FadeIn(note, shift=UP * 0.1), Create(dbox))
            self.play(Indicate(define, color=ACCENT, scale_factor=1.05))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ConditionalLaw(VoiceoverScene):
    """Beat: valid-law -- the three axioms hold, then a worked coin example."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Valid Probability Law")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        def axiom(name, tex, color=INK):
            lbl = Text(name, font_size=SMALL, color=MUTED)
            formula = MathTex(tex, font_size=SMALL, color=color)
            return VGroup(lbl, formula).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        nonneg = axiom(
            "Nonnegativity",
            r"\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)} \ge 0",
        )
        norm = axiom(
            "Normalization",
            r"\Pr(\Omega \mid B) = \frac{\Pr(B)}{\Pr(B)} = 1",
            color=ACCENT,
        )
        add = axiom(
            "Additivity",
            r"\Pr\!\left(\bigcup_k A_k \mid B\right) = \sum_k \Pr(A_k \mid B)",
        )
        checklist = VGroup(nonneg, norm, add).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        checklist.next_to(title, DOWN, buff=0.6)
        fit_to_frame(checklist)
        norm_box = SurroundingRectangle(
            norm, color=ACCENT, buff=0.2, corner_radius=0.12
        ).set_stroke(ACCENT, 2)

        # Block 1 (lead-in).
        with self.voiceover(
            text="Is this new object really a probability law? It is — it obeys "
                 "the same three axioms."
        ):
            self.play(FadeIn(title, shift=DOWN * 0.05), run_time=0.2)

        # Block 2 (nonneg).
        with self.voiceover(
            text="First, nonnegativity: a ratio of two nonnegative numbers can't "
                 "be negative."
        ):
            self.play(FadeIn(nonneg, shift=RIGHT * 0.3))

        # Block 3 (norm): the accented normalization line.
        with self.voiceover(
            text="Second, normalization. Condition the whole sample space on B: "
                 "the probability of Omega-and-B is just the probability of B, so "
                 "Pr of Omega given B is Pr of B over Pr of B — exactly one. "
                 "Under the conditional law, B carries all the probability."
        ):
            self.play(FadeIn(norm, shift=RIGHT * 0.3))
            self.play(Create(norm_box))

        # Block 4 (add).
        with self.voiceover(
            text="And third, additivity: if events are disjoint, intersecting "
                 "each with B keeps them disjoint, so their conditional "
                 "probabilities add. All three axioms hold — conditioning yields "
                 "a bona fide probability law, and every rule we proved last "
                 "chapter still works inside B."
        ):
            self.play(FadeIn(add, shift=RIGHT * 0.3))

        # Block 5 (coin): clear the checklist, work the coin example. A little
        # coin-toss figure (tails, then heads) makes the setup concrete.
        def coin(sym, col):
            c = Circle(radius=0.42, color=col).set_fill(col, 0.22)
            c.set_stroke(col, 4)
            return VGroup(c, Text(sym, font_size=SMALL, color=col).move_to(c))

        c1 = VGroup(
            coin("T", GRAY_B),
            Text("toss 1", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.16)
        c2 = VGroup(
            coin("H", GOLD),
            Text("toss 2", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.16)
        coins = VGroup(c1, c2).arrange(RIGHT, buff=0.7)
        coin_fig = VGroup(
            Text("Toss a fair coin until heads", font_size=CAPTION, color=MUTED),
            coins,
            Text("first heads on toss 2", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.35)
        fit_to_frame(coin_fig)
        coin_fig.move_to(LEFT * 3.5 + DOWN * 0.1)

        recall = MathTex(r"\Pr(\text{even}) = \frac{1}{3}",
                         font_size=SMALL, color=MUTED)
        worked = MathTex(
            r"\Pr(2 \mid \text{even}) = \frac{1/4}{1/3} = \frac{3}{4}",
            font_size=BODY, color=ACCENT,
        )
        example = VGroup(
            Text("A worked example", font_size=SMALL, color=INK),
            recall,
            worked,
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(example)
        example.move_to(RIGHT * 3.1 + DOWN * 0.1)

        with self.voiceover(
            text="Let's use it. A fair coin is tossed until the first heads; the "
                 "probability that this takes exactly k tosses is "
                 "two-to-the-minus-k. We showed earlier that the number of "
                 "tosses is even with probability one-third. What is the "
                 "probability it took exactly two tosses, given that it was "
                 "even? That's the probability of two — one quarter — over the "
                 "probability of even — one third — which is three quarters. "
                 "Knowing the count was even makes \"two\" quite likely."
        ):
            self.play(FadeOut(checklist), FadeOut(norm_box))
            self.play(FadeIn(coin_fig[0], shift=DOWN * 0.15))
            self.play(FadeIn(c1, scale=0.6))
            self.play(FadeIn(c2, scale=0.6), Flash(c2[0], color=GOLD, line_length=0.2))
            self.play(FadeIn(coin_fig[2], shift=UP * 0.1))
            self.play(FadeIn(example[0], shift=DOWN * 0.2))
            self.play(Write(recall))
            self.play(Write(worked))
            self.play(Indicate(worked, color=ACCENT, scale_factor=1.05))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChainRule(VoiceoverScene):
    """Beat: chain-rule -- the multiplication rule, the urn, the draws, outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Chain Rule")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- The two-event rule and its chained generalization. --------------
        two = MathTex(
            r"\Pr(A \cap B) = \Pr(A)\,\Pr(B \mid A)",
            font_size=BODY, color=ACCENT,
        )
        # Isolate the "=" as its own submobject ([1]) so the second line can be
        # aligned under the first line's equals sign.
        chain = MathTex(
            r"\Pr\!\left(\bigcap_{k=1}^{n} A_k\right)", r"=",
            r"\Pr(A_1)\,\Pr(A_2 \mid A_1)\,\Pr(A_3 \mid A_1, A_2)\cdots",
            font_size=SMALL, color=INK,
        )
        # Second line: expand each conditional as a ratio -- the telescoping
        # product, where each denominator cancels the previous numerator.
        telescope = MathTex(
            r"=",
            r"\Pr(A_1)\,\frac{\Pr(A_1 \cap A_2)}{\Pr(A_1)}"
            r"\,\frac{\Pr(A_1 \cap A_2 \cap A_3)}{\Pr(A_1 \cap A_2)}\cdots",
            font_size=SMALL, color=INK,
        )
        telescope.next_to(chain, DOWN, buff=0.35)
        telescope.align_to(chain[1], LEFT)   # its "=" under the "=" above
        white_eq = VGroup(chain, telescope)
        rule_group = VGroup(two, white_eq).arrange(DOWN, buff=0.55)
        fit_to_frame(rule_group)
        rule_group.move_to(DOWN * 0.15)

        # Block 1 (lead-in).
        with self.voiceover(
            text="Conditioning also runs the other way — it lets us build up the "
                 "probability of several events all happening together."
        ):
            self.play(FadeIn(title, shift=DOWN * 0.05), run_time=0.2)

        # Block 2 (rule).
        with self.voiceover(
            text="Rearrange the definition: the probability of A-and-B is the "
                 "probability of A, times the probability of B given A. Now "
                 "iterate. The probability that a whole list of events, A-one "
                 "through A-n, all occur is the probability of the first, times "
                 "the probability of the second given the first, times the third "
                 "given the first two, and so on down the chain. This is the "
                 "chain rule, and it falls out because the conditional "
                 "probabilities telescope — each denominator cancels the "
                 "previous numerator."
        ):
            self.play(Write(two))
            self.play(Write(chain))
            self.play(Write(telescope))

        # --- The urn (left column). ------------------------------------------
        urn = RoundedRectangle(
            corner_radius=0.3, width=2.6, height=3.0, color=MUTED
        ).set_stroke(MUTED, 2)
        balls = VGroup()
        for j in range(12):
            col = GREEN if j < 8 else GRAY
            balls.add(Dot(radius=0.16, color=col).set_fill(col, 0.9))
        balls.arrange_in_grid(rows=4, cols=3, buff=0.18)
        balls.move_to(urn)
        urn_label = Text("8 green · 4 gray", font_size=CAPTION, color=MUTED)
        urn_group = VGroup(urn, balls, urn_label)
        urn_label.next_to(urn, DOWN, buff=0.3)
        fit_to_frame(urn_group)
        urn_group.move_to(LEFT * 3.6 + DOWN * 0.15)

        # Block 3 (urn).
        with self.voiceover(
            text="It is tailor-made for drawing without replacement. An urn "
                 "holds eight green balls and four gray ones — twelve in all. We "
                 "draw three, and ask: what is the probability all three are "
                 "green?"
        ):
            self.play(FadeOut(rule_group))
            self.play(Create(urn))
            self.play(LaggedStartMap(FadeIn, balls, lag_ratio=0.1), run_time=1.6)
            self.play(FadeIn(urn_label, shift=UP * 0.1))

        # --- The draws (right column): the tree and the product. -------------
        tree = MathTex(
            r"\frac{8}{12}", r"\to", r"\frac{7}{11}", r"\to", r"\frac{6}{10}",
            font_size=BODY, color=INK,
        )
        result = MathTex(
            r"\Pr(ggg) = \frac{8}{12}\cdot\frac{7}{11}\cdot\frac{6}{10} "
            r"= \frac{14}{55}",
            font_size=SMALL, color=ACCENT,
        )
        draws = VGroup(tree, result).arrange(DOWN, buff=0.7)
        fit_to_frame(draws)
        draws.move_to(RIGHT * 3.3 + DOWN * 0.1)
        result_box = SurroundingRectangle(
            result, color=ACCENT, buff=0.22, corner_radius=0.12
        ).set_stroke(ACCENT, 2)

        # Block 4 (draws): reveal each fraction as a green ball leaves the urn.
        exit_base = urn.get_right() + RIGHT * 0.8
        exit_pts = [exit_base + UP * 0.7, exit_base, exit_base + DOWN * 0.7]
        drawn_cap = Text("drawn", font_size=CAPTION, color=MUTED)
        drawn_cap.move_to(exit_pts[0] + UP * 0.55)

        # One sub-block per draw, with the ball drifting out over the whole
        # sentence (tracker.duration) so the motion tracks the narration.
        with self.voiceover(
            text="The first draw is green with probability eight over twelve."
        ) as tracker:
            self.play(FadeIn(drawn_cap, shift=UP * 0.1), run_time=0.5)
            self.play(Write(tree[0]), run_time=0.6)
            self.play(balls[0].animate.move_to(exit_pts[0]),
                      run_time=max(0.8, tracker.duration - 1.1))

        with self.voiceover(
            text="Given that, eleven balls remain, seven green, so the second is "
                 "green with probability seven over eleven."
        ) as tracker:
            self.play(Write(VGroup(tree[1], tree[2])), run_time=0.6)
            self.play(balls[1].animate.move_to(exit_pts[1]),
                      run_time=max(0.8, tracker.duration - 0.6))

        with self.voiceover(
            text="With two greens gone, six of the ten left are green — six over "
                 "ten."
        ) as tracker:
            self.play(Write(VGroup(tree[3], tree[4])), run_time=0.6)
            self.play(balls[2].animate.move_to(exit_pts[2]),
                      run_time=max(0.8, tracker.duration - 0.6))

        with self.voiceover(
            text="Multiply along the chain: eight-twelfths times seven-elevenths "
                 "times six-tenths is fourteen over fifty-five."
        ) as tracker:
            self.play(Write(result), run_time=1.0)
            self.play(Create(result_box), run_time=0.9)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- Outro: key idea + bridge to the total probability theorem. ------
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            Text("Conditioning on B re-normalizes the law to B:",
                 font_size=BODY, color=INK),
            MathTex(r"\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)}",
                    font_size=BODY, color=INK),
            Text("Chaining these conditionals gives the probability of a "
                 "whole sequence of events.",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)

        # Block 5 (outro).
        with self.voiceover(
            text="Conditioning re-normalizes the law to what you know, and "
                 "chaining those conditionals gives the probability of a whole "
                 "sequence of events. Next, we turn the idea around: instead of "
                 "building intersections, we assemble the total probability of "
                 "an event from a partition of cases."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.0)
            self.play(Write(outro[2]), run_time=1.0)
            self.play(FadeIn(outro[3], shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(outro))
