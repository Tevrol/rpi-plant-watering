import RPi.GPIO as GPIO
import time


class Moisture:
    def __init__(self, pin):
        self.pin = pin

    def __del__(self):
        GPIO.cleanup()

    def test(self):
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
        try:
            GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
            GPIO.setwarnings(False)  # disable warnings
            # set button pin to an input port and set to pull-down mode
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            result = GPIO.input(self.pin)
        except Exception:
            return None
        finally:
            GPIO.cleanup()
        return result

    def isDry(self):
        count = 0
        for x in range(9):
            if self.read():
                count += 1
            time.sleep(0.05)
        if (count > 7):
            return True
        else:
            return False
