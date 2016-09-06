import csv
import json
import time

import tweepy


# You must use Python 3.0 or above
# For those who have been using python 2.7.x before, here is an article explaining key differences between python 2.7x & 3.x
# http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put in your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    with open(key_file) as data_file:
        keys = json.load(data_file)
    return keys['api_key'], keys['api_secret'], keys['token'], keys['token_secret']


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


# Q1.b - 5 Marks
def getFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
    # rtype: list containing entries in the form of a tuple (follower, root_user)
    followers = list()
    for follower in zip(range(no_of_followers),
                        limit_handled(tweepy.Cursor(api.followers, screen_name=root_user).items())):
        followers.append((follower, root_user))
    return followers


# Q1.b - 7 Marks
def getSecondaryFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    secondary_followers = list()
    for follower in followers_list:
        for secondary_follower in zip(range(no_of_followers),
                                      limit_handled(tweepy.Cursor(api.followers, screen_name=follower).items())):
            secondary_followers.append((secondary_follower, follower))
    return secondary_followers


# Q1.c - 5 Marks
def getFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    friends = list()
    for friend in zip(range(no_of_friends), limit_handled(tweepy.Cursor(api.friends, screen_name=root_user).items())):
        friends.append((friend, root_user))
    return friends


# Q1.c - 7 Marks
def getSecondaryFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    secondary_friends = list()
    for friend in friends_list:
        for secondary_friend in zip(range(no_of_friends),
                                    limit_handled(tweepy.Cursor(api.friends, screen_name=friend).items())):
            secondary_friends.append((friend, secondary_friend))
    return secondary_friends


# Q1.b, Q1.c - 6 Marks
def writeToFile(data, output_file):
    with open(output_file, 'wb') as csvfile:
        data_wrirwe = csv.writer(csvfile, delimiter=' ')
        for tuple in data:
            data_wrirwe.writerow(tuple)


"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""


def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'

    ROOT_USER = 'PoloChau'
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10

    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
    followers = primary_followers + secondary_followers

    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
    friends = primary_friends + secondary_friends

    writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    writeToFile(friends, OUTPUT_FILE_FRIENDS)


if __name__ == '__main__':
    testSubmission()
