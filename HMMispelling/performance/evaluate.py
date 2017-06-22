import HMMispelling.iohmms.tweets_io as tweetio
from os import path, listdir


def count_indexes(tweets_scores):
    indexes = {1: 0, 0: 0, -1: 0}
    total_element = 0
    for tweet_id in tweets_scores:
        for score in tweets_scores[tweet_id]:
            indexes[score] += 1
            total_element += 1
    for value in indexes:
        indexes[value] /= total_element
    return indexes


def load_files(file_name, in_path):
    files = [path.join(in_path, f) for f in listdir(in_path) if path.isfile(path.join(in_path, f)) if file_name in f]
    return files


def evaluate(tweets_path, corrected_path, out_path):
    tweets_evals = {}
    words_evals = {}

    file_name, _ = path.splitext(path.basename(tweets_path))

    perturbed_tweets = tweetio.load_tweets(tweets_path + "_autowrong.txt")
    truth_tweets = tweetio.load_tweets(tweets_path + "_cleaned.txt")

    corrected_files = load_files(file_name, corrected_path)

    for corrected_file in corrected_files:

        correct_file_name, _ = path.splitext(path.basename(corrected_file))

        corrected_tweets = tweetio.load_tweets(corrected_file)
        for tweet_id in truth_tweets:
            truth_tweet = truth_tweets[tweet_id]
            perturbed_tweet = perturbed_tweets[tweet_id]
            corrected_tweet = corrected_tweets[tweet_id]

            # check if the tweet is consistent with the ground truth
            tweets_evals[tweet_id] = [check(corrected_tweet, perturbed_tweet, truth_tweet)]

            # check if every word of the tweet is consistent with the ground truth
            words_check = []

            for truth_word, perturbed_word, corrected_word in zip(truth_tweet.split(), perturbed_tweet.split(),
                                                                  corrected_tweet.split()):
                words_check += [check(corrected_word, perturbed_word, truth_word)]
                words_evals[tweet_id] = words_check

        tweetio.write_tweets(path.join(out_path, correct_file_name + "_tweet_evaluation.txt"), tweets_evals)
        tweetio.write_tweets(path.join(out_path, correct_file_name + "_word_evaluation.txt"), words_evals)

        tweets_index = count_indexes(tweets_evals)
        words_index = count_indexes(words_evals)

        tweetio.write_tweets(path.join(out_path, correct_file_name + "_tweet_evaluation_index.txt"), tweets_index)
        tweetio.write_tweets(path.join(out_path, correct_file_name + "_word_evaluation_index.txt"), words_index)

        return tweets_index, words_index


def check(corrected, perturbed, truth):
    if corrected == truth:
        return 1
    if corrected == perturbed:
        return 0
    return -1


def evaluate_t():
    evaluate("../../dataset/apple_tweets", "../../results/predictions/", "../../results/performance")


evaluate_t()
