"""
Social card generator for EKGF documentation sites.

Generates social media preview cards (Open Graph images) by rendering
HTML templates with Playwright, ensuring the social cards look exactly
like the website with the same logos and styling.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import shutil
import tempfile
from pathlib import Path

log = logging.getLogger("mkdocs.material.social")

# Card dimensions (standard Open Graph size)
CARD_WIDTH = 1200
CARD_HEIGHT = 630

# Persistent cache directory (survives site/ rebuilds)
_DEFAULT_CACHE_DIR = ".cache/social-cards"


def get_partials_dir() -> Path:
    """Get the path to the partials directory."""
    return Path(__file__).parent / "partials"


def load_template() -> str:
    """Load the social card HTML template."""
    template_path = get_partials_dir() / "social-card.html"
    with open(template_path, encoding="utf-8") as f:
        return f.read()


def load_partial(name: str) -> str:
    """Load a partial HTML file and strip Jinja2 comments."""
    partial_path = get_partials_dir() / name
    with open(partial_path, encoding="utf-8") as f:
        content = f.read()
    # Strip Jinja2 comments {# ... #}
    return re.sub(r"\{#.*?#\}", "", content, flags=re.DOTALL)


def render_template(title: str, description: str = "") -> str:
    """
    Render the social card template with the given title and description.

    Args:
        title: Page title
        description: Page description (optional)

    Returns:
        Rendered HTML string
    """
    template = load_template()

    # Load and embed partials
    ekgf_logo = load_partial("ekgf-logo.html")
    omg_logo = load_partial("omg-logo.html")

    html = template.replace('{% include "partials/ekgf-logo.html" %}', ekgf_logo)
    html = html.replace('{% include "partials/omg-logo.html" %}', omg_logo)

    # Replace template variables
    html = html.replace("{{ title }}", title)

    if description:
        html = html.replace("{% if description %}", "")
        html = html.replace("{% endif %}", "")
        html = html.replace("{{ description }}", description)
    else:
        # Remove the description block entirely
        html = re.sub(
            r"\{% if description %\}.*?\{% endif %\}",
            "",
            html,
            flags=re.DOTALL,
        )

    return html


def _content_hash(html_content: str) -> str:
    """Compute a short SHA-256 hex digest of the rendered HTML."""
    return hashlib.sha256(html_content.encode("utf-8")).hexdigest()[:16]


class CardRenderer:
    """Reuses a single Playwright browser across all card generations.

    Cards are cached in a persistent directory (outside site/) so that
    subsequent builds can skip Playwright entirely for unchanged pages.
    """

    def __init__(self, cache_dir: str | Path | None = None):
        self._playwright = None
        self._browser = None
        self._page = None
        self._cache_dir = Path(cache_dir) if cache_dir else Path(_DEFAULT_CACHE_DIR)
        self._generated = 0
        self._cached = 0

    def _ensure_browser(self):
        if self._page is not None:
            return
        from playwright.sync_api import sync_playwright

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch()
        self._page = self._browser.new_page(
            viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT}
        )

    def _cache_png_path(self, content_hash: str) -> Path:
        """Return the cache file path for a given content hash."""
        return self._cache_dir / f"{content_hash}.png"

    def generate(
        self,
        title: str,
        description: str = "",
        output_path: str | Path | None = None,
    ) -> tuple[Path, bool]:
        """Generate a social card, skipping Playwright if cached.

        Returns:
            Tuple of (path to PNG, True if newly generated / False if cached)
        """
        html_content = render_template(title, description)
        content_hash = _content_hash(html_content)

        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".png"))
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check the persistent cache
        cached_png = self._cache_png_path(content_hash)
        if cached_png.exists():
            shutil.copy2(cached_png, output_path)
            self._cached += 1
            return output_path, False

        # Cache miss — render with Playwright
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(html_content)
            temp_html_path = f.name

        try:
            self._ensure_browser()
            self._page.goto(f"file://{temp_html_path}")
            self._page.wait_for_load_state("networkidle")
            self._page.screenshot(path=str(output_path), type="png")
        finally:
            os.unlink(temp_html_path)

        # Store in persistent cache
        shutil.copy2(output_path, cached_png)
        self._generated += 1
        return output_path, True

    def close(self):
        """Shut down the browser and Playwright, log summary."""
        if self._generated or self._cached:
            log.info(
                f"Social cards: {self._generated} generated, "
                f"{self._cached} cached"
            )
        if self._page is not None:
            self._page.close()
            self._page = None
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None


# Keep the old function signature for backward compatibility
def generate_card(
    title: str,
    description: str = "",
    output_path: str | Path | None = None,
) -> Path:
    """Generate a social card image (standalone, launches its own browser)."""
    renderer = CardRenderer()
    try:
        path, _ = renderer.generate(title, description, output_path)
        return path
    finally:
        renderer.close()
