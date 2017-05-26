# !/usr/bin/env python2

# This file uses the Nao's microphones to record audio. The audio is saved on
# the Nao in a temporary directory that is renamed when the Nao starts up, but
# always starts with "naoqi" and is always located in "/var/volatile/tmp". This
# directory is found and the audio file is copied to the computer. Then, IBM
# Watson's speech to text API is used to transcribe the audio file.

from energy_levels import level_in_baseline
import json
from naoqi import ALProxy
import os
import subprocess
import time
from watson_developer_cloud import SpeechToTextV1


def find_naoqi_folder(ip):
    """
    The sound recording is saved in a temporary folder on the Nao itself and the
    name of the folder always changes so the folder has to be found first.
    """

    temp_folder = "/var/volatile/tmp"
    cmds = ["ssh nao@" + ip, "cd "+ temp_folder, "find . -name naoqi* " + \
        "-type d 2> /dev/null", "exit"]
    p = subprocess.Popen("/bin/bash", stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    for cmd in cmds:
        p.stdin.write(cmd + "\n")
    p.stdin.close()

    naoqi_folder =  p.stdout.read().replace("\n", "").replace(".", "")
    return temp_folder + naoqi_folder


def record_audio(ip, file_path):
    """
    Uses the built-in NAOqi function to record audio using the Nao's
    microphones.
    """

    aar = ALProxy("ALAudioRecorder", ip, 9559)
    aap = ALProxy("ALAudioPlayer", ip, 9559)

    # Sometimes the microphone is already recording.
    aar.stopMicrophonesRecording()

    print "start recording"
    aar.startMicrophonesRecording(file_path, "wav", 16000, (0, 0, 1, 0))

    # Record while the energy levels are not close in range to the baseline.
    while not level_in_baseline(ip):
        print "listening"

    aar.stopMicrophonesRecording()
    print "stop recording"


def copy_audio(ip, naoqi_folder, file_path):
    """ Copies the recorded audio file to the computer. """

    cmd = "scp nao@" + ip + ":" + naoqi_folder + "/" + file_path + " ."
    os.system(cmd)


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        return json.dumps(speech_to_text.recognize(audio_file,
                                                   content_type="audio/wav"),
                          indent=2)


if __name__ == "__main__":
    ip = "146.50.60.43"
    file_path = "recording.wav"

    speech_to_text = SpeechToTextV1(
        username = "55cc7a57-301f-4f86-b38d-d3609f132000",
        password = "dPycbcXvAYIX",
        x_watson_learning_opt_out=False,
        )

    naoqi_folder = find_naoqi_folder(ip)
    record_audio(ip, file_path)
    copy_audio(ip, naoqi_folder, file_path)
    transcribe_audio(file_path)
