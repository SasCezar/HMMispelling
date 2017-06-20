##evaluate words
import HMMispelling.iohmms.tweets_io as tweetio
import fileinput
import path

def evaluate(tweets_url):
    tweet_evals = []
    word_evals = []
    for tweet in fileinput.input(tweets_url + "_autowrong.txt", inplace=1):
        tweet = tweet.split(str='\t')

        id = tweet[0]

        truth_tweet = get_word_by_id(id, tweets_url + "_cleaned.txt")
        perturbed_tweet = tweet[1]
        corrected_tweet = get_word_by_id(id, tweets_url + "_corrected.txt")

        #check if the tweet is consistent with the ground truth
        tweet_evals = check(id,corrected_tweet,perturbed_tweet, truth_tweet, tweet_evals)
        #check if every word of the tweet is ocnsistent with the ground truth
        for truth_word, perturbed_word, corrected_word in truth_tweet.split(),perturbed_tweet.split(), corrected_tweet.split():
            word_evals = check(id, corrected_word, perturbed_word, truth_word, word_evals)

    tweetio.write_tweets(tweets_url + "_tweet_evaluation.txt", tweet_evals)
    tweetio.write_tweets(tweets_url + "_word_evaluation.txt", word_evals)

def check(id, corrected, perturbed, truth, evals):
    if corrected == truth:
        evals += [id + '\t' + '1']
    elif corrected == perturbed:
        evals += [id + '\t' + '0']
    else:
        evals += [id + '\t' + '-1']
    return evals


def get_word_by_id(id, file):
    dict = tweetio.open(file)
    return dict[id]

def evaluate_test():
    evaluate("../dataset/apple_tweets")

