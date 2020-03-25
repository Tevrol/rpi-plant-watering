from ultrasonic_distance import UltrasonicDistance
import time

class WaterLevel
    def __init__(self,trigger,echo,dummy):
        self.dummy = dummy
        self.waterLevel = 999
        if not self.dummy:
            self.sensor = UltrasonicDistance(trigger,echo)
        else:
            print("Warning: Water level sensor set to dummy mode.")
            print("Pump will run dry in this mode.")

    def test(self):
        """
        Function to test whether or not the sensor is operating
        """
        if self.dummy:
            return True
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
        if self.dummy:
            return 0
        for x in range(10):
            distances[x] = sensor.distance()
            time.sleep(0.1)

        distance = 0
        for x in range(len(distances)):
            distance += distances[x]

        distance = distance / len(distances)
        return distance

    def set(self):
        if self.dummy:
            self.waterLevel = 0
            return
        self.waterLevel = read()

    def waterIsLow(self):
        if self.dummy:
            return False
