# !/usr/bin/env python2

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
        ordered_drinks = ["margarita", "martini"]
        self.available_drinks = ordered_drinks
        self.setup_program()


    def understand_sentence(self, sentence):
        parsed_sentence = self.parse_sentence(sentence)
        verbs = self.get_verbs(sentence, parsed_sentence)
        verbs, subjects, objects, negations = \
            self.analyse_sentence(verbs, parsed_sentence)

        for i in range(0, len(verbs)):
            for j in range(0, len(verbs[i])):
                if self.is_possessive(verbs[i][j]):
                    self.update_drinks(objects[i][j], negations[i][j])
                else:
                    self.update_drinks(verbs[i][j], negations[i][j])
        print self.available_drinks

        # for i in range(0, len(verbs)):
        #     if is_possessive(verbs[i]):
        #         clarification = ask_clarification(properties, verbs[i], subjects[i],
        #                                           objects[i], negations[i],
        #                                           key_words, True)
        #     else:
        #         clarification = ask_clarification(properties, verbs[i], subjects[i],
        #                                           objects[i], negations[i],
        #                                           key_words, False)
        #     robot_speak(clarification)
        #     confirmed = ask_confirmation()
        #     if confirmed:
        #         if is_possessive(verbs[i]):
        #             update_drinks(database, available_drinks, objects[i],
        #                           negations[i])
        #         else:
        #             update_drinks(database, available_drinks, verbs[i],
        #                           negations[i])
        #     else:
        #         robot_speak("Please describe what you mean differently.")
        # print available_drinks


    # def setup_program(ip):
    def setup_program(self):
        """
        Sets up the program by loading the database, parser, key words and
        drink properties and by setting up the robot.
        """

        self.load_database()
        self.load_parser()
        self.load_keywords()
        self.load_properties()
        # setup_robot(ip, key_words)


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


    def load_keywords(self):
        """
        Loads the key words that will be checked for occurrences of words in a
        natural sentence.
        """

        if os.path.exists("key_words.pkl"):
            self.key_words = pickle.load(open("key_words.pkl", "rb"))


    def load_properties(self):
        self.properties = {"drink": wn.NOUN, "color": wn.NOUN, "skill": wn.NOUN,
                           "alcoholic": wn.ADJ, "non-alcoholic": wn.ADJ,
                           "carbonated": wn.ADJ, "non-carbonated": wn.ADJ,
                           "hot": wn.ADJ, "cold": wn.ADJ, "ingredient": wn.NOUN,
                           "taste": wn.NOUN, "occasion": wn.NOUN,
                           "tool": wn.NOUN, "action": wn.VERB}


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
        """ Analyses a sentence: returns the subject, verb and object. """

        subjects = []
        objects = []
        negations = []

        for verb in verbs:
            subjects.append(self.get_function_word(sentence, verb[0], "nsubj"))
            objects.append(self.get_function_word(sentence, verb[0], "dobj"))
            negations.append(self.get_function_word(sentence, verb[0], "neg"))
        verbs, subjects, objects, negations = self.correct_functions(verbs,
                                                                     subjects,
                                                                     objects,
                                                                     negations)
        return verbs, subjects, objects, negations


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
        subjects and objects are detected.
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
                for subelement in flatten(element):
                    yield subelement
            else:
                yield element


    def correct_functions(self, verbs, subjects, objects, negations):
        """
        Corrects the found verbs, subjects, objects and negations such that they
        can easily be used for the database by copying verbs, subjects, objects
        and negations where necessary such that the lists are all of equal
        length.
        """

        sentences = [verbs, subjects, objects, negations]
        maximum_length = self.maximum_list_length(sentences)

        for i in range(0, len(sentences)):
            for j in range(0, len(sentences[i])):
                if None in sentences[i][j]:
                    sentences[i][j] = [sentences[i][j-1][0]]
                    sentences[i][j].extend(repeat(sentences[i][j], \
                                           maximum_length - \
                                           len(sentences[i][j])))
                elif len(sentences[i][j]) != maximum_length:
                    sentences[i][j].extend(repeat(sentences[i][j][0], \
                                           maximum_length - \
                                           len(sentences[i][j])))

        return sentences[0], sentences[1], sentences[2], sentences[3]


    def maximum_list_length(self, long_list):
        maximum_length = 0

        for short_list in long_list:
            for element in short_list:
                if isinstance(element, list) and len(element) > maximum_length:
                    maximum_length = len(element)
        return maximum_length


    def ask_clarification(self, verb, subject, s_object, negation, possessive):
        """
        Checks if the found verbs, subjects and objects are in the key words.
        If they are, the list of ordered drinks is updated with the new
        information. If they aren't, the robot asks for clarification.
        """

        unknown_words = self.check_keywords(verb, subject, s_object)
        if possessive:
            drink_property = self.find_drink_property(s_object, "n")
            clarification = self.understood(s_object, drink_property, negation)
        else:
            drink_property = self.find_drink_property(verb, "v")
            clarification = self.understood(verb, drink_property, negation)
        print clarification
        return clarification


    def check_keywords(self, verb, subject, s_object):
        """
        Checks if the found verb, subject and object are in the list of key
        words. Returns a list that contains the words that were not found in
        the key words.
        """

        unknown_words = []

        if verb:
            if verb.encode("utf-8") not in self.key_words:
                unknown_words.append(verb)
        if subject:
            if subject.encode("utf-8") not in self.key_words:
                unknown_words.append(subject)
        if s_object:
            if s_object.encode("utf-8") not in self.key_words:
                unknown_words.append(s_object)
        return unknown_words


    def misunderstood(self, unknown_words):
        """
        Returns a sentence that asks for clarification given the words in the
        sentence that were not understood, because they are not in the list of
        key words.
        """

        variable_words = ", ".join(unknown_words)
        request = " Please describe your response differently."

        if len(unknown_words) > 1:
            k = variable_words.rfind(", ")
            variable_words = variable_words[:k] + " and" + variable_words[k+1:]
            clarification = "I did not understand the words " + variable_words \
            + "."
        else:
            clarification = "I did not understand the word " + variable_words \
            + "."
        return clarification + request


    def find_drink_property(self, word, pos):
        """
        Finds the drink property that has the shortest distance to a common
        hypernym between a drink property and a word.
        """

        highest_similarity = 0

        for drink_property in self.properties:
            property_pos = self.properties.get(drink_property)
            property_synsets = wn.synsets(drink_property, pos=property_pos)
            word_synsets = wn.synsets(word, pos=pos)
            property_syn, word_syn, simil = \
                self.find_best_synset(property_synsets, word_synsets)

            if simil > highest_similarity:
                highest_similarity = simil
                best_property = drink_property
        return best_property


    def find_best_synset(self, synsets_1, synsets_2):
        """
        Uses the Wu-Palmer similarity to find the two synsets that are likely
        the best options for two words.
        """

        highest_similarity = 0
        best_synset_1 = ""
        best_synset_2 = ""

        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
                similarity = synset_1.wup_similarity(synset_2)
                if similarity is None:
                    similarity = 0
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_synset_1 = synset_1
                    best_synset_2 = synset_2
        return best_synset_1, best_synset_2, highest_similarity


    def understood(self, word, drink_property, negation):
        """
        Uses the most similar drink property to generate a response to the
        natural sentence that was spoken.
        """

        vowels = ("a", "e", "i", "o", "u")
        property_pos = self.properties.get(drink_property)
        start_of_sentence = "I understand you"
        end_of_sentence = ". Is this correct?"
        verb = " have "
        verb_compound = " got "
        property_as = " as a "

        if not negation:
            negation = ""

        if property_pos == wn.VERB:
            verb = " can "
            verb_compound = " "

        if drink_property.startswith(vowels):
            property_as = " as an "


        return start_of_sentence + verb + negation + verb_compound + word + \
               property_as + drink_property + end_of_sentence


    def robot_speak(self, string):
        """ Makes the robot say a string. """

        string


    def ask_confirmation(self):
        """
        Asks for confirmation from the person the robot is talking to based on
        the question that was asked and performs an action accordingly.
        """

        confirmed = True
        return confirmed


    def is_possessive(self, verb):
        """
        Returns a boolean that indicates whether a verb expresses possession.
        """

        possesive = ("has", "have", "possess", "own", "has got", "have got",
                     "hold")

        return any(verb in string for string in possesive)



    def update_drinks(self, word, negation):
        """
        Updates the list of ordered drinks.
        """

        for drink in self.available_drinks:
            properties = self.database.get(drink)
            if negation and self.substring_in_list(word, self.properties):
                self.available_drinks.remove(drink)


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
    understand.understand_sentence("I can stir and shake drinks.")
    # ordered_drinks = ["martini"]
    # available_drinks = ordered_drinks
    # sentence = "I can stir and shake drinks."
    #
    # start_time = time.time()
    # understand_sentence(sentence)
    # print "Time:", time.time() - start_time
