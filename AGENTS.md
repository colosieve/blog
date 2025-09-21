# Repository Guidelines

## Project Structure & Module Organization
- `content/posts/` holds Markdown with TOML front matter; rely on `archetypes/default.md` when adding new posts.
- `layouts/_default/` stores the base templates, partials, and slide layout logic; tweak shared markup here before touching individual pages.
- `layouts/shortcodes/` contains helper shortcodes (slides, callouts); keep slide decks co-located with their Markdown in `content/posts/`.
- `static/css/` and `static/js/` expose assets served as-is; update favicons and manifest entries under `static/`.
- `syslog-hugo.service` documents the systemd unit used for deployments—mirror changes there when automation scripts evolve.

## Build, Test, and Development Commands
- `hugo server --noHTTPCache --disableFastRender` launches a hot-reload dev server with cache busting—use it for authoring and slide checks.
- `hugo` builds the production-ready site in `public/`; clean that directory before committing artifacts.
- `hugo --panicOnWarning --printUnusedTemplates` fails fast on template issues and highlights stale layouts.
- `hugo server --buildDrafts --buildFuture` previews draft or scheduled content prior to publication.

## Coding Style & Naming Conventions
- Markdown: 80-character soft wrap, Title Case top-level headings, and fenced code blocks with a language hint (` ```bash `).
- Front matter keys stay lowercase snake_case, dates use ISO-8601, and tags remain dash-case for URLs.
- HTML templates use 4-space indentation and Hugo pipes (`| relURL`, `| safeHTML`) for transformations.
- CSS/JS in `static/` stay vanilla, camelCase functions in `static/js/icons.js`, kebab-case class names in stylesheets, and no build steps.
- Slides follow `Slide N – Topic` heading names so anchors render predictably; keep each slide as an H2.

## Testing Guidelines
- Always run `hugo --panicOnWarning` (or rely on CI) before pushing; treat warnings as blockers.
- Manually open `http://localhost:1313` to confirm Mermaid diagrams render and copy buttons attach without console errors.
- Use `curl -I http://localhost:1313/css/style.css` to confirm new assets resolve while developing.
- When templates change, smoke-test a post, a slide deck, and the landing page for regressions.

## Commit & Pull Request Guidelines
- Commits use short, imperative summaries (`Fix TOC anchor parsing`) and optional bullets in the body for context.
- Keep content, layout, and asset updates in separate commits where possible to simplify reviews.
- Pull requests link to any tracking issue, describe the Hugo command used for validation, and include screenshots/GIFs for visual tweaks.
- Request review from another maintainer familiar with Hugo; make sure the GitHub Pages workflow succeeds before merging.
