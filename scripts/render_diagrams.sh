#!/bin/sh
set -eu

repo_dir=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
version=1.2026.10
expected_sha=71972b58fe9208a78bbed614c806042b8404ca5f24022581d986bd9a1cc9463e
jar=${PLANTUML_JAR:-"$repo_dir/.tools/plantuml-$version.jar"}

if [ ! -f "$jar" ]; then
    mkdir -p "$(dirname -- "$jar")"
    download="$jar.download"
    trap 'rm -f "$download"' EXIT HUP INT TERM
    curl --fail --location --silent --show-error \
        "https://repo.maven.apache.org/maven2/net/sourceforge/plantuml/plantuml/$version/plantuml-$version.jar" \
        --output "$download"
    python3 - "$download" "$expected_sha" <<'PY'
import hashlib
import pathlib
import sys

actual = hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest()
if actual != sys.argv[2]:
    raise SystemExit(f"PlantUML checksum mismatch: {actual}")
PY
    mv "$download" "$jar"
    trap - EXIT HUP INT TERM
fi

python3 - "$jar" "$expected_sha" <<'PY'
import hashlib
import pathlib
import sys

if hashlib.sha256(pathlib.Path(sys.argv[1]).read_bytes()).hexdigest() != sys.argv[2]:
    raise SystemExit("Expected the pinned PlantUML 1.2026.10 JAR; checksum mismatch")
PY

mkdir -p "$repo_dir/diagrams/rendered"
java -Djava.awt.headless=true -Dfile.encoding=UTF-8 -jar "$jar" \
    -charset UTF-8 -failfast2 -tsvg \
    -o "$repo_dir/diagrams/rendered" "$repo_dir"/diagrams/src/*.puml
printf 'Rendered six diagrams into %s\n' "$repo_dir/diagrams/rendered"
