from machine import ADC, Pin,I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import *
from ldr import LDR
from water_sensor import WaterSensor
import bme280




def read_ldr():
    ldr_val = ldr_adc.read()

    # Print LDR value to serial monitor
    print("LDR Output Value:", ldr_val)

    # Check light intensity and control LED
    if ldr_val > 2000:
        print("High intensity")
        led.off()  # LED remains OFF
    else:
        print("Low intensity")
        led.on()   # LED remains ON
        
    return 100*ldr_val/4095

def read_bme():
    temp = bme.temperature  # Return temp in degrees
    hum = bme.humidity
    pres = bme.pressure

    print(f'Temperature: {temp}')
    print(f'Humidity: {hum}')
    print(f'Pressure: {pres}')

    sleep(1)
    print("")
    
def lcd_double_print(first_sensor, first_value, second_sensor,second_value):
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.print(first_sensor)

    lcd.move_to(8,0)
    lcd.print(":")
    
    if first_value[1]=='.':
        lcd.move_to(11,0)
    else:
        lcd.move_to(10,0)        
    lcd.print(first_value)
   
    lcd.move_to(0,1)
    lcd.print(second_sensor)
    
    lcd.move_to(8,1)
    lcd.print(":")

    if second_value[1]=='.':
        lcd.move_to(11,1)
    else:
        lcd.move_to(10,1)        
        lcd.print(second_value)
        
    sleep(1)

def lcd_single_print(first_sensor, first_value):
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.print(first_sensor)
    
    lcd.move_to(8,0)
    lcd.print(":")
    
    lcd.move_to(7,1)        
    lcd.print(first_value)
   
    sleep(1)
        
    
    
LDR_PIN = 15
LED_PIN = 2  
WATER_SENSOR_PIN= 36

# I2C(id, scl, sda, freq)
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
i2c_addr = 0x27  # Replace with the correct I2C address for your LCD

# Create an instance of I2cLcd
lcd = I2cLcd(i2c, i2c_addr, num_lines=2, num_columns=16)

#Comentariu //todo
bme = bme280.BME280(i2c=i2c, addr=0x76)

# Create ADC object
ldr_adc = ADC(Pin(LDR_PIN))

# Set LED pin as output
led = Pin(LED_PIN, Pin.OUT)

water_sensor = WaterSensor(WATER_SENSOR_PIN)
# ldr object
ldr= LDR(LDR_PIN)

while True:
    moisture = water_sensor.value()
    light_intensity=ldr.value()
    temp = bme.temperature  # Return temp in degrees
    hum = bme.humidity
    pres = bme.pressure
    lcd_double_print("Moisture","{:.1f}%".format(moisture),"Light","{:.1f}%".format(light_intensity))
    lcd_double_print("Temp",temp,"Humidity",hum)
    lcd_single_print("Pressure",pres)
    
#     print("Water sensor :{:.1f}%".format(moisture))
# 
#     lcd.clear()
#     lcd.move_to(0,0)
#     lcd.print("Light: {:.1f}%".format(ldr.value()))
#     print("LDR :{:.1f}%".format(ldr.value()))
#     sleep(1)
#     
#     temp = bme.temperature  # Return temp in degrees
#     hum = bme.humidity
#     pres = bme.pressure
# 
#     print(f'Temperature: {temp}')
#     print(f'Humidity: {hum}')
#     print(f'Pressure: {pres}\n')


