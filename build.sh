#!/usr/bin/env bash

rm -rf ./build
rm -rf ./dist
rm -rf ./slim_helper.egg-info

python setup.py sdist build && \
python setup.py bdist_wheel --universal && \
twine upload dist/*