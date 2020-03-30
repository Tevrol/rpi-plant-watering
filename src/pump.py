import RPi.GPIO as GPIO
import time


class Pump:
    def __init__(self, pin):
        self.pin = pin

    def __del__(self):
        GPIO.cleanup()

    def pumpForSeconds(self, seconds):
        """
        Turns on the water pump for a given number of seconds.

        Args:
            seconds (int): Number of seconds to turn pump on for
        """
        GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
        GPIO.setwarnings(False)  # disable warnings
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 0)
        time.sleep(seconds)
        GPIO.output(self.pin, 1)
