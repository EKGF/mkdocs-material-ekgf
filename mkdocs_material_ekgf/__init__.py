import os

from mkdocs.plugins import BasePlugin

__version__ = "0.0.13"
__author__ = "Jacobus Geluk"
__email__ = "jacobus.geluk@ekgf.org"
__license__ = "CC BY-SA 4.0"


class MaterialEkgfPlugin(BasePlugin):
    def on_config(self, config, **kwargs):
        # Path to this package
        base_path = os.path.dirname(__file__)

        # 1. Add our template dir in the right position:
        #    - AFTER any local custom_dir (so local overrides take priority)
        #    - BEFORE Material's built-in templates (so plugin templates override Material defaults)
        # Order should be: [custom_dir, plugin_dir, material_built_in]
        theme = config.get("theme")
        if theme:
            if base_path not in theme.dirs:
                if len(theme.dirs) > 1:
                    # custom_dir exists at [0], Material at [1+], insert plugin at [1]
                    theme.dirs.insert(1, base_path)
                else:
                    # No custom_dir, just Material at [0], insert plugin at [0]
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
