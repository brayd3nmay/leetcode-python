#!/bin/zsh
set -e

python3 generate_readme.py
git add README.md
git commit README.md -m "Update README"
git push

echo "✅ README updated and pushed!"