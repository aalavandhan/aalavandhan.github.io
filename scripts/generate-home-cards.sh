#!/usr/bin/env bash
#
# Figure-only cards for the home page grid. Each post's key figure is trimmed of
# its margins and centred on a plain canvas — no wordmark, no domain, no number.
# The site overlays a subtle post number in the corner (see _home.scss), so the
# figure carries the card. Figure choices mirror generate-og-cards.sh.
#
#     ./scripts/generate-home-cards.sh
#
# Requires: ImageMagick (magick), rsvg-convert (librsvg).
set -euo pipefail

cd "$(dirname "$0")/.."
OUT_DIR="assets/images/cards"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$OUT_DIR"

W=1200; H=630
BG="#ffffff"
IMG="assets/images"

# rasterize <src> <dst.png> — normalize any figure to a PNG, keeping transparency
# so it composites onto the canvas cleanly. SVGs render at ~2x for a crisp
# downscale; other formats resize to match.
rasterize() {
  local src="$1" dst="$2"
  case "${src##*.}" in
    svg) rsvg-convert -w 1400 "$src" -o "$dst" ;;
    *)   magick "$src" -resize 1400x "$dst" ;;
  esac
}

# make_card <slug> <figure-src> — trimmed figure centred on the card canvas.
make_card() {
  local slug="$1" figure="$2"
  local t="$TMP_DIR/$slug"
  mkdir -p "$t"

  magick -size "${W}x${H}" "xc:$BG" -type TrueColor -colorspace sRGB \
    -define png:color-type=2 "$t/canvas.png"

  rasterize "$figure" "$t/fig_raw.png"
  magick "$t/fig_raw.png" -fuzz 1% -trim +repage \
    -resize "$((W - 140))x$((H - 110))" "$t/fig.png"

  magick "$t/canvas.png" "$t/fig.png" -gravity center -composite "$OUT_DIR/$slug.png"
  echo "  wrote $OUT_DIR/$slug.png"
}

echo "Generating home cards…"

make_card "who-meets-whom" \
  "$IMG/who-meets-whom/co_location_frame.png"
make_card "hidden-costs-leveraged-etfs" \
  "$IMG/hidden-costs-leveraged-etfs/fig_letf_decomposition.png"
make_card "demand-deposits-are-mispriced-options" \
  "$IMG/demand-deposits-are-mispriced-options/fig_put_payoff.svg"
make_card "programs-run-on-physical-machines" \
  "$IMG/programs-run-on-physical-machines/fig_landscape.svg"
make_card "source-your-own-order-flow" \
  "$IMG/integrating-a-bespoke-amm-with-cowswap/fig_pool.svg"

echo "Done."
