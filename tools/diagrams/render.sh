#!/usr/bin/env bash
# Render the PlantUML diagrams under docs/ to SVG, or check the committed SVGs.
#
#   tools/diagrams/render.sh           render docs/**/diagrams/*.puml to *.svg
#   tools/diagrams/render.sh --check   fail if an SVG is missing or was not
#                                      rendered from the current source
#
# Needs Java, Graphviz, curl and python3. The pinned PlantUML jar is downloaded
# into ${XDG_CACHE_HOME:-$HOME/.cache}/ifdd and its SHA-256 is checked.
#
# The check compares the source PlantUML embeds in every SVG
# (<?plantuml-src ...?>), decoded to text, not the drawing: fonts and the
# Graphviz version change the layout from one machine to the next. The
# embedded string itself is compressed (deflate), and its bytes depend on the
# Java runtime (Temurin and Ubuntu's OpenJDK give different strings for the
# same source), so it is decoded before the comparison.
set -euo pipefail

version="1.2026.10"
sha256="e9bc9e6b2eb715e8c0c929f3dcb5fc1923be13f37599b09c293c66d354e88686"
url="https://github.com/plantuml/plantuml/releases/download/v$version/plantuml-$version.jar"

usage() { echo "usage: $0 [--check]" >&2; exit 2; }
mode=render
case "${1:-}" in
    "") ;;
    --check) mode=check ;;
    *) usage ;;
esac
[ $# -le 1 ] || usage

cd "$(dirname "$0")/../.."

check_sha() {
    python3 -c 'import hashlib, sys
h = hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()
sys.exit(0 if h == sys.argv[2] else f"SHA-256 mismatch for {sys.argv[1]}: {h}")' "$1" "$sha256"
}

dir="${XDG_CACHE_HOME:-$HOME/.cache}/ifdd"
jar="$dir/plantuml-$version.jar"
if [ ! -f "$jar" ]; then
    mkdir -p "$dir"
    curl -fsSL -o "$jar.part" "$url"
    check_sha "$jar.part"
    mv "$jar.part" "$jar"
fi
check_sha "$jar"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# Print the source embedded in an SVG as text (empty if there is none):
# PlantUML's base64 variant (0-9A-Za-z-_), then raw deflate.
embedded() {
    python3 - "$1" <<'EOF'
import re, sys, zlib
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
match = re.search(r"<\?plantuml-src ([0-9A-Za-z_-]+)\?>", open(sys.argv[1], encoding="utf-8").read())
if match:
    data = bytearray()
    text = match.group(1)
    for i in range(0, len(text), 4):
        chunk = [ALPHABET.index(c) for c in text[i:i + 4]] + [0, 0, 0]
        n = (chunk[0] << 18) | (chunk[1] << 12) | (chunk[2] << 6) | chunk[3]
        data += bytes([n >> 16, (n >> 8) & 255, n & 255])
    sys.stdout.write(zlib.decompressobj(-15).decompress(bytes(data)).decode("utf-8"))
EOF
}

status=0
count=0
while IFS= read -r src; do
    count=$((count + 1))
    svg="${src%.puml}.svg"
    out="$tmp/$(dirname "$src")"
    mkdir -p "$out"
    java -Djava.awt.headless=true -jar "$jar" -tsvg -o "$out" "$src"
    new="$out/$(basename "$svg")"
    if [ "$mode" = render ]; then
        cp "$new" "$svg"
        echo "rendered $svg"
    elif [ ! -f "$svg" ]; then
        echo "missing  $svg" >&2
        status=1
    elif [ "$(embedded "$svg")" != "$(embedded "$new")" ] || [ -z "$(embedded "$new")" ]; then
        echo "stale    $svg (run tools/diagrams/render.sh)" >&2
        status=1
    else
        echo "ok       $svg"
    fi
done < <(find docs -path '*/diagrams/*.puml' | LC_ALL=C sort)

[ "$count" -gt 0 ] || { echo "no diagrams found" >&2; exit 1; }
exit "$status"
