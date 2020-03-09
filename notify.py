from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json

client = AWSIoTMQTTClient(clientId) #clientId can be anything
client.configureEndpoint(host, port) #host is your Pi’s AWS IoT Endpoint, port is 8883
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

#AWSIoTMQTTClient connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
client.configureDrainingFrequency(2)  # Draining: 2 Hz
client.configureConnectDisconnectTimeout(10)  # 10 sec
client.configureMQTTOperationTimeout(5)  # 5 sec

client.connect()
client.subscribe(topic, 1, customCallback)
time.sleep(2)

message = {}
message['message'] = “your message"
message['sequence'] = loopCount
messageJson = json.dumps(message)
client.publish(topic, messageJson, 1)
