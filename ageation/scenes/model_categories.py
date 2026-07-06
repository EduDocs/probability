# derived_from: content/09-model-categories-script.md
# derived_from_sha256: a418b6077ac03f7f5141b56ba9f662b1e8798ff9244dd0b757e9b824d2e5ef8e
"""Chapter 3, Video 3 -- Categories of Probability Models (narrated with manim-voiceover).

Source notes : ../chapters/probability_models.tex  (3.2.1 Finite Sample Spaces,
               3.2.2 Countably Infinite Models, 3.2.3 Uncountably Infinite Models)
Script        : content/09-model-categories-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, timed by ``tracker.duration`` -- the
same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/model_categories.py ChapterOverview
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
    make_pmf_chart,
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

def ball(label, color, radius=0.32, font_size=22):
    """A colored disk with a dark centered label (see Chapter 1 contrast note)."""
    dot = Dot(radius=radius, color=color).set_fill(color, opacity=0.95)
    dot.set_stroke(INK, width=1.5)
    txt = MathTex(label, font_size=font_size, color=BLACK)
    return VGroup(dot, txt.move_to(dot.get_center()))


def die_face(n, size=0.95, color=INK, fill=None):
    """A rounded square die face showing n pips in the standard layout."""
    sq = RoundedRectangle(corner_radius=0.12, width=size, height=size)
    sq.set_stroke(color, 2.5)
    if fill is not None:
        sq.set_fill(fill, opacity=0.30)
    o = size * 0.26
    P = {
        "c": [0, 0, 0],
        "tl": [-o, o, 0], "tr": [o, o, 0],
        "bl": [-o, -o, 0], "br": [o, -o, 0],
        "ml": [-o, 0, 0], "mr": [o, 0, 0],
    }
    layout = {
        1: ["c"], 2: ["tl", "br"], 3: ["tl", "c", "br"],
        4: ["tl", "tr", "bl", "br"], 5: ["tl", "tr", "c", "bl", "br"],
        6: ["tl", "tr", "ml", "mr", "bl", "br"],
    }
    pips = VGroup(*[Dot(point=P[k], radius=size * 0.07, color=color)
                    for k in layout[n]])
    return VGroup(sq, pips)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of the axioms + the three families outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Categories of Probability Models",
            "Classify models by the size of the sample space.",
            kicker="Chapter 3  ·  Probability Models",
        )
        fit_to_frame(intro)
        tag = progress_tag(3, 4).to_corner(DR, buff=0.4)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="Probability now rests on three axioms — "
                 "nonnegativity, normalization, and additivity. Those axioms work "
                 "on any sample space."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(tag), run_time=0.4)

        with self.voiceover(
            text="But how you actually pin down a probability law depends on how "
                 "big that sample space is."
        ):
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)

        self.play(intro.animate.to_edge(UP), run_time=0.8)

        items = VGroup(
            Text("1.  Finite sample spaces", font_size=BODY),
            Text("2.  Countably infinite models", font_size=BODY),
            Text("3.  Uncountably infinite models", font_size=BODY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        items.next_to(intro, DOWN, buff=0.8)
        fit_to_frame(items)

        clauses = [
            "In this video we sort probabilistic models into three families. "
            "First, finite sample spaces;",
            "then countably infinite ones;",
            "and finally uncountably infinite sample spaces, where, as we will "
            "see, weighting individual outcomes breaks down, and we measure "
            "probability by integration instead.",
        ]
        for clause, item in zip(clauses, items):
            with self.voiceover(text=clause):
                self.play(FadeIn(item, shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class FiniteModels(VoiceoverScene):
    """Beat: finite -- equally-likely Pr(A)=|A|/|Omega|, the die, the caution."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Finite Sample Spaces")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        general = MathTex(
            r"\Pr(A) = \sum_{i=1}^{k} \Pr(x_i)"
            r" \quad\text{where}\quad A = \{\, x_1, x_2, \ldots, x_k \,\}",
            font_size=BODY, color=INK,
        ).next_to(title, DOWN, buff=0.9)
        fit_to_frame(general)
        with self.voiceover(
            text="Start with the simplest family: a finite sample space. When "
                 "Omega has finitely many outcomes, a probability law is "
                 "completely determined by the probabilities of those individual "
                 "outcomes: the probability of an event A is just the sum of the "
                 "probabilities of the outcomes it contains."
        ):
            self.play(Write(general))

        self.wait(0.6)

        eq_label = Text("For equally likely outcomes,", font_size=SMALL, color=INK)
        eq_label.next_to(general, DOWN, buff=0.7)
        equally = MathTex(
            r"\Pr(A) = \frac{|A|}{|\Omega|}",
            font_size=TITLE, color=ACCENT,
        ).next_to(eq_label, DOWN, buff=0.4)
        fit_to_frame(VGroup(eq_label, equally))
        with self.voiceover(
            text="There is one especially clean case — the equally-likely model. "
                 "For equally likely outcomes, each of the n outcomes carries "
                 "probability one over n, and the probability of an event A is just "
                 "the size of A divided by the size of Omega."
        ):
            self.play(FadeIn(eq_label, shift=UP * 0.1))
            self.play(Write(equally))

        # Transition: the general statement and its label fade; the
        # equally-likely formula rises to the top slot.
        self.play(
            FadeOut(general), FadeOut(eq_label),
            equally.animate.scale(0.58).next_to(title, DOWN, buff=0.5),
        )

        primes = {2, 3, 5}
        faces = VGroup(*[die_face(n) for n in range(1, 7)])
        faces.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.3)
        fit_to_frame(faces)

        with self.voiceover(
            text="Take a fair die. Six faces, each with probability one-sixth."
        ):
            self.play(LaggedStartMap(FadeIn, faces, lag_ratio=0.12), run_time=1.8)
            one_sixth = MathTex(r"\Pr(\text{a face}) = \tfrac{1}{6}",
                                font_size=BODY, color=INK)
            one_sixth.next_to(faces, DOWN, buff=0.7)
            fit_to_frame(one_sixth)
            self.play(Write(one_sixth))

        with self.voiceover(
            text="To find the probability of an event, we count. The event roll a "
                 "prime is the faces two, three, and five — three favorable "
                 "outcomes out of six — so its probability is three over six, one "
                 "half. Favorable over total, exactly the counting model from "
                 "Chapter two, now named."
        ):
            self.play(*[faces[n - 1][0].animate.set_fill(ACCENT, opacity=0.3)
                        for n in primes])
            count = MathTex(r"\Pr(\{\, 2, 3, 5 \,\}) = \frac{3}{6} = \frac{1}{2}",
                            font_size=BODY, color=ACCENT)
            count.move_to(one_sixth)
            fit_to_frame(count)
            self.play(ReplacementTransform(one_sixth, count))

        self.play(FadeOut(faces), FadeOut(count), FadeOut(equally))

        headline = VGroup(
            Text("Equal likelihood is an assumption,", font_size=BODY, color=INK),
            Text("not a law of nature.", font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.14)
        examples = VGroup(
            Text("For a loaded die, a biased coin, the sum of two dice,",
                 font_size=CAPTION, color=MUTED),
            Text("outcomes need not be equally likely.",
                 font_size=CAPTION, color=MUTED),
        ).arrange(DOWN, buff=0.14)
        misconception = Text("misconception: the outcome approach",
                             font_size=CAPTION, color=MAROON)
        caution = VGroup(headline, examples, misconception).arrange(DOWN, buff=0.45)
        caution.move_to(DOWN * 0.2)
        fit_to_frame(caution)
        with self.voiceover(
            text="One warning. Equal likelihood is a modeling assumption, not a "
                 "law of nature. A loaded die, a biased coin, the sum of two dice "
                 "— none of these have equally likely outcomes. Assuming they do "
                 "is a common misconception called the outcome approach. Use the "
                 "equally-likely model only when a genuine symmetry of the "
                 "experiment earns it."
        ):
            # Staged progression: each sentence appears in turn.
            self.play(FadeIn(headline[0], shift=DOWN * 0.2))
            self.play(FadeIn(headline[1], shift=UP * 0.1))
            self.play(FadeIn(examples, shift=UP * 0.15))
            self.play(FadeIn(misconception, shift=UP * 0.15))

        self.play(*[FadeOut(m) for m in self.mobjects])


class CountablyInfiniteModels(VoiceoverScene):
    """Beat: countable -- listable Omega, coin-until-heads, 2^-k bars, Pr(even)."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Countably Infinite Models")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        listable = MathTex(r"\Omega = \{\, 1, 2, 3, \dots \,\}",
                           font_size=SECTION, color=INK).next_to(title, DOWN, buff=0.8)
        fit_to_frame(listable)
        with self.voiceover(
            text="Now let the sample space be infinite — but countably so. A "
                 "set is countable when its elements can be lined up in a "
                 "sequence, s-one, s-two, s-three, and on; formally, it has the "
                 "same cardinality as some subset of the natural numbers. Even "
                 "though there are infinitely many outcomes, we can still specify "
                 "the law one outcome at a time, by assigning each a weight — as "
                 "long as those weights sum to one."
        ):
            self.play(Write(listable))

        coin = Text("toss a fair coin until the first heads — record the toss number",
                    font_size=CAPTION, color=MUTED).next_to(listable, DOWN, buff=0.5)
        fit_to_frame(coin)
        with self.voiceover(
            text="The classic example: toss a fair coin repeatedly until the first "
                 "heads, and record how many tosses it took. The sample space is "
                 "the positive integers, one, two, three, and so on — a countably "
                 "infinite set."
        ):
            self.play(FadeIn(coin, shift=DOWN * 0.15))

        self.play(FadeOut(listable), FadeOut(coin))

        # Decaying geometric bars: Pr(k) = 2^-k for k = 1, 2, ... (PMF look).
        vals = [0.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]
        chart, bars = make_pmf_chart(
            vals, x_max=7, y_max=0.6,
            x_label="k", y_label=r"\Pr(k)=2^{-k}",
        )
        chart.next_to(title, DOWN, buff=0.6).shift(DOWN * 0.5)
        fit_to_frame(chart)
        with self.voiceover(
            text="The probability that the first heads lands on toss k is two to "
                 "the minus k: a half, a quarter, an eighth, a sixteenth, each bar "
                 "half the height of the one before."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]))
            self.play(LaggedStartMap(GrowFromEdge, bars,
                                     edge=DOWN, lag_ratio=0.2), run_time=2.0)

        # Float the running total into the empty top-right, clear of the bars
        # (which are tall on the left and decay to the right).
        sum_eq = MathTex(r"\sum_{k=1}^{\infty} 2^{-k} = 1",
                         font_size=BODY, color=ACCENT)
        sum_eq.move_to(chart[0].get_corner(UR) + np.array([-1.5, -0.5, 0]))
        fit_to_frame(sum_eq)
        with self.voiceover(
            text="Add up that whole infinite sequence of weights and it comes to "
                 "exactly one, just as the axioms demand — the masses fill the bar."
        ):
            self.play(Write(sum_eq))

        with self.voiceover(
            text="And we can ask real questions. What is the probability that the "
                 "number of tosses is even? Add the even-indexed weights: one "
                 "quarter, plus one sixteenth, plus one sixty-fourth, and on — a "
                 "geometric series that sums to one third. An infinite "
                 "computation, made finite by the structure of the model."
        ):
            # Even-k bars are at k = 2, 4, 6 -> bars[1], bars[3], bars[5].
            self.play(*[bars[i].animate.set_fill(ACCENT, opacity=0.9)
                        for i in (1, 3, 5)])
            even_eq = MathTex(
                r"\Pr(\text{even}) = \tfrac{1}{4} + \tfrac{1}{16} + \cdots "
                r"= \tfrac{1}{3}",
                font_size=SMALL, color=ACCENT,
            ).move_to(sum_eq)
            fit_to_frame(even_eq)
            self.play(ReplacementTransform(sum_eq, even_eq))

        self.play(*[FadeOut(m) for m in self.mobjects])


class UncountableModels(VoiceoverScene):
    """Beat: uncountable -- [0,1] by length, points = 0, the wheel; outro/bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Uncountably Infinite Models")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        nl = NumberLine(
            x_range=[0, 1, 0.25], length=9, include_numbers=True,
            font_size=24,
            decimal_number_config={"num_decimal_places": 2},
            color=INK,
        ).move_to(UP * 0.6)
        fit_to_frame(nl)
        seg_lab = MathTex(r"[\,0, 1\,]", font_size=SMALL, color=MUTED)
        # Park the interval label up under the title so the point-probability
        # and length equations below have clear room (no overlap above the line).
        seg_lab.next_to(title, DOWN, buff=0.5)

        with self.voiceover(
            text="The third family is the strange one: an uncountably infinite "
                 "sample space. Take the unit interval — every real number between "
                 "zero and one. There are so many outcomes here that most subsets "
                 "cannot be written as a finite or even countable list, so the "
                 "trick of summing individual outcome-probabilities simply fails."
        ):
            self.play(Create(nl), FadeIn(seg_lab))

        # A single point has probability zero.
        pt = Dot(nl.number_to_point(0.5), radius=0.06, color=ACCENT)
        pt_lab = MathTex(r"\Pr(\{x\}) = 0", font_size=SMALL, color=ACCENT)
        pt_lab.next_to(pt, UP, buff=0.35)
        with self.voiceover(
            text="In fact, on a continuum almost every single point carries "
                 "probability zero — there are far too many of them for each to "
                 "hold positive mass. A mixed law can place a lump on a few "
                 "isolated points, but a purely continuous law spreads its mass "
                 "out, leaving every single point with none."
        ):
            self.play(FadeIn(pt, scale=1.5), Write(pt_lab))

        self.play(FadeOut(pt), FadeOut(pt_lab))

        # Shade a sub-interval [a, b]; probability = length b - a.
        a, b = 0.3, 0.75
        pa = nl.number_to_point(a)
        pb = nl.number_to_point(b)
        band = Rectangle(width=pb[0] - pa[0], height=0.55,
                         fill_color=ACCENT, fill_opacity=0.35, stroke_width=0)
        band.move_to((pa + pb) / 2)
        brace = Brace(band, DOWN, color=MUTED)
        brace_lab = brace.get_tex(r"b - a")
        length_uniform = MathTex(
            r"\text{uniform law:}\ \ \Pr\big((a,b)\big) = b - a",
            font_size=SMALL, color=ACCENT)
        length_general = MathTex(
            r"\text{in general:}\ \ \Pr\big((a,b)\big) = \int_a^b f(x)\, dx",
            font_size=SMALL, color=INK)
        length_eqs = VGroup(length_uniform, length_general)
        length_eqs.arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(DOWN, buff=1.0)
        fit_to_frame(length_eqs)
        with self.voiceover(
            text="So we specify the law a different way. For the uniform law on "
                 "this interval, the probability of landing between a and b is just "
                 "its length, b minus a. A general continuous law replaces length "
                 "with the area under a density — an integral — and length is "
                 "simply the flat-density case. From there the third axiom extends "
                 "this to any countable union of disjoint intervals by adding their "
                 "probabilities."
        ):
            self.play(FadeIn(band), GrowFromCenter(brace), Write(brace_lab))
            self.play(Write(length_uniform))
            self.play(Write(length_general))

        self.play(FadeOut(nl), FadeOut(seg_lab), FadeOut(band), FadeOut(brace),
                  FadeOut(brace_lab), FadeOut(length_eqs))

        # The wheel of serendipity.
        wheel = Circle(radius=1.7, color=INK).set_stroke(INK, 3)
        wheel.move_to(LEFT * 2.6 + DOWN * 0.3)
        C = wheel.get_center()
        hub = Dot(C, radius=0.06, color=INK)
        sector = Sector(radius=1.7, start_angle=0, angle=PI / 2,
                        arc_center=C, color=ACCENT,
                        fill_opacity=0.4, stroke_width=0)
        ang = 50 * DEGREES
        tip = C + 1.7 * np.array([np.cos(ang), np.sin(ang), 0])
        pointer = Arrow(C, tip, buff=0, color=INK, stroke_width=5)
        wheel_lab = Text("wheel of serendipity", font_size=CAPTION, color=MUTED)
        wheel_lab.next_to(wheel, DOWN, buff=0.4)
        omega_wheel = MathTex(r"\Omega = [\,0, 2\pi)", font_size=SMALL, color=INK)
        omega_wheel.next_to(wheel, UP, buff=0.4)

        with self.voiceover(
            text="Here is the idea in action: the wheel of serendipity. Spin a "
                 "pointer on a circle; the outcome is the angle where it stops, "
                 "uniform on zero to two pi — an uncountable sample space."
        ):
            self.play(Create(wheel), FadeIn(hub))
            self.play(GrowArrow(pointer), Write(omega_wheel), FadeIn(wheel_lab))
            self.play(Rotate(pointer, angle=2 * PI, about_point=C), run_time=1.4)

        arc_eq = VGroup(
            MathTex(r"\Pr(\text{arc}) = \dfrac{\text{arc length}}{2\pi}",
                    font_size=BODY, color=ACCENT),
            MathTex(r"\Pr\!\left(\left[0, \tfrac{\pi}{2}\right)\right) = "
                    r"\dfrac{\pi/2}{2\pi} = \tfrac{1}{4}",
                    font_size=BODY, color=INK),
        ).arrange(DOWN, buff=0.5)
        arc_eq.next_to(wheel, RIGHT, buff=1.0)
        fit_to_frame(arc_eq)
        with self.voiceover(
            text="The probability of landing in any arc is the length of that arc "
                 "divided by two pi. Land in the first quadrant, an arc of length "
                 "pi over two? That is one quarter. Probability has become "
                 "geometry: an arc over the whole circumference."
        ):
            self.play(FadeIn(sector))
            self.play(Write(arc_eq[0]))
            self.play(Write(arc_eq[1]))

        self.play(*[FadeOut(m) for m in self.mobjects])

        # --- Centred two-line key idea + bridge (inline, not outro_bridge) ---
        key_idea = VGroup(
            VGroup(
                Text("How you specify a probability law depends on",
                     font_size=BODY, color=INK),
                Text("the size of the sample space.", font_size=BODY, color=INK),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                Text("Weight outcomes when finite or countable;",
                     font_size=BODY, color=INK),
                Text("integrate a density when uncountable.",
                     font_size=BODY, color=INK),
            ).arrange(DOWN, buff=0.12),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(key_idea)
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            key_idea,
            Text("Coming up:  Continuity of Probability, and a Measure-Theory View",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)
        with self.voiceover(
            text="So the family of a model is set by the size of its sample space: "
                 "finite and countable models weight individual outcomes, while "
                 "uncountable models assign probability by integration — by length, "
                 "in the uniform case. That closes the core of Chapter three. Two "
                 "topics remain — the "
                 "continuity of probability, and the measure-theory that puts all "
                 "of this on a rigorous footing."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.2)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(outro))
