#!/bin/zsh
# Stages only the public site files + the worker into a temp folder and deploys from there.
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/public"
cd "$SITE"
git archive HEAD index.html favicon.ico apple-touch-icon.png robots.txt sitemap.xml 2>/dev/null | tar -x -C "$STAGE/public" \
  || git archive HEAD index.html favicon.ico apple-touch-icon.png | tar -x -C "$STAGE/public"
git archive HEAD cloudflare/worker.js cloudflare/wrangler.jsonc | tar -x -C "$STAGE" --strip-components=1
ls -a "$STAGE/public"
cd "$STAGE"
npx --prefix "$HOME/Documents/fitnessmama-platform" wrangler deploy
