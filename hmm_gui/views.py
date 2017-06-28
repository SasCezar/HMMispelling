import tweepy
from django.shortcuts import render

# Create your views here.
from core import keyboard_errors, model
from core.keyboard_errors import error_factory
from iohmms import frequency_parser
from iohmms.tweets_io import clean
from stream.twitter import TwitterService, TwitterStreamListener


def index(request):
    context = {}
    return render(request, 'HMMFrontEnd/index.html', context)


def search(request):
    text = request.POST.get('search', '')
    result = False
    if len(text) >= 1:
        result = predict(clean(text))

    context = {
        'predicted': result
    }
    print(result)
    return render(request, 'HMMFrontEnd/results.html', context)


DELETE_CHIP = """  <span class="mdl-chip mdl-chip--deletable" style="margin: 0 5px 0 5px ">
    <span class="mdl-chip__text">{}</span>
    <button type="button" class="mdl-chip__action"><i class="material-icons">cancel</i></button>
</span>  """


def live(request):
    return render(request, 'HMMFrontEnd/live.html')


consumer_key = "AHB6bSwBcXsnLzFMh4wDbne27"
consumer_secret = "YCYo9Jv9d3QSbvIZDKYyw1rFccDVLbyjJl7PCZW1ipe304Evlw"
access_token = "3531429916-GJBeBqGlMSREIpOhPuH2LZzavgzkVKVP2NiWLGD"
access_secret = "SlmBNSy1dHcdUw0sthd4oxjpNGLmEtBqnb8Ac48UwszWC"
twitter_connection = TwitterService(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    access_key=access_token, access_secret=access_secret)

last_tweet = None


def save_last_tweet(arg):
    global last_tweet
    last_tweet = arg


tweet_stream = None


def getTweets(key_word):
    twitter_connection.connect()

    api = twitter_connection.api

    stream_listener = TwitterStreamListener(subscribers=[save_last_tweet])

    global tweet_stream
    tweet_stream = tweepy.Stream(auth=api.auth, listener=stream_listener, interval=10)

    tweet_stream.filter(track=[key_word],
                        languages=["en"],
                        async=True)


def difference_results(tweet, corrected):
    result = []
    for orig, correct in zip(tweet.split(), corrected.split()):
        if orig == correct:
            result += [correct]
        else:
            result += [correct + " " + DELETE_CHIP.format(orig)]

    return " ".join(result)


trans_file = "Hybrid"
states, transition_prob = frequency_parser.load_dataframe(
    "HMMispelling/resources/{}_en_US_letters_frequencies.txt".format(trans_file))

error_string = "PseudoUniform"
param = 0.95

error_model = error_factory(error_string, param)
error = error_model.evaluate_error()
possible_observation, emission_prob = keyboard_errors.create_emission_matrix(error)

start_prob = transition_prob[0]
mispelling_model = model.MispellingHMM(start_probability=start_prob, transition_matrix=transition_prob,
                                       hidden_states=states, observables=possible_observation,
                                       emission_matrix=emission_prob)


def predict(sentence):
    predicted = mispelling_model.viterbi(sentence)
    return "".join(predicted)


def stream(request):
    if last_tweet:
        tweet = last_tweet.text
        clean_tweet = clean(tweet)
        corrected = predict(clean_tweet)
        author = last_tweet.user.screen_name
        html_tweet = difference_results(clean_tweet, corrected)
        profile_image = last_tweet.user.profile_image_url
        context = {
            'text': html_tweet,
            'profile_img': profile_image,
            'author': author
        }
    else:
        context = {
            'items': "",
        }

    return render(request, 'HMMFrontEnd/stream.html', context, content_type='text/html')


getTweets("trump")
