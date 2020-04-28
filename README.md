# HMMispelling
HMMispelling is a demo application (check webapp branch for the app) to correct input keyboard typos.  During the development of our project we made some studies on the problem: we defined an Hidden Markov Model, ran the Viterbi algorithm on it and analyzed the results by comparing different configurations and inputs.

## Model
We modeled the problem as an hidden markov model, where the hidden states are the characters of the text which should have been typed; the emissions are the actual typed characters. The chosen task to infer the correct typed text is Most Likely Sequence.

## Conclusions
In our project we developed an application able to correct keyboard typos thanksto the use of an Hidden Markov Model.  We trained the model parameters and tested the  possible  parameters  combinations  in  order  to  find  the  best  configuration  for  the model.  Moreover,  we added a dictionary to support the correction task.  Finally we analyzed the results.  We don’t have high performances due to our model weakness:  the fact that it is based on bigram frequencies and not on the whole word probability often leads the Viterbi algorithm to accept perturbed words; if all the bigrams in a word have high probability to occur, the model can’t establish if it is a perturbed or a corrected word. Future enhancements could be to use a Markov Chain and replace the bigram frequencies with longer n-grams.
