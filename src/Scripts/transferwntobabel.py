from nltk.corpus import wordnet as wn
from babelnet.resources import WordNetSynsetID
import babelnet as bn

def get_babelnet_id(wordnet_synset):
    """
    Given a WordNet synset, return the corresponding BabelNet ID.
    """
    # Constructing WordNet offset ID
    offset = str(wordnet_synset.offset()).zfill(8)  # Ensure the offset is 8 digits
    pos = wordnet_synset.pos()  # Get the part of speech

    # Construct the WordNet ID used in BabelNet
    if pos == 'n':
        wordnet_id = f"wn:{offset}n"
    elif pos == 'v':
        wordnet_id = f"wn:{offset}v"
    elif pos == 'a':
        wordnet_id = f"wn:{offset}a"  # Note: 'a' is for adjectives in WordNet
    elif pos == 'r':
        wordnet_id = f"wn:{offset}r"  # 'r' is for adverbs in WordNet
    else:
        return None  # Return None if part of speech is not supported

    # Use the WordNetSynsetID wrapper and the BabelNet API
    babel_synset = bn.get_synset(WordNetSynsetID(wordnet_id))

    # Check if a BabelSynset was found and return its ID
    if babel_synset:
        return babel_synset.id
    else:
        return None

# Example usage
wn_synset = wn.synset('dog.n.01')  # Use any synset from WordNet
bn_id = get_babelnet_id(wn_synset)
print(f"The BabelNet ID for {wn_synset} is {bn_id}")
