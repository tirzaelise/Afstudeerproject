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

    def __init__(self):
        self.ordered_drinks = ["margarita", "martini", "bloody mary"]
        self.available_drinks = self.ordered_drinks
        self.setup_program()


    def understand_sentence(self, sentence):
        parsed_sentence = self.parse_sentence(sentence)
        verbs = self.get_verbs(sentence, parsed_sentence)
        verbs, objects, negations = self.analyse_sentence(verbs,
                                                          parsed_sentence)

        for i in range(0, len(verbs)):
            for j in range(0, len(verbs[i])):
                if self.is_possessive(verbs[i][j]):
                    word = objects[i][j]
                    pos = "n"
                else:
                    word = verbs[i][j]
                    pos = "v"
                # drink_property = self.find_drink_property(word, pos)
                self.update_drinks(word, negations[i][j])

        print self.available_drinks


    # def setup_program(ip):
    def setup_program(self):
        """
        Sets up the program by loading the database, parser, key words and
        drink properties and by setting up the robot.
        """

        start_time = time.time()
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
            self.synonyms.update(all_synonyms.get(drink))


    def load_pos_tags(self):
        """ Loads the POS tags of the properties. """

        self.pos_tags = {"drink": wn.NOUN, "color": wn.NOUN, "skill": wn.NOUN,
                         "alcoholic": wn.ADJ, "non-alcoholic": wn.ADJ,
                         "carbonated": wn.ADJ, "non-carbonated": wn.ADJ,
                         "hot": wn.ADJ, "cold": wn.ADJ, "ingredient": wn.NOUN,
                         "taste": wn.NOUN, "occasion": wn.NOUN,
                         "tool": wn.NOUN, "action": wn.VERB}


    def load_properties(self):
        """ Loads the lists of properties of the ordered drinks. """

        self.properties = []

        if os.path.exists("drinks_properties.pkl"):
            all_properties = pickle.load(open("drinks_properties.pkl", "rb"))

        for drink in self.ordered_drinks:
            self.properties.append(all_properties.get(drink))


    # def setup_robot(ip, key_words):
    #     """
    #     Uses the robot's IP address to create a proxy on the speech recognition
    #     module. Sets the speech recognition language to English and uses the list
    #     of key words as vocabulary.
    #     """
    #
    #     global asr
    #     global alm
    #
    #     asr = ALProxy("ALSpeechRecognition", ip, 9559)
    #     asr.setLanguage("English")
    #     start_time = time.time()
    #     # asr.setVocabulary(key_words, True)
    #     asr.setVocabulary(key_words, False)
    #     print "set vocab time:", time.time() - start_time
    #     asr.setVisualExpression(True)
    #     asr.setAudioExpression(False)
    #     alm = ALProxy("ALMemory", ip, 9559)


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


    def analyse_sentence(self, verbs, sentence):
        """ Analyses a sentence: returns the verb, object and negation. """

        objects = []
        negations = []

        sentences = self.check_coordination(sentence)

        for i in range(0, len(sentences)):
            objects.append(self.get_function_word(sentences[i], verbs[i][0],
                                                  "dobj"))
            negations.append(self.get_function_word(sentences[i], verbs[i][0],
                                                    "neg"))
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
                    if conjunctions:
                        function_words.append(conjunctions)
                        function_words = list(self.flatten(function_words))
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
                # if None in sentences[i][j]:
                #     print "None in sentence"
                #     sentences[i][j] = [sentences[i][j-1][0]]
                #     sentences[i][j].extend(repeat(sentences[i][j],
                #                                   maximum_length -
                #                                   len(sentences[i][j])))
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

        if wn.morphy(word):
            word = wn.morphy(word)

        found_key = self.synonyms.get(word)

        if found_key:
            for drink_properties in self.properties:
                if self.substring_in_list(found_key, drink_properties):
                    self.update_availability(drink_properties, found_key,
                                             negation)
        # else:
        # Robot did not understand



    def update_availability(self, drink_properties, word, negation):
        """
        Updates the availability of a property value to False or True and
        removes the drink from the list of available drinks if the property
        value is False.
        """

        iterate_properties = iter(drink_properties)
        # Skip the first loop because it's the drink's name.
        next(iterate_properties)

        drink_property_index =  self.properties.index(drink_properties)

        for element in iterate_properties:
            if word in element:
                property_index = drink_properties.index(element)
                split_property = element.split(":")
                if negation:
                    split_property[-1] = ": False"
                    drink = drink_properties[0].split(": ")[0]
                    self.available_drinks.remove(drink)
                    del self.properties[drink_property_index]
                    self.load_synonyms(self.available_drinks)
                else:
                    split_property[-1] = ": True"
                element = "".join(split_property)
                drink_properties[property_index] = element
        self.properties[drink_property_index] = drink_properties


    def get_dict_keys(self, key, var):
        """
        Searches the entire dict for a key and returns the value.
        """

        if hasattr(var, "iteritems"):
            for k, v in var.iteritems():
                if k == key:
                    yield v
                if isinstance(v, dict):
                    for result in self.get_dict_keys(key, v):
                        yield result


    def substring_in_list(self, substring, l_ist):
        """
        Returns a boolean that indicates whether a substring can be found in a
        list.
        """

        substring_list = [s for s in l_ist if substring in s]

        if len(substring_list) > 0:
            return True
        return False


if __name__ == "__main__":
    understand = Understand()
    understand.understand_sentence("I have two lemons.")
