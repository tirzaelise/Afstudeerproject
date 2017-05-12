# !/usr/bin/env python2

from nltk import word_tokenize, pos_tag
from nltk.parse.stanford import StanfordDependencyParser
import os
import pickle
from pprint import pprint
import time


# Loads the database.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


# Loads the Stanford Dependency Parser.
def load_parser():
    jar_path = "stanford-parser-full-2016-10-31/stanford-parser.jar"
    models_path = "stanford-parser-full-2016-10-31/stanford-parser-" + \
        "3.7.0-models.jar"
    return StanfordDependencyParser(path_to_jar=jar_path,
                                    path_to_models_jar=models_path)


# Loads the key words that will be checked for occurrences of words in a natural
# sentence.
def load_keywords():
    if os.path.exists("key_words.pkl"):
        return pickle.load(open("key_words.pkl", "rb"))


# Uses the Stanford Dependency Parser to parse a sentence.
def parse_sentence(parser, sentence):
    result = parser.raw_parse(sentence)
    dep = result.next()
    return list(dep.triples())


# Returns all the verbs in a sentence.
def get_verbs(sentence):
    verbs = []
    tokenized_sentence = word_tokenize(sentence)
    tagged_sentence = pos_tag(tokenized_sentence)

    for word in tagged_sentence:
        if word[1].startswith("VB"):
            verbs.append(word[0])
    return verbs


# Analyses a sentence: returns the subject, verb and object.
def analyse_sentence(verbs, sentence):
    subjects = []
    objects = []
    negations = []

    for verb in verbs:
        subjects.append(get_function_word(sentence, verb, "nsubj"))
        objects.append(get_function_word(sentence, verb, "dobj"))
        negations.append(get_function_word(sentence, verb, "neg"))
    verbs, subjects, objects, negations = correct_functions(verbs, subjects,
                                                            objects, negations)
    return verbs, subjects, objects, negations


# Returns the word that has the requested function in a sentence.
def get_function_word(sentence, verb, requested_function):
    function_word = None

    for word in sentence:
        if word[1] == requested_function and word[0][0] == verb:
            if requested_function == "neg":
                function_word = "not"
            else:
                function_word = word[2][0]
    return function_word


# Sometimes a verb, that does not have a subject, is found. A sentence needs to
# have both a subject and a verb in order to form a sentence so then that verb
# can be omitted.
def correct_functions(verbs, subjects, objects, negations):
    i = 0

    for subject in subjects:
        if not subject:
            del verbs[i]
            del subjects[i]
            del objects[i]
            del negations[i]
        i += 1
    return verbs, subjects, objects, negations


# Checks if the found verbs, subjects and objects are in the key words and does
# an action accordingly.
def check_keywords(verbs, subjects, objects, key_words):
    unknown_functions = []

    for i in range(0, len(verbs)):
        if verbs[i]:
            if verbs[i].encode("utf-8") not in key_words:
                unknown_functions.append("verb")
        if subjects[i]:
            if subjects[i].encode("utf-8") not in key_words:
                unknown_functions.append("subject")
        if objects[i]:
            if objects[i].encode("utf-8") not in key_words:
                unknown_functions.append("object")
        if len(unknown_functions) != 0:
            print ask_clarification(unknown_functions)


# Returns a sentence that asks for clarification given the functions in the
# sentence that were not understood.
def ask_clarification(unknown_functions):
    variable_functions = ", ".join(unknown_functions)

    if len(unknown_functions) > 1:
        k = variable_functions.rfind(", ")
        variable_functions = variable_functions[:k] + " and" + \
                             variable_functions[k+1:]
    clarification = "I did not understand the " + variable_functions + " in" + \
                    " your sentence."
    return clarification


# Returns the logical form of a sentence using a verb, subject, object and
# negation.
def get_logical_form(verbs, subjects, objects, negations):
    logical_forms = []

    for i in range(0, len(subjects)):
        logical_forms.append(natural_to_logic(verbs[i], subjects[i], objects[i],
                             negations[i]))
    return logical_forms


# Uses a verb, subject, object and negation to create a logical form of a
# natural sentence. This is done with the knowledge that a sentence is only a
# sentence if it has a verb and a subject.
def natural_to_logic(verb, subject, s_object, negation):
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


if __name__ == "__main__":
    # start_time = time.time()
    sentence = "Do you have a lemon for me?"

    database = load_database()
    # print "Database:", time.time() - start_time
    # start_time = time.time()
    parser = load_parser()
    # print "Parser:", time.time() - start_time
    # start_time = time.time()
    key_words = load_keywords()
    # print "Key words:", time.time() - start_time
    # start_time = time.time()
    parsed_sentence = parse_sentence(parser, sentence)
    # print "Parse sentence:", time.time() - start_time
    # start_time = time.time()
    verbs = get_verbs(sentence)
    # print "Verbs:", time.time() - start_time
    # start_time = time.time()
    verbs, subjects, objects, negations = analyse_sentence(verbs,
                                                           parsed_sentence)
    # print "Analyse sentence:", time.time() - start_time
    # start_time = time.time()
    check_keywords(verbs, subjects, objects, key_words)
    # print "Check keywords:", time.time() - start_time
    # start_time = time.time()
    logical_forms =  get_logical_form(verbs, subjects, objects, negations)
    # print "Logical forms:", time.time() - start_time
    print logical_forms
