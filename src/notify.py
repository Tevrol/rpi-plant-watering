from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import json


# Config Information
class Notify:
    def __init__(self, config):
        self.clientId = "Waterer"
        self.__host = config['host']
        self.__port = config['port']
        self.__rootCAPath = config['rootCAPath']
        self.__privateKeyPath = config['privateKeyPath']
        self.__certificatePath = config['certificatePath']
        self.topic = "water"
        self.commandTopic = "watererCommmand"
        self.pumpIsEnabled = True
        self.sequence = 0
        # initialize
        self.client = AWSIoTMQTTClient(self.clientId)
        self.client.configureEndpoint(self.__host, self.__port)
        self.client.configureCredentials(
            self.__rootCAPath, self.__privateKeyPath, self.__certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)
        # Infinite offline Publish queueing
        self.client.configureOfflinePublishQueueing(-1)
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        # Connect and subscribe to AWS IoT


    def receiveWaterCommand(self, client, userdata, message):
        message = json.loads(message.payload)['message']
        if message == "Disable Pump":
            self.disablePump("Disabled from cloud")
        elif message == "Enable Pump":
            self.enablePump()
        else pass

    def connect(self):
        self.client.connect()
        self.client.subscribe(self.commandTopic, 1, self.receiveWaterCommand)

    # Publish
    def notifyDry(self):
        print("Sending dry notification to cloud.")
        publishBasicMessage("Dry")

    def notifyWatering(self):
        print("Sending watering notification to cloud.")
        publishBasicMessage("Watering")

    def disablePump(self, reason):
        print("Sending pump disabled notification to cloud for reason: ",reason,".")
        self.pumpIsEnabled = False
        message = {}
        message['message'] = "Pump Disabled"
        message['reason'] = reason
        message['time'] = datetime.now().__str__()
        message['sequence'] = self.sequence
        self.sequence += 1
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

    def enablePump(self):
        print("Sending pump enabled notification to cloud.")
        self.pumpIsEnabled = True
        publishBasicMessage("Pump is enabled")


    def publishBasicMessage(self,messageText):
        message = {}
        message['message'] = messageText
        message['time'] = datetime.now().__str__()
        message['sequence'] = self.sequence
        self.sequence += 1
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)
