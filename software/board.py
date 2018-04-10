import machine

class led:
    red = machine.Pin(12, machine.Pin.OUT)
    green = machine.Pin(15, machine.Pin.OUT)
    blue = machine.Pin(13, machine.Pin.OUT)

led.red.off()
led.green.off()
led.blue.off()

i2c = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(2))
i2c_devices = i2c.scan()

import bme280 as _bme280
if _bme280.BME280_I2CADDR in i2c_devices:
    bme280 = _bme280.BME280(i2c=i2c)

import network
wlan = network.WLAN(network.STA_IF)