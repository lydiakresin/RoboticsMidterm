import urequests as requests
import time, machine, mqtt, math
import network, ubinascii
from leds import LEDs # my library for controlling thermometer LEDs
import joystickButtons # my library for the joystick
import uasyncio as asyncio
from servo import Servo

TIME_UNIT = .1
LEDs.LEDreset()
# ------------------- CONNECTING TO WIFI --------------------#
ssid = "" # Add wifi username and password!
password = ""

def connect_wifi():
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)
    
    station.connect(ssid,password)
    while not station.isconnected():
        print("not connected")
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())

connect_wifi()


# ---------------- Thermistor setup ---------------- #
adcpin = 26
thermistor = machine.ADC(adcpin)
oldThermistorReading = 0 # setting up thermistor reading for callback
lastUnits = ""

# ---------------- Servo and LED setup ---------------- #
s1 = Servo(14) # Servo is connected to GP14
ChchLED = machine.Pin(5, machine.Pin.OUT)
TallinnLED = machine.Pin(2, machine.Pin.OUT)
SantiagoLED = machine.Pin(4, machine.Pin.OUT)
FairbanksLED = machine.Pin(9, machine.Pin.OUT)

# ---------------- Adafruit MQTT setup ---------------- #
ADAFRUIT_IO_KEY = '' # add!
ADAFRUIT_IO_USERNAME = '' # add!

# Create an MQTT client instance.
client = mqtt.MQTTClient('Lydia', 'io.adafruit.com', user = ADAFRUIT_IO_USERNAME, password = ADAFRUIT_IO_KEY, keepalive=1000)
client.connect()
thermistor_feed = ADAFRUIT_IO_USERNAME + "/feeds/thermistor"
apitemp_feed = ADAFRUIT_IO_USERNAME + "/feeds/api-temperature"

# ---------------- Airtable Setup ---------------- #
headers = {
    'Authorization': 'Bearer [API KEY]', # Add API key
}

#read = False

# ---------------- FUNCTION DEFINITIONS ---------------- #

# Function that reads temperature units from Airtable and returns the current units and if
# the units have changed from the last time they were checked.
# Returns the units listed in Airtable and whether the temperature needs to be re-measured
def checkAirtable():
    global lastUnits
    #print("checking airtable")
    reply = requests.get('https://api.airtable.com/v0/[baseID]/Table%201/recuPP1WjXBXAuIpB', headers=headers) # add base ID
    currentUnits = reply.json()['fields']['Units']
    #print("Last units: ", lastUnits, " Current units: ", currentUnits)
    if currentUnits != lastUnits: #if units on Airtable have changed, read the temperature
        print("Different units in Airtable")
        read = True
        #print("read in check! ", read)
    else: # units on Airtable haven't changed, so no need to update
        #print("same units")
        read = False
    lastUnits = currentUnits
    print("read in check: ", read)
    return currentUnits, read

# Function that reads resistance value from thermistor and turns into temperature
# Returns the temperature in the inputted units (C or F)
def getTemp(units): # returns temperature from thermistor
    # Voltage Divider
    Vin = 3.3
    Ro = 10000  # 10k Resistor

    # Steinhart Constants
    A = 0.001129148
    B = 0.000234125
    C = 0.0000000876741
    # Get Voltage value from ADC   
    adc = thermistor.read_u16()
    Vout = (3.3/65535)*adc
    
    # Calculate Resistance
    Rt = (Vout * Ro) / (Vin - Vout)
    
    # Steinhart - Hart Equation
    TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))

    if units == "C": #returns temperature in Celcius
        TempC = TempK - 273.15
        return round(TempC, 1)
    elif units == "F": #returns temperature in Fahrenheit
        TempF = (TempK - 273.15) * 9/5 + 32
        return(round(TempF, 1))
    else:
        return(-1)
    # Convert from Kelvin to Celsius
    
# Servo functions: depending on input units are C or F, make servo rotate to one or the other side
def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle, 0, 180, 0, 1024))) # Convert range value to angle value

def control_servo(tempUnits):
    if tempUnits == 'C':
        servo_Angle(0)  # Move to one side
    elif tempUnits == 'F':
        servo_Angle(180)  # Move to the other side
    else:
        print("Invalid units")
    
# Function turns off all LEDs relating to temperature location from gamepad
def locationLEDreset():
    FairbanksLED.low()
    TallinnLED.low()
    SantiagoLED.low()
    ChchLED.low()
# ------- Setting up callback to check temp every 5 mins --------- # WHERE TO PUT?


# Function that runs all temperature-related tasks on Pico
# Checks to see if Airtable units have updated, and if so, finds the updated temperature,
#     updates the physical display, and publishes the temperature to the Adafruit dashboard
async def picoTemp():
    while True:
        units, read = checkAirtable()
        print("units and read: ", units, read)
        if read:
            print("Getting new temp")
            temp = getTemp(units)
            tempStr = str(temp) # reads temperature from thermistor
            tempandUnits = str(temp) + " " + units
            print("The temperature is: " + tempandUnits)
            control_servo(units) # make servo move to corresponding temperature
            LEDs.LEDreset() # turning off all LEDs
            time.sleep(.005)
            LEDs.tempLedControl(temp) # turning on the thermometer LEDs
            try:
                client.publish(thermistor_feed, tempStr)
                print("published!")
            except:
                print("Didn't successfully publish")
        else:
            print("not read")
        await asyncio.sleep(TIME_UNIT)
  
# Function that controls joystick (I2C component)
# Depending on which button on joystick is clicked, posts the temperature of one
#      of 4 places on the Adafruit dashboard
async def joystickControl():
    while True:
        units, read = checkAirtable()
        #try:
        buttonClicked = joystickButtons.buttonName()
        #except:
        #    continue
        if buttonClicked is not None:
            locationLEDreset()
            print("Button is clicked, getting temp of corresponding location")
            if buttonClicked == "A": # # Tallinn coordinates: 59.4370, 24.7536
                reply = requests.get("https://api.weatherbit.io/v2.0/current?lat=59.4370&lon=24.7536&key=2264ae3973bf4063b69f92b0e00af077&")
                location = "Tallinn"
                TallinnLED.high()
                #print("Weather in Tallinn")
            elif buttonClicked == "B": # Fairbanks coordinates: 64.8401, 147.7200
                reply = requests.get("https://api.weatherbit.io/v2.0/current?lat=64.8401&lon=-147.7200&key=2264ae3973bf4063b69f92b0e00af077&")
                location = "Fairbanks"
                FairbanksLED.high()
                #print("Weather in Fairbanks")
            elif buttonClicked == "x": # Chch coordinates: 43.5320, 172.6306
                 reply = requests.get("https://api.weatherbit.io/v2.0/current?lat=43.5320&lon=172.6306&key=2264ae3973bf4063b69f92b0e00af077&")
                 location = "Christchurch"
                 ChchLED.high()
                #print("Weather in Christchurch")
            elif buttonClicked == "y": # Santiago coordinates: 33.4489, 70.6693 
                reply = requests.get("https://api.weatherbit.io/v2.0/current?lat=33.4489&lon=70.6693&key=2264ae3973bf4063b69f92b0e00af077&")
                location = "Santiago"
                SantiagoLED.high()
                #print("Weather in Santiago")
            data=reply.json()['data'] # temp is default Celcius, data is a dictionary
            temperature = data[0]['temp']
            if units == "F":
                temperature = (temperature * 9/5) + 30
            tempAndLocation = "The temperature in " + location + " is " + str(temperature) + " degrees " + units
            print(tempAndLocation)
            client.publish(apitemp_feed, tempAndLocation)
        await asyncio.sleep(TIME_UNIT)


async def async_main():
    print("in async main")
    res = await asyncio.gather(picoTemp(), joystickControl())
    return res
    
while True:
    asyncio.run(async_main())