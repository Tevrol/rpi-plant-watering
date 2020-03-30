import RPi.GPIO as GPIO
import time


class Moisture:
    def __init__(self, pin):
        self.pin = pin

    def test(self):
        """
        This function tests the moisture pin to see if it's reading correctly.

        Returns:
            bool: True if test passed, False otherwise.
        """
            count = 0
            for x in range(10):
                if (self.read() is not None):
                    count += 1
            if (count > 5):
                return True
            else:
                raise Exception("Moisture sensor failed test")
            return False

    def read(self):
        """
        This function reads the moisture sensor pin for an input. Sensor returns HIGH when no moisture,
        LOW when there is moisture.

        Returns:
            None: if it has an issue reading the pin.
            bool: Returns True if HIGH, False if LOW
        """
        try:
            GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
            GPIO.setwarnings(False)  # disable warnings
            # set moisture pin as input in pull-up mode
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            result = GPIO.input(self.pin)
        except Exception:
            return None
        finally:
            GPIO.cleanup()
        return result

    def isDry(self):
        """
        This function polls the moisture sensor 10 times. If it reads 8 or more LOW then it's dry.

        Returns:
            bool: True if dry, False if not
        """
        count = 0
        for x in range(9):
            if self.read():
                count += 1
            time.sleep(0.05)
        if (count > 7):
            return True
        else:
            return False
