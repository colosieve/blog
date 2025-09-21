# Systems Log

Bare-minimum Hugo site with posts and custom slide presentation system.

## What is this?

A minimal Hugo static site generator setup with:
- Basic post functionality
- Custom CSS-based slide presentations
- No external dependencies or themes

## Local Development

```bash
# Start development server with live reload
hugo server

# Visit http://localhost:1313
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

Pushes to master can trigger a GitHub Actions workflow for automatic deployment.