#include <Arduino.h>
#include <Wire.h>
#include <stdint.h>

#define SDA_PIN 21
#define SCL_PIN 22

// Standard Smart Battery Address
uint8_t batteryAddress = 0x0B;

// SMBus Standard Commands
#define CMD_VOLTAGE 0x09
#define CMD_CURRENT 0x0A
#define CMD_TEMPERATURE 0x08
#define CMD_REMAIN_CAP 0x0F
#define CMD_FULL_CAP 0x10
#define CMD_CYCLE_COUNT 0x17
#define CMD_BATTERY_STATUS 0x16

// Cell Voltage Commands (Typical for TI BQ series)
// 0x3C is typically lowest cell (Cell 1)
#define CMD_CELL1_ADDR 0x3C
#define CMD_CELL2_ADDR 0x3D
#define CMD_CELL3_ADDR 0x3E
#define CMD_CELL4_ADDR 0x3F

uint16_t readWord(uint8_t cmd) {
  Wire.beginTransmission(batteryAddress);
  Wire.write(cmd);
  if (Wire.endTransmission(false) != 0)
    return 0xFFFF; // Error

  Wire.requestFrom((uint8_t)batteryAddress, (uint8_t)2);
  if (Wire.available() < 2)
    return 0xFFFF;

  uint8_t low = Wire.read();
  uint8_t high = Wire.read();

  return (high << 8) | low;
}

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(100000); // Standard SMBus 100kHz
  delay(1000);

  Serial.println("ESP32 SMBus Battery Reader Started");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "READ_ALL") {
      // Read Data
      uint16_t voltage = readWord(CMD_VOLTAGE);         // mV
      int16_t current = (int16_t)readWord(CMD_CURRENT); // mA
      uint16_t tempRaw = readWord(CMD_TEMPERATURE);     // 0.1K
      uint16_t remCap = readWord(CMD_REMAIN_CAP);       // mAh
      uint16_t fullCap = readWord(CMD_FULL_CAP);        // mAh
      uint16_t cycles = readWord(CMD_CYCLE_COUNT);      // count
      uint16_t status = readWord(CMD_BATTERY_STATUS);   // Battery Status

      // Read Cells
      uint16_t val_cell1 = readWord(CMD_CELL1_ADDR);
      uint16_t val_cell2 = readWord(CMD_CELL2_ADDR);
      uint16_t val_cell3 = readWord(CMD_CELL3_ADDR);
      uint16_t val_cell4 = readWord(CMD_CELL4_ADDR);

      // Calculate Temperature in Celsius
      float temperatureC = (tempRaw / 10.0) - 273.15;
      if (tempRaw == 0xFFFF)
        temperatureC = 0.0; // Error handling

      // Create JSON response
      Serial.print("{");

      // 1. Required Fields
      Serial.print("\"PackVoltage_mV\":");
      Serial.print(voltage);
      Serial.print(",\"Current_mA\":");
      Serial.print(current);
      Serial.print(",\"Temperature_C\":");
      Serial.print(temperatureC, 1);
      Serial.print(",\"CycleCount\":");
      Serial.print(cycles);

      // 2. Compatibility & Status (Mapping status bits if possible, or 0)
      // Sending raw 0 for now as 'Safe' but we could try to map status ->
      // SafetyStatus
      Serial.print(",\"SafetyStatus\":");
      Serial.print(0);
      Serial.print(",\"PF_Status\":");
      Serial.print(0);
      Serial.print(",\"GaugeType\":");
      Serial.print("\"SMBus Standard\"");

      // 3. Cells
      Serial.print(",\"Cells\":[");
      uint16_t raw_cells[] = {val_cell1, val_cell2, val_cell3, val_cell4};
      bool first = true;
      for (int i = 0; i < 4; i++) {
        uint16_t c = raw_cells[i];
        if (c != 0xFFFF && c > 0) {
          if (!first)
            Serial.print(",");
          Serial.print(c);
          first = false;
        }
      }
      Serial.print("]");

      // 4. Extended Fields
      Serial.print(",\"RemainCapacity_mAh\":");
      Serial.print(remCap);
      Serial.print(",\"FullCapacity_mAh\":");
      Serial.print(fullCap);

      Serial.println("}");
    }
  }
}
