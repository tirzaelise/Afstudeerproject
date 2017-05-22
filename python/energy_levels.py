from naoqi import ALProxy
import os
import pickle
import threading
import time


def init_program(ip):
    key_words = load_keywords()
    key_words = encode_keywords(key_words)
    setup_robot(ip, key_words)


def load_keywords():
    """
    Loads the key words that will be checked for occurrences of words in a
    natural sentence.
    """

    if os.path.exists("key_words.pkl"):
        return pickle.load(open("key_words.pkl", "rb"))


def encode_keywords(key_words):
    """
    Encodes all the unicode type key words to string types so that they
    can be set as vocabulary for ALSpeechRecognition.
    """

    new_keywords = []

    for key_word in key_words:
        if isinstance(key_word, unicode):
            key_word = key_word.encode("ascii", "ignore")
        new_keywords.append(key_word)
    return new_keywords


def setup_robot(ip, key_words):
    global asr
    global aad
    global alm

    asr = ALProxy("ALSpeechRecognition", ip, 9559)
    asr.setLanguage("English")
    start_time = time.time()
    asr.setVocabulary(key_words, True)
    # asr.setVocabulary(key_words, False)
    print "set vocab time:", time.time() - start_time
    asr.setVisualExpression(True)
    asr.setAudioExpression(False)
    aad = ALProxy("ALAudioDevice", ip, 9559)
    aad.enableEnergyComputation()
    alm = ALProxy("ALMemory", ip, 9559)


def measure_average_energy(first_time, baseline):
    global asr
    global aad
    global alm

    end_time = time.time() + 1
    total_front = []
    total_rear = []
    total_left = []
    total_right = []

    while time.time() < end_time:
        total_front.append(aad.getFrontMicEnergy())
        total_rear.append(aad.getRearMicEnergy())
        total_left.append(aad.getLeftMicEnergy())
        total_right.append(aad.getRightMicEnergy())

    average_front = sum(total_front)/float(len(total_front))
    average_rear = sum(total_rear)/float(len(total_rear))
    average_left = sum(total_left)/float(len(total_left))
    average_right = sum(total_right)/float(len(total_right))

    average = (average_front + average_rear + average_left + average_right) / 4

    if first_time:
        baseline = average

    recognized_word = alm.getData("WordRecognized")[0]
    confidence = alm.getData("WordRecognized")[1]
    print alm.getData("WordRecognized")

    thread = threading.Timer(0.2, measure_average_energy, [False, baseline])
    thread.start()

    if baseline * 0.975 <= average <= baseline * 1.025 and not first_time:
        thread.cancel()
        asr.unsubscribe("listen")


if __name__ == "__main__":
    global asr
    ip = "10.42.0.209"


    init_program(ip)
    asr.subscribe("listen")
    measure_average_energy(True, 0)
