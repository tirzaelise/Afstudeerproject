# This file creates the list of key words using the database that was created
# from the Absolut Drinks Database. All the information that is in the database
# is added to a list and this list is cleaned by flattening it and removing
# duplicates.

# !/usr/bin/env python2

import collections
import os
import pickle
from pprint import pprint
from PyDictionary import PyDictionary


def generate_keywords(drinks, output_file):
    global dictionary

    dictionary = PyDictionary()
    database = load_database()
    key_words = make_keywords(database, drinks)
    # cleaned_keywords = clean_keywords(key_words)
    # final_keywords = get_synonyms(cleaned_keywords)
    # key_words = encode_keywords(key_words)
    # save_keywords(final_keywords, output_file)
    # print len(final_keywords)


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def make_keywords(database, drinks):
    """
    Creates a dictionary of key words using the drinks database using the name,
    colour, required skill level, whether it's alcoholic, whether it's
    carbonated, whether it's hot, ingredients, tastes, occasions, tools and
    actions of the drink.
    """

    key_words = {}

    for item in drinks:
        property_dict = {}
        name, colour, skill_level, alcoholic, carbonated, hot, ingredients, \
            tastes, occasions, tools, actions = get_properties(item, database)

        ingredients = only_ingredients(ingredients)
        tastes, occasions, tools, actions = split_lists(tastes, occasions,
                                                        tools, actions)

        update_dictionary(property_dict, ingredients)
        update_dictionary(property_dict, tastes)
        update_dictionary(property_dict, occasions)
        update_dictionary(property_dict, tools)
        update_dictionary(property_dict, actions)

        property_dict.update({colour: colour})
        property_dict.update({skill_level: skill_level})
        property_dict.update({alcoholic: alcoholic})
        property_dict.update({carbonated: carbonated})
        property_dict.update({hot: hot})

        key_words.update({name: property_dict})
        print len(property_dict)
    return key_words


def get_properties(item, database):
    """ Returns the properties of a drink. """

    drink = database.get(item)
    return drink[0], drink[2], drink[3], drink[4], drink[5], drink[6], \
        drink[7], drink[8], drink[9], drink[10], drink[11]


def only_ingredients(ingredients):
    """
    Removes the measurements from the ingredients such that "1/2 part lime"
    becomes "lime".
    """

    new_ingredients = []

    for ingredient in ingredients.split(", "):
        new_ingredient = remove_measurements(ingredient)
        new_ingredients.append(new_ingredient)
    return new_ingredients


def remove_measurements(string):
    """
    Removes the measurements from one ingredient. The words in an ingredient are
    always separated by a space. This is done by checking if the first letter of
    a word is a letter. If it is not, the first two elements in the ingredient
    are deleted.
    """

    split_string = string.split(" ")

    if not split_string[0].isalpha():
        del split_string[0]
        del split_string[0]
    return split_string


def split_lists(tastes, occasions, tools, actions):
    """ Returns the strings as lists. """

    tastes = split_string(tastes)
    occasions = split_string(occasions)
    occasions = clean_occasions(occasions)
    tools = split_string(tools)
    actions = split_string(actions)
    return tastes, occasions, tools, actions

def split_string(string):
    """
    Use the words in a string to create a list that holds each word as an
    element.
    """

    string_list = []

    for word in string.split(", "):
        string_list.append(word)
    return string_list


def clean_occasions(occasions):
    """ Removes ' drinks' from the occasions. """
    new_occasions = []

    for occasion in occasions:
        occasion = occasion.replace(" drinks", "")
        new_occasions.append(occasion)
    return new_occasions


def update_dictionary(dictionary, word):
    """ Updates the dictionary with the same key and value. """

    if isinstance(word, list):
        for element in word:
            if isinstance(element, list):
                dictionary.update({" ".join(element): " ".join(element)})
                for smaller_element in element:
                    dictionary.update({smaller_element: smaller_element})
                    generate_synonyms(dictionary, smaller_element)
            else:
                dictionary.update({element: element})
                generate_synonyms(dictionary, element)
    else:
        dictionary.update({word: word})
        generate_synonyms(dictionary, word)


def generate_synonyms(dict_to_update, word):
    """
    Generates the synonyms of a word and appends it to the dictionary of key
    words using itself as a key and the word the synonym was generated from as
    value.
    """

    global dictionary

    word = word.encode("utf-8").lower()
    synonyms = dictionary.synonym(word)

    if synonyms:
        for synonym in synonyms:
            dict_to_update.update({synonym: word})


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


def save_keywords(key_words, output_file):
    """ Saves the key words in a Pickle file. """

    pickle.dump(key_words, open(output_file, "wb"))


if __name__ == "__main__":
    # database = load_database()
    # key_words = make_keywords()
    # cleaned_keywords = clean_keywords(key_words)
    # final_keywords = get_synonyms(cleaned_keywords)
    # key_words = encode_keywords(key_words)
    # save_keywords(final_keywords)
    # print len(final_keywords)

    generate_keywords(["martini"], "output.pkl")
