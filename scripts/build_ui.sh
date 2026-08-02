#!/bin/sh
# Build the Next.js frontend and vendor the static export into the package.
# Maintainer-only: end users get the committed bundle via pip; Node never
# touches their machines.
set -e
cd "$(dirname "$0")/.."

echo "== building frontend =="
cd frontend
[ -d node_modules ] || npm ci
npx next build
cd ..

echo "== vendoring into src/openniw/ui =="
rm -rf src/openniw/ui
mkdir -p src/openniw/ui
cp -R frontend/out/. src/openniw/ui/

tree_hash=$(git rev-parse "HEAD:frontend" 2>/dev/null || echo "unknown")
if ! git diff --quiet HEAD -- frontend 2>/dev/null; then
  tree_hash="${tree_hash}-dirty"
fi
cat > src/openniw/ui/ui-build.json <<EOF
{"frontend_tree": "$tree_hash", "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
EOF
echo "ui bundle: $(du -sh src/openniw/ui | cut -f1), stamp: $tree_hash"
