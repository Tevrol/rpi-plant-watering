import RPi.GPIO as GPIO
import time

class Moisture:
    def __init__(self,pin):
        self.pin = pin

    def __del__(self):
        GPIO.cleanup()

    def test(self):
        try:
            GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
            GPIO.setwarnings(False)  # disable warnings
            # set button pin to an input port and set to pull-down mode
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            flag = False
            for x in range(10):
                if (read() != None and flag != True):
                    flag = True

            GPIO.cleanup()
            return flag
        except Exception as e:
            GPIO.cleanup()
            return False

    def read(self):
        try:
            GPIO.setmode(GPIO.BCM)  # for GPIO pin numbering
            GPIO.setwarnings(False)  # disable warnings
            # set button pin to an input port and set to pull-down mode
            GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            result = not(GPIO.input(self.pin))
        except Exception as e:
            return None
        finally:
            GPIO.cleanup()
        return result

    def isDry(self):
        count = 0
        for x in range(9):
            if read():
                count++
            time.sleep(1)
        if (count > 7):
            return True
        else return False
