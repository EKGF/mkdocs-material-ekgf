# Integration Guide

This guide explains how to integrate the mkdocs-material-ekgf theme
into your EKGF documentation website.

## Prerequisites

- Python 3.8 or higher
- MkDocs 1.5.0 or higher
- Material for MkDocs 9.0.0 or higher

## Installation

### From PyPI (when published)

```bash
uv add mkdocs-material-ekgf
```

### From Local Development

```bash
cd ~/Work/mkdocs-material-ekgf
uv sync
```

### From Git Repository

```bash
uv add git+https://github.com/EKGF/mkdocs-material-ekgf.git
```

## Configuration

### Step 1: Update mkdocs.yml

Add the `material-ekgf` plugin to your plugins list. You don't need to
specify `custom_dir` or add CSS/JS assets manually—the plugin takes
care of it.

```yaml
theme:
  name: material
  language: en
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

### Step 2: Configure Site Metadata

```yaml
site_name: Your Site Name
site_description: Your site description
repo_name: "EKGF/your-repo"
repo_url: https://github.com/EKGF/your-repo
site_url: https://yoursite.ekgf.org
edit_uri: edit/main/docs/
site_author: >-
  Object Management Group (OMG) Enterprise Knowledge Graph Forum
copyright: >-
  Copyright © 2026 EDMCouncil Inc., d/b/a
  Enterprise Data Management Association ("EDMA")
```

### Step 3: Add Extra Configuration

```yaml
extra:
  homepage: https://ekgf.org/quadrants
  generator: false
  social:
    - icon: fontawesome/brands/twitter
      link: https://twitter.com/EKG_Foundation
    - icon: fontawesome/brands/linkedin
      link: https://www.linkedin.com/company/EKGF
    - icon: fontawesome/brands/github
      link: https://github.com/EKGF/your-repo
  analytics:
    provider: google
    property: YOUR-GA-PROPERTY-ID
```

### Step 4: Include Theme Assets

The theme assets are automatically included when you use `custom_dir`.
No additional CSS or JavaScript references are needed in your
`mkdocs.yml`.

## Markdown Extensions

The theme works best with these markdown extensions:

```yaml
markdown_extensions:
  - footnotes
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - meta
  - def_list
  - abbr
  - admonition
  - tables
  - pymdownx.caret
  - pymdownx.mark
  - pymdownx.tilde
  - pymdownx.smartsymbols
  - pymdownx.snippets:
      base_path:
        - .
        - docs
      check_paths: true
  - pymdownx.details
  - pymdownx.magiclink
  - pymdownx.critic
  - pymdownx.emoji:
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
      emoji_index: !!python/name:material.extensions.emoji.twemoji
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
```

## Using Enhanced Card Components

### Process Cards

Create engaging process cards with hero background images:

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
  
  Define your use cases and identify knowledge assets for maximum reuse.
  
  ---
  
  - Strategic planning
  - Use case modeling
  - Asset identification

- <div class="process-card-header process-card-build">
    
    :material-cog-outline:{ .lg }
    
    <div class="process-card-title">
      <strong>[Build](build/)</strong>
      <span class="process-card-subtitle">Construct Knowledge</span>
    </div>
    
  </div>
  
  ---
  
  Create and integrate your knowledge graph components.
  
  ---
  
  - Data modeling
  - Integration
  - Quality assurance

</div>
```

Available background classes:

- `process-card-plan` - Planning imagery
- `process-card-build` - Building/technology imagery
- `process-card-run` - Operations imagery

### Theme Cards

Create thematic cards for principles or concepts:

```markdown
<div class="grid cards theme-cards" markdown>

- <div class="theme-card-header theme-card-transparency">
    
    :material-eye-outline:{ .lg }
    
    <div class="theme-card-title">
      <strong>[Transparency](theme/transparency/)</strong>
    </div>
    
  </div>
  
  Clear visibility into data, processes, and decisions.
  
  [Learn more](theme/transparency/)

- <div class="theme-card-header theme-card-openness">
    
    :material-open-source-initiative:{ .lg }
    
    <div class="theme-card-title">
      <strong>[Openness](theme/openness/)</strong>
    </div>
    
  </div>
  
  Open standards and collaborative knowledge sharing.
  
  [Learn more](theme/openness/)

</div>
```

Available theme card backgrounds:

- `theme-card-transparency`
- `theme-card-openness`
- `theme-card-sustainability`
- `theme-card-fairness`
- `theme-card-accountability`
- `theme-card-digital-assets`
- `theme-card-composable-business`
- And more (see CSS for complete list)

### Objective Badges

Create circular letter badges for objectives:

```markdown
<span class="objective-badge" data-letter="A"></span> **Objective A**

Or in tables:

| Objective | Description |
|-----------|-------------|
| <span class="objective-badge-sm" data-letter="A"></span> Align | Align business goals |
| <span class="objective-badge-sm" data-letter="B"></span> Build | Build capabilities |
```

## Testing Your Integration

1. Serve Locally:

```bash
uv run mkdocs serve
```

1. Check the Following:

- [ ] Header displays EKGF logo, site title, and OMG logo
- [ ] Navigation tabs appear with search box
- [ ] Theme toggle (sun/moon icon) works
- [ ] Footer matches EKGF design
- [ ] Dark/light mode switch works correctly
- [ ] Cards render properly if used
- [ ] Search functionality works

1. Build for Production:

```bash
uv run mkdocs build
```

## Troubleshooting

### Theme Not Loading

If the theme doesn't load, verify:

1. Package is installed: `uv pip list | grep mkdocs-material-ekgf`
2. The `material-ekgf` plugin is in your `mkdocs.yml`
3. Material for MkDocs is installed: `uv pip list | grep mkdocs-material`

### Styles Not Applying

Check that you're using Material for MkDocs 9.0.0 or higher:

```bash
uv add mkdocs-material --upgrade
```

### Cards Not Rendering

Ensure you have these extensions enabled:

- `attr_list`
- `md_in_html`
- `pymdownx.emoji`

## Migration from Existing Sites

### From ekg-principles

1. Remove `docs-overrides/` directory
2. Remove custom CSS from `extra_css`
3. Remove custom JavaScript from `extra_javascript`
4. Update `mkdocs.yml` as shown above
5. Install the package
6. Test locally

### From ekg-method, ekg-catalog, ekg-maturity

Same steps as above. These sites should see immediate visual
improvements.

## Getting Help

- **Issues**: [GitHub
  Issues](https://github.com/EKGF/mkdocs-material-ekgf/issues)
- **Documentation**: [EKGF Documentation](https://ekgf.org)
- **Community**: [OMG EKGF Forum](https://omg.org)
