from ultrasonic_distance import UltrasonicDistance
import time

class WaterLevel
    def __init__(self,trigger,echo):
        self.sensor = UltrasonicDistance(trigger,echo)

    def test(self):
        """
        Function to test whether or not the sensor is operating
        """
        for x in range(10):
            if (bool(sensor.distance())):
                return True
            else:
                time.sleep(0.1)
        return False

    def read(self):
        """
        Returns a somewhat averaged distance from an ultrasonic sensor
        """
        for x in range(10):
            distances[x] = sensor.distance()
            time.sleep(0.1)

        distance = 0
        for x in range(len(distances)):
            distance += distances[x]

        distance = distance / len(distances)
        return distance
