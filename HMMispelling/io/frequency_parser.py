'''
import csv

def LettersFrequenciesRead

    return LettersFrequenciesFile().read()

class LettersFrequenciesFile(object):

    def read(source):

        with open('resources/lower_by_lower_bigram_frequencies.csv', 'rb') as csvFile
            reader = csv.reader(csvFile)
            for row in reader:
                print
'''

#def read(file)

import csv
import numpy as np

i = 0
probability = np.matrix([])

with open('C:/Users/kivid/Dropbox/Universita/Corsi Magistrale/Modelli probabilistici per le decisioni/Progetto'
          ' Mispelling/HMMispelling/HMMispelling/resources/lower_by_upper_bigram_frequency.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    next(reader) # Skip of header row
    for row in reader:
        row_values = row[1:] # Remove first column
        row_float = [float(k) for k in row_values] # Casting to float
        probability = np.matrix(row_float) if i == 0 else np.vstack([probability, row_float])
        i += 1
print(probability)