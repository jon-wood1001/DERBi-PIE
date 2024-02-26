from nltk.corpus import wordnet

def generate_synsets(word, pos):
    synsets = wordnet.synsets(word, pos=pos)
    
    for synset in synsets:
        print(f"Synset ID: {word}-{pos}")
        print(f"Definition: {synset.definition()}")
        print(f"Examples: {synset.examples()}")
        print(f"Hypernyms: {[lemma.name() for lemma in synset.hypernyms()[0].lemmas()]}" if synset.hypernyms() else "No Hypernyms")
        print(f"Hyponyms: {[lemma.name() for lemma in synset.hyponyms()[0].lemmas()]}" if synset.hyponyms() else "No Hyponyms")
        print("-------------")

# Example usage
generate_synsets("dog", pos="n")
generate_synsets("word", pos="n")
generate_synsets("hit", pos="v")
generate_synsets("fun", pos="n")
generate_synsets("red", pos="a")