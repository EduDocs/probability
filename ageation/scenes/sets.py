# derived_from: content/01-sets-script.md
# derived_from_sha256: 25c257cbe966e88dc34e64c582b0ef25c38a9042216b8814646a2989e0232c09
"""Chapter 1, Video 1 -- Sets (narrated with manim-voiceover).

Source notes : ../chapters/sets_and_functions.tex  (sections: chapter intro,
               Elementary Set Operations, Additional Rules and Properties,
               Cartesian Products)
Script        : content/01-sets-script.md

Timing model (bookmark-free, portable)
---------------------------------------
Narration drives the animation. Each beat is split into several *sequential*
``with self.voiceover(text=...) as tracker:`` blocks -- one per synchronization
point in the script -- and the animation for each block is timed with
``run_time=tracker.duration``, so the visuals match the voice sentence by
sentence with no Whisper / word-level dependency. Runs on free gTTS.

Rendering (on a machine with Manim installed; NOT a cloud sandbox)
-----------------------------------------------------------------
Draft (free Google TTS, needs internet):
    uv run manim -pql scenes/sets.py ChapterOverview
Final: switch make_speech_service() to OpenAIService (needs OPENAI_API_KEY).
"""

import os
import sys

# Ensure sibling modules (e.g. _style) import regardless of working directory.
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
    """Single place to choose the voice (mirrors voice: in the script YAML).

    Draft  -> GTTSService: free, no API key, cached by text hash.
    Final  -> OpenAIService(voice=..., model="tts-1"): needs OPENAI_API_KEY.
              Always call configure_openai_client() first. Voice choice is a
              deliberate per-video decision -- pick one of alloy / echo / fable /
              onyx / nova / shimmer, don't default. This video uses `nova`
              (enthusiastic, clear -- good for technical content).
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


# --- Shared visual helpers ---------------------------------------------------

def ball(label, color, radius=0.32, font_size=22):
    """A colored disk with a centered label -- mirrors the book's ball figures.

    The label is dark (BLACK) for contrast: the default palette is light/pastel,
    so a dark numeral reads far better than white on yellow / gray / teal.
    """
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


def omega_box(width=12.0, height=6.0):
    """The universal-set frame: a dashed rounded rectangle labelled Omega."""
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


def line_with_omega(prefix, suffix, font_size=BODY, color=INK):
    """A prose line with a LaTeX-rendered Omega inline (house Text for words).

    Keeps the surrounding words in the Pango house font while the symbol is the
    same math-italic ``\\Omega`` used everywhere else in the video.
    """
    return VGroup(
        Text(prefix, font_size=font_size, color=color),
        MathTex(r"\Omega", font_size=font_size, color=color),
        Text(suffix, font_size=font_size, color=color),
    ).arrange(RIGHT, buff=0.12)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Sets",
            "The language that all of probability is written in.",
            kicker="Chapter 1  ·  Sets and Functions",
        )
        tag = progress_tag(1, 2).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="Probability is built, from the ground up, on the language of "
                 "sets. So that is where we begin."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Sets, elements, and subsets", font_size=BODY),
            line_with_omega("2.  The empty set, ", ", and the complement",
                            font_size=BODY),
            Text("3.  Union, intersection, and difference", font_size=BODY),
            Text("4.  Partitions", font_size=BODY),
            Text("5.  Algebraic laws and De Morgan", font_size=BODY),
            Text("6.  The Cartesian product", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this first video we meet sets and their elements,",
            "the two special sets that anchor everything,",
            "the operations that combine sets,",
            "the idea of a partition,",
            "the algebraic laws,",
            "and finally the Cartesian product.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.5)

        with self.voiceover(
            text="Get comfortable here, because every idea in this course casts "
                 "a set-theoretic shadow."
        ):
            self.play(Indicate(items, color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class WhatIsASet(VoiceoverScene):
    """Beat: what-is-a-set -- elements, membership, subset, set-builder."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("What Is a Set?")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        box = RoundedRectangle(
            corner_radius=0.2, width=5.2, height=4.4, color=INK
        ).shift(LEFT * 3.3 + DOWN * 0.4)
        slabel = MathTex(r"S", font_size=BODY, color=INK)
        slabel.next_to(box.get_corner(UL), DR, buff=0.2)

        # Two tidy columns: a left cluster (1,3,5) that a subset loop can
        # cleanly encircle, and a right pair (2,4) it clearly excludes.
        specs = [
            ("1", RED, [-1.3, 0.8, 0]),
            ("2", BLUE, [0.9, 1.1, 0]),
            ("3", GREEN, [0.4, 0.0, 0]),
            ("4", GRAY_B, [1.5, -1.2, 0]),
            ("5", TEAL, [-1.3, -1.0, 0]),
        ]
        balls = VGroup()
        for lab, col, pos in specs:
            b = ball(lab, col)
            b.move_to(box.get_center() + np.array(pos))
            balls.add(b)

        # The right-hand fact column is anchored at a fixed centre so nothing
        # spills off-frame; each line is placed by move_to, top to bottom.
        RC = 3.4  # x-centre of the right column (box occupies the left half)

        with self.voiceover(
            text="A set is simply a collection of objects, which we call its "
                 "elements. Picture a box holding a handful of distinct objects; "
                 "each one is an element of the set."
        ):
            self.play(Create(box), Write(slabel))
            self.play(LaggedStartMap(FadeIn, balls, lag_ratio=0.18))

        # Membership: x in S (ball 1, inside) vs x not in S (ball 6, outside S).
        # Ball 6 is a permanent part of the diagram, placed just outside the box.
        mem = MathTex(r"x \in S", font_size=BODY, color=ACCENT).move_to([RC, 1.8, 0])
        notmem = MathTex(r"x \notin S", font_size=BODY, color=MAROON).move_to([RC, 1.0, 0])
        outsider = ball("6", MAROON).move_to(box.get_center() + np.array([3.4, -0.5, 0]))
        with self.voiceover(
            text="If an object x belongs to a set S, we write x is in S."
        ):
            self.play(Indicate(balls[0], color=ACCENT, scale_factor=1.4),
                      FadeIn(mem))
        with self.voiceover(
            text="If it does not belong, we write x is not in S."
        ):
            self.play(FadeIn(outsider), FadeIn(notmem))

        with self.voiceover(
            text="Two sets are equal exactly when they contain precisely the "
                 "same elements. Equality of sets is equality of contents, "
                 "nothing more."
        ):
            eq = MathTex(r"S = T \iff \text{same elements}",
                         font_size=SMALL, color=MUTED).move_to([RC, 0.05, 0])
            fit_to_frame(eq)
            self.play(Write(eq))

        # Subset: a clean loop around balls 1 and 5, labelled R (a subset of S).
        # Centred on the 1 & 5 column so ball 3 (between them) stays outside R.
        loop = Ellipse(width=1.5, height=3.0, color=ACCENT).set_stroke(ACCENT, 3)
        loop.move_to(VGroup(balls[0], balls[4]).get_center())
        rlab = MathTex(r"R", font_size=SMALL, color=ACCENT).next_to(loop, UP, buff=0.12)
        sub = MathTex(r"R \subset S", font_size=BODY, color=ACCENT).move_to([RC, -0.9, 0])
        proper = MathTex(r"R \subsetneq S \quad (R \neq S)",
                         font_size=SMALL, color=MUTED).move_to([RC, -1.7, 0])
        with self.voiceover(
            text="Now suppose every element of one set is also an element of "
                 "another. Then the first is a subset of the second. This still "
                 "allows the two sets to be equal; when they differ, we call it a "
                 "proper subset."
        ):
            self.play(Create(loop), FadeIn(rlab))
            self.play(FadeIn(sub), FadeIn(proper))

        with self.voiceover(
            text="And here is a fact that will become useful: two sets are equal "
                 "if and only if each is a subset of the other. That double "
                 "inclusion is how you prove two sets are the same."
        ):
            dbl = MathTex(r"S = T \iff S \subset T \ \text{and}\ T \subset S",
                          font_size=SMALL, color=ACCENT).move_to([RC, -2.6, 0])
            fit_to_frame(dbl)
            self.play(Write(dbl))

        self.play(FadeOut(loop), FadeOut(rlab),
                  *[FadeOut(m) for m in (mem, notmem, eq, sub, proper, dbl)])

        # Set-builder notation, centered under the box.
        with self.voiceover(
            text="How do we actually specify a set? If it is small, we just list "
                 "its elements inside braces."
        ):
            listed = MathTex(r"S = \{\, x_1, x_2, x_3 \,\}",
                             font_size=BODY, color=INK)
            # Centred between the rectangle's right edge and the frame edge.
            listed.move_to([3.2, 0.9, 0])
            self.play(Write(listed))

        with self.voiceover(
            text="More often, we start from some collection and keep only the "
                 "elements with a given property. Starting from the integers, the "
                 "even numbers are all x in the integers such that x is even."
        ):
            builder = MathTex(
                r"S = \{\, x \in \mathbb{Z} \mid x \text{ is even} \,\}",
                font_size=BODY, color=ACCENT,
            )
            builder.next_to(listed, DOWN, buff=0.6)
            fit_to_frame(builder)
            self.play(Write(builder))

        with self.voiceover(
            text="Read the braces as the set of, and the bar as such that."
        ):
            self.play(Indicate(builder, color=ACCENT))

        self.play(*[FadeOut(m) for m in self.mobjects])


class SpecialSets(VoiceoverScene):
    """Beat: special-sets -- empty set, universal set Omega, complement."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Special Sets and the Complement")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP).shift(DOWN * 0.3))

        # Empty set.
        empty = MathTex(r"\varnothing = \{\,\}", font_size=TITLE, color=INK)
        empty_cap = Text("the set with no elements", font_size=CAPTION, color=MUTED)
        empty_cap.next_to(empty, DOWN, buff=0.4)
        empty_grp = VGroup(empty, empty_cap).move_to(ORIGIN + UP * 0.2)
        with self.voiceover(
            text="Two special sets deserve names. The first is the empty set: "
                 "the set with no elements at all. It may look useless, but it is "
                 "the natural answer whenever a condition is never met."
        ):
            self.play(Write(empty))
            self.play(FadeIn(empty_cap))
        self.play(FadeOut(empty_grp))

        # Universal set Omega. Lift the Omega label to sit just above the
        # rectangle (with the "sample space" gloss beside it), not in the corner.
        frame = omega_box(width=8.5, height=4.6)
        frame.move_to(DOWN * 0.4)
        frame[1].next_to(frame[0].get_top(), UP, buff=0.2).shift(LEFT * 1.5)
        with self.voiceover(
            text="The second is the universal set, written capital Omega: the "
                 "collection of all objects of interest in the problem at hand. "
                 "Once we fix Omega, every set we care about lives inside it."
        ):
            self.play(Create(frame[0]), Write(frame[1]))

        sample = Text("= the sample space", font_size=SMALL, color=ACCENT)
        sample.next_to(frame[1], RIGHT, buff=0.25)
        with self.voiceover(
            text="Remember this symbol: in probability, Omega has a special name "
                 "— the sample space, the set of all possible outcomes of an "
                 "experiment."
        ):
            self.play(FadeIn(sample, shift=RIGHT * 0.3))
            self.play(Indicate(VGroup(frame[1], sample), color=ACCENT))

        # Complement.
        circ = Circle(radius=1.5, color=INK).set_fill(BAR, opacity=0.55)
        circ.set_stroke(INK, 2).move_to(frame[0].get_center() + LEFT * 1.4)
        s_lab = MathTex(r"S", font_size=BODY, color=INK).move_to(circ.get_center())
        with self.voiceover(
            text="With a universal set in hand we can define the complement of a "
                 "set S. First, here is S, a region inside Omega."
        ):
            self.play(FadeIn(circ), Write(s_lab))

        comp_region = shaded(Difference(frame[0], circ), ACCENT, opacity=0.4)
        comp_lab = MathTex(r"S^{\mathrm{c}} = \{\, x \in \Omega \mid x \notin S \,\}",
                           font_size=SMALL, color=ACCENT)
        comp_lab.next_to(frame[0], DOWN, buff=0.35)
        fit_to_frame(comp_lab)
        with self.voiceover(
            text="The complement of S is everything in Omega that is not in S — "
                 "all the rest of the frame. We write it S with a small c."
        ):
            self.play(FadeIn(comp_region))
            self.play(Write(comp_lab))

        with self.voiceover(
            text="As a sanity check, the complement of Omega itself is the empty "
                 "set: outside of everything, there is nothing."
        ):
            self.play(Indicate(frame[0], color=ACCENT, scale_factor=1.0))

        self.play(*[FadeOut(m) for m in self.mobjects])


class SetOperations(VoiceoverScene):
    """Beat: operations -- union, intersection, disjoint, difference (Venn)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Elementary Set Operations")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Fixed pair of overlapping circles inside a faint Omega frame.
        frame = omega_box(width=9.5, height=4.8).shift(DOWN * 0.5)
        cS = Circle(radius=1.5, color=INK).set_stroke(INK, 2)
        cT = Circle(radius=1.5, color=INK).set_stroke(INK, 2)
        cS.move_to(frame[0].get_center() + LEFT * 0.85)
        cT.move_to(frame[0].get_center() + RIGHT * 0.85)
        labS = MathTex(r"S", font_size=BODY, color=INK).next_to(cS, UL, buff=-0.1)
        labT = MathTex(r"T", font_size=BODY, color=INK).next_to(cT, UR, buff=-0.1)
        circles = VGroup(cS, cT, labS, labT)

        # The operation label sits just above the rectangle (not high under the
        # title); the later operations Transform into this same position.
        formula = MathTex(r"S \cup T", font_size=BODY, color=ACCENT)
        formula.next_to(frame[0], UP, buff=0.15)

        with self.voiceover(
            text="Now we combine sets. Throughout, picture two overlapping "
                 "circles, S on the left and T on the right, sitting inside Omega."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(Create(cS), Create(cT), Write(labS), Write(labT))

        # Union.
        region = shaded(Union(cS, cT), BAR, opacity=0.55)
        with self.voiceover(
            text="The union of S and T is everything that lies in S, or in T, or "
                 "in both. We shade both circles completely — the union holds "
                 "anything caught by either one."
        ):
            self.play(FadeIn(formula), FadeIn(region))

        # Intersection.
        with self.voiceover(
            text="The intersection is stricter: only the elements that lie in S "
                 "and in T at the same time. That is the overlapping lens in the "
                 "middle, and nothing else."
        ):
            new_formula = MathTex(r"S \cap T", font_size=BODY, color=ACCENT)
            new_formula.move_to(formula)
            new_region = shaded(Intersection(cS, cT), BAR, opacity=0.7)
            self.play(FadeOut(region), Transform(formula, new_formula))
            self.play(FadeIn(new_region))
            region = new_region

        # Disjoint: pull circles apart, intersection empties.
        with self.voiceover(
            text="Sometimes two sets share no elements at all — their "
                 "intersection is the empty set. We call such sets disjoint, and "
                 "we will lean on disjointness again and again, because for "
                 "disjoint events probabilities simply add."
        ):
            disj_formula = MathTex(r"S \cap T = \varnothing",
                                   font_size=BODY, color=ACCENT).move_to(formula)
            cS_apart = cS.copy().shift(LEFT * 1.1)
            cT_apart = cT.copy().shift(RIGHT * 1.1)
            self.play(
                FadeOut(region),
                Transform(formula, disj_formula),
                Transform(cS, cS_apart), Transform(cT, cT_apart),
                labS.animate.next_to(cS_apart, UL, buff=-0.1),
                labT.animate.next_to(cT_apart, UR, buff=-0.1),
            )
            self.wait(0.3)

        # Bring them back together for the difference.
        with self.voiceover(
            text="Finally, bring the circles back together. The difference S "
                 "minus T is the set of elements that are in S but not in T."
        ):
            self.play(
                Transform(cS, Circle(radius=1.5, color=INK).set_stroke(INK, 2)
                          .move_to(frame[0].get_center() + LEFT * 0.85)),
                Transform(cT, Circle(radius=1.5, color=INK).set_stroke(INK, 2)
                          .move_to(frame[0].get_center() + RIGHT * 0.85)),
                labS.animate.next_to(frame[0].get_center() + LEFT * 0.85, UL, buff=0.35),
                labT.animate.next_to(frame[0].get_center() + RIGHT * 0.85, UR, buff=0.35),
            )
            diff_formula = MathTex(r"S - T", font_size=BODY, color=ACCENT).move_to(formula)
            diff_region = shaded(Difference(cS, cT), BAR, opacity=0.6)
            self.play(Transform(formula, diff_formula), FadeIn(diff_region))
            region = diff_region

        with self.voiceover(
            text="Take the left circle and carve away the overlap; what remains "
                 "is S minus T. This is also called the complement of T relative "
                 "to S — the same idea as before, measured inside S instead of "
                 "inside all of Omega."
        ):
            self.play(Indicate(region, color=ACCENT, scale_factor=1.05))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Partition(VoiceoverScene):
    """Beat: partition -- disjoint wedges tiling a disk; total-probability tease."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Disjointness and Partitions")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        r = 2.0
        wedge_specs = [
            (0, TAU / 3, BLUE, "S_1"),
            (TAU / 3, TAU / 3, GREEN, "S_2"),
            (2 * TAU / 3, TAU / 3, RED, "S_3"),
        ]
        wedges = VGroup()
        labels = VGroup()
        for start, ang, col, name in wedge_specs:
            w = AnnularSector(
                inner_radius=0.0, outer_radius=r, angle=ang, start_angle=start,
                fill_color=col, fill_opacity=0.5, stroke_color=INK, stroke_width=2,
            )
            wedges.add(w)
            mid = start + ang / 2
            lab = MathTex(name, font_size=SMALL, color=INK)
            lab.move_to(0.6 * r * np.array([np.cos(mid), np.sin(mid), 0]))
            labels.add(lab)
        disk = VGroup(wedges, labels).move_to(DOWN * 0.4)
        slab = MathTex(r"S", font_size=BODY, color=INK).next_to(disk, LEFT, buff=0.6)

        with self.voiceover(
            text="Here is a structure worth singling out. Take a set and break it "
                 "into pieces so that no two pieces overlap, and together the "
                 "pieces use up the whole set."
        ):
            self.play(Write(slab))
            self.play(LaggedStartMap(FadeIn, wedges, lag_ratio=0.3),
                      run_time=1.6)
            self.play(LaggedStartMap(Write, labels, lag_ratio=0.3))

        defn = Text(
            "A partition: nonempty, disjoint, and their union is S.",
            font_size=CAPTION, color=ACCENT,
        )
        defn.next_to(disk, DOWN, buff=0.5)
        fit_to_frame(defn)
        with self.voiceover(
            text="A collection of nonempty, disjoint sets whose union is the "
                 "whole thing is called a partition. Every point of the disk "
                 "lands in exactly one wedge — no gaps, no double counting."
        ):
            self.play(FadeIn(defn))
            self.play(LaggedStart(*[Indicate(w, color=ACCENT) for w in wedges],
                                  lag_ratio=0.25))

        # Total-probability tease: a faint event crossing all wedges.
        event = Ellipse(width=1.8, height=0.95, color=ACCENT)
        event.set_fill(ACCENT, opacity=0.25).set_stroke(ACCENT, 2)
        event.move_to(disk.get_center() + RIGHT * 0.1)
        ev_lab = MathTex(r"A", font_size=SMALL, color=ACCENT).next_to(event, UP, buff=0.15)
        with self.voiceover(
            text="Keep this picture in mind. When the sample space is "
                 "partitioned into cases, the probability of any event can be "
                 "assembled, piece by piece, from its overlap with each case."
        ):
            self.play(FadeIn(event), FadeIn(ev_lab))

        with self.voiceover(
            text="That is the law of total probability, and a partition is "
                 "exactly what makes it work."
        ):
            self.play(Indicate(event, color=ACCENT, scale_factor=1.08))

        self.play(*[FadeOut(m) for m in self.mobjects])


class AlgebraicRules(VoiceoverScene):
    """Beat: rules -- precedence, distributive laws, De Morgan (two-set+indexed)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Algebraic Rules and De Morgan's Laws")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Precedence: order matters -- shown as two differently-shaded 3-set
        # Venn diagrams (after the book's figure), one per side of the formula.
        prec = MathTex(
            r"R \cup (S \cap T)", r"\;\neq\;", r"(R \cup S) \cap T",
            font_size=BODY,
        )
        prec.next_to(title, DOWN, buff=0.5)
        prec[0].set_color(ACCENT)   # left Venn shaded to match
        prec[2].set_color(BAR)      # right Venn shaded to match

        def venn_triple(center, kind, color):
            """Three overlapping circles R, S, T with one boolean region shaded."""
            r = 0.8
            cR = Circle(radius=r, color=INK).set_stroke(INK, 2).move_to(center + np.array([-0.5, 0.42, 0]))
            cS = Circle(radius=r, color=INK).set_stroke(INK, 2).move_to(center + np.array([0.5, 0.42, 0]))
            cT = Circle(radius=r, color=INK).set_stroke(INK, 2).move_to(center + np.array([0.0, -0.5, 0]))
            if kind == "left":           # R u (S n T)
                region = Union(cR, Intersection(cS, cT))
            else:                         # (R u S) n T
                region = Intersection(Union(cR, cS), cT)
            shaded(region, color, 0.6)
            lab = VGroup(
                MathTex("R", font_size=CAPTION, color=INK).next_to(cR, UP, buff=0.15),
                MathTex("S", font_size=CAPTION, color=INK).next_to(cS, UP, buff=0.15),
                MathTex("T", font_size=CAPTION, color=INK).next_to(cT, DOWN, buff=0.15),
            )
            return VGroup(cR, cS, cT), region, lab

        left_c, left_r, left_l = venn_triple(LEFT * 3.3 + DOWN * 1.0, "left", ACCENT)
        right_c, right_r, right_l = venn_triple(RIGHT * 3.3 + DOWN * 1.0, "right", BAR)

        with self.voiceover(
            text="Set operations obey an algebra, much like ordinary arithmetic. "
                 "First, order matters, so we use parentheses to show precedence. "
                 "These two combinations are generally different sets. When in "
                 "doubt, parenthesize."
        ):
            self.play(Write(prec))
            self.play(FadeIn(left_c), FadeIn(left_l),
                      FadeIn(right_c), FadeIn(right_l))
            self.play(FadeIn(left_r), FadeIn(right_r))
            self.play(Indicate(prec[1], color=ACCENT))
        self.play(FadeOut(prec),
                  FadeOut(left_c), FadeOut(left_l), FadeOut(left_r),
                  FadeOut(right_c), FadeOut(right_l), FadeOut(right_r))

        # Distributive laws.
        dist = VGroup(
            MathTex(r"R \cap (S \cup T) = (R \cap S) \cup (R \cap T)",
                    font_size=SMALL),
            MathTex(r"R \cup (S \cap T) = (R \cup S) \cap (R \cup T)",
                    font_size=SMALL),
        ).arrange(DOWN, buff=0.4).next_to(title, DOWN, buff=1.0)
        with self.voiceover(
            text="Two combinations, though, always agree — the distributive "
                 "laws. Intersection distributes over union, and union "
                 "distributes over intersection, exactly mirroring how "
                 "multiplication distributes over addition."
        ):
            self.play(LaggedStartMap(FadeIn, dist, lag_ratio=0.4))
            self.wait(0.3)
        self.play(FadeOut(dist))

        # De Morgan, shown on a fixed pair of circles.
        frame = omega_box(width=5.2, height=4.2).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        cS = Circle(radius=1.1, color=INK).set_stroke(INK, 2)
        cT = Circle(radius=1.1, color=INK).set_stroke(INK, 2)
        cS.move_to(frame[0].get_center() + LEFT * 0.6)
        cT.move_to(frame[0].get_center() + RIGHT * 0.6)
        labS = MathTex(r"S", font_size=SMALL, color=INK).next_to(cS, UL, buff=-0.05)
        labT = MathTex(r"T", font_size=SMALL, color=INK).next_to(cT, UR, buff=-0.05)

        # De Morgan identity on a single centred line in the right-hand region;
        # revealed in two parts (LHS first, then "= ..." as the narration turns).
        dm = MathTex(r"(S \cup T)^{\mathrm{c}}", r"=",
                     r"S^{\mathrm{c}} \cap T^{\mathrm{c}}",
                     font_size=BODY, color=ACCENT)
        dm.move_to([3.0, 0.9, 0])
        fit_to_frame(dm)

        with self.voiceover(
            text="The most useful identities are De Morgan's laws. They describe "
                 "what happens when you take the complement of a combination. "
                 "Here is the complement of the union of S and T: everything "
                 "outside both circles."
        ):
            self.play(Create(frame[0]), Write(frame[1]),
                      Create(cS), Create(cT), Write(labS), Write(labT))
            comp_union = shaded(Difference(frame[0], Union(cS, cT)), ACCENT, 0.45)
            self.play(FadeIn(comp_union), Write(dm[0]))

        with self.voiceover(
            text="That very same region is the intersection of the complements: "
                 "the points outside S and outside T. Complement flips union into "
                 "intersection."
        ):
            self.play(Write(dm[1:]))
            self.play(Indicate(comp_union, color=ACCENT, scale_factor=1.05))

        # Indexed form.
        with self.voiceover(
            text="And this is not limited to two sets. Take the complement of a "
                 "union over any index set, finite or infinite, and you get the "
                 "intersection of all the complements. De Morgan scales to as "
                 "many sets as you like."
        ):
            indexed = MathTex(
                r"\left( \bigcup_{i \in I} S_i \right)^{\mathrm{c}}"
                r" = \bigcap_{i \in I} S_i^{\mathrm{c}}",
                font_size=SMALL, color=INK,
            )
            indexed.next_to(dm, DOWN, buff=0.6)
            fit_to_frame(indexed)
            self.play(Write(indexed))

        self.play(*[FadeOut(m) for m in self.mobjects])


class CartesianProduct(VoiceoverScene):
    """Beat: cartesian -- ordered pairs, the S x T grid, then the outro/bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Cartesian Products")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Ordered pair, order matters.
        pair = MathTex(r"(\,x,\, y\,)", font_size=TITLE, color=INK).shift(UP * 0.5)
        order = MathTex(r"(1, a) \;\neq\; (a, 1)", font_size=BODY, color=ACCENT)
        order.next_to(pair, DOWN, buff=0.6)
        with self.voiceover(
            text="There is one more way to build a new set, and it is the one "
                 "that lets probability talk about several things at once. Start "
                 "with an ordered pair: a first object and a second object, where "
                 "the order matters."
        ):
            self.play(Write(pair))
            self.play(FadeIn(order))
            self.play(Indicate(order, color=ACCENT))
        self.play(FadeOut(pair), FadeOut(order))

        # Definition.
        defn = MathTex(
            r"S \times T = \{\, (x, y) \mid x \in S,\ y \in T \,\}",
            font_size=SMALL, color=ACCENT,
        )
        defn.next_to(title, DOWN, buff=1.0)
        fit_to_frame(defn)
        with self.voiceover(
            text="The Cartesian product of S and T, written S cross T, is the set "
                 "of all ordered pairs whose first entry comes from S and whose "
                 "second entry comes from T."
        ):
            self.play(Write(defn))

        # Build the 3 x 2 grid from {1,2,3} x {a,b}.
        s_cols = [("1", RED), ("2", BLUE), ("3", GREEN)]
        t_rows = [("a", YELLOW), ("b", PINK)]

        s_group = VGroup(*[ball(l, c) for l, c in s_cols])
        s_group.arrange(DOWN, buff=0.45).to_edge(LEFT, buff=1.4).shift(DOWN * 0.6)
        s_brace_lab = MathTex(r"S", font_size=SMALL, color=MUTED).next_to(s_group, UP, buff=0.25)

        t_group = VGroup(*[ball(l, c) for l, c in t_rows])
        t_group.arrange(DOWN, buff=0.45).next_to(s_group, RIGHT, buff=0.8)
        t_brace_lab = MathTex(r"T", font_size=SMALL, color=MUTED).next_to(t_group, UP, buff=0.25)

        with self.voiceover(
            text="Take S to be one, two, three, and T to be a and b."
        ):
            self.play(LaggedStartMap(FadeIn, s_group, lag_ratio=0.2),
                      FadeIn(s_brace_lab))
            self.play(LaggedStartMap(FadeIn, t_group, lag_ratio=0.2),
                      FadeIn(t_brace_lab))

        # The product grid: a paired ball for every (s, t).
        grid = VGroup()
        for j, (tl, tc) in enumerate(t_rows):
            for i, (sl, sc) in enumerate(s_cols):
                cell = VGroup(
                    ball(sl, sc, radius=0.26, font_size=18),
                    ball(tl, tc, radius=0.26, font_size=18),
                ).arrange(RIGHT, buff=0.08)
                grid.add(cell)
        grid.arrange_in_grid(rows=2, cols=3, buff=(0.55, 0.6))
        grid.to_edge(RIGHT, buff=1.2).shift(DOWN * 0.6)
        arrow = Arrow(t_group.get_right(), grid.get_left(),
                      color=ACCENT, buff=0.4, stroke_width=4)
        count = MathTex(r"|S \times T| = 3 \times 2 = 6",
                        font_size=SMALL, color=MUTED).next_to(grid, DOWN, buff=0.4)
        fit_to_frame(VGroup(grid, count))

        with self.voiceover(
            text="Pair every element of S with every element of T, and you get a "
                 "grid: here, six ordered pairs in all. That grid is the "
                 "Cartesian product."
        ):
            self.play(GrowArrow(arrow))
            self.play(LaggedStartMap(FadeIn, grid, lag_ratio=0.12), run_time=2.0)
            self.play(FadeIn(count))

        with self.voiceover(
            text="When we reach random vectors later in the course, this is the "
                 "construction that lets us describe two quantities jointly."
        ):
            self.play(Indicate(grid, color=ACCENT, scale_factor=1.04))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing summary: recap the six topics as they are named, so the
        # narration plays over a retrieval cue rather than a blank screen.
        recap_title = section_title("What we covered").to_edge(UP)
        recap = VGroup(
            Text("Sets, elements, and subsets", font_size=SMALL),
            line_with_omega("The empty set, ", ", and the complement",
                            font_size=SMALL),
            Text("Union, intersection, and difference", font_size=SMALL),
            Text("Partitions", font_size=SMALL),
            Text("Algebraic laws and De Morgan", font_size=SMALL),
            Text("The Cartesian product", font_size=SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        # Vertically centre the list between the title and the bottom of frame.
        mid_y = (recap_title.get_bottom()[1] - config.frame_height / 2) / 2
        recap.move_to([0, mid_y, 0])
        fit_to_frame(recap)
        with self.voiceover(
            text="And that completes our tour of sets. We have the elements and "
                 "subsets, the empty and universal sets and the complement, the "
                 "operations and partitions, the algebraic laws, and the "
                 "Cartesian product — the alphabet that the rest of probability "
                 "is spelled with."
        ):
            self.play(FadeIn(recap_title, shift=DOWN * 0.2), run_time=0.6)
            self.play(LaggedStartMap(FadeIn, recap, lag_ratio=0.18), run_time=2.4)
            self.play(Indicate(recap, color=ACCENT, scale_factor=1.02))
        self.play(FadeOut(recap_title), FadeOut(recap))

        # Built inline (not via outro_bridge) so the split key idea is centred
        # line-over-line rather than left-justified.
        key_idea = VGroup(
            Text("Sets, their operations, and the Cartesian product",
                 font_size=BODY, color=INK),
            Text("are the alphabet of probability.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Functions", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="In the next video we put this language to work and study "
                 "functions: the special relations that send each input to "
                 "exactly one output, and the bridge from outcomes to numbers."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
