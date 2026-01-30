#!/bin/bash

# Nimar PDF Converter Build Script
# This script builds a single executable file for the application

set -e  # Exit on any error

echo "🔨 Building Nimar PDF Converter..."
echo "=================================="

# Check if PyInstaller is available
if ! python3 -m PyInstaller --version &> /dev/null; then
    echo "❌ PyInstaller not found. Installing..."
    pip3 install pyinstaller
else
    echo "✅ PyInstaller found"
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Create simple app icon (text-based if no icon available)
echo "🎨 Creating application icon..."
mkdir -p src/resources/icons

# Create a simple text-based icon description for now
echo "Creating icon resources..."

# Check requirements
echo "📦 Checking requirements..."
python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.') / 'src'))

try:
    from gui.main_window import MainWindow
    print('✅ Main window imports correctly')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)

try:
    from conversion.converter import DocumentConverter
    print('✅ Converter imports correctly')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Build the application
echo "🏗️  Building executable..."
python3 -m PyInstaller simple.spec

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📦 Executable created:"
    if [ -f "dist/NimarPDFConverter" ]; then
        echo "  Linux: dist/NimarPDFConverter"
        ls -lh "dist/NimarPDFConverter"
    elif [ -f "dist/NimarPDFConverter.exe" ]; then
        echo "  Windows: dist/NimarPDFConverter.exe"
        ls -lh "dist/NimarPDFConverter.exe"
    fi
    echo ""
    echo "🚀 Ready for distribution!"
    echo ""
    echo "To run the application:"
    echo "  ./dist/NimarPDFConverter"
else
    echo "❌ Build failed!"
    exit 1
fi