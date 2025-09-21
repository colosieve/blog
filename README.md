# Colonel's Pensieve

Bare-minimum Hugo site with posts and custom slide presentation system.

## What is this?

A minimal Hugo static site generator setup with:
- Basic post functionality
- Custom CSS-based slide presentations
- No external dependencies or themes

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
