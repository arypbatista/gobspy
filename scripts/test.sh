#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$DIR/..
GPY=$ROOT/gobspy

python3 -m unittest discover -p test_*.py -t $GPY -s $GPY
python3 -m coverage run -m unittest discover -s $GPY
python3 -m coverage report -m
