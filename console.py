import time

DBG_LOG = True

class ColorButton:
    """Class for handling of colorful buttons"""

    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

    def getStatus(self):
        return self.status

class ButtonLed:
    """Class for handling of colorful led lights on the console"""
    
    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

    def setStatus(self, status):
        self.status = status

def main():
    """Main function"""

    colorDict = {"red" : 0,
                 "blue" : 0,
                 "green" : 0,
                 "yellow" : 0}

    btnList = [ColorButton("red", 11),
               ColorButton("blue", 12),
               ColorButton("green", 12),
               ColorButton("yellow", 12),
               ColorButton("white", 12)]

    ledList = [ButtonLed("red", 11),
               ButtonLed("blue", 12),
               ButtonLed("green", 12),
               ButtonLed("yellow", 12)]
        
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
