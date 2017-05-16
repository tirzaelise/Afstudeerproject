# !/usr/bin/env python2

# This file creates the drinks database using the Absolut Drinks Database. It
# retrieves all the entries that are in the database and saves them in a
# Pickle file in a Dictionary using the following format:
# {drink name: list of drink properties}.

import drink
import json
import os.path
import cPickle as pickle
import urllib2


def scrape_page(next_url, first_scrape):
    """ Scrapes a web page of the Absolut Drinks Database. """

    url_to_api = "http://addb.absolutdrinks.com"
    api_key = "/?apiKey=4093c8e39ec5436391012017bc354c01"
    url = url_to_api + "/" + "drinks" + api_key

    if next_url:
        url = next_url
    if not next_url and not first_scrape:
        return

    return json.load(urllib2.urlopen(url))


def create_database(data):
    """
    Creates the database and returns the next url to update the database.
    """

    update_database(data, drinks_dict)
    next_url = data.get("next")

    if next_url:
        # Changes the amount of drinks on a page to 1000 instead of 25
        next_url = next_url.replace("pageSize=25", "pageSize=1000")
    return next_url


def update_database(data, drinks_dict):
    """ Updates the database (Dictionary) of drinks. """

    for element in data.get("result"):
        info = get_info(element)
        drinks_dict.update({info[0]: info})


def get_info(drink):
    """
    Retrieves the requested properties of a drink and returns them in a list.
    """

    properties = ["name", "descriptionPlain", "color", "skill", "isAlcoholic",
                  "isCarbonated", "isHot", "ingredients", "tastes", "occasions",
                  "tools", "actions"]
    info = []

    for drink_property in properties:
        property_value = drink.get(drink_property)

        if isinstance(property_value, list):
            property_value = json_to_array(property_value)
        if isinstance(property_value, dict):
            property_value = property_value.get("name").lower()
        if isinstance(property_value, str):
            property_value = property_value.lower()
        if isinstance(property_value, bool):
            property_value = bool_to_str(drink_property, property_value)
        if property_value is None:
            property_value = "none"
        info.append(property_value.lower())
    return info


def json_to_array(json_array):
    """
    Converts a JSON array into a string that only contains the text values in
    lower case.
    """

    array_string = ""

    for element in json_array:
        string = element.get("text")
        string = string.replace("[", "")
        string = string.replace("]", "")

        if len(array_string) == 0:
            array_string = string.lower()
        else:
            array_string = array_string + ", " + string.lower()
    return array_string


def bool_to_str(drink_property, property_value):
    """
    Converts the value of a boolean to a string that holds the information, such
    that "is_carbonated(True)" becomes "carbonated".
    """

    string = ""

    if drink_property == "isAlcoholic":
        if property_value:
            string = "alcoholic"
        else:
            string = "non-alcoholic"
    elif drink_property == "isCarbonated":
        if property_value:
            string = "carbonated"
        else:
            string = "non-carbonated"
    elif drink_property == "isHot":
        if property_value:
            string = "hot"
        else:
            string = "cold"
    return string


def save_database(database):
    """ Saves the database to a Pickle file. """

    pickle.dump(database, open("database.pkl", "wb"))


if __name__ == "__main__":
    next_url = ""
    first_scrape = True
    drinks_dict = {}

    while True:
        data = scrape_page(next_url, first_scrape)
        if data:
            next_url = create_database(data)
            first_scrape = False
        else:
            save_database(drinks_dict)
            break
