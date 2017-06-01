# !/usr/bin/env python2

# This file generates the properties of all the drinks in the database, which
# were obtained using the Absolut Drinks Database. For each drink in the
# database, the properties are saved in a list followed by ": None" so as to
# indicate that there is no knowledge about whether this property is available
# or not. This information is saved in a dictionary such that {drink name 1:
# [property1: None, property2: None, etc]}. 

import os
import pickle


def generate_property_dict():
    """ Generates the dictionary of drinks properties. """

    database = load_database()
    properties = create_drink_dict(database)
    pprint(properties)
    save_properties(properties, "drinks_properties.pkl")


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def create_drink_dict(database):
    """
    Generates the properties, saved in a list, of all the drinks in the database
    and saves them in a dictionary.
    """

    properties_dict = {}

    for item in database:
        drink_properties = []

        name, color, skill_level, alcoholic, carbonated, hot, ingredients, \
            tastes, occasions, tools, actions = get_properties(item, database)
        ingredients = only_ingredients(ingredients)
        tastes, occasions, tools, actions = split_lists(tastes, occasions,
                                                        tools, actions)

        drink_properties.append(name + ": None")
        drink_properties.append(color + ": None")
        drink_properties.append(skill_level + ": None")
        drink_properties.append(alcoholic + ": None")
        drink_properties.append(carbonated + ": None")
        drink_properties.append(hot + ": None")
        drink_properties = append_list(ingredients, drink_properties)
        drink_properties = append_list(tastes, drink_properties)
        drink_properties = append_list(occasions, drink_properties)
        drink_properties = append_list(tools, drink_properties)
        drink_properties = append_list(actions, drink_properties)
        properties_dict.update({name: drink_properties})
    return properties_dict


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
    return " ".join(split_string)


def split_lists(tastes, occasions, tools, actions):
    """ Returns the strings as lists. """

    tastes = split_string(tastes)
    occasions = split_string(occasions)
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


def append_list(unappended_list, list_to_append):
    """
    Appends all items in a list to a different list and adds ': None' to each
    element.
    """

    for element in unappended_list:
        list_to_append.append(element + ": None")
    return list_to_append


def save_properties(properties, output_file):
    """ Saves the properties in a Pickle file. """

    pickle.dump(properties, open(output_file, "wb"))

if __name__ == "__main__":
    generate_property_dict()