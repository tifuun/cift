#!/bin/sh

echo "START PYPI SCRIPT!" > /dev/stderr

# Exit on error
set -e

echo "GETTING TAG..." > /dev/stderr
tagname=$(git describe --tags --abbrev=0)

# Verify that tag name and token provided
if [ -z "$PYPI_TOKEN" ]
then
	echo "NO PYPI TOKEN!!" > /dev/stderr
	exit 69
fi
if [ -z "$tagname" ]
then
	echo "NO TAG!!" > /dev/stderr
	exit 69
fi

echo "INSTALLING TWINE, BUILD..." > /dev/stderr
pip install twine build

echo "BUILDING..." > /dev/stderr
python -m build

echo "UPLOADING..." > /dev/stderr
python -m twine upload \
	--username '__token__' \
	--password "$PYPI_TOKEN" \
	dist/cift-$tagname*

echo "DONE..." > /dev/stderr

