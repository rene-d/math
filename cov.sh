#!/bin/bash

# couverture manuelle

py.test --cov=. --cov-branch
coverage html
open htmlcov/index.html

