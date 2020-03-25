from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import json


# Config Information
class Notify:
    def __init__(self,config):
        self.clientId = "Waterer"
        self.__host = config.host
        self.__port = config.port
        self.__rootCAPath = config.rootCAPath
        self.__privateKeyPath = config.privateKeyPath
        self.__certificatePath = config.certificatePath
        self.topic = "water"
        self.enablePump = True
        self.sequence = 0
        # initialize
        self.client = AWSIoTMQTTClient(self.clientId)  # clientId can be anything
        # host is your Pi’s AWS IoT Endpoint, port is 8883
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


    def waterCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")

    def connect(self):
        self.client.connect()
        self.client.subscribe(topic, 1, waterCallback)

    # Publish
    def notifyDry(self):
        message = {}
        message['message'] = "Dry"
        message['time'] = datetime.now()
        message['sequence'] = self.sequence++
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

    def notifyWatering(self):
        message = {}
        message['message'] = "Watering"
        message['time'] = datetime.now()
        message['sequence'] = self.sequence++
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

    def disablePump(self,reason):
        self.enable = False
        message = {}
        message['message'] = "Pump Disabled"
        message['reason'] = reason
        message['time'] = datetime.now()
        message['sequence'] = self.sequence++
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

    def enablePump(self):
        self.enable = True
        message = {}
        message['message'] = "Pump Enabled"
        message['time'] = datetime.now()
        message['sequence'] = self.sequence++
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 1)

    def pumpIsEnabled(self):
        return self.enable
