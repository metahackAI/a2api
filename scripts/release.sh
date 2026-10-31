#!/usr/bin/env bash
# Build and check the a2api distribution. Uploads ONLY with --upload.
#
#   scripts/release.sh               # clean, test, build, twine check, fresh-venv install check
#   scripts/release.sh --skip-tests  # same without the unit test suite
#   scripts/release.sh --upload      # all checks, then twine upload to PyPI (uses ~/.pypirc)
#   scripts/release.sh --upload --repository testpypi
set -euo pipefail
cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-.venv/bin/python}"
UPLOAD=0
TESTS=1
REPOSITORY=pypi
while [[ $# -gt 0 ]]; do
  case "$1" in
    --upload) UPLOAD=1 ;;
    --skip-tests) TESTS=0 ;;
    --repository) REPOSITORY="$2"; shift ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

VERSION="$("$PYTHON" -c 'import tomllib;print(tomllib.load(open("pyproject.toml","rb"))["project"]["version"])')"
echo "== a2api $VERSION"
rm -rf dist build src/*.egg-info

if [[ $TESTS -eq 1 ]]; then
  echo "== unit tests"
  "$PYTHON" -m unittest discover -s tests
fi

echo "== build sdist + wheel"
"$PYTHON" -m build
echo "== twine check"
"$PYTHON" -m twine check --strict dist/*

echo "== install the wheel into a fresh venv"
CHECK="$(mktemp -d)"
trap 'rm -rf "$CHECK"' EXIT
python3 -m venv "$CHECK/venv"
"$CHECK/venv/bin/pip" install -q "dist/a2api-$VERSION-py3-none-any.whl"
(cd "$CHECK" && "$CHECK/venv/bin/python" - "$VERSION" <<'PY'
import sys
from importlib.metadata import version
import a2api
from a2api import Application, ExecutionContext, ToolSession, capability, protocol_schema
assert version("a2api") == sys.argv[1], version("a2api")
@capability(id="demo.echo", effect="read")
def echo(value: str) -> str:
    """Echo a value."""
    return value
app = Application([echo])
assert app.invoke("demo.echo", {"value": "ok"}, context=ExecutionContext("u", "t", frozenset()))["data"] == "ok"
assert protocol_schema("describe_request")["type"] == "object"
print("installed wheel works:", a2api.PROTOCOL_PROFILE, a2api.TOOL_PROFILE)
PY
)

if [[ $UPLOAD -eq 1 ]]; then
  echo "== twine upload to $REPOSITORY"
  "$PYTHON" -m twine upload --repository "$REPOSITORY" dist/*
else
  echo "== built and checked; not uploaded (pass --upload to publish)"
fi
