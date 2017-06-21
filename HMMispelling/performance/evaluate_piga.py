##evaluate words
import HMMispelling.iohmms.tweets_io as tweetio
from collections import defaultdict
import fileinput
from os import path

def evaluate(tweets_url):
    tweet_evals = []
    word_evals = []

    basedir_tweet = path.dirname(tweets_url)
    file_name, extension = path.splitext(path.basename(tweets_url))
    file_name = file_name.split("_")[0]
    truth_tweets = tweetio.load_tweets("../../dataset/" + file_name + "_tweets_cleaned" + extension)
    perturbed_tweets = tweetio.load_tweets("../../dataset/" + file_name + "_tweets_autowrong" + extension)
    corrected_tweets = tweetio.load_tweets(tweets_url)

    for tweet_id in truth_tweets:
        truth_tweet = truth_tweets[tweet_id]
        perturbed_tweet = perturbed_tweets[tweet_id]
        corrected_tweet = corrected_tweets[tweet_id]

        #check if the tweet is consistent with the ground truth
        tweet_evals += check(tweet_id,corrected_tweet,perturbed_tweet, truth_tweet)
        #check if every word of the tweet is ocnsistent with the ground truth
        for truth_word, perturbed_word, corrected_word in zip(truth_tweet.split(), perturbed_tweet.split(), corrected_tweet.split()):
            word_evals += check(tweet_id, corrected_word, perturbed_word, truth_word)



    dict_tweets = dict(tweet_evals)
    dict_words = {}
    for key, value in word_evals:
        if key not in dict_words:
            dict_words[key] = []
        dict_words[key] = dict_words[key] + value

    tweetio.write_tweets(path.join(basedir_tweet,file_name +"_evaluation" + extension), dict_tweets)
    tweetio.write_tweets(path.join(basedir_tweet,file_name + "_evaluation" + extension), dict_words)

    tweet_indexes = count_indexes(dict_tweets)
    word_indexes = count_indexes(dict_words)

    tweetio.write_tweets(path.join(basedir_tweet,file_name + "_tweet_evaluation_index" + extension), tweet_indexes)
    tweetio.write_tweets(path.join(basedir_tweet,file_name + "_word_evaluation_index" + extension), word_indexes)

def count_indexes(d):
    dict_values = {1:0, 0:0, -1:0}
    total_element = 0
    for x in d:
        for value in d[x]:
            dict_values[value] += 1
            total_element += 1
    for y in dict_values:
        dict_values[y] = dict_values[y]/total_element
    return dict_values


def check(id, corrected, perturbed, truth):
    if corrected == truth:
        return [(id, [1])]
    elif corrected == perturbed:
        return [(id, [0])]
    else:
        return [(id, [-1])]

def evaluate_tweet():
    evaluate("../../dataset/apple_tweets_corrected.txt")


evaluate_tweet()