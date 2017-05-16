# !/usr/bin/env python2

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordDependencyParser
import os
import pickle
from pprint import pprint
import time


# Loads the database of drinks, which is a Python Dictionary.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


# Loads the Stanford Dependency Parser to parse sentences.
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


# Checks if the found verbs, subjects and objects are in the key words. If they
# are, the list of ordered drinks is updated with the new information. If they
# aren't, the robot asks for clarification.
def do_action(verbs, subjects, objects, negations, key_words, ordered_drinks):
    for i in range(0, len(verbs)):
        unknown_words = check_keywords(verbs[i], subjects[i], objects[i],
                                       key_words)
        # if len(unknown_words) != 0:
        #     clarification = ask_clarification(unknown_words)
        #     print clarification
        # else:
        update_database(verbs[i], subjects[i], objects[i], negations[i],
                        ordered_drinks)


# Checks if the found verb, subject and object are in the list of key words.
# Returns a list that contains the words that were not found in the key
# words.
def check_keywords(verb, subject, s_object, key_words):
    unknown_words = []

    if verb:
        if verb.encode("utf-8") not in key_words:
            unknown_words.append(verb)
    if subject:
        if subject.encode("utf-8") not in key_words:
            unknown_words.append(subject)
    if s_object:
        if s_object.encode("utf-8") not in key_words:
            unknown_words.append(s_object)
    return unknown_words


# Returns a sentence that asks for clarification given the words in the
# sentence that were not understood, because they are not in the list of key
# words.
def ask_clarification(unknown_words):
    variable_words = ", ".join(unknown_words)

    if len(unknown_words) > 1:
        k = variable_words.rfind(", ")
        variable_words = variable_words[:k] + " and" + variable_words[k+1:]
        clarification = "I did not understand the words " + variable_words + "."
    else:
        clarification = "I did not understand the word " + variable_words + "."
    return clarification


# Uses the verb, subject, object and optional negation that were obtained from
# a natural language sentence to update the list of ordered drinks.
def update_database(verb, subject, s_object, negation, ordered_drinks):
    for drink in ordered_drinks:
        drink_properties = database.get(drink)

        # if substring_in_list(s_object, drink_properties):
        find_closest_hypernym(s_object, drink_properties)


# Returns a boolean that indicates whether a substring can be found in a list.
def substring_in_list(substring, l_ist):
    new_list = [s for s in l_ist if substring in s]
    if len(new_list) > 0:
        return True
    return False


# Finds the drink property that has the shortest distance to a common hypernym
# between a drink property and a word.
def find_closest_hypernym(word, drink_properties):
    shortest_distance = 1000

    for drink_property in drink_properties:
        property_synsets = wn.synsets(drink_property)
        word_synsets = wn.synsets(word)
        property_syn, word_syn, distance = find_best_synset(property_synsets,
                                                            word_synsets)
        if distance < shortest_distance:
            shortest_distance = distance
            best_property = drink_property
    print shortest_distance, best_property


def find_best_synset(synsets_1, synsets_2):
    shortest_distance = 1000
    best_synset_1 = ""
    best_synset_2 = ""

    for synset_1 in synsets_1:
        for synset_2 in synsets_2:
            current_distance = synset_1.shortest_path_distance(synset_2)
            if current_distance is None:
                current_distance = 1000
            if current_distance < shortest_distance:
                shortest_distance = current_distance
                best_synset_1 = synset_1
                best_synset_2 = synset_2
    return best_synset_1, best_synset_2, shortest_distance


if __name__ == "__main__":
    ordered_drinks = ["martini"]
    sentence = "I don't have any gin."

    database = load_database()
    parser = load_parser()
    key_words = load_keywords()
    parsed_sentence = parse_sentence(parser, sentence)
    verbs = get_verbs(sentence)
    verbs, subjects, objects, negations = analyse_sentence(verbs,
                                                           parsed_sentence)
    do_action(verbs, subjects, objects, negations, key_words, ordered_drinks)
