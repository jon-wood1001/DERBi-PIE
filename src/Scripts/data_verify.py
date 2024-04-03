import pandas as pd
import os

dir = r'../Databases/'
pie_root_file = r'data.csv'
path = dir + pie_root_file

# read data.csv
original_data = pd.read_csv(path, encoding='utf-8')

cleaned_roots = r'expanded_cleaned_data.csv'
path = dir + cleaned_roots

cleaned_data = pd.read_csv(path, encoding='utf-8')

count = 0

for root in original_data['root']:
    if root not in cleaned_data['root']:
        if(count == 0):
            print(root)
        count += 1

print(count)