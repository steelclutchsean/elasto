#!/bin/bash
# Build script for creating Bungee Biker macOS application
# This script handles the complete build process

set -e  # Exit on error

echo "================================"
echo "Bungee Biker macOS Build Script"
echo "================================"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️  Warning: This script is designed for macOS"
    echo "   You can still use PyInstaller on other platforms"
    echo ""
fi

# Step 1: Create icon
echo "Step 1: Creating application icon..."
if [ ! -f "assets/icon.png" ]; then
    python create_icon.py
else
    echo "✓ Icon already exists"
fi

# Step 2: Convert PNG to ICNS (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "Step 2: Converting icon to ICNS format..."
    if [ ! -f "assets/icon.icns" ]; then
        mkdir -p BungeeBiker.iconset
        cp assets/icon_16.png BungeeBiker.iconset/icon_16x16.png
        cp assets/icon_32.png BungeeBiker.iconset/icon_16x16@2x.png
        cp assets/icon_32.png BungeeBiker.iconset/icon_32x32.png
        cp assets/icon_64.png BungeeBiker.iconset/icon_32x32@2x.png
        cp assets/icon_128.png BungeeBiker.iconset/icon_128x128.png
        cp assets/icon_256.png BungeeBiker.iconset/icon_128x128@2x.png
        cp assets/icon_256.png BungeeBiker.iconset/icon_256x256.png
        cp assets/icon_512.png BungeeBiker.iconset/icon_256x256@2x.png
        cp assets/icon_512.png BungeeBiker.iconset/icon_512x512.png
        cp assets/icon.png BungeeBiker.iconset/icon_512x512@2x.png
        iconutil -c icns BungeeBiker.iconset -o assets/icon.icns
        rm -rf BungeeBiker.iconset
        echo "✓ Created assets/icon.icns"
    else
        echo "✓ ICNS icon already exists"
    fi
fi

# Step 3: Install build dependencies
echo ""
echo "Step 3: Installing build dependencies..."
pip install --upgrade pip
pip install pyinstaller py2app

# Step 4: Choose build method
echo ""
echo "Step 4: Building application..."
echo ""
echo "Choose build method:"
echo "  1) PyInstaller (recommended, cross-platform)"
echo "  2) py2app (macOS native)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Building with PyInstaller..."

    # Clean previous builds
    rm -rf build dist

    # Build
    pyinstaller build_macos.spec

    echo ""
    echo "✓ Build complete!"
    echo ""
    echo "Application location: dist/BungeeBiker.app"
    echo ""
    echo "To install:"
    echo "  cp -r dist/BungeeBiker.app /Applications/"
    echo ""
    echo "To create DMG:"
    echo "  hdiutil create -volname 'Bungee Biker' -srcfolder dist/BungeeBiker.app -ov -format UDZO BungeeBiker.dmg"

elif [ "$choice" = "2" ]; then
    echo ""
    echo "Building with py2app..."

    # Clean previous builds
    rm -rf build dist

    # Build
    python setup.py py2app

    echo ""
    echo "✓ Build complete!"
    echo ""
    echo "Application location: dist/Bungee Biker.app"
    echo ""
    echo "To install:"
    echo "  cp -r 'dist/Bungee Biker.app' /Applications/"
    echo ""
    echo "To create DMG:"
    echo "  hdiutil create -volname 'Bungee Biker' -srcfolder 'dist/Bungee Biker.app' -ov -format UDZO BungeeBiker.dmg"
else
    echo "Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "================================"
echo "Build process complete! 🎉"
echo "================================"
