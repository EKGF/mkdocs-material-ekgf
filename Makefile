VIRTUAL_ENV := ./.venv
PYTHON_VERSION := 3.14.2
UV := uv

# OS detection
ifeq ($(OS),Windows_NT)
	YOUR_OS := Windows
else
	YOUR_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif

.PHONY: all
all: lint build

.PHONY: info
info:
	@echo "Operating System  : ${YOUR_OS}"
	@echo "Python version    : $(PYTHON_VERSION)"
	@echo "uv version        : $$($(UV) --version)"

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

.PHONY: publish-test
publish-test: build
	@echo "Publishing to TestPyPI..."
	$(UV) run twine upload --repository testpypi dist/*

.PHONY: publish
publish: build
	@echo "Publishing to PyPI..."
	$(UV) run twine upload dist/*
