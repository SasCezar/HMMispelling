import csv
import re


def clean_tweets(file):

    dict_tweets = edit_tweets(file)
    write_tweets(dict_tweets, file)

    return 0


def edit_tweets(file):

    dict_tweets = {}

    with open(file, 'r', encoding="utf8") as csv_file:
        reader = csv.reader(csv_file, delimiter='\t')

        for tweet_id, tweet in reader:
            tweet_clean = clean(tweet)
            if tweet_clean:
                dict_tweets[tweet_id] = tweet_clean

    return dict_tweets


def write_tweets(dict_tweets, file):

    filename = re.search(r'([^/]*)$', file)
    filename = re.search(r'^[^.]*', filename.group(0))
    filename = filename.group(0) + "_cleaned.txt"

    out_file = open(filename, "w")

    for i in dict_tweets:
        out_file.write(i + "\t" + dict_tweets[i] + "\n")

    out_file.close()

    return 0


def clean(tweet):

    tweet = re.sub(r'@[^\s]*', '', tweet)  # Mentions
    tweet = re.sub(r'htt[^\s]*', '', tweet)  # URLs
    tweet = re.sub(r'[^A-Za-z ]', '', tweet)  # Symbols
    tweet = re.sub(r'\s\s*', ' ', tweet)  # Double spaces
    tweet = re.sub(r'RT', '', tweet)  # RT
    tweet = tweet.strip(' ')  # spaces at head or tail

    return tweet
