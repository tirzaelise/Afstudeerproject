# !/usr/bin/env python2

# This file uses an event listener to detect whether the Nao's left hand is
# being touched at the back. If it is, its eyes rotate until it is let go of
# again. This will be used as a listening duration.


import os
from random import choice
from recognise_speech import recognise_speech
import subprocess
import sys
import time

from understand_language import Understand
from generate_language import Generate

from naoqi import ALBroker, ALProxy, ALModule


class TouchDetectorModule(ALModule):
    """ This class detects whether the Nao's left hand is touched. """

    def __init__(self, name, ip, ats, recording_file, understand, generate,
                 question):
        ALModule.__init__(self, name)

        self.load_templates()
        self.alt = ALProxy("ALTouch", ip, 9559)
        self.als = ALProxy("ALLeds", ip, 9559)
        self.aar = ALProxy("ALAudioRecorder", ip, 9559)
        self.ats = ats
        self.alm = ALProxy("ALMemory")
        self.alm.subscribeToEvent("HandLeftBackTouched", "TouchDetector",
                                  "onTouched")

        self.ip = ip
        self.recording_file = recording_file
        self.understand = understand
        self.generate = generate
        self.question = question


    def load_templates(self):
        """
        Loads the templates of replies and saves them as a list in a dictionary.
        """

        self.templates = {}

        if os.path.exists("reply_templates.txt"):
            for line in open("reply_templates.txt", "r"):
                key, value = line.split(": ")
                if key not in self.templates:
                    self.templates.update({key: [value]})
                else:
                    existent_value = self.templates.get(key)
                    existent_value.append(value)
                    self.templates.update({key: existent_value})


    def onTouched(self, *_args):
        """
        This function is called each time the Nao's hand is touched. It starts
        recording the audio using the Nao's microphones for as long as the back
        of its left hand is being touched and rotates its eyes to indicate that
        he is listening/recording.
        """

        # Sometimes the microphone is already recording.
        self.aar.stopMicrophonesRecording()

        # Unsubscribe while listening and analysing.
        self.alm.unsubscribeToEvent("HandLeftBackTouched", "TouchDetector")
        print "unsubscribe"

        # Checks if the user started to touch the Nao's hand, in which case the
        # value is True, or if the user stopped touching the Nao's hand, in
        # which case the value is False. This is done to prevent the microphones
        # from starting to record again when the user stops touching the robot's
        # hand.

        # if self.alt.getStatus()[15][1] is True: # Nao
        if self.alt.getStatus()[12][1] is True:
            self.record_audio()

            sentence = recognise_speech(self.ip, self.recording_file)
            print sentence

            if sentence:
                if not "repeat" in sentence:
                    self.handle_answer(sentence)
                else:
                    # Agent asked to repeat the question
                    repeat = "Of course. " + self.question
                    self.ats.say(str(self.question))
            else:
                # Did not hear
                reply = choice(self.templates.get("not_heard"))
                self.ats.say(str(reply))

        self.alm.subscribeToEvent("HandLeftBackTouched", "TouchDetector",
                                  "onTouched")
        print "subscribe"


    def record_audio(self):
        """ Uses the Nao's microphones to record audio. """

        print "start recording"
        self.aar.startMicrophonesRecording(self.recording_file, "wav",
                                           16000, (0, 0, 1, 0))

        # while self.alt.getStatus()[15][1] is True: # Nao
        while self.alt.getStatus()[12][1] is True:
            self.als.rotateEyes(0x001E90FF, 0.35, 0.01)

        self.aar.stopMicrophonesRecording()
        print "stop recording"


    def handle_answer(self, answer):
        """
        Handles the answer that was given by replying that the answer was either
        understood or not.
        """

        understood = self.understand.understand_sentence(self.question, answer)

        if understood:
            # Understood and updated the drinks
            reply = choice(self.templates.get("understand_affirmative"))
            self.ats.say(str(reply))
            properties = self.understand.get_properties()

            if properties:
                self.generate_new_question(properties)
            else:
                self.finish()

        else:
            # Did not understand
            reply = choice(self.templates.get("understand_negative"))
            self.ats.say(str(reply))


    def generate_new_question(self, properties):
        """ Generates a new question from the list of drink properties. """

        self.question = self.generate.generate_language(properties)

        if self.question:
            self.ats.say(str(self.question))
        else:
            # If there are no more questions available, the program has finished
            self.finish()


    def finish(self):
        """ Finish the program. """

        available_drinks = self.understand.get_available_drinks()
        finished = self.get_finished_string(available_drinks)
        self.ats.say(str(finished))


    def get_finished_string(self, available_drinks):
        """ Constructs the string that indicates the end of the program. """

        start = "I think I have all the information I need. "

        if len(available_drinks) == 0:
            print "no available drinks"
            end = "There are no available drinks."
        else:
            print "drinks available"
            available_string = ", ".join(available_drinks)
            end = "The available drinks are " + available_string
        return start + end


if __name__ == "__main__":
    ordered_drinks = ["bloody mary"]
    understand = Understand(ordered_drinks)
    properties = understand.get_properties()
    generate = Generate()
    question = generate.generate_language(properties)

    global TouchDetector
    ip = "pepper.local"
    ats = ALProxy("ALTextToSpeech", ip, 9559)
    ats.setParameter("speed", 92)
    ats.say(str(question))

    ownBroker = ALBroker("ownBroker", "0.0.0.0", 0, ip, 9559)
    TouchDetector = TouchDetectorModule("TouchDetector", ip, ats,
                                        "recording.wav", understand, generate,
                                        question)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
                print "\nInterrupted by user, shutting down"
                ownBroker.shutdown()
                sys.exit(0)
