# Build script for Nimar PDF Converter

This script builds the Nimar PDF Converter into a single executable file.

## Requirements
- Python 3.8+
- PyInstaller (installed via pip install pyinstaller)

## Build Process
1. Run: `./build.sh`
2. Executable will be created in `dist/` directory

## Supported Platforms
- Linux: 64-bit executable
- Windows: .exe file (run on Windows)
- macOS: .app bundle (run on macOS)

## Output
The build creates:
- `NimarPDFConverter` (Linux executable)
- `NimarPDFConverter.exe` (Windows executable)
- `NimarPDFConverter.app` (macOS application bundle)

## Dependencies
All required Python packages are bundled into the executable.
No separate Python installation needed.