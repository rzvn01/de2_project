from machine import ADC, Pin
import time


class WaterSensor:

    def __init__(self, pin, min_value=0, max_value=100):
        """
        Initializes a new instance.
        :parameter pin A pin that's connected to an water sensor.
        """

        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')

        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))

        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)

        self.min_value = min_value
        self.max_value = max_value

    def read(self):
        """
        Read a raw value from the WATER SENSOR.
        """
        return self.adc.read()

    def value(self):
        """
        Read a value from the sensorin the specified range.
        :return: A string representing the value in the format "xx.x%".
        """
        raw_value = self.read()
        return float(self.max_value - self.min_value) * raw_value / 2048
        
