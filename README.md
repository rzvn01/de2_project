### Team Members

- Barbulet Ana-Maria
- Cacu Razvan
- Gavrila Andreea

## Theoretical Description and Explanation

Our project focuses on implementing a versatile system that combines various sensors, such as Light Dependent Resistors (LDRs), water sensors, and a BME280 sensor, with an OLED display. The goal is to create a portable device that can monitor environmental conditions, providing real-time data on light levels, water presence, temperature, humidity, and pressure. The system utilizes MicroPython, making it easy to deploy and program.

## Hardware Description of Demo Application

Our hardware setup includes:

- Microcontroller (e.g., ESP8266): Serves as the brain of the system, running MicroPython.
- OLED Display (e.g., SH1106): Displays information collected from sensors.
- Light Dependent Resistors (LDRs): Measure ambient light levels.
- Water Sensors: Detect the presence of water.
- BME280 Sensor: Measures temperature, humidity, and pressure.

### Wiring Schematic

Include a schematic diagram of your hardware setup here.

## Software Description

The software consists of several components:

1. **LDR Class:**
   - Represents the Light Dependent Resistor sensor, allowing reading of light levels.
   - Source File: `ldr.py`
   - Usage: `ldr = LDR(pin)`

2. **WaterSensor Class:**
   - Represents the water sensor, capable of detecting water presence.
   - Source File: [water_sensor.py](https://github.com/rzvn01/de2_project/blob/main/src/utilities/bme280.py)
   - Usage: `water_sensor = WaterSensor(pin)`

3. **BME280 Class:**
   - Represents the BME280 sensor, providing methods for reading temperature, humidity, and pressure.
   - Source File: `bme280.py`
   - Usage: `bme = BME280()`

4. **WiFiManager Class:**
   - Manages Wi-Fi connectivity for the device.
   - Source File: `wifi_manager.py`
   - Usage: `wifi_manager = WiFiManager(ssid, password)`

5. **OLED Display Class (SH1106):**
   - Manages the OLED display.
   - Source File: `sh1106.py`
   - Usage: `oled = SH1106_I2C(width, height, i2c, addr, rotate)`

## Instructions

**Setting Up the Hardware:**

1. Connect LDRs, water sensors, the BME280 sensor, and the OLED display to the microcontroller according to the provided schematic.
2. Power up the microcontroller.

**Flashing MicroPython:**

1. Follow the MicroPython installation guide for your microcontroller.
2. Upload the provided Python files to the microcontroller.

**Running the Application:**

1. Power on the device.
2. The OLED display should show real-time data from the sensors, including light levels, water presence, temperature, humidity, and pressure.

**Troubleshooting:**

- If the device fails to connect to Wi-Fi, check your credentials and network availability.
- Ensure the sensors are correctly wired.

**Demo Video:**

[Link to Demo Video](insert_link_here)

## References

1. MicroPython Documentation: [MicroPython](https://micropython.org/)
2. SH1106 OLED Driver Source Code: `sh1106.py`
3. ESP8266 Documentation: [ESP8266 MicroPython](https://docs.micropython.org/en/latest/esp8266/)
4. BME280 Datasheet: [BME280 Datasheet](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf)
