from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import json


# Config Information
class IpwsClient:
    def __init__(self, config):
        self.clientId = "Waterer"  # This is currently static.

        # AWS connection details from constructor
        self.__host = config['host']
        self.__port = config['port']
        self.__rootCAPath = config['rootCAPath']
        self.__privateKeyPath = config['privateKeyPath']
        self.__certificatePath = config['certificatePath']

        # topic to publish to and command topic to subscribe to
        self.topic = "water"
        self.commandTopic = "watererCommand"

        # initial state
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

    def receiveWaterCommand(self, client, userdata, message):
        message = json.loads(message.payload)['message']
        if message == "Disable Pump":
            self.disablePump("Disabled from cloud")
        elif message == "Enable Pump":
            self.enablePump()
        else:
            pass

    def connect(self):
        """
        Connects to the AWS MQTT broker and subscribes to the command topic
        """
        self.client.connect()
        self.client.subscribe(self.commandTopic, 1, self.receiveWaterCommand)

    def publishBasicMessage(self, messageText):
        """
        Publishes a basic message to the AWS cloud using the configured topic.
        Sends a message, current time, and sequence number to the cloud. Updates the MQTT sequence number.

        Args:
            messageText (str): The message text to be send as the message property of the MQTT message
        """
        message = {}
        message['message'] = messageText
        message['time'] = datetime.now().__str__()
        message['sequence'] = self.sequence
        self.sequence += 1
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 0)

    # Publish
    def notifyDry(self):
        print("Sending dry notification to cloud.")
        self.publishBasicMessage("Dry")

    def notifyWatering(self):
        print("Sending watering notification to cloud.")
        self.publishBasicMessage("Watering")

    def disablePump(self, reason):
        """
        Disables the pump and sends a notifcation w/ disable reason to the AWS cloud.

        Args:
            reason (str): Reason for disabling the pump
        """
        print("Sending pump disabled notification to cloud for reason: %s." % reason)
        self.pumpIsEnabled = False
        message = {}
        message['message'] = "PumpDisabled"
        message['reason'] = reason
        message['time'] = datetime.now().__str__()
        message['sequence'] = self.sequence
        self.sequence += 1
        messageJson = json.dumps(message)
        self.client.publish(self.topic, messageJson, 0)

    def enablePump(self):
        """
        Enables the pump and notifies the cloud.
        """
        print("Sending pump enabled notification to cloud.")
        self.pumpIsEnabled = True
        self.publishBasicMessage("PumpEnabled")
