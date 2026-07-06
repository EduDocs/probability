# derived_from: content/17-functions-of-random-variables-script.md
# derived_from_sha256: e9ce82bc4d5e7846423174ea2a046f89543d158c79df68b2d7e4afce5e68c717
"""Chapter 5, Video 3 -- Functions of Random Variables.

Source notes : ../chapters/discrete_random_variables.tex (Y = g(X): the PMF of
               a function of a random variable, the affine special case, and the
               taxi-fare worked example).
Script        : content/17-functions-of-random-variables-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, one per <bookmark> segment -- the same
pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/functions_of_random_variables.py ChapterOverview
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


KICKER = "Chapter 5  ·  Discrete Random Variables"


def ball(label, color, radius=0.24, font_size=20):
    """A colored disk with a dark centered label (Chapter 2 house style)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap, the guiding question, and a short outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        # Manual intro card so the objective sits on two centred lines (no
        # on-screen recap line -- the spoken recap in the narration is enough).
        intro = VGroup(
            Text(KICKER, font_size=SMALL, color=ACCENT),
            Text("Functions of Random Variables", font_size=TITLE, color=INK),
            VGroup(
                Text("Transform a random variable into a new one, Y = g(X),",
                     font_size=SMALL, color=MUTED),
                Text("and compute its PMF by summing mass over preimages.",
                     font_size=SMALL, color=MUTED),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(intro)
        tag = progress_tag(3, 3).to_corner(DR, buff=0.4)

        question = MathTex(r"Y = g(X): \ \text{what is its PMF?}",
                           font_size=BODY, color=ACCENT)
        outline = VGroup(
            Text("1.  Y = g(X) is a random variable", font_size=SMALL, color=INK),
            Text("2.  Its PMF from preimages", font_size=SMALL, color=INK),
            Text("3.  The affine case", font_size=SMALL, color=INK),
            Text("4.  Worked example: taxi fare", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)

        with self.voiceover(
            text="Last video we collected the named discrete distributions. This "
                 "time we do something with a random variable rather than just "
                 "describe it. Very often the quantity we care about isn't what we "
                 "measure directly -- it's some function of it. A fare from a "
                 "distance, a cost from a count, energy from a voltage. So the "
                 "question is: if X is a random variable and we apply a function g "
                 "to it, what is the new random variable Y equals g of X, and what "
                 "is its PMF? We'll answer that, and then work the classic "
                 "taxi-fare example end to end."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

            block = VGroup(question, outline).arrange(DOWN, buff=0.6)
            block.next_to(intro, DOWN, buff=0.9)
            fit_to_frame(block)
            self.play(Write(question), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in outline],
                                  lag_ratio=0.3), run_time=1.4)

        self.play(*[FadeOut(m) for m in self.mobjects])


class FunctionOfRandomVariable(VoiceoverScene):
    """Beat: function-of-rv -- the composition picture Omega -> X -> Y."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("A Function of a Random Variable")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Omega box with a handful of colored outcomes on the far left.
        box = RoundedRectangle(
            corner_radius=0.2, width=3.0, height=3.6, color=INK
        ).move_to(LEFT * 4.7 + DOWN * 0.4)
        omega = MathTex(r"\Omega", font_size=BODY).next_to(
            box.get_corner(UL), DR, buff=0.2
        )

        colors = [RED, BLUE, GREEN, TEAL, MAROON]
        positions = [
            box.get_center() + np.array(p)
            for p in [
                [-0.6, 1.1, 0], [0.6, 0.6, 0], [-0.5, -0.4, 0],
                [0.6, -1.0, 0], [0.0, 0.1, 0],
            ]
        ]
        outcomes = VGroup(*[
            ball(str(i + 1), c).move_to(pos)
            for i, (c, pos) in enumerate(zip(colors, positions))
        ])

        # First number line: X(Omega) on the real line.
        line_x = NumberLine(
            x_range=[0, 5, 1], length=3.4, include_numbers=True, font_size=20,
        ).move_to(LEFT * 0.4 + DOWN * 0.4)
        xlabel = MathTex(r"X", font_size=BODY, color=ACCENT).next_to(
            line_x, UP, buff=0.55
        )

        # Second number line: Y(Omega) = g(X(Omega)).
        line_y = NumberLine(
            x_range=[0, 5, 1], length=3.4, include_numbers=True, font_size=20,
        ).move_to(RIGHT * 4.2 + DOWN * 0.4)
        ylabel = MathTex(r"Y = g(X)", font_size=BODY, color=ACCENT).next_to(
            line_y, UP, buff=0.55
        )

        x_targets = [1, 4, 2, 4, 3]        # note outcomes 2 and 4 both land on 4
        arrows_x = VGroup()
        for grp, t in zip(outcomes, x_targets):
            arrows_x.add(CurvedArrow(
                grp.get_center() + RIGHT * 0.42,
                line_x.number_to_point(t),
                angle=-PI / 6, color=MUTED, stroke_width=3, tip_length=0.16,
            ))

        # g maps X-values to Y-values, merging (1,2,3,4 -> some collapse).
        g_map = {1: 1, 2: 3, 3: 3, 4: 2}    # g merges 2 and 3 onto 3
        arrows_g = VGroup()
        for xv, yv in g_map.items():
            arrows_g.add(CurvedArrow(
                line_x.number_to_point(xv) + UP * 0.15,
                line_y.number_to_point(yv),
                angle=-PI / 5, color=ACCENT, stroke_width=3, tip_length=0.16,
            ))

        merge_note = MathTex(r"|g(X(\Omega))| \le |X(\Omega)|",
                             font_size=SMALL, color=INK)
        merge_cap = Text("g can merge values, never split them",
                         font_size=CAPTION, color=MUTED)
        # The two commentary lines sit under the midpoint of the two number
        # lines, raised off the frame edge.
        merge_grp = VGroup(merge_cap, merge_note).arrange(DOWN, buff=0.2)
        mid_x = (line_x.get_center()[0] + line_y.get_center()[0]) / 2
        merge_grp.next_to(line_y, DOWN, buff=0.9).set_x(mid_x)

        diagram = VGroup(box, omega, outcomes, line_x, xlabel,
                         line_y, ylabel, arrows_x, arrows_g)
        fit_to_frame(VGroup(diagram, merge_grp))

        with self.voiceover(
            text="Recall that a random variable is already a function of the "
                 "outcome."
        ):
            self.play(Create(box), Write(omega))
            self.play(LaggedStartMap(FadeIn, outcomes, lag_ratio=0.2))

        with self.voiceover(
            text="X takes each outcome omega to a number x on the real line."
        ):
            self.play(Create(line_x), Write(xlabel))
            self.play(LaggedStart(*[Create(a) for a in arrows_x],
                                  lag_ratio=0.25), run_time=1.8)

        with self.voiceover(
            text="Now apply a second function g to that number, sending x onward "
                 "to a value y equals g of x."
        ):
            self.play(Create(line_y), Write(ylabel))
            self.play(LaggedStart(*[Create(a) for a in arrows_g],
                                  lag_ratio=0.25), run_time=1.8)

        with self.voiceover(
            text="Chain them together and you have a single map from outcomes "
                 "straight to y -- and since it assigns a number to every "
                 "outcome, Y equals g of X is itself a random variable."
        ):
            self.play(Indicate(VGroup(arrows_x, arrows_g), color=ACCENT))

        with self.voiceover(
            text="And if X is discrete, so is Y. In fact g can only merge values, "
                 "never split them, so Y takes no more values than X does."
        ):
            self.play(FadeIn(merge_cap, shift=UP * 0.1))
            self.play(Write(merge_note))

        self.play(*[FadeOut(m) for m in self.mobjects])


class PMFofFunction(VoiceoverScene):
    """Beat: pmf-of-y -- the preimage sum, and the g(x)=x^2 merge picture."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The PMF of Y = g(X)")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        formula = MathTex(
            r"p_Y(y) = \sum_{\{x \,:\, g(x) = y\}} p_X(x)",
            font_size=SECTION, color=ACCENT,
        )
        formula_cap = Text("collect the mass of every x that g sends to y",
                           font_size=CAPTION, color=MUTED)
        formula_grp = VGroup(formula, formula_cap).arrange(DOWN, buff=0.4)
        formula_grp.move_to(DOWN * 0.2)
        fit_to_frame(formula_grp)

        with self.voiceover(
            text="How do we get the PMF of Y from the PMF of X? For each value "
                 "y, we collect the mass of every x that g sends to y. In symbols, "
                 "p-sub-Y of y is the sum of p-sub-X of x over all x with g of x "
                 "equal to y -- exactly the preimage idea from the first video, "
                 "applied one step further."
        ):
            self.play(Write(formula))
            self.play(FadeIn(formula_cap, shift=UP * 0.1))

        self.play(FadeOut(formula_grp))

        # A concrete merge: g(x) = x^2, X uniform on {-1, 0, 1}.
        setup = MathTex(r"g(x) = x^2, \quad X \in \{-1, 0, 1\},"
                        r"\ \ p_X = \tfrac13",
                        font_size=BODY, color=INK).next_to(title, DOWN, buff=0.4)
        fit_to_frame(setup)

        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[0, 0.8, 0.2],
            x_length=8,
            y_length=3.6,
            axis_config={"include_numbers": True, "font_size": 20},
            tips=False,
        ).to_edge(DOWN, buff=0.7)
        fit_to_frame(axes)  # bars built from axes.c2p -> guard first
        x_lab = MathTex("x", font_size=SMALL).next_to(axes.x_axis, RIGHT, buff=0.2)

        def make_bar(x, height_val, color, opacity=0.85, width_ratio=0.5):
            unit_w = axes.x_axis.unit_size
            bottom = axes.c2p(x, 0)
            top = axes.c2p(x, height_val)
            h = max(top[1] - bottom[1], 1e-3)
            rect = Rectangle(
                width=unit_w * width_ratio, height=h,
                fill_color=color, fill_opacity=opacity,
                stroke_width=1, stroke_color=INK,
            )
            rect.move_to(bottom, aligned_edge=DOWN)
            return rect

        # X-PMF: three bars of height 1/3 at x = -1, 0, 1.
        bar_neg = make_bar(-1, 1 / 3, BAR)
        bar_zero = make_bar(0, 1 / 3, BAR)
        bar_pos = make_bar(1, 1 / 3, BAR)
        lbl_third = MathTex(r"\tfrac13", font_size=CAPTION, color=MUTED)
        lbl_third.next_to(bar_zero, UP, buff=0.12)

        with self.voiceover(
            text="Picture it with a small example. Suppose g squares its input, "
                 "and X takes the values minus-one, zero, and one. Then minus-one "
                 "and one both map to one, so their two bars merge -- their masses "
                 "add -- into a single bar of Y at the value one."
        ):
            self.play(FadeIn(setup, shift=DOWN * 0.1))
            self.play(Create(axes), Write(x_lab))
            self.play(LaggedStart(GrowFromEdge(bar_neg, DOWN),
                                  GrowFromEdge(bar_zero, DOWN),
                                  GrowFromEdge(bar_pos, DOWN),
                                  lag_ratio=0.25), run_time=1.2)
            self.play(FadeIn(lbl_third))

        # The merge: bars at -1 and +1 slide to x=1 and stack into height 2/3.
        merged = make_bar(1, 2 / 3, ACCENT)
        lbl_two_third = MathTex(r"\tfrac23", font_size=CAPTION, color=ACCENT)
        lbl_two_third.next_to(merged, UP, buff=0.12)
        y_zero = make_bar(0, 1 / 3, ACCENT)

        with self.voiceover(
            text="Wherever g is many-to-one, bars of X pile up into taller bars "
                 "of Y; and any y that g never produces simply gets zero."
        ):
            self.play(
                Transform(bar_neg, merged.copy()),
                bar_pos.animate.become(merged.copy()),
                FadeOut(lbl_third),
                run_time=1.2,
            )
            self.play(
                FadeIn(merged),
                FadeOut(bar_neg), FadeOut(bar_pos),
                Transform(bar_zero, y_zero),
                run_time=0.8,
            )
            self.play(FadeIn(lbl_two_third))
            result = MathTex(r"p_Y(0) = \tfrac13, \quad p_Y(1) = \tfrac23",
                             font_size=SMALL, color=INK)
            result.next_to(setup, DOWN, buff=0.25)
            fit_to_frame(result)
            self.play(Write(result))

        self.play(*[FadeOut(m) for m in self.mobjects])


class AffineExample(VoiceoverScene):
    """Beat: affine -- Y = aX + b is one-to-one, so nothing merges."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Affine Case")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        define = MathTex(r"Y = aX + b, \quad a \neq 0",
                         font_size=SECTION, color=ACCENT)
        define_cap = Text("one-to-one:  nothing merges",
                          font_size=CAPTION, color=MUTED)
        define_grp = VGroup(define, define_cap).arrange(DOWN, buff=0.4)
        define_grp.move_to(UP * 1.4)
        fit_to_frame(define_grp)

        with self.voiceover(
            text="One case is especially clean. Let Y equal a-X-plus-b, an affine "
                 "function, with a not zero. Because that function is one-to-one, "
                 "no two values of X ever collide -- nothing merges."
        ):
            self.play(Write(define))
            self.play(FadeIn(define_cap, shift=UP * 0.1))

        invert = MathTex(
            r"p_Y(y) = p_X\!\left(\frac{y - b}{a}\right)",
            font_size=SECTION, color=INK,
        )
        invert_cap = Text("each value is just relabeled: shifted and stretched",
                          font_size=CAPTION, color=MUTED)
        invert_grp = VGroup(invert, invert_cap).arrange(DOWN, buff=0.4)
        invert_grp.move_to(DOWN * 1.4)
        fit_to_frame(invert_grp)

        with self.voiceover(
            text="Each value just gets relabeled: the mass that X put on x now "
                 "sits on a-x-plus-b. So the PMF of Y is p-sub-X evaluated at "
                 "y-minus-b over a. The shape of the distribution is untouched -- "
                 "it is only shifted and stretched along the axis."
        ):
            self.play(Write(invert))
            self.play(FadeIn(invert_cap, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class TaxiFare(VoiceoverScene):
    """Beat: taxi -- the worked example, ending in the chapter outro."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Worked Example: Taxi Fare")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        setup = VGroup(
            MathTex(r"X \sim \text{Uniform}\{1, 2, \dots, 10\},"
                    r"\ \ p_X(k) = \tfrac{1}{10}",
                    font_size=BODY, color=INK),
            Text("meter: $2.50 start + $0.40 per fifth-mile  =  $2 per mile",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.6)
        fit_to_frame(setup)

        with self.voiceover(
            text="Let's finish with a worked example. A taxi driver's ride length, "
                 "in miles, is a discrete uniform random variable X on the whole "
                 "numbers one through ten -- each length equally likely, "
                 "probability one-tenth. The meter charges two dollars fifty just "
                 "to start, plus forty cents for every one-fifth of a mile -- "
                 "which is two dollars a mile."
        ):
            self.play(Write(setup[0]))
            self.play(FadeIn(setup[1], shift=UP * 0.1))

        fare = MathTex(r"Y = 2.5 + 2X", font_size=SECTION, color=ACCENT)
        fare_cap = Text("affine:  a = 2,  b = 2.5",
                        font_size=CAPTION, color=MUTED)
        fare_grp = VGroup(fare, fare_cap).arrange(DOWN, buff=0.35)
        fare_grp.next_to(setup, DOWN, buff=0.6)
        fit_to_frame(VGroup(setup, fare_grp))

        with self.voiceover(
            text="So the fare is Y equals two-point-five plus two X -- an affine "
                 "function of the distance, exactly the case we just did."
        ):
            self.play(Write(fare))
            self.play(FadeIn(fare_cap, shift=UP * 0.1))

        self.play(FadeOut(setup), FadeOut(fare_grp))

        # Bar chart of the ten fares, hand-built on a wide Axes.
        fares = [2.5 + 2 * k for k in range(1, 11)]   # 4.5, 6.5, ..., 22.5
        axes = Axes(
            x_range=[0, 24, 4],
            y_range=[0, 0.16, 0.05],
            x_length=11,
            y_length=3.6,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False,
        ).to_edge(DOWN, buff=1.3)
        fit_to_frame(axes)  # bars built from axes.c2p -> guard first
        x_lab = Text("fare ($)", font_size=CAPTION, color=MUTED)
        x_lab.next_to(axes.x_axis, DOWN, buff=0.3).to_edge(RIGHT, buff=1.2)

        unit_w = axes.x_axis.unit_size
        bars = VGroup()
        for f in fares:
            bottom = axes.c2p(f, 0)
            top = axes.c2p(f, 0.1)
            h = max(top[1] - bottom[1], 1e-3)
            rect = Rectangle(
                width=unit_w * 1.4, height=h,
                fill_color=BAR, fill_opacity=0.85,
                stroke_width=1, stroke_color=INK,
            )
            rect.move_to(bottom, aligned_edge=DOWN)
            bars.add(rect)

        pmf_lab = MathTex(r"p_Y(2.5 + 2k) = \tfrac{1}{10}",
                          font_size=SMALL, color=ACCENT)
        pmf_lab.next_to(title, DOWN, buff=0.4)
        chart = VGroup(axes, x_lab, bars, pmf_lab)
        fit_to_frame(chart)

        with self.voiceover(
            text="Since it's one-to-one, the uniform PMF just gets relabeled onto "
                 "the fare values: a one-mile ride costs four dollars fifty, a "
                 "two-mile ride six fifty, and so on up to twenty-two fifty for "
                 "ten miles -- each fare with probability one-tenth. A uniform "
                 "distribution, moved onto a new set of values."
        ):
            self.play(Create(axes), FadeIn(x_lab))
            self.play(Write(pmf_lab))
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.08), run_time=1.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- outro: key idea + bridge to the next chapter. ---
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            MathTex(r"Y = g(X): \quad p_Y(y) = "
                    r"\sum_{\{x \,:\, g(x) = y\}} p_X(x)",
                    font_size=BODY, color=INK),
            VGroup(
                Text("A function of a random variable is a random variable;",
                     font_size=CAPTION, color=MUTED),
                Text("its PMF sums the mass over preimages.",
                     font_size=CAPTION, color=MUTED),
            ).arrange(DOWN, buff=0.15),
        ).arrange(DOWN, buff=0.45)
        fit_to_frame(outro)

        with self.voiceover(
            text="And that is the whole idea: a function of a random variable is a "
                 "random variable, and its PMF comes from summing the mass over "
                 "preimages."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.15), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
