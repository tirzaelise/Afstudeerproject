# !/usr/bin/env python2

# This file uses an event listener to detect whether the Nao's left hand is
# being touched at the back. If it is, its eyes rotate until it is let go of
# again. This will be used as a listening duration.


import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

TouchDetector = None


class TouchDetectorModule(ALModule):
    """ This class detects whether the Nao's left hand is touched. """

    def __init__(self, name, ip):
        ALModule.__init__(self, name)

        self.alt = ALProxy("ALTouch", ip, 9559)
        self.aal = ALProxy("ALLeds", ip, 9559)
        alm = ALProxy("ALMemory")
        alm.subscribeToEvent("HandLeftBackTouched", "TouchDetector",
                                "onTouched")


    def onTouched(self, *_args):
        """ This function is called each time the Nao's hand is touched. """

        while self.alt.getStatus()[15][1] == True:
            self.aal.rotateEyes(0x001E90FF, 0.35, 0.01)


if __name__ == "__main__":
    global TouchDetector
    ip = "146.50.60.43"
    ownBroker = ALBroker("ownBroker", "0.0.0.0", 0, ip, 9559)
    TouchDetector = TouchDetectorModule("TouchDetector", ip)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "\nInterrupted by user, shutting down"
        ownBroker.shutdown()
        sys.exit(0)
