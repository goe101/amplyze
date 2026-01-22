
import os
import sys
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QComboBox, QCheckBox, QGroupBox, QFormLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, 
    QMenuBar, QAction, QDialog, QSizePolicy
)
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.core.bms import BMSManager
from src.utils.constants import APP_STYLE
from src.utils.report_generator import generate_pdf_report

class BMSGUIMain(QWidget):
    def __init__(self):
        super().__init__()
        self.bms_manager = BMSManager()
        self.data_cache = {}
        
        self.setWindowTitle("Amplyze - BMS Analyzer")
        self.setGeometry(100, 100, 1100, 800)
        self.setStyleSheet(APP_STYLE)
        
        self.init_assets()
        self.init_ui()
        
        # Initial COM port load
        self.refresh_com_list()
        
    def init_assets(self):
        """Setup paths and icons."""
        # Assume running from project root
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.assets_dir = os.path.join(self.project_root, "assets")
        self.reports_dir = os.path.join(self.project_root, "reports")
        
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Set window icon
        icon_path = os.path.join(self.assets_dir, "icons", "amplyze_64.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # Menu
        menubar = QMenuBar()
        file_menu = menubar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Controls Group
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        
        control_layout.addWidget(QLabel("COM Port:"))
        self.com_list = QComboBox()
        self.com_list.setMinimumWidth(200)
        control_layout.addWidget(self.com_list)
        
        self.btn_refresh_ports = QPushButton("⟳")
        self.btn_refresh_ports.setObjectName('ghost')
        self.btn_refresh_ports.setMaximumWidth(40)
        self.btn_refresh_ports.setToolTip('Refresh COM ports')
        self.btn_refresh_ports.clicked.connect(self.refresh_com_list)
        control_layout.addWidget(self.btn_refresh_ports)
        
        self.btn_connect = QPushButton("Connect")
        self.btn_connect.setObjectName('ghost')
        self.btn_connect.clicked.connect(self.toggle_connection)
        control_layout.addWidget(self.btn_connect)
        
        control_layout.addStretch()
        
        self.simulation_mode = QCheckBox("Simulation Mode")
        self.simulation_mode.setToolTip('Toggle simulated data')
        control_layout.addWidget(self.simulation_mode)
        
        main_layout.addLayout(control_layout)
        
        # Header / toolbar
        header_layout = QHBoxLayout()
        title = QLabel("Battery Management System (BMS) Analyzer")
        title.setStyleSheet('font-size:20px; font-weight:600; color: #003045;')
        header_layout.addWidget(title)
        
        self.btn_read = QPushButton("Read Data")
        self.btn_read.setObjectName('ghost')
        self.btn_read.clicked.connect(self.read_bms)
        header_layout.addWidget(self.btn_read)
        
        self.btn_save = QPushButton("Save Report")
        self.btn_save.setObjectName('ghost')
        self.btn_save.clicked.connect(self.save_report)
        header_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(header_layout)
        
        # Data Summary
        summary = QGroupBox("Battery Summary")
        form = QFormLayout()
        self.labels = {}
        fields = [
            "Pack Voltage (mV)", "Current (mA)", "Temperature (C)", 
            "Cycle Count", "Safety Status", "PF Status", "Gauge Type",
            "Remain Capacity (mAh)", "Full Capacity (mAh)"
        ]
        
        # Optimize Summary Layout (Grid instead of long form?)
        # Let's keep form but maybe make it 2 columns if needed? 
        # Current form is fine for top section.
        for f in fields:
            lbl = QLabel("----")
            lbl.setStyleSheet('font-weight:600; color: #007acc;')
            form.addRow(QLabel(f+":"), lbl)
            self.labels[f] = lbl
        summary.setLayout(form)
        main_layout.addWidget(summary)
        
        # --- Middle Section: Split Table and Plot ---
        middle_layout = QHBoxLayout()
        middle_layout.setSpacing(12)

        # Cells Table (Left)
        cells_group = QGroupBox("Cell Voltages")
        cells_layout = QVBoxLayout()
        self.cell_table = QTableWidget(0, 2)
        self.cell_table.setHorizontalHeaderLabels(["Cell #", "Voltage (mV)"])
        self.cell_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.cell_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # Removed maximum height to allow it to fill space
        self.cell_table.setAlternatingRowColors(True)
        cells_layout.addWidget(self.cell_table)
        cells_group.setLayout(cells_layout)
        middle_layout.addWidget(cells_group, 1) # Stretch 1

        # Embedded Plot (Right)
        plot_group = QGroupBox("Voltage Analysis")
        plot_layout = QVBoxLayout()
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout()
        plot_layout.addWidget(self.canvas)
        plot_group.setLayout(plot_layout)
        middle_layout.addWidget(plot_group, 2) # Stretch 2 (Wider)
        
        main_layout.addLayout(middle_layout)
        
        # Status Bar
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet('color: #666; font-style: italic;')
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)

    def refresh_com_list(self):
        self.com_list.clear()
        ports = self.bms_manager.get_com_ports()
        if not ports:
            self.com_list.addItem("No Ports Detected")
        else:
            self.com_list.addItems(ports)
            self.com_list.setCurrentIndex(0)

    def toggle_connection(self):
        if self.bms_manager.is_connected():
            self.bms_manager.disconnect()
            self.btn_connect.setText("Connect")
            self.status_label.setText("Status: Disconnected")
            self.com_list.setEnabled(True)
        else:
            port = self.com_list.currentText()
            if "No Ports" in port:
                return
            
            try:
                clean_port = self.bms_manager.connect(port)
                self.btn_connect.setText("Disconnect")
                self.status_label.setText(f"Status: Connected to {clean_port}")
                self.com_list.setEnabled(False)
            except Exception as e:
                QMessageBox.critical(self, "Connection Error", str(e))

    def read_bms(self):
        try:
            data = self.bms_manager.read_data(simulation_mode=self.simulation_mode.isChecked())
            self.data_cache = data # Store for plotting/reporting
            
            # Update labels with .get() for robustness
            self.labels["Pack Voltage (mV)"].setText(str(data.get("PackVoltage_mV", "---")))
            self.labels["Current (mA)"].setText(str(data.get("Current_mA", "---")))
            self.labels["Temperature (C)"].setText(str(data.get("Temperature_C", "---")))
            self.labels["Cycle Count"].setText(str(data.get("CycleCount", "---")))
            self.labels["Gauge Type"].setText(str(data.get("GaugeType", "Unknown")))
            self.labels["Remain Capacity (mAh)"].setText(str(data.get("RemainCapacity_mAh", "---")))
            self.labels["Full Capacity (mAh)"].setText(str(data.get("FullCapacity_mAh", "---")))

            
            # Decode statuses (default to 0 if missing)
            s_status = self.bms_manager.decode_safety_status(int(data.get("SafetyStatus", 0)))
            pf_status = self.bms_manager.decode_pf_status(int(data.get("PF_Status", 0)))
            
            self.labels["Safety Status"].setText(s_status)
            self.labels["PF Status"].setText(pf_status)
            
            # Store formatted strings for report
            self.data_cache['SafetyStatusStr'] = s_status
            self.data_cache['PFStatusStr'] = pf_status
            
            # Update Table
            cells = data.get("Cells", [])
            self.cell_table.setRowCount(len(cells))
            for i, v in enumerate(cells):
                self.cell_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
                self.cell_table.setItem(i, 1, QTableWidgetItem(str(v)))

            # Update embedded plot
            self.update_plot()
            
        except Exception as e:
            QMessageBox.warning(self, "Read Error", str(e))

    def update_plot(self):
        cells = self.data_cache.get("Cells", [])
        self.ax.clear()
        
        if not cells:
            self.ax.text(0.5, 0.5, 'No Data', horizontalalignment='center', verticalalignment='center')
        else:
            x = list(range(1, len(cells) + 1))
            self.ax.plot(x, cells, marker='o', linewidth=2, color='#007acc')
            self.ax.fill_between(x, cells, alpha=0.1, color='#007acc')
            self.ax.set_title("Cell Voltages", fontsize=10)
            self.ax.set_xlabel("Cell #", fontsize=8)
            self.ax.set_ylabel("mV", fontsize=8)
            self.ax.grid(True, linestyle='--', alpha=0.6)
            self.ax.set_xticks(x)

        self.canvas.draw()

    def save_report(self):
        if not self.data_cache:
            QMessageBox.warning(self, "No Data", "Please read data first.")
            return
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        default_name = f"Amplyze_Report_{timestamp}.pdf"
        default_path = os.path.join(self.reports_dir, default_name)
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", default_path, "PDF Files (*.pdf)")
        if not save_path:
            return
            
        logo_path = os.path.join(self.assets_dir, "amplyze_logo.png")
        
        success = generate_pdf_report(save_path, self.data_cache, logo_path)
        
        if success:
            QMessageBox.information(self, "Success", f"Report saved to:\n{save_path}")
        else:
            QMessageBox.critical(self, "Error", "Failed to generate report.")

    def show_about(self):
        QMessageBox.about(self, "About Amplyze", 
                          "Amplyze BMS Analyzer\n\nVersion: 2.0.0 (Modular)\n\nSupports Windows & Linux")

