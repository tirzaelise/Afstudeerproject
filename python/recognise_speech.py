# !/usr/bin/env python2

# This file uses the Nao's microphones to record audio. The audio is saved on
# the Nao in a temporary directory that is renamed when the Nao starts up, but
# always starts with "naoqi" and is always located in "/var/volatile/tmp". This
# directory is found and the audio file is copied to the computer. Then, IBM
# Watson's speech to text API is used to transcribe the audio file.


from google.cloud import speech
import io
from naoqi import ALProxy
import os
import subprocess
import time


def copy_audio(ip, recording_file):
    """ Copies the recorded audio file to the computer. """

    naoqi_folder = find_naoqi_folder(ip)
    cmd = "scp nao@" + ip + ":" + naoqi_folder + "/" + recording_file + " ."
    os.system(cmd)


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


def transcribe_audio(recording_file):
    """ Transcribes the given audio file using the Google Cloud Speech API. """

    speech_client = speech.Client()

    with io.open(recording_file, "rb") as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content=content,
            source_uri=None,
            encoding="LINEAR16",
            sample_rate_hertz=16000)

    alternatives = audio_sample.recognize("en-US")
    transcripts = ""

    for alternative in alternatives:
        transcripts = transcripts + alternative.transcript
    return transcripts


def recognise_speech(ip, recording_file):
    copy_audio(ip, recording_file)
    return transcribe_audio(recording_file)


if __name__ == "__main__":
    ip = "146.50.60.43"
    start_time = time.time()
    print transcribe_audio("recording.wav")
    print "total transcript time:", time.time() - start_time
