# derived_from: content/16-important-discrete-rvs-script.md
# derived_from_sha256: 7529f14c11eb3fdc0057932a81145daa2843f84ca925285357e78a9e99868842
"""Chapter 5 -- Important Discrete Random Variables (narrated with manim-voiceover).

Source notes : the named-distributions section of the discrete random
               variables chapter.
Script        : content/16-important-discrete-rvs-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks, one per <bookmark> segment -- the same
pattern as the earlier videos in the series. The narration is the source of
truth; visuals are timed to the spoken word without word-level timestamps.

Draft render:
    uv run manim -pql scenes/important_discrete_rvs.py ChapterOverview
Final: switch make_speech_service() to OpenAIService (needs OPENAI_API_KEY).
"""

import os
import sys
from math import comb, exp, factorial

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
    make_pmf_chart,
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


# --- PMF generators (plain Python, kept out of the Scene classes) ------------

def bernoulli_pmf(p=0.25):
    return [1 - p, p]


def binomial_pmf(n=8, p=0.25):
    return [comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]


def poisson_pmf(lam=2.0, kmax=8):
    return [lam**k / factorial(k) * exp(-lam) for k in range(kmax + 1)]


def geometric_pmf(p=0.25, kmax=12):
    # Indexed from k=0 so it lines up on the integer axis; p_X(k) = (1-p)^k * p.
    return [(1 - p) ** k * p for k in range(kmax + 1)]


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- title card, PMF recap, and a five-item outline."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "Important Discrete Random Variables",
            "Meet named distributions that are often used in probabilistic "
            "modeling.",
            kicker="Chapter 5  ·  Discrete Random Variables",
        )
        fit_to_frame(intro)
        tag = progress_tag(2, 3).to_corner(DR, buff=0.4)

        items = VGroup(
            Text("1.  Bernoulli", font_size=SMALL, color=INK),
            Text("2.  Binomial", font_size=SMALL, color=INK),
            Text("3.  Poisson", font_size=SMALL, color=INK),
            Text("4.  Geometric", font_size=SMALL, color=INK),
            Text("5.  Uniform", font_size=SMALL, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        punchline = Text("...and the binomial folds into the Poisson.",
                         font_size=SMALL, color=ACCENT)

        with self.voiceover(
            # (2026-07-06 intro-variety pass) opener reworded for playlist variety.
            text="Recall that a discrete random variable is "
                 "captured entirely by its probability mass function. In "
                 "practice, though, you rarely start from scratch. A small "
                 "number of distributions show up frequently, and almost all of "
                 "them come from counting. In this video we tour five of "
                 "them — the Bernoulli, the binomial, the Poisson, the "
                 "geometric, and the uniform — each with its own counting story "
                 "and its own bar chart. And in the middle we'll see something "
                 "surprising: the binomial, in a certain limit, turns into the "
                 "Poisson."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)

            block = VGroup(items, punchline).arrange(DOWN, buff=0.5)
            block.next_to(intro, DOWN, buff=0.9)
            fit_to_frame(block)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in items],
                                  lag_ratio=0.25), run_time=1.4)
            self.play(FadeIn(punchline, shift=UP * 0.1), run_time=0.6)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Bernoulli(VoiceoverScene):
    """Beat: bernoulli -- two-valued atom, its two-bar PMF, and the coin note."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Bernoulli Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Start with the simplest random variable there is."
        ):
            self.wait(0.3)

        formula = MathTex(
            r"p_X(x)=\begin{cases}1-p & x=0\\ p & x=1\end{cases}",
            font_size=SECTION, color=ACCENT,
        )
        formula.next_to(title, DOWN, buff=0.5)
        fit_to_frame(formula)
        with self.voiceover(
            text="A Bernoulli random variable takes only two values, zero and "
                 "one. It equals one with probability p, and zero with "
                 "probability one minus p. That's the entire distribution."
        ):
            self.play(Write(formula))

        chart, bars = make_pmf_chart(bernoulli_pmf(0.25), x_label="x")
        chart.scale(0.72).to_edge(DOWN, buff=0.65)
        fit_to_frame(chart)
        with self.voiceover(
            text="As a bar chart it is just two bars: possibly a tall one and a "
                 "short one, and here p is one-quarter."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.12), run_time=0.9)

        coin = MathTex(
            r"\text{heads}=1,\quad \text{tails}=0,\quad \Pr(\text{heads})=p",
            font_size=SMALL, color=INK,
        )
        coin.next_to(formula, DOWN, buff=0.45)
        fit_to_frame(coin)
        with self.voiceover(
            text="Every Bernoulli is really a coin flip — a biased coin that "
                 "comes up heads, which we call one, with probability p. It "
                 "looks trivial, but it is the atom from which the next two "
                 "distributions are built."
        ):
            self.play(FadeIn(coin, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Binomial(VoiceoverScene):
    """Beat: binomial -- counting successes in n trials; the soda-cap story."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Binomial Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Now flip that coin n times, independently, and count the ones."
        ):
            self.wait(0.3)

        pmf = MathTex(r"p_X(k)=\binom{n}{k}p^k(1-p)^{n-k},\quad k=0,1,\dots,n",
                      font_size=BODY, color=ACCENT)
        norm = MathTex(r"\sum_{k=0}^{n} p_X(k) = (p+(1-p))^n = 1",
                       font_size=SMALL, color=INK)
        define = VGroup(pmf, norm).arrange(DOWN, buff=0.35)
        define.next_to(title, DOWN, buff=0.4)
        fit_to_frame(define)
        with self.voiceover(
            text="The number of successes in n independent, identical Bernoulli "
                 "trials is a binomial random variable. Its PMF is n-choose-k "
                 "times p to the k times one-minus-p to the n-minus-k — the "
                 "n-choose-k counts which trials succeeded, and the powers give "
                 "the probability of any one such pattern."
        ):
            self.play(Write(pmf))
        with self.voiceover(
            text="Sum over all k and the binomial theorem gives exactly one."
        ):
            self.play(FadeIn(norm, shift=UP * 0.1))

        chart, bars = make_pmf_chart(binomial_pmf(8, 0.25), x_label="k")
        chart.scale(0.62).to_edge(DOWN, buff=0.75)
        fit_to_frame(chart)
        with self.voiceover(
            text="With n equal to eight and p a quarter, the bars rise to a "
                 "peak near two and taper off."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.08), run_time=1.0)

        soda_text = Text("Brazos Soda pays $1 under 1 cap in 4; buy 8 bottles",
                         font_size=SMALL, color=MUTED)
        soda_eq = MathTex(
            r"\Pr(X>4)=\sum_{k=5}^{8}\binom{8}{k}\tfrac{3^{8-k}}{4^8}",
            font_size=BODY, color=INK,
        )
        soda = VGroup(soda_text, soda_eq).arrange(DOWN, buff=0.5)
        soda.move_to(DOWN * 0.8)
        fit_to_frame(soda)
        with self.voiceover(
            text="Here's the story: a soda promotion pays a dollar under one cap "
                 "in four. Buy eight bottles, and the number of winners is "
                 "binomial with n eight, p one-quarter. The chance of winning "
                 "more than four dollars is the sum of the PMF from five up to "
                 "eight."
        ):
            self.play(FadeOut(chart))
            self.play(FadeIn(soda_text, shift=UP * 0.1))
            self.play(Write(soda_eq))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Poisson(VoiceoverScene):
    """Beat: poisson -- counting rare events over time; the server note."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Poisson Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="The next one counts occurrences over time."
        ):
            self.wait(0.3)

        pmf = MathTex(r"p_X(k)=\frac{\lambda^k}{k!}e^{-\lambda}",
                      font_size=SECTION, color=ACCENT)
        norm = MathTex(
            r"\sum_{k=0}^{\infty}\frac{\lambda^k}{k!}e^{-\lambda}"
            r"=e^{\lambda}e^{-\lambda}=1",
            font_size=SMALL, color=INK,
        )
        define = VGroup(pmf, norm).arrange(DOWN, buff=0.35)
        define.next_to(title, DOWN, buff=0.4)
        fit_to_frame(define)
        with self.voiceover(
            text="A Poisson random variable has PMF lambda-to-the-k over "
                 "k-factorial, times e-to-the-minus-lambda, for k equals zero, "
                 "one, two, and up."
        ):
            self.play(Write(pmf))
        with self.voiceover(
            text="It normalizes beautifully: the sum of lambda-to-the-k over "
                 "k-factorial is just the Taylor series for e-to-the-lambda, "
                 "which cancels the e-to-the-minus-lambda to leave one."
        ):
            self.play(FadeIn(norm, shift=UP * 0.1))

        chart, bars = make_pmf_chart(poisson_pmf(2.0, 8), x_label="k")
        chart.scale(0.62).to_edge(DOWN, buff=0.4)
        fit_to_frame(chart)
        with self.voiceover(
            text="With lambda equal to two, the mass peaks at one and two and "
                 "decays."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.08), run_time=1.0)

        server = MathTex(
            r"\text{arrivals at rate } \lambda:\quad p_N(0)=e^{-\lambda}",
            font_size=SMALL, color=INK,
        )
        # Sit the note above the chart so it never collides with the y-label.
        server.next_to(chart, UP, buff=0.35)
        fit_to_frame(server)
        with self.voiceover(
            text="Poisson is the go-to model for counts — requests hitting a "
                 "server, arrivals in a queue, calls in a minute. If requests "
                 "arrive at rate lambda per second, the probability that none "
                 "arrives in a given second is simply e-to-the-minus-lambda."
        ):
            self.play(FadeIn(server, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class BinomialToPoisson(VoiceoverScene):
    """Beat: binomial-to-poisson -- bars settle onto the Poisson limit."""

    def construct(self):
        self.set_speech_service(make_speech_service())
        lam = 10.0
        kmax = 16

        title = section_title("Binomial Converges to Poisson")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        formula = MathTex(
            r"\lim_{n\to\infty}\binom{n}{k}\left(\tfrac{\lambda}{n}\right)^k"
            r"\left(1-\tfrac{\lambda}{n}\right)^{n-k}"
            r"=\frac{\lambda^k}{k!}e^{-\lambda}",
            font_size=SMALL,
        ).next_to(title, DOWN, buff=0.35)
        fit_to_frame(formula)  # long formula -> never let it run off the sides
        self.play(Write(formula))

        target = [lam**k / factorial(k) * exp(-lam) for k in range(kmax + 1)]
        y_max = max(target) * 1.6
        axes = Axes(
            x_range=[0, kmax, 2],
            y_range=[0, y_max, 0.05],
            x_length=9,
            y_length=3.6,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False,
        ).to_edge(DOWN, buff=0.5)
        fit_to_frame(axes)  # bars are built from axes.c2p, so guard it first
        x_lab = axes.get_x_axis_label(
            MathTex("k", font_size=SMALL), edge=RIGHT, direction=DR, buff=0.2)

        def bars_for(values, color, opacity):
            unit_w = axes.x_axis.unit_size
            grp = VGroup()
            for k, p in enumerate(values):
                height = max(axes.c2p(k, p)[1] - axes.c2p(k, 0)[1], 1e-3)
                rect = Rectangle(
                    width=unit_w * 0.6, height=height,
                    fill_color=color, fill_opacity=opacity,
                    stroke_width=1, stroke_color=INK,
                )
                rect.move_to(axes.c2p(k, 0), aligned_edge=DOWN)
                grp.add(rect)
            return grp

        poisson_ref = bars_for(target, ACCENT, 0.18)
        ref_label = Text("Poisson(10)", font_size=CAPTION, color=ACCENT)
        ref_label.next_to(axes, UP, buff=0.35).to_edge(RIGHT, buff=1.0)

        # p = lambda/n must be <= 1, so n has to exceed lambda = 10.
        n_values = [15, 25, 35]
        binom = [
            [comb(n, k) * (lam / n) ** k * (1 - lam / n) ** (n - k)
             if k <= n else 0.0 for k in range(kmax + 1)]
            for n in n_values
        ]

        with self.voiceover(
            text="Here's the payoff, and it connects the last two."
        ):
            self.play(Create(axes), Write(x_lab))

        with self.voiceover(
            text="Fix a rate lambda, and let each of n trials succeed with "
                 "probability lambda over n — so as n grows, each success gets "
                 "rarer, but the expected count stays lambda."
        ):
            self.play(FadeIn(poisson_ref), FadeIn(ref_label))

        n_label = Text("n = 15", font_size=BODY, color=INK)
        n_label.next_to(axes, UP, buff=0.35).to_edge(LEFT, buff=1.0)
        current = bars_for(binom[0], BAR, 0.85)
        with self.voiceover(
            text="With fifteen trials the shape is close, but still a little "
                 "rough."
        ):
            self.play(FadeIn(n_label),
                      LaggedStartMap(GrowFromEdge, current, edge=DOWN,
                                     lag_ratio=0.05))

        captions = [
            (25, "Twenty-five trials, and it sharpens."),
            (35, "Thirty-five trials, and the bars"),
        ]
        for (n, narration), values in zip(captions, binom[1:]):
            new_label = Text(f"n = {n}", font_size=BODY, color=INK)
            new_label.move_to(n_label)
            new_bars = bars_for(values, BAR, 0.85)
            with self.voiceover(text=narration):
                self.play(Transform(current, new_bars),
                          Transform(n_label, new_label),
                          run_time=1.2)

        with self.voiceover(
            text="settle right onto the Poisson curve drawn faintly behind "
                 "them. In the limit, the binomial becomes the Poisson. This is "
                 "why a Poisson with lambda equal to n-times-p is such a good "
                 "approximation to a binomial when n is large and p is small."
        ):
            self.play(Indicate(poisson_ref, scale_factor=1.05, color=ACCENT))

        self.play(*[FadeOut(m) for m in self.mobjects])


class Geometric(VoiceoverScene):
    """Beat: geometric -- waiting for the first success; the memoryless law."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Geometric Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="Instead of counting successes in a fixed number of trials, "
                 "now wait for the first success."
        ):
            self.wait(0.3)

        formula = MathTex(r"p_X(k)=(1-p)^{k-1}p,\quad k=1,2,\dots",
                          font_size=SECTION, color=ACCENT)
        formula.next_to(title, DOWN, buff=0.5)
        fit_to_frame(formula)
        with self.voiceover(
            text="Keep running Bernoulli trials until you get a one; the number "
                 "of trials that took is a geometric random variable. Its PMF is "
                 "one-minus-p to the k-minus-one, times p — the probability of "
                 "k-minus-one failures followed by a success."
        ):
            self.play(Write(formula))

        chart, bars = make_pmf_chart(geometric_pmf(0.25, 12), x_label="k")
        chart.scale(0.66).to_edge(DOWN, buff=0.85)
        fit_to_frame(chart)
        with self.voiceover(
            text="Because each extra trial multiplies by one-minus-p, the bars "
                 "decay by a constant factor: a steadily shrinking staircase."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.08), run_time=1.0)

        memoryless = MathTex(r"\Pr(X=k+j \mid X>k)=\Pr(X=j)",
                             font_size=SMALL, color=ACCENT)
        memoryless.next_to(formula, DOWN, buff=0.45)
        fit_to_frame(memoryless)
        with self.voiceover(
            text="And the geometric hides a remarkable property — it is "
                 "memoryless. Given that you've already waited more than k "
                 "trials, the probability you need j more is exactly the "
                 "original probability of j. The process forgets its past "
                 "completely, and the geometric is the only discrete random "
                 "variable that does."
        ):
            self.play(FadeIn(memoryless, shift=UP * 0.1))

        self.play(*[FadeOut(m) for m in self.mobjects])


class DiscreteUniform(VoiceoverScene):
    """Beat: uniform -- the flat PMF, plus the closing key-idea + bridge."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Discrete Uniform Distribution")
        fit_to_frame(title)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        with self.voiceover(
            text="The last one is the picture of pure symmetry."
        ):
            self.wait(0.3)

        formula = MathTex(r"p_X(k)=\frac{1}{n},\quad k=1,2,\dots,n",
                          font_size=BODY, color=ACCENT)
        formula.next_to(title, DOWN, buff=0.5)
        fit_to_frame(formula)
        with self.voiceover(
            text="A discrete uniform random variable takes n values, all "
                 "equally likely — each with probability one over n."
        ):
            self.play(Write(formula))

        # Values [0] + [1/8]*8 so the eight equal bars sit at k = 1..8.
        chart, bars = make_pmf_chart([0.0] + [1 / 8] * 8, x_label="k")
        chart.scale(0.66).to_edge(DOWN, buff=0.85)
        fit_to_frame(chart)
        note = Text("A fair die and a fair coin are discrete uniforms.",
                    font_size=CAPTION, color=MUTED)
        note.next_to(formula, DOWN, buff=0.4)
        fit_to_frame(note)
        with self.voiceover(
            text="Its bar chart is perfectly flat; here n is eight, so every "
                 "bar sits at one-eighth. We've quietly met this one already: a "
                 "fair die and a fair coin are both discrete uniforms."
        ):
            self.play(Create(chart[0]), Write(chart[1]), Write(chart[2]),
                      run_time=0.8)
            self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN,
                                     lag_ratio=0.08), run_time=1.0)
            self.play(FadeIn(note, shift=UP * 0.1))

        # --- outro: key idea + bridge to functions of a random variable. ---
        outro = VGroup(
            Text("Key idea", font_size=SMALL, color=ACCENT),
            Text("A handful of named PMFs, each tied to a counting story.",
                 font_size=SMALL, color=INK),
            Text("These distributions are frequently employed in probabilistic "
                 "modeling.", font_size=SMALL, color=INK),
            Text("Coming up:  functions of a random variable",
                 font_size=SMALL, color=MUTED),
        ).arrange(DOWN, buff=0.4)
        fit_to_frame(outro)

        with self.voiceover(
            text="So there is our gallery — Bernoulli, binomial, Poisson, "
                 "geometric, uniform — five distributions, each tied to a "
                 "counting story, and the binomial folding into the Poisson in "
                 "the limit. Next, we'll take a random variable and transform "
                 "it, and follow what happens to its PMF."
        ):
            self.play(*[FadeOut(m) for m in self.mobjects])
            self.play(FadeIn(outro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(outro[1], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(outro[2], shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(outro[3], shift=UP * 0.15), run_time=0.6)

        self.wait(0.5)
        self.play(FadeOut(outro))
