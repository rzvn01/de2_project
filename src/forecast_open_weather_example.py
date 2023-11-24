from machine import ADC, Pin, I2C, deepsleep,lightsleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from ldr import LDR
from water_sensor import WaterSensor
from wifi_manager import WiFiManager
from lcd_oled import SH1106_I2C
from machine import soft_reset
import bme280
import urequests
import json
import network
from display_manager import DisplayManager


class WeatherDisplay:
    def __init__(self,wifiManager,displayManager):

        self.LDR_PIN = 15
        self.WATER_SENSOR_PIN = 36
        self.api_key = "ce0138a17e760fac657ac45c93b0fa9b"
        self.city = "BRNO,cz"  # todo further implementation geolocation api
        self.exclude="current,minutely,hourly,alerts"
        self.units = "metric"
        
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
        self.bme = bme280.BME280(i2c=self.i2c, addr=0x76)
        self.water_sensor = WaterSensor(self.WATER_SENSOR_PIN)
        self.ldr = LDR(self.LDR_PIN)

        self.wifiManager = wifiManager
        self.displayManager= displayManager
        
    def read_sensors(self):
        """
        Reads data from various sensors, including a soil moisture sensor, a light sensor, and a BME sensor (temperature, humidity, and pressure).

        This method collects data from different environmental sensors integrated into the system. It reads the moisture level from a soil moisture sensor,
        a simulated light intensity value (to be replaced with an actual light sensor reading in the future), and temperature, humidity, and pressure from a BME sensor.

        Returns:
            tuple: A tuple containing sensor readings in the following order - soil moisture level, light intensity, temperature, humidity, and pressure.
        """
        moisture = self.water_sensor.value()
        # light_intensity = self.ldr.value()  # TODO: Uncomment and replace with actual light sensor reading
        light_intensity = 100  # Placeholder value for light intensity
        temp = self.bme.temperature
        hum = self.bme.humidity
        pres = self.bme.pressure

        return moisture, light_intensity, temp, hum, pres

    def display_sensor_values(self, moisture, light_intensity, temp, hum, pres):

        self.displayManager.lcd.clear()
        self.displayManager.double_print("Moisture", "{:.1f}%".format(moisture), "Light", "{:.1f}%".format(light_intensity))
        self.displayManager.double_print("Temp", temp, "Humidity", hum)
        self.displayManager.single_print("Pressure", pres)

    def fetch_weather_data(self):

        self.wifiManager.connect_wifi()
        
        url_call = (
            "https://api.openweathermap.org/data/2.5/forecast?"
            f"q={self.city}&exclude={self.exclude}&units={self.units}&appid={self.api_key}"
        )
        
        print(url_call)  # Print the API request URL for debugging purposes
        w = urequests.get(url_call)
        weather_data = json.loads(w.content)
        w.close()
        self.wifiManager.disconnect_wifi()

        return weather_data

    def display_weather(self):
                 
        forecast = self.fetch_weather_data()
        
        print(forecast.keys())
        for day_data in forecast['list']:
            # Extract the hour from the dt_txt field
            hour = int(day_data['dt_txt'].split(' ')[1].split(':')[0])

            # Check if the hour is 12 (noon)
            if hour == 0 or hour==12:
                temp = int(day_data['main']['temp'])

                if 'rain' in day_data :
                    rain_qty = day_data['rain']
                else:
                    rain_qty = 0

                weather_main = day_data['weather'][0]['main']
                weather_descr = day_data['weather'][0]['description']
                self.displayManager.lcd.clear()
                self.displayManager.lcd.move_to(0,0)
                self.displayManager.lcd.print(day_data['dt_txt'])
                self.displayManager.lcd.move_to(0,1)
                self.displayManager.lcd.print("Weather: "+weather_main)
                
                self.displayManager.oled.fill(0)
                self.displayManager.oled_print("Temperature:"+str(temp)+" C",0,0)
                print("Temperature: {}°C".format(temp))
                print("Rain: {} mm ".format(rain_qty))
                print("-" * 20)
                sleep(2)

        # Add sleep if needed
        sleep(1)

        moisture, light_intensity, temp, hum, pres = self.read_sensors()
        self.display_sensor_values(moisture, light_intensity, temp, hum, pres)

        self.displayManager.lcd.clear()



    def upd_time(self):
        """
        Fetches the current date and time from the World Time API for the Europe/Rome timezone and formats it into a human-readable string.

        This method sends a request to the World Time API, extracts the relevant information, and returns a formatted string representing the
         last update time. The returned string includes the day and month of the update, as well as the hour and minute in 24-hour format.

        Returns:
            str: A formatted string indicating the last update time in the "Upd. DD/MM HH:mm" format.
        """
        url_call = "http://worldtimeapi.org/api/timezone/Europe/Rome"
        clock = urequests.get(url_call)
        clock_string = json.loads(clock.content)
        datetime_str = clock_string["datetime"]

        month = datetime_str[5:7]
        day = datetime_str[8:10]
        hour = datetime_str[11:13]
        minute = datetime_str[14:16]

        return "Upd." + day + "/" + month + " " + hour + ":" + minute
    
    

if __name__ == "__main__":
    wifiManager = WiFiManager(ssid="rrrr", password="12345678")
    displayManager = DisplayManager()
    weather_display = WeatherDisplay(wifiManager,displayManager)

    while True: 
            weather_display.display_weather()
            print("Going to sleep")
            sleep(90)
            #lightsleep(10*60*100)