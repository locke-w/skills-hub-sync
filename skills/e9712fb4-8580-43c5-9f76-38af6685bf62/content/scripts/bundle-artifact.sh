#!/bin/bash
set -e

echo "📦 Bundling React app to single HTML artifact..."

# Check if we're in a project directory
if [ ! -f "package.json" ]; then
  echo "❌ Error: No package.json found. Run this script from your project root."
  exit 1
fi

# Check if index.html exists
if [ ! -f "index.html" ]; then
  echo "❌ Error: No index.html found in project root."
  echo "   This script requires an index.html entry point."
  exit 1
fi

# Install bundling dependencies
echo "📦 Installing bundling dependencies..."
pnpm add -D parcel @parcel/config-default parcel-resolver-tspaths html-inline

# Create Parcel config with tspaths resolver
if [ ! -f ".parcelrc" ]; then
  echo "🔧 Creating Parcel configuration with path alias support..."
  cat > .parcelrc << 'EOF'
{
  "extends": "@parcel/config-default",
  "resolvers": ["parcel-resolver-tspaths", "..."]
}
EOF
fi

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf dist bundle.html

# Build with Parcel (with Vite fallback)
echo "🔨 Building project..."
if pnpm exec parcel build index.html --dist-dir dist --no-source-maps 2>/dev/null; then
  echo "🎯 Inlining all assets into single HTML file via html-inline..."
  pnpm exec html-inline dist/index.html > bundle.html
else
  echo "⚡ Using Vite build and inline packager..."
  pnpm exec vite build
  node -e "
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync('dist/index.html', 'utf8');
const assets = fs.readdirSync('dist/assets');
const cssFile = assets.find(f => f.endsWith('.css'));
const jsFile = assets.find(f => f.endsWith('.js'));
const cssContent = cssFile ? fs.readFileSync(path.join('dist/assets', cssFile), 'utf8') : '';
const jsContent = jsFile ? fs.readFileSync(path.join('dist/assets', jsFile), 'utf8') : '';
let bundled = html;
if (cssContent) {
  bundled = bundled.replace(/<link rel=\"stylesheet\"[^>]+>/, '<style>' + cssContent + '</style>');
}
if (jsContent) {
  bundled = bundled.replace(/<script type=\"module\"[^>]+><\/script>/, '<script type=\"module\">' + jsContent + '</script>');
}
fs.writeFileSync('bundle.html', bundled);
"
fi

# Get file size
FILE_SIZE=$(du -h bundle.html | cut -f1)

echo ""
echo "✅ Bundle complete!"
echo "📄 Output: bundle.html ($FILE_SIZE)"
echo ""
echo "You can now use this single HTML file as an artifact in Claude conversations."
echo "To test locally: open bundle.html in your browser"