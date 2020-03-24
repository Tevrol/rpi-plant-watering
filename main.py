#imports
from moisture import Moisture
from pump import Pump
from notify import Notify
from waterLevel import WaterLevel

#https://codereview.stackexchange.com/questions/238105/interactive-discord-bot-for-tabletop-rpg

#configure MQTT connection
config = {}
config['host']
config['port'] = "8883"
config['rootCAPath'] = "/home/pi/cert/CA.pem"
config['privateKeyPath'] = "/home/pi/cert/.pem.key"
config['certificatePath'] = "/home/pi/cert/.pem.crt"
#init pin variables
pumpPin = 20
moisturePin = 20
sonicTriggerPin = 20
sonicEchoPin = 20

maxWaterDistance = 20

#create objects
moisture = Moisture(moisturePin)
pump = Pump(pumpPin)
notify = Notify(config)
waterLevel = WaterLevel(sonicTriggerPin,sonicEchoPin)

#test all modules
waterLevel.test()
moisture.test()
pump.test()

#connect to AWS

#main loop
while True:
    if (waterLevel.read() < maxWaterDistance):
        if (moisture.isDry()):
            pump.pumpForSeconds(5)
        else: #not dry, all is good
    else: #no water
