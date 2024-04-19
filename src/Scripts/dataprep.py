import pandas as pd
import os

dir = r'../Databases/'
pie_root_file = r'original_derbipie_entries.csv'
intermediate_file = r'cleaned_data.csv'
final_file = r'expanded_cleaned_data.csv'
encoding = 'utf-8'

def clean_data():
    # read pie root entries
    data = pd.read_csv(dir + pie_root_file, encoding=encoding)

    # remove duplicates in the "root" column, entries shouldn't have different entries for the roots technically
    data = data.drop_duplicates(subset="root")

    # remove rows with missing values in the "root" column
    data = data.dropna(subset=["root"])

    # some meanings have <b> tags - remove them, this is probably holdover from html formatting
    data['meaning'] = data['meaning'].str.replace(r"<b>", "", regex=True)
    data['meaning'] = data['meaning'].str.replace(r"</b>", "", regex=True)

    # save the cleaned data to a new file
    data.to_csv(dir + intermediate_file, index=False, encoding=encoding)

    # # print the first 5 rows of the cleaned data
    # print(data.head())

    # Expand the 'meaning' column into separate rows for each comma-separated value
    data['meaning'] = data['meaning'].str.split(', ')  # Split the 'meaning' string into a list of strings
    exploded_data = data.explode('meaning')  # Explode the 'meaning' lists into separate rows

    #Should we also explode the semicolons?
    # exploded_data['meaning'] = exploded_data['meaning'].str.split('; ')  
    # exploded_data = exploded_data.explode('meaning')  

    # Remove missing definitions
    exploded_data = exploded_data.dropna(subset=['meaning'])

    # Optionally, you can further clean the 'meaning' column if needed (e.g., stripping whitespace)
    exploded_data['meaning'] = exploded_data['meaning'].str.strip()

    ##### REMOVE UNNECESSARY DATA (for the context of mapping to wordnet) #####
    dropped_columns = ['derivative','derivative meaning','language','form','dictionary']
    truncated_data = exploded_data.drop(columns=dropped_columns)

    truncated_data.to_csv(dir + final_file, index=False, encoding=encoding)