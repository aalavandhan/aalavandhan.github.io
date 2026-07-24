# Rough Drafts

Nithin's blog — [nithink.dev](https://nithink.dev). A [Jekyll](https://jekyllrb.com/) site with a hand-maintained theme: custom layouts, Sass, per-post color themes, interactive figures, and generated social cards.

## Quick start

```sh
make install     # bundle install
make serve       # dev server at http://localhost:4000 (watches for changes)
make help        # list every target
```

`make new title="My Post"` scaffolds a dated post; `make deploy` commits and pushes `main` (GitHub Pages serves it from `CNAME`).

## Where things live

Standard Jekyll layout — `_posts/`, `_layouts/`, `_includes/`, `_sass/`, `assets/`. To add a post, copy the front matter from a recent one in `_posts/` and go. Per-post themes are `.theme-<name>` blocks in `_sass/_variables.scss`.

`scripts/` regenerates the Open Graph cards (`generate-og-cards.sh`; needs `imagemagick` + `librsvg`). Interactive figures are raw HTML in the post plus a script under `assets/js/<slug>/`.

## Gotchas

- `jekyll serve` reads `_config.yml` once — restart after editing it.
- Serving rewrites `og:url`/`og:image` to `localhost`; production URLs only appear in a real `make build`.
- `_includes/head.html` sticks to core Liquid filters so GitHub Pages builds match local.
