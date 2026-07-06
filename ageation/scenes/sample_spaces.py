# derived_from: content/07-sample-spaces-script.md
# derived_from_sha256: eeac9dcf9f72d560d6646288aa6769202e2747d77af56686bd1ef7d427a4c4d2
"""Chapter 3, Video 1 -- Sample Spaces and Events (narrated with manim-voiceover).

Source notes : ../chapters/probability_models.tex  (chapter intro + 3.1 Sample
               Spaces and Events)
Script        : content/07-sample-spaces-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, timed by ``tracker.duration`` -- the
same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/sample_spaces.py ChapterOverview
Final: switch make_speech_service() to OpenAIService (needs OPENAI_API_KEY).
"""

import os
import random
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
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


# --- Shared visual helpers (mirroring the house style) -----------------------

def ball(label, color, radius=0.32, font_size=22):
    """A colored disk with a dark centered label (see Chapter 1 contrast note)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


def omega_box(width=8.5, height=4.6):
    """The sample-space frame: a rounded rectangle labelled Omega (Chapter 1)."""
    box = RoundedRectangle(
        corner_radius=0.25, width=width, height=height, color=MUTED
    ).set_stroke(MUTED, width=2)
    box.set_stroke(opacity=0.9)
    lab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    lab.next_to(box.get_corner(UL), DR, buff=0.22)
    return VGroup(box, lab)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of Chapter 2 + the outline of this video."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Sample Spaces and Events",
            "Build the first half of a probabilistic model: outcomes and events.",
            kicker="Chapter 3  ·  Probability Models",
        )
        fit_to_frame(intro)
        tag = progress_tag(1, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="We spent Chapter two counting outcomes; now we build the "
                 "framework that gives those counts meaning."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(tag), run_time=0.4)

        with self.voiceover(
            text="A probabilistic model has two parts — a sample space and a "
                 "probability law — and this video builds the first."
        ):
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Experiments, outcomes, and the sample space", font_size=BODY),
            Text("2.  Events as subsets of the sample space", font_size=BODY),
            Text("3.  One experiment, many sample spaces", font_size=BODY),
            Text("4.  The rules a sample space must obey", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this video we meet the experiment, its outcomes, and the sample "
            "space;",
            "we define an event;",
            "we see why one experiment can have many sample spaces;",
            "and we lay down the two rules a sample space must obey.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExperimentAndSampleSpace(VoiceoverScene):
    """Beat: the Omega box of outcome-balls, the outcome, the event loop, the die."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Experiments and Sample Spaces")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        frame = omega_box(width=8.6, height=4.8).move_to(DOWN * 0.4)
        C = frame[0].get_center()

        # Six colored outcome-balls (the die faces), positioned so a clean loop
        # can encircle the primes {2,3,5} on the right while 1,4,6 stay clear.
        specs = [
            ("1", RED, [-2.6, 1.0, 0]),
            ("4", GRAY_B, [-2.5, -1.0, 0]),
            ("6", PINK, [-0.5, 1.2, 0]),
            ("2", BLUE, [1.8, 0.7, 0]),
            ("3", GREEN, [1.7, -0.3, 0]),
            ("5", TEAL, [2.5, -1.1, 0]),
        ]
        balls = {}
        ball_grp = VGroup()
        for lab, col, pos in specs:
            b = ball(lab, col)
            b.move_to(C + np.array(pos))
            balls[lab] = b
            ball_grp.add(b)

        with self.voiceover(
            text="In probability, an experiment is a random occurrence that "
                 "produces one of several outcomes."
        ):
            self.play(LaggedStartMap(FadeIn, ball_grp, lag_ratio=0.15),
                      run_time=1.6)

        with self.voiceover(
            text="Collect every possible outcome into a single set, and you have "
                 "the sample space, written capital Omega — the same universal "
                 "set from Chapter one, now wearing its probability name. Picture "
                 "it as a box holding one ball for each possible outcome."
        ):
            self.play(Create(frame[0]), Write(frame[1]))

        # Tag a single realized outcome (ball 1).
        out_lab = Text("outcome", font_size=CAPTION, color=MUTED)
        out_lab.move_to(C + np.array([-2.6, 2.0, 0]))
        out_arrow = Arrow(out_lab.get_bottom(), balls["1"].get_top(),
                          color=MUTED, buff=0.12, stroke_width=3)
        with self.voiceover(
            text="When you actually run the experiment, exactly one of these "
                 "balls is realized: that is the outcome."
        ):
            self.play(FadeIn(out_lab), GrowArrow(out_arrow))
            self.play(Indicate(balls["1"], color=ACCENT, scale_factor=1.3))

        # An event: a dashed loop around the primes {2,3,5}.
        primes = VGroup(balls["2"], balls["3"], balls["5"])
        loop = Ellipse(width=primes.width + 0.9, height=primes.height + 0.9)
        loop.move_to(primes.get_center())
        loop = DashedVMobject(loop, num_dashes=44).set_stroke(ACCENT, 3)
        ev_lab = Text("event", font_size=CAPTION, color=ACCENT)
        ev_lab.next_to(loop, UP, buff=0.18)
        with self.voiceover(
            text="An event is an admissible subset of the sample space — any "
                 "collection of outcomes we might want to ask a question about. "
                 "Here it is a dashed loop drawn around some of the balls."
        ):
            self.play(Create(loop), FadeIn(ev_lab))

        # Make it concrete: the die.
        die_eq = MathTex(r"\Omega = \{\, 1, 2, 3, 4, 5, 6 \,\}",
                         font_size=SMALL, color=INK)
        ev_eq = MathTex(r"E = \{\, 2, 3, 5 \,\}", font_size=SMALL, color=ACCENT)
        eqs = VGroup(die_eq, ev_eq).arrange(RIGHT, buff=0.9)
        eqs.next_to(frame[0], DOWN, buff=0.35)
        fit_to_frame(eqs)
        with self.voiceover(
            text="Make it concrete with the rolling of a die. The sample space is "
                 "the six faces, Omega equals one through six."
        ):
            self.play(Write(die_eq))

        # Separate block so the prime balls light up exactly as the narration
        # reaches "The set of primes...".
        with self.voiceover(
            text="The set of primes less than or equal to six — two, three, and "
                 "five — is one event among many."
        ):
            self.play(Write(ev_eq))
            self.play(LaggedStart(*[Indicate(b, color=ACCENT) for b in primes],
                                  lag_ratio=0.3))

        with self.voiceover(
            text="And the number you actually read off the die is the outcome. "
                 "Sample space, event, outcome: the whole vocabulary, on one "
                 "picture."
        ):
            self.play(Indicate(balls["1"], color=ACCENT, scale_factor=1.2))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChoosingASampleSpace(VoiceoverScene):
    """Beat: the same coin experiment under two different sample spaces."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("One Experiment, Many Sample Spaces")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        header = Text("n tosses of a coin", font_size=BODY, color=MUTED)
        header.next_to(title, DOWN, buff=0.6)
        with self.voiceover(
            text="There is essentially no restriction on what counts as an "
                 "experiment, and — this is the subtle part — the same experiment "
                 "can have more than one sample space. Take n tosses of a coin."
        ):
            self.play(FadeIn(header, shift=DOWN * 0.2))

        # Left panel: count the heads -> {0, 1, ..., n}.
        left_cap = Text("count the heads", font_size=SMALL, color=INK)
        omega1 = MathTex(r"\Omega_1 = \{\, 0, 1, 2, \ldots, n \,\}",
                         font_size=SMALL, color=INK)
        count1 = MathTex(r"n + 1 \ \text{outcomes}", font_size=SMALL, color=ACCENT)
        left = VGroup(left_cap, omega1, count1).arrange(DOWN, buff=0.4)
        left.move_to([-3.4, -0.9, 0])

        with self.voiceover(
            text="If all you care about is how many heads come up, the natural "
                 "sample space is just the counts: zero, one, two, all the way to "
                 "n. That is only n plus one outcomes."
        ):
            self.play(FadeIn(left_cap))
            self.play(Write(omega1))
            self.play(FadeIn(count1, shift=UP * 0.15))

        # Right panel: full history -> 2^n sequences.
        right_cap = Text("record the full history", font_size=SMALL, color=INK)
        seqs = VGroup(
            Text("H H H", font_size=SMALL, color=INK),
            Text("H H T", font_size=SMALL, color=INK),
            Text("H T H", font_size=SMALL, color=INK),
            MathTex(r"\vdots", font_size=SMALL, color=INK),
            Text("T T T", font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.18)
        seq_brace = Brace(seqs, RIGHT, color=MUTED)
        seq_lab = seq_brace.get_tex(r"2^n")
        seq_lab.set_color(ACCENT)
        seq_block = VGroup(seqs, seq_brace, seq_lab)
        right = VGroup(right_cap, seq_block).arrange(DOWN, buff=0.35)
        right.move_to([3.4, -0.9, 0])

        divider = DashedLine(
            header.get_bottom() + DOWN * 0.2 + LEFT * 0.001,
            [0, -2.85, 0], color=MUTED, stroke_width=2,
        )
        with self.voiceover(
            text="But if you want the complete history — which toss was heads and "
                 "which was tails, in order — then each outcome is a full "
                 "sequence, and there are two to the n of them. Same coins, same "
                 "tosses, but a far larger sample space."
        ):
            self.play(Create(divider))
            self.play(FadeIn(right_cap))
            self.play(LaggedStartMap(FadeIn, seqs, lag_ratio=0.2), run_time=1.4)
            self.play(GrowFromCenter(seq_brace), Write(seq_lab))

        takeaway = Text(
            "The choice depends on what you want to analyze.",
            font_size=CAPTION, color=ACCENT,
        )
        takeaway.to_edge(DOWN, buff=0.5)
        fit_to_frame(takeaway)
        with self.voiceover(
            text="Neither is more correct than the other. The choice of sample "
                 "space depends on the property you wish to analyze: rich enough "
                 "to distinguish every outcome you care about, but no more "
                 "detailed than the question demands."
        ):
            self.play(FadeIn(takeaway, shift=UP * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])


class RulesForASampleSpace(VoiceoverScene):
    """Beat: the two rules, the non-admissible vs admissible contrast, outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Rules a Sample Space Must Obey")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        rule1 = VGroup(
            Text("1.  Distinct and mutually exclusive", font_size=BODY, color=INK),
            Text("the outcome is always unique", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rule2 = VGroup(
            Text("2.  Collectively exhaustive", font_size=BODY, color=INK),
            Text("every outcome is accounted for", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rules = VGroup(rule1, rule2).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        rules.move_to(DOWN * 0.3)
        fit_to_frame(rules)

        with self.voiceover(
            text="Some freedom, then — but not total freedom. A sample space must "
                 "obey two rules. First, its elements must be distinct and "
                 "mutually exclusive. No two outcomes can occur at once, so that "
                 "the outcome of the experiment is always unique."
        ):
            self.play(FadeIn(rule1, shift=RIGHT * 0.3))

        with self.voiceover(
            text="Second, the sample space must be collectively exhaustive: every "
                 "possible outcome has to be accounted for, with nothing left out."
        ):
            self.play(FadeIn(rule2, shift=RIGHT * 0.3))

        self.play(FadeOut(rules))

        # --- Not admissible: overlapping odd / even / prime ------------------
        bad_lab = Text("Not admissible", font_size=BODY, color=MAROON)
        bad_lab.next_to(title, DOWN, buff=0.4)

        # Larger circles + a roomy low prime ellipse, with the prime balls placed
        # well inside the ellipse (in each circle's lower lens) so nothing straddles
        # a boundary. 1 (odd-only) and 4,6 (even-only) sit high, clear of the ellipse.
        odd_c = Circle(radius=1.6, color=INK).set_stroke(INK, 2)
        odd_c.move_to([-2.1, 0, 0])
        even_c = Circle(radius=1.7, color=INK).set_stroke(INK, 2)
        even_c.move_to([2.1, 0, 0])
        prime_e = Ellipse(width=6.6, height=2.4, color=ACCENT).set_stroke(ACCENT, 2.5)
        prime_e.move_to([0, -1.2, 0])

        odd_t = Text("odd", font_size=CAPTION, color=INK).next_to(odd_c, UP, buff=0.12)
        even_t = Text("even", font_size=CAPTION, color=INK).next_to(even_c, UP, buff=0.12)
        prime_t = Text("prime", font_size=CAPTION, color=ACCENT).next_to(prime_e, DOWN, buff=0.12)

        # Outcome balls placed by region. 3,5 sit in odd AND prime; 2 in even AND prime.
        nums = {
            "1": ([-2.1, 0.7, 0], RED),     # odd only (high, outside the ellipse)
            "4": ([1.7, 0.7, 0], GRAY_B),   # even only
            "6": ([2.6, 0.7, 0], PINK),     # even only
            "3": ([-1.7, -0.9, 0], GREEN),  # odd & prime (lower lens, inside ellipse)
            "5": ([-2.5, -0.9, 0], TEAL),   # odd & prime
            "2": ([2.0, -0.9, 0], BLUE),    # even & prime
        }
        num_balls = {}
        for lab, (pos, col) in nums.items():
            b = ball(lab, col, radius=0.26, font_size=18).move_to(pos)
            num_balls[lab] = b

        bad_group = VGroup(odd_c, even_c, prime_e, odd_t, even_t, prime_t,
                           *num_balls.values())
        fit_to_frame(bad_group)

        with self.voiceover(
            text="Here is a tempting candidate for the die that breaks the first "
                 "rule: the odd numbers, the even numbers, and the primes."
        ):
            self.play(FadeIn(bad_lab, shift=DOWN * 0.2))
            self.play(Create(odd_c), Create(even_c), FadeIn(odd_t), FadeIn(even_t))
            self.play(Create(prime_e), FadeIn(prime_t))
            self.play(LaggedStartMap(FadeIn,
                                     VGroup(*num_balls.values()), lag_ratio=0.12))

        with self.voiceover(
            text="These overlap — three and five are both odd and prime, and two "
                 "is both prime and even — so a single roll can land in two "
                 "categories at once. The outcome is not unique, so this is not an "
                 "admissible sample space."
        ):
            self.play(LaggedStart(
                Indicate(num_balls["3"], color=ACCENT, scale_factor=1.4),
                Indicate(num_balls["5"], color=ACCENT, scale_factor=1.4),
                Indicate(num_balls["2"], color=ACCENT, scale_factor=1.4),
                lag_ratio=0.4,
            ))

        self.play(FadeOut(bad_group), FadeOut(bad_lab))

        # --- Admissible: two disjoint regions tiling {1,...,6} ---------------
        good_lab = Text("Admissible", font_size=BODY, color=GREEN)
        good_lab.next_to(title, DOWN, buff=0.4)

        odd_box = RoundedRectangle(corner_radius=0.2, width=3.4, height=3.0,
                                   color=INK).set_stroke(INK, 2).move_to([-2.4, -0.6, 0])
        even_box = RoundedRectangle(corner_radius=0.2, width=3.4, height=3.0,
                                    color=INK).set_stroke(INK, 2).move_to([2.4, -0.6, 0])
        odd_h = Text("odd", font_size=CAPTION, color=INK).next_to(odd_box, UP, buff=0.12)
        even_h = Text("even", font_size=CAPTION, color=INK).next_to(even_box, UP, buff=0.12)

        # Scatter the balls to random, non-overlapping spots inside each box
        # (the boxes themselves are unchanged). Seeded so renders are reproducible.
        def scatter(box, items, seed, radius=0.28, font_size=20):
            rng = random.Random(seed)
            cx, cy, _ = box.get_center()
            hw = box.width / 2 - radius - 0.4
            hh = box.height / 2 - radius - 0.4
            placed, grp = [], VGroup()
            for lab, col in items:
                for _ in range(400):
                    x, y = cx + rng.uniform(-hw, hw), cy + rng.uniform(-hh, hh)
                    if all((x - px) ** 2 + (y - py) ** 2 >= 0.70 ** 2
                           for px, py in placed):
                        break
                placed.append((x, y))
                grp.add(ball(lab, col, radius=radius, font_size=font_size)
                        .move_to([x, y, 0]))
            return grp

        odd_balls = scatter(odd_box,
                            [("1", RED), ("3", GREEN), ("5", TEAL)], seed=5)
        even_balls = scatter(even_box,
                             [("2", BLUE), ("4", GRAY_B), ("6", PINK)], seed=11)

        good_group = VGroup(odd_box, even_box, odd_h, even_h, odd_balls, even_balls)
        fit_to_frame(good_group)

        with self.voiceover(
            text="Fix it by dropping the primes. The odd numbers and the even "
                 "numbers are disjoint — no integer is both — and together they "
                 "cover one through six completely."
        ):
            self.play(FadeIn(good_lab, shift=DOWN * 0.2))
            self.play(Create(odd_box), Create(even_box),
                      FadeIn(odd_h), FadeIn(even_h))
            self.play(LaggedStartMap(FadeIn, VGroup(*odd_balls, *even_balls),
                                     lag_ratio=0.12))

        caption = VGroup(
            Text("distinct, mutually exclusive, and collectively exhaustive",
                 font_size=CAPTION, color=ACCENT),
            Text("a valid sample space.", font_size=CAPTION, color=ACCENT),
        ).arrange(DOWN, buff=0.15)
        caption.to_edge(DOWN, buff=0.5)
        fit_to_frame(caption)
        with self.voiceover(
            text="Distinct, mutually exclusive, and exhaustive: a partition of the "
                 "outcomes, and a perfectly valid sample space."
        ):
            self.play(FadeIn(caption, shift=UP * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- Centred two-line key idea + bridge (inline, not outro_bridge) ---
        key_idea = VGroup(
            Text("A model starts with a sample space of all outcomes;",
                 font_size=BODY, color=INK),
            Text("events are its admissible subsets.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  The Axioms of Probability",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So that is half of a probabilistic model: a sample space of all "
                 "the outcomes, with events as its admissible subsets. Next, we "
                 "give those events numbers — the rules a probability law must "
                 "obey, the axioms of probability."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
