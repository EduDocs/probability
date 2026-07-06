# derived_from: content/12-total-probability-script.md
# derived_from_sha256: b3dd138af6049f4b4280d623d7f3d061d327ddc7f1f5cd89d795f00967047a8a
"""Chapter 4, Video 2 -- The Total Probability Theorem.

Source notes : ../chapters/conditional_probability.tex (total probability).
Script        : content/12-total-probability-script.md

Timing model (bookmark-free, portable): each beat is split into sequential
``with self.voiceover(text=...)`` blocks -- one per <bookmark> segment of the
narration -- the same pattern as the earlier videos in the series.

Draft render:
    uv run manim -pql scenes/total_probability.py ChapterOverview
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

    Draft  -> GTTSService (free, ACTIVE). Final -> OpenAIService(voice="nova"),
    matching the rest of the series; swap the lines below and add OPENAI_API_KEY.
    """
    # return GTTSService(lang="en", tld="com")  # free draft voice
    configure_openai_client()
    return OpenAIService(voice="nova", model="tts-1",
                         transcription_model=None)


# --- Shared visual helpers (mirroring the house style) -----------------------

def omega_tiling(width=4.4, height=3.6):
    """Sample space Omega sliced into three disjoint vertical tiles.

    Returns VGroup(outer, olab, tiles, labels) so callers can animate the
    border, the Omega label, the coloured tiles, and their A_k labels apart.
    """
    outer = Rectangle(width=width, height=height, color=MUTED).set_stroke(MUTED, 2)
    olab = MathTex(r"\Omega", font_size=BODY, color=MUTED)
    olab.next_to(outer.get_corner(UL), DR, buff=0.22)

    cols = [BLUE, TEAL, GREEN]
    names = [r"A_1", r"A_2", r"A_3"]
    tw = width / 3.0
    left = outer.get_left()[0]
    cy = outer.get_center()[1]

    tiles = VGroup()
    labels = VGroup()
    for i, (col, nm) in enumerate(zip(cols, names)):
        cx = left + tw * (i + 0.5)
        tile = Rectangle(
            width=tw, height=height,
            fill_color=col, fill_opacity=0.25,
            stroke_color=INK, stroke_width=1.5,
        ).move_to([cx, cy, 0])
        tiles.add(tile)
        labels.add(MathTex(nm, font_size=SMALL, color=INK).move_to([cx, cy, 0]))

    return VGroup(outer, olab, tiles, labels)


def make_urn(label, greens, reds, cols):
    """A rounded-rectangle urn holding coloured balls, arranged in a grid."""
    body = RoundedRectangle(
        corner_radius=0.3, width=2.0, height=2.3, color=MUTED
    ).set_stroke(MUTED, 2)
    dots = VGroup()
    for _ in range(greens):
        dots.add(Dot(radius=0.11, color=GREEN))
    for _ in range(reds):
        dots.add(Dot(radius=0.11, color=RED))
    dots.arrange_in_grid(cols=cols, buff=0.11)
    dots.move_to(body.get_center())
    lab = MathTex(label, font_size=SMALL, color=INK)
    lab.next_to(body, UP, buff=0.18).align_to(body, RIGHT)
    return VGroup(body, dots, lab)


class ChapterOverview(VoiceoverScene):
    """Beat: overview -- recap of conditioning + the divide-and-conquer goal."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        intro = intro_card(
            "The Total Probability Theorem",
            "Compute the probability of an event by splitting the "
            "sample space.",
            kicker="Chapter 4  ·  Conditional Probability",
        )
        fit_to_frame(intro)
        tag = progress_tag(2, 4).to_corner(DR, buff=0.4)

        recap_eq = MathTex(
            r"\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)}",
            font_size=BODY, color=INK,
        )
        goal = MathTex(
            r"\text{Goal:}\ \ \Pr(B)\ \text{by conditioning on cases}",
            font_size=BODY, color=ACCENT,
        )
        below = VGroup(recap_eq, goal).arrange(DOWN, buff=0.6)

        with self.voiceover(
            text="Last video we learned to condition — to update the probability "
                 "of an event once we know another has occurred. Now we use "
                 "conditioning for a different job: computing the plain, "
                 "unconditional probability of an event that is hard to attack "
                 "head-on. The trick is divide and conquer. Break the sample space "
                 "into a handful of scenarios, work out the probability inside each "
                 "one where it's easy, then stitch the pieces back together. That "
                 "recipe is the total probability theorem, and it is the bridge to "
                 "Bayes' rule in the next video. First we need the right way to "
                 "carve up the sample space: a partition."
        ):
            self.play(FadeIn(intro[0], shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(intro[1]), run_time=1.0)
            self.play(FadeIn(intro[2], shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.play(intro.animate.to_edge(UP), run_time=0.8)
            below.next_to(intro, DOWN, buff=0.7)
            fit_to_frame(below)
            self.play(Write(recap_eq), run_time=1.2)
            self.play(Write(goal), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


class Partitioning(VoiceoverScene):
    """Beat: partition -- the definition, then a clean tiling of Omega."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Partitions")
        fit_to_frame(title)

        # Right column: the partition definition.
        dhead = Text("A partition of Ω", font_size=SMALL, color=ACCENT)
        d1 = MathTex(r"A_i \cap A_j = \varnothing,\quad i \neq j",
                     font_size=SMALL, color=INK)
        d1cap = Text("disjoint events", font_size=CAPTION, color=MUTED)
        d2 = MathTex(r"\bigcup_{k=1}^{n} A_k = \Omega",
                     font_size=SMALL, color=INK)
        d2cap = Text("together they cover everything", font_size=CAPTION,
                     color=MUTED)
        defn = VGroup(dhead, d1, d1cap, d2, d2cap).arrange(
            DOWN, buff=0.3, aligned_edge=LEFT)
        defn.move_to(RIGHT * 3.4)
        fit_to_frame(defn)

        with self.voiceover(
            text="Recall the idea of a partition. A collection of events A-one, "
                 "A-two, up to A-n is a partition of the sample space when two "
                 "things hold: the events are disjoint — no two overlap — and "
                 "together they cover everything, their union is all of Omega."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))
            self.play(FadeIn(dhead, shift=RIGHT * 0.3))
            self.play(Write(d1), FadeIn(d1cap, shift=UP * 0.1))
            self.play(Write(d2), FadeIn(d2cap, shift=UP * 0.1))

        # Left column: Omega tiled into three disjoint colored tiles.
        tiling = omega_tiling(width=4.6, height=3.8)
        tiling.move_to(LEFT * 3.4)
        fit_to_frame(tiling)
        outer, olab, tiles, labels = tiling[0], tiling[1], tiling[2], tiling[3]
        dot = Dot(radius=0.09, color=ACCENT).move_to(
            tiles[1].get_center() + DOWN * 0.7)
        dotcap = Text("every outcome in exactly one tile", font_size=CAPTION,
                      color=MUTED).next_to(tiling, DOWN, buff=0.25)
        fit_to_frame(dotcap)

        with self.voiceover(
            text="Picture Omega as a rectangle sliced cleanly into colored tiles. "
                 "Every outcome lands in exactly one tile — no gaps, no "
                 "double-counting. That \"exactly one\" is the whole point: it is "
                 "what will let us add probabilities without any fear of overlap."
        ):
            self.play(Create(outer), Write(olab))
            self.play(LaggedStartMap(FadeIn, tiles, lag_ratio=0.3))
            self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.2))
            self.play(FadeIn(dot, scale=1.4), FadeIn(dotcap, shift=UP * 0.1))
            self.play(Indicate(tiles[1], color=ACCENT, scale_factor=1.05))

        self.play(*[FadeOut(m) for m in self.mobjects])


class TotalProbability(VoiceoverScene):
    """Beat: theorem -- slice B over the tiles, add the pieces, then condition."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("The Total Probability Theorem")
        fit_to_frame(title)

        # Left column: the tiled Omega, reused from the partition beat.
        tiling = omega_tiling(width=4.4, height=3.6)
        tiling.move_to(LEFT * 3.5 + DOWN * 0.2)
        fit_to_frame(tiling)
        outer, olab, tiles = tiling[0], tiling[1], tiling[2]

        # Right column: the three equations, pre-arranged for stable alignment.
        eq_add = MathTex(
            r"\Pr(B) = \Pr(B \cap A_1) + \cdots + \Pr(B \cap A_n)",
            font_size=SMALL, color=INK,
        )
        prod = MathTex(
            r"\Pr(B \cap A_k) = \Pr(A_k)\,\Pr(B \mid A_k)",
            font_size=SMALL, color=MUTED,
        )
        theorem = MathTex(
            r"\Pr(B) = \sum_{k=1}^{n} \Pr(A_k)\,\Pr(B \mid A_k)",
            font_size=BODY, color=ACCENT,
        )
        rightcol = VGroup(eq_add, prod, theorem).arrange(
            DOWN, buff=0.55, aligned_edge=LEFT)
        rightcol.move_to(RIGHT * 3.3 + DOWN * 0.2)
        fit_to_frame(rightcol)
        thm_box = SurroundingRectangle(
            theorem, color=ACCENT, buff=0.25, corner_radius=0.12
        ).set_stroke(ACCENT, 2)

        # Event B: a translucent ellipse overlapping all three tiles.
        band = Ellipse(
            width=outer.width * 0.86, height=outer.height * 0.60,
            fill_color=MAROON, fill_opacity=0.30,
            stroke_color=MAROON, stroke_width=1.5,
        ).move_to(outer.get_center())
        blab = MathTex(r"B", font_size=SMALL, color=MAROON).next_to(
            band, UP, buff=0.12)
        # The pieces B ∩ A_k are the parts of the ellipse inside each tile.
        pieces = VGroup()
        for tile in tiles:
            piece = Intersection(band, tile).set_stroke(ACCENT, 2.5)
            piece.set_fill(opacity=0.0)
            pieces.add(piece)
        pcap = MathTex(r"\text{pieces}\quad B \cap A_k",
                       font_size=CAPTION, color=MUTED)
        pcap.next_to(tiling, DOWN, buff=0.25)
        fit_to_frame(pcap)

        with self.voiceover(
            text="Now drop an event B onto this partition. Wherever B falls, the "
                 "tiles cut it into pieces — the part of B inside A-one, the part "
                 "inside A-two, and so on. Since the tiles are disjoint, these "
                 "pieces are disjoint too, and together they reassemble all of B."
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))
            self.play(Create(outer), Write(olab))
            self.play(FadeIn(tiles), run_time=0.8)
            self.play(FadeIn(band), Write(blab))
            self.play(LaggedStart(*[Create(p) for p in pieces], lag_ratio=0.3))
            self.play(FadeIn(pcap, shift=UP * 0.1))

        with self.voiceover(
            text="By the third axiom, the probability of B is just the sum of the "
                 "probabilities of those pieces — the probability of B-and-A-one, "
                 "plus B-and-A-two, and so on across the partition."
        ):
            self.play(Write(eq_add))

        with self.voiceover(
            text="Here is the key move. Each piece, by the product rule, is the "
                 "probability of its tile times the conditional probability of B "
                 "given that tile. Substitute, and out comes the total probability "
                 "theorem: the probability of B equals the sum over k of the "
                 "probability of A-k times the probability of B given A-k. Read it "
                 "as a weighted average — the chance of B in each scenario, "
                 "weighted by how likely that scenario is."
        ):
            self.play(Write(prod))
            self.play(Write(theorem), Create(thm_box))
            self.play(Indicate(theorem, color=ACCENT, scale_factor=1.04))

        self.play(*[FadeOut(m) for m in self.mobjects])


class TwoUrns(VoiceoverScene):
    """Beat: example -- two urns, a two-branch tree, and the averaged answer."""

    def construct(self):
        self.set_speech_service(make_speech_service())

        title = section_title("Two Urns")
        fit_to_frame(title)

        # Two urns, positioned at the leaves of the tree to come.
        u1 = make_urn(r"U_1", 5, 3, cols=2).move_to(RIGHT * 1.4 + UP * 1.5)
        u2 = make_urn(r"U_2", 3, 9, cols=3).move_to(RIGHT * 1.4 + DOWN * 1.5)
        note = Text("fair coin picks the urn — probability half each",
                    font_size=CAPTION, color=MUTED)
        note.to_edge(DOWN, buff=0.6)
        fit_to_frame(note)

        with self.voiceover(
            text="Let's put it to work. Two urns sit on a table. The first holds "
                 "five green balls and three red balls; the second, three green and nine "
                 "red balls. We flip a fair coin to pick an urn — each with probability "
                 "one-half — then draw a single ball. What is the probability it's "
                 "green?"
        ):
            self.play(Write(title))
            self.play(title.animate.to_edge(UP))
            self.play(FadeIn(u1, shift=RIGHT * 0.2), FadeIn(u2, shift=RIGHT * 0.2))
            self.play(FadeIn(note, shift=UP * 0.1))

        # The two-branch tree: root -> each urn, labelled 1/2.
        root = Dot(radius=0.10, color=INK).move_to(LEFT * 4.6)
        rlab = Text("coin", font_size=CAPTION, color=MUTED).next_to(root, UP, buff=0.2)
        b1 = Line(root.get_center(), u1[0].get_left(), color=MUTED).set_stroke(MUTED, 2)
        b2 = Line(root.get_center(), u2[0].get_left(), color=MUTED).set_stroke(MUTED, 2)
        p1 = MathTex(r"\tfrac{1}{2}", font_size=SMALL, color=INK).move_to(
            b1.point_from_proportion(0.5) + UP * 0.3)
        p2 = MathTex(r"\tfrac{1}{2}", font_size=SMALL, color=INK).move_to(
            b2.point_from_proportion(0.5) + DOWN * 0.3)
        cond1 = MathTex(r"\Pr(g \mid U_1) = \tfrac{5}{8}",
                        font_size=SMALL, color=INK).next_to(u1[0], RIGHT, buff=0.35)
        cond2 = MathTex(r"\Pr(g \mid U_2) = \tfrac{3}{12}",
                        font_size=SMALL, color=INK).next_to(u2[0], RIGHT, buff=0.35)
        tree = VGroup(root, rlab, b1, b2, p1, p2, cond1, cond2)
        fit_to_frame(VGroup(tree, u1, u2))

        with self.voiceover(
            text="Condition on the urn. If we picked urn one, green has probability "
                 "five over eight. If we picked urn two, green has probability three over "
                 "twelve — one quarter."
        ):
            self.play(FadeIn(root), FadeIn(rlab))
            self.play(Create(b1), Create(b2))
            self.play(Write(p1), Write(p2))
            self.play(Write(cond1))
            self.play(Write(cond2))

        result = MathTex(
            r"\Pr(g) = \tfrac{1}{2}\cdot\tfrac{5}{8} + "
            r"\tfrac{1}{2}\cdot\tfrac{3}{12} = \tfrac{7}{16}",
            font_size=BODY, color=ACCENT,
        )
        # Sit the boxed answer in the clear lower-left, above the frame edge,
        # so it never overlaps the urns or the lower branch.
        result.move_to(LEFT * 3.1 + DOWN * 2.2)
        res_box = SurroundingRectangle(
            result, color=ACCENT, buff=0.22, corner_radius=0.12
        ).set_stroke(ACCENT, 2)
        fit_to_frame(VGroup(result, res_box))

        with self.voiceover(
            text="Total probability stitches them together: one-half times "
                 "five-eighths, plus one-half times three-twelfths, which comes to "
                 "seven-sixteenths. Notice we never had to reason about both urns "
                 "at once — we solved each easy case and let the theorem average "
                 "them."
        ):
            self.play(FadeOut(note))
            self.play(Write(result), Create(res_box))
            self.play(Indicate(result, color=ACCENT, scale_factor=1.04))

        with self.voiceover(
            text="That is the power of conditioning as a computational tool: divide "
                 "the world into cases, conquer each, and average. Next we run this "
                 "machinery in reverse — given that the ball came out green, which "
                 "urn did it most likely come from? That inversion is Bayes' rule."
        ):
            self.play(*[FadeOut(m) for m in self.mobjects])

            key_head = Text("Key idea", font_size=SMALL, color=ACCENT)
            key_eq = MathTex(
                r"\Pr(B) = \sum_{k=1}^{n} \Pr(A_k)\,\Pr(B \mid A_k)",
                font_size=BODY, color=INK,
            )
            key_sub = Text("Divide into cases, conquer each, average.",
                           font_size=SMALL, color=MUTED)
            card = VGroup(key_head, key_eq, key_sub).arrange(DOWN, buff=0.4)
            fit_to_frame(card)
            self.play(FadeIn(key_head, shift=DOWN * 0.2), run_time=0.6)
            self.play(Write(key_eq), run_time=1.2)
            self.play(FadeIn(key_sub, shift=UP * 0.1), run_time=0.6)
            self.wait(0.5)

        self.play(*[FadeOut(m) for m in self.mobjects])
