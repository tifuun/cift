#!/bin/sh

set -e

pytest
mypy --strict src/cift

git push --tags
python -m build
twine upload $(ls dist | sort -rn | head -n 2)


