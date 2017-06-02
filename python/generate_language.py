# !/usr/bin/env python2

import os
import pickle
from random import randint


class Generate(object):

    def __init__(self):
        self.load_templates()


    def load_templates(self):
        """
        Loads the textual templates of questions and saves them in a list.
        """

        self.templates = []

        if os.path.exists("templates.txt"):
            for line in open("templates.txt", "r"):
                self.templates.append(line.replace("\n", ""))


    def generate_sentence(self, properties):
        """
        Generates two random numbers to get a random property about which there
        is no knowledge yet, which is indicated by 'None'. If there is
        knowledge, then this will either be indicated by 'True' or 'False'. If
        no 'None' is found for 5 times in a row, there is done a check to make
        sure that there are still 'Nones' in the list.
        """

        split_property = ""
        tries = 0

        while split_property != "None" and tries <= 5:
            random_drink = randint(0, len(properties) - 1)
            random_property = randint(0, len(properties[random_drink]) -1 )
            drink_property = properties[random_drink][random_property]
            split_property = drink_property.split(": ")[1]
            tries += 1

        drink_property = find_first_none(properties)
        if not drink_property:
            # Program has finished/info about every property has been obtained


    def find_first_none(self, properties):
        """ Finds the first occurrence of 'None' in the list of properties. """

        for drink in properties:
            iterate_drink = iter(drink)
            next(iterate_drink)
            for drink_property in iterate_drink:
                split_property = drink_property.split(": ")
                if split_property[1] == "None":
                    return split_property[0]
        return ""


def load_properties(ordered_drinks):
    properties = []

    if os.path.exists("drinks_properties.pkl"):
        all_properties = pickle.load(open("drinks_properties.pkl", "rb"))

    for drink in ordered_drinks:
        properties.append(all_properties.get(drink))
    return properties


if __name__ == "__main__":
    properties = load_properties(["martini", "margarita", "bloody mary"])
    generate = Generate()
    generate.generate_sentence(properties)
