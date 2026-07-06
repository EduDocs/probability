# derived_from: content/35-markov-chebyshev-script.md
# derived_from_sha256: 5b21c8aa470fe976bbe3904b16a7cb4403138600fedbcbf3b141b66270c19729
"""Chapter 10, Video 2 -- The Markov and Chebyshev Inequalities.

Source notes : 35-markov-chebyshev.tex (Important Inequalities intro +
               the Markov and Chebyshev subsections; Chernoff and Jensen
               belong to video 36).
Script        : content/35-markov-chebyshev-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark
segment -- the same pattern as the earlier videos in the series.

Signature visual: the dominating-function picture -- the indicator step
1_{[a,inf)} sitting UNDER the line x/a; taking expectations of both sides
turns the domination into the inequality.

Draft render:
    uv run manim -pql scenes/markov_chebyshev.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from manim import *  # noqa: F401,F403
from manim_voiceover import VoiceoverScene

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
    pr,
    expectation,
    variance,
    section_title,
    intro_card,
    outro_bridge,
    progress_tag,
    fit_to_frame,
    mark_intended_overlap,
    speech_service,
)


def make_speech_service():
    """Voice comes from project.yaml (project.voice); AGEATION_TTS
    is the draft/final switch (render.py sets gtts for -ql)."""
    return speech_service()


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Markov and Chebyshev Inequalities",
            ["Turn one moment into a tail bound:",
             "dominate an indicator, then take expectations."],
            kicker="Chapter 10  ·  Expectations and Bounds",
        )
        tag = progress_tag(2, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  Dominating functions", font_size=BODY, color=INK),
            Text("2.  The Markov inequality", font_size=BODY, color=INK),
            Text("3.  The Chebyshev inequality", font_size=BODY, color=INK),
            Text("4.  The Cantelli inequality", font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        with self.voiceover(
            text="Last video, the moment generating function packaged every "
                 "moment of a random variable into one function. This video "
                 "puts those moments to work: when a probability cannot be "
                 "computed exactly, a single moment can still fence it in."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.6)
        fit_to_frame(outline)

        with self.voiceover(
            text="First, the engine behind every bound in this chapter: a "
                 "function that dominates another has the larger expectation."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="Then the Markov inequality, which turns one mean into a "
                 "tail bound,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="the Chebyshev inequality, a template that mints a whole "
                 "family of bounds,"
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and the Cantelli inequality, where we choose the best "
                 "bound from an entire family."
        ):
            self.play(FadeIn(outline[3], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class WhyBounds(VoiceoverScene):
    """Beat: why-bounds -- tails are hard, expectations are easy, and the
    dominating-function picture that connects them."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Bounds from Expectations")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        target = MathTex(pr(r"X \geq a"), "=", r"?", font_size=BODY)
        target.move_to(LEFT * 3.2 + UP * 1.9)
        unknown = Text("distribution unknown", font_size=CAPTION, color=MUTED)
        unknown.next_to(target, DOWN, buff=0.3)

        with self.voiceover(
            text="Here is a common predicament. We need a tail probability, "
                 "the chance that some quantity exceeds a threshold,"
        ):
            self.play(Write(target), run_time=1.0)

        with self.voiceover(
            text="and the exact value is out of reach: the distribution is "
                 "unknown, or the integral is intractable. But suppose we do "
                 "know one number, the mean."
        ):
            self.play(FadeIn(unknown, shift=UP * 0.2), run_time=0.6)

        e_card = MathTex(expectation("X"), font_size=BODY, color=ACCENT)
        e_card.move_to(RIGHT * 3.2 + UP * 1.9)
        e_note = Text("the one number we know", font_size=CAPTION,
                      color=MUTED)
        e_note.next_to(e_card, DOWN, buff=0.3)

        with self.voiceover(
            text="Remarkably, that one number can fence in the probability, "
                 "and the engine is a simple picture."
        ):
            self.play(Write(e_card), FadeIn(e_note), run_time=0.9)

        # The dominating-function picture (the notes' own figure).
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 4.6, 1],
            x_length=5.6,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        )

        def g_fn(x):
            return 3.0 * np.exp(-0.5 * (x - 2.0) ** 2)

        def h_fn(x):
            return 3.75 * x * np.exp(-0.2 * x * x) + 1.5 * np.exp(-x / 2)

        g_plot = axes.plot(g_fn, x_range=[0, 6], color=INK)
        h_plot = DashedVMobject(
            axes.plot(h_fn, x_range=[0, 6], color=BAR), num_dashes=48)
        g_lab = MathTex(r"g(x)", font_size=SMALL, color=INK)
        # Shifted right clear of the descending h curve (2026-07-05 draft
        # review, 1:29).
        g_lab.next_to(axes.c2p(2.0, g_fn(2.0)), UP + RIGHT, buff=0.15)
        g_lab.shift(RIGHT * 0.6)
        h_lab = MathTex(r"h(x)", font_size=SMALL, color=BAR)
        h_lab.next_to(axes.c2p(1.35, h_fn(1.35)), UP, buff=0.2)
        chart = VGroup(axes, g_plot, h_plot, g_lab, h_lab)
        mark_intended_overlap(
            chart, reason="dominated curve g drawn under h on shared axes")
        fit_to_frame(chart)
        chart.move_to(LEFT * 3.2).to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="Take two nonnegative functions, g below and h above, so "
                 "that g of x is at most h of x for every x."
        ):
            self.play(e_card.animate.set_color(INK), run_time=0.4)
            self.play(Create(axes), run_time=0.7)
            self.play(Create(g_plot), Write(g_lab), run_time=0.8)
            self.play(Create(h_plot), Write(h_lab), run_time=0.8)

        h_area = axes.get_area(axes.plot(h_fn, x_range=[0, 6]),
                               x_range=[0, 6], color=TEAL, opacity=0.20)
        g_area = axes.get_area(axes.plot(g_fn, x_range=[0, 6]),
                               x_range=[0, 6], color=BAR, opacity=0.35)
        mark_intended_overlap(
            chart, h_area, g_area,
            reason="weighted area under g nests inside the area under h")
        ineq = MathTex(expectation("g(X)"), r"\;\leq\;",
                       expectation("h(X)"), font_size=BODY, color=ACCENT)
        fit_to_frame(ineq)
        ineq.move_to(RIGHT * 3.4 + DOWN * 0.4)

        with self.voiceover(
            text="Now weight both by the density of X. The density is "
                 "nonnegative, so at every point the weighted g still sits "
                 "under the weighted h, and integrating preserves the order: "
                 "the expectation of g of X is at most the expectation of h "
                 "of X. Pointwise domination survives the integral."
        ):
            self.play(FadeIn(h_area), run_time=0.8)
            self.play(FadeIn(g_area), run_time=0.8)
            self.play(Write(ineq), run_time=1.0)

        identity = MathTex(pr(r"X \in S"), "=",
                           expectation(r"\mathbf{1}_S(X)"),
                           font_size=BODY, color=ACCENT)
        fit_to_frame(identity)
        identity.move_to(DOWN * 1.4)

        with self.voiceover(
            text="One more ingredient, remembered from earlier chapters: a "
                 "probability is itself an expectation. The probability that "
                 "X lands in a set S is the expectation of the indicator of "
                 "S, the function that is one on S and zero elsewhere."
        ):
            self.play(FadeOut(chart), FadeOut(h_area), FadeOut(g_area),
                      ineq.animate.set_color(INK).move_to(UP * 0.3),
                      run_time=0.8)
            self.play(Write(identity), run_time=1.2)

        strategy = Text("dominate an indicator, then take expectations",
                        font_size=CAPTION, color=MUTED)
        strategy.next_to(identity, DOWN, buff=0.45)

        with self.voiceover(
            text="The strategy is now visible. To bound a probability, sit "
                 "a computable function on top of an indicator step, and "
                 "take expectations of both sides."
        ):
            self.play(FadeIn(strategy, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MarkovInequality(VoiceoverScene):
    """Beat: markov -- the line x/a over the indicator step, and E[X]/a."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Markov Inequality")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        target = MathTex(pr(r"X \geq a"), font_size=BODY)
        target.move_to(LEFT * 3.3 + UP * 2.0)
        cond = MathTex(r"X \geq 0, \quad a > 0",
                       font_size=CAPTION, color=MUTED)
        cond.next_to(target, DOWN, buff=0.25)

        with self.voiceover(
            text="Run the strategy on the right tail. X is nonnegative, a "
                 "is positive, and the target is the probability that X is "
                 "at least a."
        ):
            self.play(Write(target), run_time=0.8)
            self.play(FadeIn(cond, shift=UP * 0.2), run_time=0.5)

        # The signature picture: the step 1_{[a, inf)} under the line x/a.
        a_val = 2.0
        axes = Axes(
            x_range=[0, 4.6, 1],
            y_range=[0, 2.5, 1],
            x_length=5.8,
            y_length=3.3,
            tips=False,
            axis_config={"include_numbers": False},
        )
        step_low = Line(axes.c2p(0, 0), axes.c2p(a_val, 0),
                        color=INK, stroke_width=5)
        step_high = Line(axes.c2p(a_val, 1), axes.c2p(4.5, 1),
                         color=INK, stroke_width=5)
        riser = DashedLine(axes.c2p(a_val, 0), axes.c2p(a_val, 1),
                           color=MUTED, stroke_width=2.5, dash_length=0.1)
        a_lab = MathTex(r"a", font_size=SMALL, color=INK)
        a_lab.next_to(axes.c2p(a_val, 0), DOWN, buff=0.25)
        one_lab = MathTex(r"1", font_size=CAPTION, color=MUTED)
        one_lab.next_to(axes.c2p(0, 1), LEFT, buff=0.15)
        step_lab = MathTex(r"\mathbf{1}_{[a,\infty)}(x)",
                           font_size=SMALL, color=INK)
        step_lab.move_to(axes.c2p(3.5, 0.55))
        chart = VGroup(axes, step_low, step_high, riser,
                       a_lab, one_lab, step_lab)
        mark_intended_overlap(
            chart,
            reason="indicator step, riser, and labels share the axes")
        fit_to_frame(chart)
        chart.move_to(LEFT * 3.3).to_edge(DOWN, buff=0.8)

        with self.voiceover(
            text="Draw the indicator of the interval from a to infinity: "
                 "zero at first, then a step up to one at a."
        ):
            self.play(Create(axes), FadeIn(one_lab), run_time=0.7)
            self.play(Create(step_low), run_time=0.5)
            self.play(Create(riser), Write(a_lab), run_time=0.5)
            self.play(Create(step_high), Write(step_lab), run_time=0.7)

        line_plot = axes.plot(lambda x: x / a_val, x_range=[0, 4.5],
                              color=BAR, stroke_width=4)
        line_lab = MathTex(r"\frac{x}{a}", font_size=SMALL, color=BAR)
        line_lab.next_to(axes.c2p(4.3, 4.3 / a_val), UP + LEFT, buff=0.15)
        pivot = Dot(axes.c2p(a_val, 1), radius=0.07, color=ACCENT)
        mark_intended_overlap(
            chart, line_plot, line_lab, pivot,
            reason="dominating line x/a drawn over the indicator step, "
                   "pivoting at (a, 1)")

        with self.voiceover(
            text="Now lay the straight line x over a on top of it. Below a, "
                 "the line is nonnegative while the step is zero; at a, the "
                 "line reaches exactly one; beyond a, it keeps climbing "
                 "while the step stays flat. Everywhere on the nonnegative "
                 "axis, the line dominates the step."
        ):
            self.play(Create(line_plot), Write(line_lab), run_time=1.2)
            self.play(FadeIn(pivot, scale=2.0), run_time=0.5)

        eq1 = MathTex(expectation(r"\mathbf{1}_{[a,\infty)}(X)"), "=",
                      pr(r"X \geq a"), font_size=SMALL)
        eq2 = MathTex(expectation(r"X/a"), "=",
                      r"\frac{" + expectation("X") + r"}{a}",
                      font_size=SMALL)
        right_col = VGroup(eq1, eq2).arrange(DOWN, buff=0.35)
        right_col.move_to(RIGHT * 3.4 + UP * 1.3)
        fit_to_frame(right_col)

        with self.voiceover(
            text="Take expectations of both sides. The expectation of the "
                 "step is the tail probability itself; the expectation of "
                 "the line is the mean of X divided by a."
        ):
            self.play(pivot.animate.set_color(INK), run_time=0.3)
            self.play(Write(eq1), run_time=0.9)
            self.play(Write(eq2), run_time=0.9)

        markov = MathTex(pr(r"X \geq a"), r"\;\leq\;",
                         r"\frac{" + expectation("X") + r"}{a}",
                         font_size=BODY, color=ACCENT)
        fit_to_frame(markov)
        markov.next_to(right_col, DOWN, buff=0.5)

        with self.voiceover(
            text="That is the Markov inequality: for a nonnegative random "
                 "variable, the probability that X is at least a is at most "
                 "the expectation of X over a. One mean, one tail bound."
        ):
            self.play(Write(markov), run_time=1.2)

        use = MathTex(expectation("X"), r"= 10:\quad",
                      pr(r"X \geq 50"), r"\leq \tfrac{1}{5}",
                      font_size=SMALL)
        fit_to_frame(use)
        use.next_to(markov, DOWN, buff=0.5)

        with self.voiceover(
            text="Put a number on it. A queue holds ten customers on "
                 "average. The chance of finding fifty or more is at most "
                 "ten over fifty, one fifth, no matter how the queue length "
                 "is distributed."
        ):
            self.play(Write(use), run_time=1.1)

        gap = Polygon(
            axes.c2p(0, 0), axes.c2p(a_val, 1), axes.c2p(4.5, 4.5 / a_val),
            axes.c2p(4.5, 1), axes.c2p(a_val, 1), axes.c2p(a_val, 0),
            stroke_width=0, fill_color=ACCENT, fill_opacity=0.18,
        )
        mark_intended_overlap(
            chart, line_plot, gap,
            reason="the slack region fills the gap between line and step")
        gap_note = Text("the gap is the slack in the bound",
                        font_size=CAPTION, color=MUTED)
        gap_note.next_to(use, DOWN, buff=0.4)

        with self.voiceover(
            text="The gap between the line and the step is the price of "
                 "that generality: the bound is often loose, and everything "
                 "that follows works to close the gap."
        ):
            self.play(markov.animate.set_color(INK), run_time=0.3)
            self.play(FadeIn(gap), run_time=0.8)
            self.play(FadeIn(gap_note, shift=UP * 0.2), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ChebyshevInequality(VoiceoverScene):
    """Beat: chebyshev -- the i_S template, the second-moment instance,
    and the variance form that feeds the Law of Large Numbers."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Chebyshev Inequality")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Nothing in that argument was special about the line. Any "
                 "dominating function works, and that observation is worth "
                 "a theorem."
        ):
            self.wait(0.3)

        # The template picture: h over S, the infimum pressing up under it.
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 4, 1],
            x_length=5.6,
            y_length=3.2,
            tips=False,
            axis_config={"include_numbers": False},
        )

        def h_fn(x):
            return 0.5 * (x - 3.0) ** 2 + 1.0

        h_plot = axes.plot(h_fn, x_range=[0.8, 5.2], color=BAR,
                           stroke_width=4)
        h_lab = MathTex(r"h(x)", font_size=SMALL, color=BAR)
        h_lab.next_to(axes.c2p(5.0, h_fn(5.0)), UP + LEFT, buff=0.15)
        s_seg = Line(axes.c2p(2, 0), axes.c2p(4, 0),
                     color=TEAL, stroke_width=7)
        s_lab = MathTex(r"S", font_size=SMALL, color=TEAL)
        s_lab.next_to(axes.c2p(3, 0), DOWN, buff=0.25)
        inf_line = DashedLine(axes.c2p(2, 1), axes.c2p(4, 1),
                              color=MUTED, stroke_width=2.5,
                              dash_length=0.1)
        inf_lab = MathTex(r"i_S", font_size=SMALL, color=INK)
        inf_lab.next_to(axes.c2p(2, 1), LEFT, buff=0.2)
        chart = VGroup(axes, h_plot, h_lab, s_seg, s_lab, inf_line, inf_lab)
        mark_intended_overlap(
            chart,
            reason="set S, curve h, and the infimum line share the axes")
        fit_to_frame(chart)
        chart.move_to(LEFT * 3.3).to_edge(DOWN, buff=0.8)

        inf_def = MathTex(r"i_S = \inf_{x \in S} h(x)", font_size=SMALL)
        inf_def.move_to(RIGHT * 3.4 + UP * 1.8)
        fit_to_frame(inf_def)

        with self.voiceover(
            text="Let h be any nonnegative function and S any set of "
                 "interest, and write i sub S for the infimum of h over S, "
                 "the lowest h ever gets on that set."
        ):
            self.play(Create(axes), run_time=0.6)
            self.play(Create(h_plot), Write(h_lab), run_time=0.8)
            self.play(Create(s_seg), Write(s_lab), run_time=0.6)
            self.play(Create(inf_line), Write(inf_lab),
                      Write(inf_def), run_time=0.9)

        chain = MathTex(
            r"i_S\,\mathbf{1}_S(x) \;\leq\; h(x)\,\mathbf{1}_S(x)"
            r" \;\leq\; h(x)",
            font_size=SMALL)
        chain.next_to(inf_def, DOWN, buff=0.45)
        fit_to_frame(chain)

        with self.voiceover(
            text="Then i sub S times the indicator of S sits under h times "
                 "the indicator, which sits under h itself, at every point."
        ):
            self.play(Write(chain), run_time=1.1)

        template = MathTex(r"i_S\,", pr(r"X \in S"), r"\;\leq\;",
                           expectation("h(X)"),
                           font_size=BODY, color=ACCENT)
        fit_to_frame(template)
        template.next_to(chain, DOWN, buff=0.5)
        family_note = Text("one template, a family of bounds",
                           font_size=CAPTION, color=MUTED)
        family_note.next_to(template, DOWN, buff=0.35)

        with self.voiceover(
            text="Take expectations and the Chebyshev inequality appears: "
                 "i sub S times the probability that X is in S is at most "
                 "the expectation of h of X. When the infimum is positive, "
                 "divide through, and the template mints a bound for every "
                 "choice of h and S."
        ):
            self.play(Write(template), run_time=1.2)
            self.play(FadeIn(family_note, shift=UP * 0.2), run_time=0.6)

        instance = MathTex(r"h(x) = x^2, \quad S = \{x \mid x^2 \geq b^2\}",
                           font_size=SMALL, color=MUTED)
        instance.move_to(LEFT * 3.2 + UP * 1.2)
        fit_to_frame(instance)
        second = MathTex(pr(r"|X| \geq b"), r"\;\leq\;",
                         r"\frac{" + expectation("X^2") + r"}{b^2}",
                         font_size=BODY)
        fit_to_frame(second)
        second.next_to(instance, DOWN, buff=0.5)

        with self.voiceover(
            text="The most famous instance takes h of x equal to x squared, "
                 "and S the set where x squared is at least b squared. The "
                 "infimum is b squared, so the probability that the "
                 "magnitude of X is at least b is at most the second moment "
                 "over b squared."
        ):
            self.play(FadeOut(chart),
                      template.animate.set_color(INK), run_time=0.6)
            self.play(Write(instance), run_time=0.8)
            self.play(Write(second), run_time=1.0)

        var_form = MathTex(pr(r"|X - m| \geq b"), r"\;\leq\;",
                           r"\frac{" + variance("X") + r"}{b^2}",
                           font_size=BODY, color=ACCENT)
        fit_to_frame(var_form)
        var_form.next_to(second, DOWN, buff=0.55)

        with self.voiceover(
            text="Apply that to the centered variable, X minus its mean, "
                 "and the second moment becomes the variance: the "
                 "probability that X strays from its mean by b or more is "
                 "at most the variance over b squared. This is the form "
                 "everyone calls Chebyshev, and it is what variance is for."
        ):
            self.play(Write(var_form), run_time=1.3)

        lln = VGroup(
            Text("Chebyshev on an empirical average:",
                 font_size=CAPTION, color=MUTED),
            Text("→ the Law of Large Numbers",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.15)
        lln.next_to(var_form, DOWN, buff=0.5)
        fit_to_frame(lln)

        with self.voiceover(
            text="Hold on to it: run this bound on an empirical average, "
                 "and out comes the Law of Large Numbers, coming soon."
        ):
            self.play(FadeIn(lln, shift=UP * 0.2), run_time=0.8)

        self.play(*[FadeOut(m) for m in self.mobjects])


class CantelliBound(VoiceoverScene):
    """Beat: cantelli -- a family of parabolic dominations, optimized
    over b; rehearsal for the Chernoff bound."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Cantelli Inequality")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # Left column rides slightly high so the bottom caption lane clears
        # the 0.8 bottom margin (2026-07-05 draft review, 6:50).
        target = MathTex(pr(r"X - m \geq a"), font_size=BODY)
        target.move_to(LEFT * 3.3 + UP * 2.2)
        known = MathTex(r"\text{known: } m \text{ and } \sigma^2",
                        font_size=CAPTION, color=MUTED)
        known.next_to(target, DOWN, buff=0.25)

        with self.voiceover(
            text="One worked bound to finish, and a preview of a powerful "
                 "move. Suppose we know the mean m and the variance sigma "
                 "squared, and we want a one-sided tail: the probability "
                 "that X exceeds its mean by at least a."
        ):
            self.play(Write(target), run_time=0.9)
            self.play(FadeIn(known, shift=UP * 0.2), run_time=0.5)

        center_eq = MathTex(r"Y = X - m, \quad " + expectation("Y") + r" = 0",
                            font_size=SMALL)
        center_eq.next_to(known, DOWN, buff=0.40)
        fit_to_frame(center_eq)

        with self.voiceover(
            text="Center the variable: Y equals X minus m has mean zero and "
                 "the same variance."
        ):
            self.play(Write(center_eq), run_time=0.9)

        fam1 = MathTex(r"h(y) = (y + b)^2, \quad b > 0", font_size=SMALL)
        # a > 0 made explicit: the infimum step and the optimum b* = sigma^2/a
        # both need it, and the notes' derivation states it (2026-07-05 draft
        # review, 6:50).
        fam2 = MathTex(r"i_S = (a + b)^2, \quad a > 0", font_size=SMALL)
        fam3 = MathTex(pr(r"Y \geq a"), r"\;\leq\;",
                       r"\frac{\sigma^2 + b^2}{(a+b)^2}",
                       font_size=SMALL)
        family = VGroup(fam1, fam2, fam3).arrange(
            DOWN, buff=0.35, aligned_edge=LEFT)
        family.move_to(LEFT * 3.3 + DOWN * 0.48)
        fit_to_frame(family)

        with self.voiceover(
            text="Now dominate with a whole family of parabolas: h of y "
                 "equals y plus b, squared, one function for every positive "
                 "b. Over the set where y is at least a, the infimum is a "
                 "plus b, squared; and the expectation of Y plus b, "
                 "squared, is sigma squared plus b squared. Chebyshev hands "
                 "us a bound for every b."
        ):
            self.play(Write(fam1), run_time=0.9)
            self.play(Write(fam2), run_time=0.8)
            self.play(Write(fam3), run_time=1.0)

        # Cantelli's dial: the bound against b (hardcoded sigma = 1, a = 1),
        # a marker sliding to the minimum at b = sigma^2/a = 1.
        axes = Axes(
            x_range=[0, 3.5, 1],
            y_range=[0, 1.2, 0.5],
            x_length=4.8,
            y_length=2.9,
            tips=False,
            axis_config={"include_numbers": False},
        )

        def bound_fn(b):
            return (1.0 + b * b) / ((1.0 + b) ** 2)

        curve = axes.plot(bound_fn, x_range=[0.0, 3.3], color=BAR,
                          stroke_width=4)
        b_lab = MathTex(r"b", font_size=CAPTION, color=MUTED)
        b_lab.next_to(axes.c2p(3.5, 0), DOWN + RIGHT, buff=0.2)
        y_lab = MathTex(r"\frac{\sigma^2 + b^2}{(a+b)^2}",
                        font_size=CAPTION, color=MUTED)
        y_lab.next_to(axes.c2p(0, 1.2), UP + RIGHT, buff=0.2)
        chart = VGroup(axes, curve, b_lab, y_lab)
        mark_intended_overlap(
            chart, reason="bound curve and its labels share the axes")
        fit_to_frame(chart)
        chart.move_to(RIGHT * 3.4 + DOWN * 0.35)

        dot = Dot(axes.c2p(0.15, bound_fn(0.15)), radius=0.07, color=ACCENT)
        path_out = axes.plot(bound_fn, x_range=[0.15, 2.6])
        path_back = axes.plot(bound_fn, x_range=[1.0, 2.6])
        path_back.reverse_points()
        drop = DashedLine(axes.c2p(1.0, bound_fn(1.0)), axes.c2p(1.0, 0),
                          color=MUTED, stroke_width=2.5, dash_length=0.1)
        bstar = MathTex(r"b^\ast = \sigma^2 / a",
                        font_size=SMALL, color=ACCENT)
        bstar.next_to(axes.c2p(1.0, 0), DOWN, buff=0.3)
        mark_intended_overlap(
            chart, dot, drop, bstar,
            reason="marker, drop line, and label ride the bound curve")

        with self.voiceover(
            text="A family of bounds means a choice: take the best one. "
                 "Slide b along the curve of bounds; it dips, bottoms out, "
                 "and rises again. Calculus finds the minimum at b equal to "
                 "sigma squared over a."
        ):
            self.play(Create(axes), FadeIn(b_lab), FadeIn(y_lab),
                      run_time=0.7)
            self.play(Create(curve), FadeIn(dot, scale=1.6), run_time=0.9)
            self.play(MoveAlongPath(dot, path_out), run_time=1.2)
            self.play(MoveAlongPath(dot, path_back), run_time=0.9)
            self.play(Create(drop), Write(bstar), run_time=0.8)

        cantelli = MathTex(pr(r"X - m \geq a"), r"\;\leq\;",
                           r"\frac{\sigma^2}{a^2 + \sigma^2}",
                           font_size=BODY, color=ACCENT)
        fit_to_frame(cantelli)
        cantelli.next_to(family, DOWN, buff=0.35)

        with self.voiceover(
            text="Substitute back, and the algebra collapses to the "
                 "Cantelli inequality: the one-sided tail is at most sigma "
                 "squared over a squared plus sigma squared."
        ):
            self.play(bstar.animate.set_color(INK), run_time=0.3)
            self.play(Write(cantelli), run_time=1.2)

        rehearse = Text("next: an exponential family, optimized with the MGF",
                        font_size=CAPTION, color=MUTED)
        # Centered bottom caption lane, >= 0.8 off the bottom edge
        # (2026-07-05 draft review, 6:50).
        rehearse.move_to(DOWN * 3.0)
        fit_to_frame(rehearse)

        with self.voiceover(
            text="Remember the move: dominate with a family, then optimize "
                 "over it. Next video, the family is exponential, the "
                 "pocket tool is the moment generating function, and the "
                 "result is the Chernoff bound."
        ):
            self.play(FadeIn(rehearse, shift=UP * 0.2), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["Probabilities are expectations of indicators;",
             "dominating an indicator turns one moment into a tail bound."],
            next_title="The Chernoff Bound and Jensen's Inequality",
        )

        with self.voiceover(
            text="The key idea of this video: probabilities are "
                 "expectations of indicators, so dominating an indicator "
                 "turns one moment into a tail bound."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(0.5)
        self.play(FadeOut(outro))
