# Quick Start Guide

Get the EKGF theme running in your MkDocs site in under 5 minutes.

## Step 1: Install the Package

### Local Development Install

```bash
cd ~/Work/mkdocs-material-ekgf
uv sync
```

This installs the package in "editable" mode, meaning changes to the
theme files will be reflected immediately.

### From Git Repository (Future)

```bash
uv add git+https://github.com/EKGF/mkdocs-material-ekgf.git
```

### From PyPI (When Published)

```bash
uv add mkdocs-material-ekgf
```

## Step 2: Update Your mkdocs.yml

Add the `material-ekgf` plugin to your `mkdocs.yml`:

```yaml
site_name: Your EKGF Site
theme:
  name: material
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

The plugin automatically:

1. Sets the correct `custom_dir` to override Material templates.
2. Adds the EKGF theme CSS and JavaScript assets.
3. Configures recommended features (tabs, sticky header, etc.).

## Step 3: Test Locally

```bash
cd /path/to/your/mkdocs/site
mkdocs serve
```

Open <http://127.0.0.1:8000> and verify:

- ✓ EKGF logo appears in header (left side)
- ✓ Site title is centered in header
- ✓ OMG logo appears in header (right side)
- ✓ Navigation tabs display below header
- ✓ Search box appears in tabs row (right side)
- ✓ Theme toggle works (sun/moon icon)
- ✓ Footer matches EKGF design

## Step 4: Build for Production

```bash
mkdocs build
```

The site will be generated in the `site/` directory.

## Troubleshooting

### Theme Not Loading

**Problem**: Site looks like default Material theme

**Solution**:

1. Verify package is installed: `uv pip list | grep mkdocs-material-ekgf`
2. Check the `custom_dir` path is correct
3. Ensure Material for MkDocs is installed: `uv pip list | grep mkdocs-material`

### CSS Not Applied

**Problem**: Layout is broken or styles missing

**Solution**:

1. Check you're using Material for MkDocs 9.0.0+:

```bash
uv add mkdocs-material --upgrade
```

1. Clear your browser cache (Cmd+Shift+R on Mac, Ctrl+Shift+R on
   Windows)

### Dark Mode Not Working

**Problem**: Theme toggle doesn't switch themes

**Solution**:

1. Ensure both palette configurations are in `mkdocs.yml`
2. Check browser console for JavaScript errors
3. Verify `refresh_on_toggle_dark_light.js` is loaded

### OMG Logo Not Showing

**Problem**: Only EKGF logo appears, no OMG logo on right

**Solution**:

1. The OMG logo is hidden on mobile/small screens (<960px width)
2. Resize browser window wider or test on desktop
3. Check browser console for errors loading SVG

## Next Steps

1. **Customize Colors**: See [INTEGRATION.md](INTEGRATION.md) for color
   customization
2. **Add Cards**: Use enhanced card components (see
   [INTEGRATION.md](INTEGRATION.md))
3. **Configure SEO**: Add page-specific meta tags in frontmatter
4. **Deploy**: Push to your hosting platform (GitHub Pages, Netlify,
   etc.)

## Example Sites

See these EKGF sites using the theme:

- [EKG Principles](https://principles.ekgf.org) - Original design
  source
- [EKG Method](https://method.ekgf.org) - After migration (planned)
- [EKG Catalog](https://catalog.ekgf.org) - After migration (planned)
- [EKG Maturity](https://maturity.ekgf.org) - After migration (planned)

## Getting Help

- **Full Documentation**: [INTEGRATION.md](INTEGRATION.md)
- **Issues**: [GitHub
  Issues](https://github.com/EKGF/mkdocs-material-ekgf/issues)
- **EKGF Forum**: [OMG EKGF](https://omg.org)
