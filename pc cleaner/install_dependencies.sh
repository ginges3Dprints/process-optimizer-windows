#!/bin/bash

echo "=================================================="
echo "🔧 Installing Task Master Pro Dependencies..."
echo "=================================================="

# Check if pip is available
if ! command -v pip &> /dev/null
then
    echo "❌ Error: 'pip' could not be found. Please ensure Python is installed and added to your system PATH."
    exit 1
fi

# Install dependencies
echo "➔ Running: pip install pyinstaller psutil"
pip install pyinstaller psutil

if [ $? -eq 0 ]; then
    echo "=================================================="
    echo "✅ Success! PyInstaller and Psutil are ready to use."
    echo "=================================================="
else
    echo "❌ Error: Installation failed. Please check your internet connection or permissions."
fi