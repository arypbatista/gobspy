#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$DIR/.."
GPY="$ROOT/gobspy"
CWD="$(pwd)"

echo $ROOT
cd $ROOT



rm -r dist
rm -r build
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*



cd $CWD
