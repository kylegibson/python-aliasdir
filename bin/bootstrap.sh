#!/bin/bash
virtualenv --clear --no-site-packages venv
pip install -E venv --requirement=pipfile
