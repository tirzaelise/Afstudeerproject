# -*- coding: utf-8 -*-
# !/usr/bin/env python2

# This file creates a list of synonyms using the database that was created
# from the Absolut Drinks Database. All the information that is in the database
# is added to a dictionary and synonyms are generated of
# the drink's temperature, carbonated, alcoholic, ingredients, tastes, tools and
# actions. This dictionary is of the following format:
# {drink name: {synonym 1: known word1, synonym2: known word2}}


from nltk.corpus import wordnet as wn
import os
import pickle


def generate_synonym_dict():
    """ Generates the synonyms of all the drinks in the database. """

    database = load_database()
    properties = load_properties()
    synonyms = make_synonyms(database, properties)
    save_synonyms(synonyms, "drinks_synonyms.pkl")


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def load_properties():
    """
    Returns a dict that holds a property as key and the desired part of speech
    of the property as a value.
    """

    return {"color": wn.NOUN, "alcoholic": wn.ADJ, "carbonation": wn.ADJ,
            "temperature": wn.ADJ, "ingredient": wn.NOUN, "taste": wn.NOUN,
            "tool": wn.NOUN, "action": wn.VERB}


def make_synonyms(database, properties):
    """
    Creates a dictionary of key words using the drinks database using the name,
    colour, whether it's alcoholic, whether it's carbonated, whether it's hot,
    ingredients, tastes, and tools of the drink.
    """

    synonyms_dict = {}

    for item in database:
        synonyms = {}
        name, color, alcoholic, carbonated, hot, ingredients, tastes, tools, \
            actions = get_properties(item, database)

        ingredients = only_ingredients(ingredients)
        tastes, tools, actions = split_lists(tastes, tools, actions)

        update_dictionary(synonyms, "ingredient", ingredients, properties)
        update_dictionary(synonyms, "taste", tastes, properties)
        update_dictionary(synonyms, "tool", tools, properties)
        update_dictionary(synonyms, "action", actions, properties)

        synonyms.update({"color": color})
        synonyms.update({"alcoholic": alcoholic})
        synonyms.update({"carbonated": carbonated})
        synonyms.update({"temperature": hot})

        synonyms_dict.update({name: synonyms})
    return synonyms_dict


def get_properties(item, database):
    """ Returns the properties of a drink. """

    drink = database.get(item)
    return drink[0], drink[1], drink[2], drink[3], drink[4], drink[5], \
        drink[6], drink[7], drink[8]


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


def split_lists(tastes, tools, actions):
    """ Returns the strings as lists. """

    tastes = split_string(tastes)
    tools = split_string(tools)
    actions = split_string(actions)
    return tastes, tools, actions


def split_string(string):
    """
    Uses the words in a string to create a list that holds each word as an
    element.
    """

    string_list = []

    for word in string.split(", "):
        string_list.append(word)
    return string_list


def update_dictionary(dictionary, key, value, properties):
    """ Updates the dictionary with the appropriate key and value. """

    if isinstance(value, list):
        for element in value:
            if isinstance(element, list):
                dictionary.update({" ".join(element): " ".join(element)})
                for smaller_element in element:
                    dictionary.update({smaller_element: smaller_element})
                    get_synonyms(dictionary, key, smaller_element,
                                 properties)
            else:
                dictionary.update({element: element})
                get_synonyms(dictionary, key, element, properties)
    else:
        dictionary.update({value: value})
        get_synonyms(dictionary, key, value, properties)


def get_synonyms(dict_to_update, key, word, properties):
    """
    Generates the synonyms of a word and appends it to the dictionary of
    synonyms using itself as a key and the word the synonym was generated from
    as value.
    """

    pos = properties.get(key)

    word = word.encode("utf-8").lower()
    word = word.decode("utf-8")

    if wn.morphy(word):
        word = wn.morphy(word)
    synsets = wn.synsets(word, pos=pos)

    if synsets:
        for synset in synsets:
            for lemma in synset.lemma_names():
                lemma = lemma.replace("_", " ")
                dict_to_update.update({lemma: word})


def save_synonyms(synonyms, output_file):
    """ Saves the synonyms in a Pickle file. """

    pickle.dump(synonyms, open(output_file, "wb"))


if __name__ == "__main__":
    generate_synonym_dict()
