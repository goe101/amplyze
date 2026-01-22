
import serial
import serial.tools.list_ports
import random
import json
import time

class BMSManager:
    def __init__(self, baudrate=115200):
        self.baudrate = baudrate
        self.ser = None

    def connect(self, port_name):
        """Connect to the specified serial port."""
        if self.ser and self.ser.is_open:
            self.ser.close()
        
        # Clean port name if it comes from the description string
        clean_port = port_name.split(" - ")[0].strip()
        
        self.ser = serial.Serial(clean_port, self.baudrate, timeout=2)
        time.sleep(1) # Wait for connection to stabilize
        return clean_port

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.ser = None

    def is_connected(self):
        return self.ser is not None and self.ser.is_open

    def read_data(self, simulation_mode=False):
        """Read data from BMS or generate fake data."""
        if simulation_mode:
            return self.generate_fake_data()
        
        if not self.is_connected():
            raise ConnectionError("Not connected to BMS")
            
        self.ser.write(b'READ_ALL\n')
        line = self.ser.readline().decode().strip()
        if not line:
            raise ValueError("No data received from BMS")
            
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid data received: {line}")

    @staticmethod
    def get_com_ports():
        """Retrieve a list of available USB COM ports with detailed information."""
        ports = []
        for port in serial.tools.list_ports.comports():
            # Filter for USB ports only
            is_usb = False
            
            # Check device path (Linux: /dev/ttyUSB*, /dev/ttyACM* are USB ports)
            if port.device.startswith('/dev/ttyUSB') or port.device.startswith('/dev/ttyACM'):
                is_usb = True
            # Check description for USB keyword
            elif port.description and 'USB' in port.description:
                is_usb = True
            # Check hwid for USB keyword
            elif hasattr(port, 'hwid') and port.hwid and 'USB' in port.hwid:
                is_usb = True
            
            if is_usb:
                # Format: "COM3 - Device Description" or just "COM3" if no description
                if port.description and port.description != 'n/a':
                    ports.append(f"{port.device} - {port.description}")
                else:
                    ports.append(port.device)
        return ports

    @staticmethod
    def generate_fake_data():
        try:
            cells = [random.randint(3700, 3900) for _ in range(4)]
            return {
                "PackVoltage_mV": random.randint(14000, 16800),
                "Current_mA": random.randint(25, 500),
                "Temperature_C": random.randint(15, 45),
                "CycleCount": random.randint(0, 500),
                "SafetyStatus": random.randint(0, 31),
                "PF_Status": random.randint(0, 31),
                "GaugeType": "BQ27545",
                "Cells": cells,
                "RemainCapacity_mAh": random.randint(1000, 2000),
                "FullCapacity_mAh": 2500
            }
        except Exception as e:
            print(f"Error generating fake data: {e}")
            return {}

    @staticmethod
    def decode_safety_status(val):
        flags = []
        if val & (1 << 1): flags.append("Overvoltage")
        if val & (1 << 2): flags.append("Undervoltage")
        if val & (1 << 3): flags.append("Overtemperature")
        if val & (1 << 4): flags.append("Short Circuit")
        if not flags:
            return "OK"
        return ", ".join(flags)

    @staticmethod
    def decode_pf_status(val):
        flags = []
        if val & (1 << 0): flags.append("Fuse Blow Event")
        if val & (1 << 1): flags.append("Cell Overvoltage")
        if val & (1 << 2): flags.append("Cell Undervoltage")
        if val & (1 << 3): flags.append("Overtemperature")
        if val & (1 << 4): flags.append("Charge Timeout")
        if not flags:
            return "No Permanent Failure"
        return ", ".join(flags)
