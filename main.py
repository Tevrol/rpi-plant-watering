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

#create objects
moisture = Moisture(moisturePin)
pump = Pump(pumpPin)
notify = Notify(config)
waterLevel = WaterLevel(0,0,True)

#test modules
moisture.test()

#connect to AWS
try:
    notify.connect()
except:
    raise
#main loop
try:
    while True:
        if (moisture.isDry()):
            notify.notifyDry()
            if notify.pumpIsEnabled():
                notify.notifyWatering()
                pump.pumpForSeconds(1)
        else: #not dry, all is good
            sleep(60)
except KeyboardInterrupt:
    GPIO.cleanup()
except:
    raise
