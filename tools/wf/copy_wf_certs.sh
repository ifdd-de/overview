#!/usr/bin/env bash
# Copy internal CA certificates into a wf instance after the cruft run.
#
# Usage: ./copy_wf_certs.sh SOURCE_DIR INSTANCE_DIR
#   SOURCE_DIR    directory with the CA certificates (*.crt or *.pem, PEM)
#   INSTANCE_DIR  generated instance (contains certs/ and adm_01_build.sh)
#
# Copies only certificates (no private keys), one certificate per file,
# checked with openssl when available. Existing files of the same name are
# replaced; others in INSTANCE_DIR/certs are left alone. Rebuild the images
# afterwards: (cd INSTANCE_DIR && ./adm_01_build.sh <mode>).
set -euo pipefail

src=${1:?usage: $0 SOURCE_DIR INSTANCE_DIR}
dst=${2:?usage: $0 SOURCE_DIR INSTANCE_DIR}
[ -d "$src" ] || { echo "no such directory: $src" >&2; exit 1; }
[ -d "$dst/certs" ] || { echo "$dst has no certs/ - not a wf instance?" >&2; exit 1; }

shopt -s nullglob
count=0
for f in "$src"/*.crt "$src"/*.pem; do
    if grep -q "PRIVATE KEY" "$f"; then
        echo "skipped $f: contains a private key" >&2
        continue
    fi
    n=$(grep -c "BEGIN CERTIFICATE" "$f" || true)
    if [ "$n" -ne 1 ]; then
        echo "skipped $f: expected exactly one PEM certificate, found $n" >&2
        continue
    fi
    if command -v openssl >/dev/null 2>&1; then
        if ! openssl x509 -in "$f" -noout 2>/dev/null; then
            echo "skipped $f: openssl cannot read it" >&2
            continue
        fi
        echo "$(basename "$f"): $(openssl x509 -in "$f" -noout -subject -enddate | tr '\n' ' ')"
    fi
    install -m 0644 "$f" "$dst/certs/$(basename "$f")"
    count=$((count + 1))
done

echo "$count certificate(s) copied to $dst/certs"
[ "$count" -gt 0 ] || exit 1
