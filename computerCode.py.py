# Computer code

import requests, time
from Adafruit_IO import MQTTClient

COLOR_FEED_ID = "Color"
TEMP_UNITS_FEED_ID = "temp-units"
lastUnits = ""
startTime = time.time()

# ---------------- Airtable Setup ---------------- #
headers = {
    'Authorization': 'Bearer [API KEY]', # add key!
}

# ---------------- Adafruit Setup ---------------- #
ADAFRUIT_IO_KEY = '' # add IO key
ADAFRUIT_IO_USERNAME = 'lkresin'
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.connect()

# ---------------- Get from Airtable and Post to Adafruit ---------------- #

# Function that gets the temperature units from Airtable 
def getTempUnits():
    reply = requests.get('https://api.airtable.com/v0/[baseID]/Table%201/recuPP1WjXBXAuIpB', headers=headers)
    currentUnits = reply.json()['fields']['Units']
    return currentUnits

# Function that posts the temperature units from Airtable to the Adafruit dashboard
def AdafruitPublish(lastUnits, currentUnits):
    #print("last units: ", lastUnits)
    #print("current units: ", currentUnits)
    if lastUnits != currentUnits:
        #print(currentUnits)
        client.publish(TEMP_UNITS_FEED_ID, currentUnits) # publishing units to Adafruit dashboard
        lastUnits = currentUnits        

# Runs above two functions for 10 minutes
while True:
#    currentTime = time.time()
#    if currentTime - startTime > 600: # times out after 10 minutes
#        print("Timeout reached, exiting program")
#        break
    currentUnits = getTempUnits()
    print("Current units are: ", currentUnits)
    AdafruitPublish(lastUnits, currentUnits)
    time.sleep(2)