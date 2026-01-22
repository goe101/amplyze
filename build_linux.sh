
#!/bin/bash
echo "Building Amplyze for Linux..."

# Check requirements
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean
rm -rf build dist *.spec

# Build
pyinstaller --noconfirm \
            --onefile \
            --windowed \
            --name "Amplyze" \
            --icon "assets/icons/amplyze_64.png" \
            --add-data "assets:assets" \
            amplyze.py

echo "Build complete! Binary is in dist/Amplyze"
