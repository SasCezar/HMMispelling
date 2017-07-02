import argparse
import csv
import glob
from os import path

import logging

from nltk.corpus import wordnet
from numpy.testing.decorators import deprecated

from HMMispelling.core import keyboard_errors, model
from HMMispelling.iohmms import frequency_parser, tweets_io
from core.keyboard_errors import error_factory
from performance import evaluate


def in_dict_corrected(orig, pred):
    """
    Corrects words using dictionary
    :param orig:
    :param pred:
    :return:
    """
    result = []
    for t, p in zip(orig.split(), pred.split()):
        if t != p and not wordnet.synsets(p.lower()):
            r = t
        else:
            r = p
        if t != p and not wordnet.synsets(t.lower()):
            r = p

        result += [r]

    return " ".join(result)


def __predict_tweets__(tweets, model):
    """
    Predicts the most likely sequence using Viterbi algorithm on the whole tweet
    :param tweets:
    :param model:
    :return:
    """
    corrected_tweets = {}
    for tweet_id in tweets:
        corrected = model.viterbi(tweets[tweet_id])

        if use_dict:
            corrected = in_dict_corrected(tweets[tweet_id], "".join(corrected))

        corrected_tweets[tweet_id] = ''.join(corrected)

    return corrected_tweets


use_dict = True


def __predict_words__(tweets, model):
    """
    Predicts the most likely sequence using Viterbi algorithm on the tweet's words
    :param tweets:
    :param model:
    :return:
    """
    corrected_tweets = {}
    for tweet_id in tweets:
        corrected_tweet = []
        for word in tweets[tweet_id]:
            corrected = model.viterbi(word)

            r = corrected
            if use_dict and not wordnet.synsets(''.join(corrected).lower()):
                r = word
            if use_dict and not wordnet.synsets(word.lower()):
                r = corrected

            corrected_tweet += [''.join(r)]

        corrected_tweets[tweet_id] = ' '.join(corrected_tweet)

    return corrected_tweets


def predict(in_path, out_path, model, params):
    """
    Runs the two types of predition on the input file
    :param in_path:
    :param out_path:
    :param model:
    :param params:
    :return:
    """
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


def load_files(filter, in_path):
    """
    Load all files in a folder and it's subfolder that matches the filter string
    :param filter:
    :param in_path:
    :return:
    """
    files = glob.glob(r'{}**\*{}.txt'.format(in_path, filter), recursive=True)
    return files


@deprecated
def perturbed_corrected_ratio(scores):
    """
    :param scores:
    :return:
    """
    result = scores[(1, 1, 1)] / (scores[(1, 1, 1)] + scores[(1, 1, 0)] + scores[(1, 0, 0)])
    return result


@deprecated
def not_perturbed_not_corrected_ratio(scores):
    result = scores[(0, 0, 1)] / (scores[(0, 0, 1)] + scores[(0, 1, 0)])
    return result


def maxes2csv(results, out_path):
    """
    Writes the performance measures to csv
    :param results:
    :param out_path:
    :return:
    """
    with open(out_path, "wt", encoding="utf8", newline="") as outf:
        writer = csv.writer(outf, delimiter="\t")

        writer.writerow(["File", "Precision", "Recall", "F1", "Accuracy"])

        for result in results:
            writer.writerow([result[0]] + list(result[1]))


def find_max(in_path, out_path):
    """
    Find the best cofiguration of the model from results files
    :param in_path:
    :param out_path:
    :return:
    """
    files = load_files("index", in_path)

    metrics = {}
    for file in files:
        with open(file, "rt", encoding="utf8") as inf:
            reader = csv.reader(inf, delimiter="\t")
            scores = {}
            for key, value in reader:
                scores[eval(key)] = int(value)

            metrics[path.splitext(path.basename(file))[0]] = get_performance_measures(scores)

    results = [(k, metrics[k]) for k in metrics]

    sorted_result = sorted(results, key=lambda v: -v[1][3])

    maxes2csv(sorted_result, out_path)


def get_precision(scores):
    result = scores[(1, 1, 1)] / (scores[(1, 1, 1)] + scores[(1, 1, 0)] + scores[(0, 1, 0)])
    return result


def get_recall(scores):
    result = scores[(1, 1, 1)] / (scores[(1, 1, 1)] + scores[(1, 0, 0)])
    return result


def get_f1_score(precision, recall):
    if recall + precision == 0:
        return 0
    result = 2 * (precision * recall) / (precision + recall)
    return result


def get_accuracy(scores):
    result = (scores[(1, 1, 1)] + scores[(0, 0, 1)]) / (
        scores[(1, 1, 1)] + scores[(1, 0, 0)] + scores[(0, 1, 0)] + scores[(1, 1, 0)] + scores[(0, 0, 1)])
    return result


def get_performance_measures(scores):
    precision = get_precision(scores)
    recall = get_recall(scores)
    f1_score = get_f1_score(precision, recall)
    accuracy = get_accuracy(scores)
    return precision, recall, f1_score, accuracy


word_dict_string = "dict=NLTKWordNet_" if use_dict else ""


def bruteforce(tweets_path, corrected_path, out_path):
    """
    Bruteforce for finding the best parameter configuration
    :param tweets_path:
    :param corrected_path:
    :param out_path:
    :return:
    """
    for trans_file in ["SwiftKey", "Hybrid", "Twitter"]:
        tweet_file_path = tweets_path + "_autowrong.txt"
        states, transition_prob = frequency_parser.load_dataframe(
            "./resources/{}_en_US_letters_frequencies.txt".format(trans_file))
        for error_string in ["Gaussian", "PseudoUniform"]:

            for int_param in range(5, 100, 5):
                param = float(int_param / 100)
                logging.info(
                    "Transition model {} - Error model {} - Model param {}".format(trans_file, error_string, param))
                error_model = error_factory(error_string, param)
                error = error_model.evaluate_error()
                possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)

                start_prob = transition_prob[0]
                mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                                       hidden_states=states, observables=possible_observation,
                                                       emission_matrix=emission_prob)

                tweet_file_corrected, word_file_corrected = predict(tweet_file_path, corrected_path, mispelling_model,
                                                                    word_dict_string + "transition=" + trans_file + "_"
                                                                    + str(error_model))

                file_name, _ = path.splitext(path.basename(tweets_path))
                evaluate.evaluate(tweets_path, tweet_file_corrected, out_path)
                evaluate.evaluate(tweets_path, word_file_corrected, out_path)

        error_string = "Uniform"
        logging.info("Transition model {} - Error model {}".format(trans_file, error_string))
        error_model = error_factory(error_string)
        error = error_model.evaluate_error()
        possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)

        start_prob = transition_prob[0]
        mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                               hidden_states=states, observables=possible_observation,
                                               emission_matrix=emission_prob)

        tweet_file_corrected, word_file_corrected = predict(tweet_file_path, corrected_path, mispelling_model,
                                                            word_dict_string + "transition=" + trans_file + "_" +
                                                            str(error_model))

        file_name, _ = path.splitext(path.basename(tweets_path))
        evaluate.evaluate(tweets_path, tweet_file_corrected, out_path)
        evaluate.evaluate(tweets_path, word_file_corrected, out_path)


def main(args):

    if args.subparser == "test":
        states, transition_prob = frequency_parser.load_dataframe("./resources/SwiftKey_en_US_letters_frequencies.txt")
        error_model = error_factory(args.error_distr, args.dist_param)
        error = error_model.evaluate_error()
        possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)
        start_prob = transition_prob[0]
        mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                               hidden_states=states, observables=possible_observation,
                                               emission_matrix=emission_prob)

        predict(args.input, args.out, mispelling_model, str(error_model))

    if args.subparser == "bruteforce":
        bruteforce(args.tweets_path, args.corrected_path, args.out_path)

    if args.subparser == "find_max":
        find_max(args.res_path, args.out_path)


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(description="A HMM misspelling correction tool")

    subparser = parser.add_subparsers(dest="subparser")

    single = subparser.add_parser("test")
    single.add_argument("-input", type=str, default="../../dataset/apple_tweets_autowrong.txt ")
    single.add_argument("-out", type=str, default="../../results/")
    single.add_argument("-error_dist", type=str, default="Gaussian")
    single.add_argument("-dist_param", type=float, default=0.5)

    brute = subparser.add_parser("bruteforce")

    brute.add_argument("-tweets_path", type=str)
    brute.add_argument("-corrected_path", type=str)
    brute.add_argument("-out_path", type=str)

    f_max = subparser.add_parser("find_max")
    f_max.add_argument("-res_path", type=str)
    f_max.add_argument("-out_path", type=str)

    args = parser.parse_args()

    main(args)
