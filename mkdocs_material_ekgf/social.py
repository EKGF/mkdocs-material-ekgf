"""
Social card generator for EKGF documentation sites.

Generates social media preview cards (Open Graph images) by rendering
HTML templates with Playwright, ensuring the social cards look exactly
like the website with the same logos and styling.
"""

from __future__ import annotations

import logging
import os
import re
import tempfile
from pathlib import Path

log = logging.getLogger("mkdocs.material.social")

# Card dimensions (standard Open Graph size)
CARD_WIDTH = 1200
CARD_HEIGHT = 630


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


def generate_card(
    title: str,
    description: str = "",
    output_path: str | Path | None = None,
) -> Path:
    """
    Generate a social card image.

    Args:
        title: Page title
        description: Page description (optional)
        output_path: Path to save the PNG image (optional, uses temp file if not provided)

    Returns:
        Path to the generated PNG image
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise ImportError(
            "Playwright is required for social card generation. "
            "Install it with: pip install 'mkdocs-material-ekgf[social]'"
        ) from e

    # Render the HTML template
    html_content = render_template(title, description)

    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(html_content)
        temp_html_path = f.name

    try:
        # Determine output path
        if output_path is None:
            output_path = Path(tempfile.mktemp(suffix=".png"))
        else:
            output_path = Path(output_path)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Use Playwright to render and screenshot
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT})

            # Navigate to the HTML file
            page.goto(f"file://{temp_html_path}")

            # Wait for fonts to load
            page.wait_for_load_state("networkidle")

            # Take screenshot
            page.screenshot(path=str(output_path), type="png")

            browser.close()

        log.debug(f"Generated social card: {output_path}")
        return output_path

    finally:
        # Clean up temporary HTML file
        os.unlink(temp_html_path)


def generate_card_async(
    title: str,
    description: str = "",
    output_path: str | Path | None = None,
) -> Path:
    """
    Generate a social card image asynchronously.

    Args:
        title: Page title
        description: Page description (optional)
        output_path: Path to save the PNG image (optional, uses temp file if not provided)

    Returns:
        Path to the generated PNG image
    """
    try:
        import asyncio

        from playwright.async_api import async_playwright
    except ImportError as e:
        raise ImportError(
            "Playwright is required for social card generation. "
            "Install it with: pip install 'mkdocs-material-ekgf[social]'"
        ) from e

    async def _generate():
        # Render the HTML template
        html_content = render_template(title, description)

        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(html_content)
            temp_html_path = f.name

        try:
            # Determine output path
            nonlocal output_path
            if output_path is None:
                output_path = Path(tempfile.mktemp(suffix=".png"))
            else:
                output_path = Path(output_path)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Use Playwright to render and screenshot
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(viewport={"width": CARD_WIDTH, "height": CARD_HEIGHT})

                # Navigate to the HTML file
                await page.goto(f"file://{temp_html_path}")

                # Wait for fonts to load
                await page.wait_for_load_state("networkidle")

                # Take screenshot
                await page.screenshot(path=str(output_path), type="png")

                await browser.close()

            log.debug(f"Generated social card: {output_path}")
            return output_path

        finally:
            # Clean up temporary HTML file
            os.unlink(temp_html_path)

    return asyncio.run(_generate())
