
BAUDRATE = 115200

APP_STYLE = """
QWidget { 
    font-family: 'Segoe UI', Arial, sans-serif; 
    font-size: 11px;
    background-color: #f5f5f5;
}
QLabel {
    color: #333;
}
QGroupBox { 
    font-weight: bold; 
    border: 2px solid #dcdcdc; 
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 8px;
    color: #003045;
}
QGroupBox::title { 
    subcontrol-origin: margin; 
    left: 10px; 
    padding: 0 3px 0 3px; 
}
QPushButton { 
    background: linear-gradient(135deg, #007acc 0%, #005a9e 100%);
    color: white; 
    border: none;
    border-radius: 4px; 
    padding: 8px 16px;
    font-weight: 600;
    font-size: 11px;
}
QPushButton:hover {
    background: linear-gradient(135deg, #0098ff 0%, #007acc 100%);
}
QPushButton:pressed {
    background: linear-gradient(135deg, #005a9e 0%, #003a6f 100%);
}
QPushButton#ghost { 
    background: transparent; 
    color: #007acc; 
    border: 2px solid #007acc;
    font-weight: 600;
}
QPushButton#ghost:hover {
    background: rgba(0, 122, 204, 0.1);
    color: #0098ff;
    border: 2px solid #0098ff;
}
QComboBox {
    background: white;
    border: 2px solid #dcdcdc;
    border-radius: 4px;
    padding: 4px 8px;
    color: #333;
}
QComboBox:focus {
    border: 2px solid #007acc;
}
QTableWidget {
    background: white;
    gridline-color: #e0e0e0;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
}
QTableWidget::item {
    padding: 4px;
}
QHeaderView::section {
    background: #f0f0f0;
    color: #003045;
    padding: 4px;
    border: none;
    font-weight: bold;
}
QCheckBox {
    color: #333;
    spacing: 6px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #dcdcdc;
    border-radius: 3px;
    background: white;
}
QCheckBox::indicator:checked {
    background: #007acc;
    border: 2px solid #007acc;
}
QDialog {
    background-color: #f5f5f5;
}
QMessageBox QLabel {
    color: #333;
}
QMessageBox QPushButton {
    min-width: 70px;
    min-height: 28px;
    color: #333;
    background: #e8e8e8;
    border: 1px solid #999;
    padding: 4px 12px;
}
QMessageBox QPushButton:hover {
    background: #d0d0d0;
    border: 1px solid #666;
}
QDialog QPushButton {
    min-width: 70px;
    min-height: 28px;
    color: #333;
    background: #e8e8e8;
    border: 1px solid #999;
    padding: 4px 12px;
}
QDialog QPushButton:hover {
    background: #d0d0d0;
    border: 1px solid #666;
}
"""
