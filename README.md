# MkDocs Material EKGF Theme

A custom Material for MkDocs theme for EKGF (Enterprise Knowledge
Graph Forum) documentation websites.

## Features

- **Custom Header**: Three-row layout with EKGF logo, centered site
  title, and OMG branding
- **Enhanced Footer**: Matches ekgf.org design with comprehensive
  navigation and social links
- **Advanced Card Components**:
  - Process cards with hero images
  - Theme cards with 4-column responsive layout
  - Objective badges for visual hierarchy
- **Integrated Search**: Custom search box in navigation tabs
- **Dark/Light Mode**: Full theme support with cross-subdomain cookie
  sync
- **SEO Optimized**: Comprehensive meta tags, Open Graph, Twitter
  Cards, and JSON-LD structured data
- **Responsive Design**: Mobile-first approach with optimizations

## Installation

```bash
pip install mkdocs-material-ekgf
```

## Usage

### Basic Configuration

In your `mkdocs.yml`:

```yaml
theme:
  name: material
  # No custom_dir needed! The plugin handles it.

  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: light-blue
      toggle:
        icon: material/weather-night
        name: Switch to dark mode

    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: deep orange
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode

plugins:
  - material-ekgf
  - search
```

## Enhanced Card Layouts

### Process Cards

```markdown
<div class="grid cards process-cards" markdown>

- <div class="process-card-header process-card-plan">
    
    :material-file-document-outline:{ .lg }
    
    <div class="process-card-title">
      <strong>[Plan](plan/)</strong>
      <span class="process-card-subtitle">Design Your EKG</span>
    </div>
    
  </div>
  
  ---
  
  Define your use cases and identify knowledge assets...

</div>
```

### Theme Cards

```markdown
<div class="grid cards theme-cards" markdown>

- <div class="theme-card-header theme-card-transparency">
    
    :material-eye-outline:{ .lg }
    
    <div class="theme-card-title">
      <strong>[Transparency](theme/transparency/)</strong>
    </div>
    
  </div>
  
  Clear visibility into data, processes, and decisions...
  
  [Learn more](theme/transparency/)

</div>
```

## Design Principles

This theme implements the EKGF design language:

- **Consistent Branding**: EKGF and OMG logos across all sites
- **Professional Aesthetics**: Clean, modern design matching ekgf.org
- **Enhanced Readability**: Optimized typography and spacing
- **Accessibility**: WCAG 2.1 AA compliant
- **Performance**: Optimized assets and minimal JavaScript

## Development

### Local Development

```bash
git clone https://github.com/EKGF/mkdocs-material-ekgf.git
cd mkdocs-material-ekgf
pip install -e .
```

### Testing

Test the theme with a sample MkDocs site:

```bash
cd examples/sample-site
mkdocs serve
```

## License

Copyright © 2026 EDMCouncil Inc., d/b/a Enterprise Data Management
Association ("EDMA")

This work is licensed under a Creative Commons Attribution-ShareAlike
4.0 International License.

## Support

For issues, questions, or contributions, please visit:

- [GitHub Issues](https://github.com/EKGF/mkdocs-material-ekgf/issues)
- [EKGF Documentation](https://ekgf.org)

## Acknowledgments

Built on top of [Material for
MkDocs](https://squidfunk.github.io/mkdocs-material/) by Martin
Donath.
