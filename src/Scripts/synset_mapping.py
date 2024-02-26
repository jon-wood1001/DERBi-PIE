# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 15:24:09 2024

@author: ritch
"""

from nltk.corpus import wordnet as wn
import csv

def map_wordnet_synset_ids():
    synset_ids = {}  # Dictionary to store mappings of synsets to unique IDs

    # Iterate through each synset in WordNet
    for synset in wn.all_synsets():
        synset_name = synset.name()
        # Check if the synset is already mapped to an ID
        if synset_name not in synset_ids:
            # Assign a new unique ID
            synset_ids[synset_name] = len(synset_ids) + 1

    return synset_ids

def write_to_csv(mapping, filename='synset_mapping.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Synset', 'ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for synset, synset_id in mapping.items():
            writer.writerow({'Synset': synset, 'ID': synset_id})

def main():
    synset_ids = map_wordnet_synset_ids()
    
    # Write mappings of synsets to unique IDs to CSV file
    write_to_csv(synset_ids)

if __name__ == "__main__":
    main()
