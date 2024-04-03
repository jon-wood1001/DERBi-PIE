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

#Generate the synsets that are currently unmapped to the 
def create_mapped_database(pie_roots_dict : dict):
    mapped_database = {}
    subset_database = {}

    for synset in wn.all_synsets():
        synset_name = synset.name()
        synset_def = synset.definition()
        pure_name = synset_name.split('.')[0]
        #If a proper noun, skip
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

    return mapped_database, subset_database

##DEFUNCT
# # Subset method
# for root_def in pie_roots_dict:
#     if root_def in synset_def:
#         key = pie_roots_dict[root_def]
#         if key in subset_database:
#             subset_database[key][0] += ', ' + synset_name
#         else:
#             # If key doesn't exist, create a new list with the current synset_name
#             subset_database[key] = [synset_name]
            


# Take all the pie roots from the cleaned file
def extract_PIE_root_defs():
    root_defs_dict = {}
    
    with open(data_dir + cleaned_file, encoding="utf8") as pie_csv:
        reader = csv.DictReader(pie_csv)
        for row in reader:

            root = row['root']
            root_def = row['meaning']
            # Check if the key already exists in the dictionary
            if root_def not in root_defs_dict:
                root_defs_dict[root_def] = [root]
            # If the definition already has an associated root then add another associated root
            else:
                root_defs_dict[root_def].append(root)
    
    return root_defs_dict

def create_unmapped_database(pie_roots_dict : dict, mapped_roots_dict : dict):
    unmapped_database = {}

    key_list = list(pie_roots_dict.keys())
    val_list = list(pie_roots_dict.values())
    
    #Loop through each mapped definition
    for roots in pie_roots_dict.values():
        #Each mapped definiton can have multiple roots
        for root in roots:
            if root in mapped_roots_dict:
                continue
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

    #loop through each value in each key
    for root in mapped_roots_dict:
        root_pos = []
        #WARNING: I'm not sure this is doing what's intended but it fixed the problem for now
        #My concern is that would there be situations where a root is the value to multiple key definitions??
        for roots in val_list:
            if root in roots:
                root_pos = roots
                continue
        position = val_list.index(root_pos)
        root_def = key_list[position]
        wordnet_synsets = mapped_roots_dict[root][0].split(', ')
        for synset in wordnet_synsets:
            synset_definition = wn.synset(synset).definition()
            synset = synset.split(".")
            synset_name = synset[0]
            synset_form = synset[1]
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


def main():
    #if file doesn't exist, create unmapped database, otherwise read in unmapped database
    pie_root_database : dict = extract_PIE_root_defs()
    brute_definition, brute_subset = create_mapped_database(pie_root_database)

    brute_unmapped = create_unmapped_database(pie_root_database, brute_definition)

    save_dict_to_csv(brute_definition, "brute_definition_map")
    # save_dict_to_csv(brute_subset, "brute_definition_subset_map")
    save_dict_to_csv(brute_unmapped, "unmapped_pie_roots")

    derbipie_entries = create_derbipie_sample_entries(pie_root_database, brute_definition)

    save_list_to_csv(derbipie_entries, "wordnet_derbipie_entries")

    proper_nouns : list = seperate_proper_nouns()
    save_list_to_csv(proper_nouns, "proper_n_synsets")




if __name__ == "__main__":
    main()