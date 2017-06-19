
import logging

import numpy

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser, tweets_io


def viterbi():
    logger = logging.getLogger(__name__)
    possible_observation, start_prob = frequency_parser.load_probabilities("./resources/upper_first_letter_frequency.csv")
    states, transition_prob = frequency_parser.load_probabilities("./resources/upper_by_upper_bigram_frequency.csv")
    emission_prob = keyboard_errors.create_emission_matrix(keyboard_errors.KeyboardPseudoUniformError().evaluate_error())

    print(numpy.sum(emission_prob, axis=1))

    mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                           hidden_states=states, observables=possible_observation,
                                           emission_matrix=emission_prob)
    dict = tweets_io.load_tweets("../dataset/apple_tweets_autowrong.txt")
    for key in dict:
        words = dict[key].split()
        for word in words:
            word = word.upper()
            mispelling_model.model.viterbi(list(word))


viterbi()