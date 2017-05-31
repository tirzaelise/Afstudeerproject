# !/usr/bin/env python2

import os
import pickle


def generate_property_list(drinks):
    database = load_database()
    drink_list = create_drink_list(database, drinks)
    # return create_drink_list(database, drinks)
    save_properties(drink_list, "property_list.pkl")


def load_database():
    """ Loads the database. """

    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


def create_drink_list(database, drinks):
    """
    Generates the list of all the properties of the drinks that were ordered
    using the database.
    """

    all_properties = []

    for drink in drinks:
        drink_list = []

        name, color, skill_level, alcoholic, carbonated, hot, ingredients, \
            tastes, occasions, tools, actions = get_properties(drink, database)
        ingredients = only_ingredients(ingredients)
        tastes, occasions, tools, actions = split_lists(tastes, occasions,
                                                        tools, actions)

        drink_list.append(name + ": None")
        drink_list.append(color + ": None")
        drink_list.append(skill_level + ": None")
        drink_list.append(alcoholic + ": None")
        drink_list.append(carbonated + ": None")
        drink_list.append(hot + ": None")
        drink_list = append_list(ingredients, drink_list)
        drink_list = append_list(tastes, drink_list)
        drink_list = append_list(occasions, drink_list)
        drink_list = append_list(tools, drink_list)
        drink_list = append_list(actions, drink_list)
        all_properties.append(drink_list)
    return all_properties


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
    generate_property_list(["martini", "margarita"])
