"""
LibreOffice dependency checker and setup helper
"""

import os
import sys
import shutil
import subprocess
import webbrowser
from pathlib import Path
from typing import Tuple, List


class LibreOfficeChecker:
    """Checks LibreOffice availability and helps with installation"""

    def __init__(self):
        self.libreoffice_path = self._find_libreoffice()

    def _find_libreoffice(self) -> str:
        """Find LibreOffice executable on the system"""
        possible_names = []
        search_paths = []

        if sys.platform.startswith("win"):
            possible_names = [
                "soffice.exe",
                "libreoffice.exe",
                "soffice.com",
                "libreoffice.com",
            ]
            search_paths = [
                os.path.expandvars(r"%PROGRAMFILES%\LibreOffice\program"),
                os.path.expandvars(r"%PROGRAMFILES(X86)%\LibreOffice\program"),
            ]

        elif sys.platform.startswith("darwin"):
            possible_names = ["soffice", "libreoffice"]
            search_paths = [
                "/Applications/LibreOffice.app/Contents/MacOS",
                "/opt/homebrew/bin",
                "/usr/local/bin",
            ]

        else:  # Linux
            possible_names = ["libreoffice", "soffice"]
            search_paths = [
                "/usr/bin",
                "/usr/local/bin",
                "/opt/libreoffice/program",
                "/snap/bin" if Path("/snap/bin").exists() else None,
            ]

        # First check system PATH
        for name in possible_names:
            if shutil.which(name):
                return name

        # Then check specific paths
        for path in search_paths:
            if path and Path(path).exists():
                for name in possible_names:
                    exe_path = Path(path) / name
                    if exe_path.exists():
                        return str(exe_path)

        return ""

    def is_available(self) -> bool:
        """Check if LibreOffice is available"""
        return self.libreoffice_path is not None

    def get_version(self) -> str:
        """Get LibreOffice version if available"""
        if not self.is_available():
            return "Not installed"

        try:
            result = subprocess.run(
                [self.libreoffice_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # Extract version from output
                output = result.stdout
                if "LibreOffice" in output:
                    version_line = output.split("\n")[0]
                    return version_line.strip()

            return "Unknown version"

        except Exception:
            return "Version check failed"

    def get_download_links(self) -> List[Tuple[str, str]]:
        """Get download links for different platforms"""
        links = []

        if sys.platform.startswith("win"):
            links.append(
                (
                    "Windows (64-bit)",
                    "https://www.libreoffice.org/download/download-libreoffice/",
                )
            )
            links.append(
                (
                    "Windows (64-bit) - Direct",
                    "https://download.documentfoundation.org/libreoffice/stable/7.6.5/win/x86_64/LibreOffice_7.6.5_Win_x86-64.msi",
                )
            )
        elif sys.platform.startswith("darwin"):
            links.append(
                ("macOS", "https://www.libreoffice.org/download/download-libreoffice/")
            )
            links.append(
                (
                    "macOS - Direct",
                    "https://download.documentfoundation.org/libreoffice/stable/7.6.5/mac/x86_64/LibreOffice_7.6.5_MacOS_x86-64.dmg",
                )
            )
        else:  # Linux
            links.append(
                (
                    "Linux - Download Page",
                    "https://www.libreoffice.org/download/download-libreoffice/",
                )
            )
            links.append(("Ubuntu/Debian", "sudo apt install libreoffice"))
            links.append(("Fedora/RedHat", "sudo dnf install libreoffice"))
            links.append(("Arch Linux", "sudo pacman -S libreoffice"))

        return links

    def get_install_instructions(self) -> str:
        """Get platform-specific installation instructions"""
        if sys.platform.startswith("win"):
            return """
1. Download LibreOffice from the official website
2. Run the downloaded installer (.msi file)
3. Follow the installation wizard
4. Restart this application
            """
        elif sys.platform.startswith("darwin"):
            return """
1. Download LibreOffice for macOS
2. Open the downloaded .dmg file
3. Drag LibreOffice to Applications folder
4. Launch LibreOffice once to complete setup
5. Restart this application
            """
        else:  # Linux
            return """
Option 1 - Package Manager:
- Ubuntu/Debian: sudo apt update && sudo apt install libreoffice
- Fedora: sudo dnf install libreoffice
- Arch: sudo pacman -S libreoffice

Option 2 - Flatpak:
flatpak install flathub org.libreoffice.LibreOffice

Option 3 - Snap:
sudo snap install libreoffice

After installation, restart this application.
            """

    def open_download_page(self):
        """Open LibreOffice download page in browser"""
        webbrowser.open("https://www.libreoffice.org/download/download-libreoffice/")

    def test_conversion(self, test_file_path: str = "") -> Tuple[bool, str]:
        """Test LibreOffice conversion with a sample file"""
        if not self.is_available():
            return False, "LibreOffice not available"

        # Create a simple test file if not provided
        if not test_file_path:
            test_file_path = os.path.join(os.getcwd(), "test_convert.txt")
            with open(test_file_path, "w", encoding="utf-8") as f:
                f.write("Test document for LibreOffice conversion\n")
                f.write("This is a test file to verify conversion works properly.\n")

        try:
            import tempfile

            with tempfile.TemporaryDirectory() as temp_dir:
                # Try conversion
                cmd = [
                    self.libreoffice_path,
                    "--headless",
                    "--invisible",
                    "--convert-to",
                    "pdf",
                    "--outdir",
                    temp_dir,
                    test_file_path,
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    # Check if PDF was created
                    input_name = Path(test_file_path).stem
                    output_pdf = Path(temp_dir) / f"{input_name}.pdf"

                    if output_pdf.exists():
                        return True, "Conversion test successful"
                    else:
                        return False, "Conversion completed but output file not found"
                else:
                    return False, f"Conversion test failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Conversion test timed out"
        except Exception as e:
            return False, f"Conversion test error: {str(e)}"
        finally:
            # Clean up test file
            if test_file_path and "test_convert.txt" in test_file_path:
                try:
                    os.remove(test_file_path)
                except Exception:
                    pass

