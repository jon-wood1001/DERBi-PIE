# DERBi PIE and WordNet Integration
## Introduction
This project was chosen by our team and by our professor for the course CS 499 - Senior Design. During the course of five Sprint cycles, the team designed and implemented requested features for the customer. The team was allowed to save the program to a team-created public GitHub repository.
### Background
The overall goal of the project was to create an easy-to-use tool for linguists who lack certain technological skills (i.e. coding/software development). It is for people who will be interacting with the software without being able to write their own interactions with the API. The API is being developed by an associate of the customer.
<br>
<br>
Linguists study a multitude of languages. The focus of this project is the Proto-Indo-European (PIE) language, which is the root language to other languages like English, Spanish, Hindi, and Russian. Our customer has already compiled a database related to Proto-Indo-European. The database is called DERBi PIE (*Database of Etymological Roots Beginning in Proto-Indo-European*). The [website](https://derbipie.as.uky.edu/results) allows access to the full database and users can search a PIE root or an english root to produce a list of Proto-Indo-European roots containing descended words. 
<br>
<br>
A majority of this project dealt with interacting with the WordNet database. **WordNet** is a lexical database produced by Princeton. It is comprised of synsets, words that have similar definitions. The WordNet package can be accessed in Python by installing the `nltk` package (Natural Language Toolkit).
## Getting Started
Required Python Packages:
* nltk
* pandas
* numpy
* babelnet*

*Babelnet is optional if you do not want to execute the [transferwntobabel.py](https://github.com/jon-wood1001/DERBi-PIE/blob/main/src/Scripts/transferwntobabel.py) file. This file is only for experimenting with Babelnet when researching alternatives to WordNet.

Using the PyPI's `pip` tool in the Windows' command line, the following installation commands are:

```
pip install nltk
```
```
pip install pandas
```
```
pip install numpy
```
```
pip install babelnet
```
To verify the installations worked, the following code should be executed:
```
from nltk.corpus import wordnet as wn 
wn.synsets(“redundant”)
```
**Expected Output**: `[Synset('excess.s.01'), Synset('pleonastic.s.01')]`
## Execution
All files are located in the [Scripts](https://github.com/jon-wood1001/DERBi-PIE/tree/main/src/Scripts) folder. Executions of any of the file should be in this folder. In the command line, use `cd src/Scripts` to navigate to the folder. For example, the command to execute the [brute_force_map.py](https://github.com/jon-wood1001/DERBi-PIE/blob/main/src/Scripts/brute_force_map.py) file is:
```
python brute_force_map.py
```
## Testing
Executing the [simple_synset_generation.py](https://github.com/jon-wood1001/DERBi-PIE/blob/main/src/Scripts/simple_synset_generation.py) file serves as good test case to see if there were any changes to the main program. Testing was performed by cross referencing between the generated databases in the [Database](https://github.com/jon-wood1001/DERBi-PIE/tree/main/src/Databases) folder.
## Demo
The project's goal was accomplished by completing a set of steps:
* Data Preprocessing:
  *  Deriving the Individual PIE roots from the PIE entries.
* Prune the WordNet Database:
  * Remove proper nouns, for example.
* Map Synsets to the Roots
* Mapping Verification:
  * Removing improper definitions.
### Progress Report
Currently there are over 1,000 mapped PIE roots to at least one WordNet synset. There has also been over 7,000 potential entries generated for the DERBi PIE Database.
