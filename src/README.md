# src Directory
This folder contains the files, documents, and databases related to the DERBi PIE/WordNet Project.
## Table of Contents
* [Databases](##Databases)
* [Scripts](##Scripts)
* [Contribution](##Contribution)
* [License](##License)
## Databases
Collected and gathered data from WordNet and the DERBi PIE website (available to download). This section discusses the what data was collected and which files it belongs to. <br>
Located in the [Databases](https://github.com/jon-wood1001/DERBi-PIE/tree/main/src/Databases) folder.
### Database Information:
* All files are formatted as a `.csv`.  
* The DERBi PIE Database: https://derbipie.as.uky.edu/results
* Database packages from WordNet.
* Databases that have been altered/cleaned/pruned:
    * If WordNet contains a part of a word in the DERBi PIE database, there should not be any duplicates among the conjunction of the databases.
    * If a word that exists in the modern lexicon but did not exist during the Proto-Indo European era, i.e. a word that has a definition with airplane.
* **Files**:
  *  *brute_definition_map.csv* -
  *  *cleaned_data.csv* -
  *  *expanded_cleaned_data.csv* - Contains the PIE roots of the cleaned data.
  *  *german_roots.csv* -
  *  *proper_n_synsets.csv* - Data where the Proper Noun Synsets were removed.
  *  *unmapped_pie_roots.csv* - Contains data where the PIE roots are unmapped.
  *  *wordnet_derbiepie_entries.csv* - Contains potential entries into DERBi PIE.
## Scripts
There were a multitude of scripts that were made by the team to complete a specific goal or task.<br>
Located in the [Scripts](https://github.com/jon-wood1001/DERBi-PIE/tree/main/src/Scripts) folder.
### Script Information:
* Most of the files contained in this folder are `Python` files. As a reference tool on how to get data from the WordNet database, a [Jupyter](https://github.com/jon-wood1001/DERBi-PIE/blob/main/src/Scripts/WordNet.ipynb) file is provided.
* **Files**:
  * *.DS_Store* -
  * *brute_force_map.py* -
  * *data_verify.py* -
  * *dataprep.py* -
  * *simple_synset_generation.py* -
  * *synset_mapping.py* -
  * *transfertobabel.py* -

## Contribution
If you want to contribute to this project, follow these steps:
1. Fork the repository
2. Create a new branch (git checkout -b feature/add-new-feature)
3. Make your changes and commit them (git commit -am 'Add new feature')
4. Push to the branch (git push origin feature/add-new-feature)
5. Open a pull request
## License
* This software project uses packages and software through WordNet, provided by Princeton University. Licensed under the WordNet License.
