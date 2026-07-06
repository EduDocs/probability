# derived_from: content/08-probability-laws-script.md
# derived_from_sha256: 6bca4b0572bc69afc330d0fb811ae3b57c770d2199825cc2d85907502915ecdd
"""Chapter 3, Video 2 -- Probability Laws (narrated with manim-voiceover).

Source notes : ../chapters/probability_models.tex  (section 3.2 Probability
               Laws: the three axioms, their consequences, the union bound)
Script        : content/08-probability-laws-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, timed by ``tracker.duration`` -- the
same pattern as the earlier videos in the series.

Draft render (free Google TTS):
    uv run manim -pql scenes/probability_laws.py ChapterOverview
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

    Draft  -> GTTSService (free, no API key, cached by text hash) -- ACTIVE.
    Final  -> OpenAIService(voice="nova", model="tts-1"): needs OPENAI_API_KEY;
              `nova` matches the rest of the series. Swap the lines below.
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


def omega_box(width=12.0, height=6.0):
    """The sample-space frame: a rounded rectangle labelled Omega."""
    box = RoundedRectangle(
        corner_radius=0.25, width=width, height=height, color=MUTED
    ).set_stroke(MUTED, width=2)
    box.set_stroke(opacity=0.9)
    lab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    lab.next_to(box.get_corner(UL), DR, buff=0.22)
    return VGroup(box, lab)


def shaded(region_vmobj, color, opacity=0.55):
    """Style a boolean-op region as a translucent fill with no stroke."""
    region_vmobj.set_fill(color, opacity=opacity)
    region_vmobj.set_stroke(width=0)
    return region_vmobj


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of Video 1, title, and the four-item outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Probability Laws",
            "Build probability from three axioms, and derive the rules for combining events.",
            kicker="Chapter 3  ·  Probability Models",
        )
        fit_to_frame(intro)
        tag = progress_tag(2, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="In the last video we built sample spaces and events — the stage "
                 "every experiment plays out on. Now we put numbers on those events."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        with self.voiceover(
            text="A probability law is the rule that assigns each event its "
                 "likelihood, and remarkably, it rests on just three axioms."
        ):
            self.play(Indicate(intro[1], color=ACCENT, scale_factor=1.05))

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  The three axioms of probability", font_size=BODY),
            Text("2.  Consequences: complement and monotonicity", font_size=BODY),
            Text("3.  The union of two events", font_size=BODY),
            Text("4.  The union bound", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this video we meet the three axioms themselves;",
            "the consequences they force, like the complement rule and monotonicity;",
            "the formula for the union of two events;",
            "and the union bound, a workhorse inequality.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="By the end, every rule you will ever use for combining "
                 "probabilities will trace back to these three axioms."
        ):
            self.play(Indicate(items, color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ThreeAxioms(VoiceoverScene):
    """Beat: three-axioms -- Pr assigns mass; nonnegativity, normalization, additivity."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Three Axioms")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Sample-space frame with an event A shaded as "mass", on the left.
        frame = omega_box(width=5.4, height=4.2).shift(LEFT * 3.5 + DOWN * 0.5)
        eventA = Ellipse(width=2.5, height=1.7, color=INK).set_stroke(INK, 2)
        eventA.set_fill(BAR, opacity=0.55)
        eventA.move_to(frame[0].get_center() + LEFT * 0.3 + DOWN * 0.1)
        aLab = MathTex(r"A", font_size=BODY, color=INK).move_to(eventA.get_center())

        # The axiom list, anchored on the right half of the frame.
        ax1 = VGroup(
            Text("1.  Nonnegativity", font_size=SMALL, color=INK),
            MathTex(r"\Pr(A) \geq 0", font_size=SMALL, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ax2 = VGroup(
            Text("2.  Normalization", font_size=SMALL, color=INK),
            MathTex(r"\Pr(\Omega) = 1", font_size=SMALL, color=ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ax3 = VGroup(
            Text("3.  Countable Additivity", font_size=SMALL, color=INK),
            MathTex(r"\Pr(A \cup B) = \Pr(A) + \Pr(B)",
                    font_size=SMALL, color=ACCENT),
            Text("(A, B disjoint)", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        axioms = VGroup(ax1, ax2, ax3).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        axioms.move_to(RIGHT * 3.3 + DOWN * 0.4)
        fit_to_frame(axioms)

        with self.voiceover(
            text="Start with the central object. A probability law assigns to "
                 "every event A a single number, written P-r of A, that measures "
                 "how likely A is."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(eventA), Write(aLab))

        with self.voiceover(
            text="Picture the sample space Omega as a region, and an event A as a "
                 "patch inside it; the probability of A is the amount of mass "
                 "sitting on that patch. Two events that look very different can "
                 "carry exactly the same probability — all the law records is how "
                 "much weight we attach to each. In other branches of mathematics "
                 "the very same object is called a probability measure, a name that "
                 "emphasizes its status as a set function; it is a name we will "
                 "follow up when we reach measure theory."
        ):
            self.play(Indicate(eventA, color=ACCENT, scale_factor=1.08))

        with self.voiceover(
            text="The first axiom is nonnegativity: every event gets a probability "
                 "that is at least zero. Weights are never negative."
        ):
            self.play(FadeIn(ax1, shift=RIGHT * 0.3))

        with self.voiceover(
            text="The second is normalization: the whole sample space carries "
                 "probability exactly one. Something in Omega is certain to happen, "
                 "and certainty is one."
        ):
            self.play(FadeIn(ax2, shift=RIGHT * 0.3))
            self.play(Indicate(frame[0], color=ACCENT, scale_factor=1.02))

        with self.voiceover(
            text="The third is additivity. If two events A and B are disjoint — "
                 "they share no outcomes — then the probability of their union is "
                 "just the sum of their probabilities. Non-overlapping masses "
                 "simply add. That third axiom is the engine of the whole theory, "
                 "so let us spend some time with it."
        ):
            self.play(FadeIn(ax3, shift=RIGHT * 0.3))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Additivity(VoiceoverScene):
    """Beat: additivity -- finite disjoint additivity, then countable additivity."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Countable Additivity")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- Finite disjoint additivity: two separated blobs inside Omega. ---
        frame = omega_box(width=9.5, height=3.6).move_to(UP * 0.3)
        blobA = Ellipse(width=2.4, height=1.7, color=INK).set_stroke(INK, 2)
        blobA.set_fill(BAR, opacity=0.6).move_to(frame[0].get_center() + LEFT * 2.4)
        blobB = Ellipse(width=2.4, height=1.7, color=INK).set_stroke(INK, 2)
        blobB.set_fill(GREEN, opacity=0.6).move_to(frame[0].get_center() + RIGHT * 2.4)
        labA = MathTex(r"A", font_size=BODY, color=INK).move_to(blobA.get_center())
        labB = MathTex(r"B", font_size=BODY, color=INK).move_to(blobB.get_center())

        with self.voiceover(
            text="Here are two disjoint events, A on the left and B on the right, "
                 "with no overlap between them."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(blobA), FadeIn(blobB), Write(labA), Write(labB))

        finite = MathTex(r"\Pr(A \cup B) = \Pr(A) + \Pr(B)",
                         font_size=BODY, color=ACCENT).to_edge(DOWN, buff=0.9)
        fit_to_frame(finite)
        with self.voiceover(
            text="Because they are disjoint, the probability of A-or-B is exactly "
                 "the probability of A plus the probability of B. Nothing is double "
                 "counted, because there is no shared region to count twice."
        ):
            self.play(Write(finite))

        self.play(FadeOut(frame), FadeOut(blobA), FadeOut(blobB),
                  FadeOut(labA), FadeOut(labB), FadeOut(finite))

        # --- Countable additivity: a unit bar split into shrinking pieces. ---
        W = 9.4
        fracs = [1 / 2, 1 / 4, 1 / 8, 1 / 16]
        cols = [BLUE, TEAL, GREEN, PURPLE]
        segs = VGroup()
        for f, c in zip(fracs, cols):
            seg = Rectangle(width=W * f, height=0.9,
                            fill_color=c, fill_opacity=0.6,
                            stroke_color=INK, stroke_width=1.5)
            segs.add(seg)
        segs.arrange(RIGHT, buff=0.0)
        dots = MathTex(r"\cdots", font_size=BODY, color=INK).next_to(segs, RIGHT, buff=0.2)
        bar = VGroup(segs, dots).move_to(UP * 0.4)
        fit_to_frame(bar)

        seg_labels = VGroup(*[
            MathTex(rf"A_{{{i + 1}}}", font_size=CAPTION, color=INK).next_to(seg, DOWN, buff=0.2)
            for i, seg in enumerate(segs)
        ])
        unit_brace = Brace(segs, UP)
        unit_lab = MathTex(
            r"A = \bigcup_{k=1}^{\infty} A_k \text{ where } A_k \text{ are disjoint}",
            font_size=SMALL, color=INK,
        ).next_to(unit_brace, UP, buff=0.12)
        fit_to_frame(unit_lab)

        with self.voiceover(
            text="But the axiom says more. Additivity holds not just for two "
                 "disjoint events, but for a whole infinite sequence of them. Take "
                 "disjoint events A-one, A-two, A-three, and so on, tiling the "
                 "sample space with no overlaps — a partition, exactly the "
                 "structure we met back in the Sets video. This is where "
                 "probability outgrows mere counting: the pieces need not be finite "
                 "in number, only pairwise disjoint."
        ):
            self.play(LaggedStartMap(FadeIn, segs, lag_ratio=0.25), run_time=1.8)
            self.play(LaggedStartMap(FadeIn, seg_labels, lag_ratio=0.25),
                      Write(dots))
            self.play(GrowFromCenter(unit_brace), Write(unit_lab))

        countable = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{\infty} A_k \right)"
            r" = \sum_{k=1}^{\infty} \Pr(A_k)",
            font_size=BODY, color=ACCENT,
        )
        # Sit halfway between the bar block above and the bottom of the frame.
        _mid_y = (seg_labels.get_bottom()[1] + (-config.frame_height / 2)) / 2
        countable.move_to([0, _mid_y, 0])
        fit_to_frame(countable)
        with self.voiceover(
            text="The probability of their union — the chance that some one of "
                 "them occurs — equals the infinite sum of the individual "
                 "probabilities. Picture the pieces as a half, then a quarter, then "
                 "an eighth, and on forever: the masses add up to the whole. "
                 "Finite additivity is just the special case where all but finitely "
                 "many pieces are empty; the countable version is strictly "
                 "stronger. This is countable additivity, and it is exactly what we "
                 "need to put probabilities on infinite sample spaces — like "
                 "tossing a coin until the very first heads, where there are "
                 "infinitely many possible outcomes."
        ):
            self.play(Write(countable))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Consequences(VoiceoverScene):
    """Beat: consequences -- complement rule, empty set, monotonicity, conjunction."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Consequences of the Axioms")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- Complement rule. ---
        frame = omega_box(width=5.6, height=4.0).shift(LEFT * 3.5 + DOWN * 0.4)
        circA = Circle(radius=1.3, color=INK).set_stroke(INK, 2)
        circA.set_fill(BAR, opacity=0.6).move_to(frame[0].get_center() + LEFT * 0.4)
        aLab = MathTex(r"A", font_size=BODY, color=INK).move_to(circA.get_center())

        with self.voiceover(
            text="The axioms immediately force a string of useful rules. Take any "
                 "event A and its complement A-c — everything in Omega outside A."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(circA), Write(aLab))

        comp = shaded(Difference(frame[0], circA), ACCENT, opacity=0.45)
        comp_rule = MathTex(r"\Pr(A^{\mathrm{c}}) = 1 - \Pr(A)",
                            font_size=BODY, color=ACCENT).move_to(RIGHT * 3.3 + UP * 0.9)
        fit_to_frame(comp_rule)
        with self.voiceover(
            text="They are disjoint, and together they fill the whole sample "
                 "space, so by normalization and additivity their probabilities "
                 "add to one. Rearranging, the probability of the complement is one "
                 "minus the probability of A. It is often far easier to compute the "
                 "probability of what you do not want, and subtract — a trick we "
                 "will reach for again and again."
        ):
            self.play(FadeIn(comp))
            self.play(Write(comp_rule))

        empty = MathTex(r"\Pr(\varnothing) = 0",
                        font_size=BODY, color=INK).next_to(comp_rule, DOWN, buff=0.7)
        fit_to_frame(empty)
        with self.voiceover(
            text="As a special case, let A be all of Omega: its complement is the "
                 "empty set, so the impossible event carries probability zero."
        ):
            self.play(Write(empty))

        self.play(FadeOut(frame), FadeOut(circA), FadeOut(aLab), FadeOut(comp),
                  FadeOut(comp_rule), FadeOut(empty))

        # --- Monotonicity: A nested inside B; ring B - A. ---
        frame2 = omega_box(width=5.6, height=4.0).shift(LEFT * 3.5 + DOWN * 0.4)
        cB = Circle(radius=1.6, color=INK).set_stroke(INK, 2)
        cB.move_to(frame2[0].get_center())
        cA = Circle(radius=0.8, color=INK).set_stroke(INK, 2)
        cA.move_to(cB.get_center() + LEFT * 0.4 + UP * 0.1)
        ring = shaded(Difference(cB, cA), GREEN, opacity=0.5)
        innerA = shaded(cA.copy(), BAR, opacity=0.6)
        lA = MathTex(r"A", font_size=SMALL, color=INK).move_to(cA.get_center())
        lB = MathTex(r"B", font_size=SMALL, color=INK).next_to(cB.get_top(), DOWN, buff=0.18)
        lBmA = MathTex(r"B - A", font_size=CAPTION, color=MUTED).move_to(
            cB.get_center() + RIGHT * 0.85 + DOWN * 0.05)

        mono = VGroup(
            MathTex(r"A \subset B", font_size=BODY, color=INK),
            MathTex(r"B = A \cup (B - A)", font_size=SMALL, color=MUTED),
            MathTex(r"\Rightarrow\ \Pr(A) \leq \Pr(B)", font_size=BODY, color=ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.3 + DOWN * 0.3)
        fit_to_frame(mono)

        with self.voiceover(
            text="Next, monotonicity. Suppose A sits inside B. Then we split B into "
                 "A together with the part of B outside A — two disjoint pieces."
        ):
            self.play(Create(frame2[0]), Write(frame2[1]))
            self.play(Create(cB), FadeIn(innerA), Create(cA),
                      Write(lA), Write(lB))
            self.play(FadeIn(ring), Write(lBmA))
            self.play(FadeIn(mono[0], shift=RIGHT * 0.3), FadeIn(mono[1], shift=RIGHT * 0.3))

        with self.voiceover(
            text="Additivity says P-r of B equals P-r of A plus the probability of "
                 "that leftover, and since probabilities are never negative, P-r of "
                 "A is at most P-r of B. A bigger event is at least as likely."
        ):
            self.play(FadeIn(mono[2], shift=RIGHT * 0.3))

        self.play(FadeOut(frame2), FadeOut(cB), FadeOut(cA), FadeOut(ring),
                  FadeOut(innerA), FadeOut(lA), FadeOut(lB), FadeOut(lBmA),
                  FadeOut(mono))

        # --- Conjunction fallacy aside. ---
        conj = MathTex(r"\Pr(A \cap B) \leq \Pr(A)",
                       font_size=TITLE, color=ACCENT).move_to(UP * 1.9)
        fallacy = VGroup(
            Text("Yet, told that someone is politically active,",
                 font_size=SMALL, color=INK),
            Text("the probability of \"a bank teller in a social movement\"",
                 font_size=SMALL, color=INK),
            Text("is often ranked above \"a bank teller\" alone.",
                 font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.3).next_to(conj, DOWN, buff=0.7)
        fit_to_frame(fallacy)
        fallacy_name = Text("the conjunction fallacy",
                            font_size=BODY, color=ACCENT).next_to(
                                fallacy, DOWN, buff=0.9)
        fit_to_frame(fallacy_name)

        with self.voiceover(
            text="This has a consequence human intuition routinely violates. "
                 "Because A-and-B sits inside A, the probability of a conjunction "
                 "can never exceed the probability of event A alone — adding detail to a "
                 "description can only lower its probability, never raise it."
        ):
            self.play(Write(conj))

        with self.voiceover(
            text="Yet people reliably get this backwards. In a classic experiment, "
                 "respondents were told that someone is politically active and "
                 "outspoken, then asked which is more likely: that the person is a "
                 "bank teller who is also active in a social movement, or simply a "
                 "bank teller. Most people chose the former — even though it is a special "
                 "case of the latter, and so can only be less probable. The richer, "
                 "more representative story simply feels more likely."
        ):
            self.play(FadeIn(fallacy, shift=UP * 0.2))

        with self.voiceover(
            text="Ranking the more specific scenario above one of its own "
                 "constituents is the conjunction fallacy."
        ):
            self.play(FadeIn(fallacy_name, shift=UP * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])


class UnionFormula(VoiceoverScene):
    """Beat: union-formula -- Pr(A u B) = Pr(A) + Pr(B) - Pr(A n B); inclusion-exclusion."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Union of Two Events")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        frame = omega_box(width=9.0, height=4.0).move_to(DOWN * 0.4)
        cA = Circle(radius=1.4, color=INK).set_stroke(INK, 2)
        cB = Circle(radius=1.4, color=INK).set_stroke(INK, 2)
        cA.move_to(frame[0].get_center() + LEFT * 0.8)
        cB.move_to(frame[0].get_center() + RIGHT * 0.8)
        fillA = shaded(cA.copy(), BAR, opacity=0.5)
        fillB = shaded(cB.copy(), GREEN, opacity=0.5)
        lA = MathTex(r"A", font_size=BODY, color=INK).next_to(cA, UL, buff=-0.1)
        lB = MathTex(r"B", font_size=BODY, color=INK).next_to(cB, UR, buff=-0.1)

        with self.voiceover(
            text="What if the two events do overlap? Here are A and B with a shared "
                 "lens in the middle."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(fillA), FadeIn(fillB),
                      Create(cA), Create(cB), Write(lA), Write(lB))

        lens = shaded(Intersection(cA, cB), ACCENT, opacity=0.85)
        with self.voiceover(
            text="If we simply add P-r of A and P-r of B, we count that "
                 "overlapping lens twice — once for each circle."
        ):
            self.play(FadeIn(lens))
            self.play(Indicate(lens, color=ACCENT, scale_factor=1.15))

        formula = MathTex(
            r"\Pr(A \cup B)", r"=", r"\Pr(A) + \Pr(B)", r"-", r"\Pr(A \cap B)",
            font_size=BODY,
        ).to_edge(DOWN, buff=0.8)
        formula[0].set_color(INK)
        formula[2].set_color(INK)
        formula[4].set_color(ACCENT)
        fit_to_frame(formula)
        with self.voiceover(
            text="So we subtract it back out once. In general, the probability of "
                 "A-union-B equals P-r of A, plus P-r of B, minus the probability "
                 "of their intersection. Add the parts, then correct for the double "
                 "counting "
                 "— and notice that when A and B are disjoint the intersection is "
                 "empty, and we recover plain additivity."
        ):
            self.play(Write(formula))

        incl = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{n} A_k \right)"
            r" = \sum_{k} \Pr(A_k) - \sum_{i<j} \Pr(A_i \cap A_j) + \cdots",
            font_size=SMALL, color=MUTED,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(incl)
        with self.voiceover(
            text="The same bookkeeping extends to any number of events, "
                 "alternately adding and subtracting the overlaps of overlaps; that "
                 "general pattern is the inclusion–exclusion principle. For three "
                 "events, you add the three single probabilities, subtract the "
                 "three pairwise overlaps, then add back the one triple overlap. "
                 "The signs alternate all the way up. We state it and move on."
        ):
            self.play(FadeIn(incl, shift=DOWN * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])


class UnionBound(VoiceoverScene):
    """Beat: union-bound -- Boole's inequality, the urn example, then outro/bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Union Bound")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        bound = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{n} A_k \right)"
            r" \leq \sum_{k=1}^{n} \Pr(A_k)",
            font_size=TITLE, color=ACCENT,
        ).move_to(UP * 1.4)
        fit_to_frame(bound)
        boole = Text("Boole's inequality  ·  proved by induction",
                     font_size=CAPTION, color=MUTED).next_to(bound, DOWN, buff=0.5)
        with self.voiceover(
            text="Sometimes the intersections are hopelessly hard to compute. Then "
                 "we settle for a bound. Drop the subtracted overlap terms from the "
                 "union formula and the right side can only grow, so the "
                 "probability of a union of events is at most the sum of their "
                 "probabilities."
        ):
            self.play(Write(bound))

        with self.voiceover(
            text="Applied repeatedly — a quick induction — this gives the union "
                 "bound, also called Boole's inequality, for any number of events."
        ):
            self.play(FadeIn(boole))

        self.play(FadeOut(bound), FadeOut(boole))

        # --- Urn example: 990 blue + 10 red, 5 draws without replacement. ---
        # A tall, evenly-padded urn filling the left column: its top sits just
        # below the title (caption between), its bottom a small gap above the
        # frame edge, with the ball-to-wall padding equal on all four sides.
        BALL_R, GRID_B, PAD = 0.13, 0.17, 0.36
        rows, colsn = 11, 7
        red_cells = {(1, 4), (4, 1), (6, 5), (9, 2), (10, 6)}
        dots = VGroup()
        for r in range(rows):
            for c in range(colsn):
                col = MAROON if (r, c) in red_cells else BLUE
                d = Dot(radius=BALL_R, color=col).set_fill(col, opacity=0.95)
                d.set_stroke(INK, width=1)
                dots.add(d)
        dots.arrange_in_grid(rows=rows, cols=colsn, buff=GRID_B)

        # Box dimensions follow the grid + uniform padding, so the gap is the
        # same on every side. Anchored low in the left column.
        urn_box = RoundedRectangle(
            corner_radius=0.22,
            width=dots.width + 2 * PAD, height=dots.height + 2 * PAD,
            color=MUTED,
        ).set_stroke(MUTED, 2)
        # Hold the top edge where the previous (12-row) box had it; dropping the
        # bottom row then raises the bottom edge by one row's height.
        _prev_box_h = 12 * 2 * BALL_R + 11 * GRID_B + 2 * PAD
        _urn_top = -config.frame_height / 2 + 0.5 + _prev_box_h
        urn_box.move_to([-3.9, _urn_top - urn_box.height / 2, 0])
        dots.move_to(urn_box.get_center())
        urn_cap = Text("990 blue  ·  10 red", font_size=CAPTION, color=MUTED)
        urn_cap.next_to(urn_box, UP, buff=0.3)

        # Right column: the draw-slots and the running computation, as one stack
        # centred vertically on the urn so both columns are balanced.
        slots = VGroup(*[Square(side_length=0.6, color=INK).set_stroke(INK, 2)
                         for _ in range(5)])
        slots.arrange(RIGHT, buff=0.2)
        slots_cap = Text("5 draws, no replacement", font_size=CAPTION, color=MUTED)
        slots_cap.next_to(slots, DOWN, buff=0.25)
        slot_grp = VGroup(slots, slots_cap)

        pk = MathTex(r"\Pr(B_k) = \tfrac{1}{100}", font_size=SMALL, color=INK)
        bound_calc = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{5} B_k \right)"
            r" \leq \sum_{k=1}^{5} \Pr(B_k)"
            r" = \tfrac{5}{100} = \tfrac{1}{20}",
            font_size=SMALL, color=ACCENT,
        )
        exact = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{5} B_k \right)"
            r" = 1 - \frac{\binom{990}{5}}{\binom{1000}{5}}"
            r" \approx 0.049",
            font_size=SMALL, color=INK,
        )
        right_col = VGroup(slot_grp, pk, bound_calc, exact).arrange(DOWN, buff=0.55)
        # Keep the right column at the centre it had with the previous box.
        right_col.move_to([2.55, -config.frame_height / 2 + 0.5 + _prev_box_h / 2, 0])
        fit_to_frame(right_col)

        draw_arrow = Arrow(
            np.array([urn_box.get_right()[0] + 0.7, slots.get_center()[1], 0]),
            slots.get_left(), color=ACCENT, buff=0.3, stroke_width=4)

        with self.voiceover(
            text="Here it earns its keep. An urn holds nine hundred ninety blue "
                 "balls and ten red ones. Five people each draw a ball, without "
                 "replacement, and we want the probability that at least one of "
                 "them draws red — the union of the five events person-k draws red."
        ):
            self.play(FadeIn(urn_box), LaggedStartMap(FadeIn, dots, lag_ratio=0.03),
                      FadeIn(urn_cap))
            self.play(GrowArrow(draw_arrow))
            self.play(Create(slots), FadeIn(slots_cap))

        with self.voiceover(
            text="Each person, on their own, has a one-in-a-hundred chance of red. "
                 "The union bound just adds those up: five times one-hundredth is "
                 "one-twentieth, or zero point zero five. That is an upper bound, "
                 "and it took almost no work."
        ):
            self.play(Write(pk))
            self.play(Write(bound_calc))
        with self.voiceover(
            text="The exact answer needs the probability that nobody draws red — a "
                 "ratio of binomial coefficients — which comes to about zero point "
                 "zero four nine. Remarkably close to the bound, and far harder to "
                 "reach. That is exactly when the union bound shines: when the "
                 "individual probabilities are simple but the joint event is not."
        ):
            self.play(Write(exact))
            self.play(Indicate(exact, color=ACCENT, scale_factor=1.05))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- A second application: each person draws TWO balls. ---
        second_head = Text("A second application", font_size=SECTION, color=INK).to_edge(UP)
        second_prose = VGroup(
            Text("Now each of the five people draws two balls.", font_size=SMALL, color=INK),
            Text("Each person's event: \"draws two reds.\"",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.3).next_to(second_head, DOWN, buff=0.7)
        fit_to_frame(second_prose)
        second = MathTex(
            r"\Pr\!\left( \bigcup_{k=1}^{5} C_k \right)"
            r" \leq \sum_{k=1}^{5} \Pr(C_k)"
            r" = \frac{5\binom{10}{2}}{\binom{1000}{2}} = \frac{1}{2220}",
            font_size=SMALL, color=ACCENT,
        ).next_to(second_prose, DOWN, buff=0.8)
        fit_to_frame(second)
        second_note = Text("Here the exact probability is much harder to compute.",
                           font_size=CAPTION, color=MUTED).next_to(second, DOWN, buff=0.7)
        fit_to_frame(second_note)

        with self.voiceover(
            text="As a second application, suppose each of the five people draws "
                 "two balls instead of one, and we ask for the probability that "
                 "someone ends up with two reds."
        ):
            self.play(FadeIn(second_head, shift=DOWN * 0.2))
            self.play(FadeIn(second_prose, shift=UP * 0.2))

        with self.voiceover(
            text="The same union bound applies with almost no extra work: five "
                 "times the chance that a single person draws two reds, which "
                 "totals one in two thousand two hundred and twenty. But computing "
                 "the exact value here is genuinely hard — and that is exactly the "
                 "situation the union bound was made for."
        ):
            self.play(Write(second))
            self.play(FadeIn(second_note, shift=UP * 0.2))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- Closing key idea + bridge (centred two-line, series house style). ---
        key_idea = VGroup(
            Text("Three axioms — nonnegativity, normalization, additivity —",
                 font_size=BODY, color=INK),
            Text("generate every rule for combining probabilities.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Three families of probability models",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So the whole of this video rests on three axioms — "
                 "nonnegativity, normalization, and additivity — and everything "
                 "else, the complement rule, monotonicity, the union formula, and "
                 "the union bound, follows from them. Next, we meet three families "
                 "of probability models: finite, countably infinite, and "
                 "uncountably infinite sample spaces."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
