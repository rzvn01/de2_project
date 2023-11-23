from machine import ADC, Pin, I2C, deepsleep,lightsleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
from ldr import LDR
from water_sensor import WaterSensor
import bme280
import urequests
import json
import network


class WiFiManager:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
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
                sleep(1)

            print(" Done")
        else:
            print("Already connected")


    def disconnect_wifi(self):
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

   
class WeatherDisplay:
    def __init__(self,wifi_manager):
        """
        Initializes the Weather Station object with default and configurable parameters.

        This method sets up the Weather Station object with various configuration parameters, including PIN assignments for sensors, Wi-Fi credentials, OpenWeatherMap API key, city for weather data, and units for temperature measurement. It also initializes the I2C interface for the LCD, BME280 sensor for temperature, humidity, and pressure, and ADC (Analog-to-Digital Converter) for light intensity readings. The method creates instances of the WaterSensor and LDR classes for soil moisture and light intensity sensing, respectively.

        Attributes:
            LDR_PIN (int): The GPIO pin for the LDR (Light Dependent Resistor) sensor.
            WATER_SENSOR_PIN (int): The GPIO pin for the soil moisture sensor.
            ssid (str): The Wi-Fi SSID for network connection.
            password (str): The Wi-Fi password for network connection.
            api_key (str): The API key for accessing the OpenWeatherMap API.
            city (str): The default city for weather data (BRNO, Czech Republic in this case).
            exclude (str): Parameter for excluding specific weather data from the OpenWeatherMap API response.
            units (str): The unit system for temperature measurement (metric in this case).
            i2c (I2C): The I2C interface for communication with devices like the LCD.
            i2c_addr (int): The I2C address of the LCD.
            lcd (I2cLcd): An instance of the I2cLcd class for interfacing with the LCD.
            bme (BME280): An instance of the BME280 class for temperature, humidity, and pressure sensing.
            ldr_adc (ADC): An instance of the Analog-to-Digital Converter for reading light intensity values.
            water_sensor (WaterSensor): An instance of the WaterSensor class for soil moisture sensing.
            ldr (LDR): An instance of the LDR class for light intensity sensing.
            wifi (network.WLAN): An instance of the WLAN class for Wi-Fi connectivity.
        """
        self.LDR_PIN = 15
        self.WATER_SENSOR_PIN = 36
        self.api_key = "ce0138a17e760fac657ac45c93b0fa9b"
        self.city = "BRNO,cz"  # todo further implementation geolocation api
        self.exclude = ""
        self.units = "metric"

        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
        self.i2c_addr = 0x27
        self.lcd = I2cLcd(self.i2c, self.i2c_addr, num_lines=2, num_columns=16)

        self.bme = bme280.BME280(i2c=self.i2c, addr=0x76)
        self.ldr_adc = ADC(Pin(self.LDR_PIN))
        self.water_sensor = WaterSensor(self.WATER_SENSOR_PIN)
        self.ldr = LDR(self.LDR_PIN)

        self.wifi_manager = wifi_manager



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
        """
        Displays sensor readings on a connected LCD screen in a formatted layout.

        This method takes sensor readings as input and presents them on a connected LCD screen. The displayed information includes soil moisture level, light intensity, temperature, humidity, and atmospheric pressure. The data is arranged in a clear and organized format to provide easy visibility and interpretation.

        Parameters:
            moisture (float): The soil moisture level, represented as a percentage.
            light_intensity (float): The intensity of light, represented as a percentage. Note: Placeholder value until an actual light sensor is implemented.
            temp (float): The temperature reading from the BME sensor.
            hum (float): The humidity reading from the BME sensor.
            pres (float): The atmospheric pressure reading from the BME sensor.
        """
        self.lcd.clear()
        self.lcd.double_print("Moisture", "{:.1f}%".format(moisture), "Light", "{:.1f}%".format(light_intensity))
        self.lcd.double_print("Temp", temp, "Humidity", hum)
        self.lcd.single_print("Pressure", pres)

    def fetch_weather_data(self):
        """
        Fetches current weather data from the OpenWeatherMap API based on specified parameters.

        This method constructs a URL for the OpenWeatherMap API using the provided city, exclusion list, units, and API key.
        It then makes a request to the API, retrieves the weather data in JSON format, and closes the connection.
        After fetching the data, the function disconnects from the Wi-Fi network.

        Returns:
            dict: A dictionary containing the current weather information, including temperature, humidity, wind speed, and more, as provided by the OpenWeatherMap API.
        """
        url_call = (
            "https://api.openweathermap.org/data/2.5/weather?"
            f"q={self.city}&exclude={self.exclude}&units={self.units}&appid={self.api_key}"
        )
        print(url_call)  # Print the API request URL for debugging purposes
        w = urequests.get(url_call)
        weather_data = json.loads(w.content)
        w.close()
        self.wifi_manager.disconnect_wifi()

        return weather_data

    def display_weather(self):
            
        """
        Displays current weather information on a connected LCD screen, including details such as temperature, humidity, wind speed, and more.

        This method fetches weather data from the OpenWeatherMap API using the `fetch_weather_data` function and extracts relevant information
        to display on a connected LCD screen. The displayed information includes the city name, current weather conditions, temperature range,
        and additional details like wind speed, humidity, and sunrise/sunset times. The function also integrates sensor readings for soil moisture,
        light intensity, temperature, humidity, and pressure.

        """
        self.wifi_manager.connect_wifi()
        weather_data = self.fetch_weather_data()

        # Extracting information from the weather_data JSON response
        coord = weather_data.get('coord', {})
        lon = coord.get('lon', '')
        lat = coord.get('lat', '')

        weather = weather_data.get('weather', [{}])[0]
        weather_id = weather.get('id', '')
        weather_main = weather.get('main', '')
        weather_description = weather.get('description', '')
        weather_icon = weather.get('icon', '')

        main_info = weather_data.get('main', {})
        temp = str(main_info.get('temp', ''))
        feels_like = str(main_info.get('feels_like', ''))
        temp_min = str(main_info.get('temp_min', ''))
        temp_max = str(main_info.get('temp_max', ''))
        pressure = str(main_info.get('pressure', ''))
        humidity = str(main_info.get('humidity', ''))

        wind_info = weather_data.get('wind', {})
        wind_speed = str(wind_info.get('speed', ''))
        wind_deg = str(wind_info.get('deg', ''))

        clouds_info = weather_data.get('clouds', {})
        cloudiness = str(clouds_info.get('all', ''))

        sys_info = weather_data.get('sys', {})
        sys_type = str(sys_info.get('type', ''))
        sys_id = str(sys_info.get('id', ''))
        sys_country = sys_info.get('country', '')
        sys_sunrise = str(sys_info.get('sunrise', ''))
        sys_sunset = str(sys_info.get('sunset', ''))

        visibility = str(weather_data.get('visibility', ''))
        dt = str(weather_data.get('dt', ''))
        timezone = str(weather_data.get('timezone', ''))
        city_id = str(weather_data.get('id', ''))
        city_name = weather_data.get('name', '')
        cod = str(weather_data.get('cod', ''))

        self.lcd.single_print("City", city_name)

        # Additional prints can be added here for more detailed weather information
        # print(weather_main)
        # print(temp_min, temp_max)
        # print(temp)

        moisture, light_intensity, temp, hum, pres = self.read_sensors()
        self.display_sensor_values(moisture, light_intensity, temp, hum, pres)

        self.lcd.clear()



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
    wifi_manager = WiFiManager(ssid="rrrr", password="12345678")
    weather_display = WeatherDisplay(wifi_manager)

    while True: 
            weather_display.display_weather()
            lightsleep(10*60*1000)