# Rough Drafts

Nithin's blog — [nithink.dev](https://nithink.dev). A [Jekyll](https://jekyllrb.com/) site with a hand-maintained theme (custom layouts, Sass, per-post palettes, interactive figures, and generated social cards).

## Quick start

```sh
make install     # bundle install
make serve        # dev server at http://localhost:4000 (watches for changes)
```

Other targets (`make help` lists them all):

| Target | Does |
| --- | --- |
| `make build` | Build the site into `_site/` |
| `make clean` | Remove `_site/` and caches |
| `make new title="My Post"` | Scaffold a dated post in `_posts/` |
| `make lint` | markdownlint `--fix` over `_posts/` |
| `make deploy` | Commit everything and push `main` (GitHub Pages serves it) |
| `make status` | Check the latest Pages deploy runs |

> Note: `jekyll serve` reads `_config.yml` once at startup. After editing `_config.yml`, restart the server. Serving also rewrites `og:url`/`og:image` to `localhost` — production URLs only appear in a real `make build`.

## Layout

```
_config.yml                 Site config (title, url, social handles, og_image default)
_posts/                     Posts, named YYYY-MM-DD-slug.md
_layouts/                   default, home, page, post
_includes/                  head (meta tags), header, footer, code-viewer, icons/
_sass/                      Styles; _variables.scss holds the palette + post themes
css/main.scss               Sass entrypoint → /css/main.css
assets/
  images/<slug>/            Per-post figures
  images/og/                Generated 1200x630 social cards
  js/<slug>/                Per-post interactive-figure scripts
scripts/
  generate-og-cards.sh      Regenerates the social cards
  coloc-capture.html        Headless-capture page for one animated figure
about.markdown research.markdown   Standalone pages
apps/ papers/               Standalone apps and PDFs
```

## Writing a post

Create `_posts/YYYY-MM-DD-slug.md` (or `make new title="…"`) with front matter:

```yaml
---
layout: post
title: "Hidden cost of leverage in LETFs"
date: 2026-03-15
categories: finance research
# Optional:
subtitle: "A one-line deck shown under the title"
description: "One-sentence summary used for the <meta> description and social cards."
image: /assets/images/og/hidden-costs-leveraged-etfs.png   # social share card
hero: /assets/images/<slug>/fig_hero.svg                    # full-bleed hero (see post.html)
hero_alt: "Alt text for the hero"
theme: autumn                                               # a palette from _sass/_variables.scss
---
```

Notes:

- **`description`** feeds the `<meta name="description">` and the Open Graph / Twitter tags. If omitted it falls back to `subtitle`, then the post's first paragraph, then the site description.
- **`image`** is the social share card (see below). Without it, pages use the default card (`og_image` in `_config.yml`).
- **`hero`** renders a full-bleed header image via `_layouts/post.html`; otherwise the plain `.post-header` is used.
- **`theme`** scopes a color palette to the post. Themes live in `_sass/_variables.scss` as `.theme-<name>` blocks that override the CSS variables; the layout puts `theme-<name>` on `<body>`.

## Social share cards

`_includes/head.html` emits Open Graph and Twitter Card tags so links unfurl with a title, description, and a 1200×630 image. Each post points `image:` at a card under `assets/images/og/`.

The cards are generated, not hand-drawn:

```sh
./scripts/generate-og-cards.sh
```

Each card is the "Rough Drafts" wordmark, the post title, a key figure, and the domain, laid out to match the site's type and palette. Requirements:

- **ImageMagick** (`magick`) and **librsvg** (`rsvg-convert`) — `brew install imagemagick librsvg`.

To add or change a card, edit the `make_card` calls near the bottom of the script (slug, title, source figure, palette) and rerun it. Source figures can be SVG, PNG, JPG, or WebP; SVGs are rasterized. Note that some figures animate their drawing on load — a static rasterize catches an empty frame, so use a pre-rendered raster for those.

One figure (the who-meets-whom co-location map) is drawn entirely by JavaScript, so there's no file to rasterize. `scripts/coloc-capture.html` renders it off-screen and headless Chrome snapshots a frame; the exact command is in the comment at the top of that file. That produces `assets/images/who-meets-whom/co_location_frame.png`, which the card script then uses.

## Interactive figures

Interactive figures are inlined into the post as raw HTML plus a script under `assets/js/<slug>/`, e.g.:

```html
<div id="letf-scatter" style="…"></div>
<script src="/assets/js/hidden-costs-leveraged-etfs/letf_scatter.js"></script>
```

kramdown passes raw HTML blocks through untouched. Keep the opening tag at column 0 and avoid blank lines inside the block, or kramdown may split it and start parsing Markdown again mid-figure.

## Deploying

`make deploy` commits and pushes `main`; GitHub Pages builds and serves the result at the custom domain in `CNAME` (`nithink.dev`). `make status` shows recent deploy runs. `head.html` sticks to core Liquid filters (no extra plugins) so a native Pages build renders the same as local.
