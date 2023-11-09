# RoboticsMidterm

The main tasks of this program are outlined below: 
1. A **thermistor** is used to find the temperature of the surroundings
2. A **physical display** updates with temperature readings and the current units
3. **Color identification** in OpenCV determines the units that the temperature is displayed in (C or F). The units are sent to Airtable.
4. The Pico and computer read the units using **Airtable’s REST API**
5. The computer updates an **Adafruit dashboard** with the new units, and the Pico updates the dashboard with a new temperature reading in those units using **Adafruit’s MQTT broker**.
6. An **i2c device (a joystick)** is integrated into the program by triggering a reading from a weather API

The code for this project is running simultaneously on the **Pico**, the **computer**, and **OpenCV**.
1. *OpenCV:** The OpenCV code has two components: identifying the primary color of an image, and posting the units that correspond to that color to Airtable.
1. *Computer:** The computer uses Airtable's REST API to get the units posted there from OpenCV. It then publishes these units to the Adafruit dashboard using MQTT.

The following libraries are used in the Pico code:
- joystickButtons.py - This library sets up the i2c joystick and returns the name of the button that was clicked. Dpending on which button is clicked, the weather of one of four locations is found using an open weather API and posted to the Adafruit dashboard.
- leds.py - This libary is used to light up the physical display's LEDs indicating the temperature. It sets up the LED pins and includes two functions: one that turns off all the LEDs and another that turns individual LEDs on depending on the temperature
