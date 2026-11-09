#!/bin/zsh
# Stages only the public site files + the worker into a temp folder and deploys from there.
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/public"
cd "$SITE"
git archive HEAD index.html stavebnictvi.html zednici.html pily.html vyroba-automotive.html potravinarstvi.html zemedelstvi.html svareci.html sklady.html jak-to-funguje.html caste-dotazy.html o-nas.html kontakt.html pracovni-skupiny.html og-image.jpg _headers img favicon.ico apple-touch-icon.png robots.txt sitemap.xml google881e039a561c0d3b.html | tar -x -C "$STAGE/public"
git archive HEAD cloudflare/worker.js cloudflare/wrangler.jsonc | tar -x -C "$STAGE" --strip-components=1
ls -a "$STAGE/public"
cd "$STAGE"
npx --prefix "$HOME/Documents/fitnessmama-platform" wrangler deploy
