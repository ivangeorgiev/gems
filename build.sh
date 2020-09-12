#!/usr/bin/bash
source .venv38/Scripts/activate
REPO_URL=$(git remote get-url origin)
rm -rf .build
git clone -b gh-pages $REPO_URL .build
mkdocs build
cp -r site/* .build/.
cd .build
git add .
git commit -m "build"
git push origin
cd ..
