import argparse
import logging
import os

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser, tweets_io


def __predict_tweets__(tweets, model):
    corrected_tweets = {}
    for tweet_id in tweets:
        corrected = model.viterbi(tweets[tweet_id])

        corrected_tweets[tweet_id] = ''.join(corrected)

    return corrected_tweets


def __predict_words__(tweets, model):
    corrected_tweets = {}
    for tweet_id in tweets:
        corrected_tweet = []
        for word in tweets[tweet_id]:
            corrected = model.viterbi(word)

            corrected_tweet += [''.join(corrected)]

        corrected_tweets[tweet_id] = ' '.join(corrected_tweet)

    return corrected_tweets


def predict(in_path, out_path, model, params):
    tweets = tweets_io.load_tweets(in_path)

    corrected_tweets = __predict_tweets__(tweets, model)
    tweets_io.write_tweets(os.path.join(out_path, "tweets_corrected_{}.txt".format(params)),
                           corrected_tweets)

    splitted_tweets = {}
    for tweets_id in tweets:
        splitted_tweets[tweets_id] = tweets[tweets_id].split()

    corrected_words = __predict_words__(splitted_tweets, model)
    tweets_io.write_tweets(os.path.join(out_path, "words_corrected_{}.txt".format(params)),
                           corrected_words)


def main(args):
    states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")

    variance = args.error_variance
    if args.error_dist == "Gaussian":
        error_model = keyboard_errors.KeyBoardGaussianError(variance=variance)
    if args.error_dist == "Uniform":
        error_model = keyboard_errors.KeyboardUniformError()
    if args.error_dist == "PseudoUniform":
        error_model = keyboard_errors.KeyboardPseudoUniformError(key_prob=args.key_prob)

    error = error_model.evaluate_error()
    possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)
    start_prob = transition_prob[0]
    mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                           hidden_states=states, observables=possible_observation,
                                           emission_matrix=emission_prob)

    predict(args.input, args.out, mispelling_model, str(error_model))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A HMM misspelling correction tool")

    parser.add_argument("-input", type=str, default=100)
    parser.add_argument("-out", type=str, default=100)

    parser.add_argument("-error_dist", type=str, default="Gaussian")
    parser.add_argument("-error_variance", type=float, default=1)
    parser.add_argument("-key_prob", type=float, default=0.7)

    args = parser.parse_args()

    main(args)
