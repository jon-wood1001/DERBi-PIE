from gensim.scripts.glove2word2vec import glove2word2vec
from scipy.spatial.distance import cosine
from gensim.models import KeyedVectors
import pandas as pd
from nltk.corpus import wordnet as wn
from nltk import download
import re, time
import numpy as np 


# Path to the GloVe file
glove_input_file = 'glove.6B.50d.txt'
glove_large_input_file = 'glove.42B.300d.txt'
word2vec_output_file = 'glove.6B.50d.txt.word2vec'
word2vec_large_output_file = 'glove.42B.300d.txt.word2vec'
#glove2word2vec(glove_input_file, word2vec_output_file)
"""
start_time = time.time()
glove2word2vec(glove_large_input_file, word2vec_large_output_file)
seconds = time.time() - start_time
print("--- %s seconds ---" % (seconds))
# min 
print('minutes: ', seconds/60)
print('this take too mf long')"""

target_word = 'scholar'
target_words = ['scholar', 'god', 'dog', 'cat', 'fish', 'bird', 'car', 'bicycle', 'house', 'tree']

def explore_hyponyms(word):
    hyponyms = []
    for synset in wn.synsets(word):
        for hyponym in synset.hyponyms():
            hyponyms.append(hyponym.lemmas()[0].name())
    print('hyponyms of ', word, ': ')
    print(hyponyms)
    return list(set(hyponyms)) 

def explore_meronyms(word):
    meronyms = []
    for synset in wn.synsets(word):
        for meronym in synset.part_meronyms():
            meronyms.append(meronym.lemmas()[0].name())
    print('meronyms of ', word, ': ')
    print(meronyms)
    return list(set(meronyms))

def explore_antonyms(word):
    antonyms = []
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            antonyms.extend([ant.name() for ant in l.antonyms()])
    print('antonyms of ', word, ': ')
    print(antonyms)
    return list(set(antonyms))  

def explore_hypernyms(word):
    hypernyms = []
    for synset in wn.synsets(word):
        for hypernym in synset.hypernyms():
            hypernyms.append(hypernym.lemmas()[0].name())
    print('hypernyms of ', word, ': ')
    print(hypernyms)
    return list(set(hypernyms)) 

# Function to clean and extract main word from meaning
def extract_main_word(meaning):
    # This pattern matches auxiliary verbs 'to be' or 'to' followed by a word.
    pattern = re.compile(r"\bto\s(?:be\s)?(\w+)")
    match = pattern.search(meaning)
    return match.group(1) if match else meaning

# Function to check if a word is in WordNet
def is_in_wordnet(word):
    return wn.synsets(word)

def get_set_of_structural_words(target_word):
    # create a set of all 'structural' words of target word
    structural_words = set(explore_hyponyms(target_word) + explore_meronyms(target_word) + explore_antonyms(target_word) + explore_hypernyms(target_word))
    return structural_words

# Load the converted model
model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
# Load the CSV file
data = pd.read_csv("./derbipie/DERBi-PIE/expanded_cleaned_data.csv")

# Set to collect unique, WordNet-verified words
unique_words = set()
unique_words.add(target_word)

# Iterate through the dataframe
for meaning in data['meaning']:
    main_word = extract_main_word(meaning)
    if is_in_wordnet(main_word) and main_word not in unique_words:
        unique_words.add(main_word)
        if len(unique_words) == 3700:  # Stop once we have 100 unique words
            break
words = unique_words

embeddings = {word: model[word] for word in words if word in model}

def calculate_similarity(word1, word2):
    # Ensure both words are in the model
    if word1 in embeddings and word2 in embeddings:
        # Calculate cosine similarity (the smaller the cosine distance, the more similar they are)
        similarity = 1 - cosine(embeddings[word1], embeddings[word2])
        return similarity
    else:
        return None
def find_most_similar_word(root_word):
    most_similar_word = None
    max_similarity = 0
    for word in embeddings:
        if word != root_word:
            similarity = calculate_similarity(root_word, word)
            if similarity is not None and similarity > max_similarity:
                max_similarity = similarity
                most_similar_word = word
    return most_similar_word, max_similarity

def calculate_similarity_to_target(target_word, word):
    if target_word in embeddings and word in embeddings:
        similarity = 1 - cosine(embeddings[target_word], embeddings[word])
        return similarity
    else:
        return None

def is_word_in_model(word, model):
    return word in model.vocab


for word in target_words: 
    structural_words = get_set_of_structural_words(word)
    # Set to collect unique, WordNet-verified words
    unique_words = set()
    unique_words.add(target_word)
    # Iterate through the dataframe
    for meaning in data['meaning']:
        main_word = extract_main_word(meaning)
        if is_in_wordnet(main_word) and main_word not in unique_words:
            unique_words.add(main_word)
            if len(unique_words) == 3700:  # Stop once we have 100 unique words
                break
    words = unique_words
    embeddings = {word: model[word] for word in words if word in model}


    words_not_in_model = []
    for word in structural_words:
        similarity = calculate_similarity_to_target(target_word, word)
        if similarity is not None:
            print(f"Similarity between '{target_word}' and '{word}': {similarity}")
        else:
            words_not_in_model.append(word)

