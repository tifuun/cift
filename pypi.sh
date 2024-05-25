#!/bin/sh

set -e

pytest
mypy --strict src/cift

git push --tags
python -m build
twine upload $(find dist -type f | sort -rn | head -n 2)


