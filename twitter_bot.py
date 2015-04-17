import os
import twitter
import markov
import sys

# Use Python os.environ to get at environmental variables
#
# Note: you must run `source secrets.sh` before running this file
# to make sure these environmental variables are set.

api = twitter.Api(
    consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
    consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
    access_token_key=os.environ["TWITTER_ACCESS_TOKEN_KEY"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

# This will print info about credentials to make sure they're correct
# print api.VerifyCredentials()

def main():

    mtg = markov.Twitter(2)
    tweet = mtg.read(sys.argv[1:])
    status = api.PostUpdate(tweet)

    stopped = False
    while not stopped:
        redo = raw_input("Enter to tweet again [q to quit] > ")
        if redo == "q":
            return "Bye Bye"
        mtg = markov.Twitter(2)
        tweet = mtg.read(sys.argv[1:])
        status = api.PostUpdate(tweet)

    print status.text    

if __name__ == "__main__":
    main()
