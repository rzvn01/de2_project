from machine import ADC, Pin,I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import *
from ldr import LDR
from water_sensor import WaterSensor
import bme280



def read_sensors():
    
    moisture = water_sensor.value()
    light_intensity=ldr.value()
    temp = bme.temperature  # Return temp in degrees
    hum = bme.humidity
    pres = bme.pressure
    
    return moisture,light_intensity,temp,hum,pres

def display_sensor_values(moisture,light_intensity,temp,hum,pres):
    
    lcd.double_print("Moisture","{:.1f}%".format(moisture),"Light","{:.1f}%".format(light_intensity))
    lcd.double_print("Temp",temp,"Humidity",hum)
    lcd.single_print("Pressure",pres)
    
LDR_PIN = 15
LED_PIN = 2  
WATER_SENSOR_PIN= 36


i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
i2c_addr = 0x27  # Replace with the correct I2C address for your LCD

# Create an instance of I2cLcd
lcd = I2cLcd(i2c, i2c_addr, num_lines=2, num_columns=16)

bme = bme280.BME280(i2c=i2c, addr=0x76)

# Create ADC object
ldr_adc = ADC(Pin(LDR_PIN))

# Set LED pin as output
led = Pin(LED_PIN, Pin.OUT)
water_sensor = WaterSensor(WATER_SENSOR_PIN)
# ldr object
ldr= LDR(LDR_PIN)

moisture,light_intensity,temp,hum,pres = read_sensors()
display_sensor_values(moisture,light_intensity,temp,hum,pres)

lcd.display_off()
    

