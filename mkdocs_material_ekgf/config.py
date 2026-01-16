"""Configuration for the Material EKGF plugin."""

from mkdocs.config.base import Config
from mkdocs.config.config_options import Type


class MaterialEkgfConfig(Config):
    """Configuration options for the Material EKGF plugin."""

    social_cards = Type(bool, default=False)
    social_cards_dir = Type(str, default="assets/images/social")
