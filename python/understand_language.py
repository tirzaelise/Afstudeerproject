import nltk
import os
import pickle

# Loads the database.
def load_database():
    if os.path.exists("database.pkl"):
        return pickle.load(open("database.pkl", "rb"))

# Tags a sentence.
def tag_sentence(sentence):
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))

    for word, tag in tagged_sentence:
        print word, tag


if __name__ == "__main__":
    database = load_database()
    if database:
        print "Database loaded successfully"
    else:
        print "Database failed to loaded"
    tag_sentence("This drink needs ice, but I do not have it.")
