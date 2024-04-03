import pandas as pd
import os

dir = r'../Databases/'
pie_root_file = r'data.csv'
intermediate_file = r'cleaned_data.csv'
final_file = r'expanded_cleaned_data.csv'
encoding = 'utf-8'

# read data.csv
data = pd.read_csv(dir + pie_root_file, encoding=encoding)

# remove duplicates in the "root" column
data = data.drop_duplicates(subset="root")

# remove rows with missing values in the "root" column
data = data.dropna(subset=["root"])

# remove text within parentheses from the "root" column
# data['root'] = data['root'].str.replace(r"\(.*?\)", "", regex=True)

# Optionally, strip leading and trailing whitespace which might be left after removing parentheses
# data['root'] = data['root'].str.strip()

# some meanings have <b> tags - remove them 
data['meaning'] = data['meaning'].str.replace(r"<b>", "", regex=True)
data['meaning'] = data['meaning'].str.replace(r"</b>", "", regex=True)

# save the cleaned data to a new file
data.to_csv(dir + intermediate_file, index=False, encoding=encoding)

# print the first 5 rows of the cleaned data
print(data.head())





##### LATER ON #####
# Assuming data.csv has been read into 'data'
data = pd.read_csv(dir + intermediate_file, encoding=encoding)

# Expand the 'meaning' column into separate rows for each comma-separated value
data['meaning'] = data['meaning'].str.split(', ')  # Split the 'meaning' string into a list of strings
exploded_data = data.explode('meaning')  # Explode the 'meaning' lists into separate rows

#Should we also explode the semicolons?
# exploded_data['meaning'] = exploded_data['meaning'].str.split('; ')  
# exploded_data = exploded_data.explode('meaning')  

# Remove duplicates and missing values if necessary
# WARNING, the code below gets rid of duplicate meanings which might not be what we want
# exploded_data = exploded_data.drop_duplicates(subset=['meaning']).dropna(subset=['meaning'])
exploded_data = exploded_data.dropna(subset=['meaning'])

# Optionally, you can further clean the 'meaning' column if needed (e.g., stripping whitespace)
exploded_data['meaning'] = exploded_data['meaning'].str.strip()

# Save the cleaned and expanded data to a new file
exploded_data.to_csv(dir + final_file, index=False, encoding=encoding)

# Print the first 5 rows of the expanded, cleaned data
print(exploded_data.head())


##### REMOVE UNNECESSARY DATA #####
data = pd.read_csv(dir + final_file, encoding=encoding)

dropped_columns = ['derivative','derivative meaning','language','form','dictionary']
truncated_data = data.drop(columns=dropped_columns)

truncated_data.to_csv(dir + final_file, index=False, encoding=encoding)