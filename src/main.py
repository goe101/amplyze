
import sys
import os
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import BMSGUIMain

def main():
    # Environment fixes for Linux/Wayland
    # Remove snap-related environment variables that cause library conflicts
    for snap_var in ['SNAP', 'SNAP_NAME', 'SNAP_VERSION', 'SNAP_REVISION', 'SNAP_ARCH', 'SNAP_LIBRARY_PATH']:
        os.environ.pop(snap_var, None)

    # Clear LD_PRELOAD to avoid library conflicts
    os.environ['LD_PRELOAD'] = ''

    if 'QT_QPA_PLATFORM' not in os.environ:
         if os.environ.get('WAYLAND_DISPLAY'):
             os.environ['QT_QPA_PLATFORM'] = 'wayland'
         elif os.environ.get('DISPLAY'):
             os.environ['QT_QPA_PLATFORM'] = 'xcb'

    app = QApplication(sys.argv)
    window = BMSGUIMain()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
