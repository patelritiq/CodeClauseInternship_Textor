# Textor
A Basic Text Editor

Textor is a simple text editor implemented in Python using Tkinter. It includes essential features such as creating, opening, saving text files, word count, and basic spell checking with misspelled words highlighted in red. The spell checker uses a local dictionary file (`words.txt`) to validate English words, ensuring efficient offline operation. Ideal for quick editing tasks and learning purposes.

** To craete words.txt
'''
import nltk
#Download the words dataset
nltk.download('words')
from nltk.corpus import words

#Get the list of English words
word_list = words.words()

#Save the words to a file
with open("words.txt", "w") as file:
    for word in word_list:
        file.write(word + "\n")
'''
