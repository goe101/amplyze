
@echo off
echo Building Amplyze for Windows...

:: Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

:: Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Build
pyinstaller --noconfirm ^
            --onefile ^
            --windowed ^
            --name "Amplyze" ^
            --icon "assets/icons/amplyze_64.png" ^
            --add-data "assets;assets" ^
            amplyze.py

echo.
echo Build complete! Executable is in dist/Amplyze.exe
pause
