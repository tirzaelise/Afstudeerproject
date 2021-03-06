# !/usr/bin/env python2

import os
import pickle
from pprint import pprint
from random import randint, choice


class Generate(object):

    def __init__(self):
        self.load_templates()


    def load_templates(self):
        """
        Loads the textual templates of questions and saves them in a list.
        """

        self.templates = []

        if os.path.exists("question_templates.txt"):
            for line in open("question_templates.txt", "r"):
                self.templates.append(line.replace("\n", ""))


    def generate_language(self, properties):
        """
        Uses the list of properties to generate a random question using the text
        file of question templates. If there are no more unknown properties,
        then the program can be completed.
        """

        drink_property = self.find_drink_property(properties)

        if drink_property:
            return self.generate_sentence(drink_property)
        else:
            return ""


    def find_drink_property(self, properties):
        """
        Generates two random numbers to get a random property about which there
        is no knowledge yet, which is indicated by 'None'. If there is
        knowledge, then this will either be indicated by 'True' or 'False'. If
        no 'None' is found for 5 times in a row, there is done a check to make
        sure that there are still 'Nones' in the list. Returns a property that
        needs knowledge or nothing if there is no more knowledge to gain.
        """

        split_status = ""
        tries = 0

        while split_status != "None" and tries <= 5:
            random_drink = randint(0, len(properties) - 1)
            random_property = randint(1, len(properties[random_drink]) - 1)
            drink_property = properties[random_drink][random_property]
            split_status = drink_property.split(": ")[1].split(" //")[0]
            tries += 1

        if split_status != "None" and tries > 5:
            drink_property = self.find_first_none(properties)
        return drink_property


    def find_first_none(self, properties):
        """ Finds the first occurrence of 'None' in the list of properties. """

        for drink in properties:
            iterate_drink = iter(drink)
            next(iterate_drink)
            for drink_property in iterate_drink:
                split_property = drink_property.split(": ")[1].split(" //")[0]
                if split_property == "None":
                    return drink_property
        return ""


    def generate_sentence(self, complete_property):
        """
        Uses the found drink property to generate a sentence from one of the
        templates.
        """

        drink_property = complete_property.split(": ")[0]
        property_type = complete_property.split(": ")[1].split("// ")[1]
        template = self.get_template(property_type)
        question = template.replace("{" + property_type + "}", drink_property)
        return self.get_correct_form(question)


    def get_template(self, property_type):
        """
        Retrieves the correct template to ask a question with the found drink
        property and its type.
        """

        valid_templates = [s for s in self.templates if "{" + property_type +
                           "}" in s]
        return choice(valid_templates)


    def get_correct_form(self, template):
        """
        Returns the correct form of a question such that e.g. 'a(n) strainer'
        becomes 'a strainer'.
        """

        if "(" in template and ")" in template:
            index = template.index(")")
            first_letter = template[index+2]
            if self.is_vowel(first_letter):
                template = template.replace("a(n)", "an")
            else:
                template = template.replace("a(n)", "a")
        return template


    def is_vowel(self, letter):
        """ Returns a boolean that indicates whether a letter is a boolean. """

        if letter in ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U"):
            return True
        return False


def load_properties(ordered_drinks):
    properties = []

    if os.path.exists("drinks_properties.pkl"):
        all_properties = pickle.load(open("drinks_properties.pkl", "rb"))

    for drink in ordered_drinks:
        properties.append(all_properties.get(drink))
    return properties


if __name__ == "__main__":
    properties = load_properties(["martini", "margarita", "sangria",
                                  "cosmopolitan", "mojito"])
    generate = Generate()
    generate.generate_language(properties)
