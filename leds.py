from machine import Pin, PWM
from utime import sleep  
            
# Pin setup
w1LED = Pin(16, Pin.OUT)
w2LED = Pin(17, Pin.OUT)
b1LED = Pin(18, Pin.OUT)
b2LED = Pin(19, Pin.OUT)
g1LED = Pin(20, Pin.OUT)
g2LED = Pin(21, Pin.OUT)
y1LED = Pin(22, Pin.OUT)
y2LED = Pin(26, Pin.OUT)
r1LED = Pin(27, Pin.OUT)
r2LED = Pin(28, Pin.OUT)

class LEDs:
    # This function turns off all LEDs
    def LEDreset():
        w1LED.low()
        w2LED.low()
        b1LED.low()
        b2LED.low()
        g1LED.low()
        g2LED.low()
        y1LED.low()
        y2LED.low()
        r1LED.low()
        r2LED.low()
    
    # This function takes in the temperature and turns on the LEDs of a thermometer correspondingly 
    def tempLedControl(temp)
        LEDreset() # turn off LEDS
        if temp <= 5:
            w1LED.on()
        elif temp > 5 and temp <= 15:
            w1LED.on()
            w2LED.on()
        elif temp > 15 and temp <= 25:
            w1LED.on()
            w2LED.on()
            b1LED.on()
        elif temp > 25 and temp <= 35:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
        elif temp > 35 and temp <= 45:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
        elif temp > 45 and temp <= 55:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
            g2LED.on()
        elif temp > 55 and temp <= 65:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
            g2LED.on()
            y1LED.on()
        elif temp > 65 and temp <= 75:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
            g2LED.on()
            y1LED.on()
            y2LED.on()
        elif temp > 75 and temp <= 85:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
            g2LED.on()
            y1LED.on()
            y2LED.on()
            r1LED.on()
        elif temp > 85:
            w1LED.on()
						w2LED.on()
            b1LED.on()
            b2LED.on()
            g1LED.on()
            g2LED.on()
            y1LED.on()
            y2LED.on()
            r1LED.on()
						r2LED.on()
        else:
            LEDreset()
