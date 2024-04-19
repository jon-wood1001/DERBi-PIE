#Author: Jackson
from nltk.corpus import wordnet as wn
import csv
import pandas as pd

data_dir = r'../Databases/'
cleaned_file = r'expanded_cleaned_data.csv'

# Potential proper nouns in wordnet database
def seperate_proper_nouns():
    proper_nouns = []
    #For every synset in wordnet
    for synset in wn.all_synsets():
        synset_name = synset.name()
        synset_def = synset.definition()
        #Wordnet definitions start with an uppercase letter if they're proper nouns
        if synset_def[0].isupper():
            proper_nouns.append([synset_name,synset_def])
    return proper_nouns

#Generate the mappings between the pie roots and the wordnet synsets.
def create_mapped_database(pie_roots_dict : dict):
    mapped_database = {}

    #Iterate through every wordnet synset
    for synset in wn.all_synsets():

        #Extract synset name and definiton for this iteration
        synset_name = synset.name()
        synset_def = synset.definition()
        #synset names usually come like fire.n.04, we remove the number and part of speech because we didn't think it necessary.
        pure_name = synset_name.split('.')[0]

        #This skips this iteration if the synset is a proper noun
        #Proper nouns in the wordnet synset have an uppercase letter at the start of the definition
        if synset_def[0].isupper():
            continue

        #Brute Force Matching Pie Root Definitions to Synset Definitions
        if synset_def in pie_roots_dict:
            keys = pie_roots_dict[synset_def]
            for key in keys:
                # Check if the key is already in the mapped database
                if key in mapped_database:
                    # If key exists, append the new synset_name to the existing list
                    mapped_database[key][0] += ', ' + synset_name
                else:
                    # If key doesn't exist, create a new list with the current synset_name
                    mapped_database[key] = [synset_name]

        #Brute Force Matching Pie Root Definitions to Synset Names
        #Some synset names match the pie root definitions themselves
        elif pure_name in pie_roots_dict:
            keys = pie_roots_dict[pure_name]
            for key in keys:
                # Check if the key is already in the mapped database
                if key in mapped_database:
                    # If key exists, append the new synset_name to the existing list
                    mapped_database[key][0] += ', ' + synset_name
                else:
                    # If key doesn't exist, create a new list with the current synset_name
                    mapped_database[key] = [synset_name]

    return mapped_database

##DEFUNCT, could be expanded upon in future use.
# # Subset method
# for root_def in pie_roots_dict:
#     if root_def in synset_def:
#         key = pie_roots_dict[root_def]
#         if key in subset_database:
#             subset_database[key][0] += ', ' + synset_name
#         else:
#             # If key doesn't exist, create a new list with the current synset_name
#             subset_database[key] = [synset_name]
            
# Take all the pie roots from the expanded_cleaned_data.csv
def extract_PIE_root_defs():
    root_defs_dict = {}
    
    with open(data_dir + cleaned_file, encoding="utf8") as pie_csv:
        reader = csv.DictReader(pie_csv)
        for row in reader:

            root = row['root']
            root_def = row['meaning']
            # Check if the key already exists in the dictionary
            if root_def not in root_defs_dict:
                #We store it as a list because some definitions are associated with multiple roots
                root_defs_dict[root_def] = [root]
            # If the definition already has an associated root then add another associated root via appending to it as a list
            else:
                root_defs_dict[root_def].append(root)
    
    return root_defs_dict

def create_unmapped_database(pie_roots_dict : dict, mapped_roots_dict : dict):
    unmapped_database = {}

    #This part is implemented poorly, can be refactored in future usage
    #Since I originally stored these as a dictionary I needed to convert them to a list for some function usage below
    #This is needed because of the way pie_roots_dict is formatted, (key: definition, value: root)
    key_list = list(pie_roots_dict.keys())
    val_list = list(pie_roots_dict.values())
    

    #Loop through each pie root
    for roots in pie_roots_dict.values():

        #Each definition can have multiple roots associated
        for root in roots:

            #If the root was mapped then skip iteration
            if root in mapped_roots_dict:
                continue

            #Otherwise the root wasn't mapped, add it to the unmapped roots list
            else:
                #Since val_list is 2d list we need to use entire list of roots of a definition as our index
                position = val_list.index(roots)
                unmapped_database[root] = [key_list[position]]
                # unmapped_database[key_list[position]] = key_list[position]

    return unmapped_database

#Final 2d list should have an entry in each row, the columns of each row should look like the following
#root, root definition, derivative(synset), derivative definition, language, form(noun, verb, etc.), dictionary
def create_derbipie_sample_entries(pie_roots_dict : dict, mapped_roots_dict : dict):
    entries = [["Root", "Root_Definition", "Synset", "Synset_Definition", "Language", "Form", "Database"]]

    #This is needed because of the way pie_roots_dict is formatted, (key: definition, value: root)
    key_list = list(pie_roots_dict.keys())
    val_list = list(pie_roots_dict.values())

    #Iterate through each root
    for root in mapped_roots_dict:

        root_pos = []
        #WARNING: I'm not sure this is doing what's intended but it fixed the problem for now
        #My concern is that would there be situations where a root is the value to multiple key definitions??
        for roots in val_list:
            if root in roots:
                root_pos = roots
                continue
        #This is needed for dictionary shenanigans, if implemented without dictionaries this wouldn't be needed 
        position = val_list.index(root_pos)
        root_def = key_list[position]
        wordnet_synsets = mapped_roots_dict[root][0].split(', ')
        
        #Find the synset that's associated with the pie root and extract its information
        for synset in wordnet_synsets:
            synset_definition = wn.synset(synset).definition()
            synset = synset.split(".")
            synset_name = synset[0]
            synset_form = synset[1]
            #Create the formatting of the entry
            entries.append([root, root_def, synset_name, synset_definition, "English", synset_form, "Wordnet"])

    return entries


def save_dict_to_csv(dictionary, name):
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(dictionary)

    # Reshape the DataFrame
    df_reshaped = pd.DataFrame([(key, value) for key, values in dictionary.items() for value in values], columns=['Key', 'Value'])

    # Specify the path where you want to save the CSV file
    csv_file_path = data_dir + name + r'.csv'

    # Write the DataFrame to a CSV file
    df_reshaped.to_csv(csv_file_path, index=False)
    return


def save_list_to_csv(items, name):
    # Specify the path where you want to save the CSV file
    csv_file_path = data_dir + name + r'.csv'

    # Write the list to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(items)
    return