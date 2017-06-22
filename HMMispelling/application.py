import argparse
from os import path

from numpy import arange

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser, tweets_io
from core.keyboard_errors import error_factory
from performance import evaluate


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
    file_name, _ = path.splitext(path.basename(in_path))

    tweets = tweets_io.load_tweets(in_path)

    corrected_tweets = __predict_tweets__(tweets, model)
    tweets_out = path.join(out_path, "{}_tweets_corrected_{}.txt".format(file_name, params))
    tweets_io.write_tweets(tweets_out, corrected_tweets)

    splitted_tweets = {}
    for tweets_id in tweets:
        splitted_tweets[tweets_id] = tweets[tweets_id].split()

    corrected_words = __predict_words__(splitted_tweets, model)
    words_out = path.join(out_path, "{}_words_corrected_{}.txt".format(file_name, params))
    tweets_io.write_tweets(words_out, corrected_words)

    return tweets_out, words_out


def find_best_score(tweets_path, corrected_path, out_path):
    words_scores = {}
    tweets_scores = {}

    tweet_file_path = tweets_path + "_autowrong.txt"
    states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")
    for error_string in ["Gaussian", "PseudoUniform"]:
        for int_param in range(5, 100, 5):
            param = float(int_param / 100)
            error_model = error_factory(error_string, param)
            error = error_model.evaluate_error()
            possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)

            start_prob = transition_prob[0]
            mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                                   hidden_states=states, observables=possible_observation,
                                                   emission_matrix=emission_prob)

            tweet_file_corrected, word_file_corrected = predict(tweet_file_path, corrected_path, mispelling_model,
                                                                str(error_model))

            file_name, _ = path.splitext(path.basename(tweets_path))
            tweet_tweet_index, tweet_word_index = evaluate.evaluate(tweets_path, tweet_file_corrected, out_path)
            word_tweet_index, word_word_index = evaluate.evaluate(tweets_path, word_file_corrected, out_path)
            # tweets_scores[str(error_model)] = tweet_index
            # words_scores[str(error_model)] = word_index

            # tweet_max = find_max(tweets_scores)
            # word_max = find_max(words_scores)


def main(args):
    states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")

    if args.subparser == "test":
        error_model = error_factory(args.error_distr, args.dist_param)
        error = error_model.evaluate_error()
        possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)
        start_prob = transition_prob[0]
        mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                               hidden_states=states, observables=possible_observation,
                                               emission_matrix=emission_prob)

        predict(args.input, args.out, mispelling_model, str(error_model))

    if args.subparser == "bruteforce":
        find_best_score(args.tweets_path, args.corrected_path, args.out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A HMM misspelling correction tool")

    subparser = parser.add_subparsers(dest="subparser")

    single = subparser.add_parser("test")
    single.add_argument("-input", type=str, default="../../dataset/apple_tweets_autowrong.txt ")
    single.add_argument("-out", type=str, default="../../dataset/results/predictions/")
    single.add_argument("-error_dist", type=str, default="Gaussian")
    single.add_argument("-dist_param", type=float, default=0.5)

    brute = subparser.add_parser("bruteforce")

    brute.add_argument("-tweets_path", type=str)
    brute.add_argument("-corrected_path", type=str)
    brute.add_argument("-out_path", type=str)

    args = parser.parse_args()

    main(args)
