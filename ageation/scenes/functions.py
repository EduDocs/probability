# derived_from: content/02-functions-script.md
# derived_from_sha256: f71e635dc69712a79b5439b500b601d7f8297062beefa578da81259199e8716f
"""Chapter 1, Video 2 -- Functions (narrated with manim-voiceover).

Source notes : ../chapters/sets_and_functions.tex  (sections: Functions, and
               Set Theory and Probability)
Script        : content/02-functions-script.md

Timing model (bookmark-free, portable)
---------------------------------------
Narration drives the animation. Each beat is split into several *sequential*
``with self.voiceover(text=...) as tracker:`` blocks -- one per synchronization
point in the script -- and the animation for each block is timed with
``run_time=tracker.duration``, so the visuals match the voice sentence by
sentence with no Whisper / word-level dependency.

Rendering (on a machine with Manim installed; NOT a cloud sandbox)
-----------------------------------------------------------------
Draft (free Google TTS, needs internet):
    uv run manim -pql scenes/functions.py ChapterOverview
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
    Final  -> OpenAIService(voice="nova", ...): the voice chosen for this series
              (see 01-sets). Switch the two lines below for the final render and
              add OPENAI_API_KEY to the project .env.
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


# --- Shared visual helpers ---------------------------------------------------

def labeled_oval(labels, center, label_side, color=INK):
    """An oval 'set' with a vertical column of labelled dots.

    Returns ``(group, dots)`` where ``dots`` is the VGroup of bare Dots, so the
    caller can anchor arrows to them.
    """
    dots = VGroup(*[Dot(radius=0.08, color=color) for _ in labels])
    dots.arrange(DOWN, buff=0.55).move_to(center)
    labs = VGroup()
    for d, lab in zip(dots, labels):
        labs.add(MathTex(lab, font_size=SMALL, color=color)
                 .next_to(d, label_side, buff=0.14))
    oval = Ellipse(width=1.7, height=dots.height + 1.1, color=color)
    oval.set_stroke(color, 2).move_to(dots.get_center())
    return VGroup(oval, dots, labs), dots


def mapping_arrows(xdots, ydots, edges, color=ACCENT):
    """Arrows from xdots[i] to ydots[j] for each (i, j) in edges."""
    arrows = VGroup()
    for i, j in edges:
        arrows.add(Arrow(
            xdots[i].get_right(), ydots[j].get_left(),
            buff=0.1, stroke_width=3, tip_length=0.18, color=color,
        ))
    return arrows


def omega_frame(width, height, center):
    """The universal-set frame: a rounded rectangle labelled Omega (corner)."""
    box = RoundedRectangle(corner_radius=0.2, width=width, height=height,
                           color=MUTED).set_stroke(MUTED, 2).move_to(center)
    lab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    lab.next_to(box.get_corner(UL), DR, buff=0.22)
    return VGroup(box, lab)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of Sets, title, and outline by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Functions",
            "From single-valued relations to numbers we can compute with.",
            kicker="Chapter 1  ·  Sets and Functions",
        )
        tag = progress_tag(2, 2).to_corner(DR, buff=0.4)

        with self.voiceover(
            text="Last video, we built the language of sets — operations, "
                 "partitions, and the Cartesian product. Now we put that "
                 "language to work."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(tag), run_time=0.4)

        with self.voiceover(
            text="A function is a special kind of relation, and it is the bridge "
                 "from sets of outcomes to numbers we can compute with."
        ):
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Relations and functions", font_size=BODY),
            Text("2.  Domain, codomain, image, preimage", font_size=BODY),
            Text("3.  One-to-one and onto", font_size=BODY),
            Text("4.  The indicator function", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(items)

        clauses = [
            "In this video we define relations and functions,",
            "meet the domain, codomain, image, and preimage,",
            "sort functions into one-to-one and onto,",
            "and finish with the indicator function — our first real taste of "
            "probability.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class RelationsToFunctions(VoiceoverScene):
    """Beat: relations-to-functions -- relation, then the single-valued rule."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Relations and Functions")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        xg, xd = labeled_oval(["x_1", "x_2", "x_3"], LEFT * 3.2 + DOWN * 0.3, LEFT)
        yg, yd = labeled_oval(["y_1", "y_2", "y_3"], RIGHT * 3.2 + DOWN * 0.3, RIGHT)
        xlab = MathTex("X", font_size=BODY, color=INK).next_to(xg, UP, buff=0.2)
        ylab = MathTex("Y", font_size=BODY, color=INK).next_to(yg, UP, buff=0.2)

        with self.voiceover(
            text="Recall the Cartesian product: all ordered pairs with a first "
                 "entry from X and a second from Y."
        ):
            self.play(Create(xg[0]), Create(yg[0]),
                      FadeIn(xg[1]), FadeIn(yg[1]),
                      FadeIn(xg[2]), FadeIn(yg[2]),
                      Write(xlab), Write(ylab))

        # A "messy" relation: x_1 has two arrows, x_3 has none.
        messy = mapping_arrows(xd, yd, [(0, 0), (0, 1), (1, 1)], color=BAR)
        rel_cap = MathTex(r"\text{relation} \subset X \times Y",
                          font_size=SMALL, color=BAR).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            text="A relation between X and Y is simply any subset of that "
                 "product. When a pair belongs to the relation, we say x is "
                 "related to y — think of it as any bundle of arrows from X to Y."
        ):
            self.play(LaggedStart(*[GrowArrow(a) for a in messy], lag_ratio=0.25),
                      run_time=1.6)
            self.play(FadeIn(rel_cap))

        # Prune to single-valued: exactly one arrow leaves each x.
        func = mapping_arrows(xd, yd, [(0, 0), (1, 1), (2, 2)], color=ACCENT)
        func_cap = MathTex(r"\text{function: exactly one arrow from each } x",
                           font_size=SMALL, color=ACCENT).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            text="A function is a relation with one extra rule: it is "
                 "single-valued. For every element of X there is one, and only "
                 "one, element of Y it points to. None is left without an arrow, "
                 "and none has two."
        ):
            self.play(FadeOut(messy), run_time=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in func], lag_ratio=0.25),
                      run_time=1.5)
            self.play(FadeOut(rel_cap), FadeIn(func_cap))

        with self.voiceover(
            text="That unique partner is written f of x, and the rule that "
                 "produces it is called the rule of correspondence."
        ):
            fx = MathTex(r"f(x) = y", font_size=BODY, color=ACCENT)
            fx.next_to(title, DOWN, buff=1.0)
            self.play(Write(fx))

        self.play(*[FadeOut(m) for m in self.mobjects])


class DomainCodomain(VoiceoverScene):
    """Beat: domain-codomain -- f: X -> Y, the triple, and the x^2 example."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Domain, Codomain, and the Rule")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Wide arrow so the "domain"/"codomain" labels under X and Y don't crowd.
        mapping = MathTex(r"f", r":", r"X", r"\quad\to\quad", r"Y", font_size=TITLE)
        mapping.move_to(UP * 1.4)
        mapping[2].set_color(ACCENT)   # X
        mapping[4].set_color(BAR)      # Y
        dom = Text("domain", font_size=SMALL, color=ACCENT).next_to(mapping[2], DOWN, buff=0.5)
        cod = Text("codomain", font_size=SMALL, color=BAR).next_to(mapping[4], DOWN, buff=0.5)
        dom_arrow = Arrow(dom.get_top(), mapping[2].get_bottom(), buff=0.1,
                          stroke_width=2.5, color=ACCENT, tip_length=0.15)
        cod_arrow = Arrow(cod.get_top(), mapping[4].get_bottom(), buff=0.1,
                          stroke_width=2.5, color=BAR, tip_length=0.15)

        with self.voiceover(
            text="Two sets come with every function. The domain is the set it is "
                 "defined on — the allowed inputs. The codomain is the set the "
                 "outputs are constrained to lie in. We write f maps X to Y."
        ):
            self.play(Write(mapping))
            self.play(GrowArrow(dom_arrow), FadeIn(dom),
                      GrowArrow(cod_arrow), FadeIn(cod))

        triple = MathTex(
            r"(X, Y, f)", r"\quad\text{with graph}\quad", r"f \subset X \times Y",
            font_size=BODY, color=MUTED,
        ).move_to(DOWN * 0.6)
        with self.voiceover(
            text="Strictly speaking, a function is a triple: the domain, the "
                 "codomain, and the graph — that single-valued subset of the "
                 "Cartesian product. The picture and the formal triple say the "
                 "same thing."
        ):
            self.play(FadeIn(triple))

        example = VGroup(
            MathTex(r"f : \mathbb{R} \to \mathbb{R}", font_size=BODY),
            MathTex(r"f(x) = x^2 \qquad x \mapsto x^2", font_size=BODY, color=ACCENT),
        ).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            text="Here is a concrete example: f maps the real numbers to the "
                 "real numbers, with f of x equal to x squared. The rule of "
                 "correspondence is x maps to x squared."
        ):
            self.play(FadeIn(example))

        self.play(*[FadeOut(m) for m in self.mobjects])


class ImagePreimage(VoiceoverScene):
    """Beat: image-preimage -- image, preimage, level set, the x^2 two-points."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Image and Preimage")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        image = MathTex(r"f(X) = \{\, f(x) : x \in X \,\} \subseteq Y",
                        font_size=BODY, color=BAR).next_to(title, DOWN, buff=1.0)
        with self.voiceover(
            text="The image is the set of values the function actually attains — "
                 "all the f of x as x ranges over the domain. It is a subset of "
                 "the codomain, and need not fill it."
        ):
            self.play(Write(image))

        preimage = MathTex(
            r"f^{-1}(T) = \{\, x \in X : f(x) \in T \,\}",
            font_size=BODY, color=ACCENT).next_to(image, DOWN, buff=0.4)
        with self.voiceover(
            text="Going the other way: the preimage of a set T is the collection "
                 "of all inputs that land in T — every x whose output lies in T."
        ):
            self.play(Write(preimage))

        level = MathTex(
            r"f^{-1}(\{y\}) = \{\, x \in X : f(x) = y \,\} \quad (\text{level set})",
            font_size=SMALL, color=MUTED).next_to(preimage, DOWN, buff=0.4)
        fit_to_frame(level)
        with self.voiceover(
            text="The most useful case is the preimage of a single value, called "
                 "its level set: all the x that map to that one value."
        ):
            self.play(Write(level))

        self.play(FadeOut(image), FadeOut(preimage), FadeOut(level))

        # The x^2 picture: one output c, two inputs +/- sqrt(c).
        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[0, 5, 1],
            x_length=6.5, y_length=3.8,
            axis_config={"include_numbers": False, "font_size": 20},
            tips=False,
        )
        x_lab = axes.get_x_axis_label(MathTex("x", font_size=SMALL))
        y_lab = axes.get_y_axis_label(MathTex("f(x)", font_size=SMALL)).shift(DOWN * 0.35)
        graph = axes.plot(lambda x: x ** 2, x_range=[-2.18, 2.18], color=BAR)
        c = 2.0
        root = c ** 0.5
        hline = DashedLine(axes.c2p(-2.5, c), axes.c2p(2.5, c),
                           color=ACCENT, stroke_width=2)
        vL = DashedLine(axes.c2p(-root, c), axes.c2p(-root, 0),
                        color=MUTED, stroke_width=2)
        vR = DashedLine(axes.c2p(root, c), axes.c2p(root, 0),
                        color=MUTED, stroke_width=2)
        meet = VGroup(
            Dot(axes.c2p(-root, c), color=ACCENT),
            Dot(axes.c2p(root, c), color=ACCENT),
        )
        feet = VGroup(
            Dot(axes.c2p(-root, 0), color=ACCENT),
            Dot(axes.c2p(root, 0), color=ACCENT),
        )
        c_lab = MathTex("c", font_size=SMALL, color=ACCENT).next_to(
            axes.c2p(0, c), UP, buff=0.12).shift(RIGHT * 0.25)
        xL = MathTex(r"-\sqrt{c}", font_size=SMALL, color=ACCENT).next_to(
            axes.c2p(-root, 0), DOWN, buff=0.18)
        xR = MathTex(r"\sqrt{c}", font_size=SMALL, color=ACCENT).next_to(
            axes.c2p(root, 0), DOWN, buff=0.18)
        plot = VGroup(axes, x_lab, y_lab, graph, hline, vL, vR, meet, feet,
                      c_lab, xL, xR)
        plot.center().shift(DOWN * 0.8)
        fit_to_frame(plot)

        with self.voiceover(
            text="And here is the crucial fact: the preimage of a single value "
                 "can contain many arguments. Take f of x equal to x squared."
        ):
            self.play(Create(axes), Write(x_lab), Write(y_lab))
            self.play(Create(graph), run_time=1.2)

        with self.voiceover(
            text="Draw the horizontal line at height c. It meets the parabola at "
                 "minus root c and plus root c — so the preimage of c is two "
                 "points. One output, several inputs."
        ):
            self.play(Create(hline), FadeIn(c_lab))
            self.play(FadeIn(meet))
            self.play(Create(vL), Create(vR))
            self.play(FadeIn(feet), Write(xL), Write(xR))

        caption = MathTex(r"f^{-1}(\{c\}) = \{\, -\sqrt{c},\ \sqrt{c} \,\}",
                          font_size=BODY, color=ACCENT)
        caption.next_to(title, DOWN, buff=0.3)
        fit_to_frame(caption)
        with self.voiceover(
            text="Hold on to this picture: pulling a value back to the set of "
                 "inputs that produce it is exactly how a random variable will "
                 "work."
        ):
            self.play(Write(caption))
            self.play(Indicate(VGroup(meet, feet), color=ACCENT))

        self.play(*[FadeOut(m) for m in self.mobjects])


class InjSurjBij(VoiceoverScene):
    """Beat: properties -- injective, surjective, bijective, inverse."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("One-to-One and Onto")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        def diagram(x_labels, y_labels, edges, color=ACCENT):
            xg, xd = labeled_oval(x_labels, LEFT * 2.9 + DOWN * 0.3, LEFT)
            yg, yd = labeled_oval(y_labels, RIGHT * 2.9 + DOWN * 0.3, RIGHT)
            xl = MathTex("X", font_size=SMALL, color=INK).next_to(xg, UP, buff=0.15)
            yl = MathTex("Y", font_size=SMALL, color=INK).next_to(yg, UP, buff=0.15)
            arrows = mapping_arrows(xd, yd, edges, color=color)
            return VGroup(xg, yg, xl, yl, arrows)

        # Injective: distinct inputs -> distinct outputs (4th codomain elt unhit).
        inj = diagram(["x_1", "x_2", "x_3"], ["y_1", "y_2", "y_3", "y_4"],
                      [(0, 0), (1, 1), (2, 2)])
        inj_cap = MathTex(
            r"\text{injective:}\quad f(x_1)=f(x_2)\ \Rightarrow\ x_1=x_2",
            font_size=SMALL, color=ACCENT).to_edge(DOWN, buff=1.0)
        fit_to_frame(inj_cap)
        with self.voiceover(
            text="A function is injective, or one-to-one, if it never sends two "
                 "different inputs to the same output. Distinct inputs, distinct "
                 "outputs — no collisions."
        ):
            self.play(FadeIn(inj))
            self.play(FadeIn(inj_cap))
        self.play(FadeOut(inj), FadeOut(inj_cap))

        # Surjective: every codomain element hit (two inputs share an output).
        surj = diagram(["x_1", "x_2", "x_3", "x_4"], ["y_1", "y_2", "y_3"],
                       [(0, 0), (1, 1), (2, 2), (3, 2)], color=BAR)
        surj_cap = MathTex(
            r"\text{surjective:}\quad \forall\, y\in Y\ \exists\, x\in X:\ f(x)=y",
            font_size=SMALL, color=BAR).to_edge(DOWN, buff=1.0)
        fit_to_frame(surj_cap)
        with self.voiceover(
            text="A function is surjective, or onto, if its image is the whole "
                 "codomain. Every target value is hit by at least one input; "
                 "nothing is missed."
        ):
            self.play(FadeIn(surj))
            self.play(FadeIn(surj_cap))
        self.play(FadeOut(surj), FadeOut(surj_cap))

        # Bijective: a perfect pairing.
        bij = diagram(["x_1", "x_2", "x_3"], ["y_1", "y_2", "y_3"],
                      [(0, 0), (1, 1), (2, 2)])
        bij_cap = MathTex(r"\text{bijective: one-to-one and onto}",
                       font_size=SMALL, color=ACCENT).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            text="A function that is both one-to-one and onto is a bijection. "
                 "Every output is hit exactly once."
        ):
            self.play(FadeIn(bij))
            self.play(FadeIn(bij_cap))

        with self.voiceover(
            text="And that is exactly when an inverse exists. The inverse maps Y "
                 "back to X, undoing the original, and the preimage of every "
                 "value is a single point."
        ):
            inv = MathTex(r"f^{-1} : Y \to X", font_size=BODY, color=ACCENT)
            inv.next_to(title, DOWN, buff=0.3)
            self.play(Write(inv))
            self.play(Indicate(bij[4], color=ACCENT))

        self.play(*[FadeOut(m) for m in self.mobjects])


class IndicatorFunction(VoiceoverScene):
    """Beat: indicator -- 1_S : Omega -> {0,1}, the seed of the Bernoulli RV."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Indicator Function")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        frame = omega_frame(6.0, 3.8, LEFT * 2.7 + DOWN * 0.3)
        circ = Circle(radius=1.0, color=INK).set_fill(BAR, opacity=0.5)
        circ.set_stroke(INK, 2).move_to(frame[0].get_center() + LEFT * 1.3)
        s_lab = MathTex("S", font_size=BODY, color=INK).move_to(circ.get_center() + UP * 0.32)
        one = MathTex("1", font_size=BODY, color=ACCENT).move_to(circ.get_center() + DOWN * 0.4)
        zero = MathTex("0", font_size=BODY, color=ACCENT).move_to(
            frame[0].get_center() + RIGHT * 1.8)

        defn = MathTex(r"\mathbf{1}_S : \Omega \to \{0, 1\}",
                       font_size=BODY, color=ACCENT)
        cases = MathTex(
            r"\mathbf{1}_S(\omega) = \begin{cases} 1 & \omega \in S \\"
            r" 0 & \omega \notin S \end{cases}", font_size=BODY,
            color=INK)
        right_col = VGroup(defn, cases).arrange(DOWN, buff=0.5)
        right_col.move_to(RIGHT * 3.6 + DOWN * 0.3)
        fit_to_frame(right_col)

        with self.voiceover(
            text="Here is the function that opens the door to probability: the "
                 "indicator function. Fix a subset S of the universal set Omega. "
                 "The indicator of S maps Omega to just two values, zero and one."
        ):
            self.play(Create(frame[0]), Write(frame[1]))
            self.play(FadeIn(circ), Write(s_lab))
            self.play(Write(defn))

        with self.voiceover(
            text="For an outcome omega, the indicator is one when omega is in S, "
                 "and zero when it is not. It simply reports whether its input "
                 "belongs to S — one for yes, zero for no."
        ):
            self.play(FadeIn(one), FadeIn(zero))
            self.play(Write(cases))

        with self.voiceover(
            text="When Omega is a sample space, that single zero-or-one readout "
                 "is the seed of the Bernoulli random variable, which we meet in "
                 "full later in the course."
        ):
            bern = Text("seed of the Bernoulli random variable",
                        font_size=CAPTION, color=MUTED).to_edge(DOWN, buff=0.5)
            fit_to_frame(bern)
            self.play(FadeIn(bern))
            self.play(Indicate(VGroup(defn, cases), color=ACCENT, scale_factor=1.03))

        self.play(*[FadeOut(m) for m in self.mobjects])


class SetTheoryAndProbability(VoiceoverScene):
    """Beat: tie-back -- which set construct underwrites which probability idea."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Set Theory and Probability")
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        def row(left, right):
            return VGroup(
                Text(left, font_size=BODY, color=INK),
                MathTex(r"\longrightarrow", font_size=BODY, color=ACCENT),
                Text(right, font_size=BODY, color=ACCENT),
            ).arrange(RIGHT, buff=0.3)

        rows = VGroup(
            row("Universal set", "sample space"),
            row("Partition", "law of total probability"),
            row("Preimage", "random variable"),
            row("Cartesian product", "joint distribution"),
        ).arrange(DOWN, buff=0.5)
        rows.move_to(DOWN * 0.3)
        fit_to_frame(rows)

        with self.voiceover(
            text="Step back and look at what Chapter one assembled, because "
                 "every piece reappears in a probabilistic guise. The universal "
                 "set Omega becomes the sample space of an experiment."
        ):
            self.play(FadeIn(rows[0], shift=RIGHT * 0.3))

        with self.voiceover(
            text="A partition of it underlies the law of total probability — "
                 "breaking a question into disjoint cases."
        ):
            self.play(FadeIn(rows[1], shift=RIGHT * 0.3))

        with self.voiceover(
            text="The preimage of a function is the mechanism behind random "
                 "variables, and the Cartesian product lets us describe several "
                 "quantities jointly."
        ):
            self.play(FadeIn(rows[2], shift=RIGHT * 0.3))
            self.play(FadeIn(rows[3], shift=RIGHT * 0.3))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # Closing key idea + bridge (centred, two-line key idea).
        key_idea = VGroup(
            Text("A function sends each input to exactly one output;",
                 font_size=BODY, color=INK),
            Text("its preimage is the seed of the random variable.",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.18)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Combinatorics", font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So the set theory was never a detour — it is the scaffolding "
                 "the whole subject is built on. With sets and functions in hand, "
                 "we are ready to start counting, which is exactly what the next "
                 "chapter, combinatorics, is about."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
