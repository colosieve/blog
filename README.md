# Colonel's Pensieve

Bare-minimum Hugo site with posts and custom slide presentation system.

## What is this?

A minimal Hugo static site generator setup with:
- Basic post functionality
- Custom CSS-based slide presentations
- No external dependencies or themes

## Site Features

### Banner Image

Configurable site banner in `hugo.toml`:

```toml
[params]
  bannerImage = "images/banner.jpg"  # path relative to static/
  bannerAlt = "Site banner"
  bannerHeight = "200px"
```

Features gradient fade (25-75% visible) and centered title overlay.

### Slide Columns

Two-column layout for slides with text + image:

```html
<div class="slide-columns">
<div class="slide-col-main">

Your content here...

</div>
<div class="slide-col-aside">

![Image](url)

</div>
</div>
```

Stacks vertically on mobile.

## Local Development

Requires the extended Hugo binary (tested with v0.150.0).

```bash
# Start development server with live reload
hugo server

# Visit http://localhost:1313
```

> Tip: When cloning this repo for a new site, update the `title` in `hugo.toml` to match your project's name.


### Run as user service

```bash
# install and launch a systemd user service from the repo root
./setup-dev-svc.sh

# inspect logs
journalctl --user -u syslog-hugo.service -f
```

### Cache Busting Implementation

Caching is disabled to prevent stale content during development:

1. **HTML meta tags** in `layouts/_default/baseof.html`:
   ```html
   <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
   <meta http-equiv="Pragma" content="no-cache">
   <meta http-equiv="Expires" content="0">
   ```

2. **CSS timestamp** in `layouts/_default/baseof.html`:
   ```html
   <link rel="stylesheet" href="{{ "css/style.css" | relURL }}?v={{ now.Unix }}">
   ```

3. **Hugo config** in `hugo.toml`:
   ```toml
   [caches]
     [caches.getresource]
       maxAge = 0
   ```

For aggressive cache busting during development:
```bash
hugo server --noHTTPCache --disableFastRender
```

## Deployment

Site can be published via GitHub Pages at https://colosieve.github.io/blog/.

Pushes to the `blog` branch trigger a GitHub Actions workflow for automatic deployment.

## Repository Guidelines

### Project Structure & Module Organization
- `content/posts/` holds Markdown with TOML front matter; rely on `archetypes/default.md` when adding new posts.
- `layouts/_default/` stores the base templates, partials, and slide layout logic; tweak shared markup here before touching individual pages.
- `layouts/shortcodes/` contains helper shortcodes (slides, callouts); keep slide decks co-located with their Markdown in `content/posts/`.
- `static/css/` and `static/js/` expose assets served as-is; update favicons and manifest entries under `static/`.
- `syslog-hugo.service.template` pairs with `setup-dev-svc.sh` to generate the user-level systemd unit; tweak both together when runtime flags change.
- `.github/workflows/deploy.yml` runs the Pages deployment; keep it aligned with local build expectations and Hugo versions noted in this README.
- `incoming/` staging area for draft content awaiting processing into posts.

### Content Publishing Workflow
When processing draft content from `incoming/` into published posts:
1. Read the draft markdown from `incoming/` directory
2. Create a new post in `content/posts/` with proper TOML front matter (title, date, tags, author)
3. Remove personal/non-public setup details while preserving technical content
4. Delete the processed file from `incoming/` after successful post creation
5. Commit both the new post and the removal of the incoming file together

### Build, Test, and Development Commands
- `hugo server --noHTTPCache --disableFastRender` launches a hot-reload dev server with cache busting—use it for authoring and slide checks.
- `hugo` builds the production-ready site in `public/`; clean that directory before committing artifacts.
- `hugo --panicOnWarning --printUnusedTemplates` fails fast on template issues and highlights stale layouts.
- `hugo server --buildDrafts --buildFuture` previews draft or scheduled content prior to publication.
- `./setup-dev-svc.sh` installs the user service for persistent local previews; rerun after editing the template or moving directories.

### Coding Style & Naming Conventions
- Markdown: 80-character soft wrap, Title Case top-level headings, and fenced code blocks with a language hint (` ```bash `).
- Front matter keys stay lowercase snake_case, dates use ISO-8601, tags remain dash-case for URLs, and author should be "colosieve".
- HTML templates use 4-space indentation and Hugo pipes (`| relURL`, `| safeHTML`) for transformations.
- CSS/JS in `static/` stay vanilla, camelCase functions in `static/js/icons.js`, kebab-case class names in stylesheets, and no build steps.
- Slides follow `Slide N – Topic` heading names so anchors render predictably; keep each slide as an H2.

### Testing Guidelines
- Always run `hugo --panicOnWarning` (or rely on CI) before pushing; treat warnings as blockers.
- Manually open `http://localhost:1313` to confirm Mermaid diagrams render and copy buttons attach without console errors.
- Use `curl -I http://localhost:1313/css/style.css` to confirm new assets resolve while developing.
- When templates change, smoke-test a post, a slide deck, and the landing page for regressions.

### Commit & Pull Request Guidelines
- Commits use short, imperative summaries (`Fix TOC anchor parsing`) and optional bullets in the body for context.
- Keep content, layout, and asset updates in separate commits where possible to simplify reviews.
- Pull requests link to any tracking issue, describe the Hugo command used for validation, and include screenshots/GIFs for visual tweaks.
- Request review from another maintainer familiar with Hugo; make sure the GitHub Pages workflow succeeds before merging.
