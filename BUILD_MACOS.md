# Building Bungee Biker for macOS

This guide explains how to package Bungee Biker as a standalone macOS application (.app bundle).

## Prerequisites

### Required
- macOS 10.14 or later
- Python 3.8 or later
- Xcode Command Line Tools (for `iconutil`)

### Install Xcode Command Line Tools
```bash
xcode-select --install
```

### Install Python Dependencies
```bash
pip install pygame numpy pyinstaller py2app
```

## Quick Build (Recommended)

The easiest way to build is using the automated build script:

```bash
./build_macos.sh
```

This script will:
1. Generate application icons
2. Convert icons to ICNS format
3. Install build dependencies
4. Build the macOS application
5. Show installation instructions

### Choose Your Build Method

The script offers two options:

**Option 1: PyInstaller** (Recommended)
- Cross-platform tool
- Better compatibility
- Easier to debug
- Produces: `dist/BungeeBiker.app`

**Option 2: py2app** (macOS Native)
- Official macOS bundler
- Native integration
- Better app bundle structure
- Produces: `dist/Bungee Biker.app`

## Manual Build Instructions

### Method 1: Using PyInstaller

#### Step 1: Create Icon
```bash
python create_icon.py
```

#### Step 2: Convert to ICNS (macOS only)
```bash
mkdir BungeeBiker.iconset
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
```

#### Step 3: Build Application
```bash
pyinstaller build_macos.spec
```

#### Output
Your app will be at: `dist/BungeeBiker.app`

### Method 2: Using py2app

#### Step 1 & 2: Same as PyInstaller (create icon)

#### Step 3: Build Application
```bash
python setup.py py2app
```

#### Output
Your app will be at: `dist/Bungee Biker.app`

## Installation

### Install to Applications Folder

**PyInstaller build:**
```bash
cp -r dist/BungeeBiker.app /Applications/
```

**py2app build:**
```bash
cp -r "dist/Bungee Biker.app" /Applications/
```

### Launch the App
Double-click `BungeeBiker.app` in Applications, or:
```bash
open /Applications/BungeeBiker.app
```

## Creating a DMG Installer

To create a distributable DMG file:

**For PyInstaller:**
```bash
hdiutil create -volname "Bungee Biker" \
               -srcfolder dist/BungeeBiker.app \
               -ov -format UDZO \
               BungeeBiker.dmg
```

**For py2app:**
```bash
hdiutil create -volname "Bungee Biker" \
               -srcfolder "dist/Bungee Biker.app" \
               -ov -format UDZO \
               BungeeBiker.dmg
```

### Create Fancy DMG (Optional)

For a professional DMG with custom background and layout:

```bash
# Install create-dmg
brew install create-dmg

# Create fancy DMG
create-dmg \
  --volname "Bungee Biker" \
  --volicon "assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "BungeeBiker.app" 175 190 \
  --hide-extension "BungeeBiker.app" \
  --app-drop-link 425 190 \
  "BungeeBiker-Installer.dmg" \
  "dist/BungeeBiker.app"
```

## Troubleshooting

### "BungeeBiker.app is damaged and can't be opened"

This happens because the app isn't signed. To run unsigned apps:

```bash
# Remove quarantine attribute
xattr -cr /Applications/BungeeBiker.app

# Or allow unsigned apps
sudo spctl --master-disable  # Enable "Anywhere" in Security settings
```

### Icon not showing

Make sure you completed the ICNS conversion step and the file exists at `assets/icon.icns`.

### App won't launch / Crashes immediately

Test the built app from terminal to see error messages:
```bash
./dist/BungeeBiker.app/Contents/MacOS/BungeeBiker
```

### Missing dependencies

Make sure all files are included in the build:
```bash
# For PyInstaller, check the spec file includes all data files
# For py2app, check setup.py includes all data files
```

### Reduce app size

The bundled app can be large. To reduce size:

**PyInstaller:**
```bash
# In build_macos.spec, set:
# upx=True (already enabled)
# strip=True
```

**py2app:**
```bash
# In setup.py OPTIONS, add:
# 'optimize': 2 (already enabled)
# 'compressed': True
```

## Code Signing (Optional but Recommended)

For distribution outside the App Store, sign your app:

### Prerequisites
- Apple Developer account
- Developer ID certificate

### Sign the app
```bash
codesign --force --deep --sign "Developer ID Application: Your Name" \
         dist/BungeeBiker.app
```

### Verify signature
```bash
codesign --verify --verbose dist/BungeeBiker.app
spctl --assess --verbose dist/BungeeBiker.app
```

### Notarize (for macOS 10.15+)
```bash
# Create a ZIP
ditto -c -k --keepParent dist/BungeeBiker.app BungeeBiker.zip

# Submit for notarization
xcrun notarytool submit BungeeBiker.zip \
    --apple-id "your@email.com" \
    --team-id "TEAMID" \
    --password "app-specific-password" \
    --wait

# Staple the ticket
xcrun stapler staple dist/BungeeBiker.app
```

## Build Configuration

### App Information

Edit these files to customize app metadata:

**PyInstaller** - `build_macos.spec`:
```python
info_plist={
    'CFBundleName': 'Bungee Biker',
    'CFBundleVersion': '0.1.0',
    # ... other settings
}
```

**py2app** - `setup.py`:
```python
'plist': {
    'CFBundleName': 'Bungee Biker',
    'CFBundleVersion': '0.1.0',
    # ... other settings
}
```

## File Structure

After building, your app bundle structure looks like:

```
BungeeBiker.app/
├── Contents/
│   ├── Info.plist          # App metadata
│   ├── MacOS/
│   │   └── BungeeBiker     # Executable
│   ├── Resources/
│   │   ├── icon.icns       # App icon
│   │   ├── assets/         # Game assets
│   │   └── src/            # Python source
│   └── Frameworks/         # Python + dependencies
```

## Distribution Checklist

Before distributing your app:

- [ ] Test on a clean macOS system
- [ ] Verify all assets load correctly
- [ ] Check app icon appears properly
- [ ] Test all game features work
- [ ] Sign the app (if distributing publicly)
- [ ] Notarize (for macOS 10.15+)
- [ ] Create README/documentation
- [ ] Create DMG installer
- [ ] Test DMG installation

## File Sizes

Typical build sizes:

- **PyInstaller**: ~80-120 MB
- **py2app**: ~70-100 MB
- **DMG (compressed)**: ~40-60 MB

Size can be reduced by:
- Removing debug symbols (`strip=True`)
- Using UPX compression
- Excluding unnecessary pygame/numpy modules

## Support

If you encounter issues:

1. Check the terminal output for error messages
2. Verify all dependencies are installed
3. Try building with the alternative method
4. Check PyInstaller/py2app documentation
5. Open an issue with build logs

## Advanced: Universal Binary (Apple Silicon + Intel)

To build for both architectures:

```bash
# Build for current architecture
pyinstaller build_macos.spec

# For universal binary, use py2app on Apple Silicon Mac
python setup.py py2app --arch=universal2
```

Note: PyInstaller currently creates single-architecture builds.

---

**Ready to build?** Run `./build_macos.sh` and follow the prompts!
