#include <Wire.h>

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

uint16_t readWord(uint8_t cmd) {
  Wire.beginTransmission(batteryAddress);
  Wire.write(cmd);
  if (Wire.endTransmission(false) != 0)
    return 0xFFFF; // Error

  Wire.requestFrom(batteryAddress, (uint8_t)2);
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
  // Read Data
  uint16_t voltage = readWord(CMD_VOLTAGE);         // mV
  int16_t current = (int16_t)readWord(CMD_CURRENT); // mA
  uint16_t tempRaw = readWord(CMD_TEMPERATURE);     // 0.1K
  uint16_t remCap = readWord(CMD_REMAIN_CAP);       // mAh
  uint16_t fullCap = readWord(CMD_FULL_CAP);        // mAh
  uint16_t cycles = readWord(CMD_CYCLE_COUNT);      // count

  // Calculate Temperature in Celsius
  float temperatureC = (tempRaw / 10.0) - 273.15;
  if (tempRaw == 0xFFFF)
    temperatureC = 0.0; // Error handling

  // Create JSON compatible with Amplyze App
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

  // 2. Compatibility Fields (Mocked or Default for Standard SMBus)
  Serial.print(",\"SafetyStatus\":");
  Serial.print(0); // 0 = OK
  Serial.print(",\"PF_Status\":");
  Serial.print(0); // 0 = OK
  Serial.print(",\"GaugeType\":");
  Serial.print("\"SMBus Generic\"");

  // 3. Cells (Empty list as standard SMBus doesn't give individual cells
  // easily)
  Serial.print(",\"Cells\":[]");

  // 4. Extended Fields (New)
  Serial.print(",\"RemainCapacity_mAh\":");
  Serial.print(remCap);
  Serial.print(",\"FullCapacity_mAh\":");
  Serial.print(fullCap);

  Serial.println("}");

  delay(1000);
}
