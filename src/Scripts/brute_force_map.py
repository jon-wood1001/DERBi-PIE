#Author: Jackson
from nltk.corpus import wordnet as wn
import csv
import pandas as pd
import openpyxl



# Potential proper nouns in wordnet database
def seperate_proper_nouns():
    proper_nouns = []
    for synset in wn.all_synsets():
        synset_name = synset.name()
        synset_def = synset.definition()
        if synset_def[0].isupper():
            proper_nouns.append([synset_name,synset_def])
    return proper_nouns

#Generate the synsets that are currently unmapped to the 
def create_mapped_database(pie_roots_dict : dict):
    mapped_database = {}
    subset_database = {}
    count = 0

    for synset in wn.all_synsets():
        synset_name = synset.name()
        synset_def = synset.definition()
        pure_name = synset_name.split('.')[0]
        if synset_def[0].isupper():
            # print(synset_name)
            count += 1
            continue
        #Normal brute force
        if synset_def in pie_roots_dict:
            key = pie_roots_dict[synset_def]
            # Check if the key is already in the mapped database
            if key in mapped_database:
                # If key exists, append the new synset_name to the existing list
                mapped_database[key][0] += ', ' + synset_name
            else:
                # If key doesn't exist, create a new list with the current synset_name
                mapped_database[key] = [synset_name]
        elif pure_name in pie_roots_dict:
            key = pie_roots_dict[pure_name]
            # Check if the key is already in the mapped database
            if key in mapped_database:
                # If key exists, append the new synset_name to the existing list
                mapped_database[key][0] += ', ' + synset_name
            else:
                # If key doesn't exist, create a new list with the current synset_name
                mapped_database[key] = [synset_name]
        #Subset method
        # for root_def in pie_roots_dict:
        #     if root_def in synset_def:
        #         key = pie_roots_dict[root_def]
        #         if key in subset_database:
        #             subset_database[key][0] += ', ' + synset_name
        #         else:
        #             # If key doesn't exist, create a new list with the current synset_name
        #             subset_database[key] = [synset_name]
            
    return mapped_database, subset_database

def extract_PIE_root_defs():
    root_defs_dict = {}
    
    path = r'../Databases/'
    with open(path + 'expanded_cleaned_data.csv', encoding="utf8") as pie_csv:
        reader = csv.DictReader(pie_csv)
        for row in reader:

            root = row['root']
            root_def = row['meaning']
            # Check if the key already exists in the dictionary
            if root_def in root_defs_dict:
                # Key already exists, handle it as needed
                print(f"Key '{root}' already exists. Skipping...")
            else:
                # Key doesn't exist, add it to the dictionary
                root_defs_dict[root_def] = root
    
    return root_defs_dict

def save_dict(dict, name):
    # Create a DataFrame from the dictionary
    df = pd.DataFrame(dict)

    df_reshaped = pd.DataFrame([(key, value) for key, values in dict.items() for value in values], columns=['Key', 'Value'])

    # Specify the path where you want to save the Excel file
    path = r'../Databases/'
    excel_file_path = path + name + r'.xlsx'

    # Write the DataFrame to an Excel file
    df_reshaped.to_excel(excel_file_path, index=False)
    return

# Incomplete
def save_list(items, name):
    # Create a new Excel workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for row_index, row_data in enumerate(items, start=1):
        for col_index, value in enumerate(row_data, start=1):
            sheet.cell(row=row_index, column=col_index, value=value)

    # Save the workbook to a file
    path = r'../Databases/'
    excel_file_path = path + name + r'.xlsx'
    workbook.save(excel_file_path)

def main():
    #if file doesn't exist, create unmapped database, otherwise read in unmapped database

    proper_nouns = seperate_proper_nouns()
    save_list(proper_nouns, "proper_n_synsets")

    pie_root_database : dict = extract_PIE_root_defs()

    brute_definition, brute_subset = create_mapped_database(pie_root_database)

    print(len(brute_definition))

    save_dict(brute_definition, "brute_definition_map")
    save_dict(brute_subset, "brute_definition_subset_map")




if __name__ == "__main__":
    main()