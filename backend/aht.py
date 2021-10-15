import time

import adafruit_tca9548a
import board
import adafruit_ahtx0

import threading




class Aht:
    def __init__(self):
        self.temperature = [-1] * 8
        self.humidity = [-1] * 8
        self.i2c = board.I2C()
        self.tca = adafruit_tca9548a.TCA9548A(self.i2c)
        self.daemon = threading.Thread(target=self.temp_humid_daemon)
        self.threading = True

    def temp_humid_daemon(self, daemon=True):
        while self.threading:
            temperature = []
            humidity = []
            for channel in range(8):
                addresses = []
                if self.tca[channel].try_lock():
                    addresses = self.tca[channel].scan()
                    self.tca[channel].unlock()
                if '0x38' in [hex(address) for address in addresses if address != 0x70]:
                    temperature.append(adafruit_ahtx0.AHTx0(self.tca[0]).temperature)
                    humidity.append(adafruit_ahtx0.AHTx0(self.tca[0]).relative_humidity)
                else:
                    temperature.append(-1)
                    humidity.append(-1)
            self.temperature = temperature
            self.humidity = humidity

    def getTemperature(self, number):
        return self.temperature[number]

    def getHumidity(self,number):
        return self.humidity[number]