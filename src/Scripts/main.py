import brute_force_map as dundant
import dataprep as birdup

def main():

    #Generates the files cleaned_data.csv and expanded_cleaned_data.csv
    birdup.clean_data()

    #Extracts a dictionary of PIE roots with their corresponding english definitions
    #Then we map these PIE roots with their definitions to wordnet synsets
    pie_root_database : dict = dundant.extract_PIE_root_defs()
    brute_definition = dundant.create_mapped_database(pie_root_database)

    #Generate a list of all pie roots that weren't mapped to at least one wordnet synset
    brute_unmapped = dundant.create_unmapped_database(pie_root_database, brute_definition)

    #Save the data to brute_definition_map.csv and unmapped_pie_roots.csv
    dundant.save_dict_to_csv(brute_definition, "brute_definition_map")
    dundant.save_dict_to_csv(brute_unmapped, "unmapped_pie_roots")

    #Generate possible new entries for DERBi PIE based off the mapped wordnet roots
    derbipie_entries = dundant.create_derbipie_sample_entries(pie_root_database, brute_definition)
    dundant.save_list_to_csv(derbipie_entries, "wordnet_derbipie_entries")

    #Records the list of proper nouns that were removed from the wordnet database during mapping process
    proper_nouns : list = dundant.seperate_proper_nouns()
    dundant.save_list_to_csv(proper_nouns, "proper_n_synsets")

    print("Finished running the script...")
    print("Check the Databases directory for the generated entries")

if __name__ == "__main__":
    main()