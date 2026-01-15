# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when
working with code in this repository.

## Project overview

This is the **MkDocs Material EKGF Theme** - a custom Material for
MkDocs theme for EKGF (Enterprise Knowledge Graph Forum) documentation
websites. It is published as a Python package on PyPI.

## Commands

### Installation

```bash
uv sync                   # Install Python dependencies
npm install               # Install Node.js dev tools (husky, commitlint)
```

### Development

```bash
uv run ruff check .       # Lint Python code
uv run ruff format .      # Format Python code
npm run lint:md           # Markdown linting
```

### Building

```bash
uv build                  # Build package for distribution
```

## Architecture

- **mkdocs_material_ekgf/** - Python package source
  - `__init__.py` - Plugin entry point and version
  - `assets/` - Static assets (CSS, JS, images)
  - `partials/` - Jinja2 template overrides
- **pyproject.toml** - Package metadata and dependencies
- **dist/** - Built package output

## Critical conventions

### Markdown formatting

- Maximum line length: 70 characters
- Use `-` for unordered lists
- Sentence case for headers (not Title Case)

### Git workflow

- **NEVER execute `git push`** - users must push manually
- **NEVER bypass hooks** with `--no-verify`
- **NEVER use `git merge`** - always use `git rebase` for linear
  history
- Commit only when explicitly requested

For commit message format, see [CONTRIBUTING.md](.github/CONTRIBUTING.md)

### Versioning

Update `__version__` in `mkdocs_material_ekgf/__init__.py` before
releasing. The CI/CD pipeline publishes to PyPI on push to main.

## Dependencies

- Python 3.14.2+ with `uv` package manager
- Node.js for dev tools (commitlint, markdownlint, prettier)
