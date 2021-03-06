# To be able to use the hue api a user must be registered first, it can be done with the following shell command:
"""
curl -H "Accept: application/json" -X POST --data '{"devicetype":"pi_app"}' http://192.168.1.103/api

[{"success":{"username":"3cae0cad339cb36732cf4f6920ad5183"}}]
"""

import json
import time
import requests

DBG_MOCK = False
if DBG_MOCK:
    import RPi_MOCK as GPIO
else:
    import RPi.GPIO as GPIO


DBG_LOG = True

HUE_USER = "3cae0cad339cb36732cf4f6920ad5183"

class ColorButton:
    """Class for handling of colorful buttons"""

    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

        # Set gpio pin to input and activate pull down
        GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Check if button is pressed and return True if so
    def poll(self):
        if DBG_MOCK == True:
            if self.color == "blue" or self.color == "green":
                self.status = True
                return True


        if GPIO.input(self.pin) == True:
            self.status = not self.status
            return True
        return False

    def getStatus(self):
        return self.status

class ButtonLed:
    """Class for handling of colorful led lights on the console"""

    def __init__(self, color, gpio_pin):
        self.color = color
        self.pin = gpio_pin
        self.status = False

         # Set gpio pin to input and activate pull up
        GPIO.setup(gpio_pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

    def setStatus(self, status):
        self.status = status
        GPIO.output(self.pin, not self.status)

class HueLamp():
    """Hue Lamp class"""
    HUE_COLORS_DEG = {"red" : 0,
                      "yellow" : 60,
                      "green" : 120,
                      "cyan" : 180,
                      "blue" : 240,
                      "purple" : 300}
    color = ""
    def __init__(self, url):
        self.url = url

    def getState(self):
        self.http_request("get")

    def mixColors(self, colors):
        if len(colors) == 1:
            return int(self.HUE_COLORS_DEG[colors[0]] * (65535/360))

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
            color = self.mixColors(colorList)
            if color == self.color:
                if DBG_LOG:
                    print "No change in color, don't send to Hue"
                return

            self.color = color
            d = {'on':state,
                 'bri':100,
                 'hue':self.color,
                 'sat':255}

        if DBG_LOG:
            print "Set lamp state: " ,d

        r = requests.put(self.url + "/state", data=json.dumps(d))

        print self.url + "/state"
        if r.status_code != 200:
            print "Bad response %s from %s" % (r.status_code, self.url)
        print r.json()


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

    lamp = HueLamp("http://192.168.1.103/api/" + HUE_USER + "/lights/1")

    while(True):
        # Main loop
        time.sleep(0.1)

        pressed = False
        for btn in btnList:
            pressed = btn.poll() or pressed

        # Start over if no button is pressed
        if pressed == False:
            continue

        # Set button led value
        colorList = []
        for btn in btnList:
            color = btn.color
            ledDict[btn.color].setStatus(btn.getStatus)

            # Append this color to list of colors
            if btn.getStatus:
                colorList.append(color)

        lamp.setState(True, colorList, 100)

if __name__ == "__main__":
    main()
