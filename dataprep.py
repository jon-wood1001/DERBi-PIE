import pandas as pd
import os

# read data.csv
data = pd.read_csv("data.csv")

# remove duplicates in the "root" column
data = data.drop_duplicates(subset="root")

# remove rows with missing values in the "root" column
data = data.dropna(subset=["root"])

# remove text within parentheses from the "root" column
data['root'] = data['root'].str.replace(r"\(.*?\)", "", regex=True)

# Optionally, strip leading and trailing whitespace which might be left after removing parentheses
data['root'] = data['root'].str.strip()

# some meanings have <b> tags - remove them 
data['meaning'] = data['meaning'].str.replace(r"<b>", "", regex=True)
data['meaning'] = data['meaning'].str.replace(r"</b>", "", regex=True)

# save the cleaned data to a new file
data.to_csv("cleaned_data.csv", index=False)

# print the first 5 rows of the cleaned data
print(data.head())




##### LATER ON #####
# Assuming data.csv has been read into 'data'
data = pd.read_csv("cleaned_data.csv")

# Expand the 'meaning' column into separate rows for each comma-separated value
data['meaning'] = data['meaning'].str.split(', ')  # Split the 'meaning' string into a list of strings
exploded_data = data.explode('meaning')  # Explode the 'meaning' lists into separate rows

# Remove duplicates and missing values if necessary
exploded_data = exploded_data.drop_duplicates(subset=['meaning']).dropna(subset=['meaning'])

# Optionally, you can further clean the 'meaning' column if needed (e.g., stripping whitespace)
exploded_data['meaning'] = exploded_data['meaning'].str.strip()

# Save the cleaned and expanded data to a new file
exploded_data.to_csv("expanded_cleaned_data.csv", index=False)

# Print the first 5 rows of the expanded, cleaned data
print(exploded_data.head())
