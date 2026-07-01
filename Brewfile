# Brewfile — system (Homebrew) tooling for the Probability course repo.
# Install everything with:  brew bundle
#
# Python itself is managed by uv (`uv python`), so it is not listed here.

brew "just"      # task runner — drives the justfile recipes
brew "uv"        # Python environment / dependency manager (see pyproject.toml)
brew "pandoc"    # Markdown sidecar build:  just build md
brew "gh"        # GitHub CLI:  just deploy, just publish-pdf

# LaTeX toolchain for building the book PDF locally (just build latex /
# just publish-pdf). MacTeX-no-gui is the full distribution and includes the
# packages the book uses (tikz, pgfplots, pageslts). If you already have a TeX
# install (e.g. full MacTeX), drop this line.
cask "mactex"
