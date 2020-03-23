from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json


# Config Information


clientId = "Waterer"

host = ""
port = "8883"
rootCAPath = "/home/pi/cert/CA.pem"
privateKeyPath = "/home/pi/cert/.pem.key"
certificatePath = "/home/pi/cert/.pem.crt"


# Custom MQTT message callback
topic = "water"


def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# initialize
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)  # clientId can be anything
# host is your Pi’s AWS IoT Endpoint, port is 8883
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(
    rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

# Publish


def waterPublish():
    message = {}
    message['message'] = ""
    message['sequence'] = 0
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
