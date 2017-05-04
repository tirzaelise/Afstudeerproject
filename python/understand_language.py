import nltk
import os
import pickle
from practnlptools.tools import Annotator
from pprint import pprint


# Loads the database.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


# Annotates a sentence.
def annotate_sentence(sentence):
    annotator = Annotator()
    annotated_sentence = annotator.getAnnotations(sentence)
    return label_sentence(annotated_sentence)


# Retrieves the interesting roles in a sentence.
def label_sentence(annotated_sentence):
    logical_forms = []

    for sentence in annotated_sentence["srl"]:
        verb = sentence.get("V")
        s_subject = sentence.get("A0")
        s_object = sentence.get("A1")
        negation = sentence.get("AM-NEG")
        logical_form = logical_sentence(verb, s_subject, s_object, negation)
        logical_forms.append(logical_form)
    return logical_forms


# Converts a sentence into its logical form.
def logical_sentence(verb, s_subject, s_object, negation):
    if len(s_object.split(" ")) > 1:
        s_object = s_object.split(" ")[-1]

    if len(s_subject.split(" ")) > 1:
        s_subject = s_subject.split(" ")[-1]

    if negation:
        sentence = verb + "(" + negation +  ", " + s_subject + ", " + s_object + ")"
    else:
        sentence = verb + "(" + s_subject + ", " + s_object + ")"
    return sentence


if __name__ == "__main__":
    database = load_database()

    if database:
        print "Database loaded successfully"
    else:
        print "Database failed to loaded"
    print

    sentence = "I do not have any lemons, but I would like avocados."
    logical_sentences = annotate_sentence(sentence)
    print logical_sentences
