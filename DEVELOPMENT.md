# Development Guide

This guide explains how to set up the development environment for
mkdocs-material-ekgf.

## Prerequisites

- Python 3.14.2 (managed by `uv`)
- Node.js and pnpm (for Husky, Commitlint, Prettier)
- Git
- **GNU Make** (`gmake` on macOS/Linux)

## Initial Setup

### GitHub Codespaces (Recommended)

The easiest way to get started is to open this repository in a GitHub
Codespace. It comes pre-configured with all necessary tools (uv,
pnpm, make, etc.).

1. Click the **Code** button on the GitHub repository.
2. Select the **Codespaces** tab.
3. Click **Create codespace on main**.

Wait for the setup to complete, and you'll have a fully functional
development environment.

### Local Setup

#### 1. Install UV

UV is a fast Python package installer and resolver:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or on macOS:

```bash
brew install uv
```

### 2. Install GNU Make (if needed)

On macOS:

```bash
brew install make
```

*Note: This installs GNU Make as `gmake`.*

### 3. Clone the Repository

```bash
git clone https://github.com/EKGF/mkdocs-material-ekgf.git
cd mkdocs-material-ekgf
```

### 4. Install Python Dependencies

UV will automatically use the Python version specified in
`.python-version`:

```bash
# Install package in editable mode with dev dependencies
uv sync --all-extras
```

### 5. Install Node.js Dependencies

```bash
# Install pnpm if you don't have it
npm install -g pnpm

# Install dependencies (includes Husky, Commitlint, Prettier)
pnpm install
```

### 6. Initialize Husky

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
gmake lint
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
uv sync
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
uv run mkdocs serve
```

### Test with EKGF Sites

Test with actual EKGF documentation sites:

```bash
# Test with ekg-principles
cd ~/Work/ekg-principles
# Update mkdocs.yml to use the package
uv run mkdocs serve

# Test with ekg-method
cd ~/Work/ekg-method
# Update mkdocs.yml to use the package
uv run mkdocs serve
```

## GitHub Actions

The repository includes two workflows:

1. **CI (`ci.yml`)**: Runs on every push and pull request to `main`.
   - Lints Python code with Ruff
   - Checks formatting
   - Builds the package to verify it's valid
2. **Release and Publish (`publish.yml`)**: Runs on every push to
   `main`.
   - Detects if the version in `__init__.py` has changed.
   - If changed, it creates a GitHub Tag and Release.
   - Automatically publishes the package to PyPI.

## Automatic Publishing (Recommended)

This project uses an automated release workflow. Tags are only created
by CI once a PR is merged into `main`.

1. Run the bump command on your branch:

```bash
gmake bump
```

1. This will commit the version change and push your current branch.
2. Open a Pull Request to `main`.
3. Once merged, GitHub Actions will:
   - Build the package and verify the version.
   - If the version is new, it will create a GitHub Tag and Release.
   - It will automatically publish the package to PyPI.

## Building the Package Manually

### Build Wheel and Source Distribution

```bash
# Build package using Makefile
gmake build
```

This creates files in `dist/`:

- `mkdocs_material_ekgf-X.Y.Z-py3-none-any.whl`
- `mkdocs_material_ekgf-X.Y.Z.tar.gz`

### Install from Local Build

```bash
uv pip install dist/mkdocs_material_ekgf-X.Y.Z-py3-none-any.whl
```

## Manual Publishing

### Publish to PyPI (when ready)

1. Build package:

```bash
gmake build
```

1. Upload to TestPyPI (for testing):

```bash
gmake publish-test
```

1. Upload to PyPI (production):

```bash
gmake publish
```

## Project Structure

```text
mkdocs-material-ekgf/
├── .devcontainer/             # GitHub Codespaces setup
├── .editorconfig              # Editor configuration
├── .github/workflows/        # GitHub Actions (CI & Publish)
├── .gitignore                 # Git ignore rules
├── .husky/                    # Git hooks
│   ├── commit-msg             # Commit message validation
│   └── pre-commit             # Pre-commit checks
├── .markdownlint.json         # Markdown linting rules
├── .markdownlintignore        # Markdown lint ignore
├── .prettierrc.json           # Prettier configuration
├── .python-version            # Python version (3.14.2)
├── .vscode/                   # VS Code shared settings
├── DEVELOPMENT.md             # This file
├── INTEGRATION.md             # Integration guide
├── LICENSE                    # MIT License
├── MANIFEST.in                # Package manifest
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Main documentation
├── STATUS.md                  # Current project status
├── SUMMARY.md                 # Project overview
├── Makefile                   # GNU Makefile
├── commitlint.config.js       # Commitlint configuration
├── mkdocs_material_ekgf/      # Theme package & Plugin
│   ├── __init__.py           # Plugin implementation
│   ├── main.html             # Base template overrides
│   ├── mkdocs_theme.yml      # Theme metadata
│   ├── assets/               # CSS and JS
│   └── partials/             # Template fragments
├── package.json               # Node.js dependencies
├── pyproject.toml             # Hatchling & uv configuration
└── uv.lock                    # Dependency lockfile
```

## Troubleshooting

### GNU Make Issues

**Problem**: `make` command fails with syntax errors or version
issues.

**Solution**: Use `gmake` on macOS and Linux. Ensure GNU Make is
installed.

```bash
# macOS
brew install make
gmake --version
```

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
uv sync --all-extras
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
