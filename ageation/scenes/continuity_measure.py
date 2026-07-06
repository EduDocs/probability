# derived_from: content/10-continuity-measure-script.md
# derived_from_sha256: 14b36099c407b473d8cebe27cc750fa13fa8a7a870a7c3b5ff92ddc8644129f7
"""Chapter 3, Video 4 -- Continuity of Probability and a Measure-Theory View.

Source notes : ../chapters/probability_models.tex  (3.2.4 Continuity of
               Probability*, 3.2.5 Probability and Measure Theory*) -- the
               coda that closes the chapter.
Script        : content/10-continuity-measure-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, timed by ``tracker.duration`` -- the
same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/continuity_measure.py ChapterOverview
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
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


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
    """Beat: overview -- recap of the three families + the two topics."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Continuity & Measure Theory",
            "Two topics that complete the probabilistic model.",
            kicker="Chapter 3  ·  Probability Models",
        )
        fit_to_frame(intro)
        tag = progress_tag(4, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="In the last video we sorted sample spaces into three families — "
                 "finite, countably infinite, and uncountably infinite. This short "
                 "coda ties off two topics that complete the picture."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  The continuity of probability", font_size=BODY),
            Text("2.  A measure-theory view", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.next_to(intro, DOWN, buff=0.9)
        fit_to_frame(items)

        with self.voiceover(
            text="First, the continuity of probability: the fact that probability "
                 "behaves well under limits, when a sequence of events steadily "
                 "grows or steadily shrinks."
        ):
            self.play(FadeIn(items[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="And second, a glimpse of measure theory — the honest answer to a "
                 "question the continuous case forces on us: can we really assign a "
                 "probability to every subset of the sample space?"
        ):
            self.play(FadeIn(items[1], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ContinuityFromBelow(VoiceoverScene):
    """Beat: continuity-below -- increasing union, disjoint shells, the proof."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Continuity from Below")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Diagram vertically centred: the gap title->box roughly matches the gap
        # equation->frame-bottom. The union label sits just below the box.
        C = LEFT * 3.4 + DOWN * 0.15
        frame = omega_box(width=5.2, height=4.6).move_to(C)

        radii = [0.6, 1.2, 1.8]
        cols = [BLUE, TEAL, GREEN]
        circs = VGroup()
        for r, col in zip(radii, cols):
            c = Circle(radius=r, color=INK).set_stroke(INK, 2)
            c.set_fill(col, opacity=0.20).move_to(C)
            circs.add(c)
        cA = DashedVMobject(Circle(radius=2.00).move_to(C),
                            num_dashes=44).set_stroke(ACCENT, 2.5)
        # A_k labels centred in their annular bands (midpoints of the radii).
        labs = VGroup(
            MathTex(r"A_1", font_size=CAPTION, color=INK).move_to(C + UP * 0.30),
            MathTex(r"A_2", font_size=CAPTION, color=INK).move_to(C + UP * 0.90),
            MathTex(r"A_3", font_size=CAPTION, color=INK).move_to(C + UP * 1.50),
        )
        # The union/limit label sits BELOW the diagram, clear of the circles.
        aLab = MathTex(r"A = \bigcup_{k} A_k", font_size=CAPTION, color=ACCENT)
        aLab.next_to(frame[0], DOWN, buff=0.20)

        with self.voiceover(
            text="Start with a sequence of events that only grows. A-one sits "
                 "inside A-two, which sits inside A-three, and so on — an "
                 "increasing sequence — and we write A for their union, the limit "
                 "they fill out. Picture nested regions, each containing the last, "
                 "expanding toward A."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(LaggedStartMap(GrowFromCenter, circs, lag_ratio=0.3),
                      run_time=1.8)
            self.play(LaggedStartMap(FadeIn, labs, lag_ratio=0.2))
            self.play(Create(cA), Write(aLab))

        stmt = MathTex(r"\Pr(A) = \lim_{n \to \infty} \Pr(A_n)",
                       font_size=BODY, color=ACCENT).move_to(RIGHT * 3.3 + UP * 1.7)
        fit_to_frame(stmt)
        with self.voiceover(
            text="Continuity from below says exactly what you would hope: the "
                 "probability of the limit is the limit of the probabilities. "
                 "Pr of A equals the limit, as n goes to infinity, of Pr of A-n."
        ):
            self.play(Write(stmt))

        # Disjoint shells B_1 = A_1, B_k = A_k - A_{k-1} -- sized to the circles.
        B1 = Circle(radius=0.6).move_to(C).set_fill(BLUE, 0.7).set_stroke(INK, 1.5)
        B2 = Annulus(inner_radius=0.6, outer_radius=1.2, color=TEAL,
                     fill_opacity=0.7).move_to(C).set_stroke(INK, 1.5)
        B3 = Annulus(inner_radius=1.2, outer_radius=1.8, color=GREEN,
                     fill_opacity=0.7).move_to(C).set_stroke(INK, 1.5)
        shells = VGroup(B1, B2, B3)
        shell_def = VGroup(
            MathTex(r"B_1 = A_1", font_size=SMALL, color=INK),
            MathTex(r"B_k = A_k - A_{k-1}", font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.3 + UP * 0.6)
        shell_note = Text("disjoint shells", font_size=CAPTION, color=MUTED)
        shell_note.next_to(shell_def, DOWN, buff=0.35)
        fit_to_frame(shell_def)
        with self.voiceover(
            text="Why is it true? The trick is to disjointify. Let B-one be A-one, "
                 "and each later B-k be the new ring that A-k adds to "
                 "A-k-minus-one. These shells are disjoint, the first n of them "
                 "union to exactly A-n, and all of them together union to A."
        ):
            self.play(FadeIn(B1), FadeIn(B2), FadeIn(B3))
            self.play(Write(shell_def), FadeIn(shell_note, shift=UP * 0.1))

        # The proof chain lives on the right, under the shell definition, as two
        # left-aligned lines (the second reads as a continuation of the first).
        proof = VGroup(
            MathTex(r"\Pr(A) = \sum_{k=1}^{\infty} \Pr(B_k)",
                    font_size=SMALL, color=INK),
            MathTex(r"= \lim_{n \to \infty} \Pr(A_n)"
                    r" = \lim_{n \to \infty} \sum_{k=1}^{n} \Pr(B_k)",
                    font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        proof.next_to(shell_note, DOWN, buff=0.55)
        fit_to_frame(proof)
        with self.voiceover(
            text="Now apply the third axiom — countable additivity. Pr of A is the "
                 "infinite sum of the shell probabilities, which is the limit of "
                 "the partial sums, which is just the limit of Pr of A-n. The axiom "
                 "of countable additivity is doing all the work."
        ):
            self.play(Write(proof))
            self.play(Indicate(proof, color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ContinuityFromAbove(VoiceoverScene):
    """Beat: continuity-above -- decreasing intersection, via complements, the name."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Continuity from Above")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Circles, rectangle and label positioned to mirror Continuity from Below.
        C = LEFT * 3.4 + DOWN * 0.15
        frame = omega_box(width=5.2, height=4.6).move_to(C)

        # Decreasing sequence: A_1 outermost -> A_3 innermost (same radii/colours).
        radii = [1.8, 1.2, 0.6]
        cols = [GREEN, TEAL, BLUE]
        circs = VGroup()
        for r, col in zip(radii, cols):
            c = Circle(radius=r, color=INK).set_stroke(INK, 2)
            c.set_fill(col, opacity=0.20).move_to(C)
            circs.add(c)
        cap_inter = Circle(radius=0.28).move_to(C).set_fill(ACCENT, 0.7)
        cap_inter.set_stroke(ACCENT, 0)
        labs = VGroup(
            MathTex(r"A_1", font_size=CAPTION, color=INK).move_to(C + UP * 1.50),
            MathTex(r"A_2", font_size=CAPTION, color=INK).move_to(C + UP * 0.90),
            MathTex(r"A_3", font_size=CAPTION, color=INK).move_to(C + UP * 0.44),
        )
        # The intersection/limit label sits below the diagram, as in From Below.
        aLab = MathTex(r"A = \bigcap_{k} A_k", font_size=CAPTION, color=ACCENT)
        aLab.next_to(frame[0], DOWN, buff=0.20)

        with self.voiceover(
            text="The mirror image holds for a sequence that only shrinks. Now "
                 "A-one contains A-two contains A-three, and so on — a decreasing "
                 "sequence — closing down onto their intersection A, the part "
                 "common to all of them."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(LaggedStartMap(GrowFromCenter, circs, lag_ratio=0.3),
                      run_time=1.8)
            self.play(LaggedStartMap(FadeIn, labs, lag_ratio=0.2))
            self.play(FadeIn(cap_inter, scale=1.3), Write(aLab))

        comp = VGroup(
            MathTex(r"A_k \downarrow \;\Rightarrow\; A_k^{\mathrm{c}} \uparrow",
                    font_size=BODY, color=INK),
            Text("complements increase —", font_size=CAPTION, color=MUTED),
            Text("apply continuity from below,", font_size=CAPTION, color=MUTED),
            Text("then the complement rule.", font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.3 + UP * 0.5)
        fit_to_frame(comp)
        with self.voiceover(
            text="We do not need a new proof. Flip to complements: as the A-k "
                 "shrink, their complements grow, an increasing sequence we already "
                 "understand. Apply continuity from below to the complements, then "
                 "use the complement rule to flip back, and out comes the same "
                 "conclusion: Pr of A equals the limit of Pr of A-n."
        ):
            self.play(FadeIn(comp[0], shift=RIGHT * 0.3))
            self.play(LaggedStartMap(FadeIn, comp[1:], lag_ratio=0.25))

        result = MathTex(r"\Pr(A) = \lim_{n \to \infty} \Pr(A_n)",
                         font_size=BODY, color=ACCENT)
        banner = VGroup(
            result,
            Text("the continuity of probability", font_size=SMALL, color=INK),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.2)
        box = SurroundingRectangle(banner, color=ACCENT, buff=0.4,
                                   corner_radius=0.15).set_stroke(ACCENT, 2)
        fit_to_frame(VGroup(banner, box))
        with self.voiceover(
            text="Continuity from below, for growing events, and continuity from "
                 "above, for shrinking ones, together go by one name: the "
                 "continuity of probability. It is what lets us pass to the limit — "
                 "to talk about what happens eventually, not just at every finite "
                 "stage."
        ):
            self.play(FadeOut(frame), FadeOut(circs), FadeOut(cap_inter),
                      FadeOut(labs), FadeOut(aLab), FadeOut(comp))
            self.play(Write(result))
            self.play(FadeIn(banner[1], shift=UP * 0.1), Create(box))

        self.play(*[FadeOut(m) for m in self.mobjects])


class MeasureTheory(VoiceoverScene):
    """Beat: measure-theory -- cardinality ladder, the sigma-field, the close."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Probability and Measure Theory")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # --- The cardinality ladder: finite < countable < uncountable. ---
        def rung(top, sub, col):
            t = Text(top, font_size=SMALL, color=col)
            s = MathTex(sub, font_size=CAPTION, color=MUTED)
            g = VGroup(t, s).arrange(DOWN, buff=0.12)
            box = SurroundingRectangle(g, color=col, buff=0.22,
                                       corner_radius=0.12).set_stroke(col, 2)
            return VGroup(box, g)

        r1 = rung("finite", r"\{1,\dots,n\}", INK)
        r2 = rung("countably infinite", r"\mathbb{N},\ \mathbb{Q}", BAR)
        r3 = rung("uncountable", r"\mathbb{R}", ACCENT)
        rungs = VGroup(r1, r2, r3).arrange(RIGHT, buff=0.9).move_to(UP * 0.6)
        sub1 = MathTex(r"\subsetneq", font_size=BODY, color=MUTED).move_to(
            (r1.get_right() + r2.get_left()) / 2)
        sub2 = MathTex(r"\subsetneq", font_size=BODY, color=MUTED).move_to(
            (r2.get_right() + r3.get_left()) / 2)
        ladder = VGroup(rungs, sub1, sub2)
        fit_to_frame(ladder)

        with self.voiceover(
            text="One last honesty. Our intuition for the infinite climbs a "
                 "ladder. The finite we grasp directly. The countably infinite — "
                 "the integers, the rationals — we can at least list, one element "
                 "after another. The uncountable — the real numbers — cannot be "
                 "listed at all; there are strictly more of them. We use the finite "
                 "to understand the countable, and the countable to reach for the "
                 "uncountable."
        ):
            self.play(FadeIn(r1, shift=UP * 0.40))
            self.play(Write(sub1), FadeIn(r2, shift=UP * 0.40))
            self.play(Write(sub2), FadeIn(r3, shift=UP * 0.40))

        self.play(ladder.animate.scale(0.85).next_to(title, DOWN, buff=0.6))

        # --- Can we assign Pr to every subset? ---
        # Sit the question midway between the ladder above and the verdicts below.
        question = MathTex(r"\Pr : 2^{\Omega} \to [0,1] \;?",
                           font_size=BODY, color=INK).move_to(UP * 0.45)
        fit_to_frame(question)
        ok = VGroup(
            MathTex(r"\checkmark", font_size=BODY, color=GREEN),
            Text("finite / countable", font_size=CAPTION, color=MUTED),
        ).arrange(RIGHT, buff=0.40)
        bad = VGroup(
            MathTex(r"\times", font_size=BODY, color=MAROON),
            Text("uncountable — contradictions", font_size=CAPTION, color=MAROON),
        ).arrange(RIGHT, buff=0.40)
        verdicts = VGroup(ok, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        verdicts.next_to(question, DOWN, buff=1.15)
        fit_to_frame(verdicts)
        with self.voiceover(
            text="Now the catch. It is tempting to assign a probability to every "
                 "single subset of the sample space. For a finite or countable "
                 "Omega, fine. But for an uncountable Omega, this leads to genuine "
                 "contradictions that cannot be patched. You simply cannot weigh "
                 "every subset at once."
        ):
            self.play(Write(question))
            self.play(FadeIn(ok, shift=RIGHT * 0.2))
            self.play(FadeIn(bad, shift=RIGHT * 0.2))

        self.play(FadeOut(question), FadeOut(verdicts))

        # --- The sigma-field of admissible events. ---
        sf = VGroup(
            MathTex(r"\mathcal{F} \subseteq 2^{\Omega}", font_size=BODY, color=ACCENT),
            Text("σ-field of admissible events", font_size=CAPTION, color=MUTED),
            Text("closed under complement and countable unions",
                 font_size=CAPTION, color=INK),
        ).arrange(DOWN, buff=0.3).move_to(DOWN * 0.5)
        sf_box = SurroundingRectangle(sf, color=MUTED, buff=0.35,
                                      corner_radius=0.15).set_stroke(MUTED, 2)
        fit_to_frame(VGroup(sf, sf_box))
        with self.voiceover(
            text="The resolution is to step back and only assign probabilities to "
                 "a well-behaved sub-collection of events — closed under "
                 "complements and countable unions. Such a collection is called a "
                 "sigma-field, and the events in it are the admissible ones."
        ):
            self.play(Create(sf_box))
            self.play(LaggedStartMap(FadeIn, sf, lag_ratio=0.2))

        unify = Text("Measure theory — one framework for the discrete and the continuous.",
                     font_size=CAPTION, color=ACCENT).to_edge(DOWN, buff=1.2)
        fit_to_frame(unify)
        with self.voiceover(
            text="Studying sigma-fields and the measures defined on them is the "
                 "subject of measure theory, and measure-theoretic probability "
                 "gives one unified framework for the discrete and the continuous "
                 "alike. We are only pointing at the door here, not walking through "
                 "it."
        ):
            self.play(FadeIn(unify, shift=UP * 0.15))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- Centred two-line key idea + chapter close. ---
        key_idea = VGroup(
            Text("Probability is continuous along monotone sequences,",
                 font_size=BODY, color=INK),
            Text("and on uncountable spaces it lives on a σ-field.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("That completes the probabilistic model — sample space and probability law.",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="And that completes the probabilistic model: a sample space of "
                 "outcomes, and a probability law that obeys the axioms and "
                 "respects limits. Everything in the rest of the subject is built "
                 "on this foundation."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
