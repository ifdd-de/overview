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
# (<?plantuml-src ...?>), not the drawing: fonts and the Graphviz version
# change the layout from one machine to the next.
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

embedded() { grep -o '<?plantuml-src [^?]*?>' "$1" || true; }

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
