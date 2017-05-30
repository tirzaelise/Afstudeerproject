# !/usr/bin/env python2

# This file uses an event listener to detect whether the Nao's left hand is
# being touched at the back. If it is, its eyes rotate until it is let go of
# again. This will be used as a listening duration.


import os
from recognise_speech import recognise_speech
import subprocess
import sys
import time
from understand_language import Understand

from naoqi import ALBroker, ALProxy, ALModule


class TouchDetectorModule(ALModule):
    """ This class detects whether the Nao's left hand is touched. """

    def __init__(self, name, ip, recording_file, understand):
        ALModule.__init__(self, name)

        self.alt = ALProxy("ALTouch", ip, 9559)
        self.als = ALProxy("ALLeds", ip, 9559)
        self.aar = ALProxy("ALAudioRecorder", ip, 9559)
        self.ip = ip
        self.recording_file = recording_file
        self.understand = understand
        alm = ALProxy("ALMemory")
        alm.subscribeToEvent("HandLeftBackTouched", "TouchDetector",
                                "onTouched")


    def onTouched(self, *_args):
        """
        This function is called each time the Nao's hand is touched. It starts
        recording the audio using the Nao's microphones for as long as the back
        of its left hand is being touched and rotates its eyes to indicate that
        he is listening/recording.
        """

        # Sometimes the microphone is already recording.
        self.aar.stopMicrophonesRecording()

        # Checks if the user started to touch the Nao's hand, in which case the
        # value is True, or if the user stopped touching the Nao's hand, in
        # which case the value is False. This is done to prevent the microphones
        # from starting to record again when the user stops touching the robot's
        # hand.
        if self.alt.getStatus()[15][1] == True:
            self.record_audio()
            sentence = recognise_speech(self.ip, self.recording_file)
            if sentence:
                understand.understand_sentence(sentence)


    def record_audio(self):
        """ Uses the Nao's microphones to record audio. """

        print "start recording"
        self.aar.startMicrophonesRecording(self.recording_file, "wav",
                                           16000, (0, 0, 1, 0))

        while self.alt.getStatus()[15][1] == True:
            self.als.rotateEyes(0x001E90FF, 0.35, 0.01)

        self.aar.stopMicrophonesRecording()
        print "stop recording"


if __name__ == "__main__":
    understand = Understand()
    global TouchDetector
    ip = "146.50.60.43"
    ownBroker = ALBroker("ownBroker", "0.0.0.0", 0, ip, 9559)
    TouchDetector = TouchDetectorModule("TouchDetector", ip, "recording.wav",
                                        understand)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
                print "\nInterrupted by user, shutting down"
                ownBroker.shutdown()
                sys.exit(0)
