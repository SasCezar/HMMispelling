##evaluate words
import HMMispelling.iohmms.tweets_io as tweetio
import fileinput
import path


def evaluate(tweets_url):
    tweets_evals = {}
    words_evals = {}

    perturbed_tweets = tweetio.load_tweets(tweets_url + "_autowrong.txt")
    truth_tweets = tweetio.load_tweets(tweets_url + "_cleaned.txt")
    corrected_tweets = tweetio.load_tweets(tweets_url + "_corrected.txt")
    for tweet_id in truth_tweets:
        truth_tweet = truth_tweets[tweet_id]
        perturbed_tweet = perturbed_tweets[tweet_id]
        corrected_tweet = corrected_tweets[tweet_id]

        # check if the tweet is consistent with the ground truth
        tweets_evals[tweet_id] = check(corrected_tweet, perturbed_tweet, truth_tweet)
        # check if every word of the tweet is consistent with the ground truth

        words_check = []

        for truth_word, perturbed_word, corrected_word in zip(truth_tweet.split(), perturbed_tweet.split(), corrected_tweet.split()):
            words_check += [check(corrected_word, perturbed_word, truth_word)]
            words_evals[tweet_id] = words_check

    tweetio.write_tweets(tweets_url + "_tweet_evaluation.txt", tweets_evals)
    tweetio.write_tweets(tweets_url + "_word_evaluation.txt", words_evals)


def check(corrected, perturbed, truth):
    if corrected == truth:
        return 1
    if corrected == perturbed:
        return 0
    return -1


def evaluate_t():
    evaluate("../../dataset/apple_tweets")


evaluate_t()
