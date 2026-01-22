
# Amplyze - Modern BMS Analyzer

Amplyze is a professional Battery Management System (BMS) analysis tool designed for cross-platform usage (Windows & Linux). It allows engineers to monitor cell voltages, check safety status, and generate PDF reports in real-time.

![Amplyze Logo](assets/amplyze_logo.png)

## ✨ Features

- **Real-time Monitoring**: Visualize Pack Voltage, Current, Temperature, and Cell Voltages.
- **Safety Analysis**: Instant decoding of Safety Status and Permanent Fail (PF) flags.
- **Interactive Plots**: Analyze cell voltage balance with interactive Matplotlib graphs.
- **PDF Reporting**: Generate professional inspection reports with one click.
- **Cross-Platform**: Runs natively on Windows and Linux.
- **Simulation Mode**: Test the UI and features without hardware.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amplyze.git
   cd amplyze
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python amplyze.py
   ```

## 📦 Building Standalone Executables

We provide scripts to bundle the application into a single executable file.

- **Windows**: Run `build_windows.bat`
- **Linux**: Run `./build_linux.sh`

The output will be placed in the `dist/` directory.

## 📂 Project Structure

```
amplyze/
├── amplyze.py           # Entry point
├── src/                 # Source code
│   ├── core/            # BMS logic & serial communication
│   ├── ui/              # GUI components
│   └── utils/           # Report generation & helpers
├── assets/              # Icons & resources
└── reports/             # Generated PDF reports
```

## 📄 License
MIT License.
