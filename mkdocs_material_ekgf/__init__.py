import logging
import os
import posixpath

from mkdocs.plugins import BasePlugin

from .config import MaterialEkgfConfig

__version__ = "0.0.21"
__author__ = "Jacobus Geluk"
__email__ = "jacobus.geluk@ekgf.org"
__license__ = "CC BY-SA 4.0"

log = logging.getLogger("mkdocs.material.ekgf")


class MaterialEkgfPlugin(BasePlugin[MaterialEkgfConfig]):
    def on_config(self, config, **kwargs):
        # Path to this package
        base_path = os.path.dirname(__file__)

        # Log social cards status
        if self.config.social_cards:
            log.info("Social cards generation enabled")

        # 1. Add our template dir in the right position:
        #    - AFTER any local custom_dir (so local overrides take priority)
        #    - BEFORE Material's built-in templates (so plugin templates override Material defaults)
        # Order should be: [custom_dir, plugin_dir, material_built_in, mkdocs_base]
        theme = config.get("theme")
        if theme:
            if base_path not in theme.dirs:
                # Check if custom_dir is set by seeing if first entry is Material's templates
                first_dir = theme.dirs[0] if theme.dirs else ""
                first_is_material = "material" in first_dir and "templates" in first_dir
                if first_is_material:
                    # No custom_dir - insert plugin at [0] to override Material
                    theme.dirs.insert(0, base_path)
                else:
                    # custom_dir at [0] - insert plugin at [1] (after custom_dir)
                    theme.dirs.insert(1, base_path)

        # 2. Add our assets to extra_css and extra_javascript
        # Note: These paths must be relative to the docs_dir or site_dir
        # MkDocs will look for them in the theme's directory since we set custom_dir

        if "assets/stylesheets/ekgf-theme.css" not in config.get("extra_css", []):
            config["extra_css"].append("assets/stylesheets/ekgf-theme.css")

        js_assets = [
            "assets/javascripts/images_dark.js",
            "assets/javascripts/refresh_on_toggle_dark_light.js",
            "assets/javascripts/nav-section-links.js",
            "assets/javascripts/tabbed-url-sync.js",
        ]

        for js in js_assets:
            if js not in config.get("extra_javascript", []):
                config["extra_javascript"].append(js)

        # Store config for later use
        self._mkdocs_config = config

        return config

    def on_page_markdown(self, markdown, *, page, config, files):
        """Generate social card for each page."""
        if not self.config.social_cards:
            return markdown

        # Skip if no site_url configured
        if not config.site_url:
            log.warning("social_cards enabled but site_url not set - cards won't be linked")
            return markdown

        try:
            from .social import generate_card
        except ImportError:
            log.warning(
                "Playwright not installed - social cards disabled. "
                "Install with: pip install 'mkdocs-material-ekgf[social]'"
            )
            self.config.social_cards = False
            return markdown

        # Get page title and description
        title = page.meta.get("title", page.title) if page.meta else page.title
        description = ""
        if page.meta and page.meta.get("description"):
            description = page.meta["description"]
        elif config.site_description:
            description = config.site_description

        # Determine output path
        cards_dir = self.config.social_cards_dir
        page_path = page.file.src_path.replace(".md", ".png")
        output_rel_path = posixpath.join(cards_dir, page_path)
        output_abs_path = os.path.join(config.site_dir, output_rel_path)

        # Generate the card
        try:
            log.info(f"Generating social card: {page.file.src_path}")
            generate_card(title, description, output_abs_path)

            # Store the card path for injection in on_post_page
            if not hasattr(page, "meta") or page.meta is None:
                page.meta = {}
            page.meta["_social_card_path"] = output_rel_path

        except Exception as e:
            log.error(f"Failed to generate social card for {page.file.src_path}: {e}")

        return markdown

    def on_post_page(self, output, *, page, config):
        """Inject social card meta tags into the page HTML."""
        if not self.config.social_cards:
            return output

        if not config.site_url:
            return output

        # Get the card path
        card_path = page.meta.get("_social_card_path") if page.meta else None
        if not card_path:
            return output

        # Build the full URL to the card
        card_url = posixpath.join(config.site_url, card_path)

        # Build meta tags
        meta_tags = [
            f'<meta property="og:image" content="{card_url}" />',
            '<meta property="og:image:type" content="image/png" />',
            '<meta property="og:image:width" content="1200" />',
            '<meta property="og:image:height" content="630" />',
            '<meta name="twitter:card" content="summary_large_image" />',
            f'<meta name="twitter:image" content="{card_url}" />',
        ]

        # Find </head> and inject meta tags before it
        head_end = output.find("</head>")
        if head_end != -1:
            meta_html = "\n    ".join(meta_tags)
            output = f"{output[:head_end]}    {meta_html}\n{output[head_end:]}"

        return output
