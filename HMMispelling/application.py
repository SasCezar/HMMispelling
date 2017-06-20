import argparse
import logging

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser
from iohmms import tweets_io


def predict_tweets(in_path, out_path, model):
    tweets = tweets_io.load_tweets(in_path)

    corrected = {}
    for tweet_id in tweets:
        corrected_tweet = model.viterbi(tweets[tweet_id])

        corrected[tweet_id] = "".join(corrected_tweet)

    tweets_io.write_tweets(out_path, corrected)


def main(args):
    states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")

    variance = args.error_variance
    if args.error_dist == "Gaussian":
        error_model = keyboard_errors.KeyBoardGaussianError(variance=variance).evaluate_error()
    if args.error_dist == "Uniform":
        error_model = keyboard_errors.KeyboardUniformError().evaluate_error()
    if args.error_dist == "PseudoUniform":
        error_model = keyboard_errors.KeyboardPseudoUniformError().evaluate_error()

    possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error_model)
    start_prob = transition_prob[0]
    mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                           hidden_states=states, observables=possible_observation,
                                           emission_matrix=emission_prob)

    predict_tweets(args.input, args.out, mispelling_model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A HMM misspelling correction tool")

    parser.add_argument("-input", type=str, default=100)
    parser.add_argument("-out", type=str, default=100)

    subparser = parser.add_subparsers(dest="subparser")

    parser.add_argument("-error_dist", type=str, default="Gaussian")
    parser.add_argument("-error_variance", type=float, default=1)

    args = parser.parse_args()

    main(args)
