# imports
from src.moisture import Moisture
from src.pump import Pump
from src.notify import Notify
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
notify = Notify(config)
waterLevel = WaterLevel(0, 0, True)

# test modules
print("Testing Modules...")
moisture.test()
waterLevel.test()

# set water level
waterLevel.set()

# connect to AWS
print("Connecting to AWS...")
try:
    notify.connect()
except Exception:
    raise
# main loop
print("Beginning to monitor soil moisture.")
try:
    while True:
        notify.disablePump("Water is low") if waterLevel.waterIsLow() else notify.enablePump()
        if moisture.isDry():
            notify.notifyDry()
            if notify.pumpIsEnabled:
                print("Sending notification and turning on pump.")
                notify.notifyWatering()
                pump.pumpForSeconds(1)
                print("Turning off pump and sleeping.")
        else:  # not dry, all is good
            print("Soil is moist.")
        time.sleep(60)
except KeyboardInterrupt:
    raise
except Exception:
    raise
