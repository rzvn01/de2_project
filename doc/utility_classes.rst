.. _utility_classes:


Utility Classes
=========
**You can find the Git repository for the project** `here. <https://github.com/rzvn01/de2_project/>`_


LDR Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Represents the Light Dependent Resistor sensor, allowing reading of light levels. It has the following methods:

1. Method **__init__**: initializes a new instance.
    - parameter pin: A pin that's connected to an LDR.
    - parameter min_value: A min value that can be returned by value() method.
    - parameter max_value: A max value that can be returned by value() method.

2. Method **read**: reads a raw value from the LDR, between 0 and 4095, and returns it.

3. Method **value**: reads a value from the LDR in the specified range and returns a string representing the value in the format "xx.x%".

Usage: *ldr = LDR(pin)*

.. code-block:: python

    from machine import ADC, Pin
    import time


    class LDR:

    def __init__(self, pin, min_value=0, max_value=100):

        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        
        return self.adc.read()

    def value(self):
        
        raw_value = self.read()
        return float(self.max_value - self.min_value) * raw_value / 4095


WaterSensor Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Represents the water sensor, capable of detecting water presence and it has the following methods:

1. Method **__init__**: initializes a new instance.
    -parameter pin: A pin that's connected to a water sensor.

2. Method **read**: reads a raw value from the water sensor.

3. Method **value**: reads a value from the water sensor in the specified range and returns a string representing the value in the format "xx.x%".

Usage: *water_sensor = WaterSensor(pin)*

.. code-block:: python

    from machine import ADC, Pin
    import time

    class WaterSensor:

    def __init__(self, pin, min_value=0, max_value=100):

        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

        self.min_value = min_value
        self.max_value = max_value

    def read(self):

        return self.adc.read()

    def value(self):
    
        raw_value = self.read()
        return float(self.max_value - self.min_value) * raw_value / 2048
        
WiFiManager Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Manages Wi-Fi connectivity for the device. It has the following methods:

1. Method **__init__**: initializes a new instance.

2. Method **connect_wifi**: activates the Wi-Fi interface, connects to the specified network, and waits until the connection is established.

3. Method **disconnect_wifi**: disconnects from Wi-Fi network; deactivates the Wi-Fi interface if active and checks if the device is not connected to any Wi-Fi network.

Usage: *wifi_manager = WiFiManager(ssid, password)*

.. code:: python

    import network
    from time import sleep

    class WiFiManager:
    def __init__(self, ssid="rrrr", password="12345678"):
        self.ssid = ssid
        self.password = password
        self.wifi = network.WLAN(network.STA_IF)
        
    def connect_wifi(self):

        from time import sleep_ms

        if not self.wifi.isconnected():
            # Activate the Wi-Fi interface
            self.wifi.active(True)

            # Connect to the specified Wi-Fi network
            self.wifi.connect(self.ssid, self.password)

            # Wait until the connection is established
            print(f"Connecting to {self.ssid}", end="")
            while not self.wifi.isconnected():
                print(".", end="")
                sleep(1)

            print(" Done")
        else:
            print("Already connected")


    def disconnect_wifi(self):

        # Check if the Wi-Fi interface is active
        if self.wifi.active():
            # Deactivate the Wi-Fi interface
           self.wifi.active(False)

        # Check if the device is not connected to any Wi-Fi network
        if not self.wifi.isconnected():
            print("Disconnected")

BME280 Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Represents the BME280 sensor, providing methods for reading temperature, humidity, and pressure. It is specific to the BME280 sensor and you can find it `here. <https://github.com/rzvn01/de2_project/blob/main/utilities/bme280.py/>`_ 

Usage: *bme = BME280()*

OLED Display Class (SH1106)
~~~~~~~~~~~~~~~~~~~~~~~~~
Manages the OLED display and is specific to it. You can find it `here. <https://github.com/rzvn01/de2_project/blob/main/utilities/lcd_oled.py/>`_ 

Usage: *oled = SH1106_I2C(width, height, i2c, addr, rotate)*

I2cLcd Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Implements a HD44780 character LCD connected via PCF8574 on I2C. You can find it `here. <https://github.com/rzvn01/de2_project/blob/main/utilities/i2c_lcd.py/>`_ 

LcdApi Class
~~~~~~~~~~~~~~~~~~~~~~~~~
Implements the API for talking with HD44780 compatible character LCDs. You can find it `here. <https://github.com/rzvn01/de2_project/blob/main/utilities/lcd_api.py/>`_ 