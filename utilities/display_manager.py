from machine import Pin, I2C
from i2c_lcd import I2cLcd
from oled_display import SH1106_I2C


class DisplayManager():
    
    def __init__(self):
        
        """
        Initializes the DisplayManager object, configuring OLED and LCD displays using I2C communication.
        """
               
        self.WIDTH = 128  # OLED display width
        self.HEIGHT = 64  # OLED display height

        # Init I2C using pins GP22 & GP21 (default I2C0 pins)
        self.i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
        
        #self.oled = SH1106_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C, rotate=180)

        self.i2c_addr = 0x27
        self.lcd = I2cLcd(self.i2c, self.i2c_addr, num_lines=2, num_columns=16)
     
        self.lcd.display_on()
        
    def double_print(self, first_sensor, first_value, second_sensor,second_value):
        
        """
        Displays two sensor readings on the LCD display with a backlight, each on a separate line.

        Parameters:
        - first_sensor (str): Name of the first sensor.
        - first_value (str): Value of the first sensor.
        - second_sensor (str): Name of the second sensor.
        - second_value (str): Value of the second sensor.
        """
        
        self.lcd.clear()
        self.lcd.move_to(0,0)
        self.lcd.print(first_sensor)

        self.lcd.move_to(8,0)
        self.lcd.print(":")
        
        if first_value[1]=='.':
            self.lcd.move_to(11,0)
        else:
            self.lcd.move_to(10,0)        
        self.lcd.print(first_value)
       
        self.lcd.move_to(0,1)
        self.lcd.print(second_sensor)
        
        self.lcd.move_to(8,1)
        self.lcd.print(":")

        if second_value[1]=='.':
            self.lcd.move_to(11,1)
        else:
            self.lcd.move_to(10,1)        
            self.lcd.print(second_value)
            
        time.sleep(1)
    
        
        
    def single_print(self,first_sensor, first_value):
        
        """
        Displays a single sensor reading on the LCD display with a backlight.

        Parameters:
        - first_sensor (str): Name of the sensor.
        - first_value (str): Value of the sensor.
        """
        
        self.lcd.clear()
        self.lcd.move_to(0,0)
        self.lcd.print(first_sensor)
        
        self.lcd.move_to(8,0)
        self.lcd.print(":")
        
        self.lcd.move_to(7,1)        
        self.lcd.print(first_value)
       
        time.sleep(1)
        
        

        