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
    def __init__(self,displayManager):

        self.LDR_PIN = 39
        self.WATER_SENSOR_PIN = 36
        self.api_key = "ce0138a17e760fac657ac45c93b0fa9b"
        self.city = "BRNO,cz"  # todo further implementation geolocation api
        self.exclude="current,minutely,hourly,alerts"
        self.units = "metric"
        
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
        self.bme = bme280.BME280(i2c=self.i2c, addr=0x76)
        self.water_sensor = WaterSensor(self.WATER_SENSOR_PIN)
        self.ldr = LDR(self.LDR_PIN)

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
        light_intensity = self.ldr.value()  # TODO: Uncomment and replace with actual light sensor reading
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
        
        url_call = (
            "https://api.openweathermap.org/data/2.5/forecast?"
            f"q={self.city}&exclude={self.exclude}&units={self.units}&appid={self.api_key}"
        )
        
        w = urequests.get(url_call)
        weather_data = json.loads(w.content)
        w.close()

        return weather_data

    def display_weather(self):
                 
        forecast = self.fetch_weather_data()
        
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
                    
                humidity= day_data['main']['humidity']  
                pressure= day_data['main']['pressure']
                wind= day_data['wind']['speed']
                weather_type = day_data['weather'][0]['main']
                
                self.displayManager.lcd.clear()
                self.displayManager.lcd.move_to(0,0)
                self.displayManager.lcd.print(day_data['dt_txt'])
                self.displayManager.lcd.move_to(0,1)
                self.displayManager.lcd.print("Weather: "+weather_type)
                
                self.displayManager.oled.fill(0)
                self.displayManager.oled_print("FORECAST FEATURE",0,0)
                self.displayManager.oled_print("Temperature:"+str(temp)+"C",0,10)
                self.displayManager.oled_print("Wind:"+str(wind)+"km/h",0,20)
                self.displayManager.oled_print("Rain:" +str(rain_qty)+"%",0,30)
                self.displayManager.oled_print("Pressure:" +str(pressure)+"hPa",0,40)
                self.displayManager.oled_print("Humidity:" +str(humidity)+"%",0,50)
                sleep(2)
        
        self.displayManager.oled.fill(0)
        self.displayManager.oled_print("READING DATA  ",15,20)
        self.displayManager.oled_print("FROM OUR SENSORS",0,40)
        
        
        moisture, light_intensity, temp, hum, pres = self.read_sensors()
        self.display_sensor_values(moisture, light_intensity, temp, hum, pres)
        self.displayManager.lcd.clear()
        
        self.displayManager.oled.fill(0)
        self.displayManager.oled_print("UPLOADING DATA",0,20)
        self.displayManager.oled_print("TO THINGSPEAK",0,40)
        
        self.send_to_thingspeak(moisture, temp, hum, pres,light_intensity)
        
        
    def send_to_thingspeak(self, moisture, temp, hum, pres,light_intensity):
        
        API_URL = "https://api.thingspeak.com/update"
        API_KEY="DO2L1H0RIXIHDZ3A"

        # POST request
        request_url = f"{API_URL}?api_key={API_KEY}"
        json = {"field1": temp, "field2": hum, "field3": pres, "field4": moisture, "field5": light_intensity}
        headers = {"Content-Type": "application/json"}
        response = urequests.post(request_url, json=json, headers=headers)

        print(f"Response from ThingSpeak: {response.text}")
        response.close()
 

if __name__ == "__main__":
    wifiManager = WiFiManager(ssid="rrrr", password="12345678")
    displayManager = DisplayManager()
    weather_display = WeatherDisplay(displayManager)

    while True:
            displayManager.oled.fill(0)
            displayManager.oled_print("Connecting to ",0,20)
            displayManager.oled_print("wifi...",0,40)
            wifiManager.connect_wifi()
            
            weather_display.display_weather()()
            
            displayManager.oled.fill(0)
            displayManager.oled_print("Disconnecting",0,20)
            displayManager.oled_print("from wifi...",0,40)
            wifiManager.disconnect_wifi()
            displayManager.oled.fill(0)
            
            deepsleep(90)
