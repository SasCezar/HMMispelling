import logging

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser


def viterbi():
    logger = logging.getLogger(__name__)
    # _, start_prob = frequency_parser.load_probabilities("./resources/lower_first_letter_frequency.csv")

    sentence = "Hellp"

    states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")

    start_prob = transition_prob[0]

    possible_observation, emission_prob = keyboard_errors.create_emission_matrix(keyboard_errors.
                                                                                 KeyBoardGaussianError(variance=0.3).
                                                                                 evaluate_error()
                                                                                 )

    mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                           hidden_states=states, observables=possible_observation,
                                           emission_matrix=emission_prob)

    result = mispelling_model.model.viterbi(list(sentence))
    print("Viterbi word {}".format(result))

    result = mispelling_model.model.forward_algo(list("hello"))
    print("Viterbi word {}".format(result))
    result = mispelling_model.model.forward_algo(list("helLo"))
    print("Viterbi word {}".format(result))


viterbi()
