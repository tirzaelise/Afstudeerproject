# !/usr/bin/env python2

# This file creates the list of key words using the database that was created
# from the Absolut Drinks Database. All the information that is in the database
# is added to a dictionary of dictionaries and synonyms are generated of
# the drink's temperature, carbonation, alcohol level, ingredients, tastes,
# occasions, tools and actions. This dictionary is of the following format:
# {drink name: {drink property1: property value1, drink property2: {synonym of
# drink property value2: property value2}}}


from nltk.corpus import wordnet as wn
import os
import pickle
from pprint import pprint


def generate_keywords(drinks):
    """ Generates the key words of a list of drinks. """

    database = load_database()
    properties = load_properties()
    key_words = make_keywords(database, drinks, properties)
    # return make_keywords(database, drinks)
    save_keywords(key_words, "synonyms.pkl")


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def make_keywords(database, drinks, properties):
    """
    Creates a dictionary of key words using the drinks database using the name,
    colour, required skill level, whether it's alcoholic, whether it's
    carbonated, whether it's hot, ingredients, tastes, occasions, tools and
    actions of the drink.
    """

    key_words = {}

    for item in drinks:
        name, color, skill_level, alcoholic, carbonated, hot, ingredients, \
            tastes, occasions, tools, actions = get_properties(item, database)

        ingredients = only_ingredients(ingredients)
        tastes, occasions, tools, actions = split_lists(tastes, occasions,
                                                        tools, actions)

        update_dictionary(key_words, "ingredient", ingredients, properties)
        update_dictionary(key_words, "taste", tastes, properties)
        update_dictionary(key_words, "occasion", occasions, properties)
        update_dictionary(key_words, "tool", tools, properties)
        update_dictionary(key_words, "action", actions, properties)

        key_words.update({"color": color})
        key_words.update({"skill": skill_level})
        key_words.update({"alcoholic": alcoholic})
        key_words.update({"carbonated": carbonated})
        key_words.update({"temperature": hot})

        key_words.update({name: key_words})
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


def update_dictionary(dictionary, key, value, properties):
    """ Updates the dictionary with the same key and value. """

    if isinstance(value, list):
        for element in value:
            if isinstance(element, list):
                dictionary.update({" ".join(element): " ".join(element)})
                for smaller_element in element:
                    dictionary.update({smaller_element: smaller_element})
                    generate_synonyms(dictionary, key, smaller_element,
                                      properties)
            else:
                dictionary.update({element: element})
                generate_synonyms(dictionary, key, element, properties)
    else:
        dictionary.update({value: value})
        generate_synonyms(dictionary, key, value, properties)


def generate_synonyms(dict_to_update, key, word, properties):
    """
    Generates the synonyms of a word and appends it to the dictionary of key
    words using itself as a key and the word the synonym was generated from as
    value.
    """

    pos = properties.get(key)

    word = word.encode("utf-8").lower()
    if wn.morphy(word):
        word = wn.morphy(word)
    synsets = wn.synsets(word, pos=pos)

    if synsets:
        for synset in synsets:
            for lemma in synset.lemma_names():
                lemma = lemma.replace("_", " ")
                dict_to_update.update({lemma: word})


def load_properties():
    """
    Returns a dict that holds a property as key and the desired part of speech
    of the property as a value.
    """

    return {"color": wn.NOUN, "skill": wn.NOUN, "alcoholic": wn.ADJ,
            "carbonation": wn.ADJ,  "temperature": wn.ADJ,
            "ingredient": wn.NOUN, "taste": wn.NOUN, "occasion": wn.NOUN,
            "tool": wn.NOUN, "action": wn.VERB}


def save_keywords(key_words, output_file):
    """ Saves the key words in a Pickle file. """

    pickle.dump(key_words, open(output_file, "wb"))


if __name__ == "__main__":
    generate_keywords(["martini", "margarita"])
