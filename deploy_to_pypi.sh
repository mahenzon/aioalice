#!/usr/bin/env bash

# remove old builds
rm ./dist/*

# build
python setup.py sdist
python setup.py bdist_wheel

# upload to PYPI
twine upload dist/*
