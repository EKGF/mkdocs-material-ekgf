VIRTUAL_ENV := ./.venv
PYTHON_VERSION := 3.14.2
UV := uv

# OS detection
ifeq ($(OS),Windows_NT)
	YOUR_OS := Windows
	MAKE := make
else
	YOUR_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
	# Check if gmake exists, otherwise fall back to make
	MAKE := $(shell command -v gmake >/dev/null 2>&1 && echo gmake || echo make)
endif

.PHONY: all
all: lint build

.PHONY: info
info:
	@echo "Operating System  : ${YOUR_OS}"
	@echo "Python version    : $(PYTHON_VERSION)"
	@echo "uv version        : $$($(UV) --version)"
	@echo "make version      : $$($(MAKE) --version | head -n 1)"

.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf dist/ 2>/dev/null || true
	@rm -rf build/ 2>/dev/null || true
	@rm -rf *.egg-info 2>/dev/null || true
	@rm -rf .venv 2>/dev/null || true
	@rm -rf .ruff_cache 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

.PHONY: install
install: venv-ensure
	@echo "Installing dependencies..."
	$(UV) sync

.PHONY: venv-ensure
venv-ensure:
	@if [ ! -d ".venv" ] || ! ./.venv/bin/python --version 2>/dev/null | grep -q "$(PYTHON_VERSION)"; then \
		echo "Creating/Recreating venv with Python $(PYTHON_VERSION)"; \
		$(UV) venv --python $(PYTHON_VERSION); \
	else \
		echo "Venv exists with correct Python version"; \
	fi

.PHONY: lint
lint: venv-ensure
	@echo "Running all linters..."
	$(UV) run ruff check .
	$(UV) run ruff format --check .
	pnpm run lint:md

.PHONY: format
format: venv-ensure
	@echo "Formatting code..."
	$(UV) run ruff check --fix .
	$(UV) run ruff format .
	pnpm exec prettier --write "**/*.md"

.PHONY: build
build: venv-ensure clean
	@echo "Building package..."
	$(UV) build

.PHONY: bump
bump:
	@echo "Bumping patch version..."
	@$(UV) run python3 -c "import re; \
	path = 'mkdocs_material_ekgf/__init__.py'; \
	content = open(path).read(); \
	v = re.search(r'__version__ = \"(\d+\.\d+\.)(\d+)\"', content); \
	new_v = v.group(1) + str(int(v.group(2)) + 1); \
	new_content = re.sub(r'__version__ = \".*?\"', f'__version__ = \"{new_v}\"', content); \
	open(path, 'w').write(new_content); \
	print(f'Bumped version to {new_v}')"

.PHONY: publish-test
publish-test: build
	@echo "Publishing to TestPyPI..."
	$(UV) run twine upload --repository testpypi dist/*

.PHONY: publish
publish: build
	@echo "Publishing to PyPI..."
	$(UV) run twine upload dist/*
