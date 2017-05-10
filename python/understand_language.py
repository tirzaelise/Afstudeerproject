# !/usr/bin/env python2

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.parse.stanford import StanfordDependencyParser
from pprint import pprint


# Loads the database.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))


# Loads the Stanford Dependency Parser.
def load_parser():
    jar_path = "stanford-parser-full-2016-10-31/stanford-parser.jar"
    models_path = "stanford-parser-full-2016-10-31/stanford-parser-" + \
        "3.7.0-models.jar"
    return StanfordDependencyParser(path_to_jar=jar_path,
                                    path_to_models_jar=models_path)


# Uses the Stanford Dependency Parser to parse a sentence.
def parse_sentence(parser, sentence):
    result = parser.raw_parse(sentence)
    dep = result.next()
    return list(dep.triples())


# Returns all the verbs in a sentence.
def get_verbs(sentence):
    verbs = []
    tokenized_sentence = word_tokenize(sentence)
    tagged_sentence = pos_tag(tokenized_sentence)

    for word in tagged_sentence:
        if word[1].startswith("VB"):
            verbs.append(word[0])
    return verbs


# Analyses a sentence: returns the subject, verb and object.
def analyse_sentence(verbs, sentence):
    subjects = []
    objects = []
    negations = []

    for verb in verbs:
        subjects = get_function_list(subjects, sentence, verb, "nsubj")
        objects = get_function_list(objects, sentence, verb, "dobj")
        negations = get_function_list(negations, sentence, verb, "neg")
    verbs, subjects, objects, negations = correct_functions(verbs, subjects,
                                                            objects, negations)
    return verbs, subjects, objects, negations


# Returns a list that holds the newly found word that fulfills a certain
# function in a sentence.
def get_function_list(function_list, sentence, verb, function):
    function_word = get_function_word(sentence, verb, function)
    if function_word:
        # function_word = get_synomyms(function_word)
        synonyms = get_synomyms(function_word)
    function_list.append(function_word)
    return function_list


# Returns the word that has the requested function in a sentence.
def get_function_word(sentence, verb, requested_function):
    function_word = None

    for word in sentence:
        if word[1] == requested_function and word[0][0] == verb:
            if requested_function == "neg":
                function_word = "not"
            else:
                function_word = word[2][0]
    return function_word


# Get the synonyms of a word using NLTK's WordNet.
def get_synomyms(word):
    synonyms = wn.synsets(word)
    for synonym in synonyms:
        for synonym_name in synonym.lemma_names():
            synonym_name = synonym_name.replace("_", " ")
            


# Sometimes a verb, that does not have a subject, is found. A sentence needs to
# have both a subject and a verb in order to form a sentence so then that verb
# can be omitted.
def correct_functions(verbs, subjects, objects, negations):
    i = 0

    for subject in subjects:
        if not subject:
            del verbs[i]
            del subjects[i]
            del objects[i]
            del negations[i]
        i +=1
    return verbs, subjects, objects, negations


# Returns the logical form of a sentence using a verb, subject, object and
# negation.
def get_logical_form(verbs, subjects, objects, negations):
    logical_forms = []

    for i in range(0, len(subjects)):
        logical_forms.append(natural_to_logic(verbs[i], subjects[i], objects[i],
                             negations[i]))
    return logical_forms


# Uses a verb, subject, object and negation to create a logical form of a
# natural sentence.
def natural_to_logic(verb, subject, s_object, negation):
    if negation:
        if s_object:
            form = verb + "(" + negation +  ", " + subject + ", " + s_object + \
            ")"
        else:
            form = verb + "(" + negation +  ", " + subject + ")"
    else:
        if s_object:
            form = verb + "(" + subject + ", " + s_object + ")"
        else:
            form = verb + "(" + subject + ")"
    return form


if __name__ == "__main__":
    sentence = "Do you have any lemons for me?"
    parser = load_parser()
    parsed_sentence = parse_sentence(parser, sentence)
    verbs = get_verbs(sentence)
    verbs, subjects, objects, negations = analyse_sentence(verbs,
                                                           parsed_sentence)
    logical_forms =  get_logical_form(verbs, subjects, objects, negations)
    print logical_forms
