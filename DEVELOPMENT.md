# Development Guide

This guide explains how to set up the development environment for
mkdocs-material-ekgf.

## Prerequisites

- Python 3.14.2 (managed by `uv`)
- Node.js and pnpm (for Husky, Commitlint, Prettier)
- Git

## Initial Setup

### 1. Install UV

UV is a fast Python package installer and resolver:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS:

```bash
brew install uv
```

### 2. Clone the Repository

```bash
git clone https://github.com/EKGF/mkdocs-material-ekgf.git
cd mkdocs-material-ekgf
```

### 3. Install Python Dependencies

UV will automatically use the Python version specified in
`.python-version`:

```bash
# Install package in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

### 4. Install Node.js Dependencies

```bash
# Install pnpm if you don't have it
npm install -g pnpm

# Install dependencies (includes Husky, Commitlint, Prettier)
pnpm install
```

### 5. Initialize Husky

Husky manages Git hooks for pre-commit checks and commit message
linting:

```bash
pnpm prepare
```

This sets up:

- Pre-commit hook: Runs ruff and markdownlint on staged files
- Commit-msg hook: Validates commit messages follow Angular
  convention

## Development Workflow

### Running Linters

**Python (Ruff):**

```bash
# Check code
uv run ruff check .

# Format code
uv run ruff format .

# Check formatting without modifying
uv run ruff format --check .
```

**Markdown (Markdownlint):**

```bash
# Lint all markdown files
pnpm run lint:md

# Or use the script directly
markdownlint '**/*.md' --ignore node_modules --ignore .husky --ignore site
```

**All linters:**

```bash
pnpm run lint
```

### Code Style

#### Python

- **Line length**: 100 characters
- **Quote style**: Double quotes
- **Indentation**: 4 spaces
- **Target**: Python 3.14

Configured in `pyproject.toml` under `[tool.ruff]`.

#### Markdown

- **Line length**: 70 characters for prose
- **Prose wrapping**: Always wrap at 70 chars
- **Code blocks**: No line length limit

Configured in `.prettierrc.json` and `.markdownlint.json`.

#### JavaScript/HTML/CSS

- **Indentation**: 2 spaces
- **Charset**: UTF-8

Configured in `.editorconfig`.

### Git Commit Messages

Follow the Angular Conventional Commits format:

```text
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `build`: Build system changes
- `ci`: CI/CD changes
- `perf`: Performance improvements

**Examples:**

```bash
git commit -m "feat(cards): add new background image options"
git commit -m "fix(header): correct OMG logo alignment in mobile"
git commit -m "docs(readme): update installation instructions"
```

The commit-msg hook will validate your commit message format.

### Pre-commit Checks

Before each commit, Husky runs:

1. **Python files**: Ruff checks and format validation
2. **Markdown files**: Markdownlint validation

If any check fails, the commit is blocked. Fix the issues and try
again.

**To bypass hooks temporarily (not recommended):**

```bash
git commit --no-verify
```

## Testing Changes

### Test Locally with a Sample Site

1. Install package in editable mode:

```bash
uv pip install -e .
```

1. Find installation path:

```bash
python3 -c "import mkdocs_material_ekgf, os; print(os.path.dirname(mkdocs_material_ekgf.__file__))"
```

1. Use in a test MkDocs site:

   Edit `mkdocs.yml`:

```yaml
plugins:
  - material-ekgf
```

1. Serve and test:

```bash
cd /path/to/test/site
mkdocs serve
```

### Test with EKGF Sites

Test with actual EKGF documentation sites:

```bash
# Test with ekg-principles
cd ~/Work/ekg-principles
# Update mkdocs.yml to use the package
mkdocs serve

# Test with ekg-method
cd ~/Work/ekg-method
# Update mkdocs.yml to use the package
mkdocs serve
```

## Building the Package

### Build Wheel and Source Distribution

```bash
# Install build tool
uv pip install build

# Build package
python -m build
```

This creates files in `dist/`:

- `mkdocs_material_ekgf-1.0.0-py3-none-any.whl`
- `mkdocs_material_ekgf-1.0.0.tar.gz`

### Install from Local Build

```bash
uv pip install dist/mkdocs_material_ekgf-1.0.0-py3-none-any.whl
```

## Publishing

### Publish to PyPI (when ready)

1. Install twine:

```bash
uv pip install twine
```

1. Build package:

```bash
python -m build
```

1. Upload to TestPyPI (for testing):

```bash
twine upload --repository testpypi dist/*
```

1. Test installation from TestPyPI:

```bash
uv pip install --index-url https://test.pypi.org/simple/ mkdocs-material-ekgf
```

1. Upload to PyPI (production):

```bash
twine upload dist/*
```

## Project Structure

```text
mkdocs-material-ekgf/
├── .editorconfig              # Editor configuration
├── .gitignore                 # Git ignore rules
├── .husky/                    # Git hooks
│   ├── commit-msg             # Commit message validation
│   └── pre-commit             # Pre-commit checks
├── .markdownlint.json         # Markdown linting rules
├── .markdownlintignore        # Markdown lint ignore
├── .prettierrc.json           # Prettier configuration
├── .python-version            # Python version (3.14.2)
├── CHANGELOG.md               # Version history
├── DEVELOPMENT.md             # This file
├── INTEGRATION.md             # Integration guide
├── LICENSE                    # MIT License
├── MANIFEST.in                # Package manifest
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
├── SUMMARY.md                 # Project summary
├── commitlint.config.js       # Commitlint configuration
├── mkdocs_material_ekgf/      # Theme package
│   ├── __init__.py
│   ├── main.html
│   ├── assets/
│   │   ├── javascripts/
│   │   └── stylesheets/
│   └── partials/
├── package.json               # Node.js dependencies
└── pyproject.toml             # Python project config
```

## Troubleshooting

### UV Issues

**Problem**: UV command not found

**Solution**: Reinstall UV or ensure it's in your PATH:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or ~/.zshrc
```

### Ruff Issues

**Problem**: Ruff not found or version issues

**Solution**: Reinstall dev dependencies:

```bash
uv pip install -e ".[dev]"
```

### Husky Issues

**Problem**: Git hooks not running

**Solution**: Reinitialize Husky:

```bash
pnpm install
pnpm prepare
```

### Python Version Issues

**Problem**: Wrong Python version

**Solution**: UV will automatically download and use Python
3.14.2 based on `.python-version`

## Best Practices

1. **Always run linters before committing** (hooks do this
   automatically)
2. **Write descriptive commit messages** following Angular
   convention
3. **Test changes with actual EKGF sites** before publishing
4. **Update CHANGELOG.md** for all notable changes
5. **Keep line lengths under limits** (70 for prose, 100 for
   code)
6. **Use semantic versioning** for releases

## Getting Help

- **Issues**: [GitHub
  Issues](https://github.com/EKGF/mkdocs-material-ekgf/issues)
- **Discussions**: [GitHub
  Discussions](https://github.com/EKGF/mkdocs-material-ekgf/discussions)
- **EKGF Forum**: [OMG EKGF](https://omg.org)
