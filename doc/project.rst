.. _project:

Project Overview
================

Our project focuses on implementing a versatile system that combines various sensors, such as Light Dependent Resistors (LDRs), water sensors, and a BME280 sensor, with an OLED display. The goal is to create a portable device that can monitor environmental conditions, providing real-time data on light levels, water presence, temperature, humidity, and pressure. The system utilizes MicroPython, making it easy to deploy and program.

**You can find the Git repository for the project** `here. <https://github.com/rzvn01/de2_project/>`_

.. contents:: Table of Contents
   :local:
   :depth: 3

Hardware Description of Demo Application
------------

1. **Microcontroller (e.g., ESP8266)**: The ESP32 serves as the central processing unit running MicroPython, handling sensor data, connecting to Wi-Fi, and driving the display.

2. **OLED Display (e.g., SH1106)**: Displays information collected from sensors.

3. **Light Dependent Resistors (LDRs)**: Measure ambient light levels.

4. **Water Sensors**: Detect the presence of water.

5. **BME280 Sensor**: Measures temperature, humidity, and pressure.


Software Description
------------
This project contains a main.py file, as well as several utility classes, both of which can be found in the current documentation, in the original table of contents on the first page.

Instructions
------------

**Setting Up the Hardware**
    1. Connect LDRs, water sensors, the BME280 sensor, and the OLED display to the microcontroller according to the schematic provided below.
    2. Power up the microcontroller.

    |   
    .. image:: _static/schematic_diagram.png
        :alt: Circuit schematic


**Flashing MicroPython**
    1. Download MicroPython firmware.
    2. Flash the firmware.
    3. Connect to the Board's Serial REPL and interact with MicroPython.
    4. Transfer files to the ESP32 board.

There are several very good tutorials how to install and use MicroPython on an ESP microcontroller, such as `this one <https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html/>`_  for Windows.

NOTE: The MicroPython firmware can also be flashed by Thonny IDE.

**Running the Application**
    1. Power on the device.
    2. Make sure all files are saved into microcontroller's memory.
    3. The displays should show real-time data from the sensors, including light levels, water presence, temperature, humidity, and pressure.

**Troubleshooting**
    1. The wrapper for functionality must be saved as main.py in order to get the desired behaviour for deepsleep() function.
    2. If the device fails to connect to Wi-Fi, check your credentials and network availability.
    3. Ensure the sensors are correctly wired.
    4. Make sure all packages are up-to-date and not deprecated.


**Demo video**
    You can find a short video demonstrating the project functionality `here! <https://github-production-user-asset-6210df.s3.amazonaws.com/100044309/288198043-b4316866-3fb9-4cb9-b8db-3046aaa8ed4d.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231205%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231205T212200Z&X-Amz-Expires=300&X-Amz-Signature=23d58c3d78d4905623290399ac13997d8c84b4cf8f86222df5795fdf93ee4fe4&X-Amz-SignedHeaders=host&actor_id=148204733&key_id=0&repo_id=721313266/>`_

References
------------
1. MicroPython Documentation: `MicroPython <https://micropython.org/>`_
2. SH1106 OLED Driver Source Code: `sh1106.py <https://github.com/robert-hh/SH1106/>`_
3. ESP8266 Documentation: `ESP8266 MicroPython <https://docs.micropython.org/en/latest/esp32/quickref.html/>`_
4. BME280 Datasheet: `BME280 Datasheet <https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf/>`_
