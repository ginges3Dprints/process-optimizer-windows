#!/bin/bash
# Task Master Pro - Standalone Single Binary Compilation Script

echo "========================================="
echo "   Task Master Pro: Build Engine v2.8   "
echo "========================================="

# 1. Clean legacy builds to prevent caching the old layout
echo "[*] Purging legacy compilation artifacts..."
rm -rf build dist __pycache__ *.spec

# 2. Compile into ONE single standalone file with the Spanner Icon
echo "[*] Launching PyInstaller asset packing sequences..."
pyinstaller --noconfirm --onefile --windowed \
    --name "TaskMasterPro" \
    --icon="spanner.ico" \
    --add-data "cleaner_support.py:." \
    --hidden-import="cleaner_support" \
    --hidden-import="psutil" \
    --clean \
    cleaner.py

# 3. Verification pass
if [ -f "dist/TaskMasterPro.exe" ] || [ -d "dist/TaskMasterPro" ]; then
    echo "========================================="
    echo "[+] SUCCESS: Single executable built!"
    echo "[+] You can now grab the file out of 'dist/' and put it anywhere!"
    echo "========================================="
else
    echo "[-] CRITICAL: Compilation routine failed."
fi