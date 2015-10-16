import time
#import RPi.GPIO as GPIO
import RPi_MOCK as GPIO

DBG_LOG = True

class ColorButton:
    """Class for handling of colorful buttons"""

    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

        # Set gpio pin to input and activate pull down
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def getStatus(self):
        self.status = GPIO.input(self.pin)
        return self.status

class ButtonLed:
    """Class for handling of colorful led lights on the console"""
    
    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

        # Set gpio pin to output and
        GPIO.setup(gpio_pin, GPIO.OUT)

    def setStatus(self, status):
        self.status = status
        GPIO.output(self.pin, status)

class HueLamp():
    """Hue Lamp class"""
    def __init__(self, url):
        self.url = url

    def get_state(self):
        self.http_request("get")

    def set_state(self, color, brightness):
        self.http_request("put", json.dumps({'on':state, 'bri':100, 'hue':0, 'sat':100}))


        
def main():
    """Main function"""

    # Set GPIO numbering mode
    GPIO.setmode(GPIO.BCM)

    btnList = [ColorButton("red", 4),
               ColorButton("blue", 17),
               ColorButton("green", 27),
               ColorButton("yellow", 22),
               ColorButton("white", 10)]

    ledDict = {"red" : ButtonLed("red", 18),
               "blue" : ButtonLed("blue", 23),
               "green" : ButtonLed("green", 24),
               "yellow" : ButtonLed("yellow", 25)}

    while(True):
        # Main loop
        time.sleep(0.1)

        # Check all buttons and store values
        colorDict = {}
        for btn in btnList:
            if btn.getStatus():
                colorDict[btn.color] = True
            else:
                colorDict[btn.color] = False

        # Start over if no button is pressed
        if len(colorDict) == 0:
            continue

        if DBG_LOG:
            print "Buttons satus: " + str(colorDict)

        # Set LED according to button status
        for led in ledList:
            led.setStatus(colorDict[btn.color])
        
if __name__ == "__main__":
    main()
