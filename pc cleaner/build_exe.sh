#!/bin/bash

echo "=================================================="
echo "🚀 Building Standalone Windows Executable (.exe)..."
echo "=================================================="

# Verify source script exists
if [ ! -f "cleaner.py" ]; then
    echo "❌ Error: 'cleaner.py' not found in this folder!"
    exit 1
fi

# Check if icon exists, warn if missing but proceed
ICON_OPTION=""
if [ -f "spanner.ico" ]; then
    echo "➔ Found spanner.ico. Applying icon metadata..."
    ICON_OPTION="--icon=spanner.ico"
else
    echo "⚠️ Warning: 'spanner.ico' not found. Building with standard default Windows icon."
fi

# Check if pyinstaller is available
if ! command -v pyinstaller &> /dev/null
then
    echo "❌ Error: 'pyinstaller' command not recognized."
    echo "➔ Please run './install_dependencies.sh' first."
    exit 1
fi

# Run compilation
echo "➔ Compiling using PyInstaller..."
pyinstaller --noconsole --onefile $ICON_OPTION cleaner.py

if [ $? -eq 0 ]; then
    echo "=================================================="
    echo "🎉 Compilation Complete!"
    echo "➔ You can find your new application inside the 'dist' folder:"
    echo "   📁 ./dist/cleaner.exe"
    echo "=================================================="
else
    echo "❌ Error: PyInstaller encountered a compilation failure."
fi