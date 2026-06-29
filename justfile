# Build configuration
outdir     := "output"
main       := "UndergraduateProbabilityI"
latex      := "pdflatex"
latexflags := "-interaction=nonstopmode -halt-on-error"
pandoc     := "pandoc"
open_cmd   := "open"

# Chapter order — mirrors the \include sequence in the main .tex.
# (appendix is intentionally excluded; it is commented out in the main file.)
md_files := "chapters/preface.md \
chapters/sets_and_functions.md \
chapters/combinatorics.md \
chapters/probability_models.md \
chapters/conditional_probability.md \
chapters/discrete_random_variables.md \
chapters/discrete_expectations.md \
chapters/discrete_vectors.md \
chapters/continuous_random_variables.md \
chapters/derived_distributions.md \
chapters/expectations_and_bounds.md \
chapters/random_vectors.md \
chapters/empirical_sums.md"

# Print available recipes (default)
default:
    @just --list

# Build either the LaTeX book or the Markdown sidecars.
#   just build latex   -> output/{{main}}.pdf
#   just build md      -> output/{{main}}_sidecars.pdf
build kind:
    @just _build-{{kind}}

# View either compiled PDF (builds first if needed).
#   just view latex
#   just view md
view kind:
    @just _view-{{kind}}

# --- LaTeX ----------------------------------------------------------------

_build-latex:
    mkdir -p {{outdir}}/chapters
    {{latex}} {{latexflags}} -output-directory={{outdir}} {{main}}.tex
    -cd {{outdir}} && makeindex {{main}}.idx
    {{latex}} {{latexflags}} -output-directory={{outdir}} {{main}}.tex
    {{latex}} {{latexflags}} -output-directory={{outdir}} {{main}}.tex

_view-latex: _build-latex
    {{open_cmd}} {{outdir}}/{{main}}.pdf

# --- Markdown sidecars ----------------------------------------------------

_build-md:
    mkdir -p {{outdir}}
    {{pandoc}} {{md_files}} \
        --top-level-division=chapter \
        --toc \
        -V geometry:margin=1in \
        -o {{outdir}}/{{main}}_sidecars.pdf

_view-md: _build-md
    {{open_cmd}} {{outdir}}/{{main}}_sidecars.pdf

# --- Derived documents ----------------------------------------------------

# Generate a derived document. Currently: just concept md -> CONCEPT_MAP.md
concept kind:
    @just _concept-{{kind}}

_concept-md:
    python3 scripts/concept_graph.py

# --- Housekeeping ---------------------------------------------------------

clean:
    rm -rf {{outdir}}
