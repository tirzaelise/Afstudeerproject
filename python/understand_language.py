# !/usr/bin/env python2

# This file uses a sentence to try to update the list of drinks that were
# ordered in order to find out what drinks are available. This is done by taking
# the verb, object and negation of a sentence (if available).


import collections
import itertools
from itertools import repeat
from naoqi import ALProxy
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.parse.stanford import StanfordDependencyParser
import os
import pickle
from pprint import pprint
import time


class Understand(object):

    def __init__(self, ordered_drinks):
        self.ordered_drinks = ordered_drinks
        self.available_drinks = self.ordered_drinks
        self.setup_program()


    def setup_program(self):
        """
        Sets up the program by loading the database, parser, key words and
        drink properties and by setting up the robot.
        """

        self.load_database()
        self.load_parser()
        self.load_synonyms(self.ordered_drinks)
        self.load_pos_tags()
        self.load_properties()


    def load_database(self):
        """ Loads the database of drinks, which is a Python Dictionary. """

        if os.path.exists("database.pkl"):
            self.database = pickle.load(open("database.pkl", "rb"))


    def load_parser(self):
        """ Loads the Stanford Dependency Parser to parse sentences. """

        jar_path = "stanford-parser-full-2016-10-31/stanford-parser.jar"
        models_path = "stanford-parser-full-2016-10-31/stanford-parser-" + \
                      "3.7.0-models.jar"
        self.parser = StanfordDependencyParser(path_to_jar=jar_path,
                                               path_to_models_jar=models_path)


    def load_synonyms(self, drinks):
        """
        Loads the key words that will be checked for occurrences of words in a
        natural sentence.
        """

        self.synonyms = {}

        if os.path.exists("drinks_synonyms.pkl"):
            all_synonyms = pickle.load(open("drinks_synonyms.pkl", "rb"))

        for drink in drinks:
            drink_synonyms = all_synonyms.get(drink)
            for synonym, word in drink_synonyms.iteritems():
                if word in self.synonyms and word == self.synonyms.get(word):
                    ab = 4
                else:
                    self.synonyms.update({synonym: word})


    def load_pos_tags(self):
        """ Loads the POS tags of the properties. """

        self.pos_tags = {"drink": wn.NOUN, "color": wn.NOUN, "skill": wn.NOUN,
                         "alcoholic": wn.ADJ, "non-alcoholic": wn.ADJ,
                         "carbonated": wn.ADJ, "non-carbonated": wn.ADJ,
                         "hot": wn.ADJ, "cold": wn.ADJ, "ingredient": wn.NOUN,
                         "taste": wn.NOUN, "tool": wn.NOUN, "action": wn.VERB}


    def load_properties(self):
        """ Loads the lists of properties of the ordered drinks. """

        self.properties = []

        if os.path.exists("drinks_properties.pkl"):
            all_properties = pickle.load(open("drinks_properties.pkl", "rb"))

        for drink in self.ordered_drinks:
            self.properties.append(all_properties.get(drink))


    def understand_sentence(self, question, answer):
        """
        Uses the main verb, object and negation of a sentence to 'understand' it
        and updates the database with it.
        """

        parsed_answer = self.parse_sentence(answer)
        answer_verbs = self.get_verbs(answer, parsed_answer)

        if self.is_empty_answer(parsed_answer, answer_verbs):
            # Use question's verbs and objects, but answer's negation
            parsed_question = self.parse_sentence(question)
            question_verbs = self.get_verbs(question, parsed_question)
            v, o, n = self.analyse_empty_sentence(answer, parsed_answer,
                                                  parsed_question, answer_verbs,
                                                  question_verbs)
        else:
            v, o, n = self.analyse_sentence(answer_verbs, parsed_answer, False,
                                            "")
        return self.apply_sentence(v, o, n)


    def parse_sentence(self, sentence):
        """ Uses the Stanford Dependency Parser to parse a sentence. """

        result = self.parser.raw_parse(sentence)
        dep = result.next()
        return list(dep.triples())


    def get_verbs(self, sentence, parsed_sentence):
        """ Returns all the verbs in a sentence. """

        verbs = []
        tokenized_sentence = word_tokenize(sentence)
        tagged_sentence = pos_tag(tokenized_sentence)

        for word in tagged_sentence:
            if word[1].startswith("VB") and not \
               self.is_auxiliary(parsed_sentence, word[0]):
                verbs.append([word[0]])

        verbs = self.check_verbs(verbs, parsed_sentence)

        if not verbs and ("can" and "MD" in element for element in
            tagged_sentence):
            verbs.append(["can"])

        return verbs


    def is_auxiliary(self, parsed_sentence, verb):
        """
        An auxiliary of a clause is a non-main verb of the clause, e.g., a
        modal auxiliary, or a form of 'be', 'do' or 'have' in a periphrastic
        tense. The parser incorrectly ascribes the main verb to the auxiliary
        verb so there is done a different check than expected, e.g. 'died' is
        the auxiliary verb in 'has died'.
        """

        for word in parsed_sentence:
            if word[0][0] == verb or word[2][0] == verb and word[1] != "aux":
                return False
        return True


    def check_verbs(self, verbs, parsed_sentence):
        """
        Checks if a found verb is also classified as a verb in the tagged
        sentence, because the NLTK POS tagger sometimes makes mistakes.
        """

        for verb in verbs:
            for parsed_element in parsed_sentence:
                if (verb[0] in parsed_element[0] and not any("VB" in string for
                    string in parsed_element[0])) or (verb[0] in
                    parsed_element[2] and not any("VB" in string for string in
                    parsed_element[2])):
                       verbs.remove(verb)
                       break
        return verbs


    def is_empty_answer(self, sentence, verbs):
        """
        Checks if there were no verbs in a sentence or if the verb 'do' is
        in the sentence without any object. In this case, the question's verbs
        and objects should be used.
        """

        if len(sentence) == 0 or (((any("do" in verb for verb in verbs) and not
                                  any("dobj") in element for element in
                                  sentence)) or (any("can") in verb for verb in
                                  verbs and not any("dobj") in element for
                                  element in sentence)) or len(verbs) == 0:
            return True
        return False


    def analyse_empty_sentence(self, answer, parsed_answer, parsed_question,
                               answer_verbs, question_verbs):
        """
        Uses the parsed answer and question to return the correct verbs,
        objects and negations.
        """

        if len(parsed_answer) == 0:
            # The answer is either only 'yes' or 'no'
            if "no" in answer or "No" in answer:
                # The answer is not affirmative: 'No'
                v, o, n = self.analyse_sentence(question_verbs, parsed_question,
                                                True, "not")
            else:
                # The answer is affirmative: 'Yes'
                v, o, n = self.analyse_sentence(question_verbs, parsed_question,
                                                True, None)
        else:
            # The answer is something along the lines of 'I do'
            _, _, n = self.analyse_sentence(answer_verbs, parsed_answer, False,
                                            "")
            v, o, _ = self.analyse_sentence(question_verbs, parsed_question,
                                            False, "")
        return v, o, n


    def analyse_sentence(self, verbs, sentence, negation_flag, own_negation):
        """ Analyses a sentence: returns the verb, object and negation. """

        objects = []
        negations = []

        sentences = self.check_coordination(sentence)

        for i in range(0, len(sentences)):
            objects.append(self.get_function_word(sentences[i], verbs[i][0],
                                                  "dobj"))
            if not negation_flag:
                negations.append(self.get_function_word(sentences[i],
                                                        verbs[i][0], "neg"))
            else:
                negations.append([own_negation])
        verbs, objects, negations = self.correct_functions(verbs, objects,
                                                           negations)
        return verbs, objects, negations


    def check_coordination(self, sentence):
        """ Checks for a coordination and splits the sentence. """

        contradiction = ("but", "however")

        for i in range(0, len(sentence)):
            if sentence[i][1] == "cc" and sentence[i][2][0] in contradiction:
                return [sentence[0:i], sentence[i:len(sentence)+1]]
        return [sentence]


    def get_function_word(self, sentence, verb, requested_function):
        """ Returns the word that has the requested function in a sentence. """

        function_words = []

        for word in sentence:
            if word[1] == requested_function and word[0][0] == verb:
                if requested_function == "neg":
                    function_words.append("not")
                else:
                    function_words.append(word[2][0])
                    conjunctions = self.get_conjunctions(sentence, word[2][0])
                    compound = self.get_compound(sentence, word[2][0])
                    if conjunctions:
                        function_words.append(conjunctions)
                        function_words = list(self.flatten(function_words))
                    if compound:
                        function_words.remove(word[2][0])
                        function_words.append(compound)
        if not function_words:
            function_words.append(None)
        return function_words


    def get_conjunctions(self, sentence, function_word):
        """
        Retrieves all the conjunctions of a word so that all the necessary
        objects and negations are detected.
        """

        conjunctions = []

        for word in sentence:
            if word[1] == "conj" and word[0][0] == function_word:
                conjunctions.append(word[2][0])
        return conjunctions


    def get_compound(self, sentence, function_word):
        """ Returns the compound of a word. """

        compound = ""

        for word in sentence:
            if (word[1] == "compound" and word[0][0] == function_word) or \
                (word[1]) == "amod" and word[0][0] == function_word:
                compound = word[2][0] + " " + function_word
        return compound


    def flatten(self, unflattened_list):
        """ Flattens a list. """

        for element in unflattened_list:
            if isinstance(element, collections.Iterable) and not \
               isinstance(element, basestring):
                for subelement in self.flatten(element):
                    yield subelement
            else:
                yield element


    def correct_functions(self, verbs, objects, negations):
        """
        Corrects the found verbs, objects and negations such that they can
        easily be used for the database by copying verbs, objects and negations
        where necessary such that the lists are all of equal length.
        """

        sentences = [verbs, objects, negations]
        maximum_length = self.maximum_list_length(sentences)

        for i in range(0, len(sentences)):
            for j in range(0, len(sentences[i])):
                if len(sentences[i][j]) != maximum_length:
                    sentences[i][j].extend(repeat(sentences[i][j][0],
                                                  maximum_length -
                                                  len(sentences[i][j])))
        return sentences[0], sentences[1], sentences[2]


    def maximum_list_length(self, long_list):
        maximum_length = 0

        for short_list in long_list:
            for element in short_list:
                if isinstance(element, list) and len(element) > maximum_length:
                    maximum_length = len(element)
        return maximum_length


    # def find_drink_property(self, word, pos):
    #     """
    #     Finds the drink property that has the shortest distance to a common
    #     hypernym between a drink property and a word.
    #     """
    #
    #     highest_similarity = 0
    #
    #     for drink_property in self.pos_tags:
    #         property_pos = self.pos_tags.get(drink_property)
    #         property_synsets = wn.synsets(drink_property, pos=property_pos)
    #         word_synsets = wn.synsets(word, pos=pos)
    #         property_syn, word_syn, simil = \
    #             self.find_best_synset(property_synsets, word_synsets)
    #
    #         if simil > highest_similarity:
    #             highest_similarity = simil
    #             best_property = drink_property
    #     return best_property
    #
    #
    # def find_best_synset(self, synsets_1, synsets_2):
    #     """
    #     Uses the Wu-Palmer similarity to find the two synsets that are likely
    #     the best options for two words.
    #     """
    #
    #     highest_similarity = 0
    #     best_synset_1 = ""
    #     best_synset_2 = ""
    #
    #     for synset_1 in synsets_1:
    #         for synset_2 in synsets_2:
    #             similarity = synset_1.wup_similarity(synset_2)
    #             if similarity is None:
    #                 similarity = 0
    #             if similarity > highest_similarity:
    #                 highest_similarity = similarity
    #                 best_synset_1 = synset_1
    #                 best_synset_2 = synset_2
    #     return best_synset_1, best_synset_2, highest_similarity


    def apply_sentence(self, verbs, objects, negations):
        """
        Uses the verbs, objects and negations to update the list of drinks.
        """

        for i in range(0, len(verbs)):
            for j in range(0, len(verbs[i])):
                if self.is_possessive(verbs[i][j]):
                    word = objects[i][j]
                    # pos = "n"
                else:
                    word = verbs[i][j]
                    # pos = "v"
                # drink_property = self.find_drink_property(word, pos)
                updated_drinks = self.update_drinks(word, negations[i][j])
        return updated_drinks


    def is_possessive(self, verb):
        """
        Returns a boolean that indicates whether a verb expresses possession.
        """

        possesive = ("has", "have", "possess", "own", "has got", "have got",
                     "hold")

        return any(verb in string for string in possesive)


    def update_drinks(self, word, negation):
        """
        Updates the list of property values of the ordered drinks if a match
        can be found between the word that was said and what is in the key
        words.
        """

        understood = False

        if wn.morphy(word):
            word = wn.morphy(word)

        found_key = self.synonyms.get(word)

        if found_key:
            for drink_properties in self.properties:
                if self.substring_in_list(found_key, drink_properties):
                    self.update_availability(drink_properties, found_key,
                                             negation)
                    # self.all_true()
                    understood = True
        else:
            split_word = word.split(" ")
            for split_element in split_word:
                found_key = self.synonyms.get(split_element)
                if found_key:
                    for drink_properties in self.properties:
                        if self.substring_in_list(found_key, drink_properties):
                            self.update_availability(drink_properties,
                                                     found_key, negation)
                            # self.all_true()
                            understood = True
        if understood:
            pprint(self.properties)
        return understood



    def substring_in_list(self, substring, l_ist):
        """
        Returns a boolean that indicates whether a substring can be found in a
        list.
        """

        substring_list = [s for s in l_ist if substring in s]

        if len(substring_list) > 0:
            return True
        return False


    # def all_true(self):
    #     for i in range(0, len(self.properties)):
    #         for j in range(0, len(self.properties[i])):
    #             if "None" in self.properties[i][j]:
                    # self.properties[i][j] = self.properties[i][j].replace("None", "True")


    def update_availability(self, drink_properties, word, negation):
        """
        Updates the availability of a property value to False or True and
        removes the drink from the list of available drinks if the property
        value is False.
        """

        iterate_properties = iter(drink_properties)
        # Skip the first loop because it's the drink's name.
        next(iterate_properties)

        drink_index = self.properties.index(drink_properties)

        for element in iterate_properties:
            if word in element:
                if negation:
                    drink = drink_properties[0].split(": ")[0]
                    if drink in self.available_drinks:
                        self.available_drinks.remove(drink)
                        del self.properties[drink_index]
                        self.load_synonyms(self.available_drinks)
                else:
                    property_index = drink_properties.index(element)
                    element = element.replace("None", "True")
                    drink_properties[property_index] = element
                    self.properties[drink_index] = drink_properties


    def get_properties(self):
        """ Returns the list of properties. """

        return self.properties


    def get_available_drinks(self):
        """ Returns the list of available drinks. """

        return self.available_drinks


if __name__ == "__main__":
    understand = Understand(["bloody mary", "martini", "margarita",
                             "cosmopolitan", "sangria"])
    print understand.understand_sentence("Can you shake drinks?", "Yes, I can.")
    pprint(understand.get_properties())
