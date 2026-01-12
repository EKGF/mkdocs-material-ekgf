import os

from mkdocs.plugins import BasePlugin

__version__ = "0.0.8"
__author__ = "Jacobus Geluk"
__email__ = "jacobus.geluk@ekgf.org"
__license__ = "CC BY-SA 4.0"


class MaterialEkgfPlugin(BasePlugin):
    def on_config(self, config, **kwargs):
        # Path to this package
        base_path = os.path.dirname(__file__)

        # 1. Automatically set custom_dir
        theme = config.get("theme")
        if theme:
            if base_path not in theme.dirs:
                theme.dirs.insert(0, base_path)

        # 2. Add our assets to extra_css and extra_javascript
        # Note: These paths must be relative to the docs_dir or site_dir
        # MkDocs will look for them in the theme's directory since we set custom_dir

        if "assets/stylesheets/ekgf-theme.css" not in config.get("extra_css", []):
            config["extra_css"].append("assets/stylesheets/ekgf-theme.css")

        js_assets = [
            "assets/javascripts/images_dark.js",
            "assets/javascripts/refresh_on_toggle_dark_light.js",
        ]

        for js in js_assets:
            if js not in config.get("extra_javascript", []):
                config["extra_javascript"].append(js)

        return config
