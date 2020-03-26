import RPi.GPIO as GPIO
import time


class Pump:
    def __init__(self, pin):
        self.pin = pin

    def __del__(self):
        GPIO.cleanup()

    def pumpForSeconds(self, seconds):
        try:
            GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
            GPIO.setwarnings(False)  # disable warnings
            GPIO.output(self.pin, 1)
            time.sleep(seconds)
            GPIO.output(self.pin, 0)
        except Exception:
            pass
        finally:
            GPIO.cleanup()
