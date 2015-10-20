import time
#import RPi.GPIO as GPIO
import RPi_MOCK as GPIO
import requests
import math

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
    HUE_COLORS_DEG = {"red" : 0,
                      "yellow" : 60,
                      "green" : 120,
                      "cyan" : 180,
                      "blue" : 240,
                      "purple" : 300}
    def __init__(self, url):
        self.url = url

    def getState(self):
        self.http_request("get")

    def mixColors(self, colors):
        if len(colors) == 1:
            return self.HUE_COLORS_DEG[colors[0]]

        mix = (self.HUE_COLORS_DEG[colors[0]] + self.HUE_COLORS_DEG[colors[1]])/2
        return int(mix * (65535/360))

    def setState(self, state, colorList, brightness):
        if len(colorList) == 0:
            return
        elif len(colorList) > 2:
            d = {'on':state,
                 'bri':255,
                 'hue':25000,
                 'sat':255,
                 'effect':"colorloop"}
        else:
            d = {'on':state,
                 'bri':255,
                 'hue':self.mixColors(colorList),
                 'sat':255}

        if DBG_LOG:
            print d
        requests.put(self.url + "/state", data=d)

        
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
               "yellow" : ButtonLed("yellow", 25),
               "white" : ButtonLed("white", 8)}

    lamp = HueLamp("http://192.168.1.102/newdeveloper/ligths/3")

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
        colorList = []
        for color, val in colorDict.items():
            ledDict[color].setStatus(val)

            if val == True:
                colorList.append(color)

        lamp.setState(True, colorList, 100)
        
if __name__ == "__main__":
    main()
