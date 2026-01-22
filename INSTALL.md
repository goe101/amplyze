
# Installation & Setup Guide

## 🖥️ Windows

### Option 1: Run from Source (Recommended for Developers)
1. Install [Python 3.8+](https://www.python.org/downloads/).
2. Open PowerShell or Command Prompt in the project folder.
3. Create a virtual environment (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install requirements:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run the app:
   ```powershell
   python amplyze.py
   ```

### Option 2: Build Executable
1. Install PyInstaller: `pip install pyinstaller`
2. Run the build script:
   ```powershell
   .\build_windows.bat
   ```
3. The `.exe` will be in the `dist` folder.

---

## 🐧 Linux

### Option 1: Run from Source
1. Install Python 3 and pip.
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```
2. Create environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python3 amplyze.py
   ```

   *Note: If you encounter serial permission errors:*
   ```bash
   sudo usermod -a -G dialout $USER
   # Logout and login required
   ```

### Option 2: Build Executable
1. Install PyInstaller: `pip install pyinstaller`
2. Run the build script:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
3. The binary will be in `dist/`.
