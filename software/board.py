import machine

class led:
    red = machine.Pin(12, machine.Pin.OUT)
    green = machine.Pin(15, machine.Pin.OUT)
    blue = machine.Pin(13, machine.Pin.OUT)

led.red.off()
led.green.off()
led.blue.off()

import network
wlan = network.WLAN(network.STA_IF)


i2c = machine.I2C(scl=machine.Pin(14), sda=machine.Pin(2))

import bme280
bme = bme280.BME280(i2c=i2c)
