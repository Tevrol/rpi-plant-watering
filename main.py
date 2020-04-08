# imports
from src.moisture import Moisture
from src.pump import Pump
from src.ipwsclient import IpwsClient
from src.waterlevel import WaterLevel
import time


print(
'''
  _____ _______          _______
 |_   _|  __ \\ \\        / / ____|
   | | | |__) \\ \\  /\\  / / (___
   | | |  ___/ \\ \\/  \\/ / \\___ \\
  _| |_| |      \\  /\\  /  ____) |
 |_____|_|       \\/  \\/  |_____/
  IoT  Plant    Watering  System
'''
)
# configure MQTT connection
print("Loading Config...")

# TODO - Create a JSON file for all the config & pin numbers
config = {}
config['host'] = "a3qo96kfy30a1-ats.iot.us-west-2.amazonaws.com"
config['port'] = "8883"
config['rootCAPath'] = "/home/pi/certs/root-CA.crt"
config['privateKeyPath'] = "/home/pi/certs/Waterer.private.key"
config['certificatePath'] = "/home/pi/certs/Waterer.cert.pem"
# init pin variables
pumpPin = 20
moisturePin = 21

# create objects
print("Creating Objects...")
moisture = Moisture(moisturePin)
pump = Pump(pumpPin)
ipwsClient = IpwsClient(config)
waterLevel = WaterLevel(0, 0, True) # Water level sensor created in dummy mode

# test modules
print("Testing Modules...")
if not moisture.test():
    raise Exception("Moisture sensor failed test.")
if not waterLevel.test():
    raise Exception("Water level sensor failed test.")

# set water level
waterLevel.set()

# connect to AWS
print("Connecting to AWS...")
try:
    ipwsClient.connect()
except Exception:
    raise
# main loop
print("Beginning to monitor soil moisture.")
time.sleep(2) # small delay before monitoring so it doesn't immediately start flooding console with stuff

try:
    while True:

        # Water level check, if low disable pump
        if waterLevel.waterIsLow():
            if ipwsClient.pumpIsEnabled:
                ipwsClient.disablePump("Water is low")

        # moisture check
        if moisture.isDry():
            ipwsClient.notifyDry()
            if ipwsClient.pumpIsEnabled:
                print("Sending notification and turning on pump.")
                ipwsClient.notifyWatering()
                pump.pumpForSeconds(3)
                print("Turning off pump and sleeping.")
        else:  # not dry, all is good
            print("Soil is moist.")

        time.sleep(30)
except KeyboardInterrupt:
    raise
except Exception:
    raise
