# RoboticsMidterm

There are three main The code for this project is running simultaneously on the Pico, the computer, and OpenCV.
1. Computer:

The following libraries are used in the Pico code:
- joystickButtons.py - This library sets up the i2c joystick and returns the name of the button that was clicked. Dpending on which button is clicked, the weather of one of four locations is found using an open weather API and posted to the Adafruit dashboard.
- leds.py - This libary is used to light up the physical display's LEDs indicating the temperature. It sets up the LED pins and includes two functions: one that turns off all the LEDs and another that turns individual LEDs on depending on the temperature
