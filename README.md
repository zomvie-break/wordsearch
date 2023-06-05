# WORDSEARCH

A simple python script to create word searhes PDF for students.

## Why?

My primary-level students enjoy solving wordsearches. However, they also like to collaborate a little too much. That is why I developed this script to generate _n_ distinct wordsearches given a list of words. In the case of spanish nouns, the list of words contain the word in Spanish, the gender (i.e. m for masculine and f for femenine) as well as the translation in English. 

Since I teach students from grade 2 to grade 6, I needed a way to adjust the difficulty of the wordsearch. The script allows you to change the dimensions of the wordsearch as well as the difficulty (if the words are placed vertically, horizontally, diagonally, or even backwards). 

## Installation

The installation process is as usual. I recommend you to create a virutal environment before running the script.

Create virtual environment:
`python -m venv ./<name_of_venv>`

Clone the repo:
`git clone https://github.com/zomvie-break/wordsearch.git`

Then activate the virtual environment and install the requirements:
`source ./<name_of_venv>/bin/activate`
`pip install -r requirements.txt`

## How to run the script?

To run the script, change the first line of `main.py` to your python interpreter in the virtual environment. 

You might also need to change the access permissions of the file with `chmod +x ./main.py`. 

Change the path of the text file in the `main.py` and choos how many wordsearches you want to generate and of what difficulty.

## Sample

Here is a sample of the wordsearch.

![Wordsearch sample](/samples/wordsearch_sample.png)