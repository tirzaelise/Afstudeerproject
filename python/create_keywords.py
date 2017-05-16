# !/usr/bin/env python2

import collections
import os
import pickle
from PyDictionary import PyDictionary


# Loads the database.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


# Creates the list of key words using drinks database using their name,
# description, color, required skill level, ingredients, tastes, occasions,
# tools and actions.
def make_keywords():
    key_words = ["alcoholic", "description", "carbonated", "hot", "cold",
                 "skill", "color", "tastes", "occasions", "tools", "actions"]

    for item in database:
        drink = database.get(item)
        split_name = split_string(drink.name)
        split_description = split_string(drink.description)
        ingredients = only_ingredients(drink.ingredients)

        key_words.append(drink.name)
        key_words.append(split_name)
        key_words.append(split_description)
        key_words.append(drink.color)
        key_words.append(drink.skill)
        key_words.append(ingredients)
        key_words.append(drink.tastes)
        key_words.append(drink.occasions)
        key_words.append(drink.tools)
        key_words.append(drink.actions)
    return key_words


# Use the words in a string to create a list that holds each word as an
# element.
def split_string(string):
    string_list = []

    for word in string.split(" "):
        string_list.append(word)
    return string_list


# Flattens the list of key words, removes duplicates and removes None types.
def clean_keywords(key_words):
    flattened_list = list(flatten(key_words))
    key_words = remove_duplicates(flattened_list)
    return [key_word for key_word in key_words if key_word is not None]


# Removes the measurements from the ingredients such that "1/2 part lime"
# becomes "lime".
def only_ingredients(ingredients):
    new_ingredients = []

    for ingredient in ingredients:
        new_ingredient = remove_measurements(ingredient)
        new_ingredients.append(new_ingredient)
    return new_ingredients


# Removes the measurements from one ingredient. The words in an ingredient are
# always separated by a space. This is done by checking if the first letter of
# a word is a letter. If it is not, the first two elements in the ingredient are
# deleted.
def remove_measurements(string):
    split_string = string.split(" ")

    if not split_string[0].isalpha():
        del split_string[0]
        del split_string[0]
    return split_string


# Flattens a list.
def flatten(unflattened_list):
    for element in unflattened_list:
        if isinstance(element, collections.Iterable) and not \
           isinstance(element, basestring):
            for subelement in flatten(element):
                yield subelement
        else:
            yield element


# Removes the duplicates from a list.
def remove_duplicates(key_words):
    return list(set(key_words))


# Returns all the synonyms of the key words and saves them in a list, including
# the original key words. The synonyms are obtained using PyDictionary.
def get_synonyms(key_words):
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


# Saves the key words in a Pickle file.
def save_keywords(key_words):
    if not os.path.exists("key_words.pkl"):
        pickle.dump(key_words, open("key_words.pkl", "wb"))


if __name__ == "__main__":
    database = load_database()
    key_words = make_keywords()
    cleaned_keywords = clean_keywords(key_words)
    final_keywords = get_synonyms(cleaned_keywords)
    save_keywords(final_keywords)
    print len(final_keywords)
