
import csv
import numpy as np
import pandas as pd

i = 0
probability = np.matrix([])

df = pd.read_csv('C:/Users/kivid/Dropbox/Universita/Corsi Magistrale/Modelli probabilistici per le decisioni/Progetto'
                 ' Mispelling/HMMispelling/HMMispelling/resources/upper_by_upper_bigram_frequency.csv')




i = 1

#for j = 1 to len(df)

#with open('C:/Users/kivid/Dropbox/Universita/Corsi Magistrale/Modelli probabilistici per le decisioni/Progetto'
     #     ' Mispelling/HMMispelling/HMMispelling/resources/upper_by_upper_bigram_frequency.csv', 'r') as csvFile:
    #reader = csv.reader(csvFile)
    #for row in reader:
      #  oneRow = row[1:]
     #   if i == 1:
    #        probability = np.matrix(oneRow)
   #     if i > 1:
  #          probability = np.vstack([probability, oneRow])
 #       i += 1
#print(probability)