# derived_from: content/34-mgfs-script.md
# derived_from_sha256: a34317995a3589ac31dbbfbad0e3fe4f4f093a9cf83f3360dbc7102822a75af6
"""Chapter 10, Video 1 -- Moment Generating Functions.

Source notes : expectations_and_bounds.tex (section "Moment Generating
               Functions" only) -- the definition, moments by
               differentiation, the exponential and Gaussian transforms,
               and the affine rule.
Script        : content/34-mgfs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per authoring bookmark segment
-- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/mgfs.py ChapterOverview
Final render: `make video PROJECT=...` reads the voice from project.yaml.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
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
    """Voice comes from project.yaml (project.voice) via _style.speech_service.

    Drafts are free: tools/render.py exports AGEATION_TTS=gtts for -ql, and
    the env var beats the configured provider. Finals read the per-project
    voice (nova for this series).
    """
    return speech_service()


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card + outline revealed clause by clause."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Moment Generating Functions",
            ["Package every moment into one function:",
             "compute one transform, then differentiate."],
            kicker="Chapter 10  ·  Expectations and Bounds",
        )
        tag = progress_tag(1, 3).to_corner(DR, buff=0.4)

        outline = VGroup(
            Text("1.  The definition: one expectation, one dial",
                 font_size=BODY, color=INK),
            Text("2.  Moments by differentiation", font_size=BODY, color=INK),
            Text("3.  Two worked transforms: exponential, Gaussian",
                 font_size=BODY, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        with self.voiceover(
            text="Last video closed the chapter on derived distributions "
                 "with a sampler: push uniform numbers through the inverse "
                 "CDF and any distribution you want comes out. This chapter "
                 "puts expectations to a new use, turning them into bounds "
                 "on probabilities — and it opens by forging the tool the "
                 "sharpest bound will run on."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

        self.wait(0.5)

        outline.next_to(intro, DOWN, buff=0.7)
        fit_to_frame(outline)

        with self.voiceover(
            text="In this video we meet the moment generating function: "
                 "one expectation with a dial."
        ):
            self.play(FadeIn(outline[0], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="We differentiate it and watch every moment fall out,"
        ):
            self.play(FadeIn(outline[1], shift=RIGHT * 0.4), run_time=0.6)

        with self.voiceover(
            text="and we work the transform for two densities we know "
                 "well: the exponential and the Gaussian."
        ):
            self.play(FadeIn(outline[2], shift=RIGHT * 0.4), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MGFDefinition(VoiceoverScene):
    """Beat: mgf-definition -- the definition, the probe, the OGF kinship."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Moment Generating Function")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        defn = MathTex(
            r"M_X(s)", "=", expectation(r"e^{sX}"),
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.5)
        fit_to_frame(defn)

        with self.voiceover(
            text="Here is the definition. The moment generating function "
                 "of a random variable X is the expected value of e to the "
                 "s X."
        ):
            self.play(Write(defn), run_time=1.2)
            self.play(defn[0].animate.set_color(ACCENT), run_time=0.5)

        dial_note = Text("one number per dial setting",
                         font_size=CAPTION, color=MUTED)
        dial_note.next_to(defn, DOWN, buff=0.3)

        with self.voiceover(
            text="Read it as a probe. The number s is a dial: fix a "
                 "setting, and the expectation returns a single number. "
                 "Sweep the dial, and you trace out an entire function of "
                 "s that encodes the distribution of X."
        ):
            self.play(FadeIn(dial_note, shift=UP * 0.2), run_time=0.7)

        integral = MathTex(
            r"M_X(s) = \int_{-\infty}^{\infty} f_X(x)\, e^{sx}\, dx",
            font_size=BODY,
        ).next_to(dial_note, DOWN, buff=0.4)
        fit_to_frame(integral)

        # The probe picture: a bell density with the tilting weight e^{sx}.
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.9, 0.5],
            x_length=6.5,
            y_length=2.2,
            tips=False,
        )
        bell = axes.plot(lambda x: 1.5 * np.exp(-x * x / 2), color=BAR)
        weight = axes.plot(lambda x: 0.4 * np.exp(0.55 * x),
                           x_range=[-3, 2.8], color=ACCENT)
        flab = MathTex(r"f_X", font_size=CAPTION, color=BAR)
        wlab = MathTex(r"e^{sx}", font_size=CAPTION, color=ACCENT)
        chart = VGroup(axes, bell, weight, flab, wlab)
        chart.to_edge(DOWN, buff=0.8)
        flab.next_to(axes.c2p(-0.9, 1.1), UP + LEFT, buff=0.1)
        wlab.next_to(axes.c2p(2.55, 1.55), UP + LEFT, buff=0.1)
        mark_intended_overlap(
            axes, bell, weight, flab, wlab,
            reason="density and weight curves share one chart")
        fit_to_frame(chart)

        with self.voiceover(
            text="For a continuous random variable, the expectation is an "
                 "integral: the density of X, weighted by e to the s x, "
                 "integrated over the whole line. At s equals zero the "
                 "weight is flat and the integral is exactly one. Tilt s "
                 "positive, and the weight favors the large values of x — "
                 "the transform feels the right tail."
        ):
            self.play(defn[0].animate.set_color(INK),
                      Write(integral), run_time=1.2)
            self.play(Create(axes), run_time=0.7)
            self.play(Create(bell), FadeIn(flab), run_time=0.8)
            self.play(Create(weight), FadeIn(wlab), run_time=0.9)

        laplace = Text("a variant of the Laplace transform",
                       font_size=CAPTION, color=MUTED)
        laplace.next_to(integral, DOWN, buff=0.3)

        with self.voiceover(
            text="If you have met the Laplace transform in a circuits or "
                 "signals course, you have seen this integral before. The "
                 "moment generating function is a variant of it, and it "
                 "strikes the same bargain: hard operations in one domain "
                 "become easy operations in the transform domain."
        ):
            self.play(weight.animate.set_color(MUTED),
                      wlab.animate.set_color(MUTED), run_time=0.5)
            self.play(FadeIn(laplace, shift=UP * 0.2), run_time=0.7)

        ogf = MathTex(
            r"M_X(s)", "=", r"\sum_{k} e^{sk}\, p_X(k)", "=", r"G_X(e^s)",
            font_size=BODY,
        ).move_to(DOWN * 1.7)
        fit_to_frame(ogf)
        # (2026-07-04 draft review, 2:00) No video numbers on screen or in
        # voice — refer to the concept instead.
        ogf_note = Text("the ordinary generating function, in new coordinates",
                        font_size=CAPTION, color=MUTED)
        ogf_note.next_to(ogf, DOWN, buff=0.35)

        with self.voiceover(
            text="The definition covers discrete random variables too. For "
                 "an integer-valued X, the expectation is a sum: e to the "
                 "s k, times the mass at k, over all values k. That is "
                 "exactly the ordinary generating function from when sums "
                 "became products for discrete variables, evaluated at z "
                 "equals e to the s. Same machine, new "
                 "coordinates — and as a party trick, it grinds out the "
                 "mean of a discrete uniform with two rounds of l'Hopital's "
                 "rule and no special sums."
        ):
            self.play(FadeOut(chart), run_time=0.5)
            self.play(Write(ogf), run_time=1.2)
            self.play(ogf[4].animate.set_color(ACCENT),
                      FadeIn(ogf_note), run_time=0.7)

        self.play(*[FadeOut(m) for m in self.mobjects])


class MomentsFromDerivatives(VoiceoverScene):
    """Beat: moments-by-differentiation -- the derivative cascade."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Moments by Differentiation")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        line = MathTex(
            r"\frac{d^n}{ds^n} M_X(s) \Big|_{s=0}",
            "=",
            r"\mathrm{E}\left[ \frac{d^n}{ds^n}\, e^{sX} \right] "
            r"\bigg|_{s=0}",
            font_size=BODY,
        ).next_to(title, DOWN, buff=0.4)
        fit_to_frame(line)

        with self.voiceover(
            text="Now the name earns itself. Suppose the transform exists "
                 "on an open interval around s equals zero, and "
                 "differentiate it n times."
        ):
            self.play(Write(line[0]), run_time=1.0)

        with self.voiceover(
            text="The derivative slips inside the expectation, so we are "
                 "differentiating e to the s X with respect to s, n times "
                 "over."
        ):
            self.play(Write(line[1]), Write(line[2]), run_time=1.2)

        cascade = MathTex(
            r"e^{sX}",
            r"\;\xrightarrow{\;d/ds\;}\;",
            r"X\, e^{sX}",
            r"\;\xrightarrow{\;d/ds\;}\;",
            r"X^2\, e^{sX}",
            r"\;\longrightarrow\;\cdots\;\longrightarrow\;",
            r"X^n\, e^{sX}",
            font_size=SMALL,
        ).next_to(line, DOWN, buff=0.5)
        fit_to_frame(cascade)

        with self.voiceover(
            text="Watch what each pass does: differentiating once pulls "
                 "one factor of X down in front of the exponential. Twice, "
                 "X squared. After n passes, X to the n stands in front."
        ):
            self.play(Write(cascade[0]), run_time=0.5)
            self.play(Write(cascade[1]), Write(cascade[2]), run_time=0.8)
            self.play(Write(cascade[3]), Write(cascade[4]), run_time=0.8)
            self.play(Write(cascade[5]), Write(cascade[6]), run_time=0.8)
            self.play(cascade[6].animate.set_color(ACCENT), run_time=0.5)

        result = MathTex(
            r"\frac{d^n}{ds^n} M_X(s) \Big|_{s=0}",
            "=",
            expectation("X^n"),
            font_size=BODY,
        ).next_to(cascade, DOWN, buff=0.5)
        fit_to_frame(result)

        with self.voiceover(
            text="Now set s to zero. The exponential collapses to one, and "
                 "what remains is the expected value of X to the n — the "
                 "n-th moment, read off on demand."
        ):
            self.play(cascade.animate.set_color(MUTED), run_time=0.5)
            self.play(Write(result), run_time=1.0)
            self.play(result[2].animate.set_color(ACCENT), run_time=0.5)

        readouts = VGroup(
            MathTex(r"M_X'(0) = " + expectation("X"), font_size=SMALL),
            MathTex(r"M_X''(0) = " + expectation("X^2"), font_size=SMALL),
        ).arrange(RIGHT, buff=1.0).next_to(result, DOWN, buff=0.45)
        fit_to_frame(readouts)
        motto = Text("differentiate, do not integrate",
                     font_size=CAPTION, color=MUTED)
        motto.next_to(readouts, DOWN, buff=0.3)

        with self.voiceover(
            # (2026-07-04 draft review, 3:28) Concept, not a video number.
            text="In particular, the first derivative at zero is the mean, "
                 "and the second derivative at zero is the second moment: "
                 "the two numbers every variance computation needs, "
                 "now delivered by one function. Compute the transform "
                 "once, and differentiation replaces integration forever "
                 "after."
        ):
            self.play(result[2].animate.set_color(INK), run_time=0.4)
            self.play(Write(readouts[0]), run_time=0.8)
            self.play(Write(readouts[1]), run_time=0.8)
            self.play(FadeIn(motto, shift=UP * 0.2), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class ExponentialMGF(VoiceoverScene):
    """Beat: exponential-mgf -- one integral, every moment."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Worked Example: the Exponential")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        card = MathTex(r"X \sim \text{Exponential}(\lambda)",
                       font_size=SMALL, color=INK)
        card.next_to(title, DOWN, buff=0.4)

        with self.voiceover(
            text="Time to work one end to end. Let X be exponential with "
                 "parameter lambda."
        ):
            self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.7)

        chain = MathTex(
            r"M_X(s)", "=",
            r"\int_0^{\infty} \lambda e^{-\lambda x}\, e^{sx}\, dx", "=",
            r"\int_0^{\infty} \lambda e^{-(\lambda - s)x}\, dx", "=",
            r"\frac{\lambda}{\lambda - s}",
            font_size=SMALL,
        ).next_to(card, DOWN, buff=0.45)
        fit_to_frame(chain)
        mark_intended_overlap(
            chain,
            reason="integral limits and fraction glyphs overlap within one "
                   "typeset equation")
        cond = MathTex(r"s < \lambda", font_size=CAPTION, color=MUTED)
        cond.next_to(chain, DOWN, buff=0.25)

        with self.voiceover(
            text="The transform is a single easy integral. From zero to "
                 "infinity, lambda e to the minus lambda x, times the probe "
                 "e to the s x. The two exponentials merge into e to the "
                 "minus lambda minus s, times x — and for s below lambda, "
                 "the integral evaluates to lambda over lambda minus s."
        ):
            self.play(Write(chain[0]), Write(chain[1]), Write(chain[2]),
                      run_time=1.1)
            self.play(Write(chain[3]), Write(chain[4]), run_time=1.0)
            self.play(Write(chain[5]), Write(chain[6]), FadeIn(cond),
                      run_time=1.0)

        with self.voiceover(
            text="That compact fraction now holds every moment of X."
        ):
            self.play(chain[6].animate.set_color(ACCENT), run_time=0.5)
            self.play(Indicate(chain[6], color=ACCENT, scale_factor=1.03),
                      run_time=0.7)

        mean = MathTex(
            expectation("X"), "=",
            r"\left. \frac{\lambda}{(\lambda - s)^2} \right|_{s=0}", "=",
            r"\frac{1}{\lambda}",
            font_size=SMALL,
        ).next_to(cond, DOWN, buff=0.35)
        fit_to_frame(mean)

        with self.voiceover(
            text="Differentiate once: lambda over lambda minus s squared. "
                 "Set s to zero, and the mean appears: one over lambda — "
                 "no integration by parts required."
        ):
            self.play(chain[6].animate.set_color(INK),
                      Write(mean), run_time=1.2)
            self.play(mean[4].animate.set_color(ACCENT), run_time=0.5)

        nth = MathTex(
            expectation("X^n"), "=",
            r"\left. \frac{n!\, \lambda}{(\lambda - s)^{n+1}} \right|_{s=0}",
            "=", r"\frac{n!}{\lambda^n}",
            font_size=SMALL,
        ).next_to(mean, DOWN, buff=0.4)
        fit_to_frame(nth)

        with self.voiceover(
            text="Keep differentiating and a factorial builds up: the n-th "
                 "derivative is n factorial lambda over lambda minus s to "
                 "the n plus one, which at zero is n factorial over lambda "
                 "to the n. Every moment of the exponential, from one "
                 "integral."
        ):
            self.play(mean[4].animate.set_color(INK),
                      Write(nth), run_time=1.2)
            self.play(nth[4].animate.set_color(ACCENT), run_time=0.5)

        var = MathTex(
            variance("X"), "=",
            r"\frac{2}{\lambda^2} - \frac{1}{\lambda^2}", "=",
            r"\frac{1}{\lambda^2}",
            font_size=SMALL,
        ).next_to(nth, DOWN, buff=0.4)
        fit_to_frame(var)

        with self.voiceover(
            text="The variance rides along for free: the second moment is "
                 "two over lambda squared; subtract the square of the "
                 "mean, and one over lambda squared remains."
        ):
            self.play(nth[4].animate.set_color(INK),
                      Write(var), run_time=1.1)
            self.play(var[4].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])


class GaussianMGF(VoiceoverScene):
    """Beat: gaussian-mgf -- complete the square, then every Gaussian."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Gaussian, and Every Gaussian")
        fit_to_frame(title)

        with self.voiceover(
            text="The jewel of the catalog is the standard normal."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))

        density = MathTex(
            r"f_X(x) = \frac{1}{\sqrt{2\pi}}\, e^{-x^2/2}",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.4)
        merged = MathTex(
            r"M_X(s)", "=",
            r"\int_{-\infty}^{\infty} \frac{1}{\sqrt{2\pi}}\,"
            r" e^{-(x^2 - 2sx)/2}\, dx",
            font_size=SMALL,
        ).next_to(density, DOWN, buff=0.35)
        fit_to_frame(merged)

        with self.voiceover(
            text="Its density is e to the minus x squared over two, scaled "
                 "by the square root of two pi. Multiply by the probe, and "
                 "the two exponents merge into minus x squared minus two "
                 "s x, over two."
        ):
            self.play(Write(density), run_time=1.0)
            self.play(Write(merged), run_time=1.2)

        completed = MathTex(
            "=", r"e^{s^2/2}",
            r"\int_{-\infty}^{\infty} \frac{1}{\sqrt{2\pi}}\,"
            r" e^{-(x - s)^2/2}\, dx",
            font_size=SMALL,
        ).next_to(merged, DOWN, buff=0.3)
        fit_to_frame(completed)

        with self.voiceover(
            text="Now complete the square: add and subtract s squared "
                 "inside, and the exponent splits into minus x minus s "
                 "squared over two, plus s squared over two. The clean "
                 "factor, e to the s squared over two, steps outside the "
                 "integral."
        ):
            self.play(Write(completed), run_time=1.3)
            self.play(completed[1].animate.set_color(ACCENT), run_time=0.5)

        # The bell slides from center 0 to center s; its area stays 1.
        axes = Axes(
            x_range=[-3, 4, 1],
            y_range=[0, 0.55, 0.25],
            x_length=6.8,
            y_length=1.9,
            tips=False,
        )
        bell = axes.plot(
            lambda x: 0.4 * np.exp(-x * x / 2), color=BAR)
        bell_s = axes.plot(
            lambda x: 0.4 * np.exp(-(x - 1.5) ** 2 / 2), color=BAR)
        chart = VGroup(axes, bell, bell_s)
        chart.to_edge(DOWN, buff=1.0)
        # (2026-07-04 draft review, 5:35) Shade the area under the slid
        # curve exactly as the narration says it still integrates to one;
        # the caption spells the word out ("area stays one").
        area = axes.get_area(bell_s, x_range=[-3, 4],
                             color=BAR, opacity=0.3)
        mark_intended_overlap(
            axes, bell, bell_s, area,
            reason="bell curve slides along its own axes; the area under "
                   "the slid curve is shaded to show it stays one")
        area_note = Text("area stays one", font_size=CAPTION, color=MUTED)
        area_note.next_to(chart, DOWN, buff=0.25)

        with self.voiceover(
            text="Look at what stays inside: a Gaussian density whose "
                 "center has slid from zero to s."
        ):
            self.play(Create(axes), run_time=0.6)
            self.play(Create(bell), run_time=0.7)
            self.play(Transform(bell, bell_s), run_time=1.0)

        with self.voiceover(
            text="Sliding a bell curve does not change its area — it "
                 "still integrates to exactly one."
        ):
            self.play(FadeIn(area), run_time=0.7)
            self.play(FadeIn(area_note, shift=UP * 0.2), run_time=0.5)

        result = MathTex(r"M_X(s) = e^{s^2/2}", font_size=BODY)
        result.next_to(completed, DOWN, buff=0.5)

        with self.voiceover(
            text="So the integral vanishes, and the factor out front is "
                 "the whole answer: the moment generating function of the "
                 "standard normal is e to the s squared over two — the "
                 "simplest transform in the catalog."
        ):
            self.play(FadeOut(chart), FadeOut(area), FadeOut(area_note),
                      run_time=0.5)
            self.play(completed[1].animate.set_color(INK),
                      Write(result), run_time=1.0)
            self.play(result.animate.set_color(ACCENT), run_time=0.5)

        affine = MathTex(
            r"M_{aX+b}(s)", "=", r"e^{sb}\, M_X(as)",
            font_size=BODY,
        )

        with self.voiceover(
            text="One more rule lifts this to every Gaussian. For Y equals "
                 "a X plus b, the transform of Y is e to the s b, times "
                 "the transform of X at a s: the shift walks out of the "
                 "expectation, and the scale folds into the dial."
        ):
            result.generate_target()
            result.target.set_color(INK).next_to(title, DOWN, buff=0.45)
            self.play(FadeOut(density), FadeOut(merged), FadeOut(completed),
                      MoveToTarget(result), run_time=0.8)
            affine.next_to(result.target, DOWN, buff=0.6)
            fit_to_frame(affine)
            self.play(Write(affine), run_time=1.1)
            self.play(affine[0].animate.set_color(ACCENT), run_time=0.5)

        gen = MathTex(
            r"Y = \sigma X + m:", r"\;\; M_Y(s) = e^{sm + s^2 \sigma^2/2}",
            font_size=BODY,
        ).next_to(affine, DOWN, buff=0.5)
        fit_to_frame(gen)

        with self.voiceover(
            text="Apply it to Y equals sigma X plus m — an affine function "
                 "of a Gaussian is Gaussian — and the general answer "
                 "appears: e to the s m plus s squared sigma squared over "
                 "two."
        ):
            self.play(affine[0].animate.set_color(INK),
                      Write(gen), run_time=1.2)
            self.play(gen[1].animate.set_color(ACCENT), run_time=0.5)

        checks = VGroup(
            MathTex(expectation("Y") + "= m", font_size=SMALL),
            MathTex(expectation("Y^2") + r"= \sigma^2 + m^2",
                    font_size=SMALL),
            MathTex(variance("Y") + r"= \sigma^2", font_size=SMALL),
        ).arrange(RIGHT, buff=0.8).next_to(gen, DOWN, buff=0.55)
        fit_to_frame(checks)

        with self.voiceover(
            text="Differentiate at zero: the mean is m; the second moment "
                 "is sigma squared plus m squared; so the variance is "
                 "sigma squared, exactly as anticipated."
        ):
            self.play(gen[1].animate.set_color(INK), run_time=0.4)
            self.play(Write(checks[0]), run_time=0.7)
            self.play(Write(checks[1]), run_time=0.7)
            self.play(Write(checks[2]), run_time=0.7)
            self.play(checks[2].animate.set_color(ACCENT), run_time=0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        outro = outro_bridge(
            ["One transform holds every moment:",
             "differentiate at zero and they fall out."],
            next_title="The Markov and Chebyshev Inequalities",
        )

        with self.voiceover(
            # (2026-07-04 draft review, 6:54) Narration stops here — the
            # "Keep it in your pocket…" close is deleted; the card holds a
            # beat longer so the visuals fit the shorter audio.
            text="The key idea of this video: one transform packages every "
                 "moment — compute it once, and differentiate instead of "
                 "integrating."
        ):
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(outro[1]), run_time=1.1)
            self.play(FadeIn(outro[2], shift=UP * 0.2), run_time=0.7)

        self.wait(1.0)
        self.play(FadeOut(outro))
