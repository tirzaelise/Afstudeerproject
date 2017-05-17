# !/usr/bin/env python2

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.parse.stanford import StanfordDependencyParser
import os
import pickle
from pprint import pprint
import time


def load_database():
    """ Loads the database of drinks, which is a Python Dictionary. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def load_parser():
    """ Loads the Stanford Dependency Parser to parse sentences. """

    jar_path = "stanford-parser-full-2016-10-31/stanford-parser.jar"
    models_path = "stanford-parser-full-2016-10-31/stanford-parser-" + \
        "3.7.0-models.jar"
    return StanfordDependencyParser(path_to_jar=jar_path,
                                    path_to_models_jar=models_path)


def load_keywords():
    """
    Loads the key words that will be checked for occurrences of words in a
    natural sentence.
    """

    if os.path.exists("key_words.pkl"):
        return pickle.load(open("key_words.pkl", "rb"))


def load_properties():
    return {"drink": wn.NOUN, "color": wn.NOUN, "skill": wn.NOUN,
            "alcoholic": wn.ADJ, "non-alcoholic": wn.ADJ, "carbonated": wn.ADJ,
            "non-carbonated": wn.ADJ, "hot": wn.ADJ, "cold": wn.ADJ,
            "ingredient": wn.NOUN, "taste": wn.NOUN, "occasion": wn.NOUN,
            "tool": wn.NOUN, "action": wn.VERB}


def parse_sentence(parser, sentence):
    """ Uses the Stanford Dependency Parser to parse a sentence. """

    result = parser.raw_parse(sentence)
    dep = result.next()
    return list(dep.triples())


def get_verbs(sentence):
    """ Returns all the verbs in a sentence. """

    verbs = []
    tokenized_sentence = word_tokenize(sentence)
    tagged_sentence = pos_tag(tokenized_sentence)

    for word in tagged_sentence:
        if word[1].startswith("VB"):
            verbs.append(word[0])
    return verbs


def analyse_sentence(verbs, sentence):
    """ Analyses a sentence: returns the subject, verb and object. """

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


def get_function_word(sentence, verb, requested_function):
    """ Returns the word that has the requested function in a sentence. """

    function_word = None

    for word in sentence:
        if word[1] == requested_function and word[0][0] == verb:
            if requested_function == "neg":
                function_word = "not"
            else:
                function_word = word[2][0]
    return function_word


def correct_functions(verbs, subjects, objects, negations):
    """
    Corrects sentences such that verbs that do not have a subject are omitted.
    """

    i = 0

    for subject in subjects:
        if not subject:
            del verbs[i]
            del subjects[i]
            del objects[i]
            del negations[i]
        i += 1
    return verbs, subjects, objects, negations


def ask_clarification(verb, subject, s_object, negation, key_words, possessive):
    """
    Checks if the found verbs, subjects and objects are in the key words. If
    they are, the list of ordered drinks is updated with the new information. If
    they aren't, the robot asks for clarification.
    """

    unknown_words = check_keywords(verb, subject, s_object, key_words)
    if possessive:
        drink_property = find_drink_property(s_object, "n")
        clarification = understood(s_object, drink_property, negation)
    else:
        drink_property = find_drink_property(verb, "v")
        clarification = understood(verb, drink_property, negation)
    print clarification
    return clarification


def check_keywords(verb, subject, s_object, key_words):
    """
    Checks if the found verb, subject and object are in the list of key words.
    Returns a list that contains the words that were not found in the key
    words.
    """

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


def misunderstood(unknown_words):
    """
    Returns a sentence that asks for clarification given the words in the
    sentence that were not understood, because they are not in the list of key
    words.
    """

    variable_words = ", ".join(unknown_words)
    request = " Please describe your response differently."

    if len(unknown_words) > 1:
        k = variable_words.rfind(", ")
        variable_words = variable_words[:k] + " and" + variable_words[k+1:]
        clarification = "I did not understand the words " + variable_words + "."
    else:
        clarification = "I did not understand the word " + variable_words + "."
    return clarification + request


def find_drink_property(word, pos):
    """
    Finds the drink property that has the shortest distance to a common hypernym
    between a drink property and a word.
    """

    highest_similarity = 0

    for drink_property in properties:
        property_pos = properties.get(drink_property)
        property_synsets = wn.synsets(drink_property, pos=property_pos)
        word_synsets = wn.synsets(word, pos=pos)
        property_syn, word_syn, similarity = find_best_synset(property_synsets,
                                                            word_synsets)

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_property = drink_property
    return best_property


def find_best_synset(synsets_1, synsets_2):
    """
    Uses the Wu-Palmer similarity to find the two synsets that are likely the
    best options for two words.
    """

    highest_similarity = 0
    best_synset_1 = ""
    best_synset_2 = ""

    for synset_1 in synsets_1:
        for synset_2 in synsets_2:
            similarity = synset_1.wup_similarity(synset_2)
            if similarity is None:
                similarity = 0
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_synset_1 = synset_1
                best_synset_2 = synset_2
    return best_synset_1, best_synset_2, highest_similarity


def understood(word, drink_property, negation):
    """
    Uses the most similar drink property to generate a response to the natural
    sentence that was spoken.
    """

    vowels = ("a", "e", "i", "o", "u")
    property_pos = properties.get(drink_property)
    start_of_sentence = "I understand you"
    end_of_sentence = ". Is this correct?"
    verb = " have "
    verb_compound = " got "
    property_as = " as a "

    if not negation:
        negation = ""

    if property_pos == wn.VERB:
        verb = " can "
        verb_compound = " "

    if drink_property.startswith(vowels):
        property_as = " as an "


    return start_of_sentence + verb + negation + verb_compound + word + \
           property_as + drink_property + end_of_sentence


def speak(string):
    """ Makes the robot say a string. """

    string


def ask_confirmation():
    """
    Asks for confirmation from the person the robot is talking to based on the
    question that was asked and performs an action accordingly.
    """

    confirmed = True
    return confirmed


def is_possessive(verb):
    """
    Returns a boolean that indicates whether a verb expresses possession.
    """

    possesive = ("has", "have", "possess", "own", "has got", "have got", "hold")

    return any(verb in string for string in possesive)



def update_drinks(database, drinks, word, negation):
    """
    Updates the list of ordered drinks.
    """

    for drink in ordered_drinks:
        properties = database.get(drink)
        if negation and substring_in_list(word, properties):
            drinks.remove(drink)
    return drinks


def substring_in_list(substring, l_ist):
    """
    Returns a boolean that indicates whether a substring can be found in a list.
    """

    substring_list = [s for s in l_ist if substring in s]
    if len(substring_list) > 0:
        return True
    return False


if __name__ == "__main__":
    ordered_drinks = ["martini"]
    available_drinks = ordered_drinks
    sentence = "I have got no lemons."

    database = load_database()
    parser = load_parser()
    key_words = load_keywords()
    properties = load_properties()
    parsed_sentence = parse_sentence(parser, sentence)
    verbs = get_verbs(sentence)
    verbs, subjects, objects, negations = analyse_sentence(verbs,
                                                           parsed_sentence)

    for i in range(0, len(verbs)):
        if is_possessive(verbs[i]):
            clarification = ask_clarification(verbs[i], subjects[i], objects[i],
                                              negations[i], key_words, True)
        else:
            clarification = ask_clarification(verbs[i], subjects[i], objects[i],
                                              negations[i], key_words, False)
        speak(clarification)
        confirmed = ask_confirmation()
        if confirmed:
            if is_possessive(verbs[i]):
                update_drinks(database, available_drinks, objects[i],
                              negations[i])
            else:
                update_drinks(database, available_drinks, verbs[i], negations[i])
        else:
            speak("Please describe what you mean differently.")
    print available_drinks
