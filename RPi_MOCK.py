
BCM = 0
BOARD = 1
IN = 0
OUT = 1
PUD_DOWN = 0
PUD_UP = 1
    
def setup(pin, dir, pull_up_down=0):
    print "Setup GPIO pin: %d %d %d" % (pin, dir, pull_up_down)

def setmode(mode):
    print "Set GPIO mode: %d" % (mode)

def input(pin):
    print "Check input GPIO pin %d" % (pin)
    return False

def output(pin, state):
    print "Set output %r on GPIO pin %d" % (state, pin)

