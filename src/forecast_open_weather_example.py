from machine import ADC, Pin, I2C, deepsleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from ldr import LDR
from water_sensor import WaterSensor
import bme280
import urequests
import json
import network

class WeatherDisplay:
    def __init__(self):
        self.LDR_PIN = 15
        self.WATER_SENSOR_PIN = 36
        self.ssid = "raszvan"
        self.password = "12345678"
        self.api_key = "ce0138a17e760fac657ac45c93b0fa9b"
        self.lat = "41.9661"
        self.lon = "12.66"
        self.exclude = "current,minutely,hourly,alerts"
        self.units = "metric"

        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
        self.i2c_addr = 0x27
        self.lcd = I2cLcd(self.i2c, self.i2c_addr, num_lines=2, num_columns=16)

        self.bme = bme280.BME280(i2c=self.i2c, addr=0x76)
        self.ldr_adc = ADC(Pin(self.LDR_PIN))
        self.water_sensor = WaterSensor(self.WATER_SENSOR_PIN)
        self.ldr = LDR(self.LDR_PIN)

        self.wifi = network.WLAN(network.STA_IF)

    def connect_wifi(self):
        """
        Connect to Wi-Fi network.

        Activates the Wi-Fi interface, connects to the specified network,
        and waits until the connection is established.

        :return: None
        """
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
                sleep_ms(100)

            print(" Done")
        else:
            print("Already connected")


    def disconnect_wifi():
        """
        Disconnect from Wi-Fi network.

        Deactivates the Wi-Fi interface if active and checks if
        the device is not connected to any Wi-Fi network.

        :return: None
        """
        # Check if the Wi-Fi interface is active
        if self.wifi.active():
            # Deactivate the Wi-Fi interface
           self.wifi.active(False)

        # Check if the device is not connected to any Wi-Fi network
        if not self.wifi.isconnected():
            print("Disconnected")

    def read_sensors(self):
        moisture = self.water_sensor.value()
        #light_intensity = self.ldr.value()
        light_intensity=100
        temp = self.bme.temperature
        hum = self.bme.humidity
        pres = self.bme.pressure
        return moisture, light_intensity, temp, hum, pres

    def display_sensor_values(self, moisture, light_intensity, temp, hum, pres):
        self.lcd.clear()
        self.lcd.double_print("Moisture", "{:.1f}%".format(moisture), "Light", "{:.1f}%".format(light_intensity))
        self.lcd.double_print("Temp", temp, "Humidity", hum)
        self.lcd.single_print("Pressure", pres)

    def fetch_weather_data(self):
        url_call = "https://api.openweathermap.org/data/2.5/onecall?lat=" + self.lat + \
                   "&lon=" + self.lon + \
                   "&exclude=" + self.exclude + \
                   "&units=" + self.units + \
                   "&appid=" + self.api_key

        w = urequests.get(url_call)
        forecast = json.loads(w.content)
        w.close()
        return forecast

    def display_weather(self):
        self.connect_wifi()  # Connect to WiFi

        forecast = self.fetch_weather_data()

        moisture, light_intensity, temp, hum, pres = self.read_sensors()
        self.display_sensor_values(moisture, light_intensity, temp, hum, pres)

        sleep(5)  # Delay for 5 seconds

        self.lcd.clear()

        temp_min = str(forecast["daily"][0]["temp"]["min"])
        temp_max = str(forecast["daily"][0]["temp"]["max"])
        rain_qty = str(forecast["daily"][0]["rain"])
        weather_main = forecast["daily"][0]["weather"][0]["main"]
        weather_descr = forecast["daily"][0]["weather"][0]["description"]

        self.lcd.text("Today's Weather", 2, 1, self.lcd.black)
        self.lcd.pbm_draw(0, 15, weather_main + '.pbm')
        self.lcd.text("TM:" + temp_max + "C", 65, 15, self.lcd.black)
        self.lcd.text("Tm:" + temp_min + "C", 65, 25, self.lcd.black)
        self.lcd.text("Rn:" + rain_qty, 65, 35, self.lcd.black)
        self.lcd.text(weather_descr, 0, 78, self.lcd.black)

        sleep(10)  # Delay for 10 seconds

        self.lcd.hline(0, 90, 125, self.lcd.black)
        self.lcd.text(self.upd_time(), 0, 92, self.lcd.black)
        self.lcd.hline(0, 101, 125, self.lcd.black)

        start_line = 105

        for day in range(0, 6):
            d = day + 1
            temp_min = int(forecast["daily"][d]["temp"]["min"])
            temp_max = int(forecast["daily"][d]["temp"]["max"])
            if "rain" in forecast["daily"][d]:
                rain_qty = int(forecast["daily"][d]["rain"])
            else:
                rain_qty = 0
            weather_main = forecast["daily"][d]["weather"][0]["main"]
            weather_descr = forecast["daily"][d]["weather"][0]["description"]
            line = start_line + 2 * day * 11
            self.lcd.text("+" + str(d) + " day> " + weather_main, 0, line, self.lcd.black)
            self.lcd.text("T:{}/{}".format(temp_max, temp_min), 4, line + 10, self.lcd.black)
            self.lcd.text("r:{:02d}".format(rain_qty), 90, line + 10, self.lcd.black)

        sleep(10)  # Delay for 10 seconds

        self.lcd.text("by peppe8o.com", 0, 242, self.lcd.black)
        self.lcd.display(self.lcd.buffer)

        self.lcd.sleep()
        sleep(10)

        sleep_minutes = 15
        sleep_time = sleep_minutes * 60 * 1000
        deepsleep(sleep_time)

    def upd_time(self):
        url_call = "http://worldtimeapi.org/api/timezone/Europe/Rome"
        clock = urequests.get(url_call)
        clock_string = json.loads(clock.content)
        datetime_str = clock_string["datetime"]

        month = datetime_str[5:7]
        day = datetime_str[8:10]
        hour = datetime_str[11:13]
        minute = datetime_str[14:16]

        return "Upd." + day + "/" + month + " " + hour + ":" + minute


# Usage
weather_display = WeatherDisplay()
weather_display.connect_wifi()
moisture, light_intensity, temp, hum, pres = weather_display.read_sensors()
weather_display.display_sensor_values(moisture, light_intensity, temp, hum, pres)
print(weather_display.upd_time())