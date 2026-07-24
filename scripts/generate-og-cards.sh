#!/usr/bin/env bash
#
# Generate 1200x630 social-share ("Open Graph") cards for the blog.
#
# Each card is a branded title card: the "Rough Drafts" wordmark, the post
# title, a key figure from the post, and the domain footer — laid out to match
# the site's own type and palette (see _sass/_variables.scss). Cards are written
# to assets/images/og/ and referenced from each post's `image:` front matter by
# _includes/head.html.
#
# Sources may be SVG (rasterized with rsvg-convert), WebP/PNG/JPG (via
# ImageMagick). Re-run any time a figure or title changes:
#
#     ./scripts/generate-og-cards.sh
#
# Requires: ImageMagick (magick), rsvg-convert (librsvg).
set -euo pipefail

cd "$(dirname "$0")/.."
OUT_DIR="assets/images/og"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$OUT_DIR"

# Card geometry
W=1200; H=630; PAD=76
CW=$((W - 2 * PAD))            # content column width = 1048

WORDMARK="Rough Drafts"
DOMAIN="nithink.dev"
FONT_TITLE="Helvetica-Bold"
FONT_UI="Helvetica-Bold"
FONT_UI_REG="Helvetica"

# rasterize <src> <dst.png> <bg-hex>
# Normalizes any supported source to a PNG flattened onto the card background,
# so figures with transparency don't punch holes in the card.
rasterize() {
  local src="$1" dst="$2" bg="$3"
  case "${src##*.}" in
    svg)
      # Render at 2x card width for crisp downscaling, on the card background.
      rsvg-convert -w 2096 --background-color "$bg" "$src" -o "$dst"
      ;;
    *)
      magick "$src" -background "$bg" -flatten "$dst"
      ;;
  esac
}

# make_brand_card <slug> <bg> <text> <muted> <accent> <avatar> <name> <tagline>
# A centered brand card for the home page and any page without its own image:
# circular avatar, site name, tagline. No figure, no duplicate wordmark.
make_brand_card() {
  local slug="$1" bg="$2" text="$3" muted="$4" accent="$5"
  local avatar="$6" name="$7" tagline="$8"
  local t="$TMP_DIR/$slug"
  mkdir -p "$t"
  local out="$OUT_DIR/$slug.png"

  # Canvas + top accent bar.
  # Force RGB PNG storage. An all-gray canvas (white bg + dark bar) is otherwise
  # written as a grayscale PNG; compositing a color figure onto it on re-read
  # then desaturates the figure. png:color-type=2 keeps the canvas RGB so colors
  # (the co-location map, the autumn figures) survive. Naturally-monochrome
  # figures still look monochrome — nothing is force-colorized.
  magick -size "${W}x${H}" "xc:$bg" -type TrueColor -colorspace sRGB \
    -fill "$accent" -draw "rectangle 0,0 ${W},8" \
    -define png:color-type=2 \
    "$t/canvas.png"

  # Circular avatar — CopyOpacity turns a black/white circle mask into alpha,
  # so the corners are transparent (they read as the card background).
  magick "$avatar" -resize "220x220^" -gravity center -extent 220x220 \
    \( -size 220x220 xc:black -fill white -draw "circle 110,110 110,0" \) \
    -alpha off -compose CopyOpacity -composite "$t/avatar.png"

  # Name and tagline.
  magick -background none -fill "$text" -font "$FONT_TITLE" -pointsize 76 \
    label:"$name" "$t/name.png"
  magick -background none -fill "$muted" -font "$FONT_UI_REG" -pointsize 34 \
    label:"$tagline" "$t/tagline.png"

  magick "$t/canvas.png" \
    "$t/avatar.png"  -gravity North -geometry "+0+120" -composite \
    "$t/name.png"    -gravity North -geometry "+0+380" -composite \
    "$t/tagline.png" -gravity North -geometry "+0+486" -composite \
    "$out"

  echo "  wrote $out"
}

# make_card <slug> <title> <figure-src> <bg> <text> <muted> <accent>
make_card() {
  local slug="$1" title="$2" figure="$3"
  local bg="$4" text="$5" muted="$6" accent="$7" border="$8"
  local t="$TMP_DIR/$slug"
  mkdir -p "$t"
  local out="$OUT_DIR/$slug.png"

  # 1. Base canvas in the theme background, with an 8px accent bar along the top.
  # Force RGB PNG storage. An all-gray canvas (white bg + dark bar) is otherwise
  # written as a grayscale PNG; compositing a color figure onto it on re-read
  # then desaturates the figure. png:color-type=2 keeps the canvas RGB so colors
  # (the co-location map, the autumn figures) survive. Naturally-monochrome
  # figures still look monochrome — nothing is force-colorized.
  magick -size "${W}x${H}" "xc:$bg" -type TrueColor -colorspace sRGB \
    -fill "$accent" -draw "rectangle 0,0 ${W},8" \
    -define png:color-type=2 \
    "$t/canvas.png"

  # 2. Wordmark (top-left, accent color).
  magick -background none -fill "$accent" -font "$FONT_UI" -pointsize 30 \
    label:"$WORDMARK" "$t/wordmark.png"

  # 3. Title — left column. Wraps within a narrow measure (so it fills the
  #    column's height) and shrinks to fit.
  magick -background "$bg" -fill "$text" -font "$FONT_TITLE" \
    -size "400x340" -pointsize 56 -gravity NorthWest \
    caption:"$title" "$t/title.png"

  # 4. Figure — right column. Trim its own margins, enlarge to fill the column
  #    width, then frame with a hairline border and a soft drop shadow.
  rasterize "$figure" "$t/fig_raw.png" "$bg"
  magick "$t/fig_raw.png" -fuzz 1% -trim +repage \
    -resize "652x480" \
    -bordercolor "$border" -border 1 \
    \( +clone -background black -shadow 40x15+0+10 \) \
    +swap -background none -layers merge +repage "$t/fig.png"

  # 5. Footer — domain on the left, muted.
  magick -background none -fill "$muted" -font "$FONT_UI_REG" -pointsize 27 \
    label:"$DOMAIN" "$t/footer.png"

  # 6. Compose — text on the left, framed figure filling the right column.
  magick "$t/canvas.png" \
    "$t/wordmark.png" -gravity NorthWest -geometry "+${PAD}+66"  -composite \
    "$t/title.png"    -gravity NorthWest -geometry "+${PAD}+118" -composite \
    "$t/fig.png"      -gravity Center    -geometry "+224+8"      -composite \
    "$t/footer.png"   -gravity NorthWest -geometry "+${PAD}+566" -composite \
    "$out"

  echo "  wrote $out"
}

# Neutral (default) palette — from :root in _sass/_variables.scss
BG="#ffffff"; TEXT="#292929"; MUTED="#757575"; ACCENT="#292929"; BORDER="#e2e2e2"
# Autumn palette — from .theme-autumn
A_BG="#fdf8f1"; A_TEXT="#2b2620"; A_MUTED="#8a765a"; A_ACCENT="#b45309"; A_BORDER="#e6ddcd"

IMG="assets/images"

echo "Generating OG cards…"

# co_location_frame.png is a static frame of the post's JS-driven co-location
# animation, captured with headless Chrome via scripts/coloc-capture.html.
make_card "who-meets-whom" \
  "Who Meets Whom" \
  "$IMG/who-meets-whom/co_location_frame.png" \
  "$BG" "$TEXT" "$MUTED" "$ACCENT" "$BORDER"

# NB: this post's inline SVG charts animate their lines on load, so a static
# rasterize catches an empty frame — use the pre-rendered PNG instead.
make_card "hidden-costs-leveraged-etfs" \
  "Hidden cost of leverage in LETFs" \
  "$IMG/hidden-costs-leveraged-etfs/fig_letf_decomposition.png" \
  "$BG" "$TEXT" "$MUTED" "$ACCENT" "$BORDER"

make_card "demand-deposits-are-mispriced-options" \
  "Demand deposits are mispriced options" \
  "$IMG/demand-deposits-are-mispriced-options/fig_put_payoff.svg" \
  "$BG" "$TEXT" "$MUTED" "$ACCENT" "$BORDER"

make_card "programs-run-on-physical-machines" \
  "Programs run on physical machines" \
  "$IMG/programs-run-on-physical-machines/fig_landscape.svg" \
  "$BG" "$TEXT" "$MUTED" "$ACCENT" "$BORDER"

make_card "source-your-own-order-flow" \
  "Source your own order flow" \
  "$IMG/integrating-a-bespoke-amm-with-cowswap/fig_pool.svg" \
  "$A_BG" "$A_TEXT" "$A_MUTED" "$A_ACCENT" "$A_BORDER"

# Site default — used for the home page and any page without its own image.
make_brand_card "default" \
  "$BG" "$TEXT" "$MUTED" "$ACCENT" \
  "$IMG/about/dp.jpg" "Rough Drafts" "Nithin's blog · nithink.dev"

echo "Done."
