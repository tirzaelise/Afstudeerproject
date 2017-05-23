# This file creates the list of key words using the database that was created
# from the Absolut Drinks Database. All the information that is in the database
# is added to a list and this list is cleaned by flattening it and removing
# duplicates.

# !/usr/bin/env python2

import collections
import os
import pickle
from PyDictionary import PyDictionary


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def make_keywords():
    """
    Creates the list of key words using drinks database using their name,
    description, color, required skill level, ingredients, tastes, occasions,
    tools and actions.
    """

    key_words = ["alcoholic", "description", "carbonated", "hot", "cold",
                 "skill", "color", "tastes", "occasions", "tools", "actions",
                 "have", "has", "have got", "has got", "own", "owns", "want",
                 "wants", "is", "are", "do", "does", "like", "likes", "hold",
                 "holds", "got", "possess", "possesses"]

    for item in database:
        drink = database.get(item)
        split_name = split_string(drink[0])
        split_description = split_string(drink[1])
        ingredients = only_ingredients(drink[7])

        key_words.append(drink[0])
        key_words.append(split_name)
        key_words.append(split_description)
        key_words.append(drink[2])
        key_words.append(drink[3])
        key_words.append(ingredients)
        key_words.append(drink[8])
        key_words.append(drink[9])
        key_words.append(drink[10])
        key_words.append(drink[11])
    return key_words


def split_string(string):
    """
    Use the words in a string to create a list that holds each word as an
    element.
    """

    string_list = []

    for word in string.split(" "):
        string_list.append(word)
    return string_list


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


def clean_keywords(key_words):
    """
    Flattens the list of key words, removes duplicates, converts unicode types
    to string types and removes None types.
    """

    flattened_list = list(flatten(key_words))
    key_words = remove_duplicates(flattened_list)
    return [key_word for key_word in key_words if key_word is not None]


def flatten(unflattened_list):
    """ Flattens a list. """

    for element in unflattened_list:
        if isinstance(element, collections.Iterable) and not \
           isinstance(element, basestring):
            for subelement in flatten(element):
                yield subelement
        else:
            yield element


def remove_duplicates(key_words):
    """ Removes the duplicates from a list. """
    return list(set(key_words))


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


def get_synonyms(key_words):
    """
    Returns all the synonyms of the key words and saves them in a list, including
    the original key words. The synonyms are obtained using PyDictionary.
    """

    dictionary = PyDictionary()
    final_keywords = []

    for key_word in key_words:
        if key_word:
            key_word = key_word.encode("utf-8").lower()
            final_keywords.append(key_word)
            synonyms = dictionary.synonym(key_word)

            if synonyms:
                for synonym in synonyms:
                    final_keywords.append(synonym.lower())
    return final_keywords


def save_keywords(key_words):
    """ Saves the key words in a Pickle file. """

    pickle.dump(key_words, open("key_words.pkl", "wb"))


if __name__ == "__main__":
    database = load_database()
    key_words = make_keywords()
    cleaned_keywords = clean_keywords(key_words)
    final_keywords = get_synonyms(cleaned_keywords)
    key_words = encode_keywords(key_words)
    save_keywords(final_keywords)
    print len(final_keywords)
