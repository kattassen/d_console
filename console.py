import time
"""import RPi.GPIO as GPIO"""

DBG_LOG = True

class ColorButton:
    """Class for handling of colorful buttons"""

    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

        """
        # Set gpio pin to input and activate pull down
        GPIO.setup(gpio_pin, GPIO.in, pull_up_down=GPIO.PUD_DOWN)
        """

    def getStatus(self):
        """self.status = GPIO.input(self.pin)"""
        return self.status

class ButtonLed:
    """Class for handling of colorful led lights on the console"""
    
    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

        """
        # Set gpio pin to output and
        GPIO.setup(gpio_pin, GPIO.out)
        """

    def setStatus(self, status):
        self.status = status
        """GPIO.output(self.pin, status)"""

def main():
    """Main function"""

    colorDict = {"red" : 0,
                 "blue" : 0,
                 "green" : 0,
                 "yellow" : 0}

    btnList = [ColorButton("red", 4),
               ColorButton("blue", 17),
               ColorButton("green", 27),
               ColorButton("yellow", 22),
               ColorButton("white", 10)]

    ledList = [ButtonLed("red", 18),
               ButtonLed("blue", 23),
               ButtonLed("green", 24),
               ButtonLed("yellow", 25)]

    while(True):
        # Main loop
        time.sleep(0.1)

        # Check all buttons and store values
        btnPressed = False
        for btn in btnList:
            if btn.getStatus():
                colorDict[btn.color] = True
                btnPressed = True
            else:
                colorDict[btn.color] = False

        # Start over if no button is pressed
        if not btnPressed:
            continue

        if DBG_LOG:
            print "Buttons satus: " + str(colorDict)

        # Set LED according to button status
        for led in ledList:
            led.setStatus(colorDict[btn.color])
        
if __name__ == "__main__":
    main()
