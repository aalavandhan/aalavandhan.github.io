#!/usr/bin/env bash
#
# Generate 1200x630 social-share ("Open Graph") cards for the blog.
#
# Each card is a branded figure card: a key figure from the post fills the right,
# and a slim brand column on the left carries the "ROUGH DRAFTS" wordmark, the
# post number (#n, in publication order), and the domain. No title is baked in —
# when a link is unfurled, the platform (X, Slack, iMessage, …) renders the title
# and description itself from the OG tags, so printing it on the image only
# duplicates it. Type and palette follow the site (see _sass/_variables.scss and
# the Georgia body font in _sass/_base.scss). Cards are written to
# assets/images/og/ and referenced from each post's `image:` front matter by
# _includes/head.html. Re-run any time a figure changes:
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
W=1200; H=630; PAD=64
PANEL_W=452                    # nominal width of the brand column
ZW=$((W - PANEL_W - 44))       # figure zone width  = 704
ZH=$((H - 120))                # figure zone height = 510
WASH=620                       # how far the left tint reaches before fading out

EYEBROW="ROUGH DRAFTS"
DOMAIN="nithink.dev"
FONT_NUM="Georgia-Bold"        # post number — matches the blog's Georgia body type
FONT_UI="Georgia"             # eyebrow + domain

# rasterize <src> <dst.png>
# Normalize any supported source to a PNG, KEEPING transparency so the figure
# blends onto the card instead of sitting in an opaque rectangle. SVGs render at
# ~2x the figure zone for crisp downscaling; other formats resize to match.
rasterize() {
  local src="$1" dst="$2"
  case "${src##*.}" in
    svg) rsvg-convert -w 1400 "$src" -o "$dst" ;;
    *)   magick "$src" -resize 1400x "$dst" ;;
  esac
}

# make_brand_card <slug> <bg> <text> <muted> <tint> <avatar> <name> <tagline>
# A centered brand card for the home page and any page without its own image:
# circular avatar, site name, tagline. No figure, no post number. (<tint> is
# accepted for a uniform signature but unused — the layout is centered.)
make_brand_card() {
  local slug="$1" bg="$2" text="$3" muted="$4" tint="$5"
  local avatar="$6" name="$7" tagline="$8"
  local t="$TMP_DIR/$slug"
  mkdir -p "$t"
  local out="$OUT_DIR/$slug.png"

  # Canvas. Force RGB PNG storage so a near-gray canvas isn't written as
  # grayscale (which would desaturate a color avatar composited onto it).
  magick -size "${W}x${H}" "xc:$bg" -type TrueColor -colorspace sRGB \
    -define png:color-type=2 "$t/canvas.png"

  # Square avatar with softly rounded corners. CopyOpacity turns the white
  # rounded-rectangle mask into alpha, so the corners read as the card background.
  magick "$avatar" -resize "230x230^" -gravity center -extent 230x230 \
    \( -size 230x230 xc:black -fill white -draw "roundrectangle 0,0 229,229 20,20" \) \
    -alpha off -compose CopyOpacity -composite "$t/avatar.png"

  magick -background none -fill "$text" -font "$FONT_NUM" -pointsize 76 \
    label:"$name" "$t/name.png"
  magick -background none -fill "$muted" -font "$FONT_UI" -pointsize 34 \
    label:"$tagline" "$t/tagline.png"

  magick "$t/canvas.png" \
    "$t/avatar.png"  -gravity North -geometry "+0+120" -composite \
    "$t/name.png"    -gravity North -geometry "+0+380" -composite \
    "$t/tagline.png" -gravity North -geometry "+0+486" -composite \
    "$out"

  echo "  wrote $out"
}

# make_card <slug> <number> <figure-src> <bg> <text> <muted> <tint>
make_card() {
  local slug="$1" number="$2" figure="$3"
  local bg="$4" text="$5" muted="$6" tint="$7"
  local t="$TMP_DIR/$slug"
  mkdir -p "$t"
  local out="$OUT_DIR/$slug.png"

  # 1. Base canvas in the theme background.
  magick -size "${W}x${H}" "xc:$bg" -type TrueColor -colorspace sRGB \
    -define png:color-type=2 "$t/canvas.png"

  # 2. Figure — contained in the right zone (nothing cropped), trimmed of its own
  #    margins. Kept transparent so it sits directly on the page.
  rasterize "$figure" "$t/fig_raw.png"
  magick "$t/fig_raw.png" -fuzz 1% -trim +repage \
    -resize "${ZW}x${ZH}" "$t/fig.png"

  # 3. Soft left wash: the theme tint at the far left dissolving to nothing, so
  #    the brand column flows into the figure with no hard edge. `gradient:`
  #    fills top→bottom; -rotate -90 lands the tinted top edge on the left.
  magick -size "${H}x${WASH}" "gradient:${tint}-none" -rotate -90 "$t/wash.png"

  # 4. Brand column — letterspaced wordmark, the post number as the hero, domain.
  magick -background none -fill "$muted" -font "$FONT_UI" -kerning 3 -pointsize 22 \
    label:"$EYEBROW" "$t/eyebrow.png"
  magick -background none -fill "$text" -font "$FONT_NUM" -pointsize 104 \
    label:"#$number" "$t/number.png"
  magick -background none -fill "$muted" -font "$FONT_UI" -pointsize 25 \
    label:"$DOMAIN" "$t/domain.png"

  # 5. Compose — wash and figure on the canvas, brand text over the wash.
  magick "$t/canvas.png" \
    "$t/wash.png"    -gravity NorthWest -geometry "+0+0"            -composite \
    "$t/fig.png"     -gravity East      -geometry "+40+0"           -composite \
    "$t/eyebrow.png" -gravity NorthWest -geometry "+${PAD}+112"     -composite \
    "$t/number.png"  -gravity NorthWest -geometry "+$((PAD-6))+166" -composite \
    "$t/domain.png"  -gravity NorthWest -geometry "+${PAD}+556"     -composite \
    "$out"

  echo "  wrote $out"
}

# Neutral (default) palette — from :root in _sass/_variables.scss
BG="#ffffff"; TEXT="#232323"; MUTED="#8f8f8f"; TINT="#f7f5f1"
# Autumn palette — from .theme-autumn
A_BG="#fdf8f1"; A_TEXT="#2b2620"; A_MUTED="#8a765a"; A_TINT="#f3ebda"

IMG="assets/images"

echo "Generating OG cards…"

# Post numbers are assigned in publication order (see _posts/ dates).

# co_location_frame.png is a static frame of the post's JS-driven co-location
# animation, captured with headless Chrome via scripts/coloc-capture.html.
make_card "who-meets-whom" 1 \
  "$IMG/who-meets-whom/co_location_frame.png" \
  "$BG" "$TEXT" "$MUTED" "$TINT"

# NB: this post's inline SVG charts animate their lines on load, so a static
# rasterize catches an empty frame — use the pre-rendered PNG instead.
make_card "hidden-costs-leveraged-etfs" 2 \
  "$IMG/hidden-costs-leveraged-etfs/fig_letf_decomposition.png" \
  "$BG" "$TEXT" "$MUTED" "$TINT"

make_card "demand-deposits-are-mispriced-options" 3 \
  "$IMG/demand-deposits-are-mispriced-options/fig_put_payoff.svg" \
  "$BG" "$TEXT" "$MUTED" "$TINT"

make_card "programs-run-on-physical-machines" 4 \
  "$IMG/programs-run-on-physical-machines/fig_landscape.svg" \
  "$BG" "$TEXT" "$MUTED" "$TINT"

make_card "source-your-own-order-flow" 5 \
  "$IMG/integrating-a-bespoke-amm-with-cowswap/fig_pool.svg" \
  "$A_BG" "$A_TEXT" "$A_MUTED" "$A_TINT"

# Site default — used for the home page and any page without its own image.
make_brand_card "default" \
  "$BG" "$TEXT" "$MUTED" "$TINT" \
  "$IMG/about/dp.jpg" "Rough Drafts" "Nithin's blog · nithink.dev"

echo "Done."
