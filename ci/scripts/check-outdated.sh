#!/bin/bash
set -e

python -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools
pip install -r requirements-dev.txt
pip install -e .

outdated=$(pip list --outdated | tail -n +3 | while read -r package rest; do
  if ! grep -q "^$package\$\|^${package%%-*}-\*$" .allowed_outdated_dependencies 2>/dev/null; then
    echo "$package $rest"
  fi
done)

if [ -n "$outdated" ]; then
  echo "Found non-allowed outdated packages:"
  echo "$outdated"
  exit 1
else
  echo "All dependencies OK."
fi
