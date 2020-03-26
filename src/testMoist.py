from moisture import Moisture
import time

#this script is for tuning the moisture sensor
#just prints is dry or not endlessly

moisturePin = 20

#create objects
moisture = Moisture(moisturePin)

print("Testing moisture")
moisture.test()

while True:
    print(moisture.isDry())
    sleep(2)
