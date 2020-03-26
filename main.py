#imports
from moisture import Moisture
from pump import Pump
from notify import Notify
from waterLevel import WaterLevel
import time

# https://codereview.stackexchange.com/questions/238105/interactive-discord-bot-for-tabletop-rpg

print(
'''
  _____ _______          _______
 |_   _|  __ \ \        / / ____|
   | | | |__) \ \  /\  / / (___
   | | |  ___/ \ \/  \/ / \___ \
  _| |_| |      \  /\  /  ____) |
 |_____|_|       \/  \/  |_____/
  IoT  Plant    Watering  System
'''
)
# configure MQTT connection
print("Loading Config...")
config = {}
config['host']
config['port'] = "8883"
config['rootCAPath'] = "/home/pi/cert/CA.pem"
config['privateKeyPath'] = "/home/pi/cert/.pem.key"
config['certificatePath'] = "/home/pi/cert/.pem.crt"
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
        if (moisture.isDry()):
            print("Soil is dry, sending notification.")
            notify.notifyDry()
            if notify.pumpIsEnabled() and not waterLevel.waterIsLow():
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
