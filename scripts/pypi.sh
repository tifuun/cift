#!/bin/sh

# Exit on error
set -e

# Get tag name
tagname=$(git describe --tags --abbrev=0)

# Verify that tag name and token provided
test -n "$PYPI_TOKEN"
test -n "$tagname"

# Twine and build needed to interface with pypi
pip install twine build

# Build wheel and tarball
python -m build

# Upload wheel and tarball
python -m twine upload \
	--username '__token__' \
	--password "$PYPI_TOKEN" \
	dist/cift-$tagname*


