# !/usr/bin/env python2


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

    annotated_sentence = annotator.getAnnotations(sentence, dep_parse=True)
    dependency_parse = annotated_sentence["dep_parse"].split("\n")
    found_verbs = annotated_sentence["verbs"]
    return dependency_parse, found_verbs


# Converts a sentence into its logical form.
def convert_sentences(dependency_parse, found_verbs):
    subjects = []
    objects = []
    verbs = []
    negations = []
    logical_sentences = []

    root_verb = get_root_verb(dependency_parse)
    verbs.append(root_verb)
    subjects.append(get_function_word(dependency_parse, root_verb, "nsubj"))
    objects.append(get_function_word(dependency_parse, root_verb, "dobj"))
    negations.append(get_function_word(dependency_parse, root_verb, "neg"))

    for verb in found_verbs:
        if verb == root_verb:
            continue
        else:
            verbs.append(verb)
            subjects.append(get_function_word(dependency_parse, verb, "nsubj"))
            objects.append(get_function_word(dependency_parse, verb, "dobj"))
            negations.append(get_function_word(dependency_parse, verb, "neg"))

    for i in range(0, len(verbs)):
        logical_sentence = get_logical_form(subjects[i], objects[i],
                                                verbs[i], negations[i])
        logical_sentences.append(logical_sentence)
    return logical_sentences


# Returns the root verb of a sentence.
def get_root_verb(sentence):
    for word in sentence:
        function, words = word.split("(")
        if function == "root":
            root_verb = words.split(",")[1].split("-")[0]
    return root_verb.replace(" ", "")


# Returns the word that has the requested function in a sentence.
def get_function_word(sentence, verb, requested_function):
    function_word = None

    for word in sentence:
        function, words = word.split("(")
        if function == requested_function and verb in words:
            function_word = words.split(",")[1].split("-")[0].replace(" ", "")
    return function_word


# Returns the logical form of a natural sentence.
def get_logical_form(subject, s_object, verb, negation):
    if negation:
        if s_object:
            form = verb + "(" + negation +  ", " + subject + ", " + s_object + \
            ")"
        else:
            form = verb + "(" + negation +  ", " + subject + ")"
    else:
        if s_object:
            form = verb + "(" + subject + ", " + s_object + ")"
        else:
            form = verb + "(" + subject + ")"
    return form


# # Retrieves the interesting roles in a sentence.
# def label_sentence(annotated_sentence):
#     logical_forms = []
#
#     for sentence in annotated_sentence["srl"]:
#         print sentence
#         verb = sentence.get("V")
#         s_subject = sentence.get("A0")
#         s_object = sentence.get("A1")
#         negation = sentence.get("AM-NEG")
#         logical_form = logical_sentence(verb, s_subject, s_object, negation)
#         logical_forms.append(logical_form)
#     return logical_forms


# # Converts a sentence into its logical form.
# def logical_sentence(verb, s_subject, s_object, negation):
#     if len(s_object.split(" ")) > 1:
#         s_object = s_object.split(" ")[-1]
#
#     if len(s_subject.split(" ")) > 1:
#         s_subject = s_subject.split(" ")[-1]
#
#     if negation:
#         sentence = verb + "(" + negation +  ", " + s_subject + ", " + s_object + ")"
#     else:
#         sentence = verb + "(" + s_subject + ", " + s_object + ")"
#     return sentence


if __name__ == "__main__":
    database = load_database()

    if database:
        print "Database loaded successfully"
    else:
        print "Database failed to loaded"
    print

    sentence = "I do not have any lemons. Would you like a different drink?"
    dependency_parse, verbs = annotate_sentence(sentence)
    print convert_sentences(dependency_parse, verbs)
    sentence = "There are not any lemons. Would you like a different drink?"
    dependency_parse, verbs = annotate_sentence(sentence)
    print convert_sentences(dependency_parse, verbs)
